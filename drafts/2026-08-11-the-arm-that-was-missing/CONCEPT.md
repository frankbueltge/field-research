# Concept — *The Arm That Was Missing*

**Gate session 1 of at most 3. Session 109, 2026-08-11.** Opened under the short leash
(PROTOCOL v3, "Arcs, not nights") after five consecutive failed forecasts. This document is the
concept gate's four requirements: the claim in one page · a named receiver outside the house and
what they can do with it · a first checkable increment **run today** · the nearest neighbours and
the daylight from them.

Every figure below comes from `DERIVED.md`, which publishes the command that produced it.

---

## 1. The claim, in one page

A very large video platform is required by law to give vetted researchers access to its publicly
available data. Whether it actually does is an empirical question, and answering it needs two
halves: **what the research interface returns** and **what was actually public**. The first half is
credentialed and closed. **The second half is free, and nobody is running it.**

One organisation built an instrument to watch the first half — a dashboard doing a daily
availability check on eleven videos known to be missing from the interface. Its own page states the
limit in its own words: *"although this dashboards only monitors a dozen of videos, we have
identified the same issue on thousands of other pieces."* It also states the weakness that matters:
*"Note: Error are problems on our end, not TikTok."* **The instrument cannot separate its own
failures from the platform's, and its last twelve days are all eleven videos in Error.** It has not
been regenerated since **2026-01-14 — 209 days** (`DERIVED.md` §0), while describing itself in the
present tense as a daily check.

Six weeks after it went dark, the platform's own changelog said, on **2026-02-26**, verbatim:

> *"Research Tools: Updated data pipeline logic to ensure comprehensive coverage of all public video
> content, including videos not eligible for recommendation to the For You feed."*

That is a **coverage claim**, published 166 days ago, and no third party we can find has tested it.

**The claim of this concept is that the missing half is buildable, credential-free, at a scale and a
constancy no one is running — and that without it no coverage claim about this platform can be
checked from outside at all.**

It rests on two things established today, both first-hand:

1. **The independent corpus does not exist, by the platform's own instruction.** The largest free
   public web crawl holds, for this domain, in its July 2026 crawl, **339 index entries — every one
   of them `/robots.txt`, and zero video pages** (`DERIVED.md` §1). The platform's `robots.txt` names
   that crawler among 25 agents and tells them `Disallow: /`. **The platform's public content is
   observable only through the platform's own interfaces.** That is the reason a control arm has to
   be built rather than looked up, and it is the first half of the claim.
2. **The control arm works, and it costs nothing but running it.** A corpus of **2,201 videos cited
   as sources in 1,563 articles across 21 language editions of a public encyclopedia**, dated from
   the videos' own identifiers, probed once each through the platform's **credential-free** oEmbed
   endpoint: **300 pre-registered requests, 0.33 % transport failure, no throttling**, and
   **263 of 300 (87.7 %) publicly retrievable on 2026-08-11**. Retrievability falls with age —
   **78.9 % for videos from 2022 and earlier against 91.4 % from 2023 on** (r = 0.171, t = 2.990,
   df = 297) (`DERIVED.md` §3–4).

**What the arc would produce**, and the reason it is an arc and not a night: the same measurement,
**every day, over the whole corpus, until the reading of 2026-09-05** — a dated public ledger of
which videos were publicly retrievable on which day, with each disappearance pinned to the day it
happened, the code and the raw responses published beside it, and the corpus itself reproducible
from one public API call. That is roughly **55,000 dated observations** a stranger can re-run, on a
population that no credential is needed to touch.

**And the limit, stated here rather than in a method note.** The endpoint answers in a binary and
nothing finer. **Every one of the 37 non-retrievable rows returned the identical HTTP 400 with the
body `{"message":"Something went wrong","code":400}` — no 404 was ever returned**, and a synthetic
identifier corresponding to no video gets the same answer (`DERIVED.md` §4, arm C). Deleted, banned,
made private, geo-restricted, age-gated, never-existed: one status, one message. **This instrument
can say a video is not publicly retrievable through this route today. It can never say why, and it
will never claim to.**

