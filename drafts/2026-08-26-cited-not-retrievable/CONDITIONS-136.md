# Conditions 136 — the gate that failed, and the two roles that failed it

**Session 136, 2026-08-26. This is not a gauntlet.** Nothing shipped, nothing graduated, no packet
exists at any status, and no file under `letter/`, `offer/`, `deliverable/` or `deliverable-v0.3/`
was touched.

**Two roles were convened, and the reason was stated in `PREREGISTRATION-136.md` §5 before either
ran.** Two search fan-outs were also convened; a fan-out is not a role and has no voice in any
verdict. **Four sub-agents in total, against the constitution's ceiling of about six.**

| verdict | who | result |
|---|---|---|
| **Interlocutor (a), refutation** | `INTERLOCUTOR-136.md` | **CORE CLAIM SURVIVES NARROWED** — 23 charges, **8 blocking**, and **8 charges it tried and lost, recorded as its own losses** |
| **Interlocutor (a), K-E** | same file | **NO — and conditionally.** Its condition is item 5 below, adopted verbatim |
| **Interlocutor (b), hostile critique** | same file, unedited | **ACCEPTED WITHOUT QUALIFICATION.** The recurring charge lands a **sixth** time |
| **Verifier, independent recomputation** | `VERIFIER-136.md` | **PASS WITH FINDINGS** — every figure reproduced from the raw data, **zero** field mismatches across the whole series file and all 122 per-edition rows; the findings are of scope and labelling |

**THE GATE FAILED. K-C fired** (`GATE-DECISION-136.md`). **Every blocking charge was accepted.**
**Every figure a reviewer handed over was recomputed here before use**, and on each one this
practice's own computation agreed with it.

---

## The dispositions

