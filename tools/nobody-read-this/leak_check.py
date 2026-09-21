#!/usr/bin/env python3
"""K4 of PREREGISTRATION.md section 9: grep the exact payload bytes for a forbidden list.

Reports every hit and says whether it falls inside a quoted DOCUMENT block (the evidence,
which cannot be edited without falsifying the item) or in the payload's own scaffolding
(which is ours and must not leak). See the dated amendment in PREREGISTRATION.md.

Usage: leak_check.py <payload.txt> <items.json> <arm>
"""
import json
import re
import sys

FORBIDDEN = ["Meridian", "field-research", "frankbueltge", "R-ship", "shipped",
             "SPDX", "defect", "metamorphic", "adjudicat"]
CATEGORIES = ["DEFECT", "LATENT", "MR-FALSE", "UNDECIDED"]

DOC = re.compile(r"--- DOCUMENT[^\n]*BEGINS ---\n(.*?)\n--- DOCUMENT[^\n]*ENDS ---", re.S)


def regions(text):
    spans, out = [], []
    for m in DOC.finditer(text):
        spans.append(m.span(1))
    prev, scaffold = 0, []
    for a, b in spans:
        scaffold.append((prev, a))
        prev = b
    scaffold.append((prev, len(text)))
    return spans, scaffold


def hits(text, spans, scaffold, needle, flags=re.I):
    out = []
    for m in re.finditer(re.escape(needle), text, flags):
        i = m.start()
        where = "document" if any(a <= i < b for a, b in spans) else "scaffolding"
        line = text[max(0, text.rfind("\n", 0, i) + 1):text.find("\n", i)]
        out.append({"at": i, "where": where, "line": line.strip()[:160]})
    return out


def main():
    payload = open(sys.argv[1], encoding="utf-8").read()
    items = json.load(open(sys.argv[2]))["items"][sys.argv[3]]
    spans, scaffold = regions(payload)
    ids = sorted({it["true_id"] for it in items}, key=len, reverse=True)

    report = {"arm": sys.argv[3], "chars": len(payload), "n_document_blocks": len(spans),
              "forbidden": {}, "categories": {}, "corpus_identifiers": {}}
    for n in FORBIDDEN:
        h = hits(payload, spans, scaffold, n)
        if h:
            report["forbidden"][n] = h
    for n in CATEGORIES:
        h = [x for x in hits(payload, spans, scaffold, n, 0)]
        if h:
            report["categories"][n] = {"n": len(h),
                                       "outside_document": sum(1 for x in h if x["where"] != "document")}
    for i in ids:
        h = [x for x in hits(payload, spans, scaffold, i, 0)]
        if h:
            report["corpus_identifiers"][i] = {
                "n": len(h),
                "in_document": sum(1 for x in h if x["where"] == "document"),
                "in_scaffolding": sum(1 for x in h if x["where"] != "document")}
    report["scaffolding_hits_total"] = (
        sum(1 for v in report["forbidden"].values() for x in v if x["where"] != "document")
        + sum(v["in_scaffolding"] for v in report["corpus_identifiers"].values()))
    print(json.dumps(report, indent=1)[:6000])
    return report


if __name__ == "__main__":
    main()
