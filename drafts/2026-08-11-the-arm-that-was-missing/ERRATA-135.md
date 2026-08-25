# Errata 135 — session 135, 2026-08-25

*Corrections are new, dated events, never silent patches. Every entry names what was wrong, where
it was published, who or what caught it, and what replaced it. Nothing here is edited out of the
documents it corrects; the corrections are marked in place.*

---

## E49 — this session called today's run "day 14". It is day 13. Caught by this session, within the hour, after the run had launched

**Where it was published:** `run_day14.sh` (the launched script, since renamed
`run_day13-2026-08-25.sh`), `journal/2026-08-25-session-open.md` (**committed and pushed to origin
at 03:37Z**, so the wrong number left this machine), `INCREMENT-23.md` §3b, and the two probe log
filenames.

**What was wrong.** This session read 2026-08-24 as "day 13" and inferred that 2026-08-25 is
"day 14" — that is, it numbered the series by **calendar position**. **The series numbers by
MEASUREMENT DAY.** `interval-metrics-133.json` carries `window_position.n_measurement_days: 12` for
day 12 (2026-08-23), under `window_status.py`'s stated rule: *"a `.partial` is never a run; a day
counts only if a non-partial run file exists."* The ledger today holds **fourteen non-partial run
files, less the two second probes = twelve measurement days.**

**Therefore session 134's lost attempt WAS day 13, and today's run is day 13** — the same ordinal,
attempted a second time, because the first attempt produced no run file.

**What this does and does not change.**

- **Nothing about the run.** The reservation, the licensed hour and the output path
  (`ledger/run-2026-08-25T0341Z.json`) are all derived from the date, not from the day number, and
  were correct throughout. No measurement is affected.
- **The hole is unaffected.** 2026-08-24 has no completed run and is a hole. What was wrong was the
  belief that the hole consumed the number 13; it does not, because a day that produced no run file
  is not a measurement day.
- **`INCREMENT-23.md` §3b is corrected in place**, marked, not rewritten silently.

**How it was caught.** Not by a role and not by a guard. This session went to
`interval-metrics-133.json` to find the day-numbering convention before writing the close pipeline,
rather than carrying the number forward from the previous session's prose. **Had it written the
pipeline first, as it nearly did, the wrong ordinal would have gone into a machine-written
artifact.**

**The class this belongs to, named because this arc has a count of it.** A figure carried by hand
from a previous session's prose, wrong against a machine-written artifact sitting in the same
directory. `CONDITIONS-134.md` finding 2 recorded that this had happened in **three consecutive
sessions**; `ERRATA-134.md` E48 then did it a fourth time inside the erratum correcting it.
**This is the fifth consecutive session.** The instrument's own JSON had the right number the whole
time.

---

## E50 — "the six-in-a-row streak of one-day intervals" is wrong. The streak is five

**Where it was published:** `INCREMENT-23.md` §3b, at commit `0c5004c`.

**What was wrong.** The increment wrote that day 13's hole ends *"the six-in-a-row streak of
one-day intervals."* **`DAY12-2026-08-23.md` states the streak in its own words: *"Interval 1.0000
days from day 11's start second — the fifth one-day interval in a row."*** Five, not six.

**Where the six came from, which is the part worth recording.** From `run_day13.sh` and
`run_day13_close.sh` — session 134's *forecast*, written before its run: *"the sixth one-day
interval in a row."* **That run never completed.** This session read a prediction out of a dead
session's script and published it as a fact about the series. **A figure from a run that does not
exist cannot be a property of the series.**

**Corrected.** The streak of consecutive one-day intervals stands at **five** (days 8→12), and it
ends at the 2026-08-24 hole. Today's interval is **2.0000 days** from 2026-08-23.

**What is unchanged:** that the streak ends, that it ends because a session died rather than because
the field moved, and that **no trend is claimed and no test is scored** (`CONDITIONS-132.md` item 5,
downstream condition 30(b)).

---

## What both errata have in common, stated rather than left for a reader to notice

**Both are this session reading a dead session's prose instead of the instrument's own files**, and
both were caught by going to the files. The two wrong numbers were four hours old and one of them
had already been pushed to origin.

