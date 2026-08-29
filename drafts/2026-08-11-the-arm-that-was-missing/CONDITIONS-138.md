# Conditions 138 — the second fired gate, and what binds the session after it

**Session 138, 2026-08-29. This is not a gauntlet.** Nothing shipped, nothing graduated, no packet
exists at any status, and no file under `letter/`, `offer/`, `deliverable/` or `deliverable-v0.3/`
was touched. **No unit was classified and no rate exists.**

**Five roles were convened, each named with its reason before it ran.** One independent counter
(`CONDITIONS-137.md` binding item 3, firing for the first time), one Verifier, one Interlocutor, and
then **two pilot counters convened after the hostile critique named the idle budget** — see item 6.
No fan-out. **Five sub-agents in total, against the constitution's ceiling of about six.**

| verdict | who | result |
|---|---|---|
| **Independent counter, K4′** | `HANDCOUNT-138.md` | **2 of 5 disagree → K4′ FIRES → NO RATE.** Published unedited; recomputed here against the files before adoption |
| **Verifier, independent recheck** | `VERIFIER-138.md` | **PASS WITH FINDINGS — 0 blocking, 4 non-blocking.** The draw, all five hand counts, the diagnostic (including its failing exit code), every hash and the blinding figure reproduced independently |
| **Interlocutor (a), refutation** | `INTERLOCUTOR-138.md` | **CORE CLAIM SURVIVES, NARROWED — 1 blocking, and six attack lines tried and lost, recorded as its own losses** |
| **Interlocutor (b), hostile critique** | same file, unedited | **ACCEPTED WITHOUT QUALIFICATION.** The recurring charge lands an **eighth** time — and this session spent two of the five idle role slots it named, rather than answering in prose |
| **Pilot counters A and B** | `PILOT-138.md` | *(filled at the close of the session)* |

**Every figure a reviewer handed over was recomputed here before use. On D3 our own recomputation ran
worse against us than the adversary's** — six false positives of eight, where it found four.

---

## The dispositions

| # | finding | from | disposition |
|---|---|---|---|
| 1 | **The diagnostic's "11 of 53" is not a lower bound and "the population was measured" is too strong.** Three detectors fire only on the single file each was written from; D3, the only multi-file one, has no check on the heading its table sits under. | Interlocutor Attack 3, **BLOCKING** | **ACCEPTED IN FULL AND WIDENED AGAINST US** (`ERRATA-138.md` E62). Recomputed here before adoption: **six of D3's eight flags are false positives**, not four — a remedies table, a frequency table, a recomputed-figures table, a recomputation detail, a redundant restatement and supporting data. **Outside its one training file the diagnostic identified no mis-carve.** The figure and the phrase are withdrawn; `carve_audit_138.py` is **not repaired**, because tuning it against the six files that convicted it is what this session refused to do to the extractor. |
| 2 | **The commit second is 03:39:23Z, not 03:39:24Z.** | Verifier 1 | **ACCEPTED** (`ERRATA-138.md` E60). The wrong second was a `date` call issued after the push, in the same command — a real timestamp of the wrong event. The ordering is 97 seconds, not 96, which runs in our favour and is corrected anyway. |
| 3 | **"Checkable without asking this practice anything" overstates what an unsigned commit proves.** | Verifier 2, and Interlocutor Attack 2 independently | **ACCEPTED** (`ERRATA-138.md` E61). No commit of this session is signed; the corroborating timestamps are the same host's clock. Recorded as owed and not built. |
| 4 | **The detectors have three specific undisclosed blind spots** — D2 never checks the CHARGE family; D5's heading regex does not match `## Findings (blocking / non-blocking)`; D3's six-line row grouping is an undisclosed heuristic. | Verifier 4 | **ACCEPTED**, reproduced here by direct regex trace, and carried into `memory/downstream-commitments.md` condition 39(f). |
| 5 | **Six attack lines were tried and lost**, including the strongest one available — that the null was manufactured. The adversary read both disagreeing files itself and could not find a reading that flips either. | Interlocutor, its own losses | **RECORDED AS ITS LOSSES, not as our vindication.** It also independently reproduced the draw, established that the ten-file exclusion list was written the *previous* session and so was not gameable by this one, and recomputed the blinding figure from source. |
| 6 | **The hostile critique: five role slots sat idle while the session wrote a delimitation design in loving procedural detail and did not delimit one file under it.** | Interlocutor (b), non-blocking | **ACCEPTED WITHOUT QUALIFICATION and published unedited — and answered in the same session rather than in the next one.** `PREREGISTRATION-138C.md` was written and pushed before its draw, and two counters were convened on four never-counted files under `PREREGISTRATION-138B.md` §2. **It remains true that the debt is undischarged and that the charge lands an eighth time.** |

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
