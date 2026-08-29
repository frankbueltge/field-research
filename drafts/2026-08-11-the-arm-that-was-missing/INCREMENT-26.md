# Increment 26 — the gate fired again, and this time the population was measured instead of a third extractor built

**Session 138, 2026-08-29.** One move: run `PREREGISTRATION-137B.md` to its end. It ended in a
kill condition, for the second consecutive session, and the standing finding
`HAND-AUDIT-137.md` §3 named in advance is now the result.

**Nothing here is verified by this practice's standard until the reviewers convened at §6 have read
it, and nothing ships under any outcome.**

---

## 1. What was locked before any evidence existed

| act | time (UTC) | record |
|---|---|---|
| session opened | 03:36:09 | `.session-open-2026-08-29.md` |
| **day 16 of the instrument reserved** | **03:36:33** | `run_day16-2026-08-29.sh`, `ledger/.run-lock-…-2026-08-29.json` |
| three inherited sha256 pins re-verified, all MATCH | 03:37 | `PREREGISTRATION-138.md` §1 |
| **`PREREGISTRATION-138.md` pushed** — seed 1380, block split, the counting role | **03:39:24** | commit on `research/session-2026-08-29` |
| daily probe fired, vantage AS396982 | 03:41:00 | `ledger/run-2026-08-29T0341Z.json` |
| **the K4′ draw made** | after 03:41 | `k4prime-draw-138.json` |

**The seed was in the public record 96 seconds before the probe fired and before the draw existed.**
That ordering is the whole guarantee this session offers about its own honesty on the draw, and it
is checkable from the commit times without asking this practice anything.

## 2. K4′ fired: two of five, counted by someone who did not build the instrument

Full record and the counter's unedited report: `HANDCOUNT-138.md`.

| drawn file | v2 units | v2 family | hand | verdict |
|---|---|---|---|---|
| `INTERLOCUTOR-11.md` | 6 | LISTNUM | **5** | **DISAGREE** |
| `INTERLOCUTOR-15.md` | 4 | CHARGE | 4 | AGREE |
| `READER-128-3.md` | 6 | HEADNUM | 6 | AGREE |
| `VERIFIER-125.md` | 5 | CHARGE | 5 | AGREE |
| `VERIFIER-134.md` | 7 | HEADNUM | **6** | **DISAGREE** |

**More than one of five disagrees. No rate is published and the extractor is reported as unfit —
the same sentence session 137 wrote about v1, one extractor later.**

**Both disagreements are the two defects v2's own docstring says it was built to repair**, recurring
on files v2's design never saw, and both were recomputed here against the files before adoption:

- `INTERLOCUTOR-11.md` — v2 carved the **six numbered remedies** of its `# CONDITIONS` section
  instead of the five `**Claim N — …**` lead-ins that carry its verdicts. *"A remedy is not a
  finding"* is defect 1 of the docstring. v2's repair cannot reach it: *specific families win by
  kind* privileges only CHARGE and LABELLED, so a bold-lead-in finding family loses to any six-item
  numbered list, because BOLDLEAD fires only when **every** other family is below MIN_UNITS.
- `VERIFIER-134.md` — v2 carved the **seven `## N.` chapters** instead of the six items of its
  `## Summary of findings`. *"It preferred a report's chapters to its findings"* is defect 2.

**The independent counter reached both by reading, without seeing any machine count.** That is
`CONDITIONS-137.md` binding item 3 firing for the first time, and it is the second consecutive
session in which the one independent pair of eyes convened found what this practice's own hand had
not.

## 3. The population-wide diagnostic, owed since session 137 and now run

`carve_audit_138.py` → `carve-audit-138.json`. `CONDITIONS-137.md` binding item 2 is discharged.
**It classifies nothing and computes no rate**, and it is **a lower bound on mis-carving, never a
clean bill** — each detector encodes one failure mode already demonstrated by hand, so a sixth kind
of mis-carve is invisible to it and counts as clean.

**53 files · 51 extracted · 2 unextractable** (`INTERLOCUTOR-16.md`, `VERIFIER-124.md`).

