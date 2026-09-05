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
