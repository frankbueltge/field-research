#!/usr/bin/env python3
"""Condition 1, session 113: the ceiling bound recomputed at every resolution.

INTERLOCUTOR-5.md broke §2a of INCREMENT-3.md. The claim was:

    "no age composition of this reference population reaches the 36 % their scrape
     measured among API-failing videos"

with the warrant that a weighted mean cannot exceed its largest component, and the largest
component being the 5y+ band at 17.80 % absent (Wilson upper 21.95 %).

THE WARRANT IS TRUE AND THE APPLICATION IS NOT. "A weighted mean cannot exceed its largest
component" holds only relative to the partition whose components you are averaging. The
reference population is not six bins - it is 3,575 individually dated identifiers, and any
sub-selection of them is also "an age composition of this population". At calendar-year
resolution the document's OWN published table already exceeds the stated ceiling, and the
adversary found it three paragraphs above the claim.

This script computes the bound at every resolution the data supports, so that whatever
survives is stated at the resolution it actually holds at, and the resolution is named.
Output: ceiling-recompute.json
"""

import json
import math

BASE = "presence-baseline.json"
RUN = "ledger/run-2026-08-12T0341Z.json"
OUT = "ceiling-recompute.json"
RECEIVER_NOT_PUBLIC = 0.36   # their published share among API-failing videos
FLOOR = 30                   # the pre-registration's own n >= 30 rule for criterion cells


def wilson(k, n, z=1.959963985):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def cells(rows, keyfn):
    out = {}
    for r in rows:
        out.setdefault(keyfn(r), []).append(r)
    res = {}
    for k, v in sorted(out.items()):
        n = len(v)
        absent = sum(1 for x in v if not x["alive"])
        lo, hi = wilson(absent, n)
        res[str(k)] = {"n": n, "absent": absent, "absent_rate": absent / n,
                       "absent_ci": [lo, hi]}
    return res


def worst(table, floor):
    elig = {k: c for k, c in table.items() if c["n"] >= floor}
    if not elig:
        return None
    k = max(elig, key=lambda k: elig[k]["absent_rate"])
    return {"cell": k, **elig[k], "n_cells_eligible": len(elig),
            "n_cells_dropped_below_floor": len(table) - len(elig)}


def main():
    import calendar
    import time
    b = json.load(open(BASE))
    d = json.load(open(RUN))
    T_REF = calendar.timegm((2026, 8, 12, 3, 40, 0, 0, 0, 0))
    YEAR_S = 365.25 * 86400.0

    rows = []
    for o in d["observations"]:
        if o["arm"] == "B-truncated" or o["state"] == "INDETERMINATE":
            continue
        vid = str(o["vid"])
        if len(vid) != 19:
            continue
        created = int(vid) >> 32
        age_s = T_REF - created
        if age_s <= 0:
            continue
        rows.append({"alive": 1 if o["state"] == "RETRIEVABLE" else 0,
                     "age_y": age_s / YEAR_S,
                     "year": time.gmtime(created).tm_year})
    assert len(rows) == b["pooled"]["n"], (len(rows), b["pooled"]["n"])

    partitions = {
        "six_published_bands": cells(
            rows, lambda r: next(f"{lo}-{hi}y" if hi < 99 else f"{lo}y+"
                                 for lo, hi in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 99)]
                                 if lo <= r["age_y"] < hi)),
        "calendar_year": cells(rows, lambda r: r["year"]),
        "integer_age_year": cells(rows, lambda r: f"{int(r['age_y'])}-{int(r['age_y'])+1}y"),
        "half_year": cells(rows, lambda r: f"{int(r['age_y']*2)/2:.1f}y"),
    }

    result = {}
    for name, table in partitions.items():
        w = worst(table, FLOOR)
        result[name] = {
            "n_cells": len(table),
            "worst_cell_at_floor_30": w,
            "excludes_receiver_36pct_on_point": (w["absent_rate"] < RECEIVER_NOT_PUBLIC) if w else None,
            "excludes_receiver_36pct_on_upper_ci": (w["absent_ci"][1] < RECEIVER_NOT_PUBLIC) if w else None,
            "table": table,
        }

    out = {
        "schema": "field-research/ceiling-recompute/1",
        "written_by": "session 113, discharging condition 1 of INTERLOCUTOR-5.md",
        "what_was_broken": (
            "INCREMENT-3.md §2a claimed no age composition of the reference population "
            "reaches 36 %, warranted by 'a weighted mean cannot exceed its largest "
            "component' applied to the six published bands. The warrant is partition-"
            "relative and the population is 3,575 individually dated identifiers, so the "
            "claim as literally written is false: finer partitions of the same population "
            "exceed the stated ceiling."),
        "receiver_share_not_public_among_api_failures": RECEIVER_NOT_PUBLIC,
        "floor": FLOOR,
        "by_partition": result,
        "the_honest_form": (
            "There is no finite supremum over arbitrary sub-selections - a one-identifier "
            "'composition' is 100 % absent. Any bound must name its resolution and its "
            "minimum cell size. The bound is therefore restated with both, and it survives "
            "only at the resolutions where it survives, which is stated rather than chosen."),
    }
    json.dump(out, open(OUT, "w"), indent=1)

    for name, r in result.items():
        w = r["worst_cell_at_floor_30"]
        print(f"{name:>22}  cells={r['n_cells']:>3}  worst(n>=30)={w['cell']:>8} "
              f"n={w['n']:>4} absent={w['absent_rate']:.4f} "
              f"CI=[{w['absent_ci'][0]:.4f},{w['absent_ci'][1]:.4f}]  "
              f"excl36(point)={r['excludes_receiver_36pct_on_point']} "
              f"excl36(upperCI)={r['excludes_receiver_36pct_on_upper_ci']}")
    print("\nwritten", OUT)


if __name__ == "__main__":
    main()
