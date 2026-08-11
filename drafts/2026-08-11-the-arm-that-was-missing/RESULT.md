# Result — gate session 1, *The Arm That Was Missing*

*Session 109, 2026-08-11. Findings, predictions and kill criteria, in the order they were fixed
before the work. Every number is derived in `DERIVED.md`, which publishes the command behind it.
Nothing here is a packet; no `status` is claimed; no party named here has been or will be contacted
by this practice.*

---

## The findings

### F1 — The instrument is still dark, and the count is now 209 days

`last-modified: Wed, 14 Jan 2026 20:53:43 GMT`, served today at HTTP 200, 246,014 bytes, unchanged
from session 108's observation in every load-bearing field. The page still describes itself in the
present tense: *"The dashboard performs daily availability tests on selected number of videos that
are missing from the API."*

**Read to the end this time, and two sentences were waiting there.** The same page carries, in its
own words, the limit of its scale — *"Note that although this dashboards only monitors a dozen of
videos, we have identified the same issue on thousands of other pieces"* — and the limit of its
meaning: *"Note: Error are problems on our end, not TikTok."* Its final stat cards read **"11 Total
Videos Tracked · 0 Available Videos · 0 Unavailable Videos · 11 Videos with Errors."** The
instrument's last published state is that it cannot see anything, and it says the fault is its own.

### F2 — The platform's public content is absent from the public web's largest free corpus, by the platform's own instruction

In the July 2026 crawl, the index holds **339 entries for this domain and every one of them is
`/robots.txt`. Zero video pages.** The reason is in the file itself: 25 named crawler agents,
including the crawler of that archive, followed by `Disallow: /`.

This is not merely an obstacle to our method. **It is the structural fact the concept rests on:
there is no independent, third-party, at-scale record of what this platform published, because the
platform has instructed the one organisation that would keep it not to look.** Any claim the
platform makes about the completeness of what it serves to researchers is therefore uncheckable
against anything except the platform's own other interfaces.

### F3 — The control arm exists, is credential-free, and cost 300 requests

**2,201 videos cited as sources in 1,563 articles across 21 language editions** of a public
encyclopedia, dated from the videos' own identifiers, all reachable through one public API with no
account. Of the **300** pre-registered sample (seed 20260811, stratified by year):

**263 of 300 — 87.7 % — were publicly retrievable on 2026-08-11.** One transport failure in the
main run, resolved to retrievable on re-ask. **Zero throttling responses.**

### F4 — Retrievability falls with age, and the fall is significant but not monotone

**≤ 2022: 71 / 90 = 78.9 %. ≥ 2023: 191 / 209 = 91.4 %.** Point-biserial correlation of decoded
creation year with retrievability **r = 0.171, t = 2.990, df = 297** (two-sided p ≈ 0.003).

The per-year series is **not monotone**: 2020 (86.7 %) sits above 2021 (77.8 %) and 2022 (79.1 %),
and 2025 (91.9 %) sits below 2024 (93.9 %). The pre-registered prediction P4 claimed a decline with
age; **it holds as a trend and fails as a monotone, and is reported as a part-failure.**

### F5 — The only credential-free presence signal this platform offers is semantically empty

Every one of the 37 non-retrievable rows returned **HTTP 400** with the identical body
`{"message":"Something went wrong","code":400}`. **No 404 was returned, ever.** A three-arm control
(176 further requests) establishes what that means and what it does not:

- **It is not a refusal of this client.** 35 of 38 rows returned 400 on all three re-asks; the
  remaining rows returned 400 on every re-ask that completed; and a control group of previously
  retrievable videos returned 200 throughout the same period.
- **It is video-specific and stable.** Every one of the 37 main-run 400s reproduced.
- **It carries no cause.** **19 of 20 synthetic identifiers** — well-formed, randomly generated,
  corresponding to no video — returned **the same 400 and the same body**.

Deleted, banned, made private, geo-restricted, age-gated, never-existed: one status. **The
instrument can say a video is not publicly retrievable through this route today. It can never say
why.** This is on the concept's front page, not in a footnote.

### F6 — A contaminant that will be in anyone else's link-checker, and is not in this one

**10 of the 262 retrievable videos in the sample (3.8 %), and 123 of 1,941 in the census (6.34 %),
are served under a different creator handle than the one written in the citation.**

**Amended after the adversary, and the amendment makes the fact simpler and stronger.** The endpoint
does not tolerate a stale handle — **it does not check the handle at all.** Reproduced here with our
own commands on three of our own census rows (`REFUTATION-REPRODUCED.md`): a handle that has never
existed returns HTTP 200 with the true author, and so does a URL with no handle in the path. A checker that resolves the cited URL as written will therefore **score a handle
change as a disappearance**. This instrument keys on the identifier and does not.

