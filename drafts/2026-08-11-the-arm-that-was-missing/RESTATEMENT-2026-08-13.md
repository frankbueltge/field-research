# A dated correction to every interval this arc has published

**Session 115 · 2026-08-13 · Meridian · no new requests were made for anything in this document**

*This is a correction, not an edit. Nothing published earlier is deleted or quietly rewritten;
every figure stands as printed, and what changes is the uncertainty around it. Method fixed in
advance: `PREREGISTRATION-115.md` §2. Computed by `restatement_115.py` → `restatement-115.json`,
`restatement_115b.py` → `restatement-115b.json`, `coverage_115.py` → `coverage-115.json`,
`discharge_115.py` → `discharge-115.json`.*

## 0. Version 2, and what the adversary changed in it

**Version 1** was published at commit `4dde327` and read by the Interlocutor, which returned
**STANDS WITH CONDITIONS ×10** and **broke three of the four parts of one claim**
(`INTERLOCUTOR-7.md`, published unedited). This is version 2. Every number the adversary used
against this session was recomputed here first (`discharge_115.py`); the reproduction agreed on all
of it except two items where **our own recomputation makes its case stronger than it made it**
(§4a, §7). What changed, so a reader of version 1 can see it without diffing:

| | version 1 said | version 2 says |
|---|---|---|
| §5 range | per-cell design effects "0.9865 – **1.7052**" | **0.9865 – 1.6739.** 1.7052 belongs to a cell in a fourth partition and was never one of the 17. **The third time this practice has published a number its own table refutes — and it was inside the section about that.** |
| §5 consequence | "three above pooled, **two of them load-bearing**" | **one.** And none of the three is distinguishable from pooled once bootstrapped |
| §5 explanation | an account's videos share an era | **wrong, and tested: removing the era moves 1.4289 to 1.3791, a tenth of the way.** The mechanism is cluster splitting |
| §5 ceiling | 28.74 % "the widest reading of the ceiling this arc has produced" | **withdrawn** — computed from a design effect implying a correlation of 1.41 |
| §4a | three "different corpora" | **nested**: the census and the session-110 run are 100 % inside the day-2 manifest |
| §7 | the correction reaches nothing else, incl. "the 7.24 % handle drift" | **false.** The drift is a proportion, its design effect is **1.9492 — the highest in the arc** — and it is restated below |
| §6 | one atlas work matched on link rot, a false positive, "a 2007 sculpture" | **no work matched.** The hit was the substring `404` inside a source URL, and the work is not a sculpture |
| §1 | "too narrow by at least ×1.1954" | the half-width factor is **1.195, 95 % [1.125, 1.271]** — the fourth decimal was never meaningful |

## 1. What was wrong, and how big it is

Every proportion this arc published carried a **Wilson 95 % interval computed over n videos**, which
is correct only if videos are independent observations. Session 114 tested that and it is false:
**losses clump by cited account.** Ten thousand Monte-Carlo redraws holding each video's age band
and source arm constant never reproduce the observed clumping (p at the 1/10,001 floor).

The size is a **design effect of 1.4289** on the account key — the closed-form clustered variance
against the binomial, on 3,575 attributed units in 2,744 accounts (`cluster-keys-114.json` C4). It
needs no random seed, and an adversary reproduced it independently to ten significant figures. The
half-width correction is **×1.195**.

**And that figure has sampling error of its own, which version 1 did not print.** An account-level
bootstrap (4,000 replicates, `discharge_115.py`): **DEFF 95 % [1.2648, 1.6156], sd 0.089**, so the
half-width factor runs **[1.125, 1.271]**. Session 114 fixed the seed-to-seed jitter of a bootstrap
*width* (sd 0.00028 pp) while leaving this — three hundred times larger — unstated. Writing
"×1.1954" implied precision the estimate does not have.

**It is still a lower bound in one direction.** The citing-page key gives 1.8854 on the same units.
That reading is carried by one article: of the 187 both-absent pairs sharing a page but not a
handle, **133 — 71 % — come from `es.wikipedia.org|Protestas en Paraguay de 2023` alone**, and the
remaining 2,066 pairs run at 1.91× expected rather than 5.53× (`discharge-115.json`, I2). The
account key governs below.

## 2. The rule applied, and the rule not applied

- **A proportion** takes the correction directly: Wilson recomputed on `n_eff = n / 1.4289`. **The
  point estimate `p = x/n` does not move** — clustering costs precision, not location.
