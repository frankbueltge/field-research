#!/usr/bin/env python3
"""Count the words of session 129's minutes proper, under the reading adopted in REQUESTS.md
on 2026-08-18: the ceiling covers the minutes proper, and verbatim material the constitution
requires to be published (the hostile critique, the reviewers' and readers' reports) sits outside
it in its own clearly-headed sections. Written as a script so the count in the entry is not typed.

Identical in method to `count_128.py`; only the anchors move. Kept as its own file rather than
generalised, so that the count for each session is reproducible against the anchor that session
actually used."""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "journal/2026-08-21.md"
text = open(path).read()
start = "## What actually happened — session 129"
if start not in text:
    raise SystemExit("minutes section not found in " + path)
body = text.split(start, 1)[1]
body = body.split("*Minutes proper:", 1)[0]
# strip markdown syntax and code spans, exactly as session 128's counter did
body = re.sub(r"`[^`]*`", " ", body)
body = re.sub(r"[*_#|>—–-]", " ", body)
words = [w for w in body.split() if any(c.isalnum() for c in w)]
print(len(words))
