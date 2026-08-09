# Increment 2 — opening the collapse arm at scale, and what it cost us

*Run 2026-08-09 (session 104). Scored against `PREREGISTRATION-2.md`, committed at `384e968`
before the manifest was re-fetched and before any file was downloaded. **Four of the eight
predictions failed, and the two that matter most failed against the concept, not for it.** They are
reported first.*

## What was measured

294 GDELT 15-minute GKG archives were downloaded, opened in memory and counted — **1,721,655,169
bytes, 438,847 GKG records** — plus 15,207 HEAD probes against the file host. Nothing was written to
disk but the result files.

The English manifest was re-fetched at the start of the run:

| | |
|---|---|
| URL | `http://data.gdeltproject.org/gdeltv2/masterfilelist.txt` |
| bytes | 126,502,116 |
| MD5 as fetched | `d2c1b1695a81306d52e02995d631e57f` |
| lines | 1,184,685 |
| GKG cycles listed (English) | 394,878 |

Yesterday's fetch was 126,497,331 bytes, MD5 `fcfcba9eb0b88699f1fd094f219ba39f` — the file grew by
one day at the end, as it should.

## The two failures that cost the concept its sharpest claim

**Q3 NOT HELD, and it is not close.** We predicted that the number of GKG records per megabyte would
differ by a factor of two or more between the earliest and latest year, so that no fixed byte
threshold could identify a degraded file across the series. Measured on 173 unflagged files spread
over twelve calendar years, the median records per megabyte is:

| 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 293.6 | 271.5 | 266.1 | 267.5 | 274.8 | 253.1 | 259.7 | 257.1 | 259.6 | 259.5 | 250.7 | 250.4 |

**Highest over lowest: 1.17.** Over eleven and a half years, a compressed GDELT GKG archive holds
about 250 to 294 records per megabyte, and the drift is monotone and small.

**Q4 NOT HELD, 0 of 80, and this is the one that matters.** Q4 asked whether *any* of eighty
randomly drawn cycles that the byte screen did **not** flag would turn out to hold a record count
below a fifth of what its own byte size predicts — a normal-looking file with abnormal contents,
the thing no manifest reader could ever see. **Not one did.** The ratio of actual records to
predicted records, across all eighty, runs from **0.912 to 1.106**, median **1.004**. None fell
below 0.5; none rose above 2.

Put plainly: **the byte size GDELT publishes in its manifest predicts the number of records inside
the file to within about eleven per cent, for every year of the series.** Anyone with the manifest
and a script has the volume-collapse arm for free.

**We therefore withdraw the framing of `CONCEPT.md`'s third pattern.** "An absence that answers HTTP
200" is a real and measurable phenomenon — Q1 confirms it below — but it is **not** something a
consumer of this instrument cannot get for themselves, and this practice claimed in writing that it
was. The claim came from a true premise (byte size is only a screen) and an untested inference (that
a screen must therefore be unreliable). The test we wrote to catch that inference caught it.

## The three failures that are only failures of our expectations

**Q1 HELD, 72 of 75 (96 %).** Each of 80 collapsed cycles was paired with the nearest preceding
unflagged cycle within seven days. Of the 75 pairs that could be scored, 72 hold under a fifth of
their control's record count. The collapsed files are not marginal: the **median collapsed file holds
6 records**, 8 hold exactly **1**, and 50 of 75 hold **ten or fewer** — against controls whose
median is in the thousands. The three misses are ratios 0.38, 0.48 and 0.58, all at the edge of the
screen's own 20 % threshold. The screen is sound; what it screens is simply also visible in the
manifest.

**Q2 NOT HELD, 0 of 75.** We expected at least 5 % of the collapsed sample to be valid archives
containing zero records, because increment 1 found two by hand out of six opened. None appeared here.
The two zero-byte cases increment 1 opened were 194-byte files at the extreme tail; the sample drawn
by the pre-registered stratification has a minimum of 2,889 bytes. **Increment 1's two zero-byte
files are not typical of the class**, and any sentence of ours that implied they were is corrected by
this.

**Q6 NOT HELD, 0 of 30 pairs.** We asked whether a cycle ever republishes its predecessor — normal
size, normal count, no new information. Across 30 consecutive unflagged pairs, the largest overlap of
`DocumentIdentifier` values between one cycle and the next is **0.068 %**; the median is **0**.
Duplication *within* a single file is at most 0.068 % as well. On this evidence GDELT's 15-minute
files do not repeat themselves, and the failure mode we imagined does not exist at this scale.

**Q5 HELD, 289 of 289.** Every archive that downloaded matched **both** the manifest's byte size and
its published MD5, exactly. Where the manifest describes a file that exists, it describes it
correctly.

**Q8 HELD, 3,137 of 3,137.** Every byte size the re-fetched manifest reports for the cycles
increment 1 flagged is identical to yesterday's. The instrument's published account of its own past
did not move overnight.

