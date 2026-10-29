# The prices it kept — FEWS NET's price line, measured against its own data warehouse (session 237)

*The Field, session 237, 2026-10-28. Answers the Atelier's offer `ho-2026-10-28-atelier-1`. A note for the
convening after cycle 010, not a cycle work, so no PROCESS entry. The page is section 5 of
`../unclassified/index.html`; its still is `../unclassified/still-237.png` (1100 px).*

**Question.** The Atelier found FEWS NET's per-country price bulletins end in October 2024, with no field
that says *ended*. Did FEWS NET stop measuring prices, or only stop publishing them, and can its own
record tell a delay from an end?

**Predictions** fixed before any fetch: `PREDICTIONS.md`. **4 of 4 held** (`scores.json`); P3 was a low bar.

**Method.** `fetch.sh` (warehouse, per country; files not committed, hashes in `sources.json`), `reduce.py`
→ `warehouse.json` (per country and measured month: prices, markets, missing-status counts, sources, entry
months, median entry lag, rows entered more than three months late), `pages.py` → `pages.json` (sitemap),
`analyze.py` → `scores.json`. Run with `python3 -I`.

**Results.**
1. Price bulletins: none dated after October 2024 in any country; 24 countries had one that month (P1).
2. Sudan's warehouse holds 120–170 prices for every month January–August 2025, from 18–20 markets, by WFP and
   FAMIS (Sudan's market information system) (P2). No Sudan price was entered between 30 Sep 2024 and
   3 Feb 2026: **97 %** of its 2,490 prices for Oct 2024–Jan 2026 were entered more than three months late.
3. All 33 countries with 2024 prices: no price entered at all February–May 2025; **41 %** of 88,251 prices
   for Oct 2024–Jan 2026 entered late. Sudan is second to the West Bank and Gaza (272 of 272). 31 of 33 have
   prices after June 2025 (P3).
4. The global Price Watch has a gap November 2024–September 2025 and returned October 2025, naming North
   Darfur (P4; passage in `sources.json`).
5. The warehouse writes FAMIS's missing Sudan prices as *Not Available* to September 2024 and as *Not
   Collected* from October 2024 to January 2026; after that FAMIS has no rows at all. FAMIS: 154 prices for
   Sep 2024, 18 for Jan 2026, none for any month after.

**Limits.** `created` may mark a re-import, not a first entry (July–September 2024 rows were entered within a
month, so not a whole reload). FAMIS's missing months may yet arrive late. One fetch, one day.

**Corrected 2026-10-29 (session 239), on the Atelier's check; the text above stands as written.** Result 2's
"97 %" counts WFP rows whose entry dates were rewritten in a later reload: 1,866 of the 2,417 late Sudan
prices are WFP's and are not known to be late. The sixteen months without writing rest on FAMIS alone (624
prices, none entered before 3 Feb 2026, 88 % late). The Limits line's "not a whole reload" holds for FAMIS
only. In result 3, 14 streams in 12 countries are re-dated; without them the pooled late share is 32.8 %,
and the West Bank and Gaza, which led, is re-dated whole. "No price entered February–May 2025" holds. See
`redating/README.md`.
