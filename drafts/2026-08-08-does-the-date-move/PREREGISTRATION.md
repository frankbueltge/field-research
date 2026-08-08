# Pre-registration — increment 1 of the investigation "Does the Date Move?"

Committed **before** the instrument existed. Session 100, 2026-08-08. Locks the population,
the method, the definitions and four predictions. Deviations are logged in `RESULT.md`, never
edited into this file.

## What is already known before this run (so nothing here is scored twice)

1. From this house's own line *"As of Today"* (`drafts/2026-08-06-as-of-today/RECORD.md`), on a
   live fetch of 2026-08-05/06: **H** (the HTTP `Last-Modified` header) was present on 36/36 EC
   and 34/34 NIST pages and absent on all IE and GOV.UK pages measured; on EC it never reported a
   time older than 26 minutes before delivery. **V** (a date printed for a human) was present on
   34/40 EC, 19/74 NIST, 7/7 GOV.UK, 2/56 IE.
2. From this session's own **feasibility probe** (`probe-cdx.json`, run before this file, declared
   as a probe and scoring nothing): the Internet Archive CDX API is reachable (HTTP 200), and
   archived replay preserves the original response headers as `x-archive-orig-*`. On the four URLs
   the probe completed, the raw capture digest changed on **almost every adjacent capture pair**
   (EC `/policies`: 163 distinct digests in 192 captures; EC `/policies/ai-office`: 515 in 529;
   NIST `/publications`: 1202 in 1208). **The raw digest is therefore not a content-change
   detector**, and the design below does not use it as one.

## The question this increment answers

For an official page whose content actually changed between two observations, did the page's own
stated change-date move with it?

## Population (fixed here, selected mechanically)

From the existing corpus files of *"As of Today"*, in file order, the first rows carrying a
non-null `v`: **3 EC** (`signals.json`), **3 NIST**, **3 GOV.UK**, **2 IE** (`signals-2.json`)
— **11 URLs**. The count is set by what one session can fetch politely, not by the results; the
arc's later increments extend the same population, they do not reselect it.

## Method

- **Window:** the 12 calendar months **2025-08 through 2026-07**.
- **Observation:** for each URL and each month, the CDX capture with `statuscode:200` whose
  timestamp is the **first at or after the 15th of that month**; if none, the **last before the
  15th**; if the month has no 200-capture, the observation is **MISSING** and every pair touching
  it is dropped, counted, and reported.
- **Fetch:** `https://web.archive.org/web/<timestamp>id_/<url>` — raw original bytes, no replay
  injection. From each response we take:
  - **H** — the `x-archive-orig-last-modified` header, i.e. what the origin server said at
    capture time. Absent is recorded as absent, never as unchanged.
  - **V** — a printed date, extracted by the **unmodified rule set of `collect_signals.py`**
    (V1-last-update → V2-published → V3-time-element, first match wins). Reusing an already
    critiqued extractor rather than writing a new one is deliberate; its known limits travel with
    it, including that session 97 **killed** that line's three-class SELF/OTHER labelling. This
    run makes no claim about what V refers to — only whether the string moved.
  - **T** — normalised visible text: `<script>`/`<style>` removed, tags stripped, entities
    unescaped, hex/base64-looking tokens of 16+ characters removed, whitespace collapsed.
- **Content change**, per consecutive month pair, by `difflib.SequenceMatcher` ratio on T:
  **IDENTICAL** = 1.0 · **TRIVIAL** = 0.98 ≤ r < 1.0 · **SUBSTANTIVE** = r < 0.98. The 0.98 line
  is an arbitrary threshold chosen before seeing any ratio; the full distribution of ratios is
  published so a reader can move it and recompute.
- **Signal moved:** V moved if the normalised V string differs between the two observations;
  H moved likewise. Where a signal is absent in either observation, that pair is
  **UNSCORABLE for that signal** and is reported as such, not as "did not move".

## Predictions, locked

- **P1 (the core).** Among SUBSTANTIVE pairs that are scorable for V, **V fails to move in more
  than half of them on at least one authority.**
- **P2.** Among all pairs scorable for H on EC, **H moves in ≥ 90 %** — including pairs where T
  is IDENTICAL. (Follows from "As of Today"'s delivery-time finding; a directional check of
  whether that finding holds historically, not a new claim.)
- **P3.** At least one pair exists where T is **IDENTICAL and V moved** — a date advancing with
  no change a reader could see.
- **P4 (confirmatory, not novel).** Among adjacent CDX captures across the whole population,
  the raw digest differs in **≥ 90 %** of pairs. Already indicated by the probe on 4 URLs; scored
  here only to state it over the population the rest of the run uses.

## What this increment cannot claim

It cannot say a page *did not* change between two monthly observations — only that the two
observations differ or do not. It cannot say a change was *editorial*: a T-difference may be a
navigation block or a promoted headline elsewhere on the page. It measures 11 URLs and is a
first increment, not the investigation. **No result from this run is a claim about any authority
until it survives the gauntlet on the exact state that ships.**
