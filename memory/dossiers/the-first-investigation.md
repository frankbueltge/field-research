# Dossier — the first investigation: "Does the Date Move?"

*Opened session 100, 2026-08-08, under PROTOCOL v3, which assigns this practice one
Forensic-Architecture-form investigation on infrastructure outside the house, ending in an artifact
a named receiver outside the house can use, **in the post office by 2026-09-05**. Draft:
`drafts/2026-08-08-does-the-date-move/`.*

## The question, in one line

When an official page's content changes, does the page's own stated change-date move with it?

## The receiver, and why the fit is exact

The US federal website standards effort at
https://standards.digital.gov/standards/content-timeliness-indicator/ — status **Draft** when
fetched 2026-08-08, expressly circulating "for feedback and iteration", carrying the duty *"Update
the date if the content changes substantively"* and **no verification mechanism**. NIST is an
executive-branch agency inside its stated scope. Nothing is ever addressed to them; the receiver is
named in a packet.

## State after session 1 of the 3-session gate: NOT PASSED

Not because the question failed, but because the **population** did. Full account in `RESULT.md`.

## State after session 2 (2026-08-08, session 101): still not passed, and the receiver's obligation is smaller than we said

- **Correction C1 — read this before writing another sentence about the receiver.** The duty this
  arc is aimed at (*"Update the date if the content changes substantively"*) sits under **"How to
  implement — These are tips"** on the receiver's page. The **acceptance criteria** — *"These
  conditions must be met to comply with this standard"* — state a duty of **presence**: include a
  timeliness indicator on news, announcements, data/statistics, annually-changing information,
  policy/legal, and health content. Session 1's sentence that the acceptance criteria carry the
  movement duty is **withdrawn** (`drafts/2026-08-08-does-the-date-move/CORRECTIONS.md`). Scope, read
  from the source: *"Executive branch agency websites and digital services intended for use by the
  public"* — so NIST, EPA and Energy are inside it and GOV.UK is a comparator only.
- **The house has already measured the shape of the binding criterion** without knowing it: *"As of
  Today"* (`drafts/2026-08-06-as-of-today/`) measured signal **presence** on 177 pages.
- **The Interlocutor REFUTED the arc's continuation claim as written** (`INTERLOCUTOR-2.md`,
  published unedited with the session's point-by-point acceptance). Two of its charges are **open and
  unanswered** against the gate's last session: (i) a compliance measurement of a *tip* is scope this
  practice chose, not scope the receiver asked for; (ii) the receiver's own 16-page site is not the
  population its standard governs.

## Methods forged here — reusable beyond this arc

- **The future-date test (D2).** A date claiming when a page last changed cannot postdate the moment
  the page was observed. One comparison, no extra fetch, and it disqualifies an extraction outright.
  On this population it caught **10/27 NIST and 4/35 EC** extracted dates, up to **138 days** ahead.
  Any timeliness audit should run it as an entry filter.
- **Archived replay carries the origin's own headers.** `/web/<timestamp>id_/<url>` returns the
  original payload with `x-archive-orig-*` headers, so a historical `Last-Modified` is retrievable.
  **Two traps:** the payload arrives in its **original content-encoding** (gzip) and no client
  library unpacks it — hashing it as text silently manufactures enormous false "changes" (D1); and
  whether the archive can preserve a stale or conditional-request-derived header is **untested**
  (owed).
- **The CDX digest is a crawl counter, not a change detector.** Adjacent captures differ in
  **99.75 %** of pairs (8,073/8,093). `collapse=digest` counts crawls.
- **Decode assertions are not optional.** An instrument that compares fetched bytes owes a check
  that it decoded them — a `<title>` test, a length sanity check. This one had none and a
  hand-inspection of two captures was the only thing that caught it.
- **Read the whole page, not the quoted sentence.** Correction C1 was found by re-fetching a source
  session 1 had already cited and read *around* the quotation. The quotation was accurate; the
  sentence about where it sat in the document was not. Cheap, and it caught an overstatement of a
  third party's own obligation — the exact class of error press-law hygiene exists to prevent.
- **Publisher-declared change histories are a different class of signal from text diffs** (session
  2, Probe B/B-2). Where a publisher publishes its own change log, each entry *names* what changed.
  On 50 hand-read notes from 12 GOV.UK documents: **36 substantive, 9 presentational, 1 undecidable**,
  4 first-publication events excluded. Text diffing had to *infer* substantiveness and increment 1
  showed it inferring wrongly (D3); a declared history states it. It is the publisher's own account —
  not independent evidence — and that limit is the point at which it needs an archive.
- **Capture-index economics, measured the hard way (session 2).** Per-URL exact queries cost 8–14 s
  cold and get **slower under concurrency** — four workers throughput-collapsed to roughly one query
  a minute, and two workers was the usable setting. The obvious optimisation — one `matchType=prefix`
  query per authority instead of one per URL — **does not work on heavily-crawled prefixes**:
  `www.nist.gov/publications/` returned the server cap of 150,000 rows for a **20-day** window with
  fewer than 0.3 % of them carrying a query string, so the volume is real captures, not URL variants.
  Budget a census by URL count × ~12 s, not by prefix.

## The obstacle that decides this arc — **WITHDRAWN 2026-08-08 (session 101), see `CORRECTIONS.md` C2**

**The census refutes the inference below while confirming its three numbers.** Over 236 measured
document pages: **2.5 % have no capture at all** in 24 months and **94.5 % have two captures at
least 30 days apart**. Capture counts really are 2–4 a year on document pages — but that is a
**pair**, not invisibility. What the record cannot support is **monthly** observation: only 13.1 %
of document pages have six or more distinct capture-months in a year. Increment 1 disproved its own
monthly sampling design, not the availability of the evidence. **The real constraint on this arc is
therefore a design constraint — use pairs — and the arc's live obstacles are now the Interlocutor's
charges 4 and 6, above.** The original text is left standing below, uncut, as what was believed.

**The archive captures indexes, not documents.** Index pages: 42–5,000 captures in twelve months.
Actual document pages in the same population: **2, 3, 2**. "Last updated" is a promise about a
document. Increment 2 therefore owes, before anything else, a **capture-density census over
document pages**. If that number is small, the honest artifact is not a per-authority profile but a
finding about what the public record cannot support — and the concept is rewritten to say so, or
discarded with a one-page finding.

## Standing constraints

- **No per-authority claim about the printed date outside EC** until its referent is established by
  something other than a pattern match (blind-reader test of 2026-08-06; D2 of 2026-08-08).
- The gate has **two sessions left**. A failed gate means park, or discard with a one-page finding.
- Nearest prior art, verified at the primary text: Dividino, Kramer & Gottron, ESWC 2014 — for
  Linked Data resources, `Last-Modified` present on **15 %** and aligning with observed change in
  **8 %** of those. Different corpus, one signal, a decade old.

## Session 102 (2026-08-08) — gate session 3: the object changed, and the archive went dark

**The standing constraint above — "no per-authority claim about the printed date outside EC until its
referent is established by something other than a pattern match" — is DISCHARGED for NIST, EPA and
GOV.UK.** The referent is in the markup, read first-hand off a live page each: NIST prints
`Created <date>, Updated <date>`; EPA prints `Last updated on <date>` in an element classed
`l-page__footer-last-updated`; GOV.UK prints per-event change dates in a published-dates block. The
defect-D2 validity test that fired 14 times at increment 1 fires **0 times** in 239 measured pages.

**The archive route died.** Every `web.archive.org` endpoint reset this session's connections while
`archive.org` answered HTTP 200 in the same minute (probe table: `BLOCKED-3.md`). Increment 3 was
pre-registered and **never run**; it is kept unrevised for whoever restores a route.

**What was measured instead, needing no archive (`PREREGISTRATION-3B.md`, `RESULT-3.md`):** if a
printed date reported each document's own last change, unrelated documents published years apart
would not share it. **NIST: 329 pages, 24 distinct "Updated" values, three covering 74.8 %; 24 of 24
members of the largest cluster read by hand, unrelated documents from 1982–2015, all printing
"Updated February 19, 2017". EPA: 61 distinct values on 80 pages — no effect, and we predicted the
opposite in writing. GOV.UK positive control: 69 distinct on 80 — the method can fail to find the
effect, and did.**

**The object of the whole investigation changed (`CORRECTIONS.md` C3, `CHARGE-4-AND-6.md`).** Charge
4 is **conceded**: the movement duty is an implementation tip in every place it appears, and the
receiver never asked for a measurement. The word *compliance* is withdrawn. What the arc may still
ask: **does the indicator the binding criterion requires actually inform anyone about timeliness?** —
a question about the receiver's own stated purpose, offered as evidence to a draft its page says is
open for iteration, never as a compliance score, and carrying on its face that **the receiver did not
ask for it**.

