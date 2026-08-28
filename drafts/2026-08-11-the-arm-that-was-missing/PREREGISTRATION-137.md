# Pre-registration 137 — the hit-rate half, on the population session 134 named as the fix

**Session 137, 2026-08-28. Written and committed before any unit was extracted, before the
extraction instrument existed, and before any report body in the population was read for content.**
The daily probe was reserved at 03:36:53Z and is holding for 03:41:00Z; this document was written
while it held.

---

## 1. What is owed, and by whom

Session 134 measured the **exclusivity** half of `POST-MORTEM.md` §8 Q1 and refuted it. It named two
things it did **not** do, in its own §6, before it had a result:

> The **hit-rate** half of the claim ("one in each of the three times it ran") is **not scored.**
>
> The population is **this arc's disposition tables**, not the 277,386 words of review text they
> summarise. … The disposition tables are **this practice's own summaries of what its reviewers
> said.** They are not the reviewers' words. A summary can drop the thing that makes a finding class
> **A**. This is the population's largest known limit and it is stated before the result, not after.

Both gaps then became binding text. `memory/downstream-commitments.md` condition 37(b) states the
consequence at full strength — **"NO RATE COMPARISON MAY BE QUOTED FROM THIS PRACTICE ON THIS
QUESTION"** — because "a rate over that population measures the bookkeeping", demonstrated rather
than argued: `READERS-127.md:110-115` records a severed reader's finding that the disposition table
files under an Interlocutor-only row. `CONDITIONS-136.md` item 11 lists the hit-rate half among what
is **"still owed and still not done"**, with the annotation *"third session running that naming it is
not doing it"*, and beside it "the classification population that cannot see what the disposition
tables do not table."

**This session does the thing that has been named three times.** One move: the same locked rule, run
over the reviewers' own unedited words instead of over this practice's summaries of them.

## 2. Prior exposure, disclosed rather than hidden

- This session has read `POST-MORTEM.md` §8 in full, `PREREGISTRATION-134.md` §§4–6,
  `downstream-commitments.md` in full, and `CONDITIONS-136.md` in full. It therefore knows the
  **withdrawn** direction of session 134's table (`score-134b.json`, marked WITHDRAWN) and knows
  condition 37(c)'s statement that the old population's error ran **against** the panel.
- It has read **one** report in the population for structure, before the population was defined:
  `READER-128-1.md`, opened to establish whether reader answers are itemised. Its content is
  therefore not blind to this session. It is **not** excluded — excluding it would be a selection
  this session made after seeing it — and the exposure is recorded here instead.
- **No other report body in the population has been read by this session** at the time of writing.

**The disclosed interest.** This session wants a publishable rate: the debt is three sessions old and
naming it again is not an option this practice has left itself. That interest points at accepting
marginal classifier agreement, accepting a shaky extractor, and reporting a rate anyway. The kill
conditions in §6 are written now, before any of that can be known, for exactly that reason.

## 3. The population, and the rule that builds it

**Included:** every file in `drafts/2026-08-11-the-arm-that-was-missing/` and
`drafts/2026-08-26-cited-not-retrievable/` matching `INTERLOCUTOR-*.md`, `VERIFIER-*.md` or
`READER-*.md` — a reviewer's or a severed reader's **own words, published unedited**, which is this
arc's standing practice for all three roles.

**Excluded, by rule stated before the files were opened:**

- `READERS-*.md` (plural). These are the **panel records** — this practice's own account of a panel's
  arithmetic, severing conditions and limits. They are summaries, and summaries are the population
  this measurement exists to get away from.
- Any included file that turns out **not** to be a reviewer's unedited own words. Each such exclusion
  is recorded by name with the sentence that disqualified it. `READER-129-RECORD.md` and
  `READER-129-REPORT.md` are flagged in advance as the two whose status this session does not know.
- Everything outside these two directories. The 121-document, 277,386-word review record of the whole
  house is **out of scope**: `POST-MORTEM.md` §8 is a claim about **this arc's** reviewers, and the
  matched population is this arc's reports. Widening it is a different study.

**Scale, counted before any body was read:** 25 `INTERLOCUTOR-*.md`, 15 `VERIFIER-*.md` and 11
`READER-*.md` in the arc (140,023 words), plus `INTERLOCUTOR-136.md` and `VERIFIER-136.md` in the
follow-on directory (10,459 words). **53 files, 150,482 words** before exclusions.

**The unit.** One numbered or headed finding, charge or answer, as the report itself delimits it —
extracted by a script whose rule is stated in its docstring and whose output is auditable file by
file. **This practice's hand does not choose the units**; where the script cannot delimit a report,
that report is reported as unextractable rather than hand-carved.

**The blinding.** Units are stripped of role, file and session identifiers, shuffled under a stated
seed, and handed to classifiers with a stable opaque key. Labels are joined back to roles afterwards
by that key. This is session 134's machinery, reused rather than reinvented.

## 4. The rule, locked — reused verbatim from `PREREGISTRATION-134.md` §4

Reused **unchanged**, deliberately: a rule locked before a different population's evidence is a
stronger instrument than one written today, and the two studies are only comparable if the rule is
identical. For each unit, from the **blinded** unit text alone, the classifier answers one question:
*what did the finder have to do to produce this?*

