# Figures — generated, do not hand-edit

*Written by `figures_page.py` at 2026-08-16T17:30:13Z. **Every number on this page is fetched from a named field of a file in this bundle** — `expectation.json`, `gradient-test.json`, `series/presence-series.json`, or `figures-derived.json`, which is built from the series — and the field is recorded in `FIGURES-PROVENANCE.json` — the table that governs this page, a different file from the `FIGURE-PROVENANCE.json` that governs the prose. Before version 0.3.2 this page was generated from variables rather than from files, and three of its numbers were literals typed into the generator; see `VERSIONS.md`.*

## 1. The panel, and what was measured each day

| day | measurement started (UTC) | units requested | in the rate | publicly absent | absent rate | 95 % Wilson |
|---|---|---|---|---|---|---|
| baseline | 2026-08-11T11:24:06Z | 3,869 | 3,581 | 437 | 12.20 % | [11.17 %–13.32 %] |
| 2026-08-12 | 2026-08-12T03:40:28Z | 3,869 | 3,582 | 437 | 12.20 % | [11.17 %–13.31 %] |
| 2026-08-13 | 2026-08-13T04:27:00Z | 3,869 | 3,576 | 439 | 12.28 % | [11.24 %–13.39 %] |
| 2026-08-14 | 2026-08-14T03:43:47Z | 3,869 | 3,583 | 435 | 12.14 % | [11.11 %–13.25 %] |
| 2026-08-15 | 2026-08-15T03:37:40Z | 3,869 | 3,576 | 438 | 12.25 % | [11.21 %–13.36 %] |
| 2026-08-16 | 2026-08-16T03:37:40Z | 3,869 | 3,580 | 436 | 12.18 % | [11.15 %–13.29 %] |

**Across 6 measured days the pooled public-absence rate of this panel moves between 12.14 % and 12.28 % — a spread of 0.14 pp on the RAW panel.**
On the balanced panel — the 3,386 non-control identifiers that are determinate on every measured day — the spread is 0.0886 pp. The raw figure is 1.53× larger, and the excess is which units fell out as `INDETERMINATE`, not anything about the platform (first gauntlet, E17). This is the same panel measured again, so it is the instrument's test-retest reproducibility and not sampling error (`LIMITS.md`).

## 2. Public absence by the age of the video — newest day

*Day: 2026-08-16. Ages are decoded from the identifier (`LIMITS.md`).*

| age band | in the rate | publicly absent | absent rate | 95 % Wilson | spread across all measured days |
|---|---|---|---|---|---|
| 0-1y | 494 | 24 | 4.86 % | [3.29 %–7.13 %] | 0.25 pp |
| 1-2y | 768 | 58 | 7.55 % | [5.89 %–9.64 %] | 0.32 pp |
| 2-3y | 791 | 97 | 12.26 % | [10.16 %–14.73 %] | 0.48 pp |
| 3-4y | 674 | 109 | 16.17 % | [13.59 %–19.14 %] | 0.57 pp |
| 4-5y | 457 | 75 | 16.41 % | [13.30 %–20.08 %] | 0.44 pp |
| 5y+ | 389 | 68 | 17.48 % | [14.03 %–21.57 %] | 0.58 pp |

## 3. The same gradient inside each source stratum

*If the gradient were an artefact of which source the older identifiers come from, it would not survive this split.*

| age band | `F-forum` | `W-article` | `W-other-ns` |
|---|---|---|---|
| 0-1y | 4.08 % (n=49) | 5.26 % (n=304) | 4.26 % (n=141) |
| 1-2y | 15.69 % (n=51) | 5.79 % (n=535) | 10.44 % (n=182) |
| 2-3y | 13.98 % (n=93) | 9.63 % (n=519) | 18.99 % (n=179) |
| 3-4y | 18.80 % (n=117) | 15.03 % (n=439) | 17.80 % (n=118) |
| 4-5y | 14.29 % (n=77) | 15.18 % (n=303) | 23.38 % (n=77) |
| 5y+ | 14.04 % (n=57) | 17.10 % (n=269) | 22.22 % (n=63) |

**The gradient's own test — 0-1y against 5y+ on 2026-08-16, two-sided Fisher exact.** The pooled progression is not strictly monotone: it rises across the bands with one flat step near four years, and the endpoints are what is tested here.

| group | 0-1y | 5y+ | ratio | Fisher two-sided p |
|---|---|---|---|---|
| pooled | 24/494 (4.86 %) | 68/389 (17.48 %) | 3.60 × | 1.474 × 10<sup>-9</sup> |
| F-forum | 2/49 (4.08 %) | 8/57 (14.04 %) | 3.44 × | 1.027 × 10<sup>-1</sup> |
| W-article | 16/304 (5.26 %) | 46/269 (17.10 %) | 3.25 × | 5.758 × 10<sup>-6</sup> |
| W-other-ns | 6/141 (4.26 %) | 14/63 (22.22 %) | 5.22 × | 1.739 × 10<sup>-4</sup> |