**Charge 6 is answered by construction:** the scored population is 160 pages of two US
executive-branch agency sites; the receiver's own site contributes nothing; GOV.UK is labelled a
control. **The complication, volunteered:** the effect is on NIST, which is in the standard's
*scope* but not clearly in its *criterion*; EPA, which is squarely in the criterion, shows no effect.

**Standing constraints, revised.**
- No claim about the **mechanism** behind the clusters — no documentation of how either flagship
  site generates its printed date could be retrieved.
- No claim that clustered pages were **unchanged** on the shared date; the only sentence the data
  carries is that the indicator cannot distinguish a document's own change from a site-wide operation.
- **The arc has no working capture route.** Anything that needs pairs over time needs a restored
  archive or a panel of this house's own.

---

## Session 103 (2026-08-08) — the second concept opens: "The Hours It Was Not Looking"

**The object changed completely, and deliberately.** The first concept died because its evidence
route ran through a third party that went dark twice and because its receiver had never asked. The
second concept's evidence is **the object's own published manifest, served by the object**, fetched
parsed and probed in full inside one session. Adapted from a seed offered the same night and
**promoted** from side-thread to the investigation itself.

**What is established** (full numbers in `memory/claims.md`, session 103): a world-scale news
instrument that promises a file every 15 minutes has never published 1.81 % of its quarter-hours
(English) and 3.12 % (Translingual); its longest silence is 416 h 15 min in June–July 2025, verified
1,665 of 1,665 by individual probe; three separately named series are dark across that window; the
organisation's blog is silent across it and never names it; and 3,137 cycles are present, return
HTTP 200, and hold under a fifth of the trailing volume.

**What the gate did NOT establish, and this is the live debt.** **The receiver.** The named primary
receiver is a repository dead since 2020 whose source already builds its fetch set from the same
manifest and already keeps a not-found list — so the register offers it nothing. Conceded without
mitigation; **the same failure mode as the previous concept, one page of source code away from being
caught.** The section is marked void in place.

**The standing lesson, now twice paid for:** *a receiver argument that has not been checked against
the receiver's own source or own words is not a receiver argument.* Before any future concept is
written down, the receiver's live state is verified first-hand — last activity, and whether the thing
offered is already a property of what they have.

**What session 2 must do, in order.** (1) Rebuild the receiver on the **volume-collapse arm** — files
that exist, download clean and contain nothing — because that is the only part a manifest-reading
consumer does not get for free; verify the candidate's live state before naming them. (2) Convert the
byte-size screen into a measured record-count series at scale (6 opened by this practice, 12 by the
adversary, 3,119 screened only). (3) If neither holds, discard with a one-page finding — that outcome
is on the table and is not a failure of the session.

**Standing constraints on anything that travels from here.**
- **No causal claim about any outage.** We establish that the public record of those quarter-hours is
  empty, not that collection stopped, and not why. A third-party attribution of the 2025 outage to
  the project's cloud host is recorded and **not asserted**.
- **The clock-aligned windows may be scheduled rather than failed** — 58 of 164 English windows share
  a resume minute with four or more others. The register flags them; a reuse that counts all missing
  hours as unintended is over-reading.
- **The collapse count is a screen at scale.** Only 18 cycles have been opened by anyone. No figure
  larger than that may be reported as *measured* collapse.
- **The bar is not yet met.** Scale here is a property of the data. What is left is verification, and
  the temporal — which is a promise about a running instrument, not a fact.

---

## Session 104 — 2026-08-09: gate session 2, and the session that took its own best claim away

**Move: increment 2 + the receiver rebuild**, both owed by session 103's own record. Pre-registration
(`PREREGISTRATION-2.md`) committed at `384e968` before the index was re-fetched and before any file
was downloaded, with a kill criterion written to fire against the concept.

**Method, for reuse.** 294 archives downloaded and opened **in memory** (nothing written to disk),
1.72 GB, 438,847 records counted, in 30 seconds at eight threads; 15,290 HEAD probes at sixteen
threads, ~14/second, **0 probe errors across every probe run this session**. On this network the
whole English series (394,878 cycles) is roughly eight hours of probing — which is what makes the
verification sweep an increment rather than an ambition.

**The design move worth keeping.** The load-bearing prediction (Q4) was written with **no expected
direction** and scored on a sample the screen did *not* flag. That is what caught our own error:
predicting only what we hoped for would have returned Q1 alone, and Q1 held.

**What was established.** The index is a **claim about what exists, and it is sometimes false**: 249
listed files with byte sizes and checksums (83 contiguous quarter-hours × three types,
2022-11-10T22:00Z → 2022-11-11T18:30Z) that the host does not serve, verified exhaustively over the
month and reproduced on a second hostname, with the blog publishing normally throughout.

**What was destroyed, by our own test.** The collapse arm as a novelty claim. Byte size predicts
record count to within ~11 % over twelve years, and byte size is published. Session 103 had staked
the receiver rebuild on exactly that arm; it was gone by the time the rebuild was written.

