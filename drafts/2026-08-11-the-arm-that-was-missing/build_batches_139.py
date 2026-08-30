#!/usr/bin/env python3
"""build_batches_139 - the counter payloads of PREREGISTRATION-139.md.

Session 139, 2026-08-30. One payload per batch, ten reports each, FILENAMES WITHHELD: every report
appears only as FILE-1 ... FILE-10, in the pre-registered split order. Nothing is edited, elided or
reflowed inside a report - each is its file's bytes, verbatim, between two markers.

The payloads are written OUTSIDE this repository so that a counter can be given the text without
being given, or needing, a path into the working tree.
"""
import json
import os

OUT = "/tmp/claude-0/-home-user-field-research/61fd4d3b-02eb-5630-9248-830e7a6f330e/scratchpad"

HEADER = """You are counting units in ten review reports. They are reproduced below, verbatim,
labelled FILE-1 through FILE-10. Their filenames are withheld deliberately.
"""

d = json.load(open("draw-139.json"))
m = json.load(open("units-manifest-137-v2.json"))
path_of = {r["file"].split("/")[-1]: r["file"] for r in m["manifest"]}
os.makedirs(OUT, exist_ok=True)
for batch in ("BATCH-1", "BATCH-2"):
    parts = [HEADER]
    for i, name in enumerate(d[batch], 1):
        text = open(path_of[name], encoding="utf-8").read()
        parts.append("\n\n===== BEGIN FILE-%d =====\n\n%s\n\n===== END FILE-%d =====\n"
                     % (i, text.rstrip("\n"), i))
    blob = "".join(parts)
    p = os.path.join(OUT, "counter-payload-139-%s.txt" % batch.lower())
    open(p, "w", encoding="utf-8").write(blob)
    print("%s -> %s  %d files  %d chars  %d words"
          % (batch, p, len(d[batch]), len(blob), len(blob.split())))
