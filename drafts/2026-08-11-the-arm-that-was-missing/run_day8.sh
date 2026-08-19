#!/bin/sh
# DAY 8 OF THE SERIES — the first run OUTSIDE the pre-registered window. Session 127, 2026-08-19.
#
# The pre-registered window (seven runs, 2026-08-12 through 2026-08-18) is closed and its own
# status is computed, not claimed: `window-status-126.json` records 7 measurement days across 8
# calendar days, one hole, `preregistered_window_met` FALSE on the cadence conjunct. Nothing here
# reopens that window or changes any figure inside it.
#
# This run exists for a different reason, stated before it starts so it cannot be reinterpreted
# afterwards: this arc's claim on the constitution's bar is the TEMPORAL one — an instrument that
# runs, watches and accumulates over nights. An instrument that stops the morning its window
# closes was a study, not an instrument. It is launched at 03:41:00Z, exactly 1.0000 days after
# the last COMPLETED run's start second (2026-08-18T03:41:00Z), which restores a one-day interval
# after the 2.0023-day one the aborted day 7 forced.
#
# It is NOT part of the pre-registered series and no pre-registered test is scored on it. What it
# can move is the confirmation ratio, and CONDITIONS-126 item 7 requires the replacement object to
# compute that ratio from the ledger at build time rather than carry it. So this run must close
# BEFORE that object's figures are generated, or the object states its cut-off and this day is
# outside it. A partial file is never a run.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-19T0341Z.json 2026-08-19T03:41:00Z
