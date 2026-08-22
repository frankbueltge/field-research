#!/usr/bin/env python3
"""Sweep the whole repository for the claim withdrawn by ERRATA-131 E34, and say where it still
reads as live.

Session 132, 2026-08-22. E34 withdrew, on 2026-08-22, the claim that the instrument's daily hour
"was never an independently chosen parameter … it is wherever the session already was". Its own
table lists **six** sites and says all six were marked in place. This script exists because the
constitutionally required memory pass of the next session found the withdrawn wording standing as a
live assertion in `memory/open-questions.md`, which is not one of the six.

The rule this enforces is not a preference. PROTOCOL v3, "Verifiability and legal hygiene", rule 6:
*"corrections and discards stay in the record, clearly marked as rejected/superseded — a discarded
claim must never read as live."*

WHAT IT LOOKS FOR, AND WHAT THAT CANNOT CATCH
---------------------------------------------
Three phrase families drawn from E34's own quotation of the withdrawn text. A hit is a site where
one of them occurs; a site is judged CLEARED if a withdrawal marker stands in the same paragraph or
in the nearest markdown heading above it, and LIVE if not. **The marker must be that close on
purpose** — one four screens below a sentence is the defect session 130 recorded about a generated
page, not a repair of it. Verbatim material published unedited (a reviewer's file, a block quote) is
never annotated by this practice and is reported as UNEDITED-BY-RULE rather than as either.

**A paraphrase still passes.** This is the same limit `errata_check.py` states about itself, and it
is stated here rather than left for a reader to discover: this finds the wording, not the belief.

USAGE
    python3 e34_sweep.py            # writes e34-sweep-132.json, exits 1 if any site is LIVE
    python3 e34_sweep.py --report   # human-readable, changes nothing
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Drawn from E34's own quotation of what was written. Case-insensitive, whitespace-flexible, so a
# sentence broken across a line is still found — that exact failure cost this practice a
# disagreement in the same morning E34 was written (`VERIFIER-131.md`).
PATTERNS = {
    "never-chosen": r"daily\W+hour\W*[\"'“”]?\W*was\W+never|hour\W*[\"'“”]?\W+was\W+never\W+(?:an\W+independently\W+)?chosen|never\W+an\W+independently\W+chosen\W+parameter",
    "wherever-the-session": r"wherever\W+the\W+session\W+(?:already\W+)?was",
    "moved-when-sessions-moved": r"it\W+moved\W+when\W+the\W+sessions\W+moved",
}

# A site is cleared if any of these stands in the same paragraph as the hit, or in the nearest
# markdown heading above it. The heading clause exists because E34's own "What was written"
# quotation sits under a heading that says WITHDRAWN — the first version of this script called that
# a live claim, which would have made the erratum a defect for containing the text it withdraws.
MARKERS = r"withdrawn|E34|struck|does not follow|not established|cannot test|never tests"

SKIP_DIRS = {".git", "node_modules", "__pycache__"}
# The sweep's own report is excluded from the sweep's own search space. Not tidiness: the report
# quotes every site it finds, so it is itself a site, and each run therefore found one more than the
# last and the count never converged. Found by running the thing twice — 11 sites, then 12, then 13,
# with nothing in the record having changed between the second and the third. **An instrument whose
# output is inside its own population measures itself measuring.** Recorded in `ERRATA-132.md`.
OUT_NAME = "e34-sweep-132.json"
# The reviewers' own reports are published unedited and are never annotated — session 131 made that
# rule explicit for a different erratum (`CONDITIONS-131.md` finding 5, and E25's seventh site).
UNEDITED_BY_RULE = ("INTERLOCUTOR-", "VERIFIER-", "CRITIQUE-", "READER-")


def paragraphs(text):
    out, pos = [], 0
    for para in re.split(r"\n\s*\n", text):
        idx = text.index(para, pos)
        out.append((idx, para))
        pos = idx + len(para)
    return out


def heading_above(text, start):
    """The nearest markdown heading before this offset, or ''."""
    heads = re.findall(r"^#{1,6} .*$", text[:start], re.M)
    return heads[-1] if heads else ""


def is_block_quote(para):
    """Verbatim material published unedited — a reviewer's report quoted into the journal, a
    critique block. The rule that such material is never annotated is this practice's own
    (`CONDITIONS-131.md` finding 5). A quotation of a claim inside a refutation of it is not the
    claim standing live."""
    lines = [ln for ln in para.splitlines() if ln.strip()]
    return bool(lines) and all(ln.lstrip().startswith(">") for ln in lines)


def main():
    sites = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith((".md", ".json", ".py", ".txt")):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT)
            if fn == OUT_NAME:
                continue
            if rel.startswith("archive" + os.sep):
                continue  # the archive is the record of superseded states and is never edited
            try:
                text = open(path, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            for start, para in paragraphs(text):
                hits = [k for k, p in PATTERNS.items() if re.search(p, para, re.I | re.S)]
                if not hits:
                    continue
                cleared = bool(re.search(MARKERS, para, re.I)) or bool(
                    re.search(MARKERS, heading_above(text, start), re.I))
                unedited = (os.path.basename(rel).startswith(UNEDITED_BY_RULE)
                            or is_block_quote(para))
                sites.append({
                    "file": rel,
                    "line": text[:start].count("\n") + 1,
                    "patterns": sorted(hits),
                    "state": "UNEDITED-BY-RULE" if unedited
                             else ("CLEARED" if cleared else "LIVE"),
                    "excerpt": " ".join(para.split())[:300],
                })

    live = [s for s in sites if s["state"] == "LIVE"]
    result = {
        "schema": "field-research/erratum-sweep/1",
        "computed_by": "e34_sweep.py, session 132",
        "erratum": "ERRATA-131.md E34",
        "what_this_checks": "whether the claim E34 withdrew still reads as live anywhere outside "
                            "archive/, which is never edited",
        "limit": "a paraphrase still passes; this finds the wording, not the belief",
        "n_sites": len(sites),
        "n_live": len(live),
        "n_cleared": sum(1 for s in sites if s["state"] == "CLEARED"),
        "n_unedited_by_rule": sum(1 for s in sites if s["state"] == "UNEDITED-BY-RULE"),
        "e34_claimed_sites": 6,
        "sites": sorted(sites, key=lambda s: (s["file"], s["line"])),
    }

    if "--report" in sys.argv:
        for s in result["sites"]:
            print(f"{s['state']:>16}  {s['file']}:{s['line']}  {s['patterns']}")
            print(f"                  {s['excerpt'][:180]}")
        print(f"\n{result['n_sites']} sites · {result['n_live']} LIVE · "
              f"{result['n_cleared']} CLEARED · {result['n_unedited_by_rule']} unedited by rule")
    else:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUT_NAME)
        with open(out, "w") as f:
            json.dump(result, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print(f"wrote {os.path.basename(out)}: {result['n_sites']} sites, {result['n_live']} LIVE")

    return 1 if live else 0


if __name__ == "__main__":
    sys.exit(main())
