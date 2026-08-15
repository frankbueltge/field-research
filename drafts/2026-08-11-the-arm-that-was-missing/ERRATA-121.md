# Errata of session 121 — every false statement, with the value that is true

**2026-08-15, session 121 (second session of the date).** The gauntlet on increment 12 returned
**Verifier: FAIL** (two blocking) and **Interlocutor (a): the core claim survives, narrowed**
(two blocking charges). Under `PROTOCOL.md` a work graduates only if the Verifier passes and the
core objection is answered, so **nothing graduated, nothing shipped, and the bundle remains
withheld at version 0.1.** Both reports are published unedited: `VERIFIER-121.md`,
`INTERLOCUTOR-13.md`.

**Every figure below was recomputed with this practice's own code before it was written down**
(`discharge_121.py` → `discharge-121.json`). Where our recomputation and a reviewer's differ,
both are printed. **No file either reviewer read was rewritten**: they read commit `ffebcf56`,
and the repairs made after them are a new state carrying no verdict.

---

## E1 — A time that never happened, stated in the past tense before it could have happened

**Where:** `INCREMENT-11.md` §3 and `deliverable/README.md`'s dated addendum.
**What was published:** that `7234106298021727515` was still `NOT-RETRIEVABLE` *"at 20:29 UTC"*,
*"an independent re-confirmation 14 h 58 m later"*, and that the tool's "unmodified" description
*"stopped being true at 20:29 UTC today."*

**True values.** The only run that happened started **2026-08-15T20:00:33Z** and finished
**20:00:44Z** (`functional-test-121.json`). Against the day-5 run's close (05:31:27Z) the gap is
**14 h 29 m 17 s**; against the day-5 confirmation's last pass (05:32:20Z) it is
**14 h 28 m 13 s**. **There was no run at 20:29 UTC.** The commit that published the claim,
`ffebcf56`, was made at **20:02:47Z** — twenty-six minutes *before* the moment it describes in
the past tense.

**How it happened, without excuse:** the time was not read off anything. It was typed. That is
the prohibition this practice puts first, committed by the session that wrote it.

**Who found it.** This session found it at 20:47Z while the reviewers were still running, and
**held it rather than edit a state under review**. The Verifier found it independently and its
finding (§7) is the one published. The Interlocutor's own §9 repeated the false *14 h 58 m*
back — an adversary can inherit a number too, which is exactly why the Verifier exists.

## E2 — The vantage-cost comparison compared three variables at once

**Where:** `INCREMENT-11.md` §3.
**What was published:** *"`--vantage none` made no third-party call (0.7 s against 10.7 s)."*

**True values.** The 0.7 s run was **1 identifier, `--confirm 0`, `--vantage none`** — it was the
missing-baseline test, not a vantage test. The 10.7 s run was **3 identifiers, `--confirm 5`,
`--vantage asn`**. Three variables differ; the second run's own mandated sleeps are already
**7 s** at `ledger.DELAY = 1.0`. **Measured directly this session: the geolocation call costs
0.451 s** (and 0.471 s on a second call). Presenting ~10 s as the cost of the call **overstates
it by more than twenty times.** The reviewer is right and the sentence is withdrawn. What is
true and was worth saying: `--vantage none` **makes no call at all**, which is a disclosure
property, not a speed property.

## E3 — A blocking defect in the confirmation logic the new tool shipped with

**Where:** `presence_check.py` v0.2, `measure()`.
**What was wrong:** `agreed = all(s == first_pass_state for s in states)` treated a confirmation
pass that **timed out** exactly like a pass that came back with the **opposite state**. A
genuinely absent unit was therefore discarded from both numerator and denominator on one
transport blip.

**Size, on this arc's own numbers.** Transport failure was measured at **1.24 %** at session 110
(`PREREGISTRATION-112.md`, P2 ceiling 2.0 %). The chance that at least one of five passes is
noise is **6.05 %** at 1.24 %, 9.61 % at 2.0 %, 1.64 % at session 109's 0.33 %. The reviewer gave
**5.8 %** using 1.2 %; both are printed. Roughly **one genuinely absent unit in seventeen** was
being thrown away, pushing the reported rate **down**, and worst exactly under the load the
confirmation step itself creates.

**Repaired in v0.2.1**, with an assertion the reviewer specified: a pass is *agreeing*,
*reversing* or *noise*; only a reversing pass refutes; an all-noise burst reports
`INDETERMINATE` and says the confirmation did not run; a partial confirmation is flagged
`partial: true` with its counts.

## E4 — The URL rule was domain-blind: I4's own failure through the accepted path

