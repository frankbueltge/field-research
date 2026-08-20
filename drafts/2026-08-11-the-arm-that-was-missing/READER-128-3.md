# Severed reader 3 — full answer, unedited

*Session 128, 2026-08-20. Entry point: the data file `dashboard-findings.json`, read before
anything else. Severing conditions: `READERS-128.md`. Nothing below is edited, reordered or cut —
including its finding 4, which is the panel's most valuable return and which this session
reproduced before accepting (`ERRATA-128.md` E24).*

---

# What I found in `copy-3`

## 1. The single most important thing this directory tells you
A public TikTok-availability dashboard has apparently been frozen since 14 January 2026 — all 11 videos it tracks flipped to an "Error" status on 3 January 2026 and nothing has changed since — while a direct check this morning found most of those same videos are still publicly fetchable, meaning the dashboard's visible tiles are seven months stale.

## 2. What is it about?
It's a self-contained evidence package built around one claim: that a specific public dashboard (at `playground.tiktok-audit.com`, connected to a published TikTok Research API audit report) stopped updating months ago but still shows "Error"/"Not Available" tiles as if current. The directory contains the saved dashboard HTML, scripts that extract and analyze its per-video data, a fresh independent probe of the same 11 videos run this morning, and a letter that lays out the comparison, its limits, and how to reproduce every step.

## 3. Who is it for, and who is it from?
It's addressed to whoever operates that dashboard — never named, referred to only as "you"/"your dashboard" — and the letter states explicitly that this person has not been contacted and the letter has not been sent. It's attributed to "Meridian," described as "an autonomous research practice" where "a machine did the measuring, the writing and the checking," with one named human, Frank Bültge (linked to `frankbueltge.de` and a GitHub repo `frankbueltge/field-research`), stated as the one who "publishes it and carries responsibility for it" and who decides whether it's ever sent.

## 4. What would you not trust, or want to check yourself?
- Two of the eleven videos show a creation date in the freshly-fetched data (`your-eleven-today.json`) that doesn't match the creation date recorded for the same video ID in the dashboard's own history (`dashboard-findings.json`) — e.g. video `7332960275127110954` is dated "March 27, 2024" in one file and "2024-02-07" in the other; video `7361448925972155679` is "March 25, 2024" versus "2024-04-24." That's a real discrepancy I'd want explained before trusting the per-video matching.
- The document's own "scoring the handed-over breakdown" section admits one figure it was checking against — a percentage range — did *not* reproduce, only the day counts and video counts did.
- The whole apparatus is self-graded: its "selftest," confirmation passes, and build log are all produced and checked by the same instrument being evaluated, and the letter itself says two of the figures it quotes (re-request counts, and how long its own daily series is) rest on a ledger that is *not* in this directory, only "public in the repository named" elsewhere — so despite the letter's claim that "everything the headline rests on is in this directory," that's not quite complete.
- It's one read from one network at one moment ("AS396982," this morning) being used to characterize a gap of over 200 days; the letter itself flags this as a real limitation rather than something I'm inferring.

## 5. Where, if anywhere, did you stop reading or want to stop?
I stopped short of reading the five Python scripts (`extract_dashboard.py`, `dashboard_findings.py`, `presence_check.py`, `ledger.py`, `run_lock.py`, `selftest_presence_check.py`) line by line, and I only sampled `receiver-series.json` (210KB of raw extracted series) and `BUILD.json` (23KB build log) rather than reading them in full — I read their structure and stated outputs instead of auditing the code logic myself. That's the honest boundary of what I verified versus what I took on the file's own word.

## 6. Anything you noticed that nobody asked about
The package is written in a strikingly rule-bound, audit-culture style — it numbers its own past failures ("erratum E21"), distinguishes a run that was "started and abandoned" from one that counts, insists on a distinction between "the count" and "the consecutiveness" of its daily measurements so a future version can't blur them together again, and warns readers that its own IP-lookup step for the "vantage" data discloses their machine's IP to a third party unless disabled. It reads less like a one-off message and more like one dated entry in an ongoing, versioned research process with its own internal review and correction history — most of which lives outside this directory and isn't something I can check from here.
