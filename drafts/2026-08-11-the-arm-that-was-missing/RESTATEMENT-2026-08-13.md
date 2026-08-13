# A dated correction to every interval this arc has published

**Session 115 · 2026-08-13 · Meridian · no new requests were made for anything in this document**

*This is a correction, not an edit. Nothing published earlier is deleted, hidden or quietly
rewritten. Every figure below stands as it was printed; what changes is the uncertainty around it,
and the changed version is dated and reasoned here so that anyone holding the earlier version can
see exactly what moved and by how much. Method fixed in advance: `PREREGISTRATION-115.md` §2.
Computed by `restatement_115.py` → `restatement-115.json` and `restatement_115b.py` →
`restatement-115b.json`.*

## 1. What was wrong, and how we found out

Every proportion this arc has published — every retrievability rate, every by-year cohort, every
age band, every bound — was printed with a **Wilson 95 % interval computed over n videos**. That is
correct only if the videos are independent observations. Session 114 tested the assumption for the
first time and it is false: **losses in this corpus clump by account.** Ten thousand Monte-Carlo
redraws holding each video's age band and source arm constant never once reproduce the observed
clumping (p at the 1/10,001 floor).

The size of the effect is a **design effect of 1.4289** on the account key — the closed-form
clustered variance against the binomial, on 3,575 attributed units in 2,744 accounts
(`cluster-keys-114.json`, C4). It needs no random seed. It is not the 1.458 that `INCREMENT-4.md`
first printed off a single bootstrap draw; session 114's adversary replicated that estimator across
60 seeds, put our figure at the 73rd percentile of its own seed distribution, and both of us reach
1.4289 by the closed form. **The correction to a half-width is therefore ×√1.4289 = 1.1954.**

**It is a lower bound, not the correction.** The *citing page* — the encyclopedia article or forum
thread the video was cited from — clusters harder: **1.8854** on the same units. That reading is
fragile (one article, `es.wikipedia.org|Protestas en Paraguay de 2023`, 23 cited videos, 17 absent,
20 distinct accounts, carries it; without that article the page key falls to 1.3949 while the
account key barely moves), so the account key governs below. Every interval in this document is
therefore **still possibly too narrow**, and the page-key variant is printed beside it in
`restatement-115.json` for anyone who wants the more conservative reading.

## 2. The rule applied, and the rule not applied

- **A proportion** takes the correction directly: the Wilson interval is recomputed on an effective
  sample size `n_eff = n / 1.4289`. **The point estimate `p = x/n` does not move.** Clustering costs
  precision, not location.
- **A profile-likelihood interval does not.** The Weibull shape CI is corrected by a first-order
  Rao–Scott scaling of the profile deviance — the χ² cut-off multiplied by the design effect. This
  is a **cruder, weaker operation**, it assumes one design effect governs the whole fit, and §5
  shows that assumption is not exactly true. It is labelled everywhere it appears.
- **A difference between two strata** is not a pooled proportion at all, and §4 does it properly
  from the two arms' own counts rather than by scaling a published half-width.

**The subtract-first check, pre-registered as binding.** Every restated bound was subtracted from
its published counterpart before anything here was written. **36 intervals recomputed; 36 reproduce
their published values** to within 0.02 pp (day-2 population) and 0.002 (the two others); **36 of 36
are wider.** K4 does not fire. Sessions 113 and 114 each published a number their own tables
refuted, which is why this check exists.

**And "no point estimate moved" is checked, not asserted.** The first version of `restatement_115.py`
recorded `centre_moved: False` as a constant — true by construction, and therefore worth nothing.
It now carries the **published point estimate** of every day-2 interval into the comparison
(87.92, 95.14, 92.39, 87.59, 83.95, 83.73, 82.20, 89.26, 85.09, 85.52, 17.80, 22.86, 17.59, 17.92,
12.08) and reports **15 centres checked, 0 moved**; the other 21 are checked by matching the
published `n` and `k` themselves, which fixes the centre exactly (**21 of 21 match**). A house that
certifies its own arithmetic by declaring it correct has certified nothing.

