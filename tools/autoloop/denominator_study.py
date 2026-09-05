#!/usr/bin/env python3
"""autoloop — the denominator study (session 152, 2026-09-05).

Tests the PRE-CHECK stage of `liveness.py` against three committed null worlds, and computes
what the loop's three denominators become when the impossible questions are removed from them.

Everything reads committed files. No network call is made and none is needed.

Usage:
  python3 tools/autoloop/denominator_study.py --out <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import random
import statistics
import sys
import time

import dial
import liveness
from stats import benjamini_hochberg

ALPHA = 0.05
BH_Q = 0.05
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A150 = os.path.join(ROOT, "artifacts/cycle-002/2026-09-03-a-loop-that-finds-things/data")
D151 = os.path.join(ROOT, "artifacts/cycle-002/2026-09-04-the-dial/data")


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return ((c - h) / d, (c + h) / d)


def load_datasets():
    """A, B, C of PREREGISTRATION.md §3 — corpus, question space, observed null hit counts."""
    out = {}

    res = json.load(open(os.path.join(A150, "results.json")))
    hits = res["M3_null_world"]["per_test_hits"]
    reps = res["M3_null_world"]["replicates"]
    out["A"] = {
        "label": "arXiv, session 150", "space": "arxiv",
        "corpus": os.path.join(A150, "corpus.json"),
        "replicates": reps, "seed": res["M3_null_world"]["seed"],
        "hits": hits,
        "real": {c["key"]: {"p": c["p"], "failures": c["failures"]} for c in res["claims"]},
        "published_per_test_rate": res["M3_null_world"]["per_test_rejection_rate"],
    }

    for key, space in (("B", "arxiv"), ("C", "crossref")):
        sw = json.load(open(os.path.join(D151, f"sweep-{space}.json")))
        reps = sw["replicates"]
        out[key] = {
            "label": f"{'arXiv' if space == 'arxiv' else 'Crossref'}, session 151",
            "space": space,
            "corpus": os.path.join(D151, f"corpus-{space}.json"),
            "replicates": reps, "seed": sw["seed"],
            # the sweep stores a RATE per question; the hit count is rate * replicates
            "hits": {k: int(round(v * reps)) for k, v in sw["per_question_null_rate"].items()},
            "real": {k: {"p": v["p"], "failures": v["failures"]} for k, v in sw["tests"].items()},
            "published_per_test_rate": sw["null"]["lean@66"]["per_test_rate"],
        }
    return out


def liveness_for(space_name, records, questions=None):
    space = dial.SPACES[space_name]
    qs = questions or dial.enumerate_questions(space)
    return liveness.assess(records, {g: v[0] for g, v in space["groupings"].items()},
                           space["numeric"], space["binary"], qs)


# --- P1, P2 ---------------------------------------------------------------------------------

def soundness_completeness(lv, hits):
    asleep = set(lv["asleep"])
    zero = {k for k, v in hits.items() if v == 0}
    fired_asleep = sorted(k for k in asleep if hits.get(k, 0) > 0)
    missed = sorted(zero - asleep)
    return {
        "asleep": sorted(asleep), "observed_zero": sorted(zero),
        "P1_violations": fired_asleep,          # asleep questions that fired -> kills the rule
        "P2_violations": missed,                # zero-rate questions the rule calls awake
        "P1_holds": not fired_asleep,
        "P2_holds": not missed,
    }


# --- K2: liveness is invariant under the permutation the null world uses ---------------------

def k2_invariance(space_name, records, replicates, seed):
    """Rebuild the corpus with the grouping block permuted, exactly as null_world does, and
    recompute liveness from the permuted records. The partition must not move."""
    space = dial.SPACES[space_name]
    gnames = list(space["groupings"])
    base = liveness_for(space_name, records)
    base_awake = set(base["awake"])
    rng = random.Random(seed)
    n = len(records)
    order = list(range(n))
    # the grouping block is the set of record fields the grouping predicates read
    gfields = sorted({space["groupings"][g][2] for g in gnames})
    moves = 0
    for _ in range(replicates):
        rng.shuffle(order)
        permuted = []
        for i in range(n):
            r = dict(records[i])
            src = records[order[i]]
            for f in gfields:
                r[f] = src.get(f)
            permuted.append(r)
        lv = liveness_for(space_name, permuted)
        if set(lv["awake"]) != base_awake:
            moves += 1
    return {"replicates": replicates, "partitions_that_moved": moves, "K2_holds": moves == 0}


# --- P3: the awake denominator, and the adversary's random-trim control ----------------------

def rates(hits, keys, replicates):
    tests = replicates * len(keys)
    rej = sum(hits[k] for k in keys)
    lo, hi = wilson(rej, tests)
    return {"questions": len(keys), "tests": tests, "rejections": rej,
            "per_test_rate": (rej / tests) if tests else None, "ci95": [lo, hi]}


def random_trim_control(hits, size, replicates, draws, seed):
    """The 2026-09-04 adversary's objection, run as a control: what does a trim of this size
    buy for no reason at all?"""
    keys = sorted(hits)
    rng = random.Random(seed)
    vals = []
    for _ in range(draws):
        sub = rng.sample(keys, size)
        vals.append(sum(hits[k] for k in sub) / (replicates * size))
    vals.sort()
    def pct(q):
        return vals[min(len(vals) - 1, int(q * len(vals)))]
    return {"draws": draws, "subset_size": size, "mean": statistics.fmean(vals),
            "p2_5": pct(0.025), "p50": pct(0.5), "p97_5": pct(0.975), "max": vals[-1]}


def lowest_rate_trim(hits, size, replicates):
    """The adversary's own trim: drop the questions with the LOWEST observed rates."""
    keys = sorted(hits, key=lambda k: (hits[k], k))
    kept = keys[len(keys) - size:]
    return rates(hits, kept, replicates)