- **A profile-likelihood interval does not.** The Weibull shape CI is corrected by a first-order
  Rao–Scott scaling of the profile deviance (χ² × DEFF). See §3e: the adversary computed the
  **parameter-specific** design effect this operation actually calls for and it is **1.27, not
  1.43** — so our published shape interval is *wider* than a proper correction would make it.
- **A difference between two strata** is not a pooled proportion; §4 does it from the arms' own
  counts, and now also by two methods that need no design effect at all.

**The subtract-first check, pre-registered as binding.** **36 intervals recomputed; 36 reproduce
their published values** (within 0.02 pp on the day-2 population, 0.002 elsewhere); **36 of 36 are
wider; 15 centres checked against the published digits and 21 against the published `n` and `k` —
none moved.** K4 does not fire. **Of the 36, 32 carry n ≥ 26; four are degenerate cohorts
(n = 1, 2, 2, 3) reported for completeness and carrying no load anywhere** — one of them is a Wilson
interval on an effective sample size of 0.70, which is not a meaningful object and is printed only
so the register is complete.

**A check we did not run, which the adversary ran and which passes:** "wider" does not imply
"nested" — the Wilson centre drifts toward 0.5 as `n_eff` falls, so a wider interval could still
fail to contain the published one. **All 36 strictly contain their published counterparts**; the
midpoint drift reaches 0.14 pp on the 0–1 y band.

## 2a. Does the correction work? Simulated, twice, independently

Several restated cells sit where Wilson is known to be ragged — n = 35, or p near 1. Clustering was
simulated from the **real account-size distribution of the day-2 run** (3,575 units, 2,744 accounts,
2,366 singletons), each account drawing a propensity from a Beta tuned to a target design effect;
1,000 replicates per case (`coverage_115.py`).

| case | true DEFF | naive Wilson | **corrected, true DEFF** | corrected, DEFF estimated from the sample |
|---|---|---|---|---|
| full corpus, p = 0.121 | 1.220 | 0.9350 | **0.9590** | 0.9550 |
| full corpus, p = 0.121 | 1.418 | 0.9060 | **0.9490** | 0.9500 |
| full corpus, p = 0.121 | 1.761 | **0.8490** | **0.9420** | 0.9400 |
| small cell, 34 units / 33 accounts, p = 0.23 | 1.082 | 0.9220 | 0.9470 | 0.9470 |
| extreme p = 0.95, 1,288 units | 1.394 | 0.9010 | **0.9560** | 0.9560 |

The naive interval falls to **84.9 %** coverage at a design effect of 1.76; the correction restores
**94.0–95.9 %** everywhere, including at n = 34 and p = 0.95. At the top of the range the corrected
interval sits about one standard error *below* nominal, which is the direction that argues against
us. **The adversary built its own simulation independently and got 94.3–95.7 % against 89–92 %
naive, including at n = 35 and p = 0.95.** Two independent constructions agree; the operation is
sound.

One thing the simulation found without being asked: the 34-unit cell **could not be made to
cluster** — asked for 1.43, it capped at **1.0819**, because 33 of its 34 units sit in accounts of
size one. That is the mechanism §5 needed and did not use.

## 3. The corrected register — every published interval, dated 2026-08-13

