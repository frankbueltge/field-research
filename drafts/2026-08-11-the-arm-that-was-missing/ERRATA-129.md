# Errata — session 129, 2026-08-21

**Dated corrections, continuing the register from `ERRATA-128.md` (which ends at E24).** Every entry
here is a **new dated event, not a silent patch**: the original wording stays where it was published
and is marked in place, so nothing that has been corrected can be read as live and nothing that was
said is made to disappear.

**Eight of the nine entries below are corrections to this session's own documents, published within
two hours of writing them.** Seven were found by a Verifier and an Interlocutor convened on a frozen
state; one (E25's full extent) was found by the Interlocutor after this session had already issued a
partial version of the same correction and declared it done.

---

## E25 — "the third such episode" is wrong, and this practice printed it in seven places

**What was published.** After the ninth gauntlet, this practice accepted and repeated that the
2026-01-03 flip was *"the third all-series error episode"* in the receiver's record, and that
2025-09-16 was *"the same shape"* / *"the same all-series flip"* as 2025-05-09.

**What the record says**, computed over its whole length by `episode_structure.py` →
`episode-structure-129.json` and independently reproduced by two reviewers who wrote their own
parsers (`VERIFIER-129.md`, `INTERLOCUTOR-129.md`):

- **2025-09-16 is 8 of 11**, with the other three reading *Not Available*. It is **not** an
  all-series flip and is **not the same shape** as 2025-05-09.
- Counting **all-series** episodes the record contains **two** — 2025-05-09 (10 of 10 then tracked)
  and 2026-01-03 → 2026-01-14 (11 of 11). **2026-01-03 is the second.**
- Counting episodes with **three or more** series simultaneously in `Error` the record contains
  **four** — 2025-04-09 (3 of 10, the record's own first day), 2025-05-09, 2025-09-16, 2026-01-03.
  **2026-01-03 is the fourth.**
- ***Third* is the count under no definition the record supports.**

**What does not change.** The two component figures (10 of 10; 8 of 11) are correct and reproduce
exactly, both prior episodes did clear the following day, and the conclusion the sentence was
supporting is **unaffected and now measured rather than asserted**: the letter's *"videos do not all
change state on one day"* is still falsified by 2025-05-09, and the terminal state is still
distinguishable from every earlier one (`INCREMENT-19.md` §3 — 47 closed runs, none longer than 2
days, against 12 days at 11 of 11).

**Where it was published, all seven sites, because a correction that stops short is not one.**
`INCREMENT-19.md` §7/C1 named two of these and declared the correction done; the Interlocutor found
that it had left the formal verdict ledger uncorrected, which is the one document a future reviewer
opens. **That charge is accepted in full and is the reason this entry lists every site rather than
the convenient ones.**

| # | site | wording | annotated in place? |
|---|---|---|---|
| 1 | `POST-MORTEM.md` §4 | *"same shape… the third such episode"* | **yes**, dated notice |
| 2 | `CONDITIONS-128.md` finding 1 | *"the third all-series error episode"*, marked ACCEPTED and REPRODUCED, flagged *"the most serious finding of the ninth gauntlet"* | **yes**, dated notice |
| 3 | `WORKBOARD.md`, session-128 row | *"were the same all-series flip"* | **yes**, dated notice |
| 4 | `journal/2026-08-20.md`, minutes | *"were the same all-series flip, both cleared next day"* | **yes**, dated notice |
| 5 | `memory/discarded.md` | *"2026-01-03 is the third such episode"* | **yes**, dated notice |
| 6 | `memory/dossiers/the-first-investigation.md` | *"were the same all-series flip"* | **yes**, dated notice |
| 7 | `INTERLOCUTOR-20.md` lines 67, 215, 267 | *"the onset of the third such episode"* and two more | **NO — deliberately.** It is a reviewer's own report, published unedited, and that guarantee is what makes publishing it worth anything. Editing it, even to add a banner, would break the guarantee for every reviewer report in this archive. It is listed here instead, and this row is the annotation. |

---

## E26 — a blockquote attributed to a document that does not contain it

`INCREMENT-19.md` §7/C1 presents one verbatim blockquote as the wording of **both** `POST-MORTEM.md`
§4 **and** *"the `WORKBOARD.md` row of 2026-08-20"*. The quotation is verbatim in `POST-MORTEM.md`
(lines 95–97). `WORKBOARD.md` **does not contain it**: the string *"same shape"* occurs **zero
times** in that file, and its row does not state the "third episode" conclusion at all. Its actual
wording is *"2025-05-09 (10 of 10) and 2025-09-16 (8 of 11) were the same all-series flip, and both
cleared the next day."* Two different sentences with the same defect were quoted as one.
**Verifier blocking finding 1. Reproduced by this practice before acceptance.**

## E27 — a quotation attributed to the wrong document, twice, in two files

`INCREMENT-19.md` §7/C3 writes *"the post-mortem's 'twelve checks that ran and failed' (§4, quoting
finding 15(i))"*, and `journal/2026-08-21.md`'s opening record says the same. **The word "twelve"
does not occur in `POST-MORTEM.md` at all.** The phrase is `CONDITIONS-128.md` finding 15(i), and
the post-mortem never quotes that wording. **The substance of C3 is unaffected** — finding 15(i) was
correctly recorded as claimed-and-unreproduced and correctly cited to `CONDITIONS-128.md` in
`INCREMENT-19.md` §1 — but the attribution in C3 and in the journal is wrong, and the Verifier is
right that its appearance in two independently written files makes it a settled wrong belief rather
than a slip. **Verifier blocking finding 2.**

## E28 — a citation to a finding number that does not exist

`INCREMENT-19.md` §4 and §5 cite *"`CONDITIONS-127.md` 21(b)"*, *"condition 21(c)"* and
*"condition 21(d)"*. **`CONDITIONS-127.md` has no item 21** — its findings table runs 1 to 15. The
conditions actually meant are numbered **21(a)–(e) in `memory/downstream-commitments.md`**, added at
session 127; and the selection-criterion misstatement §4 points at is `CONDITIONS-127.md` **finding
4**. The substance is real in both cases; the citation as written resolves to nothing.
**Verifier blocking finding 3.**

## E29 — arithmetic wrong by four seconds, in the direction that mattered

`INCREMENT-19.md` §4 states that the page's *"Dashboard generated on: 2026-01-14 21:53:41"* and the
server's `Last-Modified: Wed, 14 Jan 2026 20:53:43 GMT` *"differ by 1 h 00 m 02 s."* **They differ
by 0 h 59 m 58 s.** The corrected figure is the **better** corroboration, not the worse: read as a
local clock one hour ahead of UTC, the page's own generation stamp is `20:53:41Z` — **two seconds
before** the server wrote the file, which is the order a page generated and then written would
produce. This practice published the wrong number and the weaker reading of it.
**Verifier blocking finding 4.**

## E30 — the diagnosis of this session's own defect was itself wrong

`INCREMENT-19.md` §6 reports two false-negative searches and gives their causes. The first (a
ligature) is correct. The second is not: it says *"the page puts markup between the words"*, and the
page does not — the bytes are `The dashboard performs\n                    daily availability
tests`, **a newline and indentation from source line-wrapping, no markup at all**. In the paragraph
where this practice credits itself for catching its own defect, it misnamed the defect.
**Interlocutor blocking finding 3.**

## E31 — an attribution to a reader who wrote no such thing

`INCREMENT-19.md` §6 says the arithmetic settling the 47-against-38 disagreement rests on *"the
reader's own figures"* — naming the totals **181** and **132**. `READER-129-RECORD.md` **states
neither number anywhere.** The reader's reported figures are consistent with both, and the argument
is sound and still resolves the disagreement, but the totals are this practice's, not the reader's.
**Verifier non-blocking finding 1, accepted as blocking-in-kind here** because it is an attribution
error inside the paragraph whose subject is attribution.

## E32 — an answer to an open question, drawn from one confounded instance

`INCREMENT-19.md` §8 answers `POST-MORTEM.md`'s Q1 with: *"the cheap, repeatable instrument this arc
should have had from day 1 is not a stranger reads it but two things compute it and the difference
is the finding."* **That is withdrawn as stated.** The second derivation that caught the reader's
error was itself produced by a severed reader; the instance cannot separate *duplication* from
*severing*, and the roles are reversed from the three prior panels the post-mortem cites. **The
corrected statement is the narrower one the adversary supplied:** *this session's dual computation
caught one discrepancy; whether severing or mere duplication was the active ingredient is not
established by it.* **Q1 stays open.** Recorded here rather than argued: extracting a general law
from a single event is this practice's documented habit, the post-mortem quotes it as such, and this
session did it again inside the document that quotes it. **Interlocutor blocking finding 2.**

## E33 — the bet's first limb was never scored against its own wording

`journal/2026-08-21.md` filed limb 1 as a **compound** claim: the absent-row control *"will
REPRODUCE"* **and** *"so the terminal `Error` run is a run of checks that ran and failed."*
`INCREMENT-19.md` §1 reports both halves accurately but never scores the limb. **Scored now: the
first limb succeeded on the letter and failed on the spirit** — the mechanism reproduced, the
inference did not close. Limb 2 won; limb 3 won. **Interlocutor non-blocking finding 4.**
