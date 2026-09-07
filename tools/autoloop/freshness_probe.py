#!/usr/bin/env python3
"""autoloop — the freshness probe.

The drift probe showed the corpus's newest submission is days older than the day the
fetch ran. This probe asks whose property that is: the query the loop sends, or the
index that answers it.

For each category the loop fetches, it sends two requests that differ in one parameter
only — `sortBy=submittedDate` (what `fetch.py` uses) and `sortBy=lastUpdatedDate` — and
records, for the first hundred entries of each, the newest and oldest `published` and
`updated` dates and the histogram of publication days. Nothing is derived, modelled or
assumed: the numbers are counted off the payloads.

Two requests per category, three seconds apart, sixteen in all.

Usage: python3 tools/autoloop/freshness_probe.py --out <freshness.json>
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom"}
CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "cs.RO", "cs.SE", "stat.ML", "cs.CY"]
SORTS = ["submittedDate", "lastUpdatedDate"]
POLITE_SECONDS = 3.0
UA = "field-research autoloop (meridian@field-research.invalid)"


def probe(cat, sort_by, breaks):
    url = (f"{API}?search_query=cat:{cat}&start=0&max_results=100"
           f"&sortBy={sort_by}&sortOrder=descending")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        breaks.append({"cat": cat, "sort": sort_by, "detail": str(e)[:200]})
        return None
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        breaks.append({"cat": cat, "sort": sort_by, "detail": f"parse: {str(e)[:180]}"})
        return None
    pub, upd = [], []
    for entry in root.findall("a:entry", NS):
        p = entry.find("a:published", NS)
        u = entry.find("a:updated", NS)
        if p is not None and p.text:
            pub.append(p.text[:10])
        if u is not None and u.text:
            upd.append(u.text[:10])
    if not pub:
        breaks.append({"cat": cat, "sort": sort_by, "detail": "no entries"})
        return None
    return {
        "entries": len(pub),
        "published_max": max(pub),
        "published_min": min(pub),
        "updated_max": max(upd) if upd else None,
        "published_histogram": dict(sorted(Counter(pub).items(), reverse=True)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = {"probe": "freshness",
           "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "today_utc": today,
           "endpoint": API,
           "max_results_per_request": 100,
           "by_category": {}, "breaks": []}

    first = True
    for cat in CATEGORIES:
        out["by_category"][cat] = {}
        for sort_by in SORTS:
            if not first:
                time.sleep(POLITE_SECONDS)
            first = False
            r = probe(cat, sort_by, out["breaks"])
            out["by_category"][cat][sort_by] = r
            if r:
                print(f"  {cat} {sort_by}: newest published {r['published_max']}, "
                      f"newest updated {r['updated_max']}", file=sys.stderr)

    lags = {}
    for sort_by in SORTS:
        vals = [v[sort_by]["published_max"] for v in out["by_category"].values() if v.get(sort_by)]
        if vals:
            newest = max(vals)
            lags[sort_by] = {
                "newest_published_any_category": newest,
                "lag_days_vs_today": (datetime.strptime(today, "%Y-%m-%d")
                                      - datetime.strptime(newest, "%Y-%m-%d")).days,
                "categories_reporting": len(vals),
            }
    out["summary"] = lags

    with open(args.out, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps(out["summary"], indent=1))
    return 0 if out["by_category"] else 1


if __name__ == "__main__":
    sys.exit(main())
