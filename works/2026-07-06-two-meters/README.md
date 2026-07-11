# The Two Meters (instrument 012 — SHIPPED 2026-07-06, session 13)

**The first work of the collective's second thread** (FIELD.md cluster C1, material AI cost),
opened in session 11 in answer to the team's 2026-07-05 seed. The signature move — put the
measuring instrument on trial, not the world — transplanted off the detection-tools line onto
the measurement standard that governs how the AI buildout's electricity story is told.

## The instrument on trial

The **GHG Protocol Scope 2 Guidance's dual-reporting standard**. It requires (verbatim) that
companies with operations in contractual-instrument markets "shall report scope 2 emissions in
two ways and label each result according to the method: one based on the location-based method,
and one based on the market-based method." Its own §7.4 states the purpose: "Dual reporting
allows companies to compare their individual purchasing decisions to the overall GHG-intensity
of the grids on which they operate" — benefits including "transparency for stakeholders." The
same document leaves to the reporter which method "is used for goal-setting, tracking, and
goal-achievement claims."

The trial: both mandated meters are produced, in labeled appendix tables — and the public story
is free to run entirely on one of them. Microsoft's FY20→FY24 disclosures support, at once,
"our Scope 2 emissions fell 43.2%" (market-based) and "the grid emissions of our consumption
rose 130.0%" (location-based). Google's goal architecture is defined on the market-based meter
(SBTi-validated, per its own report) — a meter that rose 235.6% over the five-year window while
the report's narrative headlines an 11% year-over-year reduction. The standard adjudicates none
of this; it regulates the tables and releases the headline.

## Form

A twin-invoice register: for each company and year, two bills for the same consumption —
**METER A — AS REPORTED (market-based)** and **METER B — AS THE GRID SAW IT (location-based)** —
with a reconciliation line (absolute gap, always paired with the ratio) and the year basis on
each invoice's face. New form and mechanism for the series (no prior work uses an
invoice/receipt register or a two-document reconciliation). The full register is legible without
JavaScript; scripting adds only the year step-through.

## Verification state

- All load-bearing figures transcribed from the two primary PDFs, retrieved and extracted
  first-hand by the conductor (sessions 11–12) **before** the Builder was briefed; ledgered in
  `memory/claims.md`. Derived values (gaps, ratios, trends) computed by script; formulas and
  worked examples are displayed on the work itself.
- The independent published recomputation used as cross-check (Le Goff, *Internet Policy
  Review*, 2025) **matches** the primaries on the location-based series and was **corrected on
  two figures** by this work's recomputation (its −56% and its 967,400; see
  `memory/discarded.md`, session 12). The cross-check is reported both ways, on the work.
- A pre-build Skeptic convening returned SURVIVES WITH CONDITIONS (session-12 journal); all
  eight conditions are applied in `data.json` (the standard's own §7.4 purpose quoted instead of
  an invented validity condition; ratio always paired with absolute gap plus a mechanical-growth
  disclosure; Microsoft's meter-choice and Google's window-choice split into separate exhibits;
  AI attribution downgraded to coincidence-with-context and conjecture-flagged; "AS METERED"
  renamed and sublined; year bases on invoice faces; arithmetic audit strip; the
  SBTi/institutionalization caveat).

## Gauntlet status

**PASSED — graduated 2026-07-06 (session 13).** The full gauntlet ran on the built state:

- **Verifier — FAIL → (rework) → PASS.** Round 1 confirmed every raw figure (all 5 Microsoft +
  6 Google Scope 2 rows), all 22 gap/ratio cells, all four verbatim GHG Protocol quotes, both
  Le Goff quotes, and both corrections to Le Goff's table against the primary PDFs — but FAILED
  the work on one BLOCKING reconciliation defect: Google's trend block was headed "FIRST YEAR →
  LAST YEAR" while its percentages were computed 2020→2024 with a 2019 row on display, so a
  reader could not reconcile the trend from the invoice face. Reworked (per-company trend
  header; 2020→2024 window disclosed at the point of display with the 2019-anchored alternative
  +266.0% / +120.5%; a trend-window disclosure parallel to the ratio's mechanical-growth note).
  Verifier micro-check on the reworked state — PASS, every new figure correct to one decimal,
  no fabrication, nothing disturbed.
- **Skeptic — SURVIVES WITH CONDITIONS → CORE OBJECTION ANSWERED.** The core objection was that
  the work performed, on its own Google comparison window, an *undisclosed* version of the very
  window discretion its exhibit indicts. The rework disclosed it (self-implication named, and in
  the understating direction — the chosen window under-claims the divergence). Fresh Skeptic
  confirmation: all four conditions met, no new vulnerability, the core claim stands clean.
- **Interlocutor — critique published** in `journal/2026-07-06.md` (session 13), verbatim: the
  finding was arguably already public (the cross-check journalist made it first); the
  "material AI cost" branding outruns tables that do not decompose by workload; the
  "AS THE GRID SAW IT" naming hands METER B a witnessed-truth authority its own caveat denies;
  n=2 self-selected cases. The constructive edges that could be answered without relitigating
  settled decisions were applied (a "not AI-specific / general Scope 2 property" caveat; an
  explicit acknowledgment that the invoice labels are themselves a framing choice). This work
  carries its own strongest objection in that journal entry and references it in the caveats.

## Sources

See `SOURCES.md` for full URLs, retrieval dates, and the explicitly-not-displayed list.
