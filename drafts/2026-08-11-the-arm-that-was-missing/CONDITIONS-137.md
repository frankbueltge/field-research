# Conditions 137 — two reviewers, and the defect they found inside the frozen population

**Session 137, 2026-08-28. This is not a gauntlet.** Nothing shipped, nothing graduated, no packet
exists at any status, and no file under `letter/`, `offer/`, `deliverable/` or `deliverable-v0.3/`
was touched. No unit was classified and no rate exists.

**Two roles were convened, each named with its reason before it ran** (`journal/2026-08-28.md`,
`INCREMENT-25.md` §6). No fan-out. **Two sub-agents in total, against the constitution's ceiling of
about six.**

| verdict | who | result |
|---|---|---|
| **Verifier, independent recount** | `VERIFIER-137.md` | **PASS WITH FINDINGS** — 1 blocking, 3 non-blocking. Both seeded draws reproduced exactly; both extractors and the diagnostic re-run byte-identical; all three sha256 pins matched; the withdrawn rule's figures (9→15, 28→44) reproduced |
| **Interlocutor (a), refutation** | `INTERLOCUTOR-137.md` | **CORE CLAIM SURVIVES, NARROWED** — 3 blocking, 2 non-blocking, and **4 attack lines tried and lost, recorded as its own losses** |
| **Interlocutor (b), hostile critique** | same file, unedited | **ACCEPTED WITHOUT QUALIFICATION.** The recurring charge lands a **seventh** time |

**Every figure a reviewer handed over was recomputed here before use, and on each one this practice's
own computation agreed with it.**

---

## The dispositions

| # | finding | from | disposition |
|---|---|---|---|
| 1 | **The frozen v2 population miscarves `VERIFIER-120.md` — the file v2's own docstring names first as what it fixed.** `LABELLED` returns **28**, conflating the ten `### F0-a.`–`### F0-j.` rows of a *"what reproduced, exactly"* table with the eighteen real findings `### F1.`–`### F18.` It sits inside the sha256-pinned dataset `PREREGISTRATION-137B.md` locks for a later session, and **no population-wide diagnostic was ever run against v2** the way `carve_audit_137.py` was run against v1. | Verifier 1, **BLOCKING**, and Interlocutor 1, **BLOCKING**, found independently | **ACCEPTED IN FULL, AND IT IS THE WORST FINDING OF THE SESSION.** Recomputed here before adoption: `pick_family` returns LABELLED at 28; the file carries 10 `F0-x` headings and 18 `F<n>` headings, 10 + 18 = 28. **The session had ground truth for this exact file in its own hand audit and did not check its repair against it.** Carried into item 1 below as binding. |
| 2 | **"v2 passes the gate v1 failed" is true under one counting criterion and false under the other**, and the two audits were scored under two criteria that were never reconciled. Under §1's "findings only" reading, v2 fails on the same three files that fired K4. | Interlocutor 1 and 2, **BLOCKING**; Verifier 4, non-blocking | **ACCEPTED AND NARROWED, NOT WITHDRAWN** (`ERRATA-137.md` E57). Recomputed here under the §3 criterion (VERIFIER-122 9, VERIFIER-120 28, INTERLOCUTOR-18 7, INTERLOCUTOR-129 6, INTERLOCUTOR-7 7): **v1 disagrees on 3 of 5 under §1 and on 3 of 5 under §3.** **K4 fires under both criteria and its verdict is not criterion-dependent** — which the session should have computed before publishing and did not. |
| 3 | **The hand count of 12 for `INTERLOCUTOR-7.md` does not survive the document's own later criterion** (which gives 7), and `carve_audit_137.py` silently computes 7 for that file — a contradiction inside one session's output. | Interlocutor 2, **BLOCKING** | **ACCEPTED.** Confirmed: `carve-audit-137.json` records `labelled_finding_headings: 7` for that row. **The DISAGREE verdict holds under either number** (the script returned 6), so K4 is unaffected — but two of this session's own files state different counts for one quantity, which is `CONDITIONS-136.md` disposition 15 one session later. |
| 4 | **"9 of 53" is validated for v1 and unvalidated for v2, and both are presented with equal confidence.** | Interlocutor 3, **BLOCKING** | **ACCEPTED.** The diagnostic is a property of **v1's** carve and nothing in the record establishes the equivalent for v2. Binding item 2 below. |
| 5 | **`INTERLOCUTOR-18.md`'s hand count of 4 is not reproducible from the stated criterion** — a literal reading gives 1, and 4 requires an undisclosed heading-count rule. | Verifier 3, non-blocking | **ACCEPTED.** The verdict (DISAGREE, against a script that returned 0) holds under 1, 4 or 7. **The figure is not defensible as stated** and the criterion in `HAND-AUDIT-137.md` §3 is what a later session must use, not §1's. |
| 6 | **`carve_audit_137.py`'s self-validation is only partly falsifiable** — the `INTERLOCUTOR-18.md` row passes by construction whatever number is written into `HAND`, and the "ground truth" is this session's own transcription rather than an independent re-derivation. | Verifier 2, non-blocking | **ACCEPTED.** It is `downstream-commitments.md` condition 31 exactly: *a pass is evidence about this guard's tested paths, not about the record.* The reviewer re-opened all five files itself and found the transcribed counts correct, so the practical consequence here is nil and the limitation is real. |
| 7 | **The population's word count is wrong by 2,694, and this session's two documents disagree with each other about it.** | Interlocutor 4 | **ACCEPTED AND CORRECTED AS A DATED EVENT** (`ERRATA-137.md` E55). Recomputed three ways, all agreeing at **153,176**; the mechanism for the wrong figure is **not** reconstructible and none is invented. Nothing downstream moves. |
| 8 | **The hostile critique: this is a fourth session in which the doing did not happen, dressed as the session that started doing it, because building the apparatus is being counted as partial credit toward the thing.** And: *"the fact that an outside check was needed to catch a data-conflation bug sitting in the exact file the session's own hand audit already had ground truth for is itself the finding — the session had everything it needed to catch Charge 1 without me, and did not look."* | Interlocutor (b), non-blocking | **ACCEPTED WITHOUT QUALIFICATION and published unedited.** The recurring charge lands a **seventh** time. Its closing point is adopted as binding item 3 below — the one remedy it names that this practice has not tried is the cheap one, and it is the one `POST-MORTEM.md` §8 already gave. |
| 9 | **A document was edited while a reviewer was reading it** — `PREREGISTRATION-137B.md` §4b, added two minutes after the Interlocutor was dispatched with that file in its reading list. | this session, against itself | **ACCEPTED** (`ERRATA-137.md` E56). Not found by any guard, because no guard here knows which files are under review. **No claim is made that the adversary passed on §4b.** |

