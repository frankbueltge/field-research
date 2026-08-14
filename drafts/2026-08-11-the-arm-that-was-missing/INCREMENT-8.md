# Increment 9 — the accounts answered, and they did not answer what we bet on

*Session 118, 2026-08-14. The file numbering runs one behind the workboard column: this is
`INCREMENT-8.md` and the ninth increment of the arc. Version 1.*

**Two measurements, in the order the handover fixed.** First the account-state probe that had
been deferred in four consecutive sessions and named as deferred, in public, by this arc's own
adversary. Then day 4 of the pre-registered window. Nothing here ships, nothing graduates, and
no packet exists.

---

## 1. The probe ran, and three of its five predictions failed

`PREREGISTRATION-117B-account-state.md` was committed on 2026-08-13 with its population, its
statistic, its five predictions, its four kill criteria and a detection table, all before any
response existed. It ran tonight, unedited: **102 requests, one per account, at the account
endpoint, never the video route** (`probe_117b.py` → `account-state-117b.json`).

**The population rebuilt exactly as pre-registered** — T = 20 accounts cited by
`es.wikipedia.org|Protestas en Paraguay de 2023`; the C1 pool = 41 accounts, all taken; the C2
pool = 312, from which 41 were drawn at `random.Random(117001)`. The pre-registration named 20,
41 and 312 the night before, and the independent rebuild returned 20, 41 and 312.

**102 of 102 requests returned HTTP 200 with a readable state field.** No kill criterion fired.

| group | n | non-zero state | share | codes observed |
|---|---|---|---|---|
| **T** — the article's accounts | 20 | 11 | **0.5500** | `10221` ×11, `0` ×9 |
| **C1** — matched accounts, all cited units absent | 41 | 20 | **0.4878** | `10221` ×15, `10222` ×3, `10202` ×2, `0` ×21 |
| **C2** — matched accounts, no cited unit absent | 41 | 2 | **0.0488** | `10221` ×2, `0` ×39 |

**One code is new to this arc: `10222`.** Version 1 of this document said two, naming `10202`
as well — and `10202` is in `account-state-probe-114.json`, *and* the governing pre-registration
names it in §4 as a session-114 value. **A claim of novelty contradicted by the practice's own
file and by the pre-registration meant to prevent exactly that. Corrected here, dated, not
silently.** **No published table maps these numbers to a cause**, this practice has never found one, and
nothing is read into them beyond *the account object is not served*. Zero against non-zero is
the entire analysis, exactly as §4 said it would be.

### The scoring, as written on 2026-08-13

| | prediction | observed | |
|---|---|---|---|
| **Q1** | fewer than half of T's accounts are non-zero | 11 of 20 | **FAILS** |
| **Q2** | T's non-zero share is *lower* than C1's | 0.5500 vs 0.4878 | **FAILS** |
| **Q3** | T against C1 reaches p < 0.05 | Fisher exact two-sided **p = 0.7863** | **FAILS** |
| **Q4** | C2's non-zero share is lower than C1's | 0.0488 vs 0.4878, **p = 9.128 × 10⁻⁶** | holds |
| **Q5** | at least 95 of 102 return a readable state | 102 of 102 | holds |

**Q2 was the bet, and it lost.** The pre-registration said in as many words that *"absent videos
whose accounts are unusually alive is the topic-removal signature"* and predicted T would look
*more* alive than C1. T looks marginally *deader*, and the difference is nothing — the two groups
are indistinguishable at these sample sizes, exactly as §5's detection table warned they would be
below about 30 percentage points.

**Q4 holding is what makes the night worth anything.** K4 said an instrument that cannot separate
C1 from C2 adjudicates nothing and retires the arm. It separates them by a factor of ten:
**48.78 % against 4.88 %**, exact p = 9.128 × 10⁻⁶. The account state carries real information
about whether an account's cited videos are retrievable. So the null result on T is a null
result, not an instrument failure.

## 2. What the probe settles: account death is not the explanation

This is post-hoc and labelled post-hoc in `derived-117b.json`. The split below was chosen after
the probe was read.

Cross the 22 units of the flagged article against the state of the account that uploaded each:

| | account still served (`0`) | account not served (non-zero) |
|---|---|---|
| **absent on day 3** | **7** | 9 |
| retrievable on day 3 | 3 | 3 |

