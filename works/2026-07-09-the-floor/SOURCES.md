# Sources — "The Floor"

All fetched 2026-07-09 via web research (server-side full-text extraction; the sandbox has no
direct egress to the primary hosts). Every load-bearing figure was read first-hand from the
primary before the Builder was briefed. Verbatim quotes are marked as such.

## Primary — Google environmental reports (the subject's own disclosures)

**Google 2025 Environmental Report** — fiscal year 2024, published June 2025.
- Official landing: https://sustainability.google/reports/google-2025-environmental-report
- Full-text extracted from PDF mirror: https://www.smartenergydecisions.com/wp-content/uploads/2025/07/google-2025-environmental-report-1.pdf
- Verbatim (Figure 4 framing — the claim under trial): "For the first time in six years, the
  average annual power usage effectiveness (PUE) for our global fleet of data centers dropped
  below 1.10 to 1.09 (Figure 4). While a PUE improvement of 0.01 might appear small, at the scale
  of our global data center operations, this efficiency gain avoids significant electricity
  consumption. This means our global computing network requires less electricity and produces
  fewer emissions than it otherwise would have, yielding meaningful savings even as our overall
  computing demands grow."
- Verbatim (growth; mid-sentence excerpt, elision marked): "…our total data center electricity
  consumption grew by 27% in 2024, compared to 17% growth in the prior year."
- Verbatim (scope 2): "In 2024, our scope 2 (market-based) emissions were approximately 3.1
  million tCO2e, about 95% of which resulted from the electricity needed to power our data centers
  and offices."
- Verbatim (industry compare): "In 2024, the average annual PUE for our global fleet of data
  centers was 1.09, compared with the industry average of 1.56, meaning that Google data centers
  used 84% less overhead energy than the industry average."
- Verbatim (bridge graphic legend / totals): "In 2024, our total ambition-based emissions were
  11.5 million tCO2e, representing a 51% increase compared to 2019. • Operations: Combined scope 1
  and scope 2 (market-based) emissions were 3.1 million tCO2e, representing a 241% increase
  compared to 2019. • Supply chain: Scope 3 (ambition-based) emissions were 8.4 million tCO2e,
  representing a 25% increase compared to 2019." The carbon-reduction-progress graphic's legend
  lists the reduction wedges: "PUE improvements", "Clean energy procurement", "Machine hardware
  efficiencies", "Avoided emissions".
- GHG emissions inventory data table (tCO2e), years 2019 / 2020 / 2021 / 2022 / 2023 / 2024:
  - Scope 1: 81,900 / 55,800 / 64,100 / 91,200 / 79,400 / 73,100
  - Scope 2 (location-based): 5,116,900 / 5,865,100 / 6,576,200 / 8,045,400 / 9,252,900 / 11,283,200
  - Scope 2 (market-based): 835,900 / 911,600 / 1,823,500 / 2,492,100 / 3,423,400 / 3,059,100
  - Total operational (scope 1 + market-based scope 2): 917,800 / 967,400 / 1,887,600 / 2,583,300 / 3,502,800 / 3,132,200
- Highlights (same report, "2024 highlights" section; verbatim, re-verified session 17): "We
  reduced our data center energy emissions by 12%, compared to 2023. We achieved this important
  accomplishment despite a 27% increase in our electricity consumption…" And on TPU efficiency:
  "Ironwood is nearly 30 times more power efficient than our first Cloud TPU from 2018."
  *(Correction, session-17 gauntlet: an earlier version of this file rendered the 12% highlight as
  "In 2024, we reduced our data center energy emissions by 12%, even in the face of increased
  energy demands." — a paraphrase dressed as a quotation; the wording does not appear in the
  primary. It also labeled the 30x comparison "vs the earliest-generation Cloud TPU v2" — the
  "v2" identification was the collective's inference, not the report's wording. Both corrected;
  ledgered in memory/discarded.md.)*

**Google 2024 Environmental Report** — fiscal year 2023, published 2024.
- Full-text extracted from PDF mirror: https://www.smartenergydecisions.com/wp-content/uploads/2025/04/google-2024-environmental-report.pdf
- Data table "DATA CENTER ENERGY EFFICIENCY (PUE)": row "Average annual fleet-wide PUE across
  Google-owned and -operated data center campuses" reads 1.10 / 1.10 / 1.10 / 1.10 / 1.10 for
  2019–2023 (all five years). Per-site PUE table also present (e.g., Belgium St. Ghislain 1.08–1.09;
  Singapore 2nd facility 1.19–1.21).
- Verbatim: "In 2023, the average annual power usage effectiveness (PUE) for our global fleet of
  data centers was 1.10 ... compared with the industry average of 1.58 ... meaning that Google
  data centers used about 5.8 times less overhead energy for every unit of IT equipment energy."

## Primary / authoritative — the metric itself

