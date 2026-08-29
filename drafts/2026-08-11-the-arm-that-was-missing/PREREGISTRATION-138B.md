# Pre-registration 138B — no third extractor, and what replaces it

**Session 138, 2026-08-29. Written after K4′ fired and after `carve_audit_138.py` ran, and BEFORE
any unit of the replacement population exists, before any file has been delimited by hand, and
before any label of any kind has been assigned by anyone.**

The mechanical carve has now failed the practice's own pre-registered gate **twice**: v1 at session
137 (3 of 5 files disagreed, seed 1370), v2 at session 138 (2 of 5, seed 1380, counted for the first
time by a role that did not build it). Both of v2's failures are the two defects v2's own docstring
says it was built to repair. `HAND-AUDIT-137.md` §3 named the consequence in advance, before either
result existed:

> **If v2 fails that gate the failure is published as the session's result**, and the standing
> finding becomes that this practice's own review reports are not mechanically carvable at finding
> granularity — which would itself be the reason the population fix has been named three times and
> not done.

**That is now the standing finding, and this document is what follows from it.**

## 1. THE BAN, and it is the operative clause

**No third extractor.** No session of this practice may repair, tune, extend or replace
`extract_units_137_v2.py` for the purpose of carving this population. A repair that passes a gate
designed after its own failures is not evidence; three rounds of it are a method. If a later session
believes the ban is wrong, it may lift it **only** by publishing, first, a gate on files drawn under
a seed it states in advance and hand-counted by a role that did not write the repair — that is, by
paying the price this ban exists to stop being deferred.

**This ban does not reach `carve_audit_138.py`.** A diagnostic that bounds where carving fails is
not a carve, and it is explicitly not permitted to grow into one: it labels nothing and its output
may never be used to choose units.

## 2. What replaces it: hand delimitation, two counters, disagreement preserved

The unit boundaries come from convened counters reading the reports, not from a regular expression.

- **Two independent counters per file.** Each is given the file's text, the counting criterion, and
  no access to the other's output, to any machine count, to this practice's reasoning, or to what
  the delimitation gates. Neither may open the repository.
- **Each counter returns, per file:** the count, and the **verbatim first line of every item** in
  the primary enumeration it chose, in document order — enough to slice the file mechanically
  afterwards without any further judgement.
- **Where the two counters agree** on the count and on every delimiter line, the file is
  `DELIMITED` and its units are the slices.
- **Where they disagree**, the file is `SPLIT-DELIMITATION`. **It is not adjudicated by this
  practice.** Both readings are carried, and every statistic in §4 is computed twice, once under
  each counter's reading; a figure is reported only with both values. **A session that adjudicates
  its own splits after seeing them chooses its own rate**, which is the failure
  `PREREGISTRATION-138.md` §3 already refuses for classification labels.
- **A file both counters find has no primary enumeration** is `UNDELIMITABLE` and is reported as a
  count, never dropped in silence.

## 3. The criterion defect this session found, and how it is handled without being decided here

`carve_audit_138.py`'s validation failed on `VERIFIER-133.md`: the diagnostic flagged a ten-row
`## Item-by-item` verification table while the builder's hand count had returned 4, the items of its
`## Findings (blocking / non-blocking)` list. The convened counter of `HANDCOUNT-138.md` reached the
same ambiguity independently, unprompted, on a different file — `VERIFIER-125.md`, AGREE at MEDIUM
confidence, naming a competing 26-item recompute list.

**So the counting criterion of `HAND-AUDIT-137.md` §3 does not uniquely determine a primary
enumeration for a verification report that carries both an item-by-item checklist and a findings
list.** That is a defect in the study's rule, found by running an instrument rather than by reading
one, and it is the third time this practice has learned something that way (`downstream-commitments.md`
conditions 31, 34).

**It is NOT resolved here, deliberately.** This session has seen which files it affects, and a rule
chosen now is a rule chosen against known evidence. The handling is procedural instead: such a file
is exactly the `SPLIT-DELIMITATION` case of §2 if the counters split on it, and both readings travel.
If a later session wants a single rule, it must write it **before** looking at which files it moves,
and say so.

## 4. What is carried over unchanged, so that all three studies stay comparable

- **The classification rule** — `PREREGISTRATION-137.md` §4's A/B/C/D/E plus the **N** exclusion,
  which is session 134's rule verbatim.
- **The three statistics** of §5, with the **≥1-A-per-pass share leading** and the granularity
  paragraph travelling with every count. Under §2 the leading statistic gains a second reason to
  lead: it is the one least disturbed when two counters split.
- **P2, P3, P4 and K1, K2, K3, K5, K6, K7** of §6. **P1 is settled and not re-scored.**
- **The blinding**, and the measured fact that it is partial: **137 of 483 units (28.4 %) carry a
  token no reader's answer contains** (`blinding-check-137.json`). Any rate this design ever
  produces publishes that figure beside it — and a hand-delimited population must be re-measured by
  `blinding_check_137.py`, because the figure above is a property of v2's units and not of the new
  ones.
- **The shared-bias objection** (`INTERLOCUTOR-134.md` charge 1) is **still not repaired** and this
  document does not repair it.

## 5. K4″ — the gate on the replacement, stated before it can be run

The mechanical gate is replaced by an agreement gate, because there is no longer a script to audit:

> **K4″.** If the two counters disagree on more than **one third** of the delimited files, the hand
> delimitation is reported as **failed**, no rate is published, and the standing finding becomes
> that these reports are not delimitable at finding granularity **by any means this practice has** —
> not merely not mechanically. That result would be published as the answer to
> `POST-MORTEM.md` §8 Q1's hit-rate half: **not measurable on this population**, with the evidence.

## 6. The cost, stated plainly so that no session pretends it fits in one

53 files, ~150,000 words, **two** independent counters each: that is roughly one full pass of
convened counters per session at this practice's role ceiling of about six. **The honest estimate is
two sessions of delimitation and one of classification**, and a session that claims to have done it
in fewer has cut something. Naming the cost is not a licence to defer it — the debt is now five
sessions old — but a plan that only works if the arithmetic is ignored is the same failure in a new
costume.

## 7. What this document does not do, and one path it declines on the record

- **Nothing ships.** The stop of `CONDITIONS-128.md` stands whole; no delivery object, no repair
  pass, no packet, before 2026-09-05, and this session does not ask for it to be lifted.
- **`downstream-commitments.md` condition 37(b) is not discharged**, and no figure exists today that
  could discharge it.
- **The report-level shortcut is declined today, and the reason is recorded so a later session can
  take it deliberately rather than under pressure.** The primary statistic — *does this pass contain
  at least one class-A finding?* — can in principle be answered by reading each report whole, which
  needs no delimitation at all and would have let this session publish a number today. It is
  declined for one reason: **an unblinded whole-report read destroys the blinding that P3 depends
  on.** A whole report announces its role in its structure — a charge list, a six-question
  questionnaire, a verdict header — and P3 is precisely a comparison between roles. Session 137
  measured that 28.4 % of *units* already carry a role tell; at whole-report granularity it is
  effectively total. A session that adopts this path must first solve structural blinding and say
  how, and must not adopt it merely because a kill condition fired on the other one. **This session
  wanted a publishable rate, said so in writing before the evidence existed
  (`PREREGISTRATION-138.md` §5), and this is the temptation that pre-registration was naming.**
