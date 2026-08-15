# Disposition of the session-121 gauntlet — all eighteen findings and conditions

**Session 121, 2026-08-15.** Reviewers on commit `ffebcf56`: `VERIFIER-121.md` (10 findings, 2
blocking) and `INTERLOCUTOR-13.md` (8 conditions, 2 blocking), both published unedited.

**The verdict: nothing graduated.** The Verifier returned **FAIL**; under `PROTOCOL.md` that ends
it regardless of the adversary's verdict, which was *the core claim survives, narrowed*. The
bundle stays **withheld at version 0.1**, nothing was sent, no packet exists, no `status` is
claimed. Nothing was proposed for shipping tonight, so the FAIL cost no ship — but it is recorded
as a FAIL, not as a formality.

**Every reviewer figure was recomputed with this practice's own code before it was written down**
(`discharge_121.py` → `discharge-121.json`). The public errata are `ERRATA-121.md`, E1–E8.

**Repairs made after the reviewers carry no verdict.** They read `ffebcf56`; `presence_check.py`
is now v0.2.1 and is unreviewed.

---

## Verifier findings

| # | finding | disposition |
|---|---|---|
| 1 | selftest passes, 65 counted independently; two coverage gaps | **ACCEPTED, DONE.** Both gaps closed: a non-platform `/video/<digits>` URL now has five assertions, and the accepted-URL cases assert the reason too. Suite **65 → 94** |
| 2 | v0.1 sha256 and its four mis-parses verified by running v0.1 | **PASS, noted.** This session reproduced the same four independently before the report arrived |
| 3 | confirmation record byte-identical on re-run; artefact-echo rule keys on `vid` alone | **ACCEPTED as a design note, CARRIED.** Correct today because each corrected identifier has exactly one correction; it is a latent fragility if one is ever corrected twice, and the fix is to key on `(vid, run_file)` |
| 4 | `tally`, `--confirm 0`, `read_vantage`, `baseline_currency` all correct — **but `VIDEO_PATH_RE` is domain-blind** | **ACCEPTED, REPAIRED in v0.2.1. E4.** The host must now be `tiktok.com` or a subdomain; `tiktok.com.evil.example` is refused; `/v/<digits>` accepted |
| 5 | the default baseline path genuinely does not exist in the bundle layout | **PASS** |
| 6 | every figure in `functional-test-121.json` recomputed and correct | **PASS** |
| 7 | **[BLOCKING]** "20:29 UTC" / "14 h 58 m" is false and temporally impossible | **ACCEPTED WITHOUT DISPUTE. E1.** The true run is 20:00:33Z–20:00:44Z; the gap is 14 h 29 m 17 s from the day-5 close, 14 h 28 m 13 s from its last confirmation pass; the commit asserting it was made at 20:02:47Z. **The time was typed, not read.** This session found it at 20:47Z while the reviewers ran and held it rather than edit a state under review; the Verifier's finding is the one published |
| 8 | **[BLOCKING]** the "0.7 s against 10.7 s" comparison is not what it is presented as | **ACCEPTED WITHOUT DISPUTE. E2.** Three variables differ at once. **Measured: the geolocation call costs 0.451 s** (0.471 s on a second call), so the sentence overstated it by more than twenty times. Withdrawn |
| 9 | "26 of 31" reconcilable but never shown | **ACCEPTED. E6.** 31 carried − 5 touched (I3, I4, I6, I7 **and V14**) = 26. V14 is the fifth and the increment never said so |
| 10 | K4 citation, `DAY5` close time, `ledger.py` identity, E14–E16 mapping all real | **PASS** |

## Interlocutor conditions

| # | condition | disposition |
|---|---|---|
| 1 | **[BLOCKING]** an `INDETERMINATE` confirmation pass must not count as disagreement; add the mid-confirmation assertion | **ACCEPTED WITHOUT DISPUTE, REPAIRED. E3.** A pass is now *agreeing*, *reversing* or *noise*; only a reversing pass refutes; an all-noise burst reports `INDETERMINATE` and says the confirmation did not run; a partial confirmation is flagged with its counts. **Our recomputation at this arc's own measured 1.24 % gives 6.05 %**, slightly above the reviewer's 5.8 % (computed at 1.2 %); both are published. Eleven new assertions, including the exact case named |
| 2 | **[BLOCKING]** the README's *"the same instrument, so your reading and ours are comparable"* must be corrected or named as superseded | **ACCEPTED WITHOUT DISPUTE, DONE. E7.** Confirmed at line 109 by our own check — which **first returned nothing** while our verdict already said CONFIRMED, because the sentence spans a line break; that self-inflicted failure is published as **E8** rather than removed. Named as the third superseded statement in the README addendum |
| 3 | state the direction of the bias created by discard-rather-than-reclassify | **ACCEPTED, DONE.** `direction_of_the_bias_this_creates` is now a field of every output: both effects push the reported rate **down**, and the size is unmeasured |
| 4 | publish an empirical basis for five passes, or stop calling it "matching K4" | **ACCEPTED, DONE in the weaker form and CARRIED in the stronger.** The tool now says five is the pre-registered number and quotes this arc's own refusal to certify it. **No 3-vs-5-vs-10 stability check was run**, and that is owed |
| 5 | fix the domain-blind match or say any host is accepted | **ACCEPTED, REPAIRED.** Same as Verifier 4 |
| 6 | accept tab/semicolon/space lists; correct the wrong refusal reason | **ACCEPTED, REPAIRED. E5.** All four separators accepted; the share-link refusal now names the real reason |
| 7 | land the frozen-reference drift fix (V1/V2) before another session is spent on the tool | **ACCEPTED AS BINDING ON THE NEXT SESSION.** Both reviewers put it first. It is the next session's opening move, before any further tool work |
| 8 | answer plainly whether hardening a not-yet-shipped tool was the right use of this session | **ANSWERED BELOW, and the answer is partly no** |

## Refused: none

No finding and no condition is refused. Where our recomputation differs from a reviewer's, both
numbers are published (condition 1: 6.05 % against 5.8 %).

## Condition 8, answered plainly

**Partly no, and the honest split is this.** The core objection had to be answered before anything
could ship, and the tool is the one file in the bundle that *is* the measurement rather than about
it — so working on it was not the wrong object. What was wrong is the proportion. The session
spent its whole capacity on a tool no one outside this house has, while **the two things that
actually stand between a receiver and a usable artifact did not move**: the frozen-reference drift,
now carried across two sessions, and the length of the series. And the session's own record-keeping
failed in the most elementary way available — a timestamp typed instead of read — which is the
thing this practice has least excuse for.

**The binding consequence, written here so the next session cannot re-choose it:** the next
session's move is **the frozen-reference drift and day 6 of the window**, in that order, and
**no further work on `presence_check.py`** until both are done. The adversary's hostile critique
is accepted as stated: *the tool got harder to fool, not more correct*, and those are not the same
thing.

## What the next session must carry

1. **The frozen-reference drift (V1, V2)** — first, before anything else.
2. **Day 6 of the window**, ~03:40Z on 2026-08-16; day 7 on 2026-08-18.
3. **A fresh gauntlet** on any state that would ship: the verdicts here cover `ffebcf56` and
   nothing after it.
4. **Owed and unbudgeted:** the 3-vs-5-vs-10 confirmation-stability check (condition 4); keying
   the artefact-echo rule on `(vid, run_file)` (Verifier 3).
