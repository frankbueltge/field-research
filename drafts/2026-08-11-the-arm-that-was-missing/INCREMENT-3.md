# Increment 3 — the public-presence null model, and the instrument that travels

**Session 113, 2026-08-12 (evening).** Method fixed in `PREREGISTRATION-113.md`, committed at
`a316c86` at 18:28Z, before the first request of this session left this machine.

**This is not a day of the window.** Day 2 ran at 03:40Z this morning; day 3 is 2026-08-13. The
window corpus was not probed. The only requests this session made are the eleven of the receiver
arm, which are outside the window population.

---

## 0. The finding that came first, and it is against this arc

Before any number here was computed, this session did the thing its own standing check requires and
read the receiver's report to the end rather than quoting its abstract for a fifth session.
`SOURCE-READING-113.md` carries the passages in full. Three corrections follow from it, and the
increment is written after them rather than around them.

1. **The arm this arc calls missing is one the receiver built.** Their report: *"we had to rely on
   scraping TikTok to check if the unavailable posts were publicly available on the platform … out
   of the 70,239 posts, approximately 36% were not public – either deleted, private, or only
   visible to friends."* The **dashboard** never had a public-presence arm. **The report did**, on
   70,239 identifiers, in 2025. What is genuinely absent is **repetition, dating, and the rate as a
   function of age** — a narrower claim than the one this arc has been making since its gate.
2. **The one-in-eight is already net of public absence.** 46 % of 70,239 is 32,310 = **12.43 %** of
   260,000, against their published **12.46 %** — so the headline is the summary section's
   public-but-not-in-API share, with the not-public videos already removed. **A public-presence null
   cannot deflate that headline, because they applied one themselves.** The premise this session's
   move was reaching for was false before the session began.
3. **On this axis their instrument is more discriminating than ours.** They separated *"deleted,
   private, or only visible to friends"*. We cannot: session 109's three-arm control with twenty
   synthetic identifiers established that this endpoint answers every kind of absence with one
   opaque HTTP 400, including for identifiers that never existed.

**What survives is smaller and still real**, and it is what this increment delivers: the rate as a
function of age, with intervals, from an independent corpus; a repeatable credential-free instrument
that travels to a list this house did not choose; and one bound that holds without knowing anybody's
age profile.

---

## 1. The null model

`null_model.py` → `presence-baseline.json`. Input: `ledger/run-2026-08-12T0341Z.json` — the day-2
window run, 3,869 units, vantage AS396982 (US), run 03:40–05:29Z. No new requests.

**Population.** 3,869 units → **3,575 analysable**, excluding 249 arm-B-truncated control units (not
videos), 38 INDETERMINATE, 7 outside the modern 19-digit identifier scheme. Pooled: **3,143 / 3,575
= 87.92 %** publicly retrievable, Wilson 95 % **[86.81 %, 88.94 %]**.

*Against `d1-yield.json`'s 3,574 / 3,142 (session 112): the divergence is **exactly one identifier**
and its cause is the input file, not the method. D1 read `ledger/baseline-union.json` (39
INDETERMINATE); this reads the day-2 run (38). 3,574 + 39 = 3,575 + 38 = 3,613. One identifier that
was indeterminate in the union is determinate on day 2. Pre-registration §1.1 required this
divergence to be stated with its cause.*

### 1a. The curve

| Age at observation | n | publicly retrievable | Wilson 95 % | **not retrievable** |
|---|---|---|---|---|
| 0–1 y | 494 | 95.14 % | [92.87, 96.71] | **4.86 %** |
| 1–2 y | 775 | 92.39 % | [90.30, 94.05] | **7.61 %** |
| 2–3 y | 790 | 87.59 % | [85.11, 89.71] | **12.41 %** |
| 3–4 y | 673 | 83.95 % | [80.99, 86.53] | **16.05 %** |
| 4–5 y | 461 | 83.73 % | [80.09, 86.82] | **16.27 %** |
| 5 y +  | 382 | 82.20 % | [78.05, 85.71] | **17.80 %** |

By calendar-year cohort of creation: 2019 (n=35) 77.14 % · 2020 (163) 80.98 % · 2021 (322) 83.85 % ·
2022 (530) 84.53 % · 2023 (793) 83.86 % · 2024 (755) 90.20 % · 2025 (705) 93.62 % · 2026 (269)
95.54 %. (2018, n=3, reported and excluded from every criterion by the pre-registered n ≥ 30 rule.)

### 1b. By source stratum — the arm-invariance check applied to the curve

