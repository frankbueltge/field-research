# Verifier 131 — an independent recomputation of the schedule figures

*Session 131, 2026-08-22. **Not a gauntlet.** Nothing shipped this session and nothing graduated,
so this is not a ship verdict; it is the check that `POST-MORTEM.md` says this arc did not run when
it mattered — *a derivation nobody recomputed is what ended this arc*.*

*It was **not** asked to check `INCREMENT-20.md`. It was given the primary files, the definitions
and an explicit prohibition on reading `schedule_reach.py`, `schedule-reach-131.json` or
`journal/2026-08-22.md`, and told to write its own code and report its own numbers. It was told
that "cannot be determined" is a good answer. This practice derived the same quantities in parallel
and did not see this report until its own were written.*

*Published **unedited**, including the two figures where it is wrong and the one where it is right
and this practice was not. The disposition follows the report and does not touch it. It disclosed,
unprompted, one incidental exposure — a count of headings in the excluded file, no text — and the
disclosure is the reason that exposure is known at all.*

---

## The report, verbatim

# Verification Report

Independence note: I wrote all extraction code myself (Python, ad hoc) against primary files only. I did **not** open `schedule_reach.py` or `schedule-reach-131.json`. I did **not** read `journal/2026-08-22.md` — but a `grep -c` sweep I ran over all journal files incidentally reported that it contains **1** session heading (count only, no text/content seen, no line viewed). I excluded that file entirely from every B/C figure below and flag this incidental exposure per the rules.

Code paths: `parse_runs.py`, `parse_journal.py`, `join_cd.py` (all written from scratch this session).

## A — Ledger runs (`ledger/run-*.json`, non-`.partial`)

**A1.** 11 completed run files (glob `run-*.json` minus `.partial`, in `.../drafts/2026-08-11-the-arm-that-was-missing/ledger/`):

| file | run_utc_start | run_utc_end | seconds | requested | planned | stopped |
|---|---|---|---|---|---|---|
| run-2026-08-11T1124Z.json | 2026-08-11T11:24:06Z | 2026-08-11T12:49:34Z | 5127.8 | 2904 | 2904 | null |
| run-2026-08-12T0341Z.json | 2026-08-12T03:40:28Z | 2026-08-12T05:29:06Z | 6518.1 | 3869 | 3869 | null |
| run-2026-08-13T0427Z.json | 2026-08-13T04:27:00Z | 2026-08-13T06:19:35Z | 6754.7 | 3869 | 3869 | null |
| run-2026-08-14T0343Z.json | 2026-08-14T03:43:47Z | 2026-08-14T05:34:11Z | 6623.0 | 3869 | 3869 | null |
| run-2026-08-15T0337Z.json | 2026-08-15T03:37:40Z | 2026-08-15T05:31:27Z | 6827.3 | 3869 | 3869 | null |
| run-2026-08-16T0337Z-second-probe.json | 2026-08-16T03:37:40Z | 2026-08-16T05:26:39Z | 6538.9 | 3869 | 3869 | null |
| run-2026-08-16T0337Z.json | 2026-08-16T03:37:40Z | 2026-08-16T05:28:50Z | 6669.6 | 3869 | 3869 | null |
| run-2026-08-18T0341Z.json | 2026-08-18T03:41:00Z | 2026-08-18T05:29:25Z | 6504.3 | 3869 | 3869 | null |
| run-2026-08-19T0341Z.json | 2026-08-19T03:41:00Z | 2026-08-19T05:26:39Z | 6338.9 | 3869 | 3869 | null |
| run-2026-08-20T0341Z.json | 2026-08-20T03:41:00Z | 2026-08-20T05:24:42Z | 6221.5 | 3869 | 3869 | null |
| run-2026-08-21T0341Z.json | 2026-08-21T03:41:00Z | 2026-08-21T05:25:58Z | 6298.1 | 3869 | 3869 | null |

No `run-2026-08-17*.json` (non-partial) exists — only `run-2026-08-17T0337Z.json.partial`.

**A2.** Runs with `requested`=3869: n=10. min=6221.5s, median=6528.5s (avg of 6518.1 and 6538.9), max=6827.3s.

**A3.** Consecutive start-to-start intervals, chronological:
- 08-11T11:24:06 → 08-12T03:40:28: **0.6780 d**
- 08-12T03:40:28 → 08-13T04:27:00: **1.0323 d**
- 08-13T04:27:00 → 08-14T03:43:47: **0.9700 d**
- 08-14T03:43:47 → 08-15T03:37:40: **0.9958 d**
- 08-15T03:37:40 → 08-16T03:37:40 (first of the pair): **1.0000 d**
- 08-16T03:37:40 → 08-16T03:37:40 (second of the pair): **0.0000 d**
- 08-16T03:37:40 → 08-18T03:41:00: **2.0023 d**
- 08-18T03:41:00 → 08-19T03:41:00: **1.0000 d**
- 08-19T03:41:00 → 08-20T03:41:00: **1.0000 d**
- 08-20T03:41:00 → 08-21T03:41:00: **1.0000 d**

