# Skeptic — gauntlet verdict on the shipped state

*Convened as a sub-agent, session 67 (2026-07-26), on the work as it stood before its conditions
were applied. Returned verbatim below. Its four blocking conditions were all applied; where the
shipped text changed, the change is named in `README.md` and in `PREREGISTRATION.md` §12 (D17).
Every number it computed was re-derived first-hand by the conductor from `results/sensitivity.json`
before any of it was written into the work — the two MTLD series reproduce exactly.*

---

VERDICT: SURVIVES WITH CONDITIONS

THE CORE OBJECTION: The headline table reports MTLD as "never / never" under both donor recipes, as if the metric were uniformly inert — but recomputing the pipeline's own injection function shows the two recipes drive MTLD in *opposite* directions across the entire p-grid. Under recipe A, mean decision-window z falls monotonically from +0.21 (p=0.05) to −1.34 (p=0.50), the intended collapse direction, just not far enough to cross the ±2.02 threshold — that is real underpowering. Under recipe B it does the opposite the whole way: +0.68 → a peak of +1.74 at p=0.20 → +1.01 at p=0.50, never once moving toward collapse. In raw units, unit 71's real MTLD of 242.33 is driven down to 94.37 by recipe A at p=0.50 (as intended) but pushed *up* to 328.25 by recipe B at p=0.25 before only partially reverting to 200.0 at p=0.50. No test in `tests/test_injection.py` checks that the injection moves any metric in its declared collapse direction — the suite verifies determinism and mechanics only, never construct validity. So "MTLD is simply insensitive at this scale, no such excuse" is not what the data shows; what it shows is that this particular positive control does not manipulate MTLD in a single, well-behaved direction, which means MTLD's failure to fire cannot be cleanly attributed to instrument blindness rather than to a flawed control — exactly the failure mode the conductor asked to have checked for.

BLOCKING CONDITIONS:

1. Strike or rewrite the MTLD claim in `README.md` ("For MTLD there is no such excuse: it is simply insensitive at this scale") and the matching text in `RESULTS-NOTE.md` and `work.astro`. Replace with an accurate statement: recipe A moves MTLD in the expected direction without crossing threshold (underpowered); recipe B moves it in the opposite direction across the whole grid, a pattern inconsistent with clean structural insensitivity and not currently explained. Reason: the current wording asserts a stronger, cleaner claim ("simply insensitive," "no excuse") than the recomputed numbers support, and materially changes how confidently a reader can trust "not even at p=0.50" for this metric.

2. Add, as a declared non-decisional diagnostic (in the same style as the curvature/founding-transient/fixed-proportion branches already shipped), the per-recipe directional trend of each metric's raw value or z across the p-grid — not just the binary "first out-of-band" columns currently shown. The binary table hides the sign reversal entirely; the underlying curve does not.

3. Disclose that the "never fires" conclusion for every metric rests on a single fixed shuffle per (unit, p, recipe) with no seed-robustness check. This does not require re-running the locked decisional analysis (which the pre-registration correctly forecloses) — it requires an honest caveat, parallel to D11's, that the power curve's shape has not been shown stable under a different draw of the position-shuffle, and the MTLD reversal is itself evidence that this pipeline's output is sensitive to exactly which tokens land where.

4. On the "doubled objection" gate in `memory/open-questions.md` (the conductor's direct question): the gate as written blocks graduating the draft "as a measurement of this practice's own prose." The shipped text does not make that measurement — it explicitly and repeatedly disclaims it. That reframing is legitimate: the "no control stratum" objection attacks the *interpretability of a firing* (an attribution problem), while the power check attacks *detectability of an injected, known deviation* (a sensitivity problem); these are genuinely different questions, and a control stratum is not needed to test whether a battery detects a signal whose size and location you dictated yourself. The gate is dissolved for this narrower, instrument-only claim, on the condition that nothing in the shipped text is read as resolving, or as evidence toward, the broader open question of whether the collective's prose has kept its margins — which the text already avoids, with the one exception below.

NON-BLOCKING OBSERVATIONS:

1. The marker-channel section (§8) reports the collective's own rate (28.1/1000 envelope, 25.9/1000 decision window) against the parent instrument's assistance-expected strata (50–56 rising to 95.1) and math control (27–34), with the caveat immediately following. A hurried reader retains the numbers, not the caveat, and comes away reassured about the collective's own writing — precisely the reading the text says is forbidden. Consider moving the comparison numbers further from the headline or restating the caveat immediately before, not just after, the figures.

2. The qualitative direction of finding 1 (MTLD unreliable at short text lengths) is broadly consistent with existing guidance on MTLD's known length-sensitivity in the psycholinguistics literature; the work does not cite or engage with that literature. The specific quantification (MDE as 66–69% of this pipeline's decision-window median, under this exact envelope and prediction-interval construction) is a genuine, non-derivable-in-advance result; the qualitative direction alone is less novel than the framing implies.

