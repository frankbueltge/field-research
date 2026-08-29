#!/usr/bin/env python3
"""carve_audit_138 - the population-wide diagnostic for extractor v2, owed since session 137.

Session 138, 2026-08-29. `CONDITIONS-137.md` binding item 2: *"RUN THE POPULATION-WIDE DIAGNOSTIC
AGAINST v2 BEFORE ANY RATE. carve_audit_137.py was run against v1 and never against v2, and '9 of
53' is a v1 figure that this session let read as general."* This is that diagnostic. **It
classifies nothing and computes no rate.** By the time it runs, `PREREGISTRATION-138.md`'s K4'
gate has already fired on an independent hand count (2 of 5 files disagree), so no rate exists to
be computed; the diagnostic's job is to say whether that two-in-five is a property of the five or
of the population.

THE FOUR DETECTORS, AND WHY EXACTLY THESE
-----------------------------------------
Each detector is one *named-in-advance* failure mode. Three were named before this session saw any
evidence; the fourth is today's, and is marked as such.

  D2 HETEROGENEOUS-LABEL - the chosen family's own identifiers repeat a number, which is what a
     mixed label series looks like: `### F0-a.` ... `### F0-j.` (ten rows of a *"what reproduced"*
     table) sitting in the same family as `### F1.` ... `### F18.` (eighteen findings).
     Named in `CONDITIONS-137.md` item 1 and `PREREGISTRATION-137B.md` §4; the file is
     `VERIFIER-120.md` and the conflated count is 28.

  D3 TABLE-UNCOVERED - the file states an enumeration as rows of a markdown table whose first
     cell is a finding identifier, and v2 has no table family, so those rows cannot be what it
     carved. Named in `PREREGISTRATION-137B.md` §4; the file is `VERIFIER-127.md`, nine findings
     as table rows against fourteen bold lead-ins carved from a section of things that were *not*
     wrong.

  D4 REMEDIES-WON - every delimiter v2 split on lies under a remedies heading (CONDITIONS, WHAT TO
     FIX, RECOMMENDATIONS). *"A remedy is not a finding"* - `extract_units_137_v2.py`'s own
     docstring, defect 1, the thing v2 was built to stop. **Found again today**, by an independent
     hand count, in `INTERLOCUTOR-11.md`: the report's primary enumeration is five bold `**Claim
     N - ...**` lead-ins and v2 returned its six numbered CONDITIONS.

  D5 CHAPTERS-OVER-SUMMARY - the file carries a summary-of-findings section with its own
     enumeration of MIN_UNITS+ items, and v2's delimiters lie outside it. *"It preferred a
     report's chapters to its findings"* - the same docstring, defect 2. **Found again today** in
     `VERIFIER-134.md`: seven `## N.` chapters carved, against a six-item `## Summary of findings`.

D4 and D5 are v2's own two stated repairs, failing on files v2's design never saw. They are
written here as detectors rather than as sentences so that the next session can see how far each
one reaches across the other 43 files instead of taking this session's word for it.

A fifth signal, CONTESTED, is reported and **is not a defect claim**: more than one family reached
MIN_UNITS, so the family choice was a contest rather than a reading. It bounds where the other four
could bite and nothing more.

WHAT THIS IS AND IS NOT
-----------------------
**A lower bound on mis-carving, not a measurement of it**, exactly as `carve_audit_137.py` says of
itself. Every detector fires on a *syntactic* trace of a failure mode already demonstrated by hand.
A report that mis-carves in some sixth way no hand count has met is invisible here and will be
counted as clean. **A file this diagnostic does not flag is a file it has nothing to say about.**

VALIDATION, STATED BEFORE THE OUTPUT IS USED
--------------------------------------------
Eleven files have a hand verdict against **v2's** counts: the five of `HAND-AUDIT-137.md` §3 (seed
1372, counted by the session that built v2), the five of `PREREGISTRATION-138.md` §2 (seed 1380,
counted by a convened role that did not build v2), and `VERIFIER-120.md`, whose 28-vs-18 conflation
two reviewers established independently at session 137. The script asserts:

  (a) every hand-DISAGREE file is flagged by at least one of D2-D5, and
  (b) no hand-AGREE file is flagged by any of D2-D5.

It exits non-zero if either fails. A diagnostic that cannot reproduce the only ground truth this
practice has is not evidence about the other 42 files. Note what (b) costs: the detectors were
written after today's two disagreements were diagnosed by hand, so passing (a) on those two files
is not a test of anything. **The files that test this instrument are the nine it did not come
from**, and they are the ones to read the assertion against.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract_units_137_v2 as v2

MIN_UNITS = v2.MIN_UNITS

LABEL_ID = re.compile(r"^#{2,4} *(?:Claim +)?([A-Z]{1,2})(\d+)")
REMEDY_HEAD = re.compile(
    r"^#{1,4} *(?:\**)(?:THE +)?(?:CONDITIONS?|REMEDIES|RECOMMENDATIONS?|"
    r"WHAT (?:TO|MUST BE|SHOULD BE|I ASK)|REQUIRED (?:FIXES|CHANGES)|FIXES)\b", re.I)
SUMMARY_HEAD = re.compile(
    r"^#{1,4} *(?:\**)(?:SUMMARY OF (?:THE )?FINDINGS|FINDINGS SUMMARY|"
    r"(?:THE )?FINDINGS(?: IN BRIEF| AT A GLANCE)?)\s*\**\s*$", re.I)
ANY_HEAD = re.compile(r"^#{1,4} ")
TABLE_ROW = re.compile(r"^\|")
# a first cell that reads as a finding identifier: 1 | **2** | F3 | C10 | V7 | I13
TABLE_ID = re.compile(r"^\| *\**((?:[A-Z]{1,2})?\d+)\.?\** *\|")
TABLE_SEP = re.compile(r"^\|[ :|-]+\|?\s*$")

# The eleven hand verdicts against v2's counts. `hand` is the counted number of items in the
# report's own primary enumeration; `v2` is filled from the manifest at run time and asserted.
HAND = {
    # HAND-AUDIT-137.md §3 - seed 1372, counted by the session that BUILT v2.
    "VERIFIER-133.md":    {"hand": 4,  "verdict": "AGREE",    "counter": "builder", "seed": 1372},
    "INTERLOCUTOR-13.md": {"hand": 9,  "verdict": "AGREE",    "counter": "builder", "seed": 1372},
    "VERIFIER-129.md":    {"hand": 6,  "verdict": "AGREE",    "counter": "builder", "seed": 1372},
    "INTERLOCUTOR-2.md":  {"hand": 18, "verdict": "AGREE",    "counter": "builder", "seed": 1372},
    "VERIFIER-127.md":    {"hand": 9,  "verdict": "DISAGREE", "counter": "builder", "seed": 1372},
    # PREREGISTRATION-138.md §2 - seed 1380, counted by a convened role that did NOT build v2,
    # published unedited at HANDCOUNT-138.md.
    "INTERLOCUTOR-11.md": {"hand": 5,  "verdict": "DISAGREE", "counter": "independent", "seed": 1380},
    "INTERLOCUTOR-15.md": {"hand": 4,  "verdict": "AGREE",    "counter": "independent", "seed": 1380},
    "READER-128-3.md":    {"hand": 6,  "verdict": "AGREE",    "counter": "independent", "seed": 1380},
    "VERIFIER-125.md":    {"hand": 5,  "verdict": "AGREE",    "counter": "independent", "seed": 1380},
    "VERIFIER-134.md":    {"hand": 6,  "verdict": "DISAGREE", "counter": "independent", "seed": 1380},
    # CONDITIONS-137.md item 1 - established independently by two reviewers at session 137.
    "VERIFIER-120.md":    {"hand": 18, "verdict": "DISAGREE", "counter": "two reviewers", "seed": None},
}


def section_of(lines, i):
    """The nearest heading at or above line i, or '' if the line is above every heading."""
    for j in range(i, -1, -1):
        if ANY_HEAD.match(lines[j]):
            return lines[j]
    return ""


def d2_heterogeneous(lines, family):
    """The chosen family repeats an identifier number - a mixed label series."""
    if family != "LABELLED":
        return None
    ids = []
    for ln in lines:
        if v2.PAT[family].match(ln):
            m = LABEL_ID.match(ln)
            if m:
                ids.append((m.group(1), int(m.group(2))))
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if not dupes:
        return None
    return {"repeated": ["%s%d" % d for d in dupes],
            "repeat_count": sum(ids.count(d) for d in dupes),
            "family_total": len(ids)}


def d3_table(lines, family, chosen_count):
    """A markdown table whose rows are identifier-led, which no v2 family can carve."""
    rows, best = [], None
    for i, ln in enumerate(lines):
        if TABLE_ROW.match(ln) and not TABLE_SEP.match(ln):
            m = TABLE_ID.match(ln)
            if m:
                rows.append((i, m.group(1)))
    if len(rows) < MIN_UNITS:
        return None
    # group contiguous-ish runs of identifier rows into one table
    runs, cur = [], [rows[0]]
    for r in rows[1:]:
        if r[0] - cur[-1][0] <= 6:
            cur.append(r)
        else:
            runs.append(cur)
            cur = [r]
    runs.append(cur)
    for run in runs:
        if len(run) >= MIN_UNITS and (best is None or len(run) > len(best)):
            best = run
    if best is None:
        return None
    return {"table_rows": len(best),
            "first_line": best[0][0] + 1,
            "section": section_of(lines, best[0][0])[:120].strip(),
            "chosen_count": chosen_count}


def d4_remedies(lines, family):
    """Every delimiter v2 split on lies under a remedies heading."""
    hits = [i for i, ln in enumerate(lines) if v2.PAT[family].match(ln)]
    if not hits:
        return None
    heads = [section_of(lines, i) for i in hits]
    if all(REMEDY_HEAD.match(h or "") for h in heads):
        return {"carved": len(hits), "under": heads[0].strip()[:120]}
    return None


def d5_chapters_over_summary(lines, family):
    """A summary-of-findings section enumerates MIN_UNITS+ items and v2 carved outside it."""
    start = None
    for i, ln in enumerate(lines):
        if SUMMARY_HEAD.match(ln):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if ANY_HEAD.match(lines[j]):
            end = j
            break
    body = lines[start + 1:end]
    items = sum(1 for ln in body if v2.LISTNUM.match(ln) or v2.BOLDNUM.match(ln))
    if items < MIN_UNITS:
        return None
    hits = [i for i, ln in enumerate(lines) if v2.PAT[family].match(ln)]
    inside = sum(1 for i in hits if start <= i < end)
    if inside:
        return None
    return {"summary_items": items, "summary_line": start + 1,
            "carved_outside": len(hits), "heading": lines[start].strip()[:120]}


def main(manifest_path, out_path):
    man = json.load(open(manifest_path, encoding="utf-8"))
    rows, flagged, contested = [], [], []
    for rec in man["manifest"]:
        path = rec["file"]
        base = os.path.basename(path)
        lines = open(path, encoding="utf-8").read().split("\n")
        family, counts = v2.pick_family(lines)
        assert family == rec["family"], "family drift on " + base
        reached = sorted([n for n, c in counts.items() if c >= MIN_UNITS])
        row = {"file": base, "role": rec["role"], "status": rec["status"],
               "family": family, "units": rec["units"],
               "families_reaching_min": reached,
               "contested": len(reached) > 1, "detectors": {}}
        if rec["status"] == "EXTRACTED":
            for name, res in (("D2_HETEROGENEOUS_LABEL", d2_heterogeneous(lines, family)),
                              ("D3_TABLE_UNCOVERED", d3_table(lines, family, rec["units"])),
                              ("D4_REMEDIES_WON", d4_remedies(lines, family)),
                              ("D5_CHAPTERS_OVER_SUMMARY",
                               d5_chapters_over_summary(lines, family))):
                if res:
                    row["detectors"][name] = res
        if base in HAND:
            row["hand"] = HAND[base]["hand"]
            row["hand_verdict"] = HAND[base]["verdict"]
            row["hand_counter"] = HAND[base]["counter"]
        rows.append(row)
        if row["detectors"]:
            flagged.append(base)
        if row["contested"]:
            contested.append(base)

    # Validation against the eleven hand verdicts, asserted before the output is used.
    val = {"checked": 0, "failures": []}
    for row in rows:
        if "hand_verdict" not in row:
            continue
        val["checked"] += 1
        hit = bool(row["detectors"])
        if row["hand_verdict"] == "DISAGREE" and not hit:
            val["failures"].append(row["file"] + ": hand DISAGREE, no detector fired")
        if row["hand_verdict"] == "AGREE" and hit:
            val["failures"].append(
                row["file"] + ": hand AGREE, but flagged " + ",".join(row["detectors"]))
        if row["hand_verdict"] == "DISAGREE" and row["units"] == row["hand"]:
            val["failures"].append(row["file"] + ": hand DISAGREE but counts are equal")
        if row["hand_verdict"] == "AGREE" and row["units"] != row["hand"]:
            val["failures"].append(
                row["file"] + ": hand AGREE but %d != %d" % (row["units"], row["hand"]))

    by_det = {}
    for row in rows:
        for d in row["detectors"]:
            by_det.setdefault(d, []).append(row["file"])

    out = {
        "what_this_is": "a LOWER BOUND on mis-carving by extract_units_137_v2.py over the 53 "
                        "included files; it classifies nothing and computes no rate",
        "files": len(rows),
        "extracted": sum(1 for r in rows if r["status"] == "EXTRACTED"),
        "unextractable": [r["file"] for r in rows if r["status"] != "EXTRACTED"],
        "flagged_files": sorted(flagged),
        "n_flagged": len(flagged),
        "by_detector": {k: sorted(v) for k, v in sorted(by_det.items())},
        "contested_family_choice": sorted(contested),
        "n_contested": len(contested),
        "hand_verdicts": {r["file"]: {"v2": r["units"], "hand": r["hand"],
                                      "verdict": r["hand_verdict"],
                                      "counter": r["hand_counter"],
                                      "detectors": sorted(r["detectors"])}
                          for r in rows if "hand_verdict" in r},
        "validation": val,
        "rows": rows,
    }
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print("files %d  extracted %d  FLAGGED %d  contested %d"
          % (out["files"], out["extracted"], out["n_flagged"], out["n_contested"]))
    for d, fs in sorted(by_det.items()):
        print("  %-26s %2d  %s" % (d, len(fs), ", ".join(fs)))
    print("validation: %d hand verdicts checked, %d failures"
          % (val["checked"], len(val["failures"])))
    for f in val["failures"]:
        print("  FAIL " + f)
    return 1 if val["failures"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
