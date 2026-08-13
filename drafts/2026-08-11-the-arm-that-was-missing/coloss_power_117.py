#!/usr/bin/env python3
"""POST-HOC, and labelled as such: what the scan of coloss_117.py could and could not have seen.

Session 117, 2026-08-13. Nothing here was pre-registered. It exists because the scan flagged
2 pages of 54, and "2 of 54" means nothing until we know how large an excess a page of this
size would have needed before the scan could see it at all. A negative result whose detection
floor is unstated is not a negative result.

Also answers, from data already collected and with NO new request:
  - are the 20 accounts of the flagged article present anywhere else in this corpus at all
    (the mechanism arm returned 0 of 22 covered and the pre-registered power floor fired);
  - were the flagged article's videos already absent at BASELINE, i.e. is this a standing
    state and not something the window watched happen;
  - within the flagged article, do the absent units differ in age from the surviving ones.

Usage: python3 coloss_power_117.py
"""
import collections
import json

import cluster_keys as ck
import cluster_model as cm
from coloss_117 import PARAGUAY, N_MIN, cell_of, tails

RUN = "ledger/run-2026-08-13T0427Z.json"
BASELINE = "ledger/baseline-union.json"


def detectability(rows, idx):
    """For each scanned page: the smallest absent count that clears a Bonferroni threshold.

    Bonferroni over the scanned pages is CONSERVATIVE relative to the pre-registered BH, so
    this floor is an upper bound on what BH needed. Stated that way and not flattered.
    """
    att = [r for r in rows if r["vid"] in idx]
    by_page = collections.defaultdict(list)
    for r in att:
        by_page[idx[r["vid"]]].append(r)
    n_cell = collections.Counter()
    a_cell = collections.Counter()
    for r in att:
        n_cell[cell_of(r)] += 1
        a_cell[cell_of(r)] += r["absent"]

    scanned = {k: v for k, v in by_page.items() if len(v) >= N_MIN}
    alpha = 0.05 / len(scanned)
    out = []
    for page, units in scanned.items():
        ps = [a_cell[cell_of(r)] / n_cell[cell_of(r)] for r in units]
        need = None
        for a in range(len(units) + 1):
            if tails(ps, a)[0] <= alpha:
                need = a
                break
        exp = sum(ps)
        out.append({"page": page, "n": len(units), "absent": sum(r["absent"] for r in units),
                    "expected": exp, "min_detectable_absent": need,
                    "min_detectable_excess": (need - exp) if need is not None else None,
                    "min_detectable_share": (need / len(units)) if need is not None else None,
                    "undetectable_at_any_count": need is None})
    return alpha, out


def page_detail(rows, idx, page_key, baseline_states):
    units = [r for r in rows if idx.get(r["vid"]) == page_key]
    absent = [r for r in units if r["absent"]]
    present = [r for r in units if not r["absent"]]
    handles_here = {r["handle"] for r in units}
    elsewhere = collections.Counter()
    for r in rows:
        if r["vid"] in idx and idx[r["vid"]] != page_key and r["handle"] in handles_here:
            elsewhere[r["handle"]] += 1
    base = collections.Counter(baseline_states.get(str(r["vid"]), "NOT-IN-BASELINE")
                               for r in units)
    return {
        "page": page_key, "units": len(units),
        "absent": len(absent), "present": len(present),
        "distinct_accounts": len(handles_here),
        "accounts_appearing_on_any_other_page": len([h for h in handles_here if elsewhere[h]]),
        "other_page_units_by_those_accounts": sum(elsewhere.values()),
        "median_age_absent_y": (sorted(r["age_y"] for r in absent)[len(absent) // 2]
                                if absent else None),
        "median_age_present_y": (sorted(r["age_y"] for r in present)[len(present) // 2]
                                 if present else None),
        "age_range_y": [min(r["age_y"] for r in units), max(r["age_y"] for r in units)],
        "year_cohorts": dict(collections.Counter(r["year"] for r in units)),
        "strata": dict(collections.Counter(r["stratum"] for r in units)),
        "state_at_baseline": dict(base),
        "accounts_one_video_each": sum(1 for h, c in
                                       collections.Counter(r["handle"] for r in units).items()
                                       if c == 1),
    }


def main():
    idx = ck.page_index()
    d, rows, excl, key = cm.load(RUN)
    try:
        b = json.load(open(BASELINE))
        obs = b.get("observations") or b.get("units") or []
        baseline_states = {str(o["vid"]): o["state"] for o in obs}
    except (FileNotFoundError, KeyError, TypeError):
        baseline_states = {}

    alpha, det = detectability(rows, idx)
    shares = sorted(x["min_detectable_share"] for x in det if x["min_detectable_share"])
    excesses = sorted(x["min_detectable_excess"] for x in det if x["min_detectable_excess"])
    flagged = [PARAGUAY, "ja.wikipedia.org|瀬乃真帆子"]
    out = {
        "schema": "field-research/coloss-power/1", "session": 117,
        "post_hoc": True, "note": "NOT pre-registered; written after the scan was run",
        "run": RUN, "bonferroni_alpha": alpha, "pages_scanned": len(det),
        "pages_undetectable_at_any_count": sum(1 for x in det
                                               if x["undetectable_at_any_count"]),
        "min_detectable_share_median": shares[len(shares) // 2] if shares else None,
        "min_detectable_share_min": shares[0] if shares else None,
        "min_detectable_share_max": shares[-1] if shares else None,
        "min_detectable_excess_median": excesses[len(excesses) // 2] if excesses else None,
        "detectability_by_page": sorted(det, key=lambda x: (-x["n"], x["page"])),
        "flagged_page_detail": [page_detail(rows, idx, p, baseline_states) for p in flagged],
    }
    json.dump(out, open("coloss-power-117.json", "w"), indent=1)

    print(f"Bonferroni alpha over {len(det)} scanned pages = {alpha:.2e}")
    print(f"pages that could NOT be flagged even if every unit were absent: "
          f"{out['pages_undetectable_at_any_count']} of {len(det)}")
    print(f"min detectable absent share: median {100*out['min_detectable_share_median']:.1f} %  "
          f"range [{100*out['min_detectable_share_min']:.1f}, "
          f"{100*out['min_detectable_share_max']:.1f}] %")
    print(f"min detectable EXCESS over expectation: median "
          f"{out['min_detectable_excess_median']:.2f} videos")
    print("\nby page size:")
    for n in sorted({x['n'] for x in det}):
        g = [x for x in det if x["n"] == n]
        u = sum(1 for x in g if x["undetectable_at_any_count"])
        ok = [x["min_detectable_absent"] for x in g if x["min_detectable_absent"] is not None]
        print(f"  n={n:3d}  pages {len(g):3d}  undetectable {u:3d}  "
              f"needs absent >= {min(ok) if ok else '-'}")
    for p in out["flagged_page_detail"]:
        print(f"\n--- {p['page']}")
        for k, v in p.items():
            if k != "page":
                print(f"    {k}: {v}")
    print("\nwrote coloss-power-117.json")


if __name__ == "__main__":
    main()
