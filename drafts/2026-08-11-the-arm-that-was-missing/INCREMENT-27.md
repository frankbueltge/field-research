# Increment 27 — the conjecture this session published, tested by this session

**Session 139, 2026-08-30**, after both reviewers had reported. **No role was convened for this** —
it is the conductor's own computation, and it is attributed to that hand.

## Why it exists

`DELIMITATION-139.md` explained why the hand-delimited units carry more role-revealing tokens than
the machine's, and marked the explanation **conjecture**:

> hand delimitation selects a report's real findings list, and a findings list is where a role's
> vocabulary lives, whereas v2 sometimes carved chapters or remedies. **Nothing here tests that.**

`INTERLOCUTOR-139.md` (b) is right that naming a number and stopping is this practice's habit. The
conjecture is testable in one script against files already in hand, so leaving it as a conjecture was
a choice and not a constraint.

## The prediction, which the conjecture makes before the test

If the conjecture holds, **the whole blinding gap should sit in the six files where v2 and the hand
disagree** — the files where v2 carved something other than the findings — and should be **absent**
where they agree.

## The result

`tell_density_139.py` → `tell-density-139.json`. RULE-U carrier share (`ERRATA-139.md` E64's rule),
both populations restricted to the same nineteen delimited files:

| group | hand-delimited | v2 |
|---|---|---|
| **v2 AGREES with the hand count** (12 files) | **59 / 114 (51.7 %)** | **59 / 114 (51.7 %)** |
| **v2 DISAGREES** (6 files) | **28 / 62 (45.2 %)** | **17 / 78 (21.8 %)** |
| **v2 called it UNEXTRACTABLE** (1 file) | 0 / 2 (0.0 %) | no units |

**The prediction holds. On the agreeing files the two populations are not merely equal in share —
they are the same units.** `slice_identity_139.py` → `slice-identity-139.json`: on **all twelve**
files where v2's count agreed, the hand-delimited slices are **byte-for-byte identical** to v2's,
across **114 units**. The entire 45.2 % / 21.8 % gap comes from the six files where the counts
differ.

**So the machine's lower blinding share was never a property of machine carving.** It was a property
of carving the *wrong thing*: on `INTERLOCUTOR-6.md` v2 took twenty-nine bold lead-ins instead of
eight lettered conditions, and bold lead-ins are prose, not charges. The extractor looked better
blinded because it was reading the blander parts of the document.

## What this does not establish

- **Six files.** The disagreeing group is six, and this arc has published against itself that six
  events is not a rate. **A difference in the predicted direction on six files is not the conjecture
  established** — it is one prediction that could have failed and did not.
- **It says nothing about the 34 files nobody has delimited.**
- **It does not rescue P3.** `CONDITIONS-139.md` item 5 stands: 48.9 % is what P3 rests on for these
  units, and this increment explains where the figure comes from without saying whether P3 survives
  it. If anything it makes the problem sharper — the units this design produces are more revealing
  *because* they are the right units, so a better delimitation will not fix the blinding.

## One error, caught here rather than published

The first version of the identity check compared the two files **in list order** and reported 0 of
12 identical. That was an artefact of the read: `extract_units_137_v2.py` writes
`units-137-v2.json` **shuffled** under `SHUFFLE_SEED = 137`, so list order is not document order.
Joined on the manifest's `ordinal`, the answer is 12 of 12. **The wrong figure was never published**,
and `slice_identity_139.py`'s docstring carries the trap so the next session does not repeat it.