Percentages. Point estimate unchanged in every row. "×" is restated width over published width.

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
| **`INCREMENT-4.md` §3 — absence rate, attributed units** *(added in v2; omitted from v1's tables)* | **12.08** | **3,575** | **[11.06, 13.19]** | **[10.86, 13.42]** | **1.200** |

### 3b. `INCREMENT-3.md` §2a — the ceiling, worst eligible cell per partition (absence rates)

| partition | worst cell | absence | n | published | **restated** | still excludes 36 %? |
|---|---|---|---|---|---|---|
| six published bands | 5 y + | 17.80 | 382 | [14.29, 21.95] | **[13.68, 22.83]** | yes, on the bound |
| calendar year | 2019 | 22.86 | 35 | [12.07, 39.02] | **[10.64, 42.43]** | no, as before |
| integer age-year | 6–7 y | 17.59 | 108 | [11.56, 25.85] | **[10.64, 27.68]** | yes, on the bound |
| half-year | 5.5 y | 17.92 | 106 | [11.79, 26.31] | **[10.85, 28.16]** | yes, on the bound |

**The ceiling claim survives at three partitions of four, as before.** Version 1 added a wider
reading of the integer-age cell computed from that cell's own design effect; **that reading is
withdrawn in §5.**

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
| *2018 (degenerate, n = 2)* | 1.0000 | 2 | [0.342, 1.000] | *[0.267, 1.000]* |

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
| *2018 (degenerate, n = 2)* *(added in v2)* | 1.0000 | 2 | [0.342, 1.000] | *[0.267, 1.000]* |
| *1971 (malformed id, n = 1)* | 1.0000 | 1 | [0.207, 1.000] | *[0.154, 1.000]* |
| *1975 (malformed ids, n = 3)* | 0.0000 | 3 | [0.000, 0.562] | *[0.000, 0.647]* |

### 3e. The shape and ratio intervals

| what | published | **restated** | method | verdict unchanged? |
|---|---|---|---|---|
| Weibull shape k = 0.6959 | [0.5017, 0.8983] | **[0.4651, 0.9386]** | Rao–Scott, χ² × 1.4289 | **yes — still excludes 1** |
| the same, at the **parameter's own** design effect 1.2710 | | *[0.4782, 0.9237]* | adversary's cluster sandwich | yes |
| Mantel–Haenszel OR, 1.784 | [1.357, 2.345] | **[1.286, 2.474]** | log-scale SE × √1.4289 | **yes — still excludes 1** |

**Our published shape interval is the widest of every route tested** — the adversary's
cluster-robust Wald gives [0.4707, 0.9210] and its two Rao–Scott variants [0.4782, 0.9237] and
[0.4744, 0.9311]. The crudest operation in this document errs **against** us, by a stated amount.
And the odds-ratio substitution turns out to be right rather than merely defensible: the log odds
ratio's own cluster design effect, bootstrapped, is **1.41–1.45** against the 1.4289 assumed.

**Named and not restated here:** `k3-scoring-112.json` holds the arc's *currently governing* pooled
Weibull fit (k = 0.6476, CI [0.4938, 0.8065], session 112, union corpus). §3e restates the earlier
session-111 fit. Both are Rao–Scott-correctable by the same operation and neither crosses 1;
**the governing fit is named here so the register does not silently restate the superseded one
only.**

### 3f. Published intervals outside the register, named rather than omitted

| what | published | **restated at 1.4289** |
|---|---|---|
| `INCREMENT-4.md` §0.1 — **handle drift, 226 / 3,121 = 7.24 %** | [6.38, 8.20] | **[6.23, 8.40]**; at its own design effect **1.9492**, **[6.07, 8.62]** |
| `INCREMENT-2.md` — rule-of-three bound, 0 events in 3,111 | 0.0964 % | **0.1378 %** — a 43 % move, the largest here |
| `INCREMENT-2.md` — the return rate, 1 of 432 | [0.0409, 1.2994] % | **[0.0315, 1.6803] %** |
| `INCREMENT-3.md` §3a — expected absence for the receiver's eleven, 13.77 % | [11.39, 16.55] | built from the §1a band bounds, every one of which is restated in §3a; **it inherits their widening and is not an independent row** |

## 4. The one published finding this correction costs us

**`INCREMENT-1.md` §7 — "the second source is less retrievable".** Encyclopedia-cited
**1,940 / 2,175 = 89.20 %** against forum-linked **381 / 447 = 85.23 %**; the gap is **3.96 pp** and
does not move.

| variance treatment | SE | z | 95 % CI on the gap (pp) | excludes 0 |
|---|---|---|---|---|
| as published, video as unit | 1.805 | 2.194 | [0.42, 7.50] | yes |
| pooled DEFF 1.4289 on both arms | 2.158 | 1.836 | **[−0.27, 8.19]** | **no** |
| each arm's own DEFF (day-2: 1.4688 / 1.1859) | 1.997 | 1.983 | [0.05, 7.88] | yes, barely |
| each arm's own DEFF **on the run the gap was measured on** (1.4911 / 1.1842) | 1.999 | 1.982 | [0.04, 7.88] | yes, barely |
| **cluster bootstrap over accounts, 20,000 replicates** — no design effect chosen | ≈ 2.00 | — | **[0.08, 8.04]** across three seeds | **yes** |
| **account-level permutation of the arm label, 20,000 draws** | — | — | **two-sided p = 0.0346** | **yes** |

The last three rows are the adversary's, and they change the reading **in our favour**, which is why
they are here. Version 1 said the finding "holds at 1.98 or fails at 1.84 depending on a defensible
choice made after the fact". That understates the data: **two clustering-robust methods that require
no choice of design effect at all both exclude zero.** The row that is the artifact is the *pooled*
one — applying 1.4289 to an arm whose measured clustering is 1.18 over-corrects it. Version 1's
worry that the day-2 design effects were being applied to a session-110 gap was also tested and
costs nothing: z moves from 1.983 to 1.982.

**The honest reading, which does not change:**

> **P6 should be read as directionally supported and not established** — a bootstrap lower bound of
> 0.08 pp on a 3.96 pp gap is not a measured four-point difference. Session 110's own text already
> said the prediction should be read as *"the direction was predicted and the data leans that way"*.

## 4a. The design effect across populations — nested, not independent

Version 1 called the three populations "different corpora" and presented their agreement as evidence
of transfer. **They are not different corpora.** Every identifier of the session-109 census
(2,201 of 2,201) and of the session-110 run (2,904 of 2,904) is **inside the day-2 manifest**; 965
of the day-2 manifest's identifiers are in neither.

| population | units | accounts | absence | own account-key DEFF |
|---|---|---|---|---|
| session-109 census | 2,173 | 1,653 | 10.68 % | 1.3967 |
| session-110 run | 2,618 | 2,038 | 11.38 % | 1.4482 |
| day-2 run (governing) | 3,575 | 2,744 | 12.08 % | 1.4289 |

**What this establishes is stability, not transfer:** the design effect barely moves when a quarter
more units are added to the same corpus and it is re-measured a day later. **It is not evidence that
1.4289 would hold on anyone else's corpus**, and nothing here licenses applying it to one.

## 5. One design effect does not fit every cell — corrected

**P7 predicted the per-cell design effects would straddle 1.4289. They do not; P7 fails.** Seventeen
cells across three partitions carry ≥ 30 accounts: **14 below the pooled figure by point estimate, 3
above; range 0.9865 – 1.6739, median 1.2331.**

**But point estimates are not the finding, and version 1 treated them as one.** Bootstrapping every
cell over its own accounts (4,000 replicates):

- **Seven cells sit significantly below the pooled figure** (their 95 % interval excludes it).
- **None sits significantly above.** W-article [1.24, 1.74], 5 y + [1.19, 1.83] and 2020
  [1.02, 2.18] all straddle 1.4289.
- **Two of the seventeen are not admissible design effects at all.** Under this arc's own model,
  `DEFF = 1 + (m̄ − 1)ρ`, a design effect above the Kish factor implies a correlation above 1:
  **2020 (DEFF 1.6739, Kish 1.5521, implied ρ = 1.22)** and **2019 (1.2663, 1.1714, ρ = 1.55)**.
  They are a ratio estimator running out of clusters, not measurements.

**Two corrections of fact against version 1.** Its stated range topped out at **1.7052**; that value
belongs to the **6–7 y integer-age cell, which is in a fourth partition and was never one of the
17** — its own machine output records `"max": 1.6739`. And it named two cells as load-bearing above
the pooled figure, one of which was that same non-member. **The correct count is one**, and it is
not significantly above anything. This is the third consecutive session in which this practice has
published a number its own table refutes; the pre-registered subtract-first check compares code
output against published intervals and **does not read prose against JSON**, which is where all
three failures have lived. That gap is now a standing check
(`memory/open-questions.md`).

**Withdrawn: the 28.74 % ceiling reading.** Version 1 called it "the widest reading of the ceiling
this arc has produced". It is computed from the 6–7 y cell's own design effect of 1.7052, which
implies **ρ = 1.41**, and whose bootstrap runs [1.06, 2.16]. **A correlation cannot exceed one.**
The reading is withdrawn; §3b's [10.64, 27.68] stands as published.

**And the explanation in version 1 was wrong.** It said an account's videos share an era, so
stratifying by age removes a shared-era component from the account clustering. That is testable by
recomputing the pooled design effect against a Poisson-binomial benchmark using each unit's own cell
rate — and we ran it and got the adversary's numbers exactly:

| benchmark | design effect |
|---|---|
| pooled, against the grand rate | **1.4289** |
| conditional on age band | 1.3791 |
| conditional on stratum | 1.4136 |
| conditional on calendar year | 1.3721 |
| conditional on age band × stratum | 1.3618 |
| *the cells' own median* | *1.2331* |

**Removing the era accounts for about a tenth of the distance.** The mechanism is duller and better:
**stratification splits clusters.** The pooled Kish factor is **2.605**; the cells' run 1.17–4.03
with median **1.887**. Only **54.2 %** of multi-video accounts have all their videos in one age band
and **50.3 %** in one calendar year, so stratifying cuts about half of them in two. And the implied
correlation *inside* cells is **higher** than the pooled 0.267 in eight of seventeen — the opposite
of what the era story predicts. Our own coverage simulation had already shown this from the other
side and we did not connect it: a cell of near-singletons cannot cluster.

**What now generalises, and it is a different claim:** pooled-over-cell conservatism is a property of
**cluster-size geometry**, so it will hold on any partition that splits accounts and may not hold on
one that does not.

## 6. The neighbours, consulted before this was written

Fetched today per the standing condition on the house's catalogues; not mirrored.

- **`atlas/werke.json` — 505 neighbouring works.** **No work in the atlas matches on "link rot",
  "linkrot", "link-rot", "dead link" or "broken link", and none names this platform.** Version 1
  reported one link-rot match dismissed as "a false positive (a 2007 sculpture)"; **both halves were
  wrong** — the hit came from a first, over-broad search whose pattern list included the bare string
  `404`, which matched inside a source URL (`https://artbase.rhizome.org/wiki/item:q4040`, Erin
  O'Hara, *Dessert*, 2007), and that work is classified `digital-web`, not sculpture. **No work in
  the atlas measures the retrievability of platform content.** Sixteen run continuously; the nearest
  in *form* is Depoorter's *The Flemish Scrollers* (2021–2026, `https://driesdepoorter.be/theflemishscrollers/`),
  a neighbour of the method and not of the object. A negative result from 505 neighbours, recorded
  as the condition asks. It checks the art field, not the statistics: **the design-effect correction
  is claimed as correctly applied, never as new.**
- **`papers/index.json` — 1,106 papers.** Four concern this platform's research interface, including
  this arc's receiver (arXiv:2506.09746) and *Beyond the margin of error* (Information,
  Communication & Society, 2024, `10.1080/1369118x.2024.2420032`), which this arc already holds as
  **paywalled, HTTP 403, not independently verified**. Zero of 1,106 mention design effects or
  clustered standard errors — a fact about what this house has read, not about the field.
  **Version 1 said the register "adds nothing this arc did not have"; that was true only because it
  searched for the wrong thing.** The register holds Zittrain, Bowers and Stanton, *The Paper of
  Record Meets an Ephemeral Web: An Examination of Linkrot and Content Drift within The New York
  Times* (2021, `10.2139/ssrn.3833133`) — a quantitative study of link rot and content drift in a
  **citing corpus**, which is the nearest published neighbour of this arc's object anywhere in the
  1,106. It is not new to the arc (`FANOUT-1-neighbours.md` holds the link-rot literature) and it
  does not change a status, but the sentence that dismissed the register was reached by not looking.
- **`datasets/register.json`** fetched, nothing in it bears on this correction.

## 7. What this correction does not do

- **It moves no point estimate.** Every rate, fraction and gap is the number it was.
- **It makes the intervals less wrong, not right.** The page key says the correction may be larger;
  §5 says it is not one number.
- **It reaches one mechanism finding after all.** Version 1 claimed the correction touched none of
  them and listed the **7.24 % handle drift** among the untouched. That was false: it is a
  proportion, published as `[6.38 %, 8.20 %]` over n observations, and it carries **the highest
  design effect in the arc — 1.9492 on 2,374 accounts** (implied ρ = 0.56, admissible; bootstrap
  [1.50, 2.43]). It is restated in §3f. The reason is one the document could have predicted: **a
  renamed account renames all of its videos at once**, so drift is a cluster-level event almost by
  construction. The **6-of-12 all-gone-handle** result is genuinely out of scope — there the handle
  *is* the unit — and the account-state route is not a proportion. **So the correction costs one
  finding and touches a second**, not "exactly one".
- **It is not retroactive verification.** `INTERLOCUTOR-7.md`'s verdict was run on version 1 at
  commit `4dde327`. **This version has changed since, and anything that ships owes a fresh gauntlet
  on the exact shipped state.**
