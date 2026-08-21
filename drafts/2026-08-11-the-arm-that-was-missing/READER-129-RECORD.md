# Independent reader 129-A — the receiver's own record

*Published unedited, including the part this session's own derivation contradicts (`INCREMENT-19.md`
§6: the reader's "38" against this session's 47, where the reader is wrong). Nothing has been
corrected, softened or removed.*

**Severing conditions.** Dispatched 2026-08-21 at ~03:38Z, **before this session had parsed a single
date and before it had formed any reading**. Given the saved page, the extractor and the extracted
series, and nothing else: no context about this practice, no statement of what answer would be
welcome, no hint that any of the three questions had a preferred outcome, and an explicit
instruction that *"cannot be determined from this material"* is a good answer and expected wherever
true. Asked three questions: how the record represents a day on which no check ran; the full
structure of `Error` across the whole record; and whether the last event is distinguishable from the
earlier ones.

---

## What I did

I read `receiver-dashboard-2026-08-19.html` (246,014 bytes) directly, and cross-checked it against `receiver-series-2026-08-19.json`.

- Confirmed the JSON was produced from this exact HTML file: `source.sha256` in the JSON (`fff0a66f2bddc05106b892f7d18d59202eda1ab6829f71da7edbfea624f9c6bb`) matches `sha256sum receiver-dashboard-2026-08-19.html` run just now.
- Ran `extract_dashboard.py --selftest` against the HTML: all 9 checks pass, including the two adversarial controls (a renamed `Video ID:` heading is reported as a problem rather than silently absorbed; every y-value is labelled by the axis's own `ticktext`/`tickvals`, none unmapped).
- Independently re-parsed the raw HTML with my own regex/`json.loads` pass (not the extractor) to spot-check specific facts: I pulled the raw `Plotly.newPlot(...)` block for video `7366758818765638917` directly out of the byte stream and confirmed its `x`/`y` arrays match the JSON exactly, including the last 15 points (`y` goes 0,0,0 then eleven 1's from 2026‑01‑03 through 2026‑01‑14).
- Grepped the raw HTML byte stream (not the JSON) for the date strings `2025-05-23` and `2025-12-13`: each occurs **0 times anywhere in the file**. Grepped `2026-01-03` (14 occurrences = 11 video series + 3 aggregate traces) and `2025-05-09` (13 occurrences = 10 video series, since the 11th video hadn't started yet, + 3 aggregate traces) — both match the expected counts exactly.
- Extracted the page's visible prose (stripped of script/style/tags) to read what the page itself says about its own methodology.
- Confirmed `grep -c 'class="video-card"'` = 11, matching `counts.videos_extracted` = 11 and `problems` = 0 in the JSON.
- Wrote a standalone analysis script (`/tmp/.../scratchpad/analyze.py`) against the JSON's per-video `x`/`states` arrays to build a master date axis and compute per-date tracked/Error counts, run-lengths, and start/end dates for all 11 series.

## Q1 — How does the record represent a day with no check?

The y-axis in every chart is defined by its own layout ticks: `"ticktext":["Not Available","Error","Available"]`, `"tickvals":[0,1,2]` (confirmed by direct grep on the raw HTML — this is the only ticktext/tickvals pair in the file, so it's uniform across all cards). There is no fourth code and no `unmapped_y_values` anywhere (extractor's `states_are_labelled` is true for every chart). So within the record, a day can only be one of those three states — there is no in-band "not checked" value.

What actually happens on an unchecked day is that the date is simply **absent from the `x` array** — nothing is written for it, on any video. I found exactly two such dates: `2025-05-23` and `2025-12-13`. Both are missing from all 11 per-video series' `x` arrays and from the aggregate chart's three traces identically (`derived.gaps` in the JSON, e.g. video `7366758818765638917`: `[{"after":"2025-05-22","before":"2025-05-24","days":2},{"after":"2025-12-12","before":"2025-12-14","days":2}]` — the same two gaps, verbatim, on all 11 videos). Direct grep on the raw bytes confirms these two date-strings occur nowhere in the file at all — not as skipped/tombstoned entries, just genuinely absent.

**What I cannot tell**: the page's own prose says only "The dashboard performs daily availability tests" and, in the footer, "Automated daily availability checks" — stating an intended cadence but never once addressing what a missing day means (no "gap," "missing," "downtime," or similar text anywhere in the visible page). So the material lets me establish the *mechanism* (missing date = absent x-entry, not a coded status) but not the *reason* — I cannot tell whether `2025-05-23` and `2025-12-13` mean "no check was attempted" or "a check was attempted but produced nothing usable." The two dates are a Friday and a Saturday respectively, with no other pattern visible from only two instances.

## Q2 — Full structure of "Error" across the whole record, all 11 series

Record spans **2025-04-09 to 2026-01-14**, 279 distinct calendar dates (238 for the video that started later).

**Do all 11 start together?** No. Ten videos start `2025-04-09`. One — `7361448925972155679` ("Response to TikTok Ban Bill", creator `tiktok`) — starts `2025-05-20` and has 238 points instead of 279 (`derived.first_date`/`n_points` in the JSON for that video). All 11 end on the same date, `2026-01-14`.

**Per-date Error counts** (computed over the master date axis, counting only videos then tracked): for 241 of the 267 dates before 2026‑01‑03, zero series are in Error. The distribution of nonzero days before that point:

| error count | # of dates |
|---|---|
| 1 | 18 |
| 2 | 5 |
| 3 | 1 (2025-04-09, the record's very first day: 3 of 10 then-tracked videos) |
| 8 | 1 (2025-09-16) |
| 10 | 1 (2025-05-09) |

**Dates where all (or nearly all) tracked series are in Error at once**, before the final block:
- **2025-05-09**: 10 of 10 then-tracked videos (video 11 not yet started) — 100%.
- **2025-09-16**: 8 of 11 tracked videos — 73%. (The other 3 read "Not Available" that day.)

**Duration of each such episode**: both are exactly **one calendar day**. I checked the surrounding dates directly: on 2025-05-08 and 2025-05-10, all 10 videos read something other than Error (9 "Not Available", 1 "Available"); on 2025-09-15 and 2025-09-17, all 11 read non-Error. So both multi-video Error spikes appear and resolve within a single day.

**Individual per-video Error run lengths across the whole record** (every contiguous stretch of consecutive Error days, per video, excluding the trailing run): every single one is **1 day**, except two runs of **2 days** (on videos `7117394257064840490` and `7332960275127110954`). No video anywhere in the pre-2026 record stays in Error for more than 2 consecutive days.

**Then: 2026-01-03 through 2026-01-14** — all 11 tracked series enter Error simultaneously on `2026-01-03` and remain in Error every single day through `2026-01-14`, the record's last date: a **12-day run, 11 of 11 (100%) tracked series**. I confirmed this per-video via each series' `derived.last_change_date` = `2026-01-03` and `derived.final_status` = `"Error"` for all 11 videos, and via the trailing-run computation (all 11 report `2026-01-03 .. 2026-01-14, len 12`).

## Q3 — Is the last event distinguishable from earlier ones?

Yes, on the record's own numbers, in three independent ways:

1. **Duration**: every prior Error run in the record is 1 day (36 of the 38 pre-final runs) or 2 days (2 runs). The final run is **12 days** — six times the longest run ever seen before it.
2. **Breadth**: the two prior episodes where many videos were simultaneously in Error hit 10/10 (2025-05-09) and 8/11 (2025-09-16), each for a single day before reverting. The final episode is **11/11 (100%)** of tracked videos, sustained for all 12 days — no prior episode combines full breadth with any duration beyond one day.
3. **Resolution**: every prior Error day/run, in every prior instance, is bounded on both sides by a non-Error day within the record (I checked this directly for both multi-video spikes). The final run has no bound on its right side — the record simply stops on `2026-01-14` while every series is still reading Error. The page's own "Dashboard generated on: 2026-01-14 21:53:41" timestamp is the last value in every series' x-array, meaning the record ends at the moment the page was generated, not because the Error state resolved. So this episode is **right-censored**: the material shows it starting and shows it still ongoing at the last moment the record covers, but cannot show whether or when it ended.

I also cross-checked the final day against the page's own rendered summary tiles (not derived by me, but printed by the page itself at generation time): "0 Available Videos," "0 Unavailable Videos," "11 Videos with Errors" — exactly matching my count of 0/0/11 for `2026-01-14` from the per-video series.

## What I could not determine

- What a missing date (`2025-05-23`, `2025-12-13`) actually represents operationally — the page states an intended "daily" cadence but never explains a missed day. Not checkable from this material.
- Whether the 2026-01-03–01-14 all-Error episode ever resolved — the record ends at the page's own generation timestamp, so anything after `2026-01-14 21:53:41` is outside this material entirely.
- What specifically causes an "Error" state technically — the page states only "Error are problems on our end, not TikTok," with no further detail on what kind of problem.
- Why the 11th video (`7361448925972155679`) was added to tracking on `2025-05-20` rather than at the record's start — not addressed anywhere in the page text.
- Any sub-day timing (all x-values are dates only, no timestamps for individual checks besides the single page-level "generated on" line).

## Anything else I noticed

- The page identifies itself as the "TikTok Research API FAILs Dashboard," run by AI Forensics (`aiforensics.org`, per the page's logo asset path and footer copyright "© 2025 AI Forensics"). Its own stated purpose (from the visible lead paragraph) is tracking videos that are "not available through the [TikTok Research] API although they are available on the platform" — i.e., this dashboard is explicitly about API completeness, not about content moderation or takedowns.
- Directly relevant to how "Error" should be read: the page's own caption under its trend chart reads verbatim: *"Note: Error are problems on our end, not TikTok."* This is the page's own characterization, not mine.
- The footer states the intended checking method as "Automated daily availability checks of selected videos," which is consistent with the record being date-granular and (outside the two gap-days) contiguous.
