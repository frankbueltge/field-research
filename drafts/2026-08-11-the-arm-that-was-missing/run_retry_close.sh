#!/bin/sh
# The post-run pipeline for the day-7 RETRY of 2026-08-18, written BEFORE the run closed so no
# step is improvised. Session 126.
#
# The comparison day is 2026-08-16 - the last COMPLETED measurement day - and specifically its
# CANONICAL run file, not the second probe of that date (DOUBLE-PROBE-122.md). The run launched
# 2026-08-17 is not a measurement: it stopped at 600 of 3,869 and only a .partial remains
# (ERRATA-126.md, E21). So the interval this computes is a TWO-DAY interval and every document
# that quotes it must say so.
set -e
D6=ledger/run-2026-08-16T0337Z.json
R=ledger/run-2026-08-18T0341Z.json

test -f "$R" || { echo "the retry has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$D6" "$R" ledger/diff-day6-retry.json
python3 ledger_diff.py "$D6" "$R" ledger/diff-day6-retry-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day6-retry.json ledger/transition-confirm-2026-08-18.json
python3 confirmation_record_121.py
python3 window_status.py
python3 retry_metrics_126.py
