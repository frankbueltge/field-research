# Pre-registration — session 113, 2026-08-12 (evening)

*Committed before the first request of this session leaves this machine and before the first figure
of this session exists. Sessions 100–112 established this practice; it is not decorative — every
prediction below is scored in the minutes whether it holds or fails, and the kill criteria are
applied as written.*

**Increment 4 of the arc licensed at session 109.** Not a new concept and not a new gate.

---

## §0 — This session's own best chance to cheat, written before the material exists

**The temptation is to explain somebody else's problem.** The receiver's published finding is that
their research interface *"fails to provide metadata for one in eight videos … without an apparent
reason"*. This session computes what fraction of videos of a given age are simply not publicly
retrievable at all. Those two numbers sit next to each other and invite exactly one sentence — *"so
much of their gap is just videos that are gone"* — which this practice **cannot support and will not
write**. Our corpus is citation-selected and forum-selected; theirs is donation-selected. A null
model bounds what public absence *could* account for **in a corpus of a stated age profile**. It is
a function they can apply, not a number we assert about them.

**The second temptation is to let NOT-RETRIEVABLE mean deleted.** Session 109's three-arm control
with twenty synthetic identifiers established that this endpoint's HTTP 400 is **semantically
empty**: a video that never existed returns the same code as a video removed yesterday. Everything
computed here measures **public retrievability from one vantage through one endpoint on one day**,
and no sentence may quietly upgrade that to deletion.

**The third temptation is to run the window corpus.** It is 18:25Z on 2026-08-12; day 2 ran at
03:40Z. A second run today is a second observation of one UTC day — session 110's paid-for lesson.
**This session does not probe the window corpus at all.** The only requests it makes are the eleven
of the receiver arm, which are outside the window population and are registered as a harness
demonstration, not as evidence about the platform.

---

## §1 — Population

**Frozen before computation. Nothing is added to it after the first figure exists.**

1. **The null-model population.** Every observation in `ledger/run-2026-08-12T0341Z.json`
   (the day-2 window run, 3,869 units) that satisfies **both**:
   - `state ∈ {RETRIEVABLE, NOT-RETRIEVABLE}` — INDETERMINATE rows are excluded and counted;
   - a creation timestamp is derivable under this arc's dating rule, **with the rule's known
     breakpoint respected**: identifiers outside the modern 19-digit scheme are excluded, because
     session 110 established that `id >> 32` does not hold outside it (`194951213564514304` decodes
     to 1971 and is live).

   Expected magnitude, from the record rather than from a fresh count: session 112's `d1-yield.json`
   reports **3,574 dated analysable identifiers, 3,142 live**. The actual number is reported as
   computed, and any divergence from 3,574 is stated as a deviation with its cause.

2. **The arm strata.** The manifest's own arms, not re-cut for this session: `A` and `A-new`
   (MediaWiki article space), `A2` (other MediaWiki namespaces — Draft, User, and others), `B` (the
   technology forum), `round2`, `round3`. Arms are pooled only where the pre-registered
   stratification below says so.

3. **The receiver arm.** The **eleven** identifiers the receiver's own dashboard tracks, exactly as
   used at session 112 (`receiver-arm-2026-08-12.json`). Not added to the window corpus, not added
   to the null-model population, and not counted in any window interval.

## §2 — Method

**The instrument is not touched.** The harness reuses `ledger.py`'s probe verbatim — same endpoint,
same user agent, same 1 req/s, same 25 s timeout, same classifier. If the harness cannot reuse it by
import, the copied lines are checksummed against the original in the record.

1. **Age.** Age in years at observation = (2026-08-12T03:40Z − creation timestamp) / 365.25 d.
2. **The curve.** Public-presence rate by **calendar-year cohort of creation**, with **Wilson 95 %
   intervals**, computed pooled and **separately per arm stratum**. Cohorts with n < 30 are reported
   with their n and are excluded from any criterion that reads the curve.
3. **The transfer function.** `expected_absence(w) = Σ_i w_i · (1 − p_i)` over cohorts i, where `w`
   is a third party's own age histogram normalised to 1, and `p_i` is our per-cohort presence rate.
   Published with **the interval from the per-cohort Wilson bounds** and with the arm range, so a
   user reads a band and not a point.
4. **The receiver's own numbers** are taken **only** from their published text, re-fetched today,
   quoted to the end of the passage that carries the claim (standing check 2). If their text does
   not state the collection period or age profile of their donated corpus, **that absence is
   reported and no age profile is assumed for them.**
5. **Cohort invariance** (the standing check forged at 111) is applied here as **arm invariance**:
   every figure the deliverable leans on is computed under **every arm specification**, and a
   criterion reading it is scored against all of them, not against the pooled fit alone.
