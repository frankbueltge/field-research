# Increment 22 — the post-mortem's answer to its own binding question is refuted, and half of this session's answer is withdrawn

**Session 134, 2026-08-24.** Scored against `PREREGISTRATION-134.md`, committed at `6fac67e`,
03:41:12Z — before the extraction instrument existed and before any finding was classified.

**This document was rewritten after two roles read its first version at `8b89e9d`.** Both blocking
findings of `VERIFIER-134.md` and charges 1, 2, 3, 4 and 8 of `INTERLOCUTOR-134.md` were accepted and
acted on; the reports are published **unedited**. **The first version's population was short by
twenty-two findings and its role attribution had an undisclosed tie-break, so every figure below is
different from the one the reviewers read.** Their verdicts are good only for the state they read,
which no longer exists. Dispositions: `CONDITIONS-134.md`. Errata: `ERRATA-134.md` E44–E48.

Artifacts: `findings-134c.json` (population, 124 findings, payload sha256 `ce7c8c394eb2f8ca…`),
`labels-134-{A,B}.keyed.json` and `labels-134-{C,D}-round2.json` (four classifiers, two rounds),
`score-134b.json` (result). The superseded first-round artifacts stand unedited beside them.

---

## 1. The claim

`POST-MORTEM.md` §8, published 2026-08-20, is this arc's public answer to what it calls its own
binding constraint — *what checks whether the evidence was read?*

> **The severed-reader panel is the only instrument here that has ever found that class of defect,
> and it found one in each of the three times it ran.**

The class: a defect whose discovery required **reading material the practice already held** and had
not read. Nine gauntlets failed on it; the post-mortem names it the thing no guard can catch, and
draws from it the lesson that a cheap panel of strangers is the one instrument that worked.

That sentence has stood in the public record for four days, through five sessions that each read the
post-mortem, and **it had never been measured.**

## 2. The design

Every numbered row of every finding-disposition table in this arc's `CONDITIONS-*.md` files —
**124 findings across eleven files**, sessions 118 to 133 — extracted mechanically by
`extract_findings_134.py`, stripped of its role-attribution column and of a published list of
role-naming tokens, and handed to **four independent classifiers, in two rounds, who were told none
of this**: not the claim, not the predictions, not who made any finding, not whether the practice
accepted it. Each answered one question per finding under the rule locked in `PREREGISTRATION-134.md`
§4: *what did the finder have to do to produce this?* — **A** read material already held, **B** check
a statement against the artifact it names, **C** run something, **D** argue, **E** cannot tell.

**Why two rounds, stated as the deviation it is.** Round 1 classified 102 findings. The Verifier then
found that the extractor required digit-only row ids and had silently dropped `CONDITIONS-122.md`'s
twenty-two findings — a whole file, whose own title reads *"Disposition of all twenty-two findings of
the session-122 gauntlet."* The recovered 22 were classified by **two different** classifiers under
the identical rule. **Two rounds by four readers is not one reliability figure**, and the rounds are
reported separately throughout.

## 3. The result

| kill condition | value | verdict |
|---|---|---|
| **K1** raw agreement, round 1 (n=102) | **0.8039** | clears 0.60 |
| **K1** raw agreement, round 2 (n=22) | **0.7273** | clears 0.60 |
| **K1** pooled (n=124) | **0.7903** | clears 0.60 |
| **K3** unclassifiable by either | **5 of 124** | clears the one-third bar |
| **K2** attributed to a single role | **110** | clears 20 |

| prediction | result |
|---|---|
| **P1** — at least one class-A finding attributed to a role that is not a severed reader | **THE CLAIM IS REFUTED. 22 counterexamples**, each agreed by two blind classifiers; **six of them certified by this session's own adversary** as surviving a hostile reading with no real argument against A. |
| **P2** — class A is a minority (< 25 %) | **HELD**: **25 of 119** classifiable findings, **21.01 %**. |
| **P3** — at least one class A from the Interlocutor *and* one from the Verifier | **HELD.** |
| **P4** — the panel has the highest rate of class A | **WITHDRAWN. See §5. This session does not report a rate comparison and asks that none be quoted from it.** |

**The class is found 25 times in this arc's own record, and the finders are not the panel.** The six
the adversary certified, by key, all from `score-134b.json`:

- **`CONDITIONS-124.md#4`** — `DAY6-2026-08-16.md` was **committed carrying unresolved merge-conflict
  markers**, two sessions' accounts of the same run left unreconciled in a file in this directory.
- **`CONDITIONS-123.md#15`** — `prose-audit-123.json` records **a scratch path from a trial build**:
  the practice's own output, in the practice's own repository.
- **`CONDITIONS-123.md#12`** — the status pointer is **circular**: README points at VERSIONS,
  VERSIONS points at README.
- **`CONDITIONS-129.md#1`** — a correction **stopped at the least consequential copies of its own
  error**, leaving the undercount live in the formal verdict ledger, marked ACCEPTED and REPRODUCED.
- **`CONDITIONS-129.md#10`** — **day 10 was running throughout session 129 and `INCREMENT-19.md`
  never mentions it.** *"Not a stop violation — a silence."*
- **`CONDITIONS-133.md#1`** — the convergence audit's population **omitted `audit_instrument.py`**, a
  live self-referential instrument in this same arc.

**None of these needed a stranger.** Each needed somebody to open a file this practice already had.
The adversary looked for a reading under which none survives and reported that it could not produce
one.

## 4. The finding that is against this session

**This session went in believing it already had the counterexample, and it was wrong.**

