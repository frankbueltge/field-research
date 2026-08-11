#!/usr/bin/env python3
"""Corpus B — the second, independent source.

Collects public video identifiers of the same platform as cited in Hacker News comments and
stories, via that site's public search API. Credential-free, no account, no key.

Why this source and not another slice of the first one: corpus A came from one index
(MediaWiki `exturlusage`) governed by one set of citation policies and maintained by editors
and link-fixing bots. Hacker News is a different operator, a different population, has no
notability or verifiability policy governing what may be linked, and no link-maintenance
regime at all. That is the independence the gate asked for.

Neither `hn.algolia.com` nor the API host serves a `/robots.txt` (HTTP 404 and HTTP 400
respectively, checked 2026-08-11 before the first query); there is no directive to honour and
none is assumed. Requests are sequential with a fixed delay.

The search backend caps pagination at 1,000 results per query, so the run windows through time
with `created_at_i` filters and `search_by_date` rather than paging past the cap — the window
is narrowed until each window returns fewer than the cap, so nothing is silently truncated.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "field-research/1.0 (independent research instrument; sequential, rate-limited)"
DELAY = 1.0
API = "https://hn.algolia.com/api/v1/search_by_date"
PAGE_CAP = 1000          # the backend's hard pagination ceiling
HITS = 100

# The identifier as it appears in a URL. Deliberately the same shape corpus A used, so the two
# corpora are populated by the same rule and only the source differs.
VID = re.compile(r"tiktok\.com/@([^/\"'<>\s&?]+)/video/(\d+)")
# HN escapes URLs in comment HTML; entities are decoded before matching.


def unescape(s):
    return (s.replace("&#x2F;", "/").replace("&#47;", "/").replace("&amp;", "&")
             .replace("&#x27;", "'").replace("&quot;", '"').replace("&lt;", "<")
             .replace("&gt;", ">"))


def query(tags, lo, hi, page):
    p = {"query": "tiktok.com", "tags": tags, "hitsPerPage": str(HITS), "page": str(page),
         "numericFilters": f"created_at_i>={lo},created_at_i<{hi}"}
    url = API + "?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def sweep(tags, lo, hi, out, log):
    """Fetch every hit in [lo, hi). Splits the window if it would exceed the pagination cap."""
    d = query(tags, lo, hi, 0)
    time.sleep(DELAY)
    n = d.get("nbHits", 0)
    if n > PAGE_CAP and hi - lo > 1:
        mid = (lo + hi) // 2
        log.append({"tags": tags, "window": [lo, hi], "nbHits": n, "action": "split"})
        sweep(tags, lo, mid, out, log)
        sweep(tags, mid, hi, out, log)
        return
    if n > PAGE_CAP:
        log.append({"tags": tags, "window": [lo, hi], "nbHits": n,
                    "action": "CAP HIT — reported, not silently truncated"})
    pages = min(d.get("nbPages", 0), PAGE_CAP // HITS)
    log.append({"tags": tags, "window": [lo, hi], "nbHits": n, "pages_fetched": pages})
    for page in range(pages):
        d2 = d if page == 0 else query(tags, lo, hi, page)
        if page:
            time.sleep(DELAY)
        for h in d2.get("hits", []):
            text = " ".join(str(h.get(k) or "") for k in
                            ("comment_text", "story_text", "url", "story_url", "title"))
            for m in VID.finditer(unescape(text)):
                out.append({"handle": m.group(1), "vid": m.group(2),
                            "url": f"https://www.tiktok.com/@{m.group(1)}/video/{m.group(2)}",
                            "hn_object_id": h.get("objectID"), "hn_created": h.get("created_at"),
                            "hn_tags": tags,
                            "hn_permalink": f"https://news.ycombinator.com/item?id={h.get('objectID')}"})


def main():
    lo, hi = 1483228800, 1786000000   # 2017-01-01 .. beyond now; the platform did not exist earlier
    rows, log = [], []
    for tags in ("comment", "story"):
        sweep(tags, lo, hi, rows, log)
    ids = {}
    for r in rows:
        ids.setdefault(r["vid"], r)
    meta = {"source": "Hacker News public search API (hn.algolia.com/api/v1/search_by_date)",
            "query": "tiktok.com", "window_unix": [lo, hi],
            "api_calls": len([e for e in log if "pages_fetched" in e]),
            "url_rows": len(rows), "distinct_ids": len(ids), "sweep_log": log}
    json.dump({"meta": meta, "rows": rows}, open("corpus-hn.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in meta.items() if k != "sweep_log"}))


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
