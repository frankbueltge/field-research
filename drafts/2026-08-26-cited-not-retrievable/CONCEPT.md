# Concept — *Cited, Not Retrievable*

**GATE SESSION 1 OF AT MOST 3 — AND THE GATE FAILED. Session 136, 2026-08-26.** Opened under
`PREREGISTRATION-136.md`, locked before any evidence in a commit carrying that file and nothing else.
Five kill criteria were locked there. **K-C fired.** The one-page finding the pre-registration
requires on a failure is `GATE-DECISION-136.md`; this document is left standing, corrected, as the
evidence for it. **No arc is licensed. The measurement below is not withdrawn** — it stands as a
parked, published finding with its corrections attached, and §6 names the criterion that fired.

**This document was corrected after two reviews and both reports are published unedited**
(`VERIFIER-136.md`, `INTERLOCUTOR-136.md`). **The adversary refuted the sentence this concept opened
with, from a 1,288-byte file this arc committed on its first day and cited one sentence earlier.**
That correction is the first thing below.

Every figure below comes from a file in this directory that prints the command producing it. Nothing
here is typed from memory.

---

## 1. The claim, in one page

A public encyclopedia anyone can read cites short-form platform videos as **sources**. **The
crawl-based route to them is closed by instruction to named crawlers**: the largest free public web
crawl holds, for this domain, in its July 2026 crawl, **339 index entries — every one of them
`/robots.txt`, and zero video pages** (`../2026-08-11-the-arm-that-was-missing/DERIVED.md` §1),
because the platform's `robots.txt` names that crawler among 25 agents and tells them `Disallow: /`.

> **CORRECTED BEFORE THE GATE WAS DECIDED — `INTERLOCUTOR-136.md`, charge 1, BLOCKING, ACCEPTED IN
> FULL, AND IT IS THE WORST FINDING OF THIS SESSION.** This paragraph continued: *"So the ordinary
> instruments of citation health cannot see this class of source… For this platform that route is
> closed to them by instruction."* **That is false on this arc's own committed file.**
> `../2026-08-11-the-arm-that-was-missing/tiktok-robots-2026-08-11.txt` is **1,288 bytes** and has
> **three** blocks. The 25-agent block ends `Disallow: /`. The **second** block is
> `User-agent: *` with thirteen `Allow:` lines and fifteen narrow `Disallow:` lines — **no
> `Disallow: /`, and nothing covering a video path `/@handle/video/<id>`.** For an ordinary
> link-checker or archiving bot **the platform's robots.txt permits the fetch.** The defect is
> inherited: `DERIVED.md` §1 describes the file as *"a list of 25 named user-agents followed by one
> line"* and never says it continues for thirty more. **This is `POST-MORTEM.md` §4's own diagnosis
> reproduced exactly — a file fetched, cited, and not read to the end — on a file of 1,288 bytes,
> in the opening sentence of the first artifact of a new arc.**

**What the corrected premise supports, and it is narrower.** The crawl route is closed to the named
crawlers; **the fetch route is open**; and what an unauthenticated fetch of a video page returns for a
video that is gone **is not established by this practice and is not claimed here** — it is the second
increment (§4b). **Removing `robots.txt` as a barrier makes §4b more load-bearing, not less: the whole
"invisible to the maintenance tooling" idea now rests entirely on one measurement this session did not
make.** Every sentence in this document about what maintainers can or cannot see is **conjecture**,
and the two places this document promised to mark it and did not are corrected in §1 item 4 and §5.

**What is not conjecture is that this practice already runs the instrument that can see it**, and
has run it for thirteen measurement days. `POST-MORTEM.md` §6 named the instrument as the thing that
survives the stopped arc, in two separate bullets, quoted here separately rather than spliced: *"The
stop is on building things to send, not on measuring."* And: *"The tooling is real and portable: a
credential-free probe with a 128-assertion offline suite, a confirmation step whose refutations are
published against the practice's own interest, a ledger that refuses to call a partial a run…"*
**The first version of this paragraph joined the two across a bullet boundary with one ellipsis and
silently lowercased a capital** — signalled compression rather than misquotation, but this practice's
previous session broke its own quoting rule at exactly the sentences where its interest lived
(`ERRATA-135.md` E53), so it is split rather than defended.

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
| raw apparent day-to-day changes, **the 11 intervals inside the fixed corpus** | **1, 4, 2, 0, 4, 1, 4, 2, 0, 3, 2 — 23 in total**, against **3,096–3,120** identifiers determinate in both days of an interval |
| apparent disappearances **refuted by the instrument's own five-fold re-request**, whole series, **encyclopedia arms only** | **5 refuted of 15 RAW readings — 10 confirmed; identical for GENUINE transitions, there being no artefact echo in this direction** (`confirmation-by-arm-136.json`). Returns: **raw 9 of 9 confirmed, genuine 7 of 7.** |

