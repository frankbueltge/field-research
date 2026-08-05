# What was measured, and how — the archive audit

*Written 2026-08-05, session 91, while the ownership evidence was still being gathered. This file
describes the procedure only. **It contains no result**; the results are in `RESULT-ARCHIVE.md` and
`results/scores.json`, written after the evidence landed.*

## The object

*The Consensus*, a daily instrument at https://frankbueltge.de/consensus/ running since 2026-06-21.
Its published rule, from its own method sheet: pool articles → count verbatim 6-gram title phrases
across distinct domains → the most replicated is the day's headline; **echo index = share of titles
belonging to a ≥3-domain echo**. Read first-hand in its own source: `MIN_DOMAINS = 3`,
`SHINGLE_N = 6` (`provenance/SOURCE.md`).

## The material

The instrument's own committed dated snapshots, 46 of them, `2026-06-21` … `2026-08-05`, at the site
repository commit recorded in `provenance/SOURCE.md`. Each carries, for the day's headline cluster
and its runner-up: the phrase, the published `domain_count`, the **masthead list**, the instrument's
own `syndication` classification, and the day's `echo_index` and `soft_echo_index`.

**86 clusters, 596 distinct domains, 2,270 domain mentions.**

## The three stages

**Stage 0 — read** (`scripts/extract_clusters.py`). Only dated files; `latest.json` is excluded as a
duplicate. Per-file sha256 recorded. This stage found the masthead cap (see `DEVIATIONS.md` D1).

**Stage A — mechanical candidates** (`scripts/gather_dns.py`, `scripts/gather_http.py`,
`scripts/group_candidates.py`). Union-find over three relations, none of them a judgement:

- **A1** same registrable domain (explicit two-label suffix list in the script);
- **A2** identical authoritative nameserver set, over DNS-over-HTTPS, 596/596 answered;
- **A3** identical final host after redirects, 519/596 answered.

**Stage B — the evidence gate.** A candidate unit counts only where a **published ownership source**
names its members as one operator, and only for the members that source names (`DEVIATIONS.md` D2).
Candidate units are never merged with one another, even under one operator; an owner-merged variant
is computed separately and reported only as a secondary figure.

Two ownership specialists were convened for Stage B, each given half of the 22 candidate units that
touch the primary cluster set, each instructed that an honest *no evidence* is worth more than a
plausible guess and that shared nameservers often mean shared hosting rather than shared ownership.
Their reports are published at `evidence/`.

## What is scored

Fixed in `PREREGISTRATION-ARCHIVE.md` before any of the above ran:

- **Primary set:** headline clusters whose published `domain_count` equals their masthead-list length
  — 30 of 43, the rest excluded by D1 because their lists are truncated.
- **U** = distinct publisher units among a cluster's mastheads.
- **Q1** share of primary clusters with **U < 3** ≥ 25 % · **Q2** median mastheads/U ≥ 2.0 ·
  **Q3** at least one U < 3 cluster carries no syndication label from the instrument itself.

`scripts/score_archive.py` computes all of it; `scripts/selftest_score.py` checks the scorer against
fixtures worked out by hand — **19 assertions, all passing**, run before the evidence existed and
committed at that state.

## Two things measured outside the pre-registration, and labelled as such wherever they appear

1. **The instrument's own paraphrase surplus.** Its snapshots carry `soft_echo_index`, which its
   source shows to be the implemented v2 near-duplicate index seeded with the verbatim clusters, so
   that `soft ⊇ verbatim` by construction. The difference between the two published numbers is the
   instrument's own measurement of what paraphrase adds — the quantity day 1 tried to estimate from
   outside. Computed in `results/soft-vs-hard.txt`.
2. **The one day with an evidence track.** From 2026-08-05 the snapshots record a per-outlet article
   URL. On that one day, and only that day, day 1's original rule — domains serving the identical URL
   path collapse into one unit — can be applied literally to the instrument's own record. Computed in
   `results/path-evidence-2026-08-05.txt`.

Neither is pre-registered; neither is scored; both are reported as observations with their n stated.
