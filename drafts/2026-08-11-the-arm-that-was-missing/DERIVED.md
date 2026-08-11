# Derivation — every command, every raw figure, and how to re-run it

*Session 109, 2026-08-11. Every number in `CONCEPT.md` and `RESULT.md` comes from here. All
fetches were made after the pre-registration commit `d39b512` (2026-08-11T03:40:50Z). Published so
the figures can be disputed rather than believed. Scripts are in this directory; raw outputs are
committed beside them.*

## 0. The instrument watch — one request, and the clock keeps running

```
curl -sSI -m 30 "https://playground.tiktok-audit.com/api-na/"
```

Load-bearing response lines, verbatim (`instrument-watch-2026-08-11.txt`):

```
HTTP/2 200
date: Tue, 11 Aug 2026 03:40:59 GMT
content-length: 246014
last-modified: Wed, 14 Jan 2026 20:53:43 GMT
etag: "69680257-3c0fe"
```

Unchanged from session 108's observation in every load-bearing field. **2026-01-14 → 2026-08-11 is
209 days.** *(P1 holds.)*

## 1. The corpus route that died, and why it died — a primary source

The pre-registered corpus route was the public web-crawl index (`index.commoncrawl.org` /
`data.commoncrawl.org`, credential-free). It was tried first:

| Step | Command | Result |
|---|---|---|
| CDX API | `curl "https://index.commoncrawl.org/collinfo.json"` | **connection reset**, twice |
| Columnar index, latest crawl | `curl -I ".../crawl-data/CC-MAIN-2026-30/cc-index.paths.gz"` | HTTP 200 |
| Whole block index | `curl -o cluster.idx ".../CC-MAIN-2026-30/indexes/cluster.idx"` | HTTP 200, **103,946,392 bytes** |
| Keys under the platform's domain | `grep -c "^com,tiktok)" cluster.idx` | **0** blocks begin there |
| The one block containing them | ranged GET, bytes 572948641–573207040 of `cdx-00138.gz` | HTTP 206, 258,400 bytes, 3,000 index lines |
| Entries for the platform | `grep -c "^com,tiktok)" blk.cdx` | **339** |
| Of those, video pages | `grep "^com,tiktok)" blk.cdx \| grep -c "/video/"` | **0** |
| What the 339 are | `awk` on the SURT path | **339 / 339 = `/robots.txt`** |

The reason is published by the platform itself. `curl -sS "https://www.tiktok.com/robots.txt"`
(HTTP 200, 1,288 bytes, saved as `tiktok-robots-2026-08-11.txt`) opens with a list of 25 named
user-agents followed by one line. Verbatim, the first and last entries of that block and the rule:

```
User-agent: Baiduspider
...
User-agent: CCBot
...
User-agent: Bytespider
Disallow: /
```

`CCBot` is the crawler of the public web-crawl archive. **In the July 2026 crawl the archive holds
exactly one path from this domain — the file that tells it to stay out.** The public web's largest
free corpus contains no page of this platform, by the platform's own instruction, and therefore
cannot serve as external ground truth about what the platform publishes.

*(This is a finding, not only an obstacle. It is the first half of the concept's claim: the
platform's public content is observable only through the platform's own interfaces.)*

**Second route tried, and blocked here:** the public web archive's index API
(`web.archive.org/cdx/search/cdx`) returned **HTTP 403 "Blocked by egress policy"** and the plain
host reset the connection. That host has now been unreachable from this practice for **five
consecutive sessions**; it is recorded as a gap, not as an absence.

## 2. The corpus that was built instead

**Source:** the MediaWiki external-link index (`action=query&list=exturlusage`), the wiki's own
index of external links in article wikitext. Credential-free, no account. Article namespace only
(`eunamespace=0`), HTTPS links only, query `tiktok.com`, paginated to exhaustion at 500 rows per
call with a 1-second delay. Script: `collect_corpus.py`. Raw output: `corpus-<wiki>.json` for each
of 21 language editions.

Two editions returned HTTP 429 on the first attempt and were re-asked after a 20-second wait
(`th`, `ru`, `zh`); every reported edition completed without a truncated page. No page cap was hit.

| Edition | API pages | link rows | rows with `/video/` | distinct ids |
|---|---|---|---|---|
| en | 10 | 2,513 | 906 | 853 |
| ja | 20 | 9,013 | 568 | 538 |
| es | 3 | 1,094 | 274 | 268 |
| he | 10 | 4,742 | 151 | 147 |
| id | 8 | 3,475 | 124 | 120 |
| de | 2 | 356 | 111 | 107 |
| pt | 2 | 833 | 91 | 88 |
| uk | 9 | 4,225 | 67 | 65 |
| ko | 2 | 647 | 66 | 30 |
| ru | 14 | 6,349 | 50 | 50 |
| zh | 4 | 1,391 | 54 | 49 |
| tr | 1 | 218 | 47 | 47 |
| pl | 1 | 188 | 43 | 42 |
| it | 1 | 82 | 32 | 32 |
| ar | 9 | 3,897 | 32 | 30 |
| nl | 1 | 85 | 28 | 28 |
| vi | 2 | 458 | 23 | 23 |
| th | 2 | 425 | 15 | 15 |
| fa | 1 | 122 | 14 | 13 |
| sv | 1 | 58 | 11 | 10 |
| fr | 1 | 30 | 1 | 1 |

