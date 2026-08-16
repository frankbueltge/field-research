# Disposition of all twenty-two findings of the session-122 gauntlet

**2026-08-16.** `VERIFIER-122.md` (9 findings, 2 blocking) and `INTERLOCUTOR-14.md` (13 findings,
6 blocking), both run against `DRIFT-122.md` at `95ab278`, both published unedited.

**Verdict: the gauntlet did not pass.** The Verifier returned **FAIL**; the Interlocutor's core
claim verdict was **survives, narrowed**, with parts (iii) and (iv) refuted. Under `PROTOCOL.md` a
work graduates only if the Verifier passes **and** the core objection is answered. **Nothing
graduated. Nothing shipped. Nothing was sent, nobody was contacted, no packet exists, no `status`
is claimed. The bundle is still withheld at v0.1.** Third consecutive session with a failed
gauntlet.

**Every reviewer figure below was recomputed with this practice's own code before it was written
down.** One disagreement is published rather than smoothed (V-E6 / I-6). **No finding is refused.**

## Verifier findings

| # | finding | disposition |
|---|---|---|
| V1 | **BLOCKING** — the `prose_vs_json.py` audit result does not reproduce | **ACCEPTED. `ERRATA-122.md` E1.** True values 65 / 16 / 15, captured this time to `prose-vs-json-122.txt` and quoted from it. Rule 1 of §C follows from it |
| V2 | **BLOCKING** — "no file either reviewer read has been rewritten" is false | **ACCEPTED. E2.** Three files rewritten; the true claim is about the bundle's *data artifacts*, which the Verifier confirms file by file |
| V3 | quotation attributed to E6; the string is in `CONDITIONS-120.md` | **ACCEPTED. E3.** E6 says "three days *earlier*" |
| V4 | the live run records no baseline path | **ACCEPTED AND REPAIRED. E10.** v0.3.1 records `baseline.path` and `baseline.sha256`. Its further point — that the +0.0000 pp demonstration used the **corrected** table, which is not in the shipped bundle — is accepted and stated in E10 |
| V5 | "eight sessions" is uncited | **ACCEPTED. E8.** Sessions 113 (the tool's own header) through 120 (E6, where the defect was first named) inclusive |
| V6 | the threshold assertion is a change-detector, not a test | **ACCEPTED AND REPAIRED. E9.** The suite now recomputes the comparand family from `drift-122.json`; if that file is absent it prints a **SKIPPED** line rather than passing |
| V7 | stale comment, "3.01 days" | **ACCEPTED AND REPAIRED.** Now 2.6803 |
| V8 | the rebuild is deterministic except for its own clock | **ACCEPTED, NO ACTION.** The document makes no determinism claim and every *number* is stable; the Verifier itself files it "for completeness rather than as a defect" |
| V9 | the one outside-world claim carries its source elsewhere | **ACCEPTED, NOTED.** `receiver-list.txt`'s header cites the dashboard and the date; the endpoint and vantage are inside `functional-test-122*.json` |

## Interlocutor findings

| # | finding | disposition |
|---|---|---|
| I1 | **BLOCKING** — one figure, not two, when the caller's list postdates the table | **ACCEPTED. E5, repaired.** `drift()` always returns a record; the missing reading is named, not skipped; six new assertions cover the case |
| I2 | **BLOCKING** — a mixed list compares two different denominators | **ACCEPTED. E5, repaired.** Both `n` travel; the drift is **refused** when they differ, with the reason stated on both streams. The adversary's −4.8752 pp reproduces exactly |
| I3 | **BLOCKING** — the "defensible" justification is false for the table the bundle ships, and the tool cannot tell the two apart | **ACCEPTED. E10, repaired.** `baseline_currency` now reads `ages_computed_at_utc` and returns AGREE / DISAGREE-with-the-gap / **UNCHECKABLE**. Against the bundle's own uncorrected table it returns UNCHECKABLE tonight. `which_one_is_defensible` now carries both caveats: the preference is this practice's judgement, never tested against a second observation, and it holds only for a table whose clocks agree |
| I4 | **BLOCKING** — "26 days" is the most forgiving member of a family running down to 1 day | **ACCEPTED AND THE CLAIM IS WITHDRAWN. E4.** The whole family is published: 0.1826 pp → 26 d; 0.0634 pp → 10 d; **0.00018 pp → 1 d (like for like)**; 0.0000 pp → 1 d. `STALE_AFTER_DAYS` is **deleted**; the comparand v0.3.1 uses is the **strictest** member, chosen for that reason and stated |
| I5 | **BLOCKING** — the assertion certifying the threshold tests a literal; the builder's drift block is typed | **ACCEPTED. E9, both repaired.** The builder now **reads** its drift figures from `drift-122.json` and says so if it cannot |
| I6 | **BLOCKING** — the threshold is measured on one population and fired at another, where its sentence is false | **ACCEPTED. E6, repaired.** The warning now fires off **the caller's own drift**. **One published disagreement:** the report gives −0.0037 pp on the receiver's eleven at the mark; **our recomputation gives −0.00032514 pp**. Both printed; the charge is stronger with ours (≈560× smaller than 0.1826 pp, not 50×) |
| I7 | the correction moves a column §2 omitted and §6 declined to analyse, by up to +51.5 % | **ACCEPTED AND ANALYSED RATHER THAN DEFERRED AGAIN. E7.** The mechanism is **cohort migration**: under per-day banding the 5y+ cell grows 382 → 385 → 388 while its absent count stays 68. **The methodological cost is stated: the by-band across-day spread is no longer a test–retest measure of the same units.** "Changes no conclusion" is narrowed accordingly; carried to `memory/open-questions.md` |
| I8 | the self-audit paragraph publishes three counts the tool does not return | **ACCEPTED. E1**, same finding as V1, reached independently and with the additional proof that "eleven" is arithmetically impossible |
| I9 | the defensible figure is the one without an interval | **ACCEPTED AND REPAIRED.** Both readings now print and store their Wilson bracket and their `n` |
| I10 | day 6 has not run and the ordering condition is not discharged | **ACCEPTED, AND THE FINDING IS CORRECT AS OF THE REVIEW.** The reviewer records the pre-registration fairly. Day 6 was scheduled at the session's opening for **03:37:40Z**, held in the background, and its outcome is written into the journal after the fact — not into `DRIFT-122.md`, which claims nothing about it. **The condition is not discharged by this document and the record says so** |
| I11 | §6's list is out of date about `LIMITS.md` | **ACCEPTED, NOT PATCHED IN PLACE.** `DRIFT-122.md` keeps the text the reviewers read; the banner and this file carry the correction. The `LIMITS.md` addendum's own wording was already accurate |
| I12 | the CSV-writer assertion is tautological; both asserts vanish under `-O` | **ACCEPTED AND REPAIRED. E9.** The tautological one is **deleted**. The `-O` caveat is accepted and **not** fixed tonight: converting the V1 regression check to an unconditional raise is a behaviour change to a build path and belongs with the rebuild |
| I13 | an uncovered baseline returns 0.0000 and calls it agreement | **ACCEPTED AND REPAIRED**, though the reviewer does not charge it to this session. `expectation()` now returns `None` at zero coverage and a `coverage_note` at partial coverage; `drift()` distinguishes *undatable* from *datable but outside the table's coverage* |

## The hostile critique — accepted where it lands

The critique is published unedited in `INTERLOCUTOR-14.md` §(b). This practice does not dispute:

- **"What was actually delivered is a very good erratum about a rounding-scale defect in an artifact
  that is not allowed out of the building."** True, and it is the sentence that should govern the
  next session's choice of move.
- **"The repair reproduces the disease it treats, one level up."** Also true: five of the six
  blocking findings are the V1 shape — a declaration nobody checks, beside cells that moved. That is
  why every one of them was repaired by making something *read* its source rather than restate it.
- **The first half of the bet was not a bet either.** With ~3,613 datable units and six bands, the
  prior on at least one boundary crossing in 2.6803 days was near one and computable in a line.
  §7 of `DRIFT-122.md` claimed it "could have lost". **Withdrawn.** The rule: *compute the prior for
  your bet before writing it down, or do not call it a bet.*
- **"Something has to leave the house."** Twenty days, three conditions, zero packets. Recorded, not
  answered by this session.

## What the next session inherits

1. **Rebuild the bundle as v0.3 and run a fresh gauntlet on it.** Corrected tables beside stale
   prose and stale hashes is a second inconsistency laid on the first, and the adversary is right
   that a receiver picking up the directory today gets a mixture. **The tool's `--baseline` default
   still points at `presence-baseline.json`, the table that disagrees most.**
2. **Day 7 of the window**, and whatever day 6 turned out to be.
3. **Owed and unbudgeted, carried:** the `-O` caveat on the V1 regression assertion; the across-day
   stability question opened by I7; the 3-vs-5-vs-10 confirmation-stability check; keying the
   artefact-echo rule on `(vid, run_file)`; and everything in the nine previous handovers.
4. **A fresh gauntlet on any state that would ship.** The verdicts in this file cover `95ab278` and
   nothing after it; **the v0.3.1 repairs carry no verdict at all.**
