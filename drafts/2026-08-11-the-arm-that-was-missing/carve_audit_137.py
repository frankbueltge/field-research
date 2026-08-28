#!/usr/bin/env python3
"""carve_audit_137 - how often the pre-registered extractor carves the wrong thing.

Session 137, 2026-08-28. Written AFTER `PREREGISTRATION-137.md` K4 fired on a hand audit of five
files: three of the five disagreed with `extract_units_137.py` on unit boundaries, so no rate is
published from that extraction. This script asks the next question - **is that three-in-five a
property of the five, or of the population?** - over all 53 included files, and classifies nothing.

THE DIAGNOSTIC, AND WHY THIS SHAPE
----------------------------------
The hand audit found one failure mode, twice. Several reports label their findings with a LETTER
and a number - `### F1.`, `### F12.`, `### Claim C3` - and number their *structural sections*
or their *conditions list* with bare digits. The extractor's rule ("split on the numbered family
with the most matches") therefore carves a report's chapters, or its remedies, instead of its
findings, and does so silently and plausibly: it returns a sensible count of sensible-looking units.

So the diagnostic counts, per file, headings of the form

    ^#{2,4} (Claim )?<one or two capitals><digits><delimiter>

- the labelled-finding family the extractor cannot see - and flags the file MIS-CARVED when that
count EXCEEDS the count of the family the extractor actually split on. A file the extractor could
not carve at all is flagged UNEXTRACTABLE, which is the pre-registration's own handling and is
reported separately.

WHAT THE FLAG IS AND IS NOT
---------------------------
It is a **lower bound on mis-carving, not a measurement of it.** It fires only on the one failure
mode the hand audit demonstrated, and only where that family is strictly larger. A report whose
findings are delimited by bold lead-in sentences rather than headings - `INTERLOCUTOR-18.md`, one of
the five audited - is invisible to this diagnostic and was caught only by hand. The true rate of
mis-carving is therefore at least what this prints and may be higher.

VALIDATION, STATED BEFORE THE OUTPUT IS USED
--------------------------------------------
On the five hand-audited files the diagnostic must reproduce the hand verdict exactly - flagging
`VERIFIER-120.md` and `INTERLOCUTOR-7.md` (hand: disagree), flagging `INTERLOCUTOR-18.md` as
UNEXTRACTABLE (hand: disagree), and clearing `VERIFIER-122.md` and `INTERLOCUTOR-129.md` (hand:
agree). The script asserts this and exits non-zero if it fails; a diagnostic that cannot reproduce
the only ground truth this session has is not evidence about the other 48 files.
"""
import json
import re
import sys

LABELLED = re.compile(r"^#{2,4} *(?:Claim +)?[A-Z]{1,2}\d+[.):\s—-]")

# The hand audit of PREREGISTRATION-137.md K4, drawn under seed 1370, recorded here as the
# ground truth this diagnostic is validated against. Counts are this session's, by hand,
# from the files' own finding delimiters; the script's counts come from the manifest.
HAND = {
    "./VERIFIER-122.md": {"hand": 9, "verdict": "AGREE"},
    "./VERIFIER-120.md": {"hand": 18, "verdict": "DISAGREE"},
    "./INTERLOCUTOR-18.md": {"hand": 4, "verdict": "DISAGREE"},
    "./INTERLOCUTOR-129.md": {"hand": 6, "verdict": "AGREE"},
    "./INTERLOCUTOR-7.md": {"hand": 12, "verdict": "DISAGREE"},
}


def main(manifest_path, out_path):
    man = json.load(open(manifest_path, encoding="utf-8"))
    rows = []
    for rec in man["manifest"]:
        text = open(rec["file"], encoding="utf-8").read()
        labelled = sum(1 for ln in text.split("\n") if LABELLED.match(ln))
        won = rec["units"]
        if rec["status"] == "UNEXTRACTABLE":
            flag = "UNEXTRACTABLE"
        elif labelled > won:
            flag = "MIS-CARVED"
        else:
            flag = "CLEAR"
        rows.append({
            "file": rec["file"], "role": rec["role"], "status": rec["status"],
            "script_units": won, "labelled_finding_headings": labelled,
            "flag": flag,
        })

    by_flag = {}
    for r in rows:
        by_flag.setdefault(r["flag"], []).append(r["file"])

    # Validation against the hand audit, before the numbers are used for anything.
    checks = []
    ok = True
    for path, truth in HAND.items():
        row = [r for r in rows if r["file"] == path][0]
        predicted = "DISAGREE" if row["flag"] != "CLEAR" else "AGREE"
        agree = predicted == truth["verdict"]
        ok = ok and agree
        checks.append({"file": path, "hand_units": truth["hand"],
                       "script_units": row["script_units"],
                       "hand_verdict": truth["verdict"], "flag": row["flag"],
                       "diagnostic_reproduces_hand": agree})

    out = {
        "what": "lower bound on mis-carving by extract_units_137.py, over all included files",
        "files": len(rows),
        "counts": {k: len(v) for k, v in sorted(by_flag.items())},
        "units_in_mis_carved_files": sum(
            r["script_units"] for r in rows if r["flag"] == "MIS-CARVED"),
        "units_total": sum(r["script_units"] for r in rows),
        "by_role": {
            role: {
                flag: sum(1 for r in rows if r["role"] == role and r["flag"] == flag)
                for flag in ("CLEAR", "MIS-CARVED", "UNEXTRACTABLE")}
            for role in sorted({r["role"] for r in rows})},
        "hand_audit_validation": checks,
        "diagnostic_reproduces_hand_audit": ok,
        "rows": rows,
    }
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: out[k] for k in (
        "files", "counts", "units_in_mis_carved_files", "units_total",
        "by_role", "diagnostic_reproduces_hand_audit")}, indent=1))
    if not ok:
        print("VALIDATION FAILED - the diagnostic does not reproduce the hand audit",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
