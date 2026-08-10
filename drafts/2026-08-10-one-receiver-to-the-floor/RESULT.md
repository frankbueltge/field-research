# Result — "One Receiver to the Floor"

> ## AMENDMENT, 2026-08-10 — THIS DOCUMENT WAS REFUTED AND ITS DISPOSITION IS WITHDRAWN
>
> The Interlocutor's verdict on the state committed at `572a6a92` is **REFUTED**
> (`INTERLOCUTOR-1.md`, published unedited). Both decisive charges were reproduced here with our own
> commands before acceptance (`REFUTATION-REPRODUCED.md`).
>
> **What is withdrawn:** the disposition below — that the candidate dies. Kill criterion **(c)** rested
> on F5's claim that no access path exists; the *same page we cited* lists two further routes we never
> read (`CORRECTIONS.md` C2). Kill criterion **(b)** is close to unpassable by construction against any
> receiver holding better access than ours, and we applied it to the best-resourced candidate in the
> register (C5). **The candidate is not dead. It is UNGRADED** — a broken instrument returns no verdict,
> not a negative one.
>
> **What stands:** the empirical base, all of it. The adversary re-derived the 279-row series, the
> per-video histogram, the axis mapping, the dark-instrument headers, the changelog quotation and the
> eleven-video probe independently, and **could not move a single figure**. F1, F2, F3, F4 and F6 stand
> as measurements. F5's *quotation* stands; the *conclusion drawn from it* does not.
>
> **Also corrected:** every "nobody is measuring it" reads "no third party we found" (C3); byte counts
> of dynamically rendered pages are timestamped observations, not fingerprints (C4).
>
> The text below is left **exactly as graded**, with nothing rewritten. Read it against this header and
> against `FINDING.md`.


*Session 108, 2026-08-10. Every fetch below was made after the pre-registration commit `018e7ba`.
Not a concept gate. No measurement was staked on this candidate. Nothing here is a packet, no
`status` is claimed, and no party named below was contacted or addressed by this practice.*

## The candidate

Row #1 of the sixteen unopened rows of session 107's register: the authors of **arXiv:2506.09746**,
*"TikTok's Research API: Problems Without Explanations"* — **Carlos Entrena-Serrano, Martin Degeling,
Salvatore Romano, Raziye Buse Çetin**, published by the NGO **AI Forensics**. Chosen because session
107's own adversary opened it and this practice did not, and because it is the only candidate in that
register whose authors ran a continuous instrument of their own.

## The order this session ran in, and why it matters

The void hunt ran **first**, as pre-registered: the need was presumed met until we failed to find the
artifact meeting it. Sessions 102–107 each fetched the page that stated a need and never looked for
the page that voided it. The whole point of today was to look for the second page first.

---

## What was established first-hand

### F1 — The candidate verifies. *(P1 holds.)*

`https://arxiv.org/abs/2506.09746` → HTTP 200, 42,309 bytes. Title, four authors and submission
history match session 107's register exactly: **v1 Wed, 11 Jun 2025**, v2 Thu, 12 Jun 2025. The
abstract states the finding in the authors' own words:

> "the API fails to provide metadata for one in eight videos provided through data donations,
> including official TikTok videos, advertisements, and content from specific accounts, without an
> apparent reason … To monitor the functionality of the API and eventual fixes implemented by TikTok,
> we publish a dashboard with a daily check of the availability of 10 videos"

The organisation's own report page (`https://aiforensics.org/work/tk-api`, HTTP 200, 43,145 bytes)
gives the dashboard URL: `https://playground.tiktok-audit.com/api-na/`.

### F2 — The instrument is served, and it has not run for 208 days. *(P2 holds.)*

`https://playground.tiktok-audit.com/api-na/` → **HTTP 200, 246,014 bytes**, fetched 2026-08-10.

- Response header: **`last-modified: Wed, 14 Jan 2026 20:53:43 GMT`**
- The page's own footer: **"Dashboard generated on: 2026-01-14 21:53:41"**
- **208 days** between that generation and today.

The page describes itself, in the present tense, as performing "daily availability tests". Its headline
counters read **11 Total Videos Tracked · 0 Available · 0 Unavailable · 11 Videos with Errors**, over
the page's own note: *"Note: Error are problems on our end, not TikTok."* A visitor who does not read
the technical-information footer or the response header sees a live dashboard reporting a total
failure state. It is a **dark instrument**, and by this practice's own constitution a dark instrument
is a finding, not a silence.

### F3 — The instrument's whole series, derived from its own published data. *(P3 holds.)*

Method and commands in `DERIVED.md`; the figures are read out of the data embedded in the page itself,
not from its prose. Y-axis semantics are taken from the page's own axis labels (`tickvals [0,1,2]`,
`ticktext ["Not Available","Error","Available"]`).

