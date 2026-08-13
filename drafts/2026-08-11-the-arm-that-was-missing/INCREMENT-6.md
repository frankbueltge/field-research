# Increment 7 — the account and the page are not the same clumping, and the corpus's margins were still too narrow this morning

*Session 116, 2026-08-13 (second session of the date). Pre-registered in `PREREGISTRATION-116.md`,
committed at `ef89178` before any analysis ran. **No new requests**: this is a re-analysis of the
day-2 and day-3 runs already collected. The window population, its manifest and its probe are
untouched, and the account-state arm stays outside the window.*

*The file numbering of this draft runs one behind its increment numbering; this is increment 7.*

---

## 1. The finding

Videos in this corpus disappear in clumps. Which clump? The arc has measured two answers on the
same units and never together: the **account** that posted a video (design effect **1.4289**) and
the **page or thread** that cites it (**1.8854**) — `cluster-keys-114.json`, closed form, no seed.
Session 115 tried to ask whether the second adds anything beyond the first, published a permutation
test that said no, and withdrew it the same night: only 113 of 3,575 units could move under that
null, and **none of them lay inside the article that carries the entire page effect**.

A model carrying both at once now exists. On the day-3 run:

| key | design effect |
|---|---|
| account only | 1.4216 |
| citing page only | 1.8115 |
| account × page cell only | 1.3171 |
| **both, crossed** | **1.9161** |

**The crossed design effect is larger than either key alone.** The two clusterings are not two
views of one thing: they are nearly additive, and the identity that makes that exact is

    DEFF_crossed = DEFF_account + DEFF_page − DEFF_cell
    1.9161       = 1.4216       + 1.8115    − 1.3171

which is inclusion–exclusion over the pairs that share an account, a page, or both. What the cell
term removes is only the double-counting of pairs sharing *both* — 1.3171 of it — and that is far
less than either main effect. Two accounts' videos sitting on one page and one account's videos
sitting on many pages are **different** dependencies, and this corpus has both.

The consequence is immediate and unflattering. This morning this practice published a dated
correction widening 36 intervals by ×1.1954 for clustering, and called 1.4289 a lower bound.
**It was a lower bound, and the margins published this morning are themselves about 18 % too
narrow.** §4 recomputes all 36 again, beside them, never over them.

## 2. What was estimated, and how

For unit *i* with account *A(i)* and citing page *P(i)*, `y_i = 1` if NOT-RETRIEVABLE:

    y_i = mu + a_{A(i)} + b_{P(i)} + (ab)_{A(i)P(i)} + e_i

crossed, not nested — an account appears on many pages and a page cites many accounts.
`crossed_model.py` computes three things that must agree and one that need not.

**Route 1, the model.** Variance components by moments on pairwise products, closed form, no seed:
pairs sharing an account but not a page identify `sigma2_A`; pairs sharing a page but not an
account identify `sigma2_P`; pairs sharing both identify the interaction. Then
`DEFF = 1 + [sigma2_A*M_A + sigma2_P*M_P + sigma2_AP*M_AP] / (N*p(1−p))` over the ordered
same-cluster pair counts.

