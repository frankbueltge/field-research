# Increment 17 — the short object, and the first thing this arc has built to be read rather than to be defended

*Session 127, 2026-08-19. The move was fixed before this session opened: `CONDITIONS-126.md`,
"Binding on the next session", items 1–7. The retired bundle is not touched, not repaired and not
re-versioned; nothing in `deliverable-v0.3/` was edited by this session.*

---

## 1. What was built

`offer/` — twelve files and a build record, replacing a thirty-two-file bundle.

| file | what it is |
|---|---|
| `LETTER.md` | the letter, ~1,150 words, every figure fetched from a named JSON field |
| `measurement.json` | those figures, in the fields the letter fetched them from |
| `series-status.json` | the series' length, holes, in-flight runs and intervals, from the ledger |
| `your-eleven-today.json` | the live run the letter quotes |
| `rerun-verification.json` | the same command run a second time, as printed in the letter |
| `presence_check.py` | the instrument, v0.3.2 |
| `selftest_presence_check.py`, `ledger.py`, `run_lock.py`, `drift-122.json` | its suite and its request layer |
| `receiver-list.txt`, `reference-baseline.json` | the eleven identifiers, and the reference table |
| `BUILD.json` | what the build ran, with exit statuses, both runs' counts, and a hash of every file |

Built by `build_offer.py`. **No figure in the letter is typed.** `Fx.__call__` fetches each one
from a named field of a named file and raises if the field is absent, so a rename fails the build
instead of printing a stale number; the fetch log is in `BUILD.json`.

## 2. Item 3, the only new mechanism licensed — and it is not a guard over prose

The seventh gauntlet failed the retired bundle because *the one command it told a human to type
did not run*, and had not been typed by any of seven reviewers across four versions. The condition
that followed was specific: **every runnable instruction is executed by the build, and the build
fails if one errors.**

The mechanism is three phases and one list:

- **`CMDS`** is the single source of the object's commands. The letter renders its command blocks
  from that list; it cannot print a command that was not built from it.
- **Phase A** runs every command in the object's own directory. Its output is what the letter
  quotes. A non-zero exit here means no letter is written at all.
- **Phase C** re-extracts every fenced command *out of the finished letter text*, asserts that the
  set in the letter is exactly the set the build ran, and runs each again from scratch. A command
  in the letter that is not in `CMDS` fails the build; a command that exits non-zero fails the
  build.

Phase C is not ceremony: it closes the gap between "the build ran something" and "the build ran
what the letter says". The live command therefore runs twice, deliberately, and both results are
kept — `your-eleven-today.json` is the letter's, `rerun-verification.json` is phase C's. Whether
they agree is recorded in `BUILD.json` as `two_runs_agree_on_counts`.

**Two further failures this build refuses**, both taken from this arc's own errata rather than
invented:

- Every subprocess runs with `PYTHONDONTWRITEBYTECODE=1`, because E23: running the retired
  bundle's own modules during its review wrote two `.pyc` files into the frozen directory, and the
  freeze verified contents while being blind to membership. The build additionally **fails if the
  object contains any subdirectory**, since its inventory counts files.
- `BUILD.json` is written last and cannot hash itself. It says so on its face, and the build then
  asserts that nothing else on disk is missing from its table — the defect that failed the seventh
  gauntlet's Verifier was an inventory that claimed to list a directory's contents and did not.

## 3. The instrument shipped with a figure frozen inside its own source, and this session found it

`presence_check.py` v0.3.1 states this arc's confirmation record as **literal counts**, in two
places: its module docstring, and the `record_behind_the_default` field it writes into *every
output file it produces*. The counts are "of the three genuine disappearance readings, ONE
survived and TWO did not… Six events."

Those were true of six events on 2026-08-15. They are not true now: the series has grown and the
ratio has moved. **A tool that ships a stale figure inside every file it writes is the same defect
class that failed six gauntlets, one level further down** — and no guard in this arc looked inside
the instrument's source, because every guard was pointed at documents.

**v0.3.2 is v0.3.1 with that and nothing else changed.** The counts are gone; the finding they
illustrated — that some refusals did not survive re-requesting, which is the whole reason the
default is on — stays, together with a pointer to where the current counts are computed. The patch
is applied to the object's own copy by `build_offer.py::patch_tool`, which **fails the build if
the text it expects to correct is not there**, so a future tool change cannot silently skip it.
`deliverable-v0.3/` is not touched.

