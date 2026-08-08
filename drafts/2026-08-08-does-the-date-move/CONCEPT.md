# CONCEPT — "Does the Date Move?"

The first investigation, opened under Research Protocol v3 at session 100, 2026-08-08.
Concept gate, session 1 of at most 3. Forensic-Architecture form: a question about live
infrastructure outside this house, answered with verifiable material, ending in an artifact a
named receiver outside the house can use. **Deadline: in the post office by 2026-09-05.**

## 1. The claim, in one page

An official page that carries a date — *Updated 27 June 2024* — is making a promise to everyone
who cites it: *this is when what you are reading last changed.* Citations, monitoring tools,
crawl schedulers and readers all act on that promise. Standards bodies write it down as a duty.
The United States' draft federal website standard states the duty in one sentence:
**"Update the date if the content changes substantively. A substantive change is one that impacts
the information in a way that is relevant to your audience."**
(https://standards.digital.gov/standards/content-timeliness-indicator/, fetched 2026-08-08;
status on that page: **Draft**.)

**Nothing checks whether the promise is kept.** The standard specifies no verification mechanism.
No audit of it was found. And the promise is checkable — because the web's public capture history
records what the page actually said on a given day, and archived replay preserves what the origin
server claimed about itself at that moment.

**The claim this investigation will stand or fall on:** on official pages, the date a page states
about itself and the change a reader could actually see **come apart at a rate that matters** —
and that rate is measurable per authority, from public evidence, by anyone who repeats the method.

Three signals carry the promise, and they are not one thing: **H**, the HTTP `Last-Modified`
header a machine gets for free; **S**, the `<lastmod>` a site publishes in its own sitemap; **V**,
the date printed for a human. This house has already measured *which of them exist* on 177 pages
(`drafts/2026-08-06-as-of-today/RECORD.md`) and found H present on all EC and NIST pages measured
and absent on all IE and GOV.UK ones, with V present on 34/40 EC and 7/7 GOV.UK. That line stated
in its own words the wall it could not climb: *"Not a claim about when pages changed — that needs
capture history, unreachable here."* **This session tested that sentence instead of inheriting it,
and it is false for this session's network.** The capture history answers, and it carries the
origin's own headers with it. The investigation is what the wall was hiding.

## 2. The named receiver outside the house, and what they can do with it

**Primary: the United States federal website standards effort published at
`standards.digital.gov`** — the body that authored the timeliness standard quoted above. The fit
is exact and it is documented on their own page: the standard is in **Draft**, is expressly "being
shared with federal agencies and other stakeholders for feedback and iteration", and its
acceptance criteria contain a duty with **no measurement attached**. What they can do with our
artifact: take a compliance measurement of their own draft criterion, per agency domain, computed
from public evidence they do not have to trust us for — because the method and the capture
identifiers are published with it and re-run to the same numbers. A standard that cannot say
whether anyone follows it is a standard with a hole in it; this fills that hole with a number.
NIST is an executive-branch agency inside the standard's stated scope, and is one of the
authorities measured.

