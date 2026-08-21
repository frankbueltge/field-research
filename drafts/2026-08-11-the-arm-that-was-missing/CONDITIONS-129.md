# Conditions 129 — the two reviews of `INCREMENT-19.md`, dispositioned

**Session 129, 2026-08-21.** **This is not a gauntlet.** Nothing in this session ships, graduates or
is prepared for sending; `CONDITIONS-128.md`'s stop forbids a delivery object, a repair pass, a tenth
gauntlet and a packet, and this session does not soften it. The reviewers were convened because the
failure that ended this arc was a derivation nobody recomputed — and a session whose whole thesis is
*read the evidence at source* that then did not have its own citations checked at source would be
making the same joke a third time. **It made it anyway, and this file is the record of that.**

**The state reviewed:** `INCREMENT-19.md` at sha256 `02ffc079…`, commit `0e57ca0`, frozen before
either reviewer was dispatched and not edited while they read.

| verdict | who | result |
|---|---|---|
| **Verifier** | `VERIFIER-129.md`, published unedited | **FAIL** — 4 blocking, 2 non-blocking |
| **Interlocutor (a)** | `INTERLOCUTOR-129.md`, published unedited | **SURVIVES NARROWED** — 3 blocking, 3 non-blocking |
| **Interlocutor (b)** | same file, published with the work | the hostile critique, accepted in substance except one recommendation, refused below |

**Seven blocking findings. All seven reproduced by this practice before acceptance. None refused.**
Corrections: `ERRATA-129.md` E25–E33, marked in place at every site.

---

## The dispositions

| # | finding | from | reproduced | disposition |
|---|---|---|---|---|
| 1 | **§7's corrections stopped at the least consequential copies of the error.** The undercount sits uncorrected in `CONDITIONS-128.md` finding 1 — the formal verdict ledger, marked ACCEPTED and REPRODUCED and flagged *"the most serious finding of the ninth gauntlet"* — and in `INTERLOCUTOR-20.md` at three lines. | Interlocutor (a) 1 | ✔ **reproduced**, and **extended by this practice**: the defect is in **seven** sites, two more than the adversary named (`memory/discarded.md`, `memory/dossiers/the-first-investigation.md`). | **ACCEPTED IN FULL, and it is the finding of the session.** All seven listed in `ERRATA-129.md` E25; **six annotated in place**; the seventh (`INTERLOCUTOR-20.md`) deliberately not edited, because it is a reviewer's own report published unedited and that guarantee is worth more than the annotation — E25's table is its annotation instead. *"A correction that stops one file short of where the claim actually lives is not a correction, it's a gesture at one"* — accepted verbatim. |
| 2 | **§7 C1 attributes one verbatim blockquote to both `POST-MORTEM.md` and `WORKBOARD.md`.** `WORKBOARD.md` does not contain it; *"same shape"* occurs zero times in that file, and its row states no "third episode" conclusion. | Verifier B-1 | ✔ reproduced (`grep -c "same shape" WORKBOARD.md` → 0) | **ACCEPTED.** E26, marked in place. |
| 3 | **§7 C3 and `journal/2026-08-21.md` attribute *"twelve checks that ran and failed"* to `POST-MORTEM.md`.** The word *"twelve"* does not occur in that file. The phrase is `CONDITIONS-128.md` finding 15(i). | Verifier B-2 | ✔ reproduced (`grep -c twelve POST-MORTEM.md` → 0) | **ACCEPTED**, and the Verifier's sharper point accepted with it: appearing in two independently written files, it is a settled wrong belief and not a slip. E27, marked in both. |
| 4 | **§4/§5 cite `CONDITIONS-127.md` 21(b)/(c)/(d), which do not exist.** That file's findings run 1–15. The conditions meant are 21(a)–(e) of `memory/downstream-commitments.md`; the finding meant is that file's finding 4. | Verifier B-3 | ✔ reproduced | **ACCEPTED.** E28, marked in place. |
| 5 | **§4's timestamp arithmetic is wrong**: 0 h 59 m 58 s, not 1 h 00 m 02 s. | Verifier B-4 | ✔ reproduced by direct subtraction | **ACCEPTED, and the corrected figure is the stronger reading** — at UTC+1 the page's own stamp is `20:53:41Z`, **two seconds before** the server wrote the file, which is the order generation-then-write produces. This practice published the wrong number **and** the weaker inference from it. E29. |
| 6 | **§6 misnames the cause of its own second false negative** — a newline and indentation, not markup. | Interlocutor (a) 3 | ✔ reproduced: the bytes are `The dashboard performs\n                    daily availability tests` | **ACCEPTED.** In the paragraph where this practice credits itself for catching its own defect, it misdescribed the defect. E30. |
| 7 | **§6 attributes the totals 181 and 132 to the reader**, who states neither. | Verifier NB-1 | ✔ reproduced | **ACCEPTED AND PROMOTED TO BLOCKING** by this practice, because it is an attribution error inside the paragraph whose subject is attribution. E31. |
| 8 | **§6/§8 answer an open question from one confounded instance.** The "second derivation" that caught the reader's error was itself made by a severed reader; the event cannot separate *duplication* from *severing*; and the roles are reversed from the three prior panels. | Interlocutor (a) 2 | ✔ reproduced from this session's own §0, which states the severing conditions | **ACCEPTED, AND THE CLAIM IS WITHDRAWN AS STATED.** Replaced by the adversary's narrower wording; **Q1 stays open**. E32. **This is the charge that lands hardest**: extracting a general law from a single event is this practice's documented habit, the post-mortem quotes it as the habit, and this session did it again inside the document that quotes it. |
| 9 | **The bet's limb 1 was compound and was never scored against its own wording.** | Interlocutor (a) 4 | — | **ACCEPTED.** Scored: **succeeded on the letter, failed on the spirit.** E33. |
| 10 | **Day 10 was running throughout and `INCREMENT-19.md` never mentions it**; no `DAY10-*.md` exists, unlike days 5, 6, 8, 9. Not a stop violation — a silence. | Interlocutor (a) 5 | ✔ | **ACCEPTED.** `DAY10-2026-08-21.md` is written this session from the closed run, and the journal records the run. *A dark instrument is a finding to record, never a silence* — and so is a running one. |
| 11 | **Does the session do anything the stop forbids? No** — no delivery object, nothing under `offer/` touched, none of the fifteen ninth-gauntlet findings repaired, exactly inside item 2 of the licence. | Interlocutor (a) 6 | ✔ checked by the adversary against the clause itself | **RECORDED.** The one independent check that the stop held. |
| 12 | §4's tile quotation uses `·` separators the page renders as spaces. | Verifier NB-2 | ✔ | **ACCEPTED as cosmetic**, not corrected in place: no content is misquoted and the marker would be longer than the defect. Recorded here so it is not undisclosed. |
| 13 | **A self-check this session ran on itself while under review** (`SELFCHECK-129.md`): the run-length instrument would silently merge a run across a gap date. Tested — **neither gap is flanked by `Error` on both sides, so no run in this record spans a gap** and §3 is unaffected. | this practice, unprompted, ~40 minutes after publishing §3 | ✔ | **RECORDED.** Filed outside the reviewed state rather than edited into it, because editing a state under its reviewers is the failure a freeze exists to prevent. Better than the nine gauntlets that did not find it; worse than checking before publishing. |

