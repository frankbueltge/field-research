#!/usr/bin/env python3
"""Fetch PMC JATS full text for every corpus-M paper with a PMC ID. Session 170, 2026-09-25.
Raw XML is kept OUTSIDE the repository; the manifest (ids, has-body, digest) comes back in."""
import hashlib, json, os, re, sys, time, urllib.parse, urllib.request

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
W = sys.argv[1]


def get(url, data):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "field-research/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read().decode("utf-8", "replace")


def main():
    rows = [r for r in json.load(open(os.path.join(W, 'refetch.json')))['rows'] if r['pmcid']]
    os.makedirs(os.path.join(W, 'pmc'), exist_ok=True)
    man = []
    for i in range(0, len(rows), 20):
        batch = rows[i:i + 20]
        ids = [r['pmcid'][3:] for r in batch]
        for attempt in range(4):
            try:
                xml = get(EUTILS + "efetch.fcgi", urllib.parse.urlencode(
                    {"db": "pmc", "id": ",".join(ids), "retmode": "xml"}).encode())
                break
            except Exception as e:
                print("retry", e, file=sys.stderr); time.sleep(2 ** (attempt + 1))
        arts = re.findall(r"<article[ >].*?</article>", xml, re.S)
        byid = {}
        for a in arts:
            m = re.search(r'<article-id pub-id-type="(?:pmcid|pmc)">(?:PMC)?(\d+)</article-id>', a)
            if m:
                byid[m.group(1)] = a
        for r in batch:
            a = byid.get(r['pmcid'][3:])
            body = bool(a and re.search(r"<body[ >]", a))
            if a:
                open(os.path.join(W, 'pmc', r['pmcid'] + '.xml'), 'w').write(a)
            man.append({"id": r['id'], "pmcid": r['pmcid'], "returned": a is not None,
                        "has_body": body, "tables": len(re.findall(r"<table-wrap[ >]", a)) if a else 0,
                        "sha256": hashlib.sha256(a.encode()).hexdigest() if a else None})
        print(f"{i + len(batch)}/{len(rows)} returned {sum(m['returned'] for m in man)} body {sum(m['has_body'] for m in man)}", file=sys.stderr)
        time.sleep(0.4)
    json.dump({"fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "rows": man},
              open(os.path.join(W, 'fulltext-manifest.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