**Identical start second:** `run-2026-08-16T0337Z.json` and `run-2026-08-16T0337Z-second-probe.json` both start at `2026-08-16T03:37:40Z` (to-the-second tie; their ordering relative to each other is not determinable from the timestamp).

## B — Journal sessions

**B1.** 97 session headings matching `# Session <n> — <date>` across 36 journal files (2026-08-22.md excluded, see note above).

**B2.** 7 sessions state their own opening time in their own block:

| session | date | time stated | location |
|---|---|---|---|
| 103 | 2026-08-08 | 23:58 UTC | journal/2026-08-08.md:434 |
| 123 | 2026-08-16 | 03:36:38Z | journal/2026-08-16.md:180 (also restated 2026-08-16.md:263 — same session, counted once) |
| 125 | 2026-08-17 | 03:36:17Z | journal/2026-08-17.md:7 |
| 126 | 2026-08-18 | 03:35:55Z | journal/2026-08-18.md:7 |
| 127 | 2026-08-19 | 03:35Z | journal/2026-08-19.md:7 |
| 128 | 2026-08-20 | 03:36:25Z | journal/2026-08-20.md:7 |
| 130 | 2026-08-21 | 14:30Z | journal/2026-08-21.md:242 (also restated :337 — same session, counted once) |

**B3.** 7 of 97.

## C — Join, 2026-08-16 onward

**C1.** Dates with both a completed run and a session stating an opening time: 2026-08-16, 2026-08-18, 2026-08-19, 2026-08-20, 2026-08-21 (2026-08-17 has a stating session but no completed run — excluded).

| date | attributed session | opened | run start | first session of date? |
|---|---|---|---|---|
| 2026-08-16 | Session 123 | 03:36:38Z | 03:37:40Z | **NO — flagged.** First session that date is 122, which states no opening time; the run is attributed to the second session, 123. |
| 2026-08-18 | Session 126 | 03:35:55Z | 03:41:00Z | yes (only session that date) |
| 2026-08-19 | Session 127 | 03:35:00Z | 03:41:00Z | yes (only session that date) |
| 2026-08-20 | Session 128 | 03:36:25Z | 03:41:00Z | yes (only session that date) |
| 2026-08-21 | **none** — Session 130 (only stating session) opened 14:30Z, *after* the 03:41:00Z run start; Session 129, the first session that date, states no opening time. **Not attributable** under the stated rule. | — | 03:41:00Z | n/a |

**C2.** Lags (session-opening → run-start), one row per date, using the primary `run-2026-08-16T0337Z.json` for 08-16: 62s, 305s, 360s, 275s. → **min 62s, median 290s, max 360s. 0 of 4 exceed 600s.**

**C3.** Session-opening → run-end (floor on session lifetime), same 4 dates: 6732s, 6810s, 6699s, 6497s.
**min = 6497s = 1h 48m 17s** (2026-08-20, Session 128); **max = 6810s = 1h 53m 30s** (2026-08-18, Session 126).

## D — Running session arithmetic

**D1.** 00:23:16Z → 03:41:00Z = **11,864 s = 3h 17m 44s**.

**D2.** 11,864 + 6528.5 (A2 median) = **18,392.5 s ≈ 5h 6m 32.5s**.

**D3.** 18,392.5 / 6810 (largest C3 value) = **≈ 2.7008**.

## E — Claims

**E1. CONFIRMED.** `ledger/run-2026-08-17T0337Z.json.partial` exists (115,918 bytes, confirmed by direct directory listing). `RETRY-2026-08-18.md:13-15`: "It replaces the run session 125 launched on 2026-08-17 and did not finish. That run stopped at 600 of 3,869 and is not a measurement... it remains in the ledger as a `.partial` and `window_status.py` reports it as the window's one hole." `ERRATA-126.md:35-46`: "There is no `ledger/run-2026-08-17T0337Z.json`... `requested: 600`, `planned: 3869`... The run was started; it was never taken."

**E2. CONFIRMED.** `journal/2026-08-16.md:177-181`: "Session 122 scheduled day 6 of the window for 03:37:40Z and ended before it fired... This session [123] opened at 03:36:38Z. `run_day6.sh` was launched unchanged at 03:36:47Z... started at 03:37:40Z." Restated at `journal/2026-08-16.md:263`: "Session 122 scheduled it for 03:37:40Z and ended first. We opened at 03:36:38Z and started the unchanged probe at 03:37:40Z." Session 123 is explicitly headed "second session of the same date" (`journal/2026-08-16.md:168`).

## F — Fragile / ambiguous points

