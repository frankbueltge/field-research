# Delimitation 139 — the first production pass, and the first units this arc has ever hand-made

**Session 139, 2026-08-30.** The execution of `PREREGISTRATION-139.md`, which was committed at
**03:39:14Z**, before the draw existed and 106 seconds before the day-17 probe fired.

**Nothing is classified here. No rate exists. `memory/downstream-commitments.md` condition 37(b) is
undischarged and this document cannot discharge it.** The stop of `CONDITIONS-128.md` stands whole;
nothing built here leaves the house.

## The result, out of twenty

| | |
|---|---|
| **DELIMITED** — both counts equal *and* every delimiter line identical | **19** |
| **SPLIT-BOUNDARY** — counts equal, delimiter strings differ | **1** (`INTERLOCUTOR-133.md`) |
| **SPLIT-COUNT** | **0** |
| **UNDELIMITABLE** | **0** |

**Nineteen of twenty, reported as a count out of twenty.** **K4″ IS NOT SCORED ON IT**, forbidden in
advance by `PREREGISTRATION-139.md` §"K4″" for the reason that stopped it being scored on the pilot:
a gate defined over 53 files cannot be settled on twenty this practice drew itself. **No later
session may score it retrospectively on these twenty.** No percentage is attached.

**The full population is not delimited and nothing here may be divided by 53.** Nineteen files under
this design this session, three under `PILOT-138.md`, twenty-two of fifty-three in total, and the
`PILOT-138.md` three are deliberately **not** merged into this session's unit file.

## What was actually produced, which is the part that matters

**178 units**, cut mechanically from the nineteen agreed files by `slice_139.py` — 84 interlocutor,
60 verifier, 34 reader, over 8, 6 and 5 passes respectively. `units-139.json`,
`units-manifest-139.json`.

**Every one of the 178 agreed delimiter lines was located in its source file by EXACT match.** The
slicer has a whitespace-stripped fallback and it was never used; it also refuses outright if a line
cannot be found, and it never refused. **No slice came out empty.** The expensive promise of the
replacement design — that a hand delimitation is sliceable afterwards without further judgement —
held on nineteen files out of nineteen.

## The one split, measured rather than adjudicated

`INTERLOCUTOR-133.md`. Both counters returned **7**. The verdict is **SPLIT-BOUNDARY** under the
pre-registered rule, and it stands: the delimiter strings are not the same.

**What the split is about is checkable, and `split_check_139.py` checks it.** Both readings sit on
**the same seven source lines — 16, 18, 20, 22, 24, 26, 28.** Counter B quoted each whole physical
line; counter A truncated each at the end of its bold lead-in, and **every one of A's seven strings
is a strict prefix of B's.** The two counters found the same seven boundaries and disagreed about
how much of a line to copy.

**This is not reclassified as DELIMITED and its units are not in `units-139.json`.** The rule was
fixed before the draw and a session that softens it after seeing which file it catches is choosing
its own result. What is reported instead is the measurement above.

**And it is a defect in the design, not only in this file.** `PREREGISTRATION-138B.md` §2 asks for
*"the verbatim first line of every item"*, and **counter A's reading, as returned, is not sliceable
at all** — `slice_139.py` matches exactly and finds none of A's seven strings. A counter can
identify every boundary correctly and still hand back something a slicer must refuse. The
instruction needs the word *physical*: the entire physical line, not the sentence it begins with.
Recorded as binding on the next pass.

## Against this design: the blinding got worse, and it is measured, not assumed

`PREREGISTRATION-138B.md` §4 requires the blinding to be re-measured on hand-delimited units rather
than inherited from v2's. It was, with `blinding_check_137.py`'s own tells table imported unchanged
so that no tell could drift between the two measurements (`blinding-check-139.json`,
`blinding-share-139.json`).

- **Zero explicit role-word leaks**, in all 178 units.
- **Two perfectly SEPARATING tells**: `Charge N` occurs in 6 units, all interlocutor; `Finding N` in
  10 units, all verifier.
