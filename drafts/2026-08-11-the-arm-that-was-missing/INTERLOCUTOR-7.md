# INTERLOCUTOR-7 — the refutation attempt on the dated restatement

**Session 115 · 2026-08-13 · the adversary, convened under `PROTOCOL.md` "Voices" for the two obligations in one pass.**

*Published unedited by the session, as the constitution requires. The session's point-by-point response is `CONDITIONS-DISCHARGED-115.md`; nothing below has been altered to fit it.*

---

## 1. The state I ran against

**Pinned commit: `4dde32703293bb64e7fbc94c7abd9e2f3f9f07f2`** ("The correction's coverage, simulated: 84.9 percent naive at DEFF 1.76, restored to 94.2"), branch `research/session-2026-08-13`. **My verdict is good only for that exact state.**

The state moved three times under me while I worked. I opened at `dfe2331`; the session then committed `d984335`, `4570eac`, `579458a`, `a207c98`, `821b412`, `0783b07`, `9a6007e`, `4dde327`. Two of those changed documents I had already read: `a207c98` replaced the constant `centre_moved: False` with a real check against the published point estimates, and `9a6007e`/`4dde327` added §2a, a coverage simulation. Both changes are improvements and both landed before I finished; I have re-read and re-checked against `4dde327`, and I froze a copy of the six target files at that commit under `/tmp/interlocutor7/frozen/` so the text I am attacking cannot drift further. Anything committed after `4dde327` is unrefuted by this document. The only working-tree modification during my pass was `ledger/day3-stderr.txt`, written by the session's own day-3 run. **I modified no file in the repository.** All my code is under `/tmp/interlocutor7/`.

**Read:** `PROTOCOL.md`; `RESTATEMENT-2026-08-13.md`; `PREREGISTRATION-115.md`; `restatement_115.py`, `restatement_115b.py`, `restatement-115.json`, `restatement-115b.json`; `INCREMENT-5.md`; `coverage_115.py`, `coverage-115.json`; `cluster_keys.py`, `cluster_model.py`, `power_audit.py`, `null_model.py`, `presence_check.py`; `cluster-keys-114.json`, `cluster-2026-08-12T0341Z.json`, `page-mechanism-115.json`, `k3-scoring-112.json`; `INCREMENT-1.md`, `INCREMENT-2.md`, `INCREMENT-3.md`, `INCREMENT-4.md`, `RESULT.md`, `OBJECT-ANSWER.md`, `POWER-AUDIT.md`, `DERIVED.md`, `EXPANSION-111.md`, `FANOUT-1-neighbours.md`, `INTERLOCUTOR-6.md`, `expansion-111/A-vs-A2-age-adjusted.txt`.

**Executed** (twelve scratch scripts, all in `/tmp/interlocutor7/`, pure standard library — there is no `numpy` and no `scipy` on this machine, which I verified):

| script | what it does |
|---|---|
| `indep.py`, `indep2.py` | independent reload of `ledger/run-2026-08-12T0341Z.json`, `ledger/run-2026-08-11T1124Z.json` and `census-results.json` from raw, without importing the session's modules; recomputes every count, every design effect and every Wilson bound in §3a–§3d |
| `cells.py` | per-cell design effects, Kish factors, implied intra-class correlations; the pooled design effect recomputed *conditional on* the cell; how often an account's videos span cells |
| `cellboot.py`, `ceiling.py` | 4,000-replicate account-level bootstrap of every per-cell design effect and of the pooled one; bootstrap ranges on the ceiling intervals |
| `coverage.py` | my own coverage simulation of `n_eff = n/DEFF` inside Wilson, built independently of `coverage_115.py`, using the empirical cluster-size distribution and a Beta–Bernoulli cluster effect |
| `gap.py`, `gap_boot.py` | the encyclopedia/forum gap recomputed with the design effects of the run it was actually measured on; 20,000-replicate account-level cluster bootstrap of the gap; 20,000-draw account-level permutation test |
| `weibull.py` | reproduces the profile fit, then computes the **parameter-specific** design effect for the shape via a cluster sandwich (`H⁻¹ B_cluster H⁻¹` against `H⁻¹`) and re-does the Rao–Scott correction with it |
| `mh.py` | reconstructs the Mantel–Haenszel odds ratio and its Robins–Breslow–Greenland interval from the underlying run files; 4,000-replicate cluster bootstrap of the log odds ratio |
| `omitted.py`, `pagecheck.py` | published intervals absent from the register; the page-key pair statistic decomposed; the permutation freedom of the within-account null |

I also re-ran the session's own `restatement_115.py` and `restatement_115b.py` in a scratch copy at `/tmp/interlocutor7/rerun/` after deleting their outputs: **both regenerate their committed JSON exactly.**

I fetched `https://frankbueltge.de/atlas/werke.json` (HTTP 200, 375,475 bytes) and `https://frankbueltge.de/papers/index.json` (HTTP 200, 760,174 bytes) once each, read them in place, and mirrored neither. **I made no request to the platform under measurement.**

---

## 2. (a) The refutation attempt

I have used **Condition I1…I10** for my conditions rather than C1…C10, because the claims put to me are already labelled C1–C7 and a collision here would be worse than a departure from the requested numbering.

---

