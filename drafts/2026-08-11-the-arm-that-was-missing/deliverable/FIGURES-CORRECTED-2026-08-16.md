# Figures — generated, do not hand-edit

*Written by `build_deliverable.py` at 2026-08-16T00:42:26Z. Every number on this page comes from `expectation.json` and `series/presence-series.json`, which come from the run files named in `MANIFEST.json`. Rebuild the bundle and this page rebuilds with it.*

## 1. The panel, and what was measured each day

| day | measurement started (UTC) | units requested | in the rate | publicly absent | absent rate | 95 % Wilson |
|---|---|---|---|---|---|---|
| baseline | 2026-08-11T11:24:06Z | 3869 | 3581 | 437 | 12.20 % | [11.17 %, 13.32 %] |
| 2026-08-12 | 2026-08-12T03:40:28Z | 3869 | 3582 | 437 | 12.20 % | [11.17 %, 13.31 %] |
| 2026-08-13 | 2026-08-13T04:27:00Z | 3869 | 3576 | 439 | 12.28 % | [11.24 %, 13.39 %] |
| 2026-08-14 | 2026-08-14T03:43:47Z | 3869 | 3583 | 435 | 12.14 % | [11.11 %, 13.25 %] |

**Across 4 measured days the pooled public-absence rate of this panel moves between 12.14 % and 12.28 % — a spread of 0.14 percentage points.** This is the same panel measured again, so it is the instrument's test-retest reproducibility and not sampling error (`LIMITS.md` §5).

## 2. Public absence by the age of the video — newest day

*Day: 2026-08-14. Ages are decoded from the identifier (`LIMITS.md` §6).*

| age band | in the rate | publicly absent | absent rate | 95 % Wilson | spread across all measured days |
|---|---|---|---|---|---|
| 0-1y | 499 | 24 | 4.81 % | [3.25 %, 7.06 %] | 0.25 pp |
| 1-2y | 766 | 59 | 7.70 % | [6.02 %, 9.81 %] | 0.26 pp |
| 2-3y | 793 | 96 | 12.11 % | [10.02 %, 14.56 %] | 0.31 pp |
| 3-4y | 673 | 109 | 16.20 % | [13.61 %, 19.17 %] | 0.25 pp |
| 4-5y | 457 | 74 | 16.19 % | [13.10 %, 19.85 %] | 0.33 pp |
| 5y+ | 388 | 68 | 17.53 % | [14.07 %, 21.62 %] | 0.54 pp |

## 3. The same gradient inside each source stratum

*If the gradient were an artefact of which source the older identifiers come from, it would not survive this split.*

| age band | F-forum | W-article | W-other-ns |
|---|---|---|---|
| 0-1y | 4.00 % (n=50) | 5.21 % (n=307) | 4.23 % (n=142) |
| 1-2y | 15.38 % (n=52) | 6.17 % (n=535) | 10.06 % (n=179) |
| 2-3y | 13.68 % (n=95) | 9.44 % (n=519) | 18.99 % (n=179) |
| 3-4y | 18.80 % (n=117) | 15.07 % (n=438) | 17.80 % (n=118) |
| 4-5y | 14.47 % (n=76) | 14.80 % (n=304) | 23.38 % (n=77) |
| 5y+ | 14.29 % (n=56) | 17.54 % (n=268) | 20.31 % (n=64) |

**The gradient's own test — 0-1y against 5y+ on 2026-08-14, two-sided Fisher exact.** The pooled progression is not strictly monotone: it rises across the bands with one flat step near four years, and the endpoints are what is tested here.

| group | 0-1y | 5y+ | ratio | Fisher two-sided p |
|---|---|---|---|---|
| pooled | 24/499 (4.81 %) | 68/388 (17.53 %) | 3.64 × | 7.656e-10 |
| F-forum | 2/50 (4.00 %) | 8/56 (14.29 %) | 3.57 × | 9.832e-02 |
| W-article | 16/307 (5.21 %) | 47/268 (17.54 %) | 3.36 × | 3.216e-06 |
| W-other-ns | 6/142 (4.23 %) | 13/64 (20.31 %) | 4.81 × | 4.942e-04 |

## 4. Where the identifiers come from — newest day

| stratum | what it is | in the rate | publicly absent | absent rate |
|---|---|---|---|---|
| `F-forum` | public comments and stories of one technology forum | 446 | 64 | 14.35 % |
| `W-article` | article space of 21 encyclopedia language editions | 2375 | 259 | 10.91 % |
| `W-other-ns` | non-article namespaces of the same editions | 762 | 112 | 14.70 % |

**Excluded from every rate on the newest day:** 249 identifiers of the `B-truncated` control arm, which are display-truncated strings and not videos; 37 observations that ended in a transport failure or an unexpected status (`INDETERMINATE`); and 7 identifiers that carry no decodable creation time and are therefore absent from the age-banded tables only.

## 5. How much this panel moves at all

Over 4 measured days, **5 of 3620** non-control identifiers show more than one determinate state in the raw record, and **3** do so after the refuted-reading overlay is applied. The identifiers are listed so the claim can be checked:

| video id | arm | baseline | 2026-08-12 | 2026-08-13 | 2026-08-14 | changes after overlay |
|---|---|---|---|---|---|---|
| `7016669364938149122` | A | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | NOT-RETRIEVABLE | no — refuted reading, see overlay |
| `7298893164335729926` | A | NOT-RETRIEVABLE | NOT-RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | yes |
| `7446448990935354670` | A | NOT-RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | RETRIEVABLE | yes |
| `7266499914014723370` | A2 | NOT-RETRIEVABLE | NOT-RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | yes |
| `7368171405361351954` | A2 | RETRIEVABLE | RETRIEVABLE | NOT-RETRIEVABLE | RETRIEVABLE | no — refuted reading, see overlay |

## 6. Transport noise

| day | INDETERMINATE | share of the run |
|---|---|---|
| baseline | 42 | 1.09 % |
| 2026-08-12 | 40 | 1.03 % |
| 2026-08-13 | 47 | 1.21 % |
| 2026-08-14 | 40 | 1.03 % |

**The same identifier is almost never indeterminate twice.** Across the 6 day-pairs the overlap is 0, 1, 0, 0, 1, 1 identifiers respectively. Transport noise is therefore a property of the request, not of the video — which is why `INDETERMINATE` is excluded from rates rather than read as weak absence.

