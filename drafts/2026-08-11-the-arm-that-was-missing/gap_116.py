#!/usr/bin/env python3
"""What the crossed design effect does to the two findings that are not simple proportions.

Session 116, 2026-08-13. No new requests.

Session 115 restated two derived quantities at the account-key design effect 1.4289: the
encyclopedia-vs-forum gap of INCREMENT-1 §7 and the Mantel-Haenszel odds ratio of INCREMENT-3
§2a. Tonight's crossed model puts the design effect on the same population at 1.9900. Both are
recomputed here at the crossed value, and at ARM-SPECIFIC crossed design effects computed
tonight from the day-2 run — the crossed analogue of the arm-specific account figures session
115 published (1.4688 article / 1.1859 forum).

Every session-115 figure is reproduced from its own inputs by this file BEFORE the new one is
computed. If a reproduction fails it is printed as a failure and nothing downstream is claimed.

Usage: python3 gap_116.py
"""
import json
import math

from cluster_model import load
from cluster_keys import page_index
from crossed_model import agg, stats

Z = 1.959963985
DAY2 = "ledger/run-2026-08-12T0341Z.json"
DEFF_ACCOUNT = 1.428865343926577
ENC = (1940, 2175)     # retrievable, n — INCREMENT-1 §7, session 110's run
FOR = (381, 447)


def arm_crossed_deff(stratum_filter, label):
    d, rows_all, _, _ = load(DAY2)
    pidx = page_index()
    rows = [r for r in rows_all if r["vid"] in pidx and stratum_filter(r)]
    ag_a = agg(rows, lambda r: r["handle"])
    ag_p = agg(rows, lambda r: pidx[r["vid"]])
    ag_c = agg(rows, lambda r: (r["handle"], pidx[r["vid"]]))
    s = stats(len(rows), sum(r["absent"] for r in rows), ag_a, ag_p, ag_c, fpc=True)
    return {"arm": label, "units": len(rows), "absent": sum(r["absent"] for r in rows),
            "deff_account_only": s["deff_account_only"],
            "deff_page_only": s["deff_page_only"],
            "deff_crossed": s["deff_crossed_cgm_route2"],
            "sigma2_A": s["sigma2_A"], "sigma2_P": s["sigma2_P"],
            "clusters_A": s["clusters_A"], "clusters_P": s["clusters_P"]}


def gap(deff_enc, deff_for, label):
    ke, ne = ENC
    kf, nf = FOR
    pe, pf = ke / ne, kf / nf
    var = pe * (1 - pe) / ne * deff_enc + pf * (1 - pf) / nf * deff_for
    se = math.sqrt(var) * 100
    g = (pe - pf) * 100
    return {"variant": label, "deff_encyclopedia": deff_enc, "deff_forum": deff_for,
            "gap_pp": round(g, 4), "se_pp": round(se, 4), "z": round(g / se, 4),
            "ci95_pp": [round(g - Z * se, 4), round(g + Z * se, 4)],
            "excludes_0": (g - Z * se) > 0}


def mh(deff, label):
    """Published CI [1.357, 2.345] around 1.7839; log-scale SE inflated by sqrt(DEFF)."""
    lo, hi, pt = 1.357, 2.345, 1.7839
    se_log = (math.log(hi) - math.log(lo)) / 2 / Z
    se_c = se_log * math.sqrt(deff)
    return {"variant": label, "deff": deff, "point": pt,
            "se_log_published": round(se_log, 6), "se_log_corrected": round(se_c, 6),
            "ci95": [round(math.exp(math.log(pt) - Z * se_c), 4),
                     round(math.exp(math.log(pt) + Z * se_c), 4)],
            "excludes_1": math.exp(math.log(pt) - Z * se_c) > 1.0}


if __name__ == "__main__":
    cr = json.load(open("crossed-116-day2.json"))
    DEFF_CROSSED = cr["primary"]["with_finite_cluster_factor"]["deff_crossed_cgm_route2"]

    # Session 115's arm-specific figure used the ARTICLE arm alone (1.4688). Both readings of
    # "encyclopedia" are computed, because the two differ and choosing after seeing the answer is
    # the move this arc has caught itself making twice.
    art = arm_crossed_deff(lambda r: r["stratum"] == "W-article", "encyclopedia (article only)")
    artx = arm_crossed_deff(lambda r: r["stratum"] in ("W-article", "W-other-ns"),
                            "encyclopedia (article + other namespaces)")
    frm = arm_crossed_deff(lambda r: r["stratum"] == "F-forum", "forum")

    variants = [
        gap(1.0, 1.0, "published (no clustering)"),
        gap(DEFF_ACCOUNT, DEFF_ACCOUNT, "pooled account DEFF 1.4289 (session 115)"),
        gap(1.4688, 1.1859, "arm-specific account DEFFs (session 115)"),
        gap(DEFF_CROSSED, DEFF_CROSSED, "pooled crossed DEFF (session 116)"),
        gap(art["deff_crossed"], frm["deff_crossed"],
            "arm-specific crossed DEFFs, article arm (session 116)"),
        gap(artx["deff_crossed"], frm["deff_crossed"],
            "arm-specific crossed DEFFs, article + other ns (session 116)"),
    ]
    checks = {
        "reproduces_published_z_2.194": abs(variants[0]["z"] - 2.194) < 0.002,
        "reproduces_115_pooled_z_1.8355": abs(variants[1]["z"] - 1.8355) < 0.002,
        "reproduces_115_armspecific_z_1.9828": abs(variants[2]["z"] - 1.9828) < 0.002,
    }
    mhs = [mh(1.0, "published"), mh(DEFF_ACCOUNT, "account DEFF (session 115)"),
           mh(DEFF_CROSSED, "crossed DEFF (session 116)")]
    checks["reproduces_115_article_arm_account_deff_1.4688"] = abs(art["deff_account_only"] - 1.4688) < 0.001
    checks["reproduces_115_forum_arm_account_deff_1.1859"] = abs(frm["deff_account_only"] - 1.1859) < 0.001
    checks["reproduces_115_mh_ci"] = (abs(mhs[1]["ci95"][0] - 1.2864) < 0.001
                                      and abs(mhs[1]["ci95"][1] - 2.4737) < 0.001)

    out = {"session": 116, "generated_utc": "2026-08-13",
           "deff_crossed_pooled": DEFF_CROSSED,
           "arm_crossed_deffs": [art, artx, frm],
           "reproduction_checks_of_session_115": checks,
           "gap_variants": variants, "mantel_haenszel_variants": mhs}
    json.dump(out, open("gap-116.json", "w"), indent=1)

    for k, v in checks.items():
        print(f"CHECK {'PASS' if v else 'FAIL'}  {k}")
    for a in (art, artx, frm):
        print(f"arm {a['arm']:42s} n={a['units']:5d} absent={a['absent']:4d}  "
              f"account {a['deff_account_only']:.4f}  page {a['deff_page_only']:.4f}  "
              f"crossed {a['deff_crossed']:.4f}")
    for v in variants:
        print(f"gap  {v['variant']:56s} z={v['z']:.4f}  "
              f"CI [{v['ci95_pp'][0]:7.4f}, {v['ci95_pp'][1]:.4f}]  excl0={v['excludes_0']}")
    for m in mhs:
        print(f"MH   {m['variant']:44s} CI [{m['ci95'][0]:.4f}, {m['ci95'][1]:.4f}]  "
              f"excl1={m['excludes_1']}")
    print("wrote gap-116.json")
