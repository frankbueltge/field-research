#!/usr/bin/env python3
"""errata_check - a published correction must not come back.

Session 123, 2026-08-16, written after the fourth gauntlet failed.

WHY THIS EXISTS
---------------
On 2026-08-15 the first gauntlet on this arc's receiver bundle published a table of **18 errata**,
each with the false statement and its true value. On 2026-08-16 this practice rebuilt that bundle
from scratch, wrote its prose by hand from the old prose, and shipped **at least six of those
eighteen corrections back into it, unchanged**. Both reviewers found them independently. Every one
of the blocking ones is a sentence containing **no digit**, so the prose auditor this session
built - which extracts digits and compares them to a provenance table - could not have caught a
single one of them by construction.

`memory/downstream-commitments.md` and this practice's own legal-hygiene rule 6 both say a
correction stays in the record and a discarded claim must never read as live. Nothing enforced it.
This does.

WHAT IT IS
----------
A registry of corrections this practice has published, each as:

  * `false_phrase`   - a regex matching the wording that was found false
  * `true_value`     - what is actually the case, in one sentence
  * `source`         - the dated document that published the correction
  * `corrected_when` - OPTIONAL regex. A correction is often made IN PLACE: the old wording stays
    because the sentence now says what was wrong with it. This names the phrase that must appear
    in the same file for a match to count as corrected rather than as a regression. Without it a
    corrected-in-place sentence would be reported forever, and a check that cries wolf trains its
    readers to ignore it. It is also the obvious way to defeat this check by accident: a file that
    happens to contain the corrected_when phrase for an unrelated reason suppresses the finding
    for that whole file.

and a check that scans a directory for any of those phrases. A hit is a **regression**: a
correction the practice published and then un-published by rewriting around it.

WHAT IT CANNOT DO, STATED PLAINLY
----------------------------------
It matches wording, not meaning. A false claim restated in different words passes it, and a true
claim that happens to quote the old wording - as an erratum document does, on purpose - trips it.
So the errata documents themselves are excluded by path, and that exclusion is the obvious hole:
a bundle file could evade this check by paraphrasing. It catches the failure that actually
happened four times, which is verbatim reproduction of prose that was already corrected, and it
makes no claim beyond that.

The registry is also **incomplete by construction**: it holds the corrections a session took the
trouble to enter. `python3 errata_check.py --coverage` reports how many errata the published
tables contain against how many are registered here, so the gap is visible rather than implied.

Usage:
    python3 errata_check.py deliverable-v0.3          # check a bundle; exit 1 on any regression
    python3 errata_check.py --coverage                # how much of the published errata is covered
"""
import argparse
import json
import os
import re
import sys

# Paths whose whole purpose is to quote the false wording. Excluded, by design and by name.
EXCLUDE_SUBSTRINGS = ("ERRATA-", "GAUNTLET-", "INTERLOCUTOR-", "VERIFIER-", "CONDITIONS-",
                      "discharge-", "errata_check.py")

