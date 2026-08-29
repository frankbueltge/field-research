#!/bin/sh
# Session 138, 2026-08-29. Chains the day-16 close pipeline to the probe's own exit, so the day
# closes even if this session dies first — the failure that made 2026-08-24 and 2026-08-27 holes.
# Modelled on await_and_close_day13.sh.
cd "$(dirname "$0")" || exit 1
while kill -0 "$1" 2>/dev/null; do sleep 20; done
echo "probe pid $1 exited $(date -u)"
test -f ledger/run-2026-08-29T0341Z.json || { echo "no run file - a .partial is never a run"; exit 1; }
sh run_day16-2026-08-29_close.sh
echo "CLOSE_EXIT=$?"