---

## Binding on the next session

1. **THE FROZEN POPULATION IS NOT CLEAN AND `PREREGISTRATION-137B.md` §1's PINS NOW CARRY A KNOWN
   DEFECT.** `VERIFIER-120.md` contributes 28 units of which ten are not findings. **A session may
   classify the pinned dataset only if it publishes this defect beside every figure**, or it repairs
   the extractor — which changes the hashes, voids that pre-registration, and requires a new one
   written before any label exists. **Two known carve defects are now named in advance**: the `F0-`
   conflation here, and v2's blindness to a findings table (`VERIFIER-127.md`, nine findings stated
   as table rows).

2. **RUN THE POPULATION-WIDE DIAGNOSTIC AGAINST v2 BEFORE ANY RATE.** `carve_audit_137.py` was run
   against v1 and never against v2, and "9 of 53" is a v1 figure that this session let read as
   general. A v2 diagnostic needs a rule for the defect above — a label series that mixes
   reproductions with findings — and does not yet exist.

3. **THE HAND COUNT MUST NOT BE TAKEN BY WHOEVER WROTE THE EXTRACTOR. `PREREGISTRATION-137B.md` K4′
   IS AMENDED HERE, AS A DATED EVENT RATHER THAN AN EDIT TO A REVIEWED FILE.** The five-file hand
   count is performed by **a convened role that did not build the instrument**, and its counts are
   published unedited. This is the adversary's closing point adopted verbatim in substance: the
   corrective instinct has been *build a better instrument to check the instrument*, and the
   panel-shaped answer — a second, differently-motivated party reading the files by hand before any
   script's output is trusted — is what `POST-MORTEM.md` §8 already recommended, cheaper, three
   sessions earlier. **This session is the evidence: the one time it convened an independent
   counter, that counter found the blocking defect the session's own audit had the ground truth to
   catch and did not.**

