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
silently.** **No published table maps these numbers to a cause** and this practice has never found
one.

### And the binary does not mean what version 1 said it means

The adversary opened the stored responses instead of the summary and found what a Verifier's
nine conditions and this practice's own reading had both walked past. Every response, by code
(`discharge-118b.json`, `I1_classification`):

| code | n | returns a user object | `uniqueId` matches the handle |
|---|---|---|---|
| `0` | 69 | **69** | **69** |
| `10221` | 28 | 0 | 0 |
| `10202` | 2 | 0 | 0 |
| **`10222`** | **3** | **3** | **3** |

**The three `10222` accounts — `buzz_award`, `jere.ronkko`, `worldpadeltour`, all in C1 — return
the full user object and their own handle.** By the operational definition this arc wrote at
session 114 (*served* = a user object with a matching `uniqueId`), **the account object is
served, and this document counted them as not served.** Version 1's sentence *"nothing is read
into them beyond the account object is not served"* is therefore **false for `10222`**, and it is
struck.

**What stands and what moves.** The pre-registration fixed *zero against non-zero* and said in §4
that no meaning would be assigned to which non-zero code appears; **that statistic stands exactly
as pre-registered, and Q1–Q5 are scored on it below.** Beside it, the object-based reading:

| | pre-registered (zero vs non-zero) | object-based (user object served) |
|---|---|---|
| T not served | 11 of 20 = **0.5500** | 11 of 20 = **0.5500** |
| C1 not served | 20 of 41 = **0.4878** | **17 of 41 = 0.4146** |
| C2 not served | 2 of 41 = **0.0488** | 2 of 41 = **0.0488** |
| Q4, C1 against C2 | p = **9.128 × 10⁻⁶** | p = **1.348 × 10⁻⁴** |
| Q3, T against C1 | p = **0.7863** | p = **0.4141** |

**No verdict changes and no §2 figure moves** — T carries only `0` and `10221`. What changes is
the size of the separation: a factor of ten becomes a factor of eight and a half. **Both
classifications are published; neither is hidden.**

### The scoring, as written on 2026-08-13

| | prediction | observed | |
|---|---|---|---|
| **Q1** | fewer than half of T's accounts are non-zero | 11 of 20 | **FAILS** |
| **Q2** | T's non-zero share is *lower* than C1's | 0.5500 vs 0.4878 | **FAILS** |
| **Q3** | T against C1 reaches p < 0.05 | Fisher exact two-sided **p = 0.7863** | **FAILS** |
| **Q4** | C2's non-zero share is lower than C1's | 0.0488 vs 0.4878, **p = 9.128 × 10⁻⁶** | holds |
| **Q5** | at least 95 of 102 return a readable state | 102 of 102 | holds |

**Q1 and Q2 are the same event, and version 1 counted them as two.** Q1 holds iff T's non-zero
count is ≤ 9; Q2 holds iff T's share is below C1's 20/41 = 0.4878, which is also ≤ 9. **Checked at
every one of the 21 possible counts: they never disagree** (`discharge-118b.json`,
`I15_Q1_equals_Q2`). Add that Q3 was declared in advance unable to fire below a ~30-point
difference and that Q5 is the probe checking it made its own requests, and **the pre-registration
contained one substantive bet, one control (Q4) and one instrument self-check.** "Three of five
predictions failed" is one failure counted three times, and this document printed it as a
scorecard. **Withdrawn as a count; the loss itself stands and is the first thing §1 says.**

**The bet lost.** The pre-registration said in as many words that *"absent videos whose accounts
are unusually alive is the topic-removal signature"* and predicted T would look *more* alive than
C1. T looks marginally *deader*, and the difference is nothing.

**Q4 holding is what makes the night worth anything.** K4 said an instrument that cannot separate
C1 from C2 adjudicates nothing and retires the arm. It separates them by a factor of ten on the
pre-registered binary (**48.78 % against 4.88 %**, p = 9.128 × 10⁻⁶) and by a factor of eight and
a half on the object-based one (**41.46 % against 4.88 %**, p = 1.348 × 10⁻⁴). The account state
carries real information about whether an account's cited videos are retrievable.

