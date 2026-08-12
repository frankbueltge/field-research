#!/usr/bin/env python3
"""Is the unit of loss the video or the account?

Session 114, 2026-08-12. Re-analysis of a run already collected — NO new requests, and the
window ledger, its manifest and its probe are not touched.

Every number this arc has published, and the number the receiver published, treats the video
as the unit and computes a Wilson interval over n videos. If videos disappear by account, the
effective sample size is nearer the number of accounts, and every such interval is too narrow.

The credential-free interface will not say why a video is gone: in the day-2 run every
NOT-RETRIEVABLE unit is HTTP 400 with one body code. So the mechanism is read off the
structure of the losses or not at all.

Method (pre-registered, PREREGISTRATION-114.md §2):
  - population: one ledger run, INDETERMINATE dropped, arm B-truncated dropped (its absence is
    an artifact of a truncated identifier, not an event on the platform), 19-digit ids only so
    the age is decodable by this arc's dating rule (created = int(vid) >> 32).
  - grouping key: the handle from the CITED url, case-folded, because it is the only account
    identifier that exists for a unit that is not retrievable.
  - statistic: ANOVA intra-class correlation rho over handles, Kish design effect
    DEFF = 1 + (m_kish - 1) * rho, within-handle concordance of absence, and the share of
    absent units sitting in handles where every unit is absent.
  - two nulls, Monte Carlo, seeded: (1) constant pooled absence rate; (2) Poisson-binomial with
    each unit's own age-band x arm cell rate, which removes the confound that an account's
    videos share an era.

Usage: python3 cluster_model.py <run.json> [draws] [seed]
"""
import json
import random
import sys
import time

import power_audit as pa

YEAR_S = 365.2425 * 24 * 3600
STRATUM = {"A": "W-article", "A-new": "W-article", "A2": "W-other-ns", "B": "F-forum"}
AGE_BANDS = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 99)]


def band_label(lo, hi):
    return f"{lo}-{hi}y" if hi < 99 else f"{lo}y+"


def load(run_path):
    d = json.load(open(run_path))
    t_ref = time.mktime(time.strptime(d["run_utc_start"], "%Y-%m-%dT%H:%M:%SZ")) - time.timezone
    rows, excl = [], {"arm_B_truncated": 0, "indeterminate": 0, "not_19_digit": 0,
                      "nonpositive_age": 0}
    key_agree, key_total, key_seen = 0, 0, []
    for o in d["observations"]:
        if o["arm"] == "B-truncated":
            excl["arm_B_truncated"] += 1
            continue
        if o["state"] == "INDETERMINATE":
            excl["indeterminate"] += 1
            continue
        vid = str(o["vid"])
        if len(vid) != 19:
            excl["not_19_digit"] += 1
            continue
        created = int(vid) >> 32
        age_s = t_ref - created
        if age_s <= 0:
            excl["nonpositive_age"] += 1
            continue
        # P1: fidelity of the grouping key, on the units where the platform names the author
        if o["state"] == "RETRIEVABLE" and o.get("author_unique_id"):
            key_total += 1
            if str(o["author_unique_id"]).lower() == str(o["handle"]).lower():
                key_agree += 1
            elif len(key_seen) < 25:
                key_seen.append({"vid": vid, "cited": o["handle"],
                                 "returned": o["author_unique_id"]})
        age_y = age_s / YEAR_S
        band = next(band_label(lo, hi) for lo, hi in AGE_BANDS if lo <= age_y < hi)
        rows.append({"vid": vid, "arm": o["arm"], "stratum": STRATUM[o["arm"]],
                     "handle_raw": o["handle"], "handle": str(o["handle"]).lower(),
                     "absent": 0 if o["state"] == "RETRIEVABLE" else 1,
                     "year": time.gmtime(created).tm_year, "band": band, "age_y": age_y})
    key = {"n_checked": key_total, "n_agree": key_agree,
           "agreement": key_agree / key_total if key_total else None,
           "examples_of_disagreement": key_seen}
    return d, rows, excl, key