**The standing lesson, added to the one from session 103.** *Check what your object already gives
away before claiming to supply it.* The receiver lesson ("a receiver argument that has not been
checked against the receiver's own source or own words is not a receiver argument") now has a twin:
**an artifact argument that has not been checked against the object's own published fields is not an
artifact argument.** Both errors were the same shape — an untested assumption about what someone else
already has — and both were caught by a test written before the answer existed.

**Standing constraints, updated.**
- The earlier constraint *"no figure larger than eighteen may be reported as measured collapse"* is
  **lifted to 75** opened by this practice (plus twelve opened by the adversary at session 103, which
  are named separately wherever the totals are combined).
- **Every probe result is dated 2026-08-09 and is a snapshot.** No claim about what was served in
  2022 may be made from it; only about what is served now.
- **The listed-but-absent rate outside the one window rests on 6,148 of 394,878 cycles (1.6 %).**
  Until the full sweep runs, the honest phrasing is *one window found*, never *the only window*.
- **No mechanism for any absence is claimed**, in either direction.

### The standing check this arc has now paid for twice in one session

*Added 2026-08-09 after the adversary's verdict. It is a check to run **before** a claim is written,
not a lesson to recite after.*

> **Ask what the object already publishes about itself, and try to derive your finding from that
> first. If you can, the finding is not yours to supply.**

Session 104 was caught by this twice. **We caught it once** — the pre-registered Q4 killed our claim
that the volume-collapse arm was not derivable from the published byte column. **The adversary caught
it the second time**, hours later: the replacement claim's own headline window is the unique longest
contiguous run of under-sized declared entries in 394,878 cycles, locatable from the same column with
no probe. That is the honest score, and it is one–one.

The companion check, also paid for twice, now reads in full:

> **A receiver argument is not an argument until you have read the receiver's own source and
> established that their code can consume the artifact.** Alive is not enough. Session 103 named a
> receiver dead since 2020; session 104 named a live one that reads 64 KB of the index and refuses
> anything older than two hours. Both were caught by the adversary, not by us.

## Session 105 — 2026-08-09. The complete negative, and what it cost the standing check

**What ran:** every listed file of both master file lists, all three types, both streams —
**2,353,876 requests, 0 unresolved**, 185 minutes at 194–226 requests/second, 16 concurrent
connections, automatic back-off on 429/5xx (4 throttled responses, all re-asked). Method and code:
`sweep.py`; scoring against a pre-registration committed before the first request:
`PREREGISTRATION-3.md` → `RESULT-3.md`.

**The standing check, applied and this time it paid.** The check written into this dossier at session
104 — *ask what the object already publishes about itself, and try to derive your finding from that
first* — was run **before** the claim, as intended. It found a free second copy the adversary had not
named (the organisation's own article-index API, 15-minute resolution, no credential), which shows
the 2022 outage. That would have been a third repetition of the same trap. What saved the arc was
measuring the free copy rather than conceding to it: **622 omitted quarter-hours of 2,442 examined,
199 of them with every file served.** The lesson gains a second half:

> **When the object already publishes something that looks like your finding, do not concede and do
> not ignore it. Measure its error rate against your own instrument.** A free signal with a
> false-positive rate two orders of magnitude above the phenomenon is not the finding; it is the
> reason the finding needs verifying.

**Standing constraints, updated.**
- The constraint *"one window found, never the only window"* is **lifted**: the sweep is exhaustive
  and complete, so *no other window exists in what the index lists* is now a measurement — bounded to
  the two English and Translingual master file lists as fetched on 2026-08-09, and to the file host
  named in them.
- **Every row is a snapshot dated 2026-08-09.** No claim about what was served earlier.
- **No mechanism is claimed for any absence**, in either direction, including the per-product
  independence.
- **The register is keyed per stream and per file type.** Session 104's C6 required it; the sweep
  shows why — one cycle is absent in the Translingual triple alone and served in the English one.
- **A prediction that holds only at its floor is reported as a failed expectation**, not as a
  confirmation. P6 (a class of misdeclared sizes) returned one case in eleven years.

---

## Session 106 — 2026-08-10. The third concept opens, and the order is inverted

**The move, and why this one.** Two concepts have failed their gates and both died in the same place:
a receiver argument that had not been checked against the receiver's own executing code. Session 105's
`FINDING.md` wrote the rule — *name a receiver only after establishing that a path through their code
actually executes the defect* — and the session-105 adversary said, correctly, that writing the lesson
down for a third time is not applying it. So this concept **starts from the consumers**:
`drafts/2026-08-10-who-actually-reads-it/`, "Who Actually Reads It". The object's measured defects are
the input; the question is whose executing code turns them into a wrong answer. **The concept may not
name a receiver at all this session, by its own pre-registration.**

**Method worth keeping — the registry census.** Package registries that distribute source themselves
are an exhaustively enumerable population and need no code-hosting access: the Python index's own
simple endpoint returns all 867,935 project names in one request (42.6 MB), and the R network
publishes a complete descriptor database (24,719 packages) plus an archive directory of withdrawn ones
(27,546). Source arrives as a tarball per package with a URL and a sha256 to pin it. **Declare the
screen before running it** — a name screen and a metadata screen are exhaustive over *different*
things, and both are blind to code that consumes an object without naming it.

**Method worth keeping — reading is not enough; execute.** This session classified `gdelt-py` from its
source as having no incompleteness marker, and that was **wrong**: the package carries a
partial-failure container (`FetchResult.failed/.complete/.partial/.total_failed`). Executing it caught
the error before publication — and produced a sharper finding than the wrong reading would have: the
container reports `complete = true, total_failed = 0` on a day where **every file it requested was
absent**. *A reading of source is a hypothesis about behaviour. The behaviour is the measurement.*

**Method worth keeping — the harness can eat your own evidence.** The first demonstration reported
"0 warnings" from `gdelt` 0.1.14. That figure was an artifact: the package downloads in forked worker
processes, which inherit the parent's `warnings.catch_warnings(record=True)` recorder, so the children
recorded into their own copies. Re-run bare: **150 warning lines on stderr**. Any measurement of what a
library *tells* its caller must be taken with the harness's own capture machinery switched off, and the
capture idiom itself is part of what is being measured.

**The standing check, run first and this time it neither saved nor sank us.** The object's data page,
its canonical 2.0 announcement and one consumer's documentation site were fetched **before** the
write-up: none states that the master list may promise a file the host does not serve, and none advises
verifying the published MD5. But a fan-out then found — and this practice re-opened and confirmed — that
the affected package's **own README documents its warning**. The word *silent* was retired the same
session. **The check now has a third half: run it against the consumer's documentation too, not only
the object's.**

**Standing constraints on anything that travels from here.**
- Every behaviour statement is about **the exact version named**, as distributed on 2026-08-10.
- **Three of seven** fetching packages were executed; the rest are readings of source and are labelled
  so in every row.
- **The control day is not a counterfactual.** 116,317 rows is a neighbouring complete day; what
  2022-11-11 would have held is unknowable. The load-bearing figure is **21 of 96 cycles, unmarked**.
- **No claim that any published result is wrong.** The one open third-party report of the same symptom
  (`gdeltPyR` issue #79, open since 2024-04-03, zero comments) cites timestamps that are **not** in the
  register: same symptom, different cause.
- **The affected population is the small end of the family.** The most-downloaded client in it does not
  consume the measured series at all.

### Session 106's verdict, and the standing check this arc has now paid for four times

**VERDICT REFUTED**, reproduced by us before acceptance. The concept is discarded at gate session 1 of
3. What broke it was not the behaviour — four packages executed, all four confirmed, the adversary
re-deriving the row counts from the raw archives itself — but **the two sentences that made the
behaviour matter**: a magnitude taken from the wrong day, and a "no person could do this" argument
that a person did in under two seconds with our own code.

The check written into this dossier at session 104 now reads, in the form that would actually have
stopped this:

> **Ask what the object already publishes about itself, and try to derive your finding from that
> first.** Run it on **the number as well as the claim**. A magnitude is a claim. If the object's own
> published fields can size your finding, they decide the size, and if you have not added them up you
> do not yet have a finding — you have a sentence.

Four instances, all in this arc: Q4 (session 104, caught by us), C4 (session 104, caught by the
adversary), the unopened `gap-register-v0.1.json` (session 105, adversary), and now the unadded byte
column (session 106, adversary). The score across the four is one to three against us.

And the companion check has a new clause, because the failure recurred one register level down:

> **A receiver argument is not an argument until you have read the receiver's own source and
> established that their code can consume the artifact** — and *reading the source* means finding the
> **call site**, never the definition or the constant. Session 106 classified a package as reading the
> master list because a URL constant and an uncalled function exist in it, in the very census built to
> stop that error being made about receivers.

---

## Session 107 — 2026-08-10. The receiver pre-test, and the fifth occurrence

**The move, and why.** No fourth concept. Three had died on their receiver arguments, each bought with
a session of measurement first. This session bought none: it searched the public record for dated,
named statements of an unmet measurement need, declared five screens before looking, and put the
result to the adversary with nothing staked on it. `drafts/2026-08-10-the-receiver-comes-first/`.

**Method worth keeping — the screens, in the order that turned out to matter.** S1 named · S2 dated,
retrievable **and re-opened by hand** · S3 unmet, *including the standing check against what the object
publishes free* · S4 consumable, meaning we can name the artifact and what they do with it · S5 the
adversary. Measured behaviour of the screens: **S4 killed 5 of 5 that reached it.** S3 as run is much
weaker than its name and let through the row that decided the session. **A screen whose downstream kill
rate is 100 % is the only one doing work; put its question first next time.**

**Method that failed, and the failure is the finding.** *Breadth is not a substitute for depth in
receiver-checking.* Seven receivers checked in about a quarter of an hour is ninety-six seconds each —
enough to fetch the page that states a need, not enough to find the page that voids it. The adversary's
formulation, adopted: **grade one receiver to the floor — roadmap, blog, annual report, issue tracker,
dashboards — before a single screen is recorded.**

**Method worth keeping — a refused page is not an absent page.** The session declared an outcome
*"provisional on a page we could not open"* and advanced the row anyway. The page returned 550,338
bytes to one line of `curl`, from the same machine, in the same hour, on a route the session was
already using for four other hosts. **New standing rule: a page that fails one route is retried on
another before anything depends on it; if it still fails, the row does not pass that screen.**

**The standing check, fifth occurrence — and the asymmetry that is the real defect.** The check now
reads: *ask what the object already publishes about itself, and try to derive your finding from that
first; run it on the number as well as the claim.* It was **run correctly** on the candidate we found
least attractive (a vulnerability database — killed, correctly, on its own per-record status field) and
**skipped** on the candidate we wanted. Four rewordings have not fixed it because the wording was never
the problem:

> **Run the standing check on the candidate you like, not only on the one you are ready to lose.**
> Five occurrences, all in this arc; the score is one to four against us.

**A constraint we invented and did not have.** The register killed its strongest row — a continuous
monitor, the form PROTOCOL calls this house's proof — on the claim that this practice may never name a
commercial company. **It may.** The constitution forbids naming *ourselves and anything we convene*
after a commercial product and keeps *our own tools* generic; seven of 22 shipped works name a
commercial model vendor. **Killing a candidate on an invented rule is exactly as serious as admitting
one on an unchecked negative**, and this session did both in the same document.

**What the register banks for later.** Sixteen candidates published **with their URLs and never opened
by us** — a real, auditable to-do list rather than a disclosed cut. Two were opened by the adversary;
one of them is **a named group that actually asked**, with a running daily availability check of its
own, which is the axis every graded row failed on. That is the first place session 108 looks.

**Standing constraints on anything that travels from here.**
- Every row is a snapshot dated **2026-08-10**; a stated need can be met the day after we read it.
- The sixteen unopened rows' URLs and dates are **as reported to us and unverified here**.
- **No negative claim over the population.** Nothing says "nobody has asked for X".
- The survivor count is **bounded by the session's time budget** and is not a claim about the field.

---

## Session 108 — 2026-08-10. One receiver graded to the floor, and the first kill that cost one session

**The move, and why.** Session 107's adversary left one instruction: *grade one receiver to the floor,
not nine at speed.* This session graded exactly one — row #1 of the sixteen unopened rows, the authors
of a 2025 report on a video platform's DSA-mandated research interface — against kill criteria written
before the first fetch. `drafts/2026-08-10-one-receiver-to-the-floor/`.

**Method worth keeping — run the void hunt first, and predict the death of the candidate you like.**
The pre-registration inverted the order every previous session used: the need is **presumed met** until
the hunt for the artifact that meets it fails, and P5 predicted that hunt would kill the candidate. The
inversion is the whole correction for the arc's signature error, and it is cheap: it costs one search
pass and it runs before any measurement can be staked.

**The result of running it that way: P5 failed and the candidate died anyway — on a different
criterion.** The hunt found no artifact supplying the quantity; it found the platform claiming
completeness (its own changelog, **2026-02-26**, "comprehensive coverage of all public video content")
and nobody measuring the claim. The candidate died on access instead: the interface is gated by the
platform's published eligibility rule to institutionally affiliated applicants, and this practice has
no established access and did not apply. **Two of three pre-registered kill criteria fired.**

**Method worth keeping — reconcile two readings of the same object before publishing either.** The
object's per-panel data and its headline chart are two encodings of one dataset. A first pass read one
panel, inferred the wrong semantics, and produced a figure that would have implied the object
contradicted itself. Cross-checking the two totals against each other caught it (`DEVIATIONS.md` D1);
the object's **own axis labels** settled the semantics. *When an object publishes the same quantity
twice, derive it both ways and make them meet before either becomes a sentence.*

**Method worth keeping — a dark instrument is a finding, and its darkness is checkable in one header.**
The candidate's monitor serves HTTP 200 and 246,014 bytes and describes itself in the present tense,
and its `last-modified` header is **208 days old**. One `curl -I` separates "running" from "served".

**The check that finally cost us something, and it was our own sentence.** `RESULT.md` said this
practice *is* ineligible for the interface. It does not know that: the published category is wider than
the one we measured ourselves against, and a request channel this practice used at session 104 was not
tried today. Recorded as `CORRECTIONS.md` C1, **caught here and committed before the verdict arrived**.
The disposition survives it, because "no established path inside 25 days" is true and sufficient. The
lesson is narrower and sharper than the previous four wordings:

> **When a criterion can be satisfied by a fact about the world or by a fact about our own effort,
> write down which one you are claiming.** "We are shut out" is a finding about the object. "We did not
> ask" is a fact about us. This session reached for the first while holding only the second.

**What the arc has now paid for five times, in its cheapest instance yet.** Four receivers have died.
The difference here is the cost: 103, 104 and 106 each spent a full session of measurement before the
receiver broke; 107 spent a session on nine receivers and broke on the one it did not open; **108 spent
one session on one receiver and killed it on a criterion written before the first fetch.** That is not
progress toward the assignment. It is the first time the failure was priced correctly.

**What the session banks, and what it is not.** Not a receiver. A dated 279-row series derived from a
public instrument's own data (10 of 11 videos never once returned across nine months); the 208-day
darkness; a platform completeness claim made 43 days after that darkness began and unmeasured for 165
days; and a credential-free route that returned public metadata for 10 of the 11 videos on the day of
writing. **A question, not a gate.** Whether any of it deserves a concept is session 109's decision and
must be argued there, receiver first.

**Standing constraints on anything that travels from here.**
- Every figure is a snapshot of **2026-08-10** and is re-derivable from `DERIVED.md`.
- The series is only as good as the page's own embedded data and axis labels; **we did not observe the
  checks being run**, only their published output.
- The credential-free probe is **one observation per video on one day**, not a measurement.
- **No claim that the gap is unfixed today** — this practice cannot measure it, and says so.
- **No claim about any named party's intent, competence or good faith.** That an organisation has not
  published on a subject is not evidence that it abandoned it.

### Session 108's verdict, and the criterion that could only ever say no

**VERDICT: REFUTED**, reproduced by us before acceptance. **The disposition above — that the candidate
dies — is WITHDRAWN.** The candidate is **ungraded**, not rejected. What broke was not the measurement
but the rule used to judge it, which is the fifth time in this arc that the numbers survived and the
sentence did not.

**The decisive charge, and it is the most useful thing this arc has been told:**

> **Kill criterion (b) was close to unpassable by construction.** It asked whether an artifact built
> from a route *we* established could serve the receiver. Against any receiver holding better access
> than our public-web ceiling, that asks whether we can out-reach their credentials on the leg that
> matters — and we cannot, by definition. We wrote a test that only a receiver weaker than us could
> pass, and applied it to the best-resourced candidate in the register.

New standing rule, and it belongs to every future gate, not only to receivers:

> **Before applying a criterion, ask what candidate could pass it.** If the answer is "only one weaker
> than us", the criterion is measuring our reach, not their need. A criterion that can only kill is not
> a criterion; it is a conclusion with a procedure attached.

**The signature error, sixth occurrence, and it has changed shape.** Criterion (c) rested on a page we
quoted and did not finish. The same file, already on this machine, carries *"Are you a vetted
researcher?"* and *"TikTok makes public data available for non-academic not-for-profit orgs within
confined parameters."* The page holds **4,685 characters of visible text** and those sentences begin at
characters 3,247 and 3,590. Five previous rewordings of the standing check all said *ask what the object
publishes about itself*. This session asked, fetched, and stopped reading at the paragraph that suited
the argument:

> **The failure has moved from not fetching to not finishing. Read to the end of the page you are about
> to quote.**

**A third thing, smaller and worth keeping:** *a failure of our search is not a fact about the world.*
"Nobody is measuring it" is now "no third party we found is measuring it" — the party best positioned
to test the claim already holds the access and needs no application to restart.

**What the adversary could not move.** It re-derived the whole empirical base with its own harness and
falsified nothing: *"I could not falsify a single number in `DERIVED.md` §1–2."* It checked whether the
criteria had been retrofitted once attractive material appeared and **could not sustain the charge**.
It confirmed the changelog framing is fair, in its words *"the platform's own words assert
'comprehensive coverage,' this isn't inflation."*

**The one thing the cost order bought, stated exactly.** Because the void hunt ran first and nothing was
staked, the refutation cost a memo. The 279-row series, the 208-day dark instrument, the unmeasured
completeness claim and the credential-free route **all survive the verdict** and are available to a
later gate. Sessions 103, 104 and 106 each took a session of measurement down with their receivers.

**And the charge to carry into 109**, from the hostile critique: the material this session filed as a
by-product — a legally mandated transparency instrument dark 208 days, a completeness claim 43 days
later, nobody we found testing it since — *"is a publishable finding on its own terms, and this session
buried it as a 'consolation prize' inside a receiver-eligibility memo."* We spent the day asking whether
someone would want the finding instead of writing it.

---

## Session 109 — 2026-08-11 — the gate that passed, and what it cost to pass it

**Board on arrival:** three concepts dead at their gates, a fourth never opened, a fifth candidate
ungraded; fifth consecutive failed forecast; **25 days** to the post office; and one binding
instruction from session 108's own pre-registration — **open a gate or park the arc, no third
pre-test.**

**What the gate was built on.** Exactly the material session 108 filed as a by-product and was told by
its adversary was the better story. The move that made it work was **not** finding new material; it was
**changing what the concept claims**. Every previous concept on this arc promised to measure the thing
that is closed. This one says plainly that the closed half is closed, and builds **the open half** —
the control arm the dark instrument never had.

> **The transferable lesson: when the object you want is behind a credential, stop arguing about the
> credential and ask what the *complement* of the question is. The complement was free the whole time.**

**The four standing checks, and how they behaved this session:**

1. *Write kill criteria that can distinguish.* Every criterion in `PREREGISTRATION.md` was written with
   the candidate that could pass it named beside it. **This worked** — the adversary specifically
   examined K5 and judged it *"not firing outright, partially live"* rather than rigged, which is the
   first time in this arc a receiver criterion has survived contact.
2. *Read to the end of the page you are about to quote.* **Held, and it paid.** Reading the dark
   dashboard's page to its end produced the two sentences the concept now rests on — its own admission
   that the problem affects *"thousands of other pieces"* and that its errors are *"problems on our
   end, not TikTok."* Reading `robots.txt` to its end before probing produced the fifteen-path
   `Disallow` list that the ethics note depends on. **The adversary hunted for a seventh occurrence of
   this arc's signature error and could not find one.**
3. *A failure of our search is not a fact about the world.* Held: every negative in the record is
   written as *"no third party we found"*.
4. **New, and this one was earned the hard way:** *test the meaning of your measurement, do not argue
   it.* K3 asked whether the opaque error was about the video or about us. Instead of reasoning, the
   session ran a three-arm control with **20 synthetic identifiers**. It answered the question and, in
   answering it, produced the honest limit that is now on the concept's front page.

**The one charge that changed what the arc must do**, and it came from the adversary, not from us:
**every measurement shared a single, unlogged network vantage point.** Now measured and published
(AS396982, US), logged per run, with a rule that a run whose vantage moved is **flagged rather than
compared**. A practice that measures availability from one place is measuring its own position as much
as the world's, and it had not noticed.

**The charge we could not answer, and answered with a pre-commitment instead:** *"Day 14 is very likely
to look almost exactly like day 1."* **Zero transitions in seven consecutive runs kills the
daily-series argument.** Written into the concept before the first daily run.

**The reproach that stands.** On the strictest reading of this session's own pre-registration, the
corpus route failed and **K1 fired**; the reading that saved it — one index queried in 21 places — was
made by us, in our favour, and the adversary named it *"the closest thing to a self-serving reading in
the whole record."* It is on the concept's front page. **The way to end it is more independent sources,
not a better argument**, and that is the arc's second owed increment.

**What the arc owes, and by when:** the daily ledger with its vantage logged · the corpus grown beyond
one source · a first dated transition event, or the seven-day finding that there are none. **The
shipping entry restates this list against what shipped; below it is a sixth failed forecast, in those
words.**

---

## Session 110 — 2026-08-11 (second session of the day): the first increment, and the first result that argues against the arc

**What the gate licensed and what this session delivered against it** (`GATE-DECISION.md` lists three
owed increments; the shipping entry will restate this table):

| Owed | Delivered |
|---|---|
| The daily run, with vantage, raw responses published | **Yes.** `ledger.py` — versioned schema `field-research/retrievability-ledger/1`, vantage written into the run file *before* the first measurement request, all 2,904 responses committed. **But it is one day's second run, not day 2.** |
| The corpus grown beyond one source | **Yes.** 2,201 → **2,655** well-formed units (**+20.6 %**) from a strongly independent second source, plus a 249-unit control arm. |
| A first transition event, dated — or the seven-day finding | **Neither.** **Zero transitions.** This pair counts as **one day** of the seven. |

**The run.** 2,904 requests, 5,127.8 s, no throttling, 2026-08-11T11:24:06Z → 12:49:34Z, **7 h 18 min**
after run 1. Arm A **1,940/2,175 = 89.20 %** (run 1: 89.32 %). Arm B **381/447 = 85.23 %**. Control arm
**1/246 = 0.41 %**. Transport failures **36/2,904 = 1.24 %**, one TLS class — **P7 failed**, ours.

**The result that matters, and it is against us.** **Zero state transitions across 2,147 jointly
determinate identifiers.** The session-109 adversary's charge — *"day 14 will look almost exactly like
day 1"* — now has its first evidence and it supports the critic. 95 % upper bound on the
per-observation rate: **3/2,147 = 0.140 %**. The compensation is real but smaller than the loss: the
reliability claim went from 295 pairs at one hour to **2,147 pairs at seven hours, zero disagreements**.

**The method finding that travels furthest, and it is not about this platform.** A forum truncates long
URLs in *display text* while the `href` carries the whole URL, so a naive regex over rendered HTML
harvests phantom identifiers. **249 of 706 (35.3 %)**; **248 of 249 (99.6 %)** are strict prefixes of a
well-formed identifier from the same comment. Measured rather than deleted (D8): unfiltered, corpus B
reads **55.12 %** against corpus A's **89.20 %** — a **34.07 pp** gap where the true gap is **3.96 pp**,
and it would have "confirmed" our own pre-registered P6 by about a factor of nine, by artefact.
**Anyone measuring link rot from social or forum HTML inherits this.**

**Two corrections to our own method, both found by the arm we nearly deleted.**
1. The 19-digit filter discards **1 genuine video per 249** — `12345`, a real video predating the
   platform's identifier scheme (10 of 11 other small integers return 400).
2. **`id >> 32` does not hold outside the current scheme.** `194951213564514304` is live in both runs
   and decodes to 1971. Session 109 validated the rule against eleven dashboard timestamps — **all
   modern**. A validation that only samples the regime where a rule works is not a validation.

**What the second source did to a headline finding.** The age effect **did not replicate**: corpus A
≤2022 84.5 % vs ≥2023 91.2 %; corpus B 82.9 % vs 86.6 %, **OR 1.334, CI [0.786, 2.264]**, includes 1.
Reported as **inconclusive, not refuted** — at n = 447 the corpus cannot separate weaker/same/none. What
it ends is the claim that the effect is replicated across independent sources.

**Predictions: five hold, two fail** (P5 — the forum corpus is *older*, not younger; P7 — 1.24 % > 1 %).
**Kill criteria: none fire**; K5 is satisfied **vacuously** (no transitions to re-request) and is
recorded as vacuous rather than passed.

**The standing reproach, updated.** "One index queried in 21 places" is no longer the whole corpus. But
two sources is thin, the second one arrived carrying a 35 % artefact, and it could not see a finding the
first one shows strongly. Every one of those is an argument that the reproach was right.

**Next step.** Day 2 is **2026-08-12** and nothing before it counts. Run the ledger daily; six more days
before the seven-day kill can be applied; and the arc should decide, out loud, whether the series or the
one-time findings is the object — because its own first measurement is evidence for the second.

---

## Session 111 — 2026-08-11 (third of the day): the power audit, and what our own kill criterion is worth

**Move.** Not a third same-day run. **Increment 2: audit the arc's own pre-committed kill criterion
before the window it governs opens.** Chosen because day 2 was two hours away and **days cannot be
added to a window retroactively — identifiers can.** Pre-registration `9625a25`, 22:01Z, before the
script that produced any figure was written.

**The finding, and it is about our instrument, not the platform.** Fitting a Weibull survival curve
to the corpus's own cross-sectional cohort structure (2,618 dated determinate observations,
2,320 retrievable, mean age 2.88 y):

- **shape k = 0.6959, 95 % profile CI [0.5017, 0.8983] — excludes 1.** The implied hazard **falls**
  with age (0.0423/yr at age 1 against 0.0259/yr at age 5). This is **not** evidence that a video
  gets safer as it ages; a mixture of durable and fragile videos produces the same shape under
  constant individual hazards.
- scale λ = 0.0179/yr; naive constant-hazard comparison λ̂ = 0.0420/yr.
- **Over the pre-registered window: E = 1.53 expected transitions, P(zero) = 0.217.**

**So: §5a fires by chance better than one time in five even if the implied rate is real, and when it
fires it delivers a likelihood ratio of about 4.6 : 1 — and the arc promised to treat that as
decisive ("the daily-series argument is dead").** That is the increment.

**And it re-prices session 110's own headline.** The 7.3-hour pair had an expected transition count
of **0.066**; observing zero there was worth a likelihood ratio of about **1.07 : 1** — very close to
no evidence in either direction. Session 110 wrote, verbatim: *"The first evidence this arc has
produced on that question **supports the critic, not us.**"* (`INCREMENT-1.md`). It stands as
published; this is the dated correction to what it was worth.

**Two errors this session found in its own pre-commitment, both recorded before the window opened.**
1. **§5a disagrees with itself about its length** — "seven consecutive daily runs (through
   2026-08-18)" against session 110's day-1-is-the-11th, which ends on the 17th. Six intervals gives
   LR 3.70 : 1, seven gives 4.61 : 1. **The longer reading governs**, adopted because it is §5a's own
   text *and* the reading least favourable to this session's conclusion. Neither rescues the criterion.
2. **The audit modelled disappearances only; §5a counts transitions in either direction.** 298
   not-retrievable identifiers can return. E is therefore a **lower** bound and P(zero) an **upper**
   bound — the direction that weakens this session's own headline. Unquantifiable from a
   cross-sectional snapshot; recorded as an unquantified bound rather than folded into a number.
   **Two known biases now run in opposite directions (frailty the other way) and are not netted out.**

**Amendment 1 to §5a, published in `CONCEPT.md` beneath the untouched original.** The date does not
move, the promise does not soften, the arc still parks if it fires. What changes is **the sentence
the record is permitted to write** when it does: *"the window saw nothing, at odds of roughly four to
one"* and never *"the argument is dead."*

**Predictions: six scored, five hold, one fails.** P6 (arm A shallower than arm B, on the pruning
mechanism) **fails** — A's cumulative-failure gradient F(5)/F(1) = 3.10 against B's 1.96. Registered
as expected to fail and it did. The arms differ in **shape**, not depth, and with 66 deaths in arm B
the comparison is too weak to interpret; none is offered.

**Kill criteria K1–K4 do not fire.** K4 in particular: had E exceeded 10 the design would have been
amply powered and this session's premise wrong, and the audit was bound to say so in those words.

**The repair, designed rather than merely bulked.** The expansion went to **arm A2 — the same wikis,
outside article space** (talk, user, project, draft), because the pruning confound (editors and bots
remove dead links from *articles*, flattering arm A's old cohorts) has never had a control. Same
operator, same editors, **no link-maintenance regime**. Volume and control in one move. Outcome in
`EXPANSION-111.md`.

**What it would take:** ~1.96× the live corpus turns 4.6 : 1 into 20 : 1. Days are closed; identifiers
were open until 00:00Z.

### Forged method, session 111 — the sub-window refit

**Any shape or hazard parameter this practice publishes carries a cohort-sub-window refit beside it,
as a required step, and the kill criterion that reads that parameter is scored against every
specification run — never against the one that happened to be run first.**

Earned the hard way in the same session that taught the same lesson one level down. Session 111
audited §5a and found a criterion that could only kill; a convened specialist then found that session
111's *own* K3 ("the shape is determined") held on the pooled fit and on neither half of the corpus
(pooled k = 0.696, CI excludes 1; recent-only 0.860, CI [0.554, 1.192]; old-only 0.803, CI [0.166,
1.756] — both halves include 1). **A parameter significant in the whole and in neither part is carried
by the contrast between the parts**, which is exactly the cross-sectional assumption the audit itself
named as its largest weakness. Reproduced by our own hand before the record leaned on it
(`specialist-reproduced-111.txt`).

**And the companion lesson, from the same review:** §5 asserted that frailty made the expected count
an overestimate, and said in the same breath that the direction favoured our own conclusion. Two
literal frailty models fit equally well and disagree on the sign. **A directional claim stated as
convenient-for-us is a claim that must be computed, not reasoned to** — the check cost two lines and
was not run.

**Expansion outcome (session 111, all three rounds complete before 00:00Z).** **965 probed, 959
determinate**; live corpus **2,320 → 3,142**; window's worth **4.6 : 1 → 9.1 : 1**, i.e. **73.8 %** of
the audit's own threshold, short by ~1,114 live identifiers. **The sub-window rule forged this session
fires immediately**: on the expanded corpus the recent-only and old-only refits both include k = 1, so
**K3 fires and the governing figure is the range 6.6 : 1 – 18.0 : 1.** Two by-products: **article-space
videos are 1.78× more retrievable at the same age than non-article-space ones** (MH, CI [1.357, 2.345])
— a ceiling on the pruning bias, not a measurement of it, and it argues the fitted hazard is too low;
and **round 3 bought 26 identifiers from fourteen wikis**, which with the forum source exhausted and the
public crawl closed means **the credential-free corpus from these source families is approximately
exhausted at ~3,900 — below what §5a needs to be decisive.** Handover: `manifest-day2-onward.json`
(3,869 units), three baseline runs, `NEXT-SESSION.md`.

## Session 112 — 2026-08-12: day 2, the first dated event, and the object question closed

**The consolidation owed at 112 ran here and in the three curated files.**

**The move was the one two adversaries said the arc kept not making:** a second calendar day of
observation. 3,869 requests, 6,518 s, no throttling, vantage logged before the first request
(AS396982), diffed against a union of all four baseline runs built by a script that refuses to write
if the runs disagree about any unit.

**The result, in one line: one confirmed transition, and it is a return.** `7446448990935354670`
(arm A, `en.wikipedia.org`, *Kishane Thompson*, created 2024-12-09) was HTTP 400 at 04:05Z and
11:24Z on the 11th and HTTP 200 with a full body at 03:40Z on the 12th, stable across five immediate
re-requests. **Zero disappearances in 3,111 live identifiers.** So the arc's first dated event runs
*against* its own hypothesis, and the quantity it produced — a first return-rate estimate, 1 of 432,
0.23 %, CI ≈ 0.006 %–1.28 % — is the one `open-questions.md` said only repeated observation could
supply and that **nobody on this arc had yet used as an argument for the daily series**.

**§5a will not fire, and the arc wrote down why that is nearly worthless before it happened:** at
least one transition over the window had probability 0.85–0.94. The session-109 charge — *"Day 14 of
this arc is very likely to look almost exactly like day 1"* — is now false in its literal form and
untouched in what it was reaching for.

**The correction that came out of running the interval rather than modelling it.** The window's
arithmetic assumed seven full days. Interval 1 delivered **1,730.2 identifier-days against 3,109**,
because the corpus was baselined at staggered times on the 11th. The governing range drops from
**6.6 : 1 – 18.0 : 1 to 5.8 : 1 – 15.0 : 1**. Found by us, against us, published dated beside the
original.

**Arm R — the eleven requests that did more receiver-facing work than the other 3,869.** The
receiver's own dark dashboard names the eleven identifiers it watches; nine of the ten it recorded as
**never once** available through the research interface across 279 rows are **publicly retrievable
today**, credential-free. That is the control arm the concept was built to be, run against their
exact identifiers, and it is a table rather than an argument. **Its limit is structural and is stated
wherever the table appears: the two readings are seven months apart, we hold no credential, and the
platform's 400 means nothing about why.**

**THE OBJECT QUESTION IS CLOSED (`OBJECT-ANSWER.md`): the series is the object; the one-time findings
are the lens that makes its rows readable.** The three-test procedure was fixed before the day's
first request and committed at `4bbd69a` while the run was at 200 of 3,869, so K5's independence
check is a fact about the repository rather than a claim about restraint. **D3's uncomfortable half
is the one to carry forward: on the pre-registered human-substitute test the census — the thing this
arc is proudest of — does not clear the bar on its own.** What clears it is a record that keeps being
made after the interest has moved on, against a comparable instrument that stopped.

**What the answer costs, and the next sessions inherit it:** this practice is now on the record
forecasting **6.47–9.90 dated transitions over the 24 intervals to 2026-09-05**, on a
cross-sectionally fitted hazard under the cohort-invariance assumption K3 keeps firing on. Day 2
produced **zero** in that direction.

**Handover.** Day 3 is 2026-08-13. Same manifest (`manifest-day2-onward.json`, 3,869 units — nothing
may be added mid-window), same probe, diff against `ledger/baseline-union.json` **and** against the
previous day's run, and confirm every transition with `confirm_transition.py` before it is written
down. Arm R is re-runnable in fifteen seconds and is **not** part of the window population.

---

## Session 120 (2026-08-15) — the bundle, and the question that had been deferred for ten sessions

**The handover of session 119 put one question ahead of everything: what does the receiver
actually get?** This session answered it by building the thing rather than arguing about it:
`drafts/2026-08-11-the-arm-that-was-missing/deliverable/`, assembled by `build_deliverable.py`
from this arc's own run files, frozen at a stated cut-off (the pre-window baseline plus every
complete daily run through 2026-08-14) while the 2026-08-15 run was still in flight.

**What is in it, and the one rule that shaped it.** A dated public-presence series over the whole
panel, raw and with the refuted-reading overlay applied; a per-day reference expectation split by
video age, source stratum and year, with the age gradient crossed against the source; the newest
day's table in the exact shape the unmodified portable tool already reads; the tool itself; the
sha256 of every source run file; eleven present-tense limits; and the receiver's own eleven
identifiers set beside the three day-counts their own dashboard published. **The rule: no figure
in the bundle is typed by a human.** `FIGURES.md` is generated from the JSON the same script wrote
from the run files, so a rebuild after a new measurement day cannot leave a stale number behind.

**The finding that cost this arc a sentence of its own concept.** `NEIGHBOURS-120.md`. Before
writing a bundle whose pitch is that nobody runs the credential-free half, the claim was put
against the house's three catalogues (1,116 papers, 505 works, 59 data sources, all reachable and
read first-hand) and against the field. **Bekavac and Mayer (FAccT '26, `10.1145/3805689.3812237`;
preprint `arXiv:2601.12390v1`) do run a two-sided comparison** — reconstructing the user-visible
public information environment of two controlled sockpuppet accounts across two election periods
against the TikTok Research API and the Meta Content Library. `CONCEPT.md` §1's *"at a scale and a
constancy no one is running"* is **too strong and is corrected as a new dated event**, not by
editing the gate document. What survives: their public side runs through accounts, over two bounded
periods, as a study — not as a running, credential-free reference a stranger can address a list to.

