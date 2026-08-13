#!/usr/bin/env python3
"""The model this arc owed: both random effects at once — the account AND the citing page.

Session 116, 2026-08-13 (second session of the date). Pre-registered in PREREGISTRATION-116.md
before this file was run. NO new requests: a re-analysis of runs already collected. The window
population, its manifest and its probe are untouched.

WHY
---
Session 114 measured two design effects on the same units and never together: the account handle
gives 1.4289, the citing page gives 1.8854 (cluster-keys-114.json, closed form, no seed). Neither
is right. The account key ignores that two accounts' videos can sit on one page; the page key
ignores that one account's videos sit on many pages. Session 115's permutation test tried to
separate them and had no power — 113 of 3,575 units could move and none of them lay in the article
carrying the whole page effect — so it was withdrawn the same night.

THE MODEL
---------
    y_i = mu + a_{A(i)} + b_{P(i)} + (ab)_{A(i)P(i)} + e_i

crossed, not nested. Route 1 estimates sigma2_A, sigma2_P, sigma2_AP by moments on pairwise
products, in closed form, no seed. Route 2 is the two-way cluster-robust estimator of Cameron,
Gelbach & Miller: one-way variances on each key and on their intersection, "add the first two
variance matrices and subtract the third"
(https://cameron.econ.ucdavis.edu/research/JBESpaper2009version.pdf).

Both routes are computed, plus the direct double sum, because a claim that two routes agree is
worth nothing until you have checked whether they are the same estimator wearing two hats.

Route 3 is an envelope that assumes nothing: accounts and pages form a bipartite graph, all
dependence this model can express lies inside a CONNECTED COMPONENT, so components are a
legitimate one-way key and their design effect bounds the crossed one from above. The bootstrap
resamples components, which is the only resampling scheme here that respects both effects at once.

ALL BOOTSTRAP STATISTICS ARE LINEAR IN PER-COMPONENT AGGREGATES
---------------------------------------------------------------
Every quantity below reduces to sums of n_k^2, A_k^2 and A_k*n_k over the clusters of a key, and
each cluster lies wholly inside one component. So a draw costs O(components), not O(units), and is
exact rather than approximate.

Usage: python3 crossed_model.py [run.json] [draws] [seed]
"""
import json
import random
import sys

from cluster_model import load
from cluster_keys import page_index

DRAWS = 10000
SEED = 116116


# ---------------------------------------------------------------- key aggregates

def agg(rows, keyfn):
    """sum n_k^2, sum A_k^2, sum A_k n_k, cluster count — over the clusters of one key."""
    g = {}
    for r in rows:
        k = keyfn(r)
        n, a = g.get(k, (0, 0))
        g[k] = (n + 1, a + r["absent"])
    sq = sum(n * n for n, _ in g.values())
    aa = sum(a * a for _, a in g.values())
    an = sum(a * n for n, a in g.values())
    return {"sq": sq, "aa": aa, "an": an, "K": len(g)}


def sum_S2(ag, p):
    """sum_k (A_k - p*n_k)^2, the key's clustered cross-product sum, at absence rate p."""
    return ag["aa"] - 2 * p * ag["an"] + p * p * ag["sq"]


def stats(N, A, ag_a, ag_p, ag_c, fpc=False):
    """Every published quantity of this session, from key aggregates alone.

    fpc=True applies the K/(K-1) finite-cluster factor each one-way component of the arc's
    published estimator carries; the algebraic identity between the routes holds only at
    fpc=False, which is why both are reported.
    """
    if N == 0 or A == 0 or A == N:
        return None
    p = A / N
    u2 = N * p * (1 - p)                      # = sum_i (y_i - p)^2, exact for binary y
    SA, SP, SC = sum_S2(ag_a, p), sum_S2(ag_p, p), sum_S2(ag_c, p)

    # ordered same-cluster pair counts, i != j
    M_A, M_P, M_C = ag_a["sq"] - N, ag_p["sq"] - N, ag_c["sq"] - N
    # cross-product sums over those same pair sets
    T_A, T_P, T_C = SA - u2, SP - u2, SC - u2
    T_A_only, T_P_only = T_A - T_C, T_P - T_C
    M_A_only, M_P_only = M_A - M_C, M_P - M_C

    s2_A = T_A_only / M_A_only if M_A_only > 0 else None
    s2_P = T_P_only / M_P_only if M_P_only > 0 else None
    s2_C = (T_C / M_C - (s2_A or 0) - (s2_P or 0)) if M_C > 0 else None

    out = {"N": N, "absent": A, "rate": p,
           "sigma2_A": s2_A, "sigma2_P": s2_P, "sigma2_AP": s2_C,
           "sigma2_total": p * (1 - p),
           "clusters_A": ag_a["K"], "clusters_P": ag_p["K"], "clusters_AP": ag_c["K"],
           "pairs_same_account_diff_page": M_A_only,
           "pairs_same_page_diff_account": M_P_only,
           "pairs_same_cell": M_C}

    v_binom = p * (1 - p) / N
    f = (lambda K: K / (K - 1) if fpc and K > 1 else 1.0)
    v_A = f(ag_a["K"]) * SA / N ** 2
    v_P = f(ag_p["K"]) * SP / N ** 2
    v_C = f(ag_c["K"]) * SC / N ** 2
    v_2way = v_A + v_P - v_C

    # route 1: model variance of the mean from the variance components
    v_model = (u2 + (s2_A or 0) * M_A + (s2_P or 0) * M_P + (s2_C or 0) * M_C) / N ** 2
    # the direct double sum, 1[same account OR same page], by inclusion-exclusion
    v_direct = (SA + SP - SC) / N ** 2

    out.update({
        "deff_account_only": v_A / v_binom,
        "deff_page_only": v_P / v_binom,
        "deff_cell_only": v_C / v_binom,
        "deff_crossed_model_route1": v_model / v_binom,
        "deff_crossed_cgm_route2": v_2way / v_binom,
        "deff_crossed_direct_doublesum": v_direct / v_binom,
        "var_2way": v_2way, "var_binomial": v_binom, "fpc_applied": fpc})
    return out


