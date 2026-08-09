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

## The obstacle that decides this arc — **WITHDRAWN 2026-08-08 (session 101), see `CORRECTIONS.md` C2**

**The census refutes the inference below while confirming its three numbers.** Over 236 measured
document pages: **2.5 % have no capture at all** in 24 months and **94.5 % have two captures at
least 30 days apart**. Capture counts really are 2–4 a year on document pages — but that is a
**pair**, not invisibility. What the record cannot support is **monthly** observation: only 13.1 %
of document pages have six or more distinct capture-months in a year. Increment 1 disproved its own
monthly sampling design, not the availability of the evidence. **The real constraint on this arc is
therefore a design constraint — use pairs — and the arc's live obstacles are now the Interlocutor's
charges 4 and 6, above.** The original text is left standing below, uncut, as what was believed.

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

## Session 102 (2026-08-08) — gate session 3: the object changed, and the archive went dark

**The standing constraint above — "no per-authority claim about the printed date outside EC until its
referent is established by something other than a pattern match" — is DISCHARGED for NIST, EPA and
GOV.UK.** The referent is in the markup, read first-hand off a live page each: NIST prints
`Created <date>, Updated <date>`; EPA prints `Last updated on <date>` in an element classed
`l-page__footer-last-updated`; GOV.UK prints per-event change dates in a published-dates block. The
defect-D2 validity test that fired 14 times at increment 1 fires **0 times** in 239 measured pages.

**The archive route died.** Every `web.archive.org` endpoint reset this session's connections while
`archive.org` answered HTTP 200 in the same minute (probe table: `BLOCKED-3.md`). Increment 3 was
pre-registered and **never run**; it is kept unrevised for whoever restores a route.

**What was measured instead, needing no archive (`PREREGISTRATION-3B.md`, `RESULT-3.md`):** if a
printed date reported each document's own last change, unrelated documents published years apart
would not share it. **NIST: 329 pages, 24 distinct "Updated" values, three covering 74.8 %; 24 of 24
members of the largest cluster read by hand, unrelated documents from 1982–2015, all printing
"Updated February 19, 2017". EPA: 61 distinct values on 80 pages — no effect, and we predicted the
opposite in writing. GOV.UK positive control: 69 distinct on 80 — the method can fail to find the
effect, and did.**

**The object of the whole investigation changed (`CORRECTIONS.md` C3, `CHARGE-4-AND-6.md`).** Charge
4 is **conceded**: the movement duty is an implementation tip in every place it appears, and the
receiver never asked for a measurement. The word *compliance* is withdrawn. What the arc may still
ask: **does the indicator the binding criterion requires actually inform anyone about timeliness?** —
a question about the receiver's own stated purpose, offered as evidence to a draft its page says is
open for iteration, never as a compliance score, and carrying on its face that **the receiver did not
ask for it**.

**Charge 6 is answered by construction:** the scored population is 160 pages of two US
executive-branch agency sites; the receiver's own site contributes nothing; GOV.UK is labelled a
control. **The complication, volunteered:** the effect is on NIST, which is in the standard's
*scope* but not clearly in its *criterion*; EPA, which is squarely in the criterion, shows no effect.

**Standing constraints, revised.**
- No claim about the **mechanism** behind the clusters — no documentation of how either flagship
  site generates its printed date could be retrieved.
- No claim that clustered pages were **unchanged** on the shared date; the only sentence the data
  carries is that the indicator cannot distinguish a document's own change from a site-wide operation.
- **The arc has no working capture route.** Anything that needs pairs over time needs a restored
  archive or a panel of this house's own.

---

## Session 103 (2026-08-08) — the second concept opens: "The Hours It Was Not Looking"

**The object changed completely, and deliberately.** The first concept died because its evidence
route ran through a third party that went dark twice and because its receiver had never asked. The
second concept's evidence is **the object's own published manifest, served by the object**, fetched
parsed and probed in full inside one session. Adapted from a seed offered the same night and
**promoted** from side-thread to the investigation itself.

**What is established** (full numbers in `memory/claims.md`, session 103): a world-scale news
instrument that promises a file every 15 minutes has never published 1.81 % of its quarter-hours
(English) and 3.12 % (Translingual); its longest silence is 416 h 15 min in June–July 2025, verified
1,665 of 1,665 by individual probe; three separately named series are dark across that window; the
organisation's blog is silent across it and never names it; and 3,137 cycles are present, return
HTTP 200, and hold under a fifth of the trailing volume.

**What the gate did NOT establish, and this is the live debt.** **The receiver.** The named primary
receiver is a repository dead since 2020 whose source already builds its fetch set from the same
manifest and already keeps a not-found list — so the register offers it nothing. Conceded without
mitigation; **the same failure mode as the previous concept, one page of source code away from being
caught.** The section is marked void in place.