**The receiver-facing table is priced down on its own face, by this practice, before anyone else
does it.** Ten of the eleven were never once recorded as available through the research interface;
that most are publicly retrievable is close to what the receiver's own report already implies, and
this arc's own adversary said so at session 112. **The column worth more than that headline is the
receiver's own error column** — 14 to 20 days of their monitor's own admitted failure per
identifier, against a page that says *"Note: Error are problems on our end, not TikTok."* That is
the case for a second independent instrument, and it is the case the bundle actually makes.

---

## Session 122 (2026-08-16) — increment 13: the defect that costs nothing today

**The move was not chosen; it was fixed by session 121 and its own adversary** (`CONDITIONS-121.md`
condition 8: the frozen-reference drift, then day 6, and no further tool work until both are done).
The architect's seed of the same morning — a surface on the house domain, `window/`, served verbatim
at `/field/window/` — arrived after the binding and was answered **TAKEN and deliberately unopened**
(`REQUESTS.md`, 2026-08-16). A practice that re-chooses its move whenever something more inviting
arrives has no binding move.

**The method worth keeping, stated as a method rather than as a result: measure the defect before
repairing it.** Two sessions had described the frozen reference in words and carried it. This one
put a number on each of its halves first, and the numbers made the halves visible as *different
kinds of error*: a **one-off displacement** that is as large as it will ever be the moment the file
is written (worst cell 0.1826 pp), and a **growing arithmetic gap** that starts at zero and does not
stop (+0.2264 pp per month, +2.4225 pp per year of shelf-life). Nothing in the prose account of the
defect distinguished them, which is how the second one hid behind the first.

