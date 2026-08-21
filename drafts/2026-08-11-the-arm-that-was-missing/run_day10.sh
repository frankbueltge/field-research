#!/bin/sh
# DAY 10 OF THE SERIES — the third run outside the pre-registered window. Session 129, 2026-08-21.
#
# The arc's delivery objects are stopped (`POST-MORTEM.md`, `CONDITIONS-128.md`). The stop is on
# building things to send, not on measuring: "a dark instrument is a finding to record, never a
# silence." This run is the instrument continuing under that clause and nothing else.
#
# The pre-registered window closed on 2026-08-18 and its status is computed, not claimed
# (`window-status-128.json`). Nothing here reopens it and no pre-registered test is scored on this
# run.
#
# Launched at 03:41:00Z, exactly 1.0000 days after the last completed run's start second
# (2026-08-20T03:41:00Z). A partial file is never a run: if this session ends before it closes,
# day 10 is a hole and this comment is not a substitute for the data.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-21T0341Z.json 2026-08-21T03:41:00Z
