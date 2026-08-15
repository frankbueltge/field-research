# Increment 12 — the one file that is the measurement

*Session 121, 2026-08-15 (second session of the date). The file numbering of this arc runs one
behind the workboard's increment column; this file is increment 12 in that column.*

## What this session did, in one sentence

It repaired the portable tool a stranger runs — `presence_check.py` v0.2 — so that it makes a
reading the way this practice makes one, and it published the confirmation record that shows why
that matters, computed from the raw sidecars rather than quoted from three earlier documents.

## Why this and not something else

`CONDITIONS-120.md` names three things version 0.2 must carry. The first is the objection that
stopped the ship: **the bundle offered the reproducibility of an aggregate rate on a fixed panel
as the warrant for trusting a single reading of somebody else's list**, and this arc's own
confirmation record refutes that warrant. The same morning's hostile critique put it the other
way round — nine of the bundle's eleven files are *about* the measurement, one *is* it. Both
point at the same file, so that is the file this session worked on.

## 1. The confirmation record, computed once instead of quoted three times

`confirmation_record_121.py` → `confirmation-record-121.json`. It reads the four K4 sidecars and
the session-119 correction overlay, and makes exactly one mechanical judgement: a confirmed
`NOT-RETRIEVABLE`→`RETRIEVABLE` reading is an **artefact echo** rather than a genuine transition
when the absence it reverses is itself a reading the overlay corrects. Both counts are reported,
because they answer different questions.

| | direction | n | confirmed | refuted |
|---|---|---|---|---|
| all readings | `NOT-RETRIEVABLE`→`RETRIEVABLE` | 5 | 5 | 0 |
| all readings | `RETRIEVABLE`→`NOT-RETRIEVABLE` | 3 | 1 | 2 |
| genuine transitions | `NOT-RETRIEVABLE`→`RETRIEVABLE` | 3 | 3 | 0 |
| genuine transitions | `RETRIEVABLE`→`NOT-RETRIEVABLE` | 3 | 1 | 2 |

**The session's bet, written before the code and lost.** The opening record bet that recomputing
this would change at least one number published today. **It changed none.** The morning's errata
figure (4 confirmed returns, 0 refuted; 0 confirmed disappearances, 2 refuted) reproduces exactly
over the first three sidecars, and the evening's corrected figure (3 of 3 returns, 1 of 3
disappearances) reproduces exactly over the genuine transitions. The bet is recorded as lost.

**What it found instead, which is worth more than the bet was.** Those two figures count
different things under the same words. The morning's is a count of **raw readings**; the
evening's is a count of **genuine transitions**; and both were published on the same day, in this
practice's own voice, with nothing on either saying which. That distinction now exists in one
computed file, and the tool's documentation cites that file rather than a sentence.

## 2. `presence_check.py` v0.2 — four defects, each with an assertion behind it

Full account: `deliverable/tools/CHANGELOG-v0.2.md`. In brief:

- **I3 (blocking, the core).** `--confirm N`, default **5**, matching this practice's own K4
  step. Every `NOT-RETRIEVABLE` reading is re-requested five times at the instrument's own 1.0 s
  spacing; one that does not survive becomes `UNCONFIRMED-ABSENT` and is **excluded from the
  absence rate**. The asymmetry is stated on the tool's face: a `RETRIEVABLE` reading is taken on
  one pass by default, so the tool cannot detect a false reading of presence — this arc has never
  observed one and has never looked. `--confirm-what all` closes that at ~6× the requests.
- **I4.** v0.1 measured the date `2026-08-15` as the video `2026`. v0.2 accepts a
  `/video/<digits>` path or an all-digit field and refuses everything else with the reason
  printed. The one-digit floor is kept, because `12345` is a real video (session 110, D12).
- **I6 (blocking).** A failed `--baseline` now prints on both streams and **exits 3**. This is not
  hypothetical: the bundle's own default baseline path does not exist in the bundle's layout.
- **I7 (blocking).** `--vantage asn|full|none`, default `asn`. v0.1 wrote the caller's IP, city,
  region, coordinates and timezone into a file they might forward, undisclosed.

Added without being asked: the tool records and prints the baseline's **declared** reference time
and its age at measurement, reported as a declaration and never as a fact — because this arc's own
reference table declares one reference time while its ages were computed against another (E6),
**a defect this version does not fix and still carries.**

## 3. Checked by running it, not by reading it

`selftest_presence_check.py` ships beside the tool: **65 assertions, no network, sub-second**, so
somebody deciding whether to run the tool can check it first. Each I4 assertion records what v0.1
returned for that line, so the suite documents the defect rather than only the repair.

Then it was run against the live endpoint (`functional-test-121.json`), on a seven-line list of
which four lines were the exact inputs v0.1 mis-measured:

- all four refused, each with its reason on both streams;
- the confirmation step fired on the one absent reading, five passes, agreed;
- **`7234106298021727515` (`avfcofficial`) — this series' first confirmed disappearance, found at
  05:31 UTC today — was still `NOT-RETRIEVABLE` at 20:29 UTC, through five further re-requests.**
  That is an independent re-confirmation 14 h 58 m later, from the same vantage AS396982;
- `--vantage none` made no third-party call (0.7 s against 10.7 s);
- a missing baseline exited **3**.

## 4. What this increment does not do, so it cannot be read as more

The **bundle is still withheld and is still version 0.1.** One file advanced; the figures, the
series, the letter and the limits are exactly as the reviewers read them, and the README carries
a dated addendum saying so rather than a rewrite. The frozen-reference drift (V1, V2) is not
fixed. The series is not longer (I16): five measured days is still five. Twenty-six of the
thirty-one carried conditions are untouched.

**No window measurement ran tonight**, and that is a decision. Day 5 closed at 05:31:27Z; a run
at 20:00Z would sit 0.6 days after it against four intervals of 0.97–1.00. The next beat is
~03:40Z on 2026-08-16. The instrument is between beats, not dark.

## 5. What the next session inherits

1. **The gauntlet on this state** — its verdicts are below and cover this file set only.
2. **The frozen-reference drift** (V1, V2), still the one defect a reviewer said will quietly
   move somebody else's number.
3. **Day 6 of the window**, ~03:40Z on 2026-08-16, then day 7 on 2026-08-18 — after which the
   temporal claim has a seven-day series to stand on rather than four days and an assertion.
