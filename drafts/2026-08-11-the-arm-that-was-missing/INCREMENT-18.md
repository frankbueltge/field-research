# Increment 18 — the evidence, read at last

*Session 128, 2026-08-20. `CONDITIONS-127.md` item 1, discharged before anything else was built:
**read the evidence already in hand.** What follows is what the receiver's own dashboard says when
somebody opens it, the instrument that opened it, and the scoring of a breakdown this practice
accepted into its record three days ago on an adversary's word.*

---

## 1. What was not read, and for how long

`receiver-dashboard-2026-08-19.html` is 246,014 bytes. This arc fetched it on 2026-08-16, fetched
it again on 2026-08-19, hashed it both times, cited it by hash in the third paragraph of a letter
addressed to the person who publishes it — and read six summary tiles out of it. Eight adversarial
reviews of the object built around those six tiles found fifteen defects between them, and not one
of the eight opened the file.

The eighth adversary did, and reported two facts from inside it. Session 127 reproduced the first
with a regular expression and refused the second, because a regex over Plotly payloads could not
say which array belonged to which video: fourteen numeric arrays came out, two of them plainly
other charts, and the finer per-video breakdown was recorded as **claimed-and-unreproduced**. That
was the right refusal and the wrong instrument.

## 2. The instrument

`extract_dashboard.py` (in this directory; ships inside the object). It walks the document with
`html.parser`, so the join between a series and its identifier is made by the document's own
element structure — each timeline is inside the `<div class="video-card">` whose `<h3>` reads
`Video ID: <digits>` — and never by proximity in a byte stream. The Plotly arguments are parsed
with `json.JSONDecoder().raw_decode`, so every number is read by a JSON parser. Status values are
mapped to words only through the axis's **own** `ticktext`/`tickvals`, and a value outside that set
is reported rather than mapped to the nearest label.

`--selftest` runs nine positive controls. The load-bearing one mutates the document: rename a
single card's `Video ID:` heading and the extractor must report **one problem and one fewer video**,
not silently attach that card's series to a neighbour. It does.

Output: `receiver-series-2026-08-19.json` (raw series, 11 videos, 0 problems) →
`dashboard_findings.py` → `dashboard-findings.json` (the derivation).

## 3. What the record says

**Eleven videos. Every series recorded daily from 2025-04-09 (one from 2025-05-20) to
2026-01-14** — 279 recorded days for ten of them, 238 for the one that starts later, with **two
two-day gaps** (after 2025-05-22 and after 2025-12-12) and no others.

**Every one of the eleven series changes state for the last time on 2026-01-03.** Ten go from *Not
Available* to *Error*; one goes from *Available* to *Error*. None changes again. Eleven days later,
on **2026-01-14**, the record stops.

| what | value |
|---|---|
| series whose last state change is 2026-01-03 | **11 of 11** |
| state they all changed to | `Error` |
| they came from | `Not Available` ×10, `Available` ×1 |
| record's last day | 2026-01-14 |
| days from the flip to the record's end | 11 |
| days from the record's end to this session's reading | 218 |
| final status of every series | `Error` (11 of 11) |

Eleven independently checked videos do not change state on one day. That is a statement about the
thing doing the checking, and the receiver's own page says as much in its own words — *"Note: Error
are problems on our end, not TikTok."* **What the page does not say is the date, and the date is
what was in the file nobody opened.**

**The one that is not like the others.** `7332960275127110954` was recorded *Available* on **213 of
its 279 days** (76.3 %). The 2026-01-03 flip took it too. A video their own instrument had recorded
as fine for most of nine months is inside the eleven that the page's tiles now count as errors.

**And the rest of the file was read too, with nothing further to report.** Each card also carries a
metadata table — creator, creation date, location, content type, hashtags, views, duration. Reading
all eleven yields one thing worth recording and no finding: the panel includes the platform's own
account (`7361448925972155679`, creator `tiktok`, and the one series that starts later, on
2025-05-20) and an advertiser (`7347581705299053826`, creator `Evony`, location `XX`), which is
consistent with the receiver's report having a section on advertisements and one on well-known
accounts. **Nothing in the metadata changes any figure above.** It is recorded because the failure
this increment exists to correct was not opening a file, and "we opened the rest of it and found
nothing" is the only honest way to close that.

