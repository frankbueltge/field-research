#!/usr/bin/env python3
"""extractor_vs_hand_139 - the banned extractor's count beside the hand count, on the twenty drawn files.

Session 139, 2026-08-30. `PREREGISTRATION-138B.md` section 1 bans repairing `extract_units_137_v2.py`.
It does not ban MEASURING it, and this script does not touch it: it reads the counts v2 already
recorded in `units-manifest-137-v2.json` and puts them beside the hand delimitation.

THE COMPARISON IS ONLY DEFINED WHERE THE TWO COUNTERS AGREED. On a SPLIT file there is no single
hand count to compare against, and the row says so rather than picking one.

AN UNEXTRACTABLE FILE IS REPORTED AS ITS OWN CATEGORY, not as a disagreement of unknown size:
`CONDITIONS-138.md` item 5 established that v2's MIN_UNITS floor of 3 reports a two-finding report
as UNEXTRACTABLE, which is a property of the threshold and not of the report.

**Every figure here is a COUNT over twenty files. It is not a rate and may not be divided by 53.**
"""
import json

d = json.load(open("draw-139.json", encoding="utf-8"))
m = json.load(open("units-manifest-137-v2.json", encoding="utf-8"))
v2 = {r["file"].split("/")[-1]: r for r in m["manifest"]}

hand = {}
for b in ("1", "2"):
    c = json.load(open("compare-139-batch-%s.json" % b, encoding="utf-8"))
    for r in c["rows"]:
        hand[r["file"]] = r

rows = []
for name in sorted(hand):
    h, v = hand[name], v2[name]
    if h["verdict"] in ("DELIMITED",):
        hc = h["count_a"]
        if v["status"] == "UNEXTRACTABLE":
            verdict = "V2-UNEXTRACTABLE"
        elif v["units"] == hc:
            verdict = "AGREE"
        else:
            verdict = "DISAGREE"
    else:
        hc = "%s / %s" % (h["count_a"], h["count_b"])
        verdict = "NO-SINGLE-HAND-COUNT"
    rows.append({"file": name, "hand": hc, "v2": (v["units"] if v["status"] == "EXTRACTED"
                                                  else "UNEXTRACTABLE"),
                 "v2_family": v["family"], "delimitation": h["verdict"], "verdict": verdict})

tally = {}
for r in rows:
    tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
json.dump({"note": "counts over the twenty files of draw-139.json; NOT a rate, NOT divisible by 53",
           "tally": tally, "rows": rows},
          open("extractor-vs-hand-139.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("%-24s %-10s %-14s %-10s %s" % ("file", "hand", "v2", "family", "verdict"))
for r in rows:
    print("%-24s %-10s %-14s %-10s %s" % (r["file"], r["hand"], r["v2"], r["v2_family"],
                                          r["verdict"]))
print("\ntally:", tally)
