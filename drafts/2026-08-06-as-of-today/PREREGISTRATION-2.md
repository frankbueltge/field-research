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

---

## Amendment 1 — 2026-08-06, at the corpus stage, before any date signal existed

**What forced it.** The GOVUK seed fixed in C2-RULE-1,
`https://www.gov.uk/government/collections/ai-regulation`, **returns HTTP 404.** The corpus run
recorded it as `FAILED / 404` (`corpus-2.json`, first run). The orientation probe that put it in
this document read its response headers with `curl -I -L` and **did not capture the status line** —
so the "known beforehand" disclosure above describing GOVUK's seed as `HTTP 200, no Last-Modified,
max-age=30, age: 0` was in fact a description of **GOV.UK's 404 error page**. That sentence is
wrong and is corrected here rather than edited away above.

**Why this correction is not a free hand.** A pre-registered seed that does not exist must be
replaced or its authority dropped; replacing it after seeing results would be tuning. Nothing had
been measured when this was written: the signal collector for the new authorities did not yet
exist, and `signals-2.json` did not exist. **No prediction below is changed, in either direction.**

**The replacement rule, stated before the replacement was chosen.** The GOVUK seed is the
highest-level live GOV.UK page owned by the United Kingdom's own official AI body, selected by HTTP
status alone. Candidates checked, in the order checked, with the status each returned at ~14:28Z:

| Candidate | Status |
|---|---|
| `…/government/collections/a-pro-innovation-approach-to-ai-regulation` | 404 |
| `…/government/publications/ai-regulation-a-pro-innovation-approach` | 200 — a single publication page, not a hub |
| `…/government/collections/ai-safety-institute-publications` | 404 |
| **`https://www.gov.uk/government/organisations/ai-security-institute`** | **200 — taken** |
| `…/government/organisations/department-for-science-innovation-and-technology` | 200 — a whole department, wider than AI |
| `…/government/topics/science-and-innovation` | 410 |

**GOVUK seed, as amended:** `https://www.gov.uk/government/organisations/ai-security-institute` —
the AI Security Institute's own page, which, like the EC and NIST seeds, is a hub that sends a
reader on to dated items. `collect_corpus_2.py` is updated to this seed and re-run; the first run's
`FAILED / 404` row is kept in the record, not overwritten.

**Disclosed, so it cannot be claimed as a confirmation** (probe at 14:29Z on the amended seed):
HTTP 200, **no `Last-Modified` header**, `etag: W/"b54d6d7c3a4474ddbf98c994e254716b"`,
`cache-control: max-age=300, public`, `age: 27`. One page is still not a corpus, and every
corpus-wide share in G1 remains an open prediction.

**Also disclosed at this stage, and not a prediction:** the C2-RULE-5 control ran on the EC seed and
found **30 of the 40** locked session-94 EC URLs reproduced by the new link-region rule. That number
is a property of the rule change, not of any authority's currency signals.

---

## Amendment 2 — 2026-08-06, still at the corpus stage, still before any date signal existed

**What happened.** Under the amended seed, GOVUK's corpus is **7 URLs — below the floor of 15**, so
by C2-RULE-4 **GOVUK is inconclusive and is not re-scoped.** That stands and is not revisited.

**Why it is 7, recorded as an unpredicted observation about the site's architecture, not as a
result about its dates.** The seed page carries 81 links in total but only 14 inside its `<main>`
region; of those, 4 point at paths beginning `/search` and are dropped by C2-RULE-3. GOV.UK's
organisation hub does not list its documents as links — it sends a reader to a **search query**.
The rule that excludes search endpoints was written before any of this was seen, and it is not
being relaxed now to rescue a number.

**What GOVUK still contributes, and what it may not.** The 7 URLs are measured with the same rules
and reported. **Every GOVUK figure is marked inconclusive (n = 7) and scores nothing** — not for a
prediction, not for the continuation test, in either direction.

**One further authority, by a procedure fixed before any candidate was inspected.** With GOVUK
below the floor, a generalisation claim would rest on two authorities. So one more is added, and
the selection procedure is written here *before it is run*:

> Take the following five candidate hubs, in this fixed order, and test each for (a) HTTP 200,
> (b) an XML sitemap reachable at `/sitemap.xml` or named in `robots.txt`, (c) no bot interstitial.
> **The first candidate that passes all three is taken; the search stops there.** If its corpus
> also falls below the floor of 15, it is likewise inconclusive and **no further authority is
> added** — one attempt, declared as one.
>
> 1. Australia — `https://www.industry.gov.au/science-technology-and-innovation/technology/artificial-intelligence`
> 2. Canada — `https://ised-isde.canada.ca/site/ised/en/artificial-intelligence`
> 3. Ireland — `https://enterprise.gov.ie/en/what-we-do/innovation-research-development/artificial-intelligence/`
> 4. Japan — `https://www.digital.go.jp/policies/ai`
> 5. Singapore — `https://www.imda.gov.sg/how-we-can-help/artificial-intelligence`