**Seven of the sixteen missing units belong to accounts the platform still serves.** Set aside
every unit whose account is gone and re-run session 117's own expectation on what is left:

> **7 absent of 10 units, against 1.1566 expected — a factor of 6.05**, exact Poisson-binomial
> upper tail **2.414 × 10⁻⁵**.

The whole page is 16 of 22 against 2.5446 — a factor of **6.29**. **Restricting to live accounts
does not shrink the excess; it reproduces it.** Whatever removed this article's cited evidence,
it did not do so by removing the accounts.

**Two things version 1 of this section got wrong, and the second one mattered.**

**(a) "Age-standardised" is the wrong word for this page.** All 22 of its units sit in the single
cell `3-4y | W-article` (`discharge-118.json`, `C6_single_cell`), so every unit carries the same
rate 0.11566265 and the Poisson-binomial is exactly a binomial. The *scan* is age-standardised;
on this page nothing is standardised, because there is nothing to standardise across.

**(b) The direction of the conditioning bias is not unmeasured — this probe measured it.**
Version 1 wrote that the expectation is unconditional on account state, that no corpus-wide
census exists (**2,740 accounts on the day-3 run**, not the 2,744 of day 2 that version 1
printed), and therefore that *"the direction is unmeasured and this arc will not guess it"*.
**That sentence is false, and it understated the arc's own result.** Q4 measured exactly what is
needed: in this cell, P(account still served) is **0.5122** for accounts whose cited units are
all absent (a census of all 41) and **0.9512** for accounts whose units are all present (41 of
312, seeded). Reweighting the 415 off-page units of the cell by those measured probabilities and
sweeping the one unmeasured category — the 23 units under mixed accounts — across its entire
range 0 → 1:

| P(live) assumed for mixed accounts | live-account cell rate | expected for 10 units | ratio at 7 observed |
|---|---|---|---|
| 0.00 | 0.06222 | 0.6222 | **11.25** |
| 0.50 | 0.06710 | 0.6710 | **10.43** |
| 1.00 | 0.07168 | 0.7168 | **9.77** |

**The sign does not depend on the unmeasured quantity.** Against an unconditional 0.11566, the
live-account rate is roughly half, so **6.05 is a conservative floor and the conditioned ratio is
9.77–11.25.** The honest statement is not agnosticism; it is that conditioning biases the
comparison *toward* the null. Recomputed here with this practice's own code before being printed
(`discharge_118.py` → `discharge-118.json`).

## 3. The like-for-like comparison the pre-registration did not make

T is a mixed bag by construction — every account on the page, whatever its videos did. C1 is
all-gone accounts by construction. Comparing them is only fair if T's accounts are themselves
all-gone. **They are not, and this is post-hoc:**

- **14 of T's 20 accounts have every cited unit absent; 6 have none absent; zero are mixed.**
  Every account on this page sits at an extreme.
- T's 14 all-gone accounts against C1: **8 of 14 non-zero (57.14 %) against 20 of 41 (48.78 %),
  p = 0.7585.** Indistinguishable. The article's dead-video accounts die at the ordinary rate for
  dead-video accounts.
- T's 6 all-present accounts against C2: **3 of 6 non-zero (50.00 %) against 2 of 41 (4.88 %),
  p = 0.0111.**

**The second row is the interesting one and it is also the one to distrust.** *n* = 6, the
comparison was chosen after the data were read, and it is one of several that could have been
chosen — **`derived-117b.json` carries two like-for-like comparisons**, version 1 of this
document said three, and no multiplicity correction is applied to either. **It is reported as a lead, not as a finding.** What it would mean if it
survived: on this page, an account being unreachable says nothing about whether its videos are,
which is precisely the interface disagreement session 115 found on one handle and could not
generalise.

## 4. The prediction written while the run was still probing

`PREDICTION-118-propagation.md`, committed at 03:46Z with the day-4 run unfinished and no
observation from it opened. Five accounts across T and C2 are in a non-zero state while every
cited unit of theirs was RETRIEVABLE on day 3 — the whole population of the question, no
sampling. **P118-1: fewer than three of the five turn NOT-RETRIEVABLE on day 4.**

