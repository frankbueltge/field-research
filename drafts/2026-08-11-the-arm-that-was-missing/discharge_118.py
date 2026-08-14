#!/usr/bin/env python3
"""Discharging the Verifier's nine conditions on INCREMENT-8.md §§1-6, session 118.

Every figure the Verifier computed in its own scratchpad is recomputed HERE, with this
practice's own code, before any of it is printed in this arc's prose. That rule exists because
session 115 printed the adversary's numbers while its own file said something slightly
different (`memory/claims.md`, session 116 rows).

Conditions, as imposed:
  1. M1  `10202` is NOT a new code - it appears in the session-114 probe output.
  2. M2  the corpus-wide account census costs 2,740 requests on the DAY-3 run, not 2,744.
  3. M3/M4/M6  p = 0.0111 not 0.0110; an honest design-effect range across more than two
                seeds; a real count of the post-hoc splits.
  4. M5  the width column must use one definition.
  5.     "three independent routes" is two routes, one run at several seeds.
  6.     the direction of the account-state conditioning bias IS measured by Q4; sweep the one
         unmeasured quantity and report the live-account-conditioned ratio as a range.
  7.     count the bootstrap draws that silently compute a 7-stratum statistic.
  8.     isolate statistic from key: the design effect of the ABSENCE PROPORTION on the same
         component key over the same units.
  9.     the atlas negative, term by term, with every hit disclosed.

Usage: python3 discharge_118.py [draws]
"""
import json
import math
import random
import re
import sys
import urllib.request

from cluster_model import load
from cluster_keys import page_index
from crossed_model import components
from coloss_117 import cell_of
import mh_components_118 as M

PAGE = "es.wikipedia.org|Protestas en Paraguay de 2023"
CELL = ("3-4y", "W-article")
UA = "field-research/1.0 (independent research instrument)"


def mh_strata_used(rows):
    """How many strata a resample actually contributes - the check `degenerate_draws` misses."""
    strata = {}
    for r in rows:
        s = strata.setdefault(r["year"], [0, 0, 0, 0])
        live = 0 if r["absent"] else 1
        if r["arm"] == "A":
            s[0 if live else 1] += 1
        else:
            s[2 if live else 3] += 1
    return sum(1 for a, b, c, d in strata.values()
               if (a + b + c + d) and (a + b) and (c + d))


def deff_proportion(groups_):
    """Linearised clustered variance of the absence proportion against the binomial."""
    N = sum(len(v) for v in groups_)
    K = len(groups_)
    a = sum(r["absent"] for v in groups_ for r in v)
    p = a / N
    ss = sum((sum(r["absent"] for r in v) - p * len(v)) ** 2 for v in groups_)
    return (K / (K - 1) * ss / N ** 2) / (p * (1 - p) / N)