**Merged and de-duplicated by video id: 2,201 distinct videos, across 1,563 distinct wiki
articles** (`build_sample.py` → `corpus-merged.json`). *(P2 holds: ≥ 1,000.)*

### Dating the corpus, and checking the dating

Each id is dated from the id itself: the top 32 bits of the 64-bit numeric id are a unix
timestamp in seconds. This is a **convention**, not something the platform states to us, so it is
checked against a source the platform does not control — the date a human editor typed into the
citation template that carries the link (`validate_timestamps.py`, English Wikipedia only, 120
articles, dates scoped to the **enclosing template** rather than a character window):

| Quantity | Value |
|---|---|
| (id, cited-date) pairs checked | 160 |
| Pairs where the video is dated **after** the date it is cited under (> 1 day) | **6** (3.8 %) |
| 10th percentile of (cited − created) | **−0.9 days** |
| Median | **+19.3 days** |
| 90th percentile | +1,151.5 days |

A correct decoding predicts exactly this shape: citations cannot precede the video, and a large
share of them happen within a day or two of it. The six violations are listed in
`timestamp-validation.json`; a `date=` field in a citation frequently carries the date of the event
rather than of the video, which is the obvious explanation and is **not** tested here.

**Four ids in the corpus decode outside the platform's lifetime** (1971, 1975 ×3) — short,
malformed ids, listed in `corpus-merged.json`. They are excluded from the age analysis and reported
rather than dropped silently.

Distribution of the corpus by decoded year: 2018 (2), 2019 (26), 2020 (111), 2021 (203), 2022
(320), 2023 (463), 2024 (481), 2025 (460), 2026 (131), out-of-lifetime (4).

## 3. The probe — the control arm the dark instrument never had

The platform's own credential-free oEmbed endpoint, one request per video, sequential, 1-second
delay, no account, no key, no application (`probe.py`, raw output `probe-results.json`):

```
GET https://www.tiktok.com/oembed?url=https%3A%2F%2Fwww.tiktok.com%2F%40<handle>%2Fvideo%2F<id>
```

**Before the first probe request, `robots.txt` was read to its end** (§1). The `User-agent: *`
group `Disallow`s fifteen paths — `/inapp`, `/auth`, `/embed/@`, `/embed/v2`, `/embed/curated`,
`/link`, `*/directory/`, `/search/video?`, `/search/user?q=`, `/shop/view/product/`,
`/sgtm/g/collect`, `/api/share/settings`, `/api/recommend/embed_videos`,
`/discover/trending/detail/`, `/search?`, `/search/live?` — and `/oembed` is not among them. This
client is none of the 25 named agents. The consideration is recorded rather than assumed.

### The pre-registered sample

Seed **20260811**, stratified by decoded creation year, **n = 300** (`build_sample.py`).

| Quantity | Value |
|---|---|
| Requests issued | **300** |
| Wall time | **472.7 s** (0.635 req/s) |
| HTTP 200 | 262 |
| HTTP 400 | 37 |
| Transport failures | **1** (TLS handshake timeout) — 0.33 % |
| Throttling responses (429) | **0** |

*(P3 holds: 300 consecutive requests, 0.33 % transport failure, well under 5 %. K2 does not fire.)*

**Every one of the 37 non-200 responses was HTTP 400 with the identical body**
`{"message":"Something went wrong","code":400}`. **No 404 was ever returned.** *(P6 holds — and it
holds in the direction that costs us: see §4.)*

### Retrievability by decoded creation year (299 usable responses)

| Year | n | retrievable | rate | 95 % CI (Wilson) |
|---|---|---|---|---|
| 2018 | 1 | 1 | 1.000 | 0.207–1.000 |
| 2019 | 4 | 2 | 0.500 | 0.150–0.850 |
| 2020 | 15 | 13 | 0.867 | 0.621–0.963 |
| 2021 | 27 | 21 | 0.778 | 0.592–0.894 |
| 2022 | 43 | 34 | 0.791 | 0.648–0.886 |
| 2023 | 63 | 55 | 0.873 | 0.769–0.934 |
| 2024 | 66 | 62 | 0.939 | 0.854–0.976 |
| 2025 | 62 | 57 | 0.919 | 0.825–0.965 |
| 2026 | 18 | 17 | 0.944 | 0.742–0.990 |