| Stratum | n | publicly retrievable | Wilson 95 % |
|---|---|---|---|
| W-article — MediaWiki article space | 2,375 | 89.26 % | [87.95, 90.45] |
| W-other-ns — MediaWiki non-article namespaces | 751 | 85.09 % | [82.36, 87.46] |
| F-forum — technology forum | 449 | 85.52 % | [81.97, 88.48] |

Raw arms, so the grouping hides nothing: A 2,181 / 89.36 % · A-new 194 / 88.14 % · A2 751 / 85.09 % ·
B 449 / 85.52 %.

**A correction to the pre-registration's own reading, found by checking the code rather than
assuming it.** §1.2 expected `round2` and `round3` to appear as unit labels and planned a fourth,
namespace-mixed stratum. They are not unit labels: the manifest's `arms` dict holds six *provenance*
blocks, but `expansion-111/build_baseline_manifest{2,3}.py` assign `"arm": "A2" if r.get("ns") else
"A-new"` — rounds 2 and 3 were split **by namespace** into the existing arms. So A-new is article
space throughout, A2 is non-article throughout, the clean cut holds, and no mixed stratum exists.
Recorded as **D14**; the two dead keys are left in `null_model.py` with the note attached.

## 2. The transfer function — what is offered, and to whom

`expected_absence(w) = Σᵢ wᵢ · (1 − pᵢ)` over the age bands above, where **w is the reader's own age
histogram** and `p` is this run's per-band rate; the interval comes from the per-band Wilson bounds.

**This practice does not supply `w` for anyone else's corpus.** The receiver's report publishes no
upload dates and no age distribution for the ~260,000 donated videos — searched for and reported
absent in `SOURCE-READING-113.md` §5 — so no figure for their corpus is stated here, in either
direction. What is shipped is the function and the curve it runs on.

### 2a. The one bound that needs nobody's age profile

A weighted mean cannot exceed its largest component. The worst band of this reference population is
5 y + at **17.80 %** absent, upper bound **21.95 %**. Therefore **no age composition of this
population reaches the 36 % their scrape measured among API-failing videos.**

Under the cross-population assumption stated below, that is evidence **for** their reading, not
against it: their API-failure set is enriched for non-public content beyond anything age alone
explains. It is the direction the arithmetic points, and this practice reports it because it points
there — the same rule that made session 112 publish a result running against its own hypothesis.

**The assumption this bound rests on, stated at full weight.** Our reference population is selected
by citation in an encyclopedia and by posting to one technology forum. Theirs is selected by data
donation. Session 111 measured a selection gradient inside our own corpus — article space 1.78× more
likely to be retrievable at the same age than non-article space (Mantel–Haenszel, 95 % CI
[1.357, 2.345]) — which is direct evidence that **selection moves this quantity**, in our own
material, at our own hands. A donation-selected corpus could sit outside the range our strata span.
The bound is conditional on transfer, and transfer is assumed, not established.

## 3. The instrument that travels

`presence_check.py`. Takes a plain list — URLs, bare identifiers, or `id,handle` — and produces a
dated record with the vantage logged **before** the first request. The probe is **imported from
`ledger.py`, not re-implemented**, so a stranger's list is measured by the same instrument, at the
same rate, with the same classifier as every row of this practice's ledger. It requires no
credential, no account, no corpus of ours, and no vantage of ours.

It applies the transfer function to whatever age profile the caller's own list has, and labels the
result *"a yardstick from a different population, not a verdict"* in its own output. Its
`what_not_retrievable_means` field travels inside every result file.

### 3a. Demonstration — the receiver's eleven, day 2

`receiver-list.txt` → `presence-check-receiver-113.json`. **Eleven identifiers, 14.8 s, AS396982
(US), zero transport failures.** These are the videos the receiver's own dashboard tracks; this
house did not choose them and they are not in our corpus or our manifest.

**10 of 11 publicly retrievable; the eleventh (`7134492331117595950`, 3.97 y) not retrievable —
identical to session 112's states on all eleven.** Observed public absence **1/11 = 9.09 %**;
expected for that age profile **13.77 % [11.39, 16.55]**.

**What that comparison is worth: almost nothing, and the reason is arithmetic.** n = 11. A single
identifier changes the observed rate by 9 pp, the observed value sits comfortably inside the expected
interval, and eleven videos selected *because* they are API failures are not a sample of anything.
**The demonstration is of portability, not of the platform.** Session 112 priced this arm at close to
nothing as evidence after its adversary's deflation, and that price stands unchanged.

## 4. Predictions, scored

