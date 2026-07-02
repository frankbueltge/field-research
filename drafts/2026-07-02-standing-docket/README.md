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

World Bank data are themselves revised over time; the snapshot date
(2026-07-02) pinned in `PROVENANCE.md` is the reference point for this
build, not a claim that the figures are final.

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
2. Place the raw JSON under `data/raw/`, and update `PROVENANCE.md` with
   the source URL, fetch date, row count, and any spot-checks.
3. If it's a new indicator, wire it into `runner.py`'s `build_trial()`
   (add a `load_indicator_values(...)` call and a `score_real_series(...)`
   entry).
4. Run:
   ```
   python3 runner.py --date YYYY-MM-DD
   ```
   This appends a new trial to `ledger.json`, recomputes the cumulative
   block over *all* trials so far, and rewrites `data.json` (the object
   `work.astro` renders). The synthetic controls are regenerated fresh
   each trial from the same fixed seeds (42 / 43) -- they are meant to be
   a constant check on the tests, not to accumulate their own history.

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
- **Only two indicators so far.** Trial 1 covers population and GDP for
  2023. The conviction record (`false_conviction_rate_on_clean_real_data`,
  etc.) is built from `clean_real_series_tested` scorings, which is 2 after
  trial 1 -- far too small to treat any rate in the current ledger as a
  stable estimate. The point of the ledger is that this number accumulates
  across trials; read the early entries as a small pilot, not a verdict.
- **Multiple-comparisons baseline.** Every series is put through 4 tests
  (3 chi-squared + 1 MAD). Even on genuinely clean data, the chance that
  *at least one* test flags it by chance alone is higher than the 0.05
  per-test alpha: assuming independence, `1 - (1-0.05)^4 ≈ 0.185`. This
  number (`expected_familywise_rate_by_chance` in the cumulative block) is
  arithmetic, not an empirical claim, and it is the baseline the observed
  `false_conviction_rate_on_clean_real_data` should be compared against --
  not zero. In trial 1, the population series was convicted by the
  second-digit chi-squared test (p ≈ 0.034) while GDP was not, and the
  first-digit MAD flagged *both* real series and *both* synthetic controls
  at N=200-217 despite the chi-squared first-digit test clearing three of
  those four -- i.e., MAD and chi2 disagreed on 3 of 4 series/controls in
  this trial. That disagreement rate is itself tracked
  (`chi2_mad_conflict_rate`) and is a first-trial data point suggesting
  Nigrini's MAD cutoffs, calibrated on larger forensic-accounting datasets,
  may be miscalibrated at N in the low hundreds -- a hypothesis for future
  trials to test as more data accumulates, not a settled finding from one
  trial.
- **Sample size asymmetry.** Population N=217, GDP N=204 -- both real
  country counts as of the 2026-07-02 snapshot, not independently chosen.

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
- World Bank Open Data API -- see `data/raw/PROVENANCE.md` for exact
  endpoint URLs, fetch date, and row counts for the SP.POP.TOTL and
  NY.GDP.MKTP.CD snapshots used here.
