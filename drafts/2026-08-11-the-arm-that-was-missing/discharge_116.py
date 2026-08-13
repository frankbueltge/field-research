#!/usr/bin/env python3
"""Discharging the conditions of INTERLOCUTOR-8 and the qualifications of SPECIALIST-crossed-116.

Session 116, 2026-08-13. No new requests. Every figure either role used against this session is
recomputed here with this practice's own code BEFORE it is accepted, as at sessions 110-115.

What is recomputed:
  C1  the concentration of the page signal the component bootstrap resamples — is the 95 % interval
      resting on 2,394 draws or on one article? Herfindahl over per-component contributions to the
      same-page-different-account cross-product sum, and the effective cluster count it implies.
  C1b the share of the crossed design effect's EXCESS over 1 that the heaviest article carries.
  C2  the bootstrap interval on sigma2_AP, which this session computed and then printed as an
      em-dash.
  S4  a delete-one-component jackknife on sigma2_P and on the crossed design effect — deterministic,
      no seed, a different variance estimator on the same partition.
  S3b what the pooled design effect costs the two strata whose own crossed values are known.
  S5  the encyclopedia-vs-forum gap bootstrapped DIRECTLY over components, with no design effect
      anywhere in the computation — the check the sqrt(DEFF) route never had.

Usage: python3 discharge_116.py [draws] [seed]
"""
import json
import random
import sys

from cluster_model import load
from cluster_keys import page_index
from crossed_model import agg, stats, components, comp_aggregates

DAY3 = "ledger/run-2026-08-13T0427Z.json"
DAY2 = "ledger/run-2026-08-12T0341Z.json"
Z = 1.959963985


def rows_of(run):
    _, rows_all, _, _ = load(run)
    pidx = page_index()
    return [r for r in rows_all if r["vid"] in pidx], pidx


def signal_by_component(rows, pidx, comps, key, other):
    """Per-component contribution to the cross-product sum over pairs sharing `key` but not `other`.

    Decomposable because every cluster of either key lies wholly inside one component.
    For a component c:  sum_{k in c} S_k^2  -  sum_{cells in c} S_cell^2   (the 'only' pair class),
    with S_x = sum of (y_i - p) over the units of x, p the POOLED rate (the bootstrap's own centre).
    """
    N = len(rows)
    p = sum(r["absent"] for r in rows) / N
    out = []
    for c in comps:
        sk = {}
        sc = {}
        for r in c:
            k = key(r, pidx)
            cell = (r["handle"], pidx[r["vid"]])
            sk[k] = sk.get(k, 0.0) + (r["absent"] - p)
            sc[cell] = sc.get(cell, 0.0) + (r["absent"] - p)
        out.append(sum(v * v for v in sk.values()) - sum(v * v for v in sc.values()))
    return out


def concentration(contrib, comps):
    """Herfindahl over |contribution| shares, and the effective number of contributing clusters.

    |contribution| because a contribution can be negative and a share of a signed total is not a
    weight. The choice is stated rather than hidden; the raw-signed share of the largest is
    reported beside it so both readings are on the record.
    """
    tot_abs = sum(abs(x) for x in contrib)
    tot_raw = sum(contrib)
    if tot_abs == 0:
        return None
    shares = [abs(x) / tot_abs for x in contrib]
    h = sum(s * s for s in shares)
    i = max(range(len(contrib)), key=lambda j: abs(contrib[j]))
    return {"total_signed": tot_raw, "total_absolute": tot_abs,
            "components_with_nonzero_contribution": sum(1 for x in contrib if abs(x) > 1e-12),
            "herfindahl": h, "effective_clusters": 1.0 / h,
            "largest_contributor_units": len(comps[i]),
            "largest_share_of_absolute": shares[i],
            "largest_share_of_signed_total": contrib[i] / tot_raw if tot_raw else None}


