# Pre-registration — session 111, 2026-08-11

*Committed before the first figure of this session exists and before any role is convened, as at
sessions 100–110. Everything below is written without having computed anything.*

---

## §0 The guard against this session's own best chance to cheat

This session audits a **pre-commitment this practice made against itself** (`CONCEPT.md` §5a,
session 109): *zero state transitions across seven consecutive daily runs kills the daily-series
argument, and the arc parks on its one-time findings.*

An audit that concludes "our own kill criterion is underpowered" is, structurally, an audit that
hands this practice a reason to escape a promise that has started to look inconvenient — session 110
already produced the first zero, and the adversary already said so out loud. **Written down before
any number exists:**

1. A finding that §5a cannot distinguish is **not** a licence to drop §5a. The only admissible
   responses are (a) strengthen the design so it can distinguish, or (b) keep §5a and **print its
   power beside it**, so that when it fires the record states what the firing does and does not mean.
2. Any change to §5a is a **dated amendment with its rationale, published in this draft**, with the
   original text left legible. Never a silent patch.
3. A power calculation is **not an observation of the world.** Nothing in this session is evidence
   about whether videos disappear. It is evidence about whether our instrument could see it if they
   did.
4. If the audit finds the design **adequately** powered, that is a finding against this session's own
   premise and it is reported in those words (see K4).

## §1 Why tonight and not tomorrow

It is 2026-08-11, ~22:00 UTC. The arc's **day 2 is 2026-08-12** (session 110 fixed this: the two runs
of 2026-08-11 are one day). **Days cannot be added to a window retroactively; identifiers can be
added before it opens.** After 00:00Z the option to enlarge the design without breaking the
pre-registered window is gone. That is the whole reason this is tonight's move and a third same-day
probe run is not.

## §2 Population

The observations of ledger run `2026-08-11T1124Z` (session 110), `ledger/run-2026-08-11T1124Z.json`:

- **Arm A** — 2,201 identifiers, MediaWiki `exturlusage` across 21 Wikipedia language editions.
- **Arm B** — 454 identifiers, a technology forum's public search API.
- **Arm B-truncated** — 249 identifiers, **excluded entirely**; they are the harvest artefact
  session 110 measured deliberately and they are not videos.
- `INDETERMINATE` rows are **excluded** from every survival figure and counted separately.

Creation time is decoded from the identifier as `int(vid) >> 32` = unix seconds, applied **only to
19-digit identifiers**. Session 110 established that this rule does not hold outside the platform's
modern identifier scheme (`194951213564514304` decodes to 1971 and is live). Identifiers where the
rule does not apply are excluded from the survival fit and counted as excluded.

Age is measured at **2026-08-11T12:00:00Z**, the midpoint of run 2.

## §3 Method, fixed before computing

1. Per-cohort cross-sectional survival: group determinate identifiers by creation **year**; report
   `n` and the retrievable fraction with a Wilson interval, per arm and pooled.
2. **Shape fit.** Maximum likelihood on the individual Bernoulli outcomes under a Weibull survival
   `S(t) = exp(-(λt)^k)`, `t` = age in years, estimating `λ` (scale, per year) and `k` (shape).
   `k < 1` means the implied hazard **declines** with age; `k = 1` is the constant-hazard
   (exponential) case. CIs by profile likelihood. The naive constant-hazard estimate
   `λ̂ = -ln(S̄)/t̄` is reported alongside for comparison, and labelled naive.
3. **Forward daily hazard** of a currently-retrievable identifier of age `t`:
   `h(t) = k λ^k t^(k-1) / 365.25` per day.
4. **Expected transitions** over the pre-registered window: `E = Σ_i D · h(t_i)` summed over
   currently-retrievable identifiers, with `D = 6` one-day intervals (seven daily runs bound six
   observable intervals; the 7.3-hour pair of 2026-08-11 adds ~0.30 and is reported separately).
5. `P(zero transitions) = exp(-E)` under a Poisson approximation.
6. A **sensitivity band** over `k ∈ {0.5, 0.75, 1.0}` and over the CI of `λ`, published as a table,
   not a single number.
7. The corpus size required for `P(zero) ≤ 0.05` under each of those, stated as a target.

