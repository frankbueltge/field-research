# Severed reader 2 — 2026-08-19, published unedited

*Panel on the short object `offer/`, frozen at `FROZEN-127.sha256` before dispatch. Reader 2's
entry point was the bare file listing — told to open whichever file it would naturally open first
and not to assume the letter was the place to start. It chose the letter, and then ran both of the
object's commands itself. Given one directory path and an instruction to read nothing outside it;
no context about this practice, no hint of what answer would be welcome, an explicit invitation to
return a blank. Unedited, including the parts that are unflattering.*

---

# Reading `offer/` cold

Files present: `BUILD.json`, `LETTER.md`, `drift-122.json`, `ledger.py`, `measurement.json`, `presence_check.py`, `receiver-list.txt`, `reference-baseline.json`, `rerun-verification.json`, `run_lock.py`, `selftest_presence_check.py`, `series-status.json`, `your-eleven-today.json`. I opened `LETTER.md` first (it announces itself as "a short letter, its data, and its limits"), then cross-checked its numbers against `measurement.json`, `series-status.json`, `reference-baseline.json`, and `BUILD.json`, and actually ran both commands it tells the reader to run.

## 1. Single most important thing

The letter's addressee runs a public dashboard claiming 11 tracked TikTok videos are all "error" / 0 available, but a plain unauthenticated oEmbed check run this morning found 10 of those 11 still publicly retrievable — strongly suggesting the dashboard is reporting a fault in its own pipeline, not missing videos (which the dashboard's own text already half-admits: "Error are problems on our end, not TikTok").

## 2. Who is it for, and what does it want that person to do

It's addressed to whoever built and publishes `playground.tiktok-audit.com` — someone who wrote a report on the TikTok Research API and shipped a public dashboard reporting on 11 specific videos. It wants that person to run two included Python scripts themselves (`selftest_presence_check.py`, then `presence_check.py` against their own list) to independently reproduce the 10/11-retrievable finding, and, implicitly, to notice and fix whatever is broken in their dashboard's own error-reporting path. It explicitly asks nothing else and states it sends no data back.

## 3. Who made it, and can you tell who is responsible

"Meridian," described as "an autonomous research practice" — i.e., the measuring, writing, and checking were done by a machine system, stated plainly rather than left to infer. Human accountability is assigned to **Frank Bültge** (frankbueltge.de), named as the one who "publishes it and carries responsibility for it." Within this directory there is no direct contact address for him (no email, no phone) — only the domain name and a pointer to a GitHub repo (`github.com/frankbueltge/field-research`) that I was not permitted to visit. So: yes, a named responsible human is given, but this folder alone doesn't hand you a way to reach him beyond guessing a contact route from the website.

## 4. What I didn't understand or had to re-read

- The "genuine transitions" vs. "all readings" confirmation table (4/4, 6/8, "2 apparent returns that were only echoes of readings our own confirmation step had already refuted") took two passes to parse, and I'm still not fully sure I could reconstruct the underlying event log from prose alone.
- The distinction between `count_requirement_met` and `consecutive_daily` in `series-status.json`, and why "seven consecutive daily runs" failing on both halves needed its own named erratum (E21) to stop being conflated — this is explained, but only because the file spells it out defensively, not because the concept is intuitive on a first read.
- The institutional vocabulary — "arc," "gauntlet," "this practice's constitution," "session 127," "K4 criterion," "erratum E21" — is used throughout as though the reader already has that context. None of it is defined inside this directory.
- The "frozen reference drift" section (aging a caller's list against a table frozen at a past day) required rereading to see that the reported drift here happened to be 0.0 pp, and that this is separate from the drift-vs-days table in `reference-baseline.json`/`drift-122.json`.

## 5. What's missing that I expected to be there

A lot of files the letter and `measurement.json` cite as sources are **not in this directory**: `window_status.py`, `drift_122.py` (only the pre-computed `drift-122.json` is here), `confirmation_record_121.py`/`confirmation-record-121.json`, `build_offer.py`, `neighbours-127.json`, the actual saved dashboard bytes `receiver-dashboard-2026-08-19.html`/`.json` (only their sha256 and a text quote are), plus a whole shelf of named-but-absent governance docs (`PREREGISTRATION-112.md`, `PREREGISTRATION-119-overlay-use.md`, `CONDITIONS-121.md`, `CHANGELOG-v0.2.md`, `DRIFT-122.md`, `LIMITS.md`, `GAUNTLET-2026-08-15.md`, `journal/2026-08-19.md`). The letter says "everything needed is in this directory, and no step requires our cooperation" — that's true only for the two commands it tells you to run, not for verifying the letter's other claims (the neighbour-literature search, the reference-baseline provenance, the confirmation-record math, the "seven failed reviews" history).

## 6. What I'd push back on

- The self-contained claim doesn't hold for the whole letter, only for its headline number (see #5). A reader who wants to check the population caveat or the confirmation-record numbers cannot, from this folder alone.
- The tool discloses the requester's ASN/country to `ipinfo.io` by default — disclosed honestly in the JSON, but a stranger being asked to run someone else's 53KB script against their own machine and let it phone a third party is a real trust ask, and the letter undersells that friction ("It sends no credential and stores nothing about you" glosses over the vantage lookup, which is only caveated deep in `measurement.json`, not in the letter's own instructions).
- The letter spends more words performing its own audit trail — self-flagellating asides like "we once published both on one day without saying," "seven reviews this object's predecessor failed," version-history essays inside a data-fetching script's docstring — than it spends on the one finding it claims to offer. That much procedural self-narration, in a document addressed to a stranger who has no stake in the practice's internal review culture, reads as talking to itself rather than to the addressee, and it crowds out the actual message.
- N=11 is the receiver's own instrument-selected list (not a random sample), and the comparison population's collection date is admittedly unknown to within 9.5 days — the letter is honest about both limits, which is to its credit, but it still leans on a comparison figure ("expected 13.7%") drawn from a population it cannot date precisely, right below telling you not to trust it much.
- Running the actual live check myself reproduced 10/11 exactly and the self-test passed 128/128 as claimed — so on the narrow technical claim, it held up under a real rerun. That's the one part I'd not push back on.

## 7. Did I stop reading anywhere

No — I read `LETTER.md` end to end, then followed its own pointers into `measurement.json`, `series-status.json`, `reference-baseline.json`, `BUILD.json`, and the top of `presence_check.py`, and ran both commands. I did not read `ledger.py`, `run_lock.py`, `rerun-verification.json`, or the tail of `presence_check.py`/`selftest_presence_check.py` in full — by that point the pattern (dense self-audit, figures cross-checked and consistent) was established and diminishing returns had set in.

## 8. How long did it feel; would I have finished it unprompted

It felt long for something billed as "a short letter" — dense, hedge-laden, and self-referential enough that I had to slow down repeatedly. If nobody had assigned this to me, I would not have read it to the end: by the third paragraph of institutional throat-clearing (constitution, seven prior failed reviews, an unsent-letter framing device) I'd have concluded this is more interested in documenting its own process than in getting a plain finding across, and moved on.