**Route 2, model-free.** The two-way cluster-robust estimator of Cameron, Gelbach and Miller:
*"we obtain three different cluster-robust 'variance' matrices … by one-way clustering in,
respectively, the first dimension, the second dimension, and by the intersection … Then we add the
first two variance matrices and subtract the third"*
(https://cameron.econ.ucdavis.edu/research/JBESpaper2009version.pdf, version of 2009-05-15;
published as *Robust Inference With Multiway Clustering*, JBES 29(2); NBER Technical Working Paper
327, https://www.nber.org/papers/t0327).

**Route 3, the direct double sum.** `(1/N^2) * sum_{i,j} u_i u_j * 1[same account OR same page]`,
`u_i = y_i − p`.

All three return **1.916067**, agreeing to 4.4 × 10⁻¹⁶ — machine epsilon.

**And that agreement is worth nothing, which the pre-registration failed to see.** P5 predicted
routes 1 and 2 would agree within 0.20 absolute. They agree to the last bit because **they are the
same estimator**. Writing route 1's numerator out:

    sigma2_A*M_A + sigma2_P*M_P + sigma2_AP*M_AP
      = sigma2_A*(M_A − M_AP) + sigma2_P*(M_P − M_AP) + T_AP
      = T_A_only + T_P_only + T_AP

which is exactly route 2's cross-product sum once the diagonal `sum_i u_i^2 = N*p(1−p)` is added
back. A prediction that two things will agree, written without checking whether they are one thing,
is a prediction that cannot fail. **P5 held vacuously and should not have been written.** It is
recorded as a defect in the pre-registration, not as corroboration.

What that leaves is a real property, stated correctly: the crossed design effect **does not depend
on the additive model being true**, because it equals a model-free estimator. The decomposition
into `sigma2_A` and `sigma2_P` does depend on it — see §3.

**Route 4, and the one that is genuinely independent.** Accounts and pages form a bipartite graph;
every dependence this model can express lies inside a **connected component**, so components are a
legitimate one-way key and their design effect bounds the crossed one from above. On day 3:
**2,394 components over 3,569 units, the largest holding 63 units (1.8 %)**, and
`DEFF_component = 1.9414` against the crossed 1.9161. The envelope sits just above the estimate,
which is what a correct crossed estimate should do.

That also answers **P6**, which predicted a giant component holding more than half the units and a
correspondingly weak bootstrap. **P6 fails, in this arc's favour**: the graph is shattered, so
resampling components is a well-powered scheme, and it is the resampling used for every interval
below.

## 3. The variance components, and the one that is out of range

Day 3, from `crossed-116.json`:

| component | estimate | component-bootstrap 95 % |
|---|---|---|
| `sigma2_A` (account) | 0.02818880 | [0.01320801, 0.05129949] |
| `sigma2_P` (page) | 0.04019100 | [0.00218773, 0.13390395] |
| `sigma2_AP` (interaction) | **−0.03991248** | — |
| `sigma2_total` = p(1−p) | 0.10681548 | — |
| crossed DEFF | 1.9161 | [1.3482, 2.7839] |

**`sigma2_A` is clearly positive and its interval excludes zero — K1 does not fire.** The account
effect this arc has built three sessions on survives controlling for the page. **`sigma2_P` is
positive and its interval excludes zero — P2 holds.**

**The interaction estimate is negative, and a variance cannot be.** This is the classic
out-of-range moment estimate, and it is not cosmetic: it says that pairs sharing *both* an account
and a page co-vary at 0.0285 — about the same as pairs sharing only an account — rather than at the
0.0684 an additive model predicts. **The two effects are substitutes at the cell level, not
additive.** So the strictly additive model is wrong in a way this data can see, and the
decomposition in the table above is read as **descriptive** rather than as an estimated
variance structure. The design effect is unaffected, because it is the model-free quantity of §2.

## 4. What it costs — the 36 intervals, again

The pre-registration committed, before the number was known: *if `DEFF_crossed > 1.4289 + 0.05`,
the 36 intervals restated this morning are recomputed at the crossed value tonight, as a dated
addendum, never a silent edit.* The clause fires. `addendum_116.py` → `addendum-116.json`:

- **36 intervals recomputed.** All 36 **reproduce** this morning's account-key restatement from
  their own k and n before the new value is applied.
- **36 are wider again. No centre moved** — the point estimate is consistent under clustering
  whatever the design effect; only precision is lost.
- Half-width multiplier on the published naive intervals: **1.1954 → 1.4107**, a **further ×1.1801**
  on top of this morning's correction.
- Largest further widening ×1.2145 (`POWER-AUDIT §2`, cohort 2026); smallest ×1.0454
  (`RESULT.md`, census by decoded creation year 1971) — small cells widen least because a Wilson
  interval on a handful of units is already dominated by its own boundary.

The morning's figures stand as published, in every row of the addendum. Nothing is overwritten.

**And the finding that was already wounded does not survive.** `gap_116.py` → `gap-116.json`
recomputes the encyclopedia-vs-forum gap of `INCREMENT-1 §7` — session 110's **P6** — under every
design effect this arc can defend. All six of session 115's figures are reproduced by this file
from its own inputs first, including the two arm-specific design effects 1.4688 and 1.1859.

| specification | z | 95 % CI (pp) | excludes 0 |
|---|---|---|---|
| published, video as unit | 2.1940 | [0.42, 7.50] | yes |
| pooled account DEFF 1.4289 (session 115) | 1.8355 | [−0.27, 8.19] | no |
| arm-specific account DEFFs (session 115) | 1.9828 | [0.05, 7.88] | yes |
| pooled crossed DEFF (session 116) | 1.5553 | [−1.03, 8.95] | no |
| arm-specific crossed, article arm | 1.8085 | [−0.33, 8.25] | no |
| arm-specific crossed, article + other namespaces | 1.8305 | [−0.28, 8.20] | no |

This morning the arc reported that the gap crosses zero under the pooled correction and clears it
under the arm-specific one, and printed both rather than choose. **Under the crossed model it
crosses zero under both.** The arm-specific route was the last specification in which P6 cleared,
and the reason it did is now visible: the encyclopedia arm's clustering is much worse than its
account key showed — crossed **2.3515** on the article arm against **1.4688** on the account key
alone, because encyclopedia articles cite many accounts each and forum threads mostly do not
(forum crossed **1.3333**).

**P6 is withdrawn as a supported finding.** What remains, unchanged from this morning: a cluster
bootstrap and a permutation test that need no design-effect choice at all both exclude zero
(`INTERLOCUTOR-7.md`), so the direction is not refuted — but no interval this arc can defend
excludes zero, and the honest status is **unsupported**, not "directionally supported".

The Mantel–Haenszel odds ratio of `INCREMENT-3 §2a` **survives**: [1.2129, 2.6238] at the crossed
design effect, still excluding 1. The Weibull shape is not widened again here — `INTERLOCUTOR-7.md`
established a parameter-specific design effect of 1.27 for it, and the published shape interval
remains the widest of the routes tested.

## 5. The page effect is not one article

Session 114's adversary called the page key fragile and carried by a single article. That article
is `es.wikipedia.org|Protestas en Paraguay de 2023` — on day 3, **22 units in the analysis
population, 16 absent, across 20 distinct handles**.

Removing it entirely:

| | with the article | without it |
|---|---|---|
| `sigma2_P` | 0.04019100 | 0.00643578 |
| bootstrap 95 % | [0.00218773, 0.13390395] | [0.00100495, 0.01837483] |
| crossed DEFF | 1.9161 | 1.4921 |

**P3 fails.** The prediction was that `sigma2_P` would stay positive but its interval would include
zero — that the page effect would prove unestablished without that one article. It does not include
zero. The article accounts for **83.99 %** of the page variance component (`derived-116.json`) and
the remainder is still distinguishable from zero; the crossed design effect without it (1.4921) is
still above
the account-only figure (1.4216). **The page effect is dominated by one article and is not created
by it.**

## 6. Stability, and what reproduces

Day 2 was run identically (`crossed-116-day2.json`). With the same `K/(K−1)` finite-cluster factor
the published figures carry, tonight's script — written from scratch and not derived from
`cluster_keys.py` — returns **account 1.4289** and **page 1.8854**: the two published values to
four decimals, from a different implementation.

| | day 2 | day 3 |
|---|---|---|
| units | 3,575 | 3,569 |
| absence rate | 12.0839 % | 12.1603 % |
| account-only DEFF | 1.4283 | 1.4216 |
| page-only DEFF | 1.8847 | 1.8115 |
| **crossed DEFF** | **1.9892** | **1.9161** |
| components | 2,402 | 2,394 |
| largest component | 62 units | 63 units |

**P7 holds**: the crossed design effect moves by 0.0731 between the two days, inside the 0.15 the
pre-registration allowed.

## 7. Scoring, in public

Pre-registered at `ef89178`, before any of the above was computed.

| | prediction | outcome |
|---|---|---|
| P1 | crossed DEFF > account-only on the same subset | **holds** — 1.9161 vs 1.4216 |
| P2 | `sigma2_P` > 0, bootstrap excludes zero | **holds** — [0.0022, 0.1339] |
| P3 | without the heaviest page, `sigma2_P` interval includes zero | **fails** — [0.0010, 0.0184] |
| P4 | crossed DEFF < 1.8854, the page-only figure | **fails** — 1.9161, above both keys |
| P5 | routes 1 and 2 agree within 0.20 | **vacuous** — they are the same estimator (§2) |
| P6 | a giant component holding > 50 % of units | **fails** — largest is 1.8 % |
| P7 | day-2 and day-3 crossed DEFFs differ by < 0.15 | **holds** — 0.0731 |

Three hold, three fail, one should never have been written. **No kill criterion fires.** K1 does
not (`sigma2_A` positive), K2 does not (the two-way variance is positive, DEFF 1.92), K3 does not
(**100.00 %** of the day-3 analysis population is attributed to a citing page — the crossed subset
is the population, not a slice of it), K4 does not (the crossed DEFF exceeds the account-only one,
so the lower-bound framing is confirmed rather than refuted), K5 does not.

**P4's failure is the session's finding**, and it was predicted the wrong way round: the arc
expected the page key to over-state because it absorbs account structure, and the opposite is true —
each key *under*-states because it is blind to the other.

## 8. The standing check is now a script, and it does not do what was hoped

`prose_vs_json.py`, pre-registered tonight, after three consecutive sessions published a number
their own machine-written files refuted.

**Pass 1** pulls every number out of a prose file and asks whether that value occurs anywhere in
this draft's JSON. Run against the archived version of this morning's restatement that carried the
failure (`4dde327`), it audits 316 numbers and reports 7 unmatched — **and 1.7052 is not among
them.** 1.7052 is a real per-cell design effect that does occur in this draft's data; it simply
belongs to a partition that was never in the set the sentence claimed to summarise. **A
value-existence check is structurally blind to the failure it was built for**, and saying so is
worth more than shipping it quietly.

**Pass 2** therefore checks no values at all. It lists the sentences whose *form* is the form all
three failures took — a summary over a set (`range`, `ceiling`, `maximum`, `at most`, `every`,
`not one`, …) or a count out of a total (`five of ten`) — and demands each be dispositioned by hand
against the table it claims to summarise. Tested against all three archived failures:

- session 113, `INCREMENT-3` before correction: the `ceiling` sentence is flagged (line 119), as is
  the `bound` sentence below it;
- session 114, `INCREMENT-4` before correction: **`**Five of ten fail.**` is flagged** (line 196),
  by construction rather than by value;
- session 115, the restatement before correction: both failing lines are flagged — the `range`
  sentence carrying 1.7052 (line 229) and the `ceiling cell` sentence (line 245).

Three for three, on documents the script never saw while it was being written. The worklists are
39, 28 and 37 lines long — short enough to work through, which is the only property that matters
for a check that has to be run every time.

This document was run through both passes before it was committed; the dispositions are in the
session record.

## 8a. The simplification inside the page key, measured

`cluster_keys.page_index` gives each video **one** citing page — whichever the corpus files yield
first. That is a partition imposed on a hypergraph, and it can only lose page-level dependence.
`multipage_116.py` → `multipage-116.json` measures the cost:

- **479 of 3,569 units — 13.42 % — are cited by more than one page**, one of them by 15.
- Their absence rate is **12.73 %** against the pooled **12.16 %**: multiply-cited videos are not
  materially more or less likely to be gone.
- The crossed design effect needs a partition and cannot be recomputed without one. The **component
  envelope can**, because connectivity does not care how many pages a unit belongs to. Rebuilt over
  **every** (video, page) edge: **2,394 components → 2,378**, largest 63 → 68 units, envelope
  **1.9414 → 1.9484**.

So the simplification costs about **0.007** on the envelope. It runs in the direction that makes
1.9161 an under-statement rather than an over-statement, which is the direction this arc must
report rather than the one it would prefer.

## 9. What this does not establish

- **The additive crossed model is wrong** in the way §3 describes, and no attempt is made here to
  fit a better one. What is published is the design effect, which does not need the model.
- **A design effect is a first-order correction.** Everything above scales a variance; it does not
  re-derive an interval from a likelihood, and small cells are corrected worst.
- **The crossed DEFF is measured on the day-2 and day-3 crossed subsets** and applied uniformly to
  36 intervals, several of which are computed on other populations — exactly as this morning's
  1.4289 was applied uniformly, and the same approximation.
- **Nothing here is a measurement of the platform.** No request left this machine tonight. Days 4
  through 7 of the window are unaffected and unmodified.
