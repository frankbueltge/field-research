# Increment 20 — the hour the instrument cannot reach

> **THE TITLE IS REFUTED — `ERRATA-131.md` E36.** It could. The compliant run was launched at
> 03:41:00Z and closed at 05:30:09Z, **3,869 of 3,869**, in a session that ran five hours and seven
> minutes; this session's own filed bet said it would not, and **lost**. The title is left standing
> with this note under it rather than edited away, because a file that silently renames itself after
> being wrong is a file whose earlier state cannot be checked. Read every "out of reach" below as
> refuted, and `DAY11-2026-08-22.md` for what actually ran.

*Session 131, 2026-08-22. **Not a gauntlet, nothing shipped, nothing graduated, no packet at any
status.** Every figure on this page is read from `schedule-reach-131.json`, written by
`schedule_reach.py` from files already committed to this repository. Nothing here is typed, and
nothing here was fetched from the network.*

## 0. What licensed this, and what it is not

`CONDITIONS-128.md` stops this arc from producing delivery objects before 2026-09-05.
`CONDITIONS-129.md` leaves one live item — *"The daily instrument keeps running"* — and names its
hour: *"day 11 is due at 03:41:00Z."*

This session opened at **00:23:16Z**, three hours and eighteen minutes before that second. So the
one thing it is licensed to do lies, by arithmetic, on the far side of any session this record
documents. **[REFUTED the same day — `ERRATA-131.md` E36. It lay on the far side of every session
the record documented *at the time of writing*, and this session then ran longer than all of them
and delivered the day. The arithmetic below is correct; this inference from it was not.]** This increment is the instrument's own schedule, measured. It builds nothing to send,
repairs none of the ninth gauntlet's fifteen findings, and touches no file under `offer/`.

**It is not a claim about an effect of the hour on what the probe measures.** Start hour and
calendar date cannot be separated in this record — each run belongs to one date, and no two dates
were ever measured at deliberately different hours — so nothing here or anywhere else can tell the
two apart, and nothing is attempted. The quantity below is a different one and it is
not confounded: the distance between two recorded timestamps.

## 1. The one decision that could not wait, and it went against this session

At **00:24:56Z**, before any role was convened, this session reserved the day at an hour it could
reach — **00:41:00Z**, an interval of 0.875 days instead of 1.0000. The reservation holds without
measuring and dies reversibly, which is why it was taken first: `run_window_day.py` reserves before
its hold, and a killed hold leaves *"a hole honestly available to be filled, not a phantom lock."*

An adversary was convened on that single question and returned **VIOLATES** (`INTERLOCUTOR-131.md`,
published unedited). The reservation was killed at **00:29:44Z**, twelve minutes before it would
have started, and **no measurement was taken at the re-anchored hour**.

The verdict's decisive limb is not textual. Twenty-four hours earlier this practice refused to write
a private text file no stranger would ever see, and published the reason twice; a day before that, a
public page was refused on the same ground. *A stop under which the private draft is forbidden and
the convenient rescheduling is permitted is not a stop with a principle in it.* Accepted in full.

**And the fact that cuts against this session's own compliance is stated here rather than left
out:** a 0.875-day interval would have been unremarkable in this series. Its own intervals run
**0.678 · 1.0323 · 0.97 · 0.9958 · 1.0 · 2.0023 · 1.0 · 1.0 · 1.0** days. The re-anchor was refused
on the licence's wording and on the asymmetry, **not** because it would have damaged a measurement,
and this practice does not get to claim the stronger reason afterwards.

## 2. Method

`schedule_reach.py` reads two committed sources and joins them.

- **The runs.** The eleven completed files under `ledger/run-*.json`. A `.partial` is never a run
  and none is read.
- **The openings.** The journals' own text. Each journal is split at its `# Session` headings and
  the first opening time stated inside each session's own block is extracted **by pattern, not
  transcribed**, with the file and line it came from carried beside it.

A run is attributed to the session whose stated opening is the **latest one at or before the run's
start second** — not to the first session of its date. That rule is not decoration; §4 is what it
was written for.

**Three defects of this instrument, all found and fixed this morning before any figure was written
down, all recorded in the source. Two were found here; the third was not:**

1. The first version returned one row per *mention* of an opening time, so a session that states
   its own opening twice (session 123 does, session 130 does) was counted twice. A date with three
   sessions was reported as having two.
2. The heading pattern then missed **seven** headings of the form *"# Session — 2026-07-02
   (collective session 02)"*, and its replacement still missed **five** more. Found by counting the
   headings a second way — a plain prefix count — and comparing. **That control is now inside the
   script and it refuses to report at all if the two counts disagree.** They agree at **105**.
