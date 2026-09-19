# SPEC.md — the specification you are implementing

*This file is the whole of what you are told about what to measure. It is quoted verbatim from a
measurement specification written for a human reader before any data existed, plus one dated
amendment to it. Nothing has been added, removed or paraphrased inside the quoted blocks.*

---

## The two rungs

- **L1 — identified.** The file's normalised text **contains, as an exact substring, a distinctive
  operative phrase** of a known licence family. Normalisation: lowercase, all runs of whitespace
  (including newlines) collapsed to one space, curly quotes folded to straight. The phrase table is
  written by hand into `tools/is-it-a-licence/fingerprints.py` as short quotations from the licence
  texts themselves, one to four per family, each chosen to be a sentence that appears in **no other
  family**. A file matching more than one family is recorded as multi-family, not silently resolved.
  **Recall is deliberately sacrificed for precision:** a file this rule does not identify is
  recorded as *not identified by this instrument*, which is **not** a finding that it is not a
  licence. Every such file's first 200 normalised characters are committed so a reader can judge.
- **L2 — attributed.** For the families whose canonical text carries a copyright line
  (MIT, ISC, BSD-*, and the Apache-2.0 appendix), the file carries a line matching
  `copyright` + a year or year range + a holder, **where the holder is not an unfilled template
  placeholder**. The placeholder table is written by hand and holds the bracket forms the canonical
  texts themselves use (`<year>`, `<copyright holders>`, `[year]`, `[fullname]`,
  `[yyyy] [name of copyright owner]`, `<YEAR>`, `<OWNER>`, `xxxx`, `your name`, and the like),
  matched case-insensitively. **Not applicable** for families whose canonical text carries no
  copyright line (GPL-*, AGPL, LGPL, MPL-2.0, CC0, Unlicense as published): those rows are `null`,
  never `false`. *A licence that names no licensor is the measurement finding; whether it grants
  anything in law is not ours to say and this artifact will not say it.*

---

## Amendment, dated, and part of the specification

**What changes.** §4's L2 rung listed "MIT, ISC, BSD-\*, and the Apache-2.0 appendix" as the families
where a copyright line is scored. **The Apache-2.0 appendix is struck from the scored set**, and so
are GPL-\*, LGPL, AGPL, MPL-2.0, CC-\* and Unlicense, which were already outside it.

**Why, and it is a defect caught by building the rule rather than by thinking about it.** The SPDX
canonical text of Apache-2.0 ends with an appendix reading `Copyright [yyyy] [name of copyright
owner]`, and shipping that text **unedited** is the normal, correct way to apply Apache-2.0 — the
real copyright goes in file headers, not into the `LICENSE` file. Scoring it would have produced a
large "placeholder" rate that measures a convention, not an absence, and this practice would have
published it. The same holds for the GPL family's "How to Apply These Terms" appendix.

**What is scored, therefore.** L2 and prediction P4 are evaluated **only** over files identified as
**MIT-family, ISC, BSD-2/3/4-Clause and Zlib** — the families whose copyright line sits inside the
operative grant and whose canonical text's placeholder is meant to be filled in by the user.
Everything else is `null` — *not applicable* — and never `false`.

**Reported separately and explicitly not scored as a defect:** the share of Apache-2.0 files whose
appendix is unfilled. It is published because it is interesting and because leaving it out after
computing it would be the kind of silence this practice measures in others.

---

## Notes that are not part of the specification

- "Normalised" in the L1 rung is defined inside that rung and nowhere else.
- The family vocabulary you must draw from is given in your instructions, not here.
- The specification's parenthetical list of placeholder forms ends with "and the like". Extending
  it is part of implementing the rung.
- The rungs speak of "the file" and of committing characters for a reader. You implement only the
  verdict each rung defines; nothing is committed by you.