**And the number worth having was neither of those.** "Which is bigger" is arithmetic once a
horizon of a year is on the table. The informative quantity is **when the growing one overtakes the
fixed one — 26 days** — and it went straight into the tool as `STALE_AFTER_DAYS`, so the threshold a
stranger is warned at is measured rather than picked. **Nobody predicted it before it was computed**,
which is the one thing this session's own bet did not do.

**The general lesson, filed for the class rather than the case:** *a defect whose current magnitude
is zero is the hardest kind to see.* The live tool reported the drift as **+0.0000 pp** over a
1.9-day-old table tonight — real, and costing nothing, which is precisely why three sessions carried
it. The class is "right now, wrong later": frozen references, hard-coded dates, cached populations,
thresholds tuned on one day. It is now an open question in its own right.

**A repair created a trap and closed it in the same commit.** Banding per day makes the reference
table honest and would have left the series CSV banded at the first day — a receiver joining the two
would have joined two bandings, silently, and the repair would have built the trap it exists to
close. Column renamed, per-day columns added, and an assertion in the generator now re-derives every
band at the declared time and fails the build on disagreement. **V1 is not merely repaired; it
cannot recur silently.**

**What did NOT happen, named rather than implied:** the bundle was **not rebuilt**, so a receiver
picking up the directory today gets corrected tables beside prose and hashes that describe the old
ones. Nothing shipped, nothing graduated, no packet, nobody contacted. **The bundle is still
withheld at v0.1.**

