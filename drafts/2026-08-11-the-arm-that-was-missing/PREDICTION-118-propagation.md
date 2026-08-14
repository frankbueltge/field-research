# Prediction 118 — lagged propagation, written while the day-4 run is still in flight

**Committed 2026-08-14, before any day-4 result was read.** The window run started at
**03:43Z** and is still probing as this file is written; no observation from it has been opened,
no diff has been computed, and this file is committed while the run is unfinished so the order is
checkable in the git history rather than asserted.

## What makes the prediction possible tonight and was impossible before

The account-state probe of `PREREGISTRATION-117B-account-state.md` ran first this session
(102 requests, `account-state-117b.json`). Cross it against the day-3 ledger and **five accounts
are in a non-zero state while every one of their cited units was RETRIEVABLE on day 3**:

| group | handle | state | unit retrievable on day 3 |
|---|---|---|---|
| T | `bruno_martiinez` | 10221 | `7234121532635761926` |
| T | `monicaaquino191` | 10221 | `7230168662945189126` |
| T | `payo_junior_oficial` | 10221 | `7228741383975095558` |
| C2 | `sbsaustralia` | 10221 | `7193104172198202625` |
| C2 | `lazpiyanist` | 10221 | `7251623512144743686` |

**Five accounts, five units.** These are the whole population of the prediction — no sampling,
no seed, every such unit in the 102-account probe is listed.

## The prediction

**P118-1: fewer than three of these five units turn NOT-RETRIEVABLE on day 4** — i.e.
same-interval propagation from account-unavailability to video-unavailability stays refuted.

Session 115 refuted it on `grimhoundgaming`: account state non-zero at ~23:45Z on 2026-08-12,
and **0 of its 7 cited videos turned** on day 3. That was *n* = 1 account and one handle chosen
for being informative. This is five accounts, two of them outside the flagged article entirely,
selected by a rule fixed before the day-4 run was read.

**It fails if three or more turn.** That would make the two interfaces agree with a lag of about
a day, and it would mean the account route sees losses the video route has not yet reported —
which would be a finding about the instrument, not about the platform.

**What it cannot settle.** Five units cannot estimate a propagation *rate*: if zero turn, the
95 % upper bound on the per-interval propagation probability is roughly 45 %, and a lag longer
than one interval is untouched. The window runs three more days after this one and the same five
units are measured every day without any new request, so a longer lag remains observable.

## What is not claimed

This prediction is not part of `PREREGISTRATION-117B-account-state.md` and adds nothing to it;
that document's five predictions and four kill criteria are scored exactly as written. Nothing
here reclassifies any ledger unit, and the five units are measured by the window instrument
unchanged, as part of the 3,869 the manifest already carried.
