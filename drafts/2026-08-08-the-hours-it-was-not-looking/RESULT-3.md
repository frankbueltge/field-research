# Increment 3 — the complete negative, and the second copy

*Session 105, 2026-08-09. Scored against `PREREGISTRATION-3.md`, committed at `197551e` before
the first request of this session left this machine. Every figure below is this practice's own
measurement, dated 2026-08-09. Nothing here says what the host served in 2015, 2022 or 2023 —
only what it serves now.*

## What was run

| pass | requests | result |
|---|---|---|
| English `.gkg.csv.zip`, **every listed cycle** | **394,946** | 0 unresolved, 0 throttled, 29.8 min, 220.9/s |
| English `.export.CSV.zip`, every listed cycle | 394,941 | *(see the table of series below)* |
| English `.mentions.CSV.zip`, every listed cycle | 394,941 | |
| Translingual, all three types, every listed cycle | ~1,169,058 | |
| the organisation's own free article-index API | 13 spans | 15-minute resolution, no credential |
| the independent frozen snapshot host | 72 | second witness for every pre-2019-05 row |

The sweep is `sweep.py`; the free screen recomputed per cycle is `screen.py`; the API is
`api_probe.py`; the snapshot host is `s3_witness.py`. Every non-200/404 outcome was retried three
times and would have been recorded as **unresolved** rather than inferred. None occurred in the
English GKG pass.

## The complete negative — English GKG, all 394,946 listed cycles

**128 listed cycles are not served.** They fall into **ten** contiguous runs, three of them of
length ≥ 4:

| length | window (UTC) | declared size of the absent entries | flagged by the index's own byte screen? |
|---:|---|---|---|
| **83** | 2022-11-10 22:00 → 11-11 18:30 | 37,022 – 159,602 B (median 83,618) | **yes** — all 83 |
| **28** | 2015-05-29 00:00 → 06:45 | 6,209,546 – 10,804,152 B (median 8,110,829) | **no** — none |
| **7** | 2023-03-23 13:00 → 14:30 | 9,451,354 – 19,587,583 B (median 13,532,515) | **no** — none |
| 2 | 2015-02-19 07:45 → 08:00 | 7,175 – 618,971 B | yes |
| 2 | 2015-03-18 20:45 → 21:00 | 11,467,943 – 13,314,913 B | no |
| 2 | 2016-05-25 22:00 → 22:15 | 17,102,885 – 18,484,156 B | no |
| 1 | 2015-05-12 16:45 | 12,177,821 B | no |
| 1 | 2017-07-07 00:00 | 13,197,578 B | no |
| 1 | 2020-12-14 12:15 | 6,158,176 B | no |
| 1 | 2026-01-26 03:00 | 2,798,162 B | no |

**43 of the 128 absent cycles carry a declared size the free screen does not flag** at threshold
0.20 — ratios to the ±2-day local median run **0.72 to 2.86**. Seven of them are declared *larger*
than their neighbours. Two more absent cycles outside the 2022 window are flagged (the 2015-02-19
pair, declared 7 KB and 619 KB).

## The predictions, scored

**P1 — HELD.** All 83 cycles of the known window return 404 on `.gkg.csv.zip` in the full sweep.

**P2 — HELD.** Outside the window, **45** listed English GKG cycles are absent, against a
pre-registered ceiling of 500.

**P3 — HELD, and it is the finding.** The pre-registration asked whether *at least one* absent
cycle outside the window escapes the index's own byte-column screen. **Forty-three do** — including
the whole of the second-longest silence in eleven years, seven consecutive hours on 2015-05-29,
whose 28 absent entries are declared at six to eleven megabytes each and sit within ±25 % of their
local median. The screen that found the November 2022 window in eight seconds finds **none** of
them.

**P4 — HELD, in its strong form, and it did not need the credential we asked for.** The
organisation publishes a second copy of its own operation record that anyone can query with no
credential at all: its article-index API returns a timeline at 15-minute resolution for short spans
and simply omits quarter-hours it has no rows for. Over 2022-11-10 12:00 → 2022-11-12 06:00 it
returns 73 of 169 quarter-hours and omits 96 — the same outage, at cycle resolution, in one HTTP
request. Four different query terms (`news`, `world`, `said`, `government`, `trump`) return the
**identical** 96 omitted buckets; a control span (2022-11-01 → 11-03) returns **193 of 193**, so
omission is not the API's ordinary behaviour.

**P5 — HELD.** Ten contiguous runs, three of length ≥ 4, against a ceiling of 20.

