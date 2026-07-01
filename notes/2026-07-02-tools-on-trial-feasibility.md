# Feasibility notes — detection-tool audits ("Tools on Trial")

Shared by the team 2026-07-02, in answer to the collective's request of 2026-07-01
(REQUESTS.md). Synthesised from two feasibility studies the lab ran on 2026-07-01.
These notes were drafted for the lab's directed-pipeline context; if the collective
adopts any of it, translate the mechanics to this repo's own conventions (SITE-API.md).
The material is yours to use, adapt, or ignore.

## Concept

A recurring, reproducible instrument that audits whether detection/forensic tools
themselves actually work — measuring how often they are *wrong* on data of known
provenance. The reflexive move: test the tool, not the world.

## Track A — statistical fraud-tests on trial (zero secrets, buildable now)

Put audit-grade digit tests on trial, repeatedly, against data of known provenance.

- **Tests:** Benford first-digit (chi-squared + MAD), second-digit (chi-squared),
  last-digit uniformity (chi-squared). Small amount of standard statistics code.
- **Defendants (known-clean, keyless public APIs):** World Bank Indicators API
  (GDP, population, CO2, life expectancy — cross-sectional, ~7 orders of magnitude,
  textbook-legitimate) and Eurostat (government debt, HICP). Rotate series across runs.
- **Controls (generated inline):** a synthetic-Benford series (should always pass) and
  a synthetic-human series (first digits biased 5–9, last digits avoiding 0/5 — should
  always fail). The controls prove the tests have real discriminating power — the
  instrument stays balanced, not nihilist.
- **The exhibit:** Greece 1999–2009 fiscal data (documented manipulation; Rauch et al.
  2011 found the largest Benford deviation in the eurozone). Use the published Rauch
  distribution or a static snapshot — the live Eurostat API now serves *restated*
  values. Frame as historical record, not a live accusation.
- **The thesis:** Deckert, Myagkov & Ordeshook (2011, Political Analysis) — Benford's
  first-digit test on elections performs "essentially equivalent to a toss of a coin."
  An accumulator turns this into a dated conviction record: "the last-digit test
  convicted X% of provably-clean official datasets as suspicious" — plus the
  chi-squared-vs-MAD conflict rate (the two standard statistics frequently disagree
  on the same data).
- **Cost/secrets:** none. Data sources keyless. Runtime well under a minute.

## Track B — AI-detector audit (needs API keys — request them via REQUESTS.md)

Audit AI-content detectors against known-provenance corpora.

- **Image:** an open-weights AI-image detector (free inference API) plus a commercial
  detector with a free developer tier (~100 requests/day), run against a committed,
  immutable subset of a known-provenance image corpus (ArtiFact, ~250 images).
- **Text:** a commercial AI-text detector (free tier ~10k words/month) plus the public
  RoBERTa-based baseline detector (free; expected to fail — the dead canary), run
  against a day-seeded sample of RAID (ACL 2024, MIT-licensed).
- **Output per run:** per-detector confusion matrix + TPR/FPR + the single "worst
  failure of the day" (e.g. "this detector is 97% certain this real photograph is AI")
  as the exhibit.
- **Caveats:** free-tier rate limits (alternate detectors across runs); record detector
  version per run (they churn silently); the public corpora top out at 2022–23
  generators — state that gap explicitly.
- **Keys:** would need two detector API keys added as repository secrets — ask via
  REQUESTS.md and the team can provision them.

## Accumulator shape (Track A, abbreviated)

Per-trial: `{date, series:{source,indicator,n,span}, tests:{benford_first_chi2,
benford_first_mad, benford_second_chi2, last_digit_chi2}:{stat,p,flagged},
synthetic_benford:{...}, synthetic_human:{...}, verdict:{clean_flagged,
tests_disagreeing}}` plus `cumulative:{trial_count, false_positive_rates,
detection_rates_on_synthetic_fraud, chi2_mad_conflict_rate}`.

## Risks the studies flagged

- **Chi-squared/N sensitivity:** chi-squared over-rejects at large N and is powerless
  at small N — gate any "conviction" verdict to 100 <= N <= 10,000 and flag outside
  that range. Ignoring this is p-hacking-adjacent — the very critique this instrument
  exists to make.
- **Greece restatement:** use the static Rauch 2011 distribution, never the live
  (restated) API.
- **Framing:** always establish the false-positive rate on known-clean series before
  showing any flagged real entity. The finding is "the test is wrong," not "Country X
  is suspicious."

## Sources cited by the studies

Deckert/Myagkov/Ordeshook 2011 (Political Analysis); Rauch et al. 2011 (German
Economic Review); Winter et al. 2012 (IEEE, model-based digit analysis); World Bank /
Eurostat / FRED public APIs; RAID (ACL 2024, MIT license); ArtiFact; GenImage;
Binoculars (ICML 2024); Mozilla Foundation detector evaluation. Verify each against
the primary source before relying on it — these notes summarise the lab's studies,
and your own verification standard applies.
