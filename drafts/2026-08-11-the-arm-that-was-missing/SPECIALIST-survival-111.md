# Specialist review — survival analysis and study design, session 111 power audit

**Role:** convened domain specialist, no vote, no verdict. This document evaluates whether
`PREREGISTRATION-111.md` / `power_audit.py` / `POWER-AUDIT.md` / `power-audit.json` used the
right methods, and where a specialist would have done something different. Every number below
was computed by me on this machine, using the actual raw ledger file
(`ledger/run-2026-08-11T1124Z.json`), not copied from the session's own output — so this is an
independent reproduction plus extension, not a re-statement. Scripts are saved at
`specialist-survival-scripts/*.py` in this directory; every command and its actual stdout is
reproduced verbatim below. Environment: `python3 --version` → `Python 3.11.15`; confirmed no
`numpy`, no `scipy` on this machine — everything here is pure standard library, same constraint
the session worked under.

Statements are marked **[established]** when they rely on a citable, retrievable source,
**[my computation]** when they come from code I ran (reproduced below), and **[judgement]** when
they are my professional opinion with no external citation. Nothing here is invented; where I
could not verify a number I say so rather than assert it.

---

## 0. Independent reproduction, before anything else

```
$ python3 repro.py
=== SANITY: reproduce session's own load ===
n analysed: 2618 excluded: {'arm_B_truncated': 249, 'indeterminate': 33, 'not_19_digit': 4, 'nonpositive_age': 0}
live: 2320 frac: 0.8861726508785333
mean age: 2.8796361378641837
min age (days): 6.8577662037037035
min age among ALIVE (days): 6.8577662037037035
max age (years): 8.438259912033867

=== Weibull MLE (reproduction) ===
k = 0.6959  CI95 [0.5013,0.8990]  lambda = 0.01787  loglik=-899.2760

E (Weibull point est) = 1.3090  P(zero) = 0.2701
(session reported E=1.3090, P0=0.2701 -- match check above)
```

This matches `power-audit.json` to 4 decimal places on every figure I re-derived, from the raw
observations, independently coded. The data pipeline, the Weibull MLE, the profile-likelihood
CI, and the headline `E = 1.309, P(zero) = 0.270` are all confirmed. I did **not** find an
arithmetic or coding error anywhere in `power_audit.py`. The rest of this review is about
whether the *method* — not the code that implements it — is the right one, and about places
where the session's own narrative claims outran what the numbers actually show.

---

## 1. Is fitting a survival curve to a cross-sectional snapshot legitimate here?

**Yes, conditionally, and the session named the right condition — but under the wrong label,
and did not stress-test it.**

What is being fitted is not a "survival curve" in the longitudinal sense (one cohort followed
through time). It is a **single cross-sectional snapshot of a population with heterogeneous
ages**, read as if age-at-snapshot were equivalent to duration-since-origin in a single
homogeneous process. This is the same move demographers make when they build a **period
(cross-sectional) life table** instead of a **cohort (longitudinal) life table**: the period
table applies one calendar year's age-specific rates to a synthetic cohort and reads it as a
survival trajectory. That construction is exact only under a **stationarity assumption** — the
age-specific hazard schedule is not changing across the calendar/cohort dimension being
pooled over. Where period and cohort tables diverge is exactly where that assumption fails.
**[established]** — https://en.wikipedia.org/wiki/Life_table (see "Cohort vs. period tables";
this is standard demographic method, not contested).

The session's name for this, **"cohort-invariance"** (a 2019-created video faces the same
hazard schedule as a 2024-created one), is a reasonable plain-English coinage and it is
*substantively* the same restriction as demographic stationarity. It is not, however, standard
statistical terminology, and using the standard name matters because the standard name comes
with a known failure mode and known diagnostics: this is a "no cohort effect" / "no period
effect" assumption in event-history analysis, and violations are called **cohort effects**.
I'd recommend the session adopt that vocabulary going forward so it can draw on the existing
literature rather than reinventing diagnostics.

**How badly does it fail if violated, and does it actually fail here?** I tested this directly
rather than asserting it, by refitting the Weibull on two disjoint sub-populations of the same
corpus: cohorts created 2023–2026 (closest to today, least time for pruning/attrition to have
acted) versus 2018–2022.

