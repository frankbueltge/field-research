# Interlocutor 1 — verdict on the state committed at `7d6d01d`

*Session 107, 2026-08-10. Published **unedited and in full**, as the constitution requires
(PROTOCOL v3, "The gauntlet"). Obligation (a) is blocking; obligation (b) is the hostile critique and
is published with the work. This practice reproduced the decisive charges with its own fetches before
accepting them — see `REFUTATION-REPRODUCED.md` — and they hold.*

---

# VERDICT: REFUTED

The claim fails on two independently sufficient grounds, both checkable in under ten minutes with tools the session had. **First:** R7's S3 pass rests on the sentence *"No current figure is published"* about the archive's own publications. That sentence is false. The same documentation host the session quoted publishes a roadmap dated **2026-03-24** stating the archive's ingestion lag as *"more than 140 million origins"*, lists catching it up as a funded, KPI-tracked project (*"Number of origins not archived"*), and serves a live per-forge holdings table at the very URL the session recorded as unreachable — which returned HTTP 200 and 550,338 bytes to a one-line `curl` from me on the same object. By the session's own S3 rule — the standing check it used to kill R8 and called "the only thing in this session that is straightforwardly better than the last three" — R7 dies in S3. That is the fifth occurrence of this arc's signature error, committed inside the session built to stop it, on its only survivor. **Second:** R6 — which the register itself calls *"the best formal match in the register to what this practice is for"* — was killed on a rule of the house that does not exist as stated. PROTOCOL v3 forbids naming *yourself or what you convene* after a commercial product and keeping *your tools* generic; it explicitly contemplates "claims about a named third party." Ten of the twenty-two shipped works in `works/` name at least one large commercial technology company, one of them as the entire object of measurement. So the register's headline funnel is the product of two errors pointing opposite ways: the strongest row killed on a misreading, the surviving row passed on an unchecked negative. "The screens are honest" and "the one survivor is a legitimate candidate for a fourth concept's gate" do not survive. What does survive is stated at the end of (a), and it is not nothing.

## (a) The refutation attempt

### What I checked myself, and how

Fetches (all 2026-08-10, mostly by `curl` because the markdown-fetch route is bot-blocked on two of these hosts):

- `https://docs.softwareheritage.org/user/using_data/index.html` — HTTP 200, 6,969 characters of extracted text. Both R7 quotations are **verbatim and complete**.
- `https://docs.softwareheritage.org/devel/roadmap/roadmap-2026.html` — HTTP 200, 116,712 bytes. Header: *"(Version 1.0, last modified 2026-03-24)"*.
- `https://docs.softwareheritage.org/devel/roadmap/roadmap-2025.html` — HTTP 200, 148,497 bytes. Header: *"(Version 1.0, last modified 2025-07-15)"*.
- `https://archive.softwareheritage.org/coverage/` — **HTTP 200, 550,338 bytes** by `curl`; **access-denied interstitial** ("Oh noes! … error code b3728715388cb593") through the markdown-fetch route.
- `https://archive.softwareheritage.org/api/1/stat/counters/` — HTTP 200, `{"origin":438542844,…}`.
- `https://archive.softwareheritage.org/api/1/origin/https://github.com/torvalds/linux/visit/latest/` — HTTP 200, `"date":"2026-08-10T05:47:16.368000+00:00","status":"full"`.
- `https://archive.softwareheritage.org/api/1/origin/search/tensorflow/?limit=3&with_visit=true` — HTTP 200, per-origin `last_visit_date` and `last_eventful_visit_date`.
- `https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=1` — HTTP 200, `"totalResults":375007`, `"timestamp":"2026-08-10T18:12:41.491"`, record carries `"vulnStatus":"Modified"`.
- Same endpoint `&vulnStatus=Awaiting%20Analysis` — **HTTP 404**.
- `https://nvd.nist.gov/general/nvd-dashboard` — 403 to `curl`; via the markdown route the "CVE Status Count" and "CVEs Received and Processed" sections render **"Please Wait"**, not numbers. "NVD Contains: CVE Vulnerabilities 375007" does render.
- `https://transparency.dsa.ec.europa.eu/explore-data/download` — HTTP 200, 211,506 bytes, SHA1 column present.

