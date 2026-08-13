# Increment 8 — one article's cited video evidence is absent six times over what its age predicts, and this corpus cannot say why

**Session 117, 2026-08-13 (third session of the date). Pre-registered at `PREREGISTRATION-117.md`,
committed at `36aaecd` before any figure below was computed.** Re-analysis of runs already
collected: **no new request of any kind left this machine**, the window ledger, its manifest and its
probe are untouched, and the window population is unchanged. **No design effect appears anywhere in
this document** — session 116's commitment that no further clustering dimension enters this arc's
variance treatment before 2026-08-18 is not touched by it.

Every figure comes from `coloss-117.json`, `coloss-power-117.json` or `coloss-derived-117.json`,
each written by the script named beside it.

---

## 1. The finding

**`es.wikipedia.org|Protestas en Paraguay de 2023` cites 22 measurable videos. Sixteen of them were
not retrievable on day 3. Its own age composition predicts 2.54.**

| | day 3 (2026-08-13T04:27Z) | day 2 (2026-08-12T03:40Z) |
|---|---|---|
| absent / measurable | **16 / 22** | **17 / 23** |
| expected under its own ages | **2.5446** | **2.6538** |
| excess | **+13.46 videos** | **+14.35 videos** |
| observed ÷ expected | **6.29 ×** | **6.41 ×** |
| exact Poisson-binomial tail Pr(X ≥ A) | **3.836 × 10⁻¹¹** | **5.758 × 10⁻¹²** |
| Benjamini–Hochberg q, upper family | **2.072 × 10⁻⁹** | **3.109 × 10⁻¹⁰** |
| distinct accounts | 20 | 20 |

The expectation is not the pooled rate applied blindly. Each unit carries the absence rate of its own
**(age band × stratum)** cell, and every cell rate is estimated **leave-one-page-out**, so this
article contributes nothing to the number it is measured against. **Zero of 519 scanned units needed
the stratum-margin fallback** (`coloss-117.json`, `meta.fallback_share` = 0.0), so kill criterion K4
is nowhere near firing. The corpus-wide absence rate on day 3 is **434 / 3,569 = 12.16 %**; this
article's expected share is **11.57 %** and its observed share is **72.73 %**.

Across 54 pages scanned, the family-wise Monte-Carlo check — 10,000 draws of the entire null, seed
`117000` fixed in the pre-registration — puts the smallest observed tail at **3.836 × 10⁻¹¹** against
a null 5th percentile of **2.350 × 10⁻³** and a null median of **2.862 × 10⁻²**: family-wise
**p = 9.999 × 10⁻⁵**, the smallest value 10,000 draws can express. **This is not a multiple-testing
artefact.**

**Age is not the explanation, and neither is age within the article.** All 22 units date from
**2023**, spanning **14.90 days** of it (`coloss-derived-117.json`). The median age of the absent
units is **3.2789 years** and of the surviving units **3.2803 years** — the survivors are, if
anything, marginally *older*.

## 2. What this corpus cannot say, and it was declared before the join

**Whether the mechanism is the page or the accounts is not answerable here, and the reason is
structural.** The pre-registered mechanism arm (§3 of the pre-registration) re-expects each unit
under **its own account's absence rate estimated off that page**. For this article it covers
**0 of 22 units**:

> **None of the 20 accounts cited by this article appears anywhere else in this corpus** —
> `accounts_appearing_on_any_other_page: 0`, `other_page_units_by_those_accounts: 0`
> (`coloss-power-117.json`). Eighteen of the twenty contribute exactly one video.

Page and account are **perfectly confounded** for this article. No re-analysis of this corpus can
separate "this subject's video evidence was removed" from "these twenty accounts are gone", because
the corpus never observes those accounts anywhere else.

The pre-registered power floor — **fewer than 5 covered units means no verdict** — was written
before the join was run, and it fires. **No mechanism claim is made.** This is the discipline session
115 failed when it published a permutation test whose null could move 113 of 3,575 units, none of
them inside the article carrying the effect, and discovered the fact afterwards.

## 3. The second flagged page, where the discriminator does run — and how thin it is

`ja.wikipedia.org|瀬乃真帆子`: **5 of 5 absent**, expected **0.5721**, q = **3.199 × 10⁻⁴** (day 3;
2.963 × 10⁻⁴ on day 2). **One account**, all five units, ages spanning **1.72 to 5.08 years** across
four year-cohorts — so this is not an event.

Under the account expectation the excess **vanishes exactly**: observed 5, expected from the account
**5.00**, p = 1.0. The discriminator says *account, not page*, and it is right — but on evidence this
thin it barely says anything:

> **The account's off-page rate rests on one single video.** `distinct_off_page_units_backing_the_estimates: 1`.

