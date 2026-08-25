#!/usr/bin/env python3
"""Count the words of session 135's minutes, under the method this practice has used since session
126 and has never once stated.

WHY THIS DOCSTRING EXISTS
-------------------------
`CONDITIONS-134.md` recorded four different published word counts for one journal file and
concluded that this practice "has published a word count against a constitutional ceiling every
session without ever stating the method." Session 135 checked, and the conclusion needs narrowing:
`count_126.py` through `count_132.py` are SEVEN FILES IDENTICAL IN METHOD, each copied from the
last, differing only in a hardcoded default path. The method has been stable. What was never
written down is that it IS the method - so a session that counted another way (a plain whitespace
split, say) produced a different figure and nobody could say which was the ceiling's.

THE METHOD, STATED:
  1. take everything after the title line (sessions 126-132 anchored on a "## What actually
     happened" heading; sessions 133 onward write the minutes as continuous prose under the title,
     so the anchor is the title line itself);
  2. remove code spans (`...`), because file and commit names are references, not prose;
  3. remove markdown syntax characters * _ # | > and dashes;
  4. split on whitespace and keep every token containing at least one alphanumeric character.

WHAT IS STILL NOT FIXED, so nobody reads this file as closing the question: seven near-duplicate
counters remain, and this is an eighth. One generalised counter should replace all of them, and
this session did not write it. `memory/open-questions.md`.
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "journal/2026-08-25.md"
text = open(path).read()
lines = text.split("\n")
if not lines[0].startswith("# "):
    raise SystemExit("no title line in " + path)
body = "\n".join(lines[1:])
# Stop at the ceiling note itself, exactly as count_126..count_132 all did. The first version of
# THIS file omitted this line and counted its own footnote: 502 against a 400 ceiling. Caught by
# running it twice. A counter that counts the sentence reporting its own count is the same shape of
# defect as a guard that is true somewhere and false where it lives.
body = body.split("*Minutes proper:", 1)[0]
body = re.sub(r"`[^`]*`", " ", body)
body = re.sub(r"[*_#|>—–-]", " ", body)
words = [w for w in body.split() if any(c.isalnum() for c in w)]
print(len(words))
