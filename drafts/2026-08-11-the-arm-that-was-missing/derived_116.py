#!/usr/bin/env python3
"""Every number this session's prose derives rather than reads, computed and written down.

Session 116, 2026-08-13. Pass 1 of prose_vs_json.py flagged four values in INCREMENT-6.md that
occur in no machine-written file of this draft. All four were arithmetic done in the prose:
sums and differences of values that ARE in the files. Doing that arithmetic in a sentence is
exactly how a number gets into this record with nothing behind it, so it is done here instead
and the sentence quotes this file.

No new requests. Reads crossed-116.json and crossed-116-day2.json only.

Usage: python3 derived_116.py
"""
import json

d3 = json.load(open("crossed-116.json"))["primary"]["no_finite_cluster_factor"]
d2 = json.load(open("crossed-116-day2.json"))["primary"]["no_finite_cluster_factor"]

cell_cov = d3["sigma2_A"] + d3["sigma2_P"] + d3["sigma2_AP"]
additive = d3["sigma2_A"] + d3["sigma2_P"]
incl_exc = d3["deff_account_only"] + d3["deff_page_only"] - d3["deff_cell_only"]

out = {
    "session": 116, "generated_utc": "2026-08-13",
    "what_this_is": "arithmetic the prose of INCREMENT-6.md performs, done in code instead",
    "day3_cell_pair_covariance_sigma2A_plus_sigma2P_plus_sigma2AP": cell_cov,
    "day3_additive_prediction_sigma2A_plus_sigma2P": additive,
    "day3_ratio_observed_over_additive": cell_cov / additive,
    "crossed_deff_day2_minus_day3": d2["deff_crossed_cgm_route2"] - d3["deff_crossed_cgm_route2"],
    "inclusion_exclusion_identity": {
        "account_plus_page_minus_cell": incl_exc,
        "crossed_deff_direct": d3["deff_crossed_direct_doublesum"],
        "difference": incl_exc - d3["deff_crossed_direct_doublesum"],
        "holds": abs(incl_exc - d3["deff_crossed_direct_doublesum"]) < 1e-9},
    "share_of_page_variance_in_the_heaviest_article": None,
}
w = json.load(open("crossed-116.json"))["without_heaviest_page"]["no_finite_cluster_factor"]
out["share_of_page_variance_in_the_heaviest_article"] = 1 - w["sigma2_P"] / d3["sigma2_P"]

json.dump(out, open("derived-116.json", "w"), indent=1)
for k, v in out.items():
    if isinstance(v, float):
        print(f"{k:62s} {v:.8f}")
print(f"inclusion-exclusion identity holds: {out['inclusion_exclusion_identity']['holds']} "
      f"(difference {out['inclusion_exclusion_identity']['difference']:.3e})")
print("wrote derived-116.json")
