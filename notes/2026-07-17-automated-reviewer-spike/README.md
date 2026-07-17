# Falsification spike — "the Automated Reviewer's yardstick"

**Session 42, 2026-07-17. Conductor's-hand verify-before-build probe. Nothing here is shipped
or gauntleted.** This directory records the feasibility gate that the Proposer and the Skeptic
(session 42) both demanded before any instrument is framed around Frank's 2026-07-17 seed.

## The object under examination

Yamada, Lange, Cong Lu, Chris Lu, Hu, Foerster, Ha, Clune, *Towards End-to-End Automation of AI
Research*, **Nature 651, 914–919 (2026)**; preprint **arXiv:2606.15497**. One component, the
"Automated Reviewer" (an ensemble of five reviews plus an Area-Chair meta-review, reading the
paper text), reports (verbatim from the preprint):

> "The Automated Reviewer achieves a comparable balanced accuracy with humans (69% versus 66%)
> and a higher F1-score compared to inter-human group agreement (0.62 versus 0.49) in the
> NeurIPS 2021 consistency experiment (Beygelzimer et al., 2021) ... These results suggest that
> LLM-based agents can provide valuable feedback that aligns with the average human expert
> opinion."

- The **0.69** balanced accuracy is measured against **ICLR accept/reject decisions** (the
  public OpenReview dataset, González-Márquez & Kobak 2024).
- The **0.66 / 0.49** "human" figures are the **NeurIPS-2021 inter-COMMITTEE consistency**
  (panel-vs-panel agreement) — a different venue and a different quantity from "accuracy against
  a fixed label."

## The spike

How much of the ICLR accept/reject label is recoverable by a **trivial one-parameter predictor**
— a threshold on the **mean human review score** — on the *same public data source* the paper
cites? Result (`run_spike.py`, deterministic; full output in `RESULTS.txt`):

| predictor | input | balanced accuracy vs ICLR accept/reject (2017–2024, n=19,685) |
|---|---|---|
| constant / majority class | — | **0.500** (by construction: BA = mean of per-class recall) |
| **mean-score threshold (≥ ~5.7)** | mean human review score | **0.880** |
| the paper's Automated Reviewer | paper text | **0.690** (as reported) |
| human committee vs human committee | NeurIPS-2021 consistency | **0.660** (as reported) |

Per-year balanced accuracy for the threshold is stable at **0.87–0.91** across 2017–2024;
sensitivity (counting Withdrawn + Invite-to-Workshop as reject) gives 0.895. The constant-predictor
row confirms the Proposer's correction: majority class scores 0.50, not high — the naive contender
is the score threshold, **not** majority class.

## What this does and does NOT show (load-bearing — carry onto any built work)

1. **INPUT ASYMMETRY (the decisive caveat).** The threshold baseline uses the mean human review
   score — information the paper's from-text reviewer does **not** receive. So this is **not**
   "a trivial reviewer beats the LLM reviewer." What it shows is that the **ICLR accept/reject
   label is ~88% recoverable from one number (the mean score)** — i.e. the decision is, to first
   order, a threshold on the scores. Therefore "balanced accuracy against the decision" rewards
   recovering that threshold, and the paper's tool, reading only text, recovers it at 0.69 —
   *below* the 0.88 the scores themselves give, and at the level of the inter-committee **noise
   floor** (0.66) the paper adopts as its human comparator. The sharp, defensible reading is not
   "trivial beats sophisticated" but: **the benchmark is largely a score-recovery task, and the
   tool is declared "human-level" by comparison to the noise floor rather than to the signal.**
2. **NOT A STRICT REPLICATION.** The paper's exact ICLR subset/split for its 0.69 is in
   Supplementary A.3.2 (not retrieved — Nature paywalled, arXiv HTML mirror 404 at probe time).
   This is a same-corpus stress test on the same public source, not a re-run of the pipeline.
   Any built work must state this, and must frame the paper's elision as "the headline comparison
   as stated does not surface X," not "the paper hides X."
3. **NOVELTY.** The *thesis* "human accept/reject is a noisy ground truth for an LLM reviewer" is
   already published and peer-reviewed (arXiv:2605.03202, ICML 2026 Oral; 2606.25057; 2512.22145)
   and must be cited as prior art up front. The additive contribution, if any, is the **computed
   three-row yardstick above** placing 0.88 (score→decision) beside 0.69 (tool→decision) and 0.66
   (committee→committee) on one axis — showing where the tool sits relative to both the signal and
   the noise floor. Whether that specific juxtaposition is genuinely non-redundant is a gauntlet
   question for the build session.
4. **HYGIENE.** Refer to the object only as "the Automated Reviewer (arXiv:2606.15497 / Nature
   651, 914–919)"; never the product or company name. Critique stays on method/numbers.

## Gate verdict

**PASSED.** A real, reproducible, large, stable computation exists on real public data — not an
essay. The candidate instrument is therefore **workboarded as a proposed build** (working title
provisional — e.g. "The Noise Floor" / "The Naive Reviewer"), gated by the four conditions above
plus the two role sets of conditions recorded in `journal/2026-07-17.md`. **Not built, not shipped
this session.**

## Sources (all retrievable)

- Paper: https://arxiv.org/abs/2606.15497 · https://www.nature.com/articles/s41586-026-10265-5
- Dataset: https://github.com/berenslab/iclr-dataset (`data/iclr24v2.parquet`,
  sha256 `f486c7a0f58c71005ab8f86e6128038ca523a9efe7feb4ab353b37f789d47fb0`); described in
  https://arxiv.org/abs/2404.08403
- NeurIPS-2021 consistency experiment: https://arxiv.org/abs/2306.03262
- Prior art on the noisy-oracle thesis: https://arxiv.org/abs/2605.03202
