#!/usr/bin/env python3
"""Count the words of session 126's minutes proper, under the reading adopted in REQUESTS.md
on 2026-08-18: the ceiling covers the minutes proper, and verbatim material the constitution
requires to be published (the hostile critique, the severed-reader panel) sits outside it in its
own clearly-headed sections. Written as a script so the count in the entry is not typed."""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "journal/2026-08-18.md"
text = open(path).read()
start = "## What actually happened — session 126"
if start not in text:
    raise SystemExit("minutes section not found in " + path)
body = text.split(start, 1)[1]
body = body.split("*Minutes proper:", 1)[0]
# strip the italic preamble about the ceiling itself, markdown syntax and code spans
body = re.sub(r"`[^`]*`", " ", body)
body = re.sub(r"[*_#|>—–-]", " ", body)
words = [w for w in body.split() if any(c.isalnum() for c in w)]
print(len(words))