```
$ python3 robustness.py
FULL (2018-2026, session's own set)
  n=2618 alive=2320 (0.8862)
  k=0.6959 CI95=[0.5009,0.8983]  lambda=0.01787/yr
  E on this subset's own live pop (n=2320) = 1.3090  P(zero)=0.2701

RECENT ONLY (2023-2026)
  n=1796 alive=1626 (0.9053)
  k=0.8590 CI95=[0.5530,1.1934]  lambda=0.03523/yr
  E on this subset's own live pop (n=1626) = 1.2191  P(zero)=0.2955

OLD ONLY (2018-2022)
  n=822 alive=694 (0.8443)
  k=0.8033 CI95=[0.1349,1.7559]  lambda=0.02288/yr
  E on this subset's own live pop (n=694) = 0.3249  P(zero)=0.7226
```

This is the concrete answer to "how badly": restricting to recent cohorts moves the fitted
shape from **k = 0.696 (CI excludes 1)** to **k = 0.859 (CI = [0.553, 1.193], includes 1)**.
Under the session's own K3 criterion ("the 95% CI on k includes 1 → shape undetermined, every
power figure must be published as a range, never a point"), **a defensible alternative
specification — restrict to cohorts least affected by the pruning and citation-selection
confounds the session itself names in §4 — would have made K3 fire.** The headline power
number (E, P(zero)) moves less than the shape parameter does (1.22 vs 1.31, about an 8%
change, both still well inside "underpowered" territory), so the *conclusion of this audit is
robust to this specific stress test*, but the claim that "the shape **is** determined" (K3, not
firing) is **not** robust to it. That is a real finding this session did not run and should.
**[my computation]**

**Verdict on Q1:** the identifying assumption is real, correctly identified in substance,
and the session's own confound list (§4: 2023 anomaly, cross-edition heterogeneity, pruning,
left truncation) already shows awareness that it may be violated — but the session asserted
this was "the largest weakness" without quantifying it, and a two-line robustness check (which
I ran, they did not) shows it is large enough to flip a kill criterion under a reasonable
alternative specification. That is worse than the session's own stated confidence, and better
than nothing — a specialist's one-sentence addition would be: *quote a shape estimate as a
[point, CI] pair conditional on the pooling window, and report how that pair moves across at
least one alternative pooling window, before declaring the CI "determined."*

---

## 2. Is the current-status / cross-sectional design being handled correctly?

**Yes.** Each observation is `(inspection time = age at snapshot, indicator of whether the
event — going not-retrievable — had already happened by that inspection time)`. This is
**current status data**, also called **case 1 interval-censored data**, a long-studied design
in biostatistics (classic applications: age at weaning, age at HIV seroconversion, age at
tumor onset from a single palpation). The standard reference survey is Jewell, N.P. and van der
Laan, M. (2004), "Current status data: review, recent developments and open problems," in
*Advances in Survival Analysis* (Handbook of Statistics vol. 23) — **[established]**,
https://biostats.bepress.com/ucbbiostat/paper113/ (also published version indexed at
https://www.sciencedirect.com/science/article/abs/pii/S0169716103230352).

The likelihood the session wrote is exactly the correct current-status likelihood for a
parametric Weibull: for a currently-retrievable identifier of age `t`, the contribution is
`S(t) = exp(-(λt)^k)`; for a not-retrievable one, `1 - S(t)`. I checked the code
(`power_audit.py:80-96`) against the textbook current-status likelihood term by term — it
matches, including the numerically-safe handling of `log(1 - exp(-x))` for small and large `x`.
**[established + code check]**

Two things a specialist would flag that the session's code is silent on:

- **Monitoring time here is deterministic given creation date, not literally a random draw**
  (as in the textbook current-status setup, where inspection times are random and independent
  of failure time). This is not a problem in itself — a deterministic-but-covariate-independent
  inspection time still satisfies the "noninformative monitoring" condition current-status
  theory requires, because the age at which each identifier happens to be inspected is fixed
  before anyone knows its outcome. **[judgement, but a standard and uncontroversial one]**
