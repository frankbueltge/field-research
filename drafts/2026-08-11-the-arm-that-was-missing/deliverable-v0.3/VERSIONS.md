# Versions of this bundle, and what each one's status is

*Every version this practice has built, with what happened to it. A version that did not pass
its own gauntlet says so here, and its files stay retrievable at their published address so the
reports against them stay checkable.*

| Version | Date | Status | Where |
|---|---|---|---|
| 0.1 | 2026-08-15 | **WITHHELD — refuted at its gauntlet.** Its core claim was that reproducing an aggregate rate on a fixed panel warrants trusting a single reading of somebody else's list. This practice's own confirmation record refutes that, and the tool shipped in it took one pass and no confirmation. | `deliverable/` — unedited, plus `GAUNTLET-2026-08-15.md` listing every corrected statement with its true value |
| 0.1 + dated corrections | 2026-08-16 | **STILL WITHHELD.** Session 122 measured a reference-clock defect and published the corrected tables **beside** the originals rather than editing them. | `deliverable/*-CORRECTED-2026-08-16.*` |
| **0.3** | 2026-08-16 | **WITHHELD — the gauntlet FAILED.** Verifier **FAIL**, five blocking; Interlocutor: core claim **survives, narrowed**, two blocking. Every blocking finding was a *sentence*, not a measurement — and six of them were corrections this practice had already published on 2026-08-15 and reproduced unchanged. Reports published unedited (`VERIFIER-123.md`, `INTERLOCUTOR-15.md`); errata with true values in `ERRATA-123.md`. | `deliverable-v0.3/` as built at that commit |
| **0.3.2** | 2026-08-16 | **WITHHELD — the gauntlet FAILED, the fifth in a row on this bundle.** Session 124 routed `FIGURES.md` through the provenance guard, completed the errata accounting, moved the population caveat into the letter, and built the run lock. Verifier **FAIL**, one blocking: erratum **E20**, published by this session in `ERRATA-124.md`, was never brought into the errata accounting — *the session whose move was to account for every published erratum published one it did not account for*, and the build gate did not catch it because it did not read its own coverage report. | `deliverable-v0.3/` as the reviewer read it |
| **0.3.3** | **2026-08-16** | **WITHHELD — the gauntlet FAILED, the sixth in a row on this bundle.** This state was frozen, hashed before either reviewer was dispatched and re-hashed after both verdicts — 30 of 30 files unchanged, nothing edited under the reviewers — and read on 2026-08-17. Verifier **FAIL**, two blocking; Interlocutor: core claim **survives, narrowed**, one blocking. **All three blocking findings were in this file**, and the two Verifier findings were the two paragraphs that used to sit below this table describing what the guards cover: both were stale, and both described the bundle as *worse* than it is. The third is not a wording defect — the citation panel's own construction date is recorded nowhere in this arc. Reports published unedited (`VERIFIER-125.md`, `INTERLOCUTOR-17.md`), dispositioned in `CONDITIONS-125.md`. **The measurement half was recomputed independently by both roles and no numeric error was found** — the first pass on this bundle to find the arithmetic sound wherever it was tested. | `deliverable-v0.3/` as the reviewers read it, hashes in `FROZEN-033.sha256` |
| **0.3.3 + repairs of 2026-08-18** | **2026-08-18** | **WITHHELD, and these repairs carry NO VERDICT until the gauntlet of this date reports.** Per `CONDITIONS-125.md` binding item 1 the findings above are repaired **as edits and no new version number is claimed**: fixing prose that was already wrong does not earn one. What changed: the two stale guard descriptions are gone, replaced by a block this practice cannot type (below); the panel's undisclosed construction date is stated as a bracket in `LIMITS.md`; `LETTER.md` no longer says the run files are in this directory; the two provenance tables are named apart in `FIGURES.md`; one stale hash in `confirmation-record.json` is recomputed; and the persistence result the previous reviewer found in our own series is added. **A verdict is good only for the state it ran on, and the state above is not this one.** | this directory, hashes in `FROZEN-126.sha256` |

## What changed between 0.1 and 0.3

1. **The panel is longer.** 6 measurement days, 2026-08-11T11:24:06Z to 2026-08-16T03:37:40Z, built from
   6 run files whose sha256 are in `MANIFEST.json`.
