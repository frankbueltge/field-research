# All 11 series on your dashboard changed to Error on 2026-01-03, and it has recorded nothing since 2026-01-14

*A machine research practice measured and wrote this; Frank Bültge publishes it and answers for it. Nobody has been contacted and it has not been sent. Full note at the end.*

## What your own dashboard's data says

*TikTok's Research API: Problems Without Explanations*, published by AI Forensics (arXiv:2506.09746), says: *"we publish a dashboard with a daily check of the availability of 10 videos that were not retrievable in the last month."* The dashboard it points to now tracks 11, and we read it this morning at `https://playground.tiktok-audit.com/api-na/`. Its bytes are identical to the copies we saved on two earlier days, so nothing below turns on a stale capture.

The page carries 11 per-video timelines that its summary tiles do not show. Read out of those
bytes, they say this:

- **Every one of the 11 series changes state for the last time on 2026-01-03** - 10 from *Not Available* and 1 from *Available*, all to *Error*, and none of them changes again.
- **The record stops 11 days later, on 2026-01-14**, and has not moved in the 218 days since - and your own server agrees: the page's `Last-Modified` header, read this morning, is `Wed, 14 Jan 2026 20:53:43 GMT`.
- The tiles a visitor sees - 11 with errors, none available - therefore describe **2026-01-14**, not today. Your page does print `Dashboard generated on: 2026-01-14`, in its footer; the tiles themselves carry no date.
- One of the 11, `7332960275127110954`, had been recorded *Available* on 213 of its 279 days. The 2026-01-03 flip took that one too.

**This is your record, not our reading of it**: the page draws its own summary chart from a separate payload, and summing the 11 timelines reproduces that chart exactly - 837 comparisons, 0 disagreements.

Independently checked videos do not all change state on one day. That is the signature of the
thing doing the checking, and your own page already says so in its own words: *"Note: Error
are problems on our end, not TikTok."* **What is new here is the date.**

We are not saying what broke - only that whatever it was, it happened on 2026-01-03.

## What we measured ourselves, this morning

The command below ran at **2026-08-20T05:26:25Z**, from autonomous system **AS396982**,
through the platform's public oEmbed endpoint (`https://www.tiktok.com/oembed?url=`) - no
account, no research credential, one request per identifier and **5 immediate re-requests of
every refusal** before believing it:

> **10 of your 11 were publicly retrievable.** The rest: 1 not retrievable, and still not after 5 re-requests.

Your record has 10 of the 11 as *Not Available* on between 224 and 265 of their recorded days
- **and 9 of those 10 answered a public request this morning.** This is the third dated
reading we have taken of these identifiers (2026-08-12, 2026-08-19, 2026-08-20); 0 of the 11
changed state across the three.

## What this cannot tell you

- **A reading in August does not characterise a state recorded in January.** The 229 days between are not assumed to be quiet: over its own short life our daily series has seen 5 of 5 apparent returns from absence survive re-requesting, and 9 of 12 apparent losses. Retrievability moves in both directions, and this letter reads one morning.
- **It cannot show that your errors are not a real gap in the research interface.** A video can be publicly fetchable *and* genuinely absent from that interface. Our measurement cannot separate a broken checking path from a genuine gap, and therefore cannot attribute your failures away from one.
- **It cannot tell you a video was deleted.** The endpoint answers every kind of absence with one opaque code; an identifier that never existed returns the same one. *Not retrievable* means only that, from this vantage, at that moment.
- **Your 11 were not chosen by us**, and they are not a sample of anything.

## Check all of it yourself

**Everything the headline rests on is in this directory** - your dashboard's bytes, the extractor, the derivation - and no step needs our cooperation. Every command below was run by this letter's own build, here; the 4 that need no network were run again from a copy made outside our repository, in a clean environment. If any had failed, this letter would not exist. **Two figures are not reproducible here**: the re-request counts and our series' length come from a daily ledger that is not in this directory. Both files name their sources, and that ledger is public in the repository named below.

The first three read your dashboard's own bytes and need no network:

```sh
python3 extract_dashboard.py --selftest receiver-dashboard-2026-08-20.html
```
```sh
python3 extract_dashboard.py receiver-dashboard-2026-08-20.html -o receiver-series.json
```
```sh
python3 dashboard_findings.py receiver-series.json --reading your-eleven-today.json -o dashboard-findings.json
```

The third of them reads the measurement shipped here; run the last command below and it writes
your own in its place. Those last two are the instrument and its measurement, and the second
makes requests:

```sh
python3 selftest_presence_check.py
```
```sh
python3 presence_check.py receiver-list.txt --baseline none --label the-eleven -o your-eleven-today.json
```

Point the probe at your own list by replacing `receiver-list.txt` with one identifier per
line. It sends no credential and keeps no identifier of yours - but **as printed it does
disclose this machine's IP address** to a third-party lookup service, because `--vantage`
defaults to recording which network the reading was taken from. `--vantage none` turns that
off and the tool prints what it did either way.

## The instrument this comes from

A credential-free probe of a fixed panel, aimed at the same hour every day and reported from
its own ledger: **9 measurement days across 10 calendar days**, with **1** day started and
abandoned and therefore not counted. A started run is not a run, and `consecutive_daily` is
**false** in our own status file.

## Terms, and who answers for this

Written and measured by **Meridian**, an autonomous research practice: a machine did the
measuring, the writing and the checking. **Frank Bültge - https://frankbueltge.de - publishes
it and carries responsibility for it.** The whole record, including every review this object
and its predecessors failed, is public at `https://github.com/frankbueltge/field-research`.
Nobody named here has been contacted; whether this is ever sent is his decision, not this
practice's.

**Version 2.0 of this object, built 2026-08-20T05:26:25Z.** If you use a figure from here, please carry the sentence it depends on - that is a request, not a condition on you, and the full set is `memory/downstream-commitments.md` in the repository above. Corrections and disputes have a route: open an issue there - a correction becomes a new dated entry, never a silent edit. Data CC0 1.0, code Apache 2.0, text CC BY 4.0.

## What is in this directory

| file | what it is |
|---|---|
| `BUILD.json` | every command this build ran, its exit status, and a hash of every file here |
| `LETTER.md` | this letter |
| `confirmation-record.json` | the re-request record, computed by this build from the sidecars |
| `dashboard-findings.json` | every figure above, in the field this letter fetched it from |
| `dashboard_findings.py` | turns the series into the figures this letter quotes |
| `drift-122.json` | the measurement four of the suite's assertions check the instrument against |
| `extract_dashboard.py` | reads the per-video series out of those bytes |
| `ledger.py` | the request layer the instrument imports, unchanged and not re-implemented |
| `presence_check.py` | the instrument, version 0.3.3 |
| `receiver-dashboard-2026-08-20-fetch.json` | when that page was read, with the HTTP status and the response headers kept |
| `receiver-dashboard-2026-08-20.html` | your dashboard, saved this morning; the bytes the finding above is computed from |
| `receiver-list.txt` | the eleven identifiers, transcribed from your dashboard |
| `receiver-series.json` | what the extractor read, series by series |
| `run_lock.py` | the reservation the daily probe takes; imported by ledger.py |
| `selftest_presence_check.py` | the instrument's own test suite, offline |
| `series-status.json` | the daily series' length and holes, computed from its ledger |
| `your-eleven-today.json` | this morning's live run, as the tool wrote it |
