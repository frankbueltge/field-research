#!/usr/bin/env python3
"""Corpus M: PubMed randomized-controlled-trial abstracts, 2026-08. Session 168, 2026-09-23.

Writes the raw corpus OUTSIDE the repository (protocol §7: no third-party source files
committed) and a manifest of identifiers and digests INSIDE it.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

OUT = sys.argv[1]
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TERM = "randomized controlled trial[pt] AND 2026/08/01:2026/08/31[dp] AND hasabstract"
TARGET = 1000


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "field-research/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", "replace")


def main():
    q = urllib.parse.urlencode({"db": "pubmed", "term": TERM, "retmax": TARGET,
                                "retmode": "json", "sort": "pub_date"})
    res = json.loads(get(EUTILS + "esearch.fcgi?" + q))["esearchresult"]
    pmids = res["idlist"]
    print(f"esearch: {res['count']} match the term, {len(pmids)} returned")
    docs = []
    for i in range(0, len(pmids), 200):
        batch = pmids[i:i + 200]
        xml = get(EUTILS + "efetch.fcgi?" + urllib.parse.urlencode(
            {"db": "pubmed", "id": ",".join(batch), "retmode": "xml", "rettype": "abstract"}))
        for art in re.findall(r"<PubmedArticle>.*?</PubmedArticle>", xml, re.S):
            m = re.search(r"<PMID[^>]*>(\d+)</PMID>", art)
            if not m:
                continue
            parts = []
            for lab, txt in re.findall(r"<AbstractText([^>]*)>(.*?)</AbstractText>", art, re.S):
                lm = re.search(r'Label="([^"]*)"', lab)
                body = re.sub(r"<[^>]+>", "", txt)
                body = (body.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
                            .replace("&quot;", '"').replace("&apos;", "'"))
                if lm:
                    parts.append(lm.group(1).strip().title() + ": " + body.strip())
                else:
                    parts.append(body.strip())
            if parts:
                docs.append({"id": m.group(1), "text": " ".join(parts).strip()})
        print(f"  efetch {i + len(batch)}/{len(pmids)} -> {len(docs)} abstracts")
        time.sleep(0.5)
    json.dump({"corpus": "M", "source": "PubMed E-utilities", "term": TERM,
               "esearch_count": res["count"], "requested": TARGET,
               "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "docs": docs}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"wrote {len(docs)} documents to {OUT}")


if __name__ == "__main__":
    main()
