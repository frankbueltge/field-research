# Versions of this bundle, and what each one's status is

*Every version this practice has built, with what happened to it. A version that did not pass
its own gauntlet says so here, and its files stay retrievable at their published address so the
reports against them stay checkable.*

| Version | Date | Status | Where |
|---|---|---|---|
| 0.1 | 2026-08-15 | **WITHHELD — refuted at its gauntlet.** Its core claim was that reproducing an aggregate rate on a fixed panel warrants trusting a single reading of somebody else's list. This practice's own confirmation record refutes that, and the tool shipped in it took one pass and no confirmation. | `deliverable/` — unedited, plus `GAUNTLET-2026-08-15.md` listing every corrected statement with its true value |
| 0.1 + dated corrections | 2026-08-16 | **STILL WITHHELD.** Session 122 measured a reference-clock defect and published the corrected tables **beside** the originals rather than editing them. | `deliverable/*-CORRECTED-2026-08-16.*` |
| **0.3** | **2026-08-16** | see the banner on `README.md` of this directory | this directory |

## What changed between 0.1 and 0.3

1. **The panel is longer.** 5 measurement days, 2026-08-11T11:24:06Z to 2026-08-15T03:37:40Z, built from
   5 run files whose sha256 are in `MANIFEST.json`.
2. **The reference-clock defect is fixed in the build, not patched beside it.** Version 0.1
   declared a reference time of one date and computed its age bands at another. In this version
   `t_ref_utc` is 2026-08-15T03:37:40Z and `ages_computed_at_utc` is 2026-08-15T03:37:40Z; where those two agree, the
   bands are the bands of the moment the table names.
3. **One live set of tables.** There are no `-CORRECTED-` twins in this directory. The
   superseded state is not deleted — it is at its own published address in `deliverable/`.
4. **The confirmation record is on the face of the bundle** (`README.md` §3,
   `confirmation-record.json`), not in an appendix. It is the measurement that refuted version
   0.1, and a receiver meets it before any rate.
5. **The tool is version 0.3.1**, with confirmation of refusals and a caller-side staleness
   report. Every figure it prints names the version and the `--confirm` setting that produced it.
6. **The prose is generated.** Every figure in this directory's `README.md`, `LETTER.md` and
   `LIMITS.md` was read from a JSON field by `figures.py`, which recorded the field.
   `FIGURE-PROVENANCE.json` is that record — a number in the prose that is not in it was typed
   by a human, and the build refuses to complete with `--audit` if one is.

## What did NOT change, and must not be read as changed

The correction in item 2 moved **no** count of absent units and did not change the pooled rate to
the last digit: every unit that crossed an age band under the corrected clock was retrievable on
both sides of it. It moved age-band cells and three of four age-gradient rows, and changed no
conclusion. A reuse that renders it as a change in how much absence was found reports something
this practice did not measure.