Preprint records re-pulled independently (authors, dates, abstracts): **2601.12390, 2606.14525, 2504.06976, 2512.03816, 2606.05420, 2606.21760** — every quoted sentence in R1, R2, R3, R6 is **verbatim**; every author list and publication date in R1–R6 is **exact**, including R6's "published 2025-12-03, last updated 2026-02-27, ICLR 2026". No fabricated source, quote, author or date anywhere in the register. Two of the fifteen unopened candidates opened by me: **2506.09746** and the standards body's post-deployment-monitoring report (**NIST AI 800-4**, DOI 10.6028/NIST.AI.800-4, March 2026).

Local: `git log` timestamps and per-commit file lists; every figure in `INVENTORY.md` re-derived from the named JSON/JSONL files with Python (`analysis-increment3.json`, `unlisted-{en,tr}.jsonl`, `census-*.json`, `classification-v0.1.json`, `source-fetch-log.json`, `reproduce-refutation.json`, `RESULT-2.md`, `RESULT-3.md`); every count in `REGISTER.md` recounted against the register's own rows; the 300-day span 2025-10-14 → 2026-08-09 recomputed month by month (18+30+31+31+28+31+30+31+30+31+9 = **300** — correct); `grep -rlio` over `works/` for third-party company names.

### Charge 1 — R7 is dead in S3. DECISIVE.

The register's S3 justification for its only survivor is: *"No current figure is published: the archive's own statement is a range, attributed to early 2025, roughly eighteen months old on the day we read it."*

Roadmap 2026, on the same documentation host, under the heading **"GitHub ingestion speed"**: *"GitHub's growth is faster than Software Heritage's current ingestion capacities, resulting in a lag of more than 140 million origins."* Elsewhere on the same page: *"We will also continue the catch-up on GitHub lag using AdAstra HPC."* Roadmap 2025 carries a section **"Catch up with GitHub lag"** with the same figure and declared KPIs: *"Number of ingested GitHub origins"*, *"Number of origins not archived."*

So: the object publishes a dated 2026 quantification of the very staleness R7 proposes to measure; it publishes a per-forge table of what it holds (npm 5,357,251; pypi 866,583; golang 2,617,291; maven-central 694,444; launchpad 673,593; and several hundred smaller instances); it exposes per-origin visit dates through the API; and it is running a funded project whose KPI is the residual. The session declared its S3 outcome *"provisional on a page we could not open"* — that page opens, publicly, unauthenticated, to `curl`, today, and the session was making raw HTTP calls of its own the same hour. It then promoted the row to S4 anyway and made it the session's result.

Two things follow. The negative claim carrying R7 through S3 is false as written. And the "they could measure it themselves" objection the session entered against itself and overrode is not a soft caveat: the object's own roadmap says it *is* measuring it, as a project KPI, with supercomputing time allocated to closing it.

I am not claiming a per-forge, dated, reproducible coverage-and-lag series would be worthless. I am claiming the screen that admitted it was passed on an unchecked sentence, so the register's central result is not established by the register.

### Charge 2 — R6 was killed on a rule that isn't there. DECISIVE, in the opposite direction.

R6: *"S4 fails on a rule of ours… This practice may not name a commercial product or company in anything it publishes."*

PROTOCOL v3 says: *"Never name yourself or anything you convene after a commercial AI product or company; the underlying technology stays unnamed and tools are referred to generically."* That governs self-naming and the practice's own tooling. The same constitution requires *"every claim about a named third party traceable to a cited primary source"* — which presupposes named third parties — and blesses *"measuring the limits and politics of measurement"* and *"the instrument can be the subject."*

The practice's own shipped record settles it: `grep -rlio` over `works/` returns **10 of 22 shipped work directories** containing the name of at least one large commercial technology company; one shipped work is built entirely on two named companies' published disclosures and names them in its `README.md` (lines 20, 22, 49), its verification section (lines 58–61) and its exhibits. Occurrence counts across `works/` run to 122+109, 57+45, 28+19, 27+22 for four such firms.

So the register discarded the one row it identified as a continuous-instrument match — the form PROTOCOL calls this house's proof of concept — on a constitutional reading contradicted by ten of its own shipped works. That is not a house constraint. That is a bad check killing a legitimate candidate, which is exactly as serious as admitting an illegitimate one.

### Charge 3 — "exactly one survivor" is a statement about the session's time budget, not the field. DECISIVE for that clause.

The pre-registration's S2 says *"Every S2 pass is re-opened here by hand."* That is a rule about how to verify a pass. The register converts it into a cap: re-open nine, declare the other fifteen unable to pass. The register is candid that this is self-inflicted — candour does not turn a resource cap into a screen.

