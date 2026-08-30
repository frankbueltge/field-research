#!/usr/bin/env python3
"""blinding_share_139 - the one figure `PREREGISTRATION-138B.md` section 4 requires re-measuring.

Session 139, 2026-08-30. Session 137 measured, of `extract_units_137_v2.py`'s 483 units, that
**137 (28.4 %) carry a token no reader's answer contains**. Section 4 of `PREREGISTRATION-138B.md`
says that figure is a property of v2's units and that a hand-delimited population must be
re-measured rather than inherit it. This is that re-measurement, over the units of
`units-139.json`, using `blinding_check_137.py`'s own TELLS table unchanged - the table is imported,
not retyped, so no tell can drift between the two measurements.

WHAT IT COUNTS, precisely: a unit counts if it matches at least one tell whose per-role counts show
ZERO hits among reader units in THIS population. "No reader's answer contains it" is therefore a
property measured on these 34 reader units, not a general fact about readers - a tell absent here
could appear in the 19 reader-role passes this fragment does not cover.

IT IS A FRAGMENT AND NOT COMPARABLE TO 28.4 % AS A TREND. Different units, different files, a
different number of them. Two figures, not a series.
"""
import json
import sys

from blinding_check_137 import TELLS


def main(units_path, manifest_path, out_path):
    units = json.load(open(units_path, encoding="utf-8"))
    km = json.load(open(manifest_path, encoding="utf-8"))["key_map"]

    reader_free = []
    for name, pat in TELLS.items():
        if not any(pat.search(u["text"]) for u in units
                   if km[u["key"]]["role"] == "reader"):
            reader_free.append((name, pat))

    carriers, per_tell = set(), {}
    for name, pat in reader_free:
        hit = {u["key"] for u in units if pat.search(u["text"])}
        per_tell[name] = len(hit)
        carriers |= hit

    n = len(units)
    out = {
        "population": units_path, "units": n,
        "units_by_role": {r: sum(1 for v in km.values() if v["role"] == r)
                          for r in sorted({v["role"] for v in km.values()})},
        "tells_absent_from_every_reader_unit": [n_ for n_, _ in reader_free],
        "units_per_such_tell": per_tell,
        "units_carrying_at_least_one": len(carriers),
        "share": round(len(carriers) / n, 4) if n else None,
        "session_137_figure_over_v2_units": {"carriers": 137, "units": 483, "share": 0.284},
        "comparability": "NOT a series. Different units over different files, and this population "
                         "is 19 files of 53. The two shares are two measurements, not a trend, and "
                         "neither may be quoted as movement in the other's direction.",
    }
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("tells absent from every reader unit: %s" % out["tells_absent_from_every_reader_unit"])
    print("units carrying at least one: %d of %d (%.1f %%)"
          % (len(carriers), n, 100 * len(carriers) / n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