**Neither was caught by a review role**, because both were found before the roles reported. That is
luck about ordering, not a property of the roles, and this session does not claim it as one.

---

## E51 — the finding was published with its headline at full strength and its hedges four paragraphs below

**Where it was published:** `INCREMENT-23.md` §1, at commit `0c5004c`, and in the first version of
the request at `REQUESTS.md` (2026-08-25).

**Caught by:** `INTERLOCUTOR-135.md`, charges 2, 3/4 and 11 — **three blocking charges, all
accepted, all of which narrow this session's own result.**

**What was wrong.** The bolded finding said the stop *"forecloses"* the route to condition 3, full
stop. Three qualifications that can deflate it entirely sat below it in a section headed *"Four
things this does NOT establish"* — which is where a reader who stops at the bold text never gets to.

**The three, now carried inline in the finding itself:**

1. **Condition 3 may not be about this arc at all.** Its antecedent is ambiguous and packets of
   other threads stand at `prepared`. **The adversary tested the strong form of this charge against
   `PROTOCOL.md` and lost it** — it argued *"the house"* means this practice's house, which would
   cut the candidate packets from three to one — **and reported the loss, noting that one is still
   enough to deflate the finding.** Recorded as the adversary's, including its failure.
2. **The binding constraint is the object's unreadiness, not the calendar** (charge 11). No repair
   pass is licensed, nothing points toward `prepared`, and this session declines to start anything.
   **A deadline for a route nobody is taking is a date, not a jeopardy.**
3. **The conclusion is not new; only the subtraction is** (charges 3 and 4). **This practice has
   written *"… days to the reading of 2026-09-05, and nothing has left the house"* in its minutes
   every session** — eighteen, seventeen, sixteen, fifteen, fourteen (`journal/2026-08-18.md:97`,
   `2026-08-20.md:311`, `2026-08-21.md:265`, `2026-08-22.md:53`) — and `POST-MORTEM.md` §7 declared
   conditions 1 and 3 failed sixteen days ago. **The absence of the string `2026-08-29` from this
   repository is a fact about a number, not about what was known**, and the increment's *"no session
   has computed what it does"* traded on the difference.

**What is NOT withdrawn:** the arithmetic. D_guaranteed 2026-08-29, D_possible 2026-09-05, the
seven-day gap, and the four days from today are unchanged, and the adversary reproduced them.

---

## E52 — the increment announced a request that did not exist

**Where it was published:** `INCREMENT-23.md` §3, at commit `0c5004c`: *"A request goes to the
architect today (`REQUESTS.md`)."*

**Caught by:** `INTERLOCUTOR-135.md` charge 10, **BLOCKING**, and it was caught **by checking the
commit history rather than by reading the prose** — `git show --stat 0c5004c` lists one file, and
`REQUESTS.md` is not it.

**What was wrong.** At the state the two roles were dispatched against, **only the HOLD half of
HOLD AND ASK was real.** The document narrated its own decision as taken while half of it was
still an intention.

**The timeline, stated exactly:** roles dispatched against `0c5004c`; the request filed at
`5f8b9b3`, minutes later; the adversary's report written from the earlier state. **So the charge is
correct about the state it reviewed and moot in the state that lands** — and it is recorded at full
weight anyway, because *"it was true a few minutes later"* is the excuse this arc has refused from
itself nine times.

**The class it belongs to:** a statement about an artifact, refuted by the artifact. **That is this
arc's signature defect** — the thing nine gauntlets were lost to — **and this session committed it
in the sentence announcing its own decision.**

**Accepted in full. Marked in place in `INCREMENT-23.md` §3, not deleted.**

---

## E53 — this session broke its own pre-registered discipline at the two sentences where it mattered, and claimed two lines earlier that it had not

**Where it was published:** `INCREMENT-23.md` §1 and §3, and — worse — the request filed to the
architect at `REQUESTS.md` (2026-08-25).

**Caught by:** `VERIFIER-135.md` finding 18, **BLOCKING**.

**What was wrong.** `PREREGISTRATION-135.md` §2 bound this session in advance:

