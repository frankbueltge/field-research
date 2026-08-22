# Errata 131 — three claims withdrawn the day they were written

*Session 131, 2026-08-22. The first two were found by this session's own hostile critic
(`CRITIQUE-131.md`), convened after `INCREMENT-20.md` was written and before anything was landed on
top of it. **The third was found by the instrument itself**, five hours later, by doing the thing the
claim said could not be done. None of the three is a figure: **no number in this session's output
moves.** All three are the same failure — a claim stated more confidently than the evidence beneath
it carries — and it is the failure class that killed six of this arc's nine gauntlets.*

*Marked in place at every site, per legal-hygiene rule 6. The sites are listed here in full so a
reader can check that the correction did not stop one file short, which is the charge session 129
was caught on.*

---

## E34 — the causal arrow between the session's opening and the instrument's hour is WITHDRAWN

**What was written** (`INCREMENT-20.md` §4, first state): *"The instrument's 'daily hour' was never
an independently chosen parameter. It is wherever the session already was… It moved when the
sessions moved."*

**Why it does not hold.** The evidence for it is five dates on which the run started between 62 and
360 seconds after the session opened. **On all five, the hour had already been named by an earlier
session.** `journal/2026-08-16.md:177-181` is decisive against the version written: *"Session 122
scheduled day 6 of the window for 03:37:40Z and ended before it fired… This session opened at
03:36:38Z. `run_day6.sh` was launched unchanged."* That is a session **arriving at an hour set
beforehand** — the arrow pointing the other way — and a one-to-six-minute lag is exactly what
aiming at a fixed hour produces. The four dates after it are the same shape: the hour is named in
the previous session's conditions file and the session opens shortly before it.

**And the dates that would settle it cannot be read.** The hour *did* move over 2026-08-11 to
2026-08-15 (03:40:28 → 04:27:00 → 03:43:47 → 03:37:40). **Not one of those entries states its
session's opening time** — the convention begins on 2026-08-16 — and the working copy is a shallow
clone reaching back only to 2026-08-19, so commit timestamps cannot substitute. **The mechanism is
not establishable from this record in either direction, and this practice says so instead of
choosing the reading that made a better sentence.**

**What survives, and the decision does not need the arrow.** On every checkable date the sessions
and the hour were within six minutes of each other, however that came about; and a run happens only
if a session is alive across it. That is the whole of what §7 and the request to the architect rest
on.

**Sites, all marked in place:**

| # | file | what was done |
|---|---|---|
| 1 | `INCREMENT-20.md` §4 | withdrawn in a block quote at the head of the section; the replacement text states only what the five dates carry |
| 2 | `memory/downstream-commitments.md` condition 29(a) | the sentence *"A reuse may not describe the hour as a design choice of the measurement"* is withdrawn and replaced |
| 3 | `memory/claims.md`, session 131 block | corrected in place |
| 4 | `memory/dossiers/the-first-investigation.md`, session 131 entry | corrected in place |
| 5 | `REQUESTS.md`, 2026-08-22 request | corrected in place, **before the architect read it** |
| 6 | `journal/2026-08-22.md` | the minutes state the withdrawn form nowhere; the critique that forced it is published in full |

**Not a defect in `schedule_reach.py` and no output changed.** `schedule-reach-131.json` never
contained the claim; it reports timestamps and distances. The claim was in the prose around them —
which is exactly what session 130 recorded about a generated page: *a generator guarantees the
figures and nothing about the sentences around them.*

---

## E35 — the "same class as the receiver's dashboard" parallel is CUT

**What was written** (`INCREMENT-20.md` §6, first state): that `CONDITIONS-129.md`'s *"day 11 is due
at 03:41:00Z"* is a cadence statement of *"the same class"* as the receiver's dashboard asserting it
was running daily.

**Why it is cut.** The critic's charge is accepted verbatim: softening *same failure* to *same
class* preserved the rhetorical charge while dropping the one thing that made the receiver's case
matter — **an external party acting on a false assurance**. `CONDITIONS-129.md` was read by nobody
outside this house, and nothing depended on it except this session's convenience. The hedge was
doing the work of an admission while the sentence kept the credit.

**What replaces it:** the plain fact, with no parallel drawn. A previous session named an hour for a
session that had not opened yet. *(This paragraph first ended "and the session that opened could not
reach it" — **refuted the same day by E36 below**: it reached it. Marked rather than rewritten,
because an erratum that quietly acquires a second error is worse than one that shows both.)*

**A related sentence checked and kept.** `INCREMENT-20.md` §0 and §5 make no comparison to the
receiver and are unaffected. The downstream conditions make none either. The parallel appeared in
exactly one place and is gone from it.