### F7 — The identifier dating was validated against an artifact neither we nor the encyclopedia control

The decoding (top 32 bits of the identifier = unix seconds) is a convention. Checked against the
dark dashboard's **own displayed creation dates** for its eleven videos: **9 of 11 agree to within
60 seconds** once the dashboard's clock is read as Europe/Berlin local time — an offset inferred
from the data (+1 h in November and March, +2 h in May, June, July, August), not stated by the page.
**Two disagree, by 30 and 49 days; no explanation is offered** (`DEVIATIONS.md` D6).

A second, weaker check against human-written citation dates in article wikitext: **160 pairs, 6
ordering violations (3.8 %), 10th percentile −0.9 days, median +19.3 days** — the shape a correct
decoding predicts.

### F8 — Nobody else is running this, and nobody has tested the claim

A search fan-out, with every load-bearing item re-opened here:

- **No free, continuous, at-scale public-presence series** for this platform's videos exists. The
  nearest thing is the dark dashboard: eleven videos, the credentialed side, frozen.
- **No third party has tested or commented on** the 2026-02-26 coverage claim.
- **The receiver has published nothing on this subject since 2026-01-14** — eight publications since
  that date, none concerning this platform's research interface.
- The closest neighbour, **arXiv:2601.12390 (18 Jan 2026)**, re-opened here in full: sockpuppet
  accounts, credentialed APIs, election periods, weeks. Its abstract, read here: filters *"exclude
  large portions of the platform PIE (up to approximately 50 percent), strip essential contextual
  metadata (up to approximately 83 percent)"*; its body: *"between 17.7% and 23.3% of posts were no
  longer accessible within weeks."*

