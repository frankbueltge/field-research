#!/usr/bin/env python3
"""How far did the refuted readings actually reach? — the completeness bound, measured.

Session 119, answering condition 5 of `INTERLOCUTOR-11.md`: *state a real completeness bound —
how many of this arc's derived files were built from a run file at a time when it held a
since-refuted reading, and which of those have and have not been checked.*

The method is blunt and therefore honest: every JSON and Markdown file in this draft is scanned
for (a) a reference to a contaminated run file, and (b) a mention of a refuted identifier. A file
that names a contaminated run is a file whose numbers *may* include the refuted unit; a file that
names the identifier is one where the reading is visible on its face. Neither is proof of
contamination — the bound is an upper one, and it is reported as an upper one.

No requests. Reads files already on disk.
"""
import glob
import json
import os
import time

import corrections as corrections_mod

CHECKED = {
    "ledger/diff-baseline-day3.json": "recomputed under the overlay (ledger/corrected/)",
    "ledger/diff-baseline-day4.json": "recomputed under the overlay (ledger/corrected/)",
    "ledger/diff-day2-day3.json": "recomputed under the overlay (ledger/corrected/)",
    "ledger/diff-day3-day4.json": "recomputed under the overlay (ledger/corrected/)",
    "day4-118.json": "session 118 excluded the echo by hand; reproduced as an arm tonight",
    "score-115.json": "dated correction written tonight (score-115-correction-119.json)",
}


def main():
    overlay = corrections_mod.load()
    runs = sorted({rf for rf, _v in overlay})
    vids = sorted({v for _rf, v in overlay})
    run_names = [os.path.basename(r) for r in runs]

    hits = []
    for p in sorted(glob.glob("*.json") + glob.glob("*.md") + glob.glob("ledger/*.json")):
        if p.startswith("ledger/corrected/") or p in ("instrument-audit-119.json",
                                                      "overlay-downstream-119.json",
                                                      "reach-119.json"):
            continue
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        names = [n for n in run_names if n in text]
        ids = [v for v in vids if v in text]
        if not names and not ids:
            continue
        hits.append({"file": p, "names_a_contaminated_run": names,
                     "names_a_refuted_identifier": ids,
                     "checked": CHECKED.get(p),
                     "status": CHECKED.get(p, "NOT INDIVIDUALLY CHECKED")})

    unchecked = [h for h in hits if h["checked"] is None]
    out = {
        "schema": "field-research/contamination-reach/1", "session": 119,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "requests_made": 0,
        "question": ("condition 5 of INTERLOCUTOR-11.md — the completeness bound on how far the "
                     "two refuted readings reached"),
        "contaminated_runs": runs, "refuted_identifiers": vids,
        "n_files_touching_either": len(hits),
        "n_checked": len(hits) - len(unchecked),
        "n_not_individually_checked": len(unchecked),
        "files": hits,
        "what_this_bound_is": ("An UPPER bound and a coarse one. Naming a contaminated run file "
                               "does not mean a file's numbers include the refuted unit — most "
                               "of these are aggregate statistics over thousands of units where "
                               "one unit moves nothing visible, and two are this session's own "
                               "records of the problem. What the bound rules out is the claim "
                               "that the reach was surveyed: before tonight it was not."),
    }
    json.dump(out, open("reach-119.json", "w"), indent=1)
    print(f'{len(hits)} files name a contaminated run or a refuted identifier; '
          f'{len(unchecked)} not individually checked')
    for h in hits:
        print(f'  {h["file"]:52s} {h["status"]}')
    print("wrote reach-119.json")


if __name__ == "__main__":
    main()
