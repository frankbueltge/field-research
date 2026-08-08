# PROBES — two unregistered findings from session 101, 2026-08-08

**These are not part of `PREREGISTRATION-2.md` and are not scored against it.** They were run
during the census because both cost one fetch per page on hosts the census does not touch, and both
bear on the decision the census forces. They are kept in their own file so that nothing unregistered
can be mistaken for a scored prediction. Each is a **live single observation** — a photograph of
today, not a history — and neither is a compliance judgment about anyone.

---

## Probe A — the three signals on the receiver's own site

*Instrument: `probe_receiver_site.py`. Data: `receiver-site-probe.json`. All 16 URLs in
`https://standards.digital.gov/sitemap.xml`, each fetched once, 2026-08-08T03:50Z. The V extractor
and the HTTP-date parser are reused **unmodified** from `drafts/2026-08-06-as-of-today/collect_signals.py`,
with all of that instrument's known limits.*

The receiver publishes the draft standard whose acceptance criterion reads *"Update the date if the
content changes substantively"* (https://standards.digital.gov/standards/content-timeliness-indicator/,
status **Draft**). The smallest fair question about it: on the standard-setter's own pages, what do
the three signals say?

**All three signals are present on all 16 pages** — S (sitemap `<lastmod>`) on 16/16, H (HTTP
`Last-Modified`) on 16/16, V (a date printed for a human, here in a machine-readable `<time>`
element) on 10/16. That is already unusual: increment 1's corpus had authorities with no H at all
and authorities with no V at all.

**S and V agree exactly on all nine standard pages.** Where the site states a date to a reader, its
sitemap states the same date. This is the coherent case, and it is worth saying plainly because the
next paragraph is not.

**H is a deploy artifact, and it contradicts the other two by months.** Sixteen pages carry only
**six distinct `Last-Modified` values**, and pages share them *to the second*: five pages at
`2025-03-27T15:40:04`, five at `2025-02-20T19:24:33`, three at `2025-09-11T17:26:48`. Against each
page's own stated date, H runs **17 to 641 days later**:

| page | S = V (stated) | H (`Last-Modified`) | H − V |
|---|---|---|---|
| `/standards/content-timeliness-indicator/` | 2024-10-31 | 2025-03-27T15:40:04 | **+147 d** |
| `/standards/contact-page/` | 2024-10-28 | 2026-07-31T20:15:40 | **+641 d** |
| `/standards/banner/` (and 2 more) | 2024-09-26 | 2025-09-11T17:26:48 | +350 d |
| `/standards/external-link/` | 2024-10-11 | 2025-03-27T15:40:04 | +167 d |
| `/standards/site-search/` | 2024-11-05 | 2025-03-27T15:40:04 | +142 d |
| `/standards/language-selector/` | 2024-11-08 | 2025-03-27T15:40:04 | +139 d |
| `/standards/page-level-feedback/` | 2025-03-10 | 2025-03-27T15:40:04 | +17 d |
| `/standards/` (index) | 2024-09-26 (see below) | 2025-03-10T15:19:48 | +165 d |

**What this is and is not.** It is not evidence that any page changed on any of these dates, and it
is not a breach of the draft standard — the standard's duty is about the date shown to the audience,
which is exactly the signal that looks coherent here. What it is: **on the standard-setter's own
site, the one signal a machine gets for free is not a content date at all.** A crawler, a citation
tool or a monitoring service consuming H would conclude that nine standards last changed in February
or March 2025; the site itself says several of them last changed in 2024 and one in March 2025. Seven
site-chrome pages (`/`, `/about/`, `/contact/`, `/get-involved/`, `/search/`, `/404.html`,
`/standards/`) carry S = `2026-07-31` uniformly — a build date, not a content date, in the other
direction.

**And one point against our own instrument, recorded because it is the honest half.** The index page
`/standards/` returns V = 2024-09-26, which is the date of the *first standard listed on it*, not a
statement about the index. That is increment 1's D3 failure mode reproducing on a page we chose for
a different reason, and it is a second reason the printed-date extractor may not be pointed at index
pages.

**Why the receiver can use this.** It is one command's worth of evidence that a compliance
measurement of their own criterion cannot be built on `Last-Modified`, on their own site, today.

---

## Probe B — a route that does not go through any archive

*Instrument: `probe_publisher_history.py`. Data: `publisher-history-probe.json`. The **same 80 GOV.UK
documents** the census sampled — recomputed from `frames.json` with the pre-registration's seed and
rule, so no second draw was made. One content-API call each, 2026-08-08.*

The census exists because the archive may not see document pages often enough to compare a page
against itself. That is a limit of one route, and it is worth knowing whether it is a limit of the
question. One authority in the sample publishes its change history itself:

- **80 of 80 sampled documents returned a machine-readable record**, with **no errors**.
- **80 of 80 carry a `public_updated_at` timestamp**, and **80 of 80 carry a non-empty
  `details.change_history`** — a list of publisher-authored notes, each with its own timestamp.
- **1,113 declared change events** across the 80 documents; **median 6.5** per document, **maximum
  186**.

Each note is written by the publisher and says what changed — e.g. for the UK sanctions list,
*"Added 13 new designations and 6 new specifications under the Russia sanctions regime."*
(`public_timestamp` 2026-08-06T07:59:43Z, fetched 2026-08-08).

**What this means for the investigation, stated carefully.** It does **not** rescue the archive
route: a publisher's own history is the publisher's account of itself, exactly the thing an audit
would normally want an independent record for, and it exists for one authority in this sample and
cannot be assumed for others. What it does is open a different question, on ground the receiver's
standard actually names. The draft criterion turns on the word **"substantively"** and defines it as
*"a change that impacts the information in a way that is relevant to your audience"* — and here are
1,113 changes that a publisher considered worth writing a note about, on 80 documents, with dates.
That is a corpus for measuring **what publishers themselves treat as date-worthy**, which is the
question the standard leaves undefined.

**It is a candidate for increment 3, not a decision.** It is recorded here so that the gate's third
session has it, and so that if the census kills the per-authority archive profile, the arc is not
choosing between one route and nothing.
