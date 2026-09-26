#!/usr/bin/env python3
"""Corpus W: the accepted papers of Agents4Science 2025, matched to arXiv. Session 171, 2026-09-26.

Raw pages and texts are written OUTSIDE the repository (protocol §7); the artifact carries
identifiers, titles and digests only. Match rule: PREREGISTRATION.md §2.
"""
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

WORK = sys.argv[1]
LIST_URL = "https://agents4science.stanford.edu/accepted-papers.html"
UA = {"User-Agent": "field-research/1.0 (meridian@field-research.invalid)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status, r.read().decode("utf-8", "replace")


def norm(t):
    t = html.unescape(t).lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def title_match(a, b):
    a, b = norm(a), norm(b)
    if a == b:
        return True
    short, long_ = sorted((a, b), key=len)
    return long_.startswith(short) and len(short.split()) >= 8


def listed_papers(page):
    """Every card: title, authors, blurb (where the card has one), OpenReview id, tier."""
    cards = []
    for m in re.finditer(r'<h[34] class="paper(?:-item)?-title">(.*?)</h[34]>', page, flags=re.S):
        nxt = page.find('openreview.net/forum?id=', m.end())
        chunk = page[m.end():nxt]
        au = re.search(r'class="paper(?:-item)?-authors">(.*?)</div>', chunk, flags=re.S)
        ab = re.search(r'class="paper-abstract">(.*?)</p>', chunk, flags=re.S)
        orid = re.match(r'openreview\.net/forum\?id=([A-Za-z0-9_-]+)', page[nxt:]).group(1)
        clean = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x))).strip()
        cards.append({"openreview": orid, "title": clean(m.group(1)),
                      "authors": clean(au.group(1)) if au else "",
                      "blurb": clean(ab.group(1)) if ab else "",
                      "tier": "listed" if "item" in m.group(0) else "presented"})
    return cards


def arxiv_search(title):
    q = urllib.parse.urlencode({"query": " ".join(norm(title).split()[:12]), "searchtype": "title", "size": 25,
                                "abstracts": "show"})
    st, page = get("https://arxiv.org/search/?" + q)
    hits = []
    for li in re.findall(r'<li class="arxiv-result">(.*?)</li>\s*(?=<li class="arxiv-result">|</ol>)',
                         page, flags=re.S):
        idm = re.search(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', li)
        tm = re.search(r'<p class="title is-5 mathjax">(.*?)</p>', li, flags=re.S)
        am = re.search(r'<span class="abstract-full[^"]*"[^>]*>(.*?)<a', li, flags=re.S)
        if idm and tm:
            hits.append({"id": idm.group(1),
                         "title": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", tm.group(1))).strip(),
                         "abstract": re.sub(r"\s+", " ", html.unescape(
                             re.sub(r"<[^>]+>", "", am.group(1)))).strip() if am else ""})
    return hits


def main():
    os.makedirs(os.path.join(WORK, "html"), exist_ok=True)
    st, page = get(LIST_URL)
    open(os.path.join(WORK, "accepted-papers.html"), "w").write(page)
    cards = listed_papers(page)
    print(f"list: {len(cards)} cards, sha256 {hashlib.sha256(page.encode()).hexdigest()[:16]}")
    res = []
    for c in cards:
        rec = dict(c)
        try:
            hits = arxiv_search(c["title"])
        except Exception as e:
            hits, rec["search_error"] = [], repr(e)
        m = [h for h in hits if title_match(h["title"], c["title"])]
        rec["arxiv_candidates"] = len(hits)
        if m:
            h = sorted(m, key=lambda x: x["id"])[0]
            rec.update(arxiv=h["id"], arxiv_title=h["title"], arxiv_abstract=h["abstract"])
            url = f"https://arxiv.org/html/{h['id']}"
            try:
                st, doc = get(url)
                path = os.path.join(WORK, "html", h["id"] + ".html")
                open(path, "w").write(doc)
                rec["html_status"] = st
                rec["html_sha256"] = hashlib.sha256(doc.encode()).hexdigest()
            except Exception as e:
                rec["html_status"] = getattr(e, "code", None) or repr(e)
        res.append(rec)
        print(rec["openreview"], rec.get("arxiv"), rec.get("html_status"), c["title"][:60])
        time.sleep(3)
    json.dump({"list_url": LIST_URL,
               "list_sha256": hashlib.sha256(page.encode()).hexdigest(),
               "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "papers": res}, open(os.path.join(WORK, "match.json"), "w"), indent=1,
              ensure_ascii=False)


if __name__ == "__main__":
    main()
