#!/usr/bin/env python3
"""Expansion round 2 — the wikis round 1 never reached, and the editions it lost to 429.

Round 1 spent its whole 1,500 s budget on three wikis (en, es, ja) and stopped inside
`ja` namespace 15; eighteen of the twenty-one session-109 wikis were never queried at all.
Separately, 25 of the 45 language editions attempted in article space failed with HTTP 429
because `collect_corpus.py` has no backoff — a gap this session recorded before it knew the
yield.

This round does both, with backoff, while the round-1 baseline probe runs against a different
host. Same query, same instrument, same namespaces. Deadline-capped and the stopping point is
written into the output, never silently truncated.
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
DELAY = 1.2
NAMESPACES = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 100, 118, 119]

# the eighteen session-109 wikis round 1 never reached, biggest first
WIKIS_NS = [w.strip() for w in open("expansion-111/round3_wikis.txt") if w.strip()]
OLD_WIKIS_NS = [
            "ru.wikipedia.org", "uk.wikipedia.org", "zh.wikipedia.org", "ko.wikipedia.org",
            "it.wikipedia.org", "tr.wikipedia.org", "pl.wikipedia.org", "ar.wikipedia.org",
            "vi.wikipedia.org", "th.wikipedia.org", "nl.wikipedia.org", "fa.wikipedia.org",
            "sv.wikipedia.org", "fr.wikipedia.org"]

# the editions round 1 lost to 429 in article space (ns 0)
WIKIS_NS0 = []  # round 3: article space already done in round 2
UNUSED_NS0 = ["da.wikipedia.org", "el.wikipedia.org", "hu.wikipedia.org", "no.wikipedia.org",
             "ro.wikipedia.org", "bg.wikipedia.org", "sr.wikipedia.org", "hr.wikipedia.org",
             "sk.wikipedia.org", "sl.wikipedia.org", "lv.wikipedia.org", "et.wikipedia.org",
             "ca.wikipedia.org", "eu.wikipedia.org", "az.wikipedia.org", "kk.wikipedia.org",
             "mn.wikipedia.org", "sw.wikipedia.org", "af.wikipedia.org", "is.wikipedia.org",
             "mk.wikipedia.org", "bs.wikipedia.org", "be.wikipedia.org", "nn.wikipedia.org",
             "simple.wikipedia.org", "ga.wikipedia.org", "cy.wikipedia.org", "la.wikipedia.org",
             "ky.wikipedia.org"]


def fetch(wiki, ns, cont, tries=4):
    p = {"action": "query", "list": "exturlusage", "euquery": "tiktok.com",
         "eulimit": "500", "euprotocol": "https", "eunamespace": str(ns),
         "format": "json", "formatversion": "2"}
    if cont:
        p["eucontinue"] = cont
    url = f"https://{wiki}/w/api.php?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(4 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"429 exhausted: {wiki} ns{ns}")


def sweep(wiki, ns, rows, log, deadline):
    cont, pages, got = None, 0, 0
    while True:
        if time.time() > deadline:
            log.append({"STOPPED_AT_DEADLINE": {"wiki": wiki, "ns": ns}})
            return False
        d = fetch(wiki, ns, cont)
        eu = d.get("query", {}).get("exturlusage", [])
        got += len(eu)
        for r in eu:
            m = VID.search(r["url"])
            if m:
                rows.append({"wiki": wiki, "ns": ns, "page": r.get("title"),
                             "handle": m.group(1), "vid": m.group(2), "url": r["url"]})
        pages += 1
        cont = d.get("continue", {}).get("eucontinue")
        if not cont:
            break
        time.sleep(DELAY)
        if pages > 40:
            log.append({"wiki": wiki, "ns": ns, "PAGE_CAP": "reported, not silently truncated"})
            break
    if got:
        log.append({"wiki": wiki, "ns": ns, "link_rows": got, "api_pages": pages})
    return True


def main(budget_s):
    deadline = time.time() + float(budget_s)
    rows, log = [], []
    # article space first: it is the cheaper, previously-lost arm
    for wiki in WIKIS_NS0:
        if time.time() > deadline:
            log.append({"STOPPED_AT_DEADLINE": {"phase": "ns0", "wiki": wiki}})
            break
        try:
            sweep(wiki, 0, rows, log, deadline)
        except Exception as e:
            log.append({"wiki": wiki, "ns": 0, "ERROR": str(e)[:140]})
        time.sleep(DELAY)
    for wiki in WIKIS_NS:
        for ns in NAMESPACES:
            if time.time() > deadline:
                log.append({"STOPPED_AT_DEADLINE": {"phase": "ns", "wiki": wiki, "ns": ns}})
                dump(rows, log)
                return
            try:
                if not sweep(wiki, ns, rows, log, deadline):
                    dump(rows, log)
                    return
            except Exception as e:
                log.append({"wiki": wiki, "ns": ns, "ERROR": str(e)[:140]})
            time.sleep(DELAY)
    dump(rows, log)


def dump(rows, log):
    ids = {}
    for r in rows:
        ids.setdefault(r["vid"], r)
    json.dump({"meta": {"source": "MediaWiki exturlusage, expansion round 3",
                        "note": "the 14 wikis round 2 did not reach before its deadline, all namespaces",
                        "url_rows": len(rows), "distinct_ids": len(ids),
                        "collected_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "log": log},
               "rows": list(ids.values())},
              open("expansion-111/corpus-round3.json", "w"), indent=1)
    print(json.dumps({"url_rows": len(rows), "distinct_ids": len(ids),
                      "groups_with_yield": len([e for e in log if "link_rows" in e])}))


if __name__ == "__main__":
    main(sys.argv[1])
