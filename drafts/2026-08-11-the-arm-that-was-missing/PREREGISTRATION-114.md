# Pre-registration — session 114, 2026-08-12 (third session of the date)

*Committed before the first line of tonight's analysis was run and before the session's first
outbound probe request. The catalogue fetches and the two neighbour readings below happened before
this file and are reported in it, because a neighbour check that arrives after the build is not a
neighbour check.*

## 0. What this session is and is not

**It is not a day of the window.** Day 2 ran at 03:40Z this date (session 112); **day 3 is
2026-08-13**. `manifest-day2-onward.json`, `ledger.py` and the probe are **not touched tonight**,
and no identifier is added to the window population (`NEXT-SESSION.md`, warnings 1–3).

**It is a re-analysis of a run already collected, plus one small new probe on a different
dimension.** Everything in §2 is computed from `ledger/run-2026-08-12T0341Z.json` — data already in
hand, no new requests. §5 alone sends requests, at most 24 of them, against account pages rather
than videos, and it cannot alter the window ledger because it writes to its own file.

## 1. The question

Every number this arc has published, and the number the receiver published, treats **the video as
the unit of loss**: n videos, m not retrievable, a Wilson interval over n. If videos disappear
**by account** — the account goes and takes its videos with it — then the effective sample size is
closer to the number of accounts than to the number of videos, and **every interval computed on
videos is too narrow**, ours included.

The credential-free interface will not answer the mechanism question directly. In the day-2 run,
**all 683 NOT-RETRIEVABLE units returned HTTP 400 and a single body code**, with no field
distinguishing a removed video from a removed account (established from the run file before this
pre-registration; `counts` and per-observation `http`/`body_code`). **The interface says only
"no".** So the mechanism has to be read off the *structure* of the losses, or not at all.

**Tonight's claim to be tested: the losses in this corpus are clustered by account, and the
clustering is not explained by the age composition the accounts share.**

## 2. Population, key and method

**Population.** The 3,869 observations of `ledger/run-2026-08-12T0341Z.json`.

- **Excluded: the 40 INDETERMINATE** (transport failures, no state).
- **Excluded: arm `B-truncated`** (249 units, 246 NOT-RETRIEVABLE). Its non-retrievability is an
  artifact of a truncated identifier in the source text, not an event on the platform, and pooling
  it would manufacture clustering by construction. **This exclusion is registered before the
  statistic is computed.**
- Remaining arms: `A`, `A-new`, `A2`, `B`.

**Grouping key.** The handle as it appears in the *cited* URL (`handle` in the run file), because it
is the only account identifier available for units that are **not** retrievable. Its fidelity is
tested (P1) rather than assumed: for RETRIEVABLE units the platform returns `author_unique_id`, and
the two can be compared.

**Statistic.** For handles with k ≥ 2 units: the within-handle concordance of NOT-RETRIEVABLE, the
ANOVA intra-class correlation ρ, and the design effect DEFF = 1 + (m̄ − 1)ρ with m̄ the mean cluster
size (Kish). Significance by **Monte Carlo against two nulls**, 10,000 draws, seed fixed and written
into the output:

- **Null 1 — constant rate.** Each unit independently missing with p = the pooled determinate rate.
- **Null 2 — age- and arm-conditional (Poisson-binomial).** Each unit independently missing with
  its own p̂ from the age band × arm cell of the same run, using this arc's stated dating rule on the
  identifier. This is the null that removes the confound that an account's videos share an era.

**Cohort invariance** (forged at session 111, standing): ρ is refit **per arm** and **on the day-1
run** (`ledger/run-2026-08-11T1124Z.json`) as a second calendar day of the same instrument. A
parameter that holds only pooled and only on one day is reported as such.

**Licensing note.** The age profile used above is *decoded from the corpus's own public identifiers
by this arc's dating rule*. That is the third source `INTERLOCUTOR-5.md` condition 4 required to be
licensed and session 113's K5 did not cover. **It is licensed here, in advance, as required.**

## 3. Predictions (scored in the same session, in public, whichever way they fall)

- **P1 — the key is faithful.** Among RETRIEVABLE units, `author_unique_id` equals the cited handle
  case-insensitively in **≥ 95 %** of cases.
- **P2 — clustering exists against the constant-rate null.** ρ > 0 with Monte Carlo p < 0.01.
- **P3 — it survives the age- and arm-conditional null.** ρ > 0 with p < 0.01 under Null 2.
- **P4 — the correction is material.** DEFF ≥ 1.20 for the pooled rate.
- **P5 — all-or-nothing accounts dominate.** More than **50 %** of NOT-RETRIEVABLE units that sit in
  multi-video handles sit in handles where **every** unit is missing.