3. **A third defect, and this one was not found here.** The opening-time pattern required the
   clock to end in `Z`, so it missed session 103's *"The session opened at 23:58 **UTC** on
   2026-08-08"* (`journal/2026-08-08.md:434`). Found by the independent recomputation of §5, whose
   own pattern accepted both. Fixed; the count in §3 is the corrected one. **This is a defect in the
   instrument this file is built on, found by someone else, on the morning this file was written.**

## 3. What the record says

**Of 105 session headings in `journal/`, exactly 9 state the time the session opened.** Eight of
the nine fall on 2026-08-16 or later — the convention is seven days old — and the ninth is session
103 of 2026-08-08, which states its opening for an unrelated reason: it opened at 23:58 UTC and ran
past midnight, so it had to say which date it belonged to. Entries other than these nine state no
opening time and are reported as unknown rather than guessed. A further limit, stated because it
bounds what could be checked: the working copy is a **shallow clone reaching back only to
2026-08-19**, so commit timestamps were not available as a substitute and were not used.

**Six dates carry both a stated opening and a completed run** — five when this section was first
written, and **this session is now the sixth**, because `schedule_reach.py` reads the journals and
the ledger and this session put an entry in one and a run in the other. The table below is the
re-run output, not the original.

| session | opened | run started | lag | session lived at least |
|---|---|---|---|---|
| 123 | 2026-08-16T03:36:38Z | 03:37:40Z | **1 m 02 s** | 1 h 50 m 01 s |
| 126 | 2026-08-18T03:35:55Z | 03:41:00Z | **5 m 05 s** | 1 h 53 m 30 s |
| 127 | 2026-08-19T03:35**:00**Z | 03:41:00Z | **6 m 00 s** | 1 h 51 m 39 s |
| 128 | 2026-08-20T03:36:25Z | 03:41:00Z | **4 m 35 s** | 1 h 48 m 17 s |
| 129 | 2026-08-21T03:36:39Z | 03:41:00Z | **4 m 21 s** | 1 h 49 m 19 s |
| **131** | **2026-08-22T00:23:16Z** | **03:41:00Z** | **3 h 17 m 44 s** | **5 h 06 m 53 s** |

> **The claim this paragraph carried is now false, and the instrument says so before this prose
> does.** It read: *"Every lag is under ten minutes. Minimum 62 s, median 275 s, maximum 360 s."*
> With today's row included, `schedule-reach-131.json` reports **n = 6, minimum 62 s, median 290 s,
> maximum 11,864 s, and `all_within_ten_minutes: false`.** The counterexample is **this session**.
> `ERRATA-131.md` E36.

**What is true, stated so that today's row cannot be quietly folded in with the others.** On the
**five dates before today**, every lag was under ten minutes — 62 s to 360 s. **Today's lag is
3 h 17 m 44 s, and it is a different thing**: those five sessions opened and the hour was minutes
away; this one opened and **waited** for an hour that was three hours away. A table that averages
the two is describing two different behaviours as one.

**Session 127's row is accurate only to the minute** and is marked in the table: its entry states
*"03:35Z"* with no seconds, the only such row in this table (sessions 103 and 130 also state
minutes only, and neither carries a run). Its lag and its floor are each uncertain by up to
59 s. That is the largest lag in the table, so the sentence above survives the uncertainty with more
than nine minutes to spare — but the figure is not to the second and is not printed as though it
were. The uncertainty was named by the independent recomputation of §5 and is adopted from it.

The last column is a **floor, never a length**: the session wrote the closed run file, so it lived
at least that long. The five earlier floors sit inside a five-minute band, **1 h 48 m 17 s to
1 h 53 m 30 s** — close to the probe's own duration, because in those five the run is very nearly
the whole session. **Today's floor is 5 h 06 m 53 s**, and it is now the longest session span in the
record. It exceeds the **5 h 06 m 32 s** this file forecast as *required* by twenty-one seconds —
the forecast used the median probe duration and today's probe ran 6,548.4 s against that median of
6,528.5 s.

**The probe, over ten full-panel runs:** minimum **6,221.5 s**, median **6,528.5 s**, maximum
**6,827.3 s** — one hour forty-four to one hour fifty-four.

## 4. The finding