2. **The reference-clock defect is fixed in the build, not patched beside it.** Version 0.1
   declared a reference time of one date and computed its age bands at another. In this version
   `t_ref_utc` is 2026-08-16T03:37:40Z and `ages_computed_at_utc` is 2026-08-16T03:37:40Z; where those two agree, the
   bands are the bands of the moment the table names.
3. **One live set of tables.** There are no `-CORRECTED-` twins in this directory. The
   superseded state is not deleted — it is at its own published address in `deliverable/`.
4. **The confirmation record is on the face of the bundle** (the `README.md` section headed
   *The measurement that refuted version 0.1*, and `confirmation-record.json`), not in an appendix. It is the measurement that refuted version
   0.1, and a receiver meets it before any rate.
5. **The tool is version 0.3.1**, with confirmation of refusals and a caller-side staleness
   report. Every figure it prints names the version and the `--confirm` setting that produced it.
6. **The prose is generated, and so is the description of the guard that generates it.** What
   each guard actually covers is no longer written by hand anywhere in this file. It is asked of
   the guards at build time and rendered into the block below, which `guard_claims.py --check`
   re-derives and compares character for character; the build fails if what is written there is
   not what the guards report. The reason is item 6's own history: every one of the six gauntlets
   this bundle has failed died on a sentence of exactly that kind, and the two that killed the
   last one used to be items 6 and 7 of this list.

7. **A published correction cannot come back silently.** `errata_check.py` holds this arc's
   published corrections as a machine checklist and fails the build if one is live again in the
   bundle. It was written because version 0.3 shipped six of them back. Its coverage is not
   described here; it is reported by the check itself, below.

8. **The absence readings carry their own persistence.** Added 2026-08-18: how stable an absence
   is across the six days, computed over the whole non-control panel rather than at the edges of
   it. It is reported in `FIGURES.md` and `LIMITS.md` and it is **not** the same evidence as the
   immediate-re-request confirmation record. It was found by the adversary at the sixth gauntlet,
   in a file this practice had held for six days and never read that way.

<!-- GUARD-CLAIMS:BEGIN - generated by guard_claims.py; do not edit by hand -->

### What the guards cover — asked of the guards, not typed

*Every figure and every claim in this section is produced by `guard_claims.py` from the guards' own live output at build time; `guard_claims.py --check` fails the build if what is written here is not what the guards say. It exists because six consecutive gauntlets on this bundle failed on sentences of exactly this kind — descriptions of the apparatus that were true when typed and false when read — while every number in them was correctly provenanced. A claim about a guard is a figure.*

**The prose provenance guard.** Every number in `README.md`, `LETTER.md`, `LIMITS.md`, `VERSIONS.md` is fetched from a named JSON field or declared a literal with a stated reason, and recorded in `FIGURE-PROVENANCE.json` (126 entries). Unmatched numbers in this build: **0**. The build refuses to complete if that is not zero.

**The figures page.** `FIGURES.md` is governed by a separate table, `FIGURES-PROVENANCE.json` (247 entries) — a different file from `FIGURE-PROVENANCE.json` above, and the near-identical names are a hazard this bundle has already misread once. Rendered tokens checked: **265**. Unmatched: **0**.

**The one limit of both.** They read digits. **Demonstrated in this build, not remembered.** The same false figure was put through the guard twice, once as `91827` and once spelled out. The digit form was flagged; the spelled-out form was not. A figure written as a word still passes untouched, and the digit half is the positive control that makes that a finding rather than a silence.

**The errata check.** `errata_check.py` holds this arc's published corrections as a machine checklist and fails the build if one is live again in the bundle. Its coverage is an accounting, not a sample: **53** published errata are accounted for — **36** registered as wording the build fails on if it returns, **17** left out with a stated reason — with **0** unaccounted and **0** broken mappings. What it still cannot do is unchanged: a false claim reworded escapes a phrase check.

<!-- GUARD-CLAIMS:END -->

## What did NOT change, and must not be read as changed

The correction in item 2 moved **no** count of absent units and did not change the pooled rate to
the last digit: every unit that crossed an age band under the corrected clock was retrievable on
both sides of it. It moved age-band cells and three of four age-gradient rows, and changed no
conclusion. A reuse that renders it as a change in how much absence was found reports something
this practice did not measure.
