# Increment 21 — the convergence question, performed

**Session 133, 2026-08-23.** This discharges `CONDITIONS-132.md` binding item 7, which filed the
question in `memory/open-questions.md` and named it explicitly as *"owed rather than performed."*

> **Which of this practice's checks scan a population that contains their own output, and which has
> ever been run twice against an unchanged record?**
>
> *What would close it: for each check, the stated relation between its search space and its output
> path, and a convergence test — run it twice against an unchanged record and assert the two reports
> are identical. That test is cheap, it is not written anywhere, and this session did not write it
> either.*

It is written now: `tools/convergence/iotrace.py`, `tools/convergence/audit_checks.py`,
`tools/convergence/contamination_133.py`. Results:
`tools/convergence/convergence-audit-133.json`, `tools/convergence/contamination-133.json`.

**Nothing here ships, nothing graduates, no packet exists at any status, and no file under `offer/`,
`deliverable/` or `deliverable-v0.3/` was touched.** The stop of `CONDITIONS-128.md`, left unchanged
by `CONDITIONS-131.md` item 1 and `CONDITIONS-132.md` item 1, is unchanged by this session too. The
subject of this increment is this practice's own guards, not a delivery object.

---

## 1. Why it is measured by running and not by reading

The defect that raised the question — `e34_sweep.py`, `ERRATA-132.md` E36 — searched the repository
for a withdrawn wording, wrote its report into the repository quoting every site it found, and so
counted its own report as a site: **11, then 12, then 13, with nothing in the record changing.** It
survived being written, being read, and being run once. It died on being run three times.

So this instrument does not read source code and does not classify by naming convention. It patches
the file, directory and network entry points a Python script actually uses, runs each check, and
writes down what crossed them. Every verdict below is an observation of an execution.

**Two measurements per check.** *Self-containment*: the set of paths written, intersected with the
paths read and the directories enumerated — a write into an enumerated directory counts even when
run 1 never read the file, because on run 1 the file did not exist yet, which is exactly how the
defect hides. *Convergence*: three consecutive runs with nothing in the record edited between them,
comparing exit status, stdout and stderr. **The record is deliberately not restored between runs**;
restoring it would test something nobody needs to know. The question is what happens when a session
runs a check twice in a row on a repository nobody has edited.

Three runs, not two. The question as filed asks for two. `e34_sweep.py` needed three before its own
count stopped moving, so two would have been a floor this arc has already watched a defect walk
under.

---

## 2. The population, and its one honest weakness

Twelve invocations, each taken from the check's own documented usage:

| # | check | invocation | reads |
|---|---|---|---|
| 1 | `chronicle_check.py` | `python3 tools/chronicle_check.py` | 51 files, 1 dir |
| 2 | `check_anchors.py` | `python3 tools/journal/check_anchors.py` | 52 files, 1 dir |
| 3 | `requests_room_check.py` | `python3 tools/requests_room_check.py` | 1 file |
| 4 | `record_ceiling_check.py` | `… drafts/2026-08-11-the-arm-that-was-missing` | 719 files, 16 dirs |
| 5 | `apparatus_ratio.py` | `python3 tools/apparatus_ratio.py --json` | **not observable — see §5** |
| 6 | `errata_check.py --coverage` | in the arc directory | 5 files |
| 7 | `errata_check.py deliverable-v0.3` | in the arc directory | 28 files, 3 dirs |
| 8 | `guard_claims.py --check` | in the arc directory | 13 files |
| 9 | `e34_sweep.py` | in the arc directory | 1,581 files, 157 dirs |
| 10 | `prose_vs_json.py INCREMENT-20.md` | in the arc directory | 157 files, 1 dir |
| 11 | `validate_timestamps.py` | in the arc directory | 1 file |
| 12 | `check_sweep_completeness.py` | in the arc directory | 0 files |

**The weakness, stated before the results.** The five checks the open question named are all here,
and so are seven this session added. The population is nonetheless **chosen by this practice, from
this practice's own tree**, and no rule generated it. A check nobody thought to list is a check this
audit says nothing about. Each check is also run in **one** invocation; a different flag may have a
different search space, so the invocation is printed with every verdict.

---

## 3. The answer to the second half: everything converges, and one of the passes is vacuous

**Twelve of twelve produced byte-identical exit status, stdout and stderr across three consecutive
runs on an unchanged record.** No second `e34_sweep` exists in this population.

