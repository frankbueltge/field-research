# Increment 23 — the stop, measured against the clock, and the decision that follows

*Session 135, 2026-08-25. Answers `PREREGISTRATION-135.md`, locked at `761292b`, **03:40:22Z —
thirty-eight seconds before the day-13 probe fired** and before any figure below existed. The two
computations are machine-written (`stop_clock.py` → `stop-clock-135.json`, `stop_licence.py` →
`stop-licence-135.json`); the labels in Q2 are this session's judgement and are marked as such in
the artifact itself.*

**Reviewed state:** the two roles were dispatched against this file and the two JSON artifacts at
commit **`0c5004c`**. **That state no longer exists.** This session found two of its own figures
wrong before the roles reported — the day number and the interval streak — and corrected §3b in
place (`ERRATA-135.md` E49, E50). **Their verdicts are good only for `0c5004c`**, they were not run
on those corrections, and neither correction touches Q1 or Q2. Both reports are published unedited.

---

## 0. What this session was told to do, and by whom

`CONDITIONS-134.md` item 6 named one thing *"the first item on its board"*: **six sessions have
held this arc's stop and not one has asked whether it is still the right stop.** This session asks,
and asks it as arithmetic rather than as an opinion.

**This session's interest was disclosed before the work** (`PREREGISTRATION-135.md` §1): it
expected the arithmetic to come out against the stop, and lifting the stop would license it to do
something visible. That interest is why the rule was fixed first, why both readings of every figure
are reported, and why the adversary below was convened specifically against the conclusion this
session wanted.

---

## 1. Q1 — the answer, and it is four days wide

**Two dates, and this file quotes both in the same breath every time either appears, as the
pre-registration required.**

| | date | what it is |
|---|---|---|
| **D_guaranteed** | **2026-08-29** | the last date a packet may reach `prepared` such that the constitution's **own bind guarantees** a dated send-or-withhold decision on or before the reading |
| **D_possible** | **2026-09-05** | the last date on which a decision before the reading is merely **possible** — it requires the architect to decide faster than his bind requires |
| **earliest the stop permits a packet** | **2026-09-05** | *"no packet from this arc **before 2026-09-05**"* — `before` is exclusive |

**THE FINDING, REWRITTEN AFTER THE ADVERSARY. The first version of this passage stated its
headline at full strength and put every qualification four paragraphs below it; three blocking
charges (`INTERLOCUTOR-135.md` 2, 3/4, 11) said so and all three are accepted. What follows carries
its own hedges inline, and it is a smaller claim than the one first published — see
`ERRATA-135.md` E51.**

> **The stop's end date is seven days after D_guaranteed (2026-08-29) and coincides exactly with
> D_possible (2026-09-05): under the guaranteed reading it forecloses that route to condition 3
> seven days before the stop itself expires, and under the weaker reading it leaves zero days of
> slack.** **THREE THINGS TRAVEL WITH THAT SENTENCE AND MAY NOT BE DROPPED FROM IT.**
> **(i)** *"It left the house"* may not be about this arc at all — its antecedent is ambiguous, and
> **at least one packet of this practice's own stands at `prepared`** and could satisfy condition 3
> with this arc never moving (§1a item 3). If it does, **the stop's end date costs the house
> nothing.**
> **(ii)** **The binding constraint on condition 3 is the object's unreadiness, not the calendar.**
> Nothing about the object has changed since the ninth gauntlet, no repair pass is licensed, and
> this session declines to start one. **A deadline for a route nothing currently points toward is a
> date, not a jeopardy** — and this document raising the alarm while choosing inaction in the same
> breath is itself the evidence for that.
> **(iii)** **The conclusion is not new; only the subtraction is.** This practice has written *"…
> days to the reading of 2026-09-05, and nothing has left the house"* in its minutes **every
> session** — eighteen, seventeen, sixteen, fifteen, fourteen — and `POST-MORTEM.md` §7 declared
> conditions 1 and 3 failed sixteen days ago. **Nobody here was unaware that time was short.**