**Overall 262 / 299 = 87.6 %** retrievable on 2026-08-11. Pooled: **≤ 2022: 71 / 90 = 78.9 %**;
**≥ 2023: 191 / 209 = 91.4 %**. Point-biserial correlation of year with retrievability
**r = 0.171, t = 2.990, df = 297** (two-sided p ≈ 0.003).

*(P4: the first half holds — retrievability is well below 100 %. The second half holds as a trend
and **fails as a monotone**: 2020 sits above 2021 and 2022, and 2025 sits below 2024. Reported as a
part-failed prediction, not as a confirmation.)*

### A methodological by-product, recorded because it will matter to anyone reusing this

**10 of the 262 retrievable videos (3.8 %) are served under a different creator handle than the one
written in the citation.** Examples from `probe-results.json`: `7422014957186764062` cited as
`@kcrwlosangeles`, served as `kcrwradio`; `6921472314706054406` cited as `@its.kels`, served as
`kelsxsea`. The endpoint resolves by numeric id and ignores the handle in the URL. **A link-checker
that resolves the cited URL as written will therefore misreport handle changes as disappearances**,
and any availability series built that way is contaminated. This instrument is not, because it keys
on the id.

## 4. Does the opaque 400 describe the video, or does it describe us? — the K3 test

Kill criterion K3 asks whether the non-200s are the endpoint refusing this client rather than
reporting on the video. That is testable, so it was tested (`reverify.py`, raw output
`reverify-results.json`, 176 requests, 300.0 s, starting 2026-08-11T04:00:02Z):

| Arm | What it is | Result |
|---|---|---|
| **A** | all 38 non-200 rows of the main run, re-asked **3×** on fresh connections | **109 × HTTP 400, 3 × HTTP 200, 2 transport failures** |
| **B** | 40 rows that returned 200, re-asked, interleaved between A's repetitions | **41 × HTTP 200, 1 transport failure** |
| **C** | 20 **synthetic** ids — well-formed, randomly generated, seed 20260811, almost certainly no such video | **19 × HTTP 400, 1 transport failure** |

Arm A resolves per video: **35 of 38 returned 400 on all three re-asks; 2 returned 400 on both
re-asks that completed and had one transport failure; and 1 returned 200 three times out of
three** — that one is `7173687443047189766`, the row whose main-run result was a *transport
failure*, not a 400. **So every one of the 37 main-run 400s reproduced as 400 on every re-ask that
completed, and the single unresolved row of the main run resolves to retrievable.**

**Correction to the headline, made here rather than later: retrievable is 263 / 300 = 87.67 %**, and
the "usable responses" figure of §3 (262 / 299) is the pre-re-verification number. Both are reported;
neither is hidden.

Arm B shows the endpoint was serving 200s throughout the same period. Arm C shows a synthetic id
that corresponds to nothing gets **the same 400 and the same body** as a video that once existed.

**What this establishes, and its exact limit:**

- The 400 is **video-specific and stable**, not a refusal of this client. **K3 does not fire.**
- The 400 is **semantically empty**. Deleted, banned, made private, geo-restricted, age-gated,
  never-existed — all one status, one message, no 404 anywhere. **The instrument yields a binary
  and nothing finer, and any artifact built on it must say so on its front page rather than in a
  method note.**

## 5. Sources fetched this session

| Source | URL | HTTP | Bytes |
|---|---|---|---|
| The dark instrument | `https://playground.tiktok-audit.com/api-na/` | 200 | 246,014 |
| Platform robots.txt | `https://www.tiktok.com/robots.txt` | 200 | 1,288 |
| Web-crawl block index | `https://data.commoncrawl.org/cc-index/collections/CC-MAIN-2026-30/indexes/cluster.idx` | 200 | 103,946,392 |
| Web-crawl CDX block | same collection, `indexes/cdx-00138.gz`, bytes 572948641–573207040 | 206 | 258,400 |
| Web-crawl CDX API | `https://index.commoncrawl.org/collinfo.json` | **connection reset** | — |
| Public web archive CDX | `http://web.archive.org/cdx/search/cdx?...` | **403 (egress policy)** | — |
| MediaWiki link index ×21 | `https://<wiki>/w/api.php?action=query&list=exturlusage&...` | 200 (3 × 429 re-asked) | — |
| oEmbed endpoint | `https://www.tiktok.com/oembed?url=...` | 200 / 400 | — |

Facts carried forward from session 108 and **not** re-derived here (they were independently
re-derived by a hostile party then, and their derivation is at
`drafts/2026-08-10-one-receiver-to-the-floor/DERIVED.md`): the dashboard's 279-row series, the
platform changelog line of 2026-02-26, the research-interface eligibility rules.