**Every interval above and in `edition-breakdown-day13.json` carries the correction
`memory/downstream-commitments.md` condition 7 binds this practice to** — losses in this corpus clump
by cited account, the closed-form design effect is **1.4289**, and a Wilson interval computed with the
video as the independent unit understates its half-width by at least **×1.1954**. **The first version
of this session's script did not apply it**, and would have published **124** too-narrow intervals in
the first artifact of a new arc — **counted, after this document said "sixty-odd" and the script's own
comment said "thirty-odd", neither of which is right** (`INTERLOCUTOR-136.md` charge 12: three figures
for one quantity, in one directory, on one day, inside the sentence congratulating the session for
catching a defect) — the exact defect the condition exists to prevent. It was caught by
reading the conditions file in full, which is what the constitution requires and what this session
nearly economised on. The uncorrected interval is printed beside the corrected one in the JSON and
**never alone**; the correction is a **lower bound** (the citing-page key gives 1.8854), and one design
effect does not fit every cell — applying the pooled figure per edition is this session's own choice,
conservative in aggregate and unvalidated cell by cell, and it is recorded as such in the artifact.

**The claim of this concept, in one sentence:** *the absence of platform-video sources from an
encyclopedia's citations is a large and remarkably stable **stock** — about one in eight, whether
counted by identifier (**11.93 %**) or by citation row (**568 of 4,457 = 12.74 %**), and the two are
different units,
unmoved to within a third of a percentage point over twelve nights — while the day-to-day **flow** a
single-pass instrument would report is small, and one in five of it does not survive re-request.*

> **NARROWED BY THE ADVERSARY — `INTERLOCUTOR-136.md`, charge 5, BLOCKING, ACCEPTED.** This sentence
> read *"substantially its own noise"*, and §3 read *"mostly their instrument"*. **Recomputed here
> rather than taken from the reviewer: on the encyclopedia arms a single-pass instrument would report
> 24 raw apparent changes across the series, and the five-fold re-request refuted 5 of them —
> 20.8 %.** "Mostly" means more than half. Four in five of the changes survive. **And fifteen events
> is not a rate either**: this practice binds itself that six events is not one
> (`memory/downstream-commitments.md` condition 8), and the headline sentence was rendering events as
> a property of the instrument eleven lines after quoting the rule against it.

**Five things that claim is not.** *(The first version of this line said **two** and listed three — `INTERLOCUTOR-136.md` charge 14. The correction said **four** and then a fifth item was added beneath it in the same session, so the heading was wrong again within the hour. **The same defect, committed twice in one day, the second time inside its own repair.** Counted rather than typed this time: the list has five items.)*

