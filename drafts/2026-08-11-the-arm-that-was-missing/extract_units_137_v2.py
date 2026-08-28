#!/usr/bin/env python3
"""extract_units_137_v2 - the extractor rebuilt against the three defects that fired K4.

Session 137, 2026-08-28. **Nothing is classified with this script in this session, and no rate is
computed from it.** `PREREGISTRATION-137.md` K4 fired on v1 - three of five hand-audited files
disagreed on unit boundaries - and K4's consequence is that no rate is published. This file is the
repair, built so that a later session inherits an instrument rather than a diagnosis, and it is
gated by a **fresh** hand audit on five files v1 never touched, drawn under a new seed, whose
outcome is published either way.

WHAT V1 GOT WRONG, from the hand audit (`HAND-AUDIT-137.md`)
------------------------------------------------------------
1. **It could not see letter-numbered findings.** `VERIFIER-120.md` delimits eighteen findings as
   `### F1.` … `### F18.` and its *remedies* as a bare `1.` … `16.` list. v1's "most matches wins"
   split the remedies. A remedy is not a finding.
2. **It preferred a report's chapters to its findings.** `INTERLOCUTOR-7.md` numbers six structural
   sections `## 1.` … `## 6.` and delimits its seven findings as `### Claim C1` … `C7`, with five
   more as `**3.1 —**` … `**3.5 —**`. v1 returned the six chapters.
3. **It carved nothing at all from a report that delimits by bold lead-in sentence.** Three
   Interlocutor and three Verifier reports state their findings as `**<claim>.**` paragraphs under
   thematic headings, with no numbering anywhere; v1 reported six files UNEXTRACTABLE.

THE V2 RULE
-----------
Same shape - one family per file, the report's own granularity - with three changes, each aimed at
one defect above and none at anything else:

  (1) A new family **LABELLED**: `^#{2,4} (Claim )?<one or two capitals><digits><delim>`.
  (2) **Specific families win by kind, not by count.** If CHARGE or LABELLED reaches MIN_UNITS, it
      is chosen even when a bare-numbered family has more matches. Bare numbers are ambiguous
      between findings, chapters and remedies; an explicit `Charge 4` or `F12` is not.
  (3) A new fallback family **BOLDLEAD**: `^\\*\\*` at column 0, used only when every other family
      is below MIN_UNITS.

  A fourth change was written, tested and **withdrawn before any gate was run**: a rule splitting a
  unit again by any other family it contained MIN_UNITS of. It was meant to recover
  `INTERLOCUTOR-7.md`'s five `3.x` items. It shattered every long unit it touched - it took
  `VERIFIER-122.md` from 9 to 15 against a hand count of 9, and `VERIFIER-120.md` from 28 to 44 -
  and it is removed rather than tuned. `subsplit()` is left in the file, unused and unreferenced,
  so that the discarded rule stays readable beside the one that replaced it.

THE HONEST STATUS OF THIS FILE
------------------------------
Every one of those changes was designed **after** seeing which files v1 got wrong. That is fishing
unless it is tested against files that were not used to design it, so the gate is
`hand_audit_v2_137.py`'s five fresh files, drawn under seed 1372 from the files v1's audit did not
touch, hand-counted after this script was written and before its output was looked at. **If v2
fails that gate the failure is published as the session's result**, and the standing finding
becomes that this practice's own review reports are not mechanically carvable at finding
granularity - which would itself be the reason the population fix has been named three times and
not done.
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

CHARGE = re.compile(r"^#{2,4} *(?:Charge|Finding|Objection|Defect)\b[^\n]*?\d")
LABELLED = re.compile(r"^#{2,4} *(?:Claim +)?[A-Z]{1,2}\d+[.):\s—-]")
HEADNUM = re.compile(r"^#{2,4} *\d+[.)]")
BOLDNUM = re.compile(r"^\*\*\d+(?:\.\d+)?[.)]?[ —-]")
LISTNUM = re.compile(r"^\d+[.)] ")
BOLDLEAD = re.compile(r"^\*\*[^\s*]")

SPECIFIC = [("CHARGE", CHARGE), ("LABELLED", LABELLED)]
GENERIC = [("HEADNUM", HEADNUM), ("BOLDNUM", BOLDNUM), ("LISTNUM", LISTNUM)]
FALLBACK = [("BOLDLEAD", BOLDLEAD)]
ALL = SPECIFIC + GENERIC + FALLBACK
PAT = dict(ALL)

ROLE_OF_PREFIX = {"INTERLOCUTOR": "interlocutor", "VERIFIER": "verifier",
                  "READER": "reader"}

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


def counts_of(lines):
    return {name: sum(1 for ln in lines if pat.match(ln)) for name, pat in ALL}


def pick_family(lines):
    c = counts_of(lines)
    for name, _ in SPECIFIC:
        if c[name] >= MIN_UNITS:
            return name, c
    best = max((n for n, _ in GENERIC), key=lambda n: c[n])
    if c[best] >= MIN_UNITS:
        return best, c
    if c["BOLDLEAD"] >= MIN_UNITS:
        return "BOLDLEAD", c
    return best, c


def split_on(lines, family):
    pat = PAT[family]
    starts = [i for i, ln in enumerate(lines) if pat.match(ln)]
    out = []
    for n, s in enumerate(starts):
        e = starts[n + 1] if n + 1 < len(starts) else len(lines)
        out.append(lines[s:e])
    return out


def subsplit(unit_lines, chosen):
    """Split a unit again if it contains MIN_UNITS+ delimiters of another family."""
    body = unit_lines[1:]
    c = {name: sum(1 for ln in body if pat.match(ln)) for name, pat in ALL}
    for name, _ in SPECIFIC + GENERIC:
        if name == chosen:
            continue
        if c[name] >= MIN_UNITS:
            pat = PAT[name]
            starts = [i for i, ln in enumerate(body) if pat.match(ln)]
            head = unit_lines[:1] + body[:starts[0]]
            pieces = [head]
            for n, s in enumerate(starts):
                e = starts[n + 1] if n + 1 < len(starts) else len(body)
                pieces.append(body[s:e])
            return pieces
    return [unit_lines]


def blind(t):
    for pat, repl in BLIND_PATTERNS:
        t = pat.sub(repl, t)
    return t


def truncate(t):
    if len(t) <= TRUNCATE_AT:
        return t, False
    cut = t[:TRUNCATE_AT]
    nl = cut.rfind("\n")
    if nl > TRUNCATE_AT // 2:
        cut = cut[:nl]
    return cut + "\n\n[UNIT TRUNCATED FOR LENGTH]", True


def main(dirs, out_units, out_manifest):
    files = []
    for d in dirs:
        for name in sorted(os.listdir(d)):
            if name.endswith(".md") and not name.startswith("READERS-"):
                prefix = name.split("-")[0]
                if prefix in ROLE_OF_PREFIX:
                    files.append((d, name, ROLE_OF_PREFIX[prefix]))

    manifest, units = [], []
    for d, name, role in files:
        path = os.path.join(d, name)
        raw = open(path, encoding="utf-8").read()
        lines = raw.split("\n")
        family, c = pick_family(lines)
        rec = {"file": path, "role": role, "words": len(raw.split()),
               "family": family, "family_counts": c}
        if c[family] < MIN_UNITS:
            rec.update(status="UNEXTRACTABLE", units=0)
            manifest.append(rec)
            continue
        pieces = split_on(lines, family)
        texts = ["\n".join(p).strip() for p in pieces]
        texts = [t for t in texts if t]
        rec.update(status="EXTRACTED", units=len(texts))
        manifest.append(rec)
        for idx, text in enumerate(texts, 1):
            key = hashlib.sha256(
                (path + "|v2|" + str(idx)).encode("utf-8")).hexdigest()[:12]
            body, cut = truncate(blind(text))
            units.append({"key": key, "file": path, "role": role,
                          "ordinal": idx, "truncated": cut,
                          "chars": len(text), "text": body})

    rng = random.Random(SHUFFLE_SEED)
    shuffled = list(units)
    rng.shuffle(shuffled)
    json.dump([{"key": u["key"], "text": u["text"]} for u in shuffled],
              open(out_units, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    roles = sorted({f[2] for f in files})
    json.dump({
        "extractor": "v2", "seed": SHUFFLE_SEED, "min_units": MIN_UNITS,
        "truncate_at": TRUNCATE_AT, "files": len(files),
        "extracted": sum(1 for m in manifest if m["status"] == "EXTRACTED"),
        "units": len(units),
        "truncated_units": sum(1 for u in units if u["truncated"]),
        "by_role_passes": {r: sum(1 for m in manifest if m["role"] == r
                                  and m["status"] == "EXTRACTED") for r in roles},
        "by_role_units": {r: sum(1 for u in units if u["role"] == r) for r in roles},
        "key_map": {u["key"]: {"file": u["file"], "role": u["role"],
                               "ordinal": u["ordinal"]} for u in units},
        "manifest": manifest,
    }, open(out_manifest, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print("v2: files %d  extracted %d  units %d  truncated %d" % (
        len(files), sum(1 for m in manifest if m["status"] == "EXTRACTED"),
        len(units), sum(1 for u in units if u["truncated"])))
    for m in manifest:
        if m["status"] == "UNEXTRACTABLE":
            print("UNEXTRACTABLE %s %s" % (m["file"], m["family_counts"]))


if __name__ == "__main__":
    main(sys.argv[3:], sys.argv[1], sys.argv[2])
