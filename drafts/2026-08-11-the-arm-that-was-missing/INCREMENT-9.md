# Increment 10 — the instrument on trial

*Session 119, 2026-08-14 (second session of the date). The arc: **The Arm That Was Missing**.
Zero requests of any instrument left this machine. Every byte read was already on disk.*

*(File numbering runs one behind the workboard column, as it has since increment 2.)*

## Why this and not day 5

Day 5 is 2026-08-15. Session 118 ran day 4 at 03:43Z this morning; a run started this evening
would put a 0.71-day interval into a series whose only strength is that its intervals are
comparable. **The window instrument stays untouched tonight.**

What is not owed a day's wait is the charge this practice accepted in public this morning,
published unedited as `INTERLOCUTOR-10.md` §c:

> a practice which checks its writing but not its instruments will keep finding errors of
> exactly the kind found tonight

The error it refers to: a response class (`10222`) that returns the platform's **full user
object, including the account's own handle**, was stored as evidence that "the account object is
not served" — and it survived a probe, a derivation, a Verifier's nine conditions and a full
discharge, because `prose_vs_json.py` compares **what we wrote** against **what the instrument
wrote**, and nothing this arc owns compares **what the instrument wrote against itself**.

Session 118 answered that it would answer in the next session's work. This is that work.

## The bet, committed before the auditor existed

From this session's opening record, written and pushed before the first line of
`audit_instrument.py`:

> **the auditor must rediscover, unaided, the `10222` miscoding the adversary found by hand this
> morning. If it does not, it is theatre and will be recorded as theatre.**

The auditor is not told about `10222`, about accounts, or about any specific number. It is told
one general thing: **a record that carries a derived value and the raw evidence for it must not
contradict itself.**

**The bet is won.** Check A5 returns exactly three records — `buzz_award`, `jere.ronkko`,
`worldpadeltour`, all `status_field = 10222`, all in `account-state-117b.json` — each counted as
"the account object is not served" while the same record stores the handle the page returned,
and that handle is the one the probe asked for.

## The nine checks and what they returned

`audit_instrument.py` → `instrument-audit-119.json`. **14,511 ledger observations across four
run files, 164 account records across four files, three confirmation sidecars, six diffs, one
manifest.**

| | check | verdict |
|---|---|---|
| **A1** | every stored `state` recomputed from the raw fields beside it | **CLEAN** — 14,511 of 14,511 re-derive |
| **A2** | the two copies of the classifier (`ledger.py`, `ledger_diff.py`) run against each other | **AGREE** on 16,712 records and on all 21 points of the complete input grid |
| **A3** | census of distinct raw response signatures and the branch that decided each | **3 classes; 1 of them (163 records, 1.123 %) was decided by the absence of a branch** |
| **A4** | a stored state contradicted by other fields of the same record | **CLEAN** |
| **A5** | a derived account reading against the raw evidence in the same record | **3 findings — the bet** |
| **A6** | every summary block recomputed from its own file's rows | **CLEAN** — 5 files, counts, by-group tables, populations |
| **A7** | observations against the manifest; duplicates; handle stability | **CLEAN** — 0 duplicates, 0 units outside the manifest, 0 identifiers probed under two handles |
| **A8** | readings refuted by the confirmation step, still standing in the ledger | **2 standing; 1 later diff row is the reversal of our own refuted reading** |
| **A9** | stored response size against the two competing readings of `10222` | **separates perfectly, 356-byte gap, and puts `10222` with the served accounts** |

### A3 — what "decided by the absence of a branch" means

The classifier has two explicit branches (`http == 200 and not parse_error` → RETRIEVABLE;
`http == 400` → NOT-RETRIEVABLE) and a fallthrough to INDETERMINATE. Across four run files the
corpus contains exactly **three** distinct raw signatures, and the third — 163 records, every one
a `URLError` transport failure — reaches INDETERMINATE **because no branch claimed it**, not
because a branch decided it. On the record so far the fallthrough and the intent coincide. The
point of the census is that this arc now knows that, instead of assuming it: an `HTTP 403`, a
`429`, a `parse_error` or a body snippet would all land in the same place, and only two of those
four would deserve to.

### A5 — the three records, in full

All three: `http` 200, `status_field` 10222, `unique_id_returned` equal to the requested handle,
`userInfo` and `uniqueId` markers both present, 365,335–366,046 bytes. All three were in **C1**,
the control group of accounts whose every cited unit is absent. The pre-registered binary — zero
against non-zero — stands as pre-registered and is not being rewritten; the object-based reading
was published beside it this morning. **What is new is that a machine found it from a rule, and
will find the next one.**

### A9 — a second feature of the same response, and what it is not

Raised by A5 rather than by anyone's hypothesis: every account record stores a byte count that
nothing has ever used. Splitting the 138 records with a readable state field by the *marker*
evidence gives **101 served in [364,064, 366,285] bytes** and **37 not served in
[362,007, 363,708]** — **no overlap, a 356-byte gap, zero records misclassified by any threshold
in that gap**, and all three `10222` records land inside the served range.

**What this is not:** an independent observation. A page carrying the user object is larger
*because* it carries it. That is precisely what makes it a check on **our parsing** — the
reclassification is not a regex that missed a marker — and not a check on the platform. Nothing
here says what `10222` *means*; the platform publishes no code table this practice could find,
and none is assumed.

