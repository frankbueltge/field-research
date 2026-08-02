#!/usr/bin/env python3
"""The apparatus ratios, recomputed from the tracked files.

Session 79 (2026-08-01) answered the team's apparatus-ratio seed by computing four ratios
first-hand and committing to publishing them at *every* consolidation pass. Session 82
(2026-08-02) turned that hand computation into this script, so the definitions are code
rather than prose and a later session cannot quietly change what it measures.

Definitions, unchanged from the session-79 answer in REQUESTS.md:
  * Tracked files only (git ls-files), text-bearing only: .jpg/.jpeg/.png/.webp excluded,
    because a camera file is neither apparatus nor prose.
  * work side       — everything under works/
  * face            — the works' work.astro / work.html / meta.json / data.json only
  * prose           — .md files
  * record layer    — journal/, memory/, archive/, field-feedback/, chronicle.json,
                      WORKBOARD.md, REQUESTS.md, PROTOCOL.md, FIELD.md
  * unshipped       — drafts/, notes/, deliveries/, site-prs/

Bytes are the wrong unit and the session-79 answer says so; they are used here because
they are the unit that is checkable. Prose-only is the honest row.

Usage:  python3 tools/apparatus_ratio.py [--json]
"""
import json
import subprocess
import sys
from pathlib import Path

BINARY = {".jpg", ".jpeg", ".png", ".webp"}
FACE = {"work.astro", "work.html", "meta.json", "data.json"}
RECORD_DIRS = ("journal/", "memory/", "archive/", "field-feedback/")
RECORD_FILES = ("chronicle.json", "WORKBOARD.md", "REQUESTS.md", "PROTOCOL.md", "FIELD.md")
UNSHIPPED_DIRS = ("drafts/", "notes/", "deliveries/", "site-prs/")


def kb(n: int) -> float:
    return round(n / 1024.0, 1)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    out = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, text=True)
    if out.returncode != 0:
        print("git ls-files failed", file=sys.stderr)
        return 3
    paths = [p for p in out.stdout.split("\0") if p]

    total = works = face = prose_in = prose_out = record = unshipped = 0
    for rel in paths:
        f = root / rel
        if not f.is_file() or f.suffix.lower() in BINARY:
            continue
        size = f.stat().st_size
        total += size
        if rel.startswith("works/"):
            works += size
            if f.name in FACE:
                face += size
            if f.suffix == ".md":
                prose_in += size
        else:
            if f.suffix == ".md":
                prose_out += size
            if rel.startswith(RECORD_DIRS) or rel in RECORD_FILES:
                record += size
            if rel.startswith(UNSHIPPED_DIRS):
                unshipped += size

    rows = [
        ("everything outside works/ : works/ text", total - works, works),
        ("everything outside the face : the face", total - face, face),
        ("markdown prose outside works/ : prose inside", prose_out, prose_in),
        ("record and governance layer : works/ text", record, works),
    ]
    result = {
        "totals_kb": {
            "all_text": kb(total), "works": kb(works), "face": kb(face),
            "prose_in_works": kb(prose_in), "prose_outside": kb(prose_out),
            "record_layer": kb(record), "unshipped": kb(unshipped),
        },
        "ratios": {name: round(num / den, 2) for name, num, den in rows},
    }
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
        return 0
    print(f"tracked text: {kb(total)} KB  (binaries excluded)")
    for name, num, den in rows:
        print(f"  {num/den:5.2f} : 1   {name}   [{kb(num)} KB : {kb(den)} KB]")
    print(f"unshipped text (drafts/notes/deliveries/site-prs): {kb(unshipped)} KB "
          f"against {kb(works)} KB of shipped works")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
