#!/usr/bin/env python3
"""A1 — reproduce `sources/signatories-2026-08-02.json` from the committed page bytes.

Added at the Skeptic's blocking condition 3 (session 80): every other classification step of
this anchor is a committed, re-runnable tool, while the single most decisive classification —
who is and is not a Section 1 signatory — had none. It has one now, and it runs offline
against the committed HTML, so anyone can re-derive the split without refetching anything.

Also answers blocking condition 4: the same page states "about 190 organisations" signed while
its two columns total 235. The reconciliation is dual-section signers — organisations that
signed both sections and appear in both columns — and this script counts them rather than
asserting the explanation.

Usage (from the a1/ directory):
    python3 tools/parse_signatories.py            # verify against the committed JSON
    python3 tools/parse_signatories.py --write    # regenerate it

Exit 0 = the committed JSON is reproduced exactly and both stated counts match.
"""
import html
import json
import re
import sys
from pathlib import Path

A1 = Path(__file__).resolve().parent.parent
PAGE = A1 / "sources" / "signatories-page-2026-08-02.html"
OUT = A1 / "sources" / "signatories-2026-08-02.json"
ROW = re.compile(r'<tr class="ecl-table__row">(.*?)</tr>', re.S)
CELL = re.compile(r'<td class="ecl-table__cell"[^>]*>(.*?)</td>', re.S)
STATED = re.compile(r"Section 1 signatories</strong>\s*:\s*(\d+).*?"
                    r"Section 2 signatories</strong>\s*:\s*(\d+)", re.S)


def parse(text: str):
    s1, s2 = [], []
    for row in ROW.findall(text):
        cells = CELL.findall(row)
        if len(cells) != 2:
            continue
        a, b = (html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in cells)
        if a:
            s1.append(a)
        if b:
            s2.append(b)
    return s1, s2


def main(write: bool) -> int:
    text = PAGE.read_text(encoding="utf-8", errors="replace")
    s1, s2 = parse(text)
    stated = STATED.search(text)
    ok = True

    if stated:
        n1, n2 = int(stated.group(1)), int(stated.group(2))
        print(f"page states: Section 1 = {n1}, Section 2 = {n2}")
        for label, parsed, claimed in (("Section 1", len(s1), n1), ("Section 2", len(s2), n2)):
            mark = "OK" if parsed == claimed else "MISMATCH"
            ok &= parsed == claimed
            print(f"  parsed {label}: {parsed}  [{mark}]")
    else:
        print("could not find the page's own stated counts")
        ok = False

    both = sorted(set(s1) & set(s2))
    union = len(set(s1) | set(s2))
    print(f"\nsum of columns: {len(s1)} + {len(s2)} = {len(s1) + len(s2)}")
    print(f"organisations appearing in BOTH columns: {len(both)} — {', '.join(both)}")
    print(f"distinct organisations (union): {union}")
    print('the page\'s prose says "about 190 organisations" signed; the union above is the '
          "figure that prose is comparable with, not the column sum")

    payload = {"section1": s1, "section2": s2}
    if write:
        OUT.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
        print(f"\nwrote {OUT}")
    else:
        committed = json.loads(OUT.read_text())
        same = committed == payload
        ok &= same
        print(f"\ncommitted JSON reproduced exactly: {same}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
