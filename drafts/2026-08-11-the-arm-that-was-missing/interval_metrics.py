#!/usr/bin/env python3
"""interval_metrics - one interval of the series, computed to a file rather than typed.

Session 127, 2026-08-19. This is `retry_metrics_126.py` with its three hard-coded paths and its
one hard-coded sentence lifted into arguments, and nothing else changed. The method is identical;
what it stops doing is requiring a new script per day.

WHY THIS EXISTS RATHER THAN A FOURTH COPY. `day7_metrics.py` hard-coded the string "seventh
consecutive daily run; completes the pre-registered window" and that sentence was false when it
was written (`ERRATA-126.md` E21). `retry_metrics_126.py` removed the hard-coded cadence claim
and replaced it with a read from `window_status.py`. Copying that file again for day 8 would put
a fourth near-identical script in this directory, each with its own paths to get wrong. So the
paths are arguments, the window position is read and never asserted, and the interval in days is
computed from the two run files' own start seconds.

WHAT IT REFUSES TO DO. It will not describe the series as consecutive or daily under any
circumstances. `window_status.py` decides what the series is, by counting non-partial run files;
this script only reports what that scan returned.

Usage:
    python3 interval_metrics.py <prev_run.json> <curr_run.json> <diff.json> <confirm.json> \\
        [-o out.json] [--overlay-diff path] [--record confirmation-record-121.json] [--note TEXT]

Offline. Reads committed files only, makes no request.
"""
import argparse
import calendar
import json
import os
import time

import window_status


def ts(s):
    return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("prev_run")
    ap.add_argument("curr_run")
    ap.add_argument("diff")
    ap.add_argument("confirm")
    ap.add_argument("-o", "--out", default="interval-metrics.json")
    ap.add_argument("--overlay-diff", default=None,
                    help="the --corrections diff of the same pair; defaults to "
                         "<diff basename>-overlay.json beside it")
    ap.add_argument("--record", default="confirmation-record-121.json")
    ap.add_argument("--note", default=None,
                    help="what this interval is, in one sentence, for a reader who has only "
                         "this file")
    a = ap.parse_args(argv)

    overlay = a.overlay_diff
    if overlay is None:
        stem, ext = os.path.splitext(a.diff)
        overlay = stem + "-overlay" + ext

    prev, curr = json.load(open(a.prev_run)), json.load(open(a.curr_run))
    diff = json.load(open(a.diff))
    over = json.load(open(overlay))
    conf = json.load(open(a.confirm))
    rec = json.load(open(a.record))

    interval_days = (ts(curr["run_utc_start"]) - ts(prev["run_utc_start"])) / 86400.0

    sp = {str(o["vid"]): o["state"] for o in prev["observations"]}
    sc = {str(o["vid"]): o["state"] for o in curr["observations"]}
    both = [v for v in sp if v in sc]
    ret_then_det_now = [v for v in both
                        if sp[v] == "RETRIEVABLE" and sc[v] != "INDETERMINATE"]
    abs_then_det_now = [v for v in both
                        if sp[v] == "NOT-RETRIEVABLE" and sc[v] != "INDETERMINATE"]

    confirmed = [r for r in conf["results"] if r["all_passes_agree_with_new_state"]]
    losses = [r for r in confirmed if r["to"] == "NOT-RETRIEVABLE"]
    returns = [r for r in confirmed if r["to"] == "RETRIEVABLE"]

    out = {
        "schema": "field-research/window-interval/1",
        "computed_by": "interval_metrics.py, session 127",
        "from_run": a.prev_run,
        "to_run": a.curr_run,
        "what_this_interval_is": a.note,
        "window_position": window_status.scan(),
        "window_position_note": (
            "read from window_status.py, which counts only non-partial run files. Whether this "
            "series is daily or consecutive is whatever that scan says and is never asserted "
            "here: see consecutive_daily and preregistered_window_met."
        ),
        "run": {
            "file": a.curr_run,
            "utc_start": curr["run_utc_start"],
            "utc_end": curr["run_utc_end"],
            "seconds": curr.get("seconds"),
            "planned": curr.get("planned"),
            "requested": curr.get("requested"),
            "stopped": curr.get("stopped"),
            "vantage_asn": curr["vantage"]["asn"],
            "complete": (curr.get("requested") == curr.get("planned")
                         and not curr.get("stopped")),
        },
        "interval_days": round(interval_days, 4),
        "vantage_guard": diff["vantage_guard"],
        "observed_in_both": diff["observed_in_both"],
        "determinate_in_both": diff["determinate_in_both"],
        "touching_indeterminate": diff["touching_indeterminate"],
        "apparent_transitions_raw": diff["n_transitions"],
        "apparent_transitions_overlay": over["n_transitions"],
        "overlay_rows_applied": over["corrections_applied"]["n"],
        "k4": conf["K4"],
        "confirmed_this_interval": {
            "returns": len(returns),
            "losses": len(losses),
            "vids": [{"vid": r["vid"], "from": r["from"], "to": r["to"]}
                     for r in confirmed],
        },
        "denominators_this_interval": {
            "retrievable_at_previous_day_and_determinate_now": len(ret_then_det_now),
            "absent_at_previous_day_and_determinate_now": len(abs_then_det_now),
        },
        "series_after_this_interval": {
            "all_readings": rec["all_readings"],
            "genuine_transitions_only": rec["genuine_transitions_only"],
            "n_artefact_echoes": rec["n_artefact_echoes"],
            "n_sidecars": len(rec["sources"]["sidecars"]),
        },
        "per_arm_counts": curr.get("counts"),
    }
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({k: out[k] for k in
                      ["from_run", "to_run", "interval_days", "apparent_transitions_raw", "k4",
                       "confirmed_this_interval", "denominators_this_interval",
                       "series_after_this_interval"]}, indent=1))
    print(json.dumps({k: out["window_position"][k] for k in
                      ["n_measurement_days", "n_completed_run_files", "n_holes",
                       "consecutive_daily", "preregistered_window_met"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
