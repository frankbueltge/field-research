#!/usr/bin/env python3
"""Harvest cohorts A (automation-claim abstracts) and B (age-matched cs.AI control)
from the arXiv API, and extract the URLs their abstracts declare.

Writes derived data only — arXiv identifiers, dates, categories, and the URLs
themselves. No abstract text is written to disk (third-party text is not committed
to this repository; the identifier resolves to the primary record).

Usage: python3 tools/links/harvest.py <outdir>
"""
import csv, hashlib, json, os, re, sys, time, urllib.parse, urllib.request
from collections import Counter, defaultdict

API = "https://export.arxiv.org/api/query"
WINDOW = "submittedDate:[202401010000 TO 202608312359]"
PHRASES = [
    "AI scientist", "autonomous research", "automated scientific discovery",
    "research agent", "automating scientific discovery",
    "autonomous scientific discovery", "end-to-end research pipeline",
    "automate the research process", "automated research pipeline",
    "agentic research",
]
PACE = 4.0            # seconds between API calls (arXiv etiquette)
ENTRY = re.compile(r"<entry>(.*?)</entry>", re.S)
FIELD = lambda tag, s: (re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), s, re.S) or [None, None])[1]
URL_RE = re.compile(r"https?://[^\s<>\"')\]}]+")
TOTAL = re.compile(r"<opensearch:totalResults[^>]*>(\d+)<")


def fetch(params, tries=6):
    url = API + "?" + "&".join("%s=%s" % (k, v) for k, v in params)
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as exc:          # rate limit or transient network
            last = exc
            time.sleep(10 + 10 * attempt)
    raise RuntimeError("arXiv API failed for %s: %s" % (url, last))


def unescape(s):
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&#39;", "'")):
        s = s.replace(a, b)
    return s


def clean_url(u):
    u = unescape(u).rstrip(".,;:")
    while u and u[-1] in ")]}" and u.count(u[-1]) > u.count({")": "(", "]": "[", "}": "{"}[u[-1]]):
        u = u[:-1]
    return u


def parse(xml):
    out = []
    for raw in ENTRY.findall(xml):
        aid = FIELD("id", raw)
        if not aid:
            continue
        base = aid.rsplit("/", 1)[-1]
        base = re.sub(r"v\d+$", "", base)
        summary = unescape(FIELD("summary", raw) or "")
        cat = re.search(r'<arxiv:primary_category[^>]*term="([^"]+)"', raw)
        urls = []
        for u in URL_RE.findall(summary):
            u = clean_url(u)
            host = urllib.parse.urlparse(u).netloc.lower()
            if host.endswith("arxiv.org") or host.endswith("doi.org") or not host:
                continue
            if u not in urls:
                urls.append(u)
        out.append({
            "arxiv_id": base,
            "published": (FIELD("published", raw) or "")[:10],
            "updated": (FIELD("updated", raw) or "")[:10],
            "primary_category": cat.group(1) if cat else "",
            "urls": urls,
        })
    return out


def harvest_cohort_a():
    papers, phrase_hits = {}, defaultdict(set)
    for phrase in PHRASES:
        sq = 'abs:%s AND %s' % ('"%s"' % phrase, WINDOW)
        start, total = 0, None
        while True:
            xml = fetch([("search_query", urllib.parse.quote(sq)), ("start", start),
                         ("max_results", 100), ("sortBy", "submittedDate"), ("sortOrder", "ascending")])
            if total is None:
                m = TOTAL.search(xml)
                total = int(m.group(1)) if m else 0
            batch = parse(xml)
            for p in batch:
                papers.setdefault(p["arxiv_id"], p)
                phrase_hits[p["arxiv_id"]].add(phrase)
            start += len(batch)
            print("  A/%-32s %4d/%-4d" % (phrase, start, total), flush=True)
            time.sleep(PACE)
            if not batch or start >= total:
                break
    for aid, ph in phrase_hits.items():
        papers[aid]["phrases"] = "|".join(sorted(ph))
    return papers


def month_bounds(ym):
    y, m = int(ym[:4]), int(ym[5:])
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    return "submittedDate:[%04d%02d010000 TO %04d%02d010000]" % (y, m, ny, nm)


def harvest_cohort_b(month_counts):
    """For each month, draw the same number of cs.AI papers as cohort A has,
    as up to four evenly spaced contiguous blocks across that month's results."""
    papers = {}
    for ym in sorted(month_counts):
        need = month_counts[ym]
        sq = "cat:cs.AI AND " + month_bounds(ym)
        xml = fetch([("search_query", urllib.parse.quote(sq)), ("start", 0), ("max_results", 1)])
        m = TOTAL.search(xml)
        total = int(m.group(1)) if m else 0
        time.sleep(PACE)
        if total == 0:
            print("  B/%s  no control papers" % ym, flush=True)
            continue
        nblocks = min(4, need)
        per = -(-need // nblocks)                      # ceil
        got = 0
        for b in range(nblocks):
            if got >= need:
                break
            span = max(total - per, 0)
            offset = 0 if nblocks == 1 else int(round(b * span / (nblocks - 1))) if nblocks > 1 else 0
            offset = max(0, min(offset, max(total - per, 0)))
            xml = fetch([("search_query", urllib.parse.quote(sq)), ("start", offset),
                         ("max_results", min(per, need - got)),
                         ("sortBy", "submittedDate"), ("sortOrder", "ascending")])
            batch = parse(xml)
            for p in batch:
                if p["arxiv_id"] not in papers:
                    papers[p["arxiv_id"]] = p
                    got += 1
            time.sleep(PACE)
        print("  B/%s  %d of %d wanted (month total %d)" % (ym, got, need, total), flush=True)
    return papers


def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    print("cohort A ...", flush=True)
    A = harvest_cohort_a()
    counts = Counter(p["published"][:7] for p in A.values())
    print("cohort A: %d papers, %d months" % (len(A), len(counts)), flush=True)
    print("cohort B ...", flush=True)
    B = harvest_cohort_b(counts)
    for aid in list(B):
        if aid in A:                                   # a control paper that is also cohort A
            del B[aid]
    print("cohort B: %d papers" % len(B), flush=True)

    with open(os.path.join(outdir, "papers.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["arxiv_id", "cohort", "published", "primary_category", "n_urls", "phrases"])
        for cohort, coll in (("A", A), ("B", B)):
            for aid in sorted(coll):
                p = coll[aid]
                w.writerow([aid, cohort, p["published"], p["primary_category"],
                            len(p["urls"]), p.get("phrases", "")])
    with open(os.path.join(outdir, "urls.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["arxiv_id", "cohort", "published", "url", "host"])
        for cohort, coll in (("A", A), ("B", B)):
            for aid in sorted(coll):
                p = coll[aid]
                for u in p["urls"]:
                    w.writerow([aid, cohort, p["published"], u, urllib.parse.urlparse(u).netloc.lower()])
    meta = {
        "harvested_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "api": API, "window": WINDOW, "phrases": PHRASES,
        "cohort_a_papers": len(A), "cohort_b_papers": len(B),
        "cohort_a_urls": sum(len(p["urls"]) for p in A.values()),
        "cohort_b_urls": sum(len(p["urls"]) for p in B.values()),
    }
    with open(os.path.join(outdir, "harvest.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
