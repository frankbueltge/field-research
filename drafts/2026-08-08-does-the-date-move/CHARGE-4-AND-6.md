# The two charges that decide the arc — answered in one page

*Session 102, 2026-08-08. `RESULT-2.md` bound this session: "Session 3 either answers that in one
page or the concept is rewritten as a coverage finding and discarded with one." The charges are the
Interlocutor's 4 and 6 from `INTERLOCUTOR-2.md`, accepted and unanswered at session 2. Both are
answered here; **one of them is conceded**, and the concession changes what this investigation is.*

---

## Charge 4 — "you are measuring a duty the receiver only recommends"

> *"The movement 'tip' was never a duty, and C1 already conceded that — so calling for a checkable
> measurement of it is scope invented by the practice, not demanded by the receiver."*

**Conceded. The charge is correct, and this session checked it a second time and found against
itself.**

Correction C1 (session 101) established that *"Update the date if the content changes
substantively"* sits under **"How to implement — These are tips to help you implement this
standard."** This session re-fetched the page (https://standards.digital.gov/standards/content-timeliness-indicator/,
HTTP 200, 2026-08-08) and read its **heading structure**, because one thing C1 had not checked was
whether the per-content-type block was a separate, binding section. It says, five times over, for
five of the six named content types:

> *"Add an 'Updated' date if the information substantively changed after it was first published."*

That block is **`<h3>` "Timeliness indicator options for types of content", nested inside the `<h2>`
"How to implement"** — the tips section. It is not an acceptance criterion. **The movement duty is
implementation guidance in every place it appears on that page, and the charge stands on the letter.**

We also looked for a demand and did not find one. The page's own feedback channel — a public
discussion opened by the standard's author (https://github.com/GSA-TTS/federal-website-standards/discussions/188,
opened 2024-09-09) — asks stakeholders about the **language** of the indicator ("Do users have
preferences for the language used (published, updated, or reviewed)?"), whether it should be
standardised by content type, how users respond to multiple dates, and preferences on the interval
between updates. **Nothing in it asks for verification, compliance measurement, or accuracy.** We
looked; it is not there; we say so.

### What survives the concession, and it is a different object

Two sentences on that page are **not** tips. They are the standard itself and its stated purpose:

> **Standard.** *"Inform users about the timeliness of content by including the date of publication,
> a last updated date, or a last reviewed date as relevant for your content and audience."*
>
> **Why.** *"Timeliness indicators can increase user trust in the currency and accuracy of
> information."*

And the **binding** acceptance criterion — *"These conditions must be met to comply with this
standard"* — requires the **presence** of a timeliness indicator on six named content types.

So the question this investigation can legitimately ask is not *"do agencies obey the tip?"* but:

> **Does the indicator the binding criterion requires actually inform anyone about timeliness?**

That is not a compliance measurement of an implementation tip. It is evidence about whether the one
condition the receiver does bind delivers the purpose the receiver states for it. And it is
answerable without any judgement about substantive change, because a date that **twenty-four
unrelated documents published between 1982 and 2015 carry to the same day** is present, is compliant
with the presence criterion, and informs a reader of nothing about any of those documents
(`RESULT-3.md`, NIST).

**The old object is withdrawn, dated, in the record: `CORRECTIONS.md` C3.** `CONCEPT.md` §2 promised
the receiver *"a compliance measurement of their own draft criterion, per agency domain"*. That
promise is dead. What replaces it is offered as evidence for the iteration the page itself says it is
in — *"Draft … being shared with federal agencies and other stakeholders for feedback and
iteration"* — and it carries this sentence on its face, not in a caveat:

> **The receiver did not ask for this measurement. The fit is to the purpose its own page states,
> not to a request it made.**

Nothing is addressed to anyone; the receiver is named in the packet and never contacted.

---

## Charge 6 — "the receiver's own 16-page site is not the population its standard governs"

> *"Finding date confusion in the referee's own scorekeeping is a fair 'physician, heal thyself' jab,
> but it is a weak basis for concluding an artifact built from it 'remains something the receiver
> could use' against the actual population of agency sites the standard is meant to police — none of
> which have been probed this session."*

**Answered by construction, not by argument.** Increment 3B's scored population is **160 pages of two
United States executive-branch agency websites** — 80 NIST publication records, 80 EPA news releases
— which is the standard's own scope line: *"Applies to: Executive branch agency websites and digital
services that are intended for use by the public."* **The receiver's own 16-page site contributes
nothing to any scored number in `RESULT-3.md`**, and GOV.UK appears only as a positive control for
the method and is labelled out of scope everywhere it appears.

**Two caveats we volunteer rather than wait to be caught on:**

1. **Only one of the two arms is clearly inside the binding criterion.** EPA news releases are
   *"News, press releases"* — the first of the six content types the acceptance criterion names. NIST
   publication records are inside *"Applies to"* but are not obviously any of the six named types.
   The NIST arm is in the standard's **scope**; it is not demonstrably in its **criterion**.
2. **And the effect is on the arm that is not clearly in-criterion.** NIST's printed update date
   collapses onto 14 values across 79 pages; EPA's does not (61 values across 80). We predicted the
   opposite for EPA and were wrong, in writing, before the fetch (`PREREGISTRATION-3B.md` Q1, Q2).
   This complicates the receiver's interest in the finding and it is stated on the artifact's face.

**What charge 6 correctly kills:** any sentence of the form "the receiver's own site shows X,
therefore agencies show X". No such sentence survives into `RESULT-3.md`.

---

## What the two answers together do to the arc

Charge 6 is answered. Charge 4 is **conceded**, and conceding it costs the investigation the object
it was opened with. What is left is smaller, harder to sell, and — on this session's evidence —
actually measurable: **a printed date required by a binding criterion, which on one authority in the
governed population does not resolve the documents it is printed on.** Whether that is worth an arc
is the gate's question, and it goes to an Interlocutor before this session answers it.

---

## **[WITHDRAWN THE SAME SESSION — 2026-08-08, see `CORRECTIONS.md` C4 and `INTERLOCUTOR-3.md`]**

The reframing above — that measuring what the printed indicator resolves is evidence about whether
the **binding** criterion delivers the standard's stated purpose — **did not survive its first
adversary, and the refutation used this practice's own data.** The Standard is **disjunctive**:
*"the date of publication, **or** a last updated date, **or** a last reviewed date."* NIST prints a
publication date beside the update date, and on the same 329 pages that date has **291 distinct
values (ratio 0.885)** against `Updated`'s **24 (0.073)**. A page carrying a document-specific
publication date is not a page that fails to tell a reader when the document dates from.

**The text above is left standing, uncut, as the record of what was argued.** What remains true of
it: charge 4 is conceded, charge 6 is answered by the population, and both caveats it volunteers are
the ones the adversary then used. The gate did not pass; the concept is discarded; the one page it
owes is `FINDING.md`.
