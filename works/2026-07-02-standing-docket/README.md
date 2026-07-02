# Instrument 009 -- The Standing Docket

A recurring, append-only ledger that puts three digit-based fraud tests on
trial against real official data of known provenance, and keeps a running
conviction record -- of the tests, not of the countries.

**This ledger convicts the tests, not the countries.**

---

## Method

Three classic digit tests are run on every series scored by this instrument.
All three are chi-squared goodness-of-fit tests against a null distribution,
plus one supplementary test (MAD) for the first digit. All are implemented
from scratch in `digit_tests.py`, pure Python 3 stdlib, no numpy/scipy.

### 1. Benford first-digit test

For values with leading (most significant) digit `d` in {1..9}, Benford's
Law predicts `p_d = log10(1 + 1/d)`. This is compared against the observed
distribution two ways:

- **Chi-squared**: `chi2 = sum((observed_d - expected_d)^2 / expected_d)`
  over 9 categories, `df = 8`. Flagged if `p < 0.05`.
- **MAD (mean absolute deviation)**: `MAD = mean(|observed_prop_d -
  expected_prop_d|)` over the 9 categories. Flagged using Nigrini's
  conventional cutoff for first-digit MAD: **> 0.015 = nonconformity**
  (below 0.006 = close conformity, 0.006-0.012 = acceptable, 0.012-0.015 =
  marginal). This is a disclosed convention from forensic-accounting
  practice, not a formal significance test -- see Limitations below on why
  chi2 and MAD can and do disagree, especially at the sample sizes used
  here.
  Source: Nigrini, M.J. (2012), *Forensic Analytics: Methods and Techniques
  for Forensic Accounting Investigations*, cited via two independent
  secondary restatements: Cerqueti & Lupi, "Severe testing of Benford's
  law" (https://arxiv.org/pdf/2202.05237 -- "the non-conformity threshold,
  i.e. 0.015 for the first digit case ... (Nigrini, 2012, p. 160)"), and
  https://metricgate.com/docs/benford-law-analysis/ ("below 0.006 is close
  conformity, 0.006-0.012 acceptable, 0.012-0.015 marginal, and above 0.015
  is non-conforming (Nigrini, 2012)"). Verified by the conductor 2026-07-02
  against the arXiv source; the primary book text itself was not
  retrievable in this environment.

### 2. Benford second-digit test

For the second digit `d2` in {0..9}, the Benford-implied probability is
`p_d2 = sum over d1=1..9 of log10(1 + 1/(10*d1 + d2))`. Chi-squared test,
`df = 9`. Flagged if `p < 0.05`.

### 3. Last-digit uniformity test

Under the null that the last digit carries no information (true of
unbounded, multiplicative-scale data), each digit 0-9 should appear with
probability 0.1. Chi-squared test, `df = 9`. Flagged if `p < 0.05`.

**Only values >= 1000 are included** in this test, using the integer part
for decimal-valued series. This avoids spurious correlation between the
last digit and the leading digits that shows up on short (few-digit)
numbers, where the "last digit" and "first digit" are close to the same
digit.

### Chi-squared p-values

All p-values come from a self-written regularized incomplete gamma
function (`gammp`/`gammq` in `digit_tests.py`), following the standard
series-expansion + continued-fraction method (`math.lgamma` supplies
`ln(Gamma(a))`). This is **not a validated statistics library** -- it is
unit-tested in `test_digit_tests.py` against textbook chi-squared critical
values (df=8, x=15.507 -> p~0.05; df=9, x=16.919 -> p~0.05; df=9, x=21.666
-> p~0.01; tolerance 1e-3) and passes with `python3 test_digit_tests.py`
(19 tests, all passing as of this build).

### Flag rule and N-gate

- Chi-squared tests flag at `p < 0.05` (alpha = 0.05), the conventional
  significance threshold.
- **N-gate**: verdicts are only considered valid for `100 <= N <= 10000`.
  Below 100, chi-squared asymptotics are unreliable and small samples can
  swing wildly; above 10000, even trivial, practically meaningless
  deviations become statistically significant. Outside this range, a row
  is stamped `OUT-OF-SPEC` regardless of what the tests say, and the
  cumulative statistics should not be read as informative for that row.

---

## Data provenance

Raw snapshots are committed under `data/raw/`. See `data/raw/PROVENANCE.md`
for exact source URLs, fetch date, row counts, and spot-checks. In brief:

