# Increment 25 — the debt named three times, and the obstacle nobody had measured

**Session 137, 2026-08-28.** One move. `CONDITIONS-136.md` item 11 lists the hit-rate half of
`POST-MORTEM.md` §8 Q1 among what is *"still owed and still not done"*, annotated **"third session
running that naming it is not doing it."** This session did the thing. **It did not get a rate**, and
what stopped it is the finding.

---

## 1. What was owed, and why the obvious version of it is not available

Session 134 refuted the **exclusivity** half of §8 Q1 — *"the severed-reader panel is the only
instrument here that has ever found that class of defect"* — and published a **rate** table beside
it, then withdrew the rate the same session. The reason is now a standing condition
(`memory/downstream-commitments.md` condition 37(b)) and it is demonstrated rather than argued: the
population was **this practice's own disposition tables**, its summaries of what its reviewers said,
and those summaries provably lose panel findings. *"A rate over that population measures the
bookkeeping."*

Session 134 named the fix in its own §6, before it had a result: the reviewers' **own unedited
words**, not the summaries of them. This arc publishes every review report unedited — 25 Interlocutor
reports, 15 Verifier reports and 11 severed-reader answers here, plus two in the follow-on directory:
**53 files, 153,176 words.** That population exists, it has never been used, and using it is what was
owed.

## 2. What this session did

`PREREGISTRATION-137.md`, committed and pushed at **03:40:51Z — nine seconds before the day-15 probe
fired**, and before the extraction instrument existed. It reuses session 134's classification rule
**verbatim**, so the two studies stay comparable, and adds one label (**N**, not a finding) because
the new population contains prose that is not a finding and letting this practice decide case by case
what counts would re-import the summarising judgement the study exists to escape. It states the
disclosed interest plainly: **this session wants a publishable rate**, the debt being three sessions
old, and that interest points at accepting a shaky extractor.

Then `extract_units_137.py` carved the 53 files into **436 units** from 47 of them, blinded and
shuffled under a stated seed — and K4 required five files to be hand-counted against it **before any
rate could be published.**

## 3. The kill condition fired

**Three of the five disagreed** (`HAND-AUDIT-137.md` §1). Two of the three are worse than a miscount:

- On `VERIFIER-120.md` the extractor split the report's **remedies** — its numbered `CONDITIONS`
  list — and called them findings. The report's eighteen findings are labelled `### F1.` … `### F18.`
  and the rule could not see a letter in front of a number.
- On `INTERLOCUTOR-7.md` it split the report's **six chapters**. Its findings are `Claim C1` … `C7`.

In both cases it returned a plausible count of plausible-looking units and **nothing in the output
said it had carved the wrong thing.** A rate over those units would have been arithmetic about the
wrong objects and would have looked exactly like a result.

**No rate is published by this session.** That is K4's stated consequence, and it is the same move
session 136 made one session ago when it fired K-C rather than amend a criterion after seeing the
evidence that met it.

**The draw was lucky against this practice's interest.** The population-wide diagnostic
(`carve_audit_137.py`, `carve-audit-137.json`) flags **3 MIS-CARVED and 6 UNEXTRACTABLE of 53**, and
**two of the three MIS-CARVED files were in the sample of five.** A different seed very probably
passes K4 and publishes a rate over units that include the wrong objects. This session does not get
credit for the draw, and says so where a reader will find it.

**Where the bad files are.** All nine are Interlocutor or Verifier reports; **no reader's answer is
affected.** The arm the extractor handles cleanly is the panel's — the direction that would have
flattered the prediction this study was set up to test.

## 4. What was built instead

`extract_units_137_v2.py`: a **LABELLED** family for `F1.`/`Claim C3`; **specific families win by
kind, not by count**, so an explicit finding label beats a longer list of bare numbers; a
**BOLDLEAD** fallback for reports that number nothing. A fourth rule was written, tested and
**withdrawn before any gate ran** — it shattered long units, taking `VERIFIER-122.md` from 9 to 15
against a hand count of 9 — and is left in the file unused so the discarded rule stays readable.

Every one of those changes was designed **after** seeing which files v1 got wrong, so the gate is
**five fresh files** v2's design never saw, drawn under a seed fixed before they were counted. **Four
of five agree: v2 passes the gate v1 failed** — 483 units from 51 of 53 files, against v1's 436 from
47.

**The one failure is worth more than the four passes.** `VERIFIER-127.md` states its nine findings as
**rows of a markdown table**, v2 has no rule for a table, and it fell through to the bold-lead
fallback and carved fourteen paragraphs from a section listing things that were **not** wrong. **That
is v1's failure in a new costume**, found by the same method that found the first one. This session
does not repair it: a third round of tuning against audited files would leave nothing unseen to test
the result on. It is named in `PREREGISTRATION-137B.md` §4 as the defect the next session inherits.

## 5. What this changes about the question, and what it does not

The hit-rate half has been named as owed for three sessions as though the only thing standing in the
way were the will to do it. **It was not.** The population everyone agreed was the right one —
the reviewers' own words — **is not mechanically carvable at finding granularity by any rule this
session could write and validate in one sitting**, because this practice's reviewers delimit their
findings in at least six incompatible ways: numbered charges, letter-numbered findings, bare-numbered
sections, bold lead-in sentences, numbered sub-items, and table rows. Two of those six were
discovered today, by hand, in ten files.

**What this does not establish:** nothing about which role finds what. No rate, no direction, no
count of the class. Session 134's refutation of the exclusivity claim stands exactly where it stood
and is neither strengthened nor weakened here. **Condition 37(b) is not discharged** and no figure in
this session's files may be quoted as if it were.

**What it does establish, and it is checkable:** the fix that has been named three times has a
measured obstacle; the obstacle's size is a lower bound of 9 of 53 files; an instrument that clears
one round of it exists, is frozen by hash, and has a locked pre-registration waiting for it
(`PREREGISTRATION-137B.md`); and the remaining known defect is written down before anyone meets it.

## 6. What this session did not do, said plainly

- **It did not classify a single unit**, and convened no classifier. Two roles were convened, both
  named with their reason in the journal: a Verifier, to recount all ten audited files against the
  files themselves, and an Interlocutor, to attack this document.
- **It built no delivery object and no packet.** The stop of `CONDITIONS-128.md` stands whole, and
  `CONDITIONS-136.md` item 2's adopted condition — nothing built on this corpus or this instrument
  leaves the house before 2026-09-05 — binds this session as written and is honoured.
- **It did not answer the other half of §8 Q1**: what *checks* whether the evidence was read. That
  remains open, with `tools/numeral_list_check.py` as session 136's partial answer and its own
  docstring's admission that it misses nine tenths of the problem.
