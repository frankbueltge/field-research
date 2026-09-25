#!/usr/bin/env python3
"""Re-fetch corpus M (pinned 2026-09-23) by PMID, check each text against its pinned digest,
and map PMIDs to PMC IDs. Session 170, 2026-09-25.

Raw texts are written OUTSIDE the repository (protocol §7); only identifiers, digests and
verdicts come back in. The abstract text is rebuilt by 09-23's own code path, imported.
"""
import hashlib, json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PIN = os.path.join(ROOT, 'artifacts/2026-09-23-a-number-you-cannot-check/data/corpora.json')
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
OUT = sys.argv[1]


def get(url, data=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "field-research/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", "replace")


def abstract_text(art):
    # identical to tools/a-number-you-cannot-check/fetch_pubmed.py
    parts = []
    for lab, txt in re.findall(r"<AbstractText([^>]*)>(.*?)</AbstractText>", art, re.S):
        lm = re.search(r'Label="([^"]*)"', lab)
        body = re.sub(r"<[^>]+>", "", txt)
        body = (body.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
                    .replace("&quot;", '"').replace("&apos;", "'"))
        parts.append((lm.group(1).strip().title() + ": " if lm else "") + body.strip())
    return " ".join(parts).strip()


def main():
    pin = json.load(open(PIN))['M']['docs']
    pinned = {d['id']: d['sha256'] for d in pin}
    ids = [d['id'] for d in pin]
    docs, pmc = {}, {}
    for i in range(0, len(ids), 200):
        batch = ids[i:i + 200]
        xml = get(EUTILS + "efetch.fcgi", urllib.parse.urlencode(
            {"db": "pubmed", "id": ",".join(batch), "retmode": "xml", "rettype": "abstract"}).encode())
        for art in re.findall(r"<PubmedArticle>.*?</PubmedArticle>", xml, re.S):
            m = re.search(r"<PMID[^>]*>(\d+)</PMID>", art)
            if not m:
                continue
            docs[m.group(1)] = abstract_text(art)
            pm = re.search(r'<ArticleId IdType="pmc">(PMC\d+)</ArticleId>', art)
            if pm:
                pmc[m.group(1)] = pm.group(1)
        print(f"efetch {i + len(batch)}/{len(ids)}", file=sys.stderr)
        time.sleep(0.5)
    rows = []
    for pid in ids:
        t = docs.get(pid)
        h = hashlib.sha256(t.encode()).hexdigest() if t is not None else None
        rows.append({"id": pid, "returned": t is not None, "digest_match": h == pinned[pid],
                     "pmcid": pmc.get(pid)})
    json.dump({"fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "rows": rows}, open(os.path.join(OUT, 'refetch.json'), 'w'), indent=1)
    json.dump(docs, open(os.path.join(OUT, 'abstracts.json'), 'w'), ensure_ascii=False)
    n = len(rows)
    print(f"returned {sum(r['returned'] for r in rows)}/{n}, digest match "
          f"{sum(r['digest_match'] for r in rows)}, with pmcid {sum(bool(r['pmcid']) for r in rows)}")


if __name__ == "__main__":
    main()