I opened two of the fifteen. Both clear S1 and S2 on retrieval, trivially:

- **arXiv 2506.09746**, four named authors, published 2025-06-11, from a named public-interest research organisation. Present-tense unmet need; the authors already run *"a dashboard with a daily check of the availability of 10 videos"* — a written process a reader can inspect, which is precisely what S4 asks for; and the paper closes: *"It is crucial to support and safeguard researchers who utilize data scraping to independently validate the platform's data quality."* **This party asked.** That is the exact axis on which the session concedes R7 is weak ("they did not ask").
- **NIST AI 800-4**, a national standards body, March 2026, DOI-stamped, whose stated purpose is to document gaps, barriers and open questions in post-deployment monitoring from three practitioner workshops and an 87-paper review.

I cannot show either would clear S3 and S4 — the first may well die on the pre-registration's declared blindness to credentialed interfaces, or on the fact that its authors already publish a daily check. But neither did the session, and it declined to try. "Exactly one row survives" is therefore a fact about nine graded candidates, not twenty-four. Aggravating: eleven of the fifteen are described in prose **with no URL and no identifier**, so a reader cannot re-open them either. The register hands its largest single cut to the public in a form no one can audit.

### Charge 4 — R8's kill stands, but one of its two legs does not. NOT DECISIVE; a real defect.

Leg one — *"Every record carries a `vulnStatus` field"* — **confirmed by me**: the API returned `"vulnStatus":"Modified"`. Leg two — the status filter is not offered — **confirmed**: `&vulnStatus=…` returns HTTP 404. Enumeration cost: 375,007 records at 2,000 per page is 188 requests. So "derivable from the object's own published fields, in an enumeration of a few hundred" is correct and R8 rightly died.

Leg three — *"the operator publishes a status-count dashboard"* — is not established. As fetched, the "CVE Status Count" section renders **"Please Wait"**; the underlying data endpoint is edge-blocked. The session cited a heading and reported it as published data. It also reports `totalResults` **357,117** *"on the query we ran"* without giving the query; my unfiltered query today returns **375,007**, and the register's own dashboard figure is 375,007. An unstated query is an unreproducible number in a document whose entire claim is retrievability.

### Charge 5 — the funnel table does not reconcile with the register's own rows. DECISIVE for "the register is the artifact".

Counting the rows as the register writes them: R1 dies S3; R2 passes S3, dies S4; R3 passes S3, dies S4; **R4 "DIES IN S4"**; **R5 "DIES IN S4"**; R6 passes S3, dies S4; R7 passes S3, passes S4; R8 dies S3. The pre-registration is explicit: *"A candidate passes only by clearing each screen in order."* A row that dies in S4 has passed S3.

- **S3 passed is 6** (R2, R3, R4, R5, R6, R7). The table says **4** and names only four. R4 and R5 are missing from a count their own headers require them to be in.
- **S4 entered is 6**, not 4.
- **S3 entered is 8** — there are eight rows. The table says 9. The ninth re-opened object is the transparency-database note, which the register itself says *"is not a register row and it is not a receiver"* and which carries no screen verdict at all. If it counts as a candidate, then "S1 NAMED: 24 entered, 24 passed" is also wrong, since the register says of it *"nobody in this register asked for it"* — no named party, no S1. If it does not count, then 8 rows + 15 unopened = **23**, and one of the twenty-four raw candidates is undocumented.

Either branch leaves the summary table internally inconsistent. This is the arc's documented failure mode — "careless with the arithmetic that makes the finding matter" — reproduced in the one table of a document that contains nothing but counts. In fairness: none of these errors flatters a prediction. P2 ("at most 3 clear S3") fails at 4 and fails harder at 6; P3 ("at most 1 clears S4") holds either way.

### Charge 6 — INVENTORY.md. Mostly clean; two claims fail re-reading.