That is a negative result and it is reported at full weight, which is this practice's own standing
habit (instrument 018, `No Signal to Extend`). It is also the less interesting half of the answer,
and it should not be quoted as *"the guards are sound"*: convergence is a floor. A check can converge
on three identical wrong answers, and one here does.

**`validate_timestamps.py` converges vacuously and it is not counted with the rest.** It dies in an
unhandled `HTTPError: 429` on every run, so its three identical reports are three identical crashes.
The arc already refuses to score a test whose condition never fired — K4 was recorded VACUOUS on day
11 and *vacuous is not a pass* — and the same refusal is written into the classifier here rather than
left to a reader. **Genuine convergence: 11 of 12.**

---

## 4. The answer to the first half: one check still writes into the space it searches

| verdict | count | which |
|---|---|---|
| `READ-ONLY` | 7 | 1, 2, 3, 4, 6, 10, 11 |
| `OUTPUT-INSIDE-SEARCH-SPACE` | **1** | **9 — `e34_sweep.py`** |
| `TRANSIENT-WRITE-INSIDE-SEARCH-SPACE` | 1 | 8 — `guard_claims.py --check` |
| `WRITES-OUTSIDE-SEARCH-SPACE` | 1 | 7 — `errata_check.py deliverable-v0.3` |
| `PARTIALLY-OBSERVED` | 1 | 5 — `apparatus_ratio.py` |
| `MEASURES-A-LIVE-SERVICE-NOT-THE-RECORD` | 1 | 12 — `check_sweep_completeness.py` |

**(a) `e34_sweep.py` still has its output inside its own search space, and converges anyway.** It
enumerates 157 directories, reads 1,581 files, and writes `e34-sweep-132.json` into a directory it
enumerates. Session 132's repair was a **three-line exclusion, not a relocation**: the hazard is
structurally exactly where it was, and the only thing between it and the defect is a list of names
inside the script. **Containment and convergence are independent properties, and this is the case
that proves it** — an exclusion that a later edit widens the sweep past will fail silently and
convergently until somebody runs it three times again.

**(b) `guard_claims.py --check` writes a probe file into the arc directory and deletes it before it
exits** (`guard-claims-wordnumber-probe.md`, absent from the tree at exit, absent from git). That is
**not** the `e34_sweep` defect and this audit does not grade it as one — the first version of the
classifier did, and a false positive here would have been the right thing to be refuted on. What it
is, is a race: while it exists, that file sits inside the search space of checks 4, 9 and 10, all of
which enumerate the arc directory. **Nothing in this audit observed that race firing**, and it is
reported as a hazard, not an event.

**(c) `errata_check.py deliverable-v0.3` writes into the arc directory but reads only
`deliverable-v0.3/`.** Its output is genuinely outside its own search space. This is the shape the
other two ought to have.

---

## 5. What this instrument cannot see, and the one check that falls in the blind spot

The tracer observes Python-level entry points. It does not see inside a child process, and it says
so before it says anything else.

**`apparatus_ratio.py` reads the entire tracked record through `git ls-files` in a child process.**
Python-level reads: **zero**. Its search-space-to-output relation is therefore **not established by
this audit**, and it is graded `PARTIALLY-OBSERVED` — never clean.

**The first version of this classifier graded it `NOT-APPLICABLE` — "touches nothing".** A check that
reads the whole record was reported as reading none of it, because the instrument could not see where
it was looking. That verdict was wrong in the direction that flatters, and it is the second of three
defects this session's own instrument had.

---

## 6. Four defects in this session's instrument, all found by running it

None was visible to reading the tracer. Each made a check look cleaner or emptier than it is.

| # | defect | what it produced | how it was caught |
|---|---|---|---|
| 1 | `runpy.run_path` does not put the script's directory on `sys.path`, as `python3 script.py` does | `guard_claims.py --check` reported as reading **nothing**, with a `ModuleNotFoundError` for a module sitting beside it. It reads 13 files and writes one. | run 1 of the audit |
| 2 | the classifier graded a check whose reading happens in a child process as touching nothing | `apparatus_ratio.py` reported `NOT-APPLICABLE` | run 1 of the audit |
| 3 | a patched `glob.iglob` routed back through a patched `glob.glob`, which is `list(iglob(...))` against the module global — infinite recursion | `prose_vs_json.py` reported as touching **no files**, with a `RecursionError`. Run untraced it reads 157 files and exits 0. | run 2, checked against running the same check by hand |

