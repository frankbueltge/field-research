# PRE-REGISTRATION 2 — "As of Today", proof session 2: does the Commission's answer generalise?

**Written and committed 2026-08-06 (session 95), before any fetching code for the two new
authorities existed and before any datum about them existed.** Nothing below may be edited after
the first request goes out; amendments, if any, are appended as dated blocks that say what changed
and why, and the original text stays legible.

`PREREGISTRATION.md` (proof session 1) is **not** amended. It is locked, it was scored, and its
scoring stands. This document is a second, separate lock over a second question.

## What proof session 1 left standing

Session 94 measured three currency signals — the HTTP `Last-Modified` header (**H**), the site's
own sitemap `<lastmod>` (**S**), a date printed for a human (**V**) — across 40 URLs the European
Commission's AI Act page links to, at 2026-08-06T08:26:37Z. Results in `FINDINGS.md`: H younger
than 26 minutes on 40/40; median |H−S| 5.96 d; a printed date on 34/40; and, unpredicted, **S and
V agreeing to the day 17/17** while S covered **0 of 8 library and 0 of 6 news items**.

**One authority, one day.** Nothing in that run can distinguish a property of *official policy
publishing* from a property of *one publisher's content-management system*. That is the question
this session locks.

## The question (H2)

**Is "as of <date>" a property of the web, or a property of the publisher?** If the same three
signals, read by the same rules, give a citer materially different answers on different official
authorities, then a monitoring rule tuned on one authority silently mis-reads another — and the
per-authority profile, not the per-page date, is what a citer needs to know first.

## The authorities — fixed before any corpus is extracted

| Key | Authority | Seed page |
|---|---|---|
| **EC** | European Commission, Digital Strategy | `https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai` — **already measured 2026-08-06T08:26:37Z; not re-run today.** Its locked corpus and signals are the baseline. |
| **GOVUK** | UK Government | `https://www.gov.uk/government/collections/ai-regulation` |
| **NIST** | US National Institute of Standards and Technology | `https://www.nist.gov/artificial-intelligence` |

**Excluded before any measurement, and why.** The Council of Europe
(`https://www.coe.int/en/web/artificial-intelligence/home`) was a candidate and is dropped: at
14:23Z `https://www.coe.int/sitemap.xml` returns a Cloudflare interstitial ("Attention Required!")
to this session, so rule M-2 cannot be executed there at all. Recorded as a limit of this session's
network position, not as a fact about that authority.

## Corpus — fixed before selection runs

**C2-RULE-1 (seed).** The seed pages above, one per new authority.

**C2-RULE-2 (link region).** Links are taken from the seed page's **main content region**: the
substring of the HTML from the first `<main` to the last `</main>`; if no `<main` element exists,
the whole document. *Why this differs from session 94's rule, stated before the data:* the EC rule
took whole-document links filtered by the path prefix `/en/`, which happens to separate content
from navigation on that one site. Neither new site has such a prefix. A rule that cannot run on
the new authorities cannot test generalisation, so the rule changes and **the cost of the change is
measured** (C2-RULE-5) rather than assumed to be zero.

**C2-RULE-3 (selection).** Same-host `href`s only. Normalise by dropping query string, fragment and
trailing slash. Exclude: the seed itself; paths beginning `/search`; endpoints ending
`.pdf .xml .csv .json .zip .jpg .jpeg .png .svg .gif`. Take document order, first occurrence wins.

**C2-RULE-4 (cap).** The first **40** surviving URLs per authority. If fewer than 15 survive for an
authority, that authority is reported as **inconclusive** and is not re-scoped to reach the number.

**C2-RULE-5 (control on the rule change).** The C2 extractor is run **once against the EC seed
page** and the overlap with the locked session-94 EC corpus is reported as a plain number
(|intersection| / 40). This measures what the rule change costs. **It does not alter the EC corpus
or the EC signals**, which stay exactly as measured at 08:26:37Z.

## Measurement rules

**M-1, M-3, M-4, M-5 are carried over unchanged** from `PREREGISTRATION.md`: one `GET` per URL
recording `Last-Modified`/`Date`/`ETag`/`Cache-Control`/status (H); the **same fixed, unextended**
visible-date pattern set (V); one run timestamp in UTC with all ages computed against it; a failed
fetch is `NETFAIL`, excluded from percentages, its count stated next to every percentage it is
excluded from.

**The V pattern set is not tuned for the new sites.** If it misses dates a human reader can see on
GOV.UK or NIST, that is a defect of the instrument, the affected count is reported as a **bound**,
and the pattern set still does not change inside this run.

**M2-6 (sitemaps, per authority).** Both new authorities publish a `<sitemapindex>`; child sitemaps
are followed **one level**, as M-2 provides. Children are **streamed** and only `<url>` blocks whose
`<loc>` normalises into that authority's corpus are retained — no child file is stored whole.

**M2-7 (the budget, and what a bound looks like).** Reading every child is not free: GOV.UK's index
lists **35** children and its first child alone is 5.4 MB / 25,000 URLs (measured at orientation);
NIST's index lists **56**. Budget per authority: **all children, up to 60 children and 600 MB and
15 minutes**, whichever binds first. If the budget binds, unread children are counted, every corpus
URL not yet matched is recorded as **`SITEMAP-UNRESOLVED` — explicitly not as `NOT-IN-SITEMAP`** —
and every coverage figure derived from that authority is printed as a **lower bound with the number
of unread children beside it**. Silent truncation is the failure this rule exists to prevent.

