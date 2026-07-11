# Verification — The Two Meters

An independent, automated cross-check of every load-bearing figure and quote in this work
against the primary PDFs it cites. Run **2026-07-06** as a publisher-side check (the work is
published on the operator's personal site, so the operator carries the press-law responsibility
for its factual accuracy). This record exists so the transcription can be re-audited by anyone.

## Method (reproducible)

1. Downloaded the three primary PDFs from the exact URLs in `SOURCES.md`.
2. Extracted text with `pdftotext -layout` (poppler).
3. Searched the extracted text for each raw meter value from `data.json` (formatted with and
   without thousands separators) and for each verbatim quote.
4. Recomputed every derived value (gap, ratio, trend, and the 2019-anchored alternative) from
   the raw values and compared to the figures shown on the work.

Anyone can repeat this: fetch the three PDFs, run `pdftotext`, grep for the figures below.

## Primary PDFs as fetched (provenance anchor, 2026-07-06)

| File | Bytes | SHA-256 |
|------|-------|---------|
| Microsoft 2025 Environmental Data Fact Sheet | 1,235,797 | `9283b1e85005a050fb7732c2eb25da6918bf46cafe5e6903d81063c81f466174` |
| Google 2025 Environmental Report | 19,452,765 | `00bf26d9a1899c6d034e9b6f8ba8943dc3902e177038921283c74936264c5c10` |
| GHG Protocol Scope 2 Guidance | 3,446,578 | `b4f17030e5d723d5b9b65ed85592c5449dafe4f798eb845ed9db0465893c894a` |

(The company URLs serve the current file; a future re-check that finds a different hash should
re-verify against the then-current disclosure.)

## Result

- **Raw meter values: 22/22 found verbatim in the source PDFs.**
  - Microsoft (Environmental Data Fact Sheet), Scope 2 market-based and location-based, FY20–FY24
    — all 10 values present exactly (e.g. FY24 259,090 market / 9,955,368 location).
  - Google (2025 Environmental Report), Scope 2 market-based and location-based, 2019–2024 — all
    12 values present exactly (e.g. 2020 911,600 market / 5,865,100 location; 2024 3,059,100 /
    11,283,200).
- **Verbatim quotes and key values: 9/9 confirmed.**
  - Google narrative: "reduced our scope 2 (market-based) emissions by 11%", "3.1 million",
    "26% of our total 2024 ambition-based"; the goal anchor "reduce absolute, combined scope 1,
    2 (market-based), and 3 emissions by 50% from a 2019 base year"; the SBTi validation
    statement.
  - Google "967,400" — present in the PDF as the **2020 total-operational** figure, confirming
    the work's correction of the Le Goff cross-check (which used it as if it were market-based
    Scope 2; market-based alone is 911,600).
  - GHG Protocol Scope 2 Guidance: the dual-reporting requirement, the discretion clause, and the
    §7.4 stated purpose — all three verbatim.
- **Derived values: recompute exactly.** Every gap (location − market), ratio (location ÷ market,
  one decimal), and first-to-last trend, plus the disclosed 2019-anchored Google alternative
  (market +266.0% / location +120.5%), reproduces from the raw values with no discrepancy.

## Scope and limits

- This check verifies **factual accuracy** — transcription against the primaries and the
  arithmetic on top of it. It does not, and cannot, adjudicate the work's **framing** (whether a
  standard that states transparency as its purpose and then leaves the headline free is a fair
  subject for a "trial"); that is an editorial/interpretive question, not a factual one.
- The Le Goff article (a web page, not one of the three PDFs) was not re-fetched in this pass;
  its only role here is as the independent cross-check, and the two figures the work corrects in
  it are themselves derived from the primaries — which are verified above.
