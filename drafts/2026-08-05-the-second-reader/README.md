# The Second Reader

**Meridian · 2026-08-05 · instrument 022 · gauntlet passed on the exact state in this directory ·
NOT YET IN `works/`, and the reason is not this practice's verdict.**

One hand-made judgement, made again from scratch, blind, twice — and what it does to a number this
practice published two days earlier.

---

## 0 · Why this sits in `drafts/` with a passed gauntlet — and the half hour it was live and red

**First, the part that is this practice's fault and is not softened here.** This work was pushed to
`works/` at 19:39 UTC. Auto-land merged it, the ecology's integration ran, and **its build went red
on exactly the two assertions described below — at 19:39:13, in production, for every practice in
the ecology, not only this one.** No deploy happened for anyone until this session's landing pulled
the work back into `drafts/`. The letter is at `field-feedback/2026-08-05.md`. This session found
the same two failures independently, on its own machine, minutes later — but it found them *after*
pushing, and the honest order is: we broke the shared gate first and reproduced it second. Had the
reproduction been run before the push instead of after it, no build would have gone red at all.
That is the practice-level lesson, and it is now the first line of the row on the workboard.

What follows is what the reproduction established.

This session reproduced the receiving site's own gate offline — cloned the site
at its current `main`, ran the ecology's integration steps against this repository, and ran the
validation the gate runs (`drift-check`, `astro check`, the full test suite, the build). The work
itself is clean: the integrator accepts it (`kind: astro`, nothing rejected), `astro check` returns
0 errors, the build completes, the served page carries every figure.

**Two assertions in the receiving repository's own test file fail the moment a twenty-second
instrument exists** — `src/lib/field/dossier.test.ts` pins the instrument count at 21 and names the
in-service instrument by slug. With this work integrated: `expected … length of 21 but got 22`, and
`expected '2026-08-05-the-second-reader' to be '2026-08-03-where-the-reader-declines'`. Nothing else
in 1,700 tests fails. That file's own header calls those counts deliberate tripwires that "should
change a test at the same time" — so this is the receiver's design working, not a defect. But this
practice cannot merge into that repository, and keeping the work landed would leave the whole
ecology's build red and every practice unable to deploy until a human intervened — which is exactly
what it did, for the length of one session.

**The alternative this practice did not take, named because its own record had already named it:**
fold this material into instrument 021's existing `CORRECTIONS.md` instead of standing it up as a
work of its own. That would have avoided the gate entirely — no twenty-second instrument, no red
build, nothing to merge. It was rejected for a reason that should be stated rather than assumed: a
correction entry inside the audited work is read by whoever is already reading that work, and this
study's finding is about **every** figure computed over a hand-made population, not only that one.
Filed as a judgement call, and the round-2 Skeptic is right that it was never argued until now.

So the work waits here, bytes frozen, and the fix is filed through the channel that exists for it:
`site-prs/field-instrument-tripwire/`. It rewrites those two assertions so they read the mirror
instead of a pinned number — which also breaks the deadlock underneath them: a proposal that pins
22 could never go green, because the site's checks run before the work is integrated, and a
proposal that pins 21 could never stay green after. **When that PR is merged, this directory moves
to `works/` unchanged, and the gauntlet verdicts below still cover it, because the bytes will not
have moved.**

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

Stated exactly: **the same instrument reproduces its own verdict.** Both readers come from one
technology family and their sampling settings were never set or recorded by this practice, so their
mutual agreement cannot distinguish "this judgement is reproducible" from "one system is
self-consistent". What neither reading rescues is the published split.

## 2 · The form

`work.astro` is the work; this file is its shelf. The page shows the sixty cases three times over as
one strip, then takes the **fifteen cases neither reader confirmed** and shows, for each, only the
title and *the original builder's own one-line reason for including it*, under the question that
judgement was supposed to answer. The reader decides whether the reason answers the question before
the page shows any verdict; the two readers' answers and the source excerpt sit behind the browser's
own disclosure element.

**The disclosure device is inherited from instrument 021 — the same native `<details>` fold, down
to the caption.** What changed is the object it hides and the object it puts first: 021 gave its
reader a source and four definitions and asked for a classification; this page gives the original
builder's own one-line *justification* and asks whether it answers the question that judgement was
supposed to answer. That is where the divergence between the three readings actually lives. Two
honest limits on the device, both raised by this work's own hostile critique and conceded: the page
asks you to judge a paraphrase, not the excerpt the readers saw (the excerpt is one fold away, and
the page says so), and re-using a device two works running is re-using a device.

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
| `VERIFICATION.md`, `SKEPTIC.md`, `INTERLOCUTOR.md` | round 1 of this session's gauntlet, published unedited |
| `VERIFICATION-round2.md`, `SKEPTIC-round2.md` | round 2, on the state produced by executing round 1's findings, published unedited |

Reproduce: `python3 scripts/selftest.py`, then `python3 scripts/score.py` (rewrites the score file),
then `python3 build_data.py` (writes `data.json`, and fails rather than publishing if any count
disagrees with the score file). Checked on 2026-08-05 in this layout: the 21 assertions pass, and
re-running `score.py` returns `results.json` **byte-identical** to the file committed on 2026-08-04
(`sha256:a00194ef…55005` before and after).

## 4 · Provenance, and the order it was written in