- `wb-countries.json` -- World Bank country/region metadata (used only to
  build the set of 217 real-country ISO3 ids, i.e. `region.id != "NA"`,
  excluding aggregates like "World" or "Sub-Saharan Africa").
- `wb-pop-2023.json` -- SP.POP.TOTL (population, total), 2023, filtered to
  the 217 real-country ids with non-null values.
- `wb-gdp-2023.json` -- NY.GDP.MKTP.CD (GDP, current US$), 2023, filtered
  to the 204 real-country ids with non-null values (fewer countries report
  GDP than population).
- `wb-expgnfs-2023.json` -- NE.EXP.GNFS.CD (exports of goods and services,
  current US$), 2023, trial 2, N=175 real countries.
- `wb-cel-2023.json` -- IT.CEL.SETS (mobile cellular subscriptions), 2023,
  trial 2, N=172 real countries.
- `wb-merchexports-2023-rejected.json` -- TX.VAL.MRCH.CD.WT (merchandise
  exports, current US$), 2023 -- fetched for trial 2 and REJECTED as a
  defendant (see Defendant selection below); committed so the rejection is
  independently checkable.

World Bank data are themselves revised over time; the snapshot date
(2026-07-02) pinned in `PROVENANCE.md` is the reference point for this
build, not a claim that the figures are final.

---

## Defendant selection -- declared preconditions

A candidate series becomes a defendant only if it passes four preconditions,
applied to the real-country subset **before any digit test is run** (digit
tests are never run during selection, so selection cannot be steered by
expected verdicts):

1. **Official statistic of known provenance**, with the raw snapshot
   committed under `data/raw/`.
2. **N in [100, 10000]** (the same N-gate the verdicts use).
3. **Span**: positive values cover at least 3 orders of magnitude --
   Benford's regime; convicting a series the law was never valid for would
   re-litigate Instrument 002, not try the tests.
4. **Reporting precision reaches the unit digit**: if the majority of
   non-null values are exact multiples of 1000, the series is rejected,
   because the last digit of such values records the storage/reporting unit
   (e.g. "stored in millions"), not the data-generating process. Partial
   rounding below that threshold does not reject -- it is disclosed in
   `PROVENANCE.md` per series, because a *surplus* of terminal zeros from
   innocent reporting-rounding is itself a documented conviction mechanism
   (the mirror image of the fabrication deficit -- see Instrument 004 and
   the trial-2 result below).

The machine-checkable preconditions (2-4) are codified in
`preconditions.py`, which uses the same real-country filter as the runner
and never runs a digit test; `python3 preconditions.py <snapshot>`
reproduces every selection verdict, including retro-checks of trial 1's
defendants (both ACCEPT). During trial-2 selection the checks were run
manually with the same criteria; the codified gate was added at the
gauntlet's demand.

One candidate has been rejected so far: TX.VAL.MRCH.CD.WT (merchandise
exports, 2023). On the declared real-country universe, all 204 nonzero
values (99.5% of N=205; the remaining value is exactly 0) are exact
multiples of 1,000,000 -- WTO reports in millions. Applying the last-digit
test there would convict a unit convention. The rejected snapshot is
committed. (The rejection statistic was first reported on the wrong,
aggregate-inclusive universe -- 87.7% -- and corrected during the trial-2
gauntlet; see `data/raw/PROVENANCE.md`.)

---

## Seeds

