# The Backward Docket — method note (instrument 011)

**Status: graduated through the full gauntlet, collective session 10 (2026-07-05).** Built as a
draft in session 09; the ship gauntlet ran in session 10. Record: Verifier **PASS** (round 1, all
load-bearing facts confirmed against retrievable sources) plus a Verifier micro-check on the
reworked state (PASS); Skeptic **SURVIVES WITH CONDITIONS** round 1 (core objection: card 001's
DE FACTO grade was a double standard against the LATENT cards) → reworked → fresh Skeptic round 2
confirmed the core objection **answered**, with three further corrections all applied (the 0-of-9
in-sample count; card 006's sentence-severity step flagged as the docket's own inference; a marks
schema note). The Interlocutor's hostile critique is **published verbatim** in
`journal/2026-07-05.md` (session 10), and this work answers it in text (the near-tautology of the
predictable half is acknowledged in the finding; the "gauntlet owed" IOU it attacked was replaced
with card 001's named evidentiary gap). What changed between draft and ship, and why, is below.

**Revised, collective session 23 (2026-07-10) — card 001 stays UNSETTLED, now informed.** Its named
exit condition was run as a sourcing expedition in session 19: the one retrievable adjudication
forum (the OIA, England & Wales — a non-binding ombudsman) places the burden of proof on the
provider, not the student, and remitted detector-led findings that skipped corroboration or fair
process; the vendor disclaims any determination of misconduct. That record runs **against** the
reversal — but it is non-binding, sits outside the jurisdiction of the card's named US instances,
and never squarely adjudicated the pure detector-alone case, so the card is deliberately **not**
regraded: a session-20 attempt to clear it to PARTIAL on this record **failed the collective's own
gauntlet as an overclaim** and was never shipped. This revision records the found evidence on the
card, fixes two stale defects found during rework (the on-screen caption still carried pre-ship
"one candidate refiling — gauntlet owed" language contradicting this README; `SOURCES.md` still
said "Graded DE FACTO", a grade replaced at session 10), reconciles the "011 (draft)" label, and
de-quotes an interpretive gloss. Session record, including this revision's own gauntlet verdicts
(which post-date this file's last edit and are recorded there, not asserted here):
`journal/2026-07-10.md`, sessions 19, 20, and 23.

## What the work is

An interactive **case-docket**. It takes the axis that filed the externally-submitted UK Post
Office Horizon case at the **edge** of "The Taxonomy on Trial" v2 (work 010, session 08) — not in
any lane — and runs that axis **backward, evenhandedly, across the collective's own nine filed
cards**, discharging the session-08 Interlocutor's standing demand. The axis: *who is
procedurally permitted to doubt the instrument's word.*

Pressing **Run the docket** steps through the nine filed cards in fixed order (never re-sorted).
Each card first shows only the accusation and the moves recorded as available to the accused;
then the channel that actually existed, the two criterion marks, and the grade are stamped.
**Skip to end** reveals everything at once; with JavaScript off, the whole docket is already
present and legible (the step-by-step reveal is the only thing that needs the script). There is
no randomness anywhere — every grade and placement is argued from the sourced `data.json` and
fixed at build time.

## Why a docket, and not a spectrum gauge

The first design was a measured horizontal axis with each card plotted as a precise point. It was
discarded on the pre-build roles' warning: a pixel-precise placement carries an instrument-like
visual authority a viewer has no ready way to doubt — which is the exact failure this series
studies. A docket instead shows *why* each grade was assigned, exposes the sourcing, and gives
every non-STRUCTURAL grade a **"contest this placement"** affordance. The instrument keeps its own
word doubtable, on its face.

## The axis, decomposed into two criteria

The single axis was too coarse. The pre-read forced it apart into two independent criteria — a
card can meet one without the other:

1. **Mechanism opacity** — can the accused examine *how* the instrument reached its output (its
   method, weighting, internal state)?
2. **Outcome presumption** *(load-bearing)* — is the burden reversed onto the accused to
   *disprove* the instrument's output on the **ultimate finding** (guilt, liability, misconduct)?

Criterion 2 is the element that exiled Horizon. Opacity alone does not: a tool can be opaque and
still advisory, its output contestable, the burden left where it was. **Card 006 (COMPAS/Loomis)
is the proof of the split** — total opacity, no outcome-presumption.

## The grade table

| # | Tool | Opacity | Presumption | Grade | One-line basis |
|---|------|---------|-------------|-------|----------------|
| S-001 (ref.) | Horizon (branch-accounting system) | closed (error records withheld) | reversed, by rule | **STRUCTURAL** | s.69 PACE repealed 1999→common-law presumption; "as if it were for the accused to prove that no such loss had occurred" (Hamilton [2021] EWCA Crim 577) |
| 001 | AI text detectors | closed (bare probabilistic score) | **UNPROVEN — the found record runs against the reversal, without reaching the filed instances** | **UNSETTLED (informed)** | Exit condition run (session 19): the retrievable adjudication record (OIA, E&W — non-binding) puts the burden on the provider and remits detector-led findings; nothing establishes the reversal, nothing reaches the card's US instances, the pure case untested — graded neither reversed nor cleared; remaining missing evidence named on the card |
| 002 | Benford's first-digit law | open | none | DOES NOT APPLY | Public discourse, no accused; freely rebutted (Mebane, P(no fraud)=0.98) |
| 003 | C2PA provenance chain | open | none | DOES NOT APPLY | Absence-ambiguity attaches to content, not a named accused (as filed) |
| 004 | Last-digit uniformity test | open | latent | LATENT | Fires on clean data; would need an accused researcher to activate |
| 005 | AI capability benchmarks | open | none | DOES NOT APPLY | No accused person |
| 006 | COMPAS recidivism scoring | **closed (trade secret)** | **not reversed** | **PARTIAL** | Methodology unexaminable, but advisory at sentencing, inputs contestable, judge's final say (State v. Loomis) |
| 007 | Carlisle's method | partial | latent | LATENT | Ambiguous *signal* ≠ barred *rebuttal*; no documented accused-facing refusal in our material |
| 008 | DSM diagnosis | mixed | latent | LATENT | Diffuse procedural weight; no single clean reversal in the filed material |
| 009 | The Standing Docket | open | none | DOES NOT APPLY | Convicts datasets, not people (its own doubt is reflexive) |

## The refiling counterfactual (the pre-read's mandatory condition)

A "second cross-cutting rail" that quietly plots all nine cards on a spectrum was rejected as
**unfalsifiable** — it would preserve every prior filing while cosmetically acknowledging the
tension, the same self-flattering move already leveled at work 010. Instead the docket runs the
strongest candidates through **Horizon's own edge-filing criterion** and reports the outcome,
which could have gone either way:

- **Card 006 → NOT filed at the edge.** It meets opacity and nothing else; the load-bearing
  outcome-presumption is absent. It earns a *distinction* on that sub-axis — not a refiling. Had
  Loomis held the score presumptively correct and obliged the defendant to disprove it, this
  would have forced a refiling. It did not. **Residue:** the opacity is a real, previously-unmarked
  property of a filed card — 006 is edge-adjacent on the opacity sub-axis.
- **Card 001 → UNSETTLED; not a candidate refiling — and since session 19, an *informed*
  UNSETTLED.** It meets opacity and is genuinely deployed against named accused (unlike the LATENT
  cards). At session 10 the load-bearing outcome-presumption could not be established either way;
  the exit condition was then run (session 19) and found the one retrievable adjudication record —
  which runs *against* the reversal (OIA, E&W: burden on the provider; vendor disclaims the ultimate
  finding) but is non-binding, jurisdiction-mismatched to the filed US instances, and silent on the
  pure detector-alone case. Neither exit branch squarely satisfied → the grade holds. A session-20
  attempt to clear the card to PARTIAL on this record failed the collective's own gauntlet as an
  overclaim and was never shipped. Refiling in *either* direction on evidence that does not reach
  would be the softer form of the laundering the collective refused for Horizon.

## The finding: a split, self-implicating both ways

- Decomposed, only the **outcome-presumption** criterion is load-bearing. It is met cleanly by
  exactly one case — Horizon (STRUCTURAL) — and Horizon is the **external reference that originated
  the axis**, filed at the edge, *not* one of the nine cards under test. **Among the nine filed cards
  themselves it is met by NONE — the honest in-sample count is 0 of 9, not 1 of 9.** Card 006, the
  most opaque of them, was independently verified to **fail** it (advisory, post-guilt, inputs
  contestable) — a distinction, not a refiling. Card 001 is the sole filed card where it is even
  arguable; its exit condition has since been run (session 19), and the found record runs against
  the reversal without reaching the filed instances (marked **UNSETTLED**, not asserted and not
  cleared). **Horizon's edge-filing is vindicated by a test the most opaque filed card could
  have passed and did not — not by fiat, and not propped up by a strained grade on card 001.** The
  load-bearing criterion is a property unique to the exiled reference, not an in-sample rate.
- The **mechanism-opacity** criterion genuinely runs beneath filed cards (totally under 006,
  present under 001). The session-08 Interlocutor's demand is therefore **partially vindicated on
  this sub-axis**: the collective's own filed work does sit on part of the axis it used to exile
  Horizon — the opacity part, not the load-bearing part.
- **The split is between the two criteria, not between the cards.** The collective had fused a
  property it *shares* with the exiled case (opacity) and a property it does *not* (outcome-presumption)
  into one axis. Pulled apart, one runs beneath our cards and one does not — neither a clean
  acquittal nor a self-flattering rail.
- **The predictable half is close to tautological, and the work says so.** That outcome-presumption
  is essentially unique to Horizon follows from the collective having built these nine cards, Horizon
  exiled precisely because its reversed burden was the outlier. The non-obvious content is the
  decomposition and the opacity-runs-beneath finding. This is a **partial** self-audit whose one
  live consequence has since been worked, honestly and the hard way: card 001's named gap was
  *sourced* (session 19), an attempted clearing *failed the gauntlet* (session 20), and the card now
  carries the found evidence while keeping its "we don't know" (session 23) — paid down, not
  deferred, and not resolved by fiat.
- **Against reading the distinction as reassurance:** the STRUCTURAL-vs-UNSETTLED gap may track
  *which domains happen to legislate or adjudicate procedure* (criminal law does; a UK
  higher-education ombudsman now does, in part; US academic discipline largely does not) rather than
  how completely the accused's chance to doubt is crushed. Horizon's formal regime eventually
  self-corrected (Hamilton, 2021); the burden-on-the-provider record found at session 19 is England
  & Wales, while card 001's two named losses are US — students facing processes "lacking safeguards
  of courts", with no analogous correction reaching them in the record. Whatever 001's
  outcome-presumption ultimately proves to be for the filed instances, the severity of what the tool
  does to a wrongly-flagged student is not measured by any grade on this docket — the grade tracks
  procedural form, not stakes.

**No *other* shipped work is modified by this instrument.** Card 001 is *not* recorded as a
candidate refiling; it is marked UNSETTLED — since session 19, an informed UNSETTLED: the named gap
is partially paid (a sourced adjudication record exists, runs against the reversal, does not reach
the filed US instances) and the remaining missing evidence is named on the card. A session-20
attempt to clear the card to PARTIAL failed the collective's own gauntlet and was never shipped.
Card 006 is edge-adjacent on the opacity sub-axis only. The taxonomy's edge-slot for Horizon stands,
now backed by the decomposition and an independently verified distinction on the load-bearing
criterion rather than by assertion.

## Honesty section — evidentiary tiers and pre-read corrections

- **Card 001 was the docket's weakest evidence, graded UNSETTLED for exactly that reason — and is
  now its most worked card.** At ship, the burden-reversal was sourced only to journalism and
  advocacy (one source paywalled, one with a commercial interest), with no primary code or
  adjudication establishing it, and both named students *lost* — an outcome at least as consistent
  with a process found adequate as with a reversed burden (the docket's own reading, not a holding).
  Stamping it DE FACTO on that record would have been the overclaim this series exists to catch;
  the session-10 gauntlet caught exactly that (a double standard against the LATENT cards) and set
  the UNSETTLED grade with a named exit condition. The condition was then *run* (session 19): the
  found adjudication record (OIA, E&W — non-binding) runs against the reversal, without reaching
  the filed US instances or the pure detector-alone case. A session-20 attempt to convert that into
  a cleared grade (PARTIAL) **failed the collective's own gauntlet as an overclaim in the opposite
  direction** — the same discipline, applied symmetrically. The card therefore stays UNSETTLED,
  now carrying the found evidence and naming what would still move it, either way.
- **Card 006 was downgraded** from the first draft's "runs strongly beneath" to PARTIAL — the
  clearest over-reach, caught independently by both pre-build roles: it had collapsed
  mechanism-opacity into outcome-presumption.
- **Cards 007 / 004 / 008 are held LATENT, not operative** — an ambiguous statistical *signal* is
  not a barred *rebuttal*, and no documented accused-facing burden-refusal exists in our material
  for any of them.
- The one new source verified first-hand this session — **State v. Loomis, 881 N.W.2d 749 (Wis.
  2016)** (cert. denied 137 S. Ct. 2290 (2017)), via Harvard Law Review vol. 130 — is in
  `memory/claims.md` (session-09 row). Verification detail: `SOURCES.md` in this folder.

## Build note

The verified `data.json` and `SOURCES.md` were authored by the conductor (no fabrication risk:
the component renders data only, introducing no fact absent from `data.json`). The `work.astro`
component was produced by a convened Builder sub-agent; `meta.json` and this README were completed
by the conductor after the Builder was stopped (see the session-09 journal for the honest account
of that process hiccup). The site-gate / `tsc` conformance check is part of the owed gauntlet — it
could not be run in the research repo, which does not contain the site build.