def groups(rows):
    g = {}
    for r in rows:
        g.setdefault(r["handle"], []).append(r)
    return g


def icc(g):
    """ANOVA intra-class correlation for a binary response over unequal clusters.

    Standard one-way random-effects estimator. Clusters of size 1 contribute to the between
    term only; they are kept because the design effect being corrected applies to the whole
    sample, not to the multi-video part of it.
    """
    N = sum(len(v) for v in g.values())
    K = len(g)
    if K < 2 or N <= K:
        return None
    grand = sum(r["absent"] for v in g.values() for r in v) / N
    ssb = sum(len(v) * ((sum(r["absent"] for r in v) / len(v)) - grand) ** 2 for v in g.values())
    ssw = sum(sum((r["absent"] - sum(x["absent"] for x in v) / len(v)) ** 2 for r in v)
              for v in g.values())
    msb, msw = ssb / (K - 1), ssw / (N - K)
    m0 = (N - sum(len(v) ** 2 for v in g.values()) / N) / (K - 1)
    denom = msb + (m0 - 1) * msw
    if denom == 0:
        return None
    return (msb - msw) / denom


def kish(g):
    N = sum(len(v) for v in g.values())
    return sum(len(v) ** 2 for v in g.values()) / N


def concordance(g):
    """Within-handle pairs: how many are both-absent, out of all pairs."""
    pairs = both = one = 0
    for v in g.values():
        k = len(v)
        if k < 2:
            continue
        a = sum(r["absent"] for r in v)
        pairs += k * (k - 1) // 2
        both += a * (a - 1) // 2
        one += a * (k - a)
    return {"pairs": pairs, "both_absent": both, "exactly_one_absent": one,
            "p_both": both / pairs if pairs else None}


def allgone(g):
    tot = ing = in_multi = 0
    handles_all = handles_multi = 0
    for v in g.values():
        a = sum(r["absent"] for r in v)
        tot += a
        if len(v) >= 2:
            in_multi += a
            handles_multi += 1
            if a == len(v):
                ing += a
                handles_all += 1
    return {"absent_total": tot, "absent_in_multi_handles": in_multi,
            "absent_in_all_gone_handles": ing,
            "share_of_multi_absent_in_all_gone": ing / in_multi if in_multi else None,
            "handles_multi": handles_multi, "handles_all_gone": handles_all}


def cell_rates(rows):
    cells = {}
    for r in rows:
        cells.setdefault((r["arm"], r["band"]), []).append(r["absent"])
    return {k: sum(v) / len(v) for k, v in cells.items()}, \
           {k: len(v) for k, v in cells.items()}


def montecarlo(rows, probs, draws, seed):
    """Resample each unit independently at its null probability, keep the group structure,
    recompute rho. Returns the null distribution summary and the one-sided p-value."""
    rng = random.Random(seed)
    idx = {}
    for i, r in enumerate(rows):
        idx.setdefault(r["handle"], []).append(i)
    obs_groups = groups(rows)
    obs = icc(obs_groups)
    sims = []
    for _ in range(draws):
        draw = [1 if rng.random() < p else 0 for p in probs]
        g = {h: [{"absent": draw[i]} for i in ii] for h, ii in idx.items()}
        v = icc(g)
        if v is not None:
            sims.append(v)
    sims.sort()
    ge = sum(1 for s in sims if s >= obs)
    return {"observed_rho": obs, "draws": len(sims),
            "null_mean": sum(sims) / len(sims), "null_p95": sims[int(0.95 * len(sims))],
            "null_max": sims[-1], "n_ge_observed": ge,
            "p_value": (ge + 1) / (len(sims) + 1)}


def wilson_eff(k, n, deff):
    n_eff = max(1, int(n / deff))
    k_eff = k * n_eff / n
    lo, hi = pa.wilson(k_eff, n_eff)
    return {"n_eff": n_eff, "ci": [lo, hi], "width": hi - lo}


