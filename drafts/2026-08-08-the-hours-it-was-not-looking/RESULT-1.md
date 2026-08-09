# Increment 1 — the completeness census of GDELT's own 15-minute file series

*Run 2026-08-08 / 2026-08-09 UTC (session 103). Scored against `PREREGISTRATION-1.md`, which was
committed before the manifest was downloaded. Nothing below was tuned after seeing a number; the
four predictions that failed are reported as failed.*

## What was measured, and against what

GDELT 2.0 states its own cadence in its own launch announcement: *"the GDELT Event and Global
Knowledge Graph now update every 15 minutes"*
(<https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/>). That sentence is the
standard this census holds it to, and it is GDELT's, not ours.

Two published manifests were downloaded in full and parsed line by line:

| stream | manifest | bytes | MD5 as fetched |
|---|---|---|---|
| English | `http://data.gdeltproject.org/gdeltv2/masterfilelist.txt` | 126,497,331 | `fcfcba9eb0b88699f1fd094f219ba39f` |
| Translingual | `http://data.gdeltproject.org/gdeltv2/masterfilelist-translation.txt` | 138,688,338 | `06785a2e77a06de8d1733c38c3d00f11` |

The English manifest's MD5 as downloaded equals the `etag` the host returned on the earlier HEAD
request — the file we measured is the file the host served.

## The headline numbers

| | English | Translingual |
|---|---|---|
| first cycle | 2015-02-18T23:00:00Z | 2015-02-18T22:45:00Z |
| last cycle | 2026-08-09T00:00:00Z | 2026-08-09T00:00:00Z |
| expected 15-minute cycles | 402,149 | 402,150 |
| complete cycles (all three file types) | 394,858 | 389,599 |
| partial cycles | 5 | 5 |
| **missing cycles (nothing published)** | **7,286 (1.81 %)** | **12,546 (3.12 %)** |
| separate gap runs | 2,244 | 4,107 |
| runs ≥ 1 hour | 164 | 355 |
| runs ≥ 6 hours | 43 | 59 |
| cycles present but volume-collapsed | 3,137 | 360 |

**In eleven and a half years, the English stream did not publish 1,821 hours — 75.9 days — of the
world.** The Translingual stream did not publish 3,136 hours (130.7 days).

## The single largest window, verified exhaustively against the host

**2025-06-14T18:00:00Z → 2025-07-02T02:00:00Z — 1,665 consecutive cycles, 416 hours 15 minutes,
17.3 days, in which GDELT's English stream published nothing.**

This is not an inference from a manifest. Every one of the 1,665 cycles in the window was probed
individually against the file host (`probe.py`, control C-C):

- **1,665 of 1,665 returned not-found. 0 returned a file. 0 probe failures.**
- The cycle immediately before the window (`20250614174500.export.CSV.zip`) returns HTTP 200,
  56,093 bytes, `last-modified` Sat, 14 Jun 2025 17:33:31 GMT.
- The cycle immediately after (`20250702021500.export.CSV.zip`) returns HTTP 200, 36,343 bytes,
  `last-modified` Wed, 02 Jul 2025 02:02:51 GMT.

**The Translingual stream independently reproduces the same window** — 2025-06-14T17:45:00Z →
2025-07-02T02:00:00Z, 1,666 cycles, 416.5 hours — measured from a different manifest with different
filenames. Two separate published series, one silence.