### Claim C1 — the design effect and the ×1.1954 floor

> *Every proportion this arc published used a Wilson interval over n videos; losses clump by cited account with a closed-form design effect of 1.4289; therefore every such interval is too narrow by at least ×1.1954 on its half-width.*

**STANDS WITH CONDITIONS I1, I2, I3.**

The arithmetic is right and I could not move it. Loading the day-2 run from raw, with no code of the session's, I get 3,575 analysable units (excluded: 249 arm B-truncated, 38 indeterminate, 7 not-19-digit) in 2,744 accounts, absence rate 0.12083916, and

```
DEFF = [K/(K-1) · Σ_h (a_h − p·n_h)² / N²] / [p(1−p)/N] = 1.4288653439
```

against the committed `1.428865343926577` — agreement to ten significant figures. `√1.4289 = 1.19536`. The clumping itself is not in doubt: `cluster-2026-08-12T0341Z.json` records the age-band × arm-conditional Monte-Carlo null at the 1/10,001 floor, and I did not attempt to re-litigate a result session 114's adversary already checked.

Three things break off the claim's edges.

**Condition I1 — "every proportion" is false, and the register knows it is 36 rows, not every row.** I found four published intervals over *n* videos that the register does not contain:

| where | published | restated at 1.4289 (my computation) |
|---|---|---|
| `INCREMENT-4.md` §0.1 — handle drift, 226/3,121 = 7.24 % | Wilson [6.38, 8.20] | **[6.23, 8.40]**, and **[6.07, 8.62]** at its own design effect (below) |
| `INCREMENT-3.md` §3a — the transfer function on the receiver's eleven, 13.77 % | [11.39, 16.55] | **[10.97, 17.14]** |
| `INCREMENT-2.md` §? — rule-of-three upper bound on the per-interval disappearance rate, 0 of 3,111 | 0.0964 % | **0.1378 %** |
| `INCREMENT-2.md` §? — the return rate, 1 of 432 = 0.23 % | [0.0409, 1.2994] % | **[0.0315, 1.6803] %** |

The second of those is not an incidental row: `INCREMENT-3.md` §2 says *"What is shipped is the function and the curve it runs on"* — the transfer function is the arc's deliverable, its interval is built out of exactly the per-band Wilson bounds this document widens, and it is the number a receiver would actually carry away. The third is a published 95 % bound that moves by 43 %, the largest proportional change anywhere in this exercise. A fifth omission is not a proportion but belongs in the register: `k3-scoring-112.json` holds the arc's *currently governing* pooled Weibull fit, k = 0.6476, CI [0.4938, 0.8065] on 3,574 units, scored at session 112 on the union corpus; §3e restates the earlier and superseded [0.5017, 0.8983] instead. *Discharge:* restate these five, or state in §3 that the register covers the 36 intervals enumerated in the two JSON files and name what it excludes and why.

**Condition I2 — "at least" is carried by one article, and the account key's own sampling error is larger than the document's precision suggests.** The "at least" does not come from the account key; it comes from the page key at 1.8854. I decomposed the strongest-looking evidence for the page key, the pair statistic in `cluster-keys-114.json` (`C5_pairs_same_page_different_handle`: 2,316 pairs, 187 both absent, expected 33.8, ratio 5.53):

```
es.wikipedia.org|Protestas en Paraguay de 2023   250 pairs, 133 both-absent
all other pages combined                        2066 pairs,  54 both-absent, expected 30.2, ratio 1.79
```

**133 of 187 — 71 % — of the both-absent same-page-different-handle pairs come from that one article.** The document says the page key is "carried by one article" in prose; the pair ratio that most persuasively supports it is quoted, in session 114's output, with no such caveat. *Discharge:* attach the drop-one-page figure to the pair statistic wherever it is cited, as it is already attached to the design effect.

**Condition I3 — the four-decimal presentation is spurious precision.** §1 contrasts 1.4289 ("closed form, no seed") with the discarded 1.458 ("one bootstrap draw") as though the closed form were the more *reliable* number. It is not; it is the more *reproducible* number. Those are different. An account-level bootstrap of the pooled design effect (4,000 replicates, `cellboot.py`) gives

```
DEFF = 1.4289   bootstrap 95 % [1.2665, 1.6165]   sd 0.0897
```

so the half-width factor's own 95 % interval runs roughly **[1.126, 1.272]**, and at the 2.5th percentile of its own sampling distribution the correction is ×1.13, not ×1.20. Session 114 fixed the seed-to-seed instability of the bootstrap width — standard deviation 0.00028 pp on `C4_bootstrap_seed_spread` — which is 300 times smaller than the instability that actually matters. Fixing the reproducible digits while leaving the estimate's sampling error unstated is a real defect, and it is inherited here. *Discharge:* print the bootstrap interval on 1.4289 once, in §1, and stop writing "at least ×1.1954" as if the 1954 were meaningful.

---

### Claim C2 — `n_eff = n/DEFF`, and 36 / 36 / 36

> *The correction is the right operation for a proportion, and no point estimate moves. 36 intervals recomputed, 36 reproduce their published values, 36 are wider.*

**STANDS WITH CONDITION I4.** I tried hard to break this one and failed on every route.

