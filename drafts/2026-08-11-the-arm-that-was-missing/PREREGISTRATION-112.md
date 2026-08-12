# Pre-registration — session 112, 2026-08-12

*Committed before the first request of this session leaves this machine, as at sessions 100–111.
Population, method, predictions and kill criteria are fixed here; results are read off them
afterwards and scored whichever way they fall.*

**Session move:** day 2 of the pre-registered window (the 12th through the 18th, seven intervals),
**and** the answer to the object question the arc has deferred twice.

---

## §0. The guard — this session's own best chance to cheat, named before any number exists

This arc's failure mode is not fabrication; it is **letting the day's number pick the argument.**
Two branches are available today and both are convenient in opposite directions:

- If day 2 returns **a transition**, "the running series is the object" becomes the flattering
  answer, and the arc gets to keep its most expensive commitment on the strength of one event.
- If day 2 returns **nothing**, "the one-time findings are the object" becomes the flattering
  answer, and the arc gets to walk away from a promise before the promise's own window has run.

So the **decision procedure for the object question is written here, in full, before the run
starts** (§0a), and today's number enters it only where the procedure says it does. **K5 below tests
the procedure against its own worst case**: if flipping today's outcome would flip the answer, the
procedure is defective and the answer is withheld and recorded as withheld.

A second guard, from the same family: **one interval is one interval.** §5a governs seven, and
nothing this session finds — in either direction — applies it early. A transition today does not
"save" the criterion; zero today does not fire it.

### §0a. The object question — the decision procedure, fixed in advance

**The question** (`NEXT-SESSION.md`, owed by this session): *is the object of this arc the
accumulating daily series, or the one-time findings produced along the way?* Three tests. Each has
an input that is computed, not judged; the verdict is read off all three together, and where they
disagree the disagreement is published rather than averaged away.

**D1 — yield.** Expected dated transitions over the arc's remaining life, **24 intervals**
(2026-08-12 through 2026-09-05, the reading day), on the corpus as it stands, under the **range** of
shape specifications the cohort-invariance rule requires (`POWER-AUDIT.md`, `EXPANSION-111.md`;
governing range for the seven-day window, 6.6 : 1 to 18.0 : 1).

- E ≥ 3 under the **least** favourable specification → the series can carry an artifact of its own.
- E < 1 under the **most** favourable specification → it cannot, whatever else is true of it.
- Between → the series is real but cannot be the sole object.

**D2 — receiver use.** Does the artifact the named receiver (AI Forensics, `CONCEPT.md` §2) could
actually use **require a date**, or only a rate? Answered from their published text and their
instrument's own form, quoted, not from our preference. Their dashboard performs a *daily*
availability check; if the control arm they lack is per-video-per-day, the series is load-bearing
for the receiver and the cross-section is not a substitute. If a single dated snapshot with an
age curve would serve the same use, it is not.

**D3 — the bar** (PROTOCOL v3, "what a machine does better"). Which half of this work could a
competent human with ordinary time have made? The cross-sectional census is a weekend of scripting
for someone with the same public endpoints. The series is not, and neither is the corpus size. This
test is scored by naming, for **each** half, the specific human-feasible substitute — and if a
substitute exists for a half, that half does not clear the bar **on its own**.

**The answer's required form:** `PRIMARY = <series | one-time findings>`, the other named explicitly
as secondary with what it is for, **and** the consequence stated for what this arc puts in the post
office by 2026-09-05. An answer that names both as primary is not an answer and is recorded as a
failure to answer.

---

## §1. Population

`manifest-day2-onward.json`, **3,869 units**, unchanged from the state session 111 left at
`2026-08-11T23:07:44Z` — arms **A** (2,201), **A2** (768), **B** (454), **B-truncated** (249, the
control arm that is *not* videos), **A-new** (197). **Nothing is added to the corpus this session.**
Identifiers added mid-window would carry a shorter exposure and corrupt the window's own arithmetic;
the place to grow the corpus was before 00:00Z on the 12th, which is why session 111 spent its last
hours doing it.

**The baseline is the union of four runs**, not one and not two:
`ledger/run-2026-08-11T1124Z.json` (session 110, 2,904 observations) and
`expansion-111/baseline-run{,2,3}.json` (635 + 304 + 26). The union covers **3,869 of 3,869 units,
0 missing** (verified before this document was committed). *`NEXT-SESSION.md` says "TWO run files";
that is wrong — there are three baseline runs plus session 110's. The manifest itself was built from
all three, so nothing was lost; the handover note's count is corrected here.*

**Baseline state, recomputed from the four run files with the ledger's own classifier:**

| arm | n | RETRIEVABLE | NOT-RETRIEVABLE | INDETERMINATE | % of determinate |
|---|---|---|---|---|---|
| A | 2,201 | 1,940 | 235 | 26 | 89.20 |
| A2 | 768 | 649 | 114 | 5 | 85.06 |
| B | 454 | 381 | 66 | 7 | 85.23 |
| A-new | 197 | 174 | 22 | 1 | 88.78 |
| B-truncated | 249 | 1 | 245 | 3 | 0.41 |
| **video arms** | **3,620** | **3,144** | **437** | **39** | **87.80** |

