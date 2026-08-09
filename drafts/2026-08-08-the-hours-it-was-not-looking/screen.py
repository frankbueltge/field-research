#!/usr/bin/env python3
"""screen.py — the free screen, computed once for every listed cycle.

`contiguity_check.py` (session 104) reproduced the adversary's manifest-only screen and
reported counts per threshold. Increment 3 needs the screen *per cycle*, because the
pre-registered P3 asks whether the cycles the host does not serve are all already flagged
by it. So this writes, for every listed cycle of one type, the ratio

    declared size / median declared size of the +/-192 listed cycles around it

which is the quantity the screen thresholds. Same window as the session-104
implementation. A sliding sorted window keeps it to one pass.

Usage: screen.py <manifest> <suffix> <out.json>
"""

from __future__ import annotations

import bisect
import json
import re
import sys

HALF = 2 * 24 * 4          # +/- 2 days of listed cycles, as at session 104
TS = re.compile(r"/(\d{14})[.]")


def main():
    manifest, suffix, out = sys.argv[1], sys.argv[2], sys.argv[3]
    rows = []
    with open(manifest, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            p = line.split()
            if len(p) != 3 or not p[0].isdigit() or not p[2].endswith(suffix):
                continue
            m = TS.search(p[2])
            if m:
                rows.append((m.group(1), int(p[0])))
    rows.sort()
    sizes = [r[1] for r in rows]
    n = len(sizes)

    window = sorted(sizes[:min(n, HALF + 1)])
    lo, hi = 0, min(n, HALF + 1)          # window currently covers sizes[lo:hi]
    ratios = {}
    for i in range(n):
        want_lo, want_hi = max(0, i - HALF), min(n, i + HALF + 1)
        while hi < want_hi:
            bisect.insort(window, sizes[hi]); hi += 1
        while lo < want_lo:
            window.pop(bisect.bisect_left(window, sizes[lo])); lo += 1
        w = len(window)
        med = window[w // 2] if w % 2 else (window[w // 2 - 1] + window[w // 2]) / 2
        ratios[rows[i][0]] = round(sizes[i] / med, 6) if med else None

    json.dump({"suffix": suffix, "cycles": n, "half_window": HALF, "ratio": ratios},
              open(out, "w"))
    print(f"{suffix}: {n} cycles screened")


if __name__ == "__main__":
    main()
