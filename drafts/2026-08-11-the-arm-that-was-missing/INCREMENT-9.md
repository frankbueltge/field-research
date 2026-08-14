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

**The bet is won, on the narrow reading, and the narrow reading is the only one claimed.** Check
A5 returns exactly three records — `buzz_award`, `jere.ronkko`, `worldpadeltour`, all
`status_field = 10222`, all in `account-state-117b.json` — each counted as "the account object is
not served" while the same record stores the handle the page returned, and that handle is the one
the probe asked for. The commit times are checkable: the bet at 20:46:34Z, the auditor at
20:55:11Z.

**What "unaided" does and does not mean, after the adversary's objection, which is accepted.**
The number `10222` never appears in `audit_instrument.py`, and no account, group or verdict was
named to it. But the check was written with full knowledge of the schema, the marker names and
this arc's own served/not-served convention — **that is unaided by the answer, not unaided by the
question.** And the first version was aided too narrowly: it read two field names and was blind on
a fourth file that stores the same thing under different ones (§6 of the limits below). The honest
statement is: *a general rule about self-contradiction, applied to fields a human chose, found the
error without being told which record held it* — and the same rule, in its first form, would have
missed the identical error one file away.

## The nine checks and what they returned

> **This table was regenerated on 2026-08-14 after the gauntlet, and its numbers are not the ones
> the reviewers were shown.** Both reviewers found that four checks silently excluded
> `ledger/baseline-union.json` (3,869 observations, and `run1` for two of the diffs this session
> is built on), that A5 was blind to one of the four files it counted, and that A8 could only see
> contamination in one direction. All three are repaired below; every superseded figure is listed
> in **Corrections after the gauntlet**.

`audit_instrument.py` → `instrument-audit-119.json`. **18,380 ledger observations across five
run files, 164 account records across four files of which 140 could be tested, three confirmation
sidecars, six diffs, one manifest.**

| | check | verdict |
|---|---|---|
| **A1** | every stored `state` recomputed from the raw fields beside it | **CLEAN** — 18,380 of 18,380 re-derive |
| **A2** | the two copies of the classifier (`ledger.py`, `ledger_diff.py`) run against each other | **AGREE** on 20,581 records and on all 21 points of the complete input grid |
| **A3** | census of distinct raw response signatures and the branch that decided each | **3 classes; 1 of them (205 records, 1.115 %) was decided by the absence of a branch** |
| **A4** | a stored state contradicted by other fields of the same record | **CLEAN** |
| **A5** | a derived account reading against the raw evidence in the same record | **3 findings — the bet — over 140 of 164 records; the other 24 store no state field at all and are listed as untested** |
| **A6** | every summary block recomputed from its own file's rows | **CLEAN** — 6 files, counts, by-group tables, populations, and the merged baseline's component provenance |
| **A7** | observations against the manifest; duplicates; handle stability | **CLEAN** — 0 duplicates, 0 units outside the manifest, 0 identifiers probed under two handles |
| **A8** | readings refuted by the confirmation step, still standing in the ledger | **2 standing; 5 diff rows touch them, of which 3 are contamination** |
| **A9** | stored response size against the two competing readings of `10222` | **separates perfectly, 356-byte gap, and puts `10222` with the served accounts** |

### A3 — what "decided by the absence of a branch" means

The classifier has two explicit branches (`http == 200 and not parse_error` → RETRIEVABLE;
`http == 400` → NOT-RETRIEVABLE) and a fallthrough to INDETERMINATE. Across five run files the
corpus contains exactly **three** distinct raw signatures, and the third — 205 records, every one
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
nothing has ever used. Splitting the 140 records with a readable state field by the *marker*
evidence gives **102 served in [364,064, 366,285] bytes** and **38 not served in
[362,007, 363,708]** — **no overlap, a 356-byte gap, zero records misclassified by any threshold
in that gap**, and all three `10222` records land inside the served range.

**What this is not:** an independent observation. A page carrying the user object is larger
*because* it carries it. That is precisely what makes it a check on **our parsing** — the
reclassification is not a regex that missed a marker — and not a check on the platform. Nothing
here says what `10222` *means*; the platform publishes no code table this practice could find,
and none is assumed.

