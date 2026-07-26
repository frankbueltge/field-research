# First-run results note — session 63, 2026-07-25 (conductor's hand)

**Status: measurement run COMPLETE under the locked pre-registration (`5e17bf1`) + deviations
D1/D1a. NOT gauntleted, NOT shipped — the full gauntlet (independent Verifier, fresh Skeptic,
Interlocutor) is OWED before any of this graduates or travels.** This note is the plain
record of what the instrument returned, for the gauntlet session.

## Harvest (route per §10 D1/D1a)

- 2026-07-25 ~05:13Z–05:13Z window recorded in `provenance/harvest-log.json`; 338,151
  records fetched across 69 stratum×unit queries (courtesy pacing 1 req/3 s throughout).
- **Tally note (disclosed):** 5 of 69 queries under-delivered 1–2 records vs their own
  advertised `totalResults` (cs.CL 2026H1 −2; cs.CV 2021H1 −1, 2021H2 −2, 2023H1 −1,
  2026H1 −1; 6 records of 338k, ≤0.02% of any affected cell) — a known pagination artifact
  of the route; non-recoverable at the route; direction-neutral.
- Filtered corpus (primary category, dated 2015-01-01…2026-06-30, ≥50 tokens):
  **cs.CL 82,401 · cs.CV 150,822 · math.NT 19,753** abstracts. No cell below the 150 fixed
  draw — zero small-cell fallbacks fired. math.NT's short-abstract exclusion rate is high
  (~25–30% in some cells; short theorem-statement abstracts) — a disclosed corpus property.
- §2 contamination ceiling (share of pre-2023 records whose latest version date is
  ≥2023-01-01): cs.CL 5.25%, cs.CV 5.75%, math.NT 10.73%.
- sha256 manifests of all raw chunks and corpus files: `provenance/manifest.json`. Raw
  chunks and corpus JSONL are ephemeral (out of git per §2); the manifests freeze what this
  run measured.

## The verdict the instrument returned

**Both decision strata: NO SIGNAL BEYOND ORDINARY DRIFT — the §7 kill condition fires.**
All four margin metrics in cs.CL, cs.CV (and math.NT) label **NO-ANOMALY**: not one
collapse-direction out-of-band unit anywhere, in either the reference window (2023H1–2024H2)
or the extension window (2025H1–2026H1). Linear and quadratic envelopes agree
(`soft_downgrade_unresolved` = False everywhere). Control: math.NT marker channel clean →
control VALID, and clear. Full tables: `results/summary.md`, `results/results.json`.

Per the Local Commitment's own kill terms: this ships (after the gauntlet) **as a negative
result with the same weight — no threshold adjustment, no re-run; the inquiry closes on the
answer it gets.**

## The two observations beside the verdict (context, not pre-registered findings)

1. **The marker channel lights up exactly where adoption is expected, and only there.**
   Pool marker rate (per 1,000 tokens), 2015–2022 baseline ≈50–56 in cs.CL/cs.CV:
   cs.CL 64.9 → 74.1 → 89.6 → **95.1** (2024H2 peak, ≈1.8× baseline) → 86.6 → 87.0 → 71.5;
   cs.CV similar shape (peak 88.4); **math.NT flat 27–34 throughout** (validating the
   control and giving the adoption contrast). The §8 A_ref/A_ext excess-anomaly flags are
   True for cs.CL/cs.CV, False for math.NT. This is the pre-registered mixed-signal
   reading: **the corpus visibly carries the fingerprint of model-assisted writing, and the
   margins did not shrink** — replicating the published news-corpus dissociation (Fitterer
   et al., ACL 2025 SRW) on a much larger academic corpus.
2. **MTLD rose far ABOVE the pre-2023 envelope** (anti-collapse direction; outside the
   one-sided pre-registered decision space, reported as observation): Δ_ext ≈ +11.7σ
   (cs.CL), +18.0σ (cs.CV), +3.1σ (math.NT); raw series cs.CL 95.6 (2022H2) → 152.5
   (2026H1), ≈+60%. Per-abstract lexical diversity **climbed steeply** post-launch —
   opposite in sign to margin collapse at the per-document level. (Consistent with the
   published finding that MTLD rose in an LLM-era news corpus while other diversity metrics
   were flat.) The gauntlet should probe this for instrument artifacts (abstract length
   growth interacting with MTLD; composition shift) before it is asserted as a finding —
   note the smaller but same-direction rise in the low-adoption control (+3.1σ), which is
   itself diagnostic material for the composition-vs-assistance question.
3. Unforeseen, worth one line: the marker rate **declines from its 2024H2 peak through
   2026H1** (95→71 in cs.CL) while MTLD keeps climbing — marker-vocabulary fashion may be
   fading independently of assistance levels. Not a pre-registered quantity; logged for the
   gauntlet.

## Relation to the published series (qualitative, per B3)

No contradiction with Sourati et al.: their documented quantity is the **variance of
complexity features across documents** (dispersion), declining through Nov 2024; our margin
metrics are level- and pool-based (per the commitment, deliberately our own battery). On our
metrics, their era (the reference window) already shows no out-of-band collapse — so the
extension verdict is "no signal to extend," not "their decline reversed." The Dossier must
state this scope boundary prominently.

## What the gauntlet must judge (minimum docket)

- Deviations D1/D1a (route + pagination) — do they survive?
- The 6-record tally shortfall and the 2026H1 truncation question (2026H1 is complete by
  the §2 window definition — Jan–Jun 2026 — but harvested 2026-07-25; late submissions
  cross-listed later could shift counts marginally on re-harvest; manifests freeze this run).
- MTLD anti-collapse observation: artifact probes (length growth, composition).
- Verifier: independent recomputation from the manifests/scripts; spot re-fetch.

---

## Corrections, 2026-07-25 (session 65, at the gauntlet)

Dated corrections to this first-run note, in place of silent edits — the note's original wording
above is left standing so the record shows what was written and when.

1. **"not one collapse-direction out-of-band unit anywhere" (the verdict section) is FALSE.**
   Five margin-metric units fall out of band in the collapse direction across the run: cs.CL
   hapax share at 2024H2 (z = −2.61), cs.CL between-abstract similarity at 2025H1 (z = −2.59),
   math.NT similarity at 2017H1 (−2.21) and 2025H2 (−2.30), math.NT Zipf slope at 2025H2 (−2.71).
   Each is isolated, so the pre-registered two-consecutive-unit requirement makes every metric
   NO-ANOMALY — the verdict is unchanged, but the sentence as written overstated it. See the
   README, "What this null can and cannot exclude".
2. **math.NT MTLD Δ_ext is +3.0σ, not +3.1σ** (`results.json`: 2.9661). The Verifier found it;
   it appears twice in the observation section above and once in the README, corrected in both.