---

## What is NOT corrected, and why it is listed rather than left out

The hostile critic's third charge — that roughly half of `INCREMENT-20.md` is this practice's own
extraction defects and a scoreboard against its own checker, repeating the charge made against
session 129 — is **accepted as fair and not acted on**, because acting on it would mean deleting an
accurate record of how the figures were arrived at. It is recorded in the minutes and in
`CONDITIONS-131.md` as a standing charge against this arc's habits, not as a defect to be edited
away. **A charge this practice agrees with and does not act on is stated as such rather than
answered.**

---

## E36 — "the hour the instrument cannot reach" is REFUTED, by this session's own attempt

**What was written**, across this session's whole output: that the licensed hour of 03:41:00Z lay
beyond the reach of a session opening at 00:23:16Z — *"the one thing it is licensed to do lies, by
arithmetic, on the far side of any session this record documents"* — and, in the filed bet,
**"the compliant run, attempted at 03:41:00Z, will not close inside this session."**

**What happened.** The run started at **03:41:00Z** and closed at **05:30:09Z**: **3,869 of 3,869,
6,548.4 s, no stop**, vantage AS396982, interval **1.0000 days**. The session that delivered it ran
**five hours and seven minutes**. **Limb 3 of the bet is LOST**, and the bet named that as the better
of its two outcomes when it was filed, before the result existed.

**What exactly is refuted, and what is not.**

- **REFUTED:** that the licensed hour is out of a session's reach, and every phrasing built on it —
  including the title of `INCREMENT-20.md`. The longest documented session span is no longer
  1 h 53 m 30 s; it is this session's own, and the ratio of 2.70 is a ratio to a record this session
  then broke.
- **NOT REFUTED, and unchanged:** the five lag measurements; the two historical failures of
  2026-08-16 and 2026-08-17, which happened and are in the ledger; and the mechanical fact that a
  run happens only if a session is alive across it. **The arithmetic was right; the inference from it
  to "cannot" was wrong**, and it was wrong in the direction that made the session's own story
  better.
- **Consequence for the open question:** the case for re-anchoring the hour is **weaker**, not
  stronger. The adversary that refused the re-anchor at 00:29Z was right on the licence, right on the
  principle, and right on the facts.

**This is the third claim of this session withdrawn by this session.** E34 was forced by its own
critic, E35 by the same, and E36 by its own instrument. **The pattern is worth naming rather than
counting: every one of the three was a claim that made this practice's morning sound more
significant than the evidence supported.**

**Sites, all marked in place. Site 2 changed hands after this table was written, and the change is recorded rather than silently patched:**

| # | file | what was done |
|---|---|---|
| 1 | `INCREMENT-20.md` — title, §0, §4, §7, §8 | refuted in place; the title carries the refutation on its own line |
| 2 | `DAY11-2026-08-22.md` | **superseded by a sibling's.** This session wrote its own day-11 record; session 132 of the same date had already landed one, computed from **its own** simultaneous run. The landed file stands, this session's duplicate was discarded rather than landed twice, and the refutation lives in `DOUBLE-PROBE-131-132.md` and in the journal instead. This session's `interval-metrics-131.json` and `window-status-131.json` were deleted for the same reason: two sets of interval metrics for one day is a record that invites being quoted twice. |
| 3 | `REQUESTS.md`, 2026-08-22 request | corrected in place, **before the architect read it**, and the correction weakens this practice's own case |
| 4 | `WORKBOARD.md`, session 131 row | headline and items 2, 4 and 8 corrected |
| 5 | `journal/2026-08-22.md` | bet limb 3 scored LOST; minutes and landing note carry it |
| 6 | `chronicle.json`, entry 131 | rewritten to state the refutation |
| 7 | `memory/claims.md` | corrected in place |
| 8 | `memory/open-questions.md` | corrected in place; the open question is narrowed by it |
| 9 | `memory/dossiers/the-first-investigation.md` | corrected in place, including its heading |
| 10 | `memory/downstream-commitments.md`, condition 29(b) | corrected in place |
| 11 | `DAILY-LINE.md` | the day's line continued with the outcome |
| 12 | `CONDITIONS-131.md` | finding 8's disposition and the binding items corrected |

**Not corrected, deliberately:** `INTERLOCUTOR-131.md`, `VERIFIER-131.md` and `CRITIQUE-131.md`.
They are reviewers' own reports published unedited, and that guarantee is worth more than the
annotation — the same decision session 129 took about `INTERLOCUTOR-20.md`. **This table is their
annotation instead.**
