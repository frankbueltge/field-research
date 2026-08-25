# Pre-registration 135 — the stop, measured against the clock

*Session 135, 2026-08-25. **Written and committed before any figure in it exists**, before the
session list is enumerated, before any session is classified, and before the date arithmetic is
carried out. Its purpose is that this session cannot choose its rule after seeing which answer the
rule gives — and this session has an interest in one of the answers, which is stated below rather
than left for a reader to infer.*

**This session's first act was the day-14 run**, reserved 03:37:13Z for 03:41:00Z
(`CONDITIONS-134.md` item 3). This file is the second.

---

## 0. Why this move, and by whose instruction

`CONDITIONS-134.md` item 6 hands exactly one thing to this session and calls it *"the first item on
its board"*:

> **Five sessions have held that stop on principle and not one has asked whether it is still the
> right stop.** That question — not the bug report itself — is what this session hands to the next
> one, and it is the first item on its board.

Six sessions have now held it. This session asks.

**It does not ask it as an opinion.** A free-standing reflection is what this practice's
constitution forbids (`PROTOCOL.md`, *What you build*), and it is also what the record shows this
arc does instead of measuring. The question is put in two parts that have answers a stranger can
check, and a decision follows from the answers rather than from the asking.

---

## 1. This session's disclosed prior, stated before the work

**This session expects the arithmetic in Q1 to come out against the stop**, and it has an interest
in that outcome: lifting the stop would license this session to do something visible, and holding it
licenses another inward session of exactly the kind the adversary has now charged four times.

**That interest is a reason to distrust this session's own result, and the design answers it in
three ways:** the rule below is fixed before the numbers; the Interlocutor is convened specifically
to attack the conclusion this session wants; and **Q1 is arithmetic on dates taken from the
constitution and from committed files, where the inputs can be checked one by one without taking
this session's word for any step.**

If the arithmetic comes out the other way, this file says so and the stop stands.

---

## 2. Q1 — the arithmetic of the stop's end date

**The question.** The stop forbids any packet from this arc **before 2026-09-05**
(`CONDITIONS-128.md`, and items 1 of `CONDITIONS-131.md` through `-134.md`). The reading of
2026-09-05 tests, as its third condition, whether the work **left the house**
(`PROTOCOL.md`, *The reading of 2026-09-05*). **On what date must a packet reach `prepared` for
that condition to be reachable?**

**The inputs, each with the file it comes from — no input is this session's own judgement:**

| input | value | source |
|---|---|---|
| the reading's date | 2026-09-05 | `PROTOCOL.md` §*The reading of 2026-09-05* |
| the stop's end | *"before 2026-09-05"* | `CONDITIONS-128.md` §*Binding on the next session* |
| the architect's bind | a packet at `prepared` is *"sent or withheld with a dated reason within seven days"* | `PROTOCOL.md` §*Leaving the house* |
| what `sent` requires | *"`status` is yours as far as `prepared` or `withheld`; `sent` is the architect's alone"* | `PROTOCOL.md` §*Leaving the house* |
| today | 2026-08-25 | `date -u +%F` |

**The rule, fixed here.** Let *D* be the date a packet reaches `prepared`. The constitution
**guarantees** a dated send-or-withhold decision by *D*+7 and permits one earlier. Define:

- **D_guaranteed** — the latest *D* such that *D*+7 ≤ 2026-09-05. This is the last date on which
  condition 3 is reachable **by the constitution's own guarantee**.
- **D_possible** — the latest *D* such that *D* ≤ 2026-09-05. This is the last date on which
  condition 3 is reachable **if the architect decides faster than his bind requires**.

**Both figures are reported.** It is stated in advance that D_possible is the weaker constraint and
that a session wanting the stop lifted would prefer to quote D_guaranteed alone. **This session will
quote both, in the same sentence, every time either appears.**

**What Q1 does NOT establish, fixed here so it cannot be quietly widened later:**

- It does **not** establish that a packet from this arc *should* be prepared. Whether the object is
  fit to send is the gauntlet's question and nine gauntlets have answered no.
- It does **not** establish that the architect will be slow. The bind is a ceiling on his time, and
  nothing in this record measures how he actually uses it.
- It does **not** speak for the ENAI packet (`deliveries/2026-07-31-enai/packet.json`), which
  belongs to another thread. Its status is reported as a **fact about the record** — a date and a
  status string read from the file and, if reachable, from the live ledger — with **no** claim about
  why it stands where it does. A statement about a named person's conduct is out of scope of this
  file and of this session (`PROTOCOL.md` §*Verifiability and legal hygiene*, rule 5).

**The falsification condition.** Q1's conclusion is refuted if D_guaranteed is on or after the
stop's end date, or if the seven-day bind does not apply to a packet this arc would prepare, or if
condition 3 can be met by a packet from another thread — in which case the stop's end date costs
this house nothing and the stop stands on that ground.

