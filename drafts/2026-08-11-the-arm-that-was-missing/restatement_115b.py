#!/usr/bin/env python3
"""The dated restatement, part two — the survival audit and the session-109 census.

Session 115, 2026-08-13. **No new requests.** Companion to `restatement_115.py`, which covers
the day-2 window run. This file covers the two populations that file does not touch:

  * `POWER-AUDIT.md` §2 — the cross-sectional survival table and the **Weibull shape CI**, both
    computed on `ledger/run-2026-08-11T1124Z.json` (session 110, 2,904 observations).
  * `RESULT.md` / `DERIVED.md` — the by-creation-year table of the **session-109 census**
    (`census-results.json`, 2,201 requests, 2,173 usable).

Two different corrections, and the difference matters:

  * A Wilson interval takes the design-effect correction directly: `n_eff = n / DEFF`.
  * A **profile-likelihood** interval does not. The shape CI on `k` comes from the set
    `{k : 2(LLmax - LL(k)) <= 3.841}`. Under clustering the likelihood is a *pseudo*-likelihood
    and the deviance is inflated by roughly the design effect, so the first-order Rao–Scott
    correction compares the deviance against `3.841 * DEFF` instead. That is a **weaker and
    cruder operation** than the Wilson correction and is labelled as one wherever it appears.
    It assumes a single design effect governs the whole fit, which the per-cell table in
    `restatement-115.json` shows is not exactly true.

`DEFF = 1.4289` throughout — the account key, closed form, no seed (`cluster-keys-114.json` C4),
and a **lower** bound on the correction for the reason stated in the companion file.
"""
import json
import math
import time

import power_audit as pa

DEFF = 1.428865343926577
CHI2_1_95 = 3.841458821
CENSUS = "census-results.json"
YEAR_S = pa.YEAR_S


def wilson_eff(k, n, deff):
    n_eff = n / deff
    lo, hi = pa.wilson(k * n_eff / n, n_eff)
    return lo, hi, n_eff


def line(label, k, n, published, scale=1.0, digits=4):
    lo0, hi0 = pa.wilson(k, n)
    lo1, hi1, n_eff = wilson_eff(k, n, DEFF)
    out = {"label": label, "k": k, "n": n,
           "point_estimate": round(scale * k / n, digits),
           "published_ci": published,
           "reproduced_naive_ci": [round(scale * lo0, digits), round(scale * hi0, digits)],
           "restated_ci": [round(scale * lo1, digits), round(scale * hi1, digits)],
           "n_eff": round(n_eff, 2),
           "published_width": round(published[1] - published[0], digits),
           "naive_width": round(scale * (hi0 - lo0), digits),
           "restated_width": round(scale * (hi1 - lo1), digits)}
    out["widening_ratio"] = (round(out["restated_width"] / out["published_width"], 4)
                             if out["published_width"] else None)
    tol = 0.002 * scale if scale > 1 else 0.002
    out["reproduces_published"] = (abs(out["reproduced_naive_ci"][0] - published[0]) <= tol
                                   and abs(out["reproduced_naive_ci"][1] - published[1]) <= tol)
    out["wider"] = out["restated_width"] > out["published_width"]
    return out


