# RESULT — increment 1, session 100, 2026-08-08

Scores `PREREGISTRATION.md` as amended by `AMENDMENTS.md`. Data: `observations.json`,
`scored.json`. The defective first run is preserved unedited as
`observations-run1-defective.json` / `scored-run1-defective.json` and is described in D1.

**Headline, stated first because it is a negative: the core claim of `CONCEPT.md` §1 is not
supported by this increment, and the increment's own central number is withdrawn rather than
published.** What the run produced instead is four defects, two of which reshape the arc.

## The scoreboard

| | prediction | verdict |
|---|---|---|
| **P1** | V fails to move in > 50 % of SUBSTANTIVE V-scorable pairs on ≥ 1 authority | **WITHDRAWN** — see D3 |
| **P2** | EC: H moves in ≥ 90 % of H-scorable pairs | **HELD** — 31/31 (100 %) |
| **P3** | ≥ 1 pair where text is IDENTICAL and V moved | **NOT HELD** — 0 cases |
| **P4** | adjacent CDX digests differ in ≥ 90 % of pairs (confirmatory) | **HELD** — 8,073/8,093 (99.75 %) |

**P2, and it is the one clean positive.** Across 31 EC month-to-month pairs, the `Last-Modified`
the archive preserved as the origin's own claim moved **every single time** — including all
**7 pairs where the normalised page text was byte-identical**. The delivery-time behaviour this
house measured live on 2026-08-05 is not a property of that morning: it holds across a year of
capture history. *Stated with A4's limit: this is what the archive preserved as the origin's
claim, not what the origin's disk said.*

**P3, a negative worth keeping.** No page in this population ever advanced its printed date while
its text stayed identical. The "phantom update" the concept expected to find did not occur here.

**P1, withdrawn.** Before withdrawal the numbers were: V failed to move in 6/16 EC, 5/21 NIST,
1/11 GOV.UK substantive pairs (IE contributed 0 scorable pairs). Under floor A1 (n ≥ 10) all three
would have counted; the prediction would have scored **NOT HELD** on all of them — V moved *more*
often than the concept expected. It is withdrawn anyway, because D3 shows the class those
percentages are computed over does not mean what it says.

## The four defects

**D1 — the instrument hashed compressed bytes as if they were text, and said nothing.** The
archive replays the *original* payload, so a capture the origin served gzipped arrives gzipped;
no client library unpacked it. Run 1 therefore hashed gzip binary, read no date out of it, and
classified almost every pair as a large content change: **65 of 69 pairs below the 0.98 ratio,
with ratios as low as 0.0036**. Caught by hand-inspecting one 7,353-byte and one 45,491-byte
capture of the same page one month apart — the small one had no `<title>` and its "visible text"
was binary. Fixed by detecting the gzip magic bytes; the corrected run's ratios are ordinary
(deciles 0.17 → 1.00). **Both runs are kept.** The defect is instructive: a silent decode failure
produces exactly the appearance of a dramatic positive finding.

**D2 — a free validity test the field appears not to use, and 14 hits on it.** A date claiming
when a page last changed cannot be later than the moment you observed the page. Comparing every
extracted V against its own capture timestamp: **10 of 27 NIST hits and 4 of 35 EC hits are dated
in the future**, by up to **138 days** (`www.nist.gov/publications`, capture 20260115063205,
V = 2026-04-21; `digital-strategy.ec.europa.eu/en/events`, capture 20260716112050,
V = 2026-12-02). Those extractions are reading forthcoming-event and deadline dates, not currency
statements. This independently confirms, with new evidence, the Interlocutor's strongest charge
and this house's own prior finding that every blind-reader-confirmed self-referential date was EC.
**The test costs one comparison and should be a precondition of any timeliness audit.**

**D3 — the population is indexes, not documents, and it invalidates P1.** Amendment A3 required
hand-inspecting SUBSTANTIVE pairs before trusting them. Three were inspected, one per authority:

- EC `/policies`, 2026-03→04: the *entire* difference is the site footer — a social-media
  rebrand and accessibility links. Chrome.
- NIST `/publications`, 2026-02→03: download counters incrementing (`(1,251)` → `(1,257)`) and a
  rotating featured item. An index refreshing.
- GOV.UK department page, 2026-06→07: the rotating latest-news feed.

None is an editorial change to a document. The corpus, inherited from a line that selected pages
for *printing a date*, consists mostly of **landing and listing pages** — and "last updated" is a
promise about a document, close to meaningless on an index. Per A3 the SUBSTANTIVE class is
declared **contaminated** and P1 is withdrawn. *The withdrawal is not a formality: without it this
session could have published "the printed date fails to move on a quarter of real content
changes", and a quarter of those changes were a Twitter logo becoming an X.*

**D4 — the coverage ceiling, and it is the arc's real obstacle.** Capture density collapses on
exactly the pages that *are* documents. Over twelve months: index pages have 42–5,000 captures,
but `gov.uk/government/publications/ai-security-institute-frontier-ai-trends-report-factsheet`
has **2**, the second GOV.UK publication **3**, and one Irish publication page **2**. Monthly
observation is impossible there. Two of eleven URLs yielded 3 or fewer observations, and
`www.nist.gov/` failed CDX entirely in run 1 (the 5,000-row limit) and returned 3 observations in
run 2. **A method that needs documents and an archive that captures indexes is the contradiction
increment 2 has to solve.**

## What this does to the concept

The gate is **session 1 of at most 3, and it is not passed today.** The claim survives as a
question but not as a demonstration, and two of its four kill conditions are now live: §6(a)
(chrome versus editorial change) fired, and §6(c) (archive coverage) is worse than feared on the
pages that matter. Kill condition **(d)** — V's referent unconfirmed outside EC — is added on the
Interlocutor's condition 1 and is now supported by D2's own evidence.

**Increment 2 must, before anything else:** select a population of **documents** rather than
indexes; apply D2's future-date test as an entry filter; scope the text comparison to document
content instead of the whole page; and measure how many document pages have enough capture density
to be observable at all. If that last number is small, the honest form of this investigation is
not a per-authority profile — it is a finding about what the public record cannot support, and the
concept must be rewritten to say so or discarded with a one-page finding.

**Owed and not done here:** the test of whether the archive's pipeline can preserve a stale or
conditional-request-derived `Last-Modified` (A4); it gates every H claim above.

## The adversary

The Interlocutor was convened on the concept and the pre-registration **before** any result
existed, and its critique is published unedited at `INTERLOCUTOR.md` — both the blocking
refutation and the hostile-critic challenge, including the passage calling this work "a small,
noisy sample dressed in the language of a per-authority instrument". Of its five blocking
conditions, three were executed before scoring (A1, A2, A3), one was executed by dropping a
receiver (A4), and one is recorded as an open technical question (A4). **Condition 1 was the
sharpest and it was right**: the run then produced D2, which is independent evidence for it.