# ---------------------------------------------------------------- components

def components(rows, pidx):
    """Connected components of the bipartite account x page graph. Union-find, no recursion."""
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for r in rows:
        union(("a", r["handle"]), ("p", pidx[r["vid"]]))
    comp = {}
    for r in rows:
        comp.setdefault(find(("a", r["handle"])), []).append(r)
    return list(comp.values())


def comp_aggregates(comps, pidx):
    """Per component: N, A and the three key aggregates — everything a draw needs."""
    out = []
    for c in comps:
        out.append({
            "N": len(c), "A": sum(r["absent"] for r in c),
            "a": agg(c, lambda r: r["handle"]),
            "p": agg(c, lambda r: pidx[r["vid"]]),
            "c": agg(c, lambda r: (r["handle"], pidx[r["vid"]]))})
    return out


def combine(cs):
    N = sum(c["N"] for c in cs)
    A = sum(c["A"] for c in cs)
    ks = {}
    for k in ("a", "p", "c"):
        ks[k] = {f: sum(c[k][f] for c in cs) for f in ("sq", "aa", "an", "K")}
    return N, A, ks


def bootstrap(cas, draws, seed, fpc=False):
    """Resample components with replacement — the only scheme respecting both effects."""
    rng = random.Random(seed)
    K = len(cas)
    keep = {"sigma2_A": [], "sigma2_P": [], "sigma2_AP": [],
            "deff_crossed_model_route1": [], "deff_account_only": [], "deff_page_only": []}
    failed = 0
    for _ in range(draws):
        pick = [cas[rng.randrange(K)] for _ in range(K)]
        N, A, ks = combine(pick)
        s = stats(N, A, ks["a"], ks["p"], ks["c"], fpc=fpc)
        if s is None:
            failed += 1
            continue
        for k in keep:
            if s[k] is not None:
                keep[k].append(s[k])
    out = {"draws": draws, "seed": seed, "components_resampled": K, "degenerate_draws": failed}
    for k, v in keep.items():
        v.sort()
        n = len(v)
        out[k] = {"lo95": v[int(0.025 * n)], "hi95": v[int(0.975 * n)],
                  "median": v[n // 2], "n_draws_used": n,
                  "excludes_zero": v[int(0.025 * n)] > 0} if n else None
    return out


# ---------------------------------------------------------------- one population

def analyse(rows, pidx, label, draws, seed):
    ag_a = agg(rows, lambda r: r["handle"])
    ag_p = agg(rows, lambda r: pidx[r["vid"]])
    ag_c = agg(rows, lambda r: (r["handle"], pidx[r["vid"]]))
    N = len(rows)
    A = sum(r["absent"] for r in rows)

    plain = stats(N, A, ag_a, ag_p, ag_c, fpc=False)
    corr = stats(N, A, ag_a, ag_p, ag_c, fpc=True)

    comps = components(rows, pidx)
    comps.sort(key=len, reverse=True)
    comp_of = {}
    for i, c in enumerate(comps):
        for x in c:
            comp_of[x["vid"]] = i
    ag_comp = agg(rows, lambda r: comp_of[r["vid"]])
    comp_deff = stats(N, A, ag_comp, ag_comp, ag_comp, fpc=False)

    cas = comp_aggregates(comps, pidx)
    boot = bootstrap(cas, draws, seed, fpc=False)

    return {
        "label": label, "units": N, "absent": A, "rate": A / N,
        "no_finite_cluster_factor": plain,
        "with_finite_cluster_factor": corr,
        "components": {
            "count": len(comps),
            "largest_units": len(comps[0]),
            "largest_share": len(comps[0]) / N,
            "singleton_components": sum(1 for c in comps if len(c) == 1),
            "deff_component_key": comp_deff["deff_account_only"],
            "kish_components": ag_comp["sq"] / N},
        "component_bootstrap": boot,
        "identity_check_route2_minus_direct":
            plain["deff_crossed_cgm_route2"] - plain["deff_crossed_direct_doublesum"],
        "identity_check_route1_minus_route2":
            plain["deff_crossed_model_route1"] - plain["deff_crossed_cgm_route2"]}


# ---------------------------------------------------------------- main

def main(run_path, draws, seed):
    d, rows_all, excl, _ = load(run_path)
    pidx = page_index()
    rows = [r for r in rows_all if r["vid"] in pidx]

    res = {
        "script": "crossed_model.py", "run": run_path, "run_id": d["run_id"],
        "run_utc_start": d["run_utc_start"],
        "analysis_population_before_page_attribution": len(rows_all),
        "attributed_units": len(rows),
        "attributed_share": len(rows) / len(rows_all),
        "exclusions_from_load": excl,
        "primary": analyse(rows, pidx, "day-3 crossed subset", draws, seed)}

    # P3: drop the single heaviest page and re-run everything
    byp = {}
    for r in rows:
        byp.setdefault(pidx[r["vid"]], []).append(r)
    worst = max(byp, key=lambda k: sum(x["absent"] for x in byp[k]))
    res["heaviest_page"] = {
        "key": worst, "units": len(byp[worst]),
        "absent": sum(x["absent"] for x in byp[worst]),
        "distinct_handles": len({x["handle"] for x in byp[worst]})}
    res["without_heaviest_page"] = analyse(
        [r for r in rows if pidx[r["vid"]] != worst], pidx,
        "day-3 crossed subset, heaviest page removed", draws, seed + 1)
    return res


if __name__ == "__main__":
    run = sys.argv[1] if len(sys.argv) > 1 else "ledger/run-2026-08-13T0427Z.json"
    draws = int(sys.argv[2]) if len(sys.argv) > 2 else DRAWS
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else SEED
    out = main(run, draws, seed)
    name = "crossed-116.json" if "08-13" in run else "crossed-116-day2.json"
    json.dump(out, open(name, "w"), indent=1)

    P = out["primary"]["no_finite_cluster_factor"]
    C = out["primary"]["with_finite_cluster_factor"]
    print(f"population   {out['attributed_units']}/{out['analysis_population_before_page_attribution']}"
          f" attributed = {100*out['attributed_share']:.2f}%   rate {100*P['rate']:.4f}%")
    print(f"components   {out['primary']['components']['count']}  largest "
          f"{out['primary']['components']['largest_units']} units "
          f"({100*out['primary']['components']['largest_share']:.1f}%)  "
          f"DEFF_component {out['primary']['components']['deff_component_key']:.4f}")
    print(f"sigma2_A {P['sigma2_A']:.8f}   sigma2_P {P['sigma2_P']:.8f}   "
          f"sigma2_AP {P['sigma2_AP']:.8f}   sigma2_total {P['sigma2_total']:.8f}")
    print(f"DEFF  account-only {P['deff_account_only']:.4f} | page-only {P['deff_page_only']:.4f} "
          f"| cell-only {P['deff_cell_only']:.4f}")
    print(f"DEFF  route1 model {P['deff_crossed_model_route1']:.6f} | route2 CGM "
          f"{P['deff_crossed_cgm_route2']:.6f} | direct {P['deff_crossed_direct_doublesum']:.6f}")
    print(f"      identity r2-direct {out['primary']['identity_check_route2_minus_direct']:.3e}  "
          f"r1-r2 {out['primary']['identity_check_route1_minus_route2']:.3e}")
    print(f"DEFF  with K/(K-1): account {C['deff_account_only']:.4f} page {C['deff_page_only']:.4f} "
          f"crossed {C['deff_crossed_cgm_route2']:.4f}")
    b = out["primary"]["component_bootstrap"]
    for k in ("sigma2_A", "sigma2_P", "deff_crossed_model_route1"):
        v = b[k]
        print(f"boot  {k:26s} [{v['lo95']:.8f}, {v['hi95']:.8f}] median {v['median']:.8f} "
              f"excludes0={v['excludes_zero']}")
    w = out["heaviest_page"]
    print(f"heaviest page {w['key']}  units {w['units']} absent {w['absent']} "
          f"handles {w['distinct_handles']}")
    W = out["without_heaviest_page"]
    print(f"without it: sigma2_P {W['no_finite_cluster_factor']['sigma2_P']:.8f}  "
          f"crossed DEFF {W['no_finite_cluster_factor']['deff_crossed_model_route1']:.4f}  "
          f"boot sigma2_P [{W['component_bootstrap']['sigma2_P']['lo95']:.8f}, "
          f"{W['component_bootstrap']['sigma2_P']['hi95']:.8f}]")
    print(f"wrote {name}")