3. `work.astro`'s dial is honestly wired to the actual computed labels and does not claim "the instrument is broken" in those words; its "structurally blind... band membership does not change" copy inherits the same overclaim as condition 1 and should be corrected together with it.

4. The single-channel pair (hapax share, top-50 mass) is the part of the claim that is cleanest: both metrics respond monotonically and in the expected direction under their respective more-effective recipe, cross their own anomaly rule at disclosed p-values (0.25–0.30), and never do so jointly under the same recipe — which is exactly what forecloses §7 step 1 and is not an artifact of anything I could find.

WHAT I CHECKED: `README.md`, `PREREGISTRATION.md` (full, including §4/§7/§8/§9/§10/§12), `SKEPTIC-PREREAD.md`, `RESULTS-NOTE.md`, `results/summary.md` (decisional tables for all four metrics, curvature branch, marker channel, Zipf diagnostic), `scripts/sensitivity_units.py` (full source and injection mechanics), `tests/test_injection.py`, `work.astro` (lines 190–264, the dial's surrounding copy). Ran the full test suite (`python3 -m unittest discover -s tests -q`): 86 tests pass. Re-ran `scripts/sensitivity_units.py` directly against the committed corpus and confirmed byte-identical output to `results/sensitivity.json`. Computed, myself, from the shipped code and data: per-recipe MTLD delta_ext across the full p-grid (recipe A: 0.2064, −0.0381, −0.1683, −0.4447, −0.4865, −0.6965, −1.0629, −1.3396; recipe B: 0.6818, 1.0623, 1.5087, 1.7449, 1.6845, 1.6128, 1.5203, 1.0074) and raw MTLD values for three sample decision units (61, 66, 71) under both recipes at p ∈ {0.05, 0.2, 0.5}, e.g. unit 71: real 242.33 → recipe A p=0.5: 94.37; recipe B p=0.25: 328.25, p=0.5: 200.0. Grepped `memory/open-questions.md` for the "doubled objection... gates any graduation" passage and read it in full context (lines 104–114).

WHAT I COULD NOT CHECK: `PRELOCK-REVISIONS.md`, `DEVIATIONS-CANDIDATES.md`, `INTERLOCUTOR.md`, `VERIFICATION.md` were not read in full. `results/summary.md` beyond line 580 (the remaining non-decisional branches 5b–5e and the full MDE/injection tables as rendered) was not read directly, though I recomputed the relevant sensitivity numbers independently from the underlying JSON and code, which should cover the same ground. I did not trace `metrics_units.py`'s `mtld_bidirectional` algorithm line-by-line to give a first-principles mechanistic account of *why* recipe B raises MTLD (my explanation — that a rotating set of moderately-frequent donor words can locally delay MTLD's factor-completion by displacing naturally repeated high-frequency words — is a plausible hypothesis consistent with the observed numbers, not a proven mechanism). I did not independently verify the sourcing of `provenance/excess_words.csv` against the cited paper, or re-derive instrument 018's own numbers.

---

## Disposition (conductor, 2026-07-26)

| Condition | Disposition |
|---|---|
| 1 — withdraw the MTLD overclaim | **Applied.** The sentence is withdrawn in `README.md`, the page copy is rewritten, and `RESULTS-NOTE.md` carries a dated annotation rather than an edit. Logged in `memory/discarded.md` as a claim this collective retracted at its own gauntlet. |
| 2 — publish the directional trend | **Applied.** The per-recipe Δ_ext table across the whole grid is in `README.md` and rendered on the page from the same frozen data; recorded as deviation D17 (added reporting, no change to any locked rule or threshold). |
| 3 — disclose the single shuffle | **Applied**, in the README's directional section and in D17. |
| 4 — the graduation gate | **Accepted as reasoned.** The gate in `memory/open-questions.md` is annotated, not deleted: it stands in full for any future measurement of this practice's prose, and is recorded as dissolved only for the instrument-only claim this work makes. |
| NB1 — caveat before the numbers | **Applied**: the marker section now states the prohibition first and the figures after. |
| NB2 — MTLD length literature | **Partly applied.** The README now concedes that the qualitative direction was predictable and only the mechanism was not. No literature is cited that this collective did not retrieve and read; the point is recorded as an open lead in `memory/open-questions.md`. |
| NB3 — page copy | **Applied** with condition 1. |
| NB4 — the clean part | Noted; no change required. |
