#!/usr/bin/env python3
"""day6_metrics - the day-6 interval, computed to a file rather than typed into prose.

Session 123, 2026-08-16. Same shape as `day5_metrics.py`. Every figure the journal entry and the
day-6 record quote comes from here.
"""
import calendar
import json
import time

D5 = "ledger/run-2026-08-15T0337Z.json"
D6 = "ledger/run-2026-08-16T0337Z.json"
DIFF = "ledger/diff-day5-day6.json"
CONFIRM = "ledger/transition-confirm-2026-08-16.json"
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
    "computed_by": "day6_metrics.py, session 123",
    "interval": 5,
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
        open("ledger/diff-day5-day6-overlay.json"))["n_transitions"],
    "overlay_rows_applied": json.load(
        open("ledger/diff-day5-day6-overlay.json"))["corrections_applied"]["n"],
    "k4": conf["K4"],
    "confirmed_this_interval": {
        "returns": len(returns),
        "losses": len(losses),
        "vids": [{"vid": r["vid"], "from": r["from"], "to": r["to"]} for r in confirmed],
    },
    "denominators_this_interval": {
        "retrievable_at_day5_and_determinate_at_day6": len(ret_at_5_det_at_6),
        "absent_at_day5_and_determinate_at_day6": len(abs_at_5_det_at_6),
    },
    "series_after_this_interval": {
        "all_readings": rec["all_readings"],
        "genuine_transitions_only": rec["genuine_transitions_only"],
        "n_artefact_echoes": rec["n_artefact_echoes"],
        "n_sidecars": len(rec["sources"]["sidecars"]),
    },
    "per_arm_counts_day6": d6.get("counts"),
}
json.dump(out, open("day6-metrics.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in
                  ["interval_days", "apparent_transitions_raw", "k4",
                   "confirmed_this_interval", "denominators_this_interval",
                   "series_after_this_interval"]}, indent=1))