| detector | what it catches | files |
|---|---|---|
| **D2** heterogeneous label series | `### F0-a.`…`F0-j.` (a *"what reproduced"* table) sharing a family with `### F1.`…`F18.` | **1** — `VERIFIER-120.md` |
| **D3** findings stated as table rows | an identifier-led table v2 has no family for | **8** |
| **D4** remedies won | every delimiter lies under a CONDITIONS/FIXES heading | **1** — `INTERLOCUTOR-11.md` |
| **D5** chapters over summary | a summary-of-findings list exists and v2 carved outside it | **1** — `VERIFIER-134.md` |
| **flagged by any** | | **11 of 53 (20.8 %)** |
| **contested family choice** — *not a defect claim* | more than one family reached MIN_UNITS, so the choice was a contest rather than a reading | **34 of 53 (64.2 %)** — 21 of 26 Interlocutor, 11 of 16 Verifier, **2 of 11 reader** |

**The bound is below the hand-measured disagreement and that is the point.** Over the ten fresh
files ever hand-counted against v2 — five at session 137 by the builder, five today by an
independent counter — **three disagreed**. The syntactic detectors name **three** files
population-wide with the precision to reproduce ground truth, and eleven with D3's candidates
included. **Three of ten is a count and not a rate**, and this arc has published against itself that
six events is not one; but a syntactic bound of 3 in 53 sitting under a hand result of 3 in 10 says
plainly that **the detectors find what has already been demonstrated and little else.**

## 4. The diagnostic's own validation FAILED, and the failure is the most useful thing in it

The script asserts, before its output is used, that every hand-DISAGREE file is flagged and no
hand-AGREE file is. **It exits 1.** `VERIFIER-133.md` is hand-AGREE at 4 and D3 flags it: the file
carries both a ten-row `## Item-by-item` verification table and a four-item
`## Findings (blocking / non-blocking)` list.

**The detector was not tuned to pass, and it will not be.** Tuning a diagnostic against the only
ground truth it has is the move this practice has spent two sessions refusing in an extractor, and
it does not become acceptable in an auditor. What the failure locates is a defect **in the study's
own counting rule, not in the extractor**: `HAND-AUDIT-137.md` §3's criterion does not uniquely
determine a primary enumeration for a verification report that carries both a checklist and a
findings list.

**The convened counter found the same ambiguity independently, on a different file, unprompted** —
`VERIFIER-125.md`, returned AGREE at MEDIUM confidence with the competing 26-item recompute list
named in its own words. Two instruments that could not see each other landed on one hole in the
rule. It is recorded as owed and **deliberately not resolved by this session**, which has now seen
which files it moves.

## 5. What follows: `PREREGISTRATION-138B.md`, locked before any replacement unit exists

- **No third extractor**, and the ban states its own escape clause so that lifting it costs what
  deferring it has cost.
- **Hand delimitation by two independent counters per file**, returning the verbatim first line of
  every item so the slicing needs no further judgement; **disagreement is preserved, not
  adjudicated** — every statistic computed under both readings.
- **K4″**: counters disagreeing on more than a third of files ⇒ the standing finding becomes that
  these reports are not delimitable at finding granularity **by any means this practice has**, and
  that is published as the answer to `POST-MORTEM.md` §8 Q1's hit-rate half.
- **The cost is stated**: two sessions of delimitation and one of classification, at this practice's
  role ceiling. Naming the cost is not a licence to defer it.
- **One shortcut declined on the record.** The primary statistic could be answered by reading each
  report whole — no delimitation, a number today. It is declined because an unblinded whole-report
  read destroys the blinding P3 depends on, and because this session wrote down that it wanted a
  publishable rate before it knew it would not get one.

## 6. What this increment is not

- **No rate exists.** `downstream-commitments.md` condition 37(b) stands undischarged, and nothing
  computed today could discharge it.
- **No unit was classified. No label exists.** The pinned dataset of `PREREGISTRATION-137B.md` is
  untouched and its three hashes still match.
- **The `VERIFIER-120.md` conflation is unrepaired** and is republished here beside every figure, as
  `CONDITIONS-137.md` item 1 requires: 28 units of which ten are a *"what reproduced"* table.
- **Nothing left the house.** The stop of `CONDITIONS-128.md` stands whole; no delivery object, no
  repair pass, no packet, and this session did not ask for the stop to be lifted
  (`CONDITIONS-137.md` item 6: *do not ask again before 2026-09-05*).
- **The shared-bias objection is not repaired**, in this document or anywhere.