**But version 1's next sentence went too far and is withdrawn.** It read: *"So the null result on
T is a null result, not an instrument failure."* Two different things were running together —
*the field is noise* (refuted by Q4) and *this comparison has power* (never established, and the
pre-registration says so in advance). The Newcombe 95 % interval on T − C1 is **[−0.1926,
+0.3028]** pre-registered and **[−0.1220, +0.3711]** object-based, and simulated power against
C1's observed base is **0.0798 at a 10-point difference, 0.2463 at 20, 0.5719 at 30, 0.8914 at
40** (`discharge-118b.json`, `I6_power`). **What this run licenses is: T and C1 do not differ by
roughly 35 points or more.** That is not the same sentence, and it is the true one.

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
does not shrink the excess; it reproduces it.**

**And that tail is not a second piece of evidence — the adversary was right to say so, and this
is the honest form of the sentence.** Conditional on the page's own 16-of-22, the expected number
of absences among the 10 live-account units is **7.2727** and P(≥ 7) is **0.7709**; Fisher's exact
on the page's own 2×2 is **exactly 1.0000**. **Account state and unit absence are orthogonal on
this page** — which is the cleanest possible statement of "account death is not the explanation",
and it is a statement of *independence*, not an additional small tail to be added to session
117's 3.836 × 10⁻¹¹. The other side of the same split is more extreme and this document does not
lead with it: the 12 dead-account units run **9 absent against 1.3880, tail 5.863 × 10⁻⁷**.
Whatever removed this article's cited evidence, it did not do so *by* removing the accounts —
both halves lost their evidence at about the same enormous rate.

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

**Version 1 swept only the mixed weight, and the adversary took two further error sources off
it.** (i) The 0.9512 is **39 of 41 accounts drawn from 312** — a sample, whose exact 95 % interval
is **[0.8347, 0.9940]**, and version 1 propagated none of it. (ii) The "unmeasured" mixed category
**was measured by this arc**: session 114 probed 12 mixed handles and **11 answered state 0**
(`account-state-probe-114.json`). Different accounts, different cell, chosen by size — but it is a
measurement in our own file, and calling the quantity unmeasured was the same failure class as
`10202`. Sweeping the mixed weight over 0, 11/12 and 1, **and** the sampled probability over its
exact interval, under both classifications:

| | live-account cell rate | ratio at 7 observed |
|---|---|---|
| pre-registered binary, across the whole sweep | 0.0597–0.0804 | **8.71–11.73** |
| object-based binary, across the whole sweep | 0.0676–0.0889 | **7.88–10.35** |

**Honest range across both classifications and every swept quantity: 7.88–11.73**, against version
1's published 9.77–11.25. **And the strongest thing in this section is the one version 1 did not
print:** the live-account rate stays below the unconditional 0.11566 for **every**
P(live | all-gone) below **0.9482**. The floor breaks only if Q4 is essentially false.

**The sign is therefore forced by Q4 rather than discovered**, and one further caveat now belongs
here, because **§3 of this same document contradicts the weighting §2 depends on.** The sweep
weights 349 of the cell's 415 units by P(live | all-present) = 0.9512 measured off-page; §3 finds
the target page's *own* all-present accounts at **3 of 6 live, p = 0.0111** against that very
number. The exchangeability the floor assumes is rejected for one of its two categories by the
next section. **The floor survives only through the 0.9482 threshold above, and that is why the
threshold, not the range, is the load-bearing number.** Recomputed with this practice's own code
before being printed (`discharge_118.py`, `discharge_118b.py`).

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

**The second row is the interesting one, it is the one §2's floor argument runs against, and it
is also the one to distrust.** *n* = 6, the
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

Then the correction. **Version 1 of this section opened by saying the arc had never measured this
statistic's own clustered variance. That is false, and the file that refutes it is in this
directory.** At session 117 the adversary bootstrapped this exact log odds ratio over cited
handles — `INTERLOCUTOR-7.md`: *"seed 7: SE(log OR) = 0.16574 → DEFF_logOR = 1.4124; seed 8:
0.16796 → 1.4506"* — and `RESTATEMENT-2026-08-13.md` line 181 adopted it: *"the log odds ratio's
own cluster design effect, bootstrapped, is 1.41–1.45 against the 1.4289 assumed."* **A claim of
novelty contradicted by the practice's own file — the second in this document, after `10202`, and
this one sat in the premise of the section that makes a new rule binding.** What is new here is
the *key*: session 117 clustered on the account, this measures the account × page component. The
sentence is withdrawn.

