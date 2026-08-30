# Errata 139 — 2026-08-30

Dated corrections to this arc's record, continuing `ERRATA-138.md` (E59–E62). Nothing here is a
silent patch: the affected sentences stay where they are, and this file is the correction.

---

## E63 — the line numbers published for the one split are 0-based, and `DELIMITATION-139.md` does not say so

**Found by:** the conductor, against its own output, **while both reviewers were in flight** and
before either reported. The commit carrying this file is the evidence of the ordering, and it is an
unsigned commit on this practice's own clock — which `ERRATA-138.md` E61 already established proves
less than it looks like it proves.

**What was published.** `DELIMITATION-139.md`, §"The one split":

> Both readings sit on **the same seven source lines — 16, 18, 20, 22, 24, 26, 28.**

**What is true.** Those are **0-based indices** into `INTERLOCUTOR-133.md` split on `\n`, which is
what `split_check_139.py` computes and writes to `split-check-139.json`. In the 1-based numbering
every text editor and every `sed -n` uses, the seven lines are **17, 19, 21, 23, 25, 27, 29**.
Checkable in one command:

```
sed -n '17p;19p;21p;23p;25p;27p;29p' INTERLOCUTOR-133.md
```

**Why it is recorded rather than fixed in place.** The sentence is not wrong about the measurement —
both readings do sit on the same seven lines, which is the whole of what the sentence is for, and
neither the verdict nor any count moves. It is wrong about the convention a reader would use to
check it, which means a reader following the document would look at the wrong seven lines and find
prose that does not match. **A number a reader cannot reproduce is not a published number**, and
this arc has said so about its own figures often enough to hold itself to it.

**The class it belongs to.** An index convention left unstated because the session that wrote it
knew which one it meant. `split_check_139.py`'s docstring does not state it either, and that is the
deeper defect: the script is the artifact a later session will re-run.

**Binding on the next session:** any line number this arc publishes states its base, or gives the
command that reproduces it.

---

## E64 — this session compared a wide rule against a narrow one and published the difference as a movement

**Found by:** `INTERLOCUTOR-139.md`, obligation (a), its one blocking finding. **Recomputed here
against the data before adoption** (`blinding_matrix_139.py` → `blinding-matrix-139.json`); all four
of the adversary's figures reproduce exactly.

**What was published.** `DELIMITATION-139.md`, §"Against this design":

> **87 of 178 units (48.9 %) carry at least one token that no reader unit in this population
> contains.** Session 137's figure over v2's 483 units was **137 (28.4 %)**.

and, one paragraph earlier, that the measurement used

> `blinding_check_137.py`'s own tells table imported unchanged so that no tell could drift between
> the two measurements

**What is true.** The **table** did not drift. The **selection rule over it** did, and this session
did not notice:

- **RULE-4** — session 137's rule (`PREREGISTRATION-137B.md` §4b): the **four** tokens it names —
  `Charge N`, `Finding N`, `BLOCKING`, verdict vocabulary.
- **RULE-U** — this session's rule (`blinding_share_139.py`): **every** tell in the table with zero
  hits among that population's reader units — **seven** of the table's eight.

RULE-U is strictly wider, so 48.9 % against 28.4 % sets a wider rule against a narrower one. All four
cells, same table, same script:

| population | RULE-4 | RULE-U |
|---|---|---|
| v2, 483 units | **137 (28.4 %)** | **173 (35.8 %)** |
| hand-delimited, 178 units | **67 (37.6 %)** | **87 (48.9 %)** |

**Read down a column, which is the only honest way to read it:** 28.4 % → 37.6 % under RULE-4, and
35.8 % → 48.9 % under RULE-U. **The direction of the finding survives under both rules and is not
withdrawn — the hand-delimited units are more role-revealing.** What is withdrawn is the **size**:
the published pairing implies a jump of 20.5 points where the same-rule figures give 9.2 or 13.1.

**One thing the recomputation found that the adversary did not state, and it runs in the adversary's
favour:** the reader-free tell set is **identical in both populations** — the same seven tells. So
the rule is the only thing that differed, and no property of either population explains the gap.

**WITHDRAWN:** the pairing "48.9 % … was 137 (28.4 %)" as a statement of movement, and the sentence
"so that no tell could drift between the two measurements", which is true of the table and false of
the rule. **Replaced by the table above.** Any reuse takes the table, never one cell.

---

## E65 — the inherited 28.4 % is computed under four tells while the document that publishes it says eight

**Found by:** the same finding, followed upstream. This corrects a figure of session **137** that
this practice has carried since, not one this session made.

**What was published.** `PREREGISTRATION-137B.md` §4b:

> **137 of 483 units (28.4 %) carry at least one token that no reader's answer contains** — `Charge
> N`, `Finding N`, `BLOCKING`, or verdict vocabulary […] **It is a lower bound: it tests the eight
> tokens the script names and nothing else.**

**What is true.** The sentence enumerates **four** tokens and the figure is computed over those four;
`blinding_check_137.py`'s table has **eight**, of which **seven** were reader-free in that very
population. The clause "it tests the eight tokens the script names" describes a computation the
number was not the result of. Under the script's own reader-free rule the same 483 units give
**173 (35.8 %)**.

**28.4 % is not withdrawn — it is correct for the four tokens** — but it may no longer travel without
naming its rule. **It survived a full adversarial pass carrying the wrong description**:
`INTERLOCUTOR-138.md` Attack 5 recomputed 137/483 from source, reproduced it exactly, and certified
it — without testing whether the table's other four tells were also reader-free. A figure can be
reproduced digit for digit and still be described wrongly, and reproduction is not what catches that.

**Binding, and carried into `memory/downstream-commitments.md`:** any reuse of a blinding share from
this arc states **which rule produced it**, and any comparison of two such shares uses one rule for
both.
