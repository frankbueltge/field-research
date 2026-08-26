# Concept — *Cited, Not Retrievable*

**Gate session 1 of at most 3. Session 136, 2026-08-26.** Opened under `PREREGISTRATION-136.md`,
locked before any evidence in a commit carrying that file and nothing else. Five kill criteria are
locked there; §6 below reports each as fired or not fired.

Every figure below comes from a file in this directory that prints the command producing it. Nothing
here is typed from memory.

---

## 1. The claim, in one page

A public encyclopedia anyone can read cites short-form platform videos as **sources**. Those videos
are observable **only through the platform's own interfaces**: the largest free public web crawl
holds, for this domain, in its July 2026 crawl, **339 index entries — every one of them
`/robots.txt`, and zero video pages** (`../2026-08-11-the-arm-that-was-missing/DERIVED.md` §1),
because the platform's `robots.txt` names that crawler among 25 agents and tells them `Disallow: /`.

**So the ordinary instruments of citation health cannot see this class of source.** A link-checker
and an archiving bot both work by fetching the cited URL. For this platform that route is closed to
them by instruction, and what an unauthenticated fetch of a video page returns for a video that is
gone **is not established by this practice and is not claimed here** — it is the second increment
(§4b), and until it is measured every sentence in this concept about what maintainers can or cannot
see is **conjecture, marked as such wherever it appears.**

**What is not conjecture is that this practice already runs the instrument that can see it**, and
has run it for thirteen measurement days. `POST-MORTEM.md` §6 named the instrument as the thing that
survives the stopped arc: *"The stop is on building things to send, not on measuring… the tooling is
real and portable."*

**Computed today, offline, from run files already committed** (`edition-breakdown-day13.json`,
`series-stability-136.json`):

| | figure |
|---|---|
| encyclopedia-cited video identifiers under daily measurement | **3,166** |
| language editions they are cited in | **61** |
| distinct (edition, namespace, page) citations of them | **4,499** |
| **not publicly retrievable on 2026-08-25** | **374 of 3,134 determinate — 11.93 %, 95 % Wilson [10.62, 13.34] after the design-effect correction this practice owes** |
| **encyclopedia pages carrying at least one such citation** | **467 of the 3,249 pages that cite any of these videos — 14.37 %** |
| article space only | **260 of 2,376 — 10.94 %, [9.50, 12.51]** corrected, on **296** of **2,174** pages (13.62 %) |
| absent share across the **12** measurement days on one fixed corpus | **11.83 % – 12.14 %** — a range of **0.31 pp** |
| raw apparent day-to-day changes across those 12 intervals | **1, 1, 4, 2, 0, 4, 1, 4, 2, 0, 3, 2 — 24 in total**, out of ~3,134 determinate readings a day |
| apparent disappearances **refuted by the instrument's own five-fold re-request**, whole series | **6 of 16 RAW readings, and 6 of 16 GENUINE transitions — the two counts coincide in this direction** (`../2026-08-11-the-arm-that-was-missing/confirmation-record-121.json`; they do NOT coincide in the other direction, where raw is 12 of 12 confirmed and genuine is 10 of 10) |

**Every interval above and in `edition-breakdown-day13.json` carries the correction
`memory/downstream-commitments.md` condition 7 binds this practice to** — losses in this corpus clump
by cited account, the closed-form design effect is **1.4289**, and a Wilson interval computed with the
video as the independent unit understates its half-width by at least **×1.1954**. **The first version
of this session's script did not apply it**, and would have published sixty-odd too-narrow intervals in
the first artifact of a new arc — the exact defect the condition exists to prevent. It was caught by
reading the conditions file in full, which is what the constitution requires and what this session
nearly economised on. The uncorrected interval is printed beside the corrected one in the JSON and
**never alone**; the correction is a **lower bound** (the citing-page key gives 1.8854), and one design
effect does not fit every cell — applying the pooled figure per edition is this session's own choice,
conservative in aggregate and unvalidated cell by cell, and it is recorded as such in the artifact.

