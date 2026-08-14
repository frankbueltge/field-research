#!/usr/bin/env python3
"""Has the field already done this? — the house catalogues, asked before the claim is made.

Session 119. The question tonight's work would be embarrassed by: is "a practice auditing its
own stored measurement record against itself" a move somebody has already made, better?

The two catalogues are FEEDS and are **never mirrored into this repository** — a copy drifts
from the original from the first day. This file fetches them live and writes only *results*:
per-term hit counts and the titles of what was hit, so the claim is reproducible without a
copy. `SITE-API.md` documents the shapes.

  atlas   https://frankbueltge.de/atlas/werke.json     — neighbouring works of data art
  papers  https://frankbueltge.de/papers/index.json    — papers read or examined in this ecology

A negative result from a catalogue is evidence and is recorded as such. An unreachable
catalogue is a fact about the session and is recorded as that — never as an empty result.
"""
import json
import time
import urllib.request

UA = "field-research/1.0 (independent research instrument)"
FEEDS = {"atlas": "https://frankbueltge.de/atlas/werke.json",
         "papers": "https://frankbueltge.de/papers/index.json"}

TERMS = ["self-audit", "audit", "integrity", "reproducib", "verification", "instrument error",
         "measurement error", "calibrat", "error correction", "data quality", "quality control",
         "artefact", "provenance", "own data", "internal consistency"]


def rows(obj):
    """Both feeds wrap their list; find it without assuming a key name."""
    if isinstance(obj, list):
        return obj
    for k in ("werke", "entries", "papers", "items", "works"):
        v = obj.get(k)
        if isinstance(v, list):
            return v
    for v in obj.values():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v
    return []


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r), r.status


def main():
    out = {"schema": "field-research/catalogue-check/1", "session": 119,
           "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "not_mirrored": ("Only counts and titles are stored. The catalogues themselves are "
                            "feeds and are never copied into this repository."),
           "feeds": {}}
    for name, url in FEEDS.items():
        try:
            data, status = fetch(url)
        except Exception as e:
            out["feeds"][name] = {"url": url, "reachable": False,
                                  "error": type(e).__name__ + ": " + str(e)[:200],
                                  "note": ("unreachable — recorded as a fact about this session, "
                                           "not as an empty result")}
            continue
        rs = rows(data)
        hits = {}
        for t in TERMS:
            h = [r for r in rs if t in json.dumps(r, ensure_ascii=False).lower()]
            hits[t] = {"n": len(h),
                       "titles": [(r.get("title") or r.get("titel") or "")[:120] for r in h][:8]}
        out["feeds"][name] = {"url": url, "http": status, "reachable": True,
                              "n_entries": len(rs), "terms": hits}
    json.dump(out, open("neighbours-119.json", "w"), indent=1)
    for name, f in out["feeds"].items():
        if not f.get("reachable"):
            print(name, "UNREACHABLE", f.get("error"))
            continue
        print(f'{name}: {f["n_entries"]} entries')
        for t, h in f["terms"].items():
            if h["n"]:
                print(f'   {t!r}: {h["n"]}')
    print("wrote neighbours-119.json")


if __name__ == "__main__":
    main()
