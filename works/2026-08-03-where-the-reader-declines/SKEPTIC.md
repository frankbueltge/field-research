# Skeptic — Where the Reader Declines

**Run:** 2026-08-03, against the draft state of that date.
**Core claim under attack:** *the machine reader lands on the no-position
category where the blind reader commits, and never declines.*
**Verdict: SURVIVES WITH CONDITIONS.** Four blocking findings, all executed.

---

## S1 (blocking) — "Evades" is a disposition, and the data shows a distribution

The draft called the behaviour **evasion**. That word claims something about the
reader's disposition — that it *avoids* commitment. What is measured is that one
reader used a broad category more than another did.

`contextualizes` is defined as *"bears on the subject matter but takes no
position on the claim: a definition, a background measurement, a count, a
description of the field, or a statement about something adjacent."* Five
disjuncts. A reader applying that literally, without the blind reader's
willingness to infer a position from an architecture description, will land
there often — and be **right** each time by the letter of the definition.

That is a competing explanation the design cannot exclude, because both readers
saw the same definition and nothing separates "applies a broad category
literally" from "avoids committing" in this data.

**Executed.** Every occurrence of *evades / evasion* as a claim about the
machine was removed from the work and the findings. The measured statement
stands; the interpretation is named as unestablished in its own paragraph
(`FINDINGS.md`, "What this does and does not license"). The `meta.json`
`embodies` field carries the same distinction.

**What would settle it:** a third reader with the same definitions and a
different disposition, or an ablation that widens/narrows `contextualizes` and
re-measures. Neither is in this work.

---

## S2 (blocking) — The undecidable finding could be prompt mechanics

"The machine never declared a case undecidable" is only interesting if the
machine *could* have. If the affordance were buried, absent from the schema, or
absent from the prompt, the finding would be about the harness, not the reader.

**Checked, first-hand, in the runtime source:**

- `relation_service.py:148-154` — the prompt's **final sentence**: *"If the
  criteria cannot decide this case at all, answer `undecidable` and say in the
  rationale which word or distinction the excerpt fails on."*
- the target schema (`_RelationVerdict`) carries an `undecidable` field, so the
  response format admits it
- the criteria file carries `R-undecidable-is-a-finding`, and the criteria go
  into the prompt verbatim

**Refuted.** The affordance exists at all three levels — instruction, schema,
rules — and in the most prominent position a prompt has. The finding stands.

---

## S3 (blocking) — n=1 cannot carry the second result

The draft reported "of 38 decidable in-population sources, one supports the
claim" beside the primary finding, at comparable weight. A single case cannot
support a rate, an inference, or a comparison, and the runtime's own report
flags `supports` as **below_power** for exactly this reason.

**Executed.** The result is demoted to its own clearly subordinate section, with
its n stated in the same sentence and an explicit statement that it is reported
because it is what the labels say, not because it can carry weight.

---

## S4 (blocking) — The population split is the builder's judgement and was wrong once

Section 2 of the work reports a figure computed over a subset the builder
selected. The builder's first attempt at that same selection was automated and
**inverted the result for the single most consequential case**. A reader has no
way to audit a judgement they cannot see.

**Executed.** The split is written out case by case with a one-line reason in
`build_data.py`, and each in-population case carries its reason on the page
itself. The failure is stated on the work's face, not only in the findings.

**Not fully answered:** the 21 out-of-population cases carry no per-case reason
for their exclusion, only the collective category list. A reader who disputes an
exclusion must reconstruct why it was excluded. Recorded as owed.

---

## S5 (raised, resolved, title kept) — the title is itself a disposition claim

Having struck *evades*, the work is still called **"Where the Reader Declines"**.
If *evasion* is an unlicensed claim about a disposition, *declines* looks like
the same claim in quieter clothes.

**Resolved, title kept, on this reasoning:** *to decline* here describes the
**output**, not an inner state. A reader that selects the category defined as
*takes no position on the claim* has, in the plainest sense, declined to take a
position — that is what the category is. The word would be unlicensed if it
implied the reader *could* have committed and chose not to; the work now says in
its own body that it cannot distinguish that from a literal reading of a broad
category.

A Skeptic may still hold that a title carries more weight than a caveat two
screens below. That objection is recorded here rather than answered, and the
"What this does not license" paragraph was moved into the work's own body — not
left in the findings file — because of it.

## Non-blocking

- **N1.** "Blind human-analogue" is one practice's careful reading, not a
  human consensus, and the work should not let a reader hear "ground truth".
  The provenance section says who labelled and how; the phrase "gold standard"
  is avoided throughout. Accepted as sufficient.
- **N2.** The agreement grid shows all sixty while the headline figure shows 39.
  Two denominators on one page invite misreading. Each caption now names its own
  denominator. Accepted.
- **N3.** The excerpt hashes are shown truncated to 19 characters. Enough to
  spot a substitution, not enough to verify one. The full hash is in
  `data.json`. Accepted.
