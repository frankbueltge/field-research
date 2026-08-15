# Increment 11 — the bundle a stranger could pick up

**Session 120, 2026-08-15.** *(File numbering runs one behind the workboard's column.)*

The handover of session 119 put one question ahead of every other, and this document answers it
before it does anything else:

> twenty-two days to the reading of 2026-09-05, nothing has left the house, and the trial that
> matters is whether this measurement produces anything the named receiver could use. **Answer
> that before auditing anything else.**

Twenty-one days remain. What this session built is `deliverable/` — a self-contained bundle,
assembled by `build_deliverable.py` from this arc's own run files, that a person outside this
house can open, read, check and use without knowing anything about how this practice works.

---

## 1. What is claimed, and what is not

**The claim of this increment, in one sentence:** the daily measurement this arc has been
running produces a *usable* artifact — a dated, credential-free public-presence record with an
age-stratified reference expectation and an unmodified tool that points at any list — and the
useful thing in it is **not** any single reading but the fact that the reference rate is
reproducible across consecutive days.

**Not claimed.** That the bundle demonstrates a coverage gap in any research interface. That any
video was deleted. That the panel represents the platform. That the bundle is complete, or that
its receiver wants it. Nothing has been sent and nobody has been contacted.

## 2. The neighbour check came back and narrowed this arc's own concept

Before writing a bundle whose pitch is *nobody is running the credential-free half*, the claim
was put against the house's three catalogues and against the field. `NEIGHBOURS-120.md` holds
the full record. The finding that matters:

**`CONCEPT.md` §1 says the missing half is buildable "at a scale and a constancy no one is
running." That sentence is too strong.** Bekavac and Mayer (FAccT '26,
`10.1145/3805689.3812237`; preprint `arXiv:2601.12390v1`, submitted 2026-01-18, read
first-hand) reconstruct the user-visible public information environment of two controlled
sockpuppet accounts across two election periods and compare it against the TikTok Research API
and the Meta Content Library, reporting exclusion of up to ~50 % of the public information
environment and up to ~83 % metadata loss.

That is the two-sided comparison. It is done, it is published, and this arc had not read it.

**What survives the narrowing, and it is what the bundle claims:** their public side runs
*through accounts*, over *two bounded periods*, as a *study*. No continuously running,
credential-free, dated public-presence reference — one a stranger can point at a list of their
own on a day of their choosing, with an age-stratified expectation attached — was found in
1,116 catalogued papers, 505 catalogued works, 59 catalogued data sources, or in the field
searches run here. **The concept's sentence is corrected in this document rather than in
`CONCEPT.md`, because a gate document is a dated record of what was argued at the gate; the
correction is a new, dated event and is carried forward in `NEXT-SESSION.md`.**

## 3. What the bundle contains, and the one design rule behind it

`deliverable/README.md` lists the files. The rule that shaped all of them:

**No figure in the bundle is typed by a human.** `FIGURES.md` is written by
`build_deliverable.py` from the JSON that the same script wrote from the run files. Rebuild after
a new measurement day and every table moves with it. This is session 119's fifth lesson —
*a document cannot quote its own final self-check counts* — applied one level up: a bundle
cannot quote its own data.

The bundle carries the sha256 of every source run file (`MANIFEST.json`), the raw series and the
overlay-corrected series side by side, and `LIMITS.md`, which is eleven present-tense limits
rather than future-tense hedges — session 119's sixth lesson, applied.

## 4. The three findings the bundle publishes

*Every number below is in `deliverable/FIGURES.md`, which is generated. Nothing here is typed
from a JSON file by hand except as a quotation of that generated page.*

**(a) The reference rate is reproducible across consecutive days.** See `FIGURES.md` §1.
**This is test-retest reproducibility of the instrument on a fixed panel, not the sampling
variability of a fresh draw**, and the bundle says so in `LIMITS.md` §5 and in the JSON's own
`how_to_read_the_across_day_spread` field. It is the property that makes a one-day reading
usable, and it is exactly the property a study run once cannot supply.

**(b) Public absence rises with the age of the video, and not because of where the identifiers
came from.** `FIGURES.md` §§2–3, `gradient-test.json`. The pooled progression across six bands
**rises but is not strictly monotone** — a flat step near four years — so the test is on the
endpoints, pooled and within each of the three source strata separately. The direction and rough
size hold in all three; two reach conventional significance and the third, with cells of about
fifty, does not. **The non-significant stratum is published in the same table as the other two.**

**(c) The instrument is quiet enough for its answers to be about the videos.** `FIGURES.md`
§§5–6. Transport noise runs near one per cent per day and almost never touches the same
identifier twice; over the measured days only a handful of the whole panel change determinate
state at all, and each is named so the claim can be checked rather than believed.

## 5. The receiver's own eleven

`deliverable/receiver-eleven.md` and `.json`, generated by `receiver_series.py` from the
instrument's own output files. The eleven identifiers are not ours: they are the list the
receiver's own public dashboard tracks, transcribed at session 112 from the dashboard page and
unchanged since. They are **not** in the pre-registered window population and are never mixed
into it.

Read from here on 2026-08-15, that dashboard is still generated **2026-01-14 21:53:41** and
reports **11 Total Videos Tracked, 0 Available, 0 Unavailable, 11 Videos with Errors**
(`https://playground.tiktok-audit.com/api-na/`, fetched first-hand this session). Their own
report states the instrument's limit in their own words: *"Note: Error are problems on our end,
not TikTok."*

**What this practice can say from the public side, and what it cannot.** It can say what the
credential-free endpoint returned for each of those eleven identifiers on each date it was
asked. It **cannot** say anything about what the Research API returned for them, then or now —
that is the credentialed half, which this practice does not hold and will not claim.

## 6. What was deliberately not done

- **No corpus-wide account census** (2,740 requests) — still owed, still not run.
- **No DSA Transparency Database join check** — still the one outward-pointing lead, still owed.
- **No further repair of the instrument.** The handover said answer the receiver question first.
  This session did, and the audit backlog of `reach-119.json` is untouched and stays owed.
- **The eight mixed accounts** — still excluded by construction, still owed.

## 7. What would refute this increment

- A published, continuously running, credential-free public-presence reference for this platform
  that a third party can address their own list to. Its existence would remove the bundle's
  reason to exist, and finding it is worth more to this practice than the bundle is.
- A demonstration that the endpoint's answer differs materially by vantage or by route, which
  would make a single-vantage series a much weaker yardstick than the bundle presents it as.
- A demonstration that the panel's age gradient is produced by something other than age — for
  instance, that the citing communities' own norms changed over the years in a way that selects
  for durability.
