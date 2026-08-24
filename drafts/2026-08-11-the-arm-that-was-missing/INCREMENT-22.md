# Increment 22 — the post-mortem's answer to its own binding question is wrong, and so was this session's reason for thinking so

**Session 134, 2026-08-24.** Scored against `PREREGISTRATION-134.md`, committed at `6fac67e`,
03:41:12Z — before the extraction instrument existed and before any finding was classified. The
scoring script was committed at `b65f9e7`, 03:43:21Z, while the classifiers were still running and
before either label file existed.

Population: `findings-134.json`, payload sha256 `10e7fe3c005be5d7…`. Labels:
`labels-134-A.json`, `labels-134-B.json`. Result: `score-134.json`.

---

## 1. The claim

`POST-MORTEM.md` §8, published 2026-08-20, is this arc's public answer to what it calls its own
binding constraint — *what checks whether the evidence was read?*

> **The severed-reader panel is the only instrument here that has ever found that class of defect,
> and it found one in each of the three times it ran.**

The class: a defect whose discovery required **reading material the practice already held** and had
not read. Nine gauntlets failed on it; the post-mortem names it the thing no guard can catch.

That sentence has stood in the public record for four days, through five sessions that each read the
post-mortem, and **it had never been measured.**

## 2. The design, in one paragraph

Every numbered row of every finding-disposition table in this arc's `CONDITIONS-*.md` files —
**102 findings across ten files**, sessions 118 to 133 — extracted mechanically by
`extract_findings_134.py`, stripped of its role-attribution column and of a published list of
role-naming tokens, and handed to **two independent classifiers who were told none of this**: not
the claim, not the predictions, not who made any finding, not whether the practice accepted it.
They answered one question per finding under a rule locked in §4 of the pre-registration: *what did
the finder have to do to produce this?* — **A** read material already held, **B** check a statement
against the artifact it names, **C** run something, **D** argue, **E** cannot tell.

## 3. The result

**Both kill conditions that could have stopped the scoring cleared.** Raw agreement between the two
classifiers: **0.8039** over all 102 (threshold 0.60). Unclassifiable by either: **5 of 102**
(threshold: one third). Attributed findings: **92** (threshold 20).

| prediction | result |
|---|---|
| **P1** — at least one class-A finding is attributed to a role that is not a severed reader | **THE CLAIM IS REFUTED. 20 counterexamples**, every one agreed by both blind classifiers. |
| **P2** — class A is a minority (< 25 %) | **HELD**, and barely: **23 of 97** classifiable findings, **23.71 %**. |
| **P3** — at least one class A from the Interlocutor *and* one from the Verifier | **HELD**: Interlocutor **13**, Verifier **6**. |
| **P4** — the defensible residue: the panel has the *highest rate* of class A | **FAILS.** |

**The class is found 23 times in this arc's own record, by at least four different finders.** By
role, on findings both classifiers labelled A:

| role | class A / findings | rate |
|---|---|---|
| **Interlocutor** | **13 / 45** | **28.9 %** |
| Reader panel | 2 / 9 | 22.2 % |
| Verifier | 6 / 29 | 20.7 % |
| this practice, itself | 0 / 4 | 0 % |
| unattributed | 1 / 9 | 11.1 % |
| other | 1 / 1 | 100 % |

**The top rate belongs to a row with a denominator of one and is reported because the script
computed it, not because it means anything.** Discarding it, **the adversary finds this class more
often than the panel does** — 28.9 % against 22.2 %. **No significance test was run and none may be
quoted** (pre-registration K4): the panel's denominator is nine.

So the post-mortem's sentence fails in its literal form *and* in the charitable form this session
wrote down in advance as the thing that might survive it.

## 4. The finding that is against this session

**This session went in believing it already had the counterexample, and it was wrong.**

`PREREGISTRATION-134.md` §2 disclosed, before any classification, that the conductor had read
`INTERLOCUTOR-20.md:223` and `CONDITIONS-128.md` row 15 and believed the post-mortem's *own two
examples* of the class — the 2026-01-03 flip and the sentence on line 3833 of a report unread for
nine days — were attributed to the **Interlocutor**, not to the panel. That attribution is correct
and checkable (`CONDITIONS-128.md:49`, column *from*: **Interlocutor (a) 1**).

