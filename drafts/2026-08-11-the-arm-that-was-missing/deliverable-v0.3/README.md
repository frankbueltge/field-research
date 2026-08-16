# The Control Arm — a credential-free public-presence ledger

**Version 0.3.1 · 2026-08-16 · Meridian, an autonomous research practice**

> **STATUS — read this first.** Version 0.1 of this bundle was refuted at its own gauntlet on
> 2026-08-15 and withheld. This version is a rebuild, not a patch: it is built in one pass from
> the run files, it carries the correction that version made necessary, and it puts the
> measurement that refuted version 0.1 on its own face. **Whether it passes its own
> gauntlet is stated in `VERSIONS.md`** — and to say it here too, because a pointer that points at
> a pointer is not a status: **version 0.3 FAILED its gauntlet and is withheld, and this
> version, 0.3.1, is that state with the findings repaired and NO REVIEWER HAS READ IT.** Nothing
> here has been sent to anyone.

A dated record of whether named videos on a very large video platform were **publicly
retrievable**, taken without any credential, together with a reference population large enough to
give a single reading an expectation.

**Read `LIMITS.md` before you use a number from this bundle.** It is short, present-tense, and
every serious misuse of this data is a misuse it names.

---

## 1. What this is, in one paragraph

A very large video platform is required by law to give vetted researchers access to its publicly
available data. Whether it does is an empirical question with two halves: **what the research
interface returns**, and **what was actually public**. The first half is credentialed and closed.
The second half is free — no account, no allow-list — and was not being run as a continuous,
published series. This bundle is that second half: a fixed panel of publicly cited video
identifiers, re-measured once a day from one logged vantage, published with its refusals visible.

## 2. Coverage

- **5 measurement days**, 2026-08-11T11:24:06Z to 2026-08-15T03:37:40Z.
- **3,581 units** on the baseline day; 5 run files, each hashed in `MANIFEST.json`.
- The instrument is **still running**. A day missing from this bundle is a day outside its
  cut-off, never evidence that the instrument was dark.

| Day | Started (UTC) | Determinate | Not retrievable | Rate |
|---|---|---|---|---|
| baseline | 2026-08-11T11:24:06Z | 3,581 | 437 | 12.20 % |
| 2026-08-12 | 2026-08-12T03:40:28Z | 3,582 | 437 | 12.20 % |
| 2026-08-13 | 2026-08-13T04:27:00Z | 3,576 | 439 | 12.28 % |
| 2026-08-14 | 2026-08-14T03:43:47Z | 3,583 | 435 | 12.14 % |
| 2026-08-15 | 2026-08-15T03:37:40Z | 3,576 | 438 | 12.25 % |

## 3. The measurement that refuted version 0.1, on the face of the bundle

Version 0.1 argued that reproducing this aggregate rate day after day on a fixed panel was
grounds for trusting a **single** reading of somebody else's list. This practice's own record
refutes that, and the refutation is the most useful thing in this bundle.

Every apparent state change was re-requested **5 times immediately**, at the
instrument's own spacing. Counting only genuine transitions:

- **3 of 3** returns (`NOT-RETRIEVABLE` → `RETRIEVABLE`) survived re-checking.
- **1 of 3** disappearances (`RETRIEVABLE` → `NOT-RETRIEVABLE`) survived it.

Over the raw readings, before 2 of this instrument's own artefact echoes are removed,
the same two counts are **5 of 5** and **1 of
3**. **Both pairs are correct and they are not the same quantity.** A confirmation
count travels with the word *raw* or *genuine*, or it does not travel.

**The confirmation record does not cover the same days as the tables above, and that is stated
rather than left to be found.** It is built from 4 interval sidecars — one per
interval between consecutive measurement days — held in the repository this bundle comes from and
listed by path and sha256 inside `confirmation-record.json`, running from `ledger/transition-confirm-2026-08-12.json` to
`ledger/transition-confirm-2026-08-15.json`. Every interval between consecutive measurement days has one, except that an
interval whose second day is the newest day in this bundle has one only if the confirmation step
had run when the bundle was assembled. Where it has not, that interval's apparent transitions are
in `series/` as raw readings and are **not** in the counts above. A count of confirmed events is
never a count over the whole panel unless the sidecar list says so.

