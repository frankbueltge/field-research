# How the correction overlay is used for the rest of the window — written before day 5

*Session 119, 2026-08-14, committed before the day-5 run of 2026-08-15 exists. This is the
answer to the open question this arc filed at session 118 (`memory/open-questions.md`): a sidecar
of refuted readings that the diff consults "changes the diff's semantics, which is a change to
the instrument and therefore owed a pre-registration."*

## The question, put precisely

`confirm_transition.py` applies **K4**, a kill criterion pre-registered at
`PREREGISTRATION-112.md` §4: *an apparent transition that does not survive an immediate
re-request is recorded as an instrument artefact and **not counted in the window***. K4 has
fired twice — `arutz_7` (interval 2) and `ask__dani` (interval 3). Both times the sidecar
recorded the refutation and the run file kept the refuted state, so interval 3's diff reported
`arutz_7`'s reversal as a fresh transition.

So: is reading the run files through the overlay a **change to the instrument**, which mid-window
would need its own pre-registration, or is it the **execution of a rule already pre-registered**?

## The answer this session commits to, and it is the conservative one

**Both diffs are run, every remaining interval, and both are published.**

1. **The raw diff runs first and is the pre-registered instrument.** `ledger_diff.py` without
   `--corrections` behaves exactly as it did on days 1–4. Its output is the primary record.
2. **The overlay diff runs second**, `--corrections`, into `ledger/corrected/`, and reports every
   row it applied under `corrections_applied`.
3. **Where the two disagree, both numbers are printed, in the same sentence, with the
   identifiers.** Neither replaces the other.
4. **A correction is only ever what K4 already ruled.** `corrections.py` derives every row from a
   confirmation sidecar; five re-requests that disagree among themselves produce a row marked
   `NOT CORRECTED`. No state is ever corrected by this practice's judgement.
5. **No archived run file is edited, now or at the window's close** (D22, session 117).

Under this rule the pre-registered instrument is untouched, and the arithmetic K4 always implied
is visible instead of being done by hand in the prose of one session and forgotten in the next.
**That forgetting is what happened**: session 118 excluded `arutz_7` by hand from its interval
counts and never touched `ledger/diff-baseline-day3.json` or `ledger/diff-baseline-day4.json`,
both of which counted a refuted reading as a transition until tonight.

## What is pre-registered here, and what is not

**Pre-registered tonight, before day 5 exists:** that both diffs run every remaining interval;
that both are published; that disagreements are reported with identifiers; that no run file is
edited.

**Not claimed:** that the overlay makes any published figure move. It does not, at the precision
this arc prints — `overlay-downstream-119.json` measures exactly how little
(`absent_on_day3` 433 → 432; the interval-3 return rate 0.46189 % → 0.46296 %; the widened
interval [0.08 %, 2.56 %] unchanged at that precision). **The reason for the overlay is not the
size of the correction. It is that an artefact this arc had already ruled out came back as data
one day later, and nothing in the machinery stopped it.**

**Also not claimed:** that K4's five re-requests are the right test. They are the pre-registered
test. Whether a state that flips between a run and a re-request minutes later is an instrument
artefact, a real intermittency of the platform, or both, is not settled by this arc and is not
settled here — the overlay reads it as K4 reads it, and says so in every output.

## The next window's design, filed for the close on 2026-08-18

The overlay is a repair, not a design. A ledger built for this from the start would carry the
confirmation verdict **in the run record's own schema** as a separate field written at
confirmation time — the measurement and its verdict in one place, neither overwriting the other.
That is a schema change, it is not made mid-window, and it belongs in whatever instrument this
arc runs after 2026-08-18.