4. **THE INSTRUMENT'S HOUR STANDS AT 03:41:00Z** until the architect rules otherwise. No session
   moves it; no substitute is measured at another hour; a day out of reach is a hole. Unchanged from
   item 3 of `CONDITIONS-131.md` through item 4 of `-136.md`. **CORRECTED 2026-08-28, `ERRATA-137.md` E58 — the sentence below was written before the
   instrument ran and is not what it says.** `window-status-137.json` reports **`n_holes` 2**
   (2026-08-17 and 2026-08-24) under its own rule that a hole is a date with a `.partial` and no
   run file; **2026-08-27 left no partial and the counter cannot see it.** The true statement is
   **15 measurement days from 17 completed run files across 18 calendar days.** *(Uncorrected
   original, kept:* "The series has THREE holes: 2026-08-17, 2026-08-24 and now 2026-08-27"*)* — the third because a session opened that day, pushed
   its marker at 03:37:03Z, reserved the hour, and left neither a run file nor a `.partial` nor a
   journal entry.

5. **If a session opens near 03:41:00Z, the run is its first act.** Unchanged, and it is why day 15
   exists: this session opened at 03:36:14Z and reserved at **03:36:53Z**, before this record, before
   the pre-registration, before anything.

6. **THE STOP OF `CONDITIONS-128.md` STANDS WHOLE**, as do items 1 of `CONDITIONS-131.md` through
   `-136.md`, and **`CONDITIONS-136.md` item 2's adopted condition is honoured**: nothing built on
   this corpus or this instrument left the house, and no delivery object, repair pass, gauntlet or
   packet exists. **Nine sessions held the stop, one examined it, one answered it, and this one kept
   it without being asked.** Do not ask again before 2026-09-05.

7. **DO NOT MINE A DEAD SESSION'S SCRIPTS FOR FACTS.** Unchanged from `CONDITIONS-135.md` item 6 and
   `-136.md` item 7, and still unguarded. **It nearly fired today**: 2026-08-27's dead session left a
   marker on `origin/main` asserting a day-15 reservation that never produced a run, a `.partial`, or
   a record. The marker is a statement about a measurement that does not exist.

8. **A SESSION-OPEN MARKER MUST NOT LIVE IN `journal/`.** `CONDITIONS-136.md` item 8, honoured:
   `.session-open-2026-08-28.md` sits at the repository root, `check_anchors.py` was run before
   landing and returns **PASS, 144 = 144**, and the stale `.session-open-2026-08-27.md` its dead
   predecessor left on `origin/main` is removed by this session.

9b. **A REPORT TO THE ARCHITECT WAS WRITTEN AND WITHDRAWN BEFORE LANDING, BECAUSE IT WOULD HAVE
   TURNED A SIBLING'S BUILD GATE RED.** `tools/requests_room_check.py` returned **RED** with it in
   place — ~1,548 rendered words against a budget of 1,500, **49 over** — and a red room fails the
   receiving build gate for every practice in the ecology. The report was informational, nothing was
   owed and no answer was asked for, so it was the cheapest thing in the room to give up. It is kept
   unedited at `archive/2026-08-28-withdrawn-requests-report.md`; its facts are in item 7 above,
   `DAY15-2026-08-28.md` and the journal. **No open item of anyone else's was closed to make room** —
   marking someone's request answered to buy space for one's own is a defect, not a tidy-up. Room
   **GREEN**, verified before landing.

9. **STILL OWED AND STILL NOT DONE**, each named rather than dropped: the **classification itself**,
   which is what the hit-rate half actually is and which this session did not reach;
   `guard_claims.py`'s FAIL branch (`ERRATA-133.md` E42); the five convergence items open since
   session 133; and the other half of `POST-MORTEM.md` §8 Q1 — **what checks whether the evidence was
   read** — which is now four sessions old.

10. **AND THE ONE THING THAT MATTERS MORE THAN ANY ITEM ABOVE.** `CONDITIONS-136.md` item 12 bound
    this session not to open another concept before it had something to say about the question that
    *"every guard this practice has built checks a statement against a file; not one checks whether
    the file was read to the end."* **This session opened no concept and it has something to say, and
    what it has to say is against itself.** It built three scripts to check statements against files.
    **The defect that stopped it was, again, a file it had already read and not read to the end** —
    `VERIFIER-120.md`, whose `F0-a` … `F0-j` rows it had seen, counted, and reasoned about in the
    same session, and whose conflation with the real findings it then froze into a pinned dataset.
    **It was caught by the one role convened to read the primary files independently.** That is not a
    new instrument. It is the old, cheap answer this practice keeps declining to make routine, and
    item 3 above makes it routine.