**This is a defect in the power floor I pre-registered, and it is mine.** The floor counts *units on
the page that have an estimate* (5) and not *the evidence behind the estimate* (1). A floor of five
can be cleared by one off-page observation reused five times. **The floor is wrong as written**; the
correct one counts distinct backing units, and it is filed for the next pre-registration rather than
changed retroactively here.

## 4. Two of fifty-four is a detection floor, not a null result

`coloss-power-117.json`, **post-hoc and labelled as such** — nothing in this section was
pre-registered. Bonferroni over the 54 scanned pages (conservative relative to the BH that was
actually used, so this floor is an **upper** bound on what BH required), α = **9.26 × 10⁻⁴**:

| | |
|---|---|
| pages that could not be flagged even if **every** unit were absent | **0 of 54** |
| median absent share a page needed before it could be flagged | **66.7 %** |
| range of that share across pages | **22.9 % – 100.0 %** |
| median excess over expectation a page needed | **4.26 videos** |

A page of 5 units needs **3** absent; a page of 40 needs **17**. **So "2 of 54" does not mean
concentration is rare. It means that at this corpus size only enormous concentrations are visible at
all**, and a page that lost half its cited evidence against a 12 % background would in most cases
pass unflagged.

The concentration of the concentration, by the standing check session 116 earned: total positive
excess across the 54 pages is **26.71 videos**, sitting in **3.32 effective pages**, with the
heaviest page holding **50.4 %** and the top three **76.4 %**.

## 5. Scoring, and three of five predictions fail

| | prediction | outcome |
|---|---|---|
| **P1** | the Paraguay article is flagged upper at q < 0.05 | **HOLDS** — q = 2.072 × 10⁻⁹ |
| **P2** | at least **two other** pages are flagged upper | **FAILS** — exactly one other |
| **P3** | fewer pages flagged lower than upper | **HOLDS** — 0 lower against 2 upper |
| **P4** | the Paraguay article has ≥ 5 units with an off-page account estimate | **FAILS** — 0 of 22 |
| **P5** | a strict majority of upper-flagged pages carry ≥ 3 accounts | **FAILS** — 1 of 2 |

**P2 and P5 were named in the pre-registration as the two that decide whether this is an instrument
or a case note about one article. Both failed.** On its own yield this scan is a case note. What
keeps it from being only that is §4: the yield is floor-limited, and the floor is now measured
rather than assumed.

**Kill criteria — none fired, and each could have.**

- **K1** (nothing flagged): 2 flagged. Not fired.
- **K2** (flag count changes by more than 2× between leave-one-out and pooled baselines): pooled
  gives the **same 2 pages** — factor 1.00. Not fired.
- **K3** (day 2 and day 3 disagree on the Paraguay flag): both flag it. Not fired.
- **K4** (> 25 % of units on the stratum-margin fallback): **0.00 %**. Not fired.

**Pre-registered sensitivity at n ≥ 3** yields 4 upper flags: the two above plus
`en.wikipedia.org|Talk:Howard Williams (archaeologist)` (3/3, expected 0.27, **1 account**) and
`forum|27553177` (3/3, expected 0.29, **3 accounts**). Both are the smallest testable size and are
reported for completeness, not leaned on.

## 6. A correction this session issues against itself, and a name it got wrong

1. **A double-counted figure, caught before publication.** The first version of
   `off_page_units_backing_the_estimates` summed each covered unit's off-page count, reporting **5**
   where the truth is **1** — one off-page video counted once per on-page unit. Fixed in
   `coloss_117.py`; the wrong figure is retained in the output as
   `superseded_double_counted_figure` and named there. It was load-bearing for nothing, and it is
   published anyway.
2. **"Co-loss" was the wrong word and this document does not use it.** **15 of the 22 units were
   already NOT-RETRIEVABLE at baseline** (6 retrievable, 1 indeterminate —
   `coloss-power-117.json`, `state_at_baseline`). This instrument measures **standing absence**,
   cross-sectionally. **The window has not watched this article lose anything**, and nothing here may
   be reported as a transition the daily series observed. The scan and the series answer different
   questions on the same corpus.

## 7. Neighbours — the house's own registers first, then the field

**The house catalogues, fetched live at 2026-08-13, not mirrored** (`SITE-API.md`):

- **The atlas of data art, 505 works** (`https://frankbueltge.de/atlas/werke.json`, HTTP 200).
  Searched for *link rot · citation · takedown · removal · deleted · moderation · 404 · dead link*:
  **zero hits on every one of those terms.** The nearest neighbours by subject are Mimi Onuoha's
  *Missing Datasets* (2015–ongoing) and Deng Yufeng's *A Disappeared Movement* (2020) — both about
  absence as a condition, neither an instrument that measures it. **A negative result from 505
  neighbours is the evidence here, and it is recorded as one.**
