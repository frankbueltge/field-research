#!/usr/bin/env python3
"""Collect the corpus: public video URLs of one platform cited in Wikipedia articles.

Credential-free. Uses the MediaWiki `exturlusage` list, which is the wiki's own index of
external links in page wikitext. Mainspace (ns 0) only. Paginated to exhaustion.

Output: corpus-<wiki>.json — one row per (page, url), plus a de-duplicated id list.
"""
import json, re, sys, time, urllib.parse, urllib.request

UA = "field-research/1.0 (independent research instrument; sequential, rate-limited)"
VID = re.compile(r"tiktok\.com/@([^/]+)/video/(\d+)")


def fetch(wiki, cont=None):
    p = {
        "action": "query", "list": "exturlusage", "euquery": "tiktok.com",
        "eulimit": "500", "euprotocol": "https", "eunamespace": "0",
        "format": "json", "formatversion": "2",
    }
    if cont:
        p["eucontinue"] = cont
    url = f"https://{wiki}/w/api.php?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main(wiki):
    rows, cont, pages = [], None, 0
    while True:
        d = fetch(wiki, cont)
        eu = d.get("query", {}).get("exturlusage", [])
        rows.extend(eu)
        pages += 1
        cont = d.get("continue", {}).get("eucontinue")
        if not cont:
            break
        time.sleep(1.0)
        if pages > 200:
            print("PAGE CAP HIT — reported, not silently truncated", file=sys.stderr)
            break
    out = []
    for r in rows:
        m = VID.search(r["url"])
        if m:
            out.append({"page": r.get("title"), "handle": m.group(1), "vid": m.group(2),
                        "url": r["url"]})
    ids = {}
    for r in out:
        ids.setdefault(r["vid"], r)
    print(json.dumps({"wiki": wiki, "api_pages": pages, "link_rows": len(rows),
                      "video_rows": len(out), "distinct_ids": len(ids)}))
    json.dump({"meta": {"wiki": wiki, "api_pages": pages, "link_rows": len(rows),
                        "video_rows": len(out), "distinct_ids": len(ids)},
               "rows": out}, open(f"corpus-{wiki}.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
