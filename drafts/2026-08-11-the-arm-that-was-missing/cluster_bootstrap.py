#!/usr/bin/env python3
"""A design effect that does not depend on the ANOVA estimator.

Session 114, added AFTER the pre-registered statistic returned rho = 0.79 on a sample that is
two thirds singleton clusters — a regime where the ANOVA intra-class correlation is known to be
unstable, because the within-cluster mean square is computed on the few multi-unit handles
alone. Recorded as deviation D17: the pre-registered statistic is kept and reported; this is
added beside it, not instead of it, and the two are compared.

The nonparametric cluster bootstrap needs no rho at all. Resample HANDLES with replacement,
take every unit of each drawn handle, recompute the absence rate. If losses are borne by
accounts, the resulting distribution is wider than the binomial one, and the ratio of the
squared widths IS the design effect, measured rather than estimated.

Also here: the same computation under a second grouping key, to bound the damage from the
7.24 % of cited handles that the platform answers with a different account name (P1 failed,
K1 fired). Key 2 uses the platform's own author id where the platform gave one and the cited
handle otherwise. Key 2 is a SENSITIVITY, not a repair: it applies the canonical name only to
units that are retrievable, so it can merge present units while leaving absent ones apart, and
that asymmetry can manufacture concordance. It is reported for the direction it moves the
answer, and no headline is taken from it.

Usage: python3 cluster_bootstrap.py <run.json> [draws] [seed]
"""
import json
import random
import sys

import power_audit as pa
from cluster_model import load, groups, kish, icc


def boot(g, draws, seed):
    rng = random.Random(seed)
    handles = list(g.values())
    K = len(handles)
    rates = []
    for _ in range(draws):
        n = a = 0
        for _ in range(K):
            v = handles[rng.randrange(K)]
            n += len(v)
            a += sum(r["absent"] for r in v)
        rates.append(a / n)
    rates.sort()
    lo, hi = rates[int(0.025 * draws)], rates[int(0.975 * draws)]
    return {"draws": draws, "ci": [lo, hi], "width": hi - lo,
            "mean": sum(rates) / draws}


def unit_boot(rows, draws, seed):
    """The same bootstrap ignoring handles — the comparison the design effect is against."""
    rng = random.Random(seed)
    N = len(rows)
    vals = [r["absent"] for r in rows]
    rates = []
    for _ in range(draws):
        rates.append(sum(vals[rng.randrange(N)] for _ in range(N)) / N)
    rates.sort()
    lo, hi = rates[int(0.025 * draws)], rates[int(0.975 * draws)]
    return {"draws": draws, "ci": [lo, hi], "width": hi - lo}


def key2(rows, run_path):
    """Grouping key 2: the platform's own author id where it answered, cited handle otherwise."""
    d = json.load(open(run_path))
    canon = {str(o["vid"]): str(o["author_unique_id"]).lower()
             for o in d["observations"]
             if o["state"] == "RETRIEVABLE" and o.get("author_unique_id")}
    out = {}
    for r in rows:
        out.setdefault(canon.get(r["vid"], r["handle"]), []).append(r)
    return out


def main(run_path, draws, seed):
    d, rows, excl, key = load(run_path)
    g = groups(rows)
    N = len(rows)
    a = sum(r["absent"] for r in rows)
    lo, hi = pa.wilson(a, N)
    wilson = {"n": N, "absent": a, "rate": a / N, "ci": [lo, hi], "width": hi - lo}

    cb = boot(g, draws, seed)
    ub = unit_boot(rows, draws, seed + 7)
    deff_measured = (cb["width"] / ub["width"]) ** 2
    deff_vs_wilson = (cb["width"] / wilson["width"]) ** 2

    g2 = key2(rows, run_path)
    cb2 = boot(g2, draws, seed + 13)

    out = {
        "run": run_path, "run_id": d["run_id"], "n_units": N, "absent": a,
        "rate": a / N,
        "interval_wilson_video_unit": wilson,
        "bootstrap_over_units_no_clusters": ub,
        "bootstrap_over_handles_key1": cb,
        "bootstrap_over_handles_key2_sensitivity": cb2,
        "n_handles_key1": len(g), "n_handles_key2": len(g2),
        "m_kish_key1": kish(g), "m_kish_key2": kish(g2),
        "rho_anova_key1": icc(g), "rho_anova_key2": icc(g2),
        "deff_measured_cluster_vs_unit_bootstrap": deff_measured,
        "deff_cluster_bootstrap_vs_wilson": deff_vs_wilson,
        "deff_from_anova_rho_key1": 1 + (kish(g) - 1) * icc(g),
        "seed": seed,
        "note": ("The design effect that carries any restatement of an interval is "
                 "deff_measured_cluster_vs_unit_bootstrap: both terms are bootstraps of the "
                 "same data under the same resampling, differing only in whether the handle "
                 "is the resampling unit. The ANOVA figure is reported beside it and is not "
                 "used, for the reason in this file's docstring."),
    }
    json.dump(out, open("cluster-bootstrap-" + d["run_id"].replace(":", "") + ".json", "w"),
              indent=1)
    print(f"run {d['run_id']}  n {N}  absent {a}  rate {100*a/N:.2f} %")
    print(f"wilson (video unit)      [{100*wilson['ci'][0]:.2f}, {100*wilson['ci'][1]:.2f}] "
          f"width {100*wilson['width']:.3f} pp")
    print(f"bootstrap over units     [{100*ub['ci'][0]:.2f}, {100*ub['ci'][1]:.2f}] "
          f"width {100*ub['width']:.3f} pp")
    print(f"bootstrap over handles   [{100*cb['ci'][0]:.2f}, {100*cb['ci'][1]:.2f}] "
          f"width {100*cb['width']:.3f} pp   (key 1)")
    print(f"bootstrap over handles   [{100*cb2['ci'][0]:.2f}, {100*cb2['ci'][1]:.2f}] "
          f"width {100*cb2['width']:.3f} pp   (key 2, sensitivity)")
    print(f"DEFF measured (cluster/unit bootstrap) {deff_measured:.3f}")
    print(f"DEFF cluster bootstrap vs wilson       {deff_vs_wilson:.3f}")
    print(f"DEFF from ANOVA rho                    {out['deff_from_anova_rho_key1']:.3f}")
    print(f"rho key1 {out['rho_anova_key1']:.4f}   rho key2 {out['rho_anova_key2']:.4f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ledger/run-2026-08-12T0341Z.json",
         int(sys.argv[2]) if len(sys.argv) > 2 else 10000,
         int(sys.argv[3]) if len(sys.argv) > 3 else 20260812)
