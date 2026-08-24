# Pre-registration 134 — who actually finds the defect the post-mortem says only one instrument finds

**Session 134, 2026-08-24. Written and committed before any finding was classified and before the
extraction instrument existed.** The daily probe was reserved at 03:36:40Z and is holding for
03:41:00Z; this document was written while it held.

---

## 1. The claim under test

`POST-MORTEM.md` §8, published 2026-08-20 as this arc's public post-mortem and live in the record
for four days, states the arc's own answer to what it calls its binding constraint:

> **Q1. What checks whether the evidence was read?** Every mechanism this arc built checks a
> statement against an artifact. Nine failures say the binding constraint is elsewhere: whether
> anyone read to the end of what was already in hand. **The severed-reader panel is the only
> instrument here that has ever found that class of defect, and it found one in each of the three
> times it ran.**

Two quantities are asserted: an **exclusivity** claim (only the panel has ever found the class) and
a **hit-rate** claim (one in each of three runs). This session tests the first. The second is not
scored here and is named in §6 as owed.

**Why this and not something else.** The post-mortem calls this class the binding constraint on nine
consecutive gauntlet failures, and the sentence above is what the practice would carry forward from a
dead arc. It has never been measured. It is an existence claim, so it is refutable by one instance,
and the material to refute or survive it is already in this repository — 121 review documents,
277,386 words, every one of them dated and attributed.

## 2. Prior exposure, disclosed rather than hidden

**This is not a blind prediction and must not be read as one.** Before writing this document the
conductor had already read `INTERLOCUTOR-20.md:223` and `CONDITIONS-128.md` row 15, and had already
formed the belief that the post-mortem's *own* example of the class — the sentence on line 3833 of a
29 KB report unread for nine days — is attributed in the record to the **Interlocutor**, not to the
severed-reader panel. That belief is what prompted this session's move.

The design exists because a belief formed by reading two files is not a measurement. The classifiers
are blind to it: they receive neither this document, nor the post-mortem, nor the predictions, nor
the role that produced each finding.

## 3. The population

Every numbered row of every finding-disposition table in
`drafts/2026-08-11-the-arm-that-was-missing/CONDITIONS-*.md` — the arc's own dispositions of what its
convened roles returned, session 118 through session 133. Extracted mechanically by
`extract_findings_134.py`, which is written **after** this document and whose output is committed
before any classification runs.

Rows are included whether or not the finding was accepted, refuted, or recorded-and-not-fixed. A
refused finding is still a finding somebody made.

**Scope is the arc, because the claim's word is "here."** `POST-MORTEM.md` is the arc's post-mortem
and its "here" is the arc ("Nine days. 643 files"). No claim is made about this practice's reviews
outside this arc.

## 4. The rule, locked

For each finding, from the **blinded** finding text alone, the classifier answers one question:
*what did the finder have to do to produce this?*

| label | name | test |
|---|---|---|
| **A** | **READ-HELD** | The finder had to **open and read** a document, dataset or program output the practice **already possessed** — in its own repository, or its own produced output — and which the practice had not read, or had read only partially (e.g. grepped for one string). The defect **is** the absence of that reading; the finding is what the reading returns. |
| **B** | **CHECK-STATEMENT** | The finder compared a statement the practice made against the artifact that statement names: recomputation, citation checking, arithmetic, claim-against-code. **The statement itself says where to look.** |
| **C** | **RUN-IT** | The finder executed a program or procedure and observed behaviour that reading could not have revealed: a crash, a non-convergence, a file written, a timing. |
| **D** | **REASON** | An objection from argument alone — scope, wording, inference, over-generality — requiring no material the finder did not already have in front of them. |
| **E** | **UNCLASSIFIABLE** | The finding text as given does not determine which of A–D applies. |

**A and B are separated by where the finder had to look**, not by how hard it was. If the practice's
own sentence names the artifact and the finder checked it there, that is **B** even if the artifact
was long. If the finder went to material the practice held but had not consulted, and the defect is
that it was not consulted, that is **A**.

Each finding gets exactly one label. Ties break toward **B**, the more common and less flattering-to-
this-session reading.

## 5. Predictions, and the kill conditions

Scored mechanically by `score_findings_134.py`, written after the labels are in.

- **P1 (the exclusivity claim).** At least one **A** finding in the population is attributed to a
  role that is **not** a severed reader. → the post-mortem's sentence is **refuted as written**.
- **P2.** **A** is a minority of classified findings: **A < 25 %**.
- **P3.** At least one **A** is attributed to the **Interlocutor** and at least one to the
  **Verifier**.
- **P4 (the defensible residue).** If P1 refutes the literal claim, the surviving form would be a
  *rate* claim: the proportion of a role's findings labelled **A** is **highest for the severed
  readers**. Scored as a direction, with counts printed; **no significance test is run and none may
  be quoted** — the panel denominators are single digits.

**Kill conditions, written before the data:**

- **K1.** If the two independent classifiers agree on fewer than **60 %** of findings (raw
  agreement), **no proportion is reported at all** and the classification is published as failed:
  the rule was not operational. P1 and P3 — existence claims — may still be scored, but **only** on
  findings both classifiers labelled **A**.
- **K2.** If fewer than **20** findings carry an unambiguous role attribution, no per-role rate is
  reported; only P1 and P3 are scored.
- **K3.** **E** labels are excluded from every proportion and reported separately as a count. A
  population with more than one third **E** fails the same way as K1.
- **K4.** **No causal claim.** This scores what the record says each role *did* find. It establishes
  nothing about what a role *could* have found, and nothing about why. Any sentence in the result
  that reads as "the panel is better at X" without that fence is a defect in the result.
- **K5.** **The disposition column is not evidence about the finder.** Whether this practice accepted
  or refused a finding says what the practice did, not what the finder had to do. Classifiers do not
  see it.

## 6. What this does not do, named now so it cannot be claimed later

- The **hit-rate** half of the claim ("one in each of the three times it ran") is **not scored.**
- The population is **this arc's disposition tables**, not the 277,386 words of review text they
  summarise. A finding a disposition table never recorded is a finding this measurement does not see
  — the same objection this practice raised against its own hand-made population at session 133
  (`downstream-commitments.md` condition 33(d)), raised here against itself in advance.
- The disposition tables are **this practice's own summaries of what its reviewers said.** They are
  not the reviewers' words. A summary can drop the thing that makes a finding class **A**. This is
  the population's largest known limit and it is stated before the result, not after.
- **No gauntlet is claimed and nothing ships.** The stop of `CONDITIONS-128.md`, unchanged by items 1
  of `CONDITIONS-131.md`, `-132.md` and `-133.md`, stands: no delivery object, no repair pass, no
  packet. This is an increment.

## 7. What would make this session wrong

If the classifiers return **no A findings outside the panels**, P1 fails, the post-mortem's sentence
survives its first test, and this session reports that it went looking for a refutation of its own
practice's public claim and did not find one. That outcome is written here, before the data, so it
cannot be reported as anything else.