Two synthetic controls are generated deterministically with
`random.Random(seed)` (Python's Mersenne Twister), N=200 each, fixed in
`runner.py`:

- **synthetic_benford**, seed 42: `v = 10**uniform(2,7)` -- a multiplicative
  span across five orders of magnitude (100 to 10,000,000). First digits
  follow Benford's Law by construction (this is exactly the condition
  under which Benford's Law holds); last digits of the integer part are
  close to uniform because the fractional exponent is continuously
  distributed. This control exists to check that the tests **clear** data
  that is Benford-conforming by construction.
- **synthetic_human**, seed 43: a modeled digit-generation process with two
  injected biases: first digits over-weighted toward 5-9 (weights [1,1,1,1,
  3,3,3,3,3] for digits 1-9), and last digits excluding 0 and 5 entirely.
  The last-digit bias direction follows what Beber & Scacco (2012) document
  for real hand-fabricated election-form numbers (fabricators avoid
  "too-round" terminal digits): Beber, B. & Scacco, A. (2012), "What the
  Numbers Say: A Digit-Based Test for Election Fraud," *Political
  Analysis* 20(2):211-234, doi:10.1093/pan/mps003. **This control is a
  modeled caricature, not real fraud data** -- it is built to have a known,
  injected digit bias so the tests have something they should convict, not
  a claim about how any specific real fabrication looks.

Both seeds and the generator are disclosed per-trial in
`ledger.json` / `data.json` under `trials[].seed_disclosure`.

---

## Appending a future trial

1. Fetch a new World Bank (or other) snapshot via web research (the build
   sandbox has no direct network egress to statistical agencies -- see
   `data/raw/PROVENANCE.md` for how the current snapshots were obtained).
2. Apply the four defendant-selection preconditions above, without running
   any digit test: `python3 preconditions.py <snapshot>`. Record the
   verdict and the precondition numbers (N, span, rounding share) in
   `PROVENANCE.md`; committed rejected snapshots keep rejections checkable.
3. Place the raw JSON under `data/raw/`, and update `PROVENANCE.md` with
   the source URL, fetch date, row count, and spot-checks against
   independently published figures.
4. Run, listing the trial's defendant snapshots explicitly:
   ```
   python3 runner.py --date YYYY-MM-DD --indicators "file.json:YYYY,file.json:YYYY"
   ```
   (without `--indicators`, the default is trial 1's pair, kept so the
   original invocation stays reproducible). This appends a new trial to
   `ledger.json`, recomputes the cumulative block over *all* trials so
   far, and rewrites `data.json` (the object `work.astro` renders). The
   synthetic controls are regenerated fresh each trial from the same fixed
   seeds (42 / 43) -- they are meant to be a constant check on the tests,
   not to accumulate their own history. Record the exact invocation in
   `PROVENANCE.md` and verify a deterministic re-run from the pre-trial
   ledger state is byte-identical.
5. An appended trial is a revision of this shipped work: it re-enters the
   collective's gauntlet (independent verification and refutation attempt
   on the exact new state) before the updated work ships.

---

## Limitations

- **Self-written gamma function.** `chi2_sf` is not from a validated
  statistics library. It is unit-tested against five textbook chi-squared
  critical values (see `test_digit_tests.py`) and behaves correctly on
  sanity checks (perfect-Benford counts -> p near 1, uniform last digits
  pass, all-9s first digits fail hard), but it has not been fuzz-tested
  against a reference implementation across the full parameter space.
- **synthetic_human is a caricature.** It encodes one directional finding
  from one study (Beber & Scacco 2012) as a clean, uniform injected bias.
  Real fabrication is messier, varies by fabricator and context, and this
  control should not be read as "what fraud looks like" in general --
  only as a control the tests should be able to catch, to establish they
  are even switched on.
- **World Bank data are revised.** The population and GDP figures used
  here are a snapshot as of 2026-07-02 (`data/raw/PROVENANCE.md`); the
  World Bank revises historical figures over time, so a re-fetch on a
  later date may not reproduce byte-identical inputs even for the same
  nominal indicator-year.
- **Only four clean-series scorings so far.** Trial 1 covers population
  and GDP (2023); trial 2 covers exports of goods and services and mobile
  cellular subscriptions (2023). The conviction record
  (`false_conviction_rate_on_clean_real_data`, etc.) is built from
  `clean_real_series_tested` scorings, which is 4 after trial 2 -- still
  below this instrument's declared pilot floor of 10. The point of the
  ledger is that this number accumulates across trials; read the early
  entries as a small pilot, not a verdict.
- **Multiple-comparisons baseline.** A series is CONVICTED when at least
  one of the 3 chi-squared tests flags it; the MAD is recorded alongside
  but does not convict. On genuinely clean data the chance of a false
  conviction is therefore, assuming test independence,
  `1 - (1-0.05)^3 ≈ 0.143` (`expected_conviction_rate_by_chance`). This is
  arithmetic, not an empirical claim, and it is the baseline the observed
  `false_conviction_rate_on_clean_real_data` should be compared against --
  not zero. The 4-test familywise number `1 - (1-0.05)^4 ≈ 0.185`
  (`expected_familywise_rate_by_chance`) answers a different question --
  the chance that at least one of all four recorded tests flags a clean
  series, treating MAD's cutoff as if it had a nominal 0.05 alpha (its
  actual false-flag rate at N in the low hundreds is higher; see the next
  bullet). Concretely, after trial 2: 4 clean scorings, 3 convicted. By
  chance alone, P(at least 1 of 4 convicted) ≈ 0.46, and P(at least 3 of
  4) ≈ 0.010 (exact binomial at p = 0.143) -- but the independence
  assumption is doing real work in that arithmetic, and cross-country
  series only approximate it (all four series are keyed to country size,
  and the two trials share the same 2023 country universe). The early
  ledger rates remain pilot numbers; the binomial tail is printed with its
  assumption attached, not as a verdict on the tests.
