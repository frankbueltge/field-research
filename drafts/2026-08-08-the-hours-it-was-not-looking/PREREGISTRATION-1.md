# Pre-registration — increment 1: the completeness census of GDELT's own 15-minute file series

**Written and committed 2026-08-08 (session 103), before the instrument exists and before any
census number is computed.** Same discipline as sessions 100–102: predictions first, scored
afterwards, none revised after the fact. Predictions that fail are reported as failed.

## What exists at the moment of writing (checked first-hand, not assumed)

- `http://data.gdeltproject.org/gdeltv2/masterfilelist.txt` — HTTP 200, `content-length`
  **126,497,331** bytes, `last-modified` **Sat, 08 Aug 2026 23:49:28 GMT**, read at 23:58 UTC on
  2026-08-08. (`curl -I`, this session.)
- Its format, read from the first and last kilobyte by HTTP range request: one line per file,
  three whitespace-separated fields — **byte size**, **MD5**, **URL**. Three files per 15-minute
  cycle (`.export.CSV.zip`, `.mentions.CSV.zip`, `.gkg.csv.zip`), the cycle timestamp encoded in the
  filename as `YYYYMMDDHHMMSS`.
- First line: `20150218230000.export.CSV.zip`. Last line: `20260809000000.gkg.csv.zip`.
- `http://data.gdeltproject.org/gdeltv2/lastupdate.txt` — HTTP 200, naming the same
  `20260809000000` cycle.

**Nothing beyond this has been computed.** The manifest has not been downloaded in full at the time
this file is written.

## The measurement, specified before it runs

1. Download `masterfilelist.txt` in full; record its byte size and MD5 as fetched.
2. Parse every line into (size, md5, url). Derive the cycle timestamp and the file type from the URL.
3. Build the **expected grid**: every 15-minute instant from the first timestamp present to the last
   timestamp present, inclusive.
4. For each expected cycle, record which of the three file types the manifest lists.
   - **missing cycle** = none of the three listed
   - **partial cycle** = one or two of the three listed
   - **complete cycle** = all three listed
5. Group consecutive missing cycles into **gap runs**; report count, length distribution, and the
   dated start/end of the longest runs.
6. **Volume collapse (present but starved):** for each complete cycle, compare its `gkg.csv.zip`
   byte size against the **median gkg size of the 672 complete cycles preceding it** (a trailing
   seven-day window). A cycle is *collapsed* if its size is **below 20 %** of that trailing median.
   Cycles without a full trailing window are excluded from this arm and counted as excluded.
7. **Hygiene:** off-grid timestamps (not at :00/:15/:30/:45), duplicate URLs, zero-byte entries,
   malformed MD5 fields.
8. **Controls against the host — the manifest is GDELT's self-report and is not taken on trust:**
   - **C-A:** 40 manifest entries drawn at random (fixed seed, drawn before fetching) are probed with
     HTTP HEAD; the host's `content-length` is compared to the size the manifest claims.
   - **C-B:** for 20 randomly drawn *missing* cycles, the `.export.CSV.zip` URL that would exist if
     the cycle existed is probed with HTTP HEAD. A missing manifest line and a missing file are not
     the same claim, and this arm is what licenses saying "the instrument published nothing" rather
     than "the manifest does not list it".

## Predictions — committed before any number is computed

**On the shape of the gaps**

- **P1.** The series contains at least one gap run of **≥ 96 consecutive missing cycles** (≥ 24 h).
- **P2.** Missing cycles are **≥ 0.5 % and < 10 %** of expected cycles.
- **P3.** The **longest** gap run began **before 2021-01-01**.
- **P4.** More than **half** of all missing cycles fall in the **first third** of the series by time
  (2015-02-18 → roughly 2019-04).

**On partial and malformed records**

- **P5.** At least **10** partial cycles exist (some file types listed, others not).
- **P6.** Fewer than **50** off-grid timestamps exist.
- **P7.** **Zero** duplicate URLs exist in the manifest.

**On silent degradation — the arm we think matters most**

- **P8.** The number of **collapsed** cycles (present, gkg below 20 % of its trailing seven-day
  median) **exceeds** the number of missing cycles.

**On the present state of the instrument**

- **P9.** In the **last 365 days** before the final cycle, there are **fewer than 20** missing cycles.

**On the controls**

- **P10.** In C-A, the host's `content-length` matches the manifest's claimed size for **≥ 95 %** of
  the 40 probed entries (probe failures are reported, not imputed).
- **P11.** In C-B, **≥ 80 %** of the 20 probed missing-cycle URLs return a not-found status rather
  than a file — i.e. the manifest's omission corresponds to a genuine absence on the host.

## What would make this increment a failure rather than a result

- If C-B shows that files exist on the host for cycles the manifest omits (P11 badly failed), then
  the manifest is not a record of what was published and **the concept's evidence route is wrong**.
  That outcome is to be reported as such, not repaired mid-session — the same discipline that
  discarded the previous concept.
- If the census returns almost no gaps and almost no collapses, the honest finding is that this
  instrument's file series is complete, and the concept has no object. That would also be a result,
  and it would end the arc at the gate.

## Standing limits, stated before the numbers

- The manifest records **files**, not **content**. A present, normal-sized file may still contain a
  degraded or biased sample of the world; this increment cannot see that and does not claim to.
- Byte size is a **proxy** for volume, not a measurement of it. Compression ratios vary. The
  collapse arm is explicitly a screen, not a verdict, and any collapsed window this practice reports
  as load-bearing will be checked by opening the file itself in a later increment.
- Absence of a file from the public front-end does not by itself establish that the collection
  pipeline stopped; it establishes that the public record of that quarter-hour is empty. Those are
  different claims and the write-up must keep them apart.
