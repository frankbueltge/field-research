#!/usr/bin/env python3
"""The dated restatement — every interval this arc published, recomputed for clustered losses.

Session 115, 2026-08-13. **No new requests.** This reads run files already collected and
recomputes the uncertainty around numbers already published. Pre-registered in
`PREREGISTRATION-115.md` §2.

Why it exists. Session 114 established that losses in this corpus are not independent: they
clump by account. The closed-form clustered variance on the account key gives a design effect
of **1.4289** on the day-2 population (`cluster-keys-114.json`, C4 — no random seed; *not* the
1.458 that session first printed off a single bootstrap seed). Every Wilson interval this arc
has published treats one video as one independent observation, and is therefore too narrow by
about **sqrt(1.4289) = 1.1954** on its half-width.

What is corrected, and what is not:

  * The **point estimate never moves.** p = x/n is a consistent estimate of the population
    proportion whether or not the observations are clustered; clustering costs precision, not
    location. If any centre moves, the method is wrong and K4 fires.
  * The correction is `n_eff = n / DEFF`, a Wilson interval computed on the effective sample
    size. This is the standard first-order design-effect correction; it is an approximation
    and is labelled one.
  * **1.4289 is a lower bound.** The citing-page key gives 1.8854 on the same units. The
    restated bounds are computed at both, and the account-key column is the one this session
    stands behind, for the reason session 114's adversary gave: the page effect is carried by
    a single article.
  * **The pooled DEFF applied to a stratified cell is an assumption.** It is tested here: each
    cell gets its own account-key DEFF wherever it has enough clusters to carry one.

Usage:
    python3 restatement_115.py                # day-2 population + the session-109 census
"""
import json
import math
import sys

import cluster_model as cm
import power_audit as pa

DEFF_ACCOUNT = 1.428865343926577      # cluster-keys-114.json, C4, closed form, no seed
DEFF_PAGE = 1.885389216967676         # cluster-keys-114.json, C5, the fragile upper reading
DAY2 = "ledger/run-2026-08-12T0341Z.json"

MIN_CLUSTERS_FOR_OWN_DEFF = 30        # below this a cell's own DEFF is noise; stated, not hidden


def wilson_eff(k, n, deff):
    """Wilson on the effective sample size. Point estimate is returned unchanged."""
    n_eff = n / deff
    k_eff = k * n_eff / n
    lo, hi = pa.wilson(k_eff, n_eff)
    return {"n": n, "n_eff": round(n_eff, 2), "p": k / n if n else None,
            "lo": lo, "hi": hi, "half_width": (hi - lo) / 2 if lo is not None else None}


def deff_of(rows, keyfn):
    """The linearised clustered variance of the absence rate against the binomial.

    Same estimator as cluster_keys.deff_analytic, restated here so this file stands alone and
    can be checked without reading the other. Returns None when the cell cannot carry it.
    """
    g = {}
    for r in rows:
        g.setdefault(keyfn(r), []).append(r)
    N = sum(len(v) for v in g.values())
    K = len(g)
    if N == 0 or K < 2:
        return None
    a = sum(r["absent"] for r in rows)
    p = a / N
    if p in (0.0, 1.0):
        return {"n": N, "clusters": K, "rate": p, "deff": None,
                "note": "degenerate cell — every unit on one side; no variance ratio exists"}
    ss = sum((sum(r["absent"] for r in v) - p * len(v)) ** 2 for v in g.values())
    v_cluster = K / (K - 1) * ss / N ** 2
    v_binom = p * (1 - p) / N
    return {"n": N, "clusters": K, "rate": p, "deff": v_cluster / v_binom,
            "se_cluster": v_cluster ** 0.5, "se_binomial": v_binom ** 0.5}


