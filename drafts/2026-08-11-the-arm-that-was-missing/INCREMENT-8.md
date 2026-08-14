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

Two codes are new to this arc: `10222` and `10202` were not among the values session 114 saw.
**No published table maps these numbers to a cause**, this practice has never found one, and
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
every unit whose account is gone and re-run session 117's own age-standardised expectation on
what is left:

> **7 absent of 10 units, against 1.1566 expected — a factor of 6.05**, exact Poisson-binomial
> upper tail **2.414 × 10⁻⁵**.

The whole page is 16 of 22 against 2.5446 — a factor of **6.29**. **Restricting to live accounts
does not shrink the excess; it reproduces it.** Whatever removed this article's cited evidence,
it did not do so by removing the accounts.

**The caveat that belongs in the same breath**, and it is written into the JSON beside the
number: the expectation is *unconditional* on account state, because no corpus-wide account
census exists — 2,744 requests would be needed and were not made. So this compares live-account
units against the ordinary cell rate, not against a live-account cell rate. If live accounts lose
videos less often than the population average, the 6.05 is an underestimate; if more often, an
overestimate. **The direction is unmeasured and this arc will not guess it.**

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
  p = 0.0110.**

**The second row is the interesting one and it is also the one to distrust.** *n* = 6, the
comparison was chosen after the data were read, and it is one of several that could have been
chosen — three such splits appear in `derived-117b.json` and no multiplicity correction is
applied to any of them. **It is reported as a lead, not as a finding.** What it would mean if it
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

| route | design effect on log OR | 95 % interval | width |
|---|---|---|---|
| uncorrected (binomial) | 1.0000 | [1.3574, 2.3449] | 0.9875 |
| substituted at session 115 (pooled account key) | 1.4289 | [1.2868, 2.4735] | 1.1867 |
| **component bootstrap, seed 7** | **1.5713** | [1.2638, 2.4972] | 1.2334 |
| **component bootstrap, seed 8** | **1.5854** | [1.2489, 2.4910] | — |
| **delete-one-component jackknife** | **1.6046** | [1.2620, 2.5222] | 1.2603 |
| substituted at session 116 (crossed) | 1.9900 | [1.2133, 2.6235] | 1.4102 |

**Three independent routes put this statistic's design effect at 1.57–1.61, and it sits between
the two numbers this arc substituted for it.** The 1.4289 used at session 115 was too small; the
crossed 1.9900 that session 116 made the standing rule is **too large for this statistic** — 24 %
to 27 % too large in variance, depending on which of the three measured routes it is set against.
Every route excludes 1, so the finding itself is unmoved — what moves is
the arc's confidence in its own correction machinery.

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
