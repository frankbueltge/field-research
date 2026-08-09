#!/usr/bin/env python3
"""census.py — completeness census of GDELT's own 15-minute file series.

Reads GDELT's published manifest (`masterfilelist.txt`) and asks one question:
for every quarter-hour the instrument claims to run on, is there a published record?

The manifest is GDELT's self-report. This script treats it as a *claim*, not as truth;
the probe controls (C-A, C-B) that check it against the host live in `probe.py`.

Specified in PREREGISTRATION-1.md before this file existed. Nothing here was tuned
after seeing a number.

Usage:  python3 census.py <path-to-masterfilelist.txt> <output-dir>
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

STEP = timedelta(minutes=15)
TYPES = ("export", "mentions", "gkg")
TRAILING_WINDOW = 672          # complete cycles (pre-registered). NOTE, added 2026-08-08 after the
                               # adversary's objection 7(i): 672 COMPLETE cycles equals seven days only
                               # where the series is complete; across gap-heavy stretches the window
                               # spans more than a week. It is a trailing window of 672 published
                               # cycles, and calling it "seven days" was wrong.
COLLAPSE_FRACTION = 0.20       # pre-registered threshold


def parse(path):
    """-> rows, malformed, offgrid, duplicates.

    rows: {timestamp: {type: (size, md5)}}
    """
    rows = defaultdict(dict)
    malformed, offgrid = [], []
    seen_urls = Counter()
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 3:
                malformed.append({"line": lineno, "text": line[:200], "why": "field count"})
                continue
            size_s, md5, url = parts
            try:
                size = int(size_s)
            except ValueError:
                malformed.append({"line": lineno, "text": line[:200], "why": "size not an integer"})
                continue
            if len(md5) != 32 or any(c not in "0123456789abcdefABCDEF" for c in md5):
                malformed.append({"line": lineno, "text": line[:200], "why": "md5 not 32 hex chars"})
                continue
            fname = url.rsplit("/", 1)[-1]
            stamp = fname[:14]
            if len(stamp) != 14 or not stamp.isdigit():
                malformed.append({"line": lineno, "text": line[:200], "why": "no 14-digit timestamp"})
                continue
            rest = fname[14:].lower()
            # The Translingual stream names its files `<stamp>.translation.<type>.…`.
            # Added 2026-08-08 when the second stream was censused; it changes which files
            # are recognised, never which are counted as missing.
            if rest.startswith(".translation"):
                rest = rest[len(".translation"):]
            ftype = next((t for t in TYPES if rest.startswith("." + t)), None)
            if ftype is None:
                malformed.append({"line": lineno, "text": line[:200], "why": "unknown file type"})
                continue
            try:
                ts = datetime.strptime(stamp, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
            except ValueError:
                malformed.append({"line": lineno, "text": line[:200], "why": "impossible timestamp"})
                continue
            seen_urls[url] += 1
            if ts.minute % 15 or ts.second:
                offgrid.append({"line": lineno, "url": url})
            rows[ts][ftype] = (size, md5)
    duplicates = {u: n for u, n in seen_urls.items() if n > 1}
    return rows, malformed, offgrid, duplicates


def main():
    manifest, outdir = sys.argv[1], sys.argv[2]
    rows, malformed, offgrid, duplicates = parse(manifest)

    on_grid = sorted(ts for ts in rows if ts.minute % 15 == 0 and ts.second == 0)
    first, last = on_grid[0], on_grid[-1]

    expected, present, partial, missing = [], [], [], []
    complete_seq = []           # (ts, gkg_size) in grid order, complete cycles only
    ts = first
    while ts <= last:
        expected.append(ts)
        have = rows.get(ts, {})
        n = sum(1 for t in TYPES if t in have)
        if n == 3:
            present.append(ts)
            complete_seq.append((ts, have["gkg"][0]))
        elif n == 0:
            missing.append(ts)
        else:
            partial.append({"ts": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "have": sorted(have.keys())})
        ts += STEP

    # gap runs
    gaps, run = [], []
    missing_set = set(missing)
    for t in expected:
        if t in missing_set:
            run.append(t)
        elif run:
            gaps.append(run)
            run = []
    if run:
        gaps.append(run)
    gap_records = sorted(
        ({"start": g[0].strftime("%Y-%m-%dT%H:%M:%SZ"),
          "end": g[-1].strftime("%Y-%m-%dT%H:%M:%SZ"),
          "cycles": len(g),
          "hours": round(len(g) * 0.25, 2)} for g in gaps),
        key=lambda r: -r["cycles"])

    # volume collapse on the gkg arm, trailing median over complete cycles
    collapsed, excluded = [], 0
    sizes = [s for _, s in complete_seq]
    for i, (t, s) in enumerate(complete_seq):
        if i < TRAILING_WINDOW:
            excluded += 1
            continue
        med = statistics.median(sizes[i - TRAILING_WINDOW:i])
        if med > 0 and s < COLLAPSE_FRACTION * med:
            collapsed.append({"ts": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "gkg_bytes": s,
                              "trailing_median": med, "ratio": round(s / med, 4)})

    zero_byte = [{"ts": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "type": ty}
                 for t, d in rows.items() for ty, (sz, _) in d.items() if sz == 0]

    # by-year table
    by_year = defaultdict(lambda: {"expected": 0, "missing": 0, "partial": 0, "collapsed": 0})
    for t in expected:
        by_year[t.year]["expected"] += 1
    for t in missing:
        by_year[t.year]["missing"] += 1
    for p in partial:
        by_year[int(p["ts"][:4])]["partial"] += 1
    for c in collapsed:
        by_year[int(c["ts"][:4])]["collapsed"] += 1

    # pre-registered scoring windows
    first_third_end = first + (last - first) / 3
    missing_first_third = sum(1 for t in missing if t <= first_third_end)
    last_365_start = last - timedelta(days=365)
    missing_last_365 = sum(1 for t in missing if t >= last_365_start)
    collapsed_last_365 = sum(1 for c in collapsed
                             if datetime.strptime(c["ts"], "%Y-%m-%dT%H:%M:%SZ")
                             .replace(tzinfo=timezone.utc) >= last_365_start)

    result = {
        "manifest": manifest,
        "first_cycle": first.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_cycle": last.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expected_cycles": len(expected),
        "complete_cycles": len(present),
        "partial_cycles": len(partial),
        "missing_cycles": len(missing),
        "missing_pct": round(100 * len(missing) / len(expected), 4),
        "gap_runs": len(gap_records),
        "longest_gap": gap_records[0] if gap_records else None,
        "gap_runs_ge_96": sum(1 for g in gap_records if g["cycles"] >= 96),
        "top_gaps": gap_records[:25],
        "gap_length_histogram": dict(sorted(Counter(g["cycles"] for g in gap_records).items())),
        "collapsed_cycles": len(collapsed),
        "collapse_excluded_no_window": excluded,
        "worst_collapses": sorted(collapsed, key=lambda c: c["ratio"])[:15],
        "offgrid_entries": len(offgrid),
        "offgrid_sample": offgrid[:20],
        "duplicate_urls": len(duplicates),
        "malformed_lines": len(malformed),
        "malformed_sample": malformed[:20],
        "zero_byte_manifest_entries": len(zero_byte),
        "_zero_byte_note": ("counts entries whose MANIFEST-DECLARED size is 0. It is not a test of the "
                            "inner file: nine English entries declare 194 bytes and contain a zero-byte "
                            "CSV. Renamed 2026-08-08 after the adversary's objection 7(ii)."),
        "first_third_boundary": first_third_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "missing_in_first_third": missing_first_third,
        "missing_in_last_365d": missing_last_365,
        "collapsed_in_last_365d": collapsed_last_365,
        "by_year": {str(y): v for y, v in sorted(by_year.items())},
    }

    with open(f"{outdir}/census.json", "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
    with open(f"{outdir}/gaps.json", "w", encoding="utf-8") as fh:
        json.dump({"gap_runs": gap_records, "partial_cycles": partial}, fh, indent=1)
    with open(f"{outdir}/collapses.json", "w", encoding="utf-8") as fh:
        json.dump({"collapsed_cycles": collapsed}, fh, indent=1)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("top_gaps", "worst_collapses", "gap_length_histogram",
                                   "offgrid_sample", "malformed_sample", "by_year")}, indent=1))


if __name__ == "__main__":
    main()