**Where:** `presence_check.py` v0.2, `VIDEO_PATH_RE`; described as closed in `INCREMENT-11.md`
and `CHANGELOG-v0.2.md`.
**What was wrong:** the rule matched `/video/<digits>` in **any** URL with no host check, so
`https://www.youtube.com/video/7123456789012345678` and
`https://www.instagram.com/reel/video/9999999999` were **accepted** and measured against this
platform's endpoint. Found independently by both reviewers. I4 was closed for bare-digit
coercion and left open here.

**Repaired in v0.2.1**: the host must be `tiktok.com` or a subdomain of it, checked on the parsed
authority so `tiktok.com.evil.example` is refused too; the platform's own `/v/<digits>` share
path is now accepted.

## E5 — The new strictness refused ordinary lists, and gave one refusal a wrong reason

**Where:** `presence_check.py` v0.2, `parse_line`.
**What was wrong:** tab-, semicolon- and space-separated `id handle` pairs — ordinary spreadsheet
exports — were refused; and `https://m.tiktok.com/v/<id>.html` was refused with the reason *"a
short link or a link from another platform"*, which is **false on both counts**: it is the same
platform and the identifier is a plain substring, not a redirect target.

**Repaired in v0.2.1**: all four separators accepted; the share-link refusal now names the real
reason (an unresolved `vm.`/`vt.` link, and this tool does not follow redirects).

## E6 — The condition arithmetic was right and was never shown

**Where:** `INCREMENT-11.md` §4, *"Twenty-six of the thirty-one carried conditions are
untouched."*
**True and now stated:** 32 dispositioned at session 120, one (I16) discharged there, **31
carried**. v0.2 touches **five**: I3, I4, I6, I7 — and **V14**, because the README addendum is
what rewords *"unmodified since it was written"*. 31 − 5 = **26**. The figure was defensible and
a reader could not check it without reconstructing the chain. The Verifier's finding 9 stands.

## E7 — The bundle still asserts the sentence the objection was raised against

**Where:** `deliverable/README.md` §4, item 1, **line 109**: *"It is the same instrument, so your
reading and ours are comparable."*
**Why it is false:** `presence_check.py`'s own docstring, written in the same commit one file
over, says *"The two instruments are not the same and a figure from one is not a row of the
other."* The previous adversary (`INTERLOCUTOR-12.md` §a.1c) quoted this exact sentence as the
falsehood at the centre of the objection that stopped the ship. The session-121 addendum
enumerated **two** superseded statements and missed this, the one that mattered most.

**Corrected here and named as a third superseded statement in the addendum.** The body is not
rewritten, so both adversaries' quotations stay checkable.

## E8 — A check of ours returned nothing while our verdict already said CONFIRMED

**Where:** `discharge_121.py`, first version, the E7 check above.
**What happened:** the check searched line by line for *"same instrument"* and returned an
**empty** result — because the phrase is split across a line break in the source — while the
verdict beside it already read `CONFIRMED`. A verdict written before its own check ran is the
exact failure sessions 87, 88 and 90 were caught on, and this practice committed it again
tonight, in the script whose entire purpose is to stop it.

**Corrected before the file was published**: the check now reads the whole text with whitespace
collapsed, finds the sentence, and reports the line carrying its second half (**109**), which is
the line the reviewer named. The defect is recorded in the script's own comments rather than
removed from them.

---

## What is repaired, what is carried, and what carries no verdict

**Repaired tonight, in `presence_check.py` v0.2.1** (E3, E4, E5) and in the README addendum (E7),
with the selftest suite grown from **65 to 94 assertions**, including the mid-confirmation
`INDETERMINATE` case the adversary named as untested. **v0.2.1 was then run against the live
endpoint** (`functional-test-121b.json`, 20:21:26Z–20:21:37Z): the four adversarial lines refused
with correct reasons, the confirmation step fired and agreed 5 of 5, and
`7234106298021727515` was **still `NOT-RETRIEVABLE` 14 h 49 m after its day-5 confirmation** —
a second independent re-request, still n = 1 identifier and still not a persistence rate.

**Carried, unfixed, and named so it cannot be quietly dropped:**

1. **The frozen-reference drift (V1, V2)** — `reference-baseline.json` declares a `t_ref_utc` its
   own ages were not computed against. Two full sessions have now carried it. Both reviewers put
   it at the top of what to do next.
2. **The direction of the bias** the design creates (discard-rather-than-reclassify, plus never
   testing presence) is now **stated in the tool's output**, and its **size is unmeasured**.
3. **Five passes is a precedent, not a threshold.** This arc's own
   `PREREGISTRATION-119-overlay-use.md` declines to claim five re-requests are the right test.
   The tool now says so where a user reads it. Nothing has measured what a sixth pass would add.
4. **The series is still five days** (I16), and twenty-six of the thirty-one carried conditions
   are still untouched.

**The verdicts of this gauntlet are good only for commit `ffebcf56`.** Everything repaired after
them is unreviewed, and any later state needs a fresh gauntlet before anything graduates.
