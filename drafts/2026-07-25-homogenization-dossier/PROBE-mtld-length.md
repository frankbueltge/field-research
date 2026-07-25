# Probe pre-registration — is the MTLD rise a length artifact?

**Written and committed BEFORE any probe fetch** (same house discipline as the main
pre-registration: the rule is fixed before the data arrives). Session 65, 2026-07-25, conductor's
hand. This is a **gauntlet-docket diagnostic**, explicitly **non-decisional**: it cannot change the
locked instrument's verdict, which already fired the kill condition, and MTLD's observed movement
is in the anti-collapse direction, outside the pre-registered one-sided decision space either way.
The probe governs **how one observation is reported** — nothing else.

## The question

The first run reported per-abstract MTLD far **above** the pre-2023 ordinary-drift envelope in the
anti-collapse direction: cs.CL Δ_ext ≈ +11.7σ, raw series 95.6 (2022H2) → **152.5** (2026H1),
≈ +59.5 %. Before that is reported as anything but a raw number, one instrument artifact has to be
ruled in or out:

**MTLD as this instrument computes it is a per-abstract statistic** (`scripts/metrics.py`:
bidirectional MTLD per drawn abstract, averaged over the 150 seeded-drawn abstracts of the cell;
an abstract whose token stream never completes a factor in either direction returns `None` and is
**excluded from the mean**). Two length-mediated failure paths follow:

1. **Length growth.** If abstracts simply got longer, per-abstract MTLD can rise mechanically —
   MTLD is length-robust by design, but its robustness is weakest in the short-text range where
   academic abstracts sit.
2. **Computability selection.** If the share of drawn abstracts returning `None` fell over time,
   the mean is taken over a shifting subset — a selection effect, not a diversity change.

## Design (fixed before the fetch)

- **Stratum:** cs.CL only — the headline stratum and the largest reported deviation.
- **Units (4):** `2016H1`, `2019H1`, `2022H2`, `2026H1` — two envelope-era units, the pre-launch
  boundary unit, and the extension-window end.
- **Route, filter, tokenizer and seeded draw:** the locked instrument's own scripts, unchanged
  (`harvest_api.py` → `filter_corpus_api.py` → `metrics.seeded_order`), so the probe reads the
  **same 150 abstracts per unit** the shipped MTLD number was computed on, up to any records the
  archive has added or revised since 2026-07-25 05:13Z (disclosed as a re-fetch difference, and
  measured: the probe reports its own `kept` counts against `provenance/counts.json`).
- **Quantities per unit:**
  - `n_kept` (filter output) and the re-fetch difference against the frozen run;
  - mean and median token length of the 150 drawn abstracts;
  - `undefined_share` — fraction of drawn abstracts whose bidirectional MTLD is `None`;
  - `mtld_shipped_recomputed` — MTLD by the shipped definition (sanity check against
    `results/results.json`);
  - **`mtld_trunc120`** — the same mean per-abstract bidirectional MTLD computed on abstracts
    **truncated to their first 120 tokens**, restricted to drawn abstracts with **≥ 120 tokens**
    (n reported per unit). Fixed length, fixed draw, same tokenizer: the length channel is closed.

## Decision rule (fixed before the fetch)

Reference quantity: the shipped raw rise **2022H2 → 2026H1 = +56.9 MTLD units**.

Let `R_trunc` = `mtld_trunc120(2026H1) − mtld_trunc120(2022H2)`.

- `R_trunc ≥ 28.5` (≥ half the shipped rise) → **NOT A LENGTH ARTIFACT.** The rise survives at
  fixed length; report the observation as a measured, length-controlled rise, still non-decisional.
- `R_trunc ≤ 14.2` (≤ a quarter) → **SUBSTANTIALLY A LENGTH ARTIFACT.** Report the raw rise only
  with that finding attached, and withdraw any suggestion of a diversity increase.
- Between → **PARTIAL / INCONCLUSIVE.** Report both numbers and claim nothing about mechanism.

Independently of `R_trunc`: if `undefined_share` falls by more than 10 percentage points from
2022H2 to 2026H1, the computability-selection path is reported as live regardless of the truncated
result.

**Failure is a legitimate outcome.** If the probe cannot be run (route, wall clock, or a re-fetch
difference large enough to break comparability), the dossier ships saying exactly that, and the
observation ships unprobed with the artifact hypotheses named. No third attempt, no threshold
adjustment.

## Bounds

Free route, no new external cost; public/aggregate text only; raw chunks ephemeral by the same §2
rule as the main run — only the probe's aggregate outputs and the sha256 manifest are committed.