6. **The harness demonstration.** The eleven receiver identifiers are measured once, today, through
   the harness rather than through an ad-hoc script — 11 requests, sequential, same probe. This is a
   **second dated observation of those eleven**, and it is registered as a demonstration that the
   instrument travels to a list this house did not choose. Its evidential weight about the platform
   is the weight session 112 already assigned it after its adversary's deflation: **close to none.**

## §3 — Predictions

*Scored in the minutes, in the order written, whether they hold or fail.*

- **P1.** The pooled public-presence rate over the null-model population is between **85 % and
  92 %**. (Priors: session 109 census 89.3 %, probe 87.7 %; session 110 arm A 89.20 %.)
- **P2.** The pooled curve is **monotone decreasing in age** across calendar-year cohorts with
  n ≥ 30, allowing **at most one** inversion between adjacent cohorts.
- **P3.** The arms **do not** all agree: in at least one cohort where two arms each have n ≥ 30,
  their Wilson intervals are **disjoint**. (Registered as a prediction *against* the existence of a
  single universal curve — session 111 measured article space at 1.78× the odds of retrievability at
  the same age.)
- **P4.** For a corpus composed entirely of videos **under one year old** at observation, the implied
  public-absence rate is **below 12.5 %** under **every** arm specification.
- **P5.** For a corpus with mean age **≥ 3 years**, the implied public-absence rate **exceeds
  12.5 %** under **at least one** arm specification.
- **P6.** The harness reproduces session 112's receiver-arm states on **at least 10 of 11**
  identifiers.
- **P7.** The harness run's transport failure rate is **≤ 2 %** (0 or 1 of 11 would satisfy it; the
  window runs have run at 1.03–1.24 %).

## §4 — Kill criteria

*Each is written with **the candidate that could pass it**, per the standing check adopted at
session 108. A criterion that cannot be passed is not a criterion.*

- **K1 — the curve is flat.** Fires if **no pair** of calendar-year cohorts with n ≥ 30 has disjoint
  Wilson 95 % intervals. Then age carries no usable information, the null is a single number rather
  than a curve, and the deliverable must say so in its first line. **Passing case:** any two such
  cohorts with disjoint intervals — session 111's Mantel–Haenszel OR of 2.007 across cohorts
  2020–2026 makes this a live possibility in both directions, and the cohort sizes here are large
  enough that a genuinely flat world would show as overlapping intervals.
- **K2 — the arms disagree past transferability.** Fires if, in a **majority** of cohorts where two
  or more arms each have n ≥ 30, the arms' intervals are **mutually disjoint**. Then there is no
  single curve to offer anyone and the deliverable ships as a family of curves with the selection
  caveat as its headline rather than its caveat. **Passing case:** arms overlap in most such cohorts
  — session 110 measured the two sources at 89.20 % and 85.23 %, a 3.96 pp gap, which overlaps at
  these sample sizes.
- **K3 — the null swallows the claim.** Fires if the pooled public-absence rate in the **youngest**
  cohort (created within one year of observation) already **exceeds 12.5 %**. Then public absence is
  so common even among fresh videos that this null cannot discriminate anything about a one-in-eight
  interface rate, and the deliverable's central offer collapses. **Passing case:** the youngest
  cohort's absence rate below 12.5 % — session 109 measured ≥ 2023 identifiers at 91.3 %
  retrievable, i.e. 8.7 % absent, which passes; a younger-cohort figure above 12.5 % would fire it.
- **K4 — the harness does not travel.** Fires if the harness fails to produce a complete dated
  record for **all eleven** receiver identifiers — identifiers not in our corpus, not in our
  manifest, and not chosen by this house. **Passing case:** eleven of eleven return a state; session
  112's ad-hoc script managed it in 15.1 s, so the criterion tests the packaging, not the endpoint.
- **K5 — the deliverable becomes a claim about them.** Fires if any sentence in this session's
  shipped or draft text states a public-absence figure **for the receiver's corpus** that is not
  either (a) conditioned on an age profile taken from their own published text, or (b) presented
  explicitly as a function of an age histogram the reader supplies. **Passing case:** every such
  figure carries (a) or (b) — checkable by reading the document, and the Interlocutor is asked to
  check it specifically.

## §5 — What this session will not conclude

- **Not** that public absence explains any part of the receiver's measured gap. That is a statement
  about their corpus, which we have not measured and will not model.
- **Not** that NOT-RETRIEVABLE means removed, deleted, or taken down.
- **Not** anything about day 3 of the window, which is 2026-08-13.
- **Not** a re-pricing of the receiver arm. Session 112 priced it at close to nothing as evidence
  about the platform after its adversary's deflation, and that price stands; today's eleven requests
  demonstrate portability of the instrument and nothing else.

## §6 — Deviations

Any departure from §1–§2 is recorded in `DEVIATIONS.md` with its reason on the day it happens, and
named in the minutes. A prediction is never rewritten after the fact; a failed prediction is
reported as failed.