def jackknife(cas, fpc=False):
    """Delete-one-component. Deterministic, no seed. Total-minus-one over the aggregates."""
    K = len(cas)
    tot = {"N": sum(c["N"] for c in cas), "A": sum(c["A"] for c in cas)}
    keys = {k: {f: sum(c[k][f] for c in cas) for f in ("sq", "aa", "an", "K")}
            for k in ("a", "p", "c")}
    vals = {"sigma2_P": [], "deff": []}
    for c in cas:
        N = tot["N"] - c["N"]
        A = tot["A"] - c["A"]
        ks = {k: {f: keys[k][f] - c[k][f] for f in ("sq", "aa", "an", "K")}
              for k in ("a", "p", "c")}
        s = stats(N, A, ks["a"], ks["p"], ks["c"], fpc=fpc)
        if s is None or s["sigma2_P"] is None:
            continue
        vals["sigma2_P"].append(s["sigma2_P"])
        vals["deff"].append(s["deff_crossed_cgm_route2"])
    out = {}
    for name, v in vals.items():
        n = len(v)
        mean = sum(v) / n
        var = (n - 1) / n * sum((x - mean) ** 2 for x in v)
        se = var ** 0.5
        full = None
        out[name] = {"n_deletions": n, "jackknife_se": se, "pseudo_mean": mean}
        out[name]["ci95_about_full"] = None  # filled by caller, which holds the full-sample value
        out[name]["_se"] = se
    return out


def gap_component_bootstrap(run, draws, seed):
    """The gap with NO design effect anywhere: resample components, recompute both arms' rates."""
    rows, pidx = rows_of(run)
    comps = components(rows, pidx)
    enc = lambda r: r["stratum"] in ("W-article", "W-other-ns")
    packs = []
    for c in comps:
        ke = sum(1 - r["absent"] for r in c if enc(r))
        ne = sum(1 for r in c if enc(r))
        kf = sum(1 - r["absent"] for r in c if not enc(r))
        nf = sum(1 for r in c if not enc(r))
        packs.append((ke, ne, kf, nf))
    both = sum(1 for ke, ne, kf, nf in packs if ne and nf)
    KE = sum(p[0] for p in packs); NE = sum(p[1] for p in packs)
    KF = sum(p[2] for p in packs); NF = sum(p[3] for p in packs)
    point = (KE / NE - KF / NF) * 100
    rng = random.Random(seed)
    K = len(packs)
    draws_out = []
    for _ in range(draws):
        ke = ne = kf = nf = 0
        for _ in range(K):
            a, b, c_, d = packs[rng.randrange(K)]
            ke += a; ne += b; kf += c_; nf += d
        if ne and nf:
            draws_out.append((ke / ne - kf / nf) * 100)
    draws_out.sort()
    n = len(draws_out)
    lo, hi = draws_out[int(0.025 * n)], draws_out[int(0.975 * n)]
    return {"run": run, "units": len(rows), "components": K,
            "components_spanning_both_strata": both,
            "encyclopedia": [KE, NE], "forum": [KF, NF],
            "gap_pp_on_this_run": point,
            "ci95_pp_component_bootstrap": [lo, hi], "excludes_0": lo > 0,
            "draws": n, "seed": seed,
            "note": ("this is the gap ON THIS RUN, not the published 3.9605 pp of INCREMENT-1 §7, "
                     "which was measured on session 110's run; the point of the check is the "
                     "interval's width and sign, not the centre")}


