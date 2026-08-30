#!/bin/sh
# Session 139, 2026-08-30. A day that closes on disk but never reaches the record is the same loss
# as a day that never ran. The detached close waiter (await_and_close_day17.sh) guarantees the
# pipeline runs even if this session dies; this guarantees its output is committed and pushed.
cd /home/user/field-research || exit 1
i=0
while [ ! -f drafts/2026-08-11-the-arm-that-was-missing/interval-metrics-139.json ]; do
  i=$((i+1)); [ "$i" -gt 900 ] && { echo "gave up waiting after ~4h"; exit 1; }
  sleep 15
done
sleep 20   # let the pipeline finish writing every file
n=0
while [ "$n" -lt 5 ]; do
  git add -A drafts/2026-08-11-the-arm-that-was-missing/ 2>/dev/null
  if git commit -q -m "Day 17 of the series closed and landed by the orphan guard" 2>/dev/null; then
    git push -q origin research/session-2026-08-30 && { echo "pushed $(date -u)"; exit 0; }
  else
    echo "nothing to commit - the session landed it already $(date -u)"; exit 0
  fi
  n=$((n+1)); sleep 10
done
echo "push failed after retries"; exit 1