**A failure of our search is not a fact about the world** (session 108's standing rule): every
negative above is *"no third party we found"*, and it is written that way wherever it travels.

### F9 — The census: 2,201 videos, one day, and the age effect sharpens

The whole corpus, measured: **2,201 requests, 3,847 s, 28 transport failures (1.27 %), zero
throttling responses. 1,941 of 2,173 usable responses — 89.3 % — publicly retrievable on
2026-08-11.** The age effect is stronger and cleaner than in the sample: **r = 0.145, t = 6.810,
df = 2,167**; **≤ 2022: 85.0 %** against **≥ 2023: 91.3 %**; 2019 at 73.1 % rising to 2026 at 96.1 %.
**And the instrument is stable: of the 295 videos measured in both runs about an hour apart, 295
agreed. Zero disagreements.** (§6.)

---

## Predictions, scored against the pre-registration

| | Prediction | Outcome |
|---|---|---|
| **P1** | Instrument still dark, `last-modified` unchanged | **HOLDS** |
| **P2** | Corpus route yields ≥ 1,000 distinct dated ids in ≤ 10 queries | **HOLDS on our reading (2,201); FAILS on the strictest reading of our own pre-registration** (853 from a single edition) — `DEVIATIONS.md` D1. The adversary judged our reading *"the closest thing to a self-serving reading in the whole record"*; the qualifier now sits on `CONCEPT.md`'s front page |
| **P3** | ≥ 300 consecutive requests, < 5 % transport failure | **HOLDS** (300 requests, 0.33 %) |
| **P4** | Retrievability well below 100 %, declining with age | **PART-HOLDS, PART-FAILS** — 87.7 %, significant trend, **not monotone** |
| **P5** | No free continuous at-scale series published by anyone else | **HOLDS** (as "none we found") |
| **P6** | > 10 % of non-200s carry a status other than 404 | **HOLDS — 100 %, and it holds against us**: the route is semantically empty |
| **P7** | The coverage claim is still untested by any third party we can find | **HOLDS** |

**Five hold, one holds against us, one part-fails, one is contested by our own deviation note.**

## Kill criteria

| | Criterion | Fires? |
|---|---|---|
| **K1** | < 1,000 distinct dated ids credential-free | **No** (2,201) — but see D1, where the strict reading says yes |
| **K2** | Probe cannot sustain 300 requests at ≥ 0.5 req/s, < 5 % failure | **No** (0.635 req/s, 0.33 %) |
| **K3** | > half of non-200s are blanket refusals of this client | **No** — tested, not argued: the 400s are video-specific and stable (`DERIVED.md` §4) |
| **K4** | A free at-scale continuous series already exists | **No** — none found |
| **K5** | The artifact gives the receiver nothing their access does not give free | **The adversary's, not ours** |

## Corrections against our own text, this session

- **C1** — The headline retrievability figure was first computed as **262 / 299 = 87.6 %** from the
  main run alone. The re-verification resolved the single transport failure to retrievable, making
  it **263 / 300 = 87.67 %**. Both are published; the second supersedes the first.
- **C2** — The first timestamp-validation run reported 47 ordering violations. That was a bug in the
  script, not a property of the data (`DEVIATIONS.md` D2). It was never published as a result and is
  recorded because it was computed.

---

### F10 — The age effect survives an edition control (added after the adversary, condition 3)

Stratified by language edition (census, n = 2,169, ten editions with ≥ 10 videos in each age
stratum): **Mantel–Haenszel odds ratio 2.007** for retrievability of ≥ 2023 against ≤ 2022, against a
**crude odds ratio of 1.857**. The effect is not an artifact of edition composition; it strengthens
slightly under the control. **Three of the ten editions run the other way** (es −0.003, pt −0.040,
uk −0.109), all of them small strata. Full table: `edition-stratified-check.txt`.

### F11 — Every figure in this session was measured from one place, and now that place is on the record

`vantage-2026-08-11.md`: AS396982, Columbus, Ohio, US. Until the adversary raised it, this was true
and unlogged. It is the one charge that changes what the arc must do rather than how it must write.

---

## 6. The census — the whole corpus, not the sample

*Launched before the sample's numbers were written up as a claim, and it could not be selected
against: it is the entire population. Raw output `census-results.json`, script `census.py` (the
probe script with the sample line replaced by the whole corpus).*

| Quantity | Value |
|---|---|
| Requests issued | **2,201** |
| Wall time | **3,847.4 s** (0.572 req/s) |
| HTTP 200 | **1,941** |
| HTTP 400 | **232** |
| Transport failures | **28** (1.27 %) |
| Throttling responses (429) | **0** |
| **Publicly retrievable** | **1,941 / 2,173 usable = 89.3 %** |

### Retrievability by decoded creation year — the whole population

| Year | n | retrievable | rate | 95 % CI (Wilson) |
|---|---|---|---|---|
| 1975 (malformed ids) | 3 | 0 | 0.000 | 0.000–0.562 |
| 1971 (malformed id) | 1 | 1 | 1.000 | 0.207–1.000 |
| 2018 | 2 | 2 | 1.000 | 0.342–1.000 |
| 2019 | 26 | 19 | 0.731 | 0.539–0.863 |
| 2020 | 109 | 89 | 0.817 | 0.734–0.878 |
| 2021 | 201 | 170 | 0.846 | 0.789–0.889 |
| 2022 | 317 | 277 | 0.874 | 0.833–0.906 |
| 2023 | 456 | 389 | 0.853 | 0.818–0.883 |
| 2024 | 474 | 437 | 0.922 | 0.894–0.943 |
| 2025 | 456 | 434 | 0.952 | 0.928–0.968 |
| 2026 | 128 | 123 | 0.961 | 0.912–0.983 |

Restricted to ids inside the platform's lifetime (n = 2,169): **r = 0.1448, t = 6.810, df = 2,167**.
Pooled **≤ 2022: 557 / 655 = 85.0 %** against **≥ 2023: 1,383 / 1,514 = 91.3 %**. The series is
monotone from 2019 to 2026 **except** for 2023 (85.3 %), which sits below 2022 (87.4 %) — one
inversion in eight years, against two in the sample. **P4's monotonicity still fails, and it fails
by less.**

### Reliability — the only test that matters for a series that will run daily

**295 videos carry a status from both the sample run and the census, about an hour apart. All 295
agree. Zero disagreements.** A daily series is worth nothing if the measurement wobbles; this one
does not, over the interval tested. *(It does not follow that it will not wobble over a day; that is
what the arc measures.)*

### Three things the census shows that the sample could not

1. **The handle-change contaminant is twice as large as the sample suggested: 123 of 1,941
   retrievable videos (6.34 %) are served under a different creator handle than the one written in
   the citation.** Any availability series that resolves cited URLs as written would report those
   as losses.
2. **The malformed identifiers behave as malformed identifiers should:** of the four ids that decode
   outside the platform's lifetime, **three of three from "1975" are not retrievable**.
3. **196 of the 1,546 articles in the census (12.7 %) cite at least one video that is not publicly
   retrievable today; 157 of them cite no retrievable video at all.** This is a fact about the
   corpus, not a claim about encyclopedias, and it is the reason the population is worth watching
   daily rather than once.

### The by-edition spread, published because it invites a challenge

| Edition | retrievable / n | rate |
|---|---|---|
| en | 728 / 820 | 0.888 |
| ja | 460 / 505 | 0.911 |
| es | 188 / 225 | 0.836 |
| he | 107 / 113 | 0.947 |
| de | 102 / 107 | 0.953 |
| id | 73 / 80 | 0.912 |
| pt | 42 / 48 | 0.875 |
| uk | 37 / 47 | 0.787 |

**No inference is drawn from this table.** Editions differ in citation practice, topic mix and age
profile, and this practice has not controlled for any of them. It is published because someone will
want to test whether the spread survives an age control, and they should be able to.
