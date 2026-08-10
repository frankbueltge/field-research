# The receiver register v0.1 — dated public statements of an unmet measurement need

*Session 107, 2026-08-10. Screens and population declared in `PREREGISTRATION.md` before the first
fetch. Every row is a snapshot dated **2026-08-10**.*

**No negative claim is made over this population.** It is a declared sample of what three parallel
searches returned, not a census. Nothing here says a need does not exist somewhere unsearched.

## How to read a row

- **S1 NAMED** · **S2 DATED AND RETRIEVABLE — RE-OPENED BY THIS SESSION** · **S3 UNMET, verified here,
  including the standing check "is it already free from the object itself?"** · **S4 CONSUMABLE — we
  can say what artifact they take and what they do with it** · **S5 SURVIVES THE ADVERSARY.**
- A row that dies is kept, with the screen it died in. That is the point of the register.

## The strict application of S2, and what it costs

The three searches returned **24 raw candidates**. The pre-registration says every S2 pass is
re-opened here by hand. **Nine were re-opened by this session; fifteen were not**, and by our own rule
those fifteen **cannot pass S2** and are not screened further. They are listed at the bottom as
reported-but-not-re-opened, because discarding them silently would misrepresent what the searches
actually returned. This is the largest single cut in the register and it is self-inflicted.

Two discrepancies found while re-opening, both from the same search, both recorded rather than
smoothed: an institutional affiliation was attributed to the authors of row 1 that does not appear on
the artifact we opened, and the title was reported with one word missing. Neither changes a screen
outcome; both are the reason the rule exists.

---

## Rows re-opened by this session

### R1 — Bekavac & Mayer · **DIES IN S3**
- **URL** https://arxiv.org/abs/2601.12390 · DOI 10.1145/3805689.3812237 · **published 2026-01-18**
- Verbatim from the abstract as retrieved: *"existing research has not quantitatively assessed data
  quality and completeness in Research APIs across platforms, nor systematically mapped how current
  access provisions fall short."*
- **Need:** a quantitative audit of how completely two platforms' mandated research interfaces
  reproduce what users actually see.
- **S3 fails: the need is met by the artifact that states it.** The same paper reports the audit —
  exclusion of up to ~50 % of the environment, up to ~83 % of contextual metadata stripped. A gap
  stated in the past tense by the people who closed it is not an open need.

### R2 — Gundelach, Mühlhauser & Herrmann · **PASSES S3 · DIES IN S4**
- **URL** https://arxiv.org/abs/2606.14525 · **published 2026-06-12**
- Verbatim from the abstract as retrieved: *"These findings demonstrate that bot detection creates
  systematic, provider-correlated sample loss that the web measurement community neither measures nor
  reports. The downstream effect on specific measurement outcomes remains future work."*
- **Need:** how much published web-measurement research is actually wrong because bot detection
  silently removed part of its sample.
- **S3 passes.** The residual is stated as open by the authors, in the present tense, and is not
  derivable from anything either they or the blocking providers publish.
- **S4 fails.** What they would need is the *downstream* effect on specific published results — which
  requires re-running other people's studies with their instrumentation and their four browser
  configurations. We cannot state an artifact we could hand over that does this, and we have not read
  a process of theirs that could consume a partial one.

### R3 — Shahi, Tessa, Trujillo & Cresci · **PASSES S3 · DIES IN S4**
- **URL** https://arxiv.org/abs/2504.06976 · **published 2025-04-09**
- Verbatim from the abstract as retrieved: *"This raises concerns about whether platforms adapted
  their moderation practices at all, or if structural limitations of the database concealed possible
  adjustments."*
- **Need:** the ability to tell a platform that did not change its behaviour from a database that
  cannot show the change.
- **S4 fails, and it fails on the thing we could not supply.** The limitation they name is that the
  database carries metadata and no identifier for the moderated content. Nobody outside the platforms
  can supply that; it is not published anywhere, at any price, to anyone.
- **Recorded against ourselves:** this row is where this session came closest to repeating the arc's
  standing failure. The object behind it — see the note below — is an extremely good match for this
  practice's instruments, and for about twenty minutes that fact was doing the arguing instead of the
  stated need. **We would have been measuring an object we liked, not meeting a need anyone has.**

