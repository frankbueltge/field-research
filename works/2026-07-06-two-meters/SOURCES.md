# Sources — The Two Meters

All load-bearing figures were retrieved and extracted first-hand by the conductor (sessions 11
and 12, dates 2026-07-05 / 2026-07-06) before any Builder was briefed. Ledger rows:
`memory/claims.md` (Microsoft row, session 11 corrected session 12; Google row, session 12;
GHG Protocol Scope 2 Guidance row, session 12).

## Primary sources (the disclosed tables themselves)

1. **Microsoft 2025 Environmental Data Fact Sheet** (PDF)
   https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2025-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf
   — Table 1A "GHG emissions by scope" (Scope 2 location-based and market-based rows, FY20–FY24);
   the identical subtotals also appear in Table 3 "GHG emissions by region".
   Extracted 2026-07-05 (endpoints) and 2026-07-06 (full five-year series).

2. **Google 2025 Environmental Report** (PDF)
   https://www.gstatic.com/gumdrop/sustainability/google-2025-environmental-report.pdf
   — Appendix, "Environmental metrics data tables → Greenhouse gas emissions inventory"
   (Scope 2 location-based and market-based rows, 2019–2024; "Total operational" row), plus the
   narrative Scope 2 paragraph quoted on the work ("approximately 3.1 million tCO2e, representing
   26% of our total 2024 ambition-based carbon footprint"). Internal cross-check: the 2024 global
   totals (3,059,100 market / 11,283,200 location) are consistent across the inventory table, the
   by-region table, and the by-gas table in the same PDF. Also extracted (second pass,
   2026-07-06): the goal-anchor passage — "We aim to reduce absolute, combined scope 1, 2
   (market-based), and 3 emissions by 50% from a 2019 base year by 2030" — and the report's
   statement that "In February 2025, the SBTi (Science Based Targets initiative) validated
   Alphabet's near-term science-based emissions reduction ambition"; base year 2019 chosen
   because 2020 operations were pandemic-affected (report's own explanation). Extracted 2026-07-06.

3. **GHG Protocol Scope 2 Guidance** (PDF; the instrument on trial)
   https://ghgprotocol.org/sites/default/files/2023-03/Scope%202%20Guidance.pdf
   — The dual-reporting requirement, verbatim: "Companies with any operations in markets providing
   product or supplier-specific data in the form of contractual instruments shall report scope 2
   emissions in two ways and label each result according to the method: one based on the
   location-based method, and one based on the market-based method. This is also termed 'dual
   reporting.'" And the display discretion, verbatim: "Companies shall specify which method is
   used for goal-setting, tracking, and goal-achievement claims, and for scope 3 or product-level
   communication." And the standard's own stated purpose (section 7.4 "Dual reporting"), verbatim:
   "Dual reporting allows companies to compare their individual purchasing decisions to the
   overall GHG-intensity of the grids on which they operate", with listed benefits including
   "Distinguishes changes in choices vs. changes in grid emissions intensity" and "Provides
   transparency for stakeholders". Extracted 2026-07-06 (two passes: requirements; rationale).

## Independent published recomputation (cross-check)

4. **Le Goff, "Not greenwashing, but still… A closer look at big tech's 2025 sustainability
   reports", *Internet Policy Review*, 7 Aug 2025**
   https://policyreview.info/articles/news/big-techs-2025-sustainability-reports/2027
   — Independent framing and recomputation ("around 25.2 million metric tons CO₂, not the 15.5
   million they report"; "the rules allow them to tell only part of the story"). The collective's
   recomputation from the primaries **matches** this source's location-based rows exactly and
   **corrects two of its figures** (Microsoft market-based change is −43.2%, not −56%; Google's
   2020 market-based value is 911,600, not 967,400 — the latter is Google's 2020 total
   operational figure). Both corrections are ledgered in `memory/discarded.md` (session 12) and
   disclosed on the work.

## Derived values

Gaps (location − market), ratios (location / market, one decimal), and first-to-last trends
(last/first − 1) computed by script from the transcribed primary values, 2026-07-06; the
computation is deterministic arithmetic with no free parameters. Recomputation command recorded
in the session-12 journal.

## Independent verification (2026-07-06)

All 22 raw meter values and every verbatim quote above were re-checked automatically against the
primary PDFs (text extracted with `pdftotext`, each figure/quote searched): **every one matched**,
and every derived value recomputes exactly. Full record, incl. the PDFs' SHA-256 hashes and the
reproducible method: `VERIFICATION.md`.

## Explicitly NOT displayed (unverified or out of scope)

- Le Goff's Scope-3-inclusive totals for Google (23.4M vs 15.2M) — attributed to the source in
  the ledger, but the work displays only Scope 2, so these do not appear on the invoices.
- Any decomposition of Scope 2 by workload (AI vs other) — not disclosed by either company;
  the AI-attribution sentence on the work is flagged as context/conjecture accordingly.
- Meta/Amazon or any other reporter — out of scope for v1.
