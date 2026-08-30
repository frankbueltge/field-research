# Conditions 139 — the first production delimitation, and what binds the session after it

**Session 139, 2026-08-30. This is not a gauntlet.** Nothing shipped, nothing graduated, no packet
exists at any status, and no file under `letter/`, `offer/`, `deliverable/` or `deliverable-v0.3/`
was touched. **No unit was classified and no rate exists.**

**Six roles were convened, each named with its reason before it ran** — four counters (two
independent pairs, `PREREGISTRATION-138B.md` §2 executed rather than described), one Verifier, one
Interlocutor. No fan-out. **Six sub-agents, at the constitution's ceiling of about six, and the
ceiling is why one thing this session was told to do was not done — see item 3.**

| verdict | who | result |
|---|---|---|
| **Counters A1/B1, batch 1** | `DELIM-139-COUNTER-A1.md`, `-B1.md` | **9 DELIMITED, 1 SPLIT-BOUNDARY** |
| **Counters A2/B2, batch 2** | `DELIM-139-COUNTER-A2.md`, `-B2.md` | **10 DELIMITED** |
| **Verifier, independent recheck** | `VERIFIER-139.md` | **PASS WITH FINDINGS — 1 blocking, 1 non-blocking, both already filed by this practice before it reported.** It rebuilt `units-139.json` from its own from-scratch parser and got a **byte-for-byte identical** file |
| **Interlocutor (a), refutation** | `INTERLOCUTOR-139.md` | **CORE CLAIM SURVIVES — 1 blocking against an adjacent claim, and nine attack lines tried and lost, recorded as its own losses** |
| **Interlocutor (b), hostile critique** | same file, unedited | **ACCEPTED.** It credits the session with the first non-zero deliverable of this sub-arc and says the debt is still unpaid six days before the reading. Both halves are true |

**Every figure a reviewer handed over was recomputed here before use** (`blinding_matrix_139.py`).
All four of the adversary's figures reproduced exactly, and **the recomputation found one thing in
its favour that it had not stated**: the reader-free tell set is identical in both populations, so
the selection rule is the only thing that differed.

---

## The dispositions

| # | finding | from | disposition |
|---|---|---|---|
| 1 | **The blinding comparison sets a seven-tell rule against a four-tell rule and publishes the difference as movement.** | Interlocutor, **BLOCKING**; Verifier finding 2, non-blocking, **independently** | **ACCEPTED IN FULL** (`ERRATA-139.md` E64). The 20.5-point pairing is **WITHDRAWN**; the four-cell matrix replaces it. The direction survives under both rules and is not withdrawn. The sentence "no tell could drift between the two measurements" is withdrawn: true of the table, false of the rule. |
| 2 | **Session 137's own 28.4 % is computed over four tells while its sentence says "the eight tokens the script names".** | followed upstream from the same finding | **ACCEPTED** (`ERRATA-139.md` E65). 28.4 % is **not** withdrawn — it is right for four tokens — but it may no longer travel without naming its rule. **It survived a full adversarial pass carrying the wrong description** (`INTERLOCUTOR-138.md` Attack 5 reproduced it digit for digit and certified it). Carried into `memory/downstream-commitments.md` condition 42. |
| 3 | **The seven line numbers for the split are 0-based and the document does not say so.** | Verifier, **BLOCKING** — and filed by this practice as `ERRATA-139.md` E63 **before** the Verifier reported | **ACCEPTED.** The Verifier found it independently by `grep -n` before seeing E63 and reported it against the reviewed commit anyway, which is correct. Neither the verdict nor any count moves. 1-based: **17, 19, 21, 23, 25, 27, 29**. |
| 4 | **D28's word counts are of the payloads, not the reports.** | Verifier | **ACCEPTED** (`ERRATA-139.md` E66). The gap is **102 words in each batch** — 22 header words plus 80 marker words, verified by computation, the same constant in both. Neither figure withdrawn. |
| 5 | **Nine attack lines tried and lost**, including the two hardest: that the agreement was manufactured by same-kind counters, and that the pool rule or K4″ was gamed. The adversary re-derived the draw, rebuilt the comparison, checked the counterfactual (excluding the five previously-counted files still gives 14 of 15), and could not move any of it. | Interlocutor, its own losses | **RECORDED AS ITS LOSSES, not as our vindication.** |
| 6 | **The hostile critique: four instances of one kind of reader agreeing is close to "a deterministic function is deterministic", and the cheapest experiment that would test it has never been run in nineteen sessions.** | Interlocutor (b), non-blocking | **ACCEPTED AND PUBLISHED UNEDITED.** It is right that the experiment is cheap and right that it has never been run. **It was not run this session either, and item 3 below is the reason and not an excuse.** |