- **The nonparametric theory for current-status data has a well-known nonstandard asymptotic
  rate** — the nonparametric MLE of `S(t)` converges at rate `n^(1/3)`, not `n^(1/2)`, with a
  non-Gaussian (Chernoff) limiting distribution (Groeneboom & Wellner, 1992, *Information
  Bounds and Nonparametric Maximum Likelihood Estimation*; summarized in the Jewell/van der Laan
  review above). This does **not** apply to the session's fit, because the session used a
  correctly-specified 2-parameter *parametric* family (Weibull), which retains standard
  root-n / chi-square profile-likelihood behavior. I flag it only because if a future session
  is tempted to move to a flexible nonparametric or spline hazard "to be safer," it should know
  that comes with a genuine loss of estimation precision the parametric approach doesn't have —
  the parametric choice here is not a shortcut that should be apologized for; if anything it is
  the correct choice given the sample size. **[established]**

**Verdict on Q2:** design correctly named (once you use the standard term), likelihood
correctly written. No issue found.

---

## 3. Frailty — is the "forward hazard is lower, so E is an overestimate" claim correct?

**The concept the session invokes is real and correctly attributed. The specific directional
and magnitude claim in `POWER-AUDIT.md` §5 ("this pushes E below 1.31... the direction that
makes this audit's conclusion stronger") is not supported when tested, and is more confidently
stated than the arithmetic justifies.**

**The general phenomenon** — that a mixture of individually-constant-hazard subpopulations
produces an apparently *declining* population-level hazard, purely from selective survival of
the more durable subpopulation, with no individual actually "aging out of risk" — is the
central result of Vaupel, J.W., Manton, K.G., Stallard, E. (1979), "The impact of heterogeneity
in individual frailty on the dynamics of mortality," *Demography* 16(3): 439–454.
**[established]** — https://link.springer.com/article/10.2307/2061224,
https://pubmed.ncbi.nlm.nih.gov/510638/. The session cites this mechanism correctly in kind.

**But the specific inferential move needed checking, not just naming, and I ran it.** The key
fact the session's narrative misses: the fitted Weibull's own hazard function,
`h(t) = kλ^k t^(k-1)`, evaluated at each surviving identifier's current age, **is already the
marginal (selection-corrected) hazard of survivors** — that is the mathematical definition of
`-d/dt ln S(t)` for any mixture model whose survival function matches the fitted curve. There is
no additional "frailty discount" owed on top of a correctly-fitted marginal hazard; the
discount is already inside `k < 1`. Whether a further correction is needed depends on whether
the *Weibull functional form itself* is a good approximation to the true (frailty-generated)
marginal hazard at the specific ages in question — an empirical question, not a sign that can
be asserted from the mechanism alone. I tested it by fitting two explicit generative models
that instantiate the frailty story literally, to the same current-status data:

```
$ python3 frailty.py
n=2618, alive=2320

=== (1) Gamma-frailty, constant baseline hazard ===
theta = 6.89654  (CI95 on theta [1.79700,14.61316])
lambda0 (baseline/'frail unit' hazard) = 0.07345 /yr
loglik = -899.3272   (Weibull loglik was -899.2760, 2 free params either way)
AIC gamma-frailty = 1802.6543   AIC Weibull = 1802.5520
E under gamma-frailty marginal hazard = 1.3042   P(zero)=0.2714

=== (2) Two-point exponential mixture ===
p(frail)=0.0564  lambda_frail=1.00570/yr  lambda_durable=0.02540/yr
loglik = -899.3268   AIC (3 params) = 1804.6536
E under two-point-mixture marginal hazard = 1.3206   P(zero)=0.2670

=== SUMMARY: E and P(zero) across the three fitted models ===
model                              loglik      AIC        E   P(zero)
Weibull (session)               -899.2760 1802.5520   1.3090    0.2701
Gamma-frailty                   -899.3272 1802.6543   1.3042    0.2714
Two-point mixture               -899.3268 1804.6536   1.3206    0.2670
```

Model 1 is the textbook gamma-frailty construction (Vaupel-Manton-Stallard form): each
identifier has a *constant* individual hazard `λ0·Z`, `Z` gamma-distributed with mean 1 and
variance `θ`; the marginal survival is `S(t) = (1+θλ0t)^(-1/θ)`. Model 2 is a discrete two-type
mixture (fraction `p` "frail," constant hazard `λ_frail`; the rest "durable," constant hazard
`λ_durable`), the most literal possible instantiation of "some videos are fragile, some are
durable, no individual video's own risk changes with age."

Three findings from this:

1. **All three models fit the data almost identically well** (AIC differences under 2, which is
   not a meaningful difference by conventional model-selection thresholds). Cross-sectional
   current-status data of this size **cannot distinguish "true declining individual hazard"
   from "frailty mixture of constant hazards"** — this is not a defect of the session's fit, it
   is a known identifiability limit of single-spell duration data without covariates. The
   original claim that this distinction is essentially unrecoverable from single-spell data
   traces to Lancaster & Nickell (1980); Elbers, C. and Ridder, G. (1982), "True and Spurious
   Duration Dependence: The Identifiability of the Proportional Hazard Model," *Review of
   Economic Studies* 49(3): 403–409, showed identification is possible **only** under added
   structure (observed covariates, or restrictive parametric assumptions on the frailty
   distribution) that this corpus does not have. **[established]** —
   https://academic.oup.com/restud/article-abstract/49/3/403/1703596. The practical upshot,
   which I verified rather than assumed: with no covariates and this sample size, the three
   models are empirically indistinguishable here.
2. **The direction of the correction is not reliably "down."** Gamma-frailty gives
   `E = 1.304` (0.4% below the Weibull's 1.309); the two-point mixture gives `E = 1.321`
   (0.9% **above** it). Neither move is large enough to matter for the power conclusion, and
   they don't even agree on sign. The sentence in `POWER-AUDIT.md` — "this pushes E below
   1.31... the direction that makes this audit's conclusion stronger, which is exactly why it
   is stated here" — asserts a specific direction and calls out its own good luck in finding a
   confound that favors its conclusion, without having checked that the direction actually
   holds. It happens to hold for one of two natural frailty specifications and not the other,
   and by an amount (<1%) an order of magnitude smaller than the session's own sensitivity band
   already covers (their `k∈{0.5,0.75,1.0}` band moves `E` from 1.07 to 1.62, a much bigger
   range than frailty adds). **[my computation]**
3. **What frailty legitimately changes is not the magnitude of E but the interpretation of
   `k<1`.** It is correct, and worth keeping, that `k<1` should not be read as "each video gets
   individually safer as it ages." It is not correct, on the evidence, that frailty gives this
   audit's headline number an additional downward push worth naming as a reason the conclusion
   is conservative.

**Verdict on Q3:** the mechanism is real and correctly named; the specific quantitative claim
built on it is an overclaim that, when tested, turns out to be within noise and possibly
wrong-signed. It does not change the bottom line (still underpowered either way) but the
session should not have stated a direction it hadn't checked.

---

## 4. Is the forward-hazard-to-expected-transitions step right?

**Yes, to a level of precision far beyond what matters here — I checked the two places an error
could plausibly hide and found none large enough to matter.**

**Exposure accounting.** "Seven daily runs bind six one-day intervals" is the correct way to
count exposure windows from a fence-post series of measurement times — standard practice
in any panel/longitudinal design (`n` observation times give `n-1` observable intervals). No
issue.

**The "Poisson approximation."** I checked whether `P(zero) = exp(-E)` where
`E = Σ_i D·h(t_i)` is actually an approximation, and how good it is, by computing the *exact*
product of each identifier's own survival probability over its 6-day window
(`S(t_i + Δ)/S(t_i)` under the fitted Weibull, not the piecewise-constant-hazard shortcut the
session used) and comparing:

```
$ python3 checks2.py
=== Step 4 check: constant-hazard-over-window approx vs exact Weibull integral ===
E (session's piecewise-constant approx) = 1.309048  -> P(zero)=0.270077
exact integral of Weibull hazard over each identifier's 6-day window:
   P(zero) exact = 0.271144   (implied E_exact = 1.305106)
   relative difference in P(zero): 0.3950 %

exact PRODUCT over 2320 independent identifiers = 0.271144
(confirms: taking logs of (1-p_i) and summing is identical to -sum(p_i) to ~1e-6; the
 'Poisson approximation' language is essentially exact here given how small each p_i is)
largest single-identifier 6-day failure probability in the corpus: 0.002095
```

Two sub-checks, both clean: (a) treating the 2,320 identifiers as independent low-probability
events and summing their hazards (`exp(-Σp_i)` ≈ `∏(1-p_i)`) is accurate to about 1 part in
a million here, because the largest single 6-day failure probability in the whole corpus is
0.0021 — nowhere near where the Poisson approximation would start to matter; (b) using the age
at the reference instant instead of integrating the (declining, since `k<1`) hazard across the
6-day window overstates `E` by 0.4%, in the conservative direction (it very slightly *increases*
the apparent power of the design). Neither issue is worth a correction.

**Is the marginal hazard the right forward rate for an identifier already known to be alive?**
Yes, by the same identity used in §3: the marginal hazard function of a fitted survival curve
*is*, by construction, the expected hazard of the surviving subpopulation at that age. This is
not something that needs a separate frailty adjustment layered on top (see §3) — it is already
what a correctly-fitted `h(t)` represents. The one caveat, not a Poisson-approximation issue but
a modeling one: this is only right if the fitted `S(t)` (i.e., cohort-invariance, §1) is a good
description of the true marginal survival function going forward in time — the design is
correctly *conditioning on survival*, but it is *not* correctly insulated from cohort effects,
which is a real, separately-flagged issue (§1), not a "forward hazard" bug.

**What is missing:** the headline `E` and `P(zero)` are point estimates from the point-estimate
`(k,λ)`; no uncertainty from the fit itself is propagated into them except via the separate,
coarse `k∈{0.5,0.75,1.0}` sensitivity table. See §5 for how much that matters (not much, here,
but it should be done properly as a matter of practice, not luck).

**Verdict on Q4:** correct, with margins of error (0.4%, ~1e-6) that are irrelevant next to the
27-point spread the sensitivity table already reports.

---

## 5. Is the likelihood ratio the right way to score a "zero transitions" result?

**It is a legitimate and correctly-computed statistic, in a defensible framework (Royall's "law
of likelihood"), and the session's own conclusion — that 3.7:1 is weak, not decisive — is the
textbook-correct reading of that number. But it is a plug-in point-estimate LR, and there is a
more defensible version available; I built a sketch of it and it moves the number, modestly, in
the direction that makes the churn signal look *weaker*, not stronger.**

**Is 3.7:1 weak?** Under Royall's framework for measuring statistical evidence via likelihood
ratios, `k=8` and `k=32` are the conventional benchmarks separating "weak," "fairly strong," and
"strong" evidence (Royall, R., 1997, *Statistical Evidence: A Likelihood Paradigm*; the
benchmarks are also given in Blume, J.D., 2002, "Likelihood methods for measuring statistical
evidence," *Statistics in Medicine* 21(17)). **[established]** —
https://onlinelibrary.wiley.com/doi/abs/10.1002/sim.1216,
https://books.google.com/books/about/Statistical_Evidence.html?id=oysWLTFaI_gC. An LR of 3.7:1
sits below even the "weak → fairly strong" threshold of 8. The session's reading — that a
pre-commitment to treat this as decisive was a mistake — is the correct application of this
framework, not an overstatement.

**Is a point-vs-point LR the best available comparison, though?** A specialist's objection to
any plug-in LR is that it treats the alternative hypothesis's rate as if it were known exactly,
which understates the alternative's own uncertainty and can make the alternative look
artificially more (or less) probable than it should. The right correction is a Bayes factor
that integrates the "some churn is real" hypothesis over its own uncertainty in the rate,
rather than pinning it to the single MLE `(k,λ)`. I built a simple, explicitly-labeled *sketch*
of this — not a rigorous elicited-prior Bayesian analysis, but an importance-weighted average
of `P(zero|k,λ(k))` over the profile-likelihood curve already computed for the fit, treated as
an improper-flat-prior-on-k approximation:

```
$ python3 bayes_sketch.py
=== Q5 sketch: plug-in point estimate vs profile-weighted average ===
P(zero) at point MLE (k=0.696, session's number)      = 0.2701
E_theta[ P(zero|theta) ] over the profile-likelihood   = 0.2771
  (weight w(k) = exp(loglik(k) - loglik_max), i.e. an improper-flat-prior-on-k
   importance sketch -- NOT a proper posterior; illustrative of direction only)
ratio: weighted/point = 1.0259

Jensen's-inequality direction check: exp(-E) is convex in E, so averaging over
parameter uncertainty should push P(zero) UP relative to the point estimate,
which weakens (not strengthens) the case for churn. Observed direction: UP (weaker churn signal)

=== LR framing ===
LR (session's framing, point-vs-point) = 1 / 0.2701 = 3.703 : 1
LR using profile-weighted P(zero)       = 1 / 0.2771 = 3.609 : 1
```

The direction is exactly what convexity of `exp(-E)` predicts (Jensen's inequality: averaging a
convex decreasing function over parameter uncertainty raises its expectation relative to
plugging in the mean), and the magnitude is small here (about 2.6%, because the current fit is
already fairly well-pinned by 298 observed deaths) — but it is systematic, not noise, and it
always points the same way: honestly propagating uncertainty makes the "zero transitions is
surprising" story slightly *weaker*, never stronger. This means the session's headline
`LR ≈ 3.7:1` is, if anything, a mild overstatement of the evidential weight against the
no-churn hypothesis, in the same direction the session already concluded ("we promised to
treat a 4-to-1 result as decisive" — a specialist agrees the true number is a bit closer to
3.6:1, reinforcing that this was too weak to keep a hard-kill promise on).

**Is there a better framing than an LR at all?** For a live *design* decision — not just a
retrospective evidence grade — the standard tool is a **sequential test** (e.g., a Wald
sequential probability ratio test, SPRT), which sets in advance the LR thresholds at which the
process stops and declares for one hypothesis or the other, and continues collecting data
otherwise, rather than fixing the sample size (here, the 7-run window) up front and grading
whatever LR falls out. The session cannot retrofit this onto the pre-registered §5a window
(days are closed, per its own §0/§1), but it is exactly the right recommendation for what §5a's
*successor* criterion should look like, and I'd flag it as the single most useful design change
available (see §7). **[judgement, standard practice]**

**Verdict on Q5:** the LR is a legitimate, correctly-computed, and conservative-in-the-right-
-direction summary. A Bayes factor with a real prior, or better, a sequential design, would
serve the underlying decision better than a fixed-window LR — and moving to either would not
rescue the promise the session is worried about breaking; both point the same way it already
does.

---

## 6. The sample-size answer

**Arithmetic reproduced and confirmed exactly.**

```
$ python3 checks2.py   (excerpt)
=== Step 6 check: sample-size arithmetic ===
E needed for P(zero)<=0.05: -ln(0.05) = 2.995732
multiplier on live corpus = 2.288481 -> live_needed = 5310
days needed at current corpus = 13.730885 -> ceil 14
```

`5,310` live identifiers (a 2.29× multiplier on the current 2,320) or `14` days both check out
exactly against `-ln(0.05) = 2.9957`.

**Is "more identifiers" the right lever, versus more time, versus a different measurement?**
Days are foreclosed by the session's own pre-registration discipline (§0: cannot lengthen a
window retroactively without a dated amendment, and the session correctly treats that as a
promise worth keeping even when inconvenient). Given that constraint, more identifiers is the
only lever actually on the table tonight, and the session's framing of the choice is correct.

**Does the age structure matter — would enriching with young identifiers beat uniform
addition, and by how much?** Yes, and I quantified it. Because `k<1`, the fitted hazard is
strictly higher at younger ages:

```
$ python3 checks2.py   (excerpt)
=== Age-enrichment lever ===
  age=    1d (0.003y): per-day hazard = 6.967601e-04  6-day P(die) = 2.872770e-03
  age=    7d (0.019y): per-day hazard = 3.855247e-04  6-day P(die) = 2.085962e-03
  age=   30d (0.082y): per-day hazard = 2.476432e-04  6-day P(die) = 1.443154e-03
  age=   90d (0.246y): per-day hazard = 1.773018e-04  6-day P(die) = 1.052772e-03
  age=  180d (0.493y): per-day hazard = 1.436008e-04  6-day P(die) = 8.569319e-04
  age=  365d (0.999y): per-day hazard = 1.158187e-04  6-day P(die) = 6.929469e-04
  age=  730d (1.999y): per-day hazard = 9.380419e-05  6-day P(die) = 5.619662e-04
  age= 1825d (4.997y): per-day hazard = 7.098905e-05  6-day P(die) = 4.256311e-04

current live-corpus AVERAGE per-identifier per-day hazard: 9.404084e-05
corpus min observed age (days): 6.858

extra E needed: 1.6867
if EVERY new add were at the 2026-cohort mean age (0.340y, empirically supported):
   identifiers needed = 1748.4  (vs 2990 for uniform-age-mix adds)
```

Enriching entirely with identifiers at the age of the youngest well-populated cohort already in
the corpus (0.34 years, 164 identifiers, empirically supported — not extrapolated) would close
the gap to `P(zero) ≤ 0.05` with about **1,748 new identifiers instead of ~2,990** at the
current age mix — roughly a **41% reduction** in how many new identifiers are needed, for the
same power target. This is exactly the mechanism the session's own §6 (arm A2, the un-pruned
control) is reaching for, and the arithmetic backs it: age-targeted enrichment is a real,
quantifiable lever, not just a plausible-sounding idea.

**One caution the session should add before leaning on this lever further.** The Weibull
hazard has a mathematical singularity as `t → 0` for `k < 1` — the fitted model predicts
unboundedly high risk for an identifier of age approaching zero, which is a property of the
functional form, not a measured fact:

```
hazard at youngest OBSERVED age in corpus (6.86d): 3.879393e-04 /day
hazard extrapolated to age=1 day (no data support there): 6.967601e-04 /day  -- 1.80x higher
hazard extrapolated to age=0.01 day: 2.827289e-03 /day
```

At realistic scales for "identifiers created in the last few days" this is a modest, bounded
effect (1.8× at 1 day vs. the youngest age actually observed), not a runaway — but it grows
without limit as the enrichment strategy reaches for younger and younger material, and none of
it is empirically anchored below the corpus's actual youngest observed age of 6.9 days. A
specialist's recommendation: cap any enrichment-driven hazard credit at the youngest age with
real data support (here, ~7 days, or the 2026-cohort mean of 124 days if a larger, more stable
sub-sample is wanted), and do not extrapolate the power gain from identifiers younger than that
using this fitted curve. **[my computation + judgement]**

**Verdict on Q6:** arithmetic is exactly right; identifiers, not time, is correctly identified
as the only available lever; age-targeted enrichment is a real and fairly large lever
(quantified here at roughly 40% fewer identifiers needed) that the session's arm-A2 design
already intuits but did not put a number on.

---

## 7. The single biggest methodological error, and the single most important fix

**Biggest error:** the unchecked directional claim in §3 above — asserting that frailty makes
`E=1.31` "an overestimate" and explicitly noting that this direction is convenient for the
audit's own conclusion, without running the two-line check that would have shown the claimed
direction is not robust (one natural frailty model moves `E` down by 0.4%, another moves it up
by 0.9%). This is not a fatal error — it doesn't change the audit's bottom line — but it is
exactly the failure mode the session's own §0 was written to guard against: *an audit that
concludes "our kill criterion is underpowered" is structurally motivated to find reasons that
support that conclusion, and this is one place a plausible-sounding, mechanism-correct-in-kind
argument was allowed through without the arithmetic check that was available and cheap to run.*
The session was more careful about this elsewhere (P6 is scored as failing and explicitly
declines to over-interpret a weak result) — this one slipped past that same discipline.
**[judgement]**

**Single most important thing to do before the forward window opens:** run the cohort-
-invariance robustness check in §1 (refit `k` on cohort sub-windows) as a required step, not an
optional one, and report the CI-includes-1 result honestly against K3 — because on the evidence
I generated, a defensible alternative pooling choice would flip K3 from "not firing" to
"firing." If the practice wants to keep publishing a point shape estimate, it should publish
it alongside this sensitivity, the same way it already does for the `k∈{0.5,0.75,1.0}` band.
**[judgement]**

---

## 8. What the session got right without fully realizing it, and where it is too hard on itself

**Got right, undersold:**

- **The current-status likelihood is textbook-correct**, including the numerically careful
  handling of `log(1-exp(-x))`. This is not a small thing to get right from scratch with no
  `scipy` — I checked it term by term against the standard current-status likelihood and found
  no deviation. The session states this matter-of-factly in one line of §3 of the
  pre-registration and never revisits it, as if it were the least interesting part of the work.
  It is, on my review, the part with the least to criticize.
- **The Poisson-approximation language undersells how exact the calculation actually is.** The
  session writes "under a Poisson approximation" as if this were a simplifying assumption
  carrying real risk. I checked it exactly (§4): the approximation error is on the order of
  one part in a million, because the largest single-identifier 6-day failure probability in
  the whole corpus is 0.0021. This is not a place where the session should hedge; it should
  say "exact to the precision that matters here" and move the hedging budget elsewhere (e.g.,
  to §1, where it is actually needed).
- **The profile-likelihood CI methodology (chi-square 1-df, `2ΔLL ≤ 3.841`) is exactly the
  standard construction**, and correctly applied to a case (parametric current-status MLE)
  where standard asymptotics genuinely hold, as opposed to the nonparametric current-status
  case, where they famously don't (§2). This distinction was not discussed, but the choice
  made — parametric, not nonparametric — was the right one for this sample size regardless.

**Unnecessarily hard on itself:**

- The self-directed suspicion in §0 ("an audit that concludes our own kill criterion is
  underpowered is structurally an audit that hands this practice a reason to escape a
  promise") is well-calibrated as a general discipline, but in this specific case the
  headline conclusion does not actually depend on any of the places I found softness (the
  frailty overclaim, the point-estimate-only LR). Both of those, corrected, move the numbers
  by low single-digit percentages, in directions that if anything *support* rather than
  undercut "underpowered." The session does not need to worry that its own bias inflated the
  headline result — on my independent check, if anything the headline `P(zero)=0.270` is a
  slight *underestimate* of how weak the design's power really is (both the exact-integral
  correction and the uncertainty-propagation sketch push `P(zero)` up, not down, from 0.270
  toward roughly 0.277–0.280).
- The session flags "we did not know that when we published it" about session 110's 7.3-hour
  pair (LR ≈ 1.07:1). That is appropriately humble, and worth noting explicitly: the specific
  pre-registered guess in `PREREGISTRATION-111.md` ("adds ~0.30") for that same pair's expected
  transitions was itself off from the computed value (0.066) by roughly 4.5×. That is not a
  criticism — it is exactly the evidence for why hand-estimated hazard intuitions are
  unreliable enough that running the actual power calculation was the right call in the first
  place, and the session could cite its own pre-registered miss as supporting evidence for that
  argument rather than leaving it as an unremarked footnote.

---

## Appendix: reproducibility

All commands above were run from
`/tmp/claude-0/-home-user-field-research/5bb58988-490a-586c-98a6-fb4d57bc6c88/scratchpad` against
the real, unmodified ledger file at
`/home/user/field-research/drafts/2026-08-11-the-arm-that-was-missing/ledger/run-2026-08-11T1124Z.json`.
Copies of every script are saved at
`/home/user/field-research/drafts/2026-08-11-the-arm-that-was-missing/specialist-survival-scripts/`:

- `repro.py` — independent reload + Weibull MLE reproduction (§0)
- `frailty.py` — gamma-frailty and two-point mixture models (§3)
- `checks2.py` — exact-vs-approximate window integral, sample-size arithmetic, age-enrichment
  lever (§4, §6)
- `bayes_sketch.py` — profile-weighted P(zero) sketch (§5)
- `robustness.py` — cohort-window sensitivity of the Weibull shape (§1)

`python3 --version` on this machine: `Python 3.11.15`. `import numpy` and `import scipy` both
raise `ModuleNotFoundError` — confirmed before writing any of the above, same constraint stated
in `power_audit.py`'s own docstring.