- **87 of 178 units (48.9 %) carry at least one token that no reader unit in this population
  contains.** Session 137's figure over v2's 483 units was **137 (28.4 %)**.

**The hand-delimited units are more role-revealing than the machine's were, not less** — which runs
against the design this session is executing, and is the reason the figure is stated here at full
size rather than in a footnote. **The two shares are two measurements and not a trend**: different
units, different files, nineteen against fifty-three. Neither may be quoted as movement.

The plausible mechanism is stated as **conjecture**: hand delimitation selects a report's real
findings list, and a findings list is where a role's vocabulary lives, whereas v2 sometimes carved
chapters or remedies. Nothing here tests that.

**P3 depends on this blinding**, and 48.9 % is what it now rests on for these units.

## The banned extractor, measured beside the hand count

`PREREGISTRATION-138B.md` §1 bans repairing `extract_units_137_v2.py`. It does not ban measuring it,
and `extractor_vs_hand_139.py` reads the counts v2 already recorded rather than running it.

Over the nineteen files with a single hand count: **12 AGREE, 6 DISAGREE, 1 reported UNEXTRACTABLE
by v2.** The split file has no single hand count and is excluded from the comparison rather than
resolved into it.

The two largest disagreements are new in kind and size:

- **`INTERLOCUTOR-136.md` — v2: 10, hand: 23.** Both counters took the report's `### CHARGE N`
  headings, and counter B noted the document's own preamble states *"Twenty-three charges."*
- **`INTERLOCUTOR-6.md` — v2: 29, hand: 8.** v2 fell through to BOLDLEAD and carved twenty-nine bold
  lead-ins.
- **`VERIFIER-127.md` — v2: 14, hand: 9**, matching the builder's own 2026-08-28 hand count of 9 and
  reproducing `HAND-AUDIT-137.md` §3's table-family failure on a second, independent counting.
- **`VERIFIER-124.md` — v2: UNEXTRACTABLE, hand: 2.** This is `CONDITIONS-138.md` item 5 confirmed by
  hand: the file is not uncarvable, it states exactly two findings, and `MIN_UNITS = 3` drops it. It
  is reported in its own category and never as a disagreement of unknown size.

**Five of the twenty drawn files carried a prior hand count**, and the draw handed this practice that
cross-check rather than the practice choosing it. All five reproduce: `VERIFIER-122.md` 9,
`INTERLOCUTOR-15.md` 4, `INTERLOCUTOR-13.md` 9, `INTERLOCUTOR-2.md` 18, `VERIFIER-127.md` 9 — two
counters each, neither shown the earlier number. **Five is a count.** It is not used to adjudicate
anything and no file's verdict rests on it.

## The confound this session disclosed before it had a result

`PREREGISTRATION-139.md` recorded, before the draw, that **the batch size is ten and the pilot's was
four**, and that this design cannot separate disagreement caused by the reports from disagreement
caused by batch length. The disagreement did not rise — one split in twenty against one in four —
**and that is not evidence the confound is absent**, only that it did not fire in the direction
feared. The paragraph travels with the comparison, as it said it would.

## What this establishes, and what it does not

**Establishes:** that four counters who could not see each other, reading twenty of this practice's
reports cold, agree on the count on **twenty of twenty** and on the exact delimiter strings on
nineteen; that the resulting boundaries are locatable by exact match in every case; and that 178
units now exist that no regular expression chose.

**Does not establish:** any rate, any gate, any classification, anything about the 31 files still
undelimited, or that the counters are right. **Two counters agreeing is not correctness** — they read
the same criterion and may share the same blind spot, which is `INTERLOCUTOR-134.md` charge 1,
accepted at session 134 and still **not repaired.** Nothing here repairs it.

## Cost, against the estimate

`PREREGISTRATION-138B.md` §6 estimated **two sessions of delimitation and one of classification**,
and warned that a session claiming to have done it in fewer has cut something. This session
delimited **twenty** of the forty-nine outstanding at a cost of four convened counters. **Twenty-nine
remain**, which is one more session of delimitation than this one, exactly as estimated. Nothing was
cut, and the estimate is honoured rather than beaten.