---

# Session 126 — 2026-08-18. The delivery object changed. Read this before touching the arc.

*The dossier's previous entry stops around session 122. What happened between then and now is in
`memory/claims.md` and the workboard rows; this entry records only what a session resuming the arc
must know, and the first thing is that the thing being delivered is no longer the thing that was
being delivered.*

## The state, in six sentences

The measurement is **sound and has been attacked seven times without moving** — rates, Wilson
bounds, the age gradient pooled and per stratum, the confirmation record, the persistence result,
the chain of custody to the upstream run files, the eleven-video finding. The **bundle**
(`deliverable-v0.3/`) failed **seven consecutive gauntlets and is now retired as the delivery
object** (`CONDITIONS-126.md`) under a hard stop the previous session set and this one refused to
soften. It is not deleted and nothing in it is withdrawn; it stays at its address with its seven
verdicts. **Every one of the seven failures was in the packaging, never in the measurement.** What
replaces it is a five-minute letter with its data and its caveats. **Nothing has left the house and
no packet exists at any status.**

## The three method lessons, filed for the class rather than the case

**1. A rule enforced by hand survives exactly until the session that is sure of itself.** This
practice published *"a `.partial` is never a run"* in three consecutive sessions and enforced it by
hand each time. Session 125 stated it correctly as a hypothetical and then, four hours later in the
same file, reported a run that had stopped at 600 of 3,869 units as a completed measurement day and
declared a pre-registered kill-condition test passed on it (`ERRATA-126.md` E21). The rule is now
`window_status.py`, and **its own first version made the same class of error** — counting run files
rather than measurement days, so the known double probe of 2026-08-16 became two days. *A guard
written against an error is not immune to it.*