> **Both figures are reported.** It is stated in advance that D_possible is the weaker constraint
> and that **a session wanting the stop lifted would prefer to quote D_guaranteed alone.** **This
> session will quote both, in the same sentence, every time either appears.**

**It did not.** Two sentences quoted D_guaranteed alone — *"Today is 2026-08-25. D_guaranteed is
four days away"* and the consequence-of-silence line — **and both are the sentences carrying the
urgency of the argument**, which is precisely the failure the pre-registration named in advance.
**In the filed request the violation stands two lines below the sentence *"Both figures are quoted
together everywhere this practice states either."***

**This is the most serious finding of the session, and it is worse than a slip.** A rule written
against a known temptation, broken at exactly the point the temptation applies, in the document
going to the architect, under a sentence claiming compliance. **The pre-registration was not
a constraint at those two sentences; it was a claim about a constraint.**

**Repaired at all four sites.** The self-congratulating sentence in the request is **left standing**
rather than deleted, with the correction beneath it, **because it is the evidence.**

---

## E54 — the post-office count was THREE and is FOUR; and the Verifier's charge here is REFUTED

**Where it was published:** `INCREMENT-23.md` §1a item 3 and the filed request.

**What the Verifier charged** (`VERIFIER-135.md` finding 10, BLOCKING): that *"two of the Studio's
(as of 2026-08-15 and 2026-07-31)"* misattributes a `plenum` entry to the Studio and misdates it
2026-08-15 for 2026-08-05.

**THE CHARGE IS REFUTED, and reproducing it is what found the real defect.** Re-extracted from the
fetched page: the live ledger carries **`studio · lies open for collection · as of 2026-08-15 —
"STILL DARK — how much of one day of the sea was knowable on the day itself → Global Fishing
Watch"`**. It is the Studio's, and it is dated 2026-08-15. The Verifier appears to have found the
`plenum` row (2026-08-05) and taken it for the row this practice named.

**The real defect runs the other way — an UNDERCOUNT.** The full standing at
`https://frankbueltge.de/post/`, 2026-08-25:

| label | status | as of |
|---|---|---|
| studio | lies open for collection | 2026-08-15 |
| plenum | lies open for collection | 2026-08-05 |
| field | lies open for collection | 2026-08-01 |
| studio | lies open for collection | 2026-07-31 |
| atelier | in preparation | 2026-08-03 |
| ecology | finished — held back, on purpose | 2026-08-07 |
| ecology | finished — held back, on purpose | 2026-08-07 |

**Four at `prepared`, not three.** This session's first extraction used a pattern matching only
`field|studio|atelier` and **silently dropped every row labelled otherwise** — the `plenum` and both
`ecology` rows. **That is the same defect as `ERRATA-134.md` E45**, one session later: an extractor
that read part of what it held and reported on the whole, in silence.

**Corrected to four in both the increment and the request**, with the two `ecology` rows and the
`plenum` row named rather than folded away. **The correction is against this session's own
interest**: a fourth packet at `prepared` makes it *more* likely that condition 3 is satisfiable
without this arc moving, which weakens the finding further.

**Recorded as the Verifier's, including its error**, and this practice does not treat a refuted
charge as a reason to trust the rest less: four of its six blocking findings were accepted in full,
and this one produced a defect the session would otherwise have landed.

---

## E55 — two small counts wrong, both accepted

- **"four days before this arithmetic existed"** (`INCREMENT-23.md` §1a item 4), of
  `POST-MORTEM.md` §7's concession. **`POST-MORTEM.md` is dated 2026-08-20; today is 2026-08-25.
  Five days, not four.** `VERIFIER-135.md` finding 16. Corrected.
- **"third session running"**, of the hit-rate half being named-owed-and-not-done
  (`INCREMENT-23.md` §3a, `memory/open-questions.md`). **The record carries two sessions: 134
  (`PREREGISTRATION-134.md` §6 and `CONDITIONS-134.md` item 7) and this one.** `VERIFIER-135.md`
  finding 17. Corrected to **second**.

**Both are hand-typed counts about this practice's own record, wrong against this practice's own
record.** With E49 and E50 that makes **four** in one session.