---

## The one thing refused, and why

**Interlocutor (b) recommends** that this session should have drafted the short, honest note about
the receiver's frozen dashboard *"as an unshipped text file sitting in the drafts directory, so it
exists when the architect opens this on 2026-09-05."*

**REFUSED, and the reason is not that the idea is bad.** The idea is good, and part (b) is right that
Q2 is the live question. It is refused because `CONDITIONS-128.md` says **"No delivery object"** and
then lists what the next session may do *"and nothing else on this arc"* — three items, none of them
this. A drafted letter held back from sending is a delivery object at an earlier stage, not a
different kind of thing; that is exactly the reasoning by which five consecutive states of this
bundle came to carry no verdict at all. **A stop that a later session may reinterpret when it sees a
good enough reason is not a stop**, and this arc has now spent nine gauntlets learning what happens
to rules that nothing refuses.

**What is done instead, which is all this practice may do:** Q2 is recorded as open in
`memory/open-questions.md`, the adversary's framing of it is quoted there, and the point is put to
the architect in `REQUESTS.md` — where the *"worth it"* limb already sits, unanswered, and where the
decision about what follows the reading belongs.

---

## Binding on the next session

1. **The stop is unchanged and unsoftened.** No delivery object, no repair pass, no gauntlet, no
   packet from this arc before 2026-09-05. This session added nothing to the licence and removed
   nothing from it.
2. **The daily instrument keeps running.** Day 10 closed this session; day 11 is due at 03:41:00Z.
3. **If a move opens on this arc at all**, item 2 of `CONDITIONS-128.md` is now **discharged** — the
   record has been read over its whole length, the report to its last line, and both are published
   with their reviews. **There is no third reading of this evidence to do.** What remains on this arc
   is the instrument, and nothing else.
4. **Q1 is open**, narrower than this session left it and narrower than the post-mortem left it.
   **Q2 is open and untouched**, and it is the one an adversary has now twice said is the real
   question.
