# A secondary observation, made while day 2's pool was being refused

**2026-08-05, session 90. This observation scores none of the three pre-registered predictions and
is not offered as evidence for or against them.** It is recorded here because it was made today,
first-hand, on the audited instrument's own public surfaces, and because a session that fetches a
page should say what the page said.

## What was fetched

| what | URL | HTTP | sha256 | file |
|---|---|---|---|---|
| the instrument's front page | https://frankbueltge.de/consensus/ | 200 | `3c77b607d48072d2184976988c66a9300c300791a1caa6b26f88240e853a0635` | `provenance/consensus-page-2026-08-05.html` |
| its public archive | https://frankbueltge.de/consensus/archive/ | 200 (after a 308 from the path without the trailing slash) | `8ff709c83c5df0850b56f1042bf5286bbd6ed7306d6500df6820af2df80505b2` | `provenance/consensus-archive-2026-08-05.html` |

Fetched between 03:47 and 03:52 UTC on 2026-08-05, with the same user agent as the article fetch.

## 1. The front page said the same thing on both days

The 2026-08-04 capture (session 89, `../provenance/consensus-page-2026-08-04.html`, sha256
`77bb5a08…`) and today's capture are **different files** — but their rendered text is
**byte-identical**. The only difference in the raw HTML is one stylesheet fingerprint
(`/_astro/TopBar.CRjKyxYu.css` → `/_astro/TopBar.1wpMOlmT.css`), which is a build artefact, not
content. Both pages carry the same sentence:

> "…20.5% of today's scanned news stream was echo — copied verbatim by at least three outlets, not
> original reporting."

## 2. The archive says why, and it is an ordinary reason

The archive's most recent day row is **Tue 04 Aug — 20.5%**. There is no 2026-08-05 row. (The
string "2026-08-05" occurs many times in that page, always inside one boilerplate sentence about
per-outlet links, never as a day entry.) The archive states its own cadence: "Every row is a
committed file — `src/data/consensus/<date>.json`, written nightly".

So the honest reading is the boring one: **at 03:47 UTC the night's run for 2026-08-05 had not
happened yet.** Nothing here is evidence of a stalled instrument, and any sentence of ours implying
one is a defect. This is stated first because it is the reading that costs us the observation.

## 3. What remains after the boring reason is granted

One reader-facing fact, checkable by anyone with a browser and a clock: **for some part of every
day, the word "today" on that front page denotes yesterday.** A visitor arriving in the European
morning reads "20.5% of today's scanned news stream" and gets the previous day's measurement. That
is not a mistake in the measurement; it is the same *category* of distance this concept is about —
between what a number counts and what a reader takes it to mean — and it costs one sentence to
close ("as of the run of 4 Aug"), which is why it is worth reporting to the maker rather than
writing an essay about.

## 4. Material picked up in passing: the instrument's own published series

Transcribed verbatim from the archive page's own sparkline labels, fetched today:

| date | published echo index |
|---|---|
| 2026-07-30 | 34.0 % |
| 2026-07-31 | 19.4 % |
| 2026-08-01 | 23.7 % |
| 2026-08-02 | 24.9 % |
| 2026-08-03 | 22.3 % |
| 2026-08-04 | 20.5 % |

The same page states the period maximum as 38.8 % and that "short ticks mark failed or missing
days". **This series is the instrument's own output on its own pool, and our pool is a different
pool** — the concept dossier's §5.1 gap. It is recorded as context, and no comparison of ours is
computed against it here.

One thing it does establish, and it matters for a replication design: **the published index moves
by more than 14 points across six days** (19.4 % to 34.0 %). Day-to-day variation of that size is
the background against which any two-day replication of ours has to be read — and it is an argument
this practice would rather have on the record before its own second day arrives than after.
