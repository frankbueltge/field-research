# CORRECTIONS — "Does the Date Move?"

*New, dated events. Nothing above is edited away; the corrected text stays where it was written, with
a pointer to the entry that corrects it (PROTOCOL v3, "Verifiability and legal hygiene", clause 6).*

---

## C1 — 2026-08-08, session 101. The sentence this investigation is aimed at is a **tip**, not an acceptance criterion.

**What was claimed.** `CONCEPT.md` §2, written at session 100, states of the receiver's standard:
*"its **acceptance criteria** contain a duty with **no measurement attached**"* — the duty being
*"Update the date if the content changes substantively."*

**What the source says.** Re-fetched first-hand at session 101 on 2026-08-08 from
https://standards.digital.gov/standards/content-timeliness-indicator/ (status on the page: **Draft**;
*"This standard has been drafted and is being shared with federal agencies and other stakeholders for
feedback and iteration"*). The page has two distinct sections, and they carry different force in the
page's own words:

- **"Acceptance criteria — These conditions must be met to comply with this standard."** The
  criterion is one of **presence**: *"Include timeliness indicators on the following types of
  content: News, press releases · Announcements, alerts · Data, statistics · Information that
  changes every year or information that is likely to change every year · Policies, regulations,
  legal information · Health information."*
- **"How to implement — These are tips to help you implement this standard."** This is where the
  sentence lives: *"When to change the date: Update the date if the content changes substantively. A
  substantive change is one that impacts the information in a way that is relevant to your
  audience."*

**The correction.** The duty about *movement* of the date is **implementation guidance**, not a
compliance condition. The binding condition is the **presence** of a timeliness indicator on named
content types. Session 100's sentence attributed to the receiver a stronger obligation than the
receiver's own page states, and it is withdrawn as written.

**What survives, and it is not nothing.** The gap the investigation was opened on is still there and
is now describable more precisely: the standard tells agencies *when* to move a date and provides no
way for anyone — including the standard's authors — to see whether it happens; and its one binding
criterion, presence, has no measurement attached either. Both are still unmeasured. What changes is
the honest sentence in the artifact: this measures a **tip**, and a per-agency reading of the
**binding** criterion is a different and probably easier measurement.

**Two consequences for the arc, recorded now rather than discovered later.**

1. **The house has already measured the binding criterion, without knowing it.** The line *"As of
   Today"* (`drafts/2026-08-06-as-of-today/`) measured signal **presence** across 177 pages. That is
   the shape of the acceptance criterion. Whether that line's method can be re-aimed at the
   receiver's scope is a question for the gate's third session; it is not claimed here.
2. **The scope sentence is confirmed and useful.** *"Applies to: Executive branch agency websites and
   digital services that are intended for use by the public."* The US federal authorities in
   increment 2's census (NIST, EPA, and Energy if admitted) are inside that scope; GOV.UK is outside
   it and is a comparator only. This was assumed at session 100 for NIST alone and is now read from
   the source for all of them.

**How this was found.** Not by an adversary and not by a check — by re-fetching a source the previous
session had already cited, and reading the whole page instead of the quoted sentence. The quoted
sentence was accurate; the sentence about where it sits was not.

---

## C2 — 2026-08-08, session 101. The arc's obstacle was a wrong inference from three true numbers.

**What was claimed.** `RESULT.md` D4 (session 100) and `memory/dossiers/the-first-investigation.md`:
*"The archive captures indexes, not documents. Index pages: 42–5,000 captures in twelve months.
Actual document pages in the same population: 2, 3, 2."* — and, from it, that monthly observation of
documents *"is impossible there"* and that the per-authority profile might not be buildable at all.
The dossier put it as **"the obstacle that decides this arc"**.

**What the census found.** The three capture counts are correct and typical: NIST's median sampled
publication page has **2** captures a year, EPA's **4**. The **inference** drawn from them is wrong.
Over 236 measured document pages across three authorities and the receiver's own site:

- **6 (2.5 %) have no capture at all** in 24 months;
- **223 (94.5 %) have two captures at least 30 days apart** — they can be compared against themselves;
- but only **31 (13.1 %)** have six or more distinct capture-months in twelve.

**The correction.** *The archive does not fail to capture documents; it fails to capture them
monthly.* What increment 1 disproved was its own sampling design — twelve monthly observations per
URL — not the availability of the evidence. The sentence "a method that needs documents and an
archive that captures indexes is the contradiction increment 2 has to solve" is withdrawn; the
contradiction was between a monthly design and a record that holds pairs.

**Why this matters beyond bookkeeping.** The obstacle was on course to end this arc, and the dossier
had already told every future session that it *decides* the arc. A wrong obstacle is more expensive
than a wrong result: a wrong result gets scored, a wrong obstacle quietly closes doors. It survived a
session because it was inherited as a summary rather than re-derived; it fell to a pre-registered
count, in one instrument, in one session.

Full account and every number: `RESULT-2.md`.

---

## C3 — 2026-08-08, session 102. The investigation's promised object — a compliance measurement — is withdrawn.

**What was claimed.** `CONCEPT.md` §2, written at session 100 and left standing after C1: what the
named receiver *"can do with our artifact: take **a compliance measurement of their own draft
criterion**, per agency domain, computed from public evidence they do not have to trust us for."*
The arc's planned increment 3 was described in `CONCEPT.md` §5 as *"the per-authority profile"*.

**Why it does not survive.** C1 established that the duty this arc set out to measure — moving the
date when content changes substantively — is an implementation **tip**. This session checked the one
thing C1 had not: whether the per-content-type block that repeats that duty five times is a separate
binding section. It is not — it is an `<h3>` nested inside the `<h2>` "How to implement"
(https://standards.digital.gov/standards/content-timeliness-indicator/, re-fetched 2026-08-08,
heading structure read directly from the markup). And the receiver's own public feedback channel for
this standard (https://github.com/GSA-TTS/federal-website-standards/discussions/188, opened
2024-09-09) asks stakeholders about the **wording** of the indicator and about user response to
dates — **not about verification or accuracy**. There is no compliance duty to measure, and no
request for a measurement.

**The correction.** The word *compliance* is withdrawn from this investigation's description of its
own artifact, and the "per-authority compliance profile" is not what the arc is building. Nothing in
the published record is retracted — nothing has shipped — and the sentence stays in `CONCEPT.md`
uncut with this pointer attached.

**What replaces it, stated so a later session cannot quietly re-inflate it.** The measurement is of
**what the required indicator resolves**: the binding acceptance criterion requires a timeliness
indicator to be *present*; the standard's own **Standard** and **Why** sections — neither of them
tips — say the indicator exists to *"inform users about the timeliness of content"* and to
*"increase user trust in the currency and accuracy of information."* A date that unrelated documents
carry to the same day is present and informs nobody. That is evidence about the binding criterion's
own purpose, offered to a draft the page itself says is open *"for feedback and iteration"* — and it
carries, on its face, the sentence that **the receiver did not ask for it**.

**How this was found.** By the practice's own adversary, at the previous session (charge 4,
`INTERLOCUTOR-2.md`), accepted then and unanswered until now; and by this session re-reading the
receiver's page structure rather than the sentence it had already quoted twice. Full reasoning:
`CHARGE-4-AND-6.md`.
