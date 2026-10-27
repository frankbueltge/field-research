# Predictions — fixed before the full analysis (session 234, 2026-10-27)

Question (ho-2026-10-26-atelier-1): of the IPC's area classifications since 2017, how many areas went
unclassified for lack of data, and what share of a country's Phase 5 count did they hold?

Data: HDX `global-acute-food-insecurity-country-data` (CC0), `ipc_global_area_long.csv` and
`ipc_global_national_long.csv`, fetched 2026-10-27, HDX last_modified 2026-10-15.

Seen before these were written (exploration, NOT a prediction): in Sudan's analysis of Sep 2025,
the second projection lists Al Fasher Urban and Kadugli Urban with population 0 and no phase, and the
national analysed population falls from 47,490,883 (current) to 46,649,479 (second projection).

Operational definition. An area-period is *unclassified* when it carries an `all` row but no phase
rows. An area is *dropped* when it is classified in an analysis's current period and unclassified or
absent in one of its projections.

- **P1.** Unclassified area-periods are not flagged; they appear as absence. At least 10 distinct
  analyses (date × country) since 2017 carry at least one.
- **P2.** At least half of the unclassified area-periods carry population 0 (the area leaves the sum
  rather than standing in it with its people).
- **P3.** Dropped areas hold a larger share of their country's current Phase 5 count than of its
  current analysed population (pooled ratio > 1): data go missing where famine is worst.
- **P4.** The national `all` row of a projection is lower than the current period's whenever an area
  is dropped, i.e. the national table carries no remainder for the unclassified (≥ 90 % of cases).
