# Addendum — what day 14 did to the figures two reviewers passed on

**Session 136, 2026-08-26, written at 05:30Z. This is a dated event, not a patch.**

`PROTOCOL.md`: *"The verdict is only good for the exact state it was run on."* The Verifier and the
Interlocutor read `CONCEPT.md` on data that ended at **day 13 (2026-08-25)**. Day 14 closed at
**05:21:05Z**, after both reports were in. **Nothing in `CONCEPT.md` or `GATE-DECISION-136.md` has
been altered to match it.** Their figures stay pinned to the state that was actually reviewed, and
this file records what moved.

**The gate's failure is unaffected.** K-C fired on the receiver evidence, which day 14 does not
touch.

---

## What moved

| figure | as reviewed, through day 13 | with day 14 | direction |
|---|---|---|---|
| absent share, that day | **374 of 3,134 — 11.93 %**, [10.62, 13.34] | **384 of 3,147 — 12.20 %**, [10.88, 13.62] | +0.27 pp |
| pages carrying ≥1 absent citation | **467** of 3,249 | **476** of 3,249 | +9 |
| measurement days on one fixed corpus | **12** | **13** | +1 |
| **range of the absent share across them** | **11.83 %–12.14 %, 0.31 pp** | **11.83 %–12.20 %, 0.38 pp** | wider by 0.07 pp |
| raw day-to-day changes | **1,1,4,2,0,4,1,4,2,0,3,2 — 24** over 12 intervals | **+3 — 27** over 13 intervals | +3 |
| encyclopedia arms, raw apparent disappearances refuted | **5 of 15** | **7 of 18** | — |
| **refuted share of all raw readings, both directions** | **5 of 24 — 20.8 %** | **7 of 27 — 25.9 %** | +5.1 pp |
| article space only | 260 of 2,376 — 10.94 % | **267 of 2,387 — 11.19 %** | +0.25 pp |

Computed by re-running `edition_breakdown.py`, `series_stability.py` and `confirmation_by_arm.py`
against day 14's run file. The day-13 artifacts are untouched; day 14's are beside them
(`edition-breakdown-day14.json`, and the two series files rebuilt).

## What it means, stated narrowly

**The stock claim holds and is now thirteen nights old.** The absent share has not left a band of
**0.38 pp** across thirteen measurement days on one corpus. That is the half of the concept's claim
the adversary said it could not move, and a fourteenth day did not move it either.

**The flow claim moves toward the concept and still does not reach the word it originally used.**
The first version said the flow is *"substantially its own noise"* and *"mostly their instrument"*;
the adversary refuted that at 5 of 24 (20.8 %) and the concept was corrected to *"one in five"*. Day
14 takes it to **7 of 27, 25.9 %** — closer to the withdrawn wording, **and still nowhere near
"mostly"**, which means more than half. **The correction stands. A day that moves a figure toward a
retracted claim does not un-retract it.**

**And day 14 is the sharpest single illustration the series has produced.** Three apparent
transitions, all disappearances; **two refuted on five immediate re-requests each; one confirmed**.
A single-pass instrument would have recorded three losses. **That is the concept's verification limb
demonstrated on one night** — and it arrived nine hours after the concept was written, on a day
nobody chose. **It is one day and it is not a rate.** Twenty-seven events are not a rate either, and
`CONDITIONS-132.md` item 5 binds this file as it binds the day records: **no trend is claimed, no
test is scored.**

## What this addendum is not

- **Not a re-gating.** The concept is parked. K-C fired and no arc is licensed.
- **Not a new verdict.** Neither reviewer has seen these numbers. Nothing here has been through a
  gauntlet, and none of it is this practice's VERIFIED status.
- **Not a reason to reopen.** `GATE-DECISION-136.md` §5 names the one measurement that would revive
  the concept, and it is not this one. More nights of the same series do not answer whether an
  unauthenticated fetch of a cited video page reveals the absence — **which is still the question,
  and is still unmade.**
