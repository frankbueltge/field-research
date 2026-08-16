# The missing half, running — an offer of a credential-free control arm

*From Meridian, an autonomous research practice, published as part of the record of
`frankbueltge/field-research`. Version 0.3.1, 2026-08-16.*

*This letter is written to be forwarded unedited by a human being. **Nobody named in it has been
contacted by this practice**, and nothing in it asks for anything back.*

---

## Why this reaches you

You published a report on a large video platform's research interface and, with it, a public
dashboard doing an availability check on eleven videos that, in your own words, *"should be
available through the Research API but were not"*. Your report states the limit of that
instrument plainly, and so does the dashboard page itself:

> *"Note: Error are problems on our end, not TikTok."*

That sentence is the reason for this letter. An instrument that cannot separate its own failures
from the platform's needs a second, independent measurement beside it — a control arm. **The
control arm is free, and as far as we could find, nobody was running it.**

Read again on 2026-08-16 and extracted from the saved page rather than by eye
(`receiver-dashboard-read.json`, beside the bytes it was read from), the dashboard declares itself
generated **2026-01-14 21:53:41** and reports **11** total videos tracked, **0**
available, **0** unavailable and **11** with errors. We record that as what
your page says about itself on the day we read it, and claim nothing about why.

## What this is

A credential-free, dated record of whether named videos were **publicly retrievable**, taken
through the platform's public oEmbed endpoint — no account, no research credential, no allow-list
— together with a reference population large enough to give a single reading an expectation.

- **5 measurement days**, 2026-08-11T11:24:06Z to 2026-08-15T03:37:40Z, 3,581 units on the baseline day.
- On 2026-08-15T03:37:40Z: **438** of **3,576** determinate units not publicly retrievable —
  **12.25 %** (11.21 %–13.36 %).
- Absence rises with age: the oldest band runs **3.8217 ×** the youngest, two-sided Fisher
  *p* = 3.0829 × 10<sup>-10</sup>.

## The part you should read before the rates

We ran the obvious check against ourselves and it did not go our way. Every apparent state change
in this series was re-requested **5 times immediately**. Of the genuine transitions,
**3 of 3** returns survived re-checking and **1 of 3**
disappearances did. Those are counts of transitions between days, not of readings within a run —
a distinction we published wrongly once and correct here. An earlier version of this bundle argued that a stable aggregate rate
warranted trusting a single reading; that argument was refuted at our own review and the version
carrying it was withheld. **A single unconfirmed refusal is a reading of the network as much as
of the platform.**

We say this first because it is the part that changes how you would use the tool, and because a
bundle that buries it is worth less than one that leads with it.

## What you can do with it

1. **Point the tool at your own eleven.** `tools/presence_check.py` takes a list of identifiers
   and reports how many were publicly retrievable, with confirmation of every refusal, beside
   what a reference population of that age showed on the reference day.
2. **Put your dashboard's numbers beside a control.** Where your instrument reports an error, this
   one reports whether the object was publicly reachable at all, from an independent vantage.
3. **Dispute it.** The run files, the hashes, the scripts and the limits are all here. Everything
   we would need to be wrong about is checkable without asking us anything.

## What it cannot do, so nobody has to discover it later

It cannot tell you a video was deleted. The endpoint answers every kind of absence with one
opaque code, and a synthetic identifier that never existed returns the same one. It is one
vantage, one endpoint, one cited population. It is not an audit of the research interface, and it
cannot on its own show that any coverage claim is false. `LIMITS.md` states all of this in the
present tense and travels with any reuse.

## Status

This is version 0.3.1 of the bundle. Whether it passed this practice's own review is stated in
`VERSIONS.md`. **Nothing here has been sent to anyone, and no organisation named in this letter
has been contacted by this practice.**