**The tiles.** *11 tracked · 0 available · 0 unavailable · 11 with errors* are the record's state on
**2026-01-14**. The page **does** print `Dashboard generated on: 2026-01-14 21:53:41` — stated here
rather than left out, because it is the receiver's one defence against the charge that the page
presents a stale count as current. Two facts sit beside it and were checked rather than asserted:
that string begins at byte **245,199 of 246,014** in the served HTML — 99.7 % of the way
down it — under a *TECHNICAL INFORMATION* heading in the page footer; and the paragraph above the tiles reads, in the present
tense, *"The dashboard performs daily availability tests on selected number of videos."* The tiles
themselves carry no date.

**And the page has not moved since.** Read three times — 2026-08-16, 2026-08-19, 2026-08-20 — the
bytes are identical: `sha256 fff0a66f2bddc05106b892f7d18d59202eda1ab6829f71da7edbfea624f9c6bb`,
246,014 bytes each time.

**The extraction is checked against the page's own second chart, and agrees exactly.** The
dashboard draws an aggregate trend from a separate Plotly payload. Summing the eleven per-video
series per day and comparing value by value with that chart gives **837 comparisons across 279
dates and three status series, and 0 disagreements** (`dashboard-findings.json`
§`extraction_checked_against_the_pages_own_aggregate_chart`). So the flip is not an artifact of
this practice's parser — it is legible in the receiver's own summary chart:

| date | Available | Error | Not Available |
|---|---|---|---|
| 2026-01-02 | 1 | 0 | 10 |
| **2026-01-03** | **0** | **11** | **0** |
| 2026-01-04 | 0 | 11 | 0 |
| 2026-01-14 | 0 | 11 | 0 |

**And the server says the same thing independently of the page.** Read at 2026-08-20T04:09:20Z
(`receiver-dashboard-2026-08-20-fetch.json`), the response carries
`Last-Modified: Wed, 14 Jan 2026 20:53:43 GMT` and `ETag: "69680257-3c0fe"`. That is the web
server's statement about the file, owing nothing to the page's own footer text or to any reading of
its contents; it agrees with both to within the hour the footer's un-zoned timestamp leaves open
(footer `2026-01-14 21:53:41`, header `20:53:43 GMT` — consistent with a UTC+1 clock and a file
written two seconds after it was generated). **Three independent lines — the per-video series, the
page's own aggregate chart, and the HTTP header — put the last write on 14 January 2026.**

## 4. Scoring the breakdown this practice did not adopt

Recorded at `CONDITIONS-127.md` as claimed-and-unreproduced, and now scored mechanically in
`dashboard-findings.json` §`scoring_the_handed_over_breakdown` — with the claim stored **as data in
the script** so the scoring could not drift to fit the result.

| the claim, quoted from `INTERLOCUTOR-19.md` | verdict |
|---|---|
| "ten of the eleven" | **REPRODUCED** — 10 of 11 have *Not Available* on ≥ 200 of their days |
| "Not Available on 224–265 days" | **REPRODUCED** — exactly 224 to 265 |
| "(88–95 %)" | **NOT REPRODUCED** — on each series' own recorded days the range is **93.5–95.0 %** |
| "Nine of the eleven … are publicly fetchable right now" | **REPRODUCED** — 9 of those 10 were retrievable in this practice's 2026-08-19 reading |

Three of four hold exactly. The fourth does not, and this file does not claim to know which
denominator produced 88 %: it reports what the series say on the only denominator the series
themselves supply. **The adversary was right about the finding and wrong about one of its numbers,
and this practice would have shipped that number if it had adopted the breakdown on trust.** That
is the whole argument for the refusal session 127 made — recorded here as the one occasion the
refusal paid.

## 5. The bet, scored

Filed in `journal/2026-08-20.md` before the extractor was written:

- **Limb 1 — the flip reproduces on identified series: WON.** 11 of 11, each joined to its own
  identifier by the document's structure, and one of them coming from `Available` rather than from
  `Not Available` — which the anonymous-array extraction of session 127 could not have told anyone.
- **Limb 2 — at least one figure in the handed-over breakdown fails to reproduce: WON.** The
  percentage range.

Both limbs landing is the weaker outcome of the two the bet named. The stronger one — the flip
failing to reproduce, and session 127's headline retracting — did not happen, and is recorded as
not having happened rather than quietly dropped.

## 6. What this is not

- It does not identify a cause. This practice has not seen the code behind the dashboard, has not
  asked for it, and is not saying what broke.
- It does not show the receiver's error bucket is *wrong*. A video can be publicly fetchable **and**
  genuinely absent from a research interface; this measurement cannot separate the two and
  therefore cannot attribute their failures away from a real gap.
- It is a reading of one saved page. Everything above is reproducible from the bytes in the object
  by one command that needs no network and no cooperation from this practice.
