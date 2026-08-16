#!/usr/bin/env python3
"""dashboard_read_123 - read the receiver's own public dashboard off its saved bytes.

Session 123, 2026-08-16.

The covering letter of this bundle quotes the receiver's dashboard: what it says it tracks, what
it reports, and its own note that the errors it shows are problems on its end rather than the
platform's. Those are load-bearing quotations about a named third party, so they are extracted
from the saved page by rule rather than copied by eye, and the saved page is committed beside the
result.

The page is fetched over HTTP by the session; this script never fetches. It reads
`receiver-dashboard-<date>.html` and writes `receiver-dashboard-<date>.json` with the figures and
the exact strings they were read from. If a pattern does not match, the field is `null` and the
absence is reported - never filled in from an earlier reading.

Usage:  python3 dashboard_read_123.py receiver-dashboard-2026-08-16.html
"""
import hashlib
import json
import os
import re
import sys

PATTERNS = {
    "generated_utc_declared": r"Dashboard generated on:\s*([0-9]{4}-[0-9]{2}-[0-9]{2}[ T][0-9:]{8})",
    "total_videos_tracked": r"([0-9,]+)\s*(?:</[^>]+>\s*)*[^<]*Total Videos Tracked",
    "available": r"([0-9,]+)\s*(?:</[^>]+>\s*)*[^<]*Available",
    "unavailable": r"([0-9,]+)\s*(?:</[^>]+>\s*)*[^<]*Unavailable",
    "errors": r"([0-9,]+)\s*(?:</[^>]+>\s*)*[^<]*(?:Videos with )?Errors?",
    # Terminated at the first full stop. Without it the match runs past the sentence into the
    # page's inline scripts, which is what the first run of this reader did - a quotation about a
    # named third party must end where their sentence ends.
    "error_note": r"(Note:\s*Error[^.<]{0,160}\.)",
}

# The counters are rendered as a label under a number, so a label-first regex would match the
# wrong cell. This is the label order the page uses; the reader takes the labels in order and
# pairs each with the nearest preceding number, then reports both the pairing and the raw window
# it was read from, so a reviewer can check the pairing rather than trust it.
LABELS = ["Total Videos Tracked", "Available", "Unavailable", "Errors"]


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)


def main(argv):
    path = argv[0]
    raw = open(path, "rb").read()
    text = raw.decode("utf-8", "replace")
    flat = re.sub(r"\s+", " ", strip_tags(text))

    out = {
        "schema": "field-research/receiver-dashboard-read/1",
        "source_file": os.path.basename(path),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source_bytes": len(raw),
        "url": "https://playground.tiktok-audit.com/api-na/",
        "what_this_is": ("the receiver's own public dashboard, read off saved bytes. Every figure "
                         "here is a claim the dashboard makes about itself, never a measurement "
                         "by this practice."),
        "fields": {},
    }

    m = re.search(PATTERNS["generated_utc_declared"], flat)
    out["fields"]["generated_declared"] = {
        "value": m.group(1) if m else None,
        "read_from": m.group(0) if m else None,
        "note": "the dashboard's own words; no timezone is stated on the page and none is assumed",
    }

    for label in LABELS:
        i = flat.find(label)
        if i < 0:
            out["fields"][label] = {"value": None, "read_from": None,
                                    "note": "label not present in the saved page"}
            continue
        window = flat[max(0, i - 80):i + len(label)]
        nums = re.findall(r"(?<![\w.])([0-9][0-9,]*)(?![\w.])", window)
        out["fields"][label] = {
            "value": int(nums[-1].replace(",", "")) if nums else None,
            "read_from": window.strip(),
            "note": "the nearest number preceding the label; the window is printed so the "
                    "pairing can be checked rather than trusted",
        }

    m = re.search(PATTERNS["error_note"], flat)
    out["fields"]["error_note"] = {
        "value": m.group(1).strip() if m else None,
        "read_from": m.group(0).strip() if m else None,
        "note": "the dashboard's own statement about what its Error count means",
    }

    outp = path.rsplit(".", 1)[0] + ".json"
    json.dump(out, open(outp, "w"), indent=1)
    print(json.dumps({k: v["value"] for k, v in out["fields"].items()}, indent=1))
    print("->", outp)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