**PUE definition & floor** — Vertiv, Nlyte, Stulz, and the ISO/IEC 30134-2:2016 standard as
summarised on Wikipedia (https://en.wikipedia.org/wiki/Power_usage_effectiveness): PUE = total
facility energy / IT-equipment energy; developed by The Green Grid (2006–2007); published as
ISO/IEC 30134-2:2016. Floor of 1.0: Sunbird eBook
(https://www.sunbirddcim.com/sites/default/files/EB035_Sunbird_eBook_PUE_0.pdf): "A PUE of 1.0
indicates a perfectly efficient data center in which all of the energy coming into the facility is
used by IT equipment and none of it is lost through the power chain or spent on cooling."

**"PUE Abuse" / marketing misuse** — Wikipedia (as above): "There is also some concern within the
industry of PUE as a marketing tool leading some to use the term 'PUE Abuse'." Sunbird eBook:
"'PUE abuse,' involves selectively reporting PUE values or manipulating data to create a favorable
impression of energy efficiency, potentially misleading stakeholders and consumers."

**The Green Grid's own examination** — "PUE™: A Comprehensive Examination of the Metric" (The
Green Grid / ASHRAE), LBNL mirror:
https://datacenters.lbl.gov/sites/default/files/WP49-PUE%20A%20Comprehensive%20Examination%20of%20the%20Metric_v6.pdf
— "a metric best used as a tool for management, rather than for making [comparisons]"; misuse of
partial calculations "for marketing reasons"; pPUE introduced to curb misuse.

**PUE's blind spots / near-floor** — REHVA Journal, "Analysis of performance metrics for data
center efficiency" (https://www.rehva.eu/rehva-journal/chapter/analysis-of-performance-metrics-for-data-center-efficiency-should-the-power-utilization-effectiveness-pue-still-be-used-as-the-main-indicator-part-1):
PUE disregards IT-equipment efficiency ("Maybe the most important issue"); its excluded subjects
include "on-site renewable energy generation … and carbon footprint" (verbatim list). The gloss
"renewable treated identically to coal" is **our reading** of the formula's source-blindness (the
ratio contains no carbon term), not REHVA's wording. For state-of-the-art facilities PUE is
"close to values of 1.1 now ... further improvement within the boundaries PUE provides is
difficult."

**Scope note (leased facilities)** — dev/sustainability, "Data center energy and AI in 2025"
(https://www.devsustainability.com/p/data-center-energy-and-ai-in-2025): Google's PUE disclosure
is "only for Google owned and operated facilities. This is a big hole in Google's data because it
runs many more data centers leased from the likes of Equinix and Digital Realty, but doesn't report
their PUE." (Secondary; the underlying scope limitation is stated in Google's own reports.)

## Secondary — corroboration only (not load-bearing)

- Brookings, "Global energy demands within the AI regulatory landscape"
  (https://www.brookings.edu/articles/global-energy-demands-within-the-ai-regulatory-landscape):
  states the paradox — data-center emissions -12% in 2024 while absolute electricity +27%
  year-over-year; overall GHG +51% 2019–2024. (Every figure it cites is confirmed against the
  primary above; the 51% is now taken from Google's own report, not from Brookings.)
- DatacenterDynamics, "Google data center power use up 27%..."
  (https://www.datacenterdynamics.com/en/news/google-data-center-power-use-up-27-emissions-down-17-report):
  corroborates the 27% growth and the Scope-3 dominance (73% of the 2024 footprint).

## Postscript primary — Google 2026 Environmental Report (added session 17)

**Google 2026 Environmental Report** — fiscal year 2025, published June 2026. Fetched first-hand
2026-07-09 during the shipping gauntlet, after the round-1 Verifier found it retrievable.
- Official landing: https://sustainability.google/google-2026-environmental-report
- Full-text extracted from the official PDF:
  https://storage.googleapis.com/gweb-mobius-cdn/sustainability/uploads/7f477eb723fe0c23d03f94b90a08882b9f28187d.pdf
- Verbatim (growth): "…our total electricity consumption grew by 37% in 2025, up from 27% in 2024."
  (Wording caveat, quoted exactly and not conflated: the 2026 report states the 37% for TOTAL
  electricity and restates 2024's 27% on that basis; the 2025 report had stated the 27% for total
  DATA CENTER electricity.)
- Verbatim (PUE): "This focus resulted in a 2025 average annual PUE of 1.09 for our global data
  center fleet—meaning that Google data centers used 83% less overhead energy than the industry
  average."
- Used ONLY for the work's postscript (the verdict survives the subject's next disclosure:
  required PUE 1.09/1.37 = 0.796 ≈ 0.80). The claim under trial remains the 2025 report (FY2024).

## Deliberately NOT used / corrected exclusions
- *(Superseded, session 17.)* Session 16 excluded the "~43 TWh in 2025, +37%" figures as "a
  social-media post citing a 'Google 2026 Environmental Report' — not a retrievable primary."
  The session-17 gauntlet found the 2026 report IS a retrievable primary (published ~two weeks
  before session 16; the collective simply had not searched for it). The +37% growth figure is
  now verified verbatim from the primary and used in the postscript above; the ~43 TWh absolute
  remains unused (the growth rates carry the argument).
- Absolute total-electricity TWh figures — not needed for the arithmetic and not pinned to the
  primary this session; the disclosed year-over-year growth rates carry the argument.
