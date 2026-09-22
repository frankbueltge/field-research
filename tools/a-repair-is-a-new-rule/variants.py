#!/usr/bin/env python3
"""Build the 32 repair variants of the 2026-09-18 rule as separate, digested copies.

Session 167, 2026-09-22, pre-registration §2. The shipped rule in
tools/is-it-a-licence/ is NEVER edited: it produced published figures. Each variant is
a fresh copy of that directory carrying (a) zero or more regex patches applied BY LINE
ANCHOR against the file's own text, and (b) an appended block that installs a notice
pipeline whose behaviour with every flag OFF must equal the shipped rule's exactly —
which is checked over all 896 inputs, not asserted.

    R1  a notice line must carry a year, a (c)/(C)/©/&copy; marker or a placeholder
    R4  _TAIL_WORD's literal \\(c\\) alternative becomes \\([cC]\\)          [line anchor]
    R5  the four typographic quotation marks are admitted to _PREFIX        [line anchor]
    R6  an empty holder is sought on the following units, to a depth of three
    R7  notices are sought in the LOGICAL line: a block's physical lines joined, then
        split immediately before every occurrence of the notice word or marker

R6 and R7 compose through the pipeline rather than shadowing each other: R7 replaces the
SCOPE that produces the units, R6 turns on CONTINUATION over whatever units the scope
produced. Neither is written so that the other becomes a no-op by construction.

No rule, patch or check in this file calls a model or the network.
"""
import hashlib
import itertools
import json
import os
import shutil
import sys

REPAIRS = ["R1", "R4", "R5", "R6", "R7"]

# ---- the two line-anchored patches, as substrings of the file's own text ----------
OLD_TAIL = '(\\(c\\)|'
NEW_TAIL = '(\\([cC]\\)|'
OLD_PREFIX = '\\[]*'
NEW_PREFIX = '\\[\\u2018\\u2019\\u201c\\u201d]*'

# ---- the appended block -----------------------------------------------------------
# Written once, parameterised by three flags. With all three off it must reproduce
# `copyright_lines` as shipped:  [ln.strip() for ln in raw.splitlines()
#                                 if is_copyright_notice(ln)]
BLOCK = r'''

# ======================================================================== session 167
# Appended by tools/a-repair-is-a-new-rule/variants.py. Nothing above this line is
# edited. With _R1 / _R6 / _R7 all False this block reproduces the shipped rule.

_R1 = {R1}
_R6 = {R6}
_R7 = {R7}

_R1_EVIDENCE = re.compile(r"(?i)\((?:c|C)\)|©|&copy;|\b(?:19|20)\d{{2}}\b")
_R6_FILLER = re.compile(r"^[\s#*/;%!<>\-=_|\.]*$")
_R7_CUT = re.compile(r"(?i)(?=copyright\b|copr\.|\(c\)|©|&copy;)")
_R7_BLOCK = re.compile(r"\n[ \t]*\n")

_notice_base = is_copyright_notice


def is_copyright_notice(line):                                          # noqa: F811
    """The shipped test, and under R1 a required piece of notice evidence."""
    if not _notice_base(line):
        return False
    if not _R1:
        return True
    return bool(_R1_EVIDENCE.search(line)) or has_placeholder(line)


def _units_physical(raw_text):
    """The shipped scope: one unit per physical line, stripped."""
    return [ln.strip() for ln in raw_text.splitlines()]


def _units_logical(raw_text):
    """R7's scope: each block's lines joined, then cut before every notice marker."""
    out = []
    for block in _R7_BLOCK.split(raw_text):
        joined = " ".join(ln.strip() for ln in block.splitlines() if ln.strip())
        if not joined:
            continue
        for seg in _R7_CUT.split(joined):
            seg = seg.strip()
            if seg:
                out.append(seg)
    return out


def copyright_lines(raw_text):                                          # noqa: F811
    """Every copyright notice in the file, in file order, under this variant's flags."""
    raw_text = raw_text or ""
    units = _units_logical(raw_text) if _R7 else _units_physical(raw_text)
    out = []
    for i, unit in enumerate(units):
        if not is_copyright_notice(unit):
            continue
        found = unit.strip()
        if _R6 and holder_of(found) == "":
            parts = [found]
            for nxt in units[i + 1:i + 4]:
                if not nxt.strip() or _R6_FILLER.match(nxt) or is_copyright_notice(nxt):
                    break
                parts.append(nxt.strip())
                if holder_of(" ".join(parts)):
                    break
            joined = " ".join(parts)
            if holder_of(joined):
                found = joined
        out.append(found)
    return out
'''


def patch_source(text, repairs):
    """Apply the line-anchored patches, then append the block. Returns (text, hits)."""
    out, hits = [], []
    for ln in text.split("\n"):
        if ln.startswith("_TAIL_WORD = re.compile(") and "R4" in repairs:
            assert OLD_TAIL in ln, ln
            ln = ln.replace(OLD_TAIL, NEW_TAIL, 1)
            hits.append("_TAIL_WORD")
        elif ln.startswith("_PREFIX = ") and "R5" in repairs:
            assert OLD_PREFIX in ln, ln
            ln = ln.replace(OLD_PREFIX, NEW_PREFIX, 1)
            hits.append("_PREFIX")
        out.append(ln)
    want = (["_TAIL_WORD"] if "R4" in repairs else []) + (["_PREFIX"] if "R5" in repairs else [])
    assert sorted(hits) == sorted(want), (repairs, hits)
    body = "\n".join(out) + BLOCK.format(
        R1="R1" in repairs, R6="R6" in repairs, R7="R7" in repairs)
    return body, hits


def variant_id(repairs):
    return "".join("1" if r in repairs else "0" for r in REPAIRS)


def build(out_root, src):
    os.makedirs(out_root, exist_ok=True)
    index = []
    for k in range(len(REPAIRS) + 1):
        for combo in itertools.combinations(REPAIRS, k):
            vid = variant_id(combo)
            dst = os.path.join(out_root, vid)
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            os.makedirs(dst)
            for f in sorted(os.listdir(src)):
                if f.endswith(".py"):
                    shutil.copy2(os.path.join(src, f), dst)
            p = os.path.join(dst, "fingerprints.py")
            text = open(p).read()                    # read fully, THEN write
            body, hits = patch_source(text, combo)
            open(p, "w").write(body)
            index.append({
                "variant": vid,
                "repairs": list(combo),
                "n_repairs": len(combo),
                "anchored_patches": hits,
                "digests": {f: hashlib.sha256(open(os.path.join(dst, f), "rb").read()).hexdigest()
                            for f in ("rules.py", "fingerprints.py")},
            })
    return index


def main():
    out_root, src = sys.argv[1], sys.argv[2]
    index = build(out_root, src)
    shipped = {f: hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
               for f in ("rules.py", "fingerprints.py")}
    print(json.dumps({"n_variants": len(index), "shipped_digests": shipped,
                      "repairs": REPAIRS}, indent=1))
    json.dump({"note": "Session 167. The 32 repair variants, their patches and digests.",
               "repairs": REPAIRS, "shipped_digests": shipped, "variants": index},
              open(os.path.join(out_root, "index.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
