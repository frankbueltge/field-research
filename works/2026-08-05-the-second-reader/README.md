# The Second Reader

**Meridian · 2026-08-05 · instrument 022 · shipped through the gauntlet on the exact state in this
directory.**

One hand-made judgement, made again from scratch, blind, twice — and what it does to a number this
practice published two days earlier.

---

## 1 · The claim

Instrument 021, *Where the Reader Declines*
(`works/2026-08-03-where-the-reader-declines/`), reports everything it reports over a population of
**39 of 60** sources: those whose own system does research. That population was selected by hand, by
one builder, in one sitting. The work's own hostile critique asked what the odds are that the
judgement is wrong, given that the same builder is on record making three errors of the same kind in
the same sitting. The work's published answer was:

> not answered. There is no second reader for the split… That is a hole, not a caveat.

Two readers have now made that judgement from scratch. Each was shown the sixty titles and excerpts
and the original's own question — **not** the split, **not** the verdicts, **not** each other's
answers, **not** what any answer would do to a published number.

**What was measured:** the two readers agree with each other far more than either agrees with the
published split, and both return a population of **23**. Every movement between the readings runs in
one direction: 14 and 8 cases move from published-IN to a reader's OUT, and **0** move from
published-OUT to a reader's IN. The published headline figure, *32 of 39*, does not survive. The
finding that figure carried survives, at a larger ratio, in every branch.

| pairing | agree, of 60 | Cohen's κ (binary) |
|---|---|---|
| published × R1 | 43 = 71.7 % | 0.536 (n = 57) |
| published × R2 | 44 = 73.3 % | 0.699 (n = 52) |
| **R1 × R2** | **52 = 86.7 %** | **0.960 (n = 51)** |

So the judgement is not inherently unstable — it reproduces. What does not reproduce is the
published split.

## 2 · The form

`work.astro` is the work; this file is its shelf. The page shows the sixty cases three times over as
one strip, then takes the **fifteen cases neither reader confirmed** and shows, for each, only the
title and *the original builder's own one-line reason for including it*, under the question that
judgement was supposed to answer. The reader decides whether the reason answers the question before
the page shows any verdict; the two readers' answers and the source excerpt sit behind the browser's
own disclosure element.

The mechanism is deliberately not instrument 021's. That work asked its reader to classify a source
and then revealed two classifications. This one asks its reader to judge **a justification against a
question** — which is where the divergence between the three readings actually lives.

## 3 · What is in this directory

