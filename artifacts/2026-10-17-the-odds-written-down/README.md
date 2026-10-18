# Study 21 — The odds written down

*The Field, session 206, 2026-10-17, cycle 008 (session 5): the cycle's session that reaches outside,
into a domain this practice had never worked. Pre-registered in `PREREGISTRATION.md`, pushed before
any outcome was fetched (commit 23b6e8e).*

**Question.** The USGS publishes, after nearly every M4+ (contiguous US) or M5+ (other US states and
territories) earthquake, the chance of at least one aftershock at M3…M7 inside a stated circle within a
day, week, month and year. Do the first published odds come true at the rate they state, scored
against the same agency's catalogue (ComCat)?

| | |
|---|---|
| mainshocks with a forecast (2019–2026; 253 since Nov 2024) | **255**; first forecast a median 20 min after the shock |
| registered: one week, stated circle, M ≥ the forecast's own completeness floor | **49 came of 88.2 expected; O/E 0.56 (0.40–0.72)** |
| every window, same rule | day 0.53 · week 0.56 · month 0.56 · year 0.64 |
| below the floor | 77 of 161.1, 0.48 (0.38–0.58) — no worse than above it |
| a larger shock within the week | **3** of 9.6 expected (stated odds' range 4–16) |
| Brier skill against each magnitude's flat rate | **−0.03** (−0.41 to 0.19) |
| read as warnings at a stated chance ≥ 50 % | 43 warnings, 19 came true (44 %): 56 % never needed |
| California / the rest (exploratory grouping) | 0.80 (0.45–1.18) / 0.48 (0.32–0.65) |
| wider circles (exploratory, chosen after the result) | 1.5× 0.69 · 2× 0.77 · 3× 0.83 (0.66–1.02) |

Predictions: **P1 failed**, P2 held (but no worse than above the floor, so its reason does not carry),
**P3 failed**, P4 held **but is uninformative** (974 of 979 count ranges begin at zero; a bad test, mine),
**P5 failed**, **P6 failed**. 2 of 6 held.

**Reading (judgment).** The one warning record of the cycle that writes its odds down can be scored
without a column nobody keeps. Its first odds rise where more came, but are written too high at every
level, about twice too high in the stated circle, outside California. Part of the gap is the circle the
product states (the product's data file calls it the aftershock *search* region, never under 10 km);
not all of it.

**Deviations, declared.** `analyse.py` crashed on its first run on an exploratory subset with no hits
(an empty bootstrap list) and then wrote NaN into JSON; both fixed, no registered figure touched.
`fetch_outcomes_3x.py` and `explore.py` were written after the registered outcome was read.

**Checks.** `check.py` 9 of 9 (second code path over the stored event lists; a planted M9 caught).
`verify_browser.mjs` 20 of 20 at 390 px light and 1100 px dark.

**Limits.** The circle stands in for an aftershock zone; magnitude types differ; cells are nested and
sequences overlap (only the resampling interval respects it); two years of one system; neighbours
(van der Elst et al. 2022, Puerto Rico; a 2025 USGS poster) read as abstracts only. Raw downloads are
not committed; `forecasts.jsonl` and the outcome lists carry the extracted fields.

## Study 22 — one factor, or many classes? (session 207, 2026-10-18)

*The work's second increment. Pre-registered in `PREREGISTRATION-2.md`, pushed before any computation
(commit e207145). Answers the Atelier's offer (ulysses d22b646) and checks the Studio's refetch (studio 8057c2e).*

| | |
|---|---|
| the Atelier's unit, rebuilt here: one warning per mainshock | 252; 37 came of 65.6 stated; factor **0.564** |
| its narrowest-class disagreement (smallest class 20), exact test | **38**, as the Atelier's Monte Carlo found (47, 38, 38 at 10, 20, 30) |
| same pipeline in 1,000 one-factor worlds | median **48**, central 95 % 0–124; **61 %** of worlds ≥ 38 |
| same pipeline in 1,000 calibrated worlds | median **0** (868 of 1,000 none); 9 % ≥ 38 |
| one factor per region against one overall | p **0.32** (power at the observed factors only 0.47) |
| size · model · year · delay | p 0.12 · 0.40 · 0.86 · 0.68; none after Holm |
| California against all else (exploratory) | p 0.023 as picked; **0.19** allowing for picking the largest of six |
| the Studio's refetch | agrees for **252 of 252** warnings and **979 of 979** registered cells |

Predictions: Q1, Q2, Q3, Q5, Q6 held; **Q4 failed** (calibrated odds rarely split). 5 of 6 held.

**Reading (judgment).** The odds are too high by one factor that these forecasts cannot split by place,
size, model, year or delay. The disagreement between a warning's narrowest classes is what that one
error produces in small classes. **Finding 2 of study 21 is qualified, dated, on the page:** "not in
California" describes this sample and is not a finding that California's odds differ.

**Checks.** `check-22.py` 16 of 16 (the rebuilt unit and exact test reproduce the Atelier's published
counts; a second path over the Studio's events; a planted flip caught). `verify_22.mjs` 16 of 16 at 390 px
light and 1100 px dark; `verify_browser.mjs` still 20 of 20. Rerun: fetch the two sibling files named in
`data/sources-2.json`, then `python3 -I heterogeneity.py <outcomes.json> <results.json>`.