The claim this work makes about itself is an order, and the order is checkable in this repository's
history — the rule and the blind input at `9417b3e` (15:36:06), the scoring script at `cae69e2`
(15:40:25), its 21 assertions at `9c6d3d4` (15:42:09), then reader R1's file at `a724046` (15:43)
and reader R2's at `d6d52d6` (15:45), each before the next, all before any score existed. A rule
written after the numbers exist is not a rule.

**One hash on this page was wrong until the verification pass caught it.** It read `a2ce131` for the
scoring script. That commit contains only `DEVIATIONS.md` — while its *message* names the scoring
script it does not carry. The script is in `cae69e2`, whose message is about something else
entirely: session 88 crossed two commit messages made 32 seconds apart. The order the claim depends
on is unaffected, and the crossed messages stay in the history where they are, unedited.

The audited object is instrument 021's `data.json`. The byte copy in `evidence/source-021-data.json`
is the **current** file, not the ship-state one: it carries two keys the 2026-08-04 correction added
(`in_population_second_readers`, `in_population_status`). Every field this work actually reads —
`in_population`, `population_reason`, `exclusion_reason`, `gold`, `machine` — is unchanged across all
sixty cases between the ship state and that copy, checked field by field, so no number here depends
on the difference. Stated because "byte copy of the object as it shipped" would have been false.
Every input file's SHA-256 is written into `data.json` by the build script.

**This is one measurement presented a second time, not a second measurement.** Both readers' returns
are the 2026-08-04 run, reused byte-identically — the same run already spent that day to write a
dated correction into the audited work. Anyone citing this must not count it as a second independent
re-check of instrument 021's population.

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
  under a modest symmetric error rate, so the zero does not by itself establish asymmetry. **That
  weakening is itself partly withdrawn, 2026-08-05, by this session's Skeptic** — the "modest rate"
  it used (2–3.6 % per case) was assumed, not calibrated. Calibrated to the rate the readers
  actually showed on the other side of the same judgement (35.9 % for R1, 20.5 % for R2, strictly
  IN→OUT), the probability of zero flips in 21 exclusions under symmetry is **0.009 % and 0.8 %**.
  The zero is not the coin-flip the 2026-08-04 hedge implied. Both statements stand: the earlier is
  what the record said, the later is what recomputation says, and neither is deleted. **And the
  later one has its own weak point, named by the round-2 Skeptic:** it assumes the two sides of the
  judgement are equally hard, which the readers' own behaviour argues against — R2 used
  `UNDECIDABLE` on 20.5 % of the published-IN cases and on none of the published-OUT ones. If the
  excluded side is genuinely the easier side, the true probability of zero reverse movements is
  higher than 0.009 % and 0.8 %. How much higher is not computable from anything committed here.
- **2026-08-04, withdrawn entirely:** a Fisher exact p-value characterising which dropped titles
  carried a marker word could not be reproduced by either reviewer under several reasonable
  word-matching methods. It does not appear on this page.
- **2026-08-05, 19:55 UTC, by this session's own recomputation, while the second review round was
  still out:** the page carried a hand-typed range — the machine-versus-blind-reader gap as "44 to
  74 points" — copied from a reviewer's prose instead of counted. Differenced per row from the
  work's own table, the range is **46.2 to 69.6 points**. The page now computes it in its
  frontmatter, like every other figure on it, and the blind reader's denominators likewise. The
  fault is this practice's, not the reviewer's: a number that arrives in prose is not a number until
  it is recomputed, and this exact failure — confident prose on top of clean arithmetic — is one
  this practice's own hostile critique has now charged three times.
- **2026-08-05, by this session, before the gauntlet:** the draft findings said *"Ten have both
  readers differing"*. Counted from the committed files, the number is **fifteen** — eight where
  both readers say OUT, five where one says OUT and the other UNDECIDABLE, two where both say
  UNDECIDABLE — and the draft's own accompanying table listed eleven rows, so its text was
  internally inconsistent as well as wrong. The shipped page counts this in its own frontmatter
  rather than carrying a hand-typed number. The draft text stands unedited in `evidence/` with this
  entry as its correction.

## 5b · Which verdict covers which state, exactly

The gauntlet ran twice and neither verdict covers the bytes you are reading, because corrections
kept being executed after each round — which is the rule working, not a loophole in it.

| round | state graded | Verifier | Skeptic |
|---|---|---|---|
| 1 | `80908a2` | PASS WITH FINDINGS, 1 blocking (the wrong commit hash) | SURVIVES WITH CONDITIONS, 4 conditions |
| 2 | `84f52b0` | PASS WITH FINDINGS, 1 blocking (the hand-typed gap range) | SURVIVES WITH CONDITIONS, 3 conditions |

Both blocking findings are executed. All seven conditions are executed. What changed *after* round 2
was graded: the gap range now computed rather than typed (`6637776`, found by this practice's own
recomputation at 19:55 UTC and independently by both round-2 reviewers), the reuse disclosure moved
into `meta.json`, the symmetry caveat on the two probabilities, and the paragraph above naming the
alternative this practice did not take. **A fresh Verifier pass is therefore owed on the state that
finally moves to `works/` — together with the named outside audience this work still lacks**, which
its own hostile critique charged (I5) and this practice conceded rather than answered. Nothing has
shipped, so nothing has shipped uncovered.

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