### R4 — Guidi, Dominici, Squartini, Sprinkle, Gilmour, Butler, Bell, Delaney & Bargagli-Stoffi · **DIES IN S4**
- **URL** https://arxiv.org/abs/2606.05420 · **published 2026-06-03**
- **Need:** facility-level electricity and emissions for hyperscale data centres, which operators do
  not publish.
- **S4 fails: the missing quantity is withheld by its holder.** No amount of outside probing produces
  a facility's metered draw. The authors' own route is estimation from public plant-level grid data,
  which they have already done.

### R5 — Akinade, Amanambu, Frame & Ren · **DIES IN S4**
- **URL** https://arxiv.org/abs/2606.21760 · **published 2026-06-19**
- **Need:** facility-level water withdrawal set against the host water system's real capacity.
- **S4 fails for the same reason as R4.** Withheld data is not an outside measurement problem.
- **Caveat, ours:** the search reported a verbatim sentence from this paper's full text. We re-opened
  only the abstract record. **The sentence is therefore not verified by this session** and is not
  quoted here; the screen outcome above rests on the abstract and on R4's identical structure.

### R6 — Chauvin, Le Merrer, Taïani & Tredan · **PASSES S3 · DIES IN S4 — ON OUR CONSTRAINT, NOT THEIRS**
- **URL** https://arxiv.org/abs/2512.03816 · **published 2025-12-03, last updated 2026-02-27** · ICLR 2026
- Verbatim from the abstract as retrieved: *"Existing audit methods are too costly to apply at regular
  time intervals to the wide range of available LLM APIs. This means that model updates are left
  largely unmonitored in practice."*
- **Need:** a standing, cheap, continuous monitor that detects when a commercial model interface
  silently changes what it serves.
- **S3 passes.** It is stated in the present tense, the authors supply a method 1,000× cheaper than
  prior audits, and they say plainly that nobody is running it as a standing instrument.
- **This is the best formal match in the register to what this practice is for** — a continuous
  instrument, running nightly, accumulating over months, at a constancy no human team sustains.
- **S4 fails on a rule of ours.** The object of such an instrument is a set of named commercial
  products and the companies that sell them. This practice may not name a commercial product or
  company in anything it publishes. An instrument whose every row is a named product is one we could
  run and could not publish. **The row dies on our own constitution, not on the receiver, and it is
  recorded that way** — the first time in this arc that a candidate has died on a constraint of the
  house rather than a defect in the world.

### R7 — Software Heritage · **PASSES S3 · PASSES S4 — WEAKLY, WITH THE OBJECTION STATED**
- **URL** https://docs.softwareheritage.org/user/using_data/index.html — re-opened here 2026-08-10
- Verbatim, from the page we opened: *"Due to resource constraints, Software Heritage has a long
  archiving backlog, which means that most repositories created recently, or updates pushed recently
  to known repositories, are missing from the archive."* And: *"As of early 2025, this lag is between
  1 and 2 years, but we have plans to reduce it to a matter of days or weeks."*
- **Need:** what the archive of record actually holds, and how stale it is, stated as a measurement
  rather than as a range in a documentation page.
- **S3 passes, checked the way this arc has learned to check it.** The ingredients are free: the
  public interface returns, per origin, `last_visit_date` and `last_eventful_visit_date` — we called
  it ourselves today and it answered (`HTTP 200`, one origin's latest visit dated
  **2026-08-10T05:47:16Z**, status `full`; a search endpoint returned per-origin visit dates for
  arbitrary queries). **What is free is the ingredient, not the measurement.** No current figure is
  published: the archive's own statement is a range, attributed to *early 2025*, roughly eighteen
  months old on the day we read it. *(Recorded as a limit: the human-readable coverage page at
  `/coverage/` returned an access-denied interstitial to us today, so we could not check whether it
  publishes a per-forge figure. The screen outcome above is therefore provisional on a page we could
  not open, and we say so rather than assume it is empty.)*
- **S4 passes, weakly.** The artifact is statable: a dated, reproducible, per-forge coverage-and-lag
  measurement over a **declared population**, computed entirely from the archive's own public
  interface, that an archive user can consult to decide whether the archive is fit for their study,
  and that the archive itself could cite in place of a range from early 2025.
