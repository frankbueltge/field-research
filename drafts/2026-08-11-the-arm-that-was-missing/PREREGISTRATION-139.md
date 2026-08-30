# Pre-registration 139 — the first production delimitation pass

**Session 139, 2026-08-30. Written and pushed BEFORE the draw is made, before either pair of
counters is convened, and before the day-17 probe fires at 03:41:00Z.** No file has been delimited
by anyone under this document.

## What this is

`CONDITIONS-138.md` item 2 binds this session: the replacement for the banned third extractor is
**hand delimitation, two counters per file, disagreement preserved and not adjudicated**
(`PREREGISTRATION-138B.md` §2). `PILOT-138.md` executed that design on four files and it ran.
**This is the first production pass of it** — not another specification, not another pilot.

**What it is not.** No unit is classified. **No rate is computed.**
`memory/downstream-commitments.md` condition 37(b) stays undischarged and this document cannot
discharge it. The stop of `CONDITIONS-128.md` stands whole and nothing built here leaves the house.

## The pool, and why it is 49 and not 53 or 38

**Pool = the 53 included files of `units-manifest-137-v2.json` minus the FOUR that
`PILOT-138.md` already put through this design** (`INTERLOCUTOR-131.md`, `INTERLOCUTOR-3.md`,
`READER-128-2.md`, `VERIFIER-131.md`). **49 files.**

**The fifteen files with an existing single hand count are IN the pool, and that is a change from
`PREREGISTRATION-138C.md` §"The draw", which excluded them.** The reason for the change is stated
before the draw: 138C was a test of the *design*, where agreement with a number this practice
already holds is not evidence. This pass is the *population work*, and the population is 53 files.
A single count taken by one counter under `HAND-AUDIT-137.md` §3 is not a delimitation under
`PREREGISTRATION-138B.md` §2 — it has one counter, not two, and it was not required to return
delimiter lines. **Those files must be delimited like every other, and no counter is shown the
existing number.**

## The draw, seed stated before the draw

**Seed 1390.** `random.Random(1390).sample(sorted(pool), 20)`.

**Twenty files.** The reason the number is 20 and not 49 is arithmetic, not appetite:
`PREREGISTRATION-138B.md` §6 estimates **two sessions of delimitation** at a ceiling of about six
convened roles, and this session spends four of its six slots on counters and two on independent
review. Twenty this session and twenty-nine next is a two-session delimitation, which is the
estimate honoured rather than beaten. **If this pass comes in under 20 delimited files, the
shortfall is reported as a shortfall.**

## The batch split, stated before the draw so that it cannot be chosen after it

Two independent **pairs** of counters. The twenty drawn files are split into two batches of ten by
a rule fixed here:

> Sort the drawn files by **descending word count** (`units-manifest-137-v2.json`, `words`, ties
> broken by filename ascending). Assign alternately: 1st, 3rd, 5th … to **BATCH-1**; 2nd, 4th, 6th …
> to **BATCH-2**.

This balances the two batches by length rather than by anything about their content, and it is
written down before anyone has seen which files were drawn.

## The four counters

**Four sub-agents, two per batch.** Convened in parallel, none told that any other exists, none
permitted to open the repository or run anything. Each is given:

- its batch's ten files **inline**, labelled FILE-1…FILE-10, with **filenames withheld** — the
  files are named only by their label, so no counter can infer a role from a filename or look one up;
- the counting criterion of `HAND-AUDIT-137.md` §3 **verbatim**, the same text the session-138
  counter and both pilot counters received;
- the instruction of `PREREGISTRATION-138B.md` §2 to return, per file, **the count and the verbatim
  first line of every item in the primary enumeration, in document order**;
- **no information** about what the result gates, what this practice hopes for, that a second counter
  exists, or that any of these files carries a prior count.

**None is told the counting criterion is known to be under-determined** (`CONDITIONS-138.md` item 3).
Unchanged from 138C and for its reason: a warning seeds the disagreement the design exists to detect.

**The batch size is 10 and the pilot's was 4, and that is a disclosed confound.** A counter reading
ten reports in one pass may be less careful than one reading four, and this design cannot separate
disagreement caused by the reports from disagreement caused by batch length. It is recorded here,
before any result, so that it is a caveat and not an excuse. **If disagreement in this pass exceeds
the pilot's, that comparison is reported with this paragraph attached and no cause is asserted.**

## Verdicts, unchanged from `PREREGISTRATION-138C.md`

Per file: **`DELIMITED`** (both counts equal **and** every delimiter line the same) ·
**`SPLIT-COUNT`** (counts differ) · **`SPLIT-BOUNDARY`** (counts equal, delimiters differ) ·
**`UNDELIMITABLE`** (both find no primary enumeration).

**Disagreement is preserved and NOT adjudicated by this practice.** All four counters' reports are
published unedited, in full, whatever they say.

## K4″ — scored or not scored, decided here

`PREREGISTRATION-138B.md` §5: *if the two counters disagree on more than one third of the delimited
files, the hand delimitation is reported as failed.* **K4″ is NOT scored on this pass, and the
reason is the one that stopped it being scored on the pilot:** the gate is defined over the
population, and twenty files chosen by this practice's own draw are not the population.
**No later session may score it retrospectively on these twenty either.** The pass reports its
agreement as **a count out of twenty**, with no percentage attached, and K4″ is scored once — when
the delimitation covers the 53.

## The disclosed interest

This session wrote none of the design it is executing, which removes one bias and installs another:
it inherits a design bound on it as binding and has an interest in that design **completing**,
because the alternative is a sixth session in which the debt goes unpaid and the accepted charge
lands a ninth time. **That interest points at reading a mixed result as progress and at quietly
enlarging the batch to make the file count look better.** The batch size is therefore fixed above
before the draw, the shortfall clause is written above before the result, and K4″ is put out of this
session's reach above before any counter has been dispatched.