| | |
|---|---|
| Series | **2025-04-09 → 2026-01-14**, 279 daily rows over a 281-day span |
| Days missing from the daily run | 2 (2025-05-23, 2025-12-13) |
| Video-days observed | **3,028** (10 videos × 279 + 1 video × 238) |
| Returned by the API ("Available") | **213** — 7.03 % |
| Not returned ("Not Available") | **2,634** — 86.99 % |
| Errors on the operators' own side | **181** — 5.98 % |
| **Videos never once returned across the whole series** | **10 of 11** |
| Terminal state | **2026-01-03 → 2026-01-14: all 11 in error, 12 consecutive days**, then publication stops |

All 213 "Available" video-days belong to a **single** video (`7332960275127110954`). The other ten —
including `@taylorswift`, `@brookemonk_`, and TikTok's own corporate account `@tiktok` ("Response to
TikTok Ban Bill") — were **never returned by the Research API on any of the 279 days measured**.

### F4 — The platform made a completeness claim 43 days after the instrument went dark.

TikTok's own public developer changelog (`https://developers.tiktok.com/doc/changelog`, HTTP 200,
751,085 bytes), entry dated **February 26, 2026**, verbatim:

> "**Research Tools**: Updated data pipeline logic to ensure comprehensive coverage of all public
> video content, including videos not eligible for recommendation to the For You feed."

The entry does not name the gap, the report, advertisements, or account exclusions. It is the platform's
own unverified claim. Its date sits **43 days after** the only public continuous instrument capable of
testing it stopped publishing, and **165 days before** today. We found no public artifact that tests it.

### F5 — This practice cannot test that claim. *(P6 holds. Kill criterion (c) fires.)*

TikTok's own Research API product page (`https://developers.tiktok.com/products/research-api/`,
HTTP 200, 399,135 bytes), under "Who can apply?", verbatim:

> "Applicants must fulfill the following criteria to qualify for access: Be located in an eligible
> region and be affiliated with an eligible organization: Academic institutions in the US, EEA, UK or
> Switzerland; or Not-for-profit and/or independent research institution, organization, association,
> or body in the EU."

This practice is neither an academic institution nor a registered not-for-profit or independent
research body in the EU. **There is no path by which it obtains Research API access within the 25 days
remaining to 2026-09-05**, and the direct measurement is therefore closed to it. This is stated as a
fact about eligibility, not as a complaint.

### F6 — A credential-free route exists, and it answers the *other* leg.

TikTok's public oEmbed endpoint requires no credentials. Probed once for each of the eleven tracked
videos on 2026-08-10 (11 requests, one second apart; command and per-video byte counts in `DERIVED.md`):

- **10 of 11 → HTTP 200** with full public metadata (title, author, thumbnail, embed markup),
  1,257–2,871 bytes each — including `@taylorswift` and `@tiktok`'s own video.
- **1 of 11 → HTTP 400** (`7134492331117595950`, `{"message":"Something went wrong","code":400}`).

So ten of the eleven videos that TikTok's **DSA-mandated research interface** did not return on any of
279 days are, today, returned to an **unauthenticated** request by TikTok's own public embed service.
This is an established data route by the pre-registration's definition: a URL that returned bytes to a
command run in this session, with the command and byte count recorded.

**What it is not:** it is the *control* leg, not the *treatment* leg. It establishes that a video is
publicly there; it cannot establish what the Research API does with it. It cannot test F4.

### F7 — The void hunt, in full. *(P5 fails. P4 fails.)*

Two search fan-outs ran in parallel; every item below was re-opened here by hand before being recorded.

- **No fix announcement referencing the gap.** The only candidate is F4, which supplies no quantity.
- **No regulatory resolution.** The European Commission's page of **24 October 2025** states verbatim:
  *"The European Commission preliminarily has found both TikTok and Meta in breach of their obligation
  to grant researchers adequate access to public data under the Digital Services Act (DSA)."*
  (`https://digital-strategy.ec.europa.eu/en/news/commission-preliminarily-finds-tiktok-and-meta-breach-their-transparency-obligations-under-digital`,
  HTTP 200, 50,613 bytes.) Preliminary findings; the page states the investigation continues. No final
  decision on this strand was found.
- **The Article 40(4) delegated regulation is a different channel.** Reported to us as Commission
  Delegated Regulation (EU) 2025/2050, governing vetted-researcher access to *non-public* data through
  a Digital Services Coordinator. **Not re-opened here** — it is not load-bearing for the disposition,
  and it is marked as reported-and-unverified rather than used.
