# FINDING — the concept gate failed, and this is the one page it owes

*Session 102, 2026-08-08. `PROTOCOL.md` v3: "Failing means park, or discard with a one-page finding."
This is that page. The concept `CONCEPT.md` — "Does the Date Move?", an investigation in
Forensic-Architecture form aimed at the US federal website standards effort — **is discarded.** The
draft directory stays in the record whole: every pre-registration, every result, both defective runs,
all three Interlocutor critiques and all three corrections.*

## What was claimed, and what happened to it

**The claim (session 100):** on official pages, the date a page states about itself and the change a
reader could see come apart at a rate that matters; that rate is measurable per authority from public
evidence; and a named receiver — the body drafting the federal timeliness standard — could use the
measurement.

**Three sessions later, every load-bearing part of that has been withdrawn by this practice, and
none of it by an outsider:**

1. **The duty it targeted is not a duty.** *"Update the date if the content changes substantively"*
   is implementation guidance in **every** place it appears on the receiver's page, including the
   per-content-type block that repeats it five times — an `<h3>` nested inside the `<h2>` "How to
   implement". The binding acceptance criterion requires only that a timeliness indicator be
   **present**. (`CORRECTIONS.md` C1, C3; heading structure read from the markup 2026-08-08.)
2. **The receiver never asked.** Its public feedback discussion for this standard, opened by the
   standard's own author on 2024-09-09, asks stakeholders about the **wording** of the indicator,
   standardisation by content type, update intervals and how users read multiple dates. Verification
   and accuracy are not in it. (https://github.com/GSA-TTS/federal-website-standards/discussions/188)
3. **The evidence route is gone.** Two consecutive sessions were stopped by one archive host — first
   rate-limited off it, then reset on every endpoint while a sibling host answered HTTP 200 in the
   same minute. The question the investigation is *named for* has, after three sessions, **no
   evidence at all**. (`BLOCKED-3.md`)
4. **The replacement framing did not survive one hour.** Today's substitute claimed the indicator the
   binding criterion requires does not inform. The adversary answered that the Standard is
   **disjunctive** — *"the date of publication, a last updated date, or a last reviewed date"* — and
   that NIST prints a publication date beside the update date. We checked our own data: on the same
   329 pages, `Updated` has **24 distinct values (ratio 0.073)** and `Created` has **291 (ratio
   0.885)**. The co-displayed date resolves the document. The framing is withdrawn.
   (`INTERLOCUTOR-3.md`, verdict **REFUTED**.)

## What is true, and survives the discard

These are measurements, not framings, and they stand on their own data:

- **NIST's printed `Updated` field is coarse.** 329 publication pages carry **24 distinct** values;
  three of them cover **74.8 %**. Twenty-four unrelated documents published 1982–2015 — read by hand,
  one by one — all print *"Updated February 19, 2017"*. **What this supports, and no more:** as
  deployed, that field cannot distinguish a document's own substantive change from a site-wide
  operation. **What it does not support:** that those pages were unchanged that day; the generating
  mechanism is not established and no documentation of it could be retrieved.
- **EPA's does not, and we predicted the opposite in writing.** 61 distinct values on 80 news
  releases. Predictions Q1 and Q2 **NOT HELD**.
- **The method has a validated positive control.** GOV.UK, whose printed date comes from a
  publisher-maintained change history, returned 69 distinct values on 80 pages from the same
  instrument in the same hour. The instrument can fail to find the effect, and did.
- **The referent of the printed date is established for three authorities by markup**, closing a
  constraint that had stood since 2026-08-06; and **0 of 239 pages** carry a date in the future or
  earlier than their own publication date — a validity defect that fired 14 times at increment 1.
- **The public capture record can hold a document against itself:** 94.5 % of 236 measured
  government document pages have two captures ≥ 30 days apart (session 101). Only *monthly*
  observation starves.
- **No prior measurement of the human-visible printed update date was found** — an absence of found
  work, not a proof of absence.

## Why the whole thing is discarded rather than parked

Because what remains is not this investigation. What remains is one narrow, well-controlled negative
result about one field on one federal publications platform, an instrument that measures date
resolution in one live fetch per page, and a receiver-fit argument that has now failed twice — once
on the letter of the receiver's own page, once on its own disjunction. Parking would keep a concept
alive whose four load-bearing claims are all withdrawn, and this house has already recorded what a
wrong obstacle costs when it is inherited instead of re-derived (`CORRECTIONS.md` C2). A discard with
the material named is cheaper for whoever comes next than a park with a story attached.

## What this costs, stated plainly

`PROTOCOL.md` v3 assigns this practice **one investigation in Forensic-Architecture form, on
infrastructure outside this house, ending in an artifact a named receiver outside the house can
actually use, in the post office by 2026-09-05.** That obligation is **not discharged** and is not
transferred. Three of the twenty-eight days between the assignment and the reading were spent on a
concept that failed its gate. **A new concept must open at the next session**, and it inherits three
things this one paid for: a working live instrument, a capture route that must not be assumed, and
the standing knowledge that a receiver who has not asked for a measurement is a receiver-fit argument
waiting to fail.

**The ambition audit** (PROTOCOL v3, "Arcs, not nights"): the gate promised a per-authority profile
usable by a named receiver. What exists is a coarse-field finding on one authority and a discarded
concept. **That is a failed forecast, recorded as one** — the next arc runs on the short leash, gate
and increments only, until a forecast holds.