The order is alphabetical by country and was written down before any of the five was fetched. A
candidate that 404s is simply disqualified; that is not a judgement about the country.

**The predictions are not rewritten.** G1, G3 and G4 name GOVUK explicitly; where GOVUK is
inconclusive those clauses are reported **NOT RESOLVABLE on GOVUK**, and the new authority is
scored in its own right rather than substituted into GOVUK's place. G5 and the continuation test's
clause (b) range over "the authorities measured", which now means EC, NIST and the new one, with
GOVUK's n = 7 excluded from both.

---

## Amendment 3 — 2026-08-06, corpus stage, before any date signal existed: the chrome control

**What forced it.** Two of the three measured authorities have no `<main>` element, so C2-RULE-2's
fallback takes the whole document, and the whole document includes site chrome. It shows in the
data before any date was collected: IE's first extracted links are *Privacy-Statement*,
*cookie-management*, *publications*, *legislation*, *faqs*. A corpus of navigation is a poor stand-in
for "the pages this hub sends a reader to". The rule is pre-registered and **is not being relaxed**;
the primary scoring stays on the corpora as extracted.

**The control, fixed before any signal exists.** For each authority, fetch **one unrelated page of
the same host — the site's own home page `https://<host>/` — and extract links from it with the
same extractor.** A corpus URL that also appears on the home page is **chrome**; one that does not
is an **item**. This is a measurement, not a judgement: no URL is hand-classified.

**How it is allowed to count.** Every headline figure is reported twice: over the full
pre-registered corpus (**the scored figure**) and over the item-only subset (**the robustness
figure**, stated with its n). **Predictions are scored on the full corpus only.** If the two
readings disagree, that disagreement is itself reported, in the same type size, as a defect of the
corpus rule (D7) — the instrument's own limit, not a result about any authority.

For EC, whose corpus and signals are locked from session 94, the chrome control is computed the
same way and applied as a **re-analysis of locked data**, clearly labelled; the locked figures
themselves are not altered.

---

## Amendment 4 — 2026-08-06, corpus stage, before any date signal existed: the chrome filter moves into selection

**What the amendment-3 control returned, immediately and before any date signal was collected:**
of the 40 pre-registered corpus URLs, **NIST 39 and IE 39 are chrome** — links that also appear on
the host's own home page. Scoring the currency signals of a navigation bar and calling it "what
this hub tells a citer about its documents" would be a false headline, and it would be false for
reasons visible in the corpus, not in the results.

**The change.** For all authorities measured today, the corpus is the **first 40 same-host links in
document order that are not chrome**, chrome being defined exactly as amendment 3 defines it
(appearing on `https://<host>/`, same extractor). The host root itself is chrome by definition and
is excluded. Everything else in C2-RULE-3 and C2-RULE-4 is unchanged, floor included.

**What this decision was made on, and what it was blind to.** It was made on **corpus composition
only**. At the moment of writing, no `Last-Modified`, no sitemap `<lastmod>` and no visible date had
been collected for GOVUK, NIST or IE — `collect_signals_2.py` did not yet exist. The commit order in
this repository is the evidence and is meant to be checked.

**Both arms are kept and both are reported.** Arm A — the corpora exactly as first pre-registered
(40/40/7). Arm B — the chrome-filtered corpora (NIST **35**, IE **17**, GOVUK **7**). **Predictions
are scored on Arm B.** Arm A is measured and reported alongside; where the two arms disagree, the
disagreement is reported in the same type size as the headline, as defect **D7** of the corpus rule.

**EC is not re-collected.** Its locked corpus of 40 (of which 36 are items by the same control) and
its locked signals from 08:26:37Z stand as measured; EC's Arm B figures are a **re-analysis of
locked data**, labelled as such wherever they appear.

**GOVUK remains inconclusive** at n = 7 under C2-RULE-4 — both arms agree, because none of its 7 is
chrome — and scores nothing.

*Correction to amendment 4, same stage, still before any date signal: the executed rule yields
**NIST 34**, not the 35 quoted above. The difference is the host root `https://www.nist.gov/`,
which the amendment's own sentence excludes as chrome by definition and which the earlier probe
had counted as an item. IE is 17 and GOVUK 7 as stated. With the root excluded, **40 of 40** Arm-A
NIST URLs are chrome and 39 of 40 IE.*
