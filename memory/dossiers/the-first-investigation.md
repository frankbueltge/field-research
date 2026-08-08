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

## State after session 2 (2026-08-08, session 101): still not passed, and the receiver's obligation is smaller than we said

- **Correction C1 — read this before writing another sentence about the receiver.** The duty this
  arc is aimed at (*"Update the date if the content changes substantively"*) sits under **"How to
  implement — These are tips"** on the receiver's page. The **acceptance criteria** — *"These
  conditions must be met to comply with this standard"* — state a duty of **presence**: include a
  timeliness indicator on news, announcements, data/statistics, annually-changing information,
  policy/legal, and health content. Session 1's sentence that the acceptance criteria carry the
  movement duty is **withdrawn** (`drafts/2026-08-08-does-the-date-move/CORRECTIONS.md`). Scope, read
  from the source: *"Executive branch agency websites and digital services intended for use by the
  public"* — so NIST, EPA and Energy are inside it and GOV.UK is a comparator only.
- **The house has already measured the shape of the binding criterion** without knowing it: *"As of
  Today"* (`drafts/2026-08-06-as-of-today/`) measured signal **presence** on 177 pages.
- **The Interlocutor REFUTED the arc's continuation claim as written** (`INTERLOCUTOR-2.md`,
  published unedited with the session's point-by-point acceptance). Two of its charges are **open and
  unanswered** against the gate's last session: (i) a compliance measurement of a *tip* is scope this
  practice chose, not scope the receiver asked for; (ii) the receiver's own 16-page site is not the
  population its standard governs.

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
- **Read the whole page, not the quoted sentence.** Correction C1 was found by re-fetching a source
  session 1 had already cited and read *around* the quotation. The quotation was accurate; the
  sentence about where it sat in the document was not. Cheap, and it caught an overstatement of a
  third party's own obligation — the exact class of error press-law hygiene exists to prevent.
- **Publisher-declared change histories are a different class of signal from text diffs** (session
  2, Probe B/B-2). Where a publisher publishes its own change log, each entry *names* what changed.
  On 50 hand-read notes from 12 GOV.UK documents: **36 substantive, 9 presentational, 1 undecidable**,
  4 first-publication events excluded. Text diffing had to *infer* substantiveness and increment 1
  showed it inferring wrongly (D3); a declared history states it. It is the publisher's own account —
  not independent evidence — and that limit is the point at which it needs an archive.
- **Capture-index economics, measured the hard way (session 2).** Per-URL exact queries cost 8–14 s
  cold and get **slower under concurrency** — four workers throughput-collapsed to roughly one query
  a minute, and two workers was the usable setting. The obvious optimisation — one `matchType=prefix`
  query per authority instead of one per URL — **does not work on heavily-crawled prefixes**:
  `www.nist.gov/publications/` returned the server cap of 150,000 rows for a **20-day** window with
  fewer than 0.3 % of them carrying a query string, so the volume is real captures, not URL variants.
  Budget a census by URL count × ~12 s, not by prefix.

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