def main(draws, seed):
    out = {"session": 116, "no_new_requests": True,
           "reproducing": ["INTERLOCUTOR-8 C1, C1b, C2", "SPECIALIST-crossed-116 §3b, §4, §5"]}

    for label, run in (("day3", DAY3), ("day2", DAY2)):
        rows, pidx = rows_of(run)
        comps = components(rows, pidx)
        comps.sort(key=len, reverse=True)

        page_sig = signal_by_component(rows, pidx, comps,
                                       lambda r, i: i[r["vid"]], "account")
        acct_sig = signal_by_component(rows, pidx, comps,
                                       lambda r, i: r["handle"], "page")
        out[f"C1_page_signal_concentration_{label}"] = concentration(page_sig, comps)
        out[f"C1_account_signal_concentration_{label}"] = concentration(acct_sig, comps)

        cas = comp_aggregates(comps, pidx)
        jk = jackknife(cas)
        full = stats(len(rows), sum(r["absent"] for r in rows),
                     agg(rows, lambda r: r["handle"]),
                     agg(rows, lambda r: pidx[r["vid"]]),
                     agg(rows, lambda r: (r["handle"], pidx[r["vid"]])), fpc=False)
        for name, key in (("sigma2_P", "sigma2_P"), ("deff", "deff_crossed_cgm_route2")):
            se = jk[name].pop("_se")
            v = full[key]
            jk[name]["full_sample"] = v
            jk[name]["ci95_about_full"] = [v - Z * se, v + Z * se]
            jk[name]["excludes_zero"] = (v - Z * se) > 0
        out[f"S4_jackknife_{label}"] = jk

    # C1b: how much of the crossed design effect's excess over 1 the heaviest article carries
    d3 = json.load(open("crossed-116.json"))
    with_art = d3["primary"]["no_finite_cluster_factor"]["deff_crossed_cgm_route2"]
    without = d3["without_heaviest_page"]["no_finite_cluster_factor"]["deff_crossed_cgm_route2"]
    out["C1b_excess_deff_carried_by_heaviest_article"] = {
        "deff_with": with_art, "deff_without": without,
        "excess_with": with_art - 1, "excess_without": without - 1,
        "share_of_excess": ((with_art - 1) - (without - 1)) / (with_art - 1),
        "article_units": d3["heaviest_page"]["units"],
        "article_share_of_population": d3["heaviest_page"]["units"] / d3["attributed_units"]}

    # C2: the interval this session computed and printed as an em-dash
    out["C2_sigma2_AP_intervals"] = {
        "day3": d3["primary"]["component_bootstrap"]["sigma2_AP"],
        "day2": json.load(open("crossed-116-day2.json"))
                    ["primary"]["component_bootstrap"]["sigma2_AP"]}

    # S3b: what the pooled design effect costs the two strata whose own crossed values are known
    g = json.load(open("gap-116.json"))
    pooled = g["deff_crossed_pooled"]
    arms = {a["arm"]: a["deff_crossed"] for a in g["arm_crossed_deffs"]}
    out["S3b_pooled_versus_arm_specific"] = {
        "pooled_applied_to_every_row": pooled,
        "arms": arms,
        "article_interval_too_narrow_by": (arms["encyclopedia (article only)"] / pooled) ** 0.5,
        "forum_interval_too_wide_by": (pooled / arms["forum"]) ** 0.5}

    # S5: the gap with no design effect anywhere
    out["S5_gap_component_bootstrap_day2"] = gap_component_bootstrap(DAY2, draws, seed)
    out["S5_gap_component_bootstrap_day3"] = gap_component_bootstrap(DAY3, draws, seed + 1)

    json.dump(out, open("discharge-116.json", "w"), indent=1)

    for label in ("day3", "day2"):
        c = out[f"C1_page_signal_concentration_{label}"]
        a = out[f"C1_account_signal_concentration_{label}"]
        print(f"C1 {label}: page signal — {c['components_with_nonzero_contribution']} components "
              f"contribute, effective clusters {c['effective_clusters']:.2f}, largest "
              f"({c['largest_contributor_units']} units) holds "
              f"{100*c['largest_share_of_absolute']:.1f}% of |signal| and "
              f"{100*c['largest_share_of_signed_total']:.1f}% of the signed total")
        print(f"C1 {label}: account signal — effective clusters {a['effective_clusters']:.2f}")
        j = out[f"S4_jackknife_{label}"]
        for k in ("sigma2_P", "deff"):
            v = j[k]
            print(f"S4 {label}: {k:9s} full {v['full_sample']:.6f}  jackknife 95% "
                  f"[{v['ci95_about_full'][0]:.6f}, {v['ci95_about_full'][1]:.6f}]  "
                  f"excludes0={v['excludes_zero']}")
    e = out["C1b_excess_deff_carried_by_heaviest_article"]
    print(f"C1b: the article is {100*e['article_share_of_population']:.2f}% of units and carries "
          f"{100*e['share_of_excess']:.1f}% of the crossed DEFF's excess over 1")
    for d, v in out["C2_sigma2_AP_intervals"].items():
        print(f"C2 {d}: sigma2_AP 95% [{v['lo95']:.6f}, {v['hi95']:.6f}] "
              f"excludes0={v['excludes_zero']}")
    s = out["S3b_pooled_versus_arm_specific"]
    print(f"S3b: article rows too narrow by x{s['article_interval_too_narrow_by']:.4f}; "
          f"forum rows too wide by x{s['forum_interval_too_wide_by']:.4f}")
    for k in ("S5_gap_component_bootstrap_day2", "S5_gap_component_bootstrap_day3"):
        v = out[k]
        print(f"S5 {v['run'].split('/')[-1]}: gap {v['gap_pp_on_this_run']:.4f} pp  "
              f"CI [{v['ci95_pp_component_bootstrap'][0]:.4f}, "
              f"{v['ci95_pp_component_bootstrap'][1]:.4f}]  excl0={v['excludes_0']}  "
              f"(components spanning both strata: {v['components_spanning_both_strata']})")
    print("wrote discharge-116.json")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10000,
         int(sys.argv[2]) if len(sys.argv) > 2 else 811611)
