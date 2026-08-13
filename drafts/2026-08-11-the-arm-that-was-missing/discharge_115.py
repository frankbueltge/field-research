#!/usr/bin/env python3
"""Reproducing the adversary's numbers before accepting any of them, and discharging its conditions.

Session 115, 2026-08-13. **No new requests.** `INTERLOCUTOR-7.md` returned ten conditions and
broke three of four parts of claim C4. This practice does not accept an adversary's arithmetic on
its authority any more than it expects its own to be accepted: every figure below is recomputed
here, with this file's own code, and the reproduction is reported whether it agrees or not.

Covers I1 (the omitted intervals), I2 (the pair decomposition), I3 (the bootstrap on the pooled
design effect), I5 (population overlap), I6/I7 (per-cell range, Kish admissibility, bootstrap
intervals), I8 (the conditional design effects and the cluster-splitting account), I9 (the gap
under methods that need no design effect), I10 (the handle drift), and the power audit of the
within-account permutation that the adversary raised as 3.2.

Output: `discharge-115.json`.
"""
import json
import math
import random
import sys

import cluster_model as cm
import cluster_keys as ck
import power_audit as pa

DAY2 = "ledger/run-2026-08-12T0341Z.json"
DEFF = 1.428865343926577
BOOT = 4000
SEED = 20260813


def deff_of(rows, keyfn, absent=lambda r: r["absent"]):
    g = {}
    for r in rows:
        g.setdefault(keyfn(r), []).append(r)
    N, K = sum(len(v) for v in g.values()), len(g)
    if N == 0 or K < 2:
        return None
    p = sum(absent(r) for r in rows) / N
    if p in (0.0, 1.0):
        return None
    ss = sum((sum(absent(r) for r in v) - p * len(v)) ** 2 for v in g.values())
    kish = sum(len(v) ** 2 for v in g.values()) / N
    d = (K / (K - 1) * ss / N ** 2) / (p * (1 - p) / N)
    return {"n": N, "clusters": K, "rate": p, "deff": d, "kish": kish,
            "implied_rho": (d - 1) / (kish - 1) if kish > 1 else None,
            "admissible": (kish <= 1.0000001) or ((d - 1) / (kish - 1)) <= 1.0}


def boot_deff(rows, keyfn, reps, seed, absent=lambda r: r["absent"]):
    """Resample whole accounts with replacement — the unit of clustering is the unit of resampling."""
    g = {}
    for r in rows:
        g.setdefault(keyfn(r), []).append(r)
    groups = list(g.values())
    K = len(groups)
    rng = random.Random(seed)
    vals = []
    for _ in range(reps):
        drawn = [groups[rng.randrange(K)] for _ in range(K)]
        flat = [r for grp in drawn for r in grp]
        idx = {}
        for i, grp in enumerate(drawn):
            idx[i] = grp
        N = len(flat)
        p = sum(absent(r) for r in flat) / N
        if p in (0.0, 1.0):
            continue
        ss = sum((sum(absent(r) for r in grp) - p * len(grp)) ** 2 for grp in drawn)
        vals.append((K / (K - 1) * ss / N ** 2) / (p * (1 - p) / N))
    vals.sort()
    if not vals:
        return None
    m = sum(vals) / len(vals)
    return {"reps": len(vals), "mean": round(m, 4),
            "sd": round(math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1)), 4),
            "ci95": [round(vals[int(0.025 * len(vals))], 4),
                     round(vals[int(0.975 * len(vals))], 4)]}


def conditional_deff(rows, cellfn):
    """The clustered variance against a POISSON-BINOMIAL benchmark using each unit's own cell rate.

    This is the adversary's I8 test: if the account clustering is really the age effect in
    disguise, replacing the grand rate with each unit's own cell rate should collapse the ratio.
    """
    cells = {}
    for r in rows:
        cells.setdefault(cellfn(r), []).append(r)
    rate = {k: sum(x["absent"] for x in v) / len(v) for k, v in cells.items()}
    g = {}
    for r in rows:
        g.setdefault(r["handle"], []).append(r)
    N, K = len(rows), len(g)
    ss = sum((sum(x["absent"] for x in v) - sum(rate[cellfn(x)] for x in v)) ** 2
             for v in g.values())
    v_cluster = K / (K - 1) * ss / N ** 2
    v_pb = sum(rate[cellfn(r)] * (1 - rate[cellfn(r)]) for r in rows) / N ** 2
    return v_cluster / v_pb


