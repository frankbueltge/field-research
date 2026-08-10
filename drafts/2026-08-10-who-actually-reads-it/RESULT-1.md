# Result 1 — the consumer census, scored against `PREREGISTRATION-1.md`

*Session 106, 2026-08-10. The pre-registration was committed at `8e33d25`, before the first request
of this session left this machine. Every figure below is dated 2026-08-10 and is a snapshot.*

## What ran

| step | what | figure |
|---|---|---|
| P-A | complete project-name list of the public Python package index, from its own simple endpoint | HTTP 200, 42,588,269 bytes, **867,935 project names**, 20 name hits |
| P-B | complete current-package descriptor database of the R archive network | HTTP 200, **24,719 packages** screened over name+title+description, **0 hits** |
| P-B (D1) | the same network's archive directory of withdrawn packages | HTTP 200, **27,546 package directories**, **1 hit** (`GDELTtools`) |
| — | source obtained from the registries themselves and unpacked | **19 packages**, 2 name hits excluded as substring collisions |
| — | fetch paths read by hand, with file-and-line citations | `classification-v0.1.json`, 19 rows |
| — | packages **executed** against a measured outage day | **4** |

The object's own documentation was fetched first, before any of this was written up, as the standing
check requires (see below).

## The first two executions, and they agree with each other and with last session's register

Both packages were installed unmodified from the registry into a clean environment and asked for one
day of events with full 15-minute coverage. **2022-11-11** is a day this practice measured on
2026-08-09: 75 of its 96 quarter-hours are listed in the object's own master file list, each with a
byte size and an MD5, and the host serves none of them. **2022-11-09** is the control: every cycle
served.

| package | day | rows returned | distinct cycles | exception | marker in the returned value |
|---|---|---|---|---|---|
| `gdelt` 0.1.14 | 2022-11-11 | **36,005** | **21 of 96** | none | none |
| `gdelt` 0.1.14 | 2022-11-09 (control) | 116,317 | 96 of 96 | none | — |
| `gdelt-client` 0.2.1 | 2022-11-11 | **36,005** | **21 of 96** | none | none |
| `gdelt-client` 0.2.1 | 2022-11-09 (control) | 116,317 | 96 of 96 | none | — |

Two independently written packages return **the same 36,005 rows over the same 21 cycles**, and the
21 cycles are **exactly** the 21 that this practice's own `availability-register-v1.0.json` says are
served that day — `demonstration-crosscheck.json`, `exact_match_with_register: true`. That is a
third party's code independently confirming last session's register, and it is worth more than the
register's own self-consistency.

~~**A researcher asking these libraries for 11 November 2022 receives 31 % of the day's events and
is told nothing about it in the value they are handed.**~~

**WITHDRAWN — FALSE AS PUBLISHED (`CORRECTIONS.md` C5, `REFUTATION-REPRODUCED.md`).** 116,317 is a
*different day*. The index declares **178,909 bytes** for the 75 absent export files; calibrated
against 25 downloaded files of comparable declared size (median **42.0** declared bytes per event),
they held on the order of **4,260 events**. The complete day held roughly **40,000**, so the client
returns about **89 %** of what the instrument produced. What survives, and needs no counterfactual:
**21 of 96 cycles, and nothing in the returned value says so.**

**And the promise is still live today.** The master file list re-fetched 2026-08-10, HTTP 200,
126,533,378 bytes, 1,184,979 lines (`index-still-promises.json`): **all 75** of the day's absent
English export cycles are **still listed**, each with a byte size and an MD5 — e.g.
`20221111000000.export.CSV.zip`, 4,404 bytes, `9fcd7af6…`. **1,368 days** after the fact, the index still tells a reader those files exist.

**What the control day is, and what it is not — this paragraph was wrong in both directions.** It
said 116,317 is not a counterfactual (true) *and* that what the day would have held is unknowable
(false). The index declares the sizes; we simply did not add them up. See `CORRECTIONS.md` C5.

**Re-probed the same day as the executions, so the denominator is not yesterday's.** 192 HEAD probes
against the file host, 2026-08-10 (`reprobe-2026-08-10.json`): 2022-11-11 → **21 served, 75 absent**;
control 2022-11-09 → **96 served, 0 absent**; no other status on either day. The served set is
**identical** to the one the 2026-08-09 register implies. The clients' behaviour and the host's state
are therefore measured on the same date.

### The third execution, and it corrects this session's own first reading

`gdelt-py` 0.1.11 was classified from its source as a third package with no marker in the returned
value. **That reading was wrong and is corrected here**: the package has a result container with
explicit partial-failure tracking — `FetchResult.data / .failed / .complete / .partial /
.total_failed` (`py_gdelt/models/common.py`). Reading the source alone would have had this practice
publish a false statement about a third party's code. It was caught by executing the package, which
is the whole discipline this concept was opened to enforce.