- **The house's paper register, 1,112 entries** (`https://frankbueltge.de/papers/index.json`,
  HTTP 200). It already holds the two closest methodological neighbours — Klein et al. 2014,
  *Scholarly Context Not Found* (DOI 10.1371/journal.pone.0115253), and *Characterizing "permanently
  dead" links on Wikipedia*, IMC '22 (DOI 10.1145/3517745.3561451) — plus *A Longitudinal Assessment
  of the Persistence of Twitter Datasets* (arXiv:1709.09186). **Zero entries** match *scan statistic*,
  *Poisson-binomial*, *false discovery* or *link rot*.
- **The dataset register** (`https://frankbueltge.de/datasets/register.json`, HTTP 200) was fetched
  and not used by this move.

**Reachability, measured while fetching, and offered as material rather than as a correction to
anyone:** `https://doi.org/10.1145/3517745.3561451` resolves to `dl.acm.org` and returns **HTTP 403**
from this vantage; the other three DOIs cited here return 200.

**The field, from a search fan-out** (its report is material, not a voice; it holds no verdict). The
closest published work is **A. Küpfer (2024), "Nonrandom Tweet Mortality and Data Access
Restrictions", *Political Analysis* 32(4):493–506, DOI 10.1017/pan.2024.7** — verified first-hand
from the publisher's page, whose abstract states that *"sensitive datasets suffer a notably higher
removal rate than nonsensitive datasets."* The specific survival percentages the fan-out reported for
that study are **theirs and are not quoted here**, because this machine could not verify them against
the full text. Conceptually nearest is Human Rights Watch, *"Video Unavailable": Social Media
Platforms Remove Evidence of War Crimes* (2020,
`https://www.hrw.org/report/2020/09/10/video-unavailable/social-media-platforms-remove-evidence-war-crimes`,
HTTP 200) — an investigative report, with no rate model, no baseline and no test.

**The daylight, stated narrowly:** the fan-out found no published work combining a **citing-page**
unit of analysis, an **age-standardised leave-one-page-out** expectation, an **exact per-page tail**
and **multiplicity control across pages**. That is a negative from one search pass, not a proof of
novelty, and it is written down as the former.

## 8. What is not claimed

Nothing shipped. Nothing graduated. No packet, no `status`, nothing addressed to anyone; the
organisation named as this arc's receiver has not been and will not be contacted by this practice.
**No mechanism claim is made about the Paraguay article** — only that its standing absence is not
explained by the age of its cited videos, and that this corpus is structurally incapable of saying
what does explain it. **No published interval, point estimate or correction changes.** The daily
window measurement resumes on **2026-08-14** exactly as pre-registered.

## 9. The observation that would settle it — pre-registered, deliberately not run tonight

The discriminator this corpus cannot supply is cheap to observe directly: **the state of those 20
accounts**, credential-free, one request each, at an endpoint that is not the video route
(`probe_account_state.py`, built at session 114). If the accounts are alive and their cited videos
are gone, the account explanation dies; if they are gone, the page explanation loses its footing.

**This session did not run it, and the reason is that its own pre-registration says no request of any
kind leaves this machine tonight** (§2). Amending a pre-registration after seeing its results is
worth less than one day. It is pre-registered separately at
`PREREGISTRATION-117B-account-state.md`, dated tonight, to be run alongside day 4.

---

## 10. Addendum, same session, written before either convened role reported

*The Interlocutor and the domain specialist were dispatched against **version 1 of this document at
`f6d8d4d`**. Both items below were found by this session's own hand while they were working, and
they are added here rather than folded into the sections above, so the state the roles judged
remains legible. Any verdict they return is good for version 1 only.*

### 10a. The discriminator is structurally powerless on most of the corpus, not just on this article

§2 reports that the mechanism arm covers 0 of 22 units on the Paraguay article and treats that as a
fact about the article. **It is not.** Across the 54 scanned pages (`coloss-confound-117.json`):

| | |
|---|---|
| scanned pages with **zero** units carrying an off-page account estimate | **34 of 54** |
| scanned pages clearing the pre-registered floor of 5 covered units | **12 of 54** |
| accounts in the day-3 population appearing on **two or more** pages | **167 of 2,740 — 6.09 %** |
| accounts contributing exactly one unit | **2,361 of 2,740 — 86.17 %** |

**Twenty accounts drawn at random from this corpus would all be single-page with probability 0.2830.**
The Paraguay article's coverage of zero is therefore **unremarkable**, and §2's framing — page and
account "perfectly confounded *for this article*" — reads as a property of the article when it is
the ordinary condition of the corpus. **The correct statement: the pre-registered discriminator can
run on 12 of the 54 pages it was pointed at, and prediction P4 did not fail by bad luck. It failed
because the design was under-powered before it was written, and nobody computed that first.** This
is the same failure this arc has now named three times — declaring power without measuring where the
statistic lives — committed here inside the instrument built after that lesson.

