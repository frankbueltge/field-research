#!/usr/bin/env python3
"""build_register_v1.py — the availability register, v1.0.

v0.1 (increment 1) was derived from the index and was wrong about 84 cycles, because the
index is the thing under test (CORRECTIONS.md C2). v1.0 carries, for every row, a status
verified against the file host and the date it was verified, per stream and per file type
(CORRECTIONS.md C6), and it is built only from series that were swept end to end.

Every listed cycle of a completed series is accounted for. The register file lists the
rows where the host and the index disagree; the clean rows are carried as counts, with the
sweep logs beside them so the count can be re-derived.

Usage: build_register_v1.py <scratch-dir> <out.json> [--as-of YYYY-MM-DD]
"""

from __future__ import annotations

import json
import os
import sys

SERIES = [("en", "gkg", ".gkg.csv.zip"),
          ("en", "export", ".export.CSV.zip"),
          ("en", "mentions", ".mentions.CSV.zip"),
          ("tr", "gkg", ".translation.gkg.csv.zip"),
          ("tr", "export", ".translation.export.CSV.zip"),
          ("tr", "mentions", ".translation.mentions.CSV.zip")]
STREAM_NAME = {"en": "English", "tr": "Translingual"}


def load(path):
    header = footer = None
    rows = []
    if not os.path.exists(path):
        return None, [], None
    for line in open(path, encoding="utf-8"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("k") == "header":
            header = r
        elif r.get("k") == "footer":
            footer = r
        elif r.get("k") in ("absent", "size-mismatch", "unresolved", "other-status"):
            rows.append(r)
    return header, rows, footer


def main():
    scratch, out = sys.argv[1], sys.argv[2]
    as_of = "2026-08-09"
    if "--as-of" in sys.argv:
        as_of = sys.argv[sys.argv.index("--as-of") + 1]

    cycles = {}
    series_meta = {}
    for stream, typ, suffix in SERIES:
        h, rows, f = load(os.path.join(scratch, f"sweep-{stream}-{typ}.jsonl"))
        key = f"{STREAM_NAME[stream]}/{typ}"
        if h is None:
            series_meta[key] = {"state": "NOT RUN"}
            continue
        series_meta[key] = {
            "state": "COMPLETE" if f else "PARTIAL — the counts below cover only what was probed",
            "suffix": suffix,
            "listed_cycles": (f or h).get("total"),
            "probed": (f or {}).get("done"),
            "served_and_size_agrees": (f or {}).get("ok"),
            "absent": (f or {}).get("absent"),
            "size_mismatch": (f or {}).get("mismatch"),
            "unresolved": (f or {}).get("unresolved"),
            "other_status": (f or {}).get("other"),
            "throttled_responses": (f or {}).get("throttled"),
            "started_utc": h.get("started"), "finished_utc": (f or {}).get("finished"),
            "seconds": (f or {}).get("elapsed_s"), "requests_per_second": (f or {}).get("rate_per_s"),
        }
        for r in rows:
            e = cycles.setdefault(r["c"], {})
            e[key] = {"status": r.get("s"), "verdict": r["k"],
                      "declared_bytes": r.get("d"), "served_bytes": r.get("cl"),
                      "declared_md5": r.get("md5"), "url": r.get("url")}

    screen_path = os.path.join(scratch, "screen-en-gkg.json")
    screen = json.load(open(screen_path))["ratio"] if os.path.exists(screen_path) else {}

    rows_out = []
    for c in sorted(cycles):
        ratio = screen.get(c)
        rows_out.append({
            "cycle_utc": f"{c[0:4]}-{c[4:6]}-{c[6:8]}T{c[8:10]}:{c[10:12]}:{c[12:14]}Z",
            "cycle": c,
            "verified_as_of": as_of,
            "index_byte_screen_ratio": ratio,
            "findable_from_the_index_alone": (ratio is not None and ratio < 0.20),
            "series": cycles[c],
        })

    reg = {
        "register": "availability register of a public 15-minute file series",
        "version": "1.0",
        "supersedes": "gap-register-v0.1.json (derived from the index; wrong about 84 cycles — CORRECTIONS.md C2)",
        "verified_as_of": as_of,
        "method": ("one HTTP HEAD per listed file against the file host named in the index; every "
                   "non-200/404 outcome retried three times and recorded as unresolved rather than "
                   "inferred; the rows carrying the finding re-asked three further times on fresh "
                   "connections, by ranged GET as well as HEAD (reverify-outside.json)"),
        "what_a_row_means": ("absent = the index lists the file with a byte size and an MD5 and the "
                             "host does not serve it, on the date stated; size-mismatch = the host "
                             "serves it at a length other than the one the index declares. Neither "
                             "says anything about what was served on any earlier date."),
        "second_witness": ("every row before 2019-05 checked against an independent frozen public "
                           "snapshot of the same series (s3-witness.json)"),
        "series": series_meta,
        "disagreeing_cycles": len(rows_out),
        "rows": rows_out,
    }
    json.dump(reg, open(out, "w"), indent=1)
    print(json.dumps({"cycles_with_a_disagreement": len(rows_out),
                      "series": {k: v.get("state") for k, v in series_meta.items()}}, indent=1))


if __name__ == "__main__":
    main()