def analyse(run_path, draws, seed):
    d, rows, excl, key = load(run_path)
    g = groups(rows)
    N = len(rows)
    absent = sum(r["absent"] for r in rows)
    p_bar = absent / N
    rho = icc(g)
    m_kish = kish(g)
    deff = 1 + (m_kish - 1) * rho if rho is not None else None
    rates, sizes = cell_rates(rows)

    null1 = montecarlo(rows, [p_bar] * N, draws, seed)
    null2 = montecarlo(rows, [rates[(r["arm"], r["band"])] for r in rows], draws, seed + 1)

    lo, hi = pa.wilson(absent, N)
    naive = {"n": N, "absent": absent, "rate": p_bar, "ci": [lo, hi], "width": hi - lo}
    corrected = wilson_eff(absent, N, deff) if deff and deff > 1 else None

    per_arm = {}
    for arm in sorted({r["arm"] for r in rows}):
        sub = [r for r in rows if r["arm"] == arm]
        ga = groups(sub)
        ra = icc(ga)
        per_arm[arm] = {"n": len(sub), "absent": sum(r["absent"] for r in sub),
                        "handles": len(ga), "m_kish": kish(ga), "rho": ra,
                        "deff": 1 + (kish(ga) - 1) * ra if ra is not None else None}

    size_hist = {}
    for v in g.values():
        size_hist[len(v)] = size_hist.get(len(v), 0) + 1

    return {
        "run": run_path, "run_id": d["run_id"], "run_utc_start": d["run_utc_start"],
        "excluded": excl, "grouping_key_fidelity_P1": key,
        "n_units": N, "n_handles": len(g), "m_kish": m_kish,
        "handle_size_histogram": {str(k): v for k, v in sorted(size_hist.items())},
        "absent": absent, "absence_rate": p_bar,
        "rho_anova": rho, "deff_kish": deff,
        "null1_constant_rate": null1, "null2_age_arm_conditional": null2,
        "concordance": concordance(g), "all_gone": allgone(g),
        "interval_naive_video_unit": naive, "interval_corrected_for_clustering": corrected,
        "per_arm": per_arm,
        "cell_rates_used_for_null2": {f"{a}|{b}": {"p": rates[(a, b)], "n": sizes[(a, b)]}
                                      for (a, b) in sorted(rates)},
        "seed": seed, "draws_requested": draws,
    }


if __name__ == "__main__":
    run = sys.argv[1] if len(sys.argv) > 1 else "ledger/run-2026-08-12T0341Z.json"
    draws = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20260812
    out = analyse(run, draws, seed)
    name = "cluster-" + out["run_id"].replace(":", "") + ".json"
    json.dump(out, open(name, "w"), indent=1)
    print(f"run {out['run_id']}  units {out['n_units']}  handles {out['n_handles']}  "
          f"absent {out['absent']} ({100*out['absence_rate']:.2f} %)")
    print(f"P1 key fidelity   {out['grouping_key_fidelity_P1']['agreement']}")
    print(f"rho {out['rho_anova']:.4f}   m_kish {out['m_kish']:.3f}   DEFF {out['deff_kish']:.3f}")
    print(f"null1 p={out['null1_constant_rate']['p_value']:.5f} "
          f"(null mean rho {out['null1_constant_rate']['null_mean']:.4f}, "
          f"p95 {out['null1_constant_rate']['null_p95']:.4f})")
    print(f"null2 p={out['null2_age_arm_conditional']['p_value']:.5f} "
          f"(null mean rho {out['null2_age_arm_conditional']['null_mean']:.4f}, "
          f"p95 {out['null2_age_arm_conditional']['null_p95']:.4f})")
    print("concordance", json.dumps(out["concordance"]))
    print("all-gone   ", json.dumps(out["all_gone"]))
    print("naive     ", json.dumps(out["interval_naive_video_unit"]))
    print("corrected ", json.dumps(out["interval_corrected_for_clustering"]))
    for a, v in out["per_arm"].items():
        print(f"  arm {a:8s} n={v['n']:5d} handles={v['handles']:5d} rho={v['rho']} "
              f"DEFF={v['deff']}")
    print("wrote", name)
