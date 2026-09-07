# The autoloop series — what each row means, and when the schema moved

One line a night in `series.jsonl`, written by `run_series.py` from a corpus fetched the same
minute. The corpus itself is never committed; each row carries its SHA-256 and its record count.
`runs/<day>.json` holds that night's 66 test outcomes without the corpus.

**The rule for this file: a field's meaning never changes. New fields are added beside the old
ones, dated here. A row written before a field existed does not carry it, and must not be
back-filled — a series with retro-fitted values is not a series.**

## Schema history

**2026-09-03 (session 150) — opened.** `day`, `fetched_utc`, `corpus_records`, `corpus_sha256`,
`hypotheses`, `raw_findings`, `bh_survivors`, `bonferroni_survivors`, `review_kills`,
`replicating_split_half`, `null_findings_per_run`, `null_per_test_rate`,
`distinct_pairs_among_bh`, `review_disagreements`, `breaks`, `seconds`.

**2026-09-05 (session 152) — three fields added, none changed.**

| field | meaning |
|---|---|
| `questions_awake` | of the enumerated questions, how many can produce a claim at all, decided by `liveness.py` from the corpus margins before any test is run |
| `questions_asleep` | the rest: no assignment of grouping labels consistent with the margins reaches α, so their null-world rejection rate is a structural zero rather than a measurement |
| `null_per_test_rate_awake` | the per-test null rejection rate over the awake questions only |

`null_per_test_rate` keeps its 2026-09-03 definition exactly — the average over **every**
enumerated question — and is still computed that way, so the two rows written on 2026-09-03 and
2026-09-04 remain comparable with every row after them. Where the two rates differ, the
difference is the dilution: see `artifacts/cycle-002/2026-09-05-which-questions-count/`.

## Runs, and what the schedule has actually done

The nightly job is `.github/workflows/autoloop.yml`, cron `15 3 * * *` (03:15 UTC). Its record
so far, read from the GitHub Actions API rather than assumed:

- **2026-09-03** — row written by hand, at the session that built the loop. Marked here because a
  seeded first row is not a scheduled run.
- **2026-09-04** — first scheduled run. It fired at **07:55 UTC**, four hours and forty minutes
  after the hour in its cron expression, and went green. GitHub does not guarantee the minute of
  a scheduled workflow; the series must therefore be read by `day`, never by hour.
- **2026-09-05** — at 03:36 UTC, no run for this day was listed. Not a red night and not a hole:
  the day was younger than the delay the previous night showed.

## 2026-09-05, filed after the session landed — what the series is not, yet

The night of 2026-09-05 ran with the PRE-CHECK stage in place, went green, and wrote the first row
carrying `questions_awake`, `questions_asleep` and `null_per_test_rate_awake` (66 / 0 / 4.9273 %).
That part worked. **What it also showed is that the series is not yet measuring what its name
says.**

The 2026-09-04 and 2026-09-05 rows carry **different corpus digests** —
`9926d042c8ed…` against `d375abdee83e…` — and **identical measurements**: 2,039 records both
nights, 17 raw findings, 13 Benjamini–Hochberg survivors, a null per-test rate agreeing to all
sixteen digits (0.049272727272727274). Comparing the two per-run files test by test:

```
tests differing in p or n1 between runs/2026-09-04.json and runs/2026-09-05.json: 0 of 66
```

So the corpus **bytes** changed while every column the loop actually tests did not. The fetcher
returned the same papers with some field altered, and the loop recorded it as a second night.

**Consequence for anyone reading this file: the three rows are not three measurements.** Two of
them are one measurement taken twice. Do not read a variance, a trend or a stability claim off
them, and do not count nights — count distinct test vectors. The instrument this needs is a check
in `run_series.py` that compares the night's test vector against the previous night's and records
whether the corpus moved at all; until that exists, the honest description of the series is *one
seeded run plus one arXiv snapshot measured twice*.

**Why this is not repaired here.** It is a defect in `fetch.py`'s query window, not in the series
format, and diagnosing it means reading what the fetcher asks arXiv for and what changed between
the two payloads. That is a session's work, not a note's. Filed as open question 41.

## 2026-09-07 (session 154) — open question 41, diagnosed, and one guess above was wrong

Measured with `tools/autoloop/corpus_drift.py` and `tools/autoloop/freshness_probe.py`; data at
`presentations/cycle-002/data/`. Pre-registration and verdicts:
`presentations/cycle-002/PREREGISTRATION.md`.

**Two separate things were happening, and the note above named only one of them.**

1. **`corpus_sha256` cannot report that the corpus stood still.** `run_series.py` hashes the
   corpus *file*, and `fetch.py` writes `fetched_utc` and `seconds` into that file. Two corpora
   fetched **97 seconds apart** on 2026-09-07 had **different file digests, identical record
   digests, and identical id sets — Jaccard 1.000**. The field that made three nights look like
   three measurements changes every night by construction, whatever the records do.

2. **The corpus was not frozen — the source's publication calendar was.** The note above guessed
   a defect in the query window. That guess is **wrong**, and the pre-registered prediction built
   on it (P2) is **refuted**: a corpus fetched on 2026-09-07 shares **0 of 66** test outcomes with
   the committed run of 2026-09-06, and carries 2,072 records against 2,039. The corpus moves.
   What does not move is the source over a weekend: arXiv states it posts submissions publicly
   **Sunday through Thursday, with no announcements Friday or Saturday**
   (`info.arxiv.org/help/availability`, read 2026-09-07). Announcements land at 20:00 US Eastern,
   which in September is **00:00 UTC the next day** — so nothing new reaches a 03:15 UTC cron on a
   Saturday or a Sunday. The three identical nights were **Friday, Saturday and Sunday**.

**So the series is not one measurement — that claim is withdrawn** — but a nightly cadence over a
five-day-a-week source produces **two structurally duplicate rows a week**, and until today the
series had no field that could tell a reader which rows those were.

### Schema, 2026-09-07 (session 154) — three fields added, none changed

| field | meaning |
|---|---|
| `records_digest` | SHA-256 over the records array alone, id-sorted, with no timestamp — the digest `corpus_sha256` was mistaken for |
| `test_vector_digest` | SHA-256 over the night's 66 outcomes: key, p, and both group sizes |
| `vector_repeats_previous` | true when this night's vector digest equals the previous committed run's; `null` when there is no previous run |

`corpus_sha256` **keeps its 2026-09-03 definition and its defect**, so every row stays comparable.
Nothing is back-filled: the four rows written before today do not carry these fields and must not
be given them. The nights they cover can still be counted the way this session counted them —
`corpus_drift.py` recomputes a vector digest for every committed run file — but that is a
recomputation, not a row.

**Read the series by distinct test vector, not by night.** Over 2026-09-03 to 2026-09-06:
**four nights, four recorded corpus digests, two distinct test vectors.**
