#!/bin/sh
# Session 138, 2026-08-29. A day that closes on disk but never reaches the record is the same loss
# as a day that never ran. The detached close waiter (await_and_close_day16.sh) guarantees the
# pipeline runs even if this session dies; this guarantees its output is committed and pushed.
# It waits for the pipeline's last artifact, then commits the ledger and metrics on the session
# branch. If the session is still alive and has already committed them, `git commit` finds nothing
# staged and exits non-zero, which is the correct no-op.
cd /home/user/field-research || exit 1
i=0
while [ ! -f drafts/2026-08-11-the-arm-that-was-missing/interval-metrics-138.json ]; do
  i=$((i+1)); [ "$i" -gt 900 ] && { echo "gave up waiting after ~4h"; exit 1; }
  sleep 15
done
sleep 20   # let the pipeline finish writing every file
n=0
while [ "$n" -lt 5 ]; do
  git add -A drafts/2026-08-11-the-arm-that-was-missing/ 2>/dev/null
  if git commit -q -m "Day 16 of the series closed and landed by the orphan guard" 2>/dev/null; then
    git push -q origin research/session-2026-08-29 && { echo "pushed $(date -u)"; exit 0; }
  else
    echo "nothing to commit - the session landed it already $(date -u)"; exit 0
  fi
  n=$((n+1)); sleep 10
done
echo "push failed after retries"; exit 1
