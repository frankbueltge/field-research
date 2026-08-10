# Derivation — commands, raw figures, and how to re-run them

*Session 108, 2026-08-10. Everything in `RESULT.md` that is a number comes from here. All fetches were
made after the pre-registration commit `018e7ba`. Published so the figures can be disputed rather than
believed.*

## 1. The instrument's staleness

```
curl -sSI "https://playground.tiktok-audit.com/api-na/"
```

Response headers, verbatim in the load-bearing lines:

```
HTTP/2 200
server: nginx/1.18.0 (Ubuntu)
date: Mon, 10 Aug 2026 22:08:54 GMT
content-type: text/html
content-length: 246014
last-modified: Wed, 14 Jan 2026 20:53:43 GMT
etag: "69680257-3c0fe"
```

The page body carries the same date in its own words: `Dashboard generated on: 2026-01-14 21:53:41`.
2026-01-14 → 2026-08-10 is **208 days**.

## 2. The series, read out of the page's own embedded data

The page embeds its plots as JSON inside the HTML. The aggregate plot carries three named traces
(`Available`, `Error`, `Not Available`) with one value per day; each per-video plot carries a single
status trace whose axis is labelled by the page itself:

```
yaxis tickvals: [0, 1, 2]
yaxis ticktext: ['Not Available', 'Error', 'Available']
```

Method: fetch the page; locate each `Plotly.newPlot(` call; decode the JSON array of traces that
follows it and the layout object after that; sum the aggregate traces; histogram the per-video traces.

**The two readings reconcile exactly**, which is the check that the per-video panels and the headline
chart describe the same data:

```
AGGREGATE totals:  Available=213  Error=181  NotAvailable=2634
PER-VIDEO totals:  {0: 2634, 1: 181, 2: 213}
```

*(A first pass in this session read the per-video panels as binary and reported the wrong quantity —
see `DEVIATIONS.md` D1. The reconciliation above is what caught it, before anything was written.)*

### Aggregate

| Quantity | Value |
|---|---|
| First / last daily row | 2025-04-09 / 2026-01-14 |
| Rows | 279 |
| Calendar span | 281 days |
| Days absent from the run | 2 — 2025-05-23, 2025-12-13 |
| Video-days | 3,028 = 10 × 279 + 1 × 238 |
| Available | 213 (7.03 %) |
| Not Available | 2,634 (86.99 %) |
| Error | 181 (5.98 %) |
| Terminal all-11-Error run | 2026-01-03 → 2026-01-14, 12 consecutive days |

### Per video

`obs` is the number of daily rows for that video; the eleventh enters the series on 2025-05-20.

| Video ID | Creator (per the page) | obs | Available | Error | Not Available |
|---|---|---|---|---|---|
| 7366758818765638917 | camilapudim | 279 | **0** | 16 | 263 |
| 7368154048836406544 | yy0403_2 | 279 | **0** | 18 | 261 |
| 7074367286571814190 | brynnemarieeee | 279 | **0** | 17 | 262 |
| 7117394257064840490 | brookemonk_ | 279 | **0** | 18 | 261 |
| 7134492331117595950 | realnikocadoavocado | 279 | **0** | 15 | 264 |
| 7164125023886691626 | taylorswift | 279 | **0** | 18 | 261 |
| 7376726215178128673 | alandelantics | 279 | **0** | 15 | 264 |
| **7332960275127110954** | andyyahurd._ | 279 | **213** | 20 | 46 |
| 7347581705299053826 | Evony | 279 | **0** | 16 | 263 |
| 7376437810644946222 | lauren.j734 | 279 | **0** | 14 | 265 |
| 7361448925972155679 | tiktok | 238 | **0** | 14 | 224 |

**10 of 11 videos: zero Available days across the entire series.** One video carries all 213.

## 3. The credential-free probe

Eleven requests, one per tracked video, one second apart, on 2026-08-10:

```
curl -sS -m 25 -o "oe_$vid.json" -w "%{http_code} %{size_download}" \
  "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@<creator>/video/<vid>"
```

The video URLs were taken from the dashboard's own markup. No authentication, no API key, no
registration.

| Video ID | HTTP | Bytes | `author_unique_id` returned |
|---|---|---|---|
| 7074367286571814190 | 200 | 1,332 | brynnemarieeee |
| 7117394257064840490 | 200 | 1,363 | brookemonk_ |
| 7134492331117595950 | **400** | 45 | — (`{"message":"Something went wrong","code":400}`) |
| 7164125023886691626 | 200 | 1,564 | taylorswift |
| 7332960275127110954 | 200 | 1,626 | andyyahurd._ |
| 7347581705299053826 | 200 | 1,257 | Evony |
| 7361448925972155679 | 200 | 1,309 | tiktok |
| 7366758818765638917 | 200 | 2,223 | camilapudim |
| 7368154048836406544 | 200 | 1,303 | yy0403_2 |
| 7376437810644946222 | 200 | 1,384 | lauren.j734 |
| 7376726215178128673 | 200 | 2,871 | alandelantics |

A returned payload carries `title`, `author_name`, `author_url`, `author_unique_id`, `thumbnail_url`,
and embed markup. It does **not** carry view counts, hashtags, creation time, or any of the fields the
Research API is meant to serve — this probe establishes public presence, nothing more.

**Limits, stated.** One observation per video on one day. HTTP 400 is recorded as HTTP 400: we did not
establish why that video is not served, and no inference about deletion, ban or restriction is drawn
from it. The ten HTTP 200s say the videos are publicly retrievable today; they say nothing about what
the Research API does with them today, which is the question and is closed to us (`RESULT.md` F5).

## 4. Every other source, with its fetch

| Source | URL | HTTP | Bytes |
|---|---|---|---|
| The report (abstract, authors, dates) | `https://arxiv.org/abs/2506.09746` | 200 | 42,309 |
| The report page | `https://aiforensics.org/work/tk-api` | 200 | 43,145 |
| The group's publication index | `https://aiforensics.org/work` | 200 | 165,613 |
| Platform changelog (F4) | `https://developers.tiktok.com/doc/changelog` | 200 | 751,085 |
| Platform eligibility rule (F5) | `https://developers.tiktok.com/products/research-api/` | 200 | 399,135 |
| Independent audit, 2026-01-18 | `https://arxiv.org/abs/2601.12390` | 200 | 44,693 |
| Commission preliminary findings, 2025-10-24 | `https://digital-strategy.ec.europa.eu/en/news/commission-preliminarily-finds-tiktok-and-meta-breach-their-transparency-obligations-under-digital` | 200 | 50,613 |

**Routes that refused, and what was done** (standing rule from session 107: a page that fails one route
is retried on another before anything depends on it):

- The paper-index tool and the PDF-to-text conversion both failed on this machine. The abstract page
  was fetched directly instead, and no claim in `RESULT.md` depends on the paper's body text — only on
  its abstract, authors and submission history, all read from the fetched abstract page.
- A direct fetch of the audit code repository was refused (HTTP 403, twice, from this machine). It was
  re-opened by a second route, and the result is recorded as second-route material in `RESULT.md` F7,
  where it carries no load: the disposition does not depend on it.
- No outcome in this session is recorded as provisional on a page we could not open.