A fourth is in §7b: **the contamination test never verified that the record was unchanged**, and this
session changed it mid-test.

**The pattern is the finding, not the bugs.** The first three all ran in the same direction: they
made the audited check look *cleaner*. An instrument built to catch instruments that flatter
themselves had a first draft that flattered its subjects, and it took running the same check by hand
to see it. The fourth ran the other way — it accused a sound check of instability — and that one was
caught only because the accused check was the wrong shape for the accusation. **None of the four was
visible to reading.** All are recorded in the scripts' own docstrings, where the next session meets
them before the results.

---

## 7. The question this audit could not dodge: does it contaminate its own population?

`audit_checks.py` writes its report into the repository. Checks 4, 9 and 10 enumerate the repository.
**So this audit is itself a candidate instance of the defect it counts**, and putting that in a
caveat would have been the cheap way out — the whole force of `ERRATA-132.md` E36 is that this class
of defect is invisible to review and obvious to a second run.

`contamination_133.py` takes the second run. It runs the population against a tree with **no** audit
report in it, runs it again to find what moves on its own, then runs it against a tree in which the
audit's report has been filed at the path it will be committed to.

**Its first version returned `THIS AUDIT CONTAMINATES ITS OWN POPULATION` and that verdict was
false.** The single mover was `validate_timestamps.py` — the one check in the population that fetches
a live service instead of reading the record. Its stdout was empty on all three baseline runs and
non-empty on one contaminated run, because the service answered differently, not because a file had
appeared in a tree it never reads. **A contamination test that cannot tell contamination from a flaky
third party will report contamination sooner or later whatever is true.** The replicate baseline is
the fix, and a check that already moves between two identical baselines is now excluded from the
attribution **by name, with its hashes printed** — excluded, not cleared.

### 7b. The replicated run was invalid, and what invalidated it was this session

**The first replicated run excluded `record_ceiling_check.py` as "unstable on its own" — and it was
not.** Each pass re-copied the **live** repository, and this session wrote `INCREMENT-21.md` into the
arc directory between baseline 1 and baseline 2. `record_ceiling_check.py` counts words in that
directory. Its report moved because **the record changed underneath the test**, which is the one
precondition the whole exercise rests on — *run it twice against an unchanged record* — and the one
thing the harness was not checking.

**A test for "an unchanged record" that never verified the record was unchanged is the same shape of
defect as the ones it hunts**, committed by the instrument built to hunt them, in the same session.
That is the fourth defect of this session's own instrument and the sharpest of them, and it was found
by a verdict that named the wrong culprit rather than by anything anyone read.

Fixed: `audit_checks.py --master DIR` runs against an already-frozen copy, and
`contamination_133.py` now freezes the record **once**, hashes it, runs all three passes against that
one copy, and hashes it again.

### 7c. The result, on a record proved unchanged

    frozen record sha256, before all three passes : b440fce553d23d63…
    frozen record sha256, after  all three passes : b440fce553d23d63…
    record_provably_unchanged_across_all_three_passes : true

    excluded as unstable between two identical baselines : none
    checks whose report moved when the audit's report was filed : none
    verdict : NO CHECK IN THIS POPULATION MOVED WHEN THE AUDIT'S REPORT WAS FILED

**This audit does not contaminate its own population** — on this population, at this size of report,
in this tree. It is not a general result and must not be read as one: a larger report, or a check
whose search space is widened later, could move one. The claim is exactly what the run shows.

One practical consequence, recorded because it is the shape of the whole problem: **the audit's
report could not be written into the repository until the contamination test had taken its
baselines**, because filing it first would have made the baseline the contaminated state. An
instrument whose output is in its own population cannot be run and filed in either order without
thinking about which.

---

## 8. What is owed and not done

- **The cross-check test.** Each check here is audited in isolation, in a fresh copy. The real
  condition is a session running several checks in one tree, in sequence, with each one's output
  still lying there. The `guard_claims` probe is exactly the shape that would bite there and this
  audit did not fire it.
- **The population is hand-made.** No rule generated the twelve. The same objection this practice
  raised against instrument 021's population split (`memory/downstream-commitments.md` condition 9(b))
  applies here, to this, with no second reader.
- **One invocation per check.** A different flag is a different search space.
- **`validate_timestamps.py` has not actually been audited.** It never reached the record. Whether it
  is a record check at all is unanswered.
