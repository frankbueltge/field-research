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

## Trial 2 snapshots (fetched 2026-07-02, same route and cleaning as above)

| File | Source URL | Rows | API lastupdated |
|---|---|---|---|
| wb-expgnfs-2023.json | https://api.worldbank.org/v2/country/all/indicator/NE.EXP.GNFS.CD?date=2023&format=json&per_page=400&page=1 | 265 | 2026-07-01 |
| wb-cel-2023.json | https://api.worldbank.org/v2/country/all/indicator/IT.CEL.SETS?date=2023&format=json&per_page=400&page=1 | 265 | 2026-07-01 |
| wb-merchexports-2023-rejected.json | https://api.worldbank.org/v2/country/all/indicator/TX.VAL.MRCH.CD.WT?date=2023&format=json&per_page=400&page=1 | 265 | 2026-07-01 |

Spot-checks passed: US exports of goods and services 2023 = 3,073,360,000,000 in the
snapshot, vs. ~3.07e12 US$ reported publicly (BEA annual trade release / Progressive
Policy Institute summary of the census-basis figure); China mobile-cellular
subscriptions 2023 = 1,824,422,700 in the snapshot, vs. ~1.824e9 in public restatements
of the same World Bank/ITU indicator.

**Defendant-selection preconditions (declared before scoring, applied to the
real-country subset, region.id != "NA"):** N in [100, 10000]; positive-value span >= 3
orders of magnitude; reporting precision reaching the unit digit (rejected if the
majority of non-null values are exact multiples of 1000). Digit tests are not run
during selection.

- NE.EXP.GNFS.CD -- ACCEPTED. N=175, span 5.32 orders, 11/175 values (6.3%) exact
  multiples of 1000, no zeros/negatives.
- IT.CEL.SETS -- ACCEPTED. N=172, span 4.88 orders, 16/172 values (9.3%) exact
  multiples of 1000 (disclosed: partial reporting-rounding is a known conviction
  mechanism for the last-digit test), no zeros/negatives.
- TX.VAL.MRCH.CD.WT -- REJECTED on the precision precondition: 221 of 252 non-null
  values (87.7%, aggregates included) are exact multiples of 1,000,000 -- the WTO
  reporting unit is millions, so the stored last digits carry the storage convention,
  not the data-generating process. The raw snapshot is committed
  (wb-merchexports-2023-rejected.json) so this rejection is independently checkable.

Trial 2 was appended with exactly:

    python3 runner.py --date 2026-07-02 --indicators "wb-expgnfs-2023.json:2023,wb-cel-2023.json:2023"

and verified by a deterministic re-run from the pre-trial-2 ledger state
(byte-identical ledger.json and data.json).