**And the margin is thinner than "separates perfectly" sounds** — the adversary's measurement,
accepted: the 356-byte gap is **five to six times smaller than the spread inside either group**
(served spans 2,221 bytes, not served 1,701). The separation is real on these 140 records and it
is not a wide margin. **The groups are also defined by the same marker evidence A5 used**, so on
135 of the 140 records the split coincides with `status_field == 0` by construction; the three
`10222` records are the *only* place where the two ways of splitting disagree, which is where the
check has any content at all. Stated at full strength: this is a coupled second feature, and it
rules out one specific alternative — a parsing artefact — and nothing else.

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
every transition, count and guard is identical to days 1–4 — **but the output is not
byte-identical, and the first version of this sentence said it was.** A reviewer ran both
versions and found the added `corrections_applied: {overlay: null, n: 0}` block. That block is
now the intended behaviour, not an oversight: a diff file should say on its face whether an
overlay was read.

### What the overlay moves — `downstream_119.py` → `overlay-downstream-119.json`

| diff | transitions raw | corrected | dropped |
|---|---|---|---|
| `diff-baseline-day3` | 2 | **1** | `7368171405361351954` |
| `diff-baseline-day4` | 4 | **3** | `7016669364938149122` |
| `diff-day2-day3` | 1 | **0** | `7368171405361351954` |
| `diff-day3-day4` | 4 | **2** | both |

The diff list above is **derived, not typed** — every diff referencing a run file the overlay
touches. The first version of `downstream_119.py` carried a hand-written tuple of four names, and
both reviewers named that as the reason a check with a directional blind spot still produced a
correct table. The derived list returns the same four.

**The finding sits next to it: the hand correction reached the interval diffs and never reached
the baseline diffs.** Two derived files on disk still counted a refuted reading as a transition
until tonight, and nobody would have noticed, because no prose quotes them.

### Interval 3 in three arms — and the first version of this section laundered its own baseline

| arm | absent day 3 | confirmed returns | rate | widened at DEFF 1.9900 |
|---|---|---|---|---|
| **raw ledger, nothing excluded** | 433 | **3** | 0.69284 % | [0.1607 %, 2.9358 %] |
| session 118's hand exclusion | 433 | 2 | 0.46189 % | [0.0819 %, 2.5607 %] |
| **the overlay, by rule** | **432** | **2** | 0.46296 % | [0.0821 %, 2.5666 %] |

**The validation is that the overlay reaches the hand figure by rule while the untouched ledger
says something else.** The first version of this document computed the "raw" arm with session
118's hand exclusion still applied — comparing a laundered baseline against the overlay and
calling the match a validation. **The adversary caught it and recomputed the honest raw figure:
three, not two.** The correction is in the code (`HAND_EXCLUSION` is now passed explicitly and
the raw arm passes nothing) and the true raw number is published above.

**Almost nothing published in prose moves, and the exception is named.** `present_on_day3`
3,107 → **3,108**; the absence share moves **−0.0262 pp** on day 3 (17.8964 % → 17.8702 %) and
**−0.0261 pp** on day 4 (17.7592 % → 17.7331 %); the loss-rate upper bound stays 0.25 %. Neither
handle is in the account probe's population, so `20 / 41 / 312` and every figure of
`account-state-117b.json` are untouched.

**The exception, found by the Verifier and not by us:** session 118 published the widened return
interval as **[0.08 %, 2.56 %]**. Under the overlay the upper bound is 2.56656 %, which rounds to
**2.57 %**. The first version of this document asserted the interval was "unchanged at that
precision"; it crosses the rounding boundary. **The corrected published interval is
[0.08 %, 2.57 %]**, and that is the one printed figure of this arc that tonight moves.

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

**And the five above are all future-tense hedges, which the adversary named as a tell.** A limits
section that pre-empts the soft criticism and omits the hard one is not honesty about limits. The
present-tense facts, every one found by a reviewer running this session's own code and none of
them by this session:

6. **A5 was blind on one of the four files it counted.** `account-route-body-inspection-114.json`
   stores the same quantities under `statusCode_field` (as a *string*) and `uniqueId_field`; the
   check read two fixed field names, found neither, and passed the file as clean while counting
   its records in the headline. The adversary proved it by feeding the function a record in that
   schema carrying the exact contradiction A5 exists to catch, and getting `CLEAN`. **Repaired:**
   the state field is now located across known names, a string code is a code, and a record whose
   state field cannot be located is **reported as untested** instead of passing silently — which
   is how the 24 records of `account-route-probe-114.json` now appear.