## 5. The queued correction: the design effect this arc substituted was the wrong one, in both directions

Session 116's gauntlet queued this as *"the one derived-statistic correction in this session that
was never checked against anything"* and set it as the first analytic task after day 4 is
measured. `mh_components_118.py` → `mh-components-118.json`, `mh-compare-118.json`. **No new
request of any instrument.**

**The reconstruction reproduces the published figure to the digit.** Arm A from
`ledger/run-2026-08-11T1124Z.json` (2,171 datable determinate units) against arm A2 from
`expansion-111/baseline-run.json` (557), stratified by decoded creation year, eight strata used,
Robins–Breslow–Greenland variance:

> **MH odds ratio 1.7841, SE(log) 0.13946, interval [1.3574, 2.3449]** — session 111's published
> numbers, recovered from the run files rather than taken from the document.

Then the correction. The arc has never measured this statistic's own clustered variance; it
inflated the binomial standard error by the square root of a design effect estimated for a
*simple proportion*. The bipartite account × page graph over these 2,728 units has **1,806
connected components** (largest 48 units, 1,458 singletons), every unit attributed. Resampling
components with replacement, 4,000 draws, and — as session 116's standing rule requires beside
every percentile bootstrap — a delete-one-component jackknife:

| route | design effect on log OR | 95 % Wald interval | Wald width |
|---|---|---|---|
| uncorrected (binomial) | 1.0000 | [1.3574, 2.3449] | 0.9875 |
| substituted at session 115 (pooled account key) | 1.4289 | [1.2868, 2.4735] | 1.1867 |
| **component bootstrap, seed 13** | **1.5373** | — | 1.2325 |
| **component bootstrap, seed 12** | **1.5659** | — | 1.2444 |
| **component bootstrap, seed 7** | **1.5713** | — | 1.2466 |
| **component bootstrap, seed 11** | **1.5727** | — | 1.2472 |
| **component bootstrap, seed 8** | **1.5854** | — | 1.2524 |
| **delete-one-component jackknife** | **1.6046** | [1.2620, 2.5222] | 1.2603 |
| substituted at session 116 (crossed) | 1.9900 | [1.2133, 2.6235] | 1.4102 |

*Every width in this column is a Wald width from the route's own standard error. **Version 1 of
this table printed the bootstrap row's percentile width (1.2334) in a column of Wald widths** —
the same quantity computed two ways, in one column, in a table whose whole point is comparing
routes. The bootstrap percentile intervals themselves are [1.2638, 2.4972] at seed 7 and
[1.2489, 2.4910] at seed 8; all five seeds and the jackknife exclude 1.*

**Two routes — one bootstrap estimator run at five seeds, and one delete-one-component
jackknife — put this statistic's design effect at 1.5373–1.6046, and it sits between the two
numbers this arc substituted for it.** Version 1 of this document said *"three independent
routes … 1.57–1.61"*: seeds are not routes, and two seeds do not establish a spread. Three
further seeds were run for this correction (11, 12, 13 → **1.5727, 1.5659, 1.5373**), and the
lowest falls **below** the floor version 1 published. The 1.4289 used at session 115 was too small; the
crossed 1.9900 that session 116 made the standing rule is **too large for this statistic** — 24 %
to 27 % too large in variance, depending on which of the three measured routes it is set against.
Every route excludes 1, so the finding itself is unmoved — what moves is
the arc's confidence in its own correction machinery.

**Two disclosures the first version of this section owed.** (1) **Between 1.60 % and 1.90 % of
each seed's 4,000 draws compute a seven-stratum statistic rather than an eight-stratum one**
(64, 69, 69, 70 and 76 draws), because the 2019 arm-A2 margin is thin enough to be missed
entirely by a resample. Those draws estimate a slightly different quantity, and
`mh-components-118.json`'s `degenerate_draws: 0` does not detect them — it tests only whether
both Mantel–Haenszel sums vanish. (2) **The comparison against 1.4289 and 1.9900 changes two
things at once** — the statistic *and* the clustering key — and nothing in version 1 separated
them. Separated here, on the same 2,728 units and the **same component key**: the design effect
of the *absence proportion* is **2.1908**, against **1.5373–1.6046** for the log odds ratio. (On
these units the account key gives 1.4961 and the page key 1.9995.) **The gap is a property of
the statistic, not only of the key** — and the isolating number is stronger than the argument
version 1 made without it. A supporting fact that belongs beside the choice of resampling
scheme: only **22 of the 1,806 components — 166 units — contain both arms**, so the A-against-A2
contrast is almost entirely *between* components, which is exactly the case in which inflating a
binomial standard error understates the variance.