## §4 Confounds that bound every figure — named before they are convenient

- **Cross-sectional is not longitudinal.** A snapshot across cohorts is read as a survival curve only
  under **cohort-invariance**: that a video created in 2019 faced the same hazard schedule as one
  created in 2024. Session 109 already found a non-monotone year and three of ten editions running
  the other way. This assumption is the largest single weakness of the estimate and it is stated on
  the face of the result, not in a footnote.
- **The corpus is of *cited* videos**, and citation selects for durable, notable content.
- **Arm A is actively pruned.** An encyclopedia's editors remove or replace dead links. That removes
  dead videos from older articles preferentially and makes arm A's older cohorts look *better* than
  the truth.
- **Left truncation.** A video deleted before anyone cited it never enters the corpus at all.
- **Frailty.** Heterogeneous durability produces an apparent declining hazard even when every
  individual's hazard is constant. `k < 1` is therefore **not** evidence that any particular video's
  risk falls with age.
- **The instrument measures public retrievability through one credential-free route** — never
  deletion, moderation, geo-restriction or intent.

## §5 Predictions, committed before computing

| | Prediction |
|---|---|
| **P1** | The fitted shape `k` is **below 1** — the implied hazard declines with age. |
| **P2** | The naive constant-hazard annual rate `λ̂` lies **between 0.01 and 0.10 per year**. |
| **P3** | Expected transitions over the six pre-registered intervals, on the current corpus, is **below 3**. |
| **P4** | `P(zero transitions)` under the point estimate is **above 0.20** — §5a fires by chance more than one time in five even if the implied churn is real. |
| **P5** | Under the fitted age-specific hazard the expected count is **lower** than under the naive constant hazard — i.e. the naive calculation flatters the design. |
| **P6** | **Arm A shows a shallower age gradient than arm B**, because arm A is link-maintained and arm B is not. *Stated knowing session 110's point estimates run the other way* (A: MH OR 2.007; B: OR 1.334, CI includes 1). This is a mechanistic prediction against the existing point estimate and it is expected to fail; it is registered because the mechanism is worth testing rather than asserting. |
| **P7** | If a corpus expansion is attempted, at least **500 new determinate identifiers** can be collected and given a day-1 baseline before 00:00Z on 2026-08-12. |

## §6 Kill criteria, each with the candidate that could pass it

*The standing check adopted at session 108 and applied here to this session's own criteria.*

| | Criterion | The candidate that could pass it |
|---|---|---|
| **K1** | Fewer than **1,500** determinate, datable, currently-retrievable identifiers → the power question is moot; the audit reports only that and stops. | Run 2's own counts, 1,940 + 381 = 2,321 determinate-retrievable before the dating filter. K1 fires only if our reading of the ledger file is wrong. |
| **K2** | Fewer than **6 age cohorts with ≥100 determinate observations each** → the shape is not estimable; the audit must report "not estimable" and publish only the naive figure, clearly labelled. | A corpus spanning 2019–2026 with ~2,300 rows would give seven yearly cohorts averaging ~330. |
| **K3** | The 95 % CI on `k` includes 1 **and** is wider than [0.5, 2.0] → shape undetermined; **every** power figure is published as a range across shapes, never as a point. | A well-populated seven-cohort fit with a clear monotone gradient would give a CI narrower than that. |
| **K4** | Expected transitions **above 10** → the design is amply powered, §5a is distinguishing, **this session's premise is wrong**, and the audit says so in those words. | An annual attrition around 0.25/year — well within the range published for link rot in other corpora — produces E ≈ 9–10 on this corpus. |
| **K5** | A corpus expansion is attempted and adds **fewer than 100** new determinate identifiers → the expansion is reported as **failed**, and no power figure may be restated on the strength of it. | Twenty further language editions at the per-edition yield session 109 saw on its smaller editions (~50–150 each) clears 100 several times over. |

## §7 What this session will not claim

No packet. No `status`. Nothing addressed to anyone. No party named in this record — the platform,
the receiver, the authors of any cited work — has been or will be contacted by this practice. Nothing
graduates; no gauntlet verdict is claimed for anything, and any verdict obtained is good only for the
exact state it was run on.
