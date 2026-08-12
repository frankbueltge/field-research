# Addendum to the session-112 pre-registration — the receiver arm

*Written and committed before the probe it describes runs, and after the day-2 run had already
started. It is an addendum rather than an edit: `PREREGISTRATION-112.md` stands untouched.*

## What this adds, and why it is not a change to the population

D2 of the object question (`PREREGISTRATION-112.md` §0a) asks whether the artifact the named
receiver could use **requires a date or only a rate**. That question was going to be answered from
their published text — which is legitimate but is still an argument about a document. It can instead
be answered by measurement, at a cost of **eleven requests**, because the receiver's own dark
dashboard names the eleven identifiers it watches and this practice already holds them from session
108's derivation (`drafts/2026-08-10-one-receiver-to-the-floor/dashboard-derived-raw.txt`, fetched
2026-08-10, HTTP 200, 246,014 bytes).

**The eleven are probed as a separate, separately dated arm — arm R — and arm R is not part of the
window's population.** It does not enter `manifest-day2-onward.json`, it does not enter the §5a
count, it does not enter any fit, and it carries no exposure in the pre-registered window. The
pre-registration's rule that *nothing is added to the corpus this session* is unchanged and is not
being read around: this is a second, named, dated measurement standing beside the corpus, not inside
it. Any later session that folds arm R into the corpus opens it as its own arm with its own baseline
date, exactly as session 111 did for A2 and A-new.

## Why it runs after the day-2 run and not during it

Concurrent requests to the same endpoint from the same vantage risk a throttling response, and the
instrument's own rule is that **HTTP 429 ends a run by design rather than provoking a retry storm.**
A 429 during the day-2 run would cost the window an interval — K1 — for eleven rows of side
evidence. So arm R waits for the main run to finish. Recorded here so the ordering is a decision
rather than an accident.

## Predictions — registered before the eleven are probed

- **R1.** All eleven identifiers are 19-digit and decode to creation dates in 2022–2024, consistent
  with the receiver's published series beginning 2025-04-09.
- **R2.** **At least one** of the eleven is publicly retrievable today through the credential-free
  route. This is the prediction that carries the whole point: the receiver's instrument records
  *"Not Available"* against the research interface for 10 of 11 videos across its entire 279-row
  series, and its own page says *"Note: Error are problems on our end, not TikTok."* If a video the
  interface never returned is publicly retrievable, the gap between the two arms is a measured
  quantity rather than an inference.
- **R3.** The one video that *was* available through the interface on 213 of 279 days
  (`7332960275127110954`) is publicly retrievable today.

## What arm R may and may not be used to say

- It **may** be used to say what the credential-free public state of those eleven identifiers is on
  2026-08-12, from AS396982, through one endpoint.
- It **may not** be used to say anything about what the research interface returns **today**. The
  receiver's dashboard has not been regenerated since 2026-01-14; there is no current interface-side
  observation to compare against, and this practice has no credential and will not pretend to one.
  A disagreement between our reading today and their reading in January is **seven months apart** and
  is not a simultaneous comparison.
- It **may not** be used to say that a video was wrongly withheld, moderated, or anything about any
  named party's intent or competence.
- Nothing in it is addressed to the receiver. The identifiers come from a public page; no one is
  contacted.
