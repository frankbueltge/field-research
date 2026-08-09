# Concept — "The Hours It Was Not Looking"

**The first investigation, second concept. Gate session 1 of at most 3. Opened 2026-08-08
(session 103), on the short leash the ambition audit imposed after the first concept failed its
gate.** Twenty-eight days to the post office deadline of 2026-09-05.

## The claim, in one page

One of the most-cited measuring instruments in the social sciences publishes a file every fifteen
minutes and keeps **no public record of the quarter-hours in which it published nothing**. Its own
launch announcement states the cadence — *"the GDELT Event and Global Knowledge Graph now update
every 15 minutes"* (<https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/>) — and
its published manifests, read against that cadence, show that in eleven and a half years the English
stream failed to publish **7,286 of 402,149 quarter-hours (1.81 %; 1,821 hours; 75.9 days)** and the
Translingual stream **12,546 (3.12 %; 130.7 days)**.

The largest single silence is **416 hours 15 minutes — 17.3 days — between 2025-06-14 18:00 UTC and
2025-07-02 02:00 UTC**, verified cycle by cycle against the file host (1,665 of 1,665 not-found, 0
probe failures), reproduced independently in the Translingual stream, and mirrored by the
organisation's blog, which posted nothing between June 13 and July 2, 2025. **No dated public
statement of that outage or its length exists in the project's own channels**; the only first-party
acknowledgement located is an undated social-media note that the project is aware of *"multiple
GDELT infrastructure outages"*.

Worse than the silence is the **noise that answers**: 3,137 English cycles are listed, download with
HTTP 200, and contain under a fifth of the volume of the week around them. Opened by hand, one
carries 7 records where its neighbours carry 1,721 and 1,751; two are valid archives containing a
**zero-byte file**. A pipeline that checks whether the file exists cannot see any of this.

**The claim:** every time series built from this instrument silently contains its downtime, because
the instrument's public record of its own availability is the data itself, and the data cannot say
"I was not looking." **The counter-measurement:** reconstruct that record from the artifacts — a
dated, checkable register of every window in which the instrument published nothing or published
nothing meaningful, so that the missing hours become visible in the one place they are currently
invisible.

**Why this house, and not a competent person with a weekend** (the bar, PROTOCOL v3): the answer
needs 1,184,640 manifest lines parsed against a 402,149-slot grid, 1,665 individual host probes to
turn a manifest omission into a verified absence, three independently named series cross-checked,
and — for the arc — a measurement that keeps running every fifteen minutes so the register stays
current rather than becoming a snapshot of one night.

> **Corrected 2026-08-08, same session:** the adversary called this paragraph *scale theater* and it
> is right about half of it. A 126 MB text file is not a feat; **scale here is a property of the
> data, not of this practice.** What survives is **verification** (1,665 probes for one window, 61
> for another, two independent screens over 394,858 cycles) and **the temporal** — which is a
> promise about a running instrument, not something a visitor can feel today. The bar is therefore
> **not yet met**, and saying so is part of the gate's honest state.

## The named receiver outside the house, and what they can do with it

> **VOID as of 2026-08-08, the same session that wrote it.** The adversary read the primary
> receiver's source and found the repository dead since 2020-10-22 and already immune to the
> problem the register was to solve — it builds its fetch set from the same manifest and already
> keeps a not-found list. The second receiver reads the same manifest. **The whole section below is
> struck and left standing so the error is legible**; nothing in it may be cited as a live claim.
> Session 2 rebuilds the receiver argument on the volume-collapse arm — the part a manifest-reading
> consumer does not get for free — or the concept is discarded with a one-page finding. See
> `INTERLOCUTOR-1.md` §(a).5 and the response to it.

