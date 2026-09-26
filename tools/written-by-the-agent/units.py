#!/usr/bin/env python3
"""Run the 09-23 rule, unchanged, over corpus W's full texts. Session 171, 2026-09-26.

Writes texts and the full unit list OUTSIDE the repository; prints a summary. The sample of
60 not_recomputable units is drawn here, after the unit list is fixed (seed 20260926).
"""
import hashlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "a-number-you-cannot-check"))
sys.path.insert(0, HERE)
from handover import analyse          # noqa: E402  (imported, not copied)
from extract import extract           # noqa: E402

WORK = sys.argv[1]
SEED = 20260926
SAMPLE = 60


def main():
    match = json.load(open(os.path.join(WORK, "match.json")))
    os.makedirs(os.path.join(WORK, "text"), exist_ok=True)
    units, docs = [], []
    for p in match["papers"]:
        if p.get("html_status") != 200:
            continue
        raw = open(os.path.join(WORK, "html", p["arxiv"] + ".html"), encoding="utf-8").read()
        text = extract(raw)
        open(os.path.join(WORK, "text", p["arxiv"] + ".txt"), "w", encoding="utf-8").write(text)
        toks = analyse(text, doc_id=p["arxiv"])
        docs.append({"arxiv": p["arxiv"], "openreview": p["openreview"],
                     "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                     "words": len(text.split()), "tokens": len(toks)})
        for i, t in enumerate(toks):
            t["uid"] = f"{p['arxiv']}#{i}"
        units.extend(toks)
    nonrec = [u["uid"] for u in units if u["verdict"] == "not_recomputable"]
    rng = random.Random(SEED)
    sample = sorted(rng.sample(nonrec, min(SAMPLE, len(nonrec))),
                    key=lambda x: (x.split("#")[0], int(x.split("#")[1])))
    json.dump({"docs": docs, "units": units, "sample": sample},
              open(os.path.join(WORK, "units.json"), "w"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(docs), "docs;", len(units), "tokens;", Counter(u["verdict"] for u in units))


if __name__ == "__main__":
    main()
