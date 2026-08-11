#!/usr/bin/env python3
"""Completeness check on corpus B's harvest — because the backend's hit count is approximate.

The sweep log records a parent window reporting **1,804** comment hits and its two children
reporting **116** and **1,095**, whose own children reported **374** and **336**. Those numbers
do not add up, which means the backend's `nbHits` is an estimate at large N and cannot be used
as evidence that a window was exhausted.

So this does not argue about `nbHits`. It re-harvests one already-swept leaf window by cutting
it into eight narrower sub-windows and asks a plain question: does the finer sweep return any
identifier the coarser one missed? If it does, the harvest is incomplete and the record says
so and by how much.
"""
import json
import time
import urllib.parse
import urllib.request

UA = "field-research/1.0 (independent research instrument; sequential, rate-limited)"
API = "https://hn.algolia.com/api/v1/search_by_date"
import re
VID = re.compile(r"tiktok\.com/@([^/\"'<>\s&?]+)/video/(\d+)")


def unescape(s):
    return (s.replace("&#x2F;", "/").replace("&#47;", "/").replace("&amp;", "&")
             .replace("&#x27;", "'").replace("&quot;", '"').replace("&lt;", "<")
             .replace("&gt;", ">"))


def harvest(lo, hi, tags="comment"):
    ids, page, reported = set(), 0, None
    while True:
        p = {"query": "tiktok.com", "tags": tags, "hitsPerPage": "100", "page": str(page),
             "numericFilters": f"created_at_i>={lo},created_at_i<{hi}"}
        req = urllib.request.Request(API + "?" + urllib.parse.urlencode(p),
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as r:
            d = json.load(r)
        if reported is None:
            reported = d.get("nbHits")
        for h in d.get("hits", []):
            text = " ".join(str(h.get(k) or "") for k in
                            ("comment_text", "story_text", "url", "story_url", "title"))
            for m in VID.finditer(unescape(text)):
                ids.add(m.group(2))
        page += 1
        time.sleep(1.0)
        if page >= min(d.get("nbPages", 0), 10):
            break
    return ids, reported


LO, HI = 1710307200, 1786000000        # the leaf window the sweep log records as 336 hits, 4 pages
coarse, coarse_reported = harvest(LO, HI)

fine, fine_reported = set(), []
step = (HI - LO) // 8
for k in range(8):
    lo = LO + k * step
    hi = HI if k == 7 else LO + (k + 1) * step
    s, rep = harvest(lo, hi)
    fine |= s
    fine_reported.append({"window": [lo, hi], "nbHits_reported": rep, "ids": len(s)})

out = {
    "window": [LO, HI],
    "coarse": {"nbHits_reported": coarse_reported, "distinct_ids": len(coarse), "sub_windows": 1},
    "fine": {"distinct_ids": len(fine), "sub_windows": 8, "detail": fine_reported},
    "found_only_by_fine": sorted(fine - coarse),
    "found_only_by_coarse": sorted(coarse - fine),
    "verdict": None,
}
missed = len(fine - coarse)
out["verdict"] = (f"The finer sweep found {missed} identifier(s) the coarser one missed."
                  if missed else
                  "The finer sweep found nothing the coarser one missed — on this window the "
                  "harvest is complete, and the approximate hit count is a reporting artefact "
                  "rather than a gap in the corpus.")
json.dump(out, open("sweep-completeness.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "fine"}, indent=1))
print("fine distinct:", len(fine), "coarse distinct:", len(coarse))
