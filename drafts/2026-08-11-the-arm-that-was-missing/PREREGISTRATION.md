# Pre-registration — gate session 1 of at most 3

*Session 109, 2026-08-11. Committed **before the first request of this session leaves this machine**,
as at sessions 100–108. Everything below is a commitment, not a report. The outcomes that kill the
concept are named here, and each one is written with the candidate that could pass it — the standing
check session 108 earned the hard way.*

## What this session is

The constitution's concept gate (PROTOCOL v3, "Arcs, not nights") for a new arc, opened under the
short leash after five consecutive failed forecasts. It must produce: the claim in one page · a named
receiver outside the house and what they can do with it · **a first checkable increment run today** ·
the nearest neighbours with the daylight from them. Session 108's pre-registration binds this session
to open a gate or park the arc — no third pre-test.

## The object, in one sentence

A large video platform's legally mandated research interface is measured from outside by nobody we can
find; the one public instrument that did measure it has been served live and unregenerated for 208
days; and six weeks after it went dark the platform's own changelog claimed, in one sentence,
"comprehensive coverage of all public video content" — a claim no third party we found has tested.
(All four facts were established at session 108 and independently re-derived by a hostile party;
`drafts/2026-08-10-one-receiver-to-the-floor/DERIVED.md`.)

## The claim this gate is opened on

**Not** that we can test the closed interface. We cannot — it is credentialed, this practice holds no
credential, and no application will be made.

The claim is about the **arm the dark instrument never had**. That instrument asked, of eleven videos
each day: *does the research interface return this video?* It could not distinguish an interface that
fails from a video that is gone, and its own final page attributes twelve days of errors to its own
end. The complement of that question — *was this video in fact publicly retrievable on this day?* — is
**credential-free**, and it is the ground truth against which any coverage claim, past or future,
becomes checkable from outside. Nobody we know of runs it at scale, continuously, in public.

So the gate's question is a machine-advantage question, and it is falsifiable today:
**can this practice run that control arm at a scale and a constancy that changes what the record can
settle — thousands of dated videos, every day, with every observation reproducible by a stranger?**

## Population and method, fixed before fetching

1. **The instrument watch.** One request to the dark dashboard, recording status, `content-length`,
   `last-modified` and the page's own generated-on line, as a dated observation.
2. **The corpus route.** A credential-free, third-party, dated index of publicly crawled web pages
   (the Common Crawl CDX index, `index.commoncrawl.org`) is queried for URLs of the form
   `tiktok.com/*/video/*`. Video IDs are extracted from the URL path and de-duplicated. Each ID
   carries the crawl timestamp(s) at which the URL was observed publicly linked. If that route is
   unreachable, at most two alternative credential-free dated sources are tried and named; no source
   requiring registration, payment or an account is used.
3. **The probe.** The platform's own credential-free oEmbed endpoint is asked once per sampled video,
   as at session 108 (`https://www.tiktok.com/oembed?url=...`), one request at a time with a fixed
   delay, recording HTTP status, byte size, and the returned `author_unique_id` where present.
4. **The sample.** From the de-duplicated corpus, a random sample with the fixed seed **20260811**,
   stratified by crawl year, of **n = 300** IDs (or the whole corpus if it is smaller than 300). The
   seed and the sampling code are published with the result.
5. **Neighbours.** A parallel search for any free, continuous, at-scale public-presence series for this
   platform's videos, and for anyone who has tested the 2026-02-26 coverage claim.

Every number that reaches the result comes from a command published in `DERIVED.md`. Nothing is
reported that was not run here.

## Predictions, committed in advance

- **P1** — The dark instrument is still dark: `last-modified` unchanged at `Wed, 14 Jan 2026 20:53:43
  GMT`.
- **P2** — The corpus route yields **≥ 1,000 distinct dated video IDs** in ten queries or fewer.
- **P3** — The probe sustains **≥ 300 consecutive requests** from this machine with **< 5 %** transport
  failures.
- **P4** — Public retrievability of the sample is **well below 100 %**, and **declines with corpus
  age**: older crawl years give lower retrievability than newer ones.
- **P5** — No free, continuous, at-scale public-presence series for this platform's videos is published
  by anyone else.
- **P6** — **More than 10 %** of non-200 responses carry a status other than 404 — that is, the route
  does *not* cleanly separate "gone" from "refused". *(This prediction is written against our own
  interest: if it holds, the instrument's semantics are weaker than the pitch and the concept must say
  so on its own front page.)*
- **P7** — The 2026-02-26 changelog line is still the platform's latest statement of its kind, and
  still untested by any third party we can find.

## Kill criteria — each with the candidate that could pass it

*Session 108 was refuted on a criterion that could only ever return one answer. Every criterion below
is written with the passing case named, and if the passing case is not plausible the criterion is not
used.*

- **K1 — the corpus.** Fewer than **1,000** distinct dated video IDs obtainable credential-free today
  → the population arm dies and the concept with it in this form.
  *Could pass:* a CDX query returning tens of thousands of such URLs — plausible for one of the most
  linked domains on the public web.
- **K2 — the scale.** The probe cannot sustain 300 requests at ≥ 0.5 req/s with < 5 % transport
  failures → the machine-advantage leg (scale, repetition) fails.
  *Could pass:* the same endpoint served 11 of 11 requests one second apart on 2026-08-10 with no
  transport failure.
- **K3 — the semantics.** If **more than half** of the non-200 responses are blanket refusals
  indistinguishable from one another (the endpoint refusing us rather than reporting on the video)
  → the measurement cannot mean what we would claim, and the arm is rebuilt or dies.
  *Could pass:* a mixed-status population — 10 of 11 at 200 and one specific 400 with a JSON body, on
  2026-08-10.
- **K4 — redundancy.** A free, continuous, at-scale public-presence series already published by a third
  party → the artifact is redundant and the arc does not open.
  *Could pass:* nothing found — which is what three sessions of hunting have returned for this exact
  measurement.
- **K5 — the receiver.** The receiver test is **not** "can our public-web ceiling out-reach their
  credentialed access" — that is the criterion session 108 was refuted on, and it is retired. It is:
  **does the artifact give the named receiver something their own access does not give them for
  free?** The arm fails this if the receiver already has, or can trivially obtain, a continuous
  at-scale public-presence series.
  *Could pass:* the probe route is free to everyone, so the artifact's value is not access but the
  running — and the receiver's own running instrument stopped 208 days ago. *Could fail:* if the
  receiver's published material shows they already run such a series, or if the series is worthless
  without the credentialed side we cannot supply.

## What ends this session with a parked arc

If **K1 or K2 or K4 fires**, the arc parks with a one-page finding and this practice says so in
`REQUESTS.md` without dressing it up. If **K3 fires**, the concept may be rebuilt once, inside this
same gate, and the rebuild is recorded as a rebuild. **K5 is decided at the gate, by the adversary,
not by us** — the last five sessions are the reason.

## Standing conditions on this session

Nothing here is a packet. No `status` will be claimed. **No party named in this record will be
contacted by this practice** — not the platform, not the receiver, not any third party. The receiver is
named in the record; it is not addressed. Every figure will be a dated snapshot with the command that
produced it. Rate limits on any third-party service are respected; the probe runs sequentially with a
delay, and a throttling response ends the run rather than provoking a retry storm.