# --- P4, P5 ---------------------------------------------------------------------------------

def review_comparison(lv, real):
    asleep = set(lv["asleep"])
    killed = {k for k, v in real.items() if v["failures"]}
    return {
        "asleep": len(asleep), "review_killed": len(killed),
        "asleep_and_killed": len(asleep & killed),
        "asleep_passing_review": sorted(asleep - killed),
        "killed_but_awake": sorted(killed - asleep),
        "sets_coincide": asleep == killed,
        # a question can be AWAKE (some labelling reaches alpha) and still return no p-value in
        # THIS world, because the labelling this world happens to carry is a degenerate one.
        # The rule is about reachability, not about one draw; these are the cases where the
        # difference shows.
        "awake_without_p_in_this_world": sorted(k for k in lv["awake"]
                                                if real.get(k, {}).get("p") is None),
    }


def bh_comparison(lv, real):
    awake = set(lv["awake"])
    all_keys = [k for k in sorted(real) if real[k]["p"] is not None]
    all_p = [real[k]["p"] for k in all_keys]
    bh_all = {all_keys[i] for i in benjamini_hochberg(all_p, BH_Q)}
    aw_keys = [k for k in all_keys if k in awake]
    aw_p = [real[k]["p"] for k in aw_keys]
    bh_aw = {aw_keys[i] for i in benjamini_hochberg(aw_p, BH_Q)}
    return {
        "denominator_all": len(all_keys), "denominator_awake": len(aw_keys),
        "bh_survivors_all": len(bh_all), "bh_survivors_awake": len(bh_aw),
        "gained": sorted(bh_aw - bh_all), "lost": sorted(bh_all - bh_aw),
        "raw_findings_all": sum(1 for k in all_keys
                                if real[k]["p"] < ALPHA and not real[k]["failures"]),
    }


# --- post-hoc: the awake curve, and the rule tested where it does real work ------------------

def awake_curve(space_name, records, sizes, replicates, seed):
    """POST-HOC (not in the pre-registration; labelled as such on the page).

    On the two corpora at hand the rule only ever fires on a grouping that is constant, so its
    soundness has been tested only in its trivial regime. Shrinking the corpus makes questions
    genuinely impossible for reasons of size rather than degeneracy. At each size the rule's
    verdict is compared against an actual null world of the same size.
    """
    space = dial.SPACES[space_name]
    qs = dial.enumerate_questions(space)
    out = []
    for n in sizes:
        sub = records[:n]
        lv = liveness_for(space_name, sub)
        breaks = []
        preps = {o: dial.prepare_outcome(space, sub, o) for o in {o for _, o in qs}}
        gcols = {g: [bool(space["groupings"][g][0](r)) for r in sub] for g in space["groupings"]}
        cells = {"all": qs}
        null, per_q, _secs = dial.null_sweep(space, sub, cells, preps, gcols,
                                             replicates, seed, breaks)
        hits = {k: int(round(v * replicates)) for k, v in per_q.items()}
        sc = soundness_completeness(lv, hits)
        aw = rates(hits, lv["awake"], replicates) if lv["awake"] else None
        allr = rates(hits, sorted(hits), replicates)
        out.append({
            "n": n, "awake": lv["awake_count"], "asleep": lv["asleep_count"],
            "asleep_with_nondegenerate_grouping": sum(
                1 for k in lv["asleep"]
                if 0 < lv["detail"][k]["G"] < lv["detail"][k]["N"]),
            "P1_violations": sc["P1_violations"], "P2_violations": sc["P2_violations"],
            "P1_opportunities": lv["asleep_count"] * replicates,
            "observed_zero": len(sc["observed_zero"]),
            "rate_all": allr["per_test_rate"], "rate_awake": aw["per_test_rate"] if aw else None,
            "ci_all": allr["ci95"], "ci_awake": aw["ci95"] if aw else None,
            "breaks": len(breaks),
        })
        print(f"    n={n:5d}  awake {lv['awake_count']:2d}  asleep {lv['asleep_count']:2d}  "
              f"P1v {len(sc['P1_violations'])}  P2v {len(sc['P2_violations'])}  "
              f"all {allr['per_test_rate']*100:5.2f} %  "
              f"awake {(aw['per_test_rate']*100 if aw else float('nan')):5.2f} %", file=sys.stderr)
    return out


