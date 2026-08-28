#!/usr/bin/env python3
"""extract_units_137 - carve the reviewers' own unedited reports into findings, mechanically.

Session 137, 2026-08-28. Built AFTER `PREREGISTRATION-137.md` was committed and pushed
(commit of 03:40:51Z, nine seconds before the daily probe fired), and its rule is that
document's §3 rendered as code.

WHY A SCRIPT AND NOT A HAND
---------------------------
Session 134 measured this arc's disposition tables - this practice's own SUMMARIES of what its
reviewers said - and withdrew the resulting rate the same session, because a summary can drop the
thing that makes a finding class A. `downstream-commitments.md` condition 37(b) makes that a
standing condition: no rate comparison may be quoted from this practice on this question, because
"a rate over that population measures the bookkeeping."

The fix is the reviewers' own words. But a population hand-carved out of 150,000 words by the
practice whose reviewers wrote them is the same defect wearing a different coat. So the carving is
a script, its rule is stated here, and its output is auditable file by file - and
`PREREGISTRATION-137.md` K4 requires this session to hand-count five of the files against it before
any rate is published.

THE RULE
--------
A unit is "one numbered or headed finding, charge or answer, as the report itself delimits it."
Reports in this population use four delimiter families. For each file the script counts matches of
each family and splits on the family with the MOST matches; ties break toward the earlier family in
this list, which is the more specific one:

  1. CHARGE   `^#{2,4} *(Charge|Finding|Objection|Defect) *N`      - an explicitly numbered finding
  2. HEADNUM  `^#{2,4} *N[.)]`                                     - a numbered section heading
  3. BOLDNUM  `^\\*\\*N[.)]?`                                       - a bold-numbered item
  4. LISTNUM  `^N[.)] ` at column 0                                - a top-level numbered list item

A file whose winning family has fewer than MIN_UNITS matches is reported UNEXTRACTABLE and carved by
nothing: `PREREGISTRATION-137.md` §3 says such a report is "reported as unextractable rather than
hand-carved."

WHY THE DOMINANT FAMILY AND NOT ALL OF THEM
-------------------------------------------
Several reports state their findings twice - as `### N.` attack sections and again as a numbered
`N.` list of decisive charges. Splitting on every family at once double-counts those. Taking the
dominant family takes each report at one granularity: its own.

WHAT THIS DOES NOT DO, AND IT IS THE LARGEST LIMIT
--------------------------------------------------
The granularity is the REPORT's, not a fixed one. One file's `## Charge 4` is a single finding;
another's `### 3.` is an attack line holding several. A per-pass COUNT therefore partly measures how
a reviewer chose to subdivide. `PREREGISTRATION-137.md` §5 leads with the granularity-robust
statistic for this reason and prints the limit beside every count.

A unit's text runs from its delimiter line to the line before the next delimiter of the same family
(or EOF). Text is passed to classifiers whole up to TRUNCATE_AT characters; beyond that it is cut at
a line boundary and marked, and the cut is recorded per unit so the count of truncated units is
publishable.
"""
import hashlib
import json
import os
import random
import re
import sys

MIN_UNITS = 3
TRUNCATE_AT = 6000
SHUFFLE_SEED = 137

FAMILIES = [
    ("CHARGE", re.compile(r"^#{2,4} *(?:Charge|Finding|Objection|Defect)\b[^\n]*?\d")),
    ("HEADNUM", re.compile(r"^#{2,4} *\d+[.)]")),
    ("BOLDNUM", re.compile(r"^\*\*\d+[.)]?[ —-]")),
    ("LISTNUM", re.compile(r"^\d+[.)] ")),
]

ROLE_OF_PREFIX = {
    "INTERLOCUTOR": "interlocutor",
    "VERIFIER": "verifier",
    "READER": "reader",
}

# Identifiers that would tell a blinded classifier which role or which file it is reading. Applied
# to unit text only. Role words are replaced by a neutral token; the practice's own name is left
# alone because every unit is about this practice and its presence carries no role information.
BLIND_PATTERNS = [
    (re.compile(r"\b[Ii]nterlocutor\b"), "the reviewer"),
    (re.compile(r"\b[Vv]erifier\b"), "the reviewer"),
    (re.compile(r"\b[Ss]evered [Rr]eader\b"), "the reviewer"),
    (re.compile(r"\b[Cc]old [Rr]ead(er)?\b"), "the reviewer"),
    (re.compile(r"\b[Rr]eader \d+\b"), "the reviewer"),
    (re.compile(r"\b[Ss]keptic\b"), "the reviewer"),
    (re.compile(r"INTERLOCUTOR-[0-9A-Za-z-]*\.md"), "REPORT.md"),
    (re.compile(r"VERIFIER-[0-9A-Za-z-]*\.md"), "REPORT.md"),
    (re.compile(r"READERS?-[0-9A-Za-z-]*\.md"), "REPORT.md"),
]


