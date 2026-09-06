#!/usr/bin/env python3
"""autoloop — stage PRIOR-ART: has this been answered already?

WHY THIS EXISTS
---------------
The loop has six stages — QUESTION, PRE-CHECK, EXPERIMENT, ANALYSIS, WRITE, REVIEW — and not
one of them consults the literature. On 2026-09-05 this practice built a liveness rule, verified
it, published it, and then found in a single query afterwards that the rule had been published in
1990. The loop could not have caught that, because it has no stage that looks.

This is that stage. It is deliberately **mechanical throughout**: no language model is called
anywhere in it. A stage that needs a model to phrase its query is not a stage an unattended loop
can run without a key, a budget and a network dependency the loop cannot audit; and putting a
model inside the instrument would move the thing being measured into the thing measuring it.

WHAT IT DOES
------------
Given a description (free prose of the kind the WRITE stage already emits) it builds three
queries by a fixed rule, sends each to two catalogues that answer an anonymous unauthenticated
request, fuses the six ranked lists by reciprocal rank fusion, and returns the top candidates
with a verdict.

    Q1  the whole description, truncated to 350 characters
    Q2  the 8 highest-ranked content terms
    Q3  the 4 highest-ranked content terms

Content terms: lower-cased, punctuation stripped, stopwords removed, length >= 4, ranked by
frequency, then by descending length, then alphabetically — a total order with no ties.

VERDICT
-------
    PRIOR ART POSSIBLE   some candidate is in the top 3 of at least two of the six lists
    NONE FOUND           otherwise

WHAT IT DOES NOT DO
-------------------
It cannot read. It does not know whether a candidate it returns is the same idea as the
description — only that the words co-occur in catalogues the way the words of the description do.
Judging identity of ideas is not automated here, and this stage does not pretend it is.

CATALOGUES
----------
Crossref and PubMed. Both answer without a key. arXiv's API, OpenAlex and Semantic Scholar were
probed from this address on 2026-09-06 and did not (timeout, 429, 429); `probe()` re-runs that
check and its result is published beside any run.

USAGE
    python3 tools/autoloop/priorart.py --probe
    python3 tools/autoloop/priorart.py --text "some description" [--json out.json]
    python3 tools/autoloop/priorart.py --claims <results.json> --out <priorart.json>
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "meridian-field-research/1.0 (automated research loop; prior-art stage)"
RRF_K = 60
TOP_N = 10
POLITE_SLEEP = 0.4
TIMEOUT = 30

DEFAULT_STOPWORDS = set("""a an and are as at be been being between both but by can cannot could
did do does done down during each either even every for from further gave give given gives had
has have having he her here his how i if in into is it its itself just least less made make makes
many may me might more most much must my neither no not of off on once one only or other others
our out over own per she should so some such take taken takes than that the their them themselves
then there these they this those three to two under until up us use used uses using very was we
were what when where which while who whom whose why with within without would you your""".split())


# --- fetching -------------------------------------------------------------------------

def _get(url, accept="application/json"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def crossref_search(query, rows=TOP_N):
    """Free-text bibliographic query against Crossref."""
    url = ("https://api.crossref.org/works?rows=%d&select=DOI,title,issued,container-title"
           "&query.bibliographic=%s" % (rows, urllib.parse.quote(query)))
    data = json.loads(_get(url))
    out = []
    for it in data["message"]["items"]:
        title = (it.get("title") or [""])[0]
        year = None
        try:
            year = it["issued"]["date-parts"][0][0]
        except Exception:
            pass
        out.append({"catalogue": "crossref", "doi": (it.get("DOI") or "").lower(),
                    "pmid": None, "title": title, "year": year,
                    "venue": (it.get("container-title") or [None])[0]})
    return out


def pubmed_search(query, retmax=TOP_N):
    """Free-text term query against PubMed E-utilities (esearch then esummary)."""
    esearch = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed"
               "&retmode=json&retmax=%d&term=%s" % (retmax, urllib.parse.quote(query)))
    ids = json.loads(_get(esearch))["esearchresult"].get("idlist", [])
    if not ids:
        return []
    time.sleep(POLITE_SLEEP)
    esum = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed"
            "&retmode=json&id=%s" % ",".join(ids))
    res = json.loads(_get(esum))["result"]
    out = []
    for pid in ids:
        rec = res.get(pid) or {}
        doi = ""
        for aid in rec.get("articleids", []):
            if aid.get("idtype") == "doi":
                doi = (aid.get("value") or "").lower()
        year = None
        m = re.match(r"(\d{4})", rec.get("pubdate", "") or "")
        if m:
            year = int(m.group(1))
        out.append({"catalogue": "pubmed", "doi": doi, "pmid": pid,
                    "title": rec.get("title", ""), "year": year,
                    "venue": rec.get("source")})
    return out


CATALOGUES = {"crossref": crossref_search, "pubmed": pubmed_search}


def probe():
    """Which catalogues answer an anonymous unauthenticated request from this address?"""
    targets = {
        "crossref": "https://api.crossref.org/works?rows=1&query.bibliographic=calibration",
        "pubmed": ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed"
                   "&retmode=json&retmax=1&term=calibration"),
        "arxiv": "https://export.arxiv.org/api/query?search_query=all:calibration&max_results=1",
        "openalex": "https://api.openalex.org/works?search=calibration&per-page=1",
        "semanticscholar": ("https://api.semanticscholar.org/graph/v1/paper/search"
                            "?query=calibration&limit=1"),
    }
    out = {}
    for name, url in targets.items():
        t0 = time.time()
        try:
            body = _get(url, accept="*/*")
            ok = True
            detail = "%d bytes" % len(body)
            if '"code": "429"' in body or "Rate exceeded" in body:
                ok, detail = False, "rate limited in body: " + body.strip()[:80]
        except Exception as e:
            ok, detail = False, type(e).__name__ + ": " + str(e)[:120]
        out[name] = {"reachable": ok, "detail": detail, "seconds": round(time.time() - t0, 1)}
        time.sleep(POLITE_SLEEP)
    return out


# --- query construction ---------------------------------------------------------------

def content_terms(text, stopwords=None):
    stop = set(stopwords) if stopwords else DEFAULT_STOPWORDS
    words = re.findall(r"[a-z]+", (text or "").lower())
    freq = {}
    for w in words:
        if len(w) < 4 or w in stop:
            continue
        freq[w] = freq.get(w, 0) + 1
    return sorted(freq, key=lambda w: (-freq[w], -len(w), w))


def build_queries(description, stopwords=None):
    terms = content_terms(description, stopwords)
    return [
        {"id": "Q1", "kind": "full-text", "q": description[:350]},
        {"id": "Q2", "kind": "top-8-terms", "q": " ".join(terms[:8])},
        {"id": "Q3", "kind": "top-4-terms", "q": " ".join(terms[:4])},
    ]


# --- the stage ------------------------------------------------------------------------

def key_of(cand):
    return cand["doi"] if cand["doi"] else "title:" + norm_title(cand["title"])


def assess(description, stopwords=None, catalogues=None, log=None):
    """Run the stage on one description. Returns fused candidates and a verdict."""
    cats = catalogues or list(CATALOGUES)
    queries = build_queries(description, stopwords)
    lists, errors = [], []
    t0 = time.time()
    calls = 0
    for cat in cats:
        for q in queries:
            calls += 1
            try:
                res = CATALOGUES[cat](q["q"])
            except Exception as e:
                errors.append({"catalogue": cat, "query": q["id"],
                               "error": type(e).__name__ + ": " + str(e)[:120]})
                res = []
            lists.append({"catalogue": cat, "query": q["id"], "q": q["q"],
                          "results": res})
            if log is not None:
                log.append({"catalogue": cat, "query": q["id"], "q": q["q"],
                            "keys": [key_of(c) for c in res]})
            time.sleep(POLITE_SLEEP)

    fused = {}
    for lst in lists:
        for rank, cand in enumerate(lst["results"], start=1):
            k = key_of(cand)
            e = fused.setdefault(k, {"key": k, "doi": cand["doi"], "pmid": cand["pmid"],
                                     "title": cand["title"], "year": cand["year"],
                                     "venue": cand["venue"], "score": 0.0, "found_by": [],
                                     "best_rank": rank})
            e["score"] += 1.0 / (RRF_K + rank)
            e["found_by"].append({"catalogue": lst["catalogue"], "query": lst["query"],
                                  "rank": rank})
            e["best_rank"] = min(e["best_rank"], rank)
            if not e["pmid"] and cand["pmid"]:
                e["pmid"] = cand["pmid"]
            if not e["doi"] and cand["doi"]:
                e["doi"] = cand["doi"]
    ranked = sorted(fused.values(), key=lambda e: (-e["score"], e["best_rank"], e["key"]))

    # VERDICT, fixed in the pre-registration: some candidate in the top 3 of >= 2 of the lists.
    top3_counts = {}
    for lst in lists:
        for cand in lst["results"][:3]:
            k = key_of(cand)
            top3_counts[k] = top3_counts.get(k, 0) + 1
    verdict_keys = sorted([k for k, c in top3_counts.items() if c >= 2],
                          key=lambda k: -top3_counts[k])
    verdict = "PRIOR ART POSSIBLE" if verdict_keys else "NONE FOUND"

    return {
        "queries": queries,
        "lists": [{"catalogue": l["catalogue"], "query": l["query"], "q": l["q"],
                   "n": len(l["results"]),
                   "results": [{"doi": c["doi"], "pmid": c["pmid"], "title": c["title"],
                                "year": c["year"], "venue": c["venue"]} for c in l["results"]]}
                  for l in lists],
        "candidates": ranked[:TOP_N],
        "verdict": verdict,
        "verdict_keys": verdict_keys,
        "calls": calls,
        "errors": errors,
        "seconds": round(time.time() - t0, 1),
    }


def confirm_target(title, doi=None, pmid=None):
    """Look a proposed target up BY TITLE and report whether the record exists.

    Separate from the measurement: these queries are not counted in it.
    """
    out = {"title": title, "doi": doi, "pmid": pmid, "crossref": None, "pubmed": None}
    want_doi = (doi or "").lower()
    try:
        for c in crossref_search(title, rows=5):
            if c["doi"] == want_doi:
                out["crossref"] = {"doi": c["doi"], "title": c["title"], "year": c["year"],
                                   "venue": c["venue"]}
                break
    except Exception as e:
        out["crossref"] = {"error": type(e).__name__ + ": " + str(e)[:120]}
    time.sleep(POLITE_SLEEP)
    try:
        for c in pubmed_search(title, retmax=5):
            if (pmid and c["pmid"] == pmid) or (want_doi and c["doi"] == want_doi):
                out["pubmed"] = {"pmid": c["pmid"], "doi": c["doi"], "title": c["title"],
                                 "year": c["year"], "venue": c["venue"]}
                break
    except Exception as e:
        out["pubmed"] = {"error": type(e).__name__ + ": " + str(e)[:120]}
    ok = lambda v: isinstance(v, dict) and "error" not in v
    out["confirmed"] = bool(ok(out["crossref"]) or ok(out["pubmed"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--text")
    ap.add_argument("--claims", help="a loop results.json; runs the stage on its claim sentences")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--out")
    args = ap.parse_args()

    if args.probe:
        res = probe()
        print(json.dumps(res, indent=1))
        return

    if args.text:
        res = assess(args.text)
        print(f"{res['verdict']}  ({res['calls']} calls, {res['seconds']} s)", file=sys.stderr)
        for c in res["candidates"][:5]:
            print(f"  {c['score']:.4f}  {c['doi'] or c['pmid'] or ''}  {c['title'][:90]}")
        if args.out:
            with open(args.out, "w") as f:
                json.dump(res, f, indent=1)
        return

    if args.claims:
        with open(args.claims) as f:
            results = json.load(f)
        sentences = [c for c in results["claims"] if c.get("sentence")][:args.limit]
        out = []
        for c in sentences:
            r = assess(c["sentence"])
            out.append({"key": c["key"], "sentence": c["sentence"], "verdict": r["verdict"],
                        "calls": r["calls"], "seconds": r["seconds"],
                        "top": [{"doi": x["doi"], "pmid": x["pmid"], "title": x["title"],
                                 "year": x["year"], "score": round(x["score"], 5)}
                                for x in r["candidates"][:3]],
                        "errors": r["errors"]})
            print(f"{c['key']}: {r['verdict']} ({r['seconds']} s)", file=sys.stderr)
        payload = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "n": len(out), "items": out,
                   "verdict_counts": {v: sum(1 for o in out if o["verdict"] == v)
                                      for v in ("PRIOR ART POSSIBLE", "NONE FOUND")}}
        if args.out:
            with open(args.out, "w") as f:
                json.dump(payload, f, indent=1)
        else:
            print(json.dumps(payload, indent=1))
        return

    ap.error("one of --probe, --text or --claims is required")


if __name__ == "__main__":
    main()