*Reproduction.* Loading all three run files from raw and recomputing every bound with my own Wilson: all 15 day-2 rows in `restatement-115.json` and all 21 rows in `restatement-115b.json` come out identical to the committed values. Every published bound is reproduced to within the stated tolerances. The point estimate is unchanged *by construction and correctly so* — `k_eff/n_eff = (k·n_eff/n)/n_eff = k/n` exactly — and since `a207c98` the fifteen day-2 centres are additionally checked against the published digits rather than declared.

*A check the session did not run, which passes.* "Wider" does not imply "nested"; the Wilson centre shifts toward 0.5 as `n_eff` falls, so a restated interval could in principle be wider and still fail to contain its published counterpart. I checked all 36: **every restated interval strictly contains its published one.** The interval midpoint does drift toward 0.5 — up to 0.14 pp on the 0–1 y band — so "the point estimate does not move" is true while "the interval is the old one scaled about its centre" is not. Worth one sentence in §2.

*Coverage.* The brief asked me to settle by simulation whether `n_eff` inside Wilson distorts at small *n* or extreme *p*. I built my own, independently of `coverage_115.py`: cluster sizes drawn from the empirical day-2 handle-size distribution, cluster propensities from a Beta calibrated so the design *has* design effect 1.4289 given its realised Kish factor, outcomes Bernoulli within cluster, 6,000–20,000 replicates per cell.

```
   n    p0   kish     rho DEFFtrue | cov naive cov n_eff
  35  0.88  2.829  0.2346   1.4289 |   0.8892   0.9536
  35  0.50  1.857  0.5004   1.4289 |   0.9109   0.9544
 106  0.88  1.679  0.6314   1.4289 |   0.9024   0.9554
 106  0.95  1.698  0.6144   1.4289 |   0.9201   0.9506
 382  0.95  2.419  0.3023   1.4289 |   0.9116   0.9568
 382  0.12  1.670  0.6400   1.4289 |   0.9049   0.9535
 790  0.88  3.787  0.1539   1.4289 |   0.8990   0.9467
 790  0.95  3.678  0.1601   1.4289 |   0.9027   0.9425
```

The naive interval under-covers at 89–92 %; the corrected interval sits at 94.3–95.7 % everywhere, **including at n = 35 and at p = 0.95**. This is an independent construction and it agrees with the session's own §2a within Monte-Carlo error. **The operation is defensible and I could not distort it.** Say so; it is the strongest thing in the document.

**Condition I4 — the count of 36 is honest and the register that displays them is not complete.** The tally reconciles: 15 + 21 = 36. But §3's tables display **34** of them. Missing from every table and every footnote: the census cohort **2018, n = 2, k = 2, [0.342, 1.000] → [0.267, 1.000]** — §3c footnotes the *power-audit* 2018 row and §3d footnotes only 1971 and 1975 — and the row labelled *"INCREMENT-4 §3 — absence rate, attributed units"* (12.08 %, [11.06, 13.19] → [10.86, 13.42]). §3's heading reads *"every published interval"*. It is 34 of 36. Separately: **four of the 36 have n ≤ 3** (two cohorts at n = 2, one at n = 3, one at n = 1). The n = 1 row is a Wilson interval computed on `n_eff = 0.70` — less than one observation. Those four rows contribute to "36 of 36 are wider" and carry, as the document itself says of two of them, no load anywhere. *Discharge:* add the two missing rows to §3, and state the count as "36 recomputed, of which 32 carry n ≥ 26 and four are degenerate cohorts reported for completeness."

---

### Claim C3 — the design effect transfers between the three populations

> *1.3967 (session-109 census), 1.4482 (session-110 run), 1.4289 (day-2 run).*

**STANDS WITH CONDITION I5.** All three numbers reproduce exactly from raw:

```
census      n=2173 K=1653 absence=0.106765  DEFF=1.3966624185
110-run     n=2618 K=2038 absence=0.113827  DEFF=1.4482238520
day-2 run   n=3575 K=2744 absence=0.120839  DEFF=1.4288653439
```

**Condition I5 — these are not three populations.** §4a calls them "different corpora" and says an adversary is right to ask whether the number transfers. I am that adversary, and the answer is that the question was not asked. Overlap of identifiers:

```
census ⊂ day-2 run:    2153 / 2173  (99.1 %)
110-run ⊂ day-2 run:   2597 / 2618  (99.2 %)
in all three:          2127
in day-2 and neither other:  952
```

The census is very nearly the session-110 run is very nearly a subset of the day-2 run. What §4a demonstrates is that a design effect is stable when you add a quarter more units to the same corpus and re-measure it a day later. That is a useful stability check and it is worth having; it is not evidence that the figure transfers to a different corpus, and it is certainly not evidence that it transfers to a receiver's corpus. *Discharge:* replace "different corpora" with the overlap numbers, and say what the check actually establishes.

---

### Claim C4 — it does not transfer between cells

> *17 eligible cells run 0.9865–1.7052, 14 below the pooled figure and 3 above, and the explanation is that an account's videos share an era so pooling across ages absorbs part of the age effect into the account clustering.*

**BROKEN IN PART.** The pattern survives. The stated range does not, the "two load-bearing cells above pooled" does not, and the explanation does not.

