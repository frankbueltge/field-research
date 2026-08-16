# Figures — generated, do not hand-edit

*Written by `build_deliverable.py` at 2026-08-16T03:54:02Z. Every number on this page comes from `expectation.json` and `series/presence-series.json`, which come from the run files named in `MANIFEST.json`. Rebuild the bundle and this page rebuilds with it.*

## 1. The panel, and what was measured each day

| day | measurement started (UTC) | units requested | in the rate | publicly absent | absent rate | 95 % Wilson |
|---|---|---|---|---|---|---|
| baseline | 2026-08-11T11:24:06Z | 3869 | 3581 | 437 | 12.20 % | [11.17 %, 13.32 %] |
| 2026-08-12 | 2026-08-12T03:40:28Z | 3869 | 3582 | 437 | 12.20 % | [11.17 %, 13.31 %] |
| 2026-08-13 | 2026-08-13T04:27:00Z | 3869 | 3576 | 439 | 12.28 % | [11.24 %, 13.39 %] |
| 2026-08-14 | 2026-08-14T03:43:47Z | 3869 | 3583 | 435 | 12.14 % | [11.11 %, 13.25 %] |
| 2026-08-15 | 2026-08-15T03:37:40Z | 3869 | 3576 | 438 | 12.25 % | [11.21 %, 13.36 %] |

**Across 5 measured days the pooled public-absence rate of this panel moves between 12.14 % and 12.28 % — a spread of 0.14 percentage points.** This is the same panel measured again, so it is the instrument's test-retest reproducibility and not sampling error (`LIMITS.md` §5).

## 2. Public absence by the age of the video — newest day

*Day: 2026-08-15. Ages are decoded from the identifier (`LIMITS.md` §6).*

| age band | in the rate | publicly absent | absent rate | 95 % Wilson | spread across all measured days |
|---|---|---|---|---|---|
| 0-1y | 493 | 23 | 4.67 % | [3.13 %, 6.90 %] | 0.25 pp |
| 1-2y | 773 | 60 | 7.76 % | [6.08 %, 9.86 %] | 0.26 pp |
| 2-3y | 787 | 94 | 11.94 % | [9.86 %, 14.40 %] | 0.48 pp |
| 3-4y | 672 | 111 | 16.52 % | [13.90 %, 19.51 %] | 0.57 pp |
| 4-5y | 457 | 76 | 16.63 % | [13.50 %, 20.32 %] | 0.44 pp |
| 5y+ | 387 | 69 | 17.83 % | [14.34 %, 21.95 %] | 0.54 pp |

## 3. The same gradient inside each source stratum

*If the gradient were an artefact of which source the older identifiers come from, it would not survive this split.*

| age band | F-forum | W-article | W-other-ns |
|---|---|---|---|
| 0-1y | 4.00 % (n=50) | 4.95 % (n=303) | 4.29 % (n=140) |
| 1-2y | 15.38 % (n=52) | 6.12 % (n=539) | 10.44 % (n=182) |
| 2-3y | 13.68 % (n=95) | 9.34 % (n=514) | 18.54 % (n=178) |
| 3-4y | 19.49 % (n=118) | 15.23 % (n=440) | 18.42 % (n=114) |
| 4-5y | 15.58 % (n=77) | 15.13 % (n=304) | 23.68 % (n=76) |
| 5y+ | 14.29 % (n=56) | 17.60 % (n=267) | 21.88 % (n=64) |

**The gradient's own test — 0-1y against 5y+ on 2026-08-15, two-sided Fisher exact.** The pooled progression is not strictly monotone: it rises across the bands with one flat step near four years, and the endpoints are what is tested here.

| group | 0-1y | 5y+ | ratio | Fisher two-sided p |
|---|---|---|---|---|
| pooled | 23/493 (4.67 %) | 69/387 (17.83 %) | 3.82 × | 3.083e-10 |
| F-forum | 2/50 (4.00 %) | 8/56 (14.29 %) | 3.57 × | 9.832e-02 |
| W-article | 15/303 (4.95 %) | 47/267 (17.60 %) | 3.56 × | 1.358e-06 |
| W-other-ns | 6/140 (4.29 %) | 14/64 (21.88 %) | 5.10 × | 2.141e-04 |

## 4. Where the identifiers come from — newest day

| stratum | what it is | in the rate | publicly absent | absent rate |
|---|---|---|---|---|
| `F-forum` | public comments and stories of one technology forum | 448 | 66 | 14.73 % |
| `W-article` | article space of 21 encyclopedia language editions | 2371 | 259 | 10.92 % |
| `W-other-ns` | non-article namespaces of the same editions | 757 | 113 | 14.93 % |

**Excluded from every rate on the newest day:** 249 identifiers of the `B-truncated` control arm, which are display-truncated strings and not videos; 44 observations that ended in a transport failure or an unexpected status (`INDETERMINATE`); and 7 identifiers that carry no decodable creation time and are therefore absent from the age-banded tables only.

## 5. How much this panel moves at all

Over 5 measured days, **6 of 3620** non-control identifiers show more than one determinate state in the raw record, and **4** do so after the refuted-reading overlay is applied. The identifiers are listed so the claim can be checked:

| video id | arm | baseline | 2026-08-12 | 2026-08-13 | 2026-08-14 | 2026-08-15 | changes after overlay |
|---|---|---|---|---|---|---|---|
| `7016669364938149122` | A | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | no — refuted reading, see overlay |
| `7234106298021727515` | A | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | NOT-RETRIEVABLE | yes |
| `7298893164335729926` | A | NOT-RETRIEVABLE | NOT-RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | yes |
| `7446448990935354670` | A | NOT-RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | yes |
| `7266499914014723370` | A2 | NOT-RETRIEVABLE | NOT-RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | yes |
| `7368171405361351954` | A2 | RETRIEVABLE | RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | no — refuted reading, see overlay |

## 6. Transport noise

| day | INDETERMINATE | share of the run |
|---|---|---|
| baseline | 42 | 1.09 % |
| 2026-08-12 | 40 | 1.03 % |
| 2026-08-13 | 47 | 1.21 % |
| 2026-08-14 | 40 | 1.03 % |
| 2026-08-15 | 49 | 1.27 % |

**The same identifier is almost never indeterminate twice.** Across the 10 day-pairs the overlap is 0, 1, 0, 1, 0, 1, 1, 1, 0, 0 identifiers respectively. Transport noise is therefore a property of the request, not of the video — which is why `INDETERMINATE` is excluded from rates rather than read as weak absence.

