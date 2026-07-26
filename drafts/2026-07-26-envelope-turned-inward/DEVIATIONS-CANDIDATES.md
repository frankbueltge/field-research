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
