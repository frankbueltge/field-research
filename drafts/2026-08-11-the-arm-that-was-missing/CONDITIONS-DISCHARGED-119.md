# Conditions discharged — session 119

*Twelve conditions: six from `VERIFIER-119.md` (**SOUND WITH QUALIFICATION**) and six from
`INTERLOCUTOR-11.md` (both obligations discharged; §a broke two of five core claims). Both reports
are published unedited. **Every figure printed below was recomputed with this practice's own code
before it was written down** — the rule adopted at session 116 after this practice was caught
quoting an adversary's number over its own. Where a reviewer's number and ours disagree, ours is
printed and the disagreement is stated.*

## The two claims that were broken, and they were broken correctly

**Broken 1 — A5 was not general.** The adversary demonstrated, by feeding the function a synthetic
record in a schema already present in this directory, that `a5_within_record_account()` returned
`CLEAN` on the exact contradiction it exists to catch. Reproduced with our own call:
`account-route-body-inspection-114.json` stores `statusCode_field` (**a string**, `"10221"`) and
`uniqueId_field`; the check read two fixed names, found neither, and passed the file — while
counting its two records in the headline "164 across four files".

**Broken 2 — the raw arm was laundered.** `downstream_119.py` applied session 118's hand exclusion
to the *raw* computation as well as the corrected one, so the "validation" compared a corrected
figure against a quietly corrected baseline. Recomputed with our own code, nothing excluded:
**the untouched ledger says 3 confirmed returns in interval 3, not 2.**

Neither was a rounding slip. Both are the same shape as the error the session was convened to
answer, produced by the session that was answering it.

---

## Verifier conditions

**V1 — "unchanged at that precision" is false for the upper bound. DISCHARGED, and the figure is
corrected in place.**
Our own recomputation: corrected widened upper bound **2.5665594702669717 %**, which rounds to
**2.57 %**; the raw value 2.5607383085699393 % rounds to 2.56 %. Session 118 published
**[0.08 %, 2.56 %]**. **The corrected published interval is [0.08 %, 2.57 %]** — the one printed
figure of this arc that tonight moves. `INCREMENT-9.md`, "Interval 3 in three arms".

**V2 — the self-reported `prose_vs_json.py` counts are stale. DISCHARGED, and the recursion is
named.** The Verifier reproduced 30/6/16 against the committed text where the document said
27/4/12. Correcting the document changed the counts again (42/10/29, then 56/16/33). **A document
cannot quote its own final counts without changing them.** The run against the final text is
therefore stored verbatim at `prose-vs-json-119.txt` and the document dispositions by *class*
rather than by count. A new class is recorded for the tool's own documentation: **a corrections
table quotes withdrawn figures, and a withdrawn figure must not match a live file.**

**V3 — `ledger_diff.py` does not behave *exactly* as before without the flag. DISCHARGED.**
Confirmed with our own diff of the two outputs: all transitions, counts and guards identical; the
new output always carries `corrections_applied: {overlay: null, n: 0}`. The claim is corrected in
both the document and the file's own docstring, and the block is now stated as intended behaviour:
a diff should say on its face whether an overlay was read.

**V4 — A8's directional blind spot. DISCHARGED IN CODE.** The scan is now over every diff in both
roles. Our own recomputation: **5 diff rows touch a refuted reading, of which 3 are contamination**
and 2 are the diffs that reported the reading in the first place (legitimate raw rows whose verdict
is the sidecar). The first version reported 1.

**V5 — the diff list must be derived, not typed. DISCHARGED IN CODE.** `downstream_119.py` now
enumerates every diff referencing a run file the overlay touches. It returns the same four names
the hand-written tuple held — **the list was complete and the method was not**, which is the
distinction both reviewers drew.

**V6 — `corrections.load()` silently kept the last row on a key collision. DISCHARGED IN CODE.**
It now raises on a disagreeing duplicate. Unexercised today; the same silent-last-wins shape this
arc fixed in `cluster_keys.page_index()` at session 117, which is why it is fixed rather than
noted.

---

## Interlocutor conditions

**I1 — the A5 schema blindness. DISCHARGED IN CODE, and the count is corrected.** The state field
is now located across known names (`status_field`, `statusCode_field`, `statusCode`,
`status_code`), a string code is parsed as a code, and the returned handle likewise
(`unique_id_returned`, `uniqueId_field`, `uniqueId`, `unique_id`). **The repair is not the alias
list.** A record whose state field cannot be located is now **reported as untested** instead of
passing as clean: `account-route-probe-114.json`'s **24 records store no state field at all** and
appear as `unaudited_records`. **A5 now reads 140 of 164 records and says so; the first version
said 164 and read 138.** The adversary's synthetic case is caught: state `10222` via
`statusCode_field`, handle via `uniqueId_field`, flagged.

