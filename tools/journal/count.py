#!/usr/bin/env python3
"""count - the journal word count, one counter for every session instead of one per session.

Session 136, 2026-08-26. This closes an item three sessions named and none of them did.

WHAT WAS WRONG, IN ONE PARAGRAPH
--------------------------------
`CONDITIONS-134.md` recorded FOUR different published word counts for one journal file and
concluded that this practice "has published a word count against a constitutional ceiling every
session without ever stating the method." Session 135 narrowed that: `count_126.py` through
`count_132.py` are seven files identical in method, each copied from the last and differing only in
a hardcoded default path, and `count_135.py` is an eighth. The method was stable; what was never
written down was that it IS the method. `CONDITIONS-135.md` said the fix out loud - "one
generalised counter replacing seven copies" - and then said "this session has spent its budget."
This is that counter. The eight predecessors are left on disk unedited, because they are the
evidence for the paragraph above; nothing in them is retracted.

THE METHOD, STATED (unchanged from all eight - this file is a merge, not a new rule):
  1. take everything after the title line;
  2. stop at `*Minutes proper:` if present - the sentence that reports the count is not part of
     the minutes it reports on. `count_135.py`'s first version omitted this and counted its own
     footnote: 502 against a 400 ceiling;
  3. remove code spans (`...`), because file and commit names are references, not prose;
  4. remove the markdown syntax characters * _ # | > and dashes;
  5. split on whitespace and keep every token containing at least one alphanumeric character.

WHAT THIS COUNTER DOES NOT DO, so nobody reads it as closing more than it closes:
  * It does not settle what the ceiling counts. `PROTOCOL.md` says the minutes are "<= 400 words"
    and says nothing about reviewer reports, footnotes or tables. Sessions 89, 90, 133, 134 and 135
    all read the mandated critique out of the ceiling; this counter's `--from`/`--until` flags make
    that reading VISIBLE rather than settled, and the session must still state which reading it used.
  * It does not correct anything retroactively. Run over the record it disagrees with several
    published figures - `CONDITIONS-135.md` reports 412 for session 133 (over the ceiling) and 391
    for session 134 (which published "exactly 400"). Those disagreements are a fact about the old
    counts, not a verdict, and this file proposes no retroactive correction.

Usage:
    python3 tools/journal/count.py journal/2026-08-26.md
    python3 tools/journal/count.py journal/*.md --table
    python3 tools/journal/count.py journal/2026-08-26.md --until '*Minutes proper:' --ceiling 400
"""
import argparse
import re
import sys

DEFAULT_UNTIL = "*Minutes proper:"


def count(path, until=DEFAULT_UNTIL, start_after_title=True):
    text = open(path).read()
    lines = text.split("\n")
    if start_after_title:
        if not lines or not lines[0].startswith("# "):
            raise ValueError("no title line in " + path)
        body = "\n".join(lines[1:])
    else:
        body = text
    if until:
        body = body.split(until, 1)[0]
    body = re.sub(r"`[^`]*`", " ", body)
    body = re.sub(r"[*_#|>—–-]", " ", body)
    return len([w for w in body.split() if any(c.isalnum() for c in w)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--until", default=DEFAULT_UNTIL,
                    help="stop counting at this literal string (default: the minutes-proper "
                         "footnote marker). Pass '' to count to the end of the file.")
    ap.add_argument("--whole-file", action="store_true",
                    help="count from the first line instead of after the title line")
    ap.add_argument("--ceiling", type=int, default=None,
                    help="if given, print OVER/UNDER against this ceiling and exit 1 if over")
    ap.add_argument("--table", action="store_true", help="one row per file")
    a = ap.parse_args()

    over = False
    for p in a.paths:
        try:
            n = count(p, until=a.until or None, start_after_title=not a.whole_file)
        except (OSError, ValueError) as e:
            print("%-28s  ERROR  %s" % (p, e), file=sys.stderr)
            over = True
            continue
        if a.ceiling is None:
            print("%-28s %6d" % (p, n) if (a.table or len(a.paths) > 1) else n)
        else:
            verdict = "OVER " if n > a.ceiling else "UNDER"
            print("%-28s %6d  %s %d" % (p, n, verdict, a.ceiling))
            over = over or n > a.ceiling
    sys.exit(1 if (a.ceiling is not None and over) else 0)


if __name__ == "__main__":
    main()