def pick_family(lines):
    counts = {}
    for name, pat in FAMILIES:
        counts[name] = sum(1 for ln in lines if pat.match(ln))
    best = None
    for name, _ in FAMILIES:
        if best is None or counts[name] > counts[best]:
            best = name
    return best, counts


def split_units(lines, family):
    pat = dict(FAMILIES)[family]
    starts = [i for i, ln in enumerate(lines) if pat.match(ln)]
    units = []
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        units.append("\n".join(lines[start:end]).strip())
    return units


def blind(text):
    for pat, repl in BLIND_PATTERNS:
        text = pat.sub(repl, text)
    return text


def truncate(text):
    if len(text) <= TRUNCATE_AT:
        return text, False
    cut = text[:TRUNCATE_AT]
    nl = cut.rfind("\n")
    if nl > TRUNCATE_AT // 2:
        cut = cut[:nl]
    return cut + "\n\n[UNIT TRUNCATED FOR LENGTH]", True


def main(dirs, out_units, out_manifest):
    files = []
    for d in dirs:
        for name in sorted(os.listdir(d)):
            if not name.endswith(".md"):
                continue
            prefix = name.split("-")[0]
            if prefix in ROLE_OF_PREFIX and not name.startswith("READERS-"):
                files.append((d, name, ROLE_OF_PREFIX[prefix]))

    manifest = []
    units = []
    for d, name, role in files:
        path = os.path.join(d, name)
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        lines = raw.split("\n")
        family, counts = pick_family(lines)
        n = counts[family]
        rec = {
            "file": path, "role": role, "words": len(raw.split()),
            "family": family, "family_counts": counts,
        }
        if n < MIN_UNITS:
            rec["status"] = "UNEXTRACTABLE"
            rec["units"] = 0
            manifest.append(rec)
            continue
        texts = split_units(lines, family)
        rec["status"] = "EXTRACTED"
        rec["units"] = len(texts)
        manifest.append(rec)
        for idx, text in enumerate(texts, 1):
            key = hashlib.sha256(
                (path + "|" + str(idx)).encode("utf-8")).hexdigest()[:12]
            body, cut = truncate(blind(text))
            units.append({
                "key": key, "file": path, "role": role, "ordinal": idx,
                "truncated": cut, "chars": len(text), "text": body,
            })

    rng = random.Random(SHUFFLE_SEED)
    shuffled = list(units)
    rng.shuffle(shuffled)

    payload = [{"key": u["key"], "text": u["text"]} for u in shuffled]
    with open(out_units, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
    with open(out_manifest, "w", encoding="utf-8") as fh:
        json.dump({
            "seed": SHUFFLE_SEED, "min_units": MIN_UNITS,
            "truncate_at": TRUNCATE_AT,
            "files": len(files), "extracted": sum(
                1 for m in manifest if m["status"] == "EXTRACTED"),
            "units": len(units),
            "truncated_units": sum(1 for u in units if u["truncated"]),
            "by_role_passes": {
                r: sum(1 for m in manifest
                       if m["status"] == "EXTRACTED"
                       and m["role"] == r) for r in
                sorted(set(f[2] for f in files))},
            "by_role_units": {
                r: sum(1 for u in units if u["role"] == r) for r in
                sorted(set(f[2] for f in files))},
            "key_map": {u["key"]: {"file": u["file"], "role": u["role"],
                                   "ordinal": u["ordinal"]} for u in units},
            "manifest": manifest,
        }, fh, indent=1, ensure_ascii=False)

    print("files %d  extracted %d  units %d  truncated %d" % (
        len(files), sum(1 for m in manifest if m["status"] == "EXTRACTED"),
        len(units), sum(1 for u in units if u["truncated"])))
    for m in manifest:
        if m["status"] == "UNEXTRACTABLE":
            print("UNEXTRACTABLE %s  %s" % (m["file"], m["family_counts"]))


if __name__ == "__main__":
    main(sys.argv[3:], sys.argv[1], sys.argv[2])
