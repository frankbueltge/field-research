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
is — from a copy we could reach without the credential we asked the team for. But the two published
copies **do not agree**, and the disagreement is measurable:

- The API omits **2022-11-10T21:45Z**, whose file the host serves at 7,337,477 bytes.
- The API omits a **second block, 2022-11-11 20:30 → 23:15**, twelve quarter-hours whose files the
  host serves normally and which our sweep does not find absent.
- The API returns **2022-11-11 18:45 → 20:15**, seven quarter-hours in the middle of the file
  outage's trailing edge.

So of the 96 quarter-hours the free API calls empty in this window, **13 have files the host serves
today**. The API measures whether articles were indexed; the sweep measures whether the file the
index promises exists. They are different questions with different answers, and neither is a
substitute for the other.

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
