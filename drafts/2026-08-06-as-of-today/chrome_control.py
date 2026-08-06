#!/usr/bin/env python3
"""chrome_control.py — amendment 3. Chrome = a corpus URL that also appears on the host's own
home page, extracted with the same extractor. Fixed before any date signal was collected.
Writes chrome-2.json."""
from __future__ import annotations
import datetime as dt, json
from urllib.parse import urlsplit
from collect_corpus_2 import get, extract, normalise

CORPORA = {}
c2 = json.load(open("corpus-2.json"))
for k, a in c2["authorities"].items():
    if a.get("fetch") == "OK":
        CORPORA[k] = a["corpus"]
CORPORA["EC"] = [normalise(u) for u in json.load(open("corpus.json"))["corpus"]]

out = {"control": "amendment 3 — chrome vs item", "computed_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "authorities": {}}
for key, corpus in CORPORA.items():
    host = urlsplit(corpus[0]).netloc
    home = f"https://{host}/"
    r = get(home)
    if not r.get("ok") or r["status"] != 200:
        out["authorities"][key] = {"home": home, "fetch": "FAILED", "status": r.get("status", 0)}
        continue
    ex = extract(home, r["body"])
    homeset = set(ex["urls"])
    chrome = [u for u in corpus if u in homeset]
    out["authorities"][key] = {
        "home": home, "fetch": "OK", "home_links": len(homeset),
        "corpus_size": len(corpus), "chrome_n": len(chrome), "item_n": len(corpus) - len(chrome),
        "chrome": chrome,
        "items": [u for u in corpus if u not in homeset],
    }
    print(f"{key}: {len(corpus)-len(chrome)} items / {len(chrome)} chrome (home links {len(homeset)})")
json.dump(out, open("chrome-2.json", "w"), indent=1, ensure_ascii=False)
open("chrome-2.json", "a").write("\n")
