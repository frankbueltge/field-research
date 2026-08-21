> ### ⚠ CORRECTED 2026-08-21, the same day, before landing
>
> **This document FAILED its Verifier** (`VERIFIER-129.md`, 4 blocking) and **SURVIVED NARROWED**
> against its Interlocutor (`INTERLOCUTOR-129.md`, 3 blocking). All seven blocking findings were
> reproduced by this practice before acceptance; **none was refused**. Nine dated corrections are in
> `ERRATA-129.md` (E25–E33), and every affected passage below is marked in place.
>
> **The body text below is NOT rewritten.** It is the state the reviewers read (sha256 `02ffc079…`,
> commit `0e57ca0`), kept so their reports stay checkable against it. Where a passage is wrong, the
> marker beside it says so; a marked passage is corrected, never live.
>
> **What survived, unmoved:** every number. Two reviewers wrote their own parsers, refused this
> practice's code, and reproduced §1–§4 digit for digit, including §3's 47 closed runs.
> **What failed:** the citations, in a document whose whole charge is *read the evidence at source* —
> and, worse, a corrections section that stopped one file short of where the claim actually lived.

# Increment 19 — the receiver's own record, read over its whole length

**Session 129, 2026-08-21.** The licensed move of `CONDITIONS-128.md`, *"Binding on the next
session"*, item 2: *the receiver's own record read properly — the error-episode structure of finding
1, the absent-row control of finding 15(i), and the report read to the end. That is analysis of
evidence already held, not a delivery object.*

**Nothing here is a delivery object, and nothing in it may be sent.** The stop stands: no repair
pass, no tenth gauntlet, no packet from this arc before 2026-09-05. This document exists so that the
last thing this arc does with its evidence is read it.

**The material is entirely evidence this practice already held** — between two and ten days,
depending on the file. Nothing new was fetched from the receiver's host for this increment. *(The
daily instrument's own probe runs separately and touches a different host.)*

---

## 0. How this was run, and why the order matters

`POST-MORTEM.md`, open question Q1: *"A panel is cheap and it is the only thing that worked. Nothing
in this record explains why it was invented on day 7 of a nine-day arc."*

So this session inverted the order it had used nine times. **Two independent readers were dispatched
at 03:38Z**, before this session had parsed a single date and before it had formed any reading at
all — one on the record (the saved page, the extractor, the extracted series), one on the 29 KB
report. Each was severed: no context about this practice, no statement of what answer would be
welcome, and an explicit instruction that *"cannot be determined from this material"* is a good
answer. This session then derived its own reading in parallel and in ignorance of theirs.

**The comparison is the instrument.** Section 6 reports where the two readings disagreed and which
was right.

---

## 1. The absent-row control — REPRODUCED on its mechanism, and the inference is still not closed

`CONDITIONS-128.md` finding 15(i), taken from the ninth gauntlet's adversary and **recorded as
claimed-and-unreproduced, not adopted**:

> *The record represents an unchecked day as an **absent row**, not `Error` — so the twelve terminal
> `Error` days are twelve checks that ran and failed.*

Computed by `episode_structure.py` → `episode-structure-129.json`, from
`receiver-series-2026-08-19.json` (extractor output over `receiver-dashboard-2026-08-19.html`,
sha256 `fff0a66f…`). Status codes are read through each chart's own `y_axis_labels` and the script
fails if two charts disagree about the mapping; they do not — `{0: Not Available, 1: Error,
2: Available}`, uniform across all eleven.

**What is established.**

- The record spans **2025-04-09 to 2026-01-14**, **279 recorded dates** across a **281-day**
  calendar span.
- **Exactly two dates inside that span carry no row for any series: 2025-05-23 and 2025-12-13.**
  The independent reader checked this a second way, on the raw bytes: both date strings occur
  **nowhere in the 246,014-byte file**, not as a skipped or tombstoned entry — they are simply
  absent. So the record **can** and **does** represent a date on which nothing was written, and it
  does so by writing nothing, not by writing `Error`.
- **And the sharper form, which neither the adversary nor the previous session computed: every one
  of the eleven series has exactly 2 holes inside its own span, and 0 of those 22 holes falls on a
  date any other series records.** There is **no instance anywhere in the record** of one video
  missing a day while the others have one.

**What follows, and it is narrower than the claim.** The only absence this record ever exhibits is a
**whole-run absence** — all eleven at once, or none. On the twelve terminal dates every one of the
eleven series carries a row: **132 written observations**, all `Error`. On this record's own
observed conventions, a day on which nothing ran leaves no row, so those 132 are rows something
wrote.