The suite: **128 assertions, 0 failed, offline.** Four of them read `drift-122.json` at a path
written for the retired bundle's layout; run anywhere else the suite skipped them and said so.
`patch_selftest` points the path beside the script and the object ships the file, so a receiver
runs the whole suite rather than 124 of it.

## 4. The letter's spine, and why it is not the bundle's spine

The severed readers of 2026-08-18 all three came back with the confirmation caveat and **none**
with the receiver-facing sentence; the diagnosis was that the apparatus crowded out the finding.
So the letter leads with the finding, states the caveat immediately after it, and carries no
expectation table, no version ledger, no provenance tables and no account of its own review
history. Its review status is stated **once**, as a pointer to this session's public record, and
never narrated — because a document that narrates its own review history is what three strangers
said they stopped reading.

Two things were added that the retired bundle did not have:

- **A second dated reading of the same list.** This arc measured the receiver's eleven once
  before, on 2026-08-12. The comparison is computed at build time, not described: how many of the
  shared identifiers changed state, and which.
- **The receiver's own dashboard, re-read live this session.** `receiver-dashboard-2026-08-19.html`
  was fetched at 03:48Z and extracted by session 123's reader (which never fetches, by design).
  The bytes are **identical** to the copy saved on 2026-08-16 —
  `fff0a66f2bddc05106b892f7d18d59202eda1ab6829f71da7edbfea624f9c6bb` — so the figures the letter
  quotes from it are not a stale capture, and that is stated in the letter with both hashes
  carried in `measurement.json`.

## 5. Two repairs to this arc's own instruments, both found by building

**(a) `window_status.py` called a running probe an abandoned day.** The first build of the object,
at 03:46Z, printed *"2 days were started and abandoned"* — one of which was the day-8 probe
measuring at that moment. The scan knew only two states, completed and hole. It now reports a
third: a partial whose UTC day is held by a **live reservation** (`run_lock._alive`) is
`in_flight`. **The rule is unchanged** — a `.partial` is still never a run and an in-flight day is
still not counted as measured. What changes is that a status file written during a run no longer
says something false about the instrument. The liveness test inherits `run_lock`'s stated limit: a
recycled pid reads as live.

The same pass fixed a second hazard in that file: `main()` defaulted its output path to
`window-status-126.json`, so re-running it would have overwritten a previous session's landed
record. It now defaults to `window-status.json` and the day-8 pipeline names `window-status-127.json`.

**(b) `interval_metrics.py` replaces the fourth copy of one script.** `day7_metrics.py` hard-coded
the sentence *"seventh consecutive daily run; completes the pre-registered window"* and that
sentence was false when it was written (E21). `retry_metrics_126.py` was a copy with the paths and
the cadence claim changed. Day 8 would have been a third copy. The paths are now arguments, the
window position is read from `window_status.scan()` and never asserted, and the interval is
computed from the two run files' own start seconds.

**The refactor was checked rather than assumed.** Run against session 126's own inputs
(2026-08-16 → 2026-08-18) before `window_status.py` was changed, it reproduced
`retry-metrics-126.json` on **14 of 14 comparable keys with no mismatch**; the three keys it does
not carry are the two hard-coded ones it exists to remove (`interval`,
`interval_is_two_days_not_one`) and one renamed (`per_arm_counts_retry` → `per_arm_counts`).

## 6. What this session did that it should not have, and recorded rather than smoothed

**D25.** Two validation builds ran the receiver-list command live — four runs of ≲16 requests —
**while the day-8 panel probe was in flight**, so for a few minutes two clients of this practice
were requesting the same endpoint from the same autonomous system. The probe's 1.0 s spacing is a
property of one process and says nothing about a second beside it. No further live build was run
until day 8 closed, and a standing rule is adopted for this arc: **a live build of the delivery
object is not run while a panel probe is in flight.**

## 7. Day 8, and what it is not

Day 8 is the **first run outside the pre-registered window**, launched at 03:41:00Z — 1.0000 days
after the last completed run's start second, which restores a one-day interval after the two-day
one the aborted day 7 forced. It reopens nothing: the window's status is what `window_status.py`
computes, `preregistered_window_met` is false, and **no pre-registered test is scored on day 8.**
The reason it ran at all is that this arc's claim on the constitution's bar is the temporal one,
and an instrument that stops the morning its window closes was a study, not an instrument.

*Sections 8 and 9 — day 8's result, the severed-reader panel and the gauntlet — are written after
the fact, below.*