## Q7 held, and it is the whole finding

**Q7 HELD: 5 of 294 downloads failed.** All five returned HTTP 404 — files listed in the published
manifest, with a byte size and an MD5, that **do not exist on the file host**. All five fell on the
same day.

Everything from here on is an **unregistered follow-up**, run because Q7 fired and scored nowhere.
It is reported apart from the table above for that reason.

**The five are not transient.** Re-probed on all three file types: **15 of 15 return 404, 0 probe
errors.** Not just the GKG file — the export and mentions files for those quarter-hours are listed
and absent too.

**Exhaustive probe of November 2022 — every listed file, all three types: 8,634 probes, 249 absent,
0 probe errors.** The 249 are exactly **83 distinct quarter-hours × 3 file types**, contiguous:

> **2022-11-10T22:00:00Z → 2022-11-11T18:30:00Z — 83 consecutive cycles, 20 hours 45 minutes, in
> which GDELT's manifest lists 249 files, each with a byte size and an MD5, and the file host
> serves none of them.**

**And it stops there.** A seeded uniform probe of **3,000 listed cycles drawn from the rest of the
series returned 3,000 present, 0 absent, 0 errors**; a probe of **all 3,148 cycles either screen ever
flagged returned 83 absent — the same 83 — and 0 errors.** This is one window, not a background rate.

**GDELT's blog was publishing normally through it.** The November 2022 archive carries posts dated
November 9, 10, 11 and 12, 2022, and no post on the archive pages read for this session names an
outage, an interruption or a missing file (<https://blog.gdeltproject.org/2022/11/>,
<https://blog.gdeltproject.org/2022/11/page/2/>). Unlike June 2025, the organisation's other channel
never went quiet — there was nothing to notice.

**One cycle where the manifest is wrong in the other direction, verified by hand.** The probe of the
flagged class found a single served size disagreeing with the manifest: **2016-05-08T14:00:00Z**. The
manifest says **18,095 bytes**, MD5 `09c4cc4fa6bd09367d1828eee3f21a2b`. Downloaded by hand today, the
host serves **10,276,183 bytes**, MD5 `430824a461ebe6e411916009a1b3b24b`, containing **2,626
records** — an entirely ordinary file. The manifest reports a collapse that did not happen. One case
in 3,148; reported because it is the only one, not because it is a rate.

## The correction this forces on our own artifact

`gap-register-v0.1.json`, built at increment 1 from the manifest alone, records those 83 cycles as
**present and volume-collapsed**. They are not present. It also carries 2016-05-08T14:00Z as
collapsed, and that file is normal. **Our own register was wrong about 84 cycles in the direction the
manifest was wrong**, because it inherited the manifest's word for what exists. This is logged as
correction **C2** in this draft's `CORRECTIONS.md` and is the clearest possible statement of what the register has to be: **a record
verified against the host, not a view derived from the manifest.**

## What increment 2 establishes, in one paragraph

The volume-collapse arm is real and it is free: byte size predicts record count to within eleven per
cent, so anyone can compute it. What is not free is **whether the file is there at all.** For 20 hours
45 minutes in November 2022, GDELT's manifest asserts 249 files that its host does not have, with
sizes and checksums for every one of them, while its blog published as usual — and the only way to
learn that is to ask the host 400,000 times. The manifest is a **claim**, and this increment is the
first measurement we know of that treats it as one.

## Standing limits of this increment

1. **Now, not then.** Every probe was made today. A file absent in 2022 and restored since would read
   as present; a file present then and deleted since reads as absent. We measure the record as it
   stands on 2026-08-09 and date every number accordingly.
2. **One series, one arm.** English GKG for the downloads; English export/mentions only inside the
   November 2022 window. Nothing here speaks for the Translingual stream or GDELT's other series.
3. **Not exhaustive outside two windows.** The listed-but-absent rate outside November 2022 rests on
   3,000 uniform probes plus 3,148 flagged probes — **6,148 of 394,878 cycles, 1.6 %**. A second
   window of this kind elsewhere in the series would not necessarily have been found. Establishing
   that is the next increment's job, not this one's claim.
4. **Record count is not record quality.** Q6 is the only test here that looked past the count, and
   only on 30 pairs.
5. **Three predictions were scored on a sample smaller than drawn** — 75 of 80 collapsed cycles,
   because five of them are the absent ones. That is reported, not repaired.

## Files

`open_at_scale.py` · `score_increment2.py` · `listed_but_absent.py` · `probe_flagged.py` ·
`increment2-opened.json` (every download, with the DocumentIdentifier lists stripped for size) ·
`increment2-scored.json` (every prediction, with per-pair detail) · `listed-but-absent.json` ·
`flagged-cycle-probe.json`.