`PREREGISTRATION-134.md` §2 disclosed, before any classification, that the conductor believed the
post-mortem's *own two examples* of the class — the 2026-01-03 flip and the sentence on line 3833 of
a report unread for nine days — were the refutation, because both are attributed in the record to the
**Interlocutor** (`CONDITIONS-128.md:49`, column *from*: **Interlocutor (a) 1**).

**Under the locked rule, neither is class A.**

- **The flip** (`CONDITIONS-128.md#1`): both round-1 classifiers, independently, **B**. The letter
  made a novelty claim; the finder checked it against the chart on the receiver's own page, which the
  claim itself points at.
- **Line 3833** (`CONDITIONS-128.md#15`): **no agreement** — one classifier **E**, the other **A**.

**The refutation stands on twenty-two other findings and not on the one this session went in
holding.** Had the design been *go and confirm what we already think*, it would have confirmed
something false. That is what the §2 disclosure and the blinding were for.

## 5. What this session withdraws, and why the withdrawal is measured rather than conceded

**The first version of this document said: *"the adversary finds this class more often than the panel
does — 28.9 % against 22.2 %"*, and §7 said *"no instrument distinguishing itself."* Both sentences
are WITHDRAWN** (`ERRATA-134.md` E47). The adversary's charges 1, 2, 3 and 8 all bear on them, and
charge 3 is the one that decides it.

**Charge 3, demonstrated rather than argued:** the population is built from *this practice's own
summaries of what its reviewers said*, and those summaries provably under-table the panel's
reading-based output. The instance the adversary produced: `READERS-127.md:110-115` records a
severed reader finding that running the printed command discloses the reader's own IP address — read
out of the tool's own output — and the disposition table folds it into an **Interlocutor-only** row
at `CONDITIONS-127.md` finding 8. **A panel finding was recorded under another role's name.**

**And the repair made the panel look worse, which is the evidence for the withdrawal.** Correcting
the role tie-break (charge 2) moved `CONDITIONS-128.md#12` — one of the panel's two class-A findings
— into a JOINT cell, because the table credits it to *"panel, reader 3; reproduced and extended by
this session."* The panel's rate fell from 2/9 to **1/7**. **A population that gets worse for the
panel every time this practice fixes its own bookkeeping is measuring the bookkeeping.**

For completeness, and because the adversary's own arithmetic did not survive the repair either: on
the repaired population, pruning **all nine** findings charge 4 contests leaves the ranking
Interlocutor · panel · Verifier, and pruning half leaves Interlocutor · Verifier · panel. The
Interlocutor is top under every pass. **This session still reports no ranking**, because a comparison
that survives one attack and not the population's own known defect is not a result. The full table is
in `score-134b.json` under `P4_rate_comparison`, marked WITHDRAWN, published as the evidence for the
withdrawal and not as a finding.

## 6. What this does not establish, stated before anyone asks

- **K4 binds and is not softened: no causal claim, and no ranking.** This measures what the record
  says each role *did* find. It says nothing about what a role *could* have found, and nothing about
  why. **"The adversary is better at this than the panel" is not a finding of this increment.**
- **The population is the disposition tables, not the reviews.** 124 rows summarising 121 review
  documents and 277,386 words. §5 gives the demonstrated instance of what that costs.
- **The classifiers' independence is asserted, not shown** (`INTERLOCUTOR-134.md` charge 1, accepted).
  Four separate blind readers, given identical instructions and no access to each other's output or
  to this practice's reasoning; the label files carry no provenance beyond that, and **shared bias
  between readers applying one rule is not excluded by an agreement figure.** Round 2's 0.7273 on
  22 items is the only evidence here of how the rule travels between rounds.
- **Twenty-six of 124 findings were labelled differently by their round's two classifiers** (20 in
  round 1, 6 in round 2 — and the first draft of this line said nineteen, typed rather than computed,
  in the document whose own erratum E48 is about exactly that; `ERRATA-134.md` E48), and
  `INTERLOCUTOR-134.md` charge 4 argues that nine of the class-A calls have a defensible alternative
  reading. **The rule is operational, not exact**, and the agreement figure is carried by the
  unambiguous bulk.
- **Twenty-five is not a rate.** This arc has published against itself that six events is not a rate;
  twenty-five findings over eleven files, unevenly distributed by session, is a count.

## 7. What follows

The post-mortem's Q1 asked *what checks whether the evidence was read?* Its own answer — that one
cheap instrument was the only thing that ever caught this class — **is refuted on the record the
post-mortem was written from.** Twenty-two of the twenty-five class-A findings in this arc's own
dispositions belong to roles that are not the panel.

**What this changes:** nothing about the panels, which stay cheap and worth running. What it removes
is the story that they were the only thing that worked — a story that, carried past the reading of
2026-09-05, would have licensed convening fewer adversaries on the evidence that adversaries were
finding this class at all.

**What it does not license is a replacement story.** This session tried to supply one, in the form of
a rate comparison, and its own adversary showed the comparison rests on bookkeeping. **The measured
answer to Q1 is a negative result: the class is found by whoever reads the material, and this
practice's record cannot say which role reads it best.**

**No repair pass, no delivery object, no gauntlet, no packet.** The stop of `CONDITIONS-128.md`
stands, unchanged by items 1 of `CONDITIONS-131.md`, `-132.md`, `-133.md`, and unchanged by this
increment. `POST-MORTEM.md` is annotated in place under legal-hygiene rule 6 — a dated correction,
never a silent patch — and nothing else in the arc was touched.