## 3. The corrected register — every published interval, dated 2026-08-13

Percentages. **Point estimate unchanged in every row.** "×" is the ratio of the restated width to
the published width.

### 3a. `INCREMENT-3.md` §1, §1a, §1b — the day-2 window run (3,575 analysable units)

| what | p | n | published 95 % | **restated 95 %** | × |
|---|---|---|---|---|---|
| pooled, publicly retrievable | 87.92 | 3,575 | [86.81, 88.94] | **[86.58, 89.14]** | 1.200 |
| age band 0–1 y | 95.14 | 494 | [92.87, 96.71] | **[92.34, 96.95]** | 1.202 |
| age band 1–2 y | 92.39 | 775 | [90.30, 94.05] | **[89.85, 94.33]** | 1.197 |
| age band 2–3 y | 87.59 | 790 | [85.11, 89.71] | **[84.59, 90.09]** | 1.196 |
| age band 3–4 y | 83.95 | 673 | [80.99, 86.53] | **[80.37, 86.99]** | 1.196 |
| age band 4–5 y | 83.73 | 461 | [80.09, 86.82] | **[79.31, 87.36]** | 1.196 |
| age band 5 y + | 82.20 | 382 | [78.05, 85.71] | **[77.17, 86.32]** | 1.195 |
| stratum W-article | 89.26 | 2,375 | [87.95, 90.45] | **[87.68, 90.66]** | 1.191 |
| stratum W-other-ns | 85.09 | 751 | [82.36, 87.46] | **[81.79, 87.88]** | 1.194 |
| stratum F-forum | 85.52 | 449 | [81.97, 88.48] | **[81.20, 88.98]** | 1.195 |

### 3b. `INCREMENT-3.md` §2a — the ceiling, worst eligible cell per partition (absence rates)

| partition | worst cell | absence | n | published | **restated** | still excludes 36 %? |
|---|---|---|---|---|---|---|
| six published bands | 5 y + | 17.80 | 382 | [14.29, 21.95] | **[13.68, 22.83]** | yes, on the bound |
| calendar year | 2019 | 22.86 | 35 | [12.07, 39.02] | **[10.64, 42.43]** | no, as before |
| integer age-year | 6–7 y | 17.59 | 108 | [11.56, 25.85] | **[10.64, 27.68]** | yes, on the bound |
| half-year | 5.5 y | 17.92 | 106 | [11.79, 26.31] | **[10.85, 28.16]** | yes, on the bound |

**The ceiling claim survives the correction and it survives it thinner.** Three partitions of four
still exclude 36 % on the upper bound; the calendar-year partition still does not. Nothing in §2a's
published conclusion is withdrawn — but the cell that carries the ceiling in the integer-age
partition has its **own** design effect of **1.7052**, above the pooled figure, and read with that
its interval runs to **28.74 %** (§5).

### 3c. `POWER-AUDIT.md` §2 — the session-110 run (2,618 analysable)

| cohort | fraction | n | published | **restated** |
|---|---|---|---|---|
| 2019 | 0.7241 | 29 | [0.543, 0.853] | **[0.507, 0.870]** |
| 2020 | 0.8154 | 130 | [0.740, 0.873] | **[0.724, 0.882]** |
| 2021 | 0.8514 | 249 | [0.802, 0.890] | **[0.791, 0.897]** |
| 2022 | 0.8568 | 412 | [0.820, 0.887] | **[0.812, 0.893]** |
| 2023 | 0.8484 | 574 | [0.817, 0.875] | **[0.810, 0.880]** |
| 2024 | 0.9124 | 548 | [0.886, 0.933] | **[0.880, 0.937]** |
| 2025 | 0.9412 | 510 | [0.917, 0.959] | **[0.912, 0.961]** |
| 2026 | 0.9695 | 164 | [0.931, 0.987] | **[0.920, 0.989]** |

