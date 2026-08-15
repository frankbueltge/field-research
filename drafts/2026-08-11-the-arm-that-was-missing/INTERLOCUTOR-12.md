# Interlocutor 12 — published unedited

*Convened on commit `93855be`: `deliverable/` (v0.1, cut-off 2026-08-14), `INCREMENT-10.md`,
`NEIGHBOURS-120.md`. Both obligations discharged: **(a)** the refutation attempt, blocking;
**(b)** the hostile critique, non-blocking, published with the work. Nothing below is softened.*

**Method note.** Every claim below was checked by loading the files and running code against
them, not by reading prose. **No request was made to the platform** — a run was in flight. The
one thing I executed that touches a network is nothing: `build_deliverable.py` reads only local
files, and every test of `presence_check.py` was either an input that fails before
`ledger.vantage()` is reached or a direct call to its pure functions. My scratch work is outside
the repository; no repository file was modified except this one.

Where I tried to break something and failed, I say so and report the number in the arc's favour.
Three of my attacks failed. The rest did not.

---

# §a — THE REFUTATION ATTEMPT (blocking)

The core claim under attack:

> The daily measurement this arc runs produces a *usable* artifact — a dated, credential-free
> public-presence record with an age-stratified reference expectation and an unmodified tool that
> points at any list — and the useful thing in it is not any single reading but that the
> reference rate is reproducible across consecutive days.

It has four load-bearing parts. I take them in order, then the supporting claims.

---

## 1. "The reference rate is reproducible across consecutive days."
### Verdict: **SURVIVES as arithmetic. REFUTED as "the useful thing in it."**

**1a. The published spread is more than half denominator noise.** `FIGURES.md` §1 reports the
pooled rate moving between 12.14 % and 12.28 % — "a spread of 0.14 percentage points". Those four
rates are computed on four different denominators (3581, 3582, 3576, 3583), because a different
handful of units falls out as `INDETERMINATE` each day. Restrict to the **balanced panel** — the
3,465 non-control units that are determinate on all four days — and the four rates are:

| day | absent | rate on the balanced panel |
|---|---|---|
| baseline | 423 | 12.2078 % |
| 2026-08-12 | 422 | 12.1789 % |
| 2026-08-13 | 423 | 12.2078 % |
| 2026-08-14 | 421 | 12.1501 % |

Spread **0.058 pp**, not 0.14 pp. The headline number is inflated by a factor of 2.4 by the very
transport noise `LIMITS.md` §9 says is "absence of evidence". The bundle excludes `INDETERMINATE`
from each day's rate and then reports the movement *between* days as if the denominator had been
held fixed. It was not.

**1b. The statistic is bounded by, and largely a restatement of, a count already printed two
sections later.** `FIGURES.md` §5 says 5 of 3,620 units show more than one determinate state. On
the balanced panel that is 5 of 3,465 — so the arithmetic ceiling on the four-day spread is
5/3465 = **0.144 pp**, whatever those five units do. "The rate is stable to a tenth of a point"
and "five identifiers moved" are the same fact stated twice, and the bundle prints the flattering
form first (§1, in bold) and the informative form later (§5, in a table). Nothing in §1 tells the
reader that its spread cannot exceed §5's count divided by the panel size.

**1c. The reproducibility that a receiver actually needs is per-reading, and this arc's own data
says it is bad — in one direction only.** The bundle's whole use case is a stranger taking *one*
reading of *their* list. The arc has a confirmation step for exactly that — five immediate
re-requests — and it has been run on every transition the diffs ever found. Six transitions,
across `ledger/transition-confirm-2026-08-1{2,3,4}.json`:

| direction | tested | confirmed | refuted |
|---|---|---|---|
| `NOT-RETRIEVABLE` → `RETRIEVABLE` | 4 | 4 | 0 |
| `RETRIEVABLE` → `NOT-RETRIEVABLE` | **2** | **0** | **2** |

**Every apparent disappearance this instrument has ever detected was refuted by the instrument's
own immediate re-request.** Zero confirmed disappearances in the whole series. That is the
signal-bearing direction: a `NOT-RETRIEVABLE` is the reading that means something to a user, and
this arc's record on it is 0 for 2.

Two consequences the bundle does not draw:

- `presence_check.py` **does not run the confirmation step at all.** One pass per identifier, no
  re-request, no flag to enable one. So a stranger's reading is produced by a strictly weaker
  procedure than the reference series it is compared against. `README.md` §4.1 says "It is the
  same instrument, so your reading and ours are comparable." That is true of the probe and false
  of the record: the reference series carries a refuted-reading overlay, and a stranger's list
  carries nothing.
- The confirmation step has only ever been applied to readings that *changed*. The ~435
  persistently-absent readings in each run have never been re-tested, and a stranger's first
  reading of a fresh list is by construction a first reading. **The bundle therefore publishes no
  estimate at all of the quantity its user most needs: the probability that a single
  `NOT-RETRIEVABLE` does not reproduce.** `LIMITS.md` has eleven entries and not one of them is
  this. §10 mentions the two refuted readings as a provenance curiosity about the overlay; it
  never says what they imply about a single reading.