# The registry. Every entry cites the dated document that published the correction.
REGISTRY = [
    {
        "id": "E1/2026-08-15",
        "false_phrase": r"twenty synthetic identifiers[^.]{0,120}same code",
        "true_value": ("nineteen of the twenty returned the refusal code; the twentieth returned "
                       "no code at all - a transport failure, which is the absence of a code, not "
                       "the same one"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E1; re-confirmed session 123 "
                  "(discharge-123b.json)",
        "corrected_when": r"nineteen of the twenty|no code at all",
    },
    {
        "id": "E2/2026-08-15",
        "false_phrase": r"logged in(?:to)? every run file before the first",
        "true_value": ("false for the baseline union, which the bundle lists as one of its source "
                       "runs: its own vantage field says it was carried from the producing runs, "
                       "not logged before a first request"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E2; re-confirmed session 123",
        "corrected_when": r"carried from the producing runs",
    },
    {
        "id": "E3/2026-08-15",
        "false_phrase": r"checked against the endpoint's own returned metadata",
        "true_value": ("no such check exists in this arc: the probe stores no creation time "
                       "returned by the endpoint, so there is nothing to check a decoded age "
                       "against"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E3; re-confirmed session 123",
        "corrected_when": r"no such check exists|not checked against anything",
    },
    {
        "id": "E7/2026-08-15",
        "false_phrase": r"(?:that are\s*\*{0,2}\s*not\s*\*{0,2}\s*|and not\s+)videos",
        "true_value": ("248 of the 249 display-truncated control identifiers do not resolve; one "
                       "is a real video predating the platform's current identifier scheme"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E7; re-confirmed session 123",
        "corrected_when": r"248 of|one is a real video|is a real video",
    },
    {
        "id": "E11/2026-08-15",
        "false_phrase": r"TEMPLATE\s*[-—]\s*the running session sets this",
        "true_value": ("an unfilled placeholder, not a run identifier; the manifest entry it sits "
                       "in must carry the real run id or say plainly that it is unknown"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E11; re-confirmed session 123",
    },
    {
        "id": "E17/2026-08-15",
        "false_phrase": r"0\.14 (?:percentage points|pp)",
        "true_value": ("on the balanced panel of units determinate on every day the spread is "
                       "0.0577 pp; the 0.14 pp figure is 2.35x larger and the excess is which "
                       "units fell out as INDETERMINATE, not anything about the platform"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E17; re-confirmed session 123",
        "corrected_when": r"0\.0577|balanced\s*\n?panel",
    },
    {
        "id": "V3-E4/2026-08-15",
        # `21+` reads "at least 21" and is true of 37, so it is not the false claim; the false
        # claim is a bare 21 asserted as the count. The `(?!\+)` is the whole difference and it
        # was added after this check reported a true sentence as a regression.
        "false_phrase": r"\b21\b(?!\+)[^|\n]{0,60}language editions",
        "true_value": ("37 encyclopedia language editions contribute at least one article-arm unit "
                       "to this panel, re-derived independently three times"),
        "source": "CONDITIONS-120.md V3 (ACCEPTED, CARRIED); re-derived session 123 "
                  "(discharge-123.json)",
        "corrected_when": r"\b37\b",
    },
    {
        "id": "I-26day/2026-08-16",
        "false_phrase": r"threshold is measured rather than picked",
        "true_value": ("withdrawn: the crossover is a family running from 1 day to 26 on a "
                       "comparand chosen after the fact, and 26 was its most forgiving member"),
        "source": "INTERLOCUTOR-14.md, session 122; ERRATA-122.md",
    },
]


def scan(root):
    hits = []
    files = 0
    for dirpath, _, names in os.walk(root):
        for n in sorted(names):
            p = os.path.join(dirpath, n)
            if any(s in p for s in EXCLUDE_SUBSTRINGS):
                continue
            if not n.endswith((".md", ".json", ".txt", ".csv")):
                continue
            try:
                text = open(p, errors="replace").read()
            except OSError:
                continue
            files += 1
            for e in REGISTRY:
                if e.get("corrected_when") and re.search(e["corrected_when"], text):
                    continue        # corrected in place, in this file
                for m in re.finditer(e["false_phrase"], text):
                    hits.append({
                        "erratum": e["id"],
                        "file": os.path.relpath(p, root),
                        "matched": m.group(0)[:120],
                        "true_value": e["true_value"],
                        "source": e["source"],
                    })
    return files, hits


def coverage():
    """How many errata the published tables hold, against how many are registered here."""
    tables = ["deliverable/GAUNTLET-2026-08-15.md", "ERRATA-121.md", "ERRATA-122.md",
              "ERRATA-123.md"]
    found = {}
    for t in tables:
        if os.path.exists(t):
            found[t] = len(set(re.findall(r"^\|\s*(E\d+)\s*\|", open(t, errors="replace").read(),
                                          re.M))) or len(set(re.findall(r"^###?\s*(E\d+)\b",
                                          open(t, errors="replace").read(), re.M)))
    return {"errata_published_per_table": found,
            "total_published": sum(found.values()),
            "registered_here": len(REGISTRY),
            "note": ("the registry is entered by hand, one line per correction. Anything published "
                     "and not entered is unchecked, and this number is how much.")}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default="deliverable-v0.3")
    ap.add_argument("--coverage", action="store_true")
    ap.add_argument("--out", default="errata-check.json")
    a = ap.parse_args(argv)

    if a.coverage:
        print(json.dumps(coverage(), indent=1))
        return 0

    files, hits = scan(a.root)
    report = {"schema": "field-research/errata-regression-check/1",
              "root": a.root, "files_scanned": files,
              "registry_size": len(REGISTRY),
              "coverage": coverage(),
              "n_regressions": len(hits), "regressions": hits}
    json.dump(report, open(a.out, "w"), indent=1)
    for h in hits:
        print(f'REGRESSION {h["erratum"]:16s} {h["file"]:34s} "{h["matched"]}"')
    print(json.dumps({"files_scanned": files, "registry_size": len(REGISTRY),
                      "n_regressions": len(hits)}, indent=1))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
