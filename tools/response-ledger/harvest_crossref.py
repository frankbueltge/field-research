#!/usr/bin/env python3
"""Harvest every expression-of-concern and retraction notice known to the
Crossref REST API, keeping only the fields the response clock needs.

Each notice record carries an `update-to` list: the works it acts on, with the
type of action and the date the publisher assigned to it. That is the raw
material of a flag-to-response measurement, and it is public. This script only
downloads it; `ledger.py` computes.

Usage:  python3 harvest_crossref.py <out-dir>
Writes: crossref-eoc.jsonl, crossref-retraction.jsonl (one notice per line).
"""
import json
import sys
import time
import urllib.parse
import urllib.request

MAILTO = "meridian@field-research.invalid"
BASE = "https://api.crossref.org/works"
ROWS = 1000


def fetch(update_type, out_path):
    cursor = "*"
    seen = 0
    with open(out_path, "w", encoding="utf-8") as fh:
        while True:
            q = urllib.parse.urlencode({
                "filter": f"update-type:{update_type}",
                "rows": ROWS,
                "cursor": cursor,
                "select": "DOI,update-to",
                "mailto": MAILTO,
            })
            url = f"{BASE}?{q}"
            for attempt in range(5):
                try:
                    with urllib.request.urlopen(url, timeout=120) as r:
                        msg = json.load(r)["message"]
                    break
                except Exception as exc:  # network or rate limit
                    if attempt == 4:
                        raise
                    print(f"  retry {attempt + 1} after {exc}", file=sys.stderr)
                    time.sleep(2 ** attempt)
            items = msg.get("items", [])
            if not items:
                break
            for it in items:
                fh.write(json.dumps(it, ensure_ascii=False) + "\n")
            seen += len(items)
            cursor = msg.get("next-cursor")
            print(f"  {update_type}: {seen}", file=sys.stderr)
            if not cursor or len(items) < ROWS:
                break
    return seen


def main():
    out = sys.argv[1].rstrip("/")
    for t, name in (("expression_of_concern", "crossref-eoc.jsonl"),
                    ("retraction", "crossref-retraction.jsonl")):
        n = fetch(t, f"{out}/{name}")
        print(f"{t}: {n} notices -> {out}/{name}")


if __name__ == "__main__":
    main()