def restate(label, k, n, published, deff=DEFF_ACCOUNT, rows=None, scale=100.0,
            published_point=None):
    """One published interval, its recomputation, and the subtraction between them.

    `published` is the interval as it stands in the published text, in the units it was
    published in (percent by default). Nothing here reads the published number to compute the
    new one — the subtraction is the check, so the two must be independent.
    """
    naive_lo, naive_hi = pa.wilson(k, n)
    new = wilson_eff(k, n, deff)
    out = {
        "label": label, "k": k, "n": n,
        "point_estimate": round(scale * k / n, 4),
        "published_ci": published,
        "reproduced_naive_ci": [round(scale * naive_lo, 4), round(scale * naive_hi, 4)],
        "restated_ci": [round(scale * new["lo"], 4), round(scale * new["hi"], 4)],
        "n_eff": new["n_eff"],
        "published_width": round(published[1] - published[0], 4),
        "naive_width": round(scale * (naive_hi - naive_lo), 4),
        "restated_width": round(scale * (new["hi"] - new["lo"]), 4),
    }
    out["widening_pp"] = round(out["restated_width"] - out["published_width"], 4)
    out["widening_ratio"] = round(out["restated_width"] / out["published_width"], 4) \
        if out["published_width"] else None
    # The subtract-first check, pre-registered as binding.
    out["reproduces_published"] = (
        abs(out["reproduced_naive_ci"][0] - published[0]) <= 0.02
        and abs(out["reproduced_naive_ci"][1] - published[1]) <= 0.02)
    # NOT by construction: the published point estimate is carried in the call and compared.
    # Asserting "no centre moved" without checking it against the published text would be the
    # kind of self-certification this practice exists to refuse.
    if published_point is None:
        out["published_point"] = None
        out["centre_moved"] = None
        out["centre_check"] = "NOT CHECKED — no published point estimate was supplied"
    else:
        out["published_point"] = published_point
        moved = abs(out["point_estimate"] - published_point) > 0.011
        out["centre_moved"] = moved
        out["centre_check"] = ("MOVED — K4 fires" if moved else
                               f"unchanged ({published_point} recomputed as "
                               f"{out['point_estimate']})")
    out["wider"] = out["restated_width"] > out["published_width"]
    if rows is not None:
        own = deff_of(rows, lambda r: r["handle"])
        if own and own.get("deff") and own["clusters"] >= MIN_CLUSTERS_FOR_OWN_DEFF:
            own_new = wilson_eff(k, n, own["deff"])
            out["cell_own_deff"] = round(own["deff"], 4)
            out["cell_clusters"] = own["clusters"]
            out["restated_ci_own_deff"] = [round(scale * own_new["lo"], 4),
                                           round(scale * own_new["hi"], 4)]
        elif own:
            out["cell_own_deff"] = None
            out["cell_clusters"] = own["clusters"]
            out["cell_own_deff_note"] = (
                f"fewer than {MIN_CLUSTERS_FOR_OWN_DEFF} clusters — not computed")
    return out


def cells(rows, keyfn):
    out = {}
    for r in rows:
        out.setdefault(keyfn(r), []).append(r)
    return out


