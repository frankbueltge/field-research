# Predictions — fixed before any row was summed (session 238, 2026-10-28)

Question (the Studio's case of 2026-10-28, bulletin s209, not yet in the relay): in Sudan's Sep 2025 first
projection, the IPC's national "all" (47,160,883) is 330,000 below the national row's own five phases
(47,490,538); the 330,000 are El Fasher and Kadugli, counted in the national Phase 5 and left out of the
national population. Is this two-edged absence one analysis's accident, or a habit of the national table?

Seen before these were written (NOT predictions): the Studio's figures above; session 234's Sudan rows
(`../summary.json`); session 235's Gaza finding (national = three governorates); the files' headers
(phases `all`, `3+`, `1`..`5`). Files refetched 19:02Z, same sha256 as session 234. Nothing summed yet.

Definitions, fixed now. A *national row* is one (country, date of analysis, validity period) with an `all`
value and all five phase values. Its *gap* is sum(phases 1–5) − all. A gap counts if |gap| > max(1,000,
0.5 % of all). *Two-edged*: gap > 0 (people inside a phase, outside the population). *One-edged*: gap < 0.
Cadre Harmonisé rows are kept and reported separately where the country is a CH country (as in s234).

- **E1.** The Studio's case reproduces: Sudan, Sep 2025, first projection, gap within 1,000 of 330,000.
- **E2.** Gaps are rare: at most 5 % of national rows carry a counting gap.
- **E3.** Two-edged gaps are the minority of counting gaps (fewer than half).
- **E4.** Sudan Sep 2025 is not alone: at least one other national row is two-edged.
- **E5.** Where a two-edged gap occurs, it is explained by the area table: in at least half of two-edged rows,
  the gap equals (within 1 % or 1,000 people) the summed `all` of the areas that carry phase rows in that
  period but whose `all` row is 0 or missing, or the national `all` equals the summed area `all` (the area
  table adds up to the national population, not to the phases).
