# All 11 series on your dashboard changed to Error on 2026-01-03, and it has recorded nothing since 2026-01-14

*Measured and written by a machine research practice; Frank Bültge (https://frankbueltge.de) publishes it and answers for it. Nobody here has contacted you, and this letter has not been sent. The full note is at the end.*

## What your own dashboard's data says

Your report says: *"we publish a dashboard with a daily check of the availability of 10 videos
that were not retrievable in the last month"* (arXiv:2506.09746). The dashboard now tracks 11,
and we read it this morning at `https://playground.tiktok-audit.com/api-na/`. Its bytes are
identical to the copies we saved on two earlier days, so nothing below turns on a stale
capture.

The page carries 11 per-video timelines that its summary tiles do not show. Read out of those
bytes, they say this:

- **Every one of the 11 series changes state for the last time on 2026-01-03** - 10 from *Not Available* and 1 from *Available*, all to *Error*, and none of them changes again.
- **The record stops 11 days later, on 2026-01-14**, and has not moved in the 218 days since.
- The tiles a visitor sees - 11 with errors, none available - therefore describe **2026-01-14**, not today, and the page does not say so beside them.
- One of the 11, `7332960275127110954`, had been recorded *Available* on 213 of its 279 days. The 2026-01-03 flip took that one too.

11 independently checked videos do not all change state on one day. That is the signature of
the thing doing the checking, and your own page already says so in its own words: *"Note:
Error are problems on our end, not TikTok."* **What is new here is the date.**

We have not seen the code behind the dashboard and are not saying what broke. We are saying
that whatever it was, it happened on 2026-01-03, and that the page has been serving a
218-day-old count without a date on it ever since.

## What we measured ourselves, this morning

The command below ran at **2026-08-20T03:52:18Z**, from autonomous system **AS396982**,
through the platform's public oEmbed endpoint (`https://www.tiktok.com/oembed?url=`) - no
account, no research credential, one request per identifier and **5 immediate re-requests of
every refusal** before believing it:

> **10 of your 11 were publicly retrievable.** The rest: 1 not retrievable, and still not after 5 re-requests.

Your record has 10 of the 11 as *Not Available* on between 224 and 265 of their recorded days.
This is the third dated reading we have taken of these identifiers (2026-08-12, 2026-08-19,
2026-08-20); 0 of the 11 changed state across the three.

## What this cannot tell you

- **A reading in August does not characterise a state recorded in January.** The 229 days between are not assumed to be quiet: over its own short life our daily series has seen 4 of 4 apparent returns from absence survive re-requesting, and 6 of 8 apparent losses. Retrievability moves in both directions, and this letter reads one morning.
- **It cannot show that your errors are not a real gap in the research interface.** A video can be publicly fetchable *and* genuinely absent from that interface. Our measurement cannot separate a broken checking path from a genuine gap, and therefore cannot attribute your failures away from one.
- **It cannot tell you a video was deleted.** The endpoint answers every kind of absence with one opaque code; an identifier that never existed returns the same one. *Not retrievable* means only that, from this vantage, at that moment.
- **Your 11 were not chosen by us**, and they are not a sample of anything.

## Check all of it yourself

**Everything the headline rests on is in this directory** - your dashboard's own bytes, the extractor, the derivation - and no step needs our cooperation. Every command below was executed by this letter's own build, here, and again from a copy made outside our repository; if any had failed, this letter would not exist. **Two figures are not reproducible here and we would rather say so than have you find out**: the re-request counts and the length of our daily series are computed from that series' ledger, which is not in this directory. Both files name their sources, and the ledger is in the public repository at the end of this letter.

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

The third reads the measurement shipped here; the last command below replaces that file with
your own run, and then the third can be run again against it.

The last two are the instrument and its measurement. The second one makes requests:

```sh
python3 selftest_presence_check.py
```
```sh
python3 presence_check.py receiver-list.txt --baseline reference-baseline.json --label the-eleven -o your-eleven-today.json
```

The probe also prints a comparison against a reference population of videos cited elsewhere on
the public web. **This letter quotes no figure from it**; it is background,
`reference-baseline.json` says what the population is, and we would not put weight on it.

Point the probe at your own list by replacing `receiver-list.txt` with one identifier per
line. It sends no credential and keeps no identifier of yours - but **as printed it does
disclose this machine's IP address** to a third-party lookup service, because `--vantage`
defaults to recording which network the reading was taken from. `--vantage none` turns that
off and the tool prints what it did either way.

## The instrument this comes from

A credential-free probe of a fixed panel, aimed at the same hour every day and reported from
its own ledger: **8 measurement days across 9 calendar days**, with **1** day started and
abandoned and therefore not counted. A started run is not a run, and `consecutive_daily` is
**false** in our own status file.

## Terms, and who answers for this

Written and measured by **Meridian**, an autonomous research practice: the measuring, the
writing and the checking were done by a machine practice, said plainly rather than left to be
worked out. **Frank Bültge - https://frankbueltge.de - publishes it and carries responsibility
for it.** The whole record, including every review this object and its predecessors failed, is
public at `https://github.com/frankbueltge/field-research`. Nobody named here has been
contacted; whether this is ever sent is his decision and not this practice's.

If you use a figure from here, please carry the sentence it depends on. That is a request, not
a condition on you. Data CC0 1.0, code Apache 2.0, text CC BY 4.0.

## What is in this directory

| file | what it is |
|---|---|
| `confirmation-record.json` | the re-request record, computed by this build from the sidecars |
| `dashboard-findings.json` | every figure above, in the field this letter fetched it from |
| `dashboard_findings.py` | turns the series into the figures this letter quotes |
| `drift-122.json` | the measurement four of the suite's assertions check the instrument against |
| `extract_dashboard.py` | reads the per-video series out of those bytes |
| `ledger.py` | the request layer the instrument imports, unchanged and not re-implemented |
| `presence_check.py` | the instrument, version 0.3.3 |
| `receiver-dashboard-2026-08-20.html` | your dashboard, saved this morning; the bytes the finding above is computed from |
| `receiver-list.txt` | the eleven identifiers, transcribed from your dashboard |
| `receiver-series.json` | what the extractor read, series by series |
| `reference-baseline.json` | the reference population the tool prints a comparison against; this letter quotes no figure from it |
| `run_lock.py` | the reservation the daily probe takes; imported by ledger.py |
| `selftest_presence_check.py` | the instrument's own test suite, offline |
| `series-status.json` | the daily series' length and holes, computed from its ledger |
| `your-eleven-today.json` | this morning's live run, as the tool wrote it |
