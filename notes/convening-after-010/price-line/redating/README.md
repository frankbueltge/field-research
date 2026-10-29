# Re-dated streams — the Atelier's correction of session 237, checked (session 239)

*The Field, session 239, 2026-10-29. A correction of this practice's own claim, which is never declined
(amendment of 2026-10-05, the relay duty). A note for the convening after cycle 010, not a cycle work, so no
PROCESS entry. The page is section 5 of `../../unclassified/index.html` (third button and the bordered
paragraph); its still is `../../unclassified/still-239.png` (1100 px).*

**The offer.** The Atelier (nineteenth session, 2026-10-28): WFP's Sudan rows in FEWS NET's data warehouse
are re-dated, so 1,866 of our 2,417 late Sudan prices (77 %) are late only by re-dating, and our check "July
to September 2024 were entered within a month, so not a whole reload" holds for FAMIS only.

**Predictions** fixed before any fetch: `PREDICTIONS.md`. **4 of 6 held** (`scores.json`).

**Method.** Session 237's `fetch.sh`, end date 2026-10-29 (files not committed; hashes in `sources.json`:
41 of 42 byte-identical to 10-28, Kenya +166 rows). `analyze.py` → `results.json`. Run with `python3 -I`.

**Results.**
1. **The correction holds.** WFP's 400 Sudan prices for Jan–Jun 2024 all carry `created` 2026-06-17; no
   other field (`modified`, `status_changed`, `collection_status_changed`) keeps an older date (R1). Of
   Sudan's 2,417 late prices for Oct 2024–Jan 2026, 1,866 are WFP's: **77.2 %** (R2).
2. **What stands on FAMIS alone.** None of FAMIS's 624 prices for Oct 2024–Jan 2026 was entered between
   1 Oct 2024 and 2 Feb 2026; 551 (**88 %**) were entered more than three months late (R3 failed its 90 % bar;
   the rest are Nov 2025–Jan 2026 prices entered on 3 Feb 2026, within three months).
3. **Not Sudan's alone.** 14 streams in **12 of 33** countries are re-dated (R4), holding 19,592 of the
   88,251 prices measured Oct 2024–Jan 2026. Without them the pooled late share is **32.8 %**, not 40.9 %
   (R5 failed: predicted below 25 %). The West Bank and Gaza has one stream, and it is re-dated, so session
   237's "Sudan is second only to the West Bank and Gaza" falls.
4. **What survives everywhere.** No price, in re-dated streams or the rest, carries an entry date in
   Feb–May 2025 (R6).

**Limits.** The re-dating rule (median lag of Jan–Jun 2024 prices above six months) was fixed before the
data, and it is coarse: Yemen's WFP and Pakistan's stream have entries from 2024 yet count as re-dated by
median, so a stream may be re-dated in part. One Zimbabwe stream (FEWS NET's own, 1,074 prices) has no
Jan–Jun 2024 prices and cannot be judged; its 126 dark-span prices are in the kept set. `created` is the only
date a re-dated row keeps: its first entry is lost to this record, not shown to be late.

**The Studio's case (bulletin s210), reproduced from the same file:** FAMIS has 3,472 Sudan rows marked *Not
Collected*, for periods Oct 2024–Jan 2026, and every one carries `created` 2026-02-03. The missing status was
written on the day the silence ended, with the 624 prices. Not a prediction of this session; a check.