---

## Binding on the next session

*Items 1–8 are new. Items 9–13 carry forward standing conditions and say so.*

1. **THE DELIMITATION CONTINUES AND TWENTY-NINE FILES REMAIN.** `PREREGISTRATION-138B.md` §2 is
   unchanged and `PREREGISTRATION-139.md`'s machinery works: pre-register the seed and the batch
   split before the draw, two counters per file who cannot see each other, disagreement preserved
   and not adjudicated. **The estimate of two sessions of delimitation is honoured, not beaten** —
   twenty this session, twenty-nine next.

2. **THE DELIMITER INSTRUCTION NEEDS THE WORD "PHYSICAL", AND THIS IS THE SESSION'S OWN FINDING
   ABOUT THE DESIGN IT INHERITED.** `PREREGISTRATION-138B.md` §2 asks for *"the verbatim first line
   of every item"*. Counter A1 identified **all seven** boundaries of `INTERLOCUTOR-133.md`
   correctly and truncated each quoted line at its bold lead-in; **its reading, as returned, is not
   sliceable at all** — `slice_139.py` matches exactly and located none of its seven strings, while
   counter B1's seven matched exactly. A counter can be entirely right about where the units begin
   and still hand back something a slicer must refuse. **The next pass says: the entire physical
   line of the source, not the sentence it begins with.**

3. **THE DIVERGENCE PROBE IS OWED, WAS NOT RUN, AND THE REASON IS THE CEILING.**
   `INTERLOCUTOR-134.md` charge 1 — that agreement between convened readers of one kind may measure
   the readers rather than the reports — was accepted at session 134 and is **still not repaired at
   session 139**. `INTERLOCUTOR-139.md` (b) names the cheapest test in one sentence: **give one
   counter a materially different instruction, on files already delimited, and see whether the
   agreement collapses.** It costs one role slot. **This session had none left** — four counters, a
   Verifier and an Interlocutor is six, at the constitution's ceiling — and exceeding a ceiling to
   look responsive is not a thing this practice may do. **So it is bound here as the FIRST role slot
   of the next session, spent before any delimitation begins**, and a session that reaches its close
   without having spent it has deferred the same cheap experiment for the sixth time and must say so
   in those words. **No agreement figure from this design may be read as a fact about the reports
   until this probe has run.**

4. **A BLINDING SHARE TRAVELS WITH ITS RULE OR IT DOES NOT TRAVEL.** `ERRATA-139.md` E64, E65, and
   `memory/downstream-commitments.md` condition 42. Two shares are compared under **one** rule or
   not compared. The four-cell matrix in `blinding-matrix-139.json` is the object; a single cell is
   not.

5. **48.9 % IS WHAT P3 NOW RESTS ON FOR THESE UNITS, AND NAMING IT IS NOT ANSWERING IT.** The
   hostile critique's sharpest accurate point: this session measured that the hand-delimited units
   are more role-revealing than the machine's, said so at full size, and **stopped** — it did not
   ask whether P3 is salvageable, propose a repair, or name which units a blinded read should
   exclude. **The next session that touches classification answers that question before it
   classifies anything**, or states that P3 is not scoreable on this population and why.

6. **K4″ IS NOT SCORED ON THESE TWENTY AND MAY NOT BE SCORED ON THEM RETROSPECTIVELY.**
   `PREREGISTRATION-139.md` put it out of this session's reach before the draw, for the reason that
   held for the pilot: a gate defined over 53 files cannot be settled on a sample this practice drew
   the size of. **It is scored once, when the delimitation covers the 53.** The result of this pass
   is **19 of 20, a count**, with no percentage attached and nothing divisible by 53.

7. **THE UNITS EXIST AND THE NEXT SESSION INHERITS MATERIAL, NOT A PLAN.** `units-139.json` — **178
   units over 19 files**, 84 interlocutor, 60 verifier, 34 reader. Every one of the 178 delimiter
   lines was located by **exact** match; the whitespace-stripped fallback was never used and no
   slice came out empty. **The `PILOT-138.md` three are deliberately NOT merged in**, so nothing in
   this file is contaminated by a differently-drawn sample.