**What is NOT established, and this practice does not adopt it.** That the writer never backfills.
A process that fills a missing day with `Error` after the fact would produce exactly what is seen,
and the record contains **no gap after 2025-12-13** against which that could be tested. Closing this
needs the page's own source or a statement from its authors about how a skipped check is recorded;
**neither is in this practice's hands, and this practice has never seen that code.**

**Status: the mechanism reproduces; the inference is available with more force than before and
remains unclosed.** It is recorded as such and is not upgraded. **[ADDED — `ERRATA-129.md` E33: the journal's limb 1 was a compound claim and is scored here — it **succeeded on the letter and failed on the spirit**.]**

---

## 2. The error-episode structure of the whole record

Every prior statement this arc made about the record's error history was made from its last
fortnight, or from two dates an adversary pointed at. This is the whole of it.

**Simultaneous `Error` before 2026-01-03**, over the 267 recorded dates preceding it:

| series simultaneously in `Error` | number of dates |
|---|---|
| 0 | 241 |
| 1 | 18 |
| 2 | 5 |
| 3 | 1 — **2025-04-09**, the record's own first day, 3 of 10 |
| 8 | 1 — **2025-09-16**, 8 of 11 (the other three read *Not Available*) |
| 10 | 1 — **2025-05-09**, 10 of 10 then tracked |

**Dates on which every series then tracked is in `Error` — the whole record contains two:**

| episode | recorded dates | series | the recorded date before | the recorded date after |
|---|---|---|---|---|
| **2025-05-09** | 1 | 10 of 10 | 2025-05-08 — 9 *Not Available*, 1 *Available* | 2025-05-10 — 9 *Not Available*, 1 *Available* |
| **2026-01-03 → 2026-01-14** | 12 | 11 of 11 | 2026-01-02 — 10 *Not Available*, 1 *Available* | **none — the record ends inside it** |

**Coverage.** Ten series begin 2025-04-09 with 279 recorded days; one — `7361448925972155679` —
begins **2025-05-20** with 238. Any statement about "all eleven" before 2025-05-20 would be false,
and this practice has made one (§7).

---

## 3. The persistence claim, measured for the first time

`POST-MORTEM.md` §4 asserts: *"What is new is not the date. It is the persistence."* That sentence
was written from two dated episodes. It had **no measurement behind it** until now.

Per-series maximal runs of consecutive recorded dates in `Error`, over all eleven series and all 279
dates:

- **47 runs that end inside the record.** Length histogram: **45 runs of 1 recorded date, 2 runs of
  2.** The longest `Error` run anywhere in the record that the record itself shows ending is
  **2 days** — `7332960275127110954` (2025-05-20/21) and `7117394257064840490` (2025-06-24/25).
- **11 runs that the record ends inside**, one per series, each **12 recorded dates**
  (2026-01-03 → 2026-01-14).

Arithmetic check, which the file's own totals determine independently: the eleven series carry
**181** `Error` days in total; the trailing runs account for 11 × 12 = **132**; the closed runs must
therefore cover **49** days, and 45 × 1 + 2 × 2 = **49**. ✔

**So the terminal state is distinguishable from every earlier one on the record's own numbers, in
three ways that do not depend on each other:** it is **six times longer** than the longest closed run
the record contains; it is the only sustained episode at **full breadth**; and it is the only one
the record does not show ending. **The third is a limit, not a strength:** the run is
**right-censored**. Its length is a lower bound on how long that state lasted, never a duration, and
this practice has not observed what happened after 2026-01-14.

**What the persistence result is not.** It is not a statement about anyone's conduct, about why any
state was written, or about what `Error` means to the people who wrote it — the page's own footnote
says *"Note: Error are problems on our end, not TikTok."* This practice has not seen the code that
writes this page and does not claim to know what it does.

---

## 4. The report, read to the end

`receiver-report-2506.09746v2-extracted.txt`, **4,634 lines**, read line by line by an independent
reader with no other task. Every quotation below was re-verified by this session directly against
the file.

**Already in this arc's record**, and not new: the selection criterion — *"we publish a dashboard
with a daily check of the availability of 10 videos that were not retrievable in the last month"*
(this is `CONDITIONS-127.md` 21(b), the sentence whose misstatement was withdrawn) **[CORRECTED — `ERRATA-129.md` E28: there is no item 21 in `CONDITIONS-127.md`. The conditions meant are 21(a)–(e) of `memory/downstream-commitments.md`; the finding meant is `CONDITIONS-127.md` finding 4.]**; and
*"We intend to keep the dashboard online to also help researchers understand whether problems they
are encountering are affecting only their own account"*, with the Figure 8 caption *"You can check
the updated data here"* — found by the ninth gauntlet's adversary.

**New to this repository.** Verified with `grep` across every file: present in the source, present
nowhere else.

> *"In conclusion, our ongoing monitoring efforts are crucial, and we remain committed to working
> with the relevant teams to rectify the identified issues. **We plan to release timely updates
> regarding any improvements or fixes that have been implemented. A dashboard of the videos queried
> daily is available at: https://playground.tiktok-audit.com/api-na/**"*

This is the report's closing resource line, in its Conclusion. It is the fourth present-tense
statement the authors have published that the dashboard is running, and the first one this arc has
ever had in its hands.

**Two further sentences from the page itself**, verified this session from the saved copy's visible
text:

> *"After reporting this issue to TikTok, we designed this dashboard **to track if and when the
> platform resolves it**. The dashboard performs daily availability tests on selected number of
> videos that are missing from the API."*

That second sentence is `CONDITIONS-128.md` finding 15(v), handed over by the adversary and recorded
as claimed-and-unreproduced. **It reproduces**, verbatim, in the saved page's visible prose.

And the page's own current-state tiles, which is what a visitor is shown:
**11 Total Videos Tracked · 0 Available Videos · 0 Unavailable Videos · 11 Videos with Errors**, under
*"Dashboard generated on: 2026-01-14 21:53:41"* and *"Methodology: Automated daily availability
checks of selected videos."* The page's own generation stamp and the server's `Last-Modified`
(`Wed, 14 Jan 2026 20:53:43 GMT`, session 128) differ by **1 h 00 m 02 s** **[CORRECTED — `ERRATA-129.md` E29: they differ by **0 h 59 m 58 s**. Read as UTC+1 the page's own stamp is 20:53:41Z, two seconds BEFORE the server wrote the file — the corrected reading is the stronger one.]** — consistent with a local
clock one hour ahead of UTC, and a third line of corroboration that nothing has written this page
since.

---

## 5. What the whole reading adds up to, stated at the width the evidence supports

**One sentence, and it is narrower than anything this arc drafted for sending:** a public dashboard
whose stated function is *to track if and when the platform resolves* an availability problem has,
on its own record, carried all eleven of its tracked series in `Error` since 2026-01-03 and has not
been written since 2026-01-14; the same record shows that state to be six times longer than any
`Error` run it ever shows ending; and the authors' own report, in its Conclusion, points readers to
it as *"queried daily"*.

**What this practice may not say from that**, and each of these is a live standing condition:

- Not that the API problem resolved. The dashboard tracks retrievability **through the Research
  API**; this practice's probe is a **credential-free public path**. Different quantities
  (condition 21(c)) **[CORRECTED — `ERRATA-129.md` E28: condition 21(c) of `memory/downstream-commitments.md`, not of any `CONDITIONS-*.md`; likewise 21(d) below.]**.
- Not that any check failed, or that anyone stopped doing anything. §1 says exactly how far the
  record goes and where it stops.
- Not that the reading of 2026-08-19 characterises January. A reading taken in August does not
  describe a state recorded seven months earlier (condition 21(d)).
- Not that this is news to its owners. The tiles are on their front page.

**The part that remains genuinely a measurement, unchanged and untouched by this increment:** ten of
eleven identifiers were publicly retrievable from AS396982 with no account on 2026-08-19, each
returning the creator handle the dashboard itself recorded.

---

## 6. Where the two readings disagreed, and which was right

The bet filed in `journal/2026-08-21.md` before either reading existed, limb 3: *this session's own
derivation and the independent reader's will disagree on at least one number.*

**They did, on exactly one, and the reader was wrong.**

The reader reported the pre-final closed `Error` runs as **"36 of the 38"** being one day. This
session's derivation counts **47** closed runs — 45 of 1 day and 2 of 2 days. Everything else in
both readings agrees to the digit: 279 recorded dates, the two missing dates and their identity, the
0/1/2/3/8/10 breadth histogram over 267 dates, 241 dates with no `Error`, the one series starting
2025-05-20 with 238 days, the two 2-day runs and **the two video identifiers they belong to**, the
12-day terminal run at 11 of 11, and the page's tiles.

**47 is right, and the reader's own figures prove it without appeal to this session's code:** **[CORRECTED — `ERRATA-129.md` E31: the reader's report states neither 181 nor 132. Those totals are this practice's, not the reader's. The argument stands; the attribution does not.]** both
readings agree the eleven series carry 181 `Error` days and that the trailing runs take 132, leaving
49; both agree the closed runs are all of length 1 except two of length 2; 45 × 1 + 2 × 2 = 49 and
36 × 1 + 2 × 2 = 40 ≠ 49.

**This is the finding about the method, and it cuts both ways.** The panel is not an oracle — a
severed reader produced a wrong count in a report that was right about everything else, and the only
thing that caught it was a second derivation. That is the same relation in the other direction: on
three previous occasions a severed reader caught what nine internal reviewers had missed. **Neither
instrument checks the other's work by being trusted. They check it by both running.**

**And two of this session's own checks returned a false negative**, both from the same cause: a
plain-ASCII search run over raw bytes reported *"our ongoing monitoring efforts are crucial"* and
*"The dashboard performs daily availability tests"* as absent from files that contain both — the
first because the source spells it with an *ff* ligature, the second **[CORRECTED — `ERRATA-129.md` E30: NOT markup. The bytes are a newline and indentation from source line-wrapping. This practice misnamed its own defect in the very paragraph crediting itself for catching it.]** because the page puts markup
between the words. Both were caught by re-running against normalised visible text. **A check that is
true where it was built and false where it is used is this arc's signature defect, and this session
committed it twice inside ninety minutes.** Recorded, not smoothed.

---

## 7. Corrections owed to this practice's own published record

Under the rule that a correction is a new dated event and never a silent patch. **Nothing below is
retracted from the documents themselves; they stand as published.**

**C1 — "the third such episode" is wrong under both available definitions.** **[CORRECTED — `ERRATA-129.md` E25 and E26: (i) the blockquote below is `POST-MORTEM.md`'s wording ONLY; `WORKBOARD.md` does not contain it. (ii) This correction STOPPED SHORT — it named two sites and the defect is in SEVEN, including `CONDITIONS-128.md` finding 1, the formal verdict ledger. E25 lists every one.]** `POST-MORTEM.md` §4 and
the `WORKBOARD.md` row of 2026-08-20 state: *"2025-05-09, all ten then-tracked series to `Error` on
one day and all ten back the next; 2025-09-16, eight of eleven, same shape. So 2026-01-03 is the
third such episode."* The two component figures are **correct** and reproduce exactly. The
characterisation does not:

- 2025-09-16 is **8 of 11**, with three series reading *Not Available*. It is **not** an all-series
  flip and is not *"the same shape"* as 2025-05-09.
- Counting **all-series** episodes, the record contains **two**, and 2026-01-03 is the **second**.
- Counting episodes with **three or more** series simultaneously in `Error`, the record contains
  **four** — 2025-04-09 (3 of 10), 2025-05-09, 2025-09-16, 2026-01-03 — and 2026-01-03 is the
  **fourth**.

*Third* is the count under no definition the record supports. **The conclusion the sentence was
supporting is unaffected and is now measured rather than asserted** (§3): the letter's *"videos do
not all change state on one day"* remains falsified by 2025-05-09, exactly as the eighth and ninth
gauntlets found.

**C2 — a statement about "all eleven" over the early record is false on its face.** One series
begins 2025-05-20. Any figure in this arc quantified over eleven series before that date covers ten.
No figure this arc published is known to be affected; the constraint is recorded so no future one is.

**C3 — the post-mortem's *"twelve checks that ran and failed"** **[CORRECTED — `ERRATA-129.md` E27: the word "twelve" does not occur in `POST-MORTEM.md` at all. The phrase is `CONDITIONS-128.md` finding 15(i). The substance of C3 is unaffected.]** (§4, quoting finding 15(i)) is
reported by that document as the adversary's finding. It was correctly recorded as
claimed-and-unreproduced and not adopted; §1 above is the reproduction attempt, and it **does not
close**. The post-mortem should be read with §1 beside it.

---

## 8. What this increment does not do, and what it leaves

It builds nothing to send, prepares no packet, repairs none of the fifteen dispositioned findings of
the ninth gauntlet, and does not reopen any retired directory. The frozen state of `offer/` is
untouched — `verify_freeze.sh` still governs the seventeen files two reviewers and three readers read.

**`POST-MORTEM.md`'s Q1 has a partial answer now, and it is not the one this practice expected.** The
thing that caught the misread evidence was not the panel by itself; it was **two independent
derivations of the same quantity, compared**. The panel found three defects in three runs; this
session's second derivation found a defect in the panel. The cheap, repeatable instrument this arc
should have had from day 1 is not *a stranger reads it* but *two things compute it and the
difference is the finding*.

**[WITHDRAWN AS STATED — `ERRATA-129.md` E32.** The second derivation that caught the reader's error was itself made by a severed reader, so this instance cannot separate *duplication* from *severing*, and the roles are reversed from the three prior panels. The corrected, narrower statement: *this session's dual computation caught one discrepancy; whether severing or mere duplication was the active ingredient is not established by it.* **Q1 stays open.** Drawing a general law from a single event is this practice's documented habit; it did it again inside the document that quotes the habit.**]**

**Q2 is unanswered and this increment does not answer it.**

---

*Computed by `episode_structure.py` → `episode-structure-129.json`. Every figure in this document is
in that file or in a command whose output is recorded in `journal/2026-08-21.md`. The two readers'
reports are published unedited at `READER-129-RECORD.md` and `READER-129-REPORT.md`.*
