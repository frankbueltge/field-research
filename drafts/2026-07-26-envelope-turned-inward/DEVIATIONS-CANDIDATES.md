# Deviation candidates — Builder, stage 1 (extraction, pools, per-unit metrics)

Per PREREGISTRATION.md §12: everything below is an interpretation, specification, or
implementation choice required to execute the locked text, not an edit to it. The
conductor transcribes accepted items into §12; this file is not that log.

## 1. Excluded `journal/2026-07-26.md` at the file level (corpus definition)

§2's "Source" line reads: "every file matching `journal/*.md` in this repository at the
lock commit of this document." Taken fully literally, that includes
`journal/2026-07-26.md`, which already existed at the lock commit `ec6b0c5` (added by the
prior same-session commit `2576119`, "journal opened") and carries one top-level heading,
`# Session 66 — 2026-07-26` — this session's own opening record.

§5 states, unconditionally: *"This run's own output is not in the corpus. The journal
entry this session writes becomes unit 74 in any later run; the corpus is frozen at this
document's lock commit, so the probe cannot measure the session that built it."* That
sentence is only satisfiable by excluding `2026-07-26.md` itself — session 66 is the
session that produced this pre-registration and ran this extraction, so its own journal
file is "this run's own output" regardless of which commit it happens to already be
sitting in.

**Resolution:** `2026-07-26.md` is excluded by filename (`extract_units.EXCLUDED_FILES`),
unconditionally, not by any property of its content. This is the only reading consistent
with: (a) §2's pretest count "N = 73"; (b) §2's "23 calendar dates" (24 dated files exist;
excluding one gives 23); (c) `provenance/feasibility-pretest.md`'s enumerated table, which
ends at unit 73 = 2026-07-25 and does not include 2026-07-26 at all. Without this
exclusion, extraction yields N = 74, contradicting the pretest and failing the required
`assert N == 73`.

**Direction of effect:** removes exactly 1 unit (the session-66 opening, 1 heading, part
of this run's own output) that a fully literal glob would have included as unit 74. No
other file or unit is affected.

## 2. Definition of "the envelope-era pool" (§9, undefined in the locked text)

§9's synthetic-injection recipes need donor types from "the envelope-era pool," and §3(d)'s
content-word-only companion series needs "the 200 most frequent types of the envelope-era
pool" — neither §2 nor §3 defines this pool's construction. Fixed here, per the task's
explicit instruction to record this definition:

> The concatenation, in unit-index order, of the 600-token prefixes of every **computable**
> unit in the envelope window (units 1-47; a unit is computable iff n_tokens >= 600).

This mirrors §3's own fixed-prefix principle (each unit contributes its decisional
600-token slice, not its whole text) and uses only envelope-window, computable material —
consistent with the envelope being fit only on computable envelope units (§4). Implemented
in `scripts/pools.py`; the resulting table (26,400 tokens from the 44 computable envelope
units, 4,432 types) is written to `provenance/envelope-pool.json` for independent
verification.

**Direction of effect:** this choice is downstream-consequential (it fixes the exact
donor/stopword vocabulary for stage 2's injection recipes and this stage's
`sim_content`), but is the mechanically-defined, hand-picking-free construction the locked
text calls for ("a mechanically defined set — no hand-picked word list," §3(d)). A
different but equally defensible construction (e.g., whole-unit tokens rather than
600-token prefixes) would shift the exact rank table without changing its qualitative
character.

## 3. `whole_unit.computable` criterion (unspecified)