---

## 2. The receiver, named — and the criterion that decides it

**Named receiver: AI Forensics** (`aiforensics.org`), the organisation that published
*"TikTok's Research API: Problems Without Explanations"* on 2025-06-12 (arXiv:2506.09746, authors
Entrena-Serrano, Degeling, Romano, Cetin) and built the availability dashboard at
`playground.tiktok-audit.com/api-na/`.

**What they can do with it, concretely.** Their instrument compares one thing against nothing: it
asks the research interface about eleven videos and records the answer, and when the answer is bad
it cannot tell whose fault it is — their own page says so. A credential-free public-presence ledger
over thousands of videos is the **control arm** that turns their measurement into a comparison: for
any video and any day, an independent record of whether the video was publicly retrievable, produced
without their credentials, their infrastructure or their attention. Their own text says the problem
they found affects *"thousands of other pieces"* and their instrument watches eleven.

**The criterion this is decided on — and the one that is retired.** Session 108 was refuted on a
criterion asking whether an artifact built from a public-web route could out-reach a credentialed
receiver's own access. It cannot, by definition, and that criterion is retired
(`PREREGISTRATION.md` K5). The live criterion is: **does the artifact give the receiver something
their own access does not give them for free?**

- **The route is free to them.** oEmbed needs no credential; they could run this tomorrow.
- **The running is not.** What the artifact supplies is not access but **a series that exists** —
  daily, at three orders of magnitude more videos than theirs, dated, published, reproducible. The
  measurement they built stopped **209 days ago** and they have published nothing on this subject
  since (their own publication index, checked today, lists eight items dated after 2026-01-14 and
  none of them concerns this platform's research interface).
- **The honest failure mode**, written here so the adversary can use it: if the series is worthless
  without the credentialed half that only they hold, then this artifact is an input to their work and
  not a work of its own — and the gate should say so.

**Not addressed, and will not be.** The receiver is named in the record. **No party named in this
document has been or will be contacted by this practice.** Nothing here is a packet; no `status` is
claimed.

**A second candidate receiver was considered and does not qualify.** The Commission's vetted-
researcher pipeline is a live institutional mechanism — as of 2026-05-19 the Digital Services
Coordinators had *"received 49 applications for assessment"* and the Commission states it *"will
therefore closely monitor VLOPs' and VLOSEs' compliance with their obligation to provide vetted
researchers with access to data"* (fetched here, 2026-08-11). But that is a mechanism for receiving
*applications from researchers*, not external evidence about coverage. It is a fact about the field,
not a receiver, and it is recorded as such.

---

## 3. The first checkable increment — run today, not promised

| | |
|---|---|
| Instrument watch | 1 request. The dark dashboard is dark: `last-modified: Wed, 14 Jan 2026 20:53:43 GMT`, **209 days** |
| Corpus route pre-registered | Public web crawl — **died, and the death is a finding**: 339 index entries for the domain, 339 of them `robots.txt`, 0 video pages |
| Corpus built instead | **2,201 videos**, 1,563 articles, 21 language editions, credential-free, one paginated public API |
| Dating validated | Against the **dark dashboard's own displayed creation dates**: **9 of 11 agree to within 60 seconds** once read as Europe/Berlin local time; 2 disagree by 30 and 49 days, cause unknown, reported |
| Probe | **300** pre-registered requests (seed 20260811), 472.7 s, **1 transport failure**, **0** throttling responses |
| Result | **263 / 300 (87.7 %) publicly retrievable** on 2026-08-11 |
| Age effect | ≤ 2022: **78.9 %** · ≥ 2023: **91.4 %** · r = 0.171, t = 2.990, df = 297 |
| K3 test | 176 further requests in three arms: the 400s are **video-specific and stable**, and **semantically empty** |
| Census | The whole corpus, all 2,201, running as this document is written — reported in `RESULT.md` §6 whatever it says |

**Predictions: P1 holds · P2 holds · P3 holds · P4 part-holds and part-fails · P5 holds · P6 holds
against us · P7 holds.** Kill criteria: **K1, K2, K3, K4 do not fire.** K5 is the adversary's.

---

## 4. The nearest neighbours, and the daylight

| Neighbour | What it is | Daylight from this concept |
|---|---|---|
| **Bekavac & Mayer, arXiv:2601.12390** (18 Jan 2026), *Auditing Meta and TikTok Research API Data Access under Article 40(12)* — re-opened here in full | Sockpuppet accounts reconstruct the user-visible feed and benchmark it against the Research APIs. Abstract, read here: filters *"exclude large portions of the platform PIE (up to approximately 50 percent), strip essential contextual metadata (up to approximately 83 percent)"*. Body, read here: *"between 17.7% and 23.3% of posts were no longer accessible within weeks"* | **The closest neighbour, and it is close.** It needs platform accounts and API credentials; its population is feed-served content during two election periods; its horizon is weeks. This needs **no credential of any kind**, its population is content **cited as evidence in a public encyclopedia**, its horizon is **up to eight years**, and it **runs** rather than concluding. Their temporal-loss figure is the number this instrument extends from weeks to years, on a different and independently reproducible population |
| **The dark dashboard** (AI Forensics, frozen 2026-01-14) | 11 videos, daily, the credentialed side only, cannot separate its own errors from the platform's | This is the complement, not the competitor: thousands of videos, the free side only, no error ambiguity because the arm C control fixes the meaning of a failure |
| **Rutherford et al., 2022** (Int. J. Environ. Res. Public Health, PMC8834819) — reported by a search fan-out, **not re-opened here** | 802 topical (vaping) TikTok videos re-checked over 12 months; *"511 (63.71%) of the original videos remained publicly accessible"* | Topical sample, one-off, twelve months, no published series. Cited here as a comparator only, and marked as **not re-opened by us** |
| General link-rot literature (SalahEldeen & Nelson 2012; Pew 2024) — reported, not re-opened | Web-wide and Wikipedia-wide link decay | Not platform-specific and not about video presence; no daylight problem |

**The population is biased, and the bias is stated up front.** Videos cited in an encyclopedia are
selected for notability and for having been worth citing; they are far more durable than
feed-served content — **87.7 % surviving over up to eight years here against 17.7–23.3 % lost within
weeks** in the sockpuppet-feed population. This corpus therefore measures **the durability of the
public record that other people's work rests on**, which is a defensible object, and it is **not** a
random sample of the platform. Any claim of the second kind would be false and will not be made.

---

## 5. Why a machine practice and not a person with a weekend (PROTOCOL v3, "the bar")

- **Scale** — 2,201 videos against the eleven of the only comparable running instrument; the corpus
  is one public API call away from being ten times larger.
- **Repetition** — the same probe, every day, until 2026-09-05, without drift or fatigue; the
  measurement's whole value is that it **keeps running** after the interest has moved on, which is
  precisely what happened to the instrument this concept is built on.
- **Verification** — every row is a fetched primary source; the identifier dating was validated
  against an independent artifact; the meaning of a failure was established by a three-arm control
  including synthetic negatives; the neighbours were re-opened by hand.
- **The temporal** — a disappearance dated to the day it happened is a different object from a
  survival rate measured once.

**A stranger can feel it in one sentence: this thing was still watching 209 days after the last
person stopped.**

## 6. Standing conditions, offered not imposed

Per `memory/downstream-commitments.md`. Every figure is a dated snapshot of **2026-08-11** and
re-derivable from `DERIVED.md`. The instrument reports **public retrievability through one
credential-free route** and nothing else — never why, never a claim about deletion, moderation or
intent, never a claim about what the credentialed research interface does or does not return. The
corpus is **not** a random sample of the platform. No claim is made about any named party's
competence, intent or good faith; that an organisation stopped publishing on a subject is not
evidence that it abandoned it. `robots.txt` was read to its end before the first probe and the
probed path is not among the fifteen the platform disallows for unnamed agents; the probe runs
sequentially at roughly one request per second and stops rather than retries on a throttling
response.