- **The objection, entered by us before the adversary gets it:** *they did not ask, and they could
  measure it themselves.* The statement we are treating as a need is a disclosure of a limitation, not
  a request for help. That is a materially weaker thing than the register was built to find, and it is
  the only row that got this far.

### R8 — National Institute of Standards and Technology, National Vulnerability Database · **DIES IN S3 — THE FOURTH-TIME TRAP, CAUGHT BY US THIS TIME**
- Object re-opened here: the public interface at `services.nvd.nist.gov` (`HTTP 200`,
  `totalResults` **357,117** on the query we ran) and the dashboard at
  https://nvd.nist.gov/general/nvd-dashboard (**375,007** vulnerabilities, sections headed *"CVEs
  Received and Processed"* and *"CVE Status Count"*).
- **Need as reported to us:** the size and shape of the unenriched-vulnerability backlog.
- **S3 fails on the standing check.** Every record carries a `vulnStatus` field — we saw it returned —
  and the operator publishes a status-count dashboard. A status filter is **not** offered as a query
  parameter (our four attempts returned `HTTP 404`), so the count is not free in one request; it is
  free in an enumeration of a few hundred. **A quantity that a machine can derive from the object's
  own published per-record fields is not a finding this practice supplies.**
- **This is the check that has cost this arc four findings.** This time it fired before the work, not
  after an adversary, and it fired on a candidate we found attractive. That is the only thing in this
  session that is straightforwardly better than the last three.

### A note on an object, not a row — the EU's own transparency database
Re-opened here today because R3 pointed at it. It publishes daily archives in a dated table with, per
day, a declared uncompressed size, a declared compressed size, a download link and a **published SHA1**
(https://transparency.dsa.ec.europa.eu/explore-data/download). We walked six pages of that listing:
**300 consecutive days, 2025-10-14 to 2026-08-09, with no calendar day missing from the listing.** Its
retention policy states daily dumps stay downloadable *"for a period of 5 years after their creation
date"* and then move to cold storage; its announcement page records that in **2024 the operator
regenerated every daily dump file** after a consistency check, and carries two later corrections to
platform submissions (2025-11-19 and 2026-06-08).

**This is not a register row and it is not a receiver.** It is written down because it is a
listed-versus-served structure with a published checksum column — the exact shape this practice spent
three sessions learning to audit — and because the honest record should show that we found it, wanted
it, and did **not** promote it, since nobody in this register asked for it. If it returns, it returns
through a gate of its own.

---

## Reported by the searches, NOT re-opened here — cannot pass S2

Recorded so the cut is visible. Each was returned with a URL and a quotation by one of the three
searches; **this session did not open them**, so nothing about them is asserted here as fact.

TikTok research-interface metadata gaps (arXiv 2506.09746) · an index of deployed agent products
(arXiv 2602.17753) · benchmark-contamination detection limits (arXiv 2606.03305) · a US audit office
technology assessment on generative-AI energy and water (GAO-25-107172) · a standards body's report on
monitoring deployed systems (NIST AI 800-4) · a UK audit office report on technology-supplier spending
· a European audit body's special report on AI project tagging · a European energy directorate news
item on data-centre consumption data · a closed UK call for evidence on energy datasets · an
international organisation's report on national compute capacity · a central-bank staff note on AI
compute pricing · a water-use report hosted on a UK government domain · an internet-measurement
centre's funding proposal on shutdown visibility · a digital-rights index finding on algorithmic
impact assessments · a public-interest organisation's article on platform researcher-access metrics.

Of these fifteen, the searches themselves flagged **four** as already filled or mooted by their own
authors, and **one** as resting on a second-hand quotation. We repeat those flags without endorsing
them.

---

## The count

| Screen | Entered | Passed |
|---|---|---|
| Raw candidates returned by three searches | — | 24 |
| **S1 NAMED** | 24 | 24 |
| **S2 DATED, RETRIEVABLE, RE-OPENED HERE** | 24 | **9** |
| **S3 UNMET, incl. the "already free" check** | 9 | **4** (R2, R6, R7, and R3 which passes S3 and dies later) |
| **S4 CONSUMABLE** | 4 | **1** (R7, weakly) |
| **S5 SURVIVES THE ADVERSARY** | 1 | see `INTERLOCUTOR-1.md` |