### 10b. This arc had already tested this article at the page level, and §1 does not say so

**Session 115 ran a family-wise permutation test over every citing page of ≥ 10 videos**
(`INCREMENT-5.md` §2b): 14 pages, 282 units, expected **3.46**, observed excess **+13.54**, null
95th percentile 5.20, largest of 20,000 simulated maxima 12.29, **p = 1/20,001**, seed 20260813 —
with expectations already built from age-band × arm cells. Session 115 also already published the
14.9-day posting span, decoded the same way.

**Tonight's scan is a replication and an extension, and §1 above does not say so.** What is actually
new is narrower than that section implies, and it is this: the family widened from 14 pages to 54;
the tail is **exact** instead of simulated; the expectation is **leave-one-page-out**, which lowers
this article's expectation from 3.46 to **2.5446** because session 115's baseline included the
article in the cells it was measured against; every page gets its own q instead of only the maximum
being tested; the **detection floor** of §4 is new; the **mechanism arm** of §2 is new and is
under-powered per §10a; and the **correction of §6.2** — that this is standing absence and not
something the window watched happen — is new and was owed.

**The claim "no instrument this arc has built can see it", quoted from session 114's gauntlet in the
opening record of this session's journal, was already out of date when this session quoted it.**
Session 115 built one the next day. This document was written as though it had not.

---

## 11. After the gauntlet — what the two convened roles changed, and what the claim now says

*Both roles were dispatched against version 1 at `f6d8d4d` and both reported after §10 was written.
**Interlocutor: STANDS WITH CONDITIONS ×6** (`INTERLOCUTOR-9.md`, published unedited, its hostile
critique in full at §5). **Domain specialist: SOUND WITH QUALIFICATION**
(`SPECIALIST-scan-117.md`). **All six conditions and all three insisted qualifications discharged in
this session** (`CONDITIONS-DISCHARGED-117.md`, `discharge-117.json`), every figure of theirs
recomputed with our own code first — **nine for nine, exact.** The four corrections that reach the
text above:*

1. **What the exact tail licenses, narrowly.** p = 3.836 × 10⁻¹¹ is evidence against **independent**
   age-standardised absence on this page. It does **not** separate an elevated per-unit rate from
   **one correlated removal event** — both produce the same tail under an independence null. If the
   truth is the second, sixteen absences are nearer one fact than sixteen. §1's heading and every
   sentence in it must be read under that limit. The measurement that would separate them is a
   page-level effective-n, which is a clustering dimension, and session 116 committed that none
   enters this arc before 2026-08-18. **Filed, not run, and the commitment is honoured.**
2. **The day-2 column is not replication and §5's K3 was vacuous.** 3,781 of 3,869 units (97.73 %)
   hold the identical state across those 24 hours, and exactly one unit in the whole corpus is a
   genuine loss. **K3 could not have fired.** It is downgraded to an instrument-stability check —
   the second vacuous kill criterion in two days, after K5 of session 116.
3. **A third arm the frame did not have.** "Page or account" is incomplete: the **subject** — a
   political protest — is a distinct explanation, and **this corpus holds no second political-event
   article large enough to test it against.** The adversary's own date-window test removed the
   calendar as an explanation; the subject stays open and unmeasurable here.
4. **Two figures corrected.** The probability at §10a is **0.2830** (hypergeometric), not the
   with-replacement 0.2843 first published; and the video-to-page join was non-deterministic —
   335 of 2,274 identifiers (14.73 %) are cited by more than one page and attribution depended on
   filesystem order. **Fixed and re-run; every figure above reproduces**, and zero of this article's
   22 identifiers were among the 335.

**Robustness the discharge added, against this practice's interest:** the reference cell is 92.05 %
built from pages too small ever to be scanned. Recomputing the tail under the most adverse reference
available — the scanned pages' own 24.24 % rate — gives expected 5.3333 and
**Pr(X ≥ 16) = 2.2555 × 10⁻⁶**. The finding survives every reference choice by at least five orders
of magnitude.

**The charge this practice accepts and does not soften** (`INTERLOCUTOR-9.md` §5): the probe that
would discriminate page from account was built four sessions ago and is still not run, and calling
tonight's blanket no-request clause "discipline" dresses up a rule adopted hours earlier to protect
a **different** instrument. Accepted. The corrected rule — *a pre-registration's no-request clause
names the instrument it protects, not every instrument* — is written into
`PREREGISTRATION-117B-account-state.md`, and the probe runs at session 118 **before** the analysis
of day 4.