**The claim of this concept, in one sentence:** *the absence of platform-video sources from an
encyclopedia's citations is a large and remarkably stable **stock** — about one citation in eight,
unmoved to within a third of a percentage point over twelve nights — while the day-to-day **flow** a
single-pass instrument would report is small and, by this instrument's own confirmation step,
substantially its own noise.*

**Two things that claim is not.**

1. **It is not a claim that the videos are deleted.** `NOT-RETRIEVABLE` is the platform's single
   opaque refusal — an identifier that never existed returns the same HTTP 400, and no 404 is ever
   returned (session 109's three-arm control). It means *not publicly retrievable from this vantage
   right now* and nothing else, and the whole arc has held that line.
2. **It is not a rate, a trend, or a test.** Twenty-four raw apparent changes over twelve unequal
   intervals, six of sixteen confirmed disappearances refuted across the series — this practice has
   published against itself that six events is not a rate and eleven are not either
   (`CONDITIONS-132.md` item 5). **No trend is claimed here and no test is scored.** And
   `memory/downstream-commitments.md` condition 8 binds every confirmation count this practice
   publishes to travel with the word **raw** or **genuine** or not to travel at all: the table above
   was written without either word and is corrected in place. The two counts coincide for
   disappearances (16 readings either way) and **do not** coincide for returns (raw 12 of 12,
   genuine 10 of 10, after two of this arc's own artefact echoes are excluded).
3. **It is not a comparison with anybody's published figure, and one coincidence must be defused
   before a reader does the arithmetic themselves.** The Pew Research Center's May 2024 sweep of
   English Wikipedia reports **11 % of references inaccessible** and **53–54 % of pages carrying at
   least one broken reference** (`FANOUT-136-1-neighbours.md`; https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/).
   Our 11.93 % sits beside their 11 % and **the two numbers are not comparable and must not be read
   against each other**: different population (one platform's video citations against all reference
   links), different definition of inaccessible (a platform's opaque HTTP 400 against a general
   accessibility sweep), different scope (61 editions against English only), different date, and
   different method. **Nothing here says this platform's citations rot faster or slower than the
   average**, and establishing that would require running one method over both populations — which
   nobody has done and which this concept does not propose to do today.

## 2. Why this is not the stopped arc under another name

**The stopped arc asked whether a platform's credentialed research interface returns what is
public.** Its receiver was a small organisation whose dashboard monitors eleven videos; its object
was a letter; it failed nine gauntlets on what that letter said about itself, and its stop stands
whole — **this session refused, by its own decision under the architect's standing rule, the one
narrow licence it had asked for** (`../2026-08-11-the-arm-that-was-missing/INCREMENT-24.md`).

**This concept asks a different question of a different body, for a different receiver.** Not *does
the research interface cover public content* but *how much of an encyclopedia's cited evidence is
publicly unreachable, and can the encyclopedia's own maintenance regime see it*. The corpus was
built as the stopped arc's **control arm** and is here the **object**. No file frozen under
`verify_freeze.sh`, no text of the letter, and no gauntlet verdict is touched or reopened
(`PREREGISTRATION-136.md` K-D).

**This distinction is drawn by this practice in its own favour and is therefore not this practice's
to certify.** It is K-E, and it goes to the adversary as the blocking charge. **If the adversary
establishes that this is the stopped arc renamed, the gate fails and the stop stands whole.**

## 3. What only a machine could have done here

Stated against `PROTOCOL.md`'s four limbs, and stated as an argument, not as an entitlement — the
judgement of whether it holds as empirical research is the architect's, and it is a refusal he can
make, never an accolade he confers.

- **Scale.** 3,166 identifiers across 61 language editions, joined citation by citation to 4,499
  page-level references. A person with ordinary time samples; this reads the population.
- **Repetition.** Thirteen measurement days, each a full sweep of the same fixed list at a fixed
  second from a logged autonomous system, at one request per second.
- **Verification.** Every apparent change re-requested five times before it is believed, and **the
  refutations published against this practice's own interest** — 6 of 16 apparent disappearances
  refuted. That is the limb that makes the stability claim mean anything: without it, this concept
  would be reporting 24 changes it cannot tell from noise.
- **The temporal.** The stock-versus-flow distinction **is** the finding, and it does not exist on
  any single day. It required twelve nights to say that the number does not move.

**And the honest counterweight, stated here rather than left for the adversary.** The *headline
share* — one citation in eight — is a one-day figure that a competent person with ordinary time
could reach on a sample. **What a person cannot reach is that it does not move, and that the
movement they would report is mostly their instrument.** If this arc ever ships the share without
the stability and the refutation record, it has shipped the part a person could have made.

## 4. Increments

### 4a. The first, run today and offline — DONE

`edition_breakdown.py` and `series_stability.py`, both in this directory, both making **no request of
any kind**, both hashing every input they read. They produced the table in §1. `PREREGISTRATION-136.md`
K-B required exactly this: an increment computable today from files already committed, so that no arc
is gated on infrastructure that does not exist.

**Two defects of this session's own, found by this session and recorded rather than quietly fixed:**

- The first version of `edition_breakdown.py` computed per-edition absent shares over **citation
  rows** while printing a **distinct-identifier** column beside them — a share and its n from two
  different units (English: 1,343 identifiers against 1,414 "determinate"). Caught before anything
  was published from it; the unit is now the identifier-within-an-edition and is named in every row.
- The first version of the series computation, written at the shell, globbed `run-*T0341Z.json` and
  **silently dropped five measurement days** — the founding census at 1124Z and the four days the
  series ran at 0427Z, 0343Z and 0337Z before the hour settled. It reported eight days as the series.
  Nothing was published from it; `series_stability.py` now enumerates with no hour filter, prints
  every hour it used, and prints the day count so a reader can check it against the record's own
  thirteen.

### 4b. The second, and it is the one that decides whether any of this matters to anybody — NOT RUN

**Conjecture, and this concept marks it as one:** *an unauthenticated fetch of the cited video page
URL returns a success status for identifiers the platform's public oEmbed endpoint refuses — so a
link-checker records the citation as live, and this class of rot is invisible to the maintenance
tooling that actually runs.*

**It is not measured. Nothing in this repository measures it** — `grep` over the arc's 138 scripts
finds no fetch of a video page URL, only of the oEmbed endpoint and of account pages. It needs a
request, and `PREREGISTRATION-136.md` K-B forbade this session one. **It is the next session's
first increment**, it is small, and **it can falsify the whole concept**: if a plain fetch of the
page shows the absence plainly, then the ordinary instruments can see this after all and the only
thing left is the stability result. **That outcome is written here in advance so it cannot be
quietly dropped later.**

## 5. The receiver

`PREREGISTRATION-136.md` K-C requires a **real, reachable receiver outside the house with a
published interest in this exact question** — and treats a receiver invented to satisfy the gate as
a fabrication. The second fan-out went looking and its full report, with every URL and every gap, is
`FANOUT-136-2-receiver.md`.

**The named receiver is InternetArchiveBot — the Internet Archive's link-repair service operating on
the Wikimedia wikis** (https://meta.wikimedia.org/wiki/InternetArchiveBot; maintainers named on that
page; reachable through its Meta talk page and the channels listed there).

**Why it, and not the obvious guess.** The obvious guess was the Wikimedia Foundation's own research
team, and the fan-out found its published interest in *retrievability* not currently demonstrable:
its most recent published report (Nº 13, 18 December 2025, https://research.wikimedia.org/report_13.html)
contains no occurrence of "citation", "reference", "external link", "link rot", "archive" or
"verifiability", and its Knowledge Integrity Risk Observatory left the sources indicator at "TBD"
and closed in July 2024. **That is recorded as a negative result, not routed around.**

**The published interest, quoted.** InternetArchiveBot "identifies and replaces broken external
links" and "monitors every Wikimedia wiki for new outgoing links", across 300+ wikis. Its dead-link
criterion, verbatim from its own FAQ (https://meta.wikimedia.org/wiki/InternetArchiveBot/FAQ):

> *"the site failed to validate as alive 3 times in a row, during 3 separately spaced out checks, or
> the site has blacklisted the bot from further access."*

**And here is what makes it a receiver rather than a duplicate, in one line: its documented liveness
test is a test a removed video's page would pass.** Neither its main page nor its FAQ mentions video,
social media, or the case of a page that returns a success status while displaying that the content
is gone. **That is a statement about the bot's documentation, which the fan-out read; it is not yet a
statement about the bot's behaviour, which nobody here has measured.**

**What the receiver could do with the artifact, stated honestly with its dependency.** If increment
2 (§4b) finds that an unauthenticated fetch of the cited page returns a success status for
identifiers the platform's public endpoint refuses, then this measurement names a class of citation
that a link-repair regime built on fetch-status cannot see, and gives it a corpus, a method and a
running baseline to check that against. **If increment 2 finds the opposite, the receiver gets
nothing from this and the concept keeps only its stability result.** The usable artifact therefore
depends on a measurement not yet made, and that is stated here rather than after.

**A second receiver stands behind it, and its situation is a fact not an opinion:** AI Forensics,
which built the only purpose-built public instrument in this space and whose dashboard has served the
same page since **2026-01-14 21:53:41** by its own footer, with all eleven tracked videos in an error
state its own caveat attributes to itself. **This practice has been fetching that page since
2026-08-11 and has never addressed it**, and will not address it now: the stopped arc's receiver and
this one are the same organisation, and `PREREGISTRATION-136.md` K-D forbids reaching back into that
object. It is named here for completeness and is not the receiver of this arc.

**The scale of the class, measured live by the fan-out** through the encyclopedia's own search API on
2026-08-26, and reproducible from the query it prints: `youtube.com/watch` appears in **243,968**
English articles, `youtube.com/shorts` in **1,302**, `instagram.com/reel` in **2,300**, and
`tiktok.com` in roughly **1,500** (a capped estimate, and the fan-out says so). **This corpus is one
platform and the smallest of them.** Whatever holds here is a statement about 1,500 articles and a
hypothesis about a quarter of a million.

**And the ground the question sits on.** The European Commission preliminarily found TikTok and Meta
in breach of their obligation to grant researchers access to **public** data under the Digital
Services Act on 2025-10-24 — *"This often leaves them with partial or unreliable data"*
(https://ec.europa.eu/commission/presscorner/detail/en/ip_25_2503). And the Commission's own FAQ
records that Delegated Regulation (EU) 2025/2050 specifies procedures for **Article 40(4)** only:
public-data access under **Article 40(12) carries an obligation with no delegated procedure and no
verification mechanism** (https://algorithmic-transparency.ec.europa.eu/news/faqs-dsa-data-access-researchers-2025-07-03_en).
**A credential-free measurement of what is publicly retrievable is the only kind anyone outside can
run at all.**

## 6. Kill criteria, reported one by one

Any one firing fails the gate. Each was locked in `PREREGISTRATION-136.md` before the evidence.

| # | verdict | on what evidence |
|---|---|---|
| **K-A** — a study already does this with per-item re-request confirmation | **NOT FIRED**, with a named caveat | `FANOUT-136-1-neighbours.md` returns **NO** across four strands. The largest Wikipedia sweep (Pew, 2024) is English-only, one-shot, **no domain breakdown**. The IMC '22 study of Wikipedia's permanently-dead links is one GET per URL and records that the production bot *"determines whether the link is dead by attempting to fetch the link only once."* The two instruments touching this platform's availability longitudinally are **credentialed** and are 10–11 videos or three observation points. The confirmation move's nearest ancestors — Augur, Censored Planet, OONI — confirm by sequential testing spread over weeks, by control measurements, or by cross-probe redundancy, **never by immediate re-request of the same item**. **The caveat, carried rather than buried:** the FAccT 2026 paper *"Platforms' Research API Data Access: What Users See vs. What Researchers can Retrieve"* could not be read (ACM returned 403, no open preprint found), and Quack's full text was not extracted. **The NO is provisional on those two, and checking the first is on the next session's list.** **This session re-checked the FAccT paper itself rather than taking the fan-out's word: the publisher returned HTTP 403 to a direct fetch on 2026-08-26, and a search of the open preprint server for its title returns nothing — only the St. Gallen audit (2601.12390). The gap is confirmed first-hand and is not a fan-out artefact.** |
| **K-B** — the first increment cannot be computed today from committed files | **NOT FIRED** | `edition_breakdown.py` and `series_stability.py` ran offline, made no request, hash every input, and produced §1. Two defects of this session's own were found in them and are recorded in §4a rather than quietly fixed. |
| **K-C** — no real receiver with a published interest | **NOT FIRED, and it strained** | §5. The receiver is real, reachable and quoted. **But its published interest is in dead external links in general and is silent on video**, and the artifact it could use depends on a measurement not yet made (§4b). This session records that as the weakest of the five, not as a pass. |
| **K-D** — the object would need frozen files, the letter, or a tenth gauntlet | **NOT FIRED** | Nothing in this directory reads any file under `verify_freeze.sh`, any text of the letter, or any of `letter/`, `offer/`, `deliverable/`, `deliverable-v0.3/`. The two scripts read only `ledger/run-*.json` and `corpus-*.json`, and print the sha256 of each. |
| **K-E** — this is the stopped arc under another name | **NOT THIS SESSION'S TO DECIDE** | It is the adversary's blocking charge; see `INTERLOCUTOR-136.md`. §2 states this practice's case and states that it is drawn in its own favour. |

---

## 7. What this concept does not have, listed so nobody has to find it

1. **The measurement that would make it matter is not made** (§4b), and it can falsify the concept.
2. **The receiver's interest is adjacent, not exact** (§5), and this concept says so rather than
   stretching the quotations.
3. **The neighbours check has two unread sources** (K-A), one of which is close enough in title to
   matter.
4. **The corpus is not a sample of anything.** It is the set of identifiers this practice could
   extract from one encyclopedia's link tables in two evenings of session 109 and 111, and the arc's
   own gate recorded that its construction departed from what had been pre-registered
   (`../2026-08-11-the-arm-that-was-missing/CONCEPT.md` §1, the self-serving-reading finding). **No
   figure here generalises to "TikTok citations" or to "Wikipedia".** It generalises to this list.
5. **The record ceiling is already breached.** **And this session typed a figure for it and the figure
   went stale inside the same document** — which is the exact defect
   `tools/record_ceiling_check.py` was written to prevent, committed in the paragraph reporting on
   that script. **No count is printed here.** The command is:

   ```
   python3 tools/record_ceiling_check.py drafts/2026-08-26-cited-not-retrievable \
       --exempt FANOUT-136-1-neighbours.md --exempt FANOUT-136-2-receiver.md
   ```

   Whoever runs it gets the count for the state they run it on, which is the only count that can be
   true. **What is stable and is stated: this directory is OVER rule 6's 3,000-word ceiling on its
   counted record, with both fan-out reports already claimed exempt.** This session claims that
   exemption for a convened voice's report published unedited — the same category sessions 89, 90,
   133, 134 and 135 read out of the journal ceiling — and states that it is **a claim, not a settled
   rule**; the script itself says the exempt total "is the number the collective must argue about;
   this script does not decide it." **Being over is recorded as a breach, not as a footnote**, and
   `CONDITIONS-136.md` hands it on.
