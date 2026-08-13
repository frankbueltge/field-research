#!/usr/bin/env python3
"""Which citing pages lose their videos together, and is the extreme one extreme by chance?

Session 115. **No new requests.** Companion to `page_mechanism_115.py`.

The one article that carries the page-key design effect was found by an adversary, post hoc, by
being extreme. A p-value computed on a cell selected for being extreme is worthless, so this file
does the only honest version: it scores EVERY page of at least ten cited videos against the
expectation from its own units' age-band x arm cells, and reports where the found article sits in
that family. A Monte Carlo over the whole family gives the exceedance probability of a maximum,
not of a cell picked after the fact.

Output: `page-scan-115.json`.
"""
import json
import random
import sys

import cluster_model as cm
import cluster_keys as ck

RUN = "ledger/run-2026-08-12T0341Z.json"
MIN_UNITS = 10
DRAWS = 20000
SEED = 20260813


def main():
    d, rows, excl, key = cm.load(RUN)
    idx = ck.page_index()
    for r in rows:
        r["page"] = idx.get(r["vid"])
    att = [r for r in rows if r["page"]]

    # each unit's null probability: the observed absence rate of its own age-band x arm cell
    cells = {}
    for r in att:
        cells.setdefault((r["arm"], r["band"]), []).append(r["absent"])
    rate = {k: sum(v) / len(v) for k, v in cells.items()}
    for r in att:
        r["p_null"] = rate[(r["arm"], r["band"])]

    pages = {}
    for r in att:
        pages.setdefault(r["page"], []).append(r)
    big = {k: v for k, v in pages.items() if len(v) >= MIN_UNITS}

    def excess(v):
        obs = sum(r["absent"] for r in v)
        exp = sum(r["p_null"] for r in v)
        return obs, exp, obs - exp

    table = []
    for k, v in big.items():
        obs, exp, ex = excess(v)
        table.append({"page": k, "units": len(v), "absent": obs,
                      "expected_from_age_and_arm": round(exp, 3),
                      "excess": round(ex, 3),
                      "absence_rate": round(obs / len(v), 4),
                      "distinct_handles": len(set(r["handle"] for r in v))})
    table.sort(key=lambda t: -t["excess"])

    # Monte Carlo on the whole family: how often does ANY page of >= MIN_UNITS reach this excess?
    rng = random.Random(SEED)
    keys = list(big)
    probs = {k: [r["p_null"] for r in big[k]] for k in keys}
    top_excess = table[0]["excess"]
    hits = 0
    maxima = []
    for _ in range(DRAWS):
        m = -1e9
        for k in keys:
            ps = probs[k]
            obs = sum(1 for p in ps if rng.random() < p)
            e = obs - sum(ps)
            if e > m:
                m = e
        maxima.append(m)
        if m >= top_excess:
            hits += 1
    maxima.sort()

    out = {"session": 115, "run": RUN, "no_new_requests": True,
           "min_units": MIN_UNITS, "pages_scored": len(big),
           "units_in_scored_pages": sum(len(v) for v in big.values()),
           "family_monte_carlo": {
               "draws": DRAWS, "seed": SEED,
               "statistic": "the largest absent-minus-expected excess over ALL scored pages",
               "observed_top_excess": top_excess,
               "null_mean_max": round(sum(maxima) / len(maxima), 4),
               "null_p95_max": round(maxima[int(0.95 * len(maxima))], 4),
               "null_max_max": round(maxima[-1], 4),
               "n_ge_observed": hits,
               "p_value_family_wise": (hits + 1) / (DRAWS + 1)},
           "top_20_by_excess": table[:20],
           "bottom_5_by_excess": table[-5:],
           "note": ("Expected counts come from each unit's own age-band x arm absence rate in the "
                    "same run, so a page of old forum videos is not scored against a corpus-wide "
                    "rate. The family-wise test asks how often the MAXIMUM excess over all scored "
                    "pages reaches the observed maximum — the only question that can be asked of a "
                    "cell that was selected for being extreme.")}
    json.dump(out, open("page-scan-115.json", "w"), indent=1, ensure_ascii=False)

    print(f"scored {len(big)} pages of >= {MIN_UNITS} units "
          f"({out['units_in_scored_pages']} units)")
    f = out["family_monte_carlo"]
    print(f"family-wise: observed max excess {f['observed_top_excess']}, null mean max "
          f"{f['null_mean_max']}, null p95 {f['null_p95_max']}, null max {f['null_max_max']}, "
          f"p = {f['p_value_family_wise']:.5f}")
    for t in table[:8]:
        print(f"  +{t['excess']:6.2f}  {t['absent']:3d}/{t['units']:3d} "
              f"(exp {t['expected_from_age_and_arm']:6.2f}) {t['distinct_handles']:3d}h  {t['page']}")
    print("  ...")
    for t in table[-3:]:
        print(f"  {t['excess']:7.2f}  {t['absent']:3d}/{t['units']:3d} "
              f"(exp {t['expected_from_age_and_arm']:6.2f}) {t['distinct_handles']:3d}h  {t['page']}")


if __name__ == "__main__":
    sys.exit(main())
