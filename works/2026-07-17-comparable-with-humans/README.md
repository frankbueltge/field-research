# "Comparable With Humans" — instrument draft (session 43, 2026-07-17)

An instrument on the *comparator* a 2026 end-to-end AI-research-automation paper
chose when it declared its "Automated Reviewer" human-level. That reviewer (five
machine reviews + a machine Area-Chair meta-review, reading only the paper text)
is reported at **balanced accuracy 0.69 ± 0.04** against real ICLR accept/reject
decisions, and called "comparable with humans (69% versus 66%)". The work
separates the two numbers the claim treats as comparable despite their being
different quantities:

- **0.69** — accuracy against a *fixed ICLR decision* (the paper's tool).
- **0.66** — the paper's *human bar*, which is the **NeurIPS-2021 inter-committee
  consistency** (how often two independent committees agree) — a different venue
  and a different quantity, not accuracy against a fixed label.

On the decision-recovery axis (the one the paper reports on), the reader drags a
single threshold on the **mean human review score** and watches balanced accuracy
against the real decision climb to **≈0.88** on all 19,685 clearly-decided scored
papers. The 0.66 human bar is held on a **separate panel**, deliberately off that
axis, so the instrument does not itself commit the incommensurability it examines.

## The object under examination

Yamada, Lange, Cong Lu, Chris Lu, Hu, Foerster, Ha, Clune, *Towards End-to-End
Automation of AI Research*, **Nature 651, 914–919 (2026)**; preprint
**arXiv:2606.15497**. All object figures verified verbatim against the preprint's
**Table 1** (this session, first-hand, two independent routes):

| Row (Table 1) | Balanced Acc. | F1 |
|---|---|---|
| Human (NeurIPS 2021) | 0.66 | 0.49 |
| Random Decision (2017–2024) | 0.50 | 0.47 |
| Always Reject (2017–2024) | 0.50 | 0.00 |
| **Automated Reviewer (2017–2024, n=1,000)** | **0.69 ± 0.04** | 0.62 ± 0.09 |
| Automated Reviewer (2025 clean set) | 0.66 ± 0.03 | 0.67 ± 0.09 |

(All values from Table 1 of arXiv:2606.15497, transcribed verbatim: the row order
is Balanced Acc. · Accuracy · F1 · AUC · FPR · FNR; only Balanced Acc. and F1 are
shown here. The Human/Random/Always-Reject rows carry no margins in the table; the
Automated-Reviewer rows do — the Table 1 caption states the "error margins denote
the 95% bootstrapped confidence intervals.")

Note the two coincidental 0.66's: the Human(NeurIPS) row **and** the tool's 2025
row. The quote's "69% versus 66%" is tool-2017–2024 (0.69) vs Human-NeurIPS
(0.66) — fixed by the parallel F1 clause "0.62 versus 0.49", where 0.49 is the
Human(NeurIPS) F1. Object referred to only as "the Automated Reviewer
(arXiv:2606.15497 / Nature 651, 914–919)" — never the product or company name.

## Data (real, pinned, retrievable — not committed here)

- `berenslab/iclr-dataset`, `data/iclr24v2.parquet`,
  sha256 `f486c7a0f58c71005ab8f86e6128038ca523a9efe7feb4ab353b37f789d47fb0`
  (24,445 ICLR submissions 2017–2024). Source:
  https://github.com/berenslab/iclr-dataset ; described in arXiv:2404.08403 .
- Committed here: the derived compact histogram `data.json` (score-bin →
  accept/reject counts) + the scripts that produce it. The parquet itself is
  fetched and hash-checked at derivation time, not committed.

## Reproduce

```
pip install pandas pyarrow numpy
curl -sSL -o iclr24v2.parquet \
  https://raw.githubusercontent.com/berenslab/iclr-dataset/main/data/iclr24v2.parquet
sha256sum iclr24v2.parquet   # must equal f486c7a0…d47fb0
python3 run_spike.py    iclr24v2.parquet          # exact continuous computation
python3 derive_hist.py  iclr24v2.parquet data.json # the histogram the work renders
```

- `run_spike.py` (verbatim session-42 falsification spike): **BA 0.8795 at
  mean ≥ 5.69**, n=19,685; per-year 0.869–0.909; constant/majority 0.500.
- `derive_hist.py`: bins the mean score at width 0.25 and reconstructs balanced
  accuracy from the histogram — the **identical computation the client slider
  runs** → peak **0.879** (the gap to 0.8795 is binning granularity, disclosed
  on the work).

## Label rule

Accept iff `decision` starts with "accept" (case-insensitive); reject iff
`decision` ∈ {Reject, Desk rejected}; Withdrawn / Invite-to-Workshop excluded.
Predictor = mean of the integer review scores. Balanced accuracy =
½(recall_accept + recall_reject); constant predictor 0.500 — matching the paper's
own Random / Always-Reject rows.

## Load-bearing caveats (carried onto the work itself)

1. **Input asymmetry.** The threshold reads the mean *human review score*; the
   from-text tool does not. So 0.88 is not a target the tool could reach — it is
   the ceiling of how far the *decision* is a score threshold. NOT "trivial beats
   sophisticated."
2. **Not a matched-subset replication.** The tool's 0.69 is on **n=1,000**
   (2017–2024; sampling method unstated); the instrument's 0.88 is on all
   **n=19,685** of the same years. The *magnitude* of the gap is not established
   against a matched subset — only that the comparison *as stated* omits the
   score axis and treats two different quantities as comparable. Never "the
   paper hides X."
3. **Prior art up front.** Human-committee disagreement on ~half of accepted
   papers: Beygelzimer et al. (arXiv:2306.03262). Automated reviewers are
   gameable / show a hivemind effect and must be rigorously evaluated before
   deployment: Baumann et al., *Stop Automating Peer Review Without Rigorous
   Evaluation* (arXiv:2605.03202, ICML 2026 Oral) — a distinct point from the
   human-noise one; cited accurately. Additive move = only the computed
   reframing (the omitted 0.88 axis + the 0.66 incommensurability), operable by
   hand.

## Gauntlet history (this session)

- Round 1: Verifier **FAIL** (2 blocking: the tool's 0.69 is on n=1,000, openly
  stated — not "paywalled/unretrieved"; arXiv:2605.03202 mischaracterised as
  human-noise prior art) + 1 minor (add ±0.04). Skeptic **SURVIVES-WITH-
  CONDITIONS** (the single meter over-claims commensurability; add persistent
  input-asymmetry note; reword "signal/noise floor"; disclose n=1,000 vs 19,685;
  visual differentiator for 0.66). Interlocutor: the meter reproduces, in pixels,
  the category error it indicts — split the axis (constructive edge adopted).
- Reworked: retitled ("The Noise Floor" → "Comparable With Humans"); two-zone
  structure (decision-recovery axis vs the human bar held apart); all figures
  re-verified verbatim against Table 1; n=1,000 disclosed; 2605.03202 corrected;
  ±0.04 added; default slider set below the peak.
- Round 2 (on the reworked state): recorded in `journal/2026-07-17.md`.

Not in `works/` until the round-2 gauntlet passes on the exact shipped state.
