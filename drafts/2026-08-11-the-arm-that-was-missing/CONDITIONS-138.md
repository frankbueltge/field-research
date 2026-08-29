# Conditions 138 — the second fired gate, and what binds the session after it

**Session 138, 2026-08-29. This is not a gauntlet.** Nothing shipped, nothing graduated, no packet
exists at any status, and no file under `letter/`, `offer/`, `deliverable/` or `deliverable-v0.3/`
was touched. **No unit was classified and no rate exists.**

**Three roles were convened, each named with its reason before it ran.** One independent counter
(`CONDITIONS-137.md` binding item 3, firing for the first time), one Verifier, one Interlocutor.
No fan-out. **Three sub-agents in total, against the constitution's ceiling of about six.**

| verdict | who | result |
|---|---|---|
| **Independent counter, K4′** | `HANDCOUNT-138.md` | **2 of 5 disagree → K4′ FIRES → NO RATE.** Published unedited; recomputed here against the files before adoption |
| **Verifier, independent recheck** | `VERIFIER-138.md` | *(filled at the close of the session)* |
| **Interlocutor (a), refutation** | `INTERLOCUTOR-138.md` | *(filled at the close of the session)* |
| **Interlocutor (b), hostile critique** | same file, unedited | *(filled at the close of the session)* |

---

## Binding on the next session

*Items 1–6 are new. Items 7–11 carry forward standing conditions and say so.*

1. **NO THIRD EXTRACTOR.** `PREREGISTRATION-138B.md` §1 is binding, including its escape clause: the
   ban is lifted only by a gate on files drawn under a seed stated in advance and hand-counted by a
   role that did not write the repair. Two extractors have now failed the pre-registered gate, on
   fresh files both times, and the second failed on the two defects its own docstring says it was
   built to repair.

2. **THE REPLACEMENT IS HAND DELIMITATION, TWO COUNTERS PER FILE, AND DISAGREEMENT IS NOT
   ADJUDICATED.** `PREREGISTRATION-138B.md` §2 and K4″ in §5. The cost is stated in §6 and is not a
   licence to defer: **two sessions of delimitation and one of classification.** A session that
   claims to have done it in fewer has cut something and must say what.

3. **THE COUNTING CRITERION IS UNDER-DETERMINED AND A LATER SESSION MUST NOT SETTLE IT AGAINST KNOWN
   EVIDENCE.** `HAND-AUDIT-137.md` §3's rule does not decide between an item-by-item checklist and a
   findings list in a verification report. Two instruments that could not see each other found it
   the same day (`carve_audit_138.py`'s validation failure on `VERIFIER-133.md`; the convened
   counter's MEDIUM-confidence note on `VERIFIER-125.md`). This session **saw which files it moves**
   and therefore declined to write the rule. Whoever writes it must write it **before** looking at
   which files it moves, and say so in the same document.

4. **`carve_audit_138.py`'s VALIDATION FAILS AND IT MUST NOT BE TUNED TO PASS.** It exits 1 on
   `VERIFIER-133.md`. The failure is the informative part of it — it located the criterion defect in
   item 3. **Any session that makes it exit 0 must show that it did so by a rule written before
   seeing which files it moves**, or it has done to the auditor what this arc twice refused to do to
   the extractor. It also may never be used to choose units.

5. **`MIN_UNITS = 3` DROPS WHOLE PASSES FROM A PER-PASS STATISTIC, AND THE DIRECTION OF THAT BIAS IS
   KNOWN.** Found by running `carve_audit_138.py` and then opening the two files it reports
   UNEXTRACTABLE — not by reading either script. `VERIFIER-124.md` is not uncarvable: it states
   **exactly two** findings, `### Blocking — B1:` and `### Non-blocking — N1:`, and the extractor's
   floor of three units drops it. `INTERLOCUTOR-16.md` enumerates nothing at all and is uncarvable in
   the ordinary sense. **The two cases are reported under one label**, and the label reads as a
   property of the report rather than of the threshold.
   **The consequence is not cosmetic.** The study's primary statistic is *passes producing at least
   one class-A unit ÷ that role's passes*. A floor that removes passes **for having few findings**
   removes, preferentially, the passes least likely to contain an A — so the denominator loses
   exactly the cases that would pull the rate down. **Any future design must either count a
   one-or-two-finding report as a pass or state the exclusion and its direction beside the rate.**
   `PREREGISTRATION-138B.md` §2 has no such floor and must not acquire one silently.

6. **THE DEBT IS UNPAID AND ITS AGE MUST BE STATED WITH ITS READING.** The hit-rate half of
   `POST-MORTEM.md` §8 Q1 was named as owed at session 134 and is unpaid at the close of 134, 135,
   136, 137 and 138. **This session published the count two different ways in two of its own
   documents** (`ERRATA-138.md` E59). A later session states the reading with the number or does not
   state the number.

7. **THE INSTRUMENT'S HOUR STANDS AT 03:41:00Z** until the architect rules otherwise. No session
   moves it; no substitute is measured at another hour; a day out of reach is a hole. Unchanged from
   item 3 of `CONDITIONS-131.md` through item 4 of `-137.md`.

8. **If a session opens near 03:41:00Z, the run is its first act.** Unchanged, and it is why day 16
   exists: this session opened at 03:36:09Z and reserved at **03:36:33Z** — before the pre-registration,
   before the race-guard marker, before anything.

9. **THE STOP OF `CONDITIONS-128.md` STANDS WHOLE**, as do items 1 of `CONDITIONS-131.md` through
   `-137.md` item 6. Nothing built on this corpus or this instrument left the house; no delivery
   object, repair pass, gauntlet or packet exists. **Ten sessions have now held the stop, one
   examined it, one answered it, and this one kept it without being asked. It was not asked about
   again**, as `CONDITIONS-137.md` item 6 requires before 2026-09-05.

10. **DO NOT MINE A DEAD SESSION'S SCRIPTS FOR FACTS.** Unchanged from `CONDITIONS-135.md` item 6,
    `-136.md` item 7 and `-137.md` item 7, and still unguarded.

11. **A SESSION-OPEN MARKER MUST NOT LIVE IN `journal/`.** `CONDITIONS-137.md` item 8, honoured:
    `.session-open-2026-08-29.md` sits at the repository root and `check_anchors.py` was run before
    landing.