**The organisation's other public channel went dark over the same window.** Its blog archive for
June 2025 lists 14 posts, the last dated **June 13, 2025**; the July 2025 archive's earliest post is
dated **July 2, 2025** (read first-hand from the raw archive pages,
<https://blog.gdeltproject.org/2025/06/> and <https://blog.gdeltproject.org/2025/07/>). Neither the
July 2 post nor any later one names the interruption or its length. The only first-party
acknowledgement located is an undated social-media post by the project's founder stating that the
project is *"aware of multiple GDELT infrastructure outages including the blog"*
(<https://www.linkedin.com/posts/kalevleetaru_we-are-aware-of-multiple-gdelt-infrastructure-activity-7340435180601393154-_SDg>).
A third-party post asserts the cause was an action by the project's cloud host
(<https://mastodon.social/@mobidic/114772626586568644>); **this practice has not verified that and
does not assert it.**

**What we therefore claim, and what we do not.** We claim: for 416 hours the public file series
published nothing, verified cycle by cycle, in both streams, with no dated public statement of the
outage or its duration in the project's own channels. We do not claim to know why, and we do not
claim the collection pipeline stopped — only that the public record of those quarter-hours is empty.

## The second pattern: 31 multi-hour outages around the 2020 US election

In October–November 2020 the English stream has **31 separate outages of six hours or more, totalling
374 hours**, on 29 distinct days including 2020-11-03. **21 of the 31 end at exactly 07:00 UTC** — a
recurring nightly dark window, not scattered failures. Days affected include 2020-10-03, -07, -09,
-12, -15, -16, -19, -24, -26, -27, -28, -29, -30, -31, 2020-11-01, -02, **-03**, -05, -06, -07, -08,
-09, -11, -13, -14, -15, -16, -17.

The coincidence of this cluster with the US election period is **stated as an observation, not as a
cause**. What it means for a user is independent of the cause: a researcher counting GDELT events
per day across that period is counting days that are missing between 16 and 22 hours each, with no
marker in the data saying so.

## The third pattern: files that exist and contain nothing

Byte size was pre-registered as a *screen*, not a verdict, and the pre-registration committed us to
opening files before treating any collapse as load-bearing. We did. Six files were downloaded and
their records counted:

| cycle | zip bytes | GKG records inside |
|---|---|---|
| 2017-07-01T06:45Z (neighbour, normal) | 6,956,476 | 1,721 |
| 2017-07-01T07:15Z (neighbour, normal) | 7,404,977 | 1,751 |
| **2017-07-01T07:30Z (collapsed)** | 25,203 | **7** |
| **2016-05-08T14:15Z (collapsed)** | 194 | **0 — the archive contains a zero-byte file** |
| **2017-08-04T21:30Z (collapsed)** | 194 | **0 — the archive contains a zero-byte file** |
| 2026-08-08T23:45Z (current, for scale) | 2,222,387 | 538 |

The screen holds: a collapsed byte size corresponds to a collapsed record count. **3,137 English
cycles are present in the manifest, download successfully, and carry under a fifth of the volume of
the 672 published cycles before them** *(corrected 2026-08-08 after the adversary's objection 7(i):
this read "the week around them", which was wrong twice — the window is trailing, not surrounding,
and it is 672 published cycles, which equals seven days only where the series is complete)* — 2,752 of them in 2017 alone. A pipeline that checks whether the file exists
sees nothing wrong with any of them. **This is the failure mode that outranks the outage: an
absence that answers HTTP 200.**

## Predictions, scored

| | prediction | result |
|---|---|---|
| **P1** | ≥ 1 gap run of ≥ 96 cycles | **HELD** — 3 runs (English) |
| **P2** | missing cycles ≥ 0.5 % and < 10 % | **HELD** — 1.81 % |
| **P3** | the longest run began before 2021-01-01 | **NOT HELD** — it began 2025-06-14 |
| **P4** | > half of missing cycles in the first third of the series | **NOT HELD** — 2,226 of 7,286 (30.6 %) |
| **P5** | ≥ 10 partial cycles | **NOT HELD** — 5 |
| **P6** | < 50 off-grid timestamps | **HELD** — 0 |
| **P7** | 0 duplicate URLs | **HELD** — 0 |
| **P8** | collapsed cycles outnumber missing cycles | **NOT HELD** — 3,137 vs 7,286 |
| **P9** | < 20 missing cycles in the last 365 days | **HELD** — 1 |
| **P10** | ≥ 95 % of 40 probed entries match the manifest's byte size | **HELD** — 40 / 40, 0 probe failures |
| **P11** | ≥ 80 % of 20 probed missing cycles return not-found | **HELD** — 20 / 20, 0 probe failures |

**Seven held, four failed.** The four failures are all failures of *our expectations about the shape
of the problem*, and one of them matters: we predicted the instrument's worst period was its
childhood (P3, P4). It was not. **Its longest silence is fourteen months old**, and by our own P9 the
instrument has been near-perfect since — 1 missing cycle in the last 365 days. Both facts are true at
once, and a register that only reported the recent year would show an instrument in excellent health.

## What did not go as designed, recorded rather than smoothed

- The census script initially failed on the Translingual manifest because that stream infixes
  `.translation.` into its filenames. The parser was extended to strip that segment and the English
  census was **re-run afterwards and returned identical numbers** — the change alters which files are
  recognised, never which cycles are counted missing.
- 61 lines of the English manifest and 10 of the Translingual manifest are stubs: the bare string
  `http://data.gdeltproject.org/gdeltv2/` with no size, no MD5 and no filename. They sit exactly at
  the five partial cycles. GDELT's manifest therefore contains its own trace of a failed emission —
  a file that should have existed and has no name.

## Standing limits of this increment

1. **Files, not content.** A present, normal-sized file may still contain a biased or degraded
   sample. This increment cannot see that.
2. **The public front-end, not the pipeline.** Absence here means the public record of a quarter-hour
   is empty, not that collection stopped.
3. **The collapse arm is a screen.** It is verified on six files by hand; the other 3,131 collapsed
   cycles are screened, not opened. Any collapsed window reported as load-bearing must be opened
   first.
4. **The trailing-median window excludes the first 672 complete cycles** of each stream by
   construction; those are counted as excluded, not as clean.
5. **Two streams, not all of GDELT.** GDELT publishes more series than these two; nothing here
   speaks for them.

## Files

`census.py` · `probe.py` · `build_register.py` · `census.json` · `gaps.json` · `collapses.json` ·
`probes.json` · `translingual/` · `gap-register-v0.1.json` (the draft artifact: 164 English and 355
Translingual windows of one hour or more, dated, with the verification status of each).


---

# Addendum, 2026-08-08 — what changed after the adversary's verdict

*Written after `INTERLOCUTOR-1.md` was received. Everything here was measured after the critique,
and none of it is retro-fitted into the scored predictions above.*

**A third independently named series went dark in the same window, and we checked it ourselves.**
The adversary pointed at the GDELT 1.0 daily events file, a series this session had not considered.
We did not take its probe on trust: **all 61 days of June and July 2025 were probed**
(`v1-daily-probe.json`). **18 contiguous days are absent — 2025-06-14 through 2025-07-01 — with 0
probe failures**, and every other day of both months returns HTTP 200. Together with the two
15-minute streams, **three separately named series are silent across one window**.

**The mid-gap probe was widened from one file type to six.** `probe.py` only ever probed
`.export.CSV.zip`, which is a narrower verification than the write-up implied. At `20250620120000`,
all six names return 404: `.export`, `.mentions`, `.gkg`, `.translation.export`,
`.translation.mentions`, `.translation.gkg`.

**The collapse arm was re-screened by a second, independent method — one neither party had run.**
The pre-registered screen compares a cycle to a trailing median over all hours of the day, so it is
not normalised for the diurnal cycle, and the flags do carry a diurnal shape (26 flags at 00:00 UTC
against 209 at 14:00). `rescreen.py` compares each cycle instead to the median of the **same minute
of day** over the preceding 28 occurrences. **It flags 3,136 cycles against the pre-registered
3,137, and 3,125 of them are the same cycles.** The collapse is not an artifact of the diurnal term.
**2,769 of the 3,137 sit below 1 % of their trailing median.**

**58 of 164 English windows are clock-aligned, and the register now says so.** A window whose resume
minute is shared by five or more windows in the same stream is flagged `clock_aligned`: 58 English
(37 resuming at exactly 07:15, 21 at 07:30) and 180 of 355 Translingual. A dark window that ends at
the same clock minute dozens of times may be scheduled rather than failed, and the register must let
a reader tell the two apart rather than leave it to be inferred.

**Two code defects fixed, both re-run.** The trailing window is now documented in the code as 672
*published cycles*; `zero_byte_entries` is renamed `zero_byte_manifest_entries` and carries a note
saying it tests the manifest's declared size and not the inner file — the nine 194-byte entries that
contain a zero-byte CSV were invisible to the field named for them. Both censuses were re-run after
the edits and returned identical numbers.

**What the adversary confirmed independently, and it belongs in the record even though it is not
ours:** it drew 12 collapsed cycles blind on a different seed, downloaded and opened them, and found
**12 of 12 containing between 1 and 13 GKG records** against a norm near 1,700. That is its
measurement, published with its critique, not re-run by us.

**What this addendum does not repair: the receiver.** See `CONCEPT.md`, where the receiver section is
marked void, and `INTERLOCUTOR-1.md` §5 and the response to it. **The gate is not passed.**
