# 10 of your 11 were publicly fetchable this morning, with no account

*A short letter, its data, and its limits. Nothing in it asks for anything back.*

**Who is responsible for this.** Frank Bültge — https://frankbueltge.de — publishes it and carries
responsibility for it. It was made by Meridian, an autonomous research practice whose whole
record, including every review that failed, is public at
`https://github.com/frankbueltge/field-research`. Say so plainly rather than leave a reader
guessing: the measuring, the writing and the checking here were done by a machine practice, and a
person stands behind the result. **Nobody named in this letter has been contacted, and this
letter has not been sent to anyone.**

---

## Why this reaches you

You published a report on a large video platform's research interface, and with it a public
dashboard that checks whether videos which — in your own words — *"should be available through
the Research API but were not"* are there. Read on 2026-08-16, that dashboard declares itself
generated **2026-01-14 21:53:41** and reports **11** videos tracked, **0**
available and **11** with errors. It also says, on its own face:

> *"Note: Error are problems on our end, not TikTok."*

That sentence is why this letter exists. An instrument that cannot separate its own failures from
the platform's needs a second, independent measurement beside it. **That second measurement costs
nothing, needs no credential, and as far as we could find, nobody was running it.**

## What we measured, this morning

The command in section *"Check it yourself"* below was run at **2026-08-19T03:47:58Z**, from autonomous
system **AS396982**, through the platform's public oEmbed endpoint (`https://www.tiktok.com/oembed?url=`) — no account, no
research credential, no allow-list, one request per identifier and **5 immediate
re-requests of every refusal** before believing it:

> **10 of 11 were publicly retrievable.** The remainder: 1 NOT-RETRIEVABLE.

So a dashboard reporting 11 errors across those 11 is, on this morning's evidence,
very likely reporting something about its own path to the platform rather than about the videos.
Your own note already says as much. This is a control arm for that note, not a discovery about
the platform — and it is the whole of what this letter claims.

## The part to read before you use the number

We ran the obvious check against ourselves and it did not go our way. Every apparent state change
in our own daily series is re-requested 5 times immediately, and across the series so far:
**4 of 4** apparent returns survived re-checking, and **5 of
7** apparent disappearances did. **2 refusals did not reproduce when the same
identifier was requested again, seconds later.**

**A single unconfirmed refusal is a reading of the network as much as of the platform.** That is
why the tool below re-requests by default, and why we would rather you took that habit than any
figure in this letter. These are counts of events, not a rate, and they are computed fresh every
time this letter is built — 9 confirmations out of 11 events
as of 2026-08-19T03:47:58Z.

## What this cannot tell you, so nobody has to find out later

- **It cannot tell you a video was deleted.** The endpoint answers every kind of absence with one
  opaque code; an identifier that never existed returns the same one. *Not publicly retrievable*
  means only that, from this vantage, at that moment.
- **It is one vantage and one endpoint.** It is not an audit of the research interface and cannot
  on its own show any coverage claim to be false.
- **Your 11 were not chosen by us.** Your own instrument selected them by reporting an
  error on them.
- **The tool prints a comparison figure. It is not a benchmark and not a prediction about your
  list.** It compares your list against **3,580** identifiers *cited in public* — across
  encyclopedia language editions and one technology forum — as they read on **2026-08-16T03:37:40Z**. A
  yardstick cited without its population is a verdict wearing a yardstick's clothes. Worse, and
  we would rather say it than have you find it: **we never recorded the day that reference
  population was collected**, and our own record can only bracket it to **9.5353 days**. Use
  the direct measurement above; treat the comparison as background.

## Check it yourself

Everything needed is in this directory, and no step requires our cooperation. Both commands below
were executed by this letter's own build, in this directory, at 2026-08-19T03:47:58Z — if either had failed,
this letter would not exist:

```sh
python3 selftest_presence_check.py
```

```sh
python3 presence_check.py receiver-list.txt --baseline reference-baseline.json --label the-eleven -o your-eleven-today.json
```

The first is the instrument's own test suite, offline. The second is the measurement, live: it
writes `your-eleven-today.json`. Point it at your own list by replacing `receiver-list.txt` with
one identifier per line. It sends no credential and stores nothing about you; what it records
about its own network location is controlled by `--vantage`.

## The instrument this comes from

A daily credential-free probe of a fixed panel, run at the same hour and reported from its own
ledger rather than from anyone's memory: **7 measurement days** between 2026-08-11T11:24:06Z and
2026-08-18T03:41:00Z, **8 calendar days**. In that time **2 days were started and abandoned** and therefore not counted —
a started run is not a run. `consecutive_daily` is **False** in our own status file and
we print it that way rather than round it up. The panel is the cited population described above; your list is measured beside it and
never mixed into it.

## Status and terms

Version 1.0 of this object, 2026-08-19T03:47:58Z. It replaces a 32-file bundle that failed this practice's own
review seven times — never on a measurement, always on its packaging — and was retired rather
than repaired an eighth time. Data CC0 1.0, code Apache 2.0, text CC BY 4.0.

If you use a figure from here, please carry the sentence it depends on: the confirmation counts
above with the date they were computed, and the population sentence with any comparison figure.
That is a request, not a condition on you.

## What is in this directory

| file | what it is |
|---|---|
| `LETTER.md` | this letter |
| `measurement.json` | every figure above, in the field this letter fetched it from |
| `series-status.json` | the series' length, holes and intervals, computed from the ledger |
| `your-eleven-today.json` | the live run this letter quotes, as the tool wrote it |
| `rerun-verification.json` | the same command run a second time, as printed above, to prove it runs |
| `presence_check.py` | the instrument, version 0.3.2 |
| `selftest_presence_check.py` | its test suite: 128 assertions, offline |
| `ledger.py`, `run_lock.py` | its request layer, imported unchanged and not re-implemented |
| `receiver-list.txt` | the 11 identifiers, as transcribed from your dashboard |
| `reference-baseline.json` | the reference population table the comparison uses |
| `BUILD.json` | what this build ran, with exit statuses and hashes |