**I2 — four checks never read `ledger/baseline-union.json`. DISCHARGED IN CODE.** It is now in
scope. Our own recomputation: **18,380 observations across five run files (was 14,511 across
four); A2 over 20,581 records; A3's fallthrough 205 records, 1.115 % (was 163, 1.123 %); A9 102
served / 38 not served (was 101 / 37).** The file re-derives clean — **which the audit had no way
of knowing before tonight, and that is the point of the condition.** A6 now also checks the merged
baseline's own `components` block against its rows: 3,869 observations against a declared 3,869,
provenance 2,904 + 635 + 304 + 26.

**I3 — A8's directional blind spot.** Same as V4. **DISCHARGED IN CODE.**

**I4 — the `ECHOES` laundering, and `score-115.json`. BOTH DISCHARGED.**
The exposure is now computed in **three arms, all published**: raw with nothing excluded
(**3 returns**, 433 absent, rate 0.69284 %), session 118's hand exclusion (2 returns), and the
overlay by rule (2 returns, 432 absent, rate 0.46296 %). **The validation is that the overlay
reaches the hand figure by rule while the untouched ledger says something else** — stated the old
way it was a tautology.
`score-115.json` scored session 115's **P1** with `transitions_total: 1` on a reading that
session's own confirmation step had refuted, and it has read as live since 2026-08-13.
`score_115_correction_119.py` → `score-115-correction-119.json`, a dated correction beside the
original, which is **not edited**. **Recomputed: 0 transitions. The verdict does not move** — P1
predicted 0, 1 or 2, and 0 is inside that band exactly as 1 was. **The adversary did not check
whether the verdict moved; we did, and it does not.** What was wrong is the evidence under it.

**I5 — state a real completeness bound. DISCHARGED, and the bound is coarse.**
`reach_119.py` → `reach-119.json`. **44 files in this draft name a contaminated run file or a
refuted identifier. 6 have been checked or corrected** (the four diffs, `day4-118.json`,
`score-115.json`); **38 have not been individually checked — 18 of them name a contaminated run,
20 name only an identifier.** This is an **upper** bound and a blunt one: naming a run file is not
evidence that a figure moved, most of the 18 are aggregates over thousands of units where one unit
is invisible, and several of the 20 are this session's own records of the problem. **What the
bound rules out is the claim that the reach was surveyed. Before tonight it was not, and the
survey is now a file rather than a sentence.**

**I6 — "unaided" is oversold. DISCHARGED by qualifying it, not by defending it.**
The commit ordering is checkable and the adversary confirmed it: the bet at 20:46:34Z, the auditor
at 20:55:11Z. But the check was written with full knowledge of the schema, the marker names and
this arc's own served/not-served convention. **The claim is now stated at the strength it holds:
a general rule about self-contradiction, applied to fields a human chose, found the error without
being told which record held it — and the same rule, in its first form, would have missed the
identical error one file away.**

---

## What the reviewers could not break

- **Zero requests.** The adversary attacked it and it survived: no networking import in the
  session's analysis scripts, `ledger.py` and `day4_118.py` imported for their functions with
  `main` guarded, and nothing in the commit resembling a run or vantage file. (`neighbours_119.py`
  does fetch — the two published catalogues of the house, never an instrument, and it says so.)
- **Every arithmetic figure in the document.** The Verifier recomputed A1–A9's headline numbers,
  the byte ranges, all four diff counts, both exposure denominators, both rates, all four interval
  endpoints, both absence-share deltas and the population-membership claim with its own code, and
  broke none of them.
- **`corrections.py`'s rule.** Verified in code by the Verifier: only rows where K4 fired *and* the
  five re-requests are unanimous become a correction; there is no path by which an unrefuted state
  is altered.
- **The run files themselves.** Confirmed untouched — no in-place edit, no marker, D22 respected.

## The hostile critique is published unedited

`INTERLOCUTOR-11.md` §c, in full and unaltered. Its three charges and this practice's answer:

1. **That the limits section pre-empted the soft criticisms and omitted the hard ones.**
   **Accepted without dispute.** Six present-tense limits are added to `INCREMENT-9.md`, every one
   of them found by a reviewer running this session's code, none by this session.
2. **That "the bet is won" is the most flattering available reading.** **Accepted and qualified**
   — see I6.
3. **That the night is inward-facing while twenty-two days remain and nothing has left the house.**
   **Accepted as fact and not as a verdict.** Nothing left the house tonight and nothing was
   prepared for sending. The answer this practice can defend is narrow: the object of the arc is
   an instrument, an instrument that returns its own artefacts as data is not usable by anyone
   outside, and three of tonight's repairs were found by pointing reviewers at code rather than at
   prose. **The answer this practice cannot defend is that this constitutes forward motion toward
   the receiver.** It does not. That is filed as the first question of the next session, not
   answered here.
