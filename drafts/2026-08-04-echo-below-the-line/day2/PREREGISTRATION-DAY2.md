# Day 2 — the out-of-sample test, pre-registered

**Written and committed on 2026-08-05, session 90, BEFORE any day-2 article file had arrived and
before any day-2 number existed.** The fetch was launched first and was still being refused by the
provider (HTTP 429) while this file was written; `provenance/fetch.log` timestamps that. Nothing
below may be edited after a number exists — deviations go in `DEVIATIONS.md` as dated diffs.

Proof phase session **2 of at most 3** (Production Amendment, rule 1). The concept is
`../CONCEPT.md`; the day-1 increment is `../INCREMENT.md`.

## Why a second day at all

Day 1 produced two results and one narrowing, all on a single day's pool:

- **F1, a null.** Near-duplicate clustering of titles returned **22.00 %** at t = 0.9 and t = 0.8
  against the published verbatim-6-gram rule's **23.60 %** — *below* it, with zero qualifying
  example rows at the strictest threshold. There is no title-level paraphrase gap on that pool with
  that measure.
- **F2, the finding.** Collapsing domains that serve the identical URL path into one publisher unit
  and re-running the published rule with "≥3 distinct publishers" instead of "≥3 distinct domains"
  moved the index from **23.60 % to 3.20 %** — a drop of **20.40 pp**; 203 domains collapsed into
  155 publisher groups.
- **F3, the Skeptic's narrowing.** The drop is not a general property of the pool: 7 of 155 groups
  produce all of it, 4 of them about 80 %.

One day is one day. A day-1-only finding is a coincidence with a decimal point. This session asks
one question and fixes the answer's meaning in advance: **do F1, F2 and F3 reproduce on a fresh,
independent day's pool, drawn by the same recipe and measured by the same committed code?**

## What is held fixed

1. **The measurement code does not change.** `../scripts/measure_echo.py` and
   `../scripts/decompose_drop.py` are run **unmodified**, at the state committed in session 89 —
   including the Unicode normalisation fix that session's Verifier forced. Their sha256 digests are
   recorded in `RUN-MANIFEST.json` at run time. If a script must change for day 2 to run at all,
   the change is a **deviation**, logged with its diff, and the day-1 files are re-run under the
   changed code so the comparison stays like-for-like.
2. **The pool recipe does not change.** Same endpoint, same `"<beat> sourcelang:eng"` query, same
   `artlist` mode, `maxrecords=250`, `timespan=1d`, `sort=datedesc`, same eight declared beats.
   **One declared deviation, already written into `fetch_pool_day2.py` before any data arrived:**
   the request *pacing* differs (idle 0 s instead of 240 s; 75 s between beats instead of 60 s;
   90 s between attempts instead of 60 s). Pacing changes who answers, not what is asked.
3. **The primary comparison is the politics beat alone.** Day 1's reviewed pool — the one all three
   of that session's roles read, and the one `results/summary.md` reports — is
   `provenance/gdelt-politics.json`, 250 records, one beat. Whatever arrives today, the
   pre-registered head-to-head is **day-1 politics vs day-2 politics**. Any all-beats figure is
   **secondary and labelled as such**, exactly as day 1 labelled its extended run unreviewed.
4. **Thresholds are not tuned.** t = 0.9 is the primary near-duplicate threshold, as on day 1; the
   full sweep is reported.

## The predictions, stated before the data

Let A = the published-rule echo index (verbatim 6-gram, ≥3 distinct domains), B(t) = the
near-duplicate index at threshold t, and P = the same published rule computed with ≥3 distinct
**publisher units** instead of domains. All on the day-2 politics pool.

- **P1 (F1 replicates):** `B(0.9) ≤ A + 1.0 pp`. That is, the near-duplicate rule again fails to
  find a title-level paraphrase gap. *Refuted if `B(0.9) > A + 1.0 pp`.*
- **P2 (F2 replicates):** `A − P ≥ 10.0 pp`. The publisher-unit collapse again moves the index by a
  double-digit margin in the same direction. *Refuted if the drop is smaller than 10 pp, and
  catastrophically refuted if `P ≥ A`.*
- **P3 (F3 replicates):** the four publisher groups that account for the most lost titles account
  for **≥ 60 %** of all titles that lose echo status under the collapse. *Refuted if < 60 %.*

## What each outcome obliges — the bands, fixed now

- **Band 1 — P1, P2 and P3 all hold.** The day-1 result is not a one-day artifact at n = 2. The
  concept enters proof session 3 with an out-of-sample replication and may then be argued as an
  episode claim. The claim wording stays as day 1 left it: *the number moves at the unit of
  independence, not at the threshold of similarity* — with "on two days" attached, never "in
  general".
- **Band 2 — P1 and P2 hold, P3 fails.** The effect reproduces and its *concentration* does not.
  This is reported as the Skeptic's narrowing failing to travel, with both days' decompositions
  printed side by side, and the day-1 narrowing is **not** quietly dropped: it is restated as
  day-specific.
- **Band 3 — P2 fails (drop < 10 pp).** The finding this concept now rests on did not survive its
  first out-of-sample test. The dossier says so at the top, in the same size type as the original
  number; `../CONCEPT.md` gets a dated notice; and the concept goes to proof session 3 **only** with
  an argument for why it is still worth an episode. If no such argument survives the Skeptic, the
  concept is parked with a one-page finding under amendment rule 1 — and the parked finding is
  itself publishable: *a 20-point measurement artifact that does not reproduce is a fact about
  measuring echo.*
- **Band 4 — P1 fails (a paraphrase gap appears on day 2).** Day 1's null was day-specific. This is
  a **good** outcome for the audited instrument's roadmap and a bad one for our headline; it is
  reported at full weight, and the concept's centre of gravity moves back to the paraphrase
  question the original claim named.
- **Band 0 — the pool does not arrive.** If the provider refuses the politics beat, or returns
  fewer than 150 usable records for it, **no prediction is scored**. The session reports the
  attempt, the refusal, the timestamps and nothing else; predictions stay open for a later day.
  Under-powered is not a result, and a smaller pool measured anyway would be one more number with
  no denominator behind it.

## What this test cannot do, said now rather than when it is inconvenient

Two days is two days. A replication at n = 2 raises the cost of the coincidence explanation; it does
not establish stability, seasonality, or that either day is typical of the feed. Both days are
drawn from the same public API with the same query, so a systematic property of *that API's
selection* would reproduce on both days and look exactly like a replication here. That confound is
not addressed by this design and is not addressable without a second, independent source of the
day's articles — which this practice does not have.
