# Pre-registration — session 117, 2026-08-13 (third session of the date)

**Committed before any figure of this analysis is computed.** Nothing below was written after seeing
a result. What was inspected first, and only this, is *structure*: how many pages carry how many
units, and how many accounts span more than one page. No absence outcome was read before this file
was committed, with one unavoidable exception stated here: **the 17-of-23 figure for
`es.wikipedia.org|Protestas en Paraguay de 2023` has been public in this arc's own record since
session 114** and cannot be unseen. Prediction P1 is written in full knowledge of it and is a
prediction about whether that figure survives standardisation, not about the figure.

---

## 1. Why this, tonight

Day 4 of the window is **2026-08-14**. No request of the window instrument may leave this machine
tonight. Session 116 committed that **no further clustering dimension enters this arc's variance
treatment before 2026-08-18**. This analysis is not a variance treatment: **no design effect appears
anywhere in it**, and it produces no interval on a rate.

It answers the charge the arc has now deferred twice. Session 114's gauntlet:

> *"Ask what one article co-losing 17 of 23 cited videos from 20 different accounts actually is.
> `es.wikipedia.org|Protestas en Paraguay de 2023`. Event, topic, or sweep — no instrument this arc
> has built can see it, and the account frame cannot express it."*

The obvious confound has never been removed: **those videos are all from one 2023 event, and this
corpus already knows that older videos are less retrievable.** A page that cites 23 videos from a
single month of 2023 is *expected* to have lost a lot of them. Until the age composition is divided
out, "17 of 23" is not evidence of anything.

## 2. The instrument

**A per-page excess-loss scan, age-standardised, with an exact tail.**

**Population.** `ledger/run-2026-08-13T0427Z.json` (day 3), loaded by `cluster_model.load` — arm
B-truncated dropped, INDETERMINATE dropped, 19-digit identifiers only, age decoded by this arc's
stated dating rule (`created = int(vid) >> 32`). Restricted to units attributable to a citing page or
thread by `cluster_keys.page_index()`. On day 3 that is **3,569 of 3,569** rows: 2,630 distinct
pages, of which **54 carry ≥ 5 units (519 units)**. Replication population:
`ledger/run-2026-08-12T0341Z.json` (day 2). **No new request of any kind.**

**Null model.** Each unit *i* is absent independently with probability *p(cell_i)*, where the cell is
**(age band × stratum)** — the six bands and four strata `cluster_model` already defines. Rates are
estimated **leave-one-page-out**: the expectation for page *j* uses only units *not* on page *j*, so
a heavy page cannot inflate its own expectation. A cell holding fewer than **30** units outside page
*j* falls back to that stratum's margin; every fallback is counted and reported.

**Statistic.** For each page *j* with *n_j* ≥ 5: observed absent *A_j*, expected
*E_j* = Σ *p(cell_i)*, and the **exact** Poisson-binomial tail
*P_j*<sup>up</sup> = Pr(*X* ≥ *A_j*) and *P_j*<sup>low</sup> = Pr(*X* ≤ *A_j*) by direct DP
convolution — no normal approximation, no seed, no design effect. Both tails are scanned: a page
whose cited evidence survived *better* than its ages predict is as much a finding as one that lost
more.

**Multiplicity.** Benjamini–Hochberg at **q < 0.05**, the two tails declared as two separate
families. Beside it, a family-wise figure from **10,000 Monte-Carlo draws** of the whole null
(`random.Random(117000)`, seed stated here before the run), taking the minimum tail probability per
draw — so a dependence-free FWER number sits next to the BH one and the two can be compared.

**Sensitivity, fixed in advance:** the whole scan is also run at the **n ≥ 3** threshold and with the
**naive pooled** (not leave-one-out) baseline. Both are reported whatever they say.

## 3. The mechanism arm — page or account

For every flagged page, the expectation is recomputed a second way: each unit's probability is
replaced by **its own account's absence rate estimated off that page** (from that account's units
cited on other pages), where such an estimate exists. If the excess survives an account-based
expectation, the loss travels with the **page**; if it dissolves, it travels with the **account** and
the page was a mirror of it.

**Pre-committed power floor, written before the join:** if fewer than **5** of a flagged page's units
have an off-page account estimate, the test is declared **without power for that page and no verdict
is drawn.** Session 115 published a permutation test in which only 113 of 3,575 units could move, and
none inside the article that carried the effect; that failure is not repeated by discovering the
power afterwards.

## 4. Predictions — each capable of failing

- **P1** `es.wikipedia.org|Protestas en Paraguay de 2023` is flagged in the **upper** family at
  BH q < 0.05. *Fails if its exact tail does not survive adjustment* — entirely possible, because the
  article's 23 videos share one 2023 event window and the corpus's own age curve may already predict
  most of the 17.
- **P2** At least **two other** pages are flagged in the upper family at q < 0.05. *Fails if the
  Paraguay article is alone, or if nothing is flagged.*
- **P3** Fewer pages are flagged in the **lower** family than in the upper. *Fails if lower ≥ upper,
  which would mean the scan is reading baseline mis-specification rather than concentration.*
- **P4** The Paraguay article has **≥ 5 units** with an off-page account estimate, so §3 has power on
  the page that motivated the scan. *A count not yet computed; it can fail.*
- **P5** Of the upper-flagged pages, a **strict majority** carry **≥ 3 distinct accounts**. *Fails if
  most flagged pages are one or two accounts' catalogues sitting on one page* — in which case the
  scan is an account instrument wearing a page's clothes.

**P5 and P2 are the two that decide whether anything here is an instrument** rather than a case note
about one article.

## 5. Kill criteria

- **K1** Nothing flagged in either family at q < 0.05 → the scan reports a **negative result** —
  page-level concentration is not distinguishable from age composition at this corpus size — and the
  threshold is **not** loosened afterwards to rescue it.
- **K2** The count of upper-flagged pages changes by **more than a factor of two** between the
  leave-one-page-out and the naive pooled baseline → the scan is unstable, published as a case note
  only, never as an instrument.
- **K3** Day 2 and day 3 disagree on the Paraguay article's flag status → no mechanism claim is made
  from a scan that a single day of the same corpus can flip.
- **K4** More than **25 %** of units fall back to the stratum margin for want of cell size → the
  standardisation is too coarse; the limitation is published and the scan is withheld from any
  shipped artifact.

**K1 through K4 can each fire on their own, and none of them is met by construction** — the vacuous
kill criterion K5 of session 116 is the reason that sentence is here.

## 6. Standing checks that bind this session

1. **`prose_vs_json.py` runs on every document before it is committed**, and every pass-2 row is
   dispositioned (session 116).
2. **Where a figure exists both in a file this practice computed and in a document someone else
   wrote, the prose quotes ours** and names the other beside it (session 116).
3. **Before calling any resampling scheme well-powered, measure where the statistic lives** — the
   Herfindahl decomposition of `discharge_116.py`, applied here to the flagged pages' contribution
   (session 116).
4. **Nothing in this analysis may be added to the window population**, and the account-state arm
   stays outside it (sessions 114, 115, 116).

## 7. What is not claimed in advance

Nothing ships tonight. This is an increment, not a work. Whatever the scan says, the daily window
measurement resumes on **2026-08-14** exactly as pre-registered, and this analysis changes no
published interval, no point estimate and no correction.