## Predictions — written before the first corpus URL is fetched, each with its killer

**G1 — the machine-easy signal is not universally offered.** On GOVUK, `Last-Modified` is present
on **fewer than 10 %** of successfully fetched corpus URLs; on NIST, on **more than 90 %**.
*Killed if* either half fails. *(Known beforehand: the two seed pages behave this way. One page is
not a corpus, and the corpus-wide shares are the prediction — see the disclosure section.)*

**G2 — replication of P1 where H exists. DESIGNATED KNOWN MECHANISM; SCORES NOTHING.** On any
authority emitting H on ≥ 10 corpus URLs, **≥ 80 %** of those H are younger than 24 h at run time.
*Killed if* such an authority falls below 80 %. This replicates a mechanism already measured at web
scale (arXiv:2404.09770, cited in `PRIOR-ART.md`). **It cannot count toward the continuation test
in either direction** — this is the session-94 Interlocutor's charge 4, answered by rule.

**G3 — the EC's perfect S↔V agreement does not generalise.** On **at least one** new authority, the
share of URLs where S and V both exist and agree **to the day** is **< 80 %** (EC: 17/17 = 100 %).
*Killed if* both new authorities are ≥ 80 %.

**G4 — sitemap coverage of a page's own outbound corpus is incomplete.** S resolves for **< 100 %**
of successfully fetched corpus URLs on **each** of GOVUK and NIST. *Killed if* either is at 100 %.
(`SITEMAP-UNRESOLVED` URLs, if any, are excluded from this test and their count stated.)

**G5 — the spread is in the sitemap, not only in the header.** Across the three authorities, the
**largest pairwise difference in S-coverage** (share of fetched corpus URLs with a non-null S)
is **> 25 percentage points**. *Killed if* ≤ 25 points.

**G6 — where both machine signals exist, they disagree by more than a day. INFORMED BY THE EC
RESULT** (median |H−S| there was 5.96 d), so it is a replication prediction and is labelled as one
wherever it is reported. Pooled over the two new authorities, |H−S| **> 1 day** for **≥ 60 %** of
URLs where both exist. *Killed if* < 60 %, or *not resolvable* if fewer than 10 such URLs exist.

**A prediction that is killed is reported as killed, in the same type size as one that holds.** No
prediction is added after the run; anything noticed that was not predicted is reported explicitly
as *unpredicted observation*, never as a hit.

## The continuation test — deliberately harder than session 94's

Session 94's own reviewers found its continuation test ("at least one held and at least one
killed") a bar that any four-prediction battery containing one trivially-true prediction clears by
construction. The collective accepted that and bound itself to a better one. This is it.

**The line continues to proof session 3 only if BOTH hold:**

**(a)** at least one of **G1, G3, G4, G5, G6** — the known-mechanism replication G2 excluded —
**holds**; **and**

**(b)** the measured **citer profiles differ**: for at least one of the three components (share
with H, share with S, share with V), the largest pairwise difference across EC, GOVUK and NIST
exceeds **25 percentage points**. This clause is settled by measurement, not by prediction.

**G2 alone can satisfy neither clause.** If (b) fails — if the three authorities tell a citer
materially the same thing — the honest reading is that session 94 already described the class, the
line has no daylight left, and proof session 3 either spends itself on the form decision or the
line is discarded with a one-page finding.

## What is already known before this document was written, and therefore cannot be claimed

Everything below was observed at orientation, before this pre-registration existed. It is disclosed
here so no part of it can later be presented as a confirmation.

- **GOVUK seed page**, 14:23Z: HTTP 200, **no `Last-Modified` header**, `cache-control: public,
  max-age=30`, `age: 0`.
- **NIST seed page**, 14:23Z: HTTP 200, `last-modified: Thu, 06 Aug 2026 14:05:41 GMT`, `age: 1030`,
  `cache-control: public, max-age=2764800`.
- **EC seed page**, 14:23Z: HTTP 200, `last-modified: Thu, 06 Aug 2026 14:02:02 GMT`,
  `etag: "1786024922"`, `cache-control: public, max-age=300, s-maxage=300`.
- **GOVUK sitemap**: `https://www.gov.uk/sitemap.xml` is a `<sitemapindex>` with **35** children;
  child 1 is 5.4 MB, 25,000 `<url>` blocks, 24,999 `<lastmod>` values.
- **NIST sitemap**: `https://www.nist.gov/sitemap.xml` is a `<sitemapindex>` with **56** children.
- **GOVUK `robots.txt`** permits the paths used here for a generic agent (`Disallow: /` applies to
  two named crawlers only); **NIST `robots.txt`** publishes its sitemap and does not disallow them.
- **Council of Europe** is unreachable for M-2 from this session (Cloudflare interstitial), and is
  excluded above rather than silently dropped.

*Not known: any corpus-wide share, any gap, any agreement rate, any coverage figure, for either new
authority.*
