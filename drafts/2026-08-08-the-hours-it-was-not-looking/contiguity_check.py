#!/usr/bin/env python3
"""contiguity_check.py — the adversary's C-I attack, re-run independently by this practice.

INTERLOCUTOR-2.md §(a) ATTACK 1 claims the 20h45m listed-but-absent window is recoverable
from the manifest's declared byte column alone: flag each listed gkg cycle whose declared
size is below a fraction of a local rolling median, take maximal runs of consecutive
flagged cycles, and the longest run in the whole series is exactly the 83 absent ones.

This is our own implementation, written from the description, not the adversary's code.
If it reproduces, the core claim's "rather than derived from the index" clause is false
and must be struck.

Usage: python3 contiguity_check.py <manifest.txt> <out.json>
"""
import json, statistics, sys
from datetime import datetime, timedelta, timezone

STEP = timedelta(minutes=15)
HALF = 2 * 24 * 4          # +/- 2 days of cycles, as the adversary described
THRESHOLDS = [0.05, 0.10, 0.20, 0.35, 0.50]

cyc = {}
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    p = line.split()
    if len(p) != 3 or not p[0].isdigit():
        continue
    f = p[2].rsplit("/", 1)[-1]
    st, rest = f[:14], f[14:].lower()
    if not st.isdigit() or len(st) != 14 or rest.startswith(".translation") or not rest.startswith(".gkg"):
        continue
    try:
        ts = datetime.strptime(st, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    except ValueError:
        continue
    cyc[ts] = int(p[0])

order = sorted(cyc)
sizes = [cyc[t] for t in order]
out = {"listed_cycles": len(order), "half_window_cycles": HALF, "by_threshold": {}}

for thr in THRESHOLDS:
    flagged = []
    for i, t in enumerate(order):
        lo, hi = max(0, i - HALF), min(len(order), i + HALF + 1)
        med = statistics.median(sizes[lo:hi])
        if med > 0 and sizes[i] < thr * med:
            flagged.append(t)
    runs, cur = [], [flagged[0]] if flagged else []
    for a, b in zip(flagged, flagged[1:]):
        if b - a == STEP:
            cur.append(b)
        else:
            runs.append(cur); cur = [b]
    if cur:
        runs.append(cur)
    runs.sort(key=len, reverse=True)
    top = [{"length": len(r),
            "first": r[0].strftime("%Y-%m-%dT%H:%M:%SZ"),
            "last": r[-1].strftime("%Y-%m-%dT%H:%M:%SZ")} for r in runs[:5]]
    out["by_threshold"][str(thr)] = {"flagged": len(flagged), "runs": len(runs),
                                     "runs_ge_20": sum(1 for r in runs if len(r) >= 20),
                                     "top5": top}
    print(thr, "flagged", len(flagged), "longest", top[0] if top else None,
          "2nd", top[1]["length"] if len(top) > 1 else None, flush=True)

json.dump(out, open(sys.argv[2], "w"), indent=1)
