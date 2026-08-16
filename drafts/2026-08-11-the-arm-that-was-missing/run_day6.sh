#!/bin/sh
# Day 6 of the pre-registered window, session 122, 2026-08-16.
# The probe is unchanged; this script only holds the start to the series' own hour.
# Day 5 started 2026-08-15T03:37:40Z. Target start: 2026-08-16T03:37:40Z (interval 5 = 1.000 d).
# A partial file is never a run.
TARGET=$(date -u -d '2026-08-16 03:37:40' +%s)
NOW=$(date -u +%s)
WAIT=$((TARGET - NOW))
if [ "$WAIT" -gt 0 ]; then
  echo "holding $WAIT s until 2026-08-16T03:37:40Z" >&2
  sleep "$WAIT"
fi
echo "start $(date -u +%Y-%m-%dT%H:%M:%SZ)" >&2
exec python3 ledger.py manifest-day2-onward.json ledger/run-2026-08-16T0337Z.json
