#!/usr/bin/env python3
"""autoloop — stages QUESTION, EXPERIMENT, ANALYSIS, WRITE.

Runs the whole hypothesis space fixed in the pre-registration against a committed
corpus, applies the review pre-conditions, corrects for multiplicity, replicates on a
split half, and calibrates itself against a null world in which every grouping-outcome
association has been destroyed by permutation.

Every stage failure is appended to the break log instead of raising: a loop that dies
on its first bad cell measures nothing about where loops break.

Usage:
  python3 tools/autoloop/loop.py --corpus <corpus.json> --out <results.json> \
      [--replicates 500] [--seed 20260903]
"""

import argparse
import json
import random
import statistics
import sys
import time

from stats import (average_ranks, benjamini_hochberg, mannwhitney_from_ranks,
                   normal_two_sided_p, two_proportion)

ALPHA = 0.05
BH_Q = 0.05

# --- the hypothesis space, fixed in PREREGISTRATION.md §3 -----------------------------

GROUPINGS = {
    "weekend":          (lambda r: r["published_weekday"] >= 5,               "published at a weekend (UTC)"),
    "has_doi":          (lambda r: r["has_doi"],                              "carries a DOI"),
    "has_journal_ref":  (lambda r: r["has_journal_ref"],                      "carries a journal reference"),
    "has_comment":      (lambda r: r["has_comment"],                          "carries an author comment"),
    "revised":          (lambda r: r["revised"],                              "was revised after posting"),
    "cross_listed":     (lambda r: r["category_count"] > 1,                   "is cross-listed"),
    "large_team":       (lambda r: r["author_count"] >= 5,                    "has five or more authors"),
    "night_submission": (lambda r: r["published_hour_utc"] >= 22 or r["published_hour_utc"] < 6,
                                                                              "was posted between 22:00 and 06:00 UTC"),
}

NUMERIC_OUTCOMES = {
    "title_words":        "title length in words",
    "abstract_words":     "abstract length in words",
    "author_count":       "number of authors",
    "category_count":     "number of categories",
    "comment_pages":      "page count stated in the author comment",
    "published_hour_utc": "hour of posting (UTC)",
}
BINARY_OUTCOMES = {
    "has_doi":         "carrying a DOI",
    "has_journal_ref": "carrying a journal reference",
    "revised":         "having been revised after posting",
}

EXCLUDED_PAIRS = {
    ("has_doi", "has_doi"),
    ("has_journal_ref", "has_journal_ref"),
    ("revised", "revised"),
    ("cross_listed", "category_count"),
    ("large_team", "author_count"),
    ("night_submission", "published_hour_utc"),
}


def value(rec, name):
    v = rec.get(name)
    if isinstance(v, bool):
        return 1 if v else 0
    return v


def enumerate_questions():
    """Stage QUESTION. No human picks which of these is worth asking."""
    pairs = []
    for g in GROUPINGS:
        for o in list(NUMERIC_OUTCOMES) + list(BINARY_OUTCOMES):
            if (g, o) in EXCLUDED_PAIRS:
                continue
            pairs.append((g, o))
    return pairs


# --- one test -------------------------------------------------------------------------

def prepare_outcome(records, outcome):
    """Index list of records with a non-missing outcome, plus ranks for the numeric case."""
    idx = [i for i, r in enumerate(records) if value(r, outcome) is not None]
    vals = [value(records[i], outcome) for i in idx]
    if outcome in NUMERIC_OUTCOMES:
        ranks, tie_term = average_ranks(vals)
        return {"idx": idx, "vals": vals, "ranks": ranks, "tie": tie_term, "kind": "numeric"}
    return {"idx": idx, "vals": vals, "ranks": None, "tie": None, "kind": "binary"}


def run_test(prep, groups, outcome):
    """EXPERIMENT. `groups` is a boolean list aligned to the full record list."""
    idx, vals, kind = prep["idx"], prep["vals"], prep["kind"]
    g1 = [k for k, i in enumerate(idx) if groups[i]]
    g0 = [k for k, i in enumerate(idx) if not groups[i]]
    n1, n0 = len(g1), len(g0)
    if kind == "numeric":
        ranks = prep["ranks"]
        rs1 = 0.0
        for k in g1:
            rs1 += ranks[k]
        u1, z, p, rb = mannwhitney_from_ranks(rs1, n1, n0, prep["tie"])
        med1 = statistics.median([vals[k] for k in g1]) if n1 else None
        med0 = statistics.median([vals[k] for k in g0]) if n0 else None
        distinct = len(set(vals))
        return {"test": "mann-whitney-u", "n1": n1, "n0": n0, "z": z, "p": p,
                "effect": rb, "effect_kind": "rank-biserial",
                "summary1": med1, "summary0": med0, "summary_kind": "median",
                "distinct_values": distinct, "events1": None, "events0": None}
    x1 = sum(vals[k] for k in g1)
    x0 = sum(vals[k] for k in g0)
    z, p, rd = two_proportion(x1, n1, x0, n0)
    return {"test": "two-proportion-z", "n1": n1, "n0": n0, "z": z, "p": p,
            "effect": rd, "effect_kind": "risk-difference-points",
            "summary1": (100.0 * x1 / n1 if n1 else None),
            "summary0": (100.0 * x0 / n0 if n0 else None),
            "summary_kind": "percent", "distinct_values": len(set(vals)),
            "events1": x1, "events0": x0}