| # | finding | from | disposition |
|---|---|---|---|
| 1 | **The concept's opening sentence is refuted by a 1,288-byte file this arc committed on its first day and cited one sentence earlier.** The `robots.txt` has a second block, `User-agent: *`, with **no `Disallow: /`** and nothing covering a video path — so for an ordinary link-checker **the fetch is permitted**, and *"that route is closed to them by instruction"* is false. | Interlocutor 1, **BLOCKING** | **ACCEPTED IN FULL. THE WORST FINDING OF THE SESSION**, and it is `POST-MORTEM.md` §4's own diagnosis — a file fetched, cited, and not read to the end — **on 1,288 bytes**. The inherited half is `DERIVED.md` §1, which describes the file as *"25 named user-agents followed by one line"* and never says it continues for thirty more. Corrected in `CONCEPT.md` §1 with the deleted sentences quoted. **It removes the reason the measurement was supposed to matter and moves all the weight onto §4b, which was not measured.** |
| 2 | **"Conjecture, marked as such wherever it appears" is broken twice inside the document that promises it** — the framing sentence, and §5's claim about the receiver's liveness test. | Interlocutor 2, **BLOCKING** | **ACCEPTED.** Both marked. It is `CONDITIONS-135.md` disposition 2 recommitted one session later: the strong form in the bold text, the deflating qualification further down. |
| 3 | **§3's "Repetition" limb is refuted by `series-stability-136.json`, written by this session and cited by §1.** Five hours, not "a fixed second"; day 1 is a different corpus, not "the same fixed list"; two holes. **And it breaches condition 30(a)** — the count may not travel without the cadence. | Interlocutor 3, **BLOCKING** | **ACCEPTED IN FULL.** Corrected with the cadence attached. **A file this session built specifically to stop it publishing a wrong series figure did exactly that, and the session did not read its own output back against its own prose.** |
| 4 | **The confirmation ratio was computed over all arms in a table every other row of which excludes a public forum's arm by name** — 6 of 16 all-arms against 5 of 15 on the encyclopedia. | Verifier 7 **and** Interlocutor 4, found independently, **BLOCKING** | **ACCEPTED, and repaired on the Verifier's finding before the adversary's report arrived** (commit `b84814e`). `confirmation_by_arm.py` recomputes it here rather than adopting either reviewer's figure — `POST-MORTEM.md` §3's refusal applied to this practice's own reviewers — and **agrees with both**. |
| 5 | **"Substantially its own noise" and "mostly their instrument" are refuted by the practice's own record.** 5 of 24 raw changes refuted = **20.8 %**. "Mostly" means more than half. | Interlocutor 5, **BLOCKING** | **ACCEPTED.** Recomputed here: **24 raw readings, 5 refuted, 20.8 %.** The claim is narrowed to what the evidence carries, and **fifteen events is not a rate either** — condition 8 forbids rendering six as one, and this document quoted that rule eleven lines above the sentence that broke it. |
| 6 | **The article-space figure is 94 % an artefact of an assumption whose own docstring says no published number rests on it.** | Interlocutor 6, **BLOCKING** | **ACCEPTED.** Recomputed here: of 2,174 article-space pages, **124 carry an explicit `ns` of 0 and 2,050 — 94.3 % — are there because the script defaulted them.** The docstring's claim is **withdrawn**: printing a figure twice does not remove an assumption from it. Carried into `CONCEPT.md` §1 item 4. |
| 7 | **K-C fires on its own wording and was recorded NOT FIRED.** Every candidate the fan-out examined is silent on video; and **§5's daylight argument needs the receiver silent while K-C needs it to have spoken.** | Interlocutor 7, **BLOCKING** | **ACCEPTED, AND IT IS WHAT ENDS THE GATE.** The criterion is **fired, not amended** — a criterion amended after seeing the evidence that meets it is what a pre-registration exists to prevent, and this session disclosed in advance that its interest points toward permitting work. **`GATE-DECISION-136.md`.** |
| 8 | **The receiver's determining artifact was never read.** A third documentation page is quoted in this practice's *other* fan-out and was never searched; the bot's public implementation was not attempted; and the two fan-outs state the point in opposite-sounding words. | Interlocutor 8, **BLOCKING** | **ACCEPTED IN FULL.** *"Silence in two of at least three documentation pages, about software nobody here has read, is not a test result."* Marked as conjecture in §5 and written into `GATE-DECISION-136.md` §5 as work owed **before** any re-gating. **`POST-MORTEM.md` §8's open question — what checks whether the evidence was read — answered again with nothing.** |
| 9 | **A population mismatch, a count describing no set that exists, a citation pointing at a paragraph that does not carry it, a wrong interval antecedent, and a spliced quotation.** | Verifier 6, 7, 10 | **ALL ACCEPTED AND CORRECTED.** The citation error: *"six events is not a rate and eleven are not either"* was attributed to `CONDITIONS-132.md` item 5, **which does not contain it**; the pointers now name `memory/downstream-commitments.md` condition 8 and `DAY13-2026-08-25.md`. |
| 10 | **A paraphrase of the architect's own standing rule was printed inside quotation marks in the text filed to him.** | Verifier 9b | **ACCEPTED AND REPAIRED IN `REQUESTS.md`.** The rule is now quoted in full. **The reviewer found it outside the documents it was asked to check.** |
| 11 | **The architect's rule was read on the wrong branch.** The request named a deadline; on the rule's own dichotomy the decision was due **past 2026-08-29**, not on 2026-08-26. | Interlocutor 21, **BLOCKING** | **ACCEPTED.** *"The self-serving reading is not in the verdict; it is in the calendar."* `INCREMENT-24.md` §6(a): the claim that his rule licensed the decision is **withdrawn**; the refusal stands as this practice's own position, taken early, and it keeps the stop so nothing he could decide is foreclosed. |
| 12 | **`CONDITIONS-135.md` item 8 had already decided the question and was not quoted** — *"Silence means the stop and the hour both stand."* | Interlocutor 22, **BLOCKING** | **ACCEPTED.** Selecting the one of two governing items that leaves room for the move is `ERRATA-135.md` E53's shape, one session later. |
| 13 | **"A refusal against this session's own disclosed interest" is false** — both moves serve the disclosed interest. | Interlocutor 23, **BLOCKING on the characterisation** | **ACCEPTED AND WITHDRAWN.** *"The decision stands; the credit claimed for it does not."* The asymmetry the charge names — strict where the stakes are nil, loose where they are not — **no longer exists, because the gate has since failed**; that it existed when the charge was made is recorded, not explained away. |
| 14 | **Stock and flow are not commensurable**, and the residual (identifiers crossing INDETERMINATE, 46–70 per interval) is of the same order as the flow. | Interlocutor 10, non-blocking | **ACCEPTED as a real limit on the concept's central contrast**, and carried into `GATE-DECISION-136.md`. Condition 32(c) says INDETERMINATE is a property of the request, not of the identifier — **so the stock's own night-to-night wobble is partly instrument, and the concept never said so.** |
| 15 | **Three different counts for one quantity in one directory on one day** — "sixty-odd", "thirty-odd", and 124. | Interlocutor 12, non-blocking | **ACCEPTED.** Counted: **124.** Both stated figures were wrong, and they were wrong **inside the sentence congratulating the session for catching a defect.** |
| 16 | **`CONDITIONS-136.md` was named in the present tense before it existed.** | Interlocutor 13, non-blocking | **ACCEPTED.** It is `CONDITIONS-135.md` disposition 5 recommitted — *"a statement about an artifact, refuted by the artifact"* — in the section headed *what this concept does not have, listed so nobody has to find it*. **This file is now that file.** |
| 17 | **Charges 9, 15, 16, 17, 18, 19, 20:** a neighbour's soft-404 finding quoted only on the half that helped; *"reads the population"* against *"not a sample of anything"*; a receiver both standing behind this arc and not being its receiver; a headline a third of whose base is not article space; a far closer numerical coincidence than the one defused at length; condition 7(b) softened by one notch; a ceiling exemption claimed by analogy to a different ceiling. | Interlocutor, non-blocking | **ALL ACCEPTED.** Carried in `CONCEPT.md` and `GATE-DECISION-136.md` §6. **Charge 19 the adversary itself records as mostly lost, and its partial defence of this practice is left standing in its report.** |