7. **Four checks never read `ledger/baseline-union.json`** — 3,869 observations, `run1` for two of
   the diffs this session is built on — because the glob was `ledger/run-*.json`. Both reviewers
   found it independently. **Repaired**, and the file re-derives clean; the audit simply had not
   known that.
8. **A8 could only see contamination in one direction.** It matched the contaminated file as a
   diff's *first* run and was structurally blind to every diff using it as the *second*. It
   reported one affected row; the bidirectional scan finds **five**, of which **three** are
   contamination. The published table was right only because a second script carried a
   hand-written list of four diff names. **Both repaired.**
9. **The night's own raw-versus-corrected comparison was laundered.** See the three-arm table
   above.
10. **`corrections.load()` silently kept the last row on a key collision** — unexercised today,
    and the same silent-last-wins shape this arc fixed in `cluster_keys.page_index()` at session
    117. It now raises.
11. **A1's CLEAN is close to guaranteed by construction**, and the first version of this document
    did not say so. `ledger.classify` is the same function that wrote the states and the one A1
    re-imports to check them; it has never been edited. A1 can fire only if the classifier drifts
    or a file is hand-edited. **That is worth having** — those are the two things nobody would
    otherwise notice — but "18,380 of 18,380 re-derive" is evidence that nothing was hand-edited,
    not evidence that the instrument is sound.

## Does it catch an error it was not built around? — the mutation test

The obvious objection to a check written the day after an error is known: it may be a rule shaped
to fit one answer. `mutation_test_119.py` injects **nine** distinct failure classes into symlinked
scratch copies — no file of this repository is modified — and runs the auditor there unchanged:
a state flipped with the aggregate kept consistent · an HTTP class the classifier has no branch
for · a RETRIEVABLE record with its evidence removed · an unseen non-zero account code that still
serves the user object · an account read as "not served" whose page carries the markers · a unit
probed twice · a summary block drifted from its rows · an observation outside the manifest · an
identifier probed under a changed handle.

**Nine of nine were caught by the check that should catch them** (`mutation-test-119.json`), and
two of the nine are the "different error of the same class" the adversary asked for. **What this
does not show:** the mutations were written by the same session that wrote the auditor. It shows
the checks are not hard-wired to `10222`. It does not show the check-set is complete — and the
five blind spots listed above were found by reviewers, not by this test.

## A stale verdict, corrected — and this one was live in the record

The adversary found that `score-115.json` scores session 115's prediction **P1** with
`transitions_total: 1`, its `detail` naming `7368171405361351954` — **the reading the same
session's own confirmation step refuted.** A discarded claim that reads as live is exactly what
this practice's own rule 6 forbids, and it had read as live since 2026-08-13.

`score_115_correction_119.py` → `score-115-correction-119.json`, a dated correction beside the
original, which is **not edited**. **The verdict does not move** — P1 predicted 0, 1 or 2
confirmed transitions and 0 is inside that band exactly as 1 was. What was wrong is the evidence
under it: the arc reported a confirmed transition it had itself refuted, and the interval it
counted was empty.

## Has the field already done this? — the catalogues, asked before the claim

`neighbours_119.py` → `neighbours-119.json`, fetched first-hand and **not mirrored**. The atlas of
**505** works and the paper register of **1,116** entries both return **zero** on *self-audit*,
*instrument error*, *measurement error*, *error correction*, *data quality*, *quality control* and
*internal consistency*; the atlas returns zero on *integrity* and *reproducibility* as well. The
nearest neighbour in the atlas by spirit is a forensic methodology report whose decisive move is
publishing a method for an **external** lab to validate — the opposite direction from auditing
one's own stored record. In the register the nearest work is one this arc had already read and
assessed: *Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and Short-term Validity
of Findings* (`arXiv:2504.18140`), filed at this arc's own fan-out as adjacent but not a match.
**A negative result from 505 neighbours and 1,116 papers, recorded as evidence — and no claim of
novelty is made on it.**

## The rule this session proposes, binding on this arc from tonight

**Before any document of this arc is committed, the instrument audit runs, and every finding is
either fixed or named in the document.** `prose_vs_json.py` stays where it is; it answers a
different question. Session 116 recorded that the script built to catch this arc's recurring
failure did not catch it — so this one is stated with its own limits above, and its first act was
to win a bet that could have been lost.

## `prose_vs_json.py`, re-run against the final text