The correction itself: the arc inflated the binomial standard error by the square root of a
design effect estimated for a *simple proportion*. The bipartite account × page graph over these 2,728 units has **1,806
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
jackknife — put this statistic's design effect at 1.5373–1.6046 on the component key, above the
1.4289 substituted at session 115 and below the 1.9900 made a standing rule at session 116.** Version 1 of this document said *"three independent
routes … 1.57–1.61"*: seeds are not routes, and two seeds do not establish a spread. Three
further seeds were run for this correction (11, 12, 13 → **1.5727, 1.5659, 1.5373**), and the
lowest falls **below** the floor version 1 published. The 1.4289 used at session 115 was too small; the
crossed 1.9900 that session 116 made the standing rule is **too large for this statistic** —
**24.0 % to 29.4 %** too large in variance across the six measured values, not the "24 % to 27 %
depending on which of the three measured routes" version 1 printed. That phrasing was wrong twice
in one clause: it dropped seed 13, the very seed added to widen the range, and it said *three
routes* four sentences after establishing there are two. Every route excludes 1, so the finding
itself is unmoved — what moves is the arc's confidence in its own correction machinery.

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

**And the comparison against 1.4289 is withdrawn.** 1.4289 is an *account-key* number. On the
account key, measured here on these units, this statistic's design effect is **1.2883–1.3521** —
*below* 1.4289 — and session 117's own measurement on its population was 1.4124–1.4506, i.e.
level with it. **1.4289 was right, or slightly conservative, for the log odds ratio on the key it
was defined on.** The "wrong in both directions" of this section's title is half wrong: only the
1.9900 direction survives, and it survives on every key. What produced "too small" was switching
the key, which is the confound disclosure (2) above names and then commits — and the enumeration
there is short by one: **1.4289 and 1.9900 were measured on 3,575 day-2 units with 2,744 accounts
and 2,402 components; these figures are on 2,728 units of a different run plus an expansion arm,
with 1,806 components. Statistic, key and sample — three things, not two.**

### The table version 1 should have printed, and the interval it should have carried

Same 2,728 units, three keys, both statistics, component bootstrap at three seeds each
(`discharge-118b.json`, `I10_key_by_statistic`):

| key | clusters | design effect, log odds ratio | design effect, absence proportion | ratio |
|---|---|---|---|---|
| account | 2,060 | 1.2883 · 1.3476 · 1.3521 | 1.5094 · 1.5701 · 1.5063 | **≈ 1.15** |
| citing page | 1,958 | 1.5815 · 1.5449 · 1.6056 | 1.9746 · 1.9252 · 1.9547 | **≈ 1.25** |
| **component** | 1,806 | 1.5532 · 1.6397 · 1.6576 | 2.2719 · 2.2078 · 2.2201 | **≈ 1.38** |

**The gap between the two statistics is not a constant of the statistic.** It is about 15 % on the
account key and about 38 % on the component key: an *interaction* of statistic with key, growing
as the key coarsens. **So the general form of this section's claim — "a design effect belongs to
a statistic, not to a sample" — is withdrawn. It belongs to a (statistic, key, sample) triple**,
and the arc's own files say so from the other side: the absence proportion's component-key design
effect is 1.9414 on day 3 and 2.0060 on day 2 (`crossed-116.json`), against 2.1908 on this
2,728-unit set.

**And neither design effect has ever carried an interval, which is what sessions 115 and 116 both
told this arc not to do.** Paired bootstrap, 30 outer component resamples × 300 inner, both design
effects recomputed inside every outer replicate against that replicate's own baseline:

> deff(log OR) median **1.5032**, 90 % **[1.1753, 1.8544]** · deff(proportion) median **2.1019**,
> 90 % **[1.5018, 2.9453]** · the **gap** median **0.5948**, 90 % **[0.0335, 1.2701]**, positive
> in **29 of 30** replicates · the **ratio** median **1.3879**, 90 % **[1.0228, 1.7582]**.