---

## Binding on the next session

1. **THE STOP OF `CONDITIONS-128.md` STANDS WHOLE, AND THE QUESTION THAT WAS OPEN AGAINST IT IS NOW
   CLOSED BY THIS PRACTICE'S OWN HAND.** No delivery object, no repair pass, no gauntlet, no packet
   **from that arc** before 2026-09-05. The licence this practice asked for on 2026-08-25 was decided
   here, under the architect's standing rule of 2026-07-17, and **REFUSED** (`INCREMENT-24.md`).
   **Nine sessions have now held the stop; one examined it; this one answered it.** Do not ask again
   before 2026-09-05 — `CONDITIONS-135.md` item 2, honoured. **If the architect rules otherwise at
   any time, his ruling governs and ours is superseded on its face.**

2. **THE ADVERSARY'S CONDITION ON K-E, ADOPTED VERBATIM AND BINDING.** It answered *is this the
   stopped arc renamed* with **NO — and conditionally**, and named what would flip it:

   > "**no delivery object and no packet built on this corpus or this instrument leaves the house
   > before 2026-09-05.** … If a packet ships from this material on 2026-09-04, the stop will have
   > been honoured in its letter and routed around in its substance, and K-E will have been answered
   > YES by events rather than by me."

   **This practice adopts that as binding on every session before 2026-09-05.** It costs nothing
   today — the gate failed and no arc is licensed — and it is written down so that it costs nothing
   later either. **Whoever reads this: the answer to K-E is not settled by the adversary's NO. It is
   settled by what does or does not leave the house.**

3. **THE GATE FAILED AND THE CONCEPT IS PARKED, NOT DISCARDED.** `GATE-DECISION-136.md` names what
   would revive it — **one small measurement**, §4b, with all three of its outcomes written in
   advance including the one that discards the concept. **A parked concept's figures are not this
   practice's VERIFIED status and nothing in that directory has been through a gauntlet.** They are
   offered as material with a disclosed pedigree and their corrections attached.

4. **THE INSTRUMENT'S HOUR STANDS AT 03:41:00Z** until the architect rules otherwise. No session
   moves it; no substitute is measured at another hour; a day out of reach is a hole. Unchanged from
   item 3 of `CONDITIONS-131.md` through `-135.md`. **The series has two holes, 2026-08-17 and
   2026-08-24**, each because a session died mid-run.

5. **If a session opens near 03:41:00Z, the run is its first act.** Unchanged, and it is why day 14
   exists: reserved **03:37:09Z**, four minutes before the hour, before this record, before the
   pre-registration, before anything.

6. **THE DAY-NUMBERING CONVENTION IS NOW WRITTEN DOWN — `CONDITIONS-135.md` item 5 IS CLOSED.** It
   lives in `window_status.py` as `DAY_NUMBERING` and is **emitted into every window-status file the
   script writes**, so a reader of the output never has to find a comment. Day N is the Nth
   measurement day; a hole consumes no ordinal; a same-day second probe is not a measurement day.

7. **DO NOT MINE A DEAD SESSION'S SCRIPTS FOR FACTS.** Unchanged from `CONDITIONS-135.md` item 6, and
   still unguarded. A stopped session's scripts state predictions, and this practice has published
   one as a property of the series.

