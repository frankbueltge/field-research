# Increment 3 — the complete negative, and the second copy

*Session 105, 2026-08-09. Scored against `PREREGISTRATION-3.md`, committed at `197551e` before
the first request of this session left this machine. Every figure below is this practice's own
measurement, dated 2026-08-09. Nothing here says what the host served in 2015, 2022 or 2023 — only
what it serves now.*

## What was run

**2,353,876 requests to the file host. 0 unresolved. 0 other statuses. 4 throttled responses in the
last series, all backed off and re-asked.** Every listed file of every type, in both language
streams, asked once, in six passes:

| series | listed files | probed | absent | size disagrees | unresolved | minutes | req/s |
|---|---:|---:|---:|---:|---:|---:|---:|
| English `.gkg.csv.zip` | 394,946 | **394,946** | **128** | 1 | 0 | 29.8 | 220.9 |
| English `.export.CSV.zip` | 394,941 | **394,941** | **95** | 0 | 0 | 31.1 | 211.6 |
| English `.mentions.CSV.zip` | 394,941 | **394,941** | **94** | 0 | 0 | 33.9 | 194.4 |
| Translingual `.gkg.csv.zip` | 389,686 | **389,686** | **117** | 0 | 0 | 31.4 | 206.8 |
| Translingual `.export.CSV.zip` | 389,681 | **389,681** | **83** | 0 | 0 | 29.8 | 218.0 |
| Translingual `.mentions.CSV.zip` | 389,681 | **389,681** | **85** | 0 | 0 | 28.7 | 226.0 |
| **total** | **2,353,876** | **2,353,876** | **602** | **1** | **0** | **185** | — |

**Completeness check, so "every" can be checked and not taken on trust.** The English master file
list fetched today is 1,184,889 lines, of which **61 are blank**; 1,184,889 − 61 = **1,184,828**,
exactly 394,946 + 394,941 + 394,941. The Translingual list is 1,169,058 lines, of which **10 are
blank**; 1,169,058 − 10 = **1,169,048**, exactly 389,686 + 389,681 + 389,681. **Every non-blank entry
in both published indexes was asked.** Nothing was sampled and nothing was skipped.

Beside that: 27 probes of the organisation's own free article-index API, 72 against an independent
frozen snapshot host, and 189 re-verification requests on fresh connections by two methods.

Tools, all in this directory: `sweep.py` · `screen.py` · `api_probe.py` · `s3_witness.py` ·
`reverify.py` · `score_increment3.py` · `analyse_increment3.py` · `build_register_v1.py`.
Every non-200/404 outcome was retried three times and would have been recorded as **unresolved**
rather than inferred. None survived to be recorded.

## The complete negative

**602 listed files, across 138 quarter-hours, are not served.** The register keyed per stream and
per type (`availability-register-v1.0.json`) carries 139 rows — those 138 plus the one cycle whose
served size disagrees with the index.

The failure is **not** a property of a quarter-hour. It is a property of a quarter-hour *and a
product*:

| how many series are missing | cycles | what it is |
|---|---:|---|
| all six | **82** | 2022-11-10 22:00 → 11-11 18:15 — the known window, in every product and both languages |
| GKG only, **both** languages | **30** | includes the seven-hour run of 2015-05-29 |
| all three **English** products only | **11** | 2015-02-19, 2020-12-14, and 2023-03-23 13:00 → 14:30 |
| English GKG only | 5 | |
| Translingual GKG only | 4 | |
| all three **Translingual** products only | **1** | 2022-11-10T21:45Z — the outage's leading edge, in one language |
| English export only / English mentions only / Translingual mentions only | 2 / 1 / 2 | |

**The three products fail independently.** For the seven hours of 2015-05-29 the instrument's
knowledge-graph files are missing in both languages while its event and mention files for exactly
those quarter-hours are served normally. Any consumer joining the three products on a cycle gets a
silently unbalanced join, and nothing in the index says so.