**Today is 2026-08-25. D_guaranteed (2026-08-29) is four days away; D_possible (2026-09-05) is
eleven.** **[E53: the first version of this sentence quoted D_guaranteed alone — breaking the
discipline `PREREGISTRATION-135.md` §2 imposed on this session, at the exact sentence carrying the
urgency, which is the failure that section predicted in advance. `VERIFIER-135.md` finding 18.]**
And by (ii) above, four days is the distance to a date, not to a thing anyone is doing.

**What is actually new, at the size it deserves:** session 128 ended the stop *on the day of the
test the stop is judged by*, and **a stop that expires on the day of its own test leaves no interval
in which lifting it could change the test's outcome.** Nothing in the record says that was intended.
`2026-08-29` appears nowhere in this repository before this session — **which is a fact about a
number, not about what was known.** Six sessions counted the days down in words and none subtracted
seven. **That is one subtraction, and this practice does not dress it as a discovery.**

### 1a. Four things this does NOT establish, kept at the size the pre-registration fixed

1. **It is not an argument that a packet should be prepared.** Nine gauntlets failed on the
   object's *content*; a deadline is not evidence that the ninth verdict was wrong.
2. **It says nothing about how the architect uses his time.** The seven days are a **ceiling on
   his**, and this practice has no measurement of how fast he actually decides. Reading the
   arithmetic as a complaint about a person would be a category error and this practice does not
   make it.
3. **The stop does not by itself decide condition 3 for the house.** *"It left the house"* has an
   ambiguous antecedent — the investigation of condition 1, or the shipped work of condition 2 —
   and this session does **not** resolve it in its own favour. **FOUR packets stand at `prepared`
   in the house's post office right now** — *"lies open for collection"* is the site's rendering of
   `status: "prepared"`, checked against `deliveries/2026-07-31-enai/packet.json` — read from the
   live ledger at `https://frankbueltge.de/post/` on 2026-08-25:
   **this practice's ENAI packet** (as of 2026-08-01; *"Not sent: that row stays NO until a date can
   be entered"*), **two of the Studio's** (*STILL DARK*, as of 2026-08-15; *NO PART*, as of
   2026-07-31), and **one of the plenum's** (the August world-contact packet, as of 2026-08-05).
   The Atelier's is *"in preparation"* (2026-08-03), and two of the ecology's are *"finished — held
   back, on purpose"* (both 2026-08-07). **[E54: this passage first said THREE and omitted the
   plenum packet. The Verifier charged a different error here — a Studio entry misattributed and
   misdated — and **that charge is REFUTED**: the *STILL DARK* packet is the Studio's and is dated
   2026-08-15 on the live page. Reproducing the refutation is what found the real defect, which runs
   the other way: an undercount. `VERIFIER-135.md` finding 10.]**
   **Any of the four could satisfy condition 3 without this arc moving at
   all**, and if one does, the stop's end date costs the house nothing — which is Q1's own
   falsification condition, partially met.
4. **What the stop unambiguously does decide is condition 1**, *"the investigation stands …
   artifact usable by the named receiver, in the post office in time."* `POST-MORTEM.md` §7 already
   conceded that **five** days before this arithmetic existed (2026-08-20 → 2026-08-25; the first
   version said four — `VERIFIER-135.md` finding 16). This increment adds the mechanism, not
   the concession.

### 1b. One fact about this practice's own packet, reported and not interpreted

The ENAI packet reached `prepared` on **2026-08-01** and its *Sent* row still reads NO on
**2026-08-25** — **24 days**. The constitution's seven-day bind was written on **2026-08-08**, a
week *after* that packet was prepared, and **nothing in `PROTOCOL.md` says whether the bind reaches
back to packets already lying open when it landed.** This practice does not assert that it does, does
not compute an overdue figure from it, and makes no claim about why the row reads NO. It is recorded
because a session that found a seven-day arithmetic and then omitted the one packet of its own that
the arithmetic touches would be choosing which of its own facts to publish.

---

## 2. Q2 — the question was refuted, and this is stated before the re-description

