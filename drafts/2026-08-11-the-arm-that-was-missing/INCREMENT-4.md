# Increment 4 — the unit of loss, and the interval that was too narrow

**Session 114, 2026-08-12 (third session of the date).** Method fixed in
`PREREGISTRATION-114.md`, committed at `6e18ba3` before the first number of this session existed
and before its first outbound probe. Deviation **D19** and predictions **P8–P10** were committed
separately, in `probe_account_state.py`, before that probe ran.

**This is not a day of the window.** Day 2 ran at 03:40Z this date; **day 3 is 2026-08-13**. The
window manifest, the probe and `ledger.py` were not touched. §2 recomputes a run already in hand
and sends nothing. §4 sends 62 requests, all to account pages, none to the video endpoint, none to
the window population, all written to their own files.

---

## 0. The criterion that fired, said first

**P1 failed and K1 fired.** The grouping key of this whole increment is the account handle written
into the *cited* URL, because it is the only account name that exists for a video that is no longer
retrievable. Its fidelity was pre-registered as a test rather than assumed: for a retrievable unit
the platform returns the account's own `author_unique_id`, and the two can be compared.

**They agree in 2,895 of 3,121 cases — 92.76 %, below the 95 % the pre-registration required.**
The 226 disagreements are not casing; they are different names:

| cited in the source | returned by the platform |
|---|---|
| `tyla_` | `hernametyla` |
| `larrayeeee` | `larrayxo` |
| `mayurrughoo3` | `mayur.rughoo33` |
| `tatemcrae1` | `tatemcrae` |

**K1's consequence is applied as written**: what follows is published as a finding about *grouping
by cited handle*, not as a finding about the platform. The platform-level sentence this session
wanted to write — *the unit of loss is the account* — **is not written**, and §4 turns out to be
the reason it should not have been.

Two things follow from the failure itself, and both are usable:

1. **7.24 % of the account handles cited in this corpus no longer name the account that holds the
   video.** The URL still resolves — the numeric identifier is what the platform reads, and the
   handle in the path is decorative. A link-checker sees nothing wrong. **This is citation drift
   that leaves no broken link behind**, and it is measured here, not asserted.
2. **The direction of the bias is known.** A renamed account splits into two groups — old cited
   name, new cited name — so the key *dilutes* clustering. It cannot manufacture it.

---

## 1. Why the question exists

Every number this arc has published, and the receiver's published number, treats **the video as the
unit**: n videos, m missing, a Wilson interval over n. That is only correct if videos go
independently. If they go by account, the effective sample size is nearer the number of accounts,
and **every such interval is too narrow — ours first.**

The credential-free video endpoint will not answer this. In the day-2 run **every one of the 683
NOT-RETRIEVABLE units returned HTTP 400 with a single body code**, and no field distinguishes a
removed video from a removed account. The interface says only *no*. So the mechanism is read off
the structure of the losses — or it is not read at all.

## 2. What the structure says (no new requests)

**Population.** `ledger/run-2026-08-12T0341Z.json`, minus the 249 units of arm `B-truncated`
(absence there is an artifact of a truncated identifier in the source text, not an event on the
platform — excluded *before* the statistic was computed), minus 38 INDETERMINATE, minus 7
identifiers that are not 19 digits and cannot be dated. **3,575 units in 2,744 handles, 432 absent
= 12.08 %.** 2,366 handles hold exactly one unit; the largest holds 36.

**It is clustered, and not by age.** Intra-class correlation over handles, Monte Carlo against two
nulls, 10,000 draws each, seeds in the output file:

| | ρ observed | null mean ρ | null 95th pct | p |
|---|---|---|---|---|
| Null 1 — constant rate 12.08 % | 0.7912 | −0.0000 | 0.1031 | **0.0001** |
| Null 2 — each unit at its own age-band × arm rate | 0.7912 | 0.0553 | 0.1551 | **0.0001** |

Both p-values are **at the Monte Carlo floor** of 1/(10,000+1) — the statement is "not once in
10,000 draws", not a smaller number. Null 2 is the one that matters: it gives every unit the
absence probability of its own age band within its own arm, so **the shared era of an account's
videos is already priced in.** The clustering survives it.

The same thing in whole numbers, which need no estimator at all: among the 2,869 within-handle
pairs there are **67 both-absent pairs against 41.9 expected under the constant-rate null and 33.8
expected under the age-and-arm null.** And **64 of the 98 absent units that sit in a multi-video
handle — 65.31 % — sit in a handle where every unit is absent** (26 such handles: eighteen of size
2, six of size 3, one of 4, one of 6).

**A compositional fact that must be read alongside it, and it cuts against a tidy story.** Absence
is *lower* inside multi-video handles: **8.11 % (98/1,209) against 14.12 % (334/2,366) among
handles cited once.** Accounts cited more than once in an encyclopedia are more durable. So the
dependence measured here is as much *between-handle heterogeneity of rate* as *within-handle
concordance of events* — which is precisely what a design effect is, and precisely why the point
estimate must not move.

