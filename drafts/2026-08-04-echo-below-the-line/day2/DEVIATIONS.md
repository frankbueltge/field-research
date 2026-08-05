# Deviations from the day-2 pre-registration

*Every departure from `PREREGISTRATION-DAY2.md`, dated, with what it changed. Written as the
session ran, not reconstructed afterwards. A deviation is not a failure; an undeclared one is.*

## D1 — request pacing (declared **before** any data existed)

The pre-registration itself carries this one, and `fetch_pool_day2.py`'s docstring carried it before
the first request was sent: session 89 idled 240 s and paced 60 s; this session idled 0 s, paced
75 s between beats and 90 s between attempts. **Effect on the measurement: none possible.** Pacing
changes who answers, not what is asked. Recorded because the fetch is part of the method.

## D2 — the first pass was stopped by hand, and the beat order changed to politics-first

At 03:44:30 UTC, after the primary beat had been refused three times (03:37:27, 03:39:08,
03:40:52 — all HTTP 429), the first pass was killed mid-run. Left alone it would have spent roughly
forty minutes of provider cooldown on the seven beats the pre-registration does **not** score before
returning to the one it does. A second pass was started asking for **politics first**, with 240 s
between requests.

**Made while zero day-2 records existed**, so it cannot have been steered by any number, and the
kill is timestamped in `provenance/fetch.log`. **What it costs, stated plainly:** the eight-beat
order in `fetch_pool_day2.py` was itself a copy of session 89's, and re-ordering it means the
secondary all-beats figure — if any beat ever arrives — is drawn under a different order than day
1's. The primary comparison is unaffected: a single-beat query does not depend on what was asked
before it.

## D3 — the measurement scripts were run as byte-identical copies, not in place

`scripts/measure_echo.py` resolves its input and output directories from **its own file location**
(`WORKDIR = dirname(dirname(abspath(__file__)))`), not from the working directory. Running it over a
second day's pool therefore means either moving day 1's raw files out of the way — unacceptable, they
are committed evidence — or running a copy from a directory of its own.

The copies at `day2/scripts/` and `day1-rerun/scripts/` are **byte-identical** to the session-89
originals; `run_manifest.py` records both sha256 digests side by side and an `identical` flag, so
"unmodified" is checkable rather than asserted:

- `measure_echo.py` — `d4af778bc5c5081da1e1a17037db9f8662321c43b0468e7cdfec0b96c6927116`
- `decompose_drop.py` — `5b555c2c86fc64833ace6e524032c942cded71773b41a24fe7f8bab6ce01b078`

**One thing this cost, and it is recorded because it nearly went wrong silently.** The first attempt
at the day-1 re-run ran the original script from a different working directory, and because the
script anchors on its own location it read the **three-beat** parent pool and **overwrote day 1's
committed `results/`** with a run over a different pool (442 domains against 203). The overwrite was
caught by `git status` within the minute and reverted with `git checkout`; the committed day-1
results are byte-identical to what session 89 landed. Nothing downstream had read the bad state. It
is written down because a session that only records the mistakes it failed to catch is not keeping a
record.

## D4 — day 1 was re-run under identical flags, and it reproduces

The pre-registration requires the two days to be compared like-for-like. Day 1's **committed**
decomposition was produced under the pre-fix ASCII-only normalisation
(`"normalisation": "ascii-only"` in `results/drop_decomposition.json`), while the current script
defaults to Unicode-aware. So day 1's politics pool was re-run from its committed raw file
(sha256 `9a254eed…`) under today's defaults, into `day1-rerun/`.

**It reproduces exactly.** Pool 250, domains 203, publisher groups 155, A = 23.60 %, B(0.9) =
22.00 %, P = 3.20 %, drop = 20.40 pp, total drop 20.40 pp, top-four 16.40 pp, 7 groups causing any
loss — every figure identical to the committed day-1 run, with `normalisation` now reading
`unicode-aware`. The Verifier's session-89 fix therefore changes nothing on this pool, which is
worth knowing: the fix mattered for the diagnostic count it was raised against, not for the
headline.

`score_day2.py` prefers `day1-rerun/` for exactly this reason and says so in its own output when it
has to fall back.

## D5 — a secondary observation was made that the pre-registration does not cover

While the pool was being refused, the audited instrument's own front page and public archive were
fetched and committed (`OBSERVATION-ARCHIVE.md`). It scores no prediction and is labelled as
scoring none. It is listed here so that nobody has to wonder later whether it was folded into the
result quietly.