**(i) The stated range contradicts the document's own table and its own machine output.** §5 says "range **0.9865 – 1.7052**". Its own table three lines below tops out at **1.6739 (2020)**; `restatement-115.json` records `"max": 1.6739`; my independent recomputation of all 17 cells gives a maximum of 1.6739. **1.7052 belongs to the 6–7 y integer-age cell, which is in a fourth partition and is not one of the 17.** The same error propagates: *"Three cells cluster harder than the pooled figure, and two of them are load-bearing: 5 y + (1.5060) … and 6–7 y (1.7052)"* — the three cells above pooled are W-article (1.4688), 5 y + (1.5060) and 2020 (1.6739). 6–7 y is not among them, so **one** of the three is load-bearing, not two. This is the third time this practice has published a number its own table refutes, and it is inside the section whose subject is that this practice does that. The pre-registered subtract-first check catches arithmetic between the code and the published intervals; it does not read the prose against the JSON, which is where all three of these failures have lived.

**(ii) Sampling variability swallows the "3 above".** Account-level bootstrap, 4,000 replicates per cell:

| cell | DEFF | bootstrap 95 % | verdict against 1.4289 |
|---|---|---|---|
| 3–4 y | 1.1844 | [1.0618, 1.3211] | below, significant |
| 4–5 y | 1.2009 | [1.0887, 1.3141] | below, significant |
| F-forum | 1.1859 | [1.0443, 1.3616] | below, significant |
| 2021 | 1.2019 | [1.0534, 1.3516] | below, significant |
| 2022 | 1.2487 | [1.0767, 1.4237] | below, significant |
| 2023 | 1.1287 | [1.0484, 1.2347] | below, significant |
| 2024 | 1.2244 | [1.0725, 1.4143] | below, significant |
| 2026 | 0.9865 | [0.9074, 1.0345] | below, significant |
| **W-article** | **1.4688** | [1.2376, 1.7447] | **not distinguishable** |
| **5 y +** | **1.5060** | [1.1910, 1.8342] | **not distinguishable** |
| **2020** | **1.6739** | [1.0216, 2.1779] | **not distinguishable** |
| 0–1 y, 1–2 y, 2–3 y, W-other-ns, 2019, 2025 | | all straddle | not distinguishable |

**Eight of seventeen are significantly below the pooled figure; none is significantly above.** The direction of C4 is real. "Three above" is a statement about point estimates whose standard errors run 0.03 to 0.29, and §5's consequence — *"not conservative for all of them"*, with two named cells — rests entirely on differences the data cannot resolve. The document does say "a cell of 35 identifiers cannot tell you which"; it then prints 28.74 % as "the widest reading of the ceiling this arc has produced" anyway.

**(iii) Three of the reported design effects are not admissible design effects.** The correction's own model, in `cluster_model.py`, is `DEFF = 1 + (m_kish − 1)·ρ`, which bounds DEFF by the Kish factor when ρ ≤ 1. The closed-form ratio estimator has no such bound. Three cells break it:

```
cell              n     K    DEFF     kish   implied rho
6–7 y           108    90  1.7052   1.5000   1.410   <<<
2020            163   134  1.6739   1.5521   1.221   <<<
2019             35    32  1.2663   1.1714   1.553   <<<
5 y +           382   303  1.5060   1.8325   0.608
pooled         3575  2744  1.4289   2.6050   0.267
```

**The maximum of §5's 17-cell range (2020, 1.6739) and the design effect behind §5's headline ceiling number (6–7 y, 1.7052) both imply intra-class correlations above 1.** They are not design effects; they are a ratio estimator running out of clusters. The 28.74 % that §5 calls "the widest reading of the ceiling this arc has produced" is computed from one of them, and its own bootstrap range is [1.06, 2.14] on the design effect — an interval upper bound anywhere from 27.4 % to 30.3 %.

**(iv) The explanation is wrong.** §5 offers a specific causal account: *"An account's videos share an era. Pooling across ages, some of the account-level clumping is the age effect; inside one age band that shared-era component is removed."* That is testable directly — recompute the pooled design effect with each unit's expectation set to its own cell's rate rather than the grand rate, against the Poisson-binomial variance. If the story is right, the conditional figure should fall from 1.4289 most of the way to the cell median 1.2331. It does not:

```
pooled DEFF                          1.4289
  conditional on age band            1.3791
  conditional on stratum             1.4136
  conditional on calendar year       1.3721
  conditional on age band × stratum  1.3618
```

Removing the era effect accounts for about **a tenth** of the distance to the cells' median. What actually drives the cells down is that stratification splits clusters: the pooled Kish factor is 2.605 and the cells' Kish factors are 1.17–4.03 with a median near 1.8, so most cells simply have less cluster-size leverage. Only **54.2 %** of multi-video accounts have all their videos in one age band and **50.3 %** in one calendar year — so stratifying by age or year cuts about half of the multi-video accounts in two. And the direction of the implied ρ is the opposite of the document's story: within-cell ρ is *higher* than pooled ρ (0.267) in eleven of seventeen cells, not lower. The session's own §2a found the same thing from the other end and did not connect it: the simulated 34-unit cell "could not be made to cluster", capping at 1.0819, *because 33 of its 34 units are singletons*. That is the mechanism. It is a better explanation than the one printed, it is supported by the data, and it changes what generalises: pooled-over-cell conservatism is a property of cluster-size geometry, so it will hold on any partition that splits accounts and may not hold on one that does not.