8. **NEVER WRITE A SESSION-OPEN MARKER WITH A TOP-LEVEL `#` HEADING.** Honoured this session
   (`journal/2026-08-26-session-open.md` opens with `##`). Unchanged from `CONDITIONS-135.md` item 7,
   and it is the rule that costs a sibling practice nothing rather than costing them a deploy.

9. **READ `memory/downstream-commitments.md` IN FULL, AND THIS SESSION IS THE ARGUMENT FOR IT.** Its
   condition 7 caught a defect in the first artifact of a new arc that no reviewer had yet seen:
   sixty-odd Wilson intervals computed with the video as the independent unit, which that condition
   says are too narrow by at least ×1.1954 because losses clump by cited account. **The constitution
   names exactly one file to read in full every session, and this is what that instruction is for.**
   Condition 8 caught a second one in the same document, four minutes later.

10. **THE TWO CEILINGS ARE NOW MEASURED, AND BOTH ARE BREACHED.** `record_ceiling_check.py` on the
   stopped arc: **400,242 raw against 3,000**. `tools/journal/count.py` over August: every journal
   from 2026-08-08 to 2026-08-22 over the 400-word ceiling, only 2026-08-24 and -25 under. **No
   remedy is proposed for either** — compressing the stopped arc's record would destroy the evidence
   for its own post-mortem, and the journal figures carry a caveat that makes them upper bounds
   (`memory/open-questions.md`). **They are recorded as standing breaches with their commands, not as
   tasks, and this session's own new directory is over the same ceiling.**

11. **STILL OWED AND STILL NOT DONE**, each named rather than dropped: the hit-rate half of
   `POST-MORTEM.md` §8 (**third session running that naming it is not doing it**); `guard_claims.py`'s
   FAIL branch (`ERRATA-133.md` E42); the classification population that cannot see what the
   disposition tables do not table; the five convergence items open since session 133.

12. **AND THE ONE THING THAT MATTERS MORE THAN ANY ITEM ABOVE.** The adversary counted **nine**
    statements about an artifact refuted by the artifact, produced by this session, in the first
    document of a new directory. *"The machinery has not changed. It has moved directory."* **Every
    guard this practice has built checks a statement against a file; not one checks whether the file
    was read to the end**, and the worst of the nine was a 1,288-byte file this arc has had since its
    first day. **`POST-MORTEM.md` §8's question is now three sessions old and unanswered, and this
    session is the best evidence yet that it is the right question.** No session should open another
    concept before it has something to say about that.

    **AND THE COUNT IS TEN, NOT NINE — THE TENTH WAS COMMITTED WHILE REPAIRING THE FIRST NINE, AND
    THIS PRACTICE FOUND IT ITSELF.** The adversary's charge 14 was a heading reading *"Two things
    that claim is not"* above three items. The repair changed it to *"Four"*; a fifth item was then
    added beneath it in the same session; **and the heading was wrong again within the hour, inside
    its own correction.** Found by this practice reading its own section numbering back, after the
    adversary had gone. **This is not offered as credit.** It is the plainest available evidence that
    the defect is structural and not a matter of care: a session that had just been shown nine
    instances, and was writing the disposition table for them, produced a tenth in the act of fixing
    one. **Nothing in this repository counted a list's items against its heading.
    Now something does.**

    **THE CODE IS WRITTEN, BECAUSE NAMING IT AGAIN WAS NOT AN OPTION.** `tools/numeral_list_check.py`
    compares the number a line announces against the list beneath it. **It catches the planted defect
    on a fixture, and it is clean over every document this session authored** — the four hits
    remaining across this directory are all inside the reviewer and fan-out reports, published
    unedited, and all four are the false-positive class the script's own docstring predicts in
    advance (a number in prose that is not a list's length). **Two false-positive classes were
    removed on first contact with real files and both are recorded in the code**: a markdown section
    heading's number is a section number, not a count; and only the FIRST numeral in a line is
    checked, because a heading that announces a count announces it first. **And the script's own
    first run fired on the list items it was checking** — the same shape as the counter that counted
    its own footnote — **which is in the code too.**

    **What it does not catch is nine tenths of the problem**, and the docstring says so: it would
    have passed the `robots.txt` premise, the broken conjecture-marking promise, and *"a fixed
    second"* against a file listing five hours, in silence. `memory/downstream-commitments.md`
    condition 31 governs it like every other guard here — **a pass is evidence about this guard's
    tested paths, not about the document.**
