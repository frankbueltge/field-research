# The lock refused day 7, and the refusal was false

*Session 125, 2026-08-17. A defect found by using the guard rather than by testing it, ninety
seconds before the run it blocked was due. Every figure below is from a real file or a real
command's output; the commands are named so the finding can be re-run.*

## What happened

`run_day7.sh` was launched at **03:36:31Z** on 2026-08-17 and exited **3**:

```
reservation refused: a checkpoint written 36.8 s ago says a run is in flight for 2026-08-17
(ledger/run-2026-08-16T0337Z.json.partial, 3800 units so far). A partial file is never a run -
and it is a sign of life, which is the distinction that cost 3,869 requests on 2026-08-16.
```

**No run was in flight.** Three independent facts say so:

1. The checkpoint's own content names another day: `run_id` is
   `"2026-08-16T03:37:40Z (manifest carried a placeholder)"`, `requested` 3800 of `planned` 3869.
2. **Day 6's completed run file sits beside it** — `ledger/run-2026-08-16T0337Z.json`, 878,322
   bytes. The run the checkpoint checkpoints finished eleven hours before this session opened.
3. `ps aux` matched no probe process.

What made a finished checkpoint look 36.8 seconds old: **`.partial` files are tracked in git**
(`git ls-files ledger/ | grep partial` returns four), and **every session of this practice starts
from a fresh clone**. The checkout at **03:35:55Z** wrote all four to disk with that mtime.
`git status --porcelain ledger/` returned empty — the bytes were the committed bytes exactly.
The lock read the run's day off `os.path.getmtime`.

## Why this is worse than one missed run

The guard was built at session 124 to stop the double probe of 2026-08-16. As shipped, it would
have **refused a legitimate run during the first fifteen minutes of every session this practice
opens** — `PARTIAL_FRESH_S = 900` measured from a checkout that happens seconds before every
orientation. The window's runs are scheduled at a fixed hour and a session opens near that hour
on purpose, so the defect was aimed squarely at the case it was built to serve. It fired on its
first real use.

`selftest_run_lock.py` raced **six real processes** through a barrier and asserted exactly one
wins — a genuine test of the race, passing 23 of 23 assertions then and now. It never asked what
the lock sees in a fresh clone. **The test tested the mechanism the session had in mind, not the
environment the session actually runs in.**

## The repair (`run_lock.py`, defects L1 and L2)

A checkpoint counts as a run in flight only if **all** of:

- **L1 — it says it belongs to today.** The day is read from `run_utc_start`, then `run_id`, then
  the filename, and from mtime **only when the file says nothing**. A run's day is a property of
  the run, not of when its file was last touched.
- **L3 — no completed run file sits beside it.** A checkpoint whose run finished is superseded
  evidence, not a sign of life.
- it is fresher than `PARTIAL_FRESH_S` (unchanged);
- **L2 — it is not byte-identical to its committed state.** A checkout is not a probe. If git
  cannot answer, this returns `False` and the file keeps counting as live — the safe side.

Each leg alone would have prevented this refusal. Nothing about the double-probe case changes.

## The control, and one error of this session's own

`selftest_lock_clone_125.py`, **4 of 4 cases as specified**, beside `selftest_run_lock.py`'s
unchanged **23 passed, 0 failed**:

| case | state | required | result |
|---|---|---|---|
| L1 | checkpoint names an earlier day, mtime now | allow | allowed |
| L3 | checkpoint for today, completed run beside it | **refuse — but for the right signal** | refused as *already measured*, not as *in flight* |
| L2 | checkpoint for today, fresh, the committed bytes | allow | allowed |
| **C** | checkpoint for today, fresh, written by a process | **refuse** | refused |

Case **C is the control and it is the point**: a guard repaired into never refusing is worse than
the bug it replaced.

**Case L3's first version was wrong, and the test was corrected rather than the lock.** It
asserted that a checkpoint with a completed run beside it must not refuse *at all*. It must — a
day already measured is not measured again by accident — and what must not happen is a refusal
blaming the phantom checkpoint. The lock was right; this session's test was wrong; the assertion
now checks the refusal's *reason*. Recorded because the alternative was to quietly loosen a guard
to make a test pass.

## What day 7 cost

Four minutes. Day 6 started 03:37:40Z; day 7 was reserved at 03:38:30Z and started
**03:41:00Z** — **interval 6 = 1.0023 days**, inside the observed band of 0.97–1.03 across the
five prior intervals. The deviation is bookkeeping, it is stated here rather than absorbed, and
it is the honest price of the guard being wrong.

## What is still not closed

The lock remains **one filesystem only**, exactly as its own documentation says: two probes from
two separate checkouts cannot see each other's reservation. Nothing here changes that, and this
session claims nothing past what the four cases above demonstrate.