## 3. The correction, and the estimator we threw away

The pre-registered ANOVA estimator returned **ρ = 0.7912** on a sample two-thirds singleton, a
regime where its within-cluster mean square rests on the few multi-unit handles alone. Carried into
DEFF = 1 + (m̄_Kish − 1)ρ with m̄ = 2.605 it gives **DEFF = 2.270**. **We do not use it**, and we
say why before we say what we use instead (deviation **D17**).

The nonparametric cluster bootstrap needs no ρ. Resample **handles** with replacement, take every
unit of each drawn handle, recompute the rate; compare against the identical bootstrap resampling
**units**. The ratio of squared widths is a design effect *measured* rather than estimated:

| interval on the 12.08 % absence rate | 95 % | width |
|---|---|---|
| Wilson, video as unit (what this arc has been publishing) | **[11.06 %, 13.19 %]** | 2.137 pp |
| bootstrap over units (no clusters) | [11.02 %, 13.15 %] | 2.126 pp |
| **bootstrap over handles** | **[10.85 %, 13.41 %]** | **2.567 pp** |
| bootstrap over handles, sensitivity key 2 | [10.82 %, 13.40 %] | 2.578 pp |

**Measured design effect: 1.458** (cluster bootstrap against unit bootstrap; 1.442 against Wilson).
The ANOVA route overstates it by **56 %**. Effective sample size **2,452 of 3,575**, not 1,574.

**The consequence, stated exactly.** The point estimate does not move. **Every interval this arc
publishes on this corpus is 1.20× wider than the interval it has been publishing** — the ratio of
widths, √1.458. On the pooled absence rate that is 2.14 pp → 2.57 pp, and the lower bound falls
from 11.06 % to 10.85 %. Small, real, and in the direction that costs us.

**Sensitivity to the failed key (§0).** Regrouping on the platform's own author id where it gave
one, and the cited handle otherwise, moves ρ to 0.8176 and the bootstrap interval to
[10.82 %, 13.40 %] — indistinguishable. **Key 2 is not a repair and is not used as one**: it applies
the canonical name only to units that are retrievable, so it can merge present units while leaving
absent ones apart, and that asymmetry could manufacture concordance. It is reported for the
direction it moves the answer, and it moves it nowhere.

**Stability (cohort invariance, the standing method forged at session 111).** Per arm, ρ = 0.7777
(A, n = 2,181), 0.8264 (A-new, 194), 0.7695 (A2, 751), 0.9178 (B, 449). On the **day-1 run** —
2,618 units, 2,038 handles, 11.38 % absent — ρ = 0.7930 and the measured design effect is **1.462
against day 2's 1.458.** That is stability of the estimator, **not an independent replication**: the
two runs are the same corpus one day apart, with one confirmed transition between them.

## 4. The mechanism, measured — and it refutes the tidy version (62 requests)

§5 of the pre-registration sent 24 requests to public **account** pages, twelve handles whose every
corpus video is absent and twelve whose every video is retrievable, to find out whether the account
dimension is observable without credentials at all.

**P6 predicted the route would be closed. It is not.** All **24 returned HTTP 200**, 362,145 to
365,724 bytes, the same generic application shell and the same `<title>` for a live account and a
dead one. On the page as delivered, nothing distinguishes them — but the shell carries an embedded
state object, and **that** distinguishes them (D18, two further requests; D19, the rest — both
declared and committed before running, D19 with its predictions).

**36 handles, one request each, twelve per group** (the `statusCode` field carried in the page):

| group (from our corpus) | state 0, account object served | non-zero, no account object |
|---|---|---|
| every corpus video absent | **6** | **6** (five `10221`, one `10202`) |
| every corpus video retrievable | **12** | 0 |
| mixed | **11** | **1** |

**P8 failed: half, not a majority.** In six of the twelve handles where every cited video is gone,
**the account is still served and its name still resolves** — the videos were removed while the
account stayed. *The unit of loss is not the account.* It is the account **half the time**, which is
a smaller and more useful sentence than the one this session set out to write, and it is the reason
§0's K1 consequence costs this session nothing it should have kept.

**P9 held: 12 of 12.** **P10 failed on one handle** — `grimhoundgaming`, seven cited videos, some
retrievable at 03:40Z, whose account page at ~23:45Z the same day carries `10221`. Either the
account went in the twenty hours between, or the two interfaces disagree. **This is a dated,
falsifiable prediction for day 3**: if the account is gone, those seven videos turn NOT-RETRIEVABLE
on 2026-08-13. Written down before the run that would settle it.