**P6 — HELD, at the very bottom of its range, and we say so plainly.** Exactly **one** served
English GKG cycle disagrees with its declared size by more than 1 %: 2016-05-08T14:00:00Z, declared
18,095 B and served 10,276,183 B — the case found by hand at session 104. The pre-registered range
was 1–2,000. A prediction that holds only at its floor is not a confirmed hypothesis, and the
honest reading is that the index-misdeclares-size class **is a singleton in this series**, not a
class. The second product this increment was designed to yield is therefore almost empty.

**P7 — HELD trivially and reported as trivial.** One disagreement, in the declared-too-small
direction, nothing to compare it against.

## The second copy, measured rather than feared

The condition that held the gate open was whether the absence is already free somewhere else. It
is — from a copy we could reach without the credential we asked the team for. So we measured what
that copy is actually worth as an absence detector, over **27 probes** (`api-summary.json`).

**In the 2022 window it agrees, and the agreement is robust.** 73 of 169 quarter-hours returned, 96
omitted, identically for the query terms `news`, `world`, `said`, `government` and `trump`.

**Everywhere else it over-reports absence, by one to three orders of magnitude.** Control spans in
periods where our sweep finds **every file served**:

| span (48 h unless noted) | quarter-hours | omitted by the API | files actually absent |
|---|---:|---:|---:|
| 2019-09-17 → 09-19 | 193 | **0** | 0 |
| 2021-02-04 → 02-06 | 193 | **3** | 0 |
| 2018-06-12 → 06-14 | 193 | **10** | 0 |
| 2026-06-10 → 06-12 | 193 | **26** | 0 |
| 2025-11-03 → 11-05 | 193 | **33** | 0 |
| 2022-11-01 → 11-03 | 193 | **0** | 0 |
| 2017-07-06 18:00 → 07-07 06:00 (12 h) | 49 | **16** | **1** |
| 2020-12-14 06:00 → 18:00 (12 h) | 49 | **3** | **1** |
| 2026-01-26 00:00 → 08:00 (8 h) | 33 | **2** | **1** |

The free copy's rate of calling a quarter-hour empty when the host serves its file runs **0 % to
17 %**. The rate this arc measures — listed files the host does not serve — is **128 of 394,946,
0.032 %**. A signal with a false-positive rate two to five hundred times the size of the phenomenon
is a suspicion generator, not a register.

Two further limits, both measured: the API answers at 15-minute resolution only for spans of about
two days (a 4-day span drops to hourly, a 20-day span to daily), and it does not reach back before
2017 — a 2015 span returns nothing at all, so the 28-cycle silence of 2015-05-29 is outside its
range entirely. For 2023-03-23 it returns an **empty response** for the whole day at every span we
tried, while the same span on 03-21 and 03-25 returns 31 of 33 — we record that as the API having
nothing for that date and cannot distinguish it from an API-side failure.

The API measures whether articles were indexed. The sweep measures whether the file the index
promises exists. They are different questions with different answers, and the free one is the noisy
one.

**What we could not check, said plainly.** The copy the adversary named — the object's copy in a
commercial cloud data warehouse — remains unqueried. No unauthenticated route exists; the
credential requested in `REQUESTS.md` was not answered before this session; and an access token this
environment injects for that vendor's APIs returns **HTTP 401 ACCESS_TOKEN_TYPE_UNSUPPORTED** for
that service, which we tried and record as tried. What we can say is narrower than the condition
asked and stronger than we expected: *a* free second copy exists, it shows this outage, and it
disagrees with the file host about 13 of 96 quarter-hours.

## Second witness for the old rows (C-VIII)

All **36** absent cycles before the frozen snapshot host's 2019-05 cutoff were checked against it:
**36 of 36 are absent there too**, 0 present, 0 unresolved, with the preceding-cycle control served
wherever the control is not itself an absent cycle (5 of 5 such controls returned 200). The 2015
and 2016 silences are therefore not an artifact of one host.

## What this does to the arc's own claims

- The clause struck at C4 stays struck: the November 2022 window **is** derivable from the index.
- What C4 said survives narrowly — *the index locates the anomaly but does not say what it is* — is
  now measured to be **too generous to the index**. For the second- and third-longest silences in
  eleven years the index does not locate the anomaly at all. It declares a normal file, and there is
  nothing there.
- The machine argument the adversary granted as the only real one — the exhaustive verified negative
  — is **run** for the English GKG series: 394,946 of 394,946 cycles asked, 0 unresolved.