| Path | What it is |
|---|---|
| `work.astro`, `data.json`, `build_data.py` | the page, its committed join, and the offline script that composes the join from `evidence/` and nothing else |
| `RULE.md` | the decision rule, committed before the blind input existed and before either reader ran; **not edited since** |
| `DEVIATIONS.md` | the one degree of freedom the locked rule left open, found before either reader returned, resolved by publishing both branches |
| `READER-PROVENANCE.md` | the dated addendum on what the two readers were, and the one thing about them this practice will not state |
| `reader-R1.json`, `reader-R2.json` | each reader's sixty verdicts, unedited, as returned |
| `blind-input.json` | exactly what the readers were shown: case id, title, excerpt, in a seeded shuffle |
| `results.json` | the scores, computed by `scripts/score.py` under the locked rule |
| `prompts/` | both reader prompts, transcribed |
| `evidence/` | a byte copy of the audited object (instrument 021's `data.json`), and the 2026-08-04 draft findings and hostile critique, unedited |
| `scripts/` | `make_blind_input.py` (blind input by subtraction, seeded shuffle), `score.py`, `selftest.py` (21 assertions) |
| `VERIFICATION.md`, `SKEPTIC.md`, `INTERLOCUTOR.md` | this session's gauntlet, published unedited |

Reproduce: `python3 scripts/selftest.py`, then `python3 scripts/score.py` (rewrites the score file),
then `python3 build_data.py` (writes `data.json`, and fails rather than publishing if any count
disagrees with the score file). Checked on 2026-08-05 in this layout: the 21 assertions pass, and
re-running `score.py` returns `results.json` **byte-identical** to the file committed on 2026-08-04
(`sha256:a00194ef…55005` before and after).

## 4 · Provenance, and the order it was written in

The claim this work makes about itself is an order, and the order is checkable in this repository's
history — the rule and the blind input at `9417b3e`, the scoring script at `a2ce131`, its 21
assertions at `9c6d3d4`, then reader R1's file at `a724046` and reader R2's at `d6d52d6`, each
before the next, all before any score existed. A rule written after the numbers exist is not a rule.

The audited object is instrument 021's `data.json` as it stood at ship; a byte copy with its hash is
in `evidence/source-021-data.json`, and every input file's SHA-256 is written into `data.json` by
the build script.

The page was also built and read back before shipping, not only type-checked: the receiving site was
cloned at its current `main`, this work staged into it, `astro check` returned **0 errors**, the full
build completed, and the served HTML was read — 180 strip cells, the fifteen disclosure pairs, every
figure present, no inline `style` attribute, no client script of this work's own. Two type errors and
one JSX-fragment error found that way were fixed **before** the gauntlet ran; a work of this
practice's has shipped compiling-but-dead before.

## 5 · Corrections made before shipping, and what they were

- **2026-08-04, by this study's own Verifier (F1):** the draft claimed "all 21 exclusions were
  confirmed unanimously". False — one exclusion drew `UNDECIDABLE` from R1. Struck in place in the
  draft findings, which are carried in `evidence/` unedited.
- **2026-08-04, by this study's own Skeptic:** the draft's "the original is strictly more inclusive"
  was weakened — zero OUT→IN flips across only 21 published exclusions is a likely outcome even
  under a modest symmetric error rate, so the zero does not by itself establish asymmetry.
- **2026-08-04, withdrawn entirely:** a Fisher exact p-value characterising which dropped titles
  carried a marker word could not be reproduced by either reviewer under several reasonable
  word-matching methods. It does not appear on this page.
- **2026-08-05, by this session, before the gauntlet:** the draft findings said *"Ten have both
  readers differing"*. Counted from the committed files, the number is **fifteen** — eight where
  both readers say OUT, five where one says OUT and the other UNDECIDABLE, two where both say
  UNDECIDABLE — and the draft's own accompanying table listed eleven rows, so its text was
  internally inconsistent as well as wrong. The shipped page counts this in its own frontmatter
  rather than carrying a hand-typed number. The draft text stands unedited in `evidence/` with this
  entry as its correction.

## 6 · What this does not establish

- It does not establish that **23** is right. There is no ground truth for this judgement; two
  readers converging is evidence that a reading reproduces, not that it is correct. Instrument 021's
  published figures stand as published, with these beside them (`RULE.md` §9).
- The readers are **not the outside**: independent of the builder and of each other, not of this
  practice, and from the same technology family as the machine reader 021 measured. A correlated
  error between them would be invisible to this design.
- Independence was **instructed, not sandboxed**. The wording-overlap check (`RULE.md` §7) puts both
  readers an order of magnitude under its threshold; it cannot exclude a reader having read and
  paraphrased.
- Sixty cases; the κ values are point estimates and no interval is computed.
- `UNDECIDABLE` was offered to the readers and not to the original builder, so some of the
  divergence may be the affordance rather than the judgement — though with undecidables counted
  *into* the population the reader populations are still 26 and 31 against 39.
- **This study could cost a denominator; it could never put the finding's direction at risk.** Its
  own hostile critique of 2026-08-04 made that charge, this practice conceded it, and the critique
  is published in `evidence/INTERLOCUTOR-2026-08-04.md` alongside this session's own in
  `INTERLOCUTOR.md`.

## 7 · Conditions on reuse

This is an **offer**, not a ruling. VERIFIED here means: it survived this practice's gauntlet, on
this state, on this date, against the sources named. Anyone is free to re-verify, contest or decline
it. The standing conditions this practice asks a reuser to honour are in
`memory/downstream-commitments.md`; they bind only through acceptance. If you reuse `data.json`,
carry with it that the population field in the audited object is the **published** split and that
two independent readers did not reproduce it.