> **WITHDRAWN THE SAME MORNING, before this file left the drafts directory —
> `ERRATA-131.md` E34.** This section first read: *"The instrument's 'daily hour' was never an
> independently chosen parameter. It is wherever the session already was… It moved when the sessions
> moved."* **That asserts a direction of causation the evidence here cannot test, and the record
> contains a case against it.** On all five checkable dates the hour had already been named by an
> earlier session — 03:37:40Z was set by session 122 *before* session 123 opened and aimed at it —
> so a lag of one to six minutes is exactly what a session **aiming at a fixed hour** produces, and
> is equally consistent with the arrow running the other way. The dates on which the hour actually
> moved (2026-08-11 to 2026-08-15) state **no** opening times, so the mechanism cannot be
> established from this record at all. Found by this session's own hostile critic
> (`CRITIQUE-131.md`), accepted without argument, marked in place rather than rewritten. What
> survives is below and does not need the arrow.

**What the five dates establish, and it is less than the sentence above claimed.** On every date
this record can check, the run started **between one and six minutes after the session opened** —
and on all five, at an hour a previous session had already named. So: **the sessions and the hour
have been within six minutes of each other on every occasion the record can check, however that
came about.**

**What follows from that without any claim about which set which** — and it is the part the decision
turns on: **a run happens only if a session is alive across it.** The probe takes a median of
6,528.5 s. Whether the hour was chosen to suit the sessions or the sessions arrived to suit the
hour, **the measurement is hostage to a session lifetime this practice does not set**, and the
record shows that hostage-taking collecting three times in seven days.

**Three occurrences in seven days, and only the first is famous.**

- **2026-08-16.** Session 122 scheduled the day's run for 03:37:40Z and **ended before it fired**,
  writing that if nothing followed, *"day 6 is a hole — scheduled, not skipped."* Session 123 —
  a different session of the same date — opened at 03:36:38Z, **sixty-two seconds** before the
  hour, and caught it. The day survives because a second session happened to open one minute
  before the scheduled second. That is luck, and the attribution rule in §2 exists so this file
  cannot quietly credit it to session 122.
- **2026-08-17.** Session 125 launched day 7 at 03:37:40Z and the run **stopped at 600 of 3,869**
  when the session ended. It is not a measurement; it sits in the ledger as a `.partial` and is the
  series' one hole (`RETRY-2026-08-18.md`, `ERRATA-126.md` E21).
- **2026-08-22, today.** The session opened **3 h 17 m 44 s** before the hour. Delivering day 11 at
  the licensed second requires a session of **5 h 06 m 32 s** — wait plus the median probe —
  against a longest documented span of 1 h 53 m 30 s. **A factor of 2.7.** **[The forecast was
  right and its conclusion was wrong — `ERRATA-131.md` E36. The run closed at 05:30:09Z after a
  session of five hours seven minutes: the required span was met, not missed, and this date is NOT
  a third failure. It belongs in the list only as the case where the risk was seen in advance and
  the day was taken anyway.]**

The first was rescued by coincidence, the second was discovered after the fact, and the third is
**visible in advance**. That is the only thing that has improved.

## 5. The independent recomputation, and it went three ways

*What ended this arc was a derivation nobody recomputed. So a second party was given the primary
files, the definitions, and a hard instruction not to read this script or its output, and told to
write its own code and report its own numbers. It did (`VERIFIER-131.md`, published unedited). It
disclosed on its own initiative that a `grep -c` sweep had incidentally told it how many session
headings today's journal contains — a count, no text — and that it excluded that file from every
journal figure in consequence.*

**Everything from the ledger agreed to the digit.** All eleven runs, their start and end seconds,
their durations, `requested`, `planned`, `stopped`; the ten full-panel durations at **6,221.5 /
6,528.5 / 6,827.3 s**; every interval in the series; today's arithmetic at **11,864 s**,
**18,392.5 s** and a ratio of **2.70**; and the two session-lifetime floors at **1 h 48 m 17 s** and
**1 h 53 m 30 s**. Both claims put to it — the 2026-08-17 hole and the 2026-08-16 rescue — came back
**CONFIRMED**, each with a quotation this practice then re-read at source.

**Everything from the journals disagreed, in three places, and the score is two to one.**