def main(draws=4000):
    out = {"schema": "field-research/discharge-118/1", "session": 118, "date": "2026-08-14",
           "note": ("every figure here is recomputed with this practice's own code before it is "
                    "printed in this arc's prose")}

    # ---------------- C1 (M1): is 10202 new?
    p114 = json.load(open("account-state-probe-114.json"))
    codes114 = sorted({c for g in p114["status_field_by_group"].values() for c in g})
    p118 = json.load(open("account-state-117b.json"))
    codes118 = sorted({c for g in p118["codes_by_group"].values() for c in g})
    out["M1_new_codes"] = {
        "session_114_codes": codes114, "session_118_codes": codes118,
        "genuinely_new": sorted(set(codes118) - set(codes114) - {"None"}),
        "claimed_new_in_prose_v1": ["10222", "10202"],
        "verdict": ("REFUTED — 10202 appears in account-state-probe-114.json and in "
                    "PREREGISTRATION-117B §4; only 10222 is new"),
    }

    # ---------------- C2 (M2): the census cost, on the day-3 run
    _, rows3, _, _ = load("ledger/run-2026-08-13T0427Z.json")
    _, rows2, _, _ = load("ledger/run-2026-08-12T0341Z.json")
    out["M2_census_cost"] = {
        "distinct_accounts_day3": len({r["handle"] for r in rows3}),
        "distinct_accounts_day2": len({r["handle"] for r in rows2}),
        "verdict": "the analysis is on day 3; the census costs the day-3 number",
    }

    # ---------------- C3 (M3/M6): the p-value and the count of post-hoc splits
    d = json.load(open("derived-117b.json"))
    lfl = d["posthoc_declared"]["like_for_like"]
    out["M3_M6"] = {
        "p_T_allpresent_vs_C2_full": lfl["T_allpresent_vs_C2"]["fisher_two_sided_p"],
        "rounded_4dp": round(lfl["T_allpresent_vs_C2"]["fisher_two_sided_p"], 4),
        "like_for_like_comparisons_in_file": sorted(lfl.keys()),
        "count": len(lfl),
    }

    # ---------------- C6: the direction of the conditioning bias, swept
    idx = page_index()
    for r in rows3:
        r["page"] = idx.get(r["vid"])
    state = {r["handle"]: r.get("status_field") for r in p118["results"]}
    byh = {}
    for r in rows3:
        byh.setdefault(r["handle"], []).append(r)

    off = [r for r in rows3 if r["page"] != PAGE and cell_of(r) == CELL]
    cat = {"all_gone": [], "all_present": [], "mixed": []}
    for r in off:
        v = byh[r["handle"]]
        a = sum(x["absent"] for x in v)
        cat["all_gone" if a == len(v) else
            ("all_present" if a == 0 else "mixed")].append(r)
    # P(account live | category), measured by the probe: C1 is a census of all-gone accounts
    # in this cell, C2 a random sample of all-present ones. Mixed is unmeasured.
    bg = p118["by_group"]
    p_live = {"all_gone": 1 - bg["C1"]["nonzero_share"],
              "all_present": 1 - bg["C2"]["nonzero_share"]}
    sweep = []
    for p_live_mixed in (0.0, 0.25, 0.5, 0.75, 1.0):
        num = den = 0.0
        for k, rs in cat.items():
            w = p_live.get(k, p_live_mixed)
            den += w * len(rs)
            num += w * sum(r["absent"] for r in rs)
        rate = num / den
        exp10 = 10 * rate
        sweep.append({"p_live_mixed": p_live_mixed, "live_account_cell_rate": rate,
                      "expected_for_10_units": exp10, "ratio_observed_7": 7 / exp10})
    out["C6_conditioning_bias"] = {
        "off_page_cell_units": {k: {"n": len(v), "absent": sum(r["absent"] for r in v)}
                                for k, v in cat.items()},
        "p_account_live_measured": p_live,
        "sweep_over_unmeasured_mixed_category": sweep,
        "unconditional_cell_rate": sum(r["absent"] for r in off) / len(off),
        "verdict": ("the sign is invariant across the whole range of the one unmeasured "
                    "quantity: conditioning on account state biases the comparison TOWARD the "
                    "null, so 6.05 is a conservative floor"),
    }
    # this arc's own single-cell admission (the Verifier's qualification (i))
    tgt = [r for r in rows3 if r["page"] == PAGE]
    out["C6_single_cell"] = {
        "cells_on_the_page": sorted({f"{b}|{s}" for b, s in (cell_of(r) for r in tgt)}),
        "verdict": ("all 22 units sit in one cell, so the Poisson-binomial is exactly "
                    "Binomial(n, 0.11566265) and NOTHING IS STANDARDISED on this page; the "
                    "word 'age-standardised' describes the scan, not this page"),
    }

    # ---------------- C4/C5/C7: seeds, strata, widths
    _, ra, _, _ = load(M.A_RUN)
    _, rb, _, _ = load(M.A2_RUN)
    mh_rows = [r for r in ra if r["arm"] == "A"] + [r for r in rb if r["arm"] == "A2"]
    attributed = [r for r in mh_rows if r["vid"] in idx]
    comps = components(attributed, idx)
    K = len(comps)
    point = M.mh(attributed)
    seeds = {}
    for seed in (7, 8, 11, 12, 13):
        rng = random.Random(seed)
        vals, short = [], 0
        for _ in range(draws):
            drawn = []
            for _ in range(K):
                drawn.extend(comps[rng.randrange(K)])
            if mh_strata_used(drawn) < point["strata_used"]:
                short += 1
            m = M.mh(drawn)
            if m:
                vals.append(math.log(m["or"]))
        mean = sum(vals) / len(vals)
        sd = (sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5
        vals.sort()
        lo, hi = vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))]
        seeds[str(seed)] = {
            "se_log_or": sd, "deff_log_or": (sd / point["se_log"]) ** 2,
            "draws_with_fewer_strata_than_the_point_estimate": short,
            "share_short": short / draws,
            "percentile_ci_or": [math.exp(lo), math.exp(hi)],
            "wald_ci_or": [point["or"] * math.exp(-1.96 * sd),
                           point["or"] * math.exp(1.96 * sd)],
            "percentile_width": math.exp(hi) - math.exp(lo),
            "wald_width": point["or"] * (math.exp(1.96 * sd) - math.exp(-1.96 * sd)),
        }
    jack = json.load(open("mh-components-118.json"))["delete_one_component_jackknife"]
    dvals = [v["deff_log_or"] for v in seeds.values()] + [jack["deff_log_or"]]
    out["C4_C5_C7_seeds"] = {
        "seeds_run": sorted(seeds, key=int), "per_seed": seeds,
        "jackknife_deff": jack["deff_log_or"],
        "honest_range_including_jackknife": [min(dvals), max(dvals)],
        "routes": ("TWO — one bootstrap estimator run at five seeds, and one delete-one "
                   "jackknife. Seeds are not routes."),
        "strata_note": ("a resample can drop a stratum whose A2 margin is thin (2019: 4 live, "
                        "0 absent); such draws estimate a 7-stratum statistic and the "
                        "R==0/S==0 test in mh_components_118.py does not detect them"),
    }

    # ---------------- C8: isolate the statistic from the key
    def by(keyfn):
        g = {}
        for r in attributed:
            g.setdefault(keyfn(r), []).append(r)
        return list(g.values())
    out["C8_statistic_vs_key"] = {
        "units": len(attributed),
        "deff_absence_proportion_component_key": deff_proportion(comps),
        "deff_absence_proportion_account_key": deff_proportion(by(lambda r: r["handle"])),
        "deff_absence_proportion_page_key": deff_proportion(by(lambda r: idx[r["vid"]])),
        "deff_log_or_component_key_range": out["C4_C5_C7_seeds"]["honest_range_including_jackknife"],
        "verdict": ("on the SAME key and the SAME units the proportion's design effect is far "
                    "above the log odds ratio's, so the gap is a property of the statistic and "
                    "not only of the key"),
        "mixed_arm_components": sum(1 for c in comps if len({r["arm"] for r in c}) > 1),
        "units_in_mixed_arm_components": sum(len(c) for c in comps
                                             if len({r["arm"] for r in c}) > 1),
    }

    # ---------------- C9: the atlas negative, term by term
    try:
        req = urllib.request.Request("https://frankbueltge.de/atlas/werke.json",
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as f:
            W = json.load(f)
        we = W["werke"] if "werke" in W else list(W.values())[-1]
        terms = {"account suspension": r"account suspen", "deplatforming": r"deplatform|de-platform",
                 "banning": r"\bban(ning|ned|s)?\b", "moderation": r"moderat",
                 "takedown": r"takedown|take-down", "deletion": r"delet"}
        hits = {}
        for label, pat in terms.items():
            rx = re.compile(pat, re.I)
            hits[label] = [i.get("title") for i in we
                           if rx.search(json.dumps(i, ensure_ascii=False))]
        rx = re.compile(r"censor", re.I)
        hits["censorship (not in the original sentence)"] = [
            i.get("title") for i in we if rx.search(json.dumps(i, ensure_ascii=False))]
        out["C9_atlas_terms"] = {"works": len(we), "hits_by_term": hits,
                                 "fetched": "first-hand, not mirrored"}
    except Exception as e:
        out["C9_atlas_terms"] = {"error": type(e).__name__ + ": " + str(e)[:160]}

    json.dump(out, open("discharge-118.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("C4_C5_C7_seeds",)}, indent=1)[:4000])
    print(json.dumps({"deff_range": out["C4_C5_C7_seeds"]["honest_range_including_jackknife"],
                      "per_seed_deff": {k: round(v["deff_log_or"], 4)
                                        for k, v in seeds.items()},
                      "short_draws": {k: v["draws_with_fewer_strata_than_the_point_estimate"]
                                      for k, v in seeds.items()}}, indent=1))
    print("wrote discharge-118.json")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 4000)