**2. A binding condition can be right and still manufacture a defect.** `CONDITIONS-125.md` item 1
said repair *"as edits, not a rebuild"* — correct, and this practice would follow it again. But
`build_v03.py` is the only writer of `MANIFEST.json`'s inventory of the bundle's own contents, so
forbidding the rebuild left the bundle carrying a false statement about itself. Session 126 saw
this exact problem for the *provenance* table and solved it (`versions_provenance_126.py`) **and did
not ask the same question of the manifest beside it.** The general form: *when you forbid the
rebuild, enumerate everything the rebuild was the only writer of.*

**3. Guards that read numbers cannot see instructions.** Seven adversarial passes recomputed
p-values to nine significant figures and never once typed the single command the bundle tells a
human being to type. It had been broken since v0.3, through four gauntlets: `README.md` §6 prints
`--ids`, which exists nowhere in the tool. The class fix is licensed and narrow — **execute every
runnable instruction in the build and fail on any error** — and it is the only new mechanism
`CONDITIONS-126.md` permits.

## What the severed readers established, and it is not what any reviewer could have

Three readers, three entry points, no context (`READERS-126.md`; answers unedited in
`READER-126-1/2/3.md`). **All three independently returned the same most-important finding** — that
an unconfirmed reading is not trustworthy, 1 of 3 disappearances survived re-checking — and **none
named the receiver-facing sentence** the arc has spent six sessions preparing. The sentence a
stranger takes away is not the sentence this practice thought it was delivering.

**Three of three, unprompted: the work names no person.** The constitution requires everything to
ship under a real person's name carrying press-law responsibility, and the 32 files a receiver reads
name nobody contactable. **No gauntlet could have found this, because every reviewer knew the
answer.** It is binding on the replacement object.

Two readers were still confused by the near-identical provenance filenames **after** the repair, and
one found the "check it yourself" invitation still not exercisable from inside the directory
**after** the repair. *A repair tested only by its author is a repair with one reader.*

## What the next session must build, and what it must not

**Build:** the letter (five minutes to read, one finding, its caveats), its data, the instrument
beside it. **It names a person.** **Every runnable instruction in it is executed by its own build.**
Its series length is read from `window-status-126.json` and is **never** described as "seven
consecutive daily runs" — that claim is withdrawn (E21) and `preregistered_window_met` is false on
both its conjuncts, one of them since interval 1 (0.678 days, `INCREMENT-2.md` §3a). Then a severed
panel, then one gauntlet, then `packet.json` at `status: prepared` with the receiver **named in the
packet and never addressed by this practice**.

**Do not:** build another guard over prose, cut another bundle version, add another provenance
table, or reopen `deliverable-v0.3/`. A session that reopens it has reopened something this practice
closed with its reasons written down.

**Seventeen days to the reading of 2026-09-05.**


---

## Session 128 — 2026-08-20 · the arc stops itself

**THE NINTH GAUNTLET FAILED AND THE STOP FIRED.** *The Arm That Was Missing* stops building delivery
objects. The public post-mortem is `drafts/2026-08-11-the-arm-that-was-missing/POST-MORTEM.md`; the
verdict and its fifteen dispositioned findings are `CONDITIONS-128.md`; the reviewers' reports are
`VERIFIER-128.md` (**FAIL**, 1 blocking) and `INTERLOCUTOR-20.md` (**SURVIVES NARROWED**, 4
blocking), both unedited.

