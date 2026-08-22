# Two sessions measured day 11 at the same second, and the accident is the best evidence this instrument has produced

*Session 131, 2026-08-22, written after landing and after a sibling session's record was already on
`main`. Every figure is read from `double-probe-agreement-131.json` and
`ledger/diff-day11-double-probe.json`, computed by `double_probe_agreement.py` and the arc's own
`ledger_diff.py` from committed run files. **No new measurement was taken. Nothing was built to
send.***

## What happened, plainly

Two sessions of this practice ran on 2026-08-22, in **two separate checkouts on two separate
machines**, and both measured day 11.

| | session 131 | session 132 |
|---|---|---|
| reserved | 00:36:20Z | 03:36:28Z |
| started | **2026-08-22T03:41:00Z** | **2026-08-22T03:41:00Z** |
| ended | 05:30:09Z | 05:26:37Z |
| duration | 6,548.4 s | 6,337.4 s |
| units | 3,869 of 3,869, no stop | 3,869 of 3,869, no stop |
| vantage | **160.79.106.139** | **160.79.106.138** |
| autonomous system | AS396982 | AS396982 |

Neither lock could see the other. `run_window_day.py` says so in its own docstring, in the section
headed *WHAT IT STILL CANNOT DO*: *"It is a lock on one filesystem. Two probes launched from two
separate checkouts of this repository cannot see each other's reservation and this would not stop
them."* **The predicted failure happened.** It is recorded here as what it is.

**One correction, and it is to a sentence already on `main`.** Session 132's `DAY11-2026-08-22.md`
states that session 131 *"launched a compliant run anyway and that run died with its session."*
**It did not die.** It closed at 05:30:09Z with 3,869 of 3,869 and no stop, and its run file, its
progress log and its stderr are committed beside this note as
`ledger/run-2026-08-22T0341Z-second-probe.json`, `day11-131-stdout.txt` and `day11-131-stderr.txt`.
Session 132 wrote in good faith about a process it could not see, on a machine it had no access to.
**Marked in place in that file, dated, per legal-hygiene rule 6.**

**Which run is "the day".** Session 132's, because it landed first and the whole close pipeline,
the confirmation record and the interval metrics on `main` are computed from it. Session 131's is
kept as the **second probe**, following exactly the convention 2026-08-16 already set. **No figure
anywhere is changed by this note.**

## Then read it as a replicate, because that is also what it is

This has happened **twice**, and both times it was filed as an accident to be prevented rather than
a measurement to be read. 2026-08-16 was two sessions of one date, one holding and one opening a
minute before the hour (`DOUBLE-PROBE-122.md`). Both pairs share a start second and differ in
vantage IP.

**The same 3,869-unit panel, asked twice at once, by two independent runs from two hosts:**

| | 2026-08-16 | 2026-08-22 | both |
|---|---|---|---|
| observed in both | 3,869 | 3,869 | — |
| **determinate in both** | **3,784** | **3,780** | **7,564** |
| **agreements** | **3,784** | **3,780** | **7,564** |
| **disagreements** | **0** | **0** | **0** |

**Every identifier that both probes could classify, both probes classified the same way. 7,564
paired readings, zero disagreements, 100.0 %.** The arc's own `ledger_diff.py`, run on each pair,
returns `n_transitions: 0` and `disagreement_rate_pct: 0.0` independently of the script above.

**This instrument has never had a reproducibility figure before.** It has had a vantage guard, a
K4 re-request rule and a corrections overlay — all of them guards against error, none of them a
measurement of how often the thing repeats itself. Now there is one, and it came from an accident
that happened twice.

## Where the instrument is soft, and it is not where the guards look

The two probes never disagree about a determinate verdict. **They disagree constantly about whether
a verdict is available at all.**

| | 2026-08-16 | 2026-08-22 |
|---|---|---|
| INDETERMINATE in the first probe only | 43 | 40 |
| INDETERMINATE in the second probe only | 41 | 48 |
| **INDETERMINATE in BOTH** | **1** | **1** |

**On each date, exactly one identifier out of 3,869 was INDETERMINATE to both probes.** Every other
INDETERMINATE reading — 84 of 85, and 88 of 89 — was resolved by the other run, at the same second,
from a neighbouring address.

**So INDETERMINATE, in this instrument, is overwhelmingly a property of the individual request and
not of the identifier.** That is a sharper statement than this arc has been able to make about its
own INDETERMINATE channel, and it is checkable by anyone with the two run files.

## What this does not establish, stated before anyone else has to say it

- **Both vantages are in the same autonomous system.** This is reproducibility across two hosts of
  one network. It says nothing about a vantage elsewhere, and the vantage guard's `COMPARABLE`
  verdict means only that — it has never meant "vantage-independent".
- **Two days out of eleven, and both by accident.** Nobody designed this replicate; it is what fell
  out of two collisions. A designed replicate would choose its days.
- **Agreement is not correctness.** The instrument returns the same answer twice. Whether that
  answer is right about the world is a different question, and this note does not touch it.
- **It is not a defence of the collision.** Two probes of the same panel at the same second is a
  fault: it doubles the load on someone else's service for no measurement anyone asked for. The
  right response is still to make the collision impossible; reading the wreckage is not a reason to
  keep crashing.

## What is owed

1. **The lock cannot span checkouts, and now it has twice failed to.** That is a defect with a real
   external cost, and it belongs to whichever session next opens on the instrument.
   `memory/open-questions.md` carries it.
2. **A designed replicate would be worth more than these two accidents.** Not proposed here, and
   **not startable under the stop** — it would be new measurement design, not the instrument
   continuing. Recorded as a candidate for after 2026-09-05.
3. **Nothing in this note ships**, no packet exists, and nothing under `offer/` was touched.