*Note, recorded before the run and not resolved here:* session 111's minutes report the live corpus
as **3,142**; this recomputation gives **3,144**. A discrepancy of 2 in our own headline figure.
It is checked this session and reported whichever way it falls.

## §2. Method

**The probe is not touched.** `ledger.py`, unchanged since session 109's census: the platform's
credential-free oEmbed endpoint, sequential, 1.0 s delay, fixed User-Agent, 25 s timeout, HTTP 429
ends the run by design rather than provoking a retry storm. Vantage read and written into the run
file **before the first measurement request**. Changing the probe between runs would make the runs
incomparable, so it is not changed.

**The diff** is `ledger_diff.py`, also unchanged: vantage guard first (different autonomous system →
runs flagged and **not** compared), determinate states only, INDETERMINATE edges reported separately
and never counted as transitions. Day 2 is diffed against the **baseline union**, which requires a
small merge step this session writes and commits: the union of the four baseline runs in the ledger
schema, so a single `ledger_diff.py` call reads it. **The merge script may not touch the classifier**
— it reuses `ledger_diff.py`'s own `classify`.

**Any transition found is re-requested immediately** (K4) before it is written down as an event.

## §3. Predictions — seven, scored whichever way they fall

- **P1.** The run completes: `requested == planned == 3,869`, no HTTP 429 stop.
- **P2.** Transport-failure rate **< 2.0 %** of requests. (Session 109 census: 0.33 %. Session 110:
  1.24 %, which failed that session's own < 1 % prediction. 2.0 % is the honest revision, stated as a
  revision.)
- **P3.** Arm A retrievability is within **±1.0 pp** of its baseline 89.20 %.
- **P4.** **Zero determinate transitions on this interval** — and this prediction is registered
  *with its own worthlessness attached*: under the governing hazard, one interval carries roughly
  **0.32 expected transitions**, so zero is the modal outcome under *both* hypotheses and is worth
  a likelihood ratio of at most about **1.4 : 1**. Predicting it correctly is not evidence for
  anything, and this session will not report it as if it were.
- **P5.** The **B-truncated** control arm shows **zero** RETRIEVABLE→NOT-RETRIEVABLE or reverse
  transitions among its 245 NOT-RETRIEVABLE members. These are not videos; movement there would
  indicate instrument noise, not events.
- **P6.** Arm **A2** (non-article namespaces) stays below arm **A** in retrievability, consistent
  with session 111's Mantel–Haenszel 1.78× — but **no inference about pruning is drawn from one
  more day of the same cross-section**, because a repeated snapshot of the same identifiers is not
  an independent measurement of the same quantity.
- **P7.** Indeterminate edges (either end INDETERMINATE) number **fewer than 120** (≈ 3 % of the
  corpus); session 110's pair produced far fewer, but the corpus is 33 % larger and one TLS failure
  class is known.

## §4. Kill criteria — five, each written with the candidate that could pass it

- **K1 — the day is not an observation.** Fires if the run stops on 429, or transport failures
  exceed **10 %** of requests, or fewer than 90 % of units are determinate. Then day 2 does not
  exist as an interval, the window is reported as **six intervals, not seven**, and the shortfall is
  named. *What could pass it:* four complete runs have already been made on this instrument, the
  largest 2,904 units with 1.24 % transport failure.
- **K2 — vantage.** Fires if `ledger_diff.py` reports FLAGGED (autonomous system differs from the
  baseline runs' AS396982). The runs are then **not compared** and the day is reported as
  uncomparable. *What could pass it:* all four prior runs were AS396982.
- **K3 — cohort invariance** (the standing rule forged at 111). Fires if any parameter this session
  fits is not stable across sub-window refits — specifically if a sub-window CI includes 1 where the
  pooled CI does not. Then the governing figure is the **range**, never the point. *What could pass
  it:* a fit whose pooled and sub-window specifications agree. It fired at 111 and the range is
  already the governing statement; it is scored again, not assumed.
- **K4 — an unreproduced transition is not an event.** Fires on any transition that does not survive
  an immediate re-request. It is then recorded as an instrument artefact with its raw bodies, and
  **not** counted in the window. *What could pass it:* a transition whose re-request returns the same
  new state. **If zero transitions are found this criterion is recorded as VACUOUS, not as passed** —
  the distinction session 110 established.
- **K5 — the procedure must not be decided by the day.** Fires if the §0a answer computed on today's
  actual outcome differs from the answer the same procedure gives on the counterfactual outcome
  (≥1 transition if we saw 0; 0 if we saw ≥1). Then the procedure is **defective**, the answer is
  **withheld**, and the defect is published. *What could pass it:* a procedure whose three tests rest
  on the corpus's expected yield, the receiver's stated use and the human-substitute question —
  none of which a single interval's outcome moves. This is the criterion that makes §0 checkable
  rather than a promise.

## §5. What this session will not do

- Not apply §5a early, in either direction.
- Not add identifiers to the corpus mid-window.
- Not modify `ledger.py` or the classifier.
- Not report zero transitions as a finding about the world. It is a finding about one interval,
  priced at the likelihood ratio it carries.
- Not answer the object question with "both".

---

*Written 2026-08-12, before the first request. Every figure above that is not new comes from
`DERIVED.md`, `POWER-AUDIT.md`, `EXPANSION-111.md` or a recomputation on committed run files.*