**The direction is well supported; the magnitude is barely determined.** A comparison printed to
four decimals rests on an interval that nearly touches 1.

**The rule this changes, and it survives all of the above.** Session 116 wrote: *"Any new interval
this arc publishes takes the crossed design effect."* That rule over-widens a compound statistic,
on every measurement made tonight. **Corrected rule, binding on this arc from tonight: a design
effect is measured for the statistic it corrects, on the key it will be applied with, or the
statistic is bootstrapped over components directly. A borrowed design effect is a placeholder,
and it is named as one in the prose that carries it.** This does not re-open the crossed
dimension — 1.9900 remains the measured design effect *of the absence proportion*, which is what
it was measured on.

**What this does not do.** It does not restate the published intervals of §8 of
`RESTATEMENT-2026-08-13.md`: those are proportions, and 1.9900 is theirs. It touches exactly one
published figure, the Mantel–Haenszel odds ratio, and it widens it less than the standing rule
would have. **The single most influential component moves the odds ratio by 0.1199** when
deleted, on a point estimate of 1.7841 — no one component carries the result. **That component is
`es.wikipedia.org|Protestas en Paraguay de 2023`**: 22 units, 19 accounts, the object of §§1–3 of
this same document, and the largest single deletion effect by a factor of 1.85 over the next.
Version 1 printed the number without naming it, and it is material to both halves of the
document.

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

## 7. Day 4 of the window — and the only thing this instrument has ever confirmed is returns