**What the numbers are not.** We found **no code table published by the platform**; a developer's
public question asking for one stands unanswered
(`https://github.com/davidteather/TikTok-Api/issues/403`, read 2026-08-12). Third-party pages assert
meanings for these codes; we did not verify them and **rely on none of them**. Read here, the field
means only: *the account object is not served under this name.* And the strings *"Couldn't find this
account"* and *"This account was banned"* appear in the shell of **live** accounts too — they are
bundled interface text, **not evidence**, and anyone repeating this measurement by string-matching
the page will get a wrong answer.

**Can a rename explain the six?** No — and the failure in §0 is what rules it out. This corpus
contains 226 renamed handles whose videos still return HTTP 200 with a *different* author name, so
a rename demonstrably does not remove a video from the credential-free endpoint. Where the videos
are gone *and* the handle is unserved, rename alone does not account for it.

**Nothing was reclassified (K5).** No ledger unit's state was changed by any of this.

## 5. Scoring, in public

| | prediction | result |
|---|---|---|
| P1 | key fidelity ≥ 95 % | **FAIL** — 92.76 % → **K1 fires** |
| P2 | ρ > 0 vs constant-rate null, p < 0.01 | hold — p at the 0.0001 floor |
| P3 | ρ > 0 vs age × arm null, p < 0.01 | hold — p at the 0.0001 floor |
| P4 | DEFF ≥ 1.20 | hold — 1.458 measured (2.270 by the estimator we discarded) |
| P5 | > 50 % of multi-handle absences in all-gone handles | hold — 65.31 % |
| P6 | the account route is closed | **FAIL** — 24/24 HTTP 200, and it discriminates |
| P7 | day-1 ρ within a factor 2 of day-2 | hold — 0.7930 vs 0.7912 (not independent) |
| P8 | majority of all-gone handles account-dead | **FAIL** — 6 of 12 |
| P9 | all all-present handles account-live | hold — 12 of 12 |
| P10 | all mixed handles account-live | **FAIL** — 11 of 12 |

**Five of ten fail.** Kill criteria: **K1 fires** and its consequence is applied; **K2 does not**
(ρ is distinguishable from zero under both nulls); **K3 does not** (1.458 ≥ 1.05, the correction is
not cosmetic); **K4 is honoured** — nothing is claimed about the receiver's population below except
as marked conjecture; **K5 is honoured** — the probe reclassified nothing.

**Marked conjecture, and it is the only thing said here about anyone else's number.** *If* the
70,239 identifiers behind the receiver's published rate are also clustered by account — plausible
for any corpus assembled from accounts, unmeasured by us and unmeasurable from their published
text — *then* the interval around their rate is too narrow by a similar factor. **We have not
computed this, we cannot compute it from what is published, and it is a conjecture, not a
correction.**

## 6. The nearest neighbour, and the daylight

From the house's papers register (fetched, not mirrored): *A Longitudinal Assessment of the
Persistence of Twitter Datasets*, Arkaitz Zubiaga, arXiv:1709.09186, JASIST. Same method family —
re-collect by identifier, count what is gone, 147 M items. Read first-hand at
`https://arxiv.org/html/1709.09186`. On mechanism it reaches exactly the inference this increment
replaces with a measurement:

> *"The exception is the percentage of unique users found in the recollected datasets, which is
> 80.0%. This indicates that many of the tweets likely disappeared because of the removal of the
> user accounts"*

**It does not measure clustering** — no intra-class correlation, no design effect, no clustered
variance — and its reported figures treat items as independent. The daylight is exactly that: the
nearest neighbour *infers* the account mechanism from an aggregate gap and computes as if items
were independent; this increment measures the dependence, prices it into the interval, and then
finds by direct probe that the account mechanism accounts for **half** the all-gone handles, not
most of them. **The house's atlas of 505 works returns nothing on this object** — a negative result,
recorded as evidence (`PREREGISTRATION-114.md` §6). *Characterizing "permanently dead" links on
Wikipedia* (`10.1145/3517745.3561451`) is in the register and **closed to us: HTTP 403 tonight.**

## 7. What this changes for the arc

- **The arc owes a restatement, not a retraction.** No published point estimate moves; the intervals
  widen by 1.20×. `RESULT.md`, `OBJECT-ANSWER.md` and the power audit carry video-unit intervals and
  are now known to be narrow. **Corrections are dated events, never silent patches** — the
  restatement is the next session's first task, listed in `NEXT-SESSION.md`.
- **The power audit is affected in the direction that hurts.** Any power figure computed on n
  independent units overstates precision by the same factor; the window's transition arithmetic
  counts *events*, not rates, and is not touched, but nothing that reads a rate off this corpus is
  exempt.
- **A cheap new arm exists and is licensed by tonight's result**: the account state is readable
  credential-free, one request per account, ~2,744 accounts. It measures mechanism directly instead
  of inferring it. It is **not** started tonight and **not** added to the window.
