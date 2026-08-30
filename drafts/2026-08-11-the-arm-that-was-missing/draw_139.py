#!/usr/bin/env python3
"""draw_139 - the seeded draw and the batch split of PREREGISTRATION-139.md.

Session 139, 2026-08-30. The seed (1390), the pool rule, the sample size (20) and the batch-split
rule were all committed at 51a36bf, 03:39:14Z, BEFORE this script existed and before the day-17
probe fired at 03:41:00Z. This script only executes what that document already fixed.
"""
import json
import random

PILOT_DONE = {"INTERLOCUTOR-131.md", "INTERLOCUTOR-3.md",
              "READER-128-2.md", "VERIFIER-131.md"}

m = json.load(open("units-manifest-137-v2.json"))
words = {r["file"].split("/")[-1]: r["words"] for r in m["manifest"]}
assert len(words) == 53, len(words)

pool = sorted(set(words) - PILOT_DONE)
assert len(pool) == 49, len(pool)

drawn = random.Random(1390).sample(pool, 20)

# The batch split, exactly as pre-registered: descending word count, ties by filename ascending,
# then alternate 1st/3rd/5th -> BATCH-1, 2nd/4th/6th -> BATCH-2.
ordered = sorted(drawn, key=lambda f: (-words[f], f))
b1 = ordered[0::2]
b2 = ordered[1::2]

out = {
    "seed": 1390, "pool_size": len(pool), "drawn": sorted(drawn),
    "order_for_split": ordered,
    "BATCH-1": b1, "BATCH-2": b2,
    "words": {f: words[f] for f in ordered},
    "batch_words": {"BATCH-1": sum(words[f] for f in b1),
                    "BATCH-2": sum(words[f] for f in b2)},
}
json.dump(out, open("draw-139.json", "w"), indent=1)
print("pool %d  drawn %d" % (len(pool), len(drawn)))
for name, b in (("BATCH-1", b1), ("BATCH-2", b2)):
    print("\n%s  %d files  %d words" % (name, len(b), sum(words[f] for f in b)))
    for f in b:
        print("   %-24s %5d w" % (f, words[f]))
