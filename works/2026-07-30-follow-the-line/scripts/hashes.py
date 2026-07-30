#!/usr/bin/env python3
"""Hash EVERY file in the work, not the ones someone remembered to list.

The round-two Verifier found that `work.astro` — the work's most reader-facing file — was absent
from `SHA256SUMS.txt` entirely, because that file had been written by hand-typed globs over the
scripts, the sources and the results. A manifest that covers what its author remembered is not an
integrity check; it is a habit. This script walks the work directory and covers everything except
the manifest itself, so a file cannot be added in future without being hashed.

Usage:
  python3 scripts/hashes.py            # write SHA256SUMS.txt
  python3 scripts/hashes.py --check    # recompute and fail on any difference
"""
import argparse
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "SHA256SUMS.txt")
SKIP = {"SHA256SUMS.txt"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build():
    rows = []
    for root, dirs, files in os.walk(HERE):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for name in sorted(files):
            rel = os.path.relpath(os.path.join(root, name), HERE)
            if rel in SKIP or rel.endswith(".pyc"):
                continue
            rows.append("%s  %s" % (sha256(os.path.join(root, name)), rel))
    return "\n".join(rows) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    text = build()
    if args.check:
        if not os.path.exists(OUT) or open(OUT, encoding="utf-8").read() != text:
            print("FAIL: SHA256SUMS.txt does not cover this tree exactly")
            return 1
        print("OK: SHA256SUMS.txt covers every file in the work (%d)"
              % len(text.strip().split("\n")))
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote %s (%d files)" % (OUT, len(text.strip().split("\n"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