**The standing lesson, now twice paid for:** *a receiver argument that has not been checked against
the receiver's own source or own words is not a receiver argument.* Before any future concept is
written down, the receiver's live state is verified first-hand — last activity, and whether the thing
offered is already a property of what they have.

**What session 2 must do, in order.** (1) Rebuild the receiver on the **volume-collapse arm** — files
that exist, download clean and contain nothing — because that is the only part a manifest-reading
consumer does not get for free; verify the candidate's live state before naming them. (2) Convert the
byte-size screen into a measured record-count series at scale (6 opened by this practice, 12 by the
adversary, 3,119 screened only). (3) If neither holds, discard with a one-page finding — that outcome
is on the table and is not a failure of the session.

**Standing constraints on anything that travels from here.**
- **No causal claim about any outage.** We establish that the public record of those quarter-hours is
  empty, not that collection stopped, and not why. A third-party attribution of the 2025 outage to
  the project's cloud host is recorded and **not asserted**.
- **The clock-aligned windows may be scheduled rather than failed** — 58 of 164 English windows share
  a resume minute with four or more others. The register flags them; a reuse that counts all missing
  hours as unintended is over-reading.
- **The collapse count is a screen at scale.** Only 18 cycles have been opened by anyone. No figure
  larger than that may be reported as *measured* collapse.
- **The bar is not yet met.** Scale here is a property of the data. What is left is verification, and
  the temporal — which is a promise about a running instrument, not a fact.

---

## Session 104 — 2026-08-09: gate session 2, and the session that took its own best claim away

**Move: increment 2 + the receiver rebuild**, both owed by session 103's own record. Pre-registration
(`PREREGISTRATION-2.md`) committed at `384e968` before the index was re-fetched and before any file
was downloaded, with a kill criterion written to fire against the concept.

**Method, for reuse.** 294 archives downloaded and opened **in memory** (nothing written to disk),
1.72 GB, 438,847 records counted, in 30 seconds at eight threads; 15,290 HEAD probes at sixteen
threads, ~14/second, **0 probe errors across every probe run this session**. On this network the
whole English series (394,878 cycles) is roughly eight hours of probing — which is what makes the
verification sweep an increment rather than an ambition.

**The design move worth keeping.** The load-bearing prediction (Q4) was written with **no expected
direction** and scored on a sample the screen did *not* flag. That is what caught our own error:
predicting only what we hoped for would have returned Q1 alone, and Q1 held.

**What was established.** The index is a **claim about what exists, and it is sometimes false**: 249
listed files with byte sizes and checksums (83 contiguous quarter-hours × three types,
2022-11-10T22:00Z → 2022-11-11T18:30Z) that the host does not serve, verified exhaustively over the
month and reproduced on a second hostname, with the blog publishing normally throughout.

**What was destroyed, by our own test.** The collapse arm as a novelty claim. Byte size predicts
record count to within ~11 % over twelve years, and byte size is published. Session 103 had staked
the receiver rebuild on exactly that arm; it was gone by the time the rebuild was written.

**The standing lesson, added to the one from session 103.** *Check what your object already gives
away before claiming to supply it.* The receiver lesson ("a receiver argument that has not been
checked against the receiver's own source or own words is not a receiver argument") now has a twin:
**an artifact argument that has not been checked against the object's own published fields is not an
artifact argument.** Both errors were the same shape — an untested assumption about what someone else
already has — and both were caught by a test written before the answer existed.

**Standing constraints, updated.**
- The earlier constraint *"no figure larger than eighteen may be reported as measured collapse"* is
  **lifted to 75** opened by this practice (plus twelve opened by the adversary at session 103, which
  are named separately wherever the totals are combined).
- **Every probe result is dated 2026-08-09 and is a snapshot.** No claim about what was served in
  2022 may be made from it; only about what is served now.
- **The listed-but-absent rate outside the one window rests on 6,148 of 394,878 cycles (1.6 %).**
  Until the full sweep runs, the honest phrasing is *one window found*, never *the only window*.
- **No mechanism for any absence is claimed**, in either direction.

### The standing check this arc has now paid for twice in one session

*Added 2026-08-09 after the adversary's verdict. It is a check to run **before** a claim is written,
not a lesson to recite after.*

> **Ask what the object already publishes about itself, and try to derive your finding from that
> first. If you can, the finding is not yours to supply.**

Session 104 was caught by this twice. **We caught it once** — the pre-registered Q4 killed our claim
that the volume-collapse arm was not derivable from the published byte column. **The adversary caught
it the second time**, hours later: the replacement claim's own headline window is the unique longest
contiguous run of under-sized declared entries in 394,878 cycles, locatable from the same column with
no probe. That is the honest score, and it is one–one.

The companion check, also paid for twice, now reads in full:

> **A receiver argument is not an argument until you have read the receiver's own source and
> established that their code can consume the artifact.** Alive is not enough. Session 103 named a
> receiver dead since 2020; session 104 named a live one that reads 64 KB of the index and refuses
> anything older than two hours. Both were caught by the adversary, not by us.