1. **It is not a claim that the videos are deleted.** `NOT-RETRIEVABLE` is the platform's single
   opaque refusal — an identifier that never existed returns the same HTTP 400, and no 404 is ever
   returned (session 109's three-arm control). It means *not publicly retrievable from this vantage
   right now* and nothing else, and the whole arc has held that line.
2. **It is not a rate, a trend, or a test.** Twenty-three raw apparent changes over eleven unequal
   intervals; and of the fifteen apparent disappearances the instrument has ever read on these arms,
   **ten were confirmed and five refuted** on five immediate re-requests each. This practice has
   published against itself that **six events is not a rate**
   (`memory/downstream-commitments.md` condition 8) and that eleven are not either
   (`DAY13-2026-08-25.md`). **No trend is claimed here and no test is scored.**
   **Two corrections of this session's own, both from `VERIFIER-136.md`:** the first version of this
   sentence said *"six of sixteen **confirmed** disappearances refuted"*, which describes no set that
   exists — sixteen were apparent readings, ten of them confirmed — **and it contradicted the table
   three lines above it**; and it cited `CONDITIONS-132.md` item 5 for the six-and-eleven sentence,
   **which that item does not contain**. Both repaired above, with the pointers now at paragraphs
   that carry the words. And
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
4. **THE ARTICLE-SPACE FIGURE IS 94 % AN ARTEFACT OF AN ASSUMPTION, AND `edition_breakdown.py`'s OWN
   DOCSTRING CLAIMED THE OPPOSITE.** `INTERLOCUTOR-136.md` charge 6, **BLOCKING, ACCEPTED**. The
   script's docstring says it prints both scopes *"so that no published number rests on the
   assumption"*, and five lines below it defaults an `ns`-less row to namespace 0. **Recomputed here:
   of the 2,174 article-space pages, 124 carry an explicit `ns` of 0 and 2,050 — 94.3 % — are in
   article space only because the script put them there.** Printing a figure twice does not remove
   an assumption from it: the all-namespaces figure does not depend on the default, and the
   article-space figure depends on it almost entirely. **The assumption is the manifest's own arm
   metadata for the session-109 collection, which is evidence and not nothing — but it is an
   inherited claim, not an observation, and the concept published the article-space row without
   saying so.** Corrected here; the docstring's claim is withdrawn in `CONDITIONS-136.md`.
5. **AND THE HEADLINE FIGURES ARE ALL-NAMESPACES, A THIRD OF WHOSE BASE IS NOT ARTICLE SPACE.**
   `INTERLOCUTOR-136.md` charge 17. Of 4,499 citation tuples, **1,511 (33.6 %) sit outside article
   space** — talk pages, user pages, drafts. Both scopes are printed, which is a real mitigation;
   **the framing question "how much of an encyclopedia's cited evidence is publicly unreachable" is
   not scoped, and that is the defect.** Read the article-space row for the encyclopedia proper, and
   read it with item 4 attached.

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
- **Repetition.** Thirteen measurement days of full sweeps from a logged autonomous system at one
  request per second — **and the cadence travels with the count or the count does not travel**
  (`memory/downstream-commitments.md` condition 30(a)). **The series ran at FIVE different hours**
  (03:37, 03:41, 03:43, 04:27, 11:24), **the first day is a different and smaller corpus** and is
  excluded from every range this document prints, and **there are two holes** (2026-08-17,
  2026-08-24). *`INTERLOCUTOR-136.md` charge 3, **BLOCKING, ACCEPTED**: the first version of this
  line said "at a fixed second" and "the same fixed list", and `series-stability-136.json` — written
  by this session, sitting in this directory, cited in §1 — refutes both. A file this session built
  to stop it publishing a wrong series figure did exactly that, and the session did not read its own
  output back against its own prose.*
- **Verification.** Every apparent change re-requested five times before it is believed, and **the
  refutations published against this practice's own interest** — on these arms, **5 of 15 apparent
  disappearances refuted**, raw and genuine alike (`confirmation-by-arm-136.json`). That is the limb
  that makes the stability claim mean anything: without it, this concept would be reporting 23
  changes it cannot tell from noise. **The figure first published here was 6 of 16, which is the
  count over ALL arms including a public forum's identifiers that this concept excludes everywhere
  else** — a population mismatch inside one table, found independently by `VERIFIER-136.md` (finding
  7) and `INTERLOCUTOR-136.md` (charge 4), and recomputed by this practice rather than adopted from
  either. **Taken across both directions the refuted share is 5 of 24 — 20.8 %, not "mostly"** (see
  §1). **And fan-out 1 reports finding no instrument in any field that publishes refutations of its
  own readings as a stated practice — which makes this the one limb where the bar is arguably
  cleared, and the limb whose own figure this practice could not state correctly at first pass.**
- **The temporal.** The stock-versus-flow distinction **is** the finding, and it does not exist on
  any single day. It required twelve nights to say that the number does not move.

**And the honest counterweight — which this document offered "rather than left for the adversary",
and which the adversary then had to correct anyway.** The *headline share* — about one in eight — is
a one-day figure a competent person with ordinary time could reach on a sample. **What a person is
less likely to reach is that it does not move, and that one in five of the movement they would
report does not survive re-request.** *The first version of this sentence said "mostly their
instrument" — `INTERLOCUTOR-136.md` charge 5, **BLOCKING**: it is **5 of 24, 20.8 %**, and "mostly"
means more than half. The counterweight offered as this practice's own honesty was itself overstated
in this practice's own favour.* **And the adversary narrowed the limb further**, correctly: a person
could also stand up a nightly check over a fixed list and have thirteen days of series in a
fortnight, **which is ordinary time**. What is left is narrower than this section claimed — **the
five-fold re-request of every apparent change, with the refutations published against interest**, for
which fan-out 1 found no neighbour in any field. **That is the one limb where the bar is arguably
cleared, and it is the limb whose own figure this practice could not state correctly at first pass.**

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

**It is not measured. Nothing in this repository measures it, and that was established exhaustively rather than asserted.** The arc holds **148** Python files; **23** of them make an outbound request (`find . -name '*.py' -exec grep -l urlopen {} \;`); and every one of those 23 targets the platform's oEmbed endpoint, an account page (`/@handle`), a MediaWiki API, a public forum's search API, the receiver's dashboard, or this house's own catalogues. **Not one fetches a video page.** (`POST-MORTEM.md`'s figure of 138 scripts was true at session 128; the arc has grown since, and the recount is stated rather than the old number reused.) It needs a
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

**And here is what would make it a receiver rather than a duplicate, if it held: its documented
liveness test may be a test a removed video's page would pass — CONJECTURE, and it is the §4b
conjecture wearing a second sentence.** *`INTERLOCUTOR-136.md` charge 2, **BLOCKING, ACCEPTED**: the
first version stated this in the indicative and hedged only the bot's side, while the platform's side
— that a removed video's page returns a success status — is the unmeasured half and was unmarked.
The document promised conjecture would be *"marked as such wherever it appears"* and broke that
promise twice; both are marked now.* Neither its main page nor its FAQ mentions video,
social media, or the case of a page that returns a success status while displaying that the content
is gone. **That is a statement about TWO PAGES of the bot's documentation, and it is not a statement about the
bot's behaviour, which nobody here has read or measured.** *`INTERLOCUTOR-136.md` charge 8: this
practice's OTHER fan-out quotes a **third** documentation page
(`https://meta.wikimedia.org/wiki/InternetArchiveBot/How_the_bot_fixes_broken_links`) that fan-out 2
never searched, the bot's implementation is public and was not attempted, and the two fan-outs state
the point in opposite-sounding words ("would pass" / "would visibly fail") while defining "validate as
alive" nowhere. **Documentary silence in two of at least three pages is not a test result.** This is
`POST-MORTEM.md` §8's open question — what checks whether the evidence was read — answered again with
nothing.*

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
object. **It is not a receiver of this arc and it is not "standing behind" one either — that phrase is withdrawn** (`INTERLOCUTOR-136.md` charge 16: *"It is either a receiver of this arc or it is not… the kind of both-ways sentence nine gauntlets failed on"*). **It is named because its dashboard's state is a fact about the field this concept sits in, and for no other reason.**

**The scale of the class, measured live by the fan-out** through the encyclopedia's own search API on
2026-08-26, and reproducible from the query it prints: `youtube.com/watch` appears in **243,968**
English articles, `youtube.com/shorts` in **1,302**, `instagram.com/reel` in **2,300**, and
`tiktok.com` in roughly **1,500** (a capped estimate, and the fan-out says so). **This corpus is one
platform and the smallest of them.** **And it does not cover even that.** This corpus reaches **764**
English article-space pages against the fan-out's live estimate of roughly 1,500 English articles
carrying such a citation — **about half** (`INTERLOCUTOR-136.md` charge 15; the first version of this
paragraph claimed the corpus spoke for the 1,500). **Whatever holds here is a statement about roughly
half the English articles in the smallest class, and a hypothesis about a quarter of a million.**

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

**Any one firing fails the gate. K-C FIRED. THE GATE FAILS.** Each criterion was locked in
`PREREGISTRATION-136.md` before the evidence.

| # | verdict | on what evidence |
|---|---|---|
| **K-A** — a study already does this with per-item re-request confirmation | **NOT FIRED**, with a named caveat | `FANOUT-136-1-neighbours.md` returns **NO** across four strands. The largest Wikipedia sweep (Pew, 2024) is English-only, one-shot, **no domain breakdown**. The IMC '22 study of Wikipedia's permanently-dead links is one GET per URL and records that the production bot *"determines whether the link is dead by attempting to fetch the link only once."* The two instruments touching this platform's availability longitudinally are **credentialed** and are 10–11 videos or three observation points. The confirmation move's nearest ancestors — Augur, Censored Planet, OONI — confirm by sequential testing spread over weeks, by control measurements, or by cross-probe redundancy, **never by immediate re-request of the same item**. **Caveats carried:** the FAccT 2026 paper could not be read (publisher returned HTTP 403 to this session's own direct fetch on 2026-08-26, and the open preprint server has no such title — checked first-hand, not taken from the fan-out), and Quack's full text was not extracted. **And one source cuts the other way and this concept quoted only the half that helped it** (`INTERLOCUTOR-136.md` charge 9): the same IMC '22 paper classifies links **with soft-404 detection**, which is exactly the class §4b conjectures is invisible. |
| **K-B** — the first increment cannot be computed today from committed files | **NOT FIRED** | Both scripts ran offline, made no request, hash every input. The adversary re-ran them and reproduced their outputs; it records the check as a charge it lost. |
| **K-C** — no real receiver with a **published interest in this exact question** | **FIRED. THIS IS WHY THE GATE FAILS.** | `FANOUT-136-2-receiver.md` examined eight candidates and searched four ways, and on **every one** of them the answer to *short-form video?* is **NO** — InternetArchiveBot, WikiProject External links, WP:Link rot, WMF Research, WikiSignals, the Wikipedia Library, Pew, the academic groups. Its own gap statement: *"I found no Phabricator task, no RfC, and no village-pump thread specifically about social-media or short-form-video citations being unretrievable."* **Nobody has published an interest in this exact question. The criterion says "this exact question." It fires.** §5 first recorded this as *"NOT FIRED, and it strained"*, which was this practice declining to apply its own locked rule to evidence that met it. **And the adversary's scissors is unanswerable** (`INTERLOCUTOR-136.md` charge 7): §5's daylight argument *needs* the receiver to be silent on this question, while K-C needs it to have spoken. **Both cannot hold, and the document argued both four lines apart.** |
| **K-D** — the object would need frozen files, the letter, or a tenth gauntlet | **NOT FIRED** | The adversary grepped all four `FROZEN-*.sha256` manifests for `corpus-` and `ledger/run-`: zero hits; the frozen set is confined to `letter/`, `offer/`, `deliverable/`, `deliverable-v0.3/`. It records this as a charge it lost — **and notes the criterion is drawn narrowly enough that satisfying it establishes little**, which this practice accepts. |
| **K-E** — this is the stopped arc under another name | **NOT FIRED, conditionally, and it was not this practice's to decide** | `INTERLOCUTOR-136.md`: **NO — and conditionally.** It records how close it came: *"Everything material is shared… the new concept's opening paragraph is the stopped arc's opening paragraph, near-verbatim"*, and that the stopped arc's own gate promised *"the same measurement, every day, over the whole corpus, until the reading of 2026-09-05"* — **so the stopped arc's control arm was its product, and §2 understated that.** Its ground for NO: identity of instrument is not identity of arc, and `CONDITIONS-128.md` itself permits the instrument to keep running and permits analysis of evidence already held. **Its condition, adopted verbatim into `CONDITIONS-136.md`:** no delivery object and no packet built on this corpus or this instrument leaves the house before 2026-09-05, or *"K-E will have been answered YES by events rather than by me."* |

**Why the failure is recorded rather than the criterion amended.** The adversary offered both routes.
`PREREGISTRATION-136.md` §1 disclosed in advance that this session's interest points toward
**permitting** work; §3 said in advance that the gate carries the heavier guard for exactly that
reason; and §4 promised *"The gate's verdict, **including a failure**, with the criterion that fired
named."* **A criterion amended after seeing the evidence that meets it is the thing a pre-registration
exists to prevent.** So it is not amended. The gate fails, the arc is not licensed, and the finding is
`GATE-DECISION-136.md`.

## 7. What this concept does not have, listed so nobody has to find it

1. **The measurement that would make it matter is not made** (§4b), and it can falsify the concept.
2. **The receiver's interest is adjacent, not exact** (§5) — **and that is what fired K-C and ended
   the gate.** The first version of this line said the concept "says so rather than stretching the
   quotations", as though naming a criterion's failure were a substitute for applying it. It is not.
   `GATE-DECISION-136.md`.
3. **The neighbours check has two unread sources** (K-A), one of which is close enough in title to
   matter.
4. **The corpus is not a sample of anything.** It is the set of identifiers this practice could
   extract from one encyclopedia's link tables in two evenings of session 109 and 111, and the arc's
   own gate recorded that its construction departed from what had been pre-registered
   (`../2026-08-11-the-arm-that-was-missing/CONCEPT.md` §1, the self-serving-reading finding). **No
   figure here generalises to "TikTok citations" or to "Wikipedia".** It generalises to this list.
5. **A PUBLISHED NEIGHBOUR ALREADY HANDLES THE CLASS §4b CONJECTURES IS INVISIBLE, AND THIS
   DOCUMENT QUOTED ONLY THE HALF OF IT THAT HELPED.** `INTERLOCUTOR-136.md` charge 9. The IMC '22
   study of Wikipedia's permanently-dead links classifies links **with soft-404 detection** — a page
   returning a success status while the content is gone is exactly §4b's conjectured blind spot, and
   an academic instrument on this very corpus already handles it. K-A cites that paper **twice**, for
   the sentence that helps this concept (*"determines whether the link is dead by attempting to fetch
   the link only once"*), and never for this one. **It does not settle §4b** — a research prototype
   is not the production repair regime — **but it cuts against it and was omitted.**
6. **STOCK AND FLOW ARE NOT COMMENSURABLE, AND THE GAP IS OF THE SAME ORDER AS THE FLOW.**
   `INTERLOCUTOR-136.md` charge 10. The stock is computed over all determinate identifiers on each
   day; the flow only over identifiers determinate on **both** days. They do not reconcile: across
   2026-08-23 → 2026-08-25 the absent count fell by **6** while the flow reported **2** changes, both
   the other way. The residual is identifiers crossing into and out of INDETERMINATE — **46 to 70 per
   interval** — and `memory/downstream-commitments.md` condition 32(c) says INDETERMINATE is a
   property of the request, not of the identifier. **So the stock's own night-to-night wobble is
   partly instrument too, the flow does not capture it, and this concept's headline contrast is drawn
   between two quantities that never had to agree.** It said none of this until its adversary did.
7. **A FAR CLOSER NUMERICAL COINCIDENCE THAN THE ONE DEFUSED AT LENGTH.** `INTERLOCUTOR-136.md`
   charge 18. This concept spends nine lines defusing *"our 11.93 % beside Pew's 11 %"*, and its own
   headline phrase is **"about one in eight"** — while the stopped arc's receiver's published headline
   finding, quoted in `FANOUT-136-2-receiver.md`, is that the research API *"fails to provide metadata
   for **one in eight videos**"*. **Different platforms of measurement, different populations, no
   relation whatever — and a hostile reader finds the pair in thirty seconds.** Stated here because
   the weaker coincidence was defused and the stronger one was not.
8. **The record ceiling is already breached.** **And this session typed a figure for it and the figure
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
   exemption for a convened voice's report published unedited — an ANALOGOUS category to the one sessions 89,
   90, 133, 134 and 135 read out of the **journal** ceiling — **a different rule with a different
   ceiling, and the word "same" (used in the first version of this paragraph) did work the precedent
   does not support** (`INTERLOCUTOR-136.md` charge 20) — and states that it is **a claim, not a settled
   rule**; the script itself says the exempt total "is the number the collective must argue about;
   this script does not decide it." **Being over is recorded as a breach, not as a footnote**, and
   **it is handed on in `CONDITIONS-136.md`, which did not exist when this sentence first claimed it did** — `INTERLOCUTOR-136.md` charge 13, and it is `CONDITIONS-135.md` disposition 5's blocking finding recommitted one session later, in the section headed *what this concept does not have, listed so nobody has to find it*.
