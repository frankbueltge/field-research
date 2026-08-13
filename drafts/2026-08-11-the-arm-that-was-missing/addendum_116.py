#!/usr/bin/env python3
"""The consequence the pre-registration committed to before the number was known.

Session 116, 2026-08-13. PREREGISTRATION-116.md: "If DEFF_crossed > 1.4289 + 0.05, then the 36
intervals restated this morning are STILL TOO NARROW, and they are recomputed at the crossed
design effect tonight, as a dated addendum to RESTATEMENT-2026-08-13.md — never a silent edit."

The crossed design effect came out at 1.9900 on the day-2 population (with the same K/(K-1)
finite-cluster factor the published 1.4289 carries), so the clause fires. Every one of the 36
intervals is recomputed here at the crossed value, beside — never instead of — the account-key
value session 115 published this morning.

NO new requests. Reads restatement-115.json and restatement-115b.json, both machine-written this
morning, and crossed-116-day2.json, machine-written tonight.

Usage: python3 addendum_116.py
"""
import json

import power_audit as pa

DEFF_ACCOUNT = 1.428865343926577       # cluster-keys-114.json C4, what this morning used
SRC_CROSSED = "crossed-116-day2.json"  # same population as the published restatement


def wilson_eff(k, n, deff):
    n_eff = n / deff
    k_eff = k * n_eff / n
    lo, hi = pa.wilson(k_eff, n_eff)
    return lo, hi, n_eff


def restate(entries, scale):
    """Recompute each published interval at the crossed DEFF. Point estimates must not move."""
    out = []
    for e in entries:
        k, n = e["k"], e["n"]
        lo_c, hi_c, neff_c = wilson_eff(k, n, DEFF_CROSSED)
        lo_a, hi_a, _ = wilson_eff(k, n, DEFF_ACCOUNT)
        s = scale
        row = {
            "label": e["label"], "k": k, "n": n,
            "point_estimate": e["point_estimate"],
            "point_estimate_recomputed": round(s * k / n, 4),
            "centre_moved": abs(s * k / n - e["point_estimate"]) > 0.0051,
            "restated_ci_account_key_115": e["restated_ci"],
            "reproduces_session_115_restatement": (
                abs(s * lo_a - e["restated_ci"][0]) < 0.0051
                and abs(s * hi_a - e["restated_ci"][1]) < 0.0051),
            "restated_ci_crossed_key_116": [round(s * lo_c, 4), round(s * hi_c, 4)],
            "n_eff_crossed": round(neff_c, 2),
            "width_account_key_115": round(e["restated_ci"][1] - e["restated_ci"][0], 4),
            "width_crossed_key_116": round(s * (hi_c - lo_c), 4),
        }
        row["wider_than_115"] = row["width_crossed_key_116"] > row["width_account_key_115"]
        row["further_widening_ratio"] = (
            round(row["width_crossed_key_116"] / row["width_account_key_115"], 4)
            if row["width_account_key_115"] else None)
        out.append(row)
    return out


if __name__ == "__main__":
    cr = json.load(open(SRC_CROSSED))
    DEFF_CROSSED = cr["primary"]["with_finite_cluster_factor"]["deff_crossed_cgm_route2"]
    DEFF_CROSSED_NOFPC = cr["primary"]["no_finite_cluster_factor"]["deff_crossed_cgm_route2"]

    a = json.load(open("restatement-115.json"))
    b = json.load(open("restatement-115b.json"))
    rows = restate(a["restated"], 100.0) + restate(b["restated"], 1.0)

    out = {
        "generated_utc": "2026-08-13",
        "session": 116,
        "what_this_is": (
            "A dated addendum to RESTATEMENT-2026-08-13.md, not an edit of it. This morning's "
            "restatement widened 36 published intervals at the account-key design effect 1.4289. "
            "Tonight's crossed model, carrying the account AND the citing page at once, puts the "
            "design effect on the same population at 1.9900. The 36 intervals are recomputed at "
            "the crossed value here. The morning's figures stand as published and are reproduced "
            "in every row; nothing is overwritten."),
        "deff_account_key_115": DEFF_ACCOUNT,
        "deff_crossed_key_116": DEFF_CROSSED,
        "deff_crossed_key_116_no_finite_cluster_factor": DEFF_CROSSED_NOFPC,
        "half_width_multiplier_115": DEFF_ACCOUNT ** 0.5,
        "half_width_multiplier_116": DEFF_CROSSED ** 0.5,
        "further_multiplier_116_over_115": (DEFF_CROSSED / DEFF_ACCOUNT) ** 0.5,
        "caveat": (
            "The crossed DEFF is measured on the day-2/day-3 crossed subset and is applied "
            "uniformly to every row, exactly as 1.4289 was applied uniformly this morning. For "
            "rows whose population is not that subset this is an approximation, and it is "
            "labelled one. Parameter-specific design effects differ: INTERLOCUTOR-7 established "
            "1.27 for the Weibull shape, so the shape interval remains the widest of the routes "
            "tested and is not widened again here."),
        "intervals": rows,
        "n_intervals": len(rows),
        "n_reproducing_session_115": sum(r["reproduces_session_115_restatement"] for r in rows),
        "n_wider_than_115": sum(r["wider_than_115"] for r in rows),
        "n_centres_moved": sum(r["centre_moved"] for r in rows),
    }
    json.dump(out, open("addendum-116.json", "w"), indent=1)
    print(f"DEFF account key (115) {DEFF_ACCOUNT:.4f}  ->  crossed key (116) {DEFF_CROSSED:.4f}")
    print(f"half-width multiplier  {DEFF_ACCOUNT**0.5:.4f}  ->  {DEFF_CROSSED**0.5:.4f}   "
          f"further factor {(DEFF_CROSSED/DEFF_ACCOUNT)**0.5:.4f}")
    print(f"intervals {out['n_intervals']}   reproduce 115 {out['n_reproducing_session_115']}   "
          f"wider than 115 {out['n_wider_than_115']}   centres moved {out['n_centres_moved']}")
    worst = max(rows, key=lambda r: r["further_widening_ratio"] or 0)
    least = min(rows, key=lambda r: r["further_widening_ratio"] or 9)
    print(f"largest further widening  {worst['further_widening_ratio']}  {worst['label'][:70]}")
    print(f"smallest further widening {least['further_widening_ratio']}  {least['label'][:70]}")
    print("wrote addendum-116.json")