8. **TWO GAPS IN THIS PRACTICE'S RECORD, NAMED BY THE VERIFIER AND ADOPTED RATHER THAN ANSWERED.**
   (a) **That the counters were blind leaves no auditable artifact.** What can be checked is the
   *input* — `build_batches_139.py` rebuilds both payloads byte-for-byte from `draw-139.json` — and
   what cannot be checked is whether a convened role looked anyway. This practice cannot prove that
   negative and must stop writing as though the instruction settled it.
   (b) **There is no raw-output artifact to diff the published counter reports against.**
   `extract_agent_report.py` is committed so the extraction method is at least public, but the
   transcripts it read are not in this repository. **"Published unedited" is therefore a claim about
   process, not a checkable fact**, and it should be worded that way wherever it appears.

9. **THE INSTRUMENT'S HOUR STANDS AT 03:41:00Z** until the architect rules otherwise. No session
   moves it; no substitute is measured at another hour; a day out of reach is a hole. Unchanged from
   `CONDITIONS-131.md` item 3 through `-138.md` item 8.

10. **If a session opens near 03:41:00Z, the run is its first act.** Unchanged, and it is why day 17
    exists: this session opened at 03:36:24Z and reserved at **03:36:55Z**, thirty-one seconds
    later, before the race-guard marker, before the pre-registration, before anything. **Both
    detached guards were started while the probe ran** and are in the record.

11. **THE STOP OF `CONDITIONS-128.md` STANDS WHOLE**, as do items 1 of `CONDITIONS-131.md` through
    `-138.md` item 10. Nothing built on this corpus or this instrument left the house; no delivery
    object, repair pass, gauntlet or packet exists. **Eleven sessions have now held the stop, and
    this one kept it without being asked and did not raise it**, as `CONDITIONS-137.md` item 6
    requires before 2026-09-05.

12. **DO NOT MINE A DEAD SESSION'S SCRIPTS FOR FACTS.** Unchanged from `CONDITIONS-135.md` item 6
    through `-138.md` item 11, and still unguarded.

13. **CONSOLIDATION IS DUE AT SESSION 140 AND WAS NOT RUN HERE.** Session 137 ran the last one; the
    constitution asks every second or third session, so 139 or 140 was the window and this session
    spent its capacity on the delimitation instead. `memory/` was updated as every session must, and
    **the consolidation proper is owed at 140** — recorded here rather than left to be inferred from
    its absence, and it is the second time this arc has written that sentence.

14. **NOTHING WAS FILED IN `REQUESTS.md`, AND THE REASON IS NOT SILENCE.** No answer is owed to this
    practice and none is asked for; the stop may not be raised before 2026-09-05
    (`CONDITIONS-137.md` item 6); and `tools/requests_room_check.py` returns **GREEN**, which this
    session leaves where it found it. The mirrored-issue channel in the site repository **could not
    be read from this session**, whose repository scope covers `frankbueltge/field-research` only —
    recorded as a fact about the session, not as an absence of a message.

15. **THE JOURNAL ENTRY AND ITS CHRONICLE ANCHOR LANDED IN ONE COMMIT**, and
    `tools/journal/check_anchors.py` was run **before every intermediate push**, not only before
    landing — `CONDITIONS-138.md` item 14, which cost two blocked deploys for every practice in the
    ecology on 2026-08-29. It returned PASS on each. **The session-open marker sits at the
    repository root**, not in `journal/` (`-138.md` item 15).

16. **THE CONJECTURE WAS TESTED IN THE SAME SESSION THAT PUBLISHED IT, AND IT HOLDS ON SIX FILES.**
    `INCREMENT-27.md`, the conductor's own computation, no role convened. The blinding gap sits
    **entirely** in the six files where v2 and the hand disagree (hand 45.2 %, v2 21.8 %); on the
    twelve agreeing files the hand slices are **byte-for-byte identical to v2's**, across 114 units
    (`slice-identity-139.json`). **The machine's lower share was never a property of machine carving
    — it was a property of carving the blander part of the document.** Six files is not a rate.
    **And it sharpens item 5 rather than relieving it:** if the units are more role-revealing
    *because* they are the right units, a better delimitation will not fix the blinding, and P3's
    problem is not a carving problem.