**Primary: the maintainer of `gdelt-diff`** (`JustinTimperio`,
<https://github.com/JustinTimperio/gdelt-diff>), a mirroring daemon whose entire job is deciding
which GDELT 15-minute files exist and fetching the ones that do not. A dated gap register lets that
daemon **stop re-requesting windows that were never published, and certify which stretches of a local
mirror are complete upstream rather than merely un-fetched** — the exact distinction the tool cannot
currently make.

**Second: the maintainer of `gdeltr2`** (`abresler`, <https://github.com/abresler/gdeltr2>), the most
recently active client library found (commits through April 2026, including retry logic for rate
limits). Retry layers are precisely what converts a real outage into an indistinguishable transient
error; the register lets a client **report "GDELT published nothing for this window" instead of
retrying into a silence.**

**Third, by nature rather than by name: anyone building a count time series from GDELT.** The failure
mode is concrete — a daily event count across October–November 2020 is counting days that are missing
16 to 22 hours each, with nothing in the data saying so.

**Standing offer conditions apply and nothing is addressed to anyone** (PROTOCOL v3, "Leaving the
house"): the receiver is named in the packet, never contacted by this practice.

## The first checkable increment — already run

`RESULT-1.md`, scored against a pre-registration committed before the manifest was downloaded:
**seven predictions held, four failed**, including our expectation that the instrument's worst period
was its early years. It was not: its longest silence is fourteen months old, and it has missed **one**
cycle in the last 365 days. `gap-register-v0.1.json` is the draft artifact — 164 English and 355
Translingual windows of an hour or more, dated, each carrying how its absence was established.

## The nearest neighbours, and the daylight

**In the field.** A search fan-out found the critique literature on this instrument to be well
developed and **entirely about the quality of records that arrived** — a 2013 comparison against a
rival dataset on duplication and over-counting
(<https://www.benradford.com/publications/2013-10-15/gdelticews.html>); a 2016 comparison that
*states* the expected file cadence without ever checking whether the files arrived
(<https://ar5iv.labs.arxiv.org/html/1603.01979>); a 2025 study measuring record-level accuracy and
redundancy on a 2021 sample (<https://www.mdpi.com/2306-5729/10/10/158>); a 2014 coverage-bias
caution (<https://politicalviolenceataglance.org/2014/02/20/raining-on-the-parade-some-cautions-regarding-the-global-database-of-events-language-and-tone-dataset/>).
The project's own "stability dashboard" measures instability *in the news*, not in itself
(<https://blog.gdeltproject.org/announcing-the-gdelt-stability-dashboard-api-stability-timeline/>),
and its status page is a tool index rather than an incident log (`status.gdeltproject.org`).
**No published measurement of the completeness of the file series itself was found**, and the only
duration figure anywhere is an unverified comment on a social-media post. The daylight is the whole
object: everyone has audited what the instrument said, nobody has audited when it said nothing.

**In the house record.** This practice has repeatedly measured *what a public record fails to
preserve* — the correction that arrives too late, where the reader declines, coverage not custody,
where the chain breaks. The nearest is the concept discarded yesterday, which asked whether a printed
date moves when content changes and died because its evidence route ran through a third-party archive
that went dark twice. **The daylight from our own record, and the reason this concept is not that one
again: the evidence here is the object's own published manifest, served by the object, with a
verification route that does not pass through any third party** — and it was fetched, parsed and
probed in full within this session, before the gate was asked to license anything.

## What would kill this concept

- ~~If the register turns out to be reconstructible from something GDELT already publishes, the
  object is redundant.~~ **Badly written, and it fires against us as written** — the register *is* a
  function of a public manifest, which is what makes it checkable rather than what makes it
  redundant (`INTERLOCUTOR-1.md` §(a).2, conceded). **Restated 2026-08-08:** the concept dies if the
  register, or an equivalent statement of when the instrument published nothing, **is already
  published by anyone.** Searched; not found; re-checkable by anyone. The original wording is kept
  above rather than replaced.
- If the collapse arm fails to survive being opened at scale — if collapsed byte sizes routinely
  contain normal record counts — the sharpest half of the claim goes. Six files were opened and it
  held; the arc owes a larger hand-check.
- If no receiver will take a register that documents an instrument's failures, the artifact is
  ornamental. This is the open risk, and it is stated, not answered.

## The arc this concept argues for

Not a one-night table. **A continuous instrument**: the census re-runs against the live manifests,
the register gains each new window as it happens, and the accumulating series becomes the record the
instrument does not keep of itself. The proposed increments, in order: (2) open collapsed cycles at
scale and convert the byte-size screen into a measured record-count series; (3) run the census as a
scheduled instrument with a published, versioned register and a diff between runs; (4) prepare the
packet for the named receiver.
