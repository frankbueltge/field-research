#!/usr/bin/env python3
"""Second pass for the first pass's misses, a different request shape. Session 171, 2026-09-26.

Amendment A-1 (written after the first pass was seen, see PREREGISTRATION.md): each paper the
first pass did not find is searched again with its five longest title words instead of its
first twelve. The admission rule (title match, §2) is unchanged. Retitled arXiv versions are
NOT admitted; the nearest candidate title is printed so a reader can see what was refused.
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch                                                         # noqa: E402

WORK = sys.argv[1]
STOP = {"with", "from", "that", "their", "using", "through", "towards", "beyond", "large",
        "language", "models", "model"}


def main():
    path = os.path.join(WORK, "match.json")
    d = json.load(open(path))
    for p in d["papers"]:
        if p.get("arxiv"):
            continue
        words = [w for w in fetch.norm(p["title"]).split() if w not in STOP]
        q = sorted(words, key=lambda w: (-len(w), words.index(w)))[:5]
        try:
            import urllib.parse
            qs = urllib.parse.urlencode({"query": " ".join(q), "searchtype": "title", "size": 25,
                                         "abstracts": "show"})
            st, page = fetch.get("https://arxiv.org/search/?" + qs)
            hits = []
            for li in re.findall(r'<li class="arxiv-result">(.*?)</li>\s*(?=<li class="arxiv-result">|</ol>)',
                                 page, flags=re.S):
                idm = re.search(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', li)
                tm = re.search(r'<p class="title is-5 mathjax">(.*?)</p>', li, flags=re.S)
                if idm and tm:
                    hits.append({"id": idm.group(1), "title": re.sub(
                        r"\s+", " ", re.sub(r"<[^>]+>", "", tm.group(1))).strip()})
        except Exception as e:
            hits = []
            p["recheck_error"] = repr(e)
        p["recheck_query"] = " ".join(q)
        p["recheck_candidates"] = [h["title"] for h in hits[:3]]
        m = [h for h in hits if fetch.title_match(h["title"], p["title"])]
        if m:
            h = sorted(m, key=lambda x: x["id"])[0]
            p.update(arxiv=h["id"], arxiv_title=h["title"], found_on="recheck")
            try:
                st, doc = fetch.get(f"https://arxiv.org/html/{h['id']}")
                open(os.path.join(WORK, "html", h["id"] + ".html"), "w").write(doc)
                p["html_status"] = st
                import hashlib
                p["html_sha256"] = hashlib.sha256(doc.encode()).hexdigest()
            except Exception as e:
                p["html_status"] = getattr(e, "code", None) or repr(e)
        print(p["openreview"], p.get("arxiv"), len(hits), "|", p["title"][:50], "||",
              (hits[0]["title"][:60] if hits else "-"), flush=True)
        time.sleep(3)
    d["rechecked_at_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    json.dump(d, open(path, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