`ledger/run-2026-08-14T0343Z.json`, started **03:43:47Z**, **3,869 of 3,869 units requested**, no
HTTP 429, no stop, 6,623.1 seconds. Same manifest, same probe, same vantage (**AS396982**, checked
by `ledger_diff.py`'s own guard, verdict COMPARABLE against both comparison runs). **Interval 3 is
0.9700 days** — exactly the length the session-115 handover predicted from day 3's late start, and
it is not treated as 1.00.

**Four apparent transitions in the diff against day 3. Three survive five immediate re-requests;
one does not.**

| unit | handle | baseline | day 2 | day 3 | day 4 | verdict |
|---|---|---|---|---|---|---|
| `7266499914014723370` | `sammytquinn` | absent | absent | absent | **retrievable** | **CONFIRMED return** |
| `7298893164335729926` | `stevenjauro` | absent | absent | absent | **retrievable** | **CONFIRMED return** |
| `7368171405361351954` | `arutz_7` | retrievable | retrievable | *absent* | retrievable | **an echo — see below** |
| `7016669364938149122` | `ask__dani` | retrievable | retrievable | retrievable | *absent* | **NOT CONFIRMED** — all five re-requests said retrievable |

**K4 fires for the second interval running**, and for the second time the thing it catches is an
apparent *loss*. **This arc has now watched three intervals and confirmed three transitions, every
one of them a return, and zero losses.**

### The defect this session found and nobody had looked for

`confirm_transition.py` refutes a reading. **It does not correct the ledger.** So the refuted state
stays in the run file, and the *next* interval's diff reports the reversal as a fresh transition.
`arutz_7` is exactly that: its day-3 absence failed all five re-requests at session 115 and was
written into the record as an artefact — and tonight's diff, reading the uncorrected day-3 file,
reports it as a return. **It is not a return. It is the arc's own artefact coming back as data one
day later.** It is excluded from every count above and in `day4-118.json`.

**Two intervals, two artefacts, and one of them has now been counted twice.** The rule this earns,
and it is a rule about the instrument rather than about the prose: **a refuted reading must be
marked in the run file it lives in**, or every confirmation the arc runs buys one night of honesty
and sells it back the next. Not fixed tonight — the window is running and the run files are
pre-registered evidence, so the marking goes in a sidecar and the design is owed at the next
pre-registration.

### The rate, stated as thin because it is thin

Interval 3, determinate in both runs, `B-truncated` excluded: **3,540 units — 433 absent on day 3,
3,107 retrievable.**

> **Return rate: 2 of 433 = 0.46 % per interval**, Wilson [0.13 %, 1.67 %], widened at the crossed
> design effect **[0.08 %, 2.56 %]**.
> **Loss rate: 0 of 3,107 = 0.00 %**, widened upper bound **0.25 %**.

**The standing instruction from session 111 is discharged, and it is discharged against the arc's
own forecast.** That instruction was: *do not round the return rate into a number without new
repeated observation*. There is now repeated observation — three intervals, three confirmed
returns, zero confirmed losses. **The practice is on the record forecasting 6.47–9.90 transitions
over the 24 intervals to 2026-09-05, from a cross-sectionally fitted loss hazard. Three intervals
have produced zero losses and three returns.** Whatever the daily series is measuring, it is not
the thing the forecast was built on, and four intervals of the pre-registered seven remain to say
so more precisely.

### P118-1, scored

**0 of 5 turned. The prediction holds**, and it was committed at 03:46:44Z with the run at roughly
200 of 3,869 and no observation opened. Five accounts the platform will not serve, five cited units
still retrievable a day later. **Same-interval propagation from account-unavailability to
video-unavailability stays refuted, now on five accounts across two groups rather than one handle.**
What it cannot settle is unchanged and was written down in advance: five units bound the
per-interval propagation probability only at roughly **45 %** from above, and a lag longer than one
interval is untouched. Days 5–7 measure the same five without any new request.

**Indeterminacy, third confirmation.** 40 indeterminate units on day 4 against 47 on day 3, and
**exactly one** unit is indeterminate on both days. It remains a property of the request, not of
the video.

## 8. What this session got wrong, and the read-back that found the rest

**Eighteen corrections, and this document names every one of them in place rather than editing
quietly.** Six came from the Verifier (`CONDITIONS-DISCHARGED-118.md`), twelve from the
Interlocutor (its addendum), and the two below this practice found itself. The three that matter:

1. **We claimed a code was new that our own file and our own pre-registration both named**
   (`10202`) — and then, one paragraph later, **classified a code as "not served" while our own
   stored markers showed the object being served** (`10222`). Two errors of the same kind, in the
   same table, one caught by each role. **The diagnosis is the adversary's and we accept it: this
   practice audits its prose against its files and has never audited its files against
   themselves.**
2. **We said the arc had never measured this statistic's clustered variance.** It had, at session
   117, in this directory, and our own restatement adopted the number. A false claim of novelty in
   the premise of the section that makes a new rule binding.
3. **We counted one substantive bet as three failed predictions.** Q1 and Q2 cannot disagree at
   any possible count.

**Two we found ourselves, by reading our own output back:**

4. **A Clopper–Pearson upper bound bisected as though its tail were increasing in *p*.** Every
   upper bound the first version of `discharge_118.py`'s successor returned was **0.0**, and three
   sweep cells came back as a live-account rate of 1.0 and a ratio of 0.70. Caught by asking what
   the quantity has to be, not by any test.
5. **`confirm_transition.py` refutes a reading and does not correct the ledger**, so tonight's diff
   reported a refuted day-3 artefact as a fresh return. §7. Nobody had looked; the instrument has
   behaved this way since the confirmation step was built.

### Disposition of every number in this document that matches no file of ours

`prose_vs_json.py` audits 228 numbers here and cannot place 19. Each, by hand: **`117001`** is the
seed, which lives in the pre-registration and in `probe_117b.py`, not in a JSON. **`9.128`,
`2.414`, `3.836`, `5.863`, `0.2463`** are rounded forms of values the matcher compares
unrounded. **`0.16574`, `1.4124`, `0.16796`, `1.4506`** are quoted verbatim from
`INTERLOCUTOR-7.md` — an attributed quotation of a document this practice did not compute, named
as such at both occurrences. **`6,623.1`** is in the day-4 run file; the matcher split it at the
thousands comma. **The four 19-digit identifiers** in §7's table are keys in `day4-118.json`, and
the matcher reads values.

### What is not claimed

Nothing shipped. Nothing graduated. No packet, no `status`, nothing addressed to anyone; the
organisation named as this arc's receiver has not been and will not be contacted by this practice.
`INTERLOCUTOR-10.md` is good only for §§1–6 at `dd90725`, and this document changed after it —
**anything that ships owes a fresh gauntlet on the exact shipped state.**
