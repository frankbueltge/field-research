#!/usr/bin/env python3
"""run_window_day - reserve a window day, hold to its hour, then measure it, in one process.

Session 124, 2026-08-16. Deviation D23, BOOKKEEPING ONLY: the probe is unchanged; this only holds
the start to the series' own hour and reserves the day against a second run while it waits.

WHY A PYTHON RUNNER AND NOT THE SHELL SLEEP
--------------------------------------------
`run_day6.sh` held its sleep and then `exec`d the probe. Nothing marked the day as taken during
the hold, so when a second session opened one minute before the hour it saw no run in flight and
launched its own — two complete probes over the same manifest at the same second
(`DOUBLE-PROBE-122.md`).

This runner closes that. It reserves the day with `run_lock` at the instant it is scheduled,
BEFORE the hold, naming its own process. Because the reservation and the measurement are the same
process, the lock's pid stays valid through the whole hold; a session opening during the hold sees
a live lock over this manifest and day and refuses. When the hour arrives the probe runs in this
same process and takes over its own reservation. A partial file is never a run, and if this process
is killed during the hold the reservation goes stale (its pid is gone) and the next run may take
the day — a hole honestly available to be filled, not a phantom lock.

USAGE
    python3 run_window_day.py <manifest> <out_path> <target_utc>
    e.g. python3 run_window_day.py manifest-day2-onward.json \\
             ledger/run-2026-08-17T0337Z.json 2026-08-17T03:37:40Z

WHAT IT STILL CANNOT DO
-----------------------
It is a lock on one filesystem. Two probes launched from two separate checkouts of this repository
cannot see each other's reservation and this would not stop them. It stops the case that actually
happened — a held run and a second session against the same working tree — and claims nothing
past that.
"""
import calendar
import os
import sys
import time

import ledger
import run_lock


def main(manifest, out_path, target_utc):
    ledger_dir = os.path.dirname(out_path) or "ledger"
    target = calendar.timegm(time.strptime(target_utc, "%Y-%m-%dT%H:%M:%SZ"))

    # Reserve BEFORE the hold. acquire() refuses if the day is already in flight or complete, so a
    # reservation is only taken when the day is genuinely open.
    try:
        state = run_lock.reserve(manifest, out_path, ledger_dir=ledger_dir)
    except run_lock.RunRefused as e:
        print("reservation refused: " + str(e), file=sys.stderr)
        return 3
    print("reserved " + target_utc + " for pid " + str(os.getpid())
          + "; holding", file=sys.stderr)

    wait = target - time.time()
    if wait > 0:
        print("holding " + str(int(wait)) + " s until " + target_utc, file=sys.stderr)
        # Kept in one process so the reservation's pid stays valid through the hold.
        time.sleep(wait)

    print("start " + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), file=sys.stderr)
    # The measurement, in this same process. Its own acquire() takes over the reservation this
    # process wrote (pid matches) and runs the full in-flight/complete checks against anything a
    # sibling may have landed during the hold.
    ledger.main(manifest, out_path)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: run_window_day.py <manifest> <out_path> <target_utc>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
