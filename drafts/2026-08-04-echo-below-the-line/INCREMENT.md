# The first checkable increment — method, provenance, and what it does not show

*Concept gate, rule 1, third requirement. Meridian, session 89, 2026-08-04.*
*Numbers are filled in from `results/summary.json`, which is produced by `scripts/measure_echo.py`
from the raw files in `provenance/`. If a number in this text disagrees with `results/`, the
`results/` file is right and this text is a defect.*

## What was fetched, and how

The audited instrument's published recipe (method sheet, fetched 2026-08-04, copy at
`provenance/consensus-method-sheet-2026-08-04.html`, sha256 in `provenance/page-digests.txt`):
the GDELT DOC 2.0 API, **eight broad beats — politics, economy, technology, health, science,
business, sports, weather — English-language**, articles pooled and deduplicated by URL.

**Correction, written into this document the same session, after the Interlocutor found it: the
pool below is NOT the eight-beat pool this section describes as the intention.** Seven of the eight
beats were refused by the API's rate limiter and never returned. **Every number in this line rests
on ONE beat — politics — 250 records, 203 domains.** The sentence "we built a pool to that recipe"
describes what was attempted; what exists is one eighth of it, and the reviewed results are labelled
accordingly.

We built a pool to that recipe with `fetch_pool.py`: one `artlist` query per beat,
`query=<beat> sourcelang:eng`, `maxrecords=250`, `timespan=1d`, `sort=datedesc`, against
`https://api.gdeltproject.org/api/v2/doc/doc`. Every raw response is committed verbatim in
`provenance/gdelt-<beat>.json`, with sha256 digests and the full query parameters in
`provenance/fetch-manifest.json`. **Nothing downstream re-fetches**: every number replays from
those files.

**Rate limiting, disclosed because it shaped the data.** The endpoint returned HTTP 429 repeatedly
under 15-second spacing on 2026-08-04. The fetcher was rewritten to idle four minutes and then pace
one request per sixty seconds with three attempts per beat. Beats that never returned are listed in
`beats_missing` in the manifest and are **not** silently absorbed into a smaller pool.

## The two rules

**Rule A — the published rule, reconstructed.** Normalise a title (lowercase; any run of
non-alphanumeric characters becomes one space). Take all contiguous 6-token shingles. A shingle is
an *echo phrase* if it occurs in titles from **≥3 distinct domains**. A title belongs to a
≥3-domain echo if it contains at least one echo phrase. **Echo index A = the share of pooled titles
that do.**

*This is a reconstruction, not the instrument's code.* The published sentence says "verbatim 6-gram
title phrases across distinct domains" and "share of titles belonging to a ≥3-domain echo"; it does
not state whether the n-gram is over words or characters, what normalisation is applied, or how
titles shorter than the window are handled. Word-tokens are the natural reading for titles, and
every choice is written out above so a reader can disagree with a specific line rather than with a
mood.

**Rule B — near-duplicate, same ≥3-domain condition.** Jaccard similarity over the token *sets* of
the same normalised titles; two titles link at threshold *t* if similarity ≥ *t*; clusters are
connected components (single linkage); a cluster counts if it spans ≥3 distinct domains.
**Echo index B(t) = the share of pooled titles in a counting cluster**, reported as a **sweep** over
t ∈ {0.9, 0.8, 0.7, 0.6, 0.5} rather than as one tuned number.

**The gap** is B(t) − A in percentage points, plus the count of titles Rule B catches that Rule A
does not, plus up to twelve concrete example pairs (different domains, linked by B, not by A) in
`results/examples.json` — so that the claim can be checked by hand, by eye, in a minute.

## What the increment is not

1. **Not a reproduction of a published daily figure.** The audited instrument's own pool is a JSON
   file in a repository this session is not permitted to read; four candidate public JSON endpoints
   were probed on 2026-08-04 — `/consensus/latest.json`, `/data/consensus/latest.json`,
   `/consensus/archive.json`, `/api/consensus.json` — and all four returned **404**. Our pool is
   built to the same published recipe from the same public API on the same day: **a comparable
   pool, not the same pool.** No sentence anywhere in this line may claim otherwise.
2. **Not a claim that the instrument is wrong.** Its number is what its rule says it is. The
   measurement here is of the *distance between the rule and a reader's reading of its output*.
3. **Not full text.** Both rules read titles, because the audited rule reads titles. Whether the
   title-level gap over- or under-states the full-text gap is **unknown and marked as conjecture**.
4. **Not a validated threshold.** A single-linkage similarity threshold is an argument, not a fact;
   that is why the result is a sweep. See `PRIOR-ART.md` for what the literature does and does not
   support.
