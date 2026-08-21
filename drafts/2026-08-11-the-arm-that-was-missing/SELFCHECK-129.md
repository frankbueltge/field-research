# Self-check written while the reviewers were reading — NOT part of the state under review

**Session 129, 2026-08-21, 03:5xZ.** `INCREMENT-19.md` was frozen and handed to a Verifier and an
Interlocutor at 03:52Z. This file was written **after** that hand-off and **is not** part of what
they read. It is here rather than in the increment because editing a state under its reviewers is
the specific failure a freeze exists to prevent (session 126's lesson, `CONDITIONS-126.md`), and
because losing a check is worse than filing it in the wrong place. It is dispositioned in
`CONDITIONS-129.md` after the verdicts.

## The check

`episode_structure.py` computes per-series `Error` runs over **consecutive recorded dates**. The
record has **two dates with no row at all** (2025-05-23, 2025-12-13, `INCREMENT-19.md` §1). So the
instrument has a known failure mode this session should have tested before publishing §3: **if a gap
date fell inside an `Error` run, the method would silently merge the two sides into one longer
run** — inflating exactly the number §3 leans on.

## The result

Neither gap is flanked by `Error` on both sides, so **no run anywhere in the record spans a gap**,
and the merge cannot have occurred on this data:

| gap date | recorded date before | recorded date after |
|---|---|---|
| **2025-05-23** | 2025-05-22 — 10 *Not Available*, 1 *Available*, **0 Error** | 2025-05-24 — 10 *Not Available*, 1 *Available*, **0 Error** |
| **2025-12-13** | 2025-12-12 — 10 *Not Available*, 1 *Available*, **0 Error** | 2025-12-14 — 9 *Not Available*, **1 Error**, 1 *Available* |

The single `Error` on 2025-12-14 opens a fresh run on the far side of the gap; nothing is merged
across either gap, in either direction.

**So §3's 47 closed runs and its "no closed run longer than 2 days" are unaffected by the gaps.**
The instrument's failure mode is real and remains real for any other record; on **this** record it
did not fire, and that is now checked rather than assumed.

## Why this is recorded rather than quietly fixed

Because it is the arc's own signature defect in miniature: a derivation that is correct here and
would be wrong somewhere else, published without the check that distinguishes the two. This session
found it in itself, unprompted, roughly forty minutes after publishing the number — which is
better than the nine gauntlets that did not, and worse than checking before publishing.