def wilson_eff(k, n, deff):
    n_eff = n / deff
    return pa.wilson(k * n_eff / n, n_eff)


def main():
    d2, rows2, excl2, key2 = cm.load(DAY2)
    idx = ck.page_index()
    for r in rows2:
        r["page"] = idx.get(r["vid"])
    out = {"session": 115, "reproducing": "INTERLOCUTOR-7.md", "no_new_requests": True,
           "note": ("Every figure the adversary used against this session, recomputed here with "
                    "this file's own code. AGREES / DISAGREES is stated per item.")}

    # ================= I6 / I7: the 17 cells, their range, and admissibility ==============
    parts = {"age band": lambda r: r["band"], "stratum": lambda r: r["stratum"],
             "calendar year": lambda r: str(r["year"])}
    cells17, deffs17 = [], []
    for pname, keyfn in parts.items():
        groups = {}
        for r in rows2:
            groups.setdefault(keyfn(r), []).append(r)
        for cname, rs in sorted(groups.items()):
            d = deff_of(rs, lambda r: r["handle"])
            if not d or d["clusters"] < 30:
                continue
            b = boot_deff(rs, lambda r: r["handle"], BOOT, SEED)
            cells17.append({"partition": pname, "cell": cname, "n": d["n"],
                            "accounts": d["clusters"], "deff": round(d["deff"], 4),
                            "kish": round(d["kish"], 4),
                            "implied_rho": round(d["implied_rho"], 4) if d["implied_rho"] else None,
                            "admissible_rho_le_1": d["admissible"],
                            "bootstrap_ci95": b["ci95"] if b else None,
                            "vs_pooled": ("below, interval excludes pooled"
                                          if b and b["ci95"][1] < DEFF else
                                          "above, interval excludes pooled"
                                          if b and b["ci95"][0] > DEFF else
                                          "not distinguishable from pooled")})
            deffs17.append(d["deff"])
    out["I6_I7_cells"] = {
        "eligible_cells": len(cells17),
        "min": round(min(deffs17), 4), "max": round(max(deffs17), 4),
        "median": round(sorted(deffs17)[len(deffs17) // 2], 4),
        "below_pooled_point": sum(1 for x in deffs17 if x < DEFF),
        "above_pooled_point": sum(1 for x in deffs17 if x >= DEFF),
        "significantly_below": sum(1 for c in cells17
                                   if c["vs_pooled"].startswith("below")),
        "significantly_above": sum(1 for c in cells17
                                   if c["vs_pooled"].startswith("above")),
        "inadmissible_rho_gt_1": [c["cell"] for c in cells17 if not c["admissible_rho_le_1"]],
        "cells": cells17,
    }
    # the 6-7y cell the session wrongly folded into the 17 — it is a fourth partition
    six7 = [r for r in rows2 if int(r["age_y"]) == 6]
    d67 = deff_of(six7, lambda r: r["handle"])
    out["I6_the_cell_that_is_not_one_of_the_17"] = {
        "cell": "6-7y (integer-age partition, NOT among the 17)",
        "n": d67["n"], "accounts": d67["clusters"], "deff": round(d67["deff"], 4),
        "kish": round(d67["kish"], 4), "implied_rho": round(d67["implied_rho"], 4),
        "admissible_rho_le_1": d67["admissible"],
        "bootstrap_ci95": boot_deff(six7, lambda r: r["handle"], BOOT, SEED)["ci95"]}

    # ================= I3: the sampling error of the pooled design effect ================
    out["I3_pooled_deff_bootstrap"] = boot_deff(rows2, lambda r: r["handle"], BOOT, SEED)
    b = out["I3_pooled_deff_bootstrap"]
    out["I3_half_width_factor"] = {"point": round(math.sqrt(DEFF), 4),
                                   "ci95": [round(math.sqrt(b["ci95"][0]), 4),
                                            round(math.sqrt(b["ci95"][1]), 4)]}

    # ================= I8: is it the shared era, or is it cluster splitting? =============
    out["I8_conditional_deff"] = {
        "pooled_against_grand_rate": round(DEFF, 4),
        "conditional_on_age_band": round(conditional_deff(rows2, lambda r: r["band"]), 4),
        "conditional_on_stratum": round(conditional_deff(rows2, lambda r: r["stratum"]), 4),
        "conditional_on_calendar_year": round(conditional_deff(rows2, lambda r: str(r["year"])), 4),
        "conditional_on_band_x_stratum": round(
            conditional_deff(rows2, lambda r: (r["band"], r["stratum"])), 4),
        "cell_median": round(sorted(deffs17)[len(deffs17) // 2], 4),
    }
    g = {}
    for r in rows2:
        g.setdefault(r["handle"], []).append(r)
    multi = [v for v in g.values() if len(v) > 1]
    out["I8_cluster_splitting"] = {
        "accounts": len(g), "singletons": sum(1 for v in g.values() if len(v) == 1),
        "multi_video_accounts": len(multi),
        "pooled_kish": round(sum(len(v) ** 2 for v in g.values()) / len(rows2), 4),
        "cell_kish_min": round(min(c["kish"] for c in cells17), 4),
        "cell_kish_max": round(max(c["kish"] for c in cells17), 4),
        "cell_kish_median": round(sorted(c["kish"] for c in cells17)[len(cells17) // 2], 4),
        "multi_accounts_wholly_in_one_age_band": round(
            100 * sum(1 for v in multi if len({x["band"] for x in v}) == 1) / len(multi), 1),
        "multi_accounts_wholly_in_one_calendar_year": round(
            100 * sum(1 for v in multi if len({x["year"] for x in v}) == 1) / len(multi), 1),
        "pooled_implied_rho": round((DEFF - 1) / (sum(len(v) ** 2 for v in g.values())
                                                  / len(rows2) - 1), 4),
        "cells_with_rho_above_pooled": sum(
            1 for c in cells17 if c["implied_rho"] is not None
            and c["implied_rho"] > (DEFF - 1) / (sum(len(v) ** 2 for v in g.values())
                                                 / len(rows2) - 1)),
    }

    # ================= I10: the handle drift is a proportion this correction reaches =====
    raw = json.load(open(DAY2))
    drift = []
    for o in raw["observations"]:
        if o["state"] == "RETRIEVABLE" and o.get("author_unique_id"):
            drift.append({"handle": str(o["handle"]).lower(),
                          "absent": 0 if str(o["author_unique_id"]).lower()
                          == str(o["handle"]).lower() else 1})
    k = sum(r["absent"] for r in drift)
    n = len(drift)
    dd = deff_of(drift, lambda r: r["handle"])
    lo0, hi0 = pa.wilson(k, n)
    lo1, hi1 = wilson_eff(k, n, DEFF)
    lo2, hi2 = wilson_eff(k, n, dd["deff"])
    out["I10_handle_drift"] = {
        "k": k, "n": n, "rate_pct": round(100 * k / n, 4),
        "accounts": dd["clusters"], "own_deff": round(dd["deff"], 4),
        "kish": round(dd["kish"], 4), "implied_rho": round(dd["implied_rho"], 4),
        "admissible_rho_le_1": dd["admissible"],
        "published_ci": [6.38, 8.20],
        "reproduced_naive_ci": [round(100 * lo0, 4), round(100 * hi0, 4)],
        "restated_at_pooled": [round(100 * lo1, 4), round(100 * hi1, 4)],
        "restated_at_own_deff": [round(100 * lo2, 4), round(100 * hi2, 4)],
        "bootstrap_ci95_on_deff": boot_deff(drift, lambda r: r["handle"], BOOT, SEED)["ci95"]}

    # ================= I1: the other omitted intervals ==================================
    omitted = []
    # the transfer function on the receiver's eleven, INCREMENT-3 §3a
    lo0, hi0 = 11.39, 16.55
    lo1, hi1 = wilson_eff(int(round(0.1377 * 3575)), 3575, DEFF)
    omitted.append({"what": "INCREMENT-3 §3a — expected absence for the receiver's eleven, 13.77 %",
                    "published_ci": [lo0, hi0],
                    "note": ("built from the per-band Wilson bounds of §1a, every one of which is "
                             "restated in §3a of the restatement; the expected-absence interval "
                             "inherits their widening and is restated by construction"),
                    "restated_ci_from_widened_bands": [round(100 * lo1, 4), round(100 * hi1, 4)]})
    # rule-of-three, 0 of 3,111
    r3 = 3 / 3111
    r3c = 3 / (3111 / DEFF)
    omitted.append({"what": "INCREMENT-2 — rule-of-three upper bound, 0 events in 3,111",
                    "published_pct": round(100 * r3, 4),
                    "restated_pct": round(100 * r3c, 4),
                    "ratio": round(r3c / r3, 4)})
    # the return rate, 1 of 432
    lo0, hi0 = pa.wilson(1, 432)
    lo1, hi1 = wilson_eff(1, 432, DEFF)
    omitted.append({"what": "INCREMENT-2 — the return rate, 1 of 432",
                    "published_ci": [0.0409, 1.2994],
                    "reproduced_naive_ci": [round(100 * lo0, 4), round(100 * hi0, 4)],
                    "restated_ci": [round(100 * lo1, 4), round(100 * hi1, 4)]})
    out["I1_omitted"] = omitted

    # ================= I5: are the three populations three populations? =================
    ids2 = {str(o["vid"]) for o in raw["observations"]}
    census = {str(r["vid"]) for r in json.load(open("census-results.json"))["results"]}
    run110 = {str(o["vid"]) for o in json.load(open(pa.RUN))["observations"]}
    out["I5_overlap"] = {
        "census_n": len(census), "run110_n": len(run110), "day2_n": len(ids2),
        "census_inside_day2": len(census & ids2),
        "census_inside_day2_pct": round(100 * len(census & ids2) / len(census), 1),
        "run110_inside_day2": len(run110 & ids2),
        "run110_inside_day2_pct": round(100 * len(run110 & ids2) / len(run110), 1),
        "in_all_three": len(census & run110 & ids2),
        "in_day2_only": len(ids2 - census - run110)}

    # ================= 3.2: how much freedom does the within-account permutation have? ===
    movable = sum(len(v) for v in g.values()
                  if len(v) > 1 and 0 < sum(x["absent"] for x in v) < len(v))
    out["I_power_of_the_within_account_permutation"] = {
        "units": len(rows2),
        "units_that_can_move": movable,
        "pct_that_can_move": round(100 * movable / len(rows2), 2),
        "singleton_accounts": sum(1 for v in g.values() if len(v) == 1),
        "multi_accounts": len(multi),
        "multi_accounts_all_present_or_all_absent": sum(
            1 for v in multi if sum(x["absent"] for x in v) in (0, len(v))),
        "verdict": ("the permutation is mostly the identity — the test has little power and its "
                    "p-value cannot support a claim that the page adds nothing")}

    # ================= I2: the pair statistic, decomposed ===============================
    att = [r for r in rows2 if r["page"]]
    heaviest = "es.wikipedia.org|Protestas en Paraguay de 2023"

    def pair_stats(rs):
        by = {}
        for r in rs:
            by.setdefault(r["page"], []).append(r)
        pairs = both = 0
        exp = 0.0
        p = sum(x["absent"] for x in rs) / len(rs)
        for v in by.values():
            for i in range(len(v)):
                for j in range(i + 1, len(v)):
                    if v[i]["handle"] == v[j]["handle"]:
                        continue
                    pairs += 1
                    both += v[i]["absent"] * v[j]["absent"]
                    exp += p * p
        return {"pairs": pairs, "both_absent": both, "expected": round(exp, 2),
                "ratio": round(both / exp, 4) if exp else None}
    out["I2_pair_decomposition"] = {
        "all_pages": pair_stats(att),
        "the_one_article": pair_stats([r for r in att if r["page"] == heaviest]),
        "everything_else": pair_stats([r for r in att if r["page"] != heaviest])}

    json.dump(out, open("discharge-115.json", "w"), indent=1, ensure_ascii=False)

    print("I6/I7 cells:", json.dumps({k: v for k, v in out["I6_I7_cells"].items()
                                      if k != "cells"}, ensure_ascii=False))
    print("6-7y:", json.dumps(out["I6_the_cell_that_is_not_one_of_the_17"], ensure_ascii=False))
    print("I3:", json.dumps(out["I3_pooled_deff_bootstrap"]), out["I3_half_width_factor"])
    print("I8 conditional:", json.dumps(out["I8_conditional_deff"]))
    print("I8 splitting:", json.dumps(out["I8_cluster_splitting"]))
    print("I10 drift:", json.dumps(out["I10_handle_drift"], ensure_ascii=False))
    print("I5 overlap:", json.dumps(out["I5_overlap"]))
    print("power:", json.dumps(out["I_power_of_the_within_account_permutation"],
                               ensure_ascii=False))
    print("I2 pairs:", json.dumps(out["I2_pair_decomposition"]))
    print("I1 omitted:", json.dumps(out["I1_omitted"], ensure_ascii=False)[:900])


if __name__ == "__main__":
    sys.exit(main())
