# PRE-REGISTRATION — "As of Today"

**Written and committed 2026-08-06 (session 94), before any fetching code existed and before any
datum existed.** Nothing below may be edited after the first request goes out; amendments, if any,
are appended as dated blocks that say what changed and why, and the original text stays legible.

## The question

A page on an official policy surface is cited every day in the form *"as of <date>"*. Where does
that date come from, if the citer has no archive of the page's history?

Three signals are available at the moment of citation, and they are the only three:

| Key | Signal | Who states it | How a citer reaches it |
|---|---|---|---|
| **H** | HTTP `Last-Modified` response header | the delivering server / cache | any HTTP client, automatically |
| **S** | `<lastmod>` for that URL in the site's own XML sitemap | the publishing system | one extra fetch, machine-readable |
| **V** | a visible date printed in the page ("Last update …", "Published …") | the page's editors | a human reading the page |

**The claim under test (H1):** on this surface the signal that is easiest for a machine to read (H)
is the least informative about change — it reports the moment of *delivery* — and it therefore
certifies as fresh pages that the site's own sitemap says have not changed in months or years.

**The instrument measures what the surface tells a citer. It does not establish when a page really
changed** — that would need capture history, which this session cannot reach (see the session's
opening record). Every finding below is a statement about the signals, not about the underlying
edits. `S` is itself only the publishing system's claim; it is not ground truth either.

## Corpus — fixed before selection runs

**C-RULE-1.** The seed page is the Commission's own AI-Act policy page:
`https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai`.

**C-RULE-2.** The corpus is every distinct same-host link found in the seed page's HTML whose path
begins `/en/` — i.e. **the pages the Commission's own AI Act page sends a reader to** — taken in
document order, deduplicated on the URL with query string and fragment removed, excluding the seed
page itself.

**C-RULE-3.** Cap: the **first 40** such URLs in document order. If fewer than 15 survive, the
corpus is declared too small and the increment is reported as inconclusive rather than re-scoped.

**C-RULE-4.** The corpus list is committed as data before the date signals are collected, so the
selection cannot be tuned to the result.

## Measurement rules

**M-1 (H).** One `GET` per URL, no cache directives beyond default, recording the response's
`Last-Modified`, `Date`, `ETag`, `Cache-Control` and status. `H` is `Last-Modified` parsed as UTC.
Missing header → `H = null`.

**M-2 (S).** The site's sitemap(s) under `https://digital-strategy.ec.europa.eu/sitemap.xml`
(following sitemap-index entries if present, one level) are fetched once and parsed to a map
`url → lastmod`. `S` is that value for the URL, matched exactly after the same normalisation used
in C-RULE-2. Not listed → `S = null`, recorded as `NOT-IN-SITEMAP`.

**M-3 (V).** A visible date is looked for in the fetched HTML with a fixed, pre-declared pattern
set, applied in this order, first match wins:
1. `Last update[d]?[:\s]` followed within 40 characters by a date in `D Month YYYY`, `YYYY-MM-DD`
   or `DD/MM/YYYY` form;
2. `Publication date[:\s]` or `Published[:\s]` followed by the same;
3. a `<time datetime="…">` element.
No match → `V = null`. **The pattern set is not extended after seeing the data**; if it turns out to
miss dates that a human reader can see, that is recorded as a defect of the instrument (as
session 93's D6 was) and the affected count is reported as a bound, not silently repaired.

**M-4 (time base).** One run, one timestamp, recorded in UTC. All ages are computed against the
run's start time. Everything is committed: the corpus, the raw signal table, the derived table.

**M-5 (network honesty).** A URL whose fetch fails is `NETFAIL` and is excluded from percentages,
with its count stated next to every percentage it is excluded from.

## Predictions — written before the first request, each with its killer

**P1 — the header reports delivery, not change.** For **≥ 80 %** of URLs with a non-null `H`, the
gap between `H` and the run timestamp is **< 24 hours**.
*Killed if* that share is < 80 %.

**P2 — the two machine signals disagree, and not narrowly.** The **median** absolute gap between
`H` and `S`, over URLs where both exist, is **> 30 days**.
*Killed if* the median is ≤ 30 days.

**P3 — the freshness certificate on a stale page.** For **≥ 25 %** of URLs where both exist, `S` is
**older than 180 days** while `H` is **younger than 24 hours** — a page the publisher's own system
says has not changed in half a year, delivered under a header saying it changed today.
*Killed if* that share is < 25 %.

**P4 — the human signal is the rare one.** A visible date `V` is found on **fewer than half** of the
fetched pages.
*Killed if* `V` is found on half or more.

**A prediction that is killed is reported as killed, in the findings, in the same type size as one
that holds.** No prediction is added after the run; anything noticed that was not predicted is
reported explicitly as *unpredicted observation*, never as a hit.

## What is already known, and therefore cannot be claimed as a prediction

- The seed page returns HTTP 200 and its `Last-Modified` at 08:21 UTC on 2026-08-06 was
  `Thu, 06 Aug 2026 08:01:00 GMT` — 20 minutes old, with `Cache-Control: public, max-age=300,
  s-maxage=300`. This single observation motivated P1; it is one page, and it is excluded from
  nothing, but it is disclosed here so it cannot later be presented as a confirmation.
- The site publishes an XML sitemap with `<lastmod>` values (805 `<lastmod>` elements seen in
  `sitemap.xml` at orientation).
- No visible "last update" label was found on the seed page by an ad-hoc grep at orientation. This
  motivated P4 and is likewise disclosed.

## What would make this increment worth continuing (the gate's own test)

The increment is worth a second proof session **only if** the answer to "where does a citer's date
come from?" is materially different across the three signals — i.e. **at least one of P1–P3 holds
and at least one is killed**, or all three hold. If all four predictions are killed, the honest
reading is that this surface's currency signals broadly agree, the concept has no daylight, and the
line is discarded with a one-page finding rather than argued forward.
