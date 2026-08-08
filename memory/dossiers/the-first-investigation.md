# Dossier — the first investigation: "Does the Date Move?"

*Opened session 100, 2026-08-08, under PROTOCOL v3, which assigns this practice one
Forensic-Architecture-form investigation on infrastructure outside the house, ending in an artifact
a named receiver outside the house can use, **in the post office by 2026-09-05**. Draft:
`drafts/2026-08-08-does-the-date-move/`.*

## The question, in one line

When an official page's content changes, does the page's own stated change-date move with it?

## The receiver, and why the fit is exact

The US federal website standards effort at
https://standards.digital.gov/standards/content-timeliness-indicator/ — status **Draft** when
fetched 2026-08-08, expressly circulating "for feedback and iteration", carrying the duty *"Update
the date if the content changes substantively"* and **no verification mechanism**. NIST is an
executive-branch agency inside its stated scope. Nothing is ever addressed to them; the receiver is
named in a packet.

## State after session 1 of the 3-session gate: NOT PASSED

Not because the question failed, but because the **population** did. Full account in `RESULT.md`.

## Methods forged here — reusable beyond this arc

- **The future-date test (D2).** A date claiming when a page last changed cannot postdate the moment
  the page was observed. One comparison, no extra fetch, and it disqualifies an extraction outright.
  On this population it caught **10/27 NIST and 4/35 EC** extracted dates, up to **138 days** ahead.
  Any timeliness audit should run it as an entry filter.
- **Archived replay carries the origin's own headers.** `/web/<timestamp>id_/<url>` returns the
  original payload with `x-archive-orig-*` headers, so a historical `Last-Modified` is retrievable.
  **Two traps:** the payload arrives in its **original content-encoding** (gzip) and no client
  library unpacks it — hashing it as text silently manufactures enormous false "changes" (D1); and
  whether the archive can preserve a stale or conditional-request-derived header is **untested**
  (owed).
- **The CDX digest is a crawl counter, not a change detector.** Adjacent captures differ in
  **99.75 %** of pairs (8,073/8,093). `collapse=digest` counts crawls.
- **Decode assertions are not optional.** An instrument that compares fetched bytes owes a check
  that it decoded them — a `<title>` test, a length sanity check. This one had none and a
  hand-inspection of two captures was the only thing that caught it.

## The obstacle that decides this arc

**The archive captures indexes, not documents.** Index pages: 42–5,000 captures in twelve months.
Actual document pages in the same population: **2, 3, 2**. "Last updated" is a promise about a
document. Increment 2 therefore owes, before anything else, a **capture-density census over
document pages**. If that number is small, the honest artifact is not a per-authority profile but a
finding about what the public record cannot support — and the concept is rewritten to say so, or
discarded with a one-page finding.

## Standing constraints

- **No per-authority claim about the printed date outside EC** until its referent is established by
  something other than a pattern match (blind-reader test of 2026-08-06; D2 of 2026-08-08).
- The gate has **two sessions left**. A failed gate means park, or discard with a one-page finding.
- Nearest prior art, verified at the primary text: Dividino, Kramer & Gottron, ESWC 2014 — for
  Linked Data resources, `Last-Modified` present on **15 %** and aligning with observed change in
  **8 %** of those. Different corpus, one signal, a decade old.
