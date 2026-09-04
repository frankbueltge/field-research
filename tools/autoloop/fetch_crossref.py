#!/usr/bin/env python3
"""autoloop — stage DATA, second world.

Fetches a corpus from the Crossref REST API and writes a feature table with the same
contract as fetch.py: derived numbers and booleans plus a bare identifier, and nothing else.

What is never written: titles, abstracts, author names, journal names, licence URLs. Third-party
text does not enter this repository (.github/workflows/no-committed-sources.yml); the features
below are measurements of that text, not the text. The abstract is read only to count its words.

Why Crossref and not OpenAlex: OpenAlex was tried first and answered HTTP 429 to every request
after the first from this address (PREREGISTRATION.md §2). Crossref is not among the 82 entries
of the house's dataset register, so this is also the reach-outside session protocol v4 §5.3 owes
once per cycle.

Every failure is recorded in the break log rather than raised, so that a stage failure is a
measurement of the loop and not the end of the run.

Usage:  python3 tools/autoloop/fetch_crossref.py --out <corpus.json> [--per-member 300]
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from datetime import date, datetime, timezone

API = "https://api.crossref.org/works"
UA = "field-research autoloop (+https://frankbueltge.de; mailto:meridian@field-research.invalid)"

# Fixed in PREREGISTRATION.md §2 before any datum was fetched.
MEMBERS = {
    78: "Elsevier BV",
    297: "Springer Science and Business Media LLC",
    311: "Wiley",
    1968: "MDPI AG",
    301: "Informa UK Limited",
    1965: "Frontiers Media SA",
    286: "Oxford University Press (OUP)",
    179: "SAGE Publications",
}
FROM_PUB_DATE = "2026-06-01"
PAGE = 100
POLITE_SECONDS = 2.0
RETRIES = 4

TAG_RE = re.compile(r"<[^>]+>")


def _first(v):
    if isinstance(v, list):
        return v[0] if v else ""
    return v or ""


def _doy(parts):
    """Day of year from a Crossref date-parts triple; None when the date is not a full date."""
    try:
        y, m, d = parts[0], parts[1], parts[2]
        return date(int(y), int(m), int(d)).timetuple().tm_yday
    except Exception:
        return None


def features(item):
    """Derive one record. Returns None when the item lacks the identifier we key on."""
    doi = (item.get("DOI") or "").strip().lower()
    if not doi:
        return None

    authors = item.get("author") or []
    abstract = item.get("abstract") or ""
    abstract_plain = TAG_RE.sub(" ", abstract).strip()
    title = _first(item.get("title"))

    issued = (item.get("issued") or {}).get("date-parts") or [[]]
    doy = _doy(issued[0] if issued else [])

    refs = item.get("reference-count")
    cited = item.get("is-referenced-by-count")

    return {
        "id": doi,
        "member": int(item.get("member")) if str(item.get("member", "")).isdigit() else None,
        "title_words": len(title.split()) if title else None,
        "abstract_words": len(abstract_plain.split()) if abstract_plain else None,
        "author_count": len(authors),
        "reference_count": int(refs) if isinstance(refs, int) else None,
        "cited_by_count": int(cited) if isinstance(cited, int) else None,
        "published_doy": doy,
        "has_license": bool(item.get("license")),
        "has_abstract": bool(abstract_plain),
        "has_orcid": any(a.get("ORCID") for a in authors),
        "has_funder": bool(item.get("funder")),
        "has_fulltext_link": bool(item.get("link")),
    }


def fetch_page(member, offset, rows, breaks):
    q = urllib.parse.urlencode({
        "filter": f"type:journal-article,member:{member},from-pub-date:{FROM_PUB_DATE}",
        "rows": rows,
        "offset": offset,
        "sort": "deposited",
        "order": "desc",
    })
    url = f"{API}?{q}"
    body = None
    for attempt in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                body = r.read()
            break
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
            if attempt == RETRIES - 1:
                breaks.append({"stage": "DATA", "kind": "fetch_error",
                               "where": f"member{member}@{offset}", "detail": str(e)[:200]})
                return []
            time.sleep(3.0 * (attempt + 1))
    try:
        payload = json.loads(body)
    except ValueError as e:
        breaks.append({"stage": "DATA", "kind": "parse_error",
                       "where": f"member{member}@{offset}", "detail": str(e)[:200]})
        return []
    items = (payload.get("message") or {}).get("items") or []
    out = []
    for item in items:
        try:
            rec = features(item)
        except Exception as e:                                # a malformed item is a break, not a crash
            breaks.append({"stage": "DATA", "kind": "feature_error",
                           "where": f"member{member}@{offset}", "detail": str(e)[:200]})
            continue
        if rec is None:
            breaks.append({"stage": "DATA", "kind": "unkeyed_item",
                           "where": f"member{member}@{offset}", "detail": "no DOI"})
            continue
        out.append(rec)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-member", type=int, default=300)
    ap.add_argument("--breaks", default=None)
    args = ap.parse_args()

    breaks = []
    by_id = {}
    counts = {}
    requests_made = 0
    t0 = time.time()
    for member in MEMBERS:
        got = 0
        for offset in range(0, args.per_member, PAGE):
            requests_made += 1
            recs = fetch_page(member, offset, min(PAGE, args.per_member - offset), breaks)
            if not recs:
                break
            for rec in recs:
                got += 1
                by_id.setdefault(rec["id"], rec)
            time.sleep(POLITE_SECONDS)
        counts[str(member)] = got
        print(f"  member {member} ({MEMBERS[member]}): {got} items", file=sys.stderr)

    corpus = {
        "fetched_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Crossref REST API, api.crossref.org/works",
        "queries": [f"type:journal-article member:{m} from-pub-date:{FROM_PUB_DATE} "
                    f"sort=deposited desc, {args.per_member} requested" for m in MEMBERS],
        "member_names": {str(k): v for k, v in MEMBERS.items()},
        "returned_per_category": counts,
        "requests_made": requests_made,
        "records_deduplicated": len(by_id),
        "seconds": round(time.time() - t0, 1),
        "records": [by_id[k] for k in sorted(by_id)],
    }
    with open(args.out, "w") as f:
        json.dump(corpus, f, indent=1, sort_keys=True)
    if args.breaks:
        with open(args.breaks, "w") as f:
            json.dump(breaks, f, indent=1)
    print(f"corpus: {len(by_id)} records, {len(breaks)} breaks, {requests_made} requests -> {args.out}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
