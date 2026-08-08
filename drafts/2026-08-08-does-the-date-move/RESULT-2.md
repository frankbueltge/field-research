# RESULT — increment 2: the capture-density census

*Session 101, 2026-08-08. Scores `PREREGISTRATION-2.md` exactly as written. Data: `census.json`
(per-URL, per-authority), `scored-2.json` (the scoring), `frames.json` (the frames the samples were
drawn from), `route-selftest.json` (the check on the fetch-route change). Unregistered work of the
same session is kept out of this file and lives in `PROBES.md`, `notes-classified.md` and
`CORRECTIONS.md`.*

**Headline: the obstacle that was supposed to decide this arc was described wrongly, and the census
says so on a pre-registered test. Document pages are not invisible to the public capture record —
94.5 % of them can be compared against themselves. What the record cannot support is the *monthly*
observation increment 1 was built on.**

## The scoreboard

| | prediction | value | verdict |
|---|---|---|---|
| **P5** | pooled median captures per document page, 12 months, ≤ 4 | **4.0** | **HELD** (on the boundary — see below) |
| **P6** | < 25 % of document pages have ≥ 6 distinct capture-months in 12 months | **13.1 %** | **HELD** |
| **P7** | ≥ 1 authority with ≥ 30 *pairable* document pages | **NIST 80/80** — and every authority cleared it | **HELD** |
| **P8** | pooled 90th percentile of 12-month captures < 42 (increment 1's smallest index-page count) | **12.0** | **HELD** |
| **P9** | *falsifier:* ≥ 50 % of pages with ≥ 6 capture-months → the obstacle is withdrawn | 13.1 % | **did not fire** |
| **P10** | < 50 % of the receiver's own pages are pairable | **100 %** | **NOT HELD** |

## What was measured, and what was not

| authority | sampled | measured | zero captures in 24 m | median captures / 12 m | 90th pct | ≥ 6 capture-months | **pairable** |
|---|---|---|---|---|---|---|---|
| **NIST** `/publications/` | 80 | **80** | 0 | **2** | 3 | 1 (1.2 %) | **80 (100 %)** |
| **EPA** `/newsreleases/` | 80 | **80** | 0 | **4** | 5 | 1 (1.2 %) | **80 (100 %)** |
| **GOV.UK** `/government/publications/` | 80 | **76** | 6 (7.9 %) | **7** | 18.5 | 29 (38.2 %) | **63 (82.9 %)** |
| **standards.digital.gov** (receiver, whole site) | 16 | **16** | 0 | **3.5** | 7.5 | 2 (12.5 %) | **16 (100 %)** |
| **energy.gov** `/articles/` | 80 | **0** | — | — | — | — | — |
| **pooled** | 336 | **236** | 6 (2.5 %) | **4** | 12 | 31 (13.1 %) | **223 (94.5 %)** |

**The 100 unmeasured URLs, stated plainly rather than dropped.** All 80 energy.gov URLs and the last
4 GOV.UK URLs returned `Connection reset by peer` after roughly 250 successful queries, and a
single-threaded retry pass an hour later was reset identically on both the timemap and the capture-index
endpoint for every URL tried — so **this client was rate-limited off the archive**, and it is not a
property of those URLs. Per the pre-registration's denominator rule they are excluded from every
percentage and counted here. **`energy.gov` contributes nothing to this census** and no statement in
it is about energy.gov.

## What the numbers mean

**1. The arc's stated obstacle was a wrong inference from three true numbers.** Increment 1 observed
2, 3 and 2 captures a year on its three document pages and concluded *"the archive captures indexes,
not documents"*. The capture counts are confirmed — NIST's median document page has **2** captures a
year, EPA's **4** — but the conclusion drawn from them is false. **Only 6 of 236 sampled document
pages (2.5 %) have no capture at all in 24 months, and 223 of 236 (94.5 %) have two captures at
least 30 days apart.** Two captures a year is not invisibility; it is a *pair*. The correction is
entered as `CORRECTIONS.md` C2.

**2. What actually fails is the monthly design, and P6 measures exactly that.** Only **13.1 %** of
document pages have six or more distinct capture-months in a year, and the median document page has
**2**. Increment 1 asked the record for twelve monthly observations per URL. The record has two.
A method built on monthly sampling starves on documents; a method built on **pairs** does not.

**3. Documents and indexes differ by roughly an order of magnitude, as predicted.** P8's pooled 90th
percentile is **12** captures a year against increment 1's *smallest* index-page count of 42, and the
index pages there ran to 5,000. The distinction between an index and a document is not a stylistic
one for this instrument — it changes the available evidence by two orders of magnitude at the top.

**4. GOV.UK is the exception in both directions, and it is the only authority with real zeros.** It
has the densest documents (median 7 captures a year, 38.2 % with ≥ 6 capture-months, one page with
72) *and* the only pages the archive has never captured at all — **6 of 76**. Density and coverage
are different properties and this authority separates them.

**5. P10 was wrong, and being wrong here is worth more than being right would have been.** The
prediction was that the body writing the timeliness duty could not, for most of its own pages, have
that duty checked against the public record. **All 16 of its pages are pairable**, with a median of
3.5 captures a year. The method *can* be pointed at the receiver's own site. That removes an excuse
and it removes it from us, not from them.

**6. P5 is the weakest verdict in the table and is on its boundary.** The pooled median is exactly
**4.0** against a threshold of "≤ 4". Had energy.gov been measured and been denser than NIST and EPA,
this verdict could have flipped. It is HELD as written and it should be read as the least robust line
in the scoreboard.

## The fetch route changed mid-session, and the change was checked rather than asserted

The pre-registration specifies one capture-index query per URL. Executed that way the archive
answered in 8–14 s per query and **got slower under concurrency** — four workers collapsed to roughly
one query a minute. Two alternatives were tried:

- **One prefix query per authority instead of 80 per-URL queries. Abandoned, and the reason is a
  finding.** `www.nist.gov/publications/` returned the server's 150,000-row cap for a **20-day**
  window, and fewer than **0.3 %** of those rows carried a query string — so the volume is real
  captures of real pages, not URL variants. Prefix harvesting is not viable on a heavily-crawled
  prefix.
- **The per-URL *timemap* endpoint** (`/web/timemap/json/<url>`), which returns the same rows with the
  same fields in about **1 s**. Adopted.

**The route change was verified before it was used.** Every one of the **41 URLs already measured
through the capture-index route** was recomputed through the timemap route and compared on all eight
derived values (`n24, n12, months24, months12, first, last, pairable, span_days`): **41 URLs, 0
disagreements** (`route-selftest.json`). The two differences the route introduces — no server-side
window, no server-side status filter — are applied client-side in the same terms, including dropping
revisit rows whose status is `-`.

Sample, seed, window, fields and definitions are unchanged from the pre-registration. What changed is
which endpoint answered.

## The decision rule, applied

The pre-registration fixed this in advance: **P7 holds and P9 does not fire → the arc continues as a
per-authority profile, restricted to the authorities that cleared P7, and increment 3 measures
fidelity on exactly those pairs.** P7 held on every measured authority; P9 did not fire.

**So the arc continues — but not as increment 1 designed it, and not on the claim the Interlocutor
refuted today.** What the census licenses is narrow and specific:

- a **pair design**, not a monthly one: two captures per document, ≥ 30 days apart, chosen from what
  the record actually holds;
- on **NIST, EPA and GOV.UK** (and the receiver's own 16 pages), which cleared P7; **not** on
  energy.gov, which was not measured;
- with the printed-date extractor **not pointed at index pages** — increment 1's D3 and today's Probe A
  both caught it reading a listed item's date instead of the page's;
- and with increment 1's future-date test as an entry filter.

**What the census does not do is answer the Interlocutor's two open charges** (`INTERLOCUTOR-2.md`,
charges 4 and 6): that a compliance measurement of an *implementation tip* is scope this practice
chose rather than scope the receiver asked for, and that the receiver's own site is not the population
its standard governs. Those are the gate's business at session 3, and the census does not touch them.

## The gate

**Session 2 of at most 3. The gate is not passed today.** The population obstacle — the thing session
1 named as deciding the arc — is **resolved**, and resolved against the previous session's own
statement of it. What remains open is not the data but the object: whether measuring the movement of a
date the receiver only recommends is worth the arc, and against which population. Session 3 either
answers that in one page or the concept is rewritten as a coverage finding and discarded with one.

**Owed and still not done** (carried from increment 1): the test of whether the archive's pipeline can
preserve a stale or conditional-request-derived `Last-Modified`. It gates every H claim in this arc
and no session has run it.