**These counts are not readings of the tool, and the distinction is one this practice got wrong
in public and was corrected on.** The daily ledger takes one pass per identifier per day and
confirms *transitions between days*. The tool in this bundle confirms *readings within one run*.
**They are not the same instrument and a figure from one is not a row of the other.** What the
counts above establish is narrower than a rate and still decisive: on this instrument, at this
endpoint, a state change that is believed on one request is frequently not there on the next.

What follows for anyone using this bundle: **a single reading is not a finding.** A refusal that
has not been re-requested is a reading of the network as much as of the platform. The tool shipped
here (version 0.3.1) re-requests by default; a `--confirm 0` run is a version-0.1-equivalent
reading and must say so.

## 4. The reference population

On 2026-08-15T03:37:40Z, of **3,576** determinate units, **438** were not publicly retrievable — a
rate of **12.25 %** (11.21 %–13.36 %).

Absence rises with age. Pooled across the panel, the oldest band runs **3.8217 ×** the
youngest (two-sided Fisher *p* = 3.0829 × 10<sup>-10</sup>). Per age band on 2026-08-15:

| Age band | n | Not retrievable | Rate | Interval |
|---|---|---|---|---|
| 0-1y | 493 | 23 | 4.67 % | 3.13 %–6.90 % |
| 1-2y | 773 | 60 | 7.76 % | 6.08 %–9.86 % |
| 2-3y | 787 | 94 | 11.94 % | 9.86 %–14.40 % |
| 3-4y | 672 | 111 | 16.52 % | 13.90 %–19.51 % |
| 4-5y | 457 | 76 | 16.63 % | 13.50 %–20.32 % |
| 5y+ | 387 | 69 | 17.83 % | 14.34 %–21.95 % |

**This table has a date and using it later is an error that grows** — see the section of
`LIMITS.md` headed *The reference table has a date*. Its
declared reference time is 2026-08-15T03:37:40Z and its bands were computed at 2026-08-15T03:37:40Z.

## 5. What is in this directory

| File | What it is |
|---|---|
| `README.md` | this file |
| `LETTER.md` | a covering letter, written to be forwarded unedited by a human |
| `LIMITS.md` | the present-tense limits; load-bearing, travels with any reuse |
| `VERSIONS.md` | every version of this bundle and what happened to it |
| `MANIFEST.json` | the sha256 of every run file this bundle was built from |
| `FIGURE-PROVENANCE.json` | every figure in the prose above, with the JSON field it was read from |
| `expectation.json` | per-day rates by age band, source stratum and year, both arms |
| `reference-baseline.json` | the reference population as one table, with its own date and drift |
| `gradient-test.json` | the age-gradient test and its exact *p*-values |
| `confirmation-record.json` | the confirmation counts on the README's face, computed |
| `reference-drift.json` | the measured shelf-life drift of the reference table |
| `series/` | the full dated series, raw and overlay-corrected, CSV and JSON |
| `receiver-eleven.*` | this practice's readings of the eleven identifiers on one public dashboard |
| `tools/presence_check.py` | the instrument, pointable at your own list |

## 6. Using the tool on your own list

    python3 tools/presence_check.py --ids my-list.txt --baseline reference-baseline.json

It reads one identifier per line, requests each once at a fixed spacing, re-requests every refusal
before believing it, and prints your rate beside what this reference population showed **on the
reference day**. It writes the version, the `--confirm` setting, the baseline path and that
baseline's sha256 into every output. It sends no credential and stores nothing about you; the
network vantage it records about itself is controlled by `--vantage`.

## 7. Standing conditions

This bundle is an **offer**. The conditions this practice asks a reuser to honour — never
obligations imposed on anyone — are in `memory/downstream-commitments.md` of the repository this
comes from. The three that matter most are the sections of `LIMITS.md` headed *`NOT-RETRIEVABLE` does not mean deleted*, *The
population is a cited population* and *events is not a rate*: the refusal is
semantically empty, the yardstick carries its population, and a handful of events is not a rate.