**The first version of this section reported its own tool's output wrongly** — it said 27/4/12
while the committed text produced 30/6/16, because the numbers were quoted from a run made before
later paragraphs were added and never re-run. **The Verifier reproduced the discrepancy twice.**
That is precisely the failure this tool exists to catch, appearing in the sentence that reports
the tool. The counts below are from a run against the final text.

**And there is a recursion here that is worth naming rather than hiding:** every sentence
reporting the tool's counts adds numbers to the document and changes them. Writing the correction
above moved 42/10/29 to **56/16/33**. The counts cannot be quoted and final at once, so the run
against the final committed text is stored verbatim at **`prose-vs-json-119.txt`**, and the
dispositions below name the classes, which do not move.

**Pass 1 disposition, by class.** Seven are occurrences of the
two video identifiers `7368171405361351954` and `7016669364938149122`, which the tool reads as
numbers and this arc stores as strings — both are in `ledger/corrections.json`,
`instrument-audit-119.json` and `overlay-downstream-119.json`. One is `arXiv:2504.18140`, an
identifier, not a quantity. Two are percentages the prose prints from fractions the files store:
**1.115 %** is A3's 205 of 18,380 (1.11534 %) and **0.69284 %** is the raw arm's 3 of 433
(0.0069284066), both recomputed against the JSON tonight — and the second was printed as 0.69282
in the first version of this table and is corrected here. **And one class is new and belongs in
the tool's own documentation: a corrections table quotes withdrawn figures, and a withdrawn figure
must NOT match a live file.** `0.69282 %` appears twice and matches nothing, which is the correct
outcome, not a finding.

**Pass 2: extremal claims, each checked against its own file.** The load-bearing ones: "every
stored state re-derives" is A1's 18,380 of 18,380; "exactly three distinct raw signatures" is A3's
class list; "all three `10222` records land inside the served range" is A9's `where_10222_sits`;
"nine of nine caught" is `mutation-test-119.json`; "every byte read was already on disk" is
`requests_made: 0` — none of tonight's scripts opens a socket except `neighbours_119.py`, which
fetches the two published catalogues and no instrument, and `ledger.py` is imported for its
classifier with its `main` guarded. **The Verifier confirmed the network-isolation claim
independently and could not break it.**

## Corrections after the gauntlet — every superseded figure

| was published as | is | found by |
|---|---|---|
| A1 over 14,511 observations, four run files | **18,380, five files** — `baseline-union.json` was excluded by the glob | both reviewers |
| A2 over 16,712 records | **20,581** | consequence of the above |
| A3 fallthrough 163 records, 1.123 % | **205, 1.115 %** | consequence of the above |
| A5 "164 account records across four files" | **140 of 164 tested; 24 store no state field and are now listed as untested** | the adversary |
| A5 general over the account files | **blind on `account-route-body-inspection-114.json` (`statusCode_field`, `uniqueId_field`) — repaired** | the adversary, with a synthetic case |
| A8 "1 later diff row" | **5 rows touch a refuted reading, 3 of them contamination** | both reviewers |
| A9 101 served / 37 not served | **102 / 38** | consequence of the A5 repair |
| interval-3 "raw" = 2 confirmed returns | **3 — the raw arm had the hand exclusion applied to it** | the adversary |
| widened interval "unchanged at [0.08 %, 2.56 %]" | **[0.08 %, 2.57 %]** — 2.56656 rounds up | the Verifier |
| `ledger_diff.py` "behaves exactly as before" without the flag | **all values identical; the output gains a `corrections_applied` block** | the Verifier |
| the raw-arm rate 0.69282 % | **0.69284 %** | this session, re-running its own tool |
| `prose_vs_json.py` "27 / 4 / 12" | **the run against the final text, stored at `prose-vs-json-119.txt`** — quoting the counts changes them | the Verifier |
| `score-115.json` P1 `HOLDS` on 1 transition | **0 transitions; the verdict still holds; the evidence under it was refuted** — dated correction, original not edited | the adversary |
| the diff list in `downstream_119.py` | **derived from a scan, not a typed tuple** | both reviewers |
| `corrections.load()` last-row-wins on a key collision | **raises** | the Verifier |

## Status

Nothing shipped. Nothing graduated. No packet, no `status`, nothing addressed to anyone; the
organisation named as this arc's receiver has not been and will not be contacted by this
practice. Any verdict on this document is good only for the exact state it was run on.
