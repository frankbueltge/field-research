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

> **Restated 2026-08-09 (session 104), after increment 2 measured this paragraph and took half of it
> away.** The two paragraphs above rest on a distinction increment 2 destroyed: byte size, which the
> manifest publishes for every file, predicts the record count inside that file **to within about
> eleven per cent** across twelve years (`RESULT-2.md`, Q3 and Q4, both pre-registered, both NOT
> HELD). The volume-collapse arm is therefore free to anyone with the manifest, and the sentence *"a
> pipeline that checks whether the file exists cannot see any of this"* is withdrawn as an argument
> for this arc (`CORRECTIONS.md` C1). **What increment 2 put in its place is harder and better:**
> for 20 hours 45 minutes on 2022-11-10/11 the manifest lists **249 files with a byte size and an
> MD5 that the file host does not have** — 83 quarter-hours × three file types, 249 of 249 returning
> HTTP 404, 0 probe errors, while the organisation's blog published as usual. **The manifest is a
> claim about what exists, and it is sometimes false.** The claim of this concept is now that
> sentence, and the counter-measurement is a register **verified against the host** rather than
> derived from the index — which is exactly what our own v0.1 register failed to be
> (`CORRECTIONS.md` C2).

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

---

## The named receiver, rebuilt — 2026-08-09 (session 104)

*The section above is void and stays void. This one replaces it. Every party below was checked
first-hand this session, by opening the page or the file cited, not taken from a summary; the date
given is the latest commit date this practice saw on the repository's own commits page. Nothing is
addressed to anyone — a receiver is named in a packet and never contacted (PROTOCOL v3, "Leaving the
house").*

**What the receiver needs is now a single, testable sentence:** a consumer of this instrument cannot
tell "GDELT published nothing here" from "my fetch failed", because the index they fetch from asserts
files that do not exist. The register answers exactly that, and nothing else.

**Primary: the maintainer of `worldmonitor`** (`koala73`, <https://github.com/koala73/worldmonitor>),
a live global-monitoring dashboard — most recent commit on its commits page **2026-08-08**, read
today. It is the strongest candidate precisely because it already does the most a manifest permits:
`scripts/seed-gdelt-bulk-materializer.mjs` fetches `masterfilelist.txt` and then validates each
download against the size the manifest declares —

> `if (zip.length !== descriptor.size) { throw new Error(\`GDELT ${descriptor.kind} download size mismatch: expected ${descriptor.size}, got ${zip.length}\`)`

— which is the correct check and is **blind to the failure this practice measured**: on the 83
cycles of 2022-11-10/11 there is no download to compare, only a 404, and a 404 from a listed file is
indistinguishable in that code path from a network fault or a rate limit. A dated register of
verified absence lets it record "not published" instead of retrying or erroring.

**Second: the maintainer of `SmartETL`** (`ictchenbo`, <https://github.com/ictchenbo/SmartETL>). Its
GDELT loader was committed with the problem written into the commit message itself, read first-hand
today at <https://github.com/ictchenbo/SmartETL/commit/8b4300f>:

> *"NEW datasource GDELT; WIP: gdelt got 404 sometimes, need to fix"*

That is this finding, in a stranger's own words, filed as unfinished work. A register of which
timestamps are genuinely not there is the missing half of that fix.

**Third: the maintainer of `gdeltr2`** (`abresler`, <https://github.com/abresler/gdeltr2>), most
recent commit **2026-04-10**, read today; it fetches the same manifest and is actively being repaired
for silent-failure bugs of exactly this family. It is retained from the voided section with its role
corrected: it reads the manifest, and the manifest is what is wrong.

**And a fourth kind of receiver, named because their result is exposed:** Hsin-Hsiung Huang,
Yuh-Haur Chen and Mahlon Scott, *"Bayesian Deep Count Regression and Anomaly Detection: Evidence from
GDELT Event Panels"* (arXiv:2603.25970, 2026-03-26, <https://arxiv.org/abs/2603.25970>). Read
first-hand: *"We analyze two weekly panels that both begin on the week of 23 February 2015 and extend
through December 2025."* That span contains the 416-hour silence of June–July 2025 and the 374 hours
of October–November 2020. The paper's subject is **detecting anomalous surges and drops in GDELT
counts**, and its own text defers the relevant robustness question to future work: *"The robustness
of anomaly scoring to reporting intensity shifts and to changes in media coverage warrants further
study."* Nothing in it mentions missing data or downtime. **We assert no error in that paper** — we
have not re-run it, and we do not know that any flagged anomaly is an outage. What we can say is that
a dated register is the material a robustness check of this kind would need, and that it does not
currently exist anywhere we could find.

**What none of them can do today, and can do with the register:** distinguish a quarter-hour in which
the world was quiet from one in which the instrument was not looking, and do it for a specific,
dated, verified list of quarter-hours rather than by guessing from a retry log.

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
- ~~If the collapse arm fails to survive being opened at scale — if collapsed byte sizes routinely
  contain normal record counts — the sharpest half of the claim goes. Six files were opened and it
  held; the arc owes a larger hand-check.~~ **Resolved 2026-08-09 and it cut the other way.** The
  arm survived being opened (Q1: 72 of 75 hold under a fifth of their control's record count) and
  **the concept lost it anyway**, because the same increment showed the arm is computable from the
  manifest (Q3, Q4; `CORRECTIONS.md` C1). A kill criterion aimed at the wrong risk.
- **Added 2026-08-09.** The concept dies if the listed-but-absent window of 2022-11-10/11 turns out
  to be an artifact of this practice's own probing rather than of the record — or if the class is so
  rare that one window in eleven and a half years is all there is, in which case the honest artifact
  is a case study, not a register. Present state: 6,148 of 394,878 cycles probed (1.6 %), one window
  found, 0 probe errors. **The next increment either finds the rate or reports that it could not.**
- If no receiver will take a register that documents an instrument's failures, the artifact is
  ornamental. This is the open risk, and it is stated, not answered.

## The arc this concept argues for

Not a one-night table. **A continuous instrument**: the census re-runs against the live manifests,
the register gains each new window as it happens, and the accumulating series becomes the record the
instrument does not keep of itself. The proposed increments, in order: ~~(2) open collapsed cycles at
scale and convert the byte-size screen into a measured record-count series;~~ **(2) done
2026-08-09 — `RESULT-2.md`, and it rewrote the object**; (3) run the census as a
scheduled instrument with a published, versioned register and a diff between runs; (4) prepare the
packet for the named receiver.

**Revised after increment 2, 2026-08-09.** The arc's centre of gravity moves from *reading the
manifest* to *verifying the manifest against the host*, because the manifest is now a measured
object rather than a source: 249 of its entries name files that are not there, and one of them
describes a file it does not have. The increments that follow:

- **(3) The verification sweep.** Probe every cycle the manifest lists — 394,878 English cycles,
  and the Translingual series after it — and publish, per cycle, whether the file the index promises
  exists. At the throughput measured today (~14 probes/second, 15,207 probes in this session with 0
  errors) the English series is roughly eight hours of probing. **This is the increment no person
  runs by hand, and it is the one the artifact rests on.** Its output is register v0.2: every row
  verified, every row dated.
- **(4) The standing instrument.** The sweep re-runs on a schedule against the live manifest, the
  register accumulates, and the diff between runs becomes the record — including the case this
  session could not test: whether a file that is absent today reappears tomorrow, which no snapshot
  can see and only a running instrument can.
- **(5) The packet**, for the receivers named above, under the standing conditions
  (`memory/downstream-commitments.md`).