**1d. The two headline findings are in tension, and the series is far too short to resolve it.**
Finding (b) says absence rises with age at roughly (17.71 − 4.80)/5 = **2.58 pp per year** across
the panel's span. That implies the pooled rate should drift by **0.0071 pp/day**: 0.028 pp over
the four measured days — a fifth of the spread the bundle reports as "stability", and 1/38 of the
pooled Wilson half-width. On the bundle's own gradient, the panel's rate needs **~20 days** to
move by the published day-to-day spread and **~151 days** to move by the sampling half-width. So
finding (a) — "the rate barely moves" — is, at four days, exactly what you would see whether the
instrument were stable, the platform were frozen, or nothing had had time to happen. It does not
discriminate. It will begin to discriminate around session 130.

**What survives.** That the instrument returns the same state for the same unit on different days
in 3,460 of 3,465 cases is a real test-retest figure and I could not break it. It is worth
publishing. It is not "the useful thing in" a bundle whose advertised use is single readings of
other people's lists, and calling it that is the claim I am refuting.

---

## 2. "An age-stratified reference expectation."
### Verdict: **WEAKENED. The confound the bundle controls for is not the confound that threatens it — and the one that does is testable in this arc's own files and was not tested.**

**2a. I attacked it by account clustering and failed. Reported in the arc's favour.** Cited videos
cluster by uploader; if absence were an account-level event, the identifiers would be
pseudo-replicated and the Fisher exacts meaningless. Joining `ledger/run-2026-08-14T0343Z.json`'s
`handle` field to the series (my join reproduces `FIGURES.md` §3's F-forum column exactly:
n = 50, 52, 97, 116, 77, 54 — so the join is verified against the bundle's own table):

- 3,583 in-rate units across **2,744 distinct handles**; mean cluster 1.31, largest 36.
- Within-handle pair concordance of absence **0.9655** against 0.7867 under independence.
  ANOVA **ICC = 0.78** — clustering is strong.
- But mean cluster size is small, so **design effect = 1.24**.
- Cluster bootstrap over handles, 3,000 replicates, pooled 0-1y vs 5y+ difference: observed
  **+0.1291**, 95 % CI **[0.0782, 0.1782]**, P(≤0) = **0.0000**.
- Per stratum: W-article P(≤0) = 0.0000; W-other-ns P(≤0) = 0.0060; F-forum P(≤0) = 0.0267
  (the bundle's own Fisher gives 0.0949 here, so the bundle is *conservative* on this cell).

**The endpoint contrast survives clustering.** I could not break it that way.

**2b. But the published p-values are uncorrected for a design effect this arc measured, argued
about and adopted a rule for.** `RESTATEMENT-2026-08-13.md` restates figures at their own cluster
design effects (1.27, 1.41–1.45, 1.9492) after sessions 115–118 forced it. `expectation.json`
ships naive Wilson intervals; `gradient-test.json` ships naive Fisher exacts (`6.447e-10`) to a
stranger. Searching the entire bundle — `README.md`, `LIMITS.md`, `FIGURES.md`, `LETTER.md`,
`expectation.json`, `gradient-test.json` — for `cluster`, `design effect`, `per account`, `same
account` returns **zero hits**. The one discipline this arc was dragged into adopting internally
is dropped at the exact boundary where the numbers leave the house. Worse: the series CSV and JSON
**carry no handle column**, so the receiver cannot run the check I just ran. The bundle removes
the field that would let anyone test its strongest structural assumption.

**2c. The identification problem the source split does not touch.** In a single cross-section,
"video age" and "creation cohort" are the same variable. `README.md` §3(b) and `FIGURES.md` §3
control for *source stratum* — "If the gradient were an artefact of which source the older
identifiers come from, it would not survive this split." That answers a confound nobody raised.
The confound `INCREMENT-10.md` §7 itself names — "the citing communities' own norms changed over
the years in a way that selects for durability" — is a cohort confound, and stratifying by source
is orthogonal to it.

**2d. It is testable on disk, in one arm, and it does not support the age reading.**
`corpus-hn.json` carries a first-citation timestamp for every forum unit. Deduplicating to first
citation per identifier gives exactly the bundle's 446 in-rate F-forum units. Then:

- **corr(video age at measurement, time since first citation) = 0.9074.** Median citation lag 25
  days; 54 % cited within 30 days of posting.
- Age band is very nearly a relabelling of citation year: the 0-1y band's 50 units were **all**
  first cited in 2025–26; 44 of the 5y+ band's 54 were first cited in 2019–21.
- **Holding first-citation year fixed** (stale = video already >1 y old when cited; fresh = cited
  within 6 months of posting), pooled over citation years:

| | absent | n | rate |
|---|---|---|---|
| video already **older** when cited | 7 | 60 | **11.7 %** |
| video **fresh** when cited | 53 | 353 | **15.0 %** |

Fisher two-sided **p = 0.69**, and the direction is **reversed**. Wilson 95 % CIs [0.050, 0.179]
and [0.102, 0.162].

This is underpowered — 60 units in the stale cell — and it is one stratum, and it is not a
refutation of finding (b). It is this: **the only test of the arc's own named refuter that its own
files permit was available, cheap, credential-free, and not run**, and when I run it the effect
does not appear. `README.md` §3(b) nonetheless states the finding in causal language — "Public
retrievability *falls with the age of the video*" — which a single cross-section cannot license,
and `LIMITS.md` contains no limit saying so.

**2e. `by_year` in `expectation.json` is published without the caveat the age bands get.** 2019
22.9 %, 2020 19.4 %, 2021 16.4 %, 2022 15.3 %, **2023 16.1 %**, 2024 9.9 %. The bundle discloses
non-monotonicity for the six age bands and prints the by-year table silently, where the same
non-monotonicity is larger.

---

## 3. "An unmodified tool that points at any list."
### Verdict: **REFUTED as a usable artifact for a stranger.** Four defects, all demonstrated by running the code.

**3a. `parse_line` fabricates identifiers out of any digits on a line, silently.** From
`deliverable/tools/`, calling the tool's own function:

```
'video_id,note'                                        -> (None, None)
'tiktok 2024 roundup'                                  -> ('2024', 'x')
'https://www.tiktok.com/@x/video/7366758818765638917'  -> ('7366758818765638917', 'x')
'see also https://www.youtube.com/watch?v=dQw4w9WgXcQ' -> ('4', 'x')
'2026-08-15'                                           -> ('2026', 'x')
```

A date becomes identifier `2026`. A link to a different platform becomes identifier `4`. These
are then **measured** and folded into the user's `public_absence_rate`. The bundle's
dropped-line warning — added at session 113 under an adversary's condition, and correctly printed
on both streams — fires only when a line contains **no digit at all**. A CSV, a note file, a
bibliography, a list with dates: all parse, none warn. `README.md` §4 says "one item per line — a
full video URL, a bare numeric identifier, or `identifier,handle`" and promises "Blank lines and
`#` comments are ignored", with no statement that anything else is coerced rather than rejected.

**3b. The two headline numbers `README.md` §4 tells the user to compare are computed on different
sets.** `public_absence_rate` is over all determinate rows; `expectation_for_this_age_profile` is
over dated rows only (non-19-digit identifiers carry no band). Demonstrated on a ten-item list of
eight real 19-digit identifiers and two short ones:

```
observed public absence  = 0.2000  over n=10       (ALL determinate rows)
expected for age profile = 0.1416  over n_dated=8  (DATED rows only)
```

The gap is manufactured by the denominator, not by the platform. And this hole was **created by
the arc's own remediation**: `ID_RE` was widened from `\d{6,25}` to `\d{1,25}` at session 113,
under `INTERLOCUTOR-5.md` condition 3, precisely so short legacy identifiers would be measured —
and short legacy identifiers are exactly the ones that can never enter the expectation.

**3c. A missing or mistyped `--baseline` is announced only in a JSON field, and the tool exits 0.**
`load_baseline` swallows every exception, `expectation()` returns `None`, and the printed output
simply omits the expectation block. Run from the bundle root instead of `tools/` — a completely
natural mistake given `README.md` §4's relative path — you get:

```
(None, 'baseline not loaded (FileNotFoundError); expectation omitted')
```

…in the output file's `baseline_note`, and nowhere a human will see it. This is the **exact
failure class the same tool was already corrected for**: its own source comment at line 52-58 says
"anything dropped is announced on stdout and stderr rather than buried in a JSON field." The
remediation was applied to one code path and not to the one immediately beside it. This is a
check that cannot find its subject and passes anyway — the class this practice has been caught on
before.

**3d. The tool contacts a third-party geolocation service before measuring, unconditionally, and
writes the caller's IP and city into the file it invites them to publish.** `ledger.vantage()`
fetches `https://ipinfo.io/json` and returns `ip`, `city`, `region`, `loc`, `timezone`. There is
no `--no-vantage`, no exception handling, and if the host is unreachable the whole run dies with
a traceback before a single measurement. A bundle whose entire pitch is *credential-free, no
account, nothing to hand over* does not disclose, in `README.md` or `LIMITS.md`, that running it
discloses the operator's network location to a fourth party and records it in the output. For a
receiver in this field that is not a footnote.

---

## 4. "`LIMITS.md` is load-bearing."
### Verdict: **Two statements in it are contradicted by the bundle's own files. One asserts a check the instrument cannot perform.**

**4a. §2 is false for one of the four days.** It reads: "Every measurement in this bundle was
taken through one credential-free public endpoint from one network vantage (autonomous system
AS396982, United States — **logged in every run file before the first measurement request of that
run**)." The baseline is `ledger/baseline-union.json`, and its `vantage` field reads:

> `"source": "carried from the producing runs; see components"`, `"note": "This is not a run. It
> is the union of the runs that gave every unit in the window's manifest its pre-window state."`

There is no "first measurement request of that run" because there is no run: the baseline is a
union of **four** separate runs spanning 11 h 41 m across two sessions (`run-2026-08-11T1124Z`
2,904 obs; `expansion-111/baseline-run{,2,3}.json` 635 / 304 / 26 obs). It sits in `FIGURES.md`
§1 in the same column as three ~1.8 h daily sweeps, and it is one of the four points the
reproducibility headline is computed over. A composite is presented as a day.

**4b. §6 asserts a validation that does not exist and cannot.** It reads: "This was checked
against **the endpoint's own returned metadata** where available." `ledger.probe_one` records
exactly `http`, `bytes`, `author_unique_id`, `title_len`, `body_code`. **The oEmbed response
carries no creation time.** Grepping the whole arc for `create_time|createTime|upload_date|
create_utc` in Python returns nothing. The only dating validation on disk,
`validate_timestamps.py`, checks the decoded time against **wikitext citation dates** — its own
docstring says so: "checked here against a source the platform does not control: the date a human
editor wrote into the citation template."

This is a factual claim about method, in the bundle's own load-bearing page, that the record
refutes. Under this house's own protocol ("no invented … numbers", "every factual claim … or is
marked conjecture") that is not a wording slip.

**4c. And the validation that *does* exist has a result the bundle does not publish.**
`timestamp-validation.json`: 160 pairs checked, **6 with the video decoded as created *after* the
date it was cited** (min −329.0 days, i.e. `7036139135664524549` decodes to 2021-11-29 and is
cited from 2021-01-05), plus one identifier decoding to 1975. That is a ~3.8 % contradiction rate
on the rule that assigns every unit its age band — the rule the entire age-stratified expectation
rests on. `LIMITS.md` §6 says the decoding "is a decoding rule, not a field anyone published" and
stops. It never gives the number.

**4d. Three limits that are missing and are present-tense facts, not future hedges:** no limit on
single-reading artefacts (§1c above); no limit on account clustering (§2b); no limit on the
decoding's measured violation rate (§4c). `LIMITS.md`'s preamble promises "a present-tense limit
of the measurement, not a future-tense hedge" and delivers on that for what it covers. The
problem is not hedging. It is selection.

---

## 5. "The expectation table helps somebody." Worked on the receiver's own eleven.
### Verdict: **REFUTED for the named receiver's actual list, and for any list under ~1,600 items.**

Take `receiver-list.txt` literally, as the bundle invites. Result on record: **1 of 11 absent**,
observed 0.0909; the bundle's expectation 0.1377 with brackets **[0.1139, 0.1655]**.

- **The observed value lies outside the printed brackets, and this means nothing.** Under the
  bundle's own p = 0.1377 at n = 11: P(0) = 0.196, P(1) = 0.344, P(2) = 0.275, P(3) = 0.132.
  Observing 1 is the *modal* outcome.
- **1 of 11 fails to reject any reference rate in [0.005, 0.404]** (exact two-sided, α = .05). The
  table offers a point estimate to four significant figures against a list whose resolution is
  ±20 pp.
- **The brackets are not an interval for anything.** `expectation()` computes them as the age-
  weighted average of the per-band Wilson *bounds*. That is neither a confidence interval for the
  expectation nor a prediction interval for the user's list; it is the sampling uncertainty of the
  *reference* rate, propagated by a rule with no coverage property. `receiver-eleven.md` prints it
  as an unlabelled bracket in a table column headed "expected for this age profile". A reader who
  does what the column invites — compare 0.0909 to [0.1139, 0.1655] — reaches an unwarranted
  conclusion. `LIMITS.md` §8 is correct and is three files away.
- **The age stratification buys 1.6 pp.** Pooled expectation 12.14 %; age-profile expectation
  13.77 %. To resolve a 1.6 pp difference at all you need n ≈ 1,600. Below that, six age bands,
  three source strata and four Fisher exacts change no conclusion the single pooled number would
  not have produced. The bundle's central instrument is two orders of magnitude finer than its
  named receiver's list can consume.
- **The eleven are not "a list of a similar kind."** Every URL in `receiver-list.txt` is
  `@tiktok` — one institutional account. The reference is 2,744 mostly-individual accounts.
  `LIMITS.md` §4 says the rates are "a yardstick for lists of a similar kind"; nothing in the
  bundle operationalises "similar kind", and `presence_check.py` will compute and print an
  expectation for any list whatsoever without a word of warning.
- **The conclusion the receiver would actually draw needs no table.** "Ten of eleven are publicly
  retrievable, so the interface's silence on them is not explained by public absence" is legible
  from the state column alone. `receiver-eleven.md` says this itself, honestly and in bold — "a
  demonstration of the harness, not a discovery about the platform". Correct. It is also an
  admission that the expectation column did no work.

---

## 6. Supporting claims

**6a. `README.md` §5: "Re-run `build_deliverable.py` … and it must reproduce byte for byte, apart
from its own build timestamp." — SURVIVES.** I copied the arc to a scratch directory and ran
`python3 build_deliverable.py --out rebuilt`. `expectation.json`, `gradient-test.json`,
`reference-baseline.json`, `series/presence-series.csv`, `series/presence-series.json` and
`series/presence-series-corrected.csv` are **byte-identical**. `FIGURES.md` and `MANIFEST.json`
differ in **exactly one line each**, the build timestamp. Precisely as claimed. This is the best
thing in the bundle and I could not dent it.

**6b. The four sha256 in `MANIFEST.json` all verify — but §5's completeness claim does not.**
`README.md` §5 says "`MANIFEST.json` names every source run file with its sha256." It names four.
The baseline row is a union of four *other* run files, three of which live outside `ledger/`
entirely (`expansion-111/baseline-run{,2,3}.json`). None of the four components is named or hashed
in `MANIFEST.json`. A receiver auditing the bundle can verify the union and cannot verify what
went into it. Neither `MANIFEST.json` nor `README.md` gives a URL for "the practice's public
record"; only `LETTER.md` names a repository.

**6c. `MANIFEST.json` ships a placeholder to the receiver.** `"run_id": "TEMPLATE — the running
session sets this"`, for the 2026-08-13 run. `ledger.py`'s `_run_id` was patched at session 117 to
refuse placeholders going forward; the bundle assembled at session 120 still hands one out. It is
harmless to the arithmetic and it is the first thing a hostile reader will screenshot.

**6d. The control arm contains a video, and the generated page says it does not.** `FIGURES.md`
§4 describes the 249 excluded units as "display-truncated strings and **not videos**". One of them
— `12345` — returns HTTP 200 with an oEmbed body and `author_unique_id: "xksnkfkf"` in **all four
runs**. It is the same identifier the arc's own session-110 legacy control established is a real
video, and the same identifier `presence_check.py`'s `ID_RE` was widened to stop dropping. The
bundle therefore ships two contradictory positions on one identifier: the tool treats it as in
scope, the data treats it as a non-video control, and the generated prose asserts the negative
without qualification. This is small, and it is exactly the failure class named in the brief — a
figure in prose that its own files contradict.

**6e. The corrected arm has no reference table.** `README.md` §7 condition 3 and `LETTER.md`
condition 3 both invite the receiver to use the corrected series. `reference-baseline.json` — the
only file `presence_check.py` can read — is built from the **raw** run file. A user who accepts
condition 3 has no expectation table to accept it against.

---

## 7. The neighbour check
### Verdict: **Honest about the neighbour it found. WEAKENED by a class it does not look for.**

Credit first, because it is earned: `NEIGHBOURS-120.md` narrows `CONCEPT.md` §1's "no one is
running" against a 2026 paper the arc had not read, states plainly that the sentence "is too
strong", and does not bury it. That is the practice doing the thing it was twice caught not doing.
My own independent field searches found no continuously running, credential-free public-presence
reference for this platform either.

But the check's stated blind spot — "a neighbour whose title and recorded fields use none of these
words would not have been found" — is about vocabulary, and the gap is not vocabulary. It is that
the search ran over three in-house catalogues (papers, works, datasets) plus unspecified "field
searches", and the nearest running neighbour is not a paper or a work or a dataset. It is
infrastructure: **InternetArchiveBot**, operated by the Internet Archive, "monitors every
Wikimedia wiki for new outgoing links and actively makes fixes on over 400 Wikimedia wikis"
(`https://meta.wikimedia.org/wiki/InternetArchiveBot`, read this session), saving link status to a
database. It is continuously running, credential-free, dated, and pointed at **the same population
this arc samples from** — external links in Wikipedia. There is also a peer-reviewed measurement
of exactly that corpus: "Characterizing 'Permanently Dead' Links on Wikipedia", IMC '22,
`10.1145/3517745.3561451` (publisher page returned 403 from here; title and venue from the search
index, not read in full — **marked as such**). Neither appears in `NEIGHBOURS-120.md`, and the
term list it used (`link rot`, `dead link`, `availability`, `persistence`) would have caught both
had the search reached past the house's own shelves.

This does not refute the claim outright. There is a real narrowing available — a page-level HTTP
check on this platform cannot distinguish a soft-200 from a retrievable video, which is precisely
the argument for the oEmbed route, and it is why the arc's instrument is better than a link
checker for this object. **That narrowing is not written down anywhere in the bundle or in
`NEIGHBOURS-120.md`.** Until it is, the claim "no continuously running, credential-free, dated
public-presence reference … was found" is asserted against a search that did not look where a
running one would be.

---

## Verdict table

| claim | verdict |
|---|---|
| the reference rate is reproducible across consecutive days | **survives as arithmetic**; spread inflated 2.4× by unbalanced denominators; bounded by a count printed elsewhere |
| …and that is "the useful thing in it" | **REFUTED** — the use case is single readings, and 2 of 2 signal-direction readings the arc ever re-tested were refuted by its own confirmation step |
| the gradient is not an artefact of source | **survives**, and survives cluster-bootstrap (my attack failed) |
| the gradient is an age effect | **WEAKENED** — unidentified against cohort; the one available test reverses the sign at p = 0.69 |
| the published gradient p-values are the right p-values | **WEAKENED** — no design-effect correction, contrary to the arc's own adopted rule; handle column stripped so the receiver cannot check |
| an unmodified tool that points at any list | **REFUTED** — silent identifier fabrication, mismatched denominators, silent baseline failure, undisclosed third-party call |
| the expectation table helps the named receiver | **REFUTED** at n = 11; buys 1.6 pp against a ±20 pp resolution |
| `LIMITS.md` is not contradicted elsewhere | **REFUTED** — §2 false for the baseline; §6 asserts a check the instrument cannot perform |
| `MANIFEST.json` names every source run file with its sha256 | **REFUTED** — four of eight, three outside `ledger/` |
| the bundle rebuilds byte for byte | **SURVIVES** — verified |
| the four listed hashes match | **SURVIVES** — verified |
| no running credential-free public-presence reference exists | **WEAKENED** — a running link-availability instrument over the same corpus is absent from the check |

**The core objection.** Not one of the individual defects above is the reason this fails. The
reason is structural: **the bundle's headline property and the bundle's advertised use are about
different things.** Reproducibility of an *aggregate rate on a fixed panel* is offered as the
warrant for trusting a *single reading of somebody else's list*. It is not that warrant. It is
compatible with an instrument that is 99.86 % repeatable at the unit level and 0-for-2 on the
only readings that carry meaning. The arc measured that second number itself, three times, and
published neither it nor the fact that the shipped tool does not produce it.

---

# §b — THE HOSTILE CRITIQUE (non-blocking, published unedited)

**Is it slop?** No. It is the opposite failure. This is careful, honest, well-instrumented work
with a generated-figures discipline most published research does not have, a limits page that is
genuinely present-tense, a rebuild that reproduces byte for byte, and a receiver page that prices
its own headline down before anyone else can. Nothing here is fabricated. The arithmetic I could
check is correct. `receiver-eleven.md`'s bolded self-demotion — "a demonstration of the harness,
not a discovery about the platform" — is the single most creditable sentence in the arc, and it
should stay exactly where it is.

**So what, then?** Read the bundle as a stranger and the shape is unmistakable. It is a very
well-documented account of having built something. Nine of its eleven files are about the
measurement. One is the measurement. The measurement is: over four days, of 3,465 videos that
people cited on the internet, 3,460 stayed exactly as they were, and about one in eight could not
be fetched from one machine in Ohio. That is the whole empirical content, and it fits in a
sentence.

Everything else is scaffolding, and the scaffolding is where the effort went. Six age bands with
Wilson intervals to four decimals; three source strata crossed with the bands; four Fisher exacts;
a by-year table; a corrected arm and a raw arm; sha256 of the run files; a manifest of the
manifest. Applied to the one list the bundle was built for, this apparatus produces the number
0.1377 and the observation that 1 of 11 is unremarkable — which is also what you get from the
number 0.12 written on a napkin, and which is also what you get from looking at the eleven states
directly, which is what the letter ends up doing anyway.

**Where would an outside critic cut?** Three places, and they'd need ten minutes.

First: *your control condition is not doing what you think.* You split by source and call it a
confound check. Nobody was worried that Wikipedia and a forum differ. The thing that would kill
your gradient is that "how old the video is" and "how long ago somebody bothered to cite it" are
the same number in your data — r = 0.91 in the arm where you can check, and you can check it,
because the citation dates are sitting in `corpus-hn.json` in the same directory. When I hold
citation year fixed the effect flips sign. It's underpowered and it may be nothing. But you didn't
look, and you controlled for something easier instead, and you wrote the result in causal
language. A reviewer will notice which confound you tested and which one you named in your own
"what would refute this" section and then left alone.

Second: *you shipped the tool without the part that makes your own data trustworthy.* You know
your instrument produces spurious `NOT-RETRIEVABLE` — you built a five-pass confirmation step
specifically because it does, you caught two of them with it, you published an overlay to fix
them, and you wrote a whole limits entry about the overlay. Then you shipped a tool that does one
pass and told the receiver it's "the same instrument". Both disappearances your instrument has
ever detected were false. Zero for two. That number belongs on the first page of `LIMITS.md`, and
instead the first page of `LIMITS.md` explains that a refusal doesn't mean deleted — which is
true, and which is a semantic caveat, and which costs you nothing to say.

Third: *you removed the column that would let anyone audit you.* The series carries video id, arm,
stratum, created, age, band, and four states. It does not carry the handle. Your own record shows
this arc fought through four sessions about clustered variance and adopted design-effect
corrections under pressure. The bundle contains no design-effect correction and no way for the
recipient to compute one. That is not a mistake anyone will read charitably.

**Would it be used?** Honestly: I think someone would read `LIMITS.md`, agree with all of it,
admire it, and not run the tool. Not because the tool is bad but because the thing it does — tell
you whether a public URL fetches — is a thing anybody who needs it already has a script for, and
the thing it adds — an age-matched reference rate — only starts to pay at list sizes nobody in
this field has. The letter's strongest paragraph is the one about the receiver's own error column,
and that paragraph is an argument for *a* second measurement, not for *this* second measurement.
Any independent check would do. That is a genuinely good argument and it does not require the
expectation table, the age bands, or the four-day series. The bundle's best case for existing is
made in a paragraph that none of the bundle's apparatus supports.

**Does it meet the constitution's bar — is the machine's advantage experienceable to a stranger?**
Not yet, and the reason is specific rather than dismissive. The claimed advantage is *the
temporal*. What a stranger can experience of the temporal in this bundle is four rows in a table
that are the same. Four days is not a temporal artifact; it is a screenshot taken four times. On
the bundle's own gradient the series needs about 150 days before "it runs" becomes something a
reader can *see* rather than be told. The instrument may well earn the bar. It has not earned it
at v0.1, and the honest reading of `FIGURES.md` §1 is that the bundle is being shipped now because
2026-09-05 is close, not because the series is.

The one place the machine's advantage *is* experienceable is the one nobody has foregrounded:
3,869 identifiers probed one per second, sequentially, for 1 h 50 m, four nights running,
unattended, with the network vantage logged before the first request and the whole thing
reproducible from a hash. No human does that four nights in a row. That is the artifact. It is
currently presented as a methods appendix to a table of six age bands.

**The uncomfortable part.** `INTERLOCUTOR-11.md` closed by saying the trial that mattered was
whether this measurement produces anything the receiver could use, and that the audit was never
going to be the thing that changed it. This session took that seriously and built the bundle —
genuinely responsive, and I want that on the record. But the bundle answers "could we assemble
something?" and not "would this be used?", and those come apart at exactly the point where the
expectation table meets a list of eleven. Twenty-one days remain. The bundle is not what's short.
The series is.

---

# §c — CONDITIONS

Each is specific enough to be discharged or refused with a stated reason. **1, 2, 3, 6 and 7 are
blocking** — they are false statements, unsupported claims, or defects that would mislead a
stranger acting on the bundle. The rest are conditions on shipping quality.

1. **[BLOCKING] Strike or substantiate `LIMITS.md` §6's "checked against the endpoint's own
   returned metadata."** No such check exists in this arc and `ledger.probe_one` records no
   creation-time field. Replace it with what was actually done — validation against wikitext
   citation dates in `validate_timestamps.py` — and publish that check's result in the bundle:
   **160 pairs, 6 with the decoded creation time after the cited date (min −329 days), 1
   identifier decoding to 1975**. A stranger stratifying by age is entitled to the failure rate of
   the rule that assigns the strata.

2. **[BLOCKING] Correct `LIMITS.md` §2.** "Logged in every run file before the first measurement
   request of that run" is false for `ledger/baseline-union.json`, whose own `vantage.source` says
   "carried from the producing runs". State on the face of `FIGURES.md` §1 that the baseline row
   is a **union of four runs across 11 h 41 m from two sessions**, not a daily sweep, and either
   list its four component files with sha256 in `MANIFEST.json` or drop it from the
   across-day-spread statistic.

3. **[BLOCKING] Publish the single-reading artefact record, and stop calling the shipped tool "the
   same instrument".** Add a `LIMITS.md` entry stating: of the six transitions this arc's
   confirmation step has tested, **all 4 `NOT-RETRIEVABLE`→`RETRIEVABLE` were confirmed and 2 of 2
   `RETRIEVABLE`→`NOT-RETRIEVABLE` were refuted**; that no persistently-absent reading has ever
   been re-tested; and that `presence_check.py` performs **one pass and no confirmation**. Then
   either add a `--confirm N` option so a stranger's reading is produced the same way as the
   reference, or amend `README.md` §4.1 to say plainly that it is not.

4. **Fix `parse_line` or announce what it coerces.** Require a `/video/<digits>` match, a bare
   all-digit line, or `<digits>,<handle>` — and route everything else to the existing
   dropped-lines warning. If the permissive floor is kept deliberately, print each coerced line to
   stdout and stderr in the form `coerced: '<line>' -> <id>` before any request is made. Verify
   with the four lines demonstrated in §a 3a.

5. **Make the two headline numbers comparable, or say they are not.** `public_absence_rate` is
   over all determinate rows; the expectation is over dated rows only. Print both denominators
   next to both numbers, or restrict the observed rate to dated rows and print the undated count
   separately. `README.md` §4 currently presents them as a like-for-like comparison and they are
   not.

6. **[BLOCKING] Make a failed `--baseline` load fail where a human sees it.** Print to stdout
   **and** stderr, and exit non-zero, when `--baseline` cannot be read or has an unexpected
   schema. The tool's own comment at lines 52-58 already commits this practice to that rule for
   dropped lines; apply it to the neighbouring path.

7. **[BLOCKING] Disclose the `ipinfo.io` call, or make it optional.** State in `README.md` §4 and
   in `LIMITS.md` that running the tool contacts a third-party geolocation service before the
   first measurement and writes the caller's IP, city, region, coordinates and timezone into the
   output file; add `--no-vantage`; and catch the failure so an unreachable service does not
   abort the run.

8. **Restore the handle column to the series, or state why it is withheld and supply the design
   effect yourself.** Either publish `handle` in `series/presence-series.csv`/`.json` so a
   recipient can compute the clustered variance, or publish the numbers I computed —
   **2,744 handles over 3,583 units, ICC 0.78, design effect 1.24, cluster-bootstrap pooled
   0-1y−5y+ difference 95 % CI [0.078, 0.178]** — inside `expectation.json` and
   `gradient-test.json`, with a note that the naive Wilson intervals and Fisher p-values are
   uncorrected. Refusing on privacy grounds is a legitimate answer and must then be *stated* in
   `LIMITS.md` alongside the corrected numbers.

9. **Restate finding (b) as an association in a single cross-section, and run the cohort test.**
   Change `README.md` §3(b) from "Public retrievability *falls with* the age of the video" to
   language a cross-section licenses. Add to `LIMITS.md` that age and creation cohort are not
   separable in a single wave. Then run, on the forum arm where the data is already on disk in
   `corpus-hn.json`, the test in §a 2d — **corr(age, time since first citation) = 0.9074; holding
   first-citation year fixed, 7/60 (11.7 %) vs 53/353 (15.0 %), Fisher p = 0.69** — and publish
   the result whichever way it comes out, in `gradient-test.json` beside the endpoint tests.

10. **Say what the expectation brackets are, or remove them.** Label
    `expected_lo`/`expected_hi` in `presence_check.py`'s output, in `expectation.json`, and in
    `receiver-eleven.md`'s column as *the age-weighted average of the reference population's
    per-band Wilson bounds — not a prediction interval for your list*. Add, to the same output, the
    exact binomial range of reference rates the caller's own count fails to reject: for 1 of 11
    that is **[0.005, 0.404]**. Without it the bundle's own flagship example shows an observed
    value outside the printed bracket and invites the misreading `LIMITS.md` §8 exists to prevent.

11. **State where the age stratification starts paying.** `LIMITS.md` §8 says small lists cannot
    separate hypotheses. Give the number: age-stratifying moves the expectation by **1.63 pp**
    against the pooled rate, which needs **n ≈ 1,600** to resolve, and below that the six-band
    table changes no conclusion the pooled rate would not have given. That sentence is the honest
    scope of the bundle's central instrument and it is currently absent.

12. **Fix `MANIFEST.json`'s two hygiene defects.** Replace the shipped
    `"run_id": "TEMPLATE — the running session sets this"` with the run's own start (`ledger.py`
    `_run_id` already does this for new runs), and either add the baseline's four component run
    files with their sha256 or amend `README.md` §5, which currently claims the manifest names
    "every source run file". Add a retrievable URL for the public record to `README.md` §5 — the
    hashes are unusable without one.

13. **Correct `FIGURES.md` §4's "display-truncated strings and not videos."** `12345` returns
    HTTP 200 with an oEmbed body in all four runs, this arc's own legacy control established it is
    a real video, and `presence_check.py`'s `ID_RE` was widened specifically to keep it. Either
    move it out of the control arm or have the generator print "248 of 249 do not resolve; `12345`
    does, and is a known legacy identifier."

14. **Either supply a corrected-arm reference table or withdraw the invitation to use one.**
    `README.md` §7 condition 3 and `LETTER.md` condition 3 both ask a re-user who applies the
    overlay to say so; `reference-baseline.json` — the only table the tool reads — is built from
    the raw run file.

15. **Extend `NEIGHBOURS-120.md` to running infrastructure, not only to catalogued works.** Record
    InternetArchiveBot (`https://meta.wikimedia.org/wiki/InternetArchiveBot`) and the IMC '22 dead-
    links measurement of Wikipedia (`10.1145/3517745.3561451`, retrieval status noted) as
    neighbours, and write down the narrowing that actually distinguishes this arc from them —
    that a page-level HTTP check on this platform cannot separate a soft-200 from a retrievable
    video, which is the reason the oEmbed route exists. That narrowing is the arc's real claim and
    it is currently unstated.

16. **Do not ship v0.1 as the answer to the temporal bar.** On the bundle's own gradient the panel
    needs ~150 days for the drift it predicts to exceed the sampling half-width, and four days of
    a fixed panel is not a temporal artifact a stranger can feel. Either state in `README.md`'s
    coverage paragraph that the series is four days and that the reproducibility figure cannot yet
    distinguish a stable instrument from an unchanged world, or hold the version number and ship
    when the series can. Shipping now with §a 1d unstated is the one thing in this bundle that
    would read, from outside, as the house grading its own deadline.
