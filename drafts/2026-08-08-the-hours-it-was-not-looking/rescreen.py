#!/usr/bin/env python3
"""rescreen.py — hour-of-day normalised re-screen of the volume-collapse arm.

Prepared while the adversary was still reading; run only after its verdict, so the state
it graded is the state it graded. The pre-registered screen compares each cycle's GKG
byte size against the median of the 672 complete cycles before it — a window that spans
all hours of the day, so a naturally busy quarter-hour is easier to flag than a quiet one.
This variant compares each cycle against the median of the SAME hour of day over the
preceding 28 complete cycles at that hour, removing the diurnal term.

Usage: python3 rescreen.py <manifest> <out.json>
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone

WINDOW = 28          # same hour-of-day, ~28 days back
FRACTION = 0.20      # same threshold as the pre-registered screen


def main():
    manifest, out = sys.argv[1], sys.argv[2]
    cycles = {}
    with open(manifest, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            p = line.split()
            if len(p) != 3 or not p[0].isdigit():
                continue
            fname = p[2].rsplit("/", 1)[-1]
            stamp, rest = fname[:14], fname[14:].lower()
            if not stamp.isdigit() or len(stamp) != 14:
                continue
            if rest.startswith(".translation"):
                rest = rest[len(".translation"):]
            if not rest.startswith(".gkg"):
                continue
            try:
                ts = datetime.strptime(stamp, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            cycles[ts] = int(p[0])

    order = sorted(cycles)
    history = defaultdict(list)                 # (hour, minute) -> recent sizes
    flagged, excluded = [], 0
    for ts in order:
        key = (ts.hour, ts.minute)
        hist = history[key]
        if len(hist) < WINDOW:
            excluded += 1
        else:
            med = statistics.median(hist[-WINDOW:])
            if med > 0 and cycles[ts] < FRACTION * med:
                flagged.append({"ts": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "gkg_bytes": cycles[ts], "same_hour_median": med,
                                "ratio": round(cycles[ts] / med, 4)})
        hist.append(cycles[ts])

    res = {"window_same_hour_cycles": WINDOW, "fraction": FRACTION,
           "cycles_scored": len(order) - excluded, "excluded_no_window": excluded,
           "flagged": len(flagged), "detail": flagged}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "detail"}, indent=1))


if __name__ == "__main__":
    main()
