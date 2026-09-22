# is-it-a-licence, version 2 — the repaired instrument

**Landed 2026-09-22, session 167.** This is variant `01110` of that session's repair lattice:
the four-rung licence rule of 2026-09-18 with **three repairs** applied and two deliberately
withheld. Evidence, lattice and adjudication:
`artifacts/2026-09-22-a-repair-is-a-new-rule/`.

**Version 1 stays where it is.** `tools/is-it-a-licence/` produced the figures published on
2026-09-18 and is not edited: history is continued, never retouched (protocol v4 §7). Nothing
published under version 1 is restated by version 2 — the one number that could have moved,
**100 of 105 = 95.2 %**, is identical under it, over the identical set of repositories.

## What is repaired

| | defect | found by | the change |
|---|---|---|---|
| **R4** | defect 4 — `Copyright (C) 1996 X Consortium` is not recognised as a notice while the same line with a lowercase `c` is | four independent reimplementations, 2026-09-19 | `_TAIL_WORD`'s literal `\(c\)` alternative becomes `\([cC]\)` |
| **R5** | defect 5 — a notice opened with a typographic quotation mark is invisible, although `normalise()` one rung earlier folds exactly those characters | metamorphic relation M5, 2026-09-20 | the four typographic quotation marks are admitted to `_PREFIX` |
| **R6** | defect 6 — a notice whose holder sits on a later physical line than the word `copyright` reads `no_holder` | ten blind dispatched workers, unanimously, 2026-09-21 | when a notice's holder extracts empty, the holder is sought on the following units, to a depth of three, stopping at a blank line, a rule of dashes, or a new notice |

R4 and R5 are applied to `fingerprints.py` by line anchor. R6 is an appended block that
installs a notice pipeline; with its flag off the pipeline is **output-identical** to version
1 over all 896 inputs of both corpora, on the decision fields and on the fields that quote the
input, which was verified rather than asserted.

## What is NOT repaired, and why

- **Defect 1's residual.** A liability sentence beginning `COPYRIGHT HOLDERS BE LIABLE FOR ANY
  DIRECT, INDIRECT,` is still read as a notice. 15 such false notices sit in the unperturbed
  data; **none** of them changes a decision, because every file carrying one also carries a
  real notice. The candidate repair (R1: require a year, a marker or a placeholder) cuts them
  to 4 and changes no decision — and it **contradicts fixture `NOTICE/no-year-but-capital`**,
  which says `Copyright Contributors to the OpenVDB Project` is a notice. That is a
  specification question, not a bug, and it is left open rather than decided by a patch.
- **The line-anchoring trade-off.** A notice's word must begin its physical line, so a notice
  that does not is invisible, and reflowing a paragraph changes the answer. Four inputs in 896
  under relation M6. The candidate repair (R7: search the logical line) was built, measured and
  **rejected**: it multiplies the instrument's false notices by twenty, puts 18 decisions on
  them, destroys two real yearless notices, and moves the published headline by up to 3.8
  points in either direction. Its numbers are in the artifact; it is not in this directory.

## Its own test record, run tonight

- **100 of 100 fixtures pass**, none failing.
- **27 mutants**, none surviving unexpectedly, no expected survivor caught.
- **4 decision-changing metamorphic violations** over 896 inputs, down from 167; both surviving
  classes were already named and dated on 2026-09-20 and both are adjudicated `LATENT` — the
  unperturbed verdict is right in every one.
- **The negative control (a four-space indent) returns zero.**
- **15 false notices, 0 decisions at risk** — identical to version 1.

**And the boundary, which version 2 does not move:** a fixture checks that a rule computes what
its author says, never that the author wrote the right sentence. Six defects have been found in
version 1 by five different means, and none of them was found by its own fixtures.

## What this directory holds, and what it deliberately does not

`rules.py`, `fingerprints.py`, `fixtures.py`, `mutants.py` — the rule and its two suites,
runnable with no network:

    python3 fixtures.py    # 100 cases, 0 failed
    python3 mutants.py     # 27 mutants, 1 survived (0 unexpectedly)

Version 1's `harvest.py`, `build.py`, `control.py`, `make_page.py` and `tamper.py` are **not**
copied here. They are the pipeline of the 2026-09-18 artifact, they write into that artifact's
`data/`, and a copy of them beside a different rule would invite a reader to rebuild a
published page with an instrument that did not produce it. They stay where they are, with the
figures they made.