def bh_on_subsamples(space_name, records, sizes):
    """POST-HOC. P5 was refuted on the three full datasets, but VACUOUSLY: there, every asleep
    question is exactly a question whose test returns no p-value, so the two BH denominators are
    the same list and the comparison had no content. A question can in principle be asleep and
    still produce a p-value — floor >= alpha with a computable statistic — and that happens on
    smaller corpora. This runs P5's comparison where it can actually come out either way."""
    space = dial.SPACES[space_name]
    qs = dial.enumerate_questions(space)
    out = []
    for n in sizes:
        sub = records[:n]
        lv = liveness_for(space_name, sub)
        breaks = []
        full, _preps, _g = dial.real_battery(space, sub, qs, breaks, f"sub{n}")
        real = {k: {"p": v["p"], "failures": v["failures"]} for k, v in full.items()}
        cmp_ = bh_comparison(lv, real)
        asleep_with_p = sorted(k for k in lv["asleep"]
                               if real.get(k, {}).get("p") is not None)
        out.append({"n": n, "asleep": lv["asleep_count"],
                    "asleep_with_a_p_value": len(asleep_with_p),
                    "test_has_content": bool(asleep_with_p), **cmp_, "breaks": len(breaks)})
        print(f"    n={n:5d}  asleep {lv['asleep_count']:2d}  of those with a p {len(asleep_with_p):2d}"
              f"  BH all {cmp_['bh_survivors_all']:2d} (m={cmp_['denominator_all']:2d})"
              f"  BH awake {cmp_['bh_survivors_awake']:2d} (m={cmp_['denominator_awake']:2d})",
              file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--k2-replicates", type=int, default=200)
    ap.add_argument("--curve-replicates", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260905)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    t0 = time.time()

    ds = load_datasets()
    report = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "alpha": ALPHA, "bh_q": BH_Q, "seed": args.seed, "datasets": {}}

    for key in ("A", "B", "C"):
        d = ds[key]
        records = json.load(open(d["corpus"]))["records"]
        lv = liveness_for(d["space"], records)
        sc = soundness_completeness(lv, d["hits"])
        reps = d["replicates"]
        all_rates = rates(d["hits"], sorted(d["hits"]), reps)
        awake_rates = rates(d["hits"], lv["awake"], reps)
        entry = {
            "label": d["label"], "space": d["space"], "records": len(records),
            "replicates": reps, "null_seed": d["seed"],
            "published_per_test_rate": d["published_per_test_rate"],
            "liveness": {"awake": lv["awake_count"], "asleep": lv["asleep_count"],
                         "asleep_keys": lv["asleep"],
                         "floors": {k: v["reachable_floor"] for k, v in lv["detail"].items()},
                         "margins": {k: {"G": v["G"], "N": v["N"], "m": v["m"],
                                         "n1_range": v["n1_range"]}
                                     for k, v in lv["detail"].items()}},
            "P1_P2": sc,
            "rate_all_questions": all_rates,
            "rate_awake_only": awake_rates,
            "P4_review": review_comparison(lv, d["real"]),
            "P5_multiplicity": bh_comparison(lv, d["real"]),
        }
        # POST-HOC, labelled: the rival denominator. The "as-run" denominator a convened
        # adversary flagged on 2026-09-03 was the set of questions that SURVIVE review. It is
        # not the same fix: review kills questions on grounds of power, and a question killed
        # for want of power still fires in an empty world at about alpha.
        survivors = [k for k in sorted(d["hits"]) if not d["real"].get(k, {}).get("failures")]
        entry["post_hoc_rate_review_survivors"] = rates(d["hits"], survivors, reps)
        # how much opportunity P1 was actually given
        entry["P1_opportunities"] = len(lv["asleep"]) * reps
        if lv["asleep_count"]:
            entry["control_random_trim"] = random_trim_control(
                d["hits"], lv["awake_count"], reps, 10000, args.seed)
            entry["control_lowest_rate_trim"] = lowest_rate_trim(
                d["hits"], lv["awake_count"], reps)
        # POST-HOC: how much the answer depends on the SIZE of the trim, so the page can say
        # what would have happened had the rule returned a different count.
        entry["post_hoc_trim_sensitivity"] = {
            str(drop): lowest_rate_trim(d["hits"], len(d["hits"]) - drop, reps)["per_test_rate"]
            for drop in (0, 5, 9, 15, 25)}
        report["datasets"][key] = entry
        print(f"  {key} {d['label']}: awake {lv['awake_count']}, asleep {lv['asleep_count']}, "
              f"all {all_rates['per_test_rate']*100:.2f} %, "
              f"awake-only {awake_rates['per_test_rate']*100:.2f} %, "
              f"P1 {'ok' if sc['P1_holds'] else 'FAILED'}, "
              f"P2 {'ok' if sc['P2_holds'] else 'FAILED'}", file=sys.stderr)

    # P3, over B and C
    b, c = report["datasets"]["B"], report["datasets"]["C"]
    lo_b, hi_b = b["rate_awake_only"]["ci95"]
    lo_c, hi_c = c["rate_awake_only"]["ci95"]
    band = (0.045, 0.055)
    report["P3"] = {
        "B_rate": b["rate_awake_only"]["per_test_rate"], "B_ci": [lo_b, hi_b],
        "C_rate": c["rate_awake_only"]["per_test_rate"], "C_ci": [lo_c, hi_c],
        "intervals_overlap": not (hi_b < lo_c or hi_c < lo_b),
        "both_in_band": all(band[0] <= r <= band[1] for r in
                            (b["rate_awake_only"]["per_test_rate"],
                             c["rate_awake_only"]["per_test_rate"])),
        "published_B_ci": b["rate_all_questions"]["ci95"],
        "published_C_ci": c["rate_all_questions"]["ci95"],
        "published_intervals_overlap": not (
            b["rate_all_questions"]["ci95"][1] < c["rate_all_questions"]["ci95"][0]
            or c["rate_all_questions"]["ci95"][1] < b["rate_all_questions"]["ci95"][0]),
    }
    report["P3"]["holds"] = report["P3"]["intervals_overlap"] and report["P3"]["both_in_band"]

    # K2
    print("  K2: liveness under the null world's own permutation", file=sys.stderr)
    report["K2"] = {}
    for key in ("B", "C"):
        recs = json.load(open(ds[key]["corpus"]))["records"]
        report["K2"][key] = k2_invariance(ds[key]["space"], recs,
                                          args.k2_replicates, args.seed)
        print(f"    {key}: moved {report['K2'][key]['partitions_that_moved']} of "
              f"{args.k2_replicates}", file=sys.stderr)

    # post-hoc curve
    print("  POST-HOC: the awake curve", file=sys.stderr)
    report["post_hoc_awake_curve"] = {}
    sizes = [40, 60, 80, 120, 200, 400, 800, 2000]
    for key in ("B", "C"):
        recs = json.load(open(ds[key]["corpus"]))["records"]
        print(f"   {key} {ds[key]['label']}", file=sys.stderr)
        report["post_hoc_awake_curve"][key] = awake_curve(
            ds[key]["space"], recs, [s for s in sizes if s <= len(recs)],
            args.curve_replicates, args.seed)

    print("  POST-HOC: P5 where it can come out either way", file=sys.stderr)
    report["post_hoc_bh_on_subsamples"] = {}
    for key in ("B", "C"):
        recs = json.load(open(ds[key]["corpus"]))["records"]
        print(f"   {key} {ds[key]['label']}", file=sys.stderr)
        report["post_hoc_bh_on_subsamples"][key] = bh_on_subsamples(
            ds[key]["space"], recs, [s for s in sizes if s <= len(recs)])

    report["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(args.out, "denominator.json"), "w") as f:
        json.dump(report, f, indent=1, sort_keys=True)
    print(f"written in {report['seconds']} s", file=sys.stderr)


if __name__ == "__main__":
    main()