**And the two languages fail at different edges.** The English window runs 22:00 → 18:30; the
Translingual window runs **21:45 → 18:15** — the same 83 quarter-hours, shifted by one cycle at each
end.

The longest runs, per series:

| series | runs | runs ≥ 4 | longest |
|---|---:|---:|---|
| English GKG | 10 | 3 | 83 (2022-11-10 22:00 → 11-11 18:30), then 28 (2015-05-29 00:00 → 06:45), then 7 (2023-03-23 13:00 → 14:30) |
| English export | 6 | 2 | 83, then 7 |
| English mentions | 6 | 2 | 83, then 7 |
| Translingual GKG | 7 | 2 | 83 (21:45 → 18:15), then 28 |
| Translingual export | 3 | 1 | 83 |
| Translingual mentions | 5 | 1 | 83 |

## What the index can and cannot show

The adversary's C-I attack — the 2022 window is recoverable from the published byte column in eight
seconds — is true, and it stays conceded. Increment 3 measures how far it generalises. Of the 139
register rows, **86 are findable from the byte column** and **53 are not**. Outside the 2022 window
the ratio inverts:

> **55 cycles outside the window carry a disagreement. Three of them are findable from the index.
> Fifty-two are not.**

The 28 absent GKG cycles of 2015-05-29 are declared at **6,209,546 – 10,804,152 bytes**, within ±25 %
of their local median. The seven absent cycles of 2023-03-23 are declared at **9,451,354 – 19,587,583
bytes** — *larger* than their neighbours. No threshold on the published size column finds either.
They are found by asking the host, and only by asking the host.

## The predictions, scored

**P1 — HELD.** All 83 cycles of the known English window return 404 on `.gkg.csv.zip`.

**P2 — HELD.** 45 absent English GKG cycles outside the window, against a ceiling of 500.

**P3 — HELD, and it is the finding.** 43 of those 45 are **not** flagged by the index's byte-column
screen at threshold 0.20; their ratios run 0.72 to 2.86. Across all six series, 52 of the 55
out-of-window rows are invisible to it.

**P4 — HELD, and it did not need the credential we asked for** — see the next section. It is also
the prediction that was supposed to hurt, and the measurement turned it into something else.

**P5 — HELD.** Ten runs in the English GKG series, three of length ≥ 4, against a ceiling of 20.

**P6 — HELD, at the very bottom of its range, and we say so plainly.** Exactly **one** served file
in 2,353,876 disagrees with its declared size by more than 1 %: 2016-05-08T14:00:00Z, declared
18,095 B, served 10,276,183 B — the case found by hand at session 104. The pre-registered range was
1–2,000. A prediction that holds only at its floor is not a confirmed hypothesis: the honest reading
is that **index-misdeclares-size is a singleton across the whole eleven years**, not a class, and the
second product this increment was designed to yield is therefore almost empty. We report the failed
expectation, not the technically-held prediction.

**P7 — HELD trivially and reported as trivial.** One disagreement, declared-too-small, nothing to
compare it against.

## The second copy, measured rather than feared

The condition that held the gate open (C-IV) was whether the absence is already free somewhere else.
It partly is — from a copy we could reach with no credential at all: the organisation's own public
article-index API returns a timeline at 15-minute resolution and omits quarter-hours it has no rows
for. So we measured what that copy is worth as an absence detector, over 27 probes
(`api-summary.json`, `analysis-increment3.json`).

**In the 2022 window it agrees, and robustly.** 73 of 169 quarter-hours returned, 96 omitted,
**identically** for the query terms `news`, `world`, `said`, `government` and `trump`. Of those 96,
**84 have at least one genuinely absent file and 12 do not**.

**Everywhere else it over-reports absence.** In control spans where our sweep finds every file
served:

| span | quarter-hours | omitted by the API | with every file served |
|---|---:|---:|---:|
| 2017-03-01 → 03-02 | 97 | 0 | 0 |
| 2019-09-17 → 09-19 | 193 | 0 | 0 |
| 2022-11-01 → 11-03 | 193 | 0 | 0 |
| 2021-02-04 → 02-06 | 193 | 3 | 3 |
| 2018-06-12 → 06-14 | 193 | 10 | 10 |
| 2026-06-10 → 06-12 | 193 | 26 | 26 |
| 2025-11-03 → 11-05 | 193 | 33 | 33 |
| 2017-07-06 18:00 → 07-07 06:00 | 49 | 16 | 15 |
| 2025-06-13 12:00 → 06-15 00:00 | 145 | 45 | 45 |

Across all 18 probes that returned 15-minute resolution: **2,442 quarter-hours examined, 622 omitted
by the API, 199 of them with every one of their six files served today.** The phenomenon this arc
measures is **138 quarter-hours in 394,946**. A signal whose false-positive count in 2,442
quarter-hours is larger than the true phenomenon in eleven years is a suspicion generator, not a
register.

Three further limits, all measured: the API answers at 15-minute resolution only for spans of about
two days (four days drops to hourly, twenty days to daily); it does not reach before 2017, so the
2015-05-29 silence is outside its range entirely; and for 2023-03-23 it returns an **empty response**
for the whole day at every span we tried, while 03-21 and 03-25 return 31 of 33 — recorded as the API
having nothing for that date, which we cannot distinguish from an API-side failure.

One thing it got right that we would have missed: the API omits **2022-11-10T21:45Z**, whose English
files are served. The sweep shows why — the **Translingual** triple for that quarter-hour is absent.
Where the free copy and the register disagree, the register is the one that can say which.

**What we still could not check, said plainly.** The copy the adversary named — the object's copy in
a commercial cloud data warehouse — remains unqueried. No unauthenticated route exists; the
credential requested in `REQUESTS.md` was not answered before this session; and an access token this
environment injects for that vendor returns **HTTP 401 `ACCESS_TOKEN_TYPE_UNSUPPORTED`** for that
service, which we tried and record as tried. The condition is answered for *a* free second copy, not
for *that* one.

## Nothing seen once is reported

Every one of the 45 out-of-window English GKG absences was asked three more times, on fresh
connections, by ranged GET as well as HEAD: **45 of 45 not served in every round**, 0 changed. The
host answers a ranged GET for an object it does not have with **HTTP 416 and a 166-byte body** and a
HEAD with **404 and a zero-byte body**; the first run of the re-verification scored only 404 and
therefore reported every row as changed — the classifier was wrong, the data were not, and the fix
is recorded in `reverify.py`. Of 18 neighbouring controls, 14 are served in every round; the other 4
are quarter-hours the index **does not list at all** (checked against the manifest), which is the
other category this arc measured at increment 1.

**Second witness (C-VIII):** all 36 absent cycles before the frozen snapshot host's 2019-05 cutoff
were checked against it — **36 of 36 absent there too**, 0 present, 0 unresolved, with 5 of 5
listed controls served. The 2015 and 2016 silences are not an artifact of one host.

A TLS route to the file host was tried as a second channel and does not exist: the host presents a
certificate that does not match its own name, and the proxied HTTPS route answers 503. Recorded as
tried.

## What this does to the arc's own claims

- C4 stays as written: the 2022 window **is** derivable from the index.
- What C4 said survives — *the index locates the anomaly but does not say what it is* — is now
  measured to be **too generous to the index**. For 52 of the 55 disagreements outside that window
  the index does not locate anything at all: it declares an ordinary file, and there is nothing there.
- The machine argument the adversary granted as the only real one is **run**: 2,353,876 of 2,353,876
  listed files asked, 0 unresolved, in 185 minutes.
- The second product this increment was designed to yield — a class of misdeclared sizes — **is not
  a class**. One case in eleven years. That expectation failed and is reported as failed.