def preconditions(res, n_total, n_corpus):
    """REVIEW's pre-conditions c1-c4, pre-registered. Returns the list of failures."""
    fails = []
    if res["n1"] < 30 or res["n0"] < 30:
        fails.append("c1 group smaller than 30")
    if res["test"] == "two-proportion-z":
        if res["events1"] is None or min(res["events1"], res["n1"] - res["events1"],
                                         res["events0"], res["n0"] - res["events0"]) < 10:
            fails.append("c2 fewer than 10 events or non-events in a group")
    else:
        if res["distinct_values"] < 5:
            fails.append("c3 fewer than 5 distinct outcome values")
    if n_total < 0.5 * n_corpus:
        fails.append("c4 outcome missing for more than half the corpus")
    return fails


# --- WRITE ----------------------------------------------------------------------------

def claim_sentence(g, o, res):
    """Stage WRITE. A template, not a writer: it cannot invent a number, and it cannot
    notice that a claim is empty. Both halves of that are the point."""
    gdesc = GROUPINGS[g][1]
    higher = "higher" if (res["effect"] or 0) > 0 else "lower"
    if res["test"] == "mann-whitney-u":
        odesc = NUMERIC_OUTCOMES[o]
        return (f"Papers where the paper {gdesc} have {higher} {odesc} than papers where it does not: "
                f"median {fmt(res['summary1'])} against {fmt(res['summary0'])}, "
                f"rank-biserial {res['effect']:+.3f}, p = {pfmt(res['p'])} "
                f"(Mann-Whitney U, n = {res['n1']} against {res['n0']}).")
    odesc = BINARY_OUTCOMES[o]
    return (f"Papers where the paper {gdesc} differ in {odesc}: "
            f"{res['summary1']:.1f} % against {res['summary0']:.1f} %, "
            f"a difference of {res['effect']:+.1f} points, p = {pfmt(res['p'])} "
            f"(two-proportion z, n = {res['n1']} against {res['n0']}).")


def fmt(v):
    if v is None:
        return "n/a"
    return f"{v:g}"


def pfmt(p):
    if p is None:
        return "n/a"
    if p < 1e-4:
        return "<0.0001"
    return f"{p:.4f}"


# --- the null world -------------------------------------------------------------------

def null_world(records, pairs, preps, group_cols, replicates, seed, breaks):
    """M3. The grouping block is row-permuted jointly: every grouping-outcome association
    is destroyed, the dependence among groupings and among outcomes is preserved."""
    rng = random.Random(seed)
    n = len(records)
    per_run = []
    per_test_hits = {f"{g}|{o}": 0 for g, o in pairs}
    order = list(range(n))
    exemplar = None          # one whole draw, kept so the figure can show a null world
    first_at = {}            # yield -> the first replicate that produced it
    t0 = time.time()
    for rep in range(replicates):
        rng.shuffle(order)
        permuted = {g: [col[order[i]] for i in range(n)] for g, col in group_cols.items()}
        hits = 0
        draw = {}
        for g, o in pairs:
            try:
                res = run_test(preps[o], permuted[g], o)
            except Exception as e:
                breaks.append({"stage": "EXPERIMENT", "kind": "null_test_error",
                               "where": f"{g}|{o}@rep{rep}", "detail": str(e)[:160]})
                continue
            draw[f"{g}|{o}"] = {"p": res["p"], "effect": res["effect"]}
            if res["p"] is not None and res["p"] < ALPHA:
                hits += 1
                per_test_hits[f"{g}|{o}"] += 1
        per_run.append(hits)
        # Keep the first draw seen at each yield, so that after the run one *typical* null
        # world - the first replicate whose yield equals the median - can be shown whole.
        first_at.setdefault(hits, {"replicate": rep, "hits": hits, "tests": draw})
    exemplar = first_at.get(int(statistics.median(per_run)))
    return {
        "exemplar_run": exemplar,
        "replicates": replicates,
        "seed": seed,
        "seconds": round(time.time() - t0, 1),
        "findings_per_run_mean": sum(per_run) / len(per_run),
        "findings_per_run_median": statistics.median(per_run),
        "findings_per_run_max": max(per_run),
        "findings_per_run_min": min(per_run),
        "runs_with_at_least_one": sum(1 for h in per_run if h >= 1),
        "histogram": {str(k): per_run.count(k) for k in sorted(set(per_run))},
        "tests_total": replicates * len(pairs),
        "rejections_total": sum(per_run),
        "per_test_rejection_rate": sum(per_run) / (replicates * len(pairs)),
        "per_test_hits": per_test_hits,
    }


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return ((c - h) / d, (c + h) / d)


