#!/usr/bin/env python3
"""Do the run files' own count blocks survive a recount of their observations?

Session 130, 2026-08-21. This check existed as a refusal inside a page generator that was
built and then deleted unpublished (see NOTE.md). The generator refused to build if its
recount of a run file's observations disagreed with the per-arm `counts` block that same
file carries; it did not refuse, on any of the eleven completed runs. Keeping the check
alone, without the page, is what makes that a standing fact instead of a deleted one.

It reads only committed files and writes nothing.

    python3 notes/2026-08-21-window-compliance/recount_check.py

Exit 0 = every run file agrees with itself. Exit 1 = at least one does not.
"""

from __future__ import annotations

import glob
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGER = os.path.join(ROOT, "drafts", "2026-08-11-the-arm-that-was-missing", "ledger")


def main() -> int:
    bad = 0
    paths = sorted(glob.glob(os.path.join(LEDGER, "run-*.json")))
    if not paths:
        print("no run files found", file=sys.stderr)
        return 1
    for path in paths:
        run = json.load(open(path))
        recount = Counter(o["state"] for o in run["observations"])
        own: Counter = Counter()
        for arm in run["counts"].values():
            own.update(arm)
        ok = dict(recount) == dict(own)
        bad += 0 if ok else 1
        print(f"{'OK ' if ok else 'BAD'}  {os.path.basename(path)}  "
              f"{len(run['observations'])} observations  {dict(sorted(recount.items()))}")
        if not ok:
            print(f"      the file's own counts block: {dict(sorted(own.items()))}")

    print()
    print(f"{len(paths)} completed run files checked, {bad} disagreeing with themselves.")
    print("SCOPE, stated so this is not read as more than it is: this compares a run file")
    print("  against ITSELF. It says the summary block was not written from something other")
    print("  than the observations beside it. It says nothing about whether the observations")
    print("  are right, and it cannot: the probe is not re-run here.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