def main():
    out = {"session": 115, "deff": DEFF, "sqrt_deff": round(math.sqrt(DEFF), 4),
           "restated": [], "notes": {}}

    # ---------------- POWER-AUDIT §2, on session 110's run --------------------------------
    d, rows, excl = pa.load()
    out["power_audit_population"] = {"file": pa.RUN, "analysable": len(rows), "excluded": excl}

    published_cohorts = {
        2018: (2, 2, [0.342, 1.000]), 2019: (29, 21, [0.543, 0.853]),
        2020: (130, 106, [0.740, 0.873]), 2021: (249, 212, [0.802, 0.890]),
        2022: (412, 353, [0.820, 0.887]), 2023: (574, 487, [0.817, 0.875]),
        2024: (548, 500, [0.886, 0.933]), 2025: (510, 480, [0.917, 0.959]),
        2026: (164, 159, [0.931, 0.987]),
    }
    by_year = {}
    for r in rows:
        y = time.gmtime(r["created"]).tm_year
        by_year.setdefault(y, []).append(r)
    for y, (n_pub, k_pub, pub) in sorted(published_cohorts.items()):
        rs = by_year.get(y, [])
        k, n = sum(x["alive"] for x in rs), len(rs)
        rec = line(f"POWER-AUDIT §2 — cohort {y}, retrievable fraction", k, n, pub, digits=4)
        rec["published_n"] = n_pub
        rec["published_k"] = k_pub
        rec["population_matches_published"] = (n == n_pub and k == k_pub)
        out["restated"].append(rec)

    # ---------------- the Weibull shape, Rao-Scott ----------------------------------------
    best, curve = pa.fit(rows)
    klo, khi = pa.profile_ci(curve, best)
    klo_rs, khi_rs = pa.profile_ci(curve, best, crit=CHI2_1_95 * DEFF)
    out["weibull_shape"] = {
        "published": {"k": round(best[0], 4), "ci95_profile": [0.5017, 0.8983],
                      "source": "POWER-AUDIT.md §2"},
        "reproduced_naive": [round(klo, 4), round(khi, 4)],
        "restated_rao_scott": [round(klo_rs, 4), round(khi_rs, 4)],
        "criterion": {"naive_chi2": CHI2_1_95, "restated_chi2": round(CHI2_1_95 * DEFF, 4)},
        "point_estimate_moves": False,
        "still_excludes_1": khi_rs < 1.0,
        "what_this_is": (
            "A first-order Rao-Scott scaling of the profile deviance, NOT the same operation as "
            "the Wilson correction. It assumes one design effect governs the whole fit; the "
            "per-cell table shows the account-key design effect is not constant across age. "
            "Treat this interval as indicative of direction and magnitude, not as exact."),
        "why_it_matters": (
            "K3 of this arc's own pre-registration reads this interval: if the 95 % CI on k "
            "includes 1, the shape is undetermined and every power figure resting on it is "
            "withdrawn. The restated interval is the one that criterion should have been read "
            "against."),
    }

    # ---------------- RESULT.md / DERIVED.md — the session-109 census ---------------------
    census = json.load(open(CENSUS))
    crows, cexcl = [], {"transport_or_indeterminate": 0}
    for r in census["results"]:
        if r.get("http") not in (200, 400):
            cexcl["transport_or_indeterminate"] += 1
            continue
        crows.append({"vid": str(r["vid"]), "handle": (r.get("handle") or "").lower(),
                      "year": r["year"], "alive": 1 if r["http"] == 200 else 0})
    out["census_population"] = {"file": CENSUS, "usable": len(crows), "excluded": cexcl}

    published_census = {
        1975: (3, 0, [0.000, 0.562]), 1971: (1, 1, [0.207, 1.000]),
        2018: (2, 2, [0.342, 1.000]), 2019: (26, 19, [0.539, 0.863]),
        2020: (109, 89, [0.734, 0.878]), 2021: (201, 170, [0.789, 0.889]),
        2022: (317, 277, [0.833, 0.906]), 2023: (456, 389, [0.818, 0.883]),
        2024: (474, 437, [0.894, 0.943]), 2025: (456, 434, [0.928, 0.968]),
        2026: (128, 123, [0.912, 0.983]),
    }
    cby = {}
    for r in crows:
        cby.setdefault(r["year"], []).append(r)
    for y, (n_pub, k_pub, pub) in sorted(published_census.items()):
        rs = cby.get(y, [])
        k, n = sum(x["alive"] for x in rs), len(rs)
        if n == 0:
            continue
        rec = line(f"RESULT.md — census by decoded creation year {y}", k, n, pub, digits=4)
        rec["published_n"] = n_pub
        rec["published_k"] = k_pub
        rec["population_matches_published"] = (n == n_pub and k == k_pub)
        out["restated"].append(rec)

    # pooled census figure, the headline of the session-109 census
    k = sum(r["alive"] for r in crows)
    out["restated"].append(line("RESULT.md — census pooled, publicly retrievable",
                                k, len(crows), [0.879, 0.906], digits=4))

    # ---------------- the two ratio intervals ---------------------------------------------
    # These are not proportions and take the correction on the log scale: the standard error
    # of the log ratio is multiplied by sqrt(DEFF). Both are reported as indicative.
    s = math.sqrt(DEFF)
    mh_lo, mh_hi = 1.357, 2.345
    mh_point = math.sqrt(mh_lo * mh_hi)
    mh_se = (math.log(mh_hi) - math.log(mh_lo)) / (2 * 1.959963985)
    out["ratio_intervals"] = [
        {"label": "INCREMENT-3 §2a / session 111 — Mantel-Haenszel OR, article vs non-article",
         "published_ci": [mh_lo, mh_hi],
         "implied_point": round(mh_point, 4),
         "restated_ci": [round(mh_point * math.exp(-1.959963985 * mh_se * s), 4),
                         round(mh_point * math.exp(1.959963985 * mh_se * s), 4)],
         "method": "log-scale SE inflated by sqrt(DEFF); the point estimate does not move",
         "still_excludes_1": mh_point * math.exp(-1.959963985 * mh_se * s) > 1.0},
    ]
    # INCREMENT-1 §7: 1,940/2,175 encyclopedia-cited against 381/447 forum-linked. This is a
    # DIFFERENCE between two strata, not a pooled proportion, so it is recomputed from the two
    # arms' own counts rather than by scaling the published half-width — and it is done twice,
    # once with the pooled design effect and once with each arm's own, because the two answers
    # are not the same and the difference is the whole point.
    k1, n1, k2, n2 = 1940, 2175, 381, 447
    p1, p2 = k1 / n1, k2 / n2
    v1, v2 = p1 * (1 - p1) / n1, p2 * (1 - p2) / n2
    deff_article, deff_forum = 1.4688, 1.1859      # restatement-115.json, per-stratum, day-2 run
    z95 = 1.959963985
    variants = {
        "published (no clustering)": (v1, v2),
        "pooled DEFF 1.4289 on both arms": (v1 * DEFF, v2 * DEFF),
        "each arm's own DEFF (1.4688 article / 1.1859 forum)": (v1 * deff_article,
                                                                v2 * deff_forum),
    }
    gap = 100 * (p1 - p2)
    gap_rows = []
    for name, (a, b) in variants.items():
        se = 100 * math.sqrt(a + b)
        gap_rows.append({"variant": name, "gap_pp": round(gap, 4), "se_pp": round(se, 4),
                         "z": round(gap / se, 4),
                         "ci95_pp": [round(gap - z95 * se, 4), round(gap + z95 * se, 4)],
                         "excludes_0": gap - z95 * se > 0})
    out["ratio_intervals"].append(
        {"label": "INCREMENT-1 §7 — two-proportion gap, encyclopedia-cited vs forum-linked (pp)",
         "published_ci": [0.42, 7.50],
         "counts": {"encyclopedia": [k1, n1], "forum": [k2, n2]},
         "variants": gap_rows,
         "method": ("recomputed from the arm counts; each arm's binomial variance multiplied by "
                    "a design effect. The per-stratum design effects come from the day-2 run and "
                    "are applied to a gap measured on session 110's run — an approximation, "
                    "stated as one."),
         "note": ("The published interval was computed with the video as the independent unit. "
                  "Under the pooled correction the interval crosses zero; under the arm-specific "
                  "one it does not. Both are printed because choosing between them after seeing "
                  "the answer is exactly the move this arc has twice caught itself making.")})

    checks = out["restated"]
    out["subtract_first_check"] = {
        "n_intervals": len(checks),
        "reproduce_published": sum(1 for r in checks if r["reproduces_published"]),
        "fail_to_reproduce": [r["label"] for r in checks if not r["reproduces_published"]],
        "population_mismatches": [r["label"] for r in checks
                                  if r.get("population_matches_published") is False],
        "all_wider": all(r["wider"] for r in checks),
        "not_wider": [r["label"] for r in checks if not r["wider"]],
    }

    json.dump(out, open("restatement-115b.json", "w"), indent=1, ensure_ascii=False)

    for r in out["restated"]:
        flag = "" if r["reproduces_published"] else "  << DOES NOT REPRODUCE"
        pm = "" if r.get("population_matches_published", True) else \
            f"  << n/k differ: file {r['n']}/{r['k']} vs published {r['published_n']}/{r['published_k']}"
        print(f"{r['label']}: p={r['point_estimate']} n={r['n']} "
              f"pub {r['published_ci']} -> {r['restated_ci']} "
              f"(x{r['widening_ratio']}){flag}{pm}")
    print()
    w = out["weibull_shape"]
    print(f"Weibull k = {w['published']['k']}  published CI {w['published']['ci95_profile']} "
          f"reproduced {w['reproduced_naive']} -> Rao-Scott {w['restated_rao_scott']}  "
          f"excludes 1: {w['still_excludes_1']}")
    for r in out["ratio_intervals"]:
        if "restated_ci" in r:
            print(f"{r['label']}: {r['published_ci']} -> {r['restated_ci']}")
        else:
            print(f"{r['label']}: published {r['published_ci']}")
            for v in r["variants"]:
                print(f"    {v['variant']}: gap {v['gap_pp']} pp  z={v['z']}  "
                      f"CI {v['ci95_pp']}  excludes 0: {v['excludes_0']}")
    print()
    print("subtract-first:", json.dumps(out["subtract_first_check"], ensure_ascii=False))


if __name__ == "__main__":
    main()