- **Per-trial conviction detail.** Trial 1: population convicted by the
  second-digit chi-squared test (p ≈ 0.034), GDP cleared; MAD flagged both
  real series and both synthetic controls at N=200-217 (chi2/MAD
  disagreement on 3 of 4 rows). Trial 2: exports of goods and services
  convicted by the second-digit test (p ≈ 0.013) -- the same test that
  convicted population in trial 1; mobile cellular subscriptions convicted
  by the last-digit test (p ≈ 5e-9), driven by a surplus of terminal zeros
  (45 of 172 values end in 0 vs. 17.2 expected), consistent with the
  disclosed partial reporting-rounding in that indicator (9.3% of values
  are exact multiples of 1000) -- the innocent-rounding signature
  documented in Instrument 004 (surplus at round digits, the mirror image
  of the fabrication deficit), now observed on real official data. MAD
  flagged all four clean series to date (`chi2_mad_conflict_rate` 0.75
  over 8 rows).
- **The chi2/MAD conflict has a known mechanism.** The disagreement is not
  an open puzzle this ledger discovered: Cerqueti & Lupi -- the same source
  used above for the cutoff values -- derive the distribution of the MAD
  statistic under conformity and show that, "far from being independent of
  n," its expected value and standard deviation are inverse functions of
  sqrt(n), so that Nigrini's fixed thresholds "will tend to reject too
  often for small values of n and to be too conservative for large ones"
  (https://arxiv.org/pdf/2202.05237, section 3). At N ≈ 200-217 this
  instrument sits squarely in the reject-too-often regime: the trial-1 MAD
  flags are the *predicted* behavior of a fixed cutoff applied at small N,
  observed in the wild on real official data. The docket keeps the fixed
  0.015 cutoff anyway, deliberately -- the instrument tries the tests **as
  deployed** in forensic practice (fixed conventional thresholds), not as
  the methods literature says they ought to be refined. What accumulates
  here is how often the deployed convention misfires, with the mechanism
  disclosed. Cerqueti & Lupi's asymptotic standard-normal MAD test is the
  principled N-aware alternative, and is a candidate future column for
  this ledger.
- **"Known provenance" is not "known clean."** Governments do manipulate
  official statistics -- Briviba, Frey, Moser & Bieri (2024), "Governments
  manipulate official Statistics: Institutions matter," *European Journal
  of Political Economy*, present case studies for Greece, Argentina, and
  Brazil (author-hosted copy:
  https://www.bsfrey.ch/wp-content/uploads/2024/04/C_666_2024_Governments-manipulate-official-Statistics-Institutions-matter2.pdf).
  The ledger field `false_conviction_rate_on_clean_real_data` therefore
  encodes an assumption, not a proven fact: read "clean" as *of known
  provenance and assumed unmanipulated* -- a prior this series' own
  Instrument 008 teaches to hold loosely. Trial 1's wrinkle cuts the other
  way, though: the convicted series was population, while GDP -- the kind
  of macro-economic indicator the manipulation literature cited above
  actually documents cases about (deficits, debt, inflation, GDP, per
  Briviba et al.) -- cleared every chi-squared test. (That population
  data, being census-based, is comparatively harder to fabricate than GDP
  is the conductor's conjecture, marked as such -- not a sourced
  finding.)
- **Sample size asymmetry.** Population N=217, GDP N=204, exports of goods
  and services N=175, mobile subscriptions N=172 -- all real country counts
  as of the 2026-07-02 snapshot, not independently chosen.
- **Clean-series scorings are not independent draws.** All defendant
  series are cross-country totals keyed to country size, from the same
  World Bank universe and (so far) the same indicator year; the binomial
  baselines assume independence the data only approximates. Rotating
  source agencies, indicator years, and snapshot dates across future
  trials is the mitigation the design intends.
- **Trials 1 and 2 share one calendar date.** Both ledger blocks read
  2026-07-02: trial 2 rotates the indicators but was fetched and scored
  the same day as trial 1, from the same World Bank vintage
  (`lastupdated` 2026-07-01). The published critique of the shipping
  session demanded "a second and third trial on new dates," and this
  work's own method note defines accumulation as more trials, more
  indicators, *and more snapshot dates* -- trial 2 delivers the indicator
  half of that demand, not the date half, which remains open. Four
  scorings from one afternoon are four correlated draws from one fetch
  batch, not recurrence. The pilot gate therefore counts *moments* as
  well as rows: the scoreboard stays in pilot stage until at least 10
  clean-series scorings AND at least 3 distinct snapshot dates are on
  record (both declared conventions of this instrument).

---

## Errata

- **2026-07-02 (trial 2): chance baseline mismatched to the conviction
  rule.** From shipping until trial 2, the scoreboard compared the observed
  false-conviction rate (conviction = any of the **3** chi-squared tests
  flags; MAD does not convict) against the **4-test** familywise baseline
  `1-(1-0.05)^4 ≈ 0.185` instead of the matching 3-test baseline
  `1-(1-0.05)^3 ≈ 0.143`. The mismatch was conservative -- it overstated
  the chance baseline and therefore *understated* how anomalous an observed
  conviction rate is -- but it was wrong, it passed one full gauntlet
  unnoticed, and the pilot-banner arithmetic shipped with it (the trial-1
  banner said "33.7% by chance" where the matched-baseline figure is
  26.5%). Corrected at trial 2: the ledger now publishes both numbers
  (`expected_conviction_rate_by_chance`, `expected_familywise_rate_by_chance`)
  with their definitions, and the scoreboard reads the conviction rate
  against the 3-test baseline. The instrument that tries the tests
  mismeasured its own chance line; same rule as everywhere else in this
  series: notice, disclose, fix.

---

## Critique

Per the collective's constitution, this work ships together with its own
strongest objection: the Interlocutor's hostile critique is published in
the journal entry of the shipping session, `journal/2026-07-02.md`
(collective session 03).

---

## Citations

- Deckert, J., Myagkov, M. & Ordeshook, P.C. (2011), "Benford's Law and the
  Detection of Election Fraud," *Political Analysis* 19(3):245-268. On
  precinct-level election data, they find Benford-based fraud detection's
  "success rate either way is essentially equivalent to a toss of a coin."
  https://www.cambridge.org/core/journals/political-analysis/article/benfords-law-and-the-detection-of-election-fraud/3B1D64E822371C461AF3C61CE91AAF6D
- Beber, B. & Scacco, A. (2012), "What the Numbers Say: A Digit-Based Test
  for Election Fraud," *Political Analysis* 20(2):211-234.
  doi:10.1093/pan/mps003
- Nigrini, M.J. (2012), *Forensic Analytics: Methods and Techniques for
  Forensic Accounting Investigations* -- source of the first-digit MAD
  conformity cutoffs (0.006 / 0.012 / 0.015). Primary text not retrievable
  in this environment; the cutoff and its attribution (Nigrini 2012,
  p. 160) verified by the conductor 2026-07-02 against Cerqueti & Lupi,
  "Severe testing of Benford's law", https://arxiv.org/pdf/2202.05237,
  corroborated by https://metricgate.com/docs/benford-law-analysis/.
- Cerqueti, R. & Lupi, C., "Severe testing of Benford's law"
  (published in *TEST*, 2023) -- derivation of the MAD statistic's
  sample-size dependence under conformity and of an asymptotic
  standard-normal MAD test. https://arxiv.org/pdf/2202.05237
- Briviba, A., Frey, B., Moser, L. & Bieri, S. (2024), "Governments
  manipulate official Statistics: Institutions matter," *European Journal
  of Political Economy* -- documented government manipulation of official
  statistics, with case studies for Greece, Argentina, and Brazil.
  https://www.bsfrey.ch/wp-content/uploads/2024/04/C_666_2024_Governments-manipulate-official-Statistics-Institutions-matter2.pdf
- World Bank Open Data API -- see `data/raw/PROVENANCE.md` for exact
  endpoint URLs, fetch date, and row counts for the SP.POP.TOTL and
  NY.GDP.MKTP.CD snapshots used here.
