# Skeptic pre-read on the pre-registration — verdict and disposition (session 63)

The Skeptic was convened on the DRAFT pre-registration before the lock (the lock is
irreversible by the commitment's own terms — no threshold adjustment, no re-run — so a
defect surviving the lock is permanent). Verdict: **PASS WITH CONDITIONS — 7 blocking, 8
non-blocking.** All seven blocking conditions were adopted before the lock; the full verdict
text is preserved in the session-63 journal entry (`journal/2026-07-25.md`).

## Blocking conditions → how each was fixed (all in PREREGISTRATION.md, pre-lock)

1. **Stratum verdict vocabulary had an undefined bucket** (a majority-REVERSE stratum — e.g.
   2 metrics REVERSE + 2 NO-ANOMALY — satisfied neither the directional-finding test nor the
   kill test; the B1 "all three outcomes reachable" guarantee was silently at risk at the
   verdict level). → §7 rebuilt as an ordered 3-step procedure (directional finding → kill →
   plurality headline over the full label set); every configuration now lands in exactly one
   step; majority-REVERSE ships as REVERSE.
2. **REVERSE had no anomaly-established gate** — a swing between two never-anomalous windows
   could manufacture a "recovery" headline (the Skeptic's constructed CASE E collided with
   NO-ANOMALY on the same z-series). → REVERSE now requires (A_ref OR A_ext); labels are
   evaluated in a fixed order (NO-ANOMALY → NEW-ONSET → CONTINUE → PLATEAU → REVERSE →
   RESIDUAL), exhaustive and mutually exclusive. (The ordering also fixed a
   conductor-introduced shadow bug: CONTINUE's condition is a superset of NEW-ONSET's, so
   NEW-ONSET must be tested first.)
3. **The marker channel's excess direction was never formally defined** (§4's threshold is
   typed to the collapse tail; a literal implementer would have tested for anomalously LOW
   marker usage, voiding the control-validity gate). → §8 now fixes: no reorientation,
   out-of-band = z > +2.1448, with the failure mode named.
4. **The document claimed present-tense unit tests that did not exist** (tests/ was empty at
   pre-read — a "never fabricate" violation aimed at ourselves). → wording changed to
   intent + a binding condition: the lock commit contains the passing tests (the Builder
   was already building them when the pre-read landed; verified before the lock).
5. **Heteroscedasticity:** the whole-cell marker rate's precision varies ~√41× across the
   window while gating the control's veto; MTLD's 1,000-abstract cap mixed
   capped/uncapped regimes inside the cs.CL envelope. → the marker channel's decisional
   statistic moved to the same fixed 15,000-token pool as metrics 2–3 (whole-cell rate
   demoted to context); MTLD's draw fixed at 150 (constant across all cells); residual
   corpus-growth heteroscedasticity disclosed in §4 with its (conservative) direction.
6. **The seeded draw was underdetermined** (`sample()` vs `shuffle()`-prefix give different
   draws from the same seed). → §3 fixes the realization: one seeded shuffle per cell, every
   draw a prefix of that order.
7. **Non-computable cells had no defined effect on Δ or the two-consecutive rule** — and the
   failure mode concentrates exactly where collapse is severest. → §3 now defines the
   handling (excluded from Δ; cannot satisfy the rule; <2 computable units ⇒ metric
   non-decidable, excluded from the ≥2-of-4 with disclosed denominator; flags reported
   prominently).

## Non-blocking cautions → disposition

1. δ-threshold rationale (why 0.5) → one-paragraph rationale added to §6.
2. One-sided α=0.025 vs "95% PI" wording → stated precisely in §4.
3. Current-version-abstract contamination unbounded → a free datestamp-based upper bound
   per stratum is now pre-registered to ship with the Dossier (§2).
4. Any-listing counts are upper bounds; fallback trigger frequency unverified → fallback
   trigger counts now ship in the output table (§3); no pre-harvest primary-only recount
   exists (the count route cannot filter primary-only).
5. Control-window asymmetry (7-unit combined) undocumented → rationale added to §7.
6. Linear-only envelope vs steep growth → the quadratic sensitivity is now a **soft
   downgrade rule** (decisional): linear/quadratic headline disagreement ships both,
   unresolved (§4).
7. "No bulk v1 abstracts" claim unsourced → reworded as the conductor's tested observation,
   searched-not-proven-absent (§2).
8. Author fields in raw XML vs the no-personal-data bound → §2 now states the filtered
   corpus keeps no author fields and raw XML stays out of git.

## Constructed cases

The Skeptic's seven constructed z-series (CASES A–G) were re-checked by the conductor
against the amended §6/§7: A→CONTINUE, B→NEW-ONSET, C→PLATEAU, D→REVERSE-FULL,
E→NO-ANOMALY (the collision is gone), F→step-3 REVERSE headline (the gap is closed),
G→RESIDUAL. They are preserved with the full verdict in the journal and are the seed of the
classification unit tests.
