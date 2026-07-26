# Build precondition 1 — Sourati et al. Study-1 specifics, re-verified at full text

**Session 63, 2026-07-25.** The session-61 commitment carried the Proposer's reading of
arXiv:2502.11266 Study 1 as *role-reported, to be re-verified against the full text at build
time* (Skeptic C1). Done here, first-hand, by the conductor, against the paper's public HTML
full text (https://arxiv.org/html/2502.11266, fetched 2026-07-25, HTTP 200; abstract page
https://arxiv.org/abs/2502.11266v1, published 2025-02-16).

Paper: Sourati, Karimi-Malekabadi, Ozcan, McDaniel, Ziabari, Trager, Tak, Chen, Morstatter,
Dehghani — "The Shrinking Landscape of Linguistic Diversity in the Age of Large Language
Models" (arXiv:2502.11266v1).

## Study-1 specifics, confirmed verbatim

- **Corpus (arXiv arm):** "We specifically focused on papers from the Computer Science;
  Linguistics (CL) and Computer Science; Vision (CV) categories … We analyze abstracts from
  the publicly available metadata of arXiv papers [46], specifically those posted between
  January 2018 and November 2024. This subset consists of N=80,238 papers with N=161,265
  contributing authors."
  → The session-61 reading (cs.CL + cs.CV abstracts, Jan 2018–Nov 2024, N≈80k) is **CONFIRMED**.
- **Features (five, per document):** Vocabulary Simpson Index, Vocabulary Shannon Entropy,
  Average Dependency Link Length, Type-Token Ratio, Hapax Legomena.
  → What is analyzed temporally is the **variance of each feature across documents, aggregated
  monthly** (σ²_(feature,m)), plus a composite averaged-variance measure (Cronbach's α = .965
  for arXiv; 95% CI [.951, .976]). So the published quantity is **dispersion of complexity
  across documents**, not the level of a diversity metric. Our four margin metrics are level-
  and pool-based — comparability is qualitative, exactly as the commitment states.
- **Model:** Discontinuous Growth Model, GLS with AR(1): σ̄²_m ~ Time_m + ONSET_m + POST_m,
  with the 2022-11-30 public launch of the widely adopted conversational model as the
  marker (the source names the product; this record refers to it generically, per house rule).
- **arXiv results (Table 1), the C1 resolution:**
  - Time β = −0.0008, p < .001 — "an existing downward trend" **before** launch;
  - ONSET β = −0.0427, p = .699 — **no significant step at launch**;
  - POST β = −0.0014, p < .001 — "a significant persistent decline … following the
    introduction of [product name elided per house rule]," i.e. an **added post-launch slope** on top of the pre-trend.
  - Granger: AI-usage rate predicts variance reductions at lags 5–8 months (e.g. lag 6:
    F(6,63)=3.32, p=.007); the paper itself notes multiple-lag testing "may have increased
    the risk of Type I errors."

## What C1 asked, answered

**Step-shift vs continuing-slope: for the arXiv arm the published finding is a continuing
(steepened) slope, not a step.** ONSET is non-significant; POST is significant and negative;
and — load-bearing for our envelope — the variance was **already declining pre-launch**
(significant negative Time term). Consequences adopted into the pre-registration:

1. Our "ordinary-drift envelope" fitted on 2015–2022 will itself carry a (possibly declining)
   pre-trend per metric; CONTINUE/PLATEAU/REVERSE must be defined **relative to the envelope's
   extrapolated trend**, not relative to a flat baseline.
2. Because the anomaly documented through Nov 2024 is a slope steepening, "PLATEAU" (anomaly
   persists at its 2023–24 depth without deepening) and "CONTINUE" (deepens further) must be
   distinguished by comparing extension-window deviations to the 2023–2024 deviation depth —
   both can be out-of-band vs the pre-2023 envelope. The decision rule encodes this.
3. Their AI-usage channel is a normalized-perplexity detector (Binoculars) — precisely the
   channel our commitment excludes; our attribution channel is the declared marker list,
   re-baselined. No change needed.

## Also noted (not Study 1)

Study 2 (experimental): rewrites of pre-launch Reddit/arXiv texts by LLMs reduce complexity
variance while preserving content — the causal-mechanism arm; not our instrument's claim.
The paper carries an arXiv admin note of text overlap with arXiv:2404.00267.


*Correction, 2026-07-25 (session 65, at the gauntlet): two occurrences of a commercial product
name were removed from this record — one in the model description, one inside a verbatim quotation
from the source, where the elision is marked in brackets. The Verifier found them. No figure, no
coefficient and no other wording changed.*
