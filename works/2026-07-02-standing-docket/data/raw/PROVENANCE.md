# Raw snapshot provenance

Fetched 2026-07-02 by the conductor via web research (server-side extraction), because
the build sandbox has no direct egress to api.worldbank.org. The extraction layer
markdown-escapes underscores (`\_`); the only cleaning applied was `\_` -> `_`, after
which each payload parsed as valid JSON with pagination complete (pages=1) and row
count equal to the API-reported total. No other transformation.

| File | Source URL | Rows | API lastupdated |
|---|---|---|---|
| wb-countries.json | https://api.worldbank.org/v2/country?format=json&per_page=400 | 295 | — |
| wb-pop-2023.json | https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?date=2023&format=json&per_page=400&page=1 | 265 | 2026-07-01 |
| wb-gdp-2023.json | https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=2023&format=json&per_page=400&page=1 | 265 | 2026-07-01 |

Spot-checks against publicly known figures passed (India population 2023 = 1,438,069,596;
Germany GDP 2023 ≈ 4.56e12 US$). Aggregates are excluded downstream via the country
list's region.id != "NA" (217 real countries). World Bank data are themselves revised
over time; the snapshot date above is the pinned reference.

---

## Trial 2 (fetched 2026-07-09)

Fetched 2026-07-09 by the conductor via web research (server-side extraction), same
reason and same cleaning step as trial 1: the build sandbox has no direct egress to
api.worldbank.org, and the only cleaning applied was `\_` -> `_`, after which each
payload parsed as valid JSON.

| File | Source URL | Rows | API lastupdated |
|---|---|---|---|
| wb-countries-2026-07-09.json | https://api.worldbank.org/v2/country?format=json&per_page=400 | 295 | — |
| wb-pop-2024.json | https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?date=2024&format=json&per_page=400&page=1 | 265 | 2026-07-01 |
| wb-gdp-2024.json | https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=2024&format=json&per_page=400 (see merge note below) | 265 | 2026-07-01 |
| wb-lab-2024.json | https://api.worldbank.org/v2/country/all/indicator/SL.TLF.TOTL.IN?date=2024&format=json&per_page=400&page=1 | 265 | 2026-07-01 |

wb-countries-2026-07-09.json: 295 rows, pagination complete (pages=1), 217 real
countries (region.id != "NA") -- same count as trial 1's snapshot.

wb-pop-2024.json: single-page fetch (per_page=400&page=1), 265 rows, real-country
non-null N=217.

wb-gdp-2024.json -- THREE-PAGE MERGE, DISCLOSED: the single-page fetch (per_page=400)
failed repeatedly at the extraction layer. It was instead fetched in three pages
(per_page=100): page 1 = 100 rows, page 2 = 100 rows, page 3 = 65 rows, total
100+100+65 = 265 rows, all three pages reporting API lastupdated 2026-07-01 and
meta.total=265. The conductor merged the three pages' row arrays into one [meta, rows]
payload; the stored meta block is page 1's as-fetched (it still reads pages:3,
per_page:100 -- left unaltered rather than rewritten to look like a single-page fetch).
265 unique country ids were verified present after the merge, with no duplicates and no
gaps against meta.total -- uniqueness checked on the `country.id` field (the API's own
key; 5 aggregate rows, the income-level groups, legitimately carry an empty
`countryiso3code` and are excluded downstream anyway). Real-country non-null N=199.

wb-lab-2024.json (SL.TLF.TOTL.IN, "Labor force, total"): single-page fetch
(per_page=400&page=1), 265 rows, API lastupdated 2026-07-01. Real-country non-null
N=182. This is the indicator ROTATED IN for trial 2, replacing no prior indicator (it is
additive: trial 2 now scores three series, not a swap).

DISCLOSURE -- estimates-based series, not a raw count: SL.TLF.TOTL.IN is not a census-
style count the way population is. The indicator's own metadata
(https://api.worldbank.org/v2/indicator/SL.TLF.TOTL.IN?format=json, fetched 2026-07-09)
gives sourceOrganization verbatim: "International Labour Organization (ILO), type:
estimates based on external database; United Nations (UN), publisher: UN Population
Division; Staff estimates, World Bank (WB)". This series should be read as
model/estimate output blended from ILO, UN Population Division, and World Bank staff
estimates -- not as a direct administrative count -- and any digit-test verdict on it
should be read in that light. See README.md Limitations for how this is carried into
the ledger's framing.

Spot-checks the conductor ran:

- India population 2024 = 1,450,935,791 -- matches independent public restatements
  digit-for-digit (e.g. https://database.earth/population/india).
- USA GDP 2024 = 29,298,013,000,000 (approximately $29.3T), consistent in magnitude
  with U.S. national accounts.
- Germany GDP 2024 = 4,685,592,577,804.69.
- India labor force 2024 = 608,500,805 (plausibility check only -- not independently
  cross-verified against a second source, consistent with the estimates-based nature
  of this indicator).

Escaping cleanup: same as trial 1, `\_` -> `_` only, applied to all four trial-2
snapshots, after which each parsed as valid JSON with no further transformation.
World Bank data are themselves revised over time; 2026-07-09 is the pinned reference
point for this trial's snapshots, not a claim that the figures are final.