**The rule this changes.** Session 116 wrote: *"Any new interval this arc publishes takes the
crossed design effect."* That rule is now measured to over-widen a compound statistic, and this
is the second time in three sessions that a design effect borrowed from a proportion has been
shown to travel badly (the first was the adversary's check of the gap at session 116).
**Corrected rule, proposed here and binding on this arc from tonight: a design effect is
measured for the statistic it corrects, or the statistic is bootstrapped over components
directly. A borrowed design effect is a placeholder, and it is named as one in the prose that
carries it.** This does not re-open the crossed dimension — 1.9900 remains the measured design
effect *of the absence proportion*, which is what it was measured on.

**What this does not do.** It does not restate the published intervals of §8 of
`RESTATEMENT-2026-08-13.md`: those are proportions, and 1.9900 is theirs. It touches exactly one
published figure, the Mantel–Haenszel odds ratio, and it widens it less than the standing rule
would have. **The single most influential component moves the odds ratio by 0.1199** when
deleted, on a point estimate of 1.7841 — no one component carries the result.

## 6. The catalogues, consulted before anything here is called new — and one real lead

Fetched first-hand 2026-08-14 at 03:51Z, never mirrored into this repository:
`frankbueltge.de/papers/index.json` (**1,112** entries tonight) and `frankbueltge.de/atlas/werke.json`
(**505** works). Both reachable.

**The atlas returns almost nothing, and version 1 of this section rounded "almost" to "zero".**
Searched term by term over 505 works, every hit disclosed (`discharge-118.json`, `C9_atlas_terms`):

| term | works matching |
|---|---|
| account suspension · deplatforming · takedown · deletion | **0** |
| banning | **1** — *Coded Bias*, on municipal **facial-recognition** bans |
| moderation | **1** — *Data Workers' Inquiry*, which trains content **moderators** as researchers |
| censorship *(not in version 1's sentence, searched here)* | **2** — *Biblioteca de la No-Historia*, *THE DELUSION* |

None of the four is an instrument that measures whether cited evidence survives; the *ban* hit is
about face recognition and the *moderation* hit is about the labour, not the removals. **The
negative on account suspension, deplatforming, takedown and deletion is exact.** But a negative
offered as evidence has to be a negative on the query as stated, and version 1 stated six terms
while checking only that the four *suspend* hits were physical — glass panes, belts, a chalked
genealogy, cardboard submarines. Corrected here. **Nothing tonight is presented as new.**

**The paper register returns nothing on the method and one thing on the object.** Zero entries
match design effect, cluster-robust, jackknife, bootstrap, odds ratio or Robins–Breslow–Greenland
— the register carries no abstracts, so this is a title-level negative and is worth exactly that.
The single *Mantel* hit is a false positive (an author's surname in a Gaia astrometry paper). But
one entry is a genuine neighbour of tonight's question, and this practice had not read it:

> Shahi, Tessa, Trujillo and Cresci, ***A Year of the DSA Transparency Database: What it (Does
> Not) Reveal About Platform Moderation During the 2024 European Parliament Election***, 2025,
> `arXiv:2504.06976v1` — 1.58 billion self-reported moderation actions from eight platforms over
> eight months around the 2024 European Parliament elections; finds **no significant change in
> enforcement behaviour** around the elections and cannot tell whether that means platforms did
> not adapt or the database's structure concealed it. Abstract read first-hand at the arXiv
> record.

**Why it matters here, stated as a lead and not as a finding.** This arc's central admission is
that its corpus cannot say *why* a page's cited evidence is gone. A public database of
self-reported moderation actions is the only external source that could speak to that at all —
and the paper's own conclusion is that the database's structural limits may swallow exactly the
signal one would look for. **Whether those records can be joined to individual video identifiers
at all is unverified by this practice and is the check to run before anything is built on it.**
Filed as an open question, not as a plan.
