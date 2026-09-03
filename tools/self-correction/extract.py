#!/usr/bin/env python3
"""Deterministic candidate extraction for the self-correction census.

Scans this practice's own committed record for paragraphs that may describe a
correction to THIS PRACTICE's own claims, numbers, methods or shipped work.
Output is a candidate set only -- no candidate is a correction event until a
coder has read it and quoted the sentence that makes it one.

Reproducible: same repo state -> byte-identical candidates.json.
"""
import json, os, re, sys, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SOURCES = []
jdir = os.path.join(ROOT, "journal")
for fn in sorted(os.listdir(jdir)):
    if fn.endswith(".md"):
        SOURCES.append(os.path.join("journal", fn))
SOURCES.append(os.path.join("memory", "discarded.md"))

# Markers chosen before reading any candidate. Case-insensitive, word-ish.
MARKERS = [
    r"correct(?:ion|ions|ed|s)?\b", r"\bmiscount", r"\bmistyp", r"\bmisread",
    r"re-?cod(?:e|ed|ing)", r"\bretract(?:ed|ion)?\b", r"\bwithdraw(?:n|s|al)?\b",
    r"does not stand", r"did not stand", r"no longer stands", r"was wrong",
    r"were wrong", r"got it wrong", r"\berror\b", r"\berrors\b", r"\bbug\b",
    r"supersed(?:e|ed|es)", r"\bdiscard(?:ed|s)?\b", r"\brefut(?:e|ed|es|ation)",
    r"overstat(?:e|ed)", r"understat(?:e|ed)", r"\bfalse\b", r"\bfaulty\b",
    r"\bwalked back\b", r"\btook back\b", r"\bpulled back\b", r"\bnot reproducible\b",
]
RX = re.compile("|".join(MARKERS), re.I)

def paragraphs(path):
    """Yield (start_line, text) for blank-line-separated blocks."""
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    buf, start = [], 1
    for i, ln in enumerate(lines, 1):
        if ln.strip() == "":
            if buf:
                yield start, "\n".join(buf)
            buf, start = [], i + 1
        else:
            if not buf:
                start = i
            buf.append(ln)
    if buf:
        yield start, "\n".join(buf)

def main():
    out = []
    for path in SOURCES:
        for start, text in paragraphs(path):
            hits = sorted({m.group(0).lower() for m in RX.finditer(text)})
            if not hits:
                continue
            cid = hashlib.sha1(f"{path}:{start}".encode()).hexdigest()[:10]
            out.append({
                "id": cid, "file": path, "line": start,
                "markers": hits, "words": len(text.split()), "text": text,
            })
    dest = os.path.join(ROOT, "tools", "self-correction", "candidates.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"sources: {len(SOURCES)}")
    print(f"candidates: {len(out)}")
    print(f"candidate words: {sum(c['words'] for c in out)}")

if __name__ == "__main__":
    main()
