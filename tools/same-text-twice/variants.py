#!/usr/bin/env python3
"""Build the repair variants of the pinned rule as separate, digested copies.

Session 165, pre-registration §10. The shipped rule is never edited in place for the
measurement; each variant is a copy carrying one patch, and its digest is recorded
beside its results.

  B  naive repair     `_TAIL_WORD` recompiled with re.I -- the obvious fix for defect 4
  C  targeted repair  only the (c) alternative made case-blind: \\([cC]\\)
  D  C plus defect 5  typographic quotation marks admitted to `_PREFIX`

The B/C split, and D, were decided AFTER the scored run and the adjudication, and are
recorded as such. Every patch is applied by LINE ANCHOR against the text of the file
itself -- never against a literal retyped in this session, which is how a variant could
silently become a different rule than the one named.
"""
import hashlib
import json
import os
import shutil
import sys

OLD_T = '(\\(c\\)|'
NEW_T = '(\\([cC]\\)|'
OLD_P = '\\[]*'
NEW_P = '\\[\\u2018\\u2019\\u201c\\u201d]*'


def patch(text, name):
    out, hits = [], []
    for ln in text.split("\n"):
        if ln.startswith("_TAIL_WORD = re.compile("):
            if name == "B":
                assert ln.endswith('")'), ln
                ln = ln[:-1] + ", re.I)"
            else:
                assert OLD_T in ln, ln
                ln = ln.replace(OLD_T, NEW_T, 1)
            hits.append("_TAIL_WORD")
        elif ln.startswith("_PREFIX = ") and name == "D":
            assert OLD_P in ln, ln
            ln = ln.replace(OLD_P, NEW_P, 1)
            hits.append("_PREFIX")
        out.append(ln)
    want = {"B": ["_TAIL_WORD"], "C": ["_TAIL_WORD"], "D": ["_TAIL_WORD", "_PREFIX"]}[name]
    assert sorted(hits) == sorted(want), (name, hits)
    return "\n".join(out)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(root, "is-it-a-licence")
    out = sys.argv[1]
    digests = {}
    for name in ("B", "C", "D"):
        dst = os.path.join(out, name)
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(src):
            if f.endswith(".py"):
                shutil.copy2(os.path.join(src, f), dst)
        p = os.path.join(dst, "fingerprints.py")
        # Read, then write. On this session's first run these were one expression,
        # so open(p,"w") truncated the file before open(p).read() ran and the variant
        # was built from an empty file. Kept as a comment because it is the same shape
        # as the defects this session is about: a tool that destroys its own input.
        text = open(p).read()
        open(p, "w").write(patch(text, name))
        digests[name] = {f: hashlib.sha256(open(os.path.join(dst, f), "rb").read()).hexdigest()
                         for f in ("rules.py", "fingerprints.py")}
    print(json.dumps(digests, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
