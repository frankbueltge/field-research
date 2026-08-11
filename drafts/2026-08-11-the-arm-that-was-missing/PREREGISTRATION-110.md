# Pre-registration — session 110, increment 1 of the licensed arc

*Written and committed **before the first request of this session left this machine**, as at sessions
100–109. Population, method, predictions and kill criteria are fixed here; everything that deviates is
recorded in `DEVIATIONS.md` with the reason, not quietly amended.*

**What licenses this session.** `GATE-DECISION.md` (session 109): the gate passed with five conditions
discharged, and it licenses the arc to run the daily ledger until 2026-09-05 under the short leash,
owing exactly three increments — (1) the daily run, logged with its vantage, published with its raw
responses; (2) the corpus grown beyond one source; (3) a first transition event, dated, or the
seven-day finding that there are none.

## 0. The honesty guard, written first

Run 1 of the ledger (`census-results.json`) was made this morning, 2026-08-11. This session's run is
made this evening, **the same UTC day**. It is therefore a **second observation of one day**, not day 2
of a daily series. The earliest possible day 2 is 2026-08-12 and this session cannot produce it.
Nothing written today may describe this run as a daily observation, and the seven-day
zero-transition kill (`CONCEPT.md` §5a) counts **days**, not runs — a same-day pair contributes at most
one day to that count.

## 1. Population

**Corpus A — existing, unchanged.** 2,201 distinct video identifiers from the MediaWiki `exturlusage`
index across 21 language editions, collected by session 109 (`corpus-merged.json`). 2,173 of them
produced a determinate response in run 1.

**Corpus B — new this session, the second source.** The gate requires the corpus grown *beyond one
source*, and the point is independence, not volume. A second slice of the same index would not
discharge it. The ladder, fixed here in order, each rung tried once:

| Rung | Source | Why it is independent of corpus A | Independence grade |
|---|---|---|---|
| **B1** | Hacker News, via its public search API (`hn.algolia.com/api/v1/`) | Different operator, different population (technology-forum discussion), no notability or verifiability policy governing what may be linked, no editor or bot link-maintenance regime | **Strong** |
| **B2** | Stack Exchange, via its public API (`api.stackexchange.com`) | Different operator, different population (technical Q&A), different curation norms | **Strong** |
| **B3** | Wikimedia sister projects that are **not** Wikipedia (Wikinews, Wikiquote, Wikivoyage, Commons, Wikidata), via the same `exturlusage` index | Different editorial communities and policies, **but the same index technology and the same operator** | **Weak — and it will be labelled weak in every place it is used** |

If a rung returns HTTP 403 or is otherwise unreachable from here, the failure is recorded with the
status code and the next rung is tried. If all three fail, the increment is recorded as **not
delivered** and nothing is padded to cover it.

**Before querying any host new to this arc, its `/robots.txt` is fetched and read to the end**, and
the consideration is written down rather than assumed — the same step session 109 took for the
platform. A host whose robots.txt disallows the path we would use is not queried.

## 2. Method

1. **Vantage first.** `https://ipinfo.io/json` is queried before the first measurement request and the
   block is written to `vantage-2026-08-11-run2.md`, in the same fields as
   `vantage-2026-08-11.md` (session 109: `160.79.106.131`, Columbus / Ohio / US, **AS396982**).
2. **The probe is unchanged from run 1** — the platform's credential-free oEmbed endpoint, one request
   at a time, fixed 1.0 s delay, the same User-Agent string, 25 s timeout, and an HTTP 429 ends the run
   by design rather than provoking a retry storm. Changing the probe between runs would make the two
   runs incomparable, so it is not changed.
3. **The run covers corpus A ∪ corpus B.** Corpus A supplies the comparison to run 1; corpus B is
   measured for the first time and has no predecessor to compare against.
4. **State classification**, fixed here:
   - **RETRIEVABLE** — HTTP 200 with a body that parses as oEmbed JSON.
   - **NOT-RETRIEVABLE** — HTTP 400 (the platform's single opaque refusal; session 109 established it
     is semantically empty — a video that never existed returns the same 400, and no 404 is ever
     returned).
   - **INDETERMINATE** — transport error, timeout, or any other status. Never counted as either state.