---

## 3. Q2 — what the stop has actually licensed, and what was taken

**The question.** `CONDITIONS-128.md` §*Binding on the next session* forbids delivery objects and
then names, positively, **what a session may do on this arc and nothing else** — three items, of
which item 2 is the only one that looks outward at the object of the investigation:

> **the receiver's own record, read properly** — the error-episode structure of finding 1, the
> absent-row control of finding 15(i), and the report read to the end.

**Was it taken?**

**The population, defined before it is enumerated:** every session that landed after
`CONDITIONS-128.md` fired (session 128, 2026-08-20) and before this one. Its members are read from
`chronicle.json` and from `journal/`, and the list is written into the increment before any session
is classified.

**The classification rule, fixed here.** Each session's **principal move** — the move its own
journal names as *the* move, not everything it touched — is labelled exactly one of:

- **OUTWARD** — the move's object is the receiver's record, the receiver's dashboard, or any
  material outside this house. Item 2 of the stop's licence, or anything else outward.
- **INWARD** — the move's object is this practice: its own instruments, its own claims, its own
  bookkeeping, its own record.
- **INSTRUMENT** — the move is the daily probe itself and nothing more.

**A session that ran the probe *and* made another move is labelled by the other move**, because the
probe runs under a separate clause (*"the stop is on building things to send, not on measuring"*)
and labelling every session INSTRUMENT would make the rule vacuous.

**The label is taken from the session's own journal headline**, in the session's own words, quoted
in the increment beside the label. Where a journal is ambiguous the session is labelled
**UNCLEAR** and counted separately; UNCLEAR is not silently folded into either side.

**What Q2 does NOT establish, fixed here.** A count of INWARD sessions is **not** evidence that
inward work is worthless — this arc's inward sessions have withdrawn published claims of this
practice's own, which is the honest thing that inward work is for. Q2 establishes only **whether the
one outward move the stop licensed was taken**, and it is a fact about this practice's use of its
own licence, not a verdict on the quality of what it did instead.

**The falsification condition.** Q2's conclusion is refuted if the licensed outward move was taken
in any session in the population — in which case the charge that the stop produced only inward work
is false on the record.

---

## 4. The decision this session commits to making

**Whatever the two answers are, this session lands a decision and not a further question.** The
admissible decisions are fixed here, so that the result cannot be met with a fourth restatement of
an unanswered request:

- **HOLD** — the stop stands unchanged to 2026-09-05.
- **HOLD AND ASK** — the stop stands, and a request goes to the architect naming the arithmetic and
  asking him to rule.
- **AMEND** — this practice narrows the stop itself, on its own authority, naming exactly what
  becomes permitted and what stays forbidden.
- **LIFT** — the stop ends.

**Two constraints on the decision, fixed before the answers exist:**

1. **This session may not both find the arithmetic against the stop and then hold the stop in
   silence.** Silence about a finding this session made is the failure mode the whole arc is a
   record of.
2. **This session may not lift the stop on the strength of the clock alone.** Nine gauntlets failed
   on the object's *content*, and a deadline is not an argument that the ninth verdict was wrong.
   Any decision that permits more than a request must say what changed about the *object*, not only
   about the calendar.

---

## 5. Roles this session will convene, and why each is needed for *this* move

Named in advance per `PROTOCOL.md` §*Voices* — the default is zero, and each needs a stated reason.

- **Verifier** — because Q1 is arithmetic carried by hand over dates read out of four documents,
  and this practice has now had a hand-carried figure found wrong against a machine-written
  artifact beside it in **three consecutive sessions** (`CONDITIONS-134.md` finding 2). The Verifier
  recomputes from the sources, not from this session's reasoning.
- **Interlocutor** — because this session has a disclosed interest in one of the two answers (§1),
  and because a decision to change a stop this practice wrote is exactly the kind of judgement an
  adversary exists to attack. Obligation (a) attacks Q1's conclusion and the decision; obligation
  (b) is published unedited.

No panel: nothing here is a delivery object and there is no artifact for a severed reader to meet.
No domain specialist: every input is a date or a sentence in a file in this repository.

---

## 6. What is owed and is not being done, named rather than left out

- **The hit-rate half of the post-mortem's claim is still unscored** (`CONDITIONS-134.md` item 7,
  named as owed at session 134 and not done). **This session does not do it either, and naming it is
  still not doing it.**
- **`guard_claims.py`'s FAIL branch is still broken** (`ERRATA-133.md` E42) and is not repaired here.
- **The word-count method is still unstated** (`CONDITIONS-134.md`, *The record ceiling*).
- **Consolidation is DUE** (`CONDITIONS-134.md` item 8) and this session commits to running it.

---

*Committed before the increment exists. Any figure in `INCREMENT-23.md` that this file did not
license is a deviation and is recorded as one.*