def main():
    d2, rows2, excl2, key2 = cm.load(DAY2)
    result = {
        "generated_utc": None,
        "session": 115,
        "what_this_is": (
            "A dated restatement, not an edit. Every interval below stands as published; the "
            "restated column is the same estimate with the clustering of losses priced in. No "
            "point estimate moves."),
        "design_effects": {
            "account_key": DEFF_ACCOUNT,
            "page_key": DEFF_PAGE,
            "source": "cluster-keys-114.json (session 114), closed-form clustered variance, no seed",
            "which_one_governs": (
                "the account key. The page key is larger and is carried by a single article "
                "(es.wikipedia.org|Protestas en Paraguay de 2023, 23 units, 17 absent, 20 "
                "distinct handles); removing that one article collapses the page key to 1.3949 "
                "while the account key barely moves. Every restated bound below is therefore a "
                "LOWER bound on the correction, not the correction."),
            "sqrt_account": round(math.sqrt(DEFF_ACCOUNT), 4),
            "sqrt_page": round(math.sqrt(DEFF_PAGE), 4),
        },
        "population_day2": {"analysable": len(rows2), "excluded": excl2},
        "restated": [],
        "page_key_variants": [],
        "per_cell_deff": {},
    }

    # ---- INCREMENT-3 §1: the pooled day-2 rate -------------------------------------------
    n = len(rows2)
    ret = sum(1 for r in rows2 if not r["absent"])
    result["restated"].append(restate(
        "INCREMENT-3 §1 — pooled public retrievability, day-2 window run",
        ret, n, [86.81, 88.94], rows=rows2, published_point=87.92))

    # ---- INCREMENT-3 §1a: the six published age bands ------------------------------------
    published_bands = {
        "0-1y": [92.87, 96.71], "1-2y": [90.30, 94.05], "2-3y": [85.11, 89.71],
        "3-4y": [80.99, 86.53], "4-5y": [80.09, 86.82], "5y+": [78.05, 85.71],
    }
    published_band_points = {"0-1y": 95.14, "1-2y": 92.39, "2-3y": 87.59,
                             "3-4y": 83.95, "4-5y": 83.73, "5y+": 82.20}
    band_cells = cells(rows2, lambda r: r["band"])
    for band, pub in published_bands.items():
        rs = band_cells[band]
        k = sum(1 for r in rs if not r["absent"])
        result["restated"].append(restate(
            f"INCREMENT-3 §1a — age band {band}, publicly retrievable", k, len(rs), pub,
            rows=rs, published_point=published_band_points[band]))

    # ---- INCREMENT-3 §1b: the three source strata ----------------------------------------
    published_strata = {
        "W-article": [87.95, 90.45], "W-other-ns": [82.36, 87.46], "F-forum": [81.97, 88.48],
    }
    published_stratum_points = {"W-article": 89.26, "W-other-ns": 85.09, "F-forum": 85.52}
    stratum_cells = cells(rows2, lambda r: r["stratum"])
    for st, pub in published_strata.items():
        rs = stratum_cells[st]
        k = sum(1 for r in rs if not r["absent"])
        result["restated"].append(restate(
            f"INCREMENT-3 §1b — stratum {st}, publicly retrievable", k, len(rs), pub,
            rows=rs, published_point=published_stratum_points[st]))

    # ---- INCREMENT-3 §2a: the ceiling, four partitions, worst eligible cell --------------
    # These are ABSENCE rates, not retrievability. Published in ceiling-recompute.json.
    ceiling = json.load(open("ceiling-recompute.json"))
    pub_ceiling = {
        "the six published bands": ("5y+", [14.29, 21.95], 17.80),
        "calendar year of creation": ("2019", [12.07, 39.02], 22.86),
        "integer age-year": ("6-7y", [11.56, 25.85], 17.59),
        "half-year": ("5.5y", [11.79, 26.31], 17.92),
    }
    keyfns = {
        "the six published bands": lambda r: r["band"],
        "calendar year of creation": lambda r: str(r["year"]),
        "integer age-year": lambda r: f"{int(r['age_y'])}-{int(r['age_y'])+1}y",
        "half-year": lambda r: f"{math.floor(r['age_y'] * 2) / 2}y",
    }
    for part, (cellname, pub, pub_pt) in pub_ceiling.items():
        cs = cells(rows2, keyfns[part])
        rs = cs.get(cellname)
        if rs is None:
            result["restated"].append({"label": f"INCREMENT-3 §2a — {part} / {cellname}",
                                       "error": "cell key not reproduced from the run file",
                                       "keys_seen": sorted(cs)[:20]})
            continue
        k = sum(r["absent"] for r in rs)
        result["restated"].append(restate(
            f"INCREMENT-3 §2a — ceiling, {part}, worst eligible cell {cellname} (ABSENCE)",
            k, len(rs), pub, rows=rs, published_point=pub_pt))

    # ---- INCREMENT-4 §3: the absence rate the correction was found on --------------------
    # Already restated in INCREMENT-4 itself; carried here so the register is complete.
    att = [r for r in rows2 if r["handle"]]
    k = sum(r["absent"] for r in att)
    result["restated"].append(restate(
        "INCREMENT-4 §3 — absence rate, attributed units (already restated at session 114)",
        k, len(att), [11.06, 13.19], rows=att, published_point=12.08))

    # ---- the page-key variant of every one of the above ----------------------------------
    for row in list(result["restated"]):
        if "error" in row:
            continue
        pg = wilson_eff(row["k"], row["n"], DEFF_PAGE)
        result["page_key_variants"].append({
            "label": row["label"],
            "restated_ci_account_key": row["restated_ci"],
            "restated_ci_page_key": [round(100 * pg["lo"], 4), round(100 * pg["hi"], 4)],
            "extra_widening_pp": round(100 * (pg["hi"] - pg["lo"]) - row["restated_width"], 4),
        })

    # ---- P7: is the pooled DEFF a fair proxy per cell? -----------------------------------
    for name, keyfn in [("age band", lambda r: r["band"]),
                        ("stratum", lambda r: r["stratum"]),
                        ("calendar year", lambda r: str(r["year"]))]:
        tab = {}
        for cname, rs in sorted(cells(rows2, keyfn).items()):
            own = deff_of(rs, lambda r: r["handle"])
            if own is None:
                continue
            tab[cname] = {"n": own["n"], "clusters": own["clusters"],
                          "absence_rate": round(own["rate"], 6),
                          "deff": round(own["deff"], 4) if own.get("deff") else None,
                          "eligible": own["clusters"] >= MIN_CLUSTERS_FOR_OWN_DEFF}
        result["per_cell_deff"][name] = tab

    elig = [v["deff"] for t in result["per_cell_deff"].values() for v in t.values()
            if v["eligible"] and v["deff"]]
    result["per_cell_deff_summary"] = {
        "eligible_cells": len(elig),
        "below_pooled": sum(1 for x in elig if x < DEFF_ACCOUNT),
        "above_pooled": sum(1 for x in elig if x >= DEFF_ACCOUNT),
        "min": round(min(elig), 4) if elig else None,
        "max": round(max(elig), 4) if elig else None,
        "median": round(sorted(elig)[len(elig) // 2], 4) if elig else None,
        "pooled": round(DEFF_ACCOUNT, 4),
        "note": ("P7 asked whether the per-cell design effects straddle the pooled value. A "
                 "cell's own DEFF is noisier than the pooled one and cells overlap across the "
                 "three partitions; this is a proxy check, not an independent test."),
    }

    # ---- the subtract-first check, pre-registered as binding -----------------------------
    checks = [r for r in result["restated"] if "error" not in r]
    result["subtract_first_check"] = {
        "n_intervals": len(checks),
        "reproduce_published_within_0.02pp": sum(1 for r in checks if r["reproduces_published"]),
        "fail_to_reproduce": [r["label"] for r in checks if not r["reproduces_published"]],
        "all_wider": all(r["wider"] for r in checks),
        "not_wider": [r["label"] for r in checks if not r["wider"]],
        "centres_checked": sum(1 for r in checks if r["centre_moved"] is not None),
        "centres_moved": [r["label"] for r in checks if r["centre_moved"]],
        "min_widening_ratio": round(min(r["widening_ratio"] for r in checks), 4),
        "max_widening_ratio": round(max(r["widening_ratio"] for r in checks), 4),
        "K4": None,
    }
    result["subtract_first_check"]["K4"] = (
        "DOES NOT FIRE — every centre checked against its published value and unchanged, "
        "every bound wider"
        if (result["subtract_first_check"]["all_wider"]
            and not result["subtract_first_check"]["centres_moved"]
            and result["subtract_first_check"]["centres_checked"] == len(checks)) else
        "FIRES — a centre moved, a centre went unchecked, or a bound did not widen; "
        "the restatement is withdrawn")

    json.dump(result, open("restatement-115.json", "w"), indent=1, ensure_ascii=False)

    print(f"day-2 analysable {len(rows2)}  excluded {excl2}")
    print(f"DEFF account {DEFF_ACCOUNT:.4f} (sqrt {math.sqrt(DEFF_ACCOUNT):.4f})  "
          f"page {DEFF_PAGE:.4f} (sqrt {math.sqrt(DEFF_PAGE):.4f})")
    print()
    for r in result["restated"]:
        if "error" in r:
            print(f"  !! {r['label']}: {r['error']} :: {r.get('keys_seen')}")
            continue
        flag = "" if r["reproduces_published"] else "   << DOES NOT REPRODUCE PUBLISHED"
        print(f"  {r['label']}")
        print(f"    p={r['point_estimate']:.4f}  n={r['n']}  n_eff={r['n_eff']}  "
              f"published [{r['published_ci'][0]}, {r['published_ci'][1]}] w={r['published_width']} "
              f"-> restated [{r['restated_ci'][0]}, {r['restated_ci'][1]}] "
              f"w={r['restated_width']} (x{r['widening_ratio']}){flag}")
        if r.get("cell_own_deff"):
            print(f"    cell's own DEFF {r['cell_own_deff']} on {r['cell_clusters']} accounts "
                  f"-> [{r['restated_ci_own_deff'][0]}, {r['restated_ci_own_deff'][1]}]")
    print()
    print("subtract-first:", json.dumps(result["subtract_first_check"], ensure_ascii=False))
    print("per-cell DEFF:", json.dumps(result["per_cell_deff_summary"], ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
