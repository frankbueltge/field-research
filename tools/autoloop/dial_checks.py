#!/usr/bin/env python3
"""autoloop — the pre-registered checks for the dial, computed from the sweep files.

Every number the artifact states about P1-P5 comes from here, and nothing here decides
anything the pre-registration did not decide in advance. Run:

  python3 tools/autoloop/dial_checks.py --sweeps <arxiv.json> <crossref.json> --out <checks.json>
"""

import argparse
import json
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dial                                                              # noqa: E402
from stats import benjamini_hochberg                                     # noqa: E402


def through_origin(ks, ys):
    """Least-squares slope through the origin, and the R^2 of that one-parameter fit."""
    num = sum(k * y for k, y in zip(ks, ys))
    den = sum(k * k for k in ks)
    b = num / den
    ss_res = sum((y - b * k) ** 2 for k, y in zip(ks, ys))
    ss_tot = sum(y * y for y in ys)                  # about zero, as the model has no intercept
    return b, (1 - ss_res / ss_tot if ss_tot else None)


def centered(ks, ys):
    """Ordinary least squares WITH an intercept, and the conventional mean-centred R^2.

    Added 2026-09-04 after a convened adversary showed the through-origin R^2 above is the
    lenient convention: its denominator is dominated by the largest-k point, so a large
    relative distortion at small k barely moves it. Both are now reported, always.
    """
    n = len(ks)
    mk, my = sum(ks) / n, sum(ys) / n
    sxx = sum((k - mk) ** 2 for k in ks)
    b = sum((k - mk) * (y - my) for k, y in zip(ks, ys)) / sxx
    a = my - b * mk
    ss_res = sum((y - (a + b * k)) ** 2 for k, y in zip(ks, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    return b, a, (1 - ss_res / ss_tot if ss_tot else None)


def paired_mean_diff(a, b):
    """Paired difference b - a over the shared permutation stream: mean, SE, z, two-sided p."""
    d = [x - y for x, y in zip(b, a)]
    n = len(d)
    m = sum(d) / n
    sd = statistics.stdev(d) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n > 1 else 0.0
    z = m / se if se > 0 else None
    p = math.erfc(abs(z) / math.sqrt(2.0)) if z is not None else None
    return {"mean_difference": m, "se": se, "z": z, "p": p, "n": n}


def mcnemar(a, b):
    """Paired test on 'at least one finding': b vs a. Exact binomial on the discordant pairs."""
    b_only = sum(1 for x, y in zip(a, b) if y >= 1 and x < 1)
    a_only = sum(1 for x, y in zip(a, b) if x >= 1 and y < 1)
    nd = a_only + b_only
    if nd == 0:
        return {"a_only": a_only, "b_only": b_only, "discordant": 0, "p": None}
    p = sum(math.comb(nd, i) for i in range(0, min(a_only, b_only) + 1)) / (2 ** nd) * 2
    return {"a_only": a_only, "b_only": b_only, "discordant": nd, "p": min(1.0, p)}


def variance_ratio_bootstrap(a, b, reps=2000, seed=20260904):
    """Paired bootstrap of Var(b)/Var(a): resample replicate indices, keeping cells paired."""
    import random
    rng = random.Random(seed)
    n = len(a)
    ratios = []
    for _ in range(reps):
        idx = [rng.randrange(n) for _ in range(n)]
        va = statistics.pvariance([a[i] for i in idx])
        vb = statistics.pvariance([b[i] for i in idx])
        if va > 0:
            ratios.append(vb / va)
    ratios.sort()
    lo = ratios[int(0.025 * len(ratios))]
    hi = ratios[int(0.975 * len(ratios)) - 1]
    return {"point": statistics.pvariance(b) / statistics.pvariance(a),
            "ci95": [lo, hi], "bootstrap_replicates": len(ratios)}


def dedup_sensitivity(space_name, d):
    """Does P4's answer depend on WHICH copy of a duplicated question is kept?

    Added 2026-09-04 after an adversary showed the canonical-order rule was not tested.
    Three rules: first appearance (as run), the copy with the smallest p, the copy with the
    largest p. If the three disagree, "BH is self-correcting for exact duplicates" is a
    property of this data, not a guarantee.
    """
    space = dial.SPACES[space_name]
    tests = d["tests"]
    questions = dial.enumerate_questions(space)

    def bh_over(keys):
        ks_ = [k for k in keys if tests.get(k) and tests[k]["p"] is not None and not tests[k]["failures"]]
        ps = [tests[k]["p"] for k in ks_]
        return {ks_[i] for i in benjamini_hochberg(ps, 0.05)}

    by_pair = {}
    for g, o in questions:
        by_pair.setdefault(dial.var_pair(space, g, o), []).append(f"{g}|{o}")

    out = {}
    for rule in ("first", "min_p", "max_p"):
        reps = []
        for _vp, keys in by_pair.items():
            avail = [k for k in keys if tests.get(k) and tests[k]["p"] is not None]
            if not avail or rule == "first":
                reps.append(keys[0])
            elif rule == "min_p":
                reps.append(min(avail, key=lambda k: tests[k]["p"]))
            else:
                reps.append(max(avail, key=lambda k: tests[k]["p"]))
        s = bh_over(reps)
        out[rule] = {"survivors": len(s),
                     "distinct": len({dial.var_pair(space, *k.split("|")) for k in s})}
    out["invariant_across_rules"] = len({v["survivors"] for v in
                                         (out["first"], out["min_p"], out["max_p"])}) == 1
    return out


def trim_control(d):
    """Is the post-hoc 'claimable questions' rate a transfer result, or just a trimmed mean?

    Added 2026-09-04 after an adversary's objection. Control: drop the N questions with the
    LOWEST null rate, where N is the number the review actually killed, with no reference to
    the pre-conditions at all. If the control lands where the principled restriction lands,
    the restriction is not evidence of anything about the architecture.
    """
    pq = d["per_question_null_rate"]
    tests = d["tests"]
    killed = [k for k in pq if tests[k]["failures"]]
    kept = [k for k in pq if k not in killed]
    n = len(killed)
    vals = sorted(pq.values())
    return {
        "whole_space": sum(vals) / len(vals), "n_whole": len(vals),
        "claimable": (sum(pq[k] for k in kept) / len(kept)) if kept else None, "n_claimable": len(kept),
        "killed": (sum(pq[k] for k in killed) / n) if n else None, "n_killed": n,
        "naive_drop_lowest_n": (sum(vals[n:]) / len(vals[n:])) if n < len(vals) else None,
        "dead_questions": sorted(k for k, v in pq.items() if v == 0.0),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweeps", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    arms = {}
    for path in args.sweeps:
        d = json.load(open(path))
        arms[d["space"]] = d

    checks = {"arms": {}, "P1": {}, "P2": {}, "P3": {}, "P4": {}, "P5": {}}

    for space, d in arms.items():
        ks = d["k_values"]
        arm = {"records": d["corpus"]["records"], "questions": d["questions"],
               "distinct_pairs": d["distinct_pairs"], "review_kills": d["review_kills"],
               "breaks": len(d["breaks"]), "K2": d["K2"]}

        # --- P1: is the dial a line? -------------------------------------------------
        p1 = {}
        for fam in ("lean", "dense"):
            ys = [d["null"][f"{fam}@{k}"]["mean"] for k in ks]
            b, r2 = through_origin(ks, ys)
            cb, ca, cr2 = centered(ks, ys)
            p1[fam] = {"slope": b, "r2": r2, "means": ys,
                       "slope_in_band": 0.045 <= b <= 0.055, "r2_ok": r2 >= 0.99,
                       "centered_slope": cb, "centered_intercept": ca, "centered_r2": cr2,
                       "centered_r2_ok": cr2 >= 0.99}
        arm["P1"] = p1

        # --- P2 / P3: the matched-redundancy contrast at k = 30 ------------------------
        lean, dense = d["null"]["lean@30"], d["null"]["dense@30"]
        a, b = lean["counts"], dense["counts"]
        arm["P2"] = {
            "lean_variance": lean["variance"], "dense_variance": dense["variance"],
            "ratio": dense["variance"] / lean["variance"],
            "ratio_ci95_paired_bootstrap": variance_ratio_bootstrap(a, b),
            "lean_overdispersion": lean["overdispersion"], "dense_overdispersion": dense["overdispersion"],
            "mean_difference_dense_minus_lean": paired_mean_diff(a, b),
            "predicted": "dense variance at least 10 % above lean",
            "holds": (dense["variance"] / lean["variance"]) >= 1.10,
        }
        indep = lean["p_at_least_one_independent"]
        arm["P3"] = {
            "independence_value": indep,
            "lean_p_at_least_one": lean["p_at_least_one"],
            "dense_p_at_least_one": dense["p_at_least_one"],
            "lean_below_independence": lean["p_at_least_one"] < indep,
            "dense_below_independence": dense["p_at_least_one"] < indep,
            "dense_below_lean": dense["p_at_least_one"] < lean["p_at_least_one"],
            "paired_mcnemar_dense_vs_lean": mcnemar(a, b),
        }

        # --- P4: the power tax ---------------------------------------------------------
        r = d["real_full_space"]
        arm["P4"] = {
            "raw_findings": r["raw_findings"],
            "distinct_pairs_among_raw": r["distinct_pairs_among_raw"],
            "bh_survivors_all66": r["bh_survivors_all66"],
            "bh_denominator_all66": r["bh_denominator_all66"],
            "bh_survivors_dedup51": r["bh_survivors_dedup51"],
            "bh_denominator_dedup51": r["bh_denominator_dedup51"],
            "distinct_claims_all66": r["distinct_pairs_among_bh_all66"],
            "distinct_claims_dedup51": r["distinct_pairs_among_bh_dedup51"],
            "dedup_recovers_any": len(r["dedup_only"]) > 0,
            "dedup_only": r["dedup_only"],
            "all66_only": r["all66_only"],
            "predicted": "deduplicating the space yields MORE survivors",
            "holds": len(r["dedup_only"]) > 0,
            "distinct_claim_set_identical":
                r["distinct_pairs_among_bh_all66"] == r["distinct_pairs_among_bh_dedup51"],
        }

        # --- P5: does the slope transfer? ----------------------------------------------
        cell = d["null"]["lean@66"]
        arm["P5"] = {
            "per_test_rate": cell["per_test_rate"],
            "ci95": cell["per_test_ci95"],
            "contains_alpha": cell["per_test_ci95"][0] <= 0.05 <= cell["per_test_ci95"][1],
        }

        # per-question spread of the null rate, the diagnostic behind P5
        rates = sorted(d["per_question_null_rate"].items(), key=lambda kv: kv[1])
        vals = [v for _, v in rates]
        arm["per_question_null_rate"] = {
            "min": rates[0], "max": rates[-1],
            "median": statistics.median(vals),
            "below_0.02": sum(1 for v in vals if v < 0.02),
            "above_0.08": sum(1 for v in vals if v > 0.08),
            "lowest_five": rates[:5], "highest_five": rates[-5:],
        }
        arm["P4_representative_sensitivity"] = dedup_sensitivity(space, d)
        arm["posthoc_trim_control"] = trim_control(d)
        # the pairing claim, checked rather than asserted: lean@66 and dense@66 are the same
        # question set, so their count vectors must be identical if the stream really is shared
        arm["pairing_verified"] = (d["null"]["lean@66"]["counts"] == d["null"]["dense@66"]["counts"])
        checks["arms"][space] = arm

    # cross-arm: do the two per-test intervals overlap?
    if len(arms) == 2:
        (s1, a1), (s2, a2) = list(checks["arms"].items())
        c1, c2 = a1["P5"]["ci95"], a2["P5"]["ci95"]
        checks["P5"] = {
            "arms": [s1, s2],
            "rates": [a1["P5"]["per_test_rate"], a2["P5"]["per_test_rate"]],
            "intervals": [c1, c2],
            "intervals_overlap": not (c1[1] < c2[0] or c2[1] < c1[0]),
            "both_contain_alpha": a1["P5"]["contains_alpha"] and a2["P5"]["contains_alpha"],
        }

    for pkey in ("P1", "P2", "P3", "P4"):
        checks[pkey] = {s: checks["arms"][s][pkey] for s in checks["arms"]}

    with open(args.out, "w") as f:
        json.dump(checks, f, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in checks.items() if k != "arms"}, indent=1, sort_keys=True)[:4000])


if __name__ == "__main__":
    main()
