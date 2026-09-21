#!/usr/bin/env python3
"""Count STATE-OF-THE-FIELD.md by its own declared rule: whitespace-separated tokens
holding at least one letter or digit. Written out so the cap is checkable by anyone."""
import re
import sys

t = open(sys.argv[1] if len(sys.argv) > 1 else "STATE-OF-THE-FIELD.md", encoding="utf-8").read()
n = sum(1 for tok in t.split() if re.search(r"[A-Za-z0-9]", tok))
print(n)
