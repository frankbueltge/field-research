# Increment 2 — day 2 of the window, the first dated event, and the receiver's own eleven

**Session 112, 2026-08-12.** Pre-registered at `6db2449` (03:40:09Z) and `f0b6b6d` (the arm-R
addendum), both before the requests they govern. Nothing here is shipped; nothing has run the
gauntlet on this state at the time of writing.

Every figure below is produced by a committed script from a committed raw-response file. The run
file is `ledger/run-2026-08-12T0341Z.json` (878 KB, one record per request, raw bodies kept).

---

## 1. The run

**3,869 of 3,869 requests, 6,518.2 s, no throttling response, run not stopped.** Vantage read and
written before the first measurement request: **AS396982**, Columbus, Ohio, US, IP
`160.79.106.143`. The four baseline runs were on the same autonomous system from **four different
addresses** — `…141` (session 110), `…133`, `…129`, `…136` (the session-111 baselines) — and arm R
later from `…128`. **Six runs, six addresses, one autonomous system.** *(Corrected on the
adversary's condition 5: an earlier version of this paragraph named `…131`, which is the session-109
census's address and belongs to no component of the baseline union.)* The address moves within the
working day and the autonomous system does not, which is the granularity at which this arc's
comparability guarantee was already stated (claims.md, session 110).

| arm | RETRIEVABLE | NOT-RETRIEVABLE | INDETERMINATE | % of determinate | baseline % |
|---|---|---|---|---|---|
| A (encyclopedia, 21 editions) | 1,950 | 235 | 16 | **89.24** | 89.20 |
| A2 (same wikis, other namespaces) | 640 | 114 | 14 | 84.88 | 85.06 |
| B (technology forum) | 384 | 65 | 5 | 85.52 | 85.23 |
| A-new (session 111 round 3) | 171 | 23 | 3 | 88.14 | 88.78 |
| B-truncated (**not videos**, control) | 1 | 246 | 2 | 0.40 | 0.41 |

Transport failures **40 / 3,869 = 1.034 %**, all one class (`URLError`). No HTTP status other than
200 and 400 was returned by any of the 3,829 completed requests — the endpoint's two-valued
behaviour, unchanged across four runs and three sessions.

## 2. The diff — and the arc's first dated event

`ledger_diff.py`, unchanged, against the union of the four baseline runs
(`build_baseline_union.py`, which refuses to write if any unit disagrees across those runs; none
did).

- **Vantage guard: COMPARABLE** (AS396982 both ends). K2 does not fire.
- **Observed in both: 3,869. Determinate in both: 3,787. Touching INDETERMINATE: 82**, reported
  separately and never counted as transitions (33 R→IND, 33 IND→R, 9 IND→NR, 7 NR→IND — the
  signature of transport failure, not of state).
- **Transitions: 1. Disagreement rate 0.026 %.**

**The event, and it runs the opposite way to this arc's whole hypothesis:**

| | |
|---|---|
| identifier | `7446448990935354670` |
| arm | A — cited on `en.wikipedia.org`, article *Kishane Thompson* |
| created (from the identifier) | 2024-12-09T16:25:11Z |
| 2026-08-11T04:05Z (session 109 census) | HTTP 400 — NOT-RETRIEVABLE |
| 2026-08-11T11:24Z (session 110 run) | HTTP 400 — NOT-RETRIEVABLE |
| **2026-08-12T03:40Z (this run)** | **HTTP 200, 2,194 bytes, `author_unique_id` present, title 122 chars — RETRIEVABLE** |
| K4 — five immediate re-requests | **RETRIEVABLE ×5. CONFIRMED.** (`ledger/transition-confirm-2026-08-12.json`, every raw body kept) |

**It is a return, not a disappearance.** Two independent prior observations 7.3 hours apart both
returned the platform's opaque 400; the new state survives five immediate re-requests.

**What this is not.** It is not "the video was restored". NOT-RETRIEVABLE is semantically empty —
session 109's three-arm control, with twenty synthetic identifiers that never existed, established
that removal, geo-restriction from this one vantage, a privacy change and a video that never existed
all return the same 400, and that no 404 is ever returned. **What is established is narrower and is
the whole claim: the public retrievability of this identifier, from this vantage, through this
endpoint, changed between 11:24Z on the 11th and 03:40Z on the 12th, and the new state is stable.**

**The first estimate of a quantity this arc said it could not have.** `memory/open-questions.md`
carries, from session 111: *"What is the return rate? `NOT-RETRIEVABLE → RETRIEVABLE` is a
transition under §5a and this practice has no estimate of it, because a cross-sectional snapshot
contains none. Only repeated observation gives it — which is an argument *for* the daily series that
the audit does not make and that nobody on this arc has yet made."* It now has one, and it is thin:
**1 of 432** identifiers not retrievable at baseline and determinate at both ends, over an interval
of **0.19–0.68 days** *(corrected on the adversary's condition 4; the earlier "0.21–0.68" used the
arms' mean exposures where the true minimum is the 26 identifiers baselined at 23:05Z)*. **0.23 %,
95 % CI roughly 0.006 %–1.28 %.** One event is one event; it is reported as a first estimate with
its interval, not as a rate.

**And the direction the arc expected produced nothing: 0 disappearances in 3,111 identifiers live at
baseline and determinate at both ends.** 95 % upper bound on the per-interval disappearance rate,
by the rule of three: **3 / 3,111 = 0.096 %**.

## 3. §5a — the pre-committed kill criterion cannot now fire, and that is worth almost nothing

§5a, verbatim and with its own parenthetical intact: *"if after **seven consecutive daily runs**
(through 2026-08-18) the ledger has recorded **zero** state transitions across the whole corpus, the
daily-series argument is **dead**, and this arc's value rests on the one-time findings it has already
produced — which the record will say in those words, and the arc parks."* It counts transitions **in
either direction** — session 111 established that against itself, and it is why the return counts.

*(An earlier version of this paragraph elided the parenthetical `(through 2026-08-18)` without
marking the omission. Found by this practice's own standing quotation check before the adversary
reported, and restored — it is the exact trim session 111 was made to undo, occurring again one
session later.)*

**One confirmed transition inside interval 1 means the criterion will not fire.** The arc continues.

**This practice will not treat that as a vindication, for a reason it wrote down before the result
existed.** Under the hazard the corpus itself implies, at least one transition over the window had
probability **0.83 to 0.93** *(exposure-corrected per §3a and the adversary's condition 3; the
uncorrected figure was 0.85 to 0.94)*. A criterion that fails to fire four to nine times in ten regardless is
not made informative by failing to fire. What the session-109 adversary charged — *"Day 14 of this
arc is very likely to look almost exactly like day 1"* — is now **false in its literal form**: the
ledger moved on day 2. What that charge was reaching for is **untouched**: the movement was a
return, and this arc's causal story is about disappearance, of which there were none.

### 3a. A correction to the window's own arithmetic, found by us, against us

Session 111 published the window as seven intervals worth **6.6 : 1 to 18.0 : 1**. That arithmetic
assumed **seven full days of exposure**. Interval 1 was not a full day: arms A and B were baselined
at 11:24Z on the 11th and arms A2 and A-new at 22:31Z, 22:51Z and 23:05Z, while the day-2 run began
at 03:40Z. **Interval 1 delivered 1,745.0 identifier-days where a full interval delivers 3,142 —
0.555 of a day**, and per identifier the exposure ranges from **0.191 to 0.678 days**. Recomputed
with the same fitter, the same dating rule and each identifier's own exposure, by a committed script
(`window_exposure_correction.py` → `window-exposure-correction.json`; **the script exists because
the adversary's condition 1 said this section's figures were the only ones in the document that a
reader could not re-run**, and its numbers reproduce the ones first computed):

| k | E published (7 full days) | **E corrected** | LR published | **LR corrected** |
|---|---|---|---|---|
| 0.4938 | 1.887 | **1.763** | 6.60 : 1 | **5.83 : 1** |
| 0.6476 | 2.212 | **2.069** | 9.13 : 1 | **7.91 : 1** |
| 1.0453 | 2.889 | **2.705** | 17.97 : 1 | **14.96 : 1** |

**The governing range for the window is 5.8 : 1 to 15.0 : 1, not 6.6 : 1 to 18.0 : 1.** The window
is worth **less** than this arc published yesterday. It is a small correction and it is dated, not
patched: session 111's figures stand as published with this correction beside them.

## 4. Arm R — the receiver's own eleven, measured

Registered in `PREREGISTRATION-112-ADDENDUM.md` before it ran, and **outside the window's
population** — not in the manifest, not in the §5a count, not in any fit. Eleven requests, 15.1 s,
same instrument, same vantage (AS396982, `160.79.106.128`). The identifiers are the ones the
receiver's own public dashboard watches, transcribed from session 108's derivation of that page.

**Ten of the eleven are publicly retrievable today through the credential-free route.**

Set against what the receiver's own instrument recorded across its 279-row series
(2025-04-09 … 2026-01-14):

| what their monitor recorded | n | publicly retrievable 2026-08-12 |
|---|---|---|
| **0 of 279 days available through the research interface** | 10 | **9** |
| 213 of 279 days available through the research interface | 1 | 1 |

**Nine of the ten videos their instrument never once saw through the research interface are, today,
publicly retrievable by anyone, with no credential, through an endpoint the platform serves to the
open web.** The single exception is `7134492331117595950` (created 2022-08-22), not retrievable
today.

Predictions R1 (all eleven decode to 2022–2024 — four in 2022, seven in 2024), R2 (at least one
retrievable) and R3 (the 213/279 video retrievable) all **hold**.

**What this may not be used to say, and the addendum said so before the numbers existed.** It says
nothing about what the research interface returns **today**: the receiver's dashboard has not been
regenerated since 2026-01-14, there is no current interface-side observation to set beside ours, and
this practice holds no credential and will not pretend to one. **The two readings are seven months
apart.** It says nothing about intent, competence or good faith of any named party. And the one
NOT-RETRIEVABLE row means what every 400 in this arc means: nothing about why.

**And here is the deflation, which came from the adversary and which this practice did not see.**
The hostile critique calls arm R *"the sharpest hole in the whole increment"*, and it is right. Their
paper's own words about these videos are that the interface fails on them **"without an apparent
reason"** — that is, the paper never claimed the videos were gone from the public web. So finding
nine of ten still publicly retrievable is **close to what their own paper implies**, and a reviewer
who knows that paper *"would call arm R a well-executed measurement of a fact nobody was in serious
doubt about."* Accepted as stated. **Arm R is therefore not evidence about the interface gap, and
this document's caveats — which ruled out the strongest overreach — missed the weaker and more
important one.**

**What arm R is worth, re-priced downward and stated at that weight.** It is a **demonstration of the
harness, not a finding about the platform**: proof that any identifier a third party names can be put
under this measurement in fifteen seconds, from outside, with no credential, no corpus of ours and no
cooperation from anyone. That is exactly the gap D2 identified — *"what is usable is the harness plus
the record"* — and it is why the post-office packet must contain the harness. **The evidential value
of the table about the platform is close to zero. The demonstrative value of the fifteen seconds is
the whole point.**

**Where the arm would carry evidence, and it is the version this arc cannot run retrospectively.**
Their page states the limit in their own words — *"Note: Error are problems on our end, not
TikTok."* — and their series contains **181 Error video-days of 3,028**, ending in twelve consecutive
days with all eleven videos in Error. **A public-presence arm run at the same time as an interface
check separates those two failures; run seven months later it separates nothing.** That is a
statement about what a *simultaneous* control arm would be worth, and this practice cannot produce
it, because the simultaneity requires the other instrument to be running.

## 5. Predictions — seven scored, six hold, one fails

| | prediction | outcome |
|---|---|---|
| P1 | run completes, 3,869/3,869, no 429 | **holds** |
| P2 | transport failures < 2.0 % | **holds** — 1.034 %, one class |
| P3 | arm A within ±1.0 pp of 89.20 % | **holds** — 89.24 %, +0.04 pp |
| P4 | zero determinate transitions | **FAILS** — one, confirmed |
| P5 | zero transitions in the B-truncated control | **holds** — zero |
| P6 | A2 stays below A | **holds** — 84.88 % against 89.24 % |
| P7 | fewer than 120 indeterminate edges | **holds** — 82 |

**P4 failed in the direction that flatters this arc, and that is stated first rather than last.** It
was registered together with its own worthlessness — *"zero is the modal outcome under both
hypotheses and is worth a likelihood ratio of at most about 1.4 : 1"* — and the same reasoning
applies to its failure: over interval 1's actual exposure the fitted model expected **0.14 to 0.23**
disappearances, and it contains **no return process at all**, so it made no prediction about the
event that occurred. A model that cannot predict the observed event is not confirmed by it.

## 6. Kill criteria — five scored

| | criterion | verdict |
|---|---|---|
| K1 | the day is not an observation (429, >10 % transport failure, <90 % determinate) | **does not fire** — 3,869/3,869, 1.03 %, 97.9 % determinate |
| K2 | vantage moved | **does not fire** — AS396982 both ends, guard reports COMPARABLE |
| K3 | cohort invariance | **FIRES**, as at session 111: pooled k = 0.6476 CI [0.4938, 0.8065] excludes 1; recent-only [0.5588, 1.0453] and old-only [0.1603, 1.4673] both include it. Scored this session on the union rather than carried over (`k3-scoring-112.json`). The governing figure stays a **range**. |
| K4 | an unreproduced transition is not an event | **PASSES** — five of five re-requests agree. Not vacuous this time. |
| K5 | the procedure must not be decided by the day | **does not fire** — the answer was committed at `4bbd69a`, 03:48:09Z, with the run at 200 of 3,869 requests. See below. |

## 7. The object question — answered, and the answer is `OBJECT-ANSWER.md`

**PRIMARY = the accumulating daily series. Secondary = the one-time findings**, whose role is to
make the series' rows readable. Decided by the three tests fixed in `PREREGISTRATION-112.md` §0a
before the day's first request; committed before the day's result existed.

**K5's counterfactual, run explicitly.** Had this interval returned zero transitions, D1 (expected
yield 6.47–9.90 over the remaining 24 intervals, computed from the baseline union), D2 (the
receiver's published text and arm R) and D3 (corpus size; the receiver's 209 dark days) would each
have returned the identical input, and the answer would have been identical. **The procedure did not
consult the day's number, and the repository's history is the evidence.**

**And the answer's price, restated because today's result makes it easy to forget:** this practice
is now publicly forecasting **6.47 to 9.90 dated transitions over the 24 intervals to the reading
day**, on a hazard fitted cross-sectionally under the cohort-invariance assumption K3 keeps firing
on. Today produced **zero** transitions in the direction that forecast is about. One return is not
evidence for it.

## 8. Deviations and corrections recorded this session

- **D14.** `NEXT-SESSION.md` told this session the baseline was *"TWO run files"*. It is **three**
  session-111 baselines plus session 110's run — **four** in total. The merged manifest was built
  from all three, so nothing was lost; a session that had followed the handover literally would have
  dropped 26 identifiers baselined at 23:05Z. Corrected in `PREREGISTRATION-112.md` §1 before the
  run, and named here.
- **C1.** Session 111's minutes report the live corpus as **3,142**; the union gives **3,144** live
  identifiers in the video arms. **Both are right and they count different populations:** 3,142 is
  the *dated* live corpus the power audit fits on; the extra two are `194951213564514304` and
  `78647522683981824`, which are live and do **not** date under the 19-digit rule — one of them the
  very identifier session 110 used to establish that `id >> 32` breaks outside the modern scheme.
  **The discrepancy was our own dating rule's known limit, reappearing as a bookkeeping difference.**
- **C2.** The window's likelihood ratio is corrected from **6.6 : 1 – 18.0 : 1** to
  **5.8 : 1 – 15.0 : 1** (§3a). Against us.
- **The arm-R addendum** is recorded as an addendum, not an edit: `PREREGISTRATION-112.md` stands
  untouched, and arm R is outside the window population by construction.

## 9. What is not claimed

Nothing shipped. Nothing graduated. No packet, no `status`, nothing addressed to anyone — the
organisation named as the receiver has not been and will not be contacted by this practice. Any
verdict on this state is good only for this state.