def battery(records, pairs, breaks, label):
    """Run the whole space once against a record list. Returns per-pair results."""
    preps = {o: prepare_outcome(records, o) for o in set(o for _, o in pairs)}
    group_cols = {g: [bool(fn(r)) for r in records] for g, (fn, _) in GROUPINGS.items()}
    out = {}
    for g, o in pairs:
        key = f"{g}|{o}"
        try:
            res = run_test(preps[o], group_cols[g], o)
        except Exception as e:
            breaks.append({"stage": "EXPERIMENT", "kind": "test_error", "where": f"{key}@{label}",
                           "detail": str(e)[:160]})
            continue
        if res["p"] is None:
            breaks.append({"stage": "EXPERIMENT", "kind": "degenerate_test", "where": f"{key}@{label}",
                           "detail": "no p-value computable (zero variance or empty group)"})
        res["failures"] = preconditions(res, len(preps[o]["idx"]), len(records))
        out[key] = res
    return out, preps, group_cols


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--replicates", type=int, default=500)
    ap.add_argument("--seed", type=int, default=20260903)
    args = ap.parse_args()

    with open(args.corpus) as f:
        corpus = json.load(f)
    records = corpus["records"]
    breaks = []

    pairs = enumerate_questions()
    print(f"QUESTION: {len(pairs)} hypotheses enumerated", file=sys.stderr)

    full, preps, group_cols = battery(records, pairs, breaks, "full")

    # ANALYSIS: multiplicity over the tests that survived the pre-conditions.
    keys = [k for k in full if not full[k]["failures"] and full[k]["p"] is not None]
    pvals = [full[k]["p"] for k in keys]
    bh = benjamini_hochberg(pvals, BH_Q)
    bh_keys = {keys[i] for i in bh}
    bonf = {k for k, p in zip(keys, pvals) if p < ALPHA / len(keys)} if keys else set()

    # M6 split-half by the parity of the last digit of the arXiv identifier.
    even = [r for r in records if int(r["id"][-1]) % 2 == 0]
    odd = [r for r in records if int(r["id"][-1]) % 2 == 1]
    half_a, _, _ = battery(even, pairs, breaks, "half-even")
    half_b, _, _ = battery(odd, pairs, breaks, "half-odd")

    claims = []
    for k in sorted(full, key=lambda k: (full[k]["p"] is None, full[k]["p"])):
        g, o = k.split("|")
        res = full[k]
        sig = res["p"] is not None and res["p"] < ALPHA and not res["failures"]
        a, b = half_a.get(k), half_b.get(k)
        rep = None
        if sig and a and b and a["p"] is not None and b["p"] is not None:
            same_sign = (a["effect"] or 0) * (res["effect"] or 0) > 0 and (b["effect"] or 0) * (res["effect"] or 0) > 0
            rep = bool(a["p"] < ALPHA and b["p"] < ALPHA and same_sign)
        claims.append({
            "key": k, "grouping": g, "outcome": o,
            **{kk: res[kk] for kk in ("test", "n1", "n0", "z", "p", "effect", "effect_kind",
                                      "summary1", "summary0", "summary_kind", "events1", "events0",
                                      "distinct_values", "failures")},
            "significant": sig,
            "bh_survivor": k in bh_keys,
            "bonferroni_survivor": k in bonf,
            "half_even_p": a["p"] if a else None,
            "half_odd_p": b["p"] if b else None,
            "half_even_effect": a["effect"] if a else None,
            "half_odd_effect": b["effect"] if b else None,
            "replicates_split_half": rep,
            "sentence": claim_sentence(g, o, res) if sig else None,
        })

    m1 = [c for c in claims if c["significant"]]
    killed = [c for c in claims if c["failures"]]
    nulls = null_world(records, pairs, preps, group_cols, args.replicates, args.seed, breaks)
    lo, hi = wilson(nulls["rejections_total"], nulls["tests_total"])

    results = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "corpus": {"records": len(records), "fetched_utc": corpus["fetched_utc"],
                   "source": corpus["source"], "per_category": corpus["returned_per_category"]},
        "hypotheses": len(pairs),
        "tests_run": len(full),
        "M1_raw_findings": len(m1),
        "M2_bh_survivors": len([c for c in claims if c["bh_survivor"]]),
        "M2_bonferroni_survivors": len([c for c in claims if c["bonferroni_survivor"]]),
        "M4_review_kills": len(killed),
        "M4_killed_keys": [c["key"] for c in killed],
        "M6_replicating": len([c for c in m1 if c["replicates_split_half"]]),
        "M6_of": len(m1),
        "M6_halves": {"even": len(even), "odd": len(odd)},
        "M3_null_world": nulls,
        "M3_per_test_rate_ci95": [lo, hi],
        "breaks": breaks,
        "claims": claims,
    }
    with open(args.out, "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print(f"M1 {results['M1_raw_findings']} raw · BH {results['M2_bh_survivors']} · "
          f"kills {results['M4_review_kills']} · replicating {results['M6_replicating']}/{results['M6_of']} · "
          f"null {nulls['findings_per_run_mean']:.2f}/run ({nulls['per_test_rejection_rate']*100:.2f} % per test) · "
          f"breaks {len(breaks)}", file=sys.stderr)


if __name__ == "__main__":
    main()
