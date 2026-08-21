#!/usr/bin/env python3
"""Which file does the series-shape guard call day 6, and is it the series record?

Found on 2026-08-21 (session 130) while building a page from the committed run files.
Nothing here edits anything. It reproduces one selection and prints what it selects.

THE GUARD'S OWN RULE, quoted from window_status.py:

    "The first run of a UTC day is the day; any further completed run of the same day
     is reported separately as an extra pass."

THE CASE IT MEETS: on 2026-08-16 two complete probes ran over the same manifest, started
by two sessions of the same date that could not see each other, at the SAME SECOND
(DOUBLE-PROBE-122.md). "First" has nothing to order on, so the tie falls to the iteration
order, which is `sorted(glob("run-*.json"))` — filename order. `-` (0x2D) sorts before
`.` (0x2E), so `run-...T0337Z-second-probe.json` precedes `run-...T0337Z.json`.

    python3 notes/2026-08-21-window-compliance/day6_selection_check.py
"""

from __future__ import annotations

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARC = os.path.join(ROOT, "drafts", "2026-08-11-the-arm-that-was-missing")
LEDGER = os.path.join(ARC, "ledger")


def main() -> int:
    paths = sorted(glob.glob(os.path.join(LEDGER, "run-*.json")))
    same_day = [p for p in paths if "2026-08-16" in os.path.basename(p)]
    print("run files for 2026-08-16, in the guard's own iteration order:")
    for p in same_day:
        d = json.load(open(p))
        counts = {}
        for arm in d["counts"].values():
            for k, v in arm.items():
                counts[k] = counts.get(k, 0) + v
        print(f"  {os.path.basename(p)}")
        print(f"      start {d['run_utc_start']}  end {d['run_utc_end']}  "
              f"requested {d['requested']}")
        print(f"      {counts}")

    status = json.load(open(os.path.join(ARC, "window-status-129.json")))
    day6 = [e["file"] for e in status["measurement_days"] if e["start_utc"].startswith("2026-08-16")]
    extra = [e["file"] for e in status["extra_passes_same_day"]]
    print()
    print("window-status-129.json calls the measurement day :", *day6)
    print("window-status-129.json calls the extra pass      :", *extra)

    diff = json.load(open(os.path.join(LEDGER, "diff-day5-day6.json")))
    retry = json.load(open(os.path.join(LEDGER, "diff-day6-retry.json")))
    print()
    print("the arc's diff chain uses, into day 6            :", diff["run2"]["path"])
    print("the arc's diff chain uses, out of day 6          :", retry["run1"]["path"])
    print("DOUBLE-PROBE-122.md section 1 records            : "
          "ledger/run-2026-08-16T0337Z.json keeps the canonical name and "
          "'landed as the series record'")

    verdict = "AGREE" if day6 and day6[0] == diff["run2"]["path"] else "DISAGREE"
    print()
    print(f"VERDICT: the series-shape guard and the diff chain {verdict} "
          "about which file is day 6.")
    print("SCOPE: window-status-129.json publishes only file, start_utc, n_observations and")
    print("  n_planned per day. Both files carry 3869/3869 and the identical start second, so")
    print("  NO figure in that file moves. What is wrong is the attribution: the file whose own")
    print("  name says it is the second probe is named as the day, and the file the arc records")
    print("  as the series record is filed as the extra pass. Had the two runs started at")
    print("  different seconds, or had the status file published per-day state counts (they")
    print("  differ: see above), this would have moved figures.")
    return 0 if verdict == "AGREE" else 1


if __name__ == "__main__":
    sys.exit(main())
