#!/usr/bin/env python3
"""versions_provenance_126 - provenance for the version-table rows this session added by hand.

Session 126, 2026-08-18. `CONDITIONS-125.md` binding item 1 requires the repairs be made **as
edits, not a rebuild** - so `build_v03.py`, which is what normally writes
`FIGURE-PROVENANCE.json`, is deliberately not run. That leaves the numbers in the two version
rows this session edited outside the provenance table, which the prose guard reported the moment
the edits were made: six unmatched tokens, all in `VERSIONS.md`, all typed by this session.

**That is the defect class arriving in real time, in the session whose move is to close it**, and
it is recorded rather than quietly fixed: the rule this practice wrote is that a number in the
prose which is not in the provenance table was typed by a human and is a defect. Six were. This
script does not excuse them; it gives each one a source or a stated reason, which is the only
disposition the rule allows.

WHAT IS COMPUTED AND WHAT IS DECLARED
-------------------------------------
- The **freeze count** is computed: the number of file lines in `FROZEN-033.sha256`, the manifest
  session 125 hashed before dispatching either reviewer. It is not typed and it is recountable.
- The **dates** are declared literals with a reason. A session date in a changelog sentence is
  not read from a measurement file and pretending otherwise would be worse than declaring it.
  `figures.lit()` exists for exactly this and records the reason beside the value.

The additions are appended to the existing table rather than replacing it, and the script refuses
to run twice over the same table so a re-run cannot inflate `n_figures`.
"""
import json
import os
import sys

import figures as F

BUNDLE = "deliverable-v0.3"
PROV = os.path.join(BUNDLE, "FIGURE-PROVENANCE.json")
FROZEN = "FROZEN-033.sha256"
MARK = "session 126: version-table rows edited under CONDITIONS-125.md item 1"


def frozen_count(path=FROZEN):
    """Count the entries in the freeze manifest, so '30 of 30' is recounted, never remembered."""
    with open(path) as fh:
        return sum(1 for line in fh if line.strip() and not line.lstrip().startswith("#"))


def main():
    prov = json.load(open(PROV))
    if any(f.get("note", "").startswith(MARK) for f in prov["figures"]):
        print("already applied - the version-row figures are in " + PROV + "; nothing to do")
        return 0

    n = frozen_count()
    fig = F.Figures(relative_to=BUNDLE)
    fig.lit(str(n), MARK + ": entries in FROZEN-033.sha256, counted by versions_provenance_126.py "
                          "- the freeze session 125 verified before and after both verdicts")
    fig.lit("2026-08-17", MARK + ": the date the sixth gauntlet was run. A session date in a "
                          "changelog sentence, declared rather than fetched.")
    fig.lit("2026-08-18", MARK + ": the date of this session's repairs and of the gauntlet they "
                          "are submitted to. Declared rather than fetched.")

    added = fig.provenance()["figures"]
    prov["figures"].extend(added)
    prov["n_figures"] = len(prov["figures"])
    prov.setdefault("appended_without_a_rebuild", []).append({
        "session": 126,
        "date": "2026-08-18",
        "by": "versions_provenance_126.py",
        "why": ("CONDITIONS-125.md item 1 requires the repairs be made as edits, not a rebuild, "
                "so build_v03.py did not run and did not rewrite this table. These entries cover "
                "the numbers in the version rows those edits added, and nothing else."),
        "n_added": len(added),
    })
    json.dump(prov, open(PROV, "w"), indent=1)
    print("appended " + str(len(added)) + " figures to " + PROV
          + "; n_figures is now " + str(prov["n_figures"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
