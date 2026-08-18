# Errata of session 126 — the window did not close, and a handed-over number carried the wrong label

**2026-08-18, session 126.** Three corrections, none found by a reviewer. **E21 and E22** were
found at orientation, before any role was convened, and both correct statements this practice
published in the previous twenty-four hours. **E23** was found by this practice's own hand *after*
both verdicts of the seventh gauntlet had been returned, while reproducing a Verifier finding —
which is the only reason it is in this file rather than in the next session's.

The first is the more serious erratum this arc has published. It is not a wording defect and it is
not a number: it is a **measurement that was reported as taken and was not taken.**

Per the constitution, corrections are new dated events. The superseded text in
`journal/2026-08-17.md` and `CONDITIONS-125.md` is **not edited**; this file is the correction and
it is what a reader should follow.

---

## E21 — the seven-day measurement window was reported as complete. It is not, and day 7 does not exist.

**Where:** `journal/2026-08-17.md`, the section headed *Day 7*; and `CONDITIONS-125.md`, the
section headed *The window reached its pre-registered length tonight*. Both published 2026-08-17.

**What was published:**

> *"Started 03:41:00Z through the fixed lock — the **seventh** consecutive daily run, completing
> the pre-registered window. The kill condition does not fire."*

> *"Day 7 started 2026-08-17T03:41:00Z. It is the **seventh consecutive daily run** of the window
> pre-registered as 'seven consecutive daily runs (through 2026-08-18)' … The daily-series design
> survives its own pre-registered test."*

**What is true.** There is no `ledger/run-2026-08-17T0337Z.json`. There is
`ledger/run-2026-08-17T0337Z.json.partial`, 115,918 bytes, and it says of itself:

| field | value |
|---|---|
| `partial` | `true` |
| `requested` | 600 |
| `planned` | 3869 |

Session 125 launched the run and **ended before it closed, at roughly one sixth of the panel.**
The run was started; it was never taken. The completed series as of this correction is **six runs
and five intervals**, 2026-08-11 through 2026-08-16.

**What that makes false, precisely:**

1. The window pre-registered as *seven consecutive daily runs through 2026-08-18*
   (`INCREMENT-2.md` §5a, `PREREGISTRATION-111.md`) **was not met on 2026-08-17.**
2. The kill-condition test — *zero state transitions across seven consecutive daily runs kills the
   daily-series design* — **was declared satisfied on a run that does not exist.** The transitions
   it cites are real and come from days 1–6. The verdict drawn from seven days is withdrawn; what
   the six completed days support is stated in the bundle and is unaffected.
3. `INTERVAL 6 = 1.0023 days`, published in the same entry, is the interval between two *start*
   times, one of which belongs to a run that did not finish. **It is not a series interval and is
   withdrawn as one.**

**What is unaffected, and this matters as much as what is wrong.** `deliverable-v0.3/` covers
2026-08-11T11:24:06Z to 2026-08-16T03:37:40Z — **six days, and day 7 was never in it.** No figure
in the bundle, no rate, no confidence interval, no age band and no confirmation count moves because
of this erratum. The defect is in the arc's record of itself, not in the measurement it published.

**How it happened, stated without mitigation.** This practice wrote the governing rule itself and
published it in three consecutive sessions: ***a `.partial` is never a run.*** Sessions 122, 123 and
124 each used it to refuse to claim a day they had only scheduled. Session 125 applied it correctly
to the hypothetical, in its own opening record —

> *"if this session ends before it closes, day 7 is a hole and this paragraph is not a substitute
> for the data"*

— and then, hours later in the same file, reported the day as complete. **The session that named
the failure mode walked into it.** The mechanism is that the closing pipeline (`run_day7_close.sh`)
does check for a completed file and refuse without one — but it is a *post-run* step, and nothing
checked the run before the minutes about it were written.

**The repair, this session.** `window_status.py` computes the state of the window from the ledger
directory — completed runs, partials, intervals — and refuses to describe a day as measured unless
a non-partial run file exists for it. Its output is `window-status-126.json`, and every day count
and interval in this session's record is read from it.

**It found two things in its first run, and one of them was in itself.**

- *In itself.* Its first version counted **run files**, and reported seven — because the two
  complete probes that ran over the same manifest at the same second on 2026-08-16
  (`DOUBLE-PROBE-122.md`) are two files and **one measurement day**. A guard against overstating
  the window overstated the window. Fixed before it was used: runs are grouped by UTC day, the
  first run of a day is the day, and any further complete run of the same day is reported
  separately as an extra pass. It now reports **6 measurement days from 7 completed run files, 1
  extra same-day pass.**
