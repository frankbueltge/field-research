#!/bin/sh
# Wait for the day-13 probe (pid passed in) to exit, then run the close pipeline.
# Session 135, 2026-08-25. Written so the close is not improvised and not forgotten.
PID=$1
while kill -0 "$PID" 2>/dev/null; do sleep 20; done
echo "probe pid $PID exited at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ -f ledger/run-2026-08-25T0341Z.json ]; then
  echo "run file present; running close pipeline"
  sh run_day13-2026-08-25_close.sh
  echo "close pipeline exit: $?"
else
  echo "NO RUN FILE - day 13 is a hole for the second time. A partial is never a run."
  ls -la ledger/ | grep 2026-08-25
fi