## 4. Where the identifiers come from — newest day

| stratum | what it is | in the rate | publicly absent | absent rate |
|---|---|---|---|---|
| `F-forum` | public comments and stories of one technology forum | 444 | 64 | 14.41 % |
| `W-article` | article space of 37 encyclopedia language editions | 2,373 | 258 | 10.87 % |
| `W-other-ns` | non-article namespaces of the same editions | 763 | 114 | 14.94 % |

**Excluded from every rate on the newest day:** 249 identifiers of the `B-truncated` control arm, which are display-truncated strings, 248 of 249 of which do not resolve — the remainder is a real video predating the platform's current identifier scheme (first gauntlet, E7); 40 observations that ended in a transport failure or an unexpected status (`INDETERMINATE`, control arm not counted — see section 6); and 7 identifiers that carry no decodable creation time and are therefore absent from the age-banded tables only.

## 5. How much this panel moves at all

Over 6 measured days, **7 of 3,620** non-control identifiers show more than one determinate state in the raw record, and **5** do so after the refuted-reading overlay is applied. The identifiers are listed so the claim can be checked:

| video id | arm | baseline | 2026-08-12 | 2026-08-13 | 2026-08-14 | 2026-08-15 | 2026-08-16 | changes after overlay |
|---|---|---|---|---|---|---|---|---|
| `7016669364938149122` | A | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | no — refuted reading, see overlay |
| `7234106298021727515` | A | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | NOT-RETRIEVABLE | NOT-RETRIEVABLE | yes |
| `7298893164335729926` | A | NOT-RETRIEVABLE | NOT-RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | yes |
| `7446448990935354670` | A | NOT-RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | yes |
| `7266499914014723370` | A2 | NOT-RETRIEVABLE | NOT-RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | yes |
| `7368171405361351954` | A2 | RETRIEVABLE | RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | no — refuted reading, see overlay |
| `7118519163416497450` | B | NOT-RETRIEVABLE | NOT-RETRIEVABLE | NOT-RETRIEVABLE | NOT-RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | yes |

## 6. Transport noise

*Two counts, and they are not the same question. The first gauntlet found them printed together with nothing saying so (finding 14). `all units` includes the `B-truncated` control arm; `non-control` excludes it and is the scope of the exclusion counts in section 4.*

| day | INDETERMINATE, all units | share of the run | INDETERMINATE, non-control |
|---|---|---|---|
| baseline | 42 | 1.09 % | 39 |
| 2026-08-12 | 40 | 1.03 % | 38 |
| 2026-08-13 | 47 | 1.21 % | 44 |
| 2026-08-14 | 40 | 1.03 % | 37 |
| 2026-08-15 | 49 | 1.27 % | 44 |
| 2026-08-16 | 44 | 1.14 % | 40 |

**The same identifier is almost never indeterminate twice.** Across the 15 day-pairs the overlap is 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 2, 0, 1, 0 identifiers respectively — at most 2. Transport noise is therefore a property of the request, not of the video — which is why `INDETERMINATE` is excluded from rates rather than read as weak absence.

<!-- SESSION-126:PERSISTENCE:BEGIN - generated by session126_sections.py; do not edit by hand -->

## How stable an absence is, across the whole panel

*Added 2026-08-18. Found by the adversary at the gauntlet of 2026-08-17, in this practice's own series file, which had sat in this repository for six days without anyone reading it this way. It is reported because it strengthens the work, and it is reported with the definition problem it arrived with.*

The bundle's headline confirmation evidence is a small one: every apparent state change between two days was immediately re-requested five times, and the record says how many survived. That is 9 events, and the bundle says so. The same series carries a second, independent and much larger form of confirmation, which the bundle never reported: an identifier absent on every one of six daily passes has had that absence re-observed five more times, at 24-hour spacing.

Of the **3,620** non-control identifiers, **446** were ever read as absent on a determinate day. Of those:

| Reading | Count | Share of ever-absent |
|---|---|---|
| Absent on **all six days** (an `INDETERMINATE` day breaks it) | 412 | 92.38 % |
| Absent on **every day it was measured** (`INDETERMINATE` days excluded, as this arc treats them everywhere else) | 439 | 98.43 % |

The gap between the two rows is **27** identifiers whose only non-absent readings are `INDETERMINATE`, plus **7** that genuinely showed both states across the six days. **Both rows are printed because a single number here would be a choice presented as a fact**; the stricter one is the conservative figure and is the one to quote if only one is quoted.

**What this is not.** It is not an immediate re-request, and it is weaker evidence than one. Repeated absence at 24-hour spacing from a single vantage cannot separate a persistent platform state from a persistent network or endpoint condition, and it says nothing at all about identifiers that were never absent. It does not make a single refusal trustworthy — the arc's own confirmation record refutes that, and the version of this bundle which argued it was withheld. What it does say is narrower: **an absence that this instrument reports on six separate days is not, on this panel, usually a flicker.**

<!-- SESSION-126:PERSISTENCE:END -->