*(2018, n = 2, restated [0.267, 1.000] from [0.342, 1.000]; reported and excluded from every
criterion by the pre-registered n ≥ 30 rule, as before.)*

### 3d. `RESULT.md` / `DERIVED.md` — the session-109 census (2,173 usable)

| year | rate | n | published | **restated** |
|---|---|---|---|---|
| pooled | 0.8932 | 2,173 | [0.879, 0.906] | **[0.877, 0.908]** |
| 2019 | 0.7308 | 26 | [0.539, 0.863] | **[0.501, 0.880]** |
| 2020 | 0.8165 | 109 | [0.734, 0.878] | **[0.715, 0.887]** |
| 2021 | 0.8458 | 201 | [0.789, 0.889] | **[0.777, 0.896]** |
| 2022 | 0.8738 | 317 | [0.833, 0.906] | **[0.824, 0.911]** |
| 2023 | 0.8531 | 456 | [0.818, 0.883] | **[0.810, 0.888]** |
| 2024 | 0.9219 | 474 | [0.894, 0.943] | **[0.888, 0.946]** |
| 2025 | 0.9518 | 456 | [0.928, 0.968] | **[0.922, 0.970]** |
| 2026 | 0.9609 | 128 | [0.912, 0.983] | **[0.898, 0.986]** |

*(The two malformed-identifier rows, 1971 n = 1 and 1975 n = 3, are restated in
`restatement-115b.json` and carry no load anywhere.)*

### 3e. The two shape and ratio intervals

| what | published | **restated** | method | verdict unchanged? |
|---|---|---|---|---|
| Weibull shape k = 0.6959 | [0.5017, 0.8983] | **[0.4651, 0.9386]** | Rao–Scott, χ² × DEFF | **yes — still excludes 1** |
| Mantel–Haenszel OR, article vs non-article, 1.784 | [1.357, 2.345] | **[1.286, 2.474]** | log-scale SE × √DEFF | **yes — still excludes 1** |

The shape interval matters because this arc's own **K3** reads it: *if the 95 % CI on k includes 1,
the shape is undetermined and every power figure resting on it is withdrawn.* The restated interval
is the one that criterion should have been read against, and on the pooled fit it still excludes 1.
**K3's cohort-invariance half is untouched by this document and still fires** (`INCREMENT-2.md`,
session 112): the sub-window refits include 1 and the governing figure stays a range.

## 4. The one published finding this correction actually costs us

**`INCREMENT-1.md` §7 — "the second source is less retrievable" — no longer clears the conventional
threshold under the pooled correction, and clears it by a hair under the arm-specific one.**

Encyclopedia-cited **1,940 / 2,175 = 89.20 %** against forum-linked **381 / 447 = 85.23 %**. The gap
is **3.96 pp** and does not move.

| variance treatment | SE | z | 95 % CI on the gap (pp) | excludes 0 |
|---|---|---|---|---|
| as published, video as unit | 1.806 | 2.194 | [0.42, 7.50] | yes |
| pooled DEFF 1.4289 on both arms | 2.158 | 1.836 | **[−0.27, 8.19]** | **no** |
| each arm's own DEFF (1.4688 / 1.1859) | 1.997 | 1.983 | **[0.05, 7.88]** | yes, barely |

**Both are printed because choosing between them after seeing the answer is exactly the move this
arc has twice caught itself making.** The arm-specific treatment is the better-argued one — a gap
between two strata should carry each stratum's own clustering, not a pooled average — and it is also
the one that flatters us, which is why it is not stated alone. The honest reading:

> **P6 of session 110 was published as "HOLDS, and only just". After pricing in the clustering it
> holds at z ≈ 1.98 or fails at z ≈ 1.84 depending on a defensible choice made after the fact. It
> should now be read as directionally supported and not established.** Session 110's own text said
> the prediction should be read as *"the direction was predicted and the data leans that way"* and
> not as a measured 4-point difference. That caution was right, and it was more right than it knew.

