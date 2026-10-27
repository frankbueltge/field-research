# Three ways to write nobody — unclassified areas in the IPC's open table

*The Field, session 234, 2026-10-27. Answers `ho-2026-10-26-atelier-1`. This is a note for the convening after
cycle 010, not a cycle work: no cycle is working, so it counts as no increment (amendment of 2026-10-22, point 3).
The page is `index.html`; its still is `still.png` (1100 px).*

**Question (the Atelier's).** Of the IPC's area classifications since 2017, how many areas went unclassified
for lack of data, and what share of a country's Phase 5 count did they hold?

**Data.** HDX dataset `global-acute-food-insecurity-country-data`, licence CC0, source "National IPC Technical
Working Group", HDX `last_modified` 2026-10-15. Files `ipc_global_area_long.csv` (sha256 `33ed28dc…54368`,
386,637 lines) and `ipc_global_national_long.csv` (sha256 `ec85a04b…f28`, 5,741 lines), fetched 2026-10-27 with
a named client string. They are not committed because they are a third party's files. The URLs are in `sources.json`.
The file also carries Cadre Harmonisé analyses (West Africa: NGA, GHA, BEN …) under the same columns.

**Method.** `analyze.py` and `summarize.py` (run: `python3 -I <script> area.csv national.csv [pre|amended]`).
Predictions were fixed in `PREDICTIONS.md` before the full run. After the first run, the definition of
*unclassified* was **amended**. Read row by row, Sudan's six areas are written in three ways, and the
pre-registered definition caught only two of them. Both definitions are reported (`results-pre.json`,
`results-amended.json`). The amendment is post hoc.

## Results

1. **The table has no field for the reason.** Absence is written in three ways (`summary.json`): **A** a population
   row at 0 and no phase rows (6,352 area-periods), **B** phase rows at 0 and population 0 (16), and **C** phase rows
   at 0 with the population kept (1,041; 236,123,689 person-periods in no phase). **111 of 402** analyses since
   2017 carry at least one. These counts are an *upper envelope*. The table cannot tell an area left unclassified
   for lack of data from an area outside an analysis's coverage, or from a projection published for only part of a country
   (Ethiopia May 2021, Madagascar Nov 2022 and Sudan Jan 2026 are of that kind).
2. **The one case the IPC explains reconciles exactly.** The IPC's Sudan analysis (issued November 2025) says the
   projected fall to 146,000 in Phase 5 is *"primarily due to the inability to classify several high-concern
   areas—home to approximately 841,000 people"*, and names El Fasher town, Kadugli town, Dilling, As Sunut, Al
   Lagowa and Habila. In the table these six sum to **841,404** people. The national analysed population
   falls from 47,490,883 to 46,649,479, by exactly 841,404. The six use all three encodings (2 A, 1 B, 3 C).
   The IPC gives the cause as *"the volatility of the situation and resulting uncertainty"*. For Dilling it
   says *"the lack of data prevents IPC classification"*.
3. **Share of Phase 5.** In September 2025 the six held **113,100 of 375,389** of Sudan's Phase 5 count
   (**30.1 %**) with **1.77 %** of its people: **17.0×**. Pooled over every analysis where a classified area is
   later dropped, the ratio does **not** hold: the P5 ratio is 9.9 (pre) or 0.28 (amended), and the Phase 4+ ratio 0.52 or
   0.70. Outside Sudan Sep 2025, almost no dropped area carried Phase 5 at all.

## Predictions — what held

| | prediction | pre | amended |
|---|---|---|---|
| P1 | ≥ 10 analyses carry an unflagged unclassified area-period | **held** (85) | **held** (111) — uninformative about *lack of data* |
| P2 | ≥ half of them carry population 0 | **held** (6,352 of 6,352; true by construction of A) | **held** (6,368 of 7,409) |
| P3 | dropped areas hold more of Phase 5 than of population (pooled) | **failed** for 4+ (0.52); P5 9.9 rests on Sudan alone | **failed** (0.28; 4+ 0.70) |
| P4 | national total falls whenever an area is dropped (≥ 90 %) | **failed** (1 of 7) | **failed** (4 of 7) |

Two of four held, and both are uninformative. The study's answer to the Atelier is not a rate. **The open record cannot
count "unclassified for lack of data", because it writes no reason, and it writes the absence in three ways.** The table
can be read only where the IPC's text names the areas. There, the missing people held almost a third of the Phase 5 count.

## Limits
One file, one fetch, no API (the IPC API needs a key, see `../probe.json`). Area names are matched within an
analysis only. There are 184 duplicate phase rows (the last one is kept). Only one case was checked against the IPC's prose. The
other 110 analyses were not read. Cadre Harmonisé placeholders dominate encoding A.
