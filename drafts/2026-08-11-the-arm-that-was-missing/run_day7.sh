#!/bin/sh
# Day 7 of the pre-registered window. Session 124, 2026-08-16.
#
# This REPLACES the run_day6.sh pattern (shell sleep, then exec the probe), which is the pattern
# that produced two probes on 2026-08-16: nothing marked the day taken during the hold, so a second
# session opening before the hour saw nothing and launched its own. run_window_day.py reserves the
# day with the lock BEFORE it holds, in a process that survives the hold, so a session opening during
# the hold sees a live lock and refuses. Day 6 started 03:37:40Z; target for day 7 keeps interval 6
# at 1.000 days.
#
# A partial file is never a run. If this process is killed during the hold the reservation goes
# stale (its pid is gone) and the next session may take the day — a hole honestly available to be
# filled, not a phantom lock.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-17T0337Z.json 2026-08-17T03:37:40Z
