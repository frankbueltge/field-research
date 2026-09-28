#!/usr/bin/env python3
"""Twenty Augusts — session 173, 2026-09-28. Fetch the five trial-abstract corpora.

    fetch.py <raw_dir>

The abstract extraction is copied line for line from 09-23's
tools/a-number-you-cannot-check/fetch_pubmed.py; only the term is per year. The 2026 year is re-fetched by the PMIDs pinned on 09-23, and
the digest match proves the extraction unchanged. Raw texts stay outside the repository.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TERM = "randomized controlled trial[pt] AND {y}/08/01:{y}/08/31[dp] AND hasabstract"
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PIN = os.path.join(ROOT, 'artifacts/2026-09-23-a-number-you-cannot-check/data/corpora.json')


def get(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "field-research/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read().decode("utf-8", "replace")
            if '"API rate limit exceeded"' in body[:200]:
                raise IOError("rate limit")
            return body
        except Exception as e:                                   # noqa: BLE001
            print(f"  retry {i + 1}: {e}", file=sys.stderr)
            time.sleep(2 ** i)
    raise SystemExit("fetch failed: " + url[:120])


def extract(xml):
    """Identical to fetch_pubmed.py's loop body (09-23)."""
    docs = []
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
    return docs


def efetch(pmids):
    docs = []
    for i in range(0, len(pmids), 200):
        docs += extract(get(EUTILS + "efetch.fcgi?" + urllib.parse.urlencode(
            {"db": "pubmed", "id": ",".join(pmids[i:i + 200]), "retmode": "xml",
             "rettype": "abstract"})))
        time.sleep(0.6)
    return docs


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for y in (2006, 2011, 2016, 2021):
        term = TERM.format(y=y)
        q = urllib.parse.urlencode({"db": "pubmed", "term": term, "retmax": 1000,
                                    "retmode": "json", "sort": "pub_date"})
        res = json.loads(get(EUTILS + "esearch.fcgi?" + q))["esearchresult"]
        time.sleep(0.6)
        docs = efetch(res["idlist"])
        json.dump({"year": y, "term": term, "esearch_count": int(res["count"]),
                   "returned_ids": len(res["idlist"]),
                   "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "docs": docs}, open(os.path.join(out, f"{y}.json"), "w"), ensure_ascii=False)
        print(y, res["count"], len(res["idlist"]), len(docs))
    pin = [d["id"] for d in json.load(open(PIN))["M"]["docs"]]
    docs = efetch(pin)
    json.dump({"year": 2026, "term": "PMIDs pinned 2026-09-23 (corpus M)", "esearch_count": None,
               "returned_ids": len(pin),
               "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "docs": docs}, open(os.path.join(out, "2026.json"), "w"), ensure_ascii=False)
    print(2026, len(pin), len(docs))


if __name__ == "__main__":
    main()
