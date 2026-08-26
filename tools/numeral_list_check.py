#!/usr/bin/env python3
"""numeral_list_check - does a heading's number word match the list under it?

Session 136, 2026-08-26. Written because this practice's signature defect - a statement about an
artifact refuted by the artifact - fired TWICE IN ONE DAY in its narrowest possible form: a heading
reading "Two things that claim is not" above three items; corrected to "Four"; a fifth item added
beneath it in the same session; wrong again within the hour, INSIDE ITS OWN CORRECTION
(`drafts/2026-08-26-cited-not-retrievable/CONDITIONS-136.md` item 12).

`CONDITIONS-136.md` said "one line of code would" catch it. This is that code, and writing it is the
only honest response to having named it.

WHAT IT CHECKS, AND IT IS ONE NARROW THING
------------------------------------------
A line containing a spelled-out number word (one .. twenty) or a digit, immediately followed - after
at most one blank line - by a markdown ordered list (`1.` `2.` ...) or an unordered list (`-` `*`).
It compares the number named to the number of top-level items and reports a mismatch.

WHAT IT DOES NOT CATCH, stated so nobody reads a pass as a clean bill
--------------------------------------------------------------------
Everything else. It does not read prose against data, it does not check a figure against a JSON
file, it does not know what a claim is. The nine OTHER instances the adversary counted in one
session - a premise refuted by a robots.txt, a promise to mark conjecture broken by the document
making it, "a fixed second" against a file listing five hours - would all pass this check silently.
**`memory/downstream-commitments.md` condition 31 applies to this script as it applies to every
other guard here: a pass is evidence about this guard's tested paths, not about the document.**

It also has a known false-positive class, left in deliberately rather than tuned away: a heading may
legitimately name a number that is not the length of the list beneath it ("Nine gauntlets, and the
three that mattered:"). Those are reported and the caller judges them; a checker that guessed which
numbers were load-bearing would be a guard that can be talked round.

Usage:
    python3 tools/numeral_list_check.py FILE [FILE ...]
    python3 tools/numeral_list_check.py drafts/*/CONCEPT.md --quiet
Exit 1 if any mismatch is reported. Offline; reads the files named and nothing else.
"""
import argparse
import re
import sys

WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
         "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
         "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
         "nineteen": 19, "twenty": 20}
NUM_RE = re.compile(r"\b(" + "|".join(WORDS) + r"|\d{1,2})\b", re.I)
ORDERED = re.compile(r"^\s{0,3}(\d{1,2})[.)]\s+\S")
BULLET = re.compile(r"^\s{0,3}[-*]\s+\S")
CONTINUATION = re.compile(r"^\s{2,}\S")


def strip_markup(line):
    line = re.sub(r"`[^`]*`", " ", line)
    return re.sub(r"[*_#>]", "", line)


def list_len(lines, i):
    """Number of TOP-LEVEL items in the list starting at lines[i], or 0 if none starts there."""
    if not (ORDERED.match(lines[i]) or BULLET.match(lines[i])):
        return 0, None
    ordered = bool(ORDERED.match(lines[i]))
    n, j = 0, i
    while j < len(lines):
        ln = lines[j]
        if (ORDERED.match(ln) if ordered else BULLET.match(ln)):
            n += 1
        elif ln.strip() == "" or CONTINUATION.match(ln):
            pass                       # blank line or wrapped/nested continuation
        else:
            break
        j += 1
    return n, ("ordered" if ordered else "bullet")


def check(path):
    lines = open(path).read().split("\n")
    out = []
    for i, raw in enumerate(lines):
        text = strip_markup(raw).strip()
        if not text:
            continue
        # A list ITEM is not a heading for the item beneath it. Without this, every "1." reports a
        # mismatch against the two items that follow it - which the first run of this script did,
        # on its own test fixture. A checker that fires on the thing it is checking is the same
        # shape of defect as the counter that counted its own footnote (`count_135.py`).
        if ORDERED.match(raw) or BULLET.match(raw) or CONTINUATION.match(raw):
            continue
        # A markdown section heading's number is a SECTION number, not a count. "## 4. What is NOT
        # withdrawn" above three bullets is not a defect, and the first run of this script reported
        # three of them.
        if raw.lstrip().startswith("#"):
            continue
        # find where the list starts: next line, or the line after one blank
        for skip in (1, 2):
            k = i + skip
            if k >= len(lines):
                continue
            if skip == 2 and lines[i + 1].strip() != "":
                break
            n, kind = list_len(lines, k)
            if n:
                # ONLY THE FIRST NUMERAL IN THE LINE. A heading that announces a count announces
                # it first; every later numeral is prose ("Five things ... the first version said
                # two and listed three"). Checking all of them made this script spray five rows at
                # one correctly-numbered heading on its first run over this session's own work.
                m = NUM_RE.search(text)
                if m:
                    tok = m.group(1).lower()
                    named = WORDS.get(tok) or int(tok)
                    if named != n and 1 <= named <= 20:
                        out.append((i + 1, text[:96], named, n, kind))
                break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--quiet", action="store_true", help="print only mismatches")
    a = ap.parse_args()
    bad = 0
    for p in a.paths:
        try:
            rows = check(p)
        except OSError as e:
            print("%s  ERROR  %s" % (p, e), file=sys.stderr)
            bad += 1
            continue
        if rows:
            print("%s" % p)
            for (ln, text, named, n, kind) in rows:
                print("  line %-5d names %-2d, the %s list beneath has %-2d  |  %s"
                      % (ln, named, kind, n, text))
            bad += len(rows)
        elif not a.quiet:
            print("%s  no numeral/list mismatch found" % p)
    if bad:
        print("\n%d line(s) to judge. A number in a heading need not be the list's length - "
              "this script reports, it does not decide." % bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