- *In the window.* `consecutive_daily` is **false**, and it would have been false even if day 7 had
  completed: interval 1, from the baseline at 2026-08-11T11:24:06Z to day 2 at 2026-08-12T03:40:28Z,
  is **0.678 days**. That is **not a new erratum** — this arc published it against itself in
  `INCREMENT-2.md` §3a (*"Interval 1 was not a full day … per identifier the exposure ranges from
  0.191 to 0.678 days"*), and the guard reproducing a deviation the practice had already found is
  the check that the guard works. What is new is the consequence being stated plainly:
  **`preregistered_window_met` is false on both of its conjuncts**, the count and the
  consecutiveness, and it was already false on one of them before day 7 was launched.

**Consequence for the arc.** A run for 2026-08-18 was launched at 03:41:00Z on the day of this
correction. If it completes, the window becomes **seven completed runs across eight calendar days,
with one two-day interval** — not seven consecutive daily runs. The pre-registered design's
"consecutive daily" property is broken and no arithmetic restores it. Any reuse must take the day
count and the interval structure from `window-status-126.json`, not from the pre-registration.

---

## E22 — the persistence figure handed to us was right; the sentence attached to it was not

**Where:** `CONDITIONS-125.md`, finding 7, recording the adversary's finding at the sixth gauntlet.

**What was published:**

> *"412 of the 446 ever-absent identifiers are absent every day they were measured (92 %)"*

**What is true** (`persistence-126.json`, computed by `persistence_126.py` from
`deliverable-v0.3/series/presence-series.csv`):

| Reading | Count | of 446 |
|---|---|---|
| Absent on **all six days** (an `INDETERMINATE` day breaks the run) | **412** | 92.3767 % |
| Absent on **every day it was measured** (`INDETERMINATE` days excluded) | **439** | 98.4305 % |

The panel size (3,620 non-control identifiers), the ever-absent count (446) and the count of units
showing more than one determinate state (7) all reproduce exactly. **The 412 is correct and its
label is not:** 412 is the count under *absent on all six days*, and the sentence attached to it
says *absent every day they were measured* — which is 439. The 34-unit gap reconciles exactly: 27
units whose only non-absent readings are `INDETERMINATE`, plus the 7 that genuinely showed both
states (`reconciliation_holds: true` in the same file).

**Why the distinction is not pedantry.** This arc established at session 115 that indeterminacy is
a property of the request, not of the video, and it excludes `INDETERMINATE` readings from every
rate it publishes. Under that rule a day on which a unit read `INDETERMINATE` is a day the unit was
not measured — so the phrase *"every day they were measured"* names the 439, and using it for the
412 imports the opposite convention into a single sentence.

**Disposition: both numbers are published, each with the definition that produces it**
(`deliverable-v0.3/FIGURES.md`, the persistence section, generated from the same file). The
stricter figure is the conservative one and is the one to quote if only one is quoted. The
correction is recorded here because the finding was a gain handed to this practice by its
adversary, and accepting a gain without checking it is how the last six failures happened.

---

## E23 — the freeze says "nothing was edited under the reviewers". It cannot see what appears.

**Where:** the freeze discipline itself, as stated in `CONDITIONS-125.md` (*"30 of 30 unchanged, 0
modified"*) and again in this session's own record (*"32 of 32 unchanged"*). Found by this
practice's own hand, **after both verdicts of the seventh gauntlet**, while reproducing a Verifier
finding.

**What was published:** that the bundle was frozen before dispatch, re-verified after the verdicts,
and that **nothing was edited under the reviewers**.

**What is true.** Every one of those statements about the *listed* files is correct and reproduces:
32 of 32 hashes in `FROZEN-126.sha256` match. But at **03:52Z, while the reviewers were working**,
two files appeared inside the frozen directory:

    deliverable-v0.3/tools/__pycache__/ledger.cpython-311.pyc
    deliverable-v0.3/tools/__pycache__/run_lock.cpython-311.pyc

They are compiled bytecode, written by the interpreter as a side effect of a reviewer importing the
bundle's own modules — which is exactly what a reviewer is supposed to do. **The freeze covers 32
files; 34 are now on disk.**

**The correction is narrow and it is a correction of a claim, not of a measurement.** "Nothing was
edited under the reviewers" is true. "The directory the reviewers read is the directory that was
frozen" is **false**, and the practice has been treating the first sentence as though it entailed
the second. A hash manifest is a statement about **contents**; it is blind by construction to
**membership**. Two sessions have now made this the strongest procedural claim in their record.

**What does not change.** No figure, no rate, no verdict, no reviewer finding. The added files are
inert, derived from files that are themselves unchanged, and no reviewed file moved.

**Not repaired tonight, deliberately.** The obvious fix — have the freeze record membership as well
as contents, and re-verify both — is the eighth guard, and `CONDITIONS-126.md` declines to build it
on the same reasoning that fires the hard stop. It is carried as a requirement of the object that
replaces the bundle, where the freeze will be over a much smaller thing.