What execution actually returned, through the package's own async entry point:

| day | records | `complete` | `total_failed` | exception |
|---|---|---|---|---|
| 2022-11-11 (75 of 96 cycles absent) | **0** | **true** | **0** | none |
| 2022-11-09 (control) | 2,668 | true | 0 | none |

The diagnostic (`diagnose-gdelt-py.json`) says why, and the why matters: **for a whole-day range this
package requests exactly one cycle per stream (00:00:00), not 96.** On the outage day both of those
requests returned 404 — two `File not found (404)` lines in its own debug log — and **neither reached
the `failed` list.** So a result object designed to report partial failure reported a **complete**
result with **zero** failures on a day where every file it asked for was missing.

Two caveats this practice states against its own interest. The control day's 2,668 records are far
smaller than the 116,317 the other two clients return for the same day, precisely because this
package asked for one cycle rather than 96 — that per-day behaviour is a separate matter this session
did not diagnose and makes no claim about. And the package's documented *synchronous* entry point
raised `RuntimeError("Event loop is closed")` in this environment on both windows, so the async entry
point was used; recorded, not diagnosed.

### The word "silently" does not survive intact, and it is retired here

A search fan-out found, and this practice re-opened and confirmed first-hand at
`https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master/README.rst`, that `gdeltPyR`'s own README
says:

> *"Some time intervals in GDELT 2.0 are missing; ``gdeltPyR`` provides a warning message when data is
> missing"*

The behaviour is documented by its author. **This result therefore does not claim silence.** What it
claims, and what it measured, is narrower and has to be said in the narrow form every time: **the
signal is in a channel the returned value does not reach.** 150 lines on worker-process stderr;
nothing in the DataFrame; nothing that survives the ordinary idiom for capturing warnings around a
call. See `NEIGHBOURS-1.md`, which puts this first among the neighbours because it cuts against us.

## Where the signal does go, stated exactly — and a correction to this session's own first run

`gdelt` 0.1.14 is not silent at the process level. Run with no warnings machinery at all it writes
**150 warnings across 300 stderr lines** — one warning per line-pair, two warnings per absent cycle, from its worker processes. *(An earlier sentence here said "150 warning lines"; corrected, `CORRECTIONS.md` C9.)*

This session's **first** harness reported zero warnings, and that figure was **wrong and is
withdrawn** (deviation D2). The harness wrapped the call in the standard record-warnings idiom; the
package downloads in forked worker processes, which inherit the parent's warning recorder, so each
child recorded into its own copy and the parent saw nothing. The error was ours, not the package's.
It is reported here rather than quietly fixed because it is also the finding's own best illustration:
**the ordinary idiom for capturing warnings around a call is enough to lose all 150 of them**, and
this practice lost them by accident on its first attempt.

`gdelt-client` 0.2.1 is better on this axis — its 75 warnings are raised in the calling process and
are visible to an ordinary caller. **Neither package puts anything in the returned object.**

## The census, in one paragraph

Of the 19 packages, **six consume the measured 15-minute series**. Of those six:

- **three** hand the caller a result whose **incompleteness is not readable from the returned value** —
  `gdelt` and `gdelt-client`, which carry no such field at all, and `gdelt-py`, which carries one and
  reported `complete = true, total_failed = 0` on the outage day. All three were executed;
- **one** — `pygdelt` — performs **no status check of any kind** and streams the not-found response
  body into a file named `<cycle>.zip` on disk. **Executed** (`demonstration-pygdelt.json`): for
  2022-11-11 it writes **96 files, no exception, and 75 of them are zero bytes and not zip archives**;
  the 21 real archives are exactly the 21 cycles the host serves;
- **one** — `gdelttools` — raises, prints and calls `sys.exit(1)`: loud, and arguably too loud, since
  one broken promise in the master list terminates a bulk download of the whole series;
- **one** — `gdeltforge`, released five days ago — retries and then returns the failure to its caller
  **as a value**, in a `failed` list beside the success and skipped counts. It is the only package in
  the census that does.

**One correction to the paragraph above, from the adversary and confirmed by us:** `gdelt-py`'s
master-list constant is **dead code** — `get_master_file_list` is defined and called from nowhere in
the package (`CORRECTIONS.md` C7) — so its row's `C1_reads_master_list` is now `false`.

**Two of the six verify the MD5 the master list publishes** (`gdelttools`, `gdeltforge`), as does the
withdrawn R package on the older daily series. **Three of the six never read the master list at all**
— they construct file names arithmetically from the 15-minute grid, so they never see the promise
that is broken; they only see a 404.

