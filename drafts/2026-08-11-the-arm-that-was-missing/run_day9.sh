#!/bin/sh
# DAY 9 OF THE SERIES — the second run outside the pre-registered window. Session 128, 2026-08-20.
#
# The pre-registered window closed on 2026-08-18 and its status is computed, not claimed
# (`window-status-127.json`). Nothing here reopens it and no pre-registered test is scored on this
# run. It exists for the reason day 8 gave: this arc's claim on the constitution's bar is the
# TEMPORAL one, and an instrument that stops the morning its window closes was a study.
#
# Launched at 03:41:00Z, exactly 1.0000 days after the last completed run's start second
# (2026-08-19T03:41:00Z). A partial file is never a run: if this session ends before it closes,
# day 9 is a hole and this comment is not a substitute for the data.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-20T0341Z.json 2026-08-20T03:41:00Z