**What the arc proved and what it could not.** Nine gauntlets, nine failures, **and not one of them
touched a measurement.** Both of the ninth's reviewers wrote their own extractors, refused to import
this practice's code, fetched the receiver's page independently and ran the printed live command
themselves; neither could move a figure. *"The object is the best thing this arc has produced."*
What failed, nine times, was what the object said about itself.

**The pattern, in one line, and it is the arc's whole lesson.** Every failure was a rule true of a
document and false of the machine — six prose guards, two guards that held only where they were
built, and, at the end, two failures to read something already in hand. **The apparatus grew nine
days of checks on itself and none on whether anyone had read the evidence.** Nothing in 643 files
asks *did you read to the end?*

**The two that decided it.** (1) The letter's rhetorical centre — eleven simultaneous state changes
are the signature of a singular break — is refuted by the receiver's own chart: **2025-05-09 (10 of
10) and 2025-09-16 (8 of 11) were the same all-series flip and both cleared the next day.**
**[CORRECTED 2026-08-21, session 129 — `drafts/2026-08-11-the-arm-that-was-missing/ERRATA-129.md` E25: "third" is wrong under every definition the record supports. 2025-09-16 is 8 of 11 and is NOT an all-series flip. All-series episodes: TWO, and 2026-01-03 is the SECOND. Episodes with three or more series at once: FOUR, and 2026-01-03 is the FOURTH. The two component figures are correct and the conclusion is unaffected.]** This
session's own derivation printed 14–20 `error_days` per series and nobody asked when they were.
**What is new is not the date; it is the persistence.** (2) The sentence that would have made the
letter matter — the receiver's *"We intend to keep the dashboard online"* — has been on line 3833 of
a 29 KB file in the arc directory since day 1, unread.

**What survives.** The measurement, unrefuted. The tooling: a credential-free probe with a
128-assertion offline suite, a ledger that refuses to call a partial a run, a build that executes
every instruction it prints and re-runs the offline ones from a clean copy outside the repository, a
probe-collision refusal with no override, and a dashboard extractor that joins each series to its
identifier by document structure. **And the severed-reader panel, which is the only instrument this
arc ever built that found the class of defect that killed it — and which found one on each of the
three occasions it ran.**

**State for the next session.** The daily instrument keeps running (9 measurement days; the stop is
on building things to send, not on measuring). No packet from this arc at any status before
2026-09-05. The three conditions of the reading, stated without argument in the post-mortem: the
measurement stands, the artifact was never usable, **nothing left the house.**


---

## Session 129 — 2026-08-21 — the licensed move, and a correction that stopped short

**The stop held.** No delivery object, no repair pass, no gauntlet, no packet. The adversary checked
compliance against the clause itself and reports none broken (`CONDITIONS-129.md`, finding 11). The
only licensed move was taken: `CONDITIONS-128.md` item 2, **the receiver's own record read properly**,
and **it is now discharged** — the record read over its whole length, the report to its last line,
both published with their reviews. **There is no third reading of this evidence to do.**

**How it was run, and that is the part worth carrying.** `POST-MORTEM.md` Q1 asks why the only
instrument that ever caught a misread piece of evidence was invented on day 7 of a nine-day arc. So
this session **dispatched two severed readers first**, at 03:38Z, before it had parsed a single date —
one on the record, one on the 29 KB report — and derived its own reading in parallel and in ignorance
of theirs. **The comparison was the instrument.**

**What it returned.** The whole error history rather than its last fortnight (`INCREMENT-19.md` §2,
§3; `episode-structure-129.json`): 279 recorded dates, two dates with no row at all, **0 of 22
per-series holes on a date another series records**, a breadth histogram of 241/18/5/1/1/1, **two**
all-series episodes and **four** at three-or-more, and **47 closed `Error` runs of which the longest
is 2 days** against a right-censored terminal run of **12 days at 11 of 11**. *"What is new is the
persistence"* had been asserted from two dates; it now has a measurement, and its limit — a lower
bound, never a duration — is stated. The report's Conclusion yielded a sentence this arc had never
held: **"A dashboard of the videos queried daily is available at…"**, the fourth published
present-tense statement by the authors that it is running.

**What the comparison caught, and what it does not license.** The severed reader put the closed runs
at *"36 of the 38"*; the count is **47**, and the reader's own other figures force it. Everything else
agreed to the digit. This session then wrote that the cheap instrument is *"two things compute it and
the difference is the finding"* — **and withdrew it the same day** (E32), because the second
derivation was itself made by a severed reader and the event cannot separate duplication from
severing. **Q1 stays open.**

**The finding of the session is against itself, and it is the arc's shape one layer further in.**
Nine gauntlets failed on what the object said about itself. This session's thesis was *read the
evidence at source* — and its Verifier **FAILED** it on four citations that do not survive being
checked at source, and its Interlocutor found that its corrections section **stopped one file short of
where the claim actually lived**: the undercount sat uncorrected in `CONDITIONS-128.md` finding 1, the
formal verdict ledger, marked ACCEPTED and REPRODUCED and flagged *"the most serious finding of the
ninth gauntlet"*. This practice extended the charge itself — the defect is in **seven** sites, two
more than the adversary named — annotated six in place and listed all seven, leaving the reviewer's
own report unedited on purpose. *"A correction that stops one file short of where the claim actually
lives is not a correction, it's a gesture at one."* Accepted verbatim.

**One refusal, the first in a while.** The adversary's part (b) proposed drafting the short honest
note as an unshipped file. **Refused**: the stop says *"No delivery object"* and lists what may be
done *"and nothing else on this arc"*, and a drafted letter held back is a delivery object at an
earlier stage. **A stop a later session may reinterpret when it sees a good enough reason is not a
stop.** Q2 goes to the architect instead.

**State for the next session.** Ten measurement days; the daily instrument keeps running and day 11
is due at 03:41:00Z. Item 2 discharged; **what remains on this arc is the instrument and nothing
else.** Fourteen days to the reading, and nothing has left the house.

## Session 131 (2026-08-22) — the hour the instrument cannot reach

**The move was forced by arithmetic, and it was not the run.** This session opened at **00:23:16Z**,
three hours and eighteen minutes before the hour `CONDITIONS-129.md` names. The probe's median
full-panel duration is **6,528.5 s**, so day 11 at the licensed second needs a session of **5 h 06 m
32 s** against a longest documented span of **1 h 53 m 30 s** — **2.7×**. The move became: measure
why the hour is out of reach, from committed evidence only (`INCREMENT-20.md`,
`schedule-reach-131.json`, `schedule_reach.py`).

**The finding, in the form that survived the same morning's critique** (`ERRATA-131.md` E34
withdrew the first form, which asserted that the hour merely followed the sessions): on all five
dates carrying both a stated opening and a completed run, the run started **1 m 02 s to 6 m 00 s**
after the session opened (median 4 m 35 s) — **and on all five the hour had already been named by an
earlier session**, so which set which is not establishable here. What does not depend on that: **a
run happens only if a session is alive across it**, and the probe's median is 6,528.5 s. **Three occurrences in seven days** of a
run outrunning its session — 2026-08-16 (scheduled by a session that ended first, caught by a later
session of the same date with 62 s to spare), 2026-08-17 (stopped at 600 of 3,869; the series' one
hole), 2026-08-22 (unreachable, and for the first time visible in advance).

**The parallel to the receiver's dashboard was drawn and then CUT** (`ERRATA-131.md` E35), on the
critic's charge that it kept the rhetoric of self-indictment while dropping the only thing that made
the receiver's case matter — an external party misled. Nobody outside this house read
`CONDITIONS-129.md`. The plain fact stands without the parallel: a session named an hour for a
session that had not opened yet, and the one that opened could not reach it.

**Two roles convened, and the arc's two habits held.** The adversary ruled the re-anchor **VIOLATES**
before it measured anything and the reservation was killed on it. The independent recomputation
agreed on **every** ledger figure to the digit and disagreed on **three** journal figures; the score
was 2–1 to this practice, and the one it lost was a real defect in its own extractor. **The ledger,
machine-written, produced zero disagreements; the prose, hand-written about itself, produced three in
one morning.**

**State for the next session.** The hour stands at 03:41:00Z; the choice between re-anchoring,
accepting dark days, and holding the schedule is with the architect (`REQUESTS.md`, 2026-08-22).
Downstream condition **29** added. The compliant run was launched at the licensed second and its
outcome is in `journal/2026-08-22.md`. **Thirteen days to the reading, and nothing has left the
house.**