That split is the shape of the thing: **the packages that read the index verify it and stop; the
packages that skip quietly never read the index.** Nobody in this census is positioned to notice that
the index promised a file that does not exist.

## Predictions, scored

| # | prediction | outcome |
|---|---|---|
| N1 | P-A returns 1–25; P-B returns 1–15 | **PART-FAILED.** P-A: 20 ✓. **P-B returned 0** on the pre-registered screen — the floor was 1. The single archived package was found by a screen that was **not** pre-registered (D1) and is reported separately. |
| N2 | ≥2 candidates with a readable fetch path | **HELD** — seven fetching packages, all read by hand. |
| N3 | 0 candidates verify the published checksum *(no expected direction)* | **FAILED, against us.** Three verify it. Two of them are among the six that consume the measured series. Reported here in the same breath as every claim about the others. |
| N4 | **KILL** — ≥1 candidate returns a result the caller cannot distinguish from a legitimate one | **HELD.** Three do; two were executed and produced the table above. The kill criterion does not fire. |
| N5 | ≥1 candidate offers a joined view across the three products | **FAILED.** None does. The per-product independence measured last session therefore has no consumer in this population that it can silently unbalance — a claim this concept had been half-expecting to make, and cannot. |
| N6 | ≥1 candidate released within 24 months | **HELD** — `gdeltforge` 2026-08-05 (five days ago), `gdeltnews` 2026-07-28, `gdelt-py` 2026-06-27, `gdelt-client` 2026-02-18. *(Aliveness is not a receiver argument and is not used as one.)* |
| N7 | ≥1 candidate constructs file names arithmetically | **HELD** — three do. |

**Four held, one part-failed, two failed.** The two failures both cut against the concept: consumers
are more careful than predicted (N3), and one of the object's measured defects has no consumer in
this population that it can harm (N5).

## The standing check, run before the write-up and not after

> *Ask what the object already publishes about itself, and try to derive the finding from that first.*

Fetched this session: the object's own data page (`https://www.gdeltproject.org/data.html`), its
canonical 2.0 announcement (`https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/`),
and the documentation site of one consumer that reads the master list
(`https://rbozydar.github.io/py-gdelt/getting-started/data-sources/`).

**None of the three states that the master file list may list a file the host does not serve, and
none advises verifying the published MD5.** The announcement documents the master lists and the
15-minute cadence and says the streams begin in February 2015; it says nothing about completeness.
So the finding is **not** "consumers ignore documented guidance" — there is no guidance to ignore.

**Bound on that check, stated:** three pages and one search, not an exhaustive read of the object's
documentation, which is large and partly frozen. If a fourth page says otherwise, this paragraph is
wrong and must be corrected as a dated event.

## Deviations

- **D1.** The pre-registered P-B screen (current-package metadata) returned zero. A second screen —
  the archive directory of withdrawn packages, by name — was added afterwards and returned one. It was
  not pre-registered; its hit is reported in its own row and is never folded into any rate.
- **D2.** The first execution harness reported "0 warnings" for `gdelt` 0.1.14. That figure was an
  artifact of the harness (forked workers inheriting the parent's warning recorder) and is
  **withdrawn**. Re-run with no warnings machinery: 150 lines on stderr. Both runs are kept in the
  directory (`demonstration-gdeltpyr.json`, `demonstration-default-harness.json`).
- **D3.** Four of the seven fetching packages were executed; the other three are readings of source
  code and are labelled as such in every row of `classification-v0.1.json`.
- **D6.** Four measurements were added *after* the state was frozen for the adversary at `c18a8bf`:
  the same-day re-probe, the master-list re-fetch, the counterfactual caveat, and the `pygdelt`
  execution. They are additions, not revisions of anything it graded, and the sequence is recorded in
  the session's minutes with hashes. The adversary's verdict is good for `c18a8bf`.
- **D4.** `gdelt-py`'s classification was corrected mid-session, from a reading of its source to a
  measurement of its behaviour, after the source turned out to contain a partial-failure container the
  first reading had missed. The wrong reading is not deleted; it is stated in the result above as what
  was believed, and the correction is the reason the executed row exists.
- **D5.** The census's word for the behaviour was "silent" until a fan-out surfaced the affected
  package's own README documenting its warning. The word is retired in this document and in
  `CONCEPT.md`; what is claimed instead is stated in the narrow form wherever it appears.

## What this result does not establish

- **Nothing about a receiver.** Naming one was explicitly out of scope for this gate session, and
  nothing here names one.
- **Nothing about how much this matters.** Whether these packages are used by anyone whose results
  would change is a separate question, put to a search fan-out this session and answered in the
  minutes.
- **Nothing about any maintainer.** Two of six verify the checksum; one returns failures as a value;
  the census says so as loudly as it says the rest.
- **Nothing about why any file is absent**, in either direction.