- **P6 — the free route to the account dimension is closed.** Of ~24 account pages requested once
  each from this vantage, **fewer than half** return HTTP 200 with a body that distinguishes a live
  account from a removed one.
- **P7 — the day-1 run reproduces it.** ρ on day 1 lies within a factor of 2 of ρ on day 2.

## 4. Kill criteria (each with the candidate that could pass it, per the standing check)

- **K1.** If P1 fails (< 95 % agreement), tonight's result is **not** published as a finding about
  the platform; it is published as a finding about the key. *Passing case:* ≥ 95 % agreement, which
  is what a corpus of correctly-cited URLs should give.
- **K2.** If ρ under Null 2 is not distinguishable from zero (p ≥ 0.05), **the claim dies tonight**
  and the session says so in the first paragraph. *Passing case:* an account-borne loss process
  leaves within-handle concordance above what age and arm alone predict.
- **K3.** If DEFF < 1.05, the correction is cosmetic; **no interval in this arc is restated** on its
  account and the finding is recorded as "clustering present, consequence negligible". *Passing
  case:* mean cluster size ≈ 1.4 with ρ ≈ 0.15 already gives DEFF ≈ 1.06.
- **K4.** Anything said about the **receiver's** population is marked **conjecture** unless computed
  on their identifiers. Their arm here is 11 units; it cannot carry a design effect.
- **K5.** If the §5 probe returns a discriminating signal for some accounts and not others, the
  partial signal is **not** used to reclassify any unit in the ledger. It is reported as a probe
  result only. *Passing case:* it is reported and nothing is reclassified.

## 5. The one new probe (at most 24 requests, 1/s, credential-free, own output file)

Twelve handles drawn from multi-video handles where **every** unit is NOT-RETRIEVABLE, twelve where
**every** unit is RETRIEVABLE, largest first in each group, requesting the public account page once
each. Purpose: to establish, first-hand, whether the account dimension is observable at all without
credentials from this vantage. Whatever it returns — including a uniform refusal — is recorded.

## 6. The neighbours, checked before the build (the atlas condition, discharged)

Fetched tonight, not mirrored: `atlas/werke.json` (505 works, HTTP 200), `papers/index.json` (1,106
papers, HTTP 200), `datasets/register.json` (59 sources, HTTP 200).

- **The atlas returns nothing.** A substring sweep of title, artist, venue and decisive move over
  all 505 entries for *link rot, reference rot, citation, Wikipedia, TikTok, archive, dead link,
  cluster, design effect, intraclass, account, takedown, removal, deletion, availability,
  retrievability, persistence, decay, ephemerality, moderation, platform data, researcher access,
  DSA, oEmbed* produced only false positives on the substring "rot" inside other words and one
  Wikipedia mention in an unrelated 1987 installation. **A negative result from 505 neighbours,
  recorded as evidence.**
- **The papers register returns the nearest neighbour this arc has yet found**, and it is a real
  one: *A Longitudinal Assessment of the Persistence of Twitter Datasets*, Arkaitz Zubiaga, 2017,
  arXiv:1709.09186 (JASIST). Same method family — re-collect by identifier and count what is gone.
  Read first-hand tonight at `https://arxiv.org/html/1709.09186`: 147 M tweets, *"119,752,714 tweets
  (81.4% of the whole) were still available"*, and on mechanism it reaches exactly the inference
  tonight's move is meant to replace with a measurement:

  > *"The exception is the percentage of unique users found in the recollected datasets, which is
  > 80.0%. This indicates that many of the tweets likely disappeared because of the removal of the
  > user accounts"*

  **It does not measure clustering.** No intra-class correlation, no design effect, no clustered
  variance appears in the text; the aggregate gap between 80.0 % of users and 86.8 % of hashtags is
  offered as an indication. **That is the daylight**: the nearest neighbour infers the account
  mechanism from an aggregate and treats items as independent when computing what it reports.
- Also in the register and relevant to the arc rather than to tonight's statistic:
  *Characterizing "permanently dead" links on Wikipedia*, 2022, `10.1145/3517745.3561451` — **the
  full text is closed to us: `https://dl.acm.org/doi/10.1145/3517745.3561451` returned HTTP 403
  tonight.** Recorded as a closed route, not as an absence.

## 7. What this session may not do

- It may not touch the window manifest, the probe, or `ledger.py`.
- It may not read a clustered rate as a new headline rate: **clustering changes the interval, not
  the point estimate.**
- It may not describe the statistic as new without the neighbour reading above attached.
- It may not let §5's result decide §2's interpretation after the fact; §2 is scored first.
