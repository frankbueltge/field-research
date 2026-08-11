#!/usr/bin/env python3
"""Corpus expansion, session 111 — arm A2: the same wikis, OUTSIDE article space.

Why this and not simply "more identifiers". PREREGISTRATION-111.md §4 names a confound it
cannot remove: **arm A is actively pruned.** An encyclopedia's editors and its link-fixing
bots remove or replace dead external links in articles, which deletes dead videos from the
corpus preferentially in the oldest articles and makes arm A's older cohorts look better
than the truth. That confound sits directly under this session's hazard estimate.

Talk pages, user pages, project pages and drafts carry the same operator, the same editors
and the same subject matter — and **no link-maintenance regime**. Nobody fixes a dead link
in a 2019 talk-page comment. So arm A2 is at once the volume the power audit needs and the
control the pruning confound has been missing.

Namespaces: everything except 0 (article), which is arm A. Credential-free, sequential,
backs off on HTTP 429 rather than hammering.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "field-research/1.0 (independent research instrument; sequential, rate-limited)"
VID = re.compile(r"tiktok\.com/@([^/]+)/video/(\d+)")
DELAY = 1.5
NAMESPACES = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 100, 118, 119]

WIKIS = ["en.wikipedia.org", "es.wikipedia.org", "ja.wikipedia.org", "de.wikipedia.org",
         "id.wikipedia.org", "he.wikipedia.org", "pt.wikipedia.org", "ru.wikipedia.org",
         "uk.wikipedia.org", "zh.wikipedia.org", "ko.wikipedia.org", "it.wikipedia.org",
         "tr.wikipedia.org", "pl.wikipedia.org", "ar.wikipedia.org", "vi.wikipedia.org",
         "th.wikipedia.org", "nl.wikipedia.org", "fa.wikipedia.org", "sv.wikipedia.org",
         "fr.wikipedia.org"]


def fetch(wiki, ns, cont, tries=5):
    p = {"action": "query", "list": "exturlusage", "euquery": "tiktok.com",
         "eulimit": "500", "euprotocol": "https", "eunamespace": str(ns),
         "format": "json", "formatversion": "2"}
    if cont:
        p["eucontinue"] = cont
    url = f"https://{wiki}/w/api.php?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 5 * (attempt + 1)
                print(f"  429 on {wiki} ns{ns} — backing off {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError(f"429 exhausted: {wiki} ns{ns}")


def main():
    rows, log = [], []
    deadline = time.time() + float(sys.argv[1]) if len(sys.argv) > 1 else None
    for wiki in WIKIS:
        for ns in NAMESPACES:
            if deadline and time.time() > deadline:
                log.append({"STOPPED_AT_DEADLINE": {"wiki": wiki, "ns": ns}})
                print("DEADLINE — stopping, reported not silently truncated", file=sys.stderr)
                dump(rows, log)
                return
            cont, pages, got = None, 0, 0
            try:
                while True:
                    d = fetch(wiki, ns, cont)
                    eu = d.get("query", {}).get("exturlusage", [])
                    got += len(eu)
                    for r in eu:
                        m = VID.search(r["url"])
                        if m:
                            rows.append({"wiki": wiki, "ns": ns, "page": r.get("title"),
                                         "handle": m.group(1), "vid": m.group(2),
                                         "url": r["url"]})
                    pages += 1
                    cont = d.get("continue", {}).get("eucontinue")
                    if not cont:
                        break
                    time.sleep(DELAY)
                    if pages > 60:
                        log.append({"wiki": wiki, "ns": ns,
                                    "PAGE_CAP": "reported, not silently truncated"})
                        break
            except Exception as e:
                log.append({"wiki": wiki, "ns": ns, "ERROR": str(e)[:160]})
                continue
            if got:
                log.append({"wiki": wiki, "ns": ns, "link_rows": got, "api_pages": pages})
            time.sleep(DELAY)
    dump(rows, log)


def dump(rows, log):
    ids = {}
    for r in rows:
        ids.setdefault(r["vid"], r)
    json.dump({"meta": {"source": "MediaWiki exturlusage, non-article namespaces",
                        "wikis": len(WIKIS), "namespaces": NAMESPACES,
                        "url_rows": len(rows), "distinct_ids": len(ids),
                        "collected_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "log": log},
               "rows": list(ids.values())},
              open("expansion-111/corpus-A2-namespaces.json", "w"), indent=1)
    print(json.dumps({"url_rows": len(rows), "distinct_ids": len(ids),
                      "wikis_logged": len([e for e in log if "link_rows" in e])}))


if __name__ == "__main__":
    main()