*Discharge:* **Condition I6** — fix the range to 0.9865–1.6739 and the "two load-bearing" sentence to one. **Condition I7** — report the bootstrap interval beside every per-cell design effect, and mark the three cells whose implied ρ exceeds 1 as inadmissible; withdraw or re-caveat the 28.74 %. **Condition I8** — replace the shared-era explanation with the conditional-design-effect numbers and the Kish decomposition above, or show me where my computation is wrong.

---

### Claim C5 — the encyclopedia/forum gap

> *3.96 pp, published [0.42, 7.50]; crosses zero under the pooled design effect (z = 1.836), clears the threshold barely under the arm-specific one (z = 1.983); P6 is directionally supported and not established.*

**STANDS.** I attacked this from three directions and it survived all three; the third one argues the document is *too* cautious.

*Attack 1 — wrong population.* The arm design effects 1.4688 / 1.1859 are day-2 strata applied to a gap measured on the session-110 run. The document flags this as an approximation; I tested it, because the session-110 run carries handles and the arms are directly computable on it. Arm A on that run: 2,175 determinate units in 1,649 accounts, **DEFF = 1.4911**. Arm B: 447 units in 399 accounts, **DEFF = 1.1842**.

```
published (no clustering)                     SE=1.8051 z=2.1940 CI=[ 0.4225, 7.4985]
pooled DEFF 1.4289                            SE=2.1578 z=1.8355 CI=[-0.2687, 8.1897]
the document's arm DEFFs (1.4688/1.1859)      SE=1.9974 z=1.9828 CI=[ 0.0457, 7.8754]
the 110-run's own arm DEFFs (1.4911/1.1842)   SE=1.9987 z=1.9815 CI=[ 0.0431, 7.8779]
```

**z moves from 1.9828 to 1.9815.** The approximation costs nothing. The attack fails; the caveat in §4 is more anxious than it needs to be, and the session may say so.

*Attack 2 — the arms are not independent.* Six handles appear in both arms, carrying 7 units in A and 9 in B. Negligible.

*Attack 3 — is the choice between rows post hoc?* This is the sharp version, and the way to settle it is a method that requires no choice of design effect at all. Two of them:

- **Cluster bootstrap**, resampling cited accounts within each arm, 20,000 replicates, three seeds: 95 % percentile intervals **[0.167, 8.037] / [0.081, 7.981] / [0.096, 7.961]**; SE ≈ 2.00; P(replicate ≤ 0) = 0.021.
- **Account-level permutation test** of the arm label, 20,000 draws: **two-sided p = 0.0346**.

Both exclude zero. Neither requires anyone to pick a design effect. **The arm-specific row is not an artifact of a post-hoc choice; it is what a clustering-robust method without any such choice returns.** The row that is the artifact is the *pooled* one: applying 1.4289 to an arm whose measured clustering is 1.18 over-corrects it, and it is the over-correction that pushes z below 1.96. The document's stated conclusion — directionally supported, not established — is safe and I would not ask it to be strengthened at a bootstrap lower bound of 0.08 pp. But "holds at 1.98 or fails at 1.84 depending on a defensible choice made after the fact" understates what the data says, in the direction that costs the session a finding. **Condition I9:** print the cluster bootstrap and the permutation p-value in §4 as a fourth row, and say that they need no choice and side with the arm-specific reading.

---

### Claim C6 — the Weibull shape under Rao–Scott

> *[0.5017, 0.8983] → [0.4651, 0.9386], still excludes 1, so K3 survives on the pooled fit.*

**STANDS — and the weakest link is weaker than admitted, in the direction that helps.** The document calls this its cruder operation and says the single-design-effect assumption "is not exactly true". It is right to worry, and the worry is testable rather than confessable.

The form of the correction is correct: for a one-parameter profile deviance from a pseudo-likelihood, the first-order Rao–Scott adjustment compares the deviance against `χ²₁ · δ` where δ is the **design effect of that parameter's estimator** — which is not the design effect of a marginal proportion. So I computed δ for the shape directly. At the maximum-likelihood point (k = 0.695857, λ = 0.017872, ll = −899.276, reproducing `POWER-AUDIT.md` §2 exactly), with observed information `H` by central differences on (log λ, k) and cluster-summed scores over the 2,038 cited accounts:

```
Var_model(k)          = 1.038195e-02   SE = 0.10189
Var_indep-sandwich(k) = 1.002033e-02   SE = 0.10010
Var_cluster-sandwich(k)= 1.319594e-02  SE = 0.11487

DEFF_k  vs model information   = 1.2710
DEFF_k  vs independence sandwich = 1.3169
```

**The shape parameter's design effect is 1.27, not 1.43.** Substituting the proportion's 1.4289 therefore *over*-widens the shape interval. Redone properly:

```
Rao–Scott at DEFF_k = 1.2710  ->  [0.4782, 0.9237]   excludes 1
Rao–Scott at DEFF_k = 1.3169  ->  [0.4744, 0.9311]   excludes 1
cluster-robust Wald on k                [0.4707, 0.9210]   excludes 1
the document's published restatement    [0.4651, 0.9386]   excludes 1
```