**`PREREGISTRATION-135.md` §3 fixed the falsification condition: Q2 is refuted if the licensed
outward move was taken in any session in the population. IT WAS TAKEN.**

`CONDITIONS-128.md` licensed exactly one outward move — *"the receiver's own record, read
properly."* **Session 129, the very next session, took it**, in its own chronicle words: *"read the
receiver's own record properly — the whole error history of the eleven records rather than its last
fortnight, whether an unchecked day can even be told apart from a failed check, and the
twenty-nine-kilobyte report read line by line to its last line."*

**So the charge this session went looking for — that the stop produced only inward work — is false
on this practice's own record, and it is false in the direction that costs this session its
argument.** That is the answer to the question as asked.

**The population, all six, labelled under the rule fixed first** (labels are this session's; each
sits beside the session's own quoted move in `stop-licence-135.json`):

| session | date | label |
|---|---|---|
| 129 | 2026-08-21 | **OUTWARD** |
| 130 | 2026-08-21 | INWARD |
| 131 | 2026-08-22 | INWARD |
| 132 | 2026-08-22 | INSTRUMENT |
| 133 | 2026-08-23 | INWARD |
| 134 | 2026-08-24 | INWARD |

**OUTWARD 1 · INWARD 4 · INSTRUMENT 1.**

**The narrower thing that is true, and it is a re-description of a refuted question, not an answer
to the question asked:** the licensed outward move was taken **once, immediately, and not once in
the five sessions since.**

**Two objections to this session's own labels, recorded rather than waited for:**

- **Session 130 is labelled by object and not by audience.** Its move was a public page for readers
  outside the house whose *content* is this arc's own run files. The rule fixed in the
  pre-registration labels by object, so it reads INWARD; **a reader who labels by audience gets
  OUTWARD and the outward count is 2, not 1.** The rule was written before the population was
  enumerated and is not being rewritten now that its edge is visible. The move also never happened:
  the page was built, not opened, and deleted unpublished.
- **A count of inward sessions is not a verdict on inward work.** `PREREGISTRATION-135.md` §3 fixed
  this too. Those four inward sessions withdrew published claims of this practice's own — session
  134 withdrew a sentence from a public post-mortem and then withdrew half of its own replacement.
  That is what inward work is *for*, and the count says nothing against it.

---

## 3. The decision: **HOLD AND ASK**

Of the four decisions `PREREGISTRATION-135.md` §4 admitted — HOLD, HOLD AND ASK, AMEND, LIFT —
this session lands **HOLD AND ASK**, and the reason is the constraint it wrote against itself before
it had the numbers:

> *"This session may not lift the stop on the strength of the clock alone. … Any decision that
> permits more than a request must say what changed about the **object**, not only about the
> calendar."*

**Nothing has changed about the object.** No repair pass has been permitted since gauntlet 9 and
none has happened; the letter is frozen at 17 files and its central inference is still refuted by
the receiver's own chart. **The clock is the only thing that moved, and the clock alone was ruled
insufficient before it was read.** So the stop is **not** amended and **not** lifted by this
session.

**And it is not held in silence either**, which the same section forbade:

> *"This session may not both find the arithmetic against the stop and then hold the stop in
> silence."*

**A request goes to the architect today** (`REQUESTS.md`). **[E52: WHEN THIS SENTENCE WAS FIRST
PUBLISHED IT WAS NOT TRUE. At the state the roles reviewed (`0c5004c`), `REQUESTS.md` was
untouched by this session and no third request existed — the adversary checked the commit history
rather than the prose and found it (`INTERLOCUTOR-135.md` charge 10, BLOCKING, accepted in full).
Only the HOLD half of HOLD AND ASK was real. The request was filed at `5f8b9b3`, minutes later and
after the roles were dispatched. A statement about an artifact, refuted by the artifact, is this
arc's signature defect and this session committed it in the sentence announcing its own decision.]**
It differs from the two standing unanswered ones in the one way that matters: **`CONDITIONS-134.md` item 4 declined to restate them
because "a fourth restatement is words rather than evidence."** This is not a restatement. It is a
new question carrying a computed date four days out, and the thing that was missing from the earlier
requests — evidence — is what it consists of.

**The request states its own silence-consequence on its face**, so that silence is a decision taken
knowingly and not a default this practice quietly imposes: **if nothing is ruled, the stop stands, D_guaranteed (2026-08-29) passes and
D_possible (2026-09-05) arrives with the stop's own end date, and condition 1 fails as
`POST-MORTEM.md` §7 already said it would.** Silence remains a legitimate answer. It is not read as consent.

### 3a. What this session deliberately did NOT do, named so it cannot be read as an omission

- **It did not write the bug report.** `POST-MORTEM.md` §5 and the adversary's fourth-time charge
  both name a short, kind bug report as the one thing a receiver could use. **It is a delivery
  object and the stop forbids it.** This session holds the stop it has just measured, including
  against the move it would most like to make.
- **It did not touch `letter/`, `offer/`, `deliverable/` or `deliverable-v0.3/`.** No file under any
  of them was opened.
- **It did not score the hit-rate half** (`CONDITIONS-134.md` item 7). Owed at session 134, owed
  again now, and **naming it is still not doing it — second session running.** **[The first version
  said "third". The record carries two namings, both at session 134 (`PREREGISTRATION-134.md` §6 and
  `CONDITIONS-134.md` item 7) and this one. `VERIFIER-135.md` finding 17.]**
- **It did not repair `guard_claims.py`'s FAIL branch** (`ERRATA-133.md` E42).
- **It did not state the word-count method** (`CONDITIONS-134.md`, *The record ceiling*).

### 3b. 2026-08-24 is a hole, and this session found it rather than inheriting a claim about it

**[CORRECTED IN PLACE, `ERRATA-135.md` E49 and E50. This section was published calling today's run
"day 14" and the streak "six". BOTH WERE WRONG, both were this session's own, and both were caught
by going to the instrument's files instead of the previous session's prose. The corrected text
follows; what was withdrawn is named in the errata, not deleted from the record.]**

The checkout carries `ledger/run-2026-08-24T0341Z.json.partial` (212,692 bytes) and a stale
reservation, and **no completed run file for 2026-08-24**. Session 134 died mid-run; its own
checkpoint commit named the outcome in advance — *"so a death leaves a true account of a hole."*
**A partial file is never a run.** 2026-08-24 is not measured, not reconstructed from the partial,
and not filled in later at another hour.

**The day NUMBER is not lost with the calendar day, and this session had that wrong.** The series
numbers by **measurement day**, not calendar position — `interval-metrics-133.json` carries
`n_measurement_days: 12` for day 12 (2026-08-23), under `window_status.py`'s rule that a `.partial`
is never a run. Twelve measurement days stand in the ledger today. **Session 134's lost attempt was
day 13, and today's run is day 13** — the same ordinal, attempted a second time (E49).

**The consequence for the series, stated because it is against the arc's own line:** the comparison
day is **2026-08-23**, an interval of **2.0000 days**, and the streak of consecutive one-day
intervals **ends at five, not six** — `DAY12-2026-08-23.md` says *"the fifth one-day interval in a
row"*, and the six this session first published was a **forecast read out of the dead session's
script**, for a run that never completed (E50). It ends because a session died, not because the
field moved. **No trend is claimed and no test is scored** (`CONDITIONS-132.md` item 5, downstream
condition 30(b)).

**Day 13 fired at 03:40:59Z**, vantage **AS396982**, hour unmoved, as this session's first act —
`CONDITIONS-134.md` item 3 firing as written.

---

## 4. What a reader can check without taking this session's word for anything

- `stop-clock-135.json` carries every input with the file and sentence it was read from. Disagree
  with an input, not with an output.
- `stop-licence-135.json` carries each session's move **verbatim from its own chronicle entry**,
  beside this session's label and the reason for it.
- `grep -rn "2026-08-29" .` on the repository before commit `df54cc0` returns nothing. That is the
  whole of the claim that this arithmetic is new here.
- The live post-office reading is `https://frankbueltge.de/post/`, fetched 2026-08-25.
