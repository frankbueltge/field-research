#!/bin/sh
# THE DAY-7 RETRY. Session 126, 2026-08-18.
#
# Day 7 was launched by session 125 at 2026-08-17T03:41:00Z and DID NOT COMPLETE: the session
# ended with 600 of 3,869 units measured, and `ledger/run-2026-08-17T0337Z.json.partial` is all
# that exists of it. A partial file is never a run. The record written last night states the
# window reached seven consecutive daily runs; it did not, and that is corrected in this
# session's own record rather than smoothed.
#
# This run takes the same manifest and the same probe, unchanged, at 03:41:00Z today — exactly
# 1.0000 days after the aborted attempt's start second, and 2.0023 days after day 6's completed
# run (2026-08-16T03:37:40Z). Both intervals are stated because only the second one is the
# series interval, and it is a TWO-DAY interval: the "consecutive daily" property of the
# pre-registered design is broken and no arithmetic here restores it.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-18T0341Z.json 2026-08-18T03:41:00Z
