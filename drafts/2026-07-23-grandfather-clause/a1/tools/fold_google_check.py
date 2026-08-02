#!/usr/bin/env python3
"""A1 — what happens to the S stratum if the Google group is folded into it.

Added at the Skeptic's blocking condition 6 (session 80). The objection: four of Black Forest
Labs' five specimens are `indeterminate-at-capture` from a content-delivery host exactly as all
four Google specimens are, yet BFL was placed inside the decision rule and Google outside it, on
a ground that appears in neither Rule A1-S nor the pre-registration. The asymmetry is real and
is disclosed in CAPTURE-NOTES.md; this script answers the question the objection implies — does
the asymmetry change anything?

It applies Rule A1-S to a merged `S-signatory ∪ X-observation-only` group and prints the result
beside the reported one. It writes nothing and decides nothing.
"""
import json
from pathlib import Path

A1 = Path(__file__).resolve().parent.parent


def summarise(rows, label):
    n = len(rows)
    ind = sum(r["state"] == "indeterminate-at-capture" for r in rows)
    marked = sum(r["state"] == "machine-readable-marked" for r in rows)
    eff = n - ind
    rate = ind / n if n else None
    print(f"{label}: n={n} indeterminate={ind} ({rate:.1%}) effective_n={eff} marked={marked} "
          f"-> {'capture-inconclusive' if rate and rate > 0.40 else 'not inconclusive'}")


def main() -> int:
    rows = json.loads((A1 / "a1-results.json").read_text())["specimens"]
    s = [r for r in rows if r["stratum"] == "S-signatory"]
    x = [r for r in rows if r["stratum"] == "X-observation-only"]
    summarise(s, "as reported  (S-signatory alone)   ")
    summarise(s + x, "folded       (S-signatory + Google)")
    print("\nBoth exceed the pre-registered 40% indeterminate threshold, so both are forced into "
          "no directional label. The asymmetry the Skeptic identified does not change this "
          "anchor's outcome; it is disclosed because it is a real piece of post-hoc discretion, "
          "not because it moved a number.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
