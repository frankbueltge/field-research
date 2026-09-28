#!/usr/bin/env python3
"""Twenty Augusts — exploratory, registered as A-2 AFTER the primary results were seen.

    explore.py <raw_dir>

(1) Two more frames with the primary term: August 2025, and August 2026 as the index stands
today. (2) Journal of every record in all seven frames (esummary), for a journal-mix check.
"""
import json
import os
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch import EUTILS, TERM, get, efetch                        # noqa: E402


def main():
    raw = sys.argv[1]
    for y, name in ((2025, '2025'), (2026, '2026-today')):
        term = TERM.format(y=y)
        res = json.loads(get(EUTILS + "esearch.fcgi?" + urllib.parse.urlencode(
            {"db": "pubmed", "term": term, "retmax": 1000, "retmode": "json", "sort": "pub_date"})))["esearchresult"]
        time.sleep(0.6)
        docs = efetch(res["idlist"])
        json.dump({"year": y, "term": term, "esearch_count": int(res["count"]),
                   "returned_ids": len(res["idlist"]),
                   "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "docs": docs}, open(os.path.join(raw, f"{name}.json"), "w"), ensure_ascii=False)
        print(name, res["count"], len(docs))
    journals = {}
    for name in ('2006', '2011', '2016', '2021', '2026', '2025', '2026-today'):
        ids = [d['id'] for d in json.load(open(os.path.join(raw, f'{name}.json')))['docs']]
        for i in range(0, len(ids), 200):
            r = json.loads(get(EUTILS + "esummary.fcgi?" + urllib.parse.urlencode(
                {"db": "pubmed", "id": ",".join(ids[i:i + 200]), "retmode": "json"})))["result"]
            for pid in r.get("uids", []):
                journals[pid] = r[pid].get("fulljournalname") or r[pid].get("source")
            time.sleep(0.6)
        print(name, 'journals', sum(1 for x in ids if x in journals))
    json.dump(journals, open(os.path.join(raw, 'journals.json'), 'w'))


if __name__ == '__main__':
    main()
