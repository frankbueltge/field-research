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
| apparent disappearances **refuted by the instrument's own five-fold re-request**, whole series | **6 of 16** (`../2026-08-11-the-arm-that-was-missing/confirmation-record-121.json`) |

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
   (`CONDITIONS-132.md` item 5). **No trend is claimed here and no test is scored.**
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

*(§5 and §6.K-A are completed from this session's two independent search fan-outs; see
`FANOUT-136-*.md` in this directory, published unedited.)*

## 6. Kill criteria, reported one by one

*(Completed below once the fan-outs land; each criterion is reported as FIRED or NOT FIRED with the
evidence, and any one firing fails the gate.)*