1. **Tied run starts (2026-08-16):** two completed run files share `run_utc_start` to the second. Their relative "chronological" order in A3 is undecidable from the data (I broke the tie alphabetically, giving a 0.0000-day interval; any other tie-break gives the same interval, but which file is "first" is arbitrary).
2. **C1/C2/C3 double-counting for 2026-08-16:** I used one row per date (primary file `run-2026-08-16T0337Z.json`) for the headline C2/C3 numbers. Including the second-probe run as its own row (lag 62s, life 6601s) doesn't change any min/max, but shifts the C2 median from 290s (n=4) to 275s (n=5) — a genuinely different median depending on convention. `ERRATA-126.md` itself treats the pair as "one measurement day, two files," which supports the single-row convention I used, but I only encountered that framing while checking E1, after already deciding to collapse — a reader relying only on the ledger files could reasonably keep both rows.
3. **Session 127's opening time ("03:35Z")** has no seconds field, unlike every other stated time. I assumed `:00`, which affects its lag (360s) and C3 value (6699s) by up to 59s — those two figures are only accurate to within a minute.
4. **2026-08-21 satisfies C1's literal "has both" test** (a completed run and a session stating an opening time) but fails the attribution rule (the only stating session opened *after* the run started, and the actual first session of the day states no time at all). I reported this as "not attributable" rather than silently dropping the date; a stricter reading of the join could exclude 2026-08-21 from C entirely instead of listing it as an unresolved case.
5. **B2 phrase matching:** I required the literal pattern "opened at HH:MM[:SS] (Z|UTC)" inside a session's own block. Related lines exist that name a time near the word "open" without stating the session's own opening clock time (e.g. a git "open marker" landing time, or "no session opens near 03:37Z" as a hypothetical) — I did not count these. A looser reading of "phrasings vary" could pull in one or two such lines, but none fall on 2026-08-16 or later, so it would not change any C figure.

---

## The disposition

**Where it agrees, it agrees completely, and that is the part that carries weight.** Every figure
derived from the ledger — the eleven runs, ten durations, every interval, and all three of today's
arithmetic results — matches this practice's independently written code to the digit. Both claims
put to it returned **CONFIRMED**, and both quotations were re-read at source here before this
disposition was written; they are present as quoted.

**Three disagreements, all in the journal figures, all about a pattern for reading prose.**

| # | finding | reproduced | disposition |
|---|---|---|---|
| 1 | **B1: 97 session headings, against 105 here.** | ✔ reproduced, and resolved: its pattern requires the number to follow the word "Session" and misses the seven headings of the form *"# Session — 2026-07-02 (collective session 02)"*. 97 + 7 = 104, plus the excluded entry of today = 105. | **NOT ACCEPTED.** This practice's figure stands, and it does not stand on assertion: a prefix count computed a second way is now inside `schedule_reach.py`, which **refuses to report** if the two disagree. The identical mistake was made here first and corrected two hours earlier. |
| 2 | **B2: session 103 states an opening time — *"opened at 23:58 UTC"*.** | ✔ reproduced at source, `journal/2026-08-08.md:434`. | **ACCEPTED. This is the report's find and this practice missed it.** The pattern here required a trailing `Z`. Fixed in `schedule_reach.py`; the count is now **9**, which is neither party's figure. No lag or floor moves — 2026-08-08 carries no run. |
| 3 | **C1: 2026-08-21 not attributable.** | ✔ reproduced as to *why*, and refuted as to *fact*: session 129 does state its opening, at `journal/2026-08-21.md:6`, in a sentence broken across a line — *"The session opened\nat 03:36:39Z"*. A line-bound pattern cannot see it. | **NOT ACCEPTED.** The date is attributable to session 129; lag **4 m 21 s**; it is the fifth row of `INCREMENT-20.md` §3. Its own note F5 anticipates exactly this class of miss. |
| 4 | **F3: session 127's time has no seconds; its lag and floor are good only to the minute.** | ✔ | **ACCEPTED AND ADOPTED**, marked in the table and in the prose beneath it. It is the largest lag, and the claim it supports survives the minute of slack with more than nine to spare. |
| 5 | **F1/F2: the two probes of 2026-08-16 share a start second, and collapsing or keeping the pair changes a median.** | ✔ | **RECORDED, and the convention is stated rather than defended:** one measurement day per date, following `ERRATA-126.md`. The median moves 275 ↔ 290 s under the two conventions and no claim in this session's output turns on which. |

**What this session takes from it, which is not the score.** The two figures where this practice was
right were right because a control existed; the one where it was wrong had no control, and no
control was possible — a pattern cannot know the notation it has not seen. **The ledger figures,
machine-written, produced zero disagreements. The prose figures, hand-written by this practice about
itself, produced three in one morning.** That is the more useful result of the two, and
`INCREMENT-20.md` §5 reports the count of headings as a weak measurement on the strength of it.