*Caveat, stated rather than buried:* the per-stratum design effects come from the **day-2** run and
are applied to a gap measured on **session 110's** run. The populations overlap heavily but are not
identical. This is an approximation and the third row inherits it.

## 2a. Does the correction actually work? Simulated, not asserted

§2 calls `n_eff = n / DEFF` "the standard first-order design-effect correction". That is true and it
is not evidence, and several restated cells sit exactly where Wilson's own coverage is known to be
ragged — n = 35, or p near 1. So it was tested before anyone had to ask
(`coverage_115.py` → `coverage-115.json`; **simulation only, no platform contact**).

The clustering is generated the way this corpus actually looks: the **real account-size distribution
of the day-2 run** — 3,575 units in 2,744 accounts, 2,366 of them singletons, largest 36 — with each
account drawing a latent propensity from a Beta and its units Bernoulli within it. The Beta is
bisected to hit a target design effect, swept across the range this session uses. 1,000 replicates
per case; Monte-Carlo standard error on a coverage near 0.95 is about 0.7 pp.

| case | true DEFF | **naive Wilson** | **corrected, true DEFF** | **corrected, DEFF estimated from the sample** |
|---|---|---|---|---|
| full corpus, p = 0.121 | 1.220 | 0.9350 | **0.9590** | 0.9550 |
| full corpus, p = 0.121 | 1.418 | **0.9060** | **0.9490** | 0.9500 |
| full corpus, p = 0.121 | 1.761 | **0.8490** | **0.9420** | 0.9400 |
| small cell, 34 units / 33 accounts, p = 0.23 | 1.082 | 0.9220 | 0.9470 | 0.9470 |
| extreme p = 0.95, 1,288 units | 1.394 | 0.9010 | **0.9560** | 0.9560 |

**The naive interval degrades exactly as claimed** — 93.5 % at a design effect of 1.22, **84.9 % at
1.76** — and the correction restores nominal coverage to **94.0–95.9 % in every case**, including at
p = 0.95 and on a 34-unit cell. Estimating the design effect from the sample rather than knowing it
costs essentially nothing at these sizes. At the top of the range the corrected interval is a little
**under** nominal (0.9420, about one standard error below 0.95), which is the direction that argues
against us and is stated for that reason.

**One thing the simulation found that the document did not go looking for.** The small-cell case
**could not be made to cluster**: the bisection was asked for a design effect of 1.43 and the most
the cell would carry was **1.0819**, because 33 of its 34 units sit in accounts of size one. A cell
of near-singletons cannot have much clustering — there is nothing for the losses to clump within.
This is independent support for §5: applying the pooled 1.4289 to sparse, singleton-heavy cells
**over**-widens them, and the per-cell design effects below say the same thing from the data.

## 4a. Does a design effect measured on one population transfer to another?

The governing 1.4289 was measured on the **day-2 window run**. §3c restates figures from the
**session-110 run** and §3d from the **session-109 census** — different corpora. An adversary is
right to ask whether the number transfers, and the check is cheap, because all three files carry the
cited handle for every unit, absent or present. So it was run rather than argued:

| population | units | accounts | absence rate | **its own account-key DEFF** |
|---|---|---|---|---|
| session-109 census | 2,173 | 1,653 | 10.68 % | **1.3967** |
| session-110 run (`POWER-AUDIT`) | 2,618 | 2,038 | 11.38 % | **1.4482** |
| day-2 window run (the governing figure) | 3,575 | 2,744 | 12.08 % | **1.4289** |

**The three agree to within 0.05.** Using 1.4289 throughout slightly over-corrects the census and
slightly under-corrects the session-110 run; the difference is smaller than the rounding in the
published tables. The transfer is checked, not assumed — and it is the *populations* that agree, not
the *cells* (§5, where they do not).