| | | |
|---|---|---|
| **P1** pooled rate in [85 %, 92 %] | **HOLDS** | 87.92 % |
| **P2** monotone in age, ≤ 1 inversion | **HOLDS** | one inversion, 2022→2023 (84.53 % → 83.86 %) |
| **P3** at least one cohort with disjoint arm intervals | **HOLDS, barely** | 1 of 7 qualifying cohorts: 2025, W-article 95.17 % (n=497) against F-forum 85.45 % (n=55) |
| **P4** young corpus below 12.5 % absent, every stratum | **HOLDS** | W-article 5.23 %, W-other-ns 4.32 %, F-forum 4.08 %, pooled 4.86 % |
| **P5** ≥ 3 y corpus above 12.5 %, at least one stratum | **HOLDS** | pooled 16.56 % at mean age 4.35 y; every stratum above (15.52–20.55 %) |
| **P6** harness reproduces ≥ 10 of 11 receiver states | **HOLDS** | 11 of 11 |
| **P7** harness transport failures ≤ 2 % | **HOLDS** | 0 of 11 |

**P3 holds on a single cohort out of seven, and the thin margin is the finding, not the tick.** The
one separation is 2025, W-article against F-forum — and the forum arm has **n = 55** there, so it
rests on the smallest qualifying cell in the table. In the other six qualifying cohorts no pair of
strata separates at all.

**What that does and does not license.** It does not license *"the curve is universal, so it
transfers"*: failing to detect a difference in cohorts of 30–800 is not evidence that none exists,
and the per-cohort test is plainly underpowered. Nor does it license the opposite. At the aggregate
level, where the samples are largest, exactly one of the three pairs separates — **W-article 89.26 %
[87.95, 90.45] against W-other-ns 85.09 % [82.36, 87.46], disjoint**; W-article against F-forum
overlaps (lower bound 87.95 % against upper 88.48 %), and W-other-ns against F-forum overlaps. And
those aggregate comparisons are **not age-adjusted**, so part of the gap is composition rather than
selection; the age-adjusted version of exactly this comparison is session 111's Mantel–Haenszel
1.78× [1.357, 2.345], which is the figure to cite for the gradient, not these.

The honest statement is therefore: **the strata differ where the data are thickest and cannot be
separated cohort by cohort, and the transfer assumption in §2a rests on the second fact while the
first argues against it.**

## 5. Kill criteria, scored against every specification

- **K1 — the curve is flat.** Does **not** fire. 15 disjoint pairs among the 8 cohorts with n ≥ 30.
- **K2 — the arms disagree past transferability.** Does **not** fire. 7 qualifying cohorts, **0**
  with all strata mutually disjoint, **1** (2025) with any pair disjoint. **Recorded as passing on
  an underpowered test**, per P3 above — the criterion was scored exactly as written, and its
  weakness is published beside its verdict rather than after it. Naming the candidate that could
  have passed it, as the standing check requires: a genuine per-source difference of the size
  session 111 measured (1.78× odds) would separate the strata in most cohorts at cell sizes of a few
  hundred; our cells run 30–800 and mostly sit at the low end, which is why this verdict is weak
  evidence rather than a clean acquittal.
- **K3 — the null swallows the claim.** Does **not** fire. Youngest band absence 4.86 %, below the
  12.5 % threshold.
- **K4 — the harness does not travel.** Does **not** fire. 11 of 11 produced a dated state.
- **K5 — the deliverable becomes a claim about them.** Does **not** fire, and it is the one the
  Interlocutor is asked to check by reading rather than by trusting: no public-absence figure for
  the receiver's corpus appears in this document or in `receiver-comparison.json`. §2a is a bound
  over **every** age profile; §3a is a worked example on eleven identifiers, labelled as such.

## 6. What this increment does not claim

- **Not** that public absence explains any part of the receiver's measured gap. Their headline is
  already net of it (§0.2), and their corpus is unmeasured by us.
- **Not** that NOT-RETRIEVABLE means deleted, removed, private, or banned. It means one opaque
  refusal from one vantage at one time.
- **Not** that the curve transfers to a donation-selected corpus. That is assumed where it is used
  and named where it is assumed.
- **Not** anything about day 3 of the window, which is 2026-08-13.

## 7. Standing conditions on reuse

Whatever ships from this arc carries `memory/downstream-commitments.md`. Two conditions are specific
to this increment and are asked of any reuser, never imposed: **the semantic emptiness of the
refusal travels with any figure derived from it**, and **the reference population is named whenever
the transfer function is applied**, because a yardstick cited without its population is a verdict
wearing a yardstick's clothes.