**A second class of user, deliberately not named as a receiver** (amendment A4, on the
Interlocutor's condition 4): projects that monitor government pages for change and — like every
such project this session found — work purely from content diffing, having routed around stated
dates without ever testing them. A per-authority reliability profile tells such a monitor where a
stated date may be used as a cheap change signal and where it must not be. A specific project was
proposed as a secondary receiver and **withdrawn**: the direct route to its code host returned
**HTTP 403** to this session, so its current liveness is reported by a search pass and unconfirmed
by us, and an unconfirmed-live project is not a receiver.

**Nothing is addressed to anyone.** Per PROTOCOL v3 and the architect's standing rule, the
receiver is named in the packet; the practice contacts no one.

## 3. The first checkable increment — run today

Pre-registered in `PREREGISTRATION.md` before the instrument existed; executed by `observe.py`;
results and scored predictions in `RESULT.md`. Eleven URLs across four authorities, twelve
monthly archived observations each, each observation carrying the normalised page text, the
printed date V, and the origin's own `Last-Modified` as the archive preserved it. It answers, on
a small population, exactly the question above — and it already returned one design-breaking
finding before a single prediction was scored (§5).

## 4. The nearest neighbours, and the daylight

Established by a search fan-out and then verified at the primary text where it is load-bearing:

- **The one real precedent, and it is close.** Dividino, Kramer & Gottron, *An Investigation of
  HTTP Header Information for Detecting Changes of Linked Open Data Sources*, ESWC 2014 satellite
  events (PDF read directly by this session:
  https://2014.eswc-conferences.org/sites/default/files/eswc2014pd_submission_75.pdf). From its
  own abstract, quoted from the text we extracted: for **only 15 %** of Linked Data resources is
  `Last-Modified` available at all, and where present the date **"aligns in only 8 % with the
  observed changes of the data itself."** *Daylight:* machine-readable data endpoints, not
  human-authored official pages; the H arm only — no sitemap `lastmod`, no printed date; a decade
  old; and the ground truth is their own crawl, not public capture history anyone can re-check.
- **The content-drift lineage** — Jones, Van de Sompel, Shankar, Klein, Tobin & Grover, *Scholarly
  Context Adrift: Three out of Four URI References Lead to Changed Content*, PLOS ONE 2016
  (https://doi.org/10.1371/journal.pone.0167475), and Klein et al., *Scholarly Context Not Found*,
  PLOS ONE 2014 (https://doi.org/10.1371/journal.pone.0115253). *Daylight:* these measure whether
  cited content changed. They use header equality as a *proxy for* sameness; none asks whether the
  stated signal is faithful when treated as fallible.
- **The government-monitoring lineage** — EDGI's own peer-reviewed output (Nost et al., PLOS ONE
  2021, https://doi.org/10.1371/journal.pone.0246450) and the now-defunct Sunlight Web Integrity
  Project and ChangeTracker. *Daylight:* all of them diff content and ignore the stated signals
  entirely. The applied field has **assumed** our answer without measuring it.
- **The house's own nearest work** — *"As of Today"* measured signal *presence*. This measures
  signal *fidelity*. It is the same corpus and the opposite question.

**The daylight, stated plainly and at our own risk:** the printed human-visible date appears to be
the least-studied of the three signals; no study was found testing its fidelity anywhere, and none
was found using public capture digests to audit stated dates on official pages. *This is an
absence of found work, not a proof of absence* — a null search result is the weakest kind of
evidence, and the concept does not lean on it. Even if a study surfaced tomorrow, the receiver's
draft standard would still have no compliance measurement.

**One source was deliberately set aside.** The most quotable statement that publisher-supplied
`lastmod` is widely inaccurate comes from the operator of a major crawler. That operator is also a
commercial vendor of the class of tool this practice may never name, so the source is not cited
and its claim is not used. The argument above does not need it; recording the exclusion is
cheaper than a silent gap.

## 5. Why a machine, and why an arc

The bar (PROTOCOL v3): the machine's advantage must be experienceable in the work. This question
is unanswerable by hand — a single URL-month costs one archive fetch, and a population worth a
per-authority profile is thousands of them, each re-derivable to the same hash by anyone. That is
**scale**, **repetition** and **verification** at once, and the object itself is **temporal**: the
finding *is* a comparison across time that no single visit to a page can produce.

It is an arc, not a night. Increment 1 is 11 URLs; the profile the receiver can use needs the
full corpus and a defensible treatment of the confounder found today. Planned increments: **2** —
extend the population and split trivial from substantive change with a stated rule; **3** — the
per-authority profile and the machine-readable dataset; **4** — the gauntlet and the packet, due
in the post office by **2026-09-05**.

## 6. What would kill this

Named now, so a later session cannot quietly move them: **(a)** if the normalised-text measure
cannot separate an editorial change from a rotating navigation block, the core claim is
unmeasurable as designed and the arc reduces to a methods finding; **(b)** if V turns out to move
with content nearly always, the claim is simply false and the finding is a negative one, published
as such; **(c)** if archive coverage is too sparse on the authorities the receiver cares about,
the profile cannot be built for them and the artifact must say which authorities it cannot speak
for. **(d)** *(added by amendment A2, on the Interlocutor's condition 1)* if the **referent** of V
cannot be established outside EC — this house's own blind-reader test found that every
reader-confirmed self-referential date in its corpus was EC, and killed the labelling scheme that
produced the classes — then this investigation cannot make a per-authority claim about V beyond
EC at all, and the artifact must say so on its face rather than in a caveat.

None of these four is a reason to stop today; each is a reason the gate may fail at session 2 or 3.

**Status after increment 1 (see `RESULT.md`): the gate is NOT passed.** (a) fired — the sampled
content differences were footer rebrands and rotating news feeds. (c) is worse than feared: the
pages that are actually documents have 2–3 captures in a year, not twelve. (d) is now supported by
this session's own evidence — 14 extracted dates lie in the future relative to the capture that
contains them. The core claim is unproven, not disproven; sessions 2 and 3 of the gate must fix the
population before they can test it.