The task's field list requires `whole_unit` to carry the same keys as `prefix600`,
including `computable`, but neither PREREGISTRATION.md nor the task states a floor for it
(unlike prefix600's `n_tokens >= 600` and prop40's `length >= 100`). Since `whole_unit` is
explicitly context-only and never enveloped (§3), and this corpus's minimum unit length is
349 tokens (unit 33) — comfortably enough for every metric function to return a defined
value, as verified in the actual output — `whole_unit.computable` is set unconditionally
`true`. **Direction of effect:** none observable in this corpus (no unit trips any
metric's internal degeneracy at whole-unit scale); flagged for the record because the
criterion was not given.

## 4. `top50_partial` — an added key beyond the literal key list

§3 states: "If the pool has fewer than 50 types, use all types and flag" — but the task's
"EXACTLY these key names" list for prefix600/whole_unit/prop40 does not include a name for
this flag. `top50_partial` (bool) was added to each metric block to carry it, which means
each block has one key beyond the literal list. Verified programmatically before adding
it: **no unit's pool (prefix600, whole_unit, or prop40, all 73 units) has fewer than 50
types in this corpus**, so the flag is `false` everywhere in `results/metrics.json` today
— inert as a matter of corpus fact, not because the mechanism is missing. **Direction of
effect:** additive only; zero effect on any numeric value in this run.

## 5. Unit-boundary split computed on raw, pre-exclusion lines

§2 defines a unit as "the text from a line beginning `# ` ... up to the next such line or
end of file," stated before the six line-level exclusion rules are given, which read "line
by line **inside a unit**." Read in that order, unit boundaries are fixed on the raw file
first; exclusions are then applied within each already-delimited unit. This is how
`extract_units._split_into_raw_units` is implemented: it scans raw lines for `^# ` before
rule 1 (fenced-code removal) ever runs.

**Latent edge case, checked and found absent in this corpus:** if a fenced code block
contained a line matching `^# ` (e.g., a shell comment or Python comment quoted verbatim),
this ordering would misidentify it as a unit boundary. Checked mechanically across all 23
included journal files: zero `^# ` lines occur inside a ` ``` ` fence anywhere in the
corpus. N = 73 is therefore unaffected, but this is a structural fragility of the locked
ordering, not of the implementation, and is worth the gauntlet's attention if the corpus
ever grows.

## 6. Two distinct heading regexes, by design, not by drift

The unit-boundary regex (`^# `, level-1 only, no leading whitespace, per §2's "a line
beginning `# `") is deliberately stricter than exclusion rule 4's in-unit heading-drop
regex (`^\s*#`, any level, any indentation, per §2's literal rule text). A `##` subheading
inside a unit is dropped as prose noise by rule 4 but never starts a new unit. This is a
direct implementation of two different sentences in the same locked paragraph, not an
inconsistency; recorded so a verifier does not mistake one regex for a typo of the other.

## 7. `window_similarity`'s idf denominator generalized to the actual window size

§3 metric 4 states idf = ln(5/df) for the 5-document trailing window. §3's disjoint-block
companion series is defined over 5-unit blocks, but 73 is not divisible by 5, so the last
block (units 71-73) has only 3 documents. `scripts/metrics_units.window_similarity`
therefore uses `idf = ln(n_window/df)` with `n_window` = the actual number of documents in
whatever window or block it is given (5 for every trailing window and every full block; 3
for the one short block) — the literal `ln(5/df)` would be undefined or wrong wherever
`df` could exceed a hardcoded 5 that isn't the true document count. This is the same
formula §3 states, generalized to the block realization §3(e) itself requires; no
alternative reading was available. **Direction of effect:** only unit indices 71-73's
`sim_block` are affected by the generalization (`n_window = 3` there); every other block
and every trailing window has `n_window = 5`, identical to a literal reading.

## No defects found in the Builder's own code after review

Cross-checked prefix600 metrics on units 5, 44 and 70 against the values recorded in the
pre-lock estimator diagnostic (`provenance/prelock-estimator-diagnostic.md`, computed by a
throwaway script before this extractor existed): types, zipf slope, MTLD, hapax share and
top-50 mass agree exactly on all three units. `sim_trailing` / `sim_block` computable
counts were independently re-derived by hand from the three sub-600-token unit indices
(29, 33, 40) and matched the code's output exactly (55 and 58 respectively) before this
file was written.

## No defect found in the spec beyond what is resolved above

Item 1 (the file-glob vs. "this run's own output" tension) is the one place the locked
text is not self-consistent on its face; §5's explicit sentence resolves it unambiguously,
so it is recorded here as an interpretation rather than reported as an open defect.

---

# Deviation candidates — Builder, stage 2 (envelope, classification, verdict, sensitivity)

Everything below is an interpretation, specification, or implementation choice required
to execute PREREGISTRATION.md §4-§9 against stage 1's frozen `results/metrics.json`, not
an edit to the locked text. Stage 1's items above are unchanged.

## 8. Prop40 branch (§3 sensitivity companion) has only 3 metrics, not 4

§3's fixed-proportion companion series is described as "each metric ... computed through
the identical envelope machinery," and the task lists "the prop40 fixed-proportion series
(§3)" as one of five non-decisional branches to run through the identical machinery.
`results/metrics.json`'s `prop40` block (stage 1's frozen output) carries `mtld`,
`hapax_share`, `top50_mass`, `zipf_slope` and `marker_rate_per_1000` — but **no
`prop40`-scale similarity series**: metric 4 is a between-unit window construction over
each unit's 600-token *prefix600*, and stage 1 never computed an analogous window over
each unit's first-40%-of-tokens slice. Since this stage may not regenerate
`results/metrics.json` (frozen input, hard rule), the prop40 branch here runs the §7
machinery over the 3 metrics that do exist (`mtld`, `hapax_share`, `top50_mass`) and is
explicitly noted as a 3-metric roster in `results/envelope.json`
(`branches.prop40_fixed_proportion.note`).

**Direction of effect:** the §7 thresholds (>=2 of ext-decidable for step 1, <=1 for the
step-2 kill condition) are applied unchanged to a 3-metric denominator instead of 4, which
is a *smaller* base to reach ">=2 of N" against — mechanically slightly easier to fire on
this branch than the 4-metric decisional roster, in proportion terms, though this branch
is declared non-decisional and never overrides the decisional verdict either way. No
alternative construction was available without regenerating frozen stage-1 output, which
is prohibited.

## 9. Sim_block anomaly rule operationalized at BLOCK granularity, not the naive per-unit rule

§3(e)'s disjoint-block companion series exists specifically to "restore the
independent-observation logic the two-consecutive rule assumes." But `metrics.json`
stores `sim_block` as one value **per unit**, with every unit inside the same 5-unit block
carrying its block's identical value (and therefore identical `out_of_band` status once
enveloped). Applying §4's literal "two consecutive computable units out-of-band" rule at
unit granularity to this series would make ANY single out-of-band block trivially satisfy
the anomaly condition (any two of its <=5 constituent units are "two consecutive
out-of-band units") — which tests nothing beyond "one block fired," defeating the
independent-two-observations purpose §3(e) states for building this series in the first
place.

**Resolution, implemented in `scripts/envelope_units.py`'s `anomaly_two_consecutive_blocks`:**
rows in the window are collapsed to one representative row per distinct block touched
(first occurrence, since all units in a block share one value), and the rule becomes "two
ADJACENT blocks (by block index, no gap), both out-of-band" — the genuine block-level
analogue of the unit-level rule.

**Direction of effect:** substantially HARDER to fire than the naive (vacuous) per-unit
reading would have been — consistent with this task's instruction to resolve ambiguity in
the direction that makes a positive finding harder. Non-decisional branch only; never
affects the decisional verdict.

## 10. Sim_content branch keeps the five-apart anomaly exception

§4's Skeptic-condition-1 exception ("metric 4's two out-of-band units must be >= 5 apart")
is stated for metric 4 / `similarity` specifically, in the context of the decisional
trailing-window series. The sim_content companion series (§3(d)) uses the IDENTICAL
trailing-window construction (same `window_indices`, same document-sharing-by-construction
property) with only the token content filtered — so the same serial-correlation rationale
applies verbatim. `sim_content` is therefore evaluated under the five-apart rule, not the
plain two-consecutive rule, in `results/envelope.json`'s `branches.sim_content_companion`.

**Direction of effect:** harder to fire than a bare two-consecutive default would have
been for this branch; consistent with the same window-overlap logic §4 already applies to
the decisional similarity metric, and with the instruction to resolve ambiguity toward
harder-to-fire where the locked text does not explicitly say.

## 11. Injection mechanics: donor-cycle phase and its interaction with within-window idf

§9.2 leaves two things unstated, both now fixed and documented in
`scripts/sensitivity_units.py`'s module docstring: (a) `n_replace = round(p * 600)` — moot
here since every grid `p` gives an exact integer (30, 60, ..., 300), verified by
`tests/test_injection.py`; (b) the donor list for a recipe is shuffled ONCE with a
recipe-only seed (`20260726:donors:{recipe}`), and for every decision unit's injection the
donor cycle **restarts at the front of that same shuffled list** — chosen so a single
unit's injected prefix is a pure function of `(unit, p, recipe)` alone, independent of
whatever else is being injected in the same run (required for the determinism test, and
for the "envelope fit itself stays fitted on the real envelope-era data" independence the
task requires).

**Observed, disclosed consequence (not a bug, but worth stating plainly because it
explains a result in `results/sensitivity.json`):** because every decision unit under a
given `(p, recipe)` receives donor tokens in the SAME phase, and because several decision
units are simultaneously injected under one `(p, recipe)` combination, shared donor tokens
tend to land with near-identical relative frequency across multiple documents inside a
similarity window. §3(a)'s idf construction (`idf = ln(n_window/df)`) zeroes any token
present in ALL documents of its window — so once several members of a similarity window
are co-injected decision units, part of the injected homogenization signal can be
idf-zeroed away by the very metric the injection is meant to move. In this run, `similarity`
is reported "structurally blind to this injection" at every grid `p` under both recipes
(`results/sensitivity.json.structurally_blind_metrics`); this donor-phasing interaction is
one contributor to that result, alongside the metric's already-larger prediction-interval
margin. **Direction of effect:** makes the measured power against `similarity` more
conservative (harder to detect) than a design that varied donor phase per unit would have
been — again on the side the task instructs ambiguity to be resolved toward, but flagged
here because "structurally blind" could otherwise be misread as a property of the corpus
rather than partly an artifact of this implementation choice.

## 12. Degenerate-fit guard in `build_rows` (z_raw defined as 0.0 when se == 0)

PREREGISTRATION.md §4's formula `z = (y - yhat) / SE_pred` is undefined (0/0) for an
exactly-collinear fit (`s = 0`, hence `SE_pred = 0` at every `x`). This never occurs on
the real corpus (real residuals are never exactly zero), but the task requires a unit test
asserting "a perfectly linear series must give z = 0 at every envelope point," which needs
this case to be well-defined rather than raising `ZeroDivisionError`. `build_rows` in
`scripts/envelope_units.py` treats `se == 0` as `z_raw = 0.0` (the deviation is also
exactly 0 in every case this guard can be reached from). **Direction of effect:** none on
any output derived from real data (the guard is provably unreachable there, since it
requires `ss_res == 0` exactly across 44 or more real, independently-drafted units); exists
only to make `tests/test_envelope_arithmetic.py`'s required fixture well-defined.

## 13. Marker channel evaluated over the single combined window (48-73), not split ref/ext

The task's instruction for the marker channel (§8) states explicitly: "its own envelope
over units 1-47, raw (UNreoriented) z, excess-direction rule z > +t, over the **combined
window 48-73**." This is implemented as written — one anomaly boolean and one mean-z over
units 48-73 together — which differs from the parent instrument's own `marker_report`
(`works/2026-07-25-no-signal-to-extend/scripts/envelope.py`), which reports separate
`a_ref`/`a_ext`/`delta_ref`/`delta_ext` for its two windows. **Direction of effect:**
neutral — faithful to this task's explicit instruction, which is more specific than and
supersedes the parent's own convention for this adapted instrument.

## 14. "§7 step 1 fires" operationalized as reaching step 1 of the ordered procedure

§9.3's "the smallest p at which §7 step 1 fires (battery level)" is operationalized in
`scripts/sensitivity_units.py` as: the injected run's `evaluate_verdict(...)["step"] == 1`,
i.e. >=2 ext-decidable margin metrics show `A_ext` (including when that pair triggers the
SINGLE-CHANNEL downgrade, since SINGLE-CHANNEL is still reached via step 1's branch of the
ordered procedure — it is a modifier of step 1's headline, not a different step).
**Direction of effect:** neutral, the only reading consistent with §7's own text ("first
applicable step wins"); recorded because §9 does not itself restate the step-1 predicate.

## 15. §9.4 informativeness bar computed unconditionally, not gated on the real verdict being a null

§9.4's bar text ("For a §7 step-2 null to be reported as informative...") is conditional
language about how a null WOULD be reported. The task's build instructions require the
sensitivity script to "Emit the resulting label" as one of the script's required outputs
regardless. `results/sensitivity.json` therefore always computes and emits
`informativeness.label`, with a note that the bar's normative force (whether it actually
qualifies a null) only applies if `results/envelope.json`'s decisional verdict is itself a
step-2 null. **Direction of effect:** neutral, additive-only; the label is diagnostic
context in this run's case (see the return summary for what the real decisional verdict
actually was).
