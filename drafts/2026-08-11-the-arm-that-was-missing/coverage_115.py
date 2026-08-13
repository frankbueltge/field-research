#!/usr/bin/env python3
"""Does the correction this session published actually deliver 95 % coverage?

Session 115. **No new requests, no platform contact — this is a simulation.**

`RESTATEMENT-2026-08-13.md` corrects every published interval by computing Wilson on
`n_eff = n / DEFF`. The document calls that "the standard first-order design-effect correction",
which is true and is not evidence. Several restated cells have n = 35 or p near 1, where Wilson's
own coverage is already ragged and a non-integer effective sample size is doing work nobody
checked. So it is checked here, before an adversary has to.

Design. The clustering is simulated the way this corpus actually looks, from the day-2 run's own
account-size distribution: 2,744 accounts holding 3,575 units, two thirds of them singletons. Each
account draws a latent propensity from a Beta distribution and its units are Bernoulli at that
propensity — a beta-binomial cluster model, which is the textbook generator for exactly this kind
of over-dispersion. The Beta is tuned by bisection so the realised design effect matches a target,
and the target is swept across the range this session actually uses (1.20 to 1.75).

Three intervals are compared on identical data: the naive Wilson over n, the corrected Wilson over
n / DEFF_true, and the corrected Wilson over an estimated DEFF computed from the sample itself
(which is what a real analyst has). Coverage is the share of replicates whose interval contains the
population value.

Usage: python3 coverage_115.py [replicates] [seed]
Output: coverage-115.json
"""
import json
import math
import random
import sys

import power_audit as pa
import cluster_model as cm

DAY2 = "ledger/run-2026-08-12T0341Z.json"


def cluster_sizes():
    """The real account-size distribution of this corpus, not an invented one."""
    _, rows, _, _ = cm.load(DAY2)
    g = {}
    for r in rows:
        g.setdefault(r["handle"], []).append(r)
    return sorted((len(v) for v in g.values()), reverse=True)


def deff_hat(clusters):
    """The estimator the session actually uses: linearised clustered variance / binomial."""
    N = sum(len(c) for c in clusters)
    K = len(clusters)
    a = sum(sum(c) for c in clusters)
    p = a / N
    if p in (0.0, 1.0):
        return None
    ss = sum((sum(c) - p * len(c)) ** 2 for c in clusters)
    return (K / (K - 1) * ss / N ** 2) / (p * (1 - p) / N)


def draw(sizes, p, rho, rng):
    """Beta-binomial clusters: each account gets its own propensity, units Bernoulli within."""
    if rho <= 0:
        return [[1 if rng.random() < p else 0 for _ in range(m)] for m in sizes]
    nu = (1 - rho) / rho
    a, b = p * nu, (1 - p) * nu
    out = []
    for m in sizes:
        q = rng.betavariate(a, b)
        out.append([1 if rng.random() < q else 0 for _ in range(m)])
    return out


def realised_deff(sizes, p, rho, rng, reps=200):
    vals = []
    for _ in range(reps):
        d = deff_hat(draw(sizes, p, rho, rng))
        if d:
            vals.append(d)
    return sum(vals) / len(vals) if vals else None


def rho_for_target(sizes, p, target, seed):
    """Bisect on the beta-binomial's intra-cluster correlation to hit a target design effect."""
    lo, hi = 1e-5, 0.99
    for _ in range(22):
        mid = (lo + hi) / 2
        rng = random.Random(seed)
        d = realised_deff(sizes, p, mid, rng)
        if d is None or d < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def wilson_eff(k, n, deff):
    n_eff = n / deff
    return pa.wilson(k * n_eff / n, n_eff)


def run_case(sizes, p, target_deff, reps, seed):
    rho = rho_for_target(sizes, p, target_deff, seed)
    rng = random.Random(seed + 7)
    realised = realised_deff(sizes, p, rho, random.Random(seed + 11), reps=300)
    naive = corrected = estimated = 0
    widths_n, widths_c = [], []
    deffs = []
    for _ in range(reps):
        cl = draw(sizes, p, rho, rng)
        n = sum(len(c) for c in cl)
        k = sum(sum(c) for c in cl)
        lo, hi = pa.wilson(k, n)
        if lo <= p <= hi:
            naive += 1
        widths_n.append(hi - lo)
        lo2, hi2 = wilson_eff(k, n, realised)
        if lo2 <= p <= hi2:
            corrected += 1
        widths_c.append(hi2 - lo2)
        dh = deff_hat(cl)
        if dh:
            deffs.append(dh)
            lo3, hi3 = wilson_eff(k, n, max(1.0, dh))
            if lo3 <= p <= hi3:
                estimated += 1
    return {"p": p, "target_deff": target_deff, "rho_used": round(rho, 5),
            "realised_deff": round(realised, 4),
            "replicates": reps,
            "coverage_naive_wilson": round(naive / reps, 4),
            "coverage_corrected_true_deff": round(corrected / reps, 4),
            "coverage_corrected_estimated_deff": round(estimated / reps, 4),
            "mean_width_naive": round(sum(widths_n) / len(widths_n), 5),
            "mean_width_corrected": round(sum(widths_c) / len(widths_c), 5),
            "mean_estimated_deff": round(sum(deffs) / len(deffs), 4) if deffs else None}


def main(reps=2000, seed=20260813):
    full = cluster_sizes()
    out = {"session": 115, "simulation_only": True, "replicates": reps, "seed": seed,
           "cluster_sizes_from": DAY2,
           "full_corpus": {"units": sum(full), "accounts": len(full),
                           "singletons": sum(1 for m in full if m == 1),
                           "largest": full[0]},
           "cases": []}

    # the full corpus, at the absence rate this arc measures, across the design effects it uses
    for target in (1.20, 1.43, 1.75):
        out["cases"].append({"population": "full corpus (3,575 units / 2,744 accounts)",
                             **run_case(full, 0.1208, target, reps, seed)})

    # a small cell near the sparse end, and one with p near 1 — the two places the document
    # actually relies on and where Wilson is known to behave worst
    small = [m for m in full if m == 1][:32] + [2]          # 34 units in 33 accounts, ~ the 2019 cell
    out["cases"].append({"population": "small cell (34 units / 33 accounts), p = 0.23",
                         **run_case(small, 0.23, 1.43, reps, seed + 1)})
    mid = full[: len(full) // 6]
    out["cases"].append({"population": f"extreme p ({sum(mid)} units), p = 0.95",
                         **run_case(mid, 0.95, 1.43, reps, seed + 2)})

    json.dump(out, open("coverage-115.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(out["full_corpus"]))
    for c in out["cases"]:
        print(f"{c['population']}  p={c['p']}  target DEFF {c['target_deff']} "
              f"(realised {c['realised_deff']})")
        print(f"    naive Wilson        coverage {c['coverage_naive_wilson']:.4f}  "
              f"mean width {c['mean_width_naive']:.5f}")
        print(f"    corrected, true     coverage {c['coverage_corrected_true_deff']:.4f}  "
              f"mean width {c['mean_width_corrected']:.5f}")
        print(f"    corrected, estimated coverage {c['coverage_corrected_estimated_deff']:.4f}  "
              f"(mean estimated DEFF {c['mean_estimated_deff']})")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000,
         int(sys.argv[2]) if len(sys.argv) > 2 else 20260813)
