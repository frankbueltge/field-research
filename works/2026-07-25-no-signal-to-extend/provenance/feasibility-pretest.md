# Build precondition 2 — harvest wall-clock pre-test (Skeptic C3)

**Session 63, 2026-07-25, conductor's hand.** Feasibility probes only — none of the fetched
records enter the measurement corpus; the measurement harvest runs only after the
pre-registration is locked in git.

## Bulk metadata route (OAI-PMH), measured

Endpoint: `https://oaipmh.arxiv.org/oai` (the archive's own bulk-metadata route; metadata CC0).

- `ListRecords&metadataPrefix=arXiv&set=cs` → HTTP 200, **1,300 records / response**,
  ~2.86 MB, **0.47–0.75 s** per response (two probes, 2026-07-25 ~03:38Z).
- Continuation via `resumptionToken` (URL-encoded; token expiry next midnight UTC) —
  confirmed working; records arrive in ID order from the oldest.
- Allowed parameters per the endpoint's own error message: `metadataPrefix, set, verb, from,
  until` — `from` filters on **datestamp** (last metadata change), not submission date. A
  record created in year Y always has datestamp ≥ Y, so `from=2015-01-01` yields a **superset**
  of all 2015+ submissions (plus older records updated since); stratum membership and dating
  are then decided client-side from `<categories>` (first entry = primary) and `<created>`
  (v1 submission date), both present in the `arXiv` metadata format.
- No throttling encountered at ~1 request/3 s pacing (the published courtesy rate; we keep it).

**Wall-clock estimate:** set=cs superset ≈ 0.9–1.0 M records → ~700–770 requests ≈ 45–50 min;
set=math superset ≈ 0.4–0.6 M → ~25–35 min. **Total ≈ 70–90 min, serial, at the courtesy
rate.** Conclusion: a one-session harvest is feasible only as a background job; the build
therefore locks the pre-registration first and treats harvest completion as checkpointable
(a partial harvest is discarded and re-run, never topped up across differently-dated runs).

## Corpus sizing (query-API counts; feasibility metadata only)

`https://export.arxiv.org/api/query` totalResults for `cat:<stratum> AND submittedDate:[H1]`
(these counts match **any listed category**, so they are upper bounds for the primary-category
strata defined in the pre-registration; measured 2026-07-25):

| Stratum | 2015H1 | 2020H1 | 2022H1 | 2025H1 | 2026H1 |
|---|---|---|---|---|---|
| cs.CL | 348 | 3,246 | 4,289 | 12,550 | 14,315 |
| cs.CV | 1,092 | — | 9,248 | 17,095 | 19,750 |
| math.NT | 1,040 | — | 1,453 | 1,699 | 2,159 |

The binding constraint is the smallest cell, cs.CL 2015H1 = 348 any-listing (primary-only
lower). Fixed-draw sizes in the pre-registration are set to fit it with margin (N_s = 150
abstracts; pooled-token prefix T = 15,000 tokens).

## Probe artifacts

Probe responses (`oai-test-*.xml`, `oai-tok-2.xml`, `probe*.xml`, `halfyear-counts.txt`) were
kept in the session scratchpad and are **not** part of the corpus or the repo; the numbers
above are their complete extract.
