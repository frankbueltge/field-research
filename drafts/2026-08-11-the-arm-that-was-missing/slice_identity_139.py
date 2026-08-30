#!/usr/bin/env python3
"""slice_identity_139 - where v2 agreed on the count, did it carve the same text?

Session 139, 2026-08-30. "12 AGREE" in `extractor-vs-hand-139.json` compares COUNTS. A count can
agree while the text does not: two carvings of one file into nine pieces need not be the same nine
pieces. This script checks the stronger property, which nothing in this arc had checked before.

A TRAP THIS SCRIPT EXISTS TO AVOID, recorded because this session fell into it first.
`units-137-v2.json` is written SHUFFLED - `extract_units_137_v2.main()` calls
`rng.shuffle(shuffled)` under `SHUFFLE_SEED = 137` before dumping, because the file is a
classification payload and unit order would leak document order. A comparison that reads the two
files in list order therefore compares shuffled v2 units against ordinal hand units and reports
total disagreement. This session's first pass did exactly that and reported 0 of 12 identical, which
was an artefact of the read and not a fact about the carves. **The units must be joined on the
manifest's `ordinal`, and that is what this does.** The wrong figure was never published.
"""
import json

hand = json.load(open("units-139.json", encoding="utf-8"))
hand_km = json.load(open("units-manifest-139.json", encoding="utf-8"))["key_map"]
v2 = json.load(open("units-137-v2.json", encoding="utf-8"))
v2_km = json.load(open("units-manifest-137-v2.json", encoding="utf-8"))["key_map"]
rows = json.load(open("extractor-vs-hand-139.json", encoding="utf-8"))["rows"]
agree = {r["file"] for r in rows if r["verdict"] == "AGREE"}


def by_file(units, km):
    d = {}
    for u in units:
        m = km[u["key"]]
        f = m["file"].split("/")[-1]
        if f in agree:
            d.setdefault(f, []).append((m["ordinal"], u["text"]))
    return {f: [t for _, t in sorted(v)] for f, v in d.items()}


A, B = by_file(hand, hand_km), by_file(v2, v2_km)
same = sorted(f for f in A if A[f] == B[f])
diff = sorted(f for f in A if A[f] != B[f])
out = {"files_compared": len(A), "byte_identical": same, "differing": diff,
       "units_compared": sum(len(v) for v in A.values()),
       "join": "on units-manifest ordinal, NOT list order - units-137-v2.json is shuffled"}
json.dump(out, open("slice-identity-139.json", "w", encoding="utf-8"), indent=1,
          ensure_ascii=False)
print("files where v2's count agreed with the hand count: %d" % len(A))
print("of those, slice sets byte-identical to v2's: %d" % len(same))
print("units compared: %d" % out["units_compared"])
for f in diff:
    print("DIFFERS %s" % f)