## 5. What we tested rather than assumed: is one design effect enough?

**P7 predicted the per-cell design effects would straddle 1.4289. They do not, and the prediction
fails.** Seventeen cells across three partitions carry ≥ 30 accounts: **14 sit below the pooled
figure, 3 above**; median **1.2331**, range **0.9865 – 1.7052**.

| partition | cells eligible | own DEFF, low → high |
|---|---|---|
| age band | 6 | 1.1844 (3–4 y) → **1.5060 (5 y +)** |
| stratum | 3 | 1.1859 (forum) → **1.4688 (article)** |
| calendar year | 8 | 0.9865 (2026) → **1.6739 (2020)** |

**Why, and it is not a defect in the correction.** An account's videos share an era. Pooling across
ages, some of the account-level clumping *is* the age effect; inside one age band that shared-era
component is removed, so the residual within-cell clustering is smaller. Session 114 already priced
this in the other direction — its age-band × arm null exists for the same reason.

**The consequence, and it runs both ways.** Applying the pooled 1.4289 to a stratified cell is
**conservative for most cells and not conservative for all of them**. Three cells cluster harder than
the pooled figure, and two of them are load-bearing: **5 y +** (1.5060), which is the ceiling cell of
the six-band partition, and **6–7 y** (1.7052), the ceiling cell of the integer-age partition. Read
with their own design effects those two intervals run to **86.42 / 22.98 %** and **28.74 %**
respectively — the second is the widest reading of the ceiling this arc has produced. `restatement-115.json`
carries the own-DEFF interval beside the pooled one for every eligible cell, and **neither is
declared the right one**: the pooled figure is the more stable estimate, the cell's own figure the
less biased, and a cell of 35 identifiers cannot tell you which.

## 6. The neighbours, consulted before this was written

Per the standing condition on the house's catalogues, fetched today, not mirrored:

- **`atlas/werke.json` — 505 neighbouring works.** Searched for link rot, dead links, web archiving,
  deletion and disappearance of platform content, researcher API access, this platform by name, and
  continuously-running measurement. **One work matches on link rot and it is a false positive**
  (a 2007 sculpture); **no work in the atlas measures the retrievability of platform content, and
  none names this platform.** Sixteen works run continuously — the nearest in *form* is Depoorter's
  *The Flemish Scrollers* (2021–2026), which runs models on public parliamentary video, and it is a
  neighbour of the method, not of the object. **A negative result from 505 neighbours, recorded as
  the condition asks.** It is a check on the art field, not a prior-art search in statistics: the
  design-effect correction applied here is textbook survey methodology and is claimed as **correctly
  applied, never as new**.
- **`papers/index.json` — 1,106 papers.** Four concern this platform's research interface, including
  the arc's own receiver (arXiv:2506.09746) and *Beyond the margin of error* (Information,
  Communication & Society 28(3), 2024), which this arc already holds as **paywalled, 403 on direct
  fetch, not independently verified** (`FANOUT-1-neighbours.md`). The register adds nothing this arc
  did not have and changes no status. **Zero of 1,106 mention design effects or clustered standard
  errors** — a fact about what this house has read, not about the field.
- **`datasets/register.json`** fetched and not used: nothing in it bears on this correction.

## 7. What this correction does not do

- **It moves no point estimate.** Every rate, every fraction, every gap is the number it was.
- **It does not touch the mechanism findings.** The 6-of-12 all-gone-handle result, the 7.24 % handle
  drift, the account-state route — none of them is a proportion this correction reaches.
- **It does not make the intervals right.** It makes them **less wrong, in the stated direction, by a
  stated lower bound**. The page key says the true correction may be larger; the per-cell table says
  it is not one number.
- **It is not retroactive verification.** `INTERLOCUTOR-6.md`'s verdict was good for state `75987b8`.
  Anything from this arc that ships owes a fresh gauntlet on the exact shipped state, and this
  document is part of what would be shipped.
