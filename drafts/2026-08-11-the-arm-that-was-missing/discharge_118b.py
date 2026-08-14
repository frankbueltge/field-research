#!/usr/bin/env python3
"""Discharging the Interlocutor's twelve conditions on INCREMENT-8.md §§1-6, session 118.

The adversary found something a Verifier's nine conditions and this practice's own gauntlet
walked past: THE PRIMARY STATISTIC'S BINARY IS NOT THE THING THE PROSE SAYS IT IS. Three C1
accounts answer `10222` while returning the full user object and a uniqueId matching the
requested handle, so by this arc's own session-114 definition the account object IS served -
and they are counted as not served.

Everything the adversary computed is recomputed here with this practice's own code before any
of it is printed in this arc's prose.

Usage: python3 discharge_118b.py [outer] [inner]
"""
import json
import math
import random
import sys

from cluster_model import load
from cluster_keys import page_index
from crossed_model import components
from coloss_117 import cell_of, tails
from probe_117b import fisher_two_sided, PAGE, CELL
import mh_components_118 as M

probe = json.load(open("account-state-117b.json"))


def served_object(r):
    """The session-114 operational definition, applied to the stored markers."""
    return bool(r["markers"].get("userInfo")) and bool(r.get("unique_id_returned"))


def tab(pred):
    out = {}
    for r in probe["results"]:
        g = out.setdefault(r["group"], {"n": 0, "not_served": 0})
        g["n"] += 1
        g["not_served"] += 0 if pred(r) else 1
    for g in out.values():
        g["share_not_served"] = g["not_served"] / g["n"]
    return out


def fisher(t, a, b):
    x, y = t[a]["not_served"], t[a]["n"] - t[a]["not_served"]
    u, v = t[b]["not_served"], t[b]["n"] - t[b]["not_served"]
    return {"table": [[x, y], [u, v]], "p": fisher_two_sided(x, y, u, v)}


def newcombe(x1, n1, x2, n2):
    """Newcombe method 10 interval for a difference of proportions (Wilson-based)."""
    def wilson(x, n, z=1.959963985):
        p = x / n
        d = 1 + z * z / n
        c = p + z * z / (2 * n)
        h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
        return ((c - h) / d, (c + h) / d)
    l1, u1 = wilson(x1, n1)
    l2, u2 = wilson(x2, n2)
    p1, p2 = x1 / n1, x2 / n2
    return [p1 - p2 - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2),
            p1 - p2 + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)]