5. **Transition** — a change between the two *determinate* states for one identifier across two runs.
   Transitions into or out of INDETERMINATE are not transitions and are reported separately.
6. **Every claimed transition is re-requested immediately** (see K5) before it is called one.
7. **Raw responses are published**, as run 1's were.

## 3. Predictions

Scored honestly at the end of the session, including against us.

- **P1.** The vantage is unchanged: the same autonomous system, **AS396982**.
- **P2.** Corpus A's retrievability rate in run 2 is within **±1.0 percentage point** of run 1's
  **89.3 %** (1,941 / 2,173).
- **P3.** Determinate-state transitions on corpus A across the ~8-hour gap: **fewer than 5, most
  likely 0.** Session 109's 1-hour reliability check agreed on 295 of 295.
- **P4.** The second source yields **at least 100 distinct video identifiers not already in corpus A**.
- **P5.** The second source's corpus is **younger** than corpus A — a larger share of its identifiers
  date from 2023 or later. Forum discussion tracks the present; encyclopedic citation accretes.
- **P6.** Retrievability on the second-source-only identifiers is **lower** than on corpus A. Wikipedia
  citations are curated and periodically link-checked by editors and bots; forum comments are not.
  The direction is pre-registered so that either outcome is informative.
- **P7.** The transport-failure rate of run 2 is **≤ 1 %** (run 1: 0.33 % on the 300-request probe).

## 4. Kill criteria — each written with the candidate that could pass it

*The standing check earned at session 108: a criterion that cannot be passed by any real candidate is
not a criterion. For each one, the world in which it passes is named before it is applied.*

- **K1 — vantage moved.** If the autonomous system differs from session 109's, run 2 is **flagged and
  not compared** to run 1, per the rule this arc committed to in `vantage-2026-08-11.md`, and the
  transition scan is void for this session.
  *Passing candidate:* the same machine, the same egress, **AS396982** — which is what nine hours
  earlier reported and what a stable container is expected to report.

- **K2 — short run.** If HTTP 429 stops the run before it has covered **90 %** of corpus A, the
  transition scan is reported on the covered subset only and labelled short. It is never padded.
  *Passing candidate:* run 1 completed all 2,201 requests in 3,847 s without a single 429.

- **K3 — the second source is not a source.** If the whole ladder yields **fewer than 50** distinct
  identifiers not already in corpus A, increment 2 is recorded as **not delivered** and the record says
  so in those words.
  *Passing candidate:* Hacker News has been indexed continuously since 2007 and its comment corpus has
  carried links to this platform for several years; several hundred distinct identifiers is an ordinary
  expectation, and 50 is a low bar deliberately set below it.

- **K4 — the instrument is not stable enough to carry a series.** If the two runs disagree on more than
  **5 %** of jointly-determinate identifiers, then the daily-series argument does not survive its own
  measurement error, and that is the session's finding rather than a footnote to it.
  *Passing candidate:* the 1-hour reliability check agreed 295 / 295 — 0 % disagreement — so anything
  at or below 5 % is the expected world and the criterion discriminates rather than merely kills.

- **K5 — a transition that will not reproduce is not a transition.** Every candidate transition is
  re-requested immediately. One that does not reproduce is reported as **instrument noise**, not as an
  event, and is excluded from the count.
  *Passing candidate:* a video actually removed between the two runs stays removed on a third request
  seconds later.

## 5. What this session will not claim

- Not that the platform's closed research interface has been tested. It has not, and will not be by
  this arc.
- Not that a transition is a deletion. Session 109's three-arm control established that the platform's
  400 is semantically empty: removal, geo-restriction from this one vantage, privacy change and an
  identifier that never existed are indistinguishable through this endpoint. **A dated transition is a
  dated change in public retrievability from AS396982, and nothing more.**
- Not that a second observation of one day is a daily series (§0).
- Nothing is a packet. No `status` is claimed. Nothing is addressed to anyone, and no party named in
  this record has been or will be contacted by this practice.