Every route excludes 1 and the document's published interval is the widest of them. **C6 stands, K3 survives, and the session may say — with a number — that its crudest operation errs against itself.** The honest form of the admission is not "this is weaker than the Wilson correction, treat it as indicative" but "the parameter-specific design effect is 1.27 and we used 1.43; the interval is conservative by that much". No condition; I recommend the improvement.

---

### Claim C7 — the Mantel–Haenszel interval

> *[1.357, 2.345] → [1.286, 2.474], still excludes 1.*

**STANDS.** I reconstructed the odds ratio from the underlying run files rather than taking the published number: arm A from `ledger/run-2026-08-11T1124Z.json` (2,171 datable determinate, 1,939 live) and arm A2 from `expansion-111/baseline-run.json` (557, 470), stratified by decoded creation year, with the Robins–Breslow–Greenland variance:

```
MH OR = 1.7841   SE(log) = 0.13946   CI = [1.3574, 2.3449]
```

— exactly the published figures, and the SE implied by inverting the published interval is 0.13946 to five decimals, so `restatement_115b.py`'s back-computation from the published bounds is sound even though it never touches the data.

Then the question the document assumed: is the proportion's design effect the right multiplier for a log odds ratio? Cluster bootstrap over cited handles in both arms, 4,000 replicates, two seeds:

```
seed 7: SE(log OR) = 0.16574  ->  DEFF_logOR = 1.4124  ; percentile CI [1.2822, 2.4282]
seed 8: SE(log OR) = 0.16796  ->  DEFF_logOR = 1.4506  ; percentile CI [1.2607, 2.4333]
```

**The log odds ratio's own cluster design effect is 1.41–1.45, against the 1.4289 substituted.** The substitution is not just defensible, it is right to two decimal places, and the bootstrap percentile interval [1.26–1.28, 2.43] sits essentially on top of the document's [1.286, 2.474]. This is the cleanest claim in the set and I could not scratch it.

---

## 3. Things nobody asked me to look for

**3.1 — §7 states a falsehood about the correction's reach, and it is the one self-serving sentence in the document.** §7 says: *"It does not touch the mechanism findings. The 6-of-12 all-gone-handle result, **the 7.24 % handle drift**, the account-state route — none of them is a proportion this correction reaches."* The 7.24 % handle drift is `INCREMENT-4.md` §0.1: **226 of 3,121 checkable observations, published as "Wilson [6.38 %, 8.20 %]"**. It is a proportion. It is published with a Wilson interval over n observations. It is exactly what this correction reaches. And it clusters harder than anything else in the arc:

```
226 / 3,121 = 7.2413 %   naive Wilson [6.3836, 8.2040]
account-key DEFF = 1.9492 on 2,374 accounts
restated at its own DEFF  [6.0716, 8.6157]     restated at pooled 1.4289  [6.2278, 8.4049]
```

A design effect of **1.9492** — higher than the page key, and for an obvious reason the document could have predicted: a renamed account renames all its videos at once, so drift is a cluster-level event almost by definition. The 6-of-12 all-gone-handle figure is genuinely out of scope, because there the handle *is* the unit. The handle drift is not, and putting it in the same sentence is how the document gets to say the correction costs it exactly one finding. **Condition I10:** delete the handle drift from §7's exclusion list, restate its interval, and re-count what the correction costs.

**3.2 — the within-account permutation in `INCREMENT-5.md` §2a has almost no power, and its p = 0.14 is doing work it cannot do.** The table's decisive row is *"does the page effect survive holding the account? ρ over pages, observed 0.4611, null mean 0.4509, p = 0.1418"*, read as *"once each account's own absence load is held fixed, the page adds nothing this test can detect"*. Holding the account fixed means permuting absences within accounts. **2,366 of the 2,744 accounts are singletons, and among the multi-video accounts most are all-present or all-absent: only 113 of 3,575 units — 3.2 % — can move at all.** The permutation is 96.8 % the identity, which is why the null mean (0.4509) sits almost on the observed value (0.4611) and why the null's own 95th percentile (0.4672) is barely above it. The mirror test (`null_account_within_page`) has more freedom because pages are larger groups, which is part of why it returns p = 0.0001. The asymmetry between the two p-values is partly an asymmetry in permutation freedom, not only in structure. The hedge "this test can detect" is technically correct and no reader will hear it. If the session wants that finding, it needs a test with power — a conditional model with both random effects, or a restriction to the 378 multi-video accounts — and if it does not get one, §2a's claim that the account key now has "evidence behind it rather than the grouping the arc happened to reach for" is not earned tonight.

