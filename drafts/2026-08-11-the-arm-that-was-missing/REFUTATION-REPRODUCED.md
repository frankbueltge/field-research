# Reproducing the adversary's own tests with our commands, before accepting them

*Session 109, 2026-08-11, after `INTERLOCUTOR-1.md`. This practice's standing rule: a charge is
reproduced here before it is accepted. The adversary ran live tests our K3 control did not. We
re-ran the two that carry its strongest claims, on rows from our own census, with our own code.*

## Test 1 — is the handle in the URL checked at all?

| video (from our census, HTTP 200) | cited handle | with a handle that has never existed | with no handle in the path |
|---|---|---|---|
| `194951213564514304` | `@ranzandniana1314` | HTTP 200, 2001 B, author `ranzandniana1314` | HTTP 200, 2001 B, author `ranzandniana1314` |
| `6529030482422664450` | `@tokisen_official` | HTTP 200, 2135 B, author `tokisen_official` | HTTP 200, 2141 B, author `tokisen_official` |
| `6605829627413794050` | `@97riho23` | HTTP 200, 1666 B, author `97riho23` | HTTP 200, 1668 B, author `97riho23` |

**The charge reproduces.** The endpoint resolves by numeric identifier and ignores the handle
entirely — not merely tolerating a stale one. `RESULT.md` F6 called this a *contaminant for other
people's link-checkers*; the adversary is right that the underlying fact is stronger and simpler,
and F6 is amended to state it: **the handle is not checked.**

## Test 2 — does a known-400 row 400 under a different user agent?

| video (from our census, HTTP 400) | our agent | a plain browser agent string |
|---|---|---|
| `6641440663898426626` | HTTP 400 | HTTP 400 |
| `6675280377084382469` | HTTP 400 | HTTP 400 |
| `6677668300152900870` | HTTP 400 | HTTP 400 |

**Reproduced.** The 400 is not an agent-string block.

## What we did not reproduce, and why

The adversary's concurrent-burst test (10 parallel workers) is a load pattern this practice
declines to send to a third party for a second time in one day (`DEVIATIONS.md` D5). Its result is
accepted **as the adversary's measurement, attributed to it**, and nothing in this record depends
on it. Its vantage-point finding needed no reproduction: we ran the same query and published the
answer in `vantage-2026-08-11.md`, and it is the one charge that changes what the arc must do.
