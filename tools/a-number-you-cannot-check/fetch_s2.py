#!/usr/bin/env python3
"""Corpus A: Semantic Scholar abstracts, query "large language model", year 2026.

Session 168, 2026-09-23. Raw corpus written outside the repository (protocol §7).
"""
import json
import sys
import time
import urllib.parse
import urllib.request

OUT = sys.argv[1]
BASE = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
QUERY = "large language model"
YEAR = "2026"
TARGET = 1000


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "field-research/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def main():
    docs, token, pages, seen_records = [], None, 0, 0
    while len(docs) < TARGET and pages < 12:
        params = {"query": QUERY, "year": YEAR,
                  "fields": "title,abstract,year,externalIds,venue"}
        if token:
            params["token"] = token
        res = get(BASE + "?" + urllib.parse.urlencode(params))
        pages += 1
        data = res.get("data") or []
        seen_records += len(data)
        for d in data:
            ab = (d.get("abstract") or "").strip()
            if ab and len(docs) < TARGET:
                docs.append({"id": d["paperId"], "doi": (d.get("externalIds") or {}).get("DOI"),
                             "title": d.get("title"), "venue": d.get("venue"), "text": ab})
        print(f"  page {pages}: {len(data)} records, {len(docs)} with abstracts kept")
        token = res.get("token")
        if not token:
            break
        time.sleep(1.2)
    json.dump({"corpus": "A", "source": "Semantic Scholar graph API, bulk search",
               "query": QUERY, "year": YEAR, "pages_fetched": pages,
               "records_seen": seen_records, "requested": TARGET,
               "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "docs": docs}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"wrote {len(docs)} documents from {seen_records} records to {OUT}")


if __name__ == "__main__":
    main()