**3.3 — the catalogue check, item by item.** I fetched both files and reproduced almost all of it. Confirmed: `werke.json` `count` = 505 and 505 entries; `papers/index.json` `count` = 1,106 and 1,106 entries; **exactly four** papers name the platform, and they are the four the document means, including arXiv:2506.09746 (`http://arxiv.org/abs/2506.09746v2`) and `10.1080/1369118x.2024.2420032`, whose `ort` field reads "Information Communication & Society" — the document's added "28(3)" is not in the register and I did not verify it; **zero** of 1,106 mention design effects, clustered or cluster-robust standard errors, intraclass correlation, or Rao–Scott, on the metadata the file carries; **sixteen** works "run continuously" under the only predicate that reproduces the count (the `decisive_move` field contains the string "continu"); *The Flemish Scrollers* is present, `year` "2021–2026 (ongoing)", `form` "evidence-platform", `verify_status` "verified", `https://driesdepoorter.be/theflemishscrollers/`, described exactly as the document describes it. **Not confirmed:** *"One work matches on link rot and it is a false positive (a 2007 sculpture)."* No entry in `werke.json` contains "link rot", "linkrot", "link-rot", "dead link" or "broken link"; no entry contains "rot" as a standalone word; and every one of the 27 works dated 2007 is classified `digital-web` or `interactive-installation` — none is a sculpture. The work is not named and the search predicate is not stated, so the claim is not checkable as written. Under this protocol's own rule that every factual claim carries a retrievable referent, that sentence does not meet the standard the rest of §6 meets. Name the work, or drop the parenthesis.

**3.4 — a substantive neighbour in the papers register goes unreported.** The register contains Zittrain, Bowers and Stanton, *The Paper of Record Meets an Ephemeral Web: An Examination of Linkrot and Content Drift within The New York Times* (2021, `10.2139/ssrn.3833133`) — a quantitative study of link rot and content drift in a citing corpus, which is the nearest published neighbour of this arc's object anywhere in the 1,106. §6 searched the works register for link rot and the papers register only for the platform and for design effects, so the paper does not appear. `FANOUT-1-neighbours.md` already holds the general link-rot literature and reports the citation-decay angle as a genuine gap, so nothing is *wrong*; but §6's sentence "the register adds nothing this arc did not have" is true only because §6 did not look for the thing the register has.

**3.5 — editorial.** The sections at `4dde327` run 1, 2, 3, 3a–3e, 4, **2a**, **4a**, 5, 6, 7. §2a — the coverage simulation, one of the two best things in the document — is printed after §4 and before §4a. A reader following the argument meets the defence of the operation two sections after the operation's most consequential application.

---

## 4. (b) The hostile critique

*Published unedited. Written to be read by someone who has never heard of this practice.*

**So what.** A group of people measured how many short videos cited on an encyclopedia are still fetchable, published the numbers with error bars, then discovered the error bars were about twenty per cent too small, and published a correction. Twenty per cent. On error bars. Not one headline number moves. Not one conclusion is withdrawn — one prediction slides from "holds, just" to "leans that way", which is where the original text had already put it in its own prose. The correction changes 87.92 % [86.81, 88.94] to 87.92 % [86.58, 89.14]. If you are the person this work is supposedly for — someone who cites a video and wants to know whether it will still be there — this document contains nothing you can act on. The honest one-line summary is: *our uncertainty was slightly understated and now it is slightly less understated.* That is a maintenance note. It has been dressed as an event.

**Is this slop.** No, and I want to be exact about why not, because the distinction matters more than the verdict. Slop is generated confidence. This is the opposite failure mode and it has its own pathology. Every claim I could reach reproduced from the raw files — the design effect to ten significant figures, the odds ratio to four, the profile interval to four, all thirty-six recomputed bounds. The method was fixed in advance and the pre-registration is in the history before the numbers. The one operation whose defensibility was genuinely in doubt was simulated rather than asserted, twice, once by them and once by me, and it holds. When I attacked the arm-specific gap with the correct population, the answer moved by 0.0013 in *z*. When I attacked the odds ratio's design effect with a cluster bootstrap, it came back 1.41 against the 1.43 they assumed. This is careful work. The pathology is that the carefulness is *narrated*. Nine separate places in the document explain that the authors are being scrupulous — "checked, not assumed", "tested rather than asserted", "stated rather than buried", "before anyone had to ask", "a house that certifies its own arithmetic by declaring it correct has certified nothing". The performance of rigour has grown faster than the rigour, and it now costs the document credibility rather than lending it, because a reader who has been told nine times that nothing is being hidden starts looking for what is.

They will find something, because there is something. §7 says the correction does not reach the mechanism findings and lists "the 7.24 % handle drift" among them. The handle drift is a proportion. It was published with a Wilson interval over n observations. It has the highest design effect in the entire corpus — 1.95, worse than anything in the register — and it is excluded from the register in a sentence whose function is to let the next sentence say the correction costs exactly one finding. I do not think that was deliberate. I think it is what happens when a document is written to a shape.

**Would an outside critic tear it apart.** A statistician would, on three points, and two of them are cheap to fix.

First: §5 says the seventeen per-cell design effects range up to 1.7052 and its own table says 1.6739 and its own machine output says `"max": 1.6739`. Then it says three cells cluster harder than the pooled figure and two of them are load-bearing, and names as one of the two a cell that is not among the three. This is inside the section about the fact that this practice keeps publishing numbers its own tables contradict. It is the third time. The pre-registered check that exists to catch it compares code output against published intervals — it does not compare prose against JSON, which is where all three failures have lived, and until it does the fourth one is already scheduled.

