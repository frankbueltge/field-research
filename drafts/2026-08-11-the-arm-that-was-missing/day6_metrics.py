#!/usr/bin/env python3
"""Interval 5 of the pre-registered window, computed to a file (session 122, 2026-08-16).

The same shape as `day5_metrics.py`, and written for the same reason this session's own erratum E1
gave: a figure quoted in prose that lives only in a shell one-liner cannot be re-checked. Every
number in `DAY6-2026-08-16.md` comes from here.

The panel is the OVERLAY-CORRECTED one (`ledger/corrections.json`, per
`PREREGISTRATION-119-overlay-use.md`); the raw diff stays primary and is published beside it.
Exclusions, unchanged: arm `B-truncated` is not videos; either day INDETERMINATE drops the pair.

    python3 day6_metrics.py [--out day6-metrics.json]

No request leaves the machine: this is arithmetic over run files already on disk.
"""
import argparse
import calendar
import json
import time

import power_audit as pa

DAY5 = "ledger/run-2026-08-15T0337Z.json"
DAY6 = "ledger/run-2026-08-16T0337Z.json"
CORRECTIONS = "ledger/corrections.json"


def t(s):
    return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))


def states(path, overlay):
    run = json.load(open(path))
    out = {}
    for o in run["observations"]:
        vid, st = str(o["vid"]), o["state"]
        c = overlay.get((path, vid))
        if c and st == c["state_in_run_file"]:
            st = c["corrected_state"]
        out[vid] = (st, o["arm"])
    return run, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="day6-metrics.json")
    a = ap.parse_args()

    corr = json.load(open(CORRECTIONS))
    overlay = {(c["run_file"], str(c["vid"])): c for c in corr["corrections"]}
    r5, s5 = states(DAY5, overlay)
    r6, s6 = states(DAY6, overlay)

    ret_base = loss = abs_base = ret = 0
    movers = []
    for vid in set(s5) & set(s6):
        a5, arm = s5[vid]
        a6, _ = s6[vid]
        if arm == "B-truncated" or "INDETERMINATE" in (a5, a6):
            continue
        if a5 == "RETRIEVABLE":
            ret_base += 1
            if a6 == "NOT-RETRIEVABLE":
                loss += 1
                movers.append({"vid": vid, "from": a5, "to": a6, "arm": arm})
        elif a5 == "NOT-RETRIEVABLE":
            abs_base += 1
            if a6 == "RETRIEVABLE":
                ret += 1
                movers.append({"vid": vid, "from": a5, "to": a6, "arm": arm})

    rlo, rhi = pa.wilson(ret, abs_base)
    llo, lhi = pa.wilson(loss, ret_base)
    interval = (t(r6["run_utc_start"]) - t(r5["run_utc_start"])) / 86400.0

    out = {
        "schema": "field-research/window-interval/1",
        "written_by": "day6_metrics.py, session 122, 2026-08-16",
        "interval": 5,
        "run": {"file": DAY6, "run_utc_start": r6["run_utc_start"],
                "run_utc_end": r6["run_utc_end"], "seconds": r6["seconds"],
                "requested": r6["requested"], "planned": r6["planned"],
                "stopped": r6["stopped"], "vantage_asn": r6["vantage"]["asn"],
                "vantage_country": r6["vantage"]["country"],
                "probe_identical_to_day5": r6["probe"] == r5["probe"]},
        "interval_days": interval,
        "previous_run": {"file": DAY5, "run_utc_start": r5["run_utc_start"]},
        "arm": "overlay-corrected; the raw diff is the primary record and is published beside it",
        "retrievable_at_day5_and_determinate_at_day6": ret_base,
        "confirmed_losses": loss,
        "absent_at_day5_and_determinate_at_day6": abs_base,
        "confirmed_returns": ret,
        "return_rate": None if not abs_base else ret / abs_base,
        "return_rate_wilson": [rlo, rhi],
        "loss_rate": None if not ret_base else loss / ret_base,
        "loss_rate_wilson": [llo, lhi],
        "movers": movers,
        "the_intervals_travel_unwidened": (
            "these Wilson brackets take the video as the independent unit. Losses in this corpus "
            "clump by cited account and every proportion this arc publishes takes the crossed "
            "design effect (1.9900, session 116); condition 7 of memory/downstream-commitments.md "
            "governs any reuse. Six confirmed events across five intervals is not a rate and this "
            "practice does not turn it into one."),
    }
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({k: out[k] for k in (
        "interval_days", "retrievable_at_day5_and_determinate_at_day6", "confirmed_losses",
        "absent_at_day5_and_determinate_at_day6", "confirmed_returns")}, indent=1))


if __name__ == "__main__":
    main()
