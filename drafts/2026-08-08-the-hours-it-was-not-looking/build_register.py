#!/usr/bin/env python3
"""build_register.py — emit the artifact a downstream user can actually consume.

A dated register of the quarter-hours in which GDELT's public file series published
nothing, per stream, in a form a pipeline can read and mask against. Every window
carries how it was established, so a user can tell a manifest omission that was probed
against the host from one that was not.

Usage: python3 build_register.py <out.json>
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone

STREAMS = {
    "english": {"dir": ".", "manifest": "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"},
    "translingual": {"dir": "translingual",
                     "manifest": "http://data.gdeltproject.org/gdeltv2/masterfilelist-translation.txt"},
}
MIN_CYCLES = 4          # publish windows of one hour or longer; shorter runs stay in gaps.json


def main():
    out = sys.argv[1]
    probes = json.load(open("probes.json"))
    verified_window = probes["C_C"]["window"]

    register = {
        "register": "gdelt-publication-gaps",
        "version": "0.1",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "DRAFT — not shipped, not verified by this practice's gauntlet",
        "what_this_is": (
            "Quarter-hour windows in which GDELT's public 15-minute file series published no "
            "file at all, derived from GDELT's own published manifests. A window listed here "
            "means the manifest lists none of the cycle's files; where 'host_probed' is true, "
            "the absence was additionally confirmed against the file host itself."),
        "what_this_is_not": (
            "Not a claim about GDELT's collection pipeline, and not a claim about content. A "
            "cycle absent here was not published; a cycle absent from this register may still "
            "have been published empty or degraded (see 'collapsed_cycles')."),
        "cadence_source": "https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/",
        "min_window_cycles": MIN_CYCLES,
        "streams": {},
    }

    for name, cfg in STREAMS.items():
        census = json.load(open(f"{cfg['dir']}/census.json"))
        gaps = json.load(open(f"{cfg['dir']}/gaps.json"))
        windows = []
        for g in gaps["gap_runs"]:
            if g["cycles"] < MIN_CYCLES:
                continue
            probed = (name == "english"
                      and g["start"] == verified_window["start"]
                      and g["cycles"] == verified_window["cycles"])
            windows.append({**g, "host_probed": probed,
                            "host_probe_result": (
                                f"{probes['C_C']['absent']}/{probes['C_C']['n']} cycles "
                                f"returned not-found; 0 probe failures" if probed else None)})
        # `clock_aligned`, added 2026-08-08 after the adversary's objection 1: a window whose
        # resume minute-of-day is shared by five or more windows in the same stream looks
        # scheduled, not accidental, and a consumer must be able to tell the two apart.
        resume_counts = {}
        for w in windows:
            end = datetime.strptime(w["end"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(minutes=15)
            w["resume_utc"] = end.strftime("%Y-%m-%dT%H:%M:%SZ")
            w["resume_time_of_day"] = end.strftime("%H:%M")
            resume_counts[w["resume_time_of_day"]] = resume_counts.get(w["resume_time_of_day"], 0) + 1
        for w in windows:
            w["clock_aligned"] = resume_counts[w["resume_time_of_day"]] >= 5
        windows.sort(key=lambda w: w["start"])
        collapsed = json.load(open(f"{cfg['dir']}/collapses.json"))["collapsed_cycles"]
        register["streams"][name] = {
            "manifest": cfg["manifest"],
            "first_cycle": census["first_cycle"],
            "last_cycle": census["last_cycle"],
            "expected_cycles": census["expected_cycles"],
            "missing_cycles": census["missing_cycles"],
            "missing_pct": census["missing_pct"],
            "gap_runs_total": census["gap_runs"],
            "windows_ge_1h": len(windows),
            "windows_clock_aligned": sum(1 for w in windows if w["clock_aligned"]),
            "windows": windows,
            "collapsed_cycles_count": len(collapsed),
            "collapsed_cycles": collapsed,
        }

    json.dump(register, open(out, "w"), indent=1)
    for n, s in register["streams"].items():
        print(n, s["windows_ge_1h"], "windows >= 1h;", s["missing_cycles"], "missing cycles;",
              s["collapsed_cycles_count"], "collapsed")


if __name__ == "__main__":
    main()