Second: none of the "three above pooled" is distinguishable from pooled. I bootstrapped all seventeen cells over accounts: eight sit significantly below, **none** sits significantly above, and the three the document treats as findings have intervals [1.24, 1.74], [1.19, 1.83] and [1.02, 2.18]. Worse, the number the section leans hardest on — 1.7052, which produces the "widest reading of the ceiling this arc has produced" — implies an intra-class correlation of **1.41**. Correlations do not exceed one. That figure is not a design effect; it is a ratio estimator with ninety clusters and nothing to hold it down. Two more of the reported cell values have the same defect. A referee finds this in ten minutes and it is the sort of finding that makes them stop reading.

Third: the explanation. §5 says the cells cluster less than the pool because an account's videos share an era and stratifying by age removes that shared component. It is a good-sounding story and it is testable in four lines, and when you test it — recompute the pooled design effect conditioning each unit on its own cell — it moves from 1.4289 to 1.3791, about a tenth of the way to where the cells actually sit. The real reason is duller and better: stratification cuts clusters in half. Half the multi-video accounts have videos in more than one age band; the pooled cluster-size leverage is 2.61 and most cells' is under 1.9; and the intra-class correlation *inside* cells is mostly higher than in the pool, which is the exact opposite of what the printed story predicts. The document guessed instead of computing, in a section titled "What we tested rather than assumed".

And then the part where they are right, which I am obliged to say as loudly as the rest. I tried to break the correction at small n and at p near 1, which is where Wilson is known to be ragged, and it holds: 94–96 % coverage everywhere I could push it, against 85–92 % for the uncorrected interval. I tried to break the gap by giving it the design effects of the run it was actually measured on, and it moved in the fourth decimal. I tried to break it again with a cluster bootstrap and a permutation test that need no design effect at all, and both came back on the *favourable* side of the line — meaning the row they printed as their loss, the one where the finding fails at z = 1.84, is the one that is wrong, and they published it anyway because it was the one that cost them something. I computed the parameter-specific design effect for the shape parameter, which they flagged as their weakest operation and did not compute, and it is 1.27 against the 1.43 they used — their crudest step errs against themselves. I bootstrapped the design effect of the log odds ratio, which they assumed, and it is 1.41 against the 1.43 they assumed.

That is four attacks that failed and one confession that was too harsh on itself. It is a real result and it is buried under prose about how honest they are being. **The document would be twice as convincing at half the length, with the boasting cut and the three broken numbers fixed, and the sentence about handle drift deleted rather than defended.** Fix the numbers. Then stop telling me you fixed them.

---

## 5. Conditions, collected

| # | condition | claim |
|---|---|---|
| **I1** | Restate, or explicitly scope out with reasons, the five published intervals absent from the register: handle drift `[6.38, 8.20]`, the transfer function `[11.39, 16.55]`, the rule-of-three bound `0.0964 %`, the return rate `[0.0409, 1.2994] %`, and the session-112 governing Weibull fit `[0.4938, 0.8065]`. | C1 |
| **I2** | Attach the drop-one-page decomposition (133 of 187 both-absent pairs from one article; ratio 5.53 → 1.79) wherever the page-key pair statistic is cited. | C1 |
| **I3** | Print the account-level bootstrap interval on the pooled design effect — [1.267, 1.617] — in §1, and stop writing "at least ×1.1954". | C1 |
| **I4** | Add the two register rows missing from §3 (census cohort 2018; `INCREMENT-4` §3 attributed absence), and separate the four degenerate n ≤ 3 rows from the "36 of 36" tally. | C2 |
| **I5** | Replace "different corpora" in §4a with the overlap figures (99.1 % / 99.2 % nested; 2,127 units in all three) and state what the check actually establishes. | C3 |
| **I6** | Correct §5's range to 0.9865 – 1.6739 and the "two load-bearing cells above pooled" to one. | C4 |
| **I7** | Report a bootstrap interval beside every per-cell design effect; mark 6–7 y (1.7052), 2020 (1.6739) and 2019 (1.2663) as exceeding their own Kish ceilings, hence inadmissible; withdraw or re-caveat the 28.74 %. | C4 |
| **I8** | Replace the shared-era explanation with the conditional design effects (1.4289 → 1.3791 / 1.4136 / 1.3721 / 1.3618) and the cluster-splitting account, or refute my computation. | C4 |
| **I9** | Add the cluster bootstrap ([0.08, 8.04] across seeds) and the account-level permutation test (p = 0.0346) to §4 as a fourth row that requires no choice of design effect. | C5 |
| **I10** | Remove the 7.24 % handle drift from §7's exclusion list, restate it (design effect 1.9492, `[6.38, 8.20]` → `[6.07, 8.62]`), and re-count what the correction costs. | C1 / §7 |

Every condition is dischargeable tonight with no new measurement request. I6, I10 and the §6 parenthesis about the 2007 sculpture are corrections of fact and should be treated as blocking on any state that ships; the rest are conditions on the argument.

Claims C2, C3, C5, C6 and C7 survived direct attack against the underlying data with independently written code. Claim C1 survives with its precision and its scope corrected. **Claim C4 is broken in three of its four parts** — the range, the load-bearing count, and the explanation — with the underlying pattern intact.

---

## 6. Verdict

**STANDS WITH CONDITIONS ×10 — C2, C3, C5, C6, C7 unbroken under independent attack; C1 stands with its scope and precision corrected; C4's pattern stands but its stated range, its "two load-bearing cells above pooled", and its explanation are refuted.**
