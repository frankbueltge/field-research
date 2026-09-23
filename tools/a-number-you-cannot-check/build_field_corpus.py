#!/usr/bin/env python3
"""Corpus F: this practice's own public summary record. Session 168, 2026-09-23.

Every SUMMARY.md under artifacts/ and presentations/, and every version of BULLETIN.md in
this repository's history. These are our own files, so this corpus IS committed with the
artifact -- only the two world corpora stay outside (protocol §7).
"""
import json
import os
import subprocess
import sys
import time

ROOT = sys.argv[1]
OUT = sys.argv[2]


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True,
                          text=True, check=True).stdout


def main():
    docs = []
    for base in ("artifacts", "presentations"):
        for dirpath, _dirs, files in os.walk(os.path.join(ROOT, base)):
            for f in files:
                if f == "SUMMARY.md":
                    p = os.path.join(dirpath, f)
                    rel = os.path.relpath(p, ROOT)
                    docs.append({"id": rel, "kind": "summary",
                                 "text": open(p, encoding="utf-8").read()})
    revs = [l.split(None, 1) for l in git("log", "--format=%H %ad", "--date=short",
                                          "--", "BULLETIN.md").strip().split("\n") if l]
    for sha, date in revs:
        try:
            text = git("show", f"{sha}:BULLETIN.md")
        except subprocess.CalledProcessError:
            continue
        docs.append({"id": f"BULLETIN.md@{sha[:8]} ({date})", "kind": "bulletin", "text": text})
    docs.sort(key=lambda d: d["id"])
    json.dump({"corpus": "F", "source": "this repository",
               "summaries": sum(1 for d in docs if d["kind"] == "summary"),
               "bulletins": sum(1 for d in docs if d["kind"] == "bulletin"),
               "built_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "docs": docs}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"wrote {len(docs)} documents "
          f"({sum(1 for d in docs if d['kind'] == 'summary')} summaries, "
          f"{sum(1 for d in docs if d['kind'] == 'bulletin')} bulletins) to {OUT}")


if __name__ == "__main__":
    main()
