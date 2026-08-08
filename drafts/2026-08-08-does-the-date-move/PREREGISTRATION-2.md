# PRE-REGISTRATION — increment 2: the capture-density census over document pages

*Written and committed at session 101, 2026-08-08, **before the census instrument existed and before
any census number was computed**. Same discipline as increment 1. Anything this file gets wrong stays
wrong in the record; `RESULT-2.md` scores it as written.*

## Why this increment and not another

`RESULT.md` (increment 1) and `memory/dossiers/the-first-investigation.md` name one thing increment 2
owes before anything else. Quoting the dossier: *"The archive captures indexes, not documents. Index
pages: 42–5,000 captures in twelve months. Actual document pages in the same population: 2, 3, 2.
'Last updated' is a promise about a document. Increment 2 therefore owes, before anything else, a
capture-density census over document pages."*

Three data points are an anecdote. This increment turns them into a measurement, because the answer
decides the arc: if document pages are not observable at pair density in the public capture record,
the per-authority profile the receiver was promised cannot be built from that record, and the honest
artifact is a finding about what the public record cannot support.

## 1. What is being measured

For each sampled **document page**: how often the public web capture record holds a capture of it,
and whether those captures are spread widely enough in time to compare the page against itself.

**Nothing about content is fetched or compared in this increment.** No payloads, no dates, no text.
The census is an index query only. This is deliberate: a coverage question must be answerable before
a fidelity question, and it keeps the increment cheap enough to run in one session.

## 2. Frame — what counts as a document page, fixed in advance

A **document page** is an individual dated item of content published by the authority, as opposed to
a landing, listing or index page. It is operationalised per authority by a **URL path prefix that the
authority itself uses exclusively for individual items**, chosen from that authority's own public
machine-readable listing and stated here before sampling:

| Authority | Frame source (public, re-fetchable) | Document rule |
|---|---|---|
| **NIST** (`www.nist.gov`) — US federal, inside the receiver's stated scope, and one of increment 1's authorities | `https://www.nist.gov/sitemap.xml` (paged) | path begins `/publications/` and has a slug after it |
| **EPA** (`www.epa.gov`) — US federal | `https://www.epa.gov/sitemap.xml` (paged) | path begins `/newsreleases/` and has a slug after it |
| **GOV.UK** (`www.gov.uk`) — non-US comparator, and one of increment 1's authorities | `https://www.gov.uk/api/search.json` with `filter_content_store_document_type=guidance` | the API's own `link` field, restricted to paths beginning `/government/publications/` |
| **standards.digital.gov** — **the receiver's own site**, taken whole, not sampled | `https://standards.digital.gov/sitemap.xml` | every URL in the sitemap |

**A fourth US agency (`www.energy.gov`) is admitted only if** its sitemap yields ≥ 200 URLs under a
single individual-item prefix, decided by the frame builder before sampling and recorded either way.

**One authority is excluded before sampling, and the reason is recorded now:** the EC's
`digital-strategy.ec.europa.eu` sitemap enumerates only `/policies/`, `/factpages/`, `/faqs/` and
`/activities/` — no news or library items — so no document frame can be built from it by this rule.
EC therefore contributes nothing to this census, and any later per-authority statement about EC
documents must build its frame another way. Recording this is not a caveat; it is a limit of the
census, and increment 1's clean positive (P2) was an EC result.

## 3. Sample — deterministic and reproducible

Per sampled authority: the frame list is de-duplicated, sorted lexicographically (so it does not
depend on fetch order), and a sample of **80** URLs is drawn with Python's `random.Random(20260808)`.
Seed and procedure are fixed here. If a frame yields fewer than 80, all of it is taken. The receiver's
own site is taken whole.

## 4. The measurement, per URL

One query to the public capture index (CDX), `output=json`, fields `timestamp,statuscode,digest`,
`filter=statuscode:200`, `limit=1000`, over **2024-08-01 → 2026-07-31** (24 months). Derived:

- `n24` — captures in the 24-month window; `n12` — captures in **2025-08-01 → 2026-07-31**, the same
  12-month window increment 1 used, so the numbers are comparable to it.
- `months24`, `months12` — count of distinct calendar months holding ≥ 1 capture.
- `pairable` — TRUE if two captures exist in the 24-month window at least **30 days** apart.
- `first`, `last`, `truncated` (rows == limit), `error` (query failed after 3 tries).

**Denominator rule:** URLs whose query errors are excluded from percentages and reported as a
separate count. **URLs with zero captures are kept in every denominator** — zero is the finding, not
missing data.

## 5. Predictions — scored exactly as written

- **P5 (density).** Pooled over all sampled document pages, the **median `n12` ≤ 4**.
- **P6 (monthly observability).** **Fewer than 25 %** of sampled document pages have `months12 ≥ 6`.
- **P7 (arc viability).** **At least one** sampled authority yields **≥ 30** document pages that are
  `pairable`.
- **P8 (documents versus indexes).** The **90th percentile of `n12`** over sampled document pages is
  **below 42** — the smallest 12-month capture count increment 1 observed on any index page.
- **P9 (the falsifier, declared before the run).** If **≥ 50 %** of pooled document pages have
  `months12 ≥ 6`, then D4 is a property of increment 1's three-page anecdote and **not** of the public
  record; this increment must say so plainly, the obstacle is withdrawn, and the arc proceeds to
  fidelity measurement instead of to a coverage finding.
- **P10 (the receiver's own site).** **Fewer than 50 %** of `standards.digital.gov` pages are
  `pairable` — i.e. the body that writes the timeliness duty cannot, for most of its own pages, have
  that duty checked against the public record by this method.

## 6. What the census cannot say, stated before it runs

Absence of captures is **absence of observation**, never evidence that a page did not change. A
capture record is a property of crawler behaviour — submission, popularity, robots directives, the
authority's own sitemap advertising — and not a property of the page's editorial history. Every
statement this increment makes is of the form *"this method, on this record, can or cannot see X"*.

The census also cannot say whether the sampled prefixes are representative of an authority's
documents in general; it can only say what it sampled. And a single capture index is one archive
among possible archives: this measures **the public capture record most cited by researchers**, not
"the archive of the web".

## 7. Decision rule, fixed in advance

- **P7 holds and P9 does not fire** → the arc continues as a per-authority profile, restricted to the
  authorities that cleared P7, and increment 3 measures fidelity on exactly those pairs.
- **P7 fails** → the per-authority profile is not buildable from this record. The concept is rewritten
  at the gate's third and last session as a coverage finding — *what the public record cannot support*
  — or discarded with a one-page finding. No third option is left open here on purpose.
- **P9 fires** → the obstacle is withdrawn in writing and increment 1's D4 is corrected in the record
  as an artefact of its sample.
