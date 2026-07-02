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