| # | disagreement | who was right |
|---|---|---|
| 1 | **Session headings: 97 against 105.** | **This practice.** The recomputation used a pattern requiring the number to follow the word — the same mistake made and corrected here two hours earlier — and missed the seven headings of the form *"# Session — 2026-07-02 (collective session 02)"*. 97 + 7 = 104, plus today's entry, which it deliberately excluded, = **105**. Demonstrable with a prefix count, which is why that control now sits inside the script. |
| 2 | **Sessions stating an opening: 7 against 8.** | **The recomputation.** It found session 103's *"opened at 23:58 UTC"*, which this script's `Z`-only pattern could not see. Corrected; the count is now **9**, and neither party had it. |
| 3 | **2026-08-21 attributable, or not.** It reported the date **not attributable** — session 129 states no opening, session 130 opened after the run. | **This practice.** Session 129 does state it, at `journal/2026-08-21.md:6`: the sentence is broken across a line — *"The session opened\nat 03:36:39Z"* — and a line-bound pattern cannot see it. The date is attributable to session 129, its lag is **4 m 21 s**, and it is the fifth row of §3's table. |

**What this changes in §3 and §4: nothing.** The lags are 62, 305, 360, 275 and 261 seconds either
way; the recomputation's own n=4 set gives a median of 290 s and this file's n=5 set gives 275 s,
and both are inside ten minutes with four minutes to spare. **What it changes in the instrument is
one real defect**, listed as the third in §2.

**The honest reading of the score, and it is not a boast.** Every disagreement was a disagreement
about a *pattern for reading prose*, and each of the three was one party's pattern being narrower
than the record. Two ran the other way this time; in the three panels before this one they ran
mostly against this practice. **A count of prose that two independent patterns disagree about three
times in one morning is a weak measurement, and this file says so rather than reporting the number
that survived.** The ledger figures, where the data is machine-written, did not disagree once.

## 6. The reflexive turn — cut back, because it was doing more work than it had earned

> **CUT THE SAME MORNING — `ERRATA-131.md` E35.** This section first claimed that
> `CONDITIONS-129.md`'s *"day 11 is due at 03:41:00Z"* is a cadence statement of *"the same class"*
> as the receiver's frozen dashboard. **The hostile critic's charge is accepted:** softening *same
> failure* to *same class* keeps the rhetoric — *we found our own hypocrisy* — while dropping the
> only thing that made the receiver's case worth nine gauntlets, which is that **an external party
> was misled**. Nobody outside this house ever read `CONDITIONS-129.md`, and nothing turned on it
> but this session's own inconvenience. What is left is the plain fact, without the parallel.

`CONDITIONS-129.md` named an hour for a session that had not opened yet, and the session that opened
had to wait three hours and eighteen minutes for it — **and did**. **It is not the same finding as
the receiver's dashboard and this file no longer says it is.** *(This paragraph first ended "could
not reach it": refuted the same day, `ERRATA-131.md` E36.)*

## 7. What is not this session's to decide

Three courses exist and **none of them is a session's to take alone under the stop**: re-anchor the
instrument to an hour the sessions can reach; leave the hour and accept that days go dark whenever
the schedule does not line up; or hold the schedule near the hour, which is not this practice's to
do at all, since the schedule is external to it.

Put to the architect in `REQUESTS.md` with these figures. **Until then the hour stands as
`CONDITIONS-129.md` wrote it, and a day the session cannot reach is recorded as a hole and not
filled by a substitute.**

**And the question is now less urgent than this section made it sound** (`ERRATA-131.md` E36).
Day 11 was delivered at the licensed second by a session that simply waited. Waiting is not free —
it cost this session five hours it could not have known in advance it would be given — but the
choice is no longer "re-anchor or go dark". It is: **re-anchor, wait, or go dark**, and the middle
option has now been demonstrated once. That strengthens the case for leaving the hour where it is.

## 8. The attempt, scored

Claiming a thing is out of reach without trying is the sort of sentence this arc has been failing
gauntlets on for two weeks. So the compliant run was launched — **reserved at 00:36:20Z, held to
03:41:00Z**, at the hour the licence names and no other.

**It closed.** 03:41:00Z to 05:30:09Z, **3,869 of 3,869**, 6,548.4 s, no stop, vantage AS396982,
interval **1.0000 days**, **zero apparent transitions** — the first empty interval in the series.
Full record: `DAY11-2026-08-22.md`.

**This session's bet said it would not close, and the bet is LOST** — which the bet itself named, in
advance and in writing, as the better of its two outcomes. Everything in this file built on the word
*"cannot"* is refuted by it (`ERRATA-131.md` E36), including the title, and the refutation is marked
at twelve sites rather than tidied away.

**What the attempt was actually worth.** Not the day, which is one measurement among eleven and
scores no pre-registered test. **The forecast.** This file computed that the run needed
**5 h 06 m 32 s** and the session that delivered it ran **5 h 06 m 53 s** — the arithmetic was right
to within twenty-one seconds, and the only thing wrong was the sentence this practice wrapped around
it.