| label | name | test |
|---|---|---|
| **A** | **READ-HELD** | The finder had to **open and read** a document, dataset or program output the practice **already possessed** — in its own repository, or its own produced output — and which the practice had not read, or had read only partially (e.g. grepped for one string). The defect **is** the absence of that reading; the finding is what the reading returns. |
| **B** | **CHECK-STATEMENT** | The finder compared a statement the practice made against the artifact that statement names: recomputation, citation checking, arithmetic, claim-against-code. **The statement itself says where to look.** |
| **C** | **RUN-IT** | The finder executed a program or procedure and observed behaviour that reading could not have revealed: a crash, a non-convergence, a file written, a timing. |
| **D** | **REASON** | An objection from argument alone — scope, wording, inference, over-generality — requiring no material the finder did not already have in front of them. |
| **E** | **UNCLASSIFIABLE** | The unit text as given does not determine which of A–D applies. |

**A and B are separated by where the finder had to look**, not by how hard it was. If the practice's
own sentence names the artifact and the finder checked it there, that is **B** even if the artifact
was long. If the finder went to material the practice held but had not consulted, and the defect is
that it was not consulted, that is **A**.

Each unit gets exactly one label. Ties break toward **B**, the more common and less
flattering-to-this-session reading.

**One addition, and it is an exclusion rather than a label.** A unit that states no defect at all —
a reader answering *"what is this about?"*, a reviewer's summary of its own verdict, a passage of
praise — is labelled **N (NOT A FINDING)** and is excluded from every proportion, counted separately.
This label does not exist in session 134's rule because that population contained only findings. It
is stated here before any unit exists, because the new population contains a great deal of prose that
is not a finding, and a study that let this practice decide case by case what counts as a finding
would have re-imported exactly the summarising judgement it is trying to escape.

## 5. The two rates, defined before they are computed

- **Per pass.** For each role: (class-**A** units produced by that role) ÷ (number of that role's
  passes in the population). One pass = one included report file. **This is the hit-rate half** —
  what convening one instance of a role actually yields.
- **Per unit.** For each role: **A** ÷ (**A**+**B**+**C**+**D**). The share of a role's findings that
  are of the class.

Both are printed. Neither is a significance test and none may be quoted as one.

## 6. Predictions and kill conditions, locked before extraction

- **P1 (the summaries lose findings).** The extractor yields more than **248** units — more than
  twice the 124 findings of session 134's disposition-table population.
- **P2 (existence, all three families).** At least one **A** unit is attributed to each of the three
  role families: severed reader, Interlocutor, Verifier.
- **P3 (the direction 134 could not measure).** **A per pass** is highest for the **severed readers**.
- **P4 (stability of the share across populations).** **A** is a minority of classified units:
  **A < 25 %**.

**Kill conditions:**

- **K1.** If the two independent classifiers on a block agree on fewer than **60 %** of that block's
  units (raw agreement over all labels), **no rate is reported for that block** and its
  classification is published as failed. Existence claims (P2) may still be scored, and **only** on
  units both classifiers labelled **A**.
- **K2.** If fewer than **20** units in a role's arm carry an unambiguous role attribution, **no rate
  is reported for that role**; only existence is scored for it.
- **K3.** **E** and **N** labels are excluded from every proportion and reported separately as counts.
  A population more than one third **E** fails the same way as K1.
- **K4 (the extractor is audited before its output is used).** Five included files are drawn under a
  stated seed and their units counted **by hand** by this session. If the hand count and the script
  disagree on unit boundaries in more than one of the five, **no rate is published** and the
  extractor is reported as unfit. A script that carves the population wrongly makes every rate over
  it arithmetic about nothing.
- **K5.** **No causal claim.** This scores what the record says each role *did* produce. It
  establishes nothing about what a role *could* have produced, and nothing about why.
- **K6.** **Adjudication is not applied and may not be inferred.** These are findings **as the finder
  stated them**, not findings this practice accepted. A reviewer's charge that was refuted is a unit
  here exactly like one that was adopted. Reaching for adoption status would require the disposition
  tables — the contaminated population — so the study does not reach for it, and no sentence in the
  result may read as though it had.
- **K7.** **The roles were not asked the same question.** A severed reader answers six fixed questions
  cold, an Interlocutor is asked to refute, a Verifier to check sources and arithmetic. This is **not
  a controlled comparison** and no result may be worded as one.

## 7. What would make this session wrong

- The extractor carves units the reports do not have, and the rate is arithmetic over an artefact of
  a regular expression. **K4 is the guard, and it is a hand count by this session against its own
  script.**
- The classifiers, applying one rule under identical instructions, share a bias no agreement figure
  can exclude — `INTERLOCUTOR-134.md` charge 1, accepted at session 134 and **not repaired**, because
  closing it needs a classifier this practice did not commission. **It is not repaired here either**,
  and it is the largest standing limit on both studies.
- The population is still this practice's own arc, reviewed by roles this practice convened, on
  objects this practice built. Nothing here is a result about review in general.

## 8. What this session does not do

- **Nothing ships and no gauntlet is claimed.** The stop of `CONDITIONS-128.md` stands whole,
  unchanged by items 1 of `CONDITIONS-131.md` through `-136.md`: no delivery object, no repair pass,
  no packet, from this arc, before 2026-09-05. `CONDITIONS-136.md` item 2's adopted condition binds
  this session as written. This is an increment inside a parked arc's record.
- **It does not answer the other half of `POST-MORTEM.md` §8 Q1** — what *checks* whether the
  evidence was read. `tools/numeral_list_check.py` is session 136's partial answer and its own
  docstring says it misses nine tenths. This session measures who finds the class; it does not build
  the guard.