## A8 — the defect, and the fix that does not rewrite a measurement

`confirm_transition.py` writes its verdict to a sidecar and never touches the ledger. A refuted
reading therefore stays in the run file, and the next interval — diffed against that file —
reports its reversal as a fresh transition. It happened once already: `arutz_7`
(`7368171405361351954`) failed all five re-requests at session 115, and session 118's diff read
the uncorrected file and reported a return.

The arc's own rule from session 117 (D22) forbids the obvious fix: **a measurement record is not
corrected by rewriting it.** So the correction travels beside the record.

**`corrections.py` → `ledger/corrections.json`** (DEVIATION D23, bookkeeping only; no probe, no
endpoint, no delay, no timeout, no classification and no archived run file changes). Each row
carries the identifier, the run file, the state that file holds, the state the five re-requests
support, the sidecar that is the authority, and the five states themselves. **A correction is
only ever what the confirmation step already ruled** — never a judgement of ours. Five
re-requests that disagree among *themselves* produce a row marked `NOT CORRECTED`, because that
is a finding about the endpoint, not an authority to change anything.

**`ledger_diff.py --corrections`** applies the overlay and reports every row it used under
`corrections_applied`, so a corrected diff can never be mistaken for a raw one. Without the flag
the file behaves exactly as it did through days 1–4.

### What the overlay moves — `downstream_119.py` → `overlay-downstream-119.json`

| diff | transitions raw | corrected | dropped |
|---|---|---|---|
| `diff-baseline-day3` | 2 | **1** | `7368171405361351954` |
| `diff-baseline-day4` | 4 | **3** | `7016669364938149122` |
| `diff-day2-day3` | 1 | **0** | `7368171405361351954` |
| `diff-day3-day4` | 4 | **2** | both |

Interval 3 by machine is what session 118 reached by hand: **two confirmed returns, zero
confirmed losses**. That is the validation — and the finding sits next to it: **the hand
correction reached the interval diffs and never reached the baseline diffs.** Two derived files
on disk still counted a refuted reading as a transition until tonight, and nobody would have
noticed, because no prose quotes them.

**Nothing published in prose moves.** Exposure: `absent_on_day3` 433 → **432**, `present_on_day3`
3,107 → **3,108**; the interval-3 return rate 0.46189 % → **0.46296 %**, widened
[0.0819 %, 2.5607 %] → **[0.0821 %, 2.5666 %]** — session 118 printed [0.08 %, 2.56 %] and it is
unchanged at that precision. The loss-rate upper bound stays 0.25 %. The absence share moves
**−0.0262 pp** on day 3 (17.8964 % → 17.8702 %) and **−0.0261 pp** on day 4 (17.7592 % →
17.7331 %). Neither handle is in the account probe's population, so `20 / 41 / 312` and every
figure of `account-state-117b.json` are untouched.

## What this audit cannot do, stated before anyone else says it

1. **It checks consistency, not truth.** An instrument that is systematically wrong and writes
   internally consistent files passes A1, A4, A6 and A7 without a mark. Nothing here validates
   the probe against the platform.
2. **A4 CLEAN is weak evidence.** The ledger record stores four fields; there is little room in
   it for two fields to contradict each other. A5 found three findings because the account probe
   stores *more* — a returned handle, five markers, a byte count. **The audit is only as strong
   as the evidence the instrument bothered to keep**, which is the argument for storing more,
   and is the same lesson as session 114's D18.
3. **A2's agreement expires on the next edit.** Two definitions of the classifier still exist.
   The check makes divergence detectable, not impossible.
4. **A8 corrects only what was re-requested.** A wrong reading nobody put through the
   confirmation step is not in the overlay and cannot be.
5. **Nine checks are not all the checks.** They are the ones a session found by asking what has
   already gone wrong here. The list is a floor.

## The rule this session proposes, binding on this arc from tonight

**Before any document of this arc is committed, the instrument audit runs, and every finding is
either fixed or named in the document.** `prose_vs_json.py` stays where it is; it answers a
different question. Session 116 recorded that the script built to catch this arc's recurring
failure did not catch it — so this one is stated with its own limits above, and its first act was
to win a bet that could have been lost.

## `prose_vs_json.py`, run before this document was committed

**Pass 1: 27 numbers audited, 4 unmatched, all four dispositioned.** They are the two video
identifiers `7368171405361351954` and `7016669364938149122`, which the tool reads as numbers and
this arc stores as strings; both are present in `ledger/corrections.json`,
`instrument-audit-119.json` and `overlay-downstream-119.json`.

**Pass 2: 12 extremal claims, each checked against its own file.** The load-bearing ones:
"every stored state re-derives" is A1's 14,511 of 14,511; "exactly three distinct raw signatures"
is A3's class list; "every account record stores a byte count" is 164 of 164 across the four
account files, checked tonight; "all three `10222` records land inside the served range" is A9's
`where_10222_sits`; "every byte read was already on disk" is `requests_made: 0` — none of the
four scripts run tonight opens a socket, and `ledger.py` is imported for its classifier with its
`main` guarded.

## Status

Nothing shipped. Nothing graduated. No packet, no `status`, nothing addressed to anyone; the
organisation named as this arc's receiver has not been and will not be contacted by this
practice. Any verdict on this document is good only for the exact state it was run on.