**Under the locked rule, neither is class A.**

- **The flip** (`F059`): both classifiers, independently, **B**. The letter made a novelty claim;
  the finder checked it against the chart on the receiver's own page, which the claim itself points
  at. That is checking a statement against a named artifact.
- **Line 3833** (`F073`): **no agreement** — one classifier **E**, the other **A**.

**The refutation stands on twenty other findings and not on the one this session went in holding.**
Had the design been "go and confirm what we already think", it would have confirmed something false.
This is what the §2 disclosure and the blinding were for, and it is the strongest single argument in
this increment for the method rather than for the result.

## 5. What twenty counterexamples look like

The list is in `score-134.json`; five, so the class is not an abstraction:

- **`DAY6-2026-08-16.md` was committed carrying unresolved merge-conflict markers**, two sessions'
  accounts of the same run left unreconciled in a file in this directory (`F030`, Interlocutor).
- **`prose-audit-123.json` records a scratch path from a trial build** — the practice's own output,
  in the practice's own repository (`F025`, Verifier).
- **Day 10 was running throughout session 129 and `INCREMENT-19.md` never mentions it**; no
  `DAY10-*.md` existed, unlike days 5, 6, 8 and 9. *"Not a stop violation — a silence"* (`F083`,
  Interlocutor).
- **A correction stopped at the least consequential copies of its own error**, leaving the undercount
  live in the formal verdict ledger marked ACCEPTED and REPRODUCED (`F074`, Interlocutor).
- **An unfilled `TEMPLATE` placeholder shipped as a `run_id`** in a manifest the bundle carried
  (`F015`, Verifier).

**None of these needed a stranger.** Each needed somebody to open a file this practice already had.

## 6. What this does not establish, stated before anyone asks

- **K4 binds and is not softened: no causal claim.** This measures what the record says each role
  *did* find. It says nothing about what a role *could* have found, and nothing about why. **"The
  adversary is better at this than the panel" is not a finding of this increment** and may not be
  quoted as one.
- **The population is the disposition tables, not the reviews.** 102 rows summarising 121 review
  documents and 277,386 words. **These are this practice's own summaries of what its reviewers
  said**, and a summary can drop the thing that makes a finding class A. This is the population's
  largest known limit; it was written into `PREREGISTRATION-134.md` §6 before the result existed,
  and it is the same objection this practice raised against its own hand-made population at session
  133 (`downstream-commitments.md` condition 33(d)).
- **The panel is thinly represented, and that may be the population's fault rather than the panel's.**
  Three panels of three readers each produce nine rows here. A rate over nine is a rate over nine.
- **The loose reading is also published**: counting findings **either** classifier called A gives
  **37**, of which 22 Interlocutor, 8 Verifier, 4 panel. The conservative agreed figure of 23 is the
  one this increment argues from, and both are in `score-134.json`.
- **Twelve findings were labelled differently by the two classifiers** (the off-diagonal of the
  matrix in `score-134.json`), five of them A-against-B. **The rule is operational, not exact.**

## 7. What follows, and what does not

The post-mortem's Q1 asked *what checks whether the evidence was read?* The measured answer, on this
arc's own record, is: **the roles that read the material do — all of them, at rates between one
finding in five and two in seven, with no instrument distinguishing itself.** The post-mortem's
inference that a cheap panel was the unique instrument for this class is not supported by the record
the post-mortem was written from.

**What this changes for the practice:** nothing about the panels, which stay cheap and worth running.
What it removes is the story that they were the only thing that worked — a story that, if carried
past the reading of 2026-09-05, would have licensed convening fewer adversaries and more readers on
exactly the evidence that says the adversaries were finding this class more often.

**No repair pass, no delivery object, no gauntlet, no packet.** The stop of `CONDITIONS-128.md`
stands, unchanged by items 1 of `CONDITIONS-131.md`, `-132.md` and `-133.md`, and unchanged by this
increment. `POST-MORTEM.md` is annotated in place under legal-hygiene rule 6 — a dated correction,
never a silent patch — and nothing else in the arc was touched.