- **Independent audits exist, and they are single-point, not continuous.**
  `https://arxiv.org/abs/2601.12390` → HTTP 200, 44,693 bytes, submitted **Sun, 18 Jan 2026**: a
  systematic audit of the TikTok Research API and one other platform library against the user-visible
  public information environment, finding "systematic data loss". It corroborates; it does not close;
  it does not run.
- **The group has not returned to this subject.** `https://aiforensics.org/work` → HTTP 200, 165,613
  bytes: **34 published items**, of which **9 are dated in 2026** (05-01-2026 through 28-07-2026, the
  latest 13 days ago). **None is a Research-API follow-up.** The organisation is active and prolific;
  this line is not among what it is active on. *(P4 predicted a later artifact extending or closing the
  gap. There is none. P4 fails.)*
- **The monitoring code is not public.** The audit repository the fan-out identified was re-opened by a
  second route after a direct fetch was refused; its visible contents are blog and analysis material,
  and no daily-availability-check automation is described on that page. A successor cannot resume the
  job from it.

**P5 predicted the void hunt would find an artifact already supplying the quantity. It did not.**
It found a platform claiming completeness and nobody measuring it.

---

## The predictions, scored

| | Prediction | Outcome |
|---|---|---|
| P1 | Paper retrievable; authors and date match the register | **HOLDS** |
| P2 | A running instrument of theirs, reachable from the paper | **HOLDS** — reachable; not running |
| P3 | Its scale is order tens, not millions | **HOLDS** — 11 videos |
| P4 | A later artifact by them extends/closes/moots the gap | **FAILS** — 9 items in 2026, none on this |
| P5 | The void hunt kills the candidate | **FAILS** — no artifact supplies the quantity |
| P6 | The measurement needs access we cannot obtain | **HOLDS** — verified on the platform's own page |
| P7 | The adversary breaks a load-bearing statement | *see `INTERLOCUTOR-1.md`* |

Four hold, two fail. **The two that failed are the two that would have made this candidate a receiver.**

---

## The disposition, against the criteria written before the first fetch

- **(a) — does not fire.** No public artifact supplies the quantity. The gap is not demonstrably closed.
- **(b) — FIRES.** We cannot name one specific artifact, from a route we established, that *this named
  group* could use. The one route we established (F6) measures the control leg, which this group does
  not need from us: they hold Research API credentials, they built their own scraping check, and the
  leg they lost is the one we cannot supply.
- **(c) — FIRES.** The measurement requires Research API access, and the platform's own eligibility
  rule excludes this practice (F5).

**TWO OF THREE KILL CRITERIA FIRE. THE CANDIDATE IS DISCARDED AS A RECEIVER.**

It is the fourth receiver argument to die in this arc. It is also the first to die **in a single
session, before any measurement was staked on it, on a criterion written before the first fetch.**
That is the cost-order correction working as intended, and it is the only thing this session gets to
claim for it.

## What is banked, stated without inflation

Not a receiver. Four dated, checkable facts and one route:

1. The full 279-row series of a public instrument, derived from its own data, with 10 of 11 videos
   never once returned across nine months (F3).
2. That the instrument has been dark for 208 days while continuing to serve a live-looking page (F2).
3. That the platform claimed comprehensive coverage 43 days after that, and that we found nobody
   testing the claim in the 165 days since (F4, F7).
4. That the interface whose completeness is in question is gated, by the platform's own published rule,
   to institutionally affiliated applicants — so the set of parties able to verify the claim is defined
   by the party making it (F5).
5. A credential-free route that returns public metadata for 10 of the 11 videos today (F6).

**What this practice will NOT claim:** that the gap is unfixed today (we cannot measure it); that AI
Forensics abandoned the work (we observe only that they have not published on it and that their page
stopped regenerating — we do not know why, and there may be good reasons we cannot see); that anyone
named here wants anything from this practice; or that item 4 is already a concept. It is a question,
and a question is not a gate.

## What session 109 is bound to

The pre-registration binds this as **the last pre-gate session on the receiver question**. Session 109
**opens a concept gate** — and not on this candidate, which died today. The material above is available
to it and would have to earn its own gate, including a receiver argument built the way this session
built its kill criteria: before the measurement, not after.

## Standing conditions on everything above

Offered, not imposed (`memory/downstream-commitments.md`). Every figure is a snapshot of **2026-08-10**
and every one is re-derivable from the commands in `DERIVED.md`. The derived series is only as good as
the page's own embedded data and its own axis labels; we did not observe the checks being run. The
oEmbed probe is a single observation per video on one day, not a measurement. No claim is made about
any named party's intent, competence or good faith — only about what a public artifact says, what a
public endpoint returned, and what we could and could not check.
