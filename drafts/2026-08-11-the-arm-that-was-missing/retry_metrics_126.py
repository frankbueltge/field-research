#!/usr/bin/env python3
"""retry_metrics_126 - the interval of the day-7 RETRY, computed to a file rather than typed.

Session 126, 2026-08-18. Adapted from `day7_metrics.py` unchanged in METHOD and changed in exactly
two ways, both because the record it feeds must not repeat erratum E21:

1. **The paths.** Day 7 as launched on 2026-08-17 does not exist; it stopped at 600 of 3,869 and
   only a `.partial` remains. This measures the retry launched 2026-08-18T03:41:00Z against the
   last COMPLETED day, 2026-08-16 - so the interval it computes is a TWO-DAY interval and the
   script says so rather than leaving a reader to divide.
2. **`window_position` no longer claims a cadence.** `day7_metrics.py` hard-coded the string
   "seventh consecutive daily run; completes the pre-registered window". That sentence was written
   before the run it described had finished, and it was false. This one reports the window's state
   by reading `window_status.py`, which counts only non-partial run files, and it refuses to
   describe the series as consecutive or daily under any circumstances.

The day-6 side uses the CANONICAL run file, not the second probe of that date (DOUBLE-PROBE-122.md).
Every figure the record quotes about this interval comes from here.
"""
import calendar
import json
import time

import window_status

D5 = "ledger/run-2026-08-16T0337Z.json"      # the last COMPLETED day, canonical run
D6 = "ledger/run-2026-08-18T0341Z.json"      # the retry
DIFF = "ledger/diff-day6-retry.json"
CONFIRM = "ledger/transition-confirm-2026-08-18.json"
RECORD = "confirmation-record-121.json"


def ts(s):
    return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))


d5, d6 = json.load(open(D5)), json.load(open(D6))
diff = json.load(open(DIFF))
conf = json.load(open(CONFIRM))
rec = json.load(open(RECORD))

interval_days = (ts(d6["run_utc_start"]) - ts(d5["run_utc_start"])) / 86400.0

# The denominators the interval's own rates are taken over, computed from the two run files.
s5 = {str(o["vid"]): o["state"] for o in d5["observations"]}
s6 = {str(o["vid"]): o["state"] for o in d6["observations"]}
both = [v for v in s5 if v in s6]
ret_at_5_det_at_6 = [v for v in both if s5[v] == "RETRIEVABLE" and s6[v] != "INDETERMINATE"]
abs_at_5_det_at_6 = [v for v in both if s5[v] == "NOT-RETRIEVABLE" and s6[v] != "INDETERMINATE"]

confirmed = [r for r in conf["results"] if r["all_passes_agree_with_new_state"]]
losses = [r for r in confirmed if r["to"] == "NOT-RETRIEVABLE"]
returns = [r for r in confirmed if r["to"] == "RETRIEVABLE"]

out = {
    "schema": "field-research/window-interval/1",
    "computed_by": "retry_metrics_126.py, session 126",
    "interval": 6,
    "interval_is_two_days_not_one": True,
    "what_this_interval_is": (
        "the gap from the last COMPLETED measurement day (2026-08-16) to the retry of 2026-08-18. "
        "The run launched on 2026-08-17 stopped at 600 of 3,869 units and is not a measurement "
        "(ERRATA-126.md, E21), so no one-day interval exists across this gap and none is reported."
    ),
    "window_position": window_status.scan(),
    "window_position_note": (
        "read from window_status.py, which counts only non-partial run files. This series is NOT "
        "seven consecutive daily runs and must never be described as such: see "
        "preregistered_window_met, which is false on both of its conjuncts."
    ),
    "run": {
        "file": D6,
        "utc_start": d6["run_utc_start"],
        "utc_end": d6["run_utc_end"],
        "seconds": d6.get("seconds"),
        "planned": d6.get("planned"),
        "requested": d6.get("requested"),
        "stopped": d6.get("stopped"),
        "vantage_asn": d6["vantage"]["asn"],
        "complete": d6.get("requested") == d6.get("planned") and not d6.get("stopped"),
    },
    "interval_days": round(interval_days, 4),
    "vantage_guard": diff["vantage_guard"],
    "observed_in_both": diff["observed_in_both"],
    "determinate_in_both": diff["determinate_in_both"],
    "touching_indeterminate": diff["touching_indeterminate"],
    "apparent_transitions_raw": diff["n_transitions"],
    "apparent_transitions_overlay": json.load(
        open("ledger/diff-day6-retry-overlay.json"))["n_transitions"],
    "overlay_rows_applied": json.load(
        open("ledger/diff-day6-retry-overlay.json"))["corrections_applied"]["n"],
    "k4": conf["K4"],
    "confirmed_this_interval": {
        "returns": len(returns),
        "losses": len(losses),
        "vids": [{"vid": r["vid"], "from": r["from"], "to": r["to"]} for r in confirmed],
    },
    "denominators_this_interval": {
        "retrievable_at_2026_08_16_and_determinate_at_retry": len(ret_at_5_det_at_6),
        "absent_at_2026_08_16_and_determinate_at_retry": len(abs_at_5_det_at_6),
    },
    "series_after_this_interval": {
        "all_readings": rec["all_readings"],
        "genuine_transitions_only": rec["genuine_transitions_only"],
        "n_artefact_echoes": rec["n_artefact_echoes"],
        "n_sidecars": len(rec["sources"]["sidecars"]),
    },
    "per_arm_counts_retry": d6.get("counts"),
}
json.dump(out, open("retry-metrics-126.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in
                  ["interval_days", "interval_is_two_days_not_one", "apparent_transitions_raw",
                   "k4", "confirmed_this_interval", "denominators_this_interval",
                   "series_after_this_interval"]}, indent=1))
print(json.dumps({k: out["window_position"][k] for k in
                  ["n_measurement_days", "n_completed_run_files", "n_holes",
                   "consecutive_daily", "preregistered_window_met"]}, indent=1))