def deff_prop_boot(comps, draws, seed):
    rng = random.Random(seed)
    K = len(comps)
    agg = [(len(c), sum(r["absent"] for r in c)) for c in comps]
    N0 = sum(n for n, _ in agg)
    A0 = sum(a for _, a in agg)
    p0 = A0 / N0
    vals = []
    for _ in range(draws):
        n = a = 0
        for _ in range(K):
            dn, da = agg[rng.randrange(K)]
            n += dn
            a += da
        vals.append(a / n)
    m = sum(vals) / len(vals)
    sd = (sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5
    return sd ** 2 / (p0 * (1 - p0) / N0)


def deff_prop_jack(comps):
    agg = [(len(c), sum(r["absent"] for r in c)) for c in comps]
    N0 = sum(n for n, _ in agg)
    A0 = sum(a for _, a in agg)
    p0 = A0 / N0
    K = len(agg)
    vals = [(A0 - a) / (N0 - n) for n, a in agg]
    m = sum(vals) / K
    se = math.sqrt((K - 1) / K * sum((v - m) ** 2 for v in vals))
    return se ** 2 / (p0 * (1 - p0) / N0)


def deff_logor_boot(comps, point_se, draws, seed):
    rng = random.Random(seed)
    K = len(comps)
    vals = []
    for _ in range(draws):
        drawn = []
        for _ in range(K):
            drawn.extend(comps[rng.randrange(K)])
        m = M.mh(drawn)
        if m:
            vals.append(math.log(m["or"]))
    mu = sum(vals) / len(vals)
    sd = (sum((v - mu) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5
    return (sd / point_se) ** 2


def main(outer=30, inner=300):
    out = {"schema": "field-research/discharge-118b/1", "session": 118, "date": "2026-08-14",
           "note": "the Interlocutor's twelve conditions, recomputed with this practice's code"}

    # ---- I1: the misclassification, and every statistic it touches
    pre = tab(lambda r: r.get("status_field") == 0)          # the pre-registered binary
    obj = tab(served_object)                                  # the object-based definition
    codes = {}
    for r in probe["results"]:
        codes.setdefault(str(r.get("status_field")), {"n": 0, "user_object": 0, "id_match": 0})
        c = codes[str(r.get("status_field"))]
        c["n"] += 1
        c["user_object"] += 1 if r["markers"].get("userInfo") else 0
        c["id_match"] += 1 if (r.get("unique_id_returned") or "").lower() == r["handle"].lower() else 0
    out["I1_classification"] = {
        "by_code": codes,
        "preregistered_zero_vs_nonzero": pre,
        "object_based_user_object_and_matching_id": obj,
        "reclassified_accounts": [r["handle"] for r in probe["results"]
                                  if r.get("status_field") not in (0, None) and served_object(r)],
        "preregistered": {"Q4_C1_vs_C2": fisher(pre, "C1", "C2"),
                          "Q3_T_vs_C1": fisher(pre, "T", "C1")},
        "object_based": {"Q4_C1_vs_C2": fisher(obj, "C1", "C2"),
                         "Q3_T_vs_C1": fisher(obj, "T", "C1")},
        "verdict": ("the pre-registration fixed zero-against-non-zero and that statistic stands "
                    "as pre-registered; the PROSE claim that non-zero means 'the account object "
                    "is not served' is refuted for code 10222, where the object is served"),
    }

    # ---- I6: what the T-against-C1 comparison actually licenses
    out["I6_power"] = {
        "newcombe_T_minus_C1_preregistered": newcombe(pre["T"]["not_served"], pre["T"]["n"],
                                                      pre["C1"]["not_served"], pre["C1"]["n"]),
        "newcombe_T_minus_C1_object_based": newcombe(obj["T"]["not_served"], obj["T"]["n"],
                                                     obj["C1"]["not_served"], obj["C1"]["n"]),
    }
    rng = random.Random(118001)
    pc = {}
    base = pre["C1"]["not_served"] / pre["C1"]["n"]
    for delta in (0.10, 0.20, 0.30, 0.40):
        hit = 0
        for _ in range(8000):
            a = sum(1 for _ in range(20) if rng.random() < min(1.0, base + delta))
            c = sum(1 for _ in range(41) if rng.random() < base)
            if fisher_two_sided(a, 20 - a, c, 41 - c) < 0.05:
                hit += 1
        pc[f"{delta:.2f}"] = hit / 8000
    out["I6_power"]["simulated_power_vs_C1_base"] = pc
    out["I6_power"]["C1_base_used"] = base

    # ---- I15/A15: are Q1 and Q2 the same event?
    same = all((k < 10) == ((k / 20) < base) for k in range(21))
    out["I15_Q1_equals_Q2"] = {
        "checked_k": list(range(21)), "identical_for_every_k": same,
        "verdict": ("Q1 and Q2 score identically for every possible T count given the observed "
                    "C1; the pre-registration contained ONE substantive bet, scored twice"),
    }

    # ---- I5: what the section-2 tail actually adds
    _, rows3, _, _ = load("ledger/run-2026-08-13T0427Z.json")
    idx = page_index()
    for r in rows3:
        r["page"] = idx.get(r["vid"])
    state = {r["handle"]: r for r in probe["results"]}
    tgt = [r for r in rows3 if r["page"] == PAGE]
    live = [r for r in tgt if state[r["handle"]].get("status_field") == 0]
    dead = [r for r in tgt if state[r["handle"]].get("status_field") != 0]
    off = [r for r in rows3 if r["page"] != PAGE and cell_of(r) == CELL]
    rate = sum(r["absent"] for r in off) / len(off)
    a_live = sum(r["absent"] for r in live)
    a_dead = sum(r["absent"] for r in dead)
    up_live, _ = tails([rate] * len(live), a_live)
    up_dead, _ = tails([rate] * len(dead), a_dead)
    # hypergeometric: given 16 of 22 absent, how surprising is 7 of the 10 live ones?
    from math import comb
    n_all, a_all, n_live = len(tgt), sum(r["absent"] for r in tgt), len(live)
    hyp = sum(comb(n_live, x) * comb(n_all - n_live, a_all - x) / comb(n_all, a_all)
              for x in range(a_live, min(n_live, a_all) + 1))
    out["I5_what_the_tail_adds"] = {
        "live": {"n": len(live), "absent": a_live, "expected": rate * len(live),
                 "upper_tail": up_live},
        "dead": {"n": len(dead), "absent": a_dead, "expected": rate * len(dead),
                 "upper_tail": up_dead},
        "conditional_on_the_page_total": {
            "expected_live_absent_given_16_of_22": a_all * n_live / n_all,
            "P_at_least_observed": hyp},
        "fisher_on_the_page_2x2": fisher_two_sided(a_live, len(live) - a_live,
                                                   a_dead, len(dead) - a_dead),
        "verdict": ("account state and unit absence are orthogonal ON THIS PAGE; the subset tail "
                    "carries no evidence beyond the page tail published at session 117, and the "
                    "dead-account side is the more extreme of the two"),
    }

    # ---- I3/I4: the sweep, with the sampling error and the measured mixed weight
    byh = {}
    for r in rows3:
        byh.setdefault(r["handle"], []).append(r)
    cat = {"all_gone": [], "all_present": [], "mixed": []}
    for r in off:
        v = byh[r["handle"]]
        a = sum(x["absent"] for x in v)
        cat["all_gone" if a == len(v) else ("all_present" if a == 0 else "mixed")].append(r)

    def sweep(p_gone, p_present, p_mixed):
        num = den = 0.0
        for k, rs in cat.items():
            w = {"all_gone": p_gone, "all_present": p_present}.get(k, p_mixed)
            den += w * len(rs)
            num += w * sum(r["absent"] for r in rs)
        return num / den

    def cp(x, n, lo=True):
        """Clopper-Pearson bound by bisection on the exact binomial tail.

        The two tails move in OPPOSITE directions in p, and the first version of this function
        bisected both as if they were increasing, so every upper bound it returned was 0.0 and
        three sweep cells came back as nonsense (rate 1.0, ratio 0.70). Found by reading the
        printed cells back against what the quantity has to be. Fixed here.
        """
        if lo:                     # P(X >= x) is INCREASING in p
            f = lambda p: sum(comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(x, n + 1)) - 0.025
            a, b = 1e-12, 1 - 1e-12
            for _ in range(200):
                m = (a + b) / 2
                if f(m) < 0:
                    a = m
                else:
                    b = m
        else:                      # P(X <= x) is DECREASING in p
            f = lambda p: sum(comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(0, x + 1)) - 0.025
            a, b = 1e-12, 1 - 1e-12
            for _ in range(200):
                m = (a + b) / 2
                if f(m) > 0:
                    a = m
                else:
                    b = m
        return (a + b) / 2

    variants = {}
    for lab, t in (("preregistered", pre), ("object_based", obj)):
        pg = 1 - t["C1"]["share_not_served"]
        pp = 1 - t["C2"]["share_not_served"]
        pp_lo = cp(t["C2"]["n"] - t["C2"]["not_served"], t["C2"]["n"], lo=True)
        pp_hi = cp(t["C2"]["n"] - t["C2"]["not_served"], t["C2"]["n"], lo=False)
        rows = {}
        for mlab, pm in (("mixed=0", 0.0), ("mixed=1", 1.0),
                         ("mixed=11/12 measured at session 114", 11 / 12)):
            for plab, ppv in (("C2 point", pp), ("C2 exact lower", pp_lo),
                              ("C2 exact upper", pp_hi)):
                rr = sweep(pg, ppv, pm)
                rows[f"{mlab} | {plab}"] = {"rate": rr, "expected_10": 10 * rr,
                                            "ratio_at_7": 7 / (10 * rr)}
        ratios = [v["ratio_at_7"] for v in rows.values()]
        variants[lab] = {"p_live_all_gone": pg, "p_live_all_present": pp,
                         "p_live_all_present_exact_95": [pp_lo, pp_hi],
                         "cells": rows, "ratio_range": [min(ratios), max(ratios)]}
    # the sign-flip threshold on P(live | all-gone)
    lo_, hi_ = 0.0, 1.0
    for _ in range(200):
        mid = (lo_ + hi_) / 2
        if sweep(mid, 1 - obj["C2"]["share_not_served"], 1.0) < rate:
            lo_ = mid
        else:
            hi_ = mid
    out["I3_I4_sweep"] = {"unconditional_cell_rate": rate, "variants": variants,
                          "sign_flip_threshold_on_P_live_all_gone": (lo_ + hi_) / 2,
                          "mixed_measured_session_114": {"handles": 12, "state_zero": 11,
                                                         "source": "account-state-probe-114.json"}}

    # ---- I2: does section 3 falsify section 2's weighting?
    T = probe["population"]["T"]
    tgone = [h for h in T if all(x["absent"] for x in byh[h])]
    tpres = [h for h in T if not any(x["absent"] for x in byh[h])]
    out["I2_exchangeability"] = {
        "on_page_all_present_live": sum(1 for h in tpres if state[h].get("status_field") == 0),
        "on_page_all_present_n": len(tpres),
        "off_page_all_present_live_share": 1 - pre["C2"]["share_not_served"],
        "on_page_all_gone_live": sum(1 for h in tgone if state[h].get("status_field") == 0),
        "on_page_all_gone_n": len(tgone),
        "off_page_all_gone_live_share": 1 - pre["C1"]["share_not_served"],
        "verdict": ("the sweep weights 349 of 415 units by a rate this document's own section 3 "
                    "rejects for the target page at p = 0.0111; the floor survives only through "
                    "the sign-flip threshold above"),
    }

    # ---- I10/I11/I12: matched estimators, the key x statistic table, and an interval on both
    _, ra, _, _ = load(M.A_RUN)
    _, rb, _, _ = load(M.A2_RUN)
    mh_rows = [r for r in ra if r["arm"] == "A"] + [r for r in rb if r["arm"] == "A2"]
    att = [r for r in mh_rows if r["vid"] in idx]
    comps = components(att, idx)
    point = M.mh(att)

    def group_by(keyfn):
        g = {}
        for r in att:
            g.setdefault(keyfn(r), []).append(r)
        return list(g.values())
    keys = {"account": group_by(lambda r: r["handle"]),
            "page": group_by(lambda r: idx[r["vid"]]),
            "component": comps}
    table = {}
    for kname, groups_ in keys.items():
        table[kname] = {
            "clusters": len(groups_),
            "deff_log_or_boot": [deff_logor_boot(groups_, point["se_log"], 1500, s)
                                 for s in (7, 8, 11)],
            "deff_proportion_boot": [deff_prop_boot(groups_, 1500, s) for s in (7, 8, 11)],
            "deff_proportion_jack": deff_prop_jack(groups_),
        }
    out["I10_key_by_statistic"] = {
        "units": len(att), "table": table,
        "verdict": ("the gap between the two statistics is small on the account key and large on "
                    "the component key: it is an interaction of statistic WITH key, not a "
                    "property of the statistic alone"),
    }

    # ---- I11: an interval on the gap, paired outer/inner bootstrap
    rngo = random.Random(118002)
    K = len(comps)
    gaps, ratios, dl, dp = [], [], [], []
    for _ in range(outer):
        rs = [comps[rngo.randrange(K)] for _ in range(K)]
        flat = [r for c in rs for r in c]
        m = M.mh(flat)
        if not m:
            continue
        a = deff_logor_boot(rs, m["se_log"], inner, rngo.randrange(10 ** 6))
        b = deff_prop_boot(rs, inner, rngo.randrange(10 ** 6))
        dl.append(a)
        dp.append(b)
        gaps.append(b - a)
        ratios.append(b / a)

    def pct(v, q):
        v = sorted(v)
        return v[max(0, min(len(v) - 1, int(q * len(v))))]
    out["I11_uncertainty"] = {
        "outer": outer, "inner": inner, "usable": len(gaps),
        "deff_log_or": {"median": pct(dl, .5), "p05": pct(dl, .05), "p95": pct(dl, .95)},
        "deff_proportion": {"median": pct(dp, .5), "p05": pct(dp, .05), "p95": pct(dp, .95)},
        "gap": {"median": pct(gaps, .5), "p05": pct(gaps, .05), "p95": pct(gaps, .95),
                "positive_in": sum(1 for g in gaps if g > 0), "of": len(gaps)},
        "ratio": {"median": pct(ratios, .5), "p05": pct(ratios, .05), "p95": pct(ratios, .95)},
    }

    # ---- I12: which component is the most influential
    worst = None
    for j, c in enumerate(comps):
        flat = [r for i, cc in enumerate(comps) if i != j for r in cc]
        m = M.mh(flat)
        if not m:
            continue
        d = abs(m["or"] - point["or"])
        if worst is None or d > worst[0]:
            worst = (d, j, m["or"])
    j = worst[1]
    pages_in = sorted({idx[r["vid"]] for r in comps[j]})
    out["I12_most_influential_component"] = {
        "delta_or": worst[0], "n_units": len(comps[j]),
        "pages": pages_in[:5], "n_pages": len(pages_in),
        "accounts": len({r["handle"] for r in comps[j]}),
    }

    json.dump(out, open("discharge-118b.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items()
                      if k in ("I1_classification", "I15_Q1_equals_Q2", "I5_what_the_tail_adds",
                               "I12_most_influential_component")}, indent=1)[:3500])
    print(json.dumps({"sweep_ranges": {k: v["ratio_range"] for k, v in variants.items()},
                      "flip": out["I3_I4_sweep"]["sign_flip_threshold_on_P_live_all_gone"],
                      "power": pc, "newcombe": out["I6_power"],
                      "keytable": {k: {"logor": [round(x, 4) for x in v["deff_log_or_boot"]],
                                       "prop": [round(x, 4) for x in v["deff_proportion_boot"]],
                                       "prop_jack": round(v["deff_proportion_jack"], 4)}
                                   for k, v in table.items()},
                      "uncertainty": out["I11_uncertainty"]}, indent=1))
    print("wrote discharge-118b.json")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 30,
         int(sys.argv[2]) if len(sys.argv) > 2 else 300)