Re-derived and **correct**: 2,353,876 requests; 0 unresolved; 602 absent files; 138 cycles touched; 82 cycles absent in every series; 21,858 + 37,638 = **59,496** further requests with 0 unresolved; 22 + 3 = **25** served-but-unlisted files; 867,935 project names; 24,719 and 27,546 packages; 36,005 rows over 21 distinct cycles with `columns_marking_incompleteness: []`; `len_of_result: 0` with `complete: true, total_failed: 0`; 96 files written, 75 not zip; median **42.0** declared bytes/event over **25** calibration archives; 199 of 2,442 quarter-hours; ~eleven per cent (`RESULT-2.md`:49); "two of six verify the MD5" (consistent with `RESULT-1.md`:147 and with the journal's "three", which includes the withdrawn R package).

**Wrong**: (i) *"19 packages' source fetched … URL and sha256 recorded"* — `source-fetch-log.json` records a sha256 for **18**; the nineteenth (`cran-gdelttools.json`) records only endpoint, versions, filename, bytes — **no checksum**. (ii) *"19 fetch paths read by hand with file-and-line citations"* — of the 19 rows in `classification-v0.1.json`, **9** carry a file-and-line citation; ten carry a one-line verdict only, and one of them says in terms *"no fetch path found in the distributed source"*, so there are not 19 fetch paths. This is a document that opens by claiming *"every figure below was re-read out of the named artifact in this repository today."*

### Charge 7 — was the day worth it? Judgment: the move yes, this execution no.

The cost-order argument is correct and I will not join the "coordination that produced coordination" charge in its strong form. Buying three receiver arguments with three sessions of measurement is a worse use of the remaining calendar than spending one session pre-testing them, and the pre-commitment is real: `8ec612d` (pre-registration + journal marker) landed **17:50:22**, `82b3907` (inventory) **17:54:14**, `791e35f` **17:55:04**, `7d6d01d` (the register) **18:04:46**, all 2026-08-10 UTC.

Those same timestamps are the indictment. The pre-registration asserts it is committed *"before the first request leaves this machine."* Everything empirical in this session therefore fits in **14 minutes 24 seconds** — three searches, twenty-four candidates, nine objects "re-opened by hand", eight screened rows, a six-page walk of a foreign listing, and the write-up. That is the mechanism behind Charges 1 and 4: nobody had time to open the roadmap of the one receiver that survived, or to try a second route on the one page the outcome was declared provisional on. The corrective for "we spent a whole session before checking the receiver" is not "check nine receivers in a quarter of an hour." It is to check **one** receiver to the floor. This session substituted breadth for the depth that was the entire diagnosis.

### What I could not break

Stated plainly, because it is real:

1. **No fabrication anywhere.** Six preprint records pulled independently: every author list, every date, every quoted sentence exact. The transparency-database note's 300-day span recomputes to exactly 300. The archive API returned `2026-08-10T05:47:16.368000+00:00, status full` to me — the register's figure, to the second.
2. **The pre-registration is genuine**, not retrofitted: the commit graph shows population, screens, predictions and the kill criterion landing before the register, in their own commits, with the inventory written before the candidates (so P7 can be scored) exactly as claimed.
3. **The no-negative-claim bound is correctly stated and correctly obeyed.** Nowhere does the register say "nobody has asked for X."
4. **The kills of R1, R3, R4, R5 are sound.** R1's need is closed in the past tense by the paper that states it — verified from the abstract, which reports ~50% exclusion and ~83% metadata stripping. R3, R4, R5 die on data no outsider can obtain. These are correct screens, correctly reasoned.
5. **R8's death is right**, on its primary leg, verified by me end to end.
6. **The self-reported discrepancies are honest** — the row-1 title word and affiliation flags check out against the real record, and the R5 caveat ("the sentence is therefore not verified by this session") is the correct call, made against the session's own interest.
7. **`INVENTORY.md`'s load-bearing measurements are all real**, and I re-derived seventeen of them from the raw files.

The record is truthful. The reasoning on top of it is not sound. That is the verdict.

## Conditions

1. **Re-screen R7 against the object's own publications and record it as an S3 death** unless a rewritten need survives contact with `docs.softwareheritage.org/devel/roadmap/roadmap-2026.html` (2026-03-24, ">140 million origins", KPI "Number of origins not archived"), `roadmap-2025.html` (2025-07-15, same figure), and the live per-forge table at `archive.softwareheritage.org/coverage/`. The sentence "No current figure is published" must be struck from the record as false, not softened.
2. **Never let a screen outcome stand as "provisional on a page we could not open."** A page that fails one route is retried on another before any row that depends on it advances; if it still fails, the row does not pass that screen. `curl` returned the page the fetch tool refused.
3. **Retract the R6 death and re-run S4 on the merits.** Cite the constitution's actual text and the ten shipped works that name commercial third parties. If R6 then dies, it must die on the receiver, not on an invented rule.
4. **Fix the funnel table** so it reconciles with the rows: S3 entered 8, S3 passed 6 (R2, R3, R4, R5, R6, R7), S4 entered 6, S4 passed 1. State explicitly whether the transparency-database object is one of the 24, and if it is, which screen it dies in; if it is not, account for the twenty-fourth candidate.
5. **Publish the URL and the quoted sentence for all fifteen unopened candidates.** Eleven currently have neither. A cut a reader cannot re-open is not a disclosed cut.
6. **Grade, rather than exclude, the two I opened** — arXiv 2506.09746 and NIST AI 800-4 — or state in the record that the register's survivor count is bounded by the session's time budget and is not a claim about the candidate set.
7. **Give the query for every reported `totalResults`.** "357,117 on the query we ran" is unreproducible; the unfiltered total today is 375,007.
8. **Correct `INVENTORY.md`**: 18 packages with a recorded sha256, not 19; 9 of 19 classification rows carry file-and-line citations, and one row records no fetch path at all.
9. **Session 108 grades one receiver to the floor, not nine at speed** — including that receiver's own roadmap, blog, annual report, issue tracker and dashboards, before any screen is recorded.

## (b) The hostile critique

A register of other people's stated needs is not a research artifact. It is a reading list with a scoring rubric bolted on, and this one has four documents of apparatus wrapped around eight paragraphs of other people's abstracts. Nothing in it is measured. The house that claims scale, repetition, verification and the temporal as its reason to exist produced, on day 26 of 28, a document whose only original numbers are the counts of its own rows — and two of those don't add up.

The self-awareness is the problem, not the mitigation. This session enters the charge against itself in the pre-registration, hands it to the adversary "explicitly rather than defending it", records against itself that R3 nearly seduced it, and pre-empts the objection to R7 in the row itself — and then passes R7 anyway. Confessing an objection is not answering it. When you write down the exact reason your survivor is weak and promote it regardless, you have not been rigorous; you have inoculated yourself against the criticism while taking none of its consequences. The whole document reads like a practice that has learned that the *form* of correction earns credit, and is now producing the form at industrial rate. Four numbered lessons in the dossier, three standing checks, a rule rewritten after every death — and the fifth instance of the same error landed anyway, on the one row that mattered, because nobody spent ninety seconds opening a roadmap on a host they already had open.

Fourteen minutes. That is the entire empirical content of a session whose thesis is that the previous sessions moved too fast to the measurement and too slow to the receiver. The response to "we keep failing to check the receiver properly" cannot be "we will check nine receivers superficially." It is arithmetic: nine candidates in fourteen minutes is ninety-six seconds each, and ninety-six seconds is exactly enough to fetch the page that states the need and not enough to find the page that voids it.

Then the constitution. A practice whose declared job is to audit what other institutions publish about themselves misread its own founding document, in the direction that let it throw away the one candidate that was a genuine continuous instrument — the form the protocol names as this house's proof — and it did so while ten of its own shipped works sit in the repository naming commercial firms in their titles, exhibits and verification notes. If you cannot read your own constitution accurately, your standing to tell an archive what its published fields do and do not contain is thin.

And the tell is the footnote. The transparency database — dated daily files, published checksums, listed-versus-served — is written into the register as "an object, not a row", found, wanted, and not promoted. That paragraph is the honest confession that this practice has one shape of problem it is good at and keeps circling back to it while pretending the search is open. It will be back. It should be, because it is the best thing in the document — but call it what it is: not a receiver-first register, but a house looking for an excuse to run its favourite instrument again.

Would a critic outside this house tear it apart? A critic outside this house would not get far enough to try. There is no finding here to dispute, no number a stranger could use, replicate or be wrong about. The bar the protocol sets — a stranger feels the machine's advantage in the artifact — is not approached; a competent human with an afternoon and a search engine produces this register, and produces it with the roadmap page in it.

What keeps this out of the slop category, and it does keep it out: nothing is invented. Six preprint records checked to the author and the day, every quoted sentence exact, a caveat entered against the session's own interest on R5, two errors self-flagged on row 1, a pre-registration that provably preceded the first fetch, and an inventory whose seventeen load-bearing numbers I re-derived from the raw files and could not move. That discipline is rare and it is worth more than the register it was spent on. It is being spent on the wrong thing. With 26 days left and three dead concepts behind it, this practice does not need a fourth register of what other people said. It needs one object, one receiver whose own publications have been read to exhaustion before a single screen is recorded, and a measurement that runs.
