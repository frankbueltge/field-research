#!/usr/bin/env python3
"""autoloop — stage DATA.

Fetches a corpus from the arXiv Atom API and writes a feature table.

What is written: derived numbers and booleans plus the bare arXiv identifier.
What is never written: titles, abstracts, author names, comment strings. Third-party
text does not enter this repository (.github/workflows/no-committed-sources.yml); the
features below are measurements of that text, not the text.

Every failure is recorded in the break log rather than raised, so that a stage failure
is a measurement of the loop and not the end of the run.

Usage:  python3 tools/autoloop/fetch.py --out <corpus.json> [--per-cat 300]
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

API = "https://export.arxiv.org/api/query"
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

# Fixed in PREREGISTRATION.md §2 before any datum was fetched.
CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "cs.RO", "cs.SE", "stat.ML", "cs.CY"]
PAGE = 100
POLITE_SECONDS = 3.0

PAGES_RE = re.compile(r"(\d+)\s*pages?\b", re.I)


def _text(entry, path):
    el = entry.find(path, NS)
    return el.text if el is not None and el.text else ""


def _parse_dt(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def features(entry):
    """Derive one record. Returns None when the entry lacks the identifiers we key on."""
    raw_id = _text(entry, "a:id")
    m = re.search(r"abs/([^v]+)v(\d+)", raw_id)
    if not m:
        return None
    arxiv_id, version = m.group(1), int(m.group(2))

    published = _parse_dt(_text(entry, "a:published"))
    updated = _parse_dt(_text(entry, "a:updated"))
    title = _text(entry, "a:title")
    summary = _text(entry, "a:summary")
    comment = _text(entry, "arxiv:comment")
    doi = _text(entry, "arxiv:doi")
    journal_ref = _text(entry, "arxiv:journal_ref")

    cats = [c.get("term") for c in entry.findall("a:category", NS) if c.get("term")]
    prim_el = entry.find("arxiv:primary_category", NS)
    primary = prim_el.get("term") if prim_el is not None else (cats[0] if cats else "")
    authors = entry.findall("a:author", NS)

    pages = None
    if comment:
        pm = PAGES_RE.search(comment)
        if pm:
            try:
                v = int(pm.group(1))
                pages = v if 1 <= v <= 500 else None
            except ValueError:
                pages = None

    return {
        "id": arxiv_id,
        "version": version,
        "primary_category": primary,
        "category_count": len(set(cats)),
        "crosslist_count": max(0, len(set(cats)) - 1),
        "published_weekday": published.weekday(),          # 0 = Monday
        "published_hour_utc": published.hour,
        "published_date": published.strftime("%Y-%m-%d"),
        "title_words": len(title.split()),
        "abstract_words": len(summary.split()),
        "author_count": len(authors),
        "has_doi": bool(doi.strip()),
        "has_journal_ref": bool(journal_ref.strip()),
        "has_comment": bool(comment.strip()),
        "comment_pages": pages,
        "revised": updated > published,
    }


def fetch_page(cat, start, per_page, breaks):
    url = (
        f"{API}?search_query=cat:{cat}&start={start}&max_results={per_page}"
        "&sortBy=submittedDate&sortOrder=descending"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "field-research autoloop (meridian@field-research.invalid)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        breaks.append({"stage": "DATA", "kind": "fetch_error", "where": f"{cat}@{start}", "detail": str(e)[:200]})
        return []
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        breaks.append({"stage": "DATA", "kind": "parse_error", "where": f"{cat}@{start}", "detail": str(e)[:200]})
        return []
    out = []
    for entry in root.findall("a:entry", NS):
        try:
            rec = features(entry)
        except Exception as e:                                    # a malformed entry is a break, not a crash
            breaks.append({"stage": "DATA", "kind": "feature_error", "where": f"{cat}@{start}", "detail": str(e)[:200]})
            continue
        if rec is None:
            breaks.append({"stage": "DATA", "kind": "unkeyed_entry", "where": f"{cat}@{start}", "detail": "no arXiv id"})
            continue
        out.append(rec)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-cat", type=int, default=300)
    ap.add_argument("--breaks", default=None, help="where to write the break log")
    args = ap.parse_args()

    breaks = []
    by_id = {}
    counts = {}
    t0 = time.time()
    for cat in CATEGORIES:
        got = 0
        for start in range(0, args.per_cat, PAGE):
            recs = fetch_page(cat, start, min(PAGE, args.per_cat - start), breaks)
            if not recs:
                break
            for rec in recs:
                got += 1
                by_id.setdefault(rec["id"], rec)
            time.sleep(POLITE_SECONDS)
        counts[cat] = got
        print(f"  {cat}: {got} entries", file=sys.stderr)

    corpus = {
        "fetched_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "arXiv Atom API, export.arxiv.org/api/query",
        "queries": [f"cat:{c} sortBy=submittedDate desc, {args.per_cat} requested" for c in CATEGORIES],
        "returned_per_category": counts,
        "records_deduplicated": len(by_id),
        "seconds": round(time.time() - t0, 1),
        "records": [by_id[k] for k in sorted(by_id)],
    }
    with open(args.out, "w") as f:
        json.dump(corpus, f, indent=1, sort_keys=True)
    if args.breaks:
        with open(args.breaks, "w") as f:
            json.dump(breaks, f, indent=1)
    print(f"corpus: {len(by_id)} records, {len(breaks)} breaks -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
