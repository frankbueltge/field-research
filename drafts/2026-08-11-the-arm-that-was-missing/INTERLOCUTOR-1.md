# Interlocutor report — gate session 1, *The Arm That Was Missing*

*Judging commit `4dc00eb`. Every figure below that is asserted as "confirmed," "matches," or
"reproduces" was independently recomputed or independently re-fetched by me in this session, with my
own code and my own network calls — not by re-reading the practice's method description. Commands are
listed at the end. Nothing here was taken on the practice's word.*

## (a) Refutation attempt

### 1. Re-deriving the headline numbers from raw JSON, independently

I wrote my own parser against `probe-results.json` and `census-results.json` (not against
`DERIVED.md`'s prose) and recomputed, from scratch:

- Sample: 300 requests, statuses `{200: 262, 400: 37, None: 1}`, 0 duplicate video ids. Retrievability
  262/299 = 87.6%. My own Pearson-on-binary (point-biserial) of retrievable-vs-year: **r = 0.17093,
  t = 2.9897, df = 297** — matches the published r = 0.171, t = 2.990 to four significant figures.
- Census: 2,201 requests, `{200: 1941, 400: 232, None: 28}`. Restricted to plausible platform-lifetime
  years (n = 2,169): **r = 0.14475, t = 6.8101, df = 2,167** — matches the published figures exactly.
- Pooled ≤2022 vs ≥2023 in both sample and census reproduced exactly (71/90, 191/209, 557/655, 1383/1514).
- Cross-run reliability: I intersected `probe-results.json` and `census-results.json` by video id myself
  (not by reading their reliability claim) — **295 videos in common with a usable status in both runs,
  295 agree, 0 disagree.** Matches exactly.
- K3 reverify arms: recomputed status counts and per-video resolution from `reverify-results.json`
  independently — arm A 109×400/3×200/2 transport-fail, arm B 41×200/1 transport-fail, arm C
  19×400/1 transport-fail, 35/38 arm-A videos all-400 across reps, exactly 1 video (`7173687443047189766`)
  all-200 across reps. Matches exactly.
- Corpus structure: `corpus-merged.json` has exactly 2,201 keys (distinct video ids), spanning exactly
  1,563 distinct `(wiki, page)` pairs (I computed this by pair, not by page title alone — 1,555 distinct
  bare titles exist because some titles collide across language editions, which the practice's method,
  correctly, does not conflate).
- The 1,546-vs-1,563 article-count discrepancy between `RESULT.md`'s census-article stats and the raw
  corpus size is real but resolves cleanly: exactly 17 articles have *zero* video in the census run that
  returned a usable (200/400) status — all their citations hit transport failures — so the reported
  denominator of 1,546 is correct, just under-explained in the prose. Once that's accounted for, **196
  articles citing ≥1 unavailable video and 157 citing zero retrievable videos both reproduce exactly.**

I could not break the arithmetic anywhere. Every headline number in `CONCEPT.md` and `RESULT.md` that I
attempted to re-derive from the raw JSON, using my own code, reproduced to the figure given.

### 2. Attacking the corpus

- **Cross-edition duplication is real and larger than stated anywhere in the record**: 232 of 2,201
  video ids (10.5%) are cited from more than one language edition. This is not a bug — the merge is
  correctly keyed by video id, so the 2,201 distinct-id count is not inflated by it — but it is a fact
  about the corpus's composition that isn't surfaced in `DERIVED.md` §2, and it means the "21 language
  editions" framing overstates independence: one video appearing in `ar`, `en`, and `es` is one video, not
  three data points, and the by-edition retrievability table (F9 "by-edition spread") is measuring 21
  overlapping, not disjoint, populations.
- **Malformed ids** (1971, 1975×3) are handled honestly — reported, excluded from age analysis, and I
  confirmed 3 of 3 "1975" ids are non-retrievable, consistent with them being garbage rather than real
  videos.
- **Population validity**: "videos cited in an encyclopedia" is explicitly and correctly flagged in
  `CONCEPT.md` §4 as *not* a random sample of the platform, and the 87–89% figure is framed against the
  sockpuppet paper's 17.7–23.3%-in-weeks figure as a durability-of-the-cited-record claim, not a
  platform-wide claim. That hedge is accurate and I could not find anywhere it is quietly dropped.
- **Age confound with edition**: I ran my own within-edition stratification on the census (a test the
  practice did not run). The ≤2022-vs-≥2023 gap holds in the same direction in 5 of 6 editions large
  enough to check (en +8.4pp, ja +12.8pp, he +3.8pp, de +0.9pp, id +6.7pp), and is flat in `es` (−0.3pp).
  The age effect is not purely an artifact of edition composition, but it is not uniform either, and this
  check is mine, not theirs — it does not appear in `DERIVED.md`.
- **Age confound with topic (person vs. event)**: untested, by them and by me. No field in the corpus
  encodes article topic type, and classifying 1,563 articles was out of scope for this session. This is
  a real, unresolved gap, not a refutation.
- **The point-biserial correlation as an instrument**: it is the mathematically correct choice for
  binary-vs-continuous association, but the practice's own §4 admits the year-retrievability relationship
  is *not monotone* (2020 > 2021, 2022; 2025 < 2024 in the sample; one inversion at 2023 in the census).
  A single linear-correlation statistic dressed up with a t-test and a p-value is a weak, slightly
  over-precise instrument for a relationship that is visibly non-monotone in the same document's own
  table. The aggregate ≤2022-vs-≥2023 comparison (which does not assume monotonicity) is the more honest
  number, and it is the one that survives my within-edition check above.

### 3. Attacking the probe's meaning — I ran tests they did not

I did not just re-read `reverify.py`. I hit the live endpoint myself, right now, with tests the
practice's own K3 control did not include:

- **Wrong-handle test**: `@totallywronghandle999/video/7279205800122305798` (a real, retrievable id from
  their own 200-set with a handle that has never existed) still returns HTTP 200 with full metadata. So
  does the bare path `tiktok.com/video/7279205800122305798` with no `@handle` at all. **The handle field
  in the URL is not merely sometimes-stale (F6's framing) — it is entirely ignored by the endpoint.**
  This *strengthens* their claim that the instrument keys on id, not URL — the "handle-change
  contaminant" they report is actually a special case of "handle is not checked at all," which is a
  stronger and cleaner fact than the one they state.
- **Different User-Agent** on a known-400 id: still 400. Rules out a trivial UA-based block as the
  explanation.
- **Concurrent burst test** (10 parallel workers, 20 rapid requests, no 1 s delay) against four known-good
  ids: **20/20 return 200, zero 429s, zero spurious 400s.** Same burst pattern against three known-400
  ids: **15/15 return 400.** This is a genuinely discriminating test the practice's sequential-only
  design did not run, and it rules out both "rate pressure manufactures 400s" and "rate pressure
  manufactures false 200s."
- **Independently-sourced famous, definitely-live videos** not in their corpus at all (found via a fresh
  web search, not from their data): Khaby Lame's top video (6953610726955126022) and two other
  high-view-count 2025-vintage videos found by search — **all three return clean 200s.** This is the
  "does an obviously-live video ever 400" test the task asked for, and the answer is no, not once, across
  three independently chosen cases.
- **Geographic vantage point — genuinely unresolved.** `ipinfo.io` on this machine resolves to a
  US-based cloud egress (Columbus, OH, AS396982). I have no way, in this sandbox, to repeat the probe
  from a second geography, and neither, as far as the record shows, did the practice. Every 400 in this
  dataset is only known to be a 400 *from this vantage point*. Since geo-restriction is explicitly on
  their own list of things the 400 cannot distinguish, the daily series they propose to run cannot tell
  a real deletion from "this session's egress region changed." I could not move this: it is a real,
  unaddressed risk to the "each disappearance pinned to the day it happened" promise in `CONCEPT.md` §1,
  and it is not mentioned once in `DEVIATIONS.md`.

None of this refutes K3's finding — if anything my tests reproduce and extend it — but the vantage-point
gap is a genuine, load-bearing hole in the "daily series" promise that survives everything else I tried.

### 4. Attacking the receiver argument

I fetched `aiforensics.org/work` myself and parsed title/date pairs independently (not from the fan-out's
summary). Result: **8 items dated after 2026-01-14** (14-01-2026 in the page's own DD-MM-YYYY format),
none titled about TikTok's Research API. I went one step further than the fan-out and fetched the full
text of the two most TikTok-adjacent post-cutoff items (`artificial-elections-2.0`,
`dutch_parliamentary_elections_2025`): TikTok is mentioned in both, but only as one of several platforms
in ad-repository/content-collection monitoring — never in connection with the Research API or a coverage
claim. **`RESULT.md`'s precise claim ("none of them concerns this platform's research interface") survives
a harder read than the one it was given**, and does not overclaim by saying "nothing about TikTok."

I also fetched the dark dashboard's full HTML and extracted all 11 videos' displayed "Created:" timestamps
myself, decoded the ids independently with my own script, and applied the Europe/Berlin offset rule
stated in `DEVIATIONS.md` D6. Result: **9 of 11 match to the displayed minute, and the two disagreements
are exactly 49 days and 30 days** — I did not just check that 9/11 "agree," I recomputed the actual gap
for the two outliers and got 49 and 30 days independently, matching D6's numbers precisely. This is a
non-trivial, load-bearing check and it holds.

On K5 itself: the receiver clearly has the technical means to build exactly this kind of instrument —
they already built the more sophisticated one (Plotly dashboard, per-video metadata, creation-date
display) for their 11 videos. The concept's argument that "the running is not free" is therefore an
argument about labor and attention, not about capability, and it is honest about that. But this cuts
against the artifact's value as much as for it: an artifact whose main offering is "we did the tedious
part" is real but modest, and — as the concept's own "honest failure mode" paragraph concedes — the
artifact **cannot itself detect a Research API coverage gap**; it only supplies the credential-free half.
Turning it into the comparison the concept is named for still requires the receiver's credentialed side,
which this practice cannot supply and never will. I judge K5 as **not firing outright** (no evidence they
already run this, no evidence it's worthless to them) but **partially live**: the concept should say, as
load-bearing text rather than a hedge, that the artifact is an input component to an audit, not an audit.

### 5. Attacking D1, on the merits

I read `PREREGISTRATION.md` §2 and `DEVIATIONS.md` D1 side by side. The pre-registration says "at most
two alternative credential-free dated sources are tried and named." The practice's reading — "one API,
one query shape, one namespace rule, one data model, therefore one source queried in 21 places" — is a
mechanical, interface-level reading. But the by-edition spread table the practice itself publishes (F9,
78.7%–95.3% across editions) proves these 21 pools are **not statistically interchangeable**: different
contributor bases, different notability norms, different citation practices, different age profiles. A
"source," for the purpose of a guardrail against scope-creep-until-you-clear-a-threshold, is more
naturally read as an evidentiary population, not an API signature — and English Wikipedia alone (853
ids) misses the 1,000 floor. **I judge this the closest thing to a self-serving reading in the whole
record.** It is not hidden — the practice states both readings and says K1 fires on the strict one — but
that disclosure lives in `RESULT.md` and `DEVIATIONS.md`, not in `CONCEPT.md`, which is the actual gate
document under judgment and which reports P2 and K1 as passing without surfacing the tension on its own
page. That asymmetry between the two documents is a real charge.

### 6. Attacking novelty

I ran two independent web searches for TikTok-citation-decay and continuous-availability-tracker work
beyond what the fan-out found. Nothing closer than `arXiv:2601.12390` turned up. I independently fetched
that paper's abstract and body text and confirmed, character for character, the two quotes CONCEPT.md
relies on ("exclude large portions of the platform PIE (up to approximately 50 percent), strip essential
contextual metadata (up to approximately 83 percent)" and "between 17.7% and 23.3% of posts were no
longer accessible within weeks") are both accurate and not truncated in a way that changes their meaning
— I read the surrounding paragraphs in both cases. The novelty claim survives.

### 7. Attacking the bar — "a stranger can feel it in one sentence"

This is the weakest sentence in the concept, and no amount of re-derivation rescues it. "This thing was
still watching 209 days after the last person stopped" is a claim about the *maker's* persistence, not a
property a stranger encounters *in the artifact*. A stranger looking at a daily retrievability percentage
does not spontaneously feel institutional abandonment on the other side of the comparison; they see a
number that moves a little or doesn't. The actual experienceable machine-advantage properties — scale
(2,201 vs. 11), reproducibility (seed published, script published), and the semantic disclaimer stated on
the front page rather than buried — are real and are properties of the artifact. The "still watching"
framing is not; it's a claim about session cadence, asserted, not shown. This is a rhetorical overreach
that should be cut or rewritten to describe what a reader actually sees.

### 8. Hunting for the signature error, a seventh time

I specifically looked for: quotes not read to the end, and search-failure-as-fact-about-the-world.
I did not find a new instance. Every negative claim I checked ("no third party we found," "nothing
published… since 2026-01-14," "no free continuous at-scale series") is consistently hedged with "we
found" / "we can find" language in both `CONCEPT.md` and `RESULT.md`. The one place a source could not be
re-opened (D3, the December 2025 Commission press release) is explicitly marked as carrying no load, and
I confirmed by trying to fetch it myself that the underlying problem (PDF text extraction failing on this
machine) is plausible and the practice did not fall back on quoting it anyway. The quotes I independently
re-fetched — the changelog line, the EC roundtable line, the arXiv abstract and body lines, the dashboard's
two self-descriptive sentences — all reproduced verbatim from the live pages. I could not find a seventh
occurrence of the practice's own named failure mode.

## The decisive charges

None of the following, individually or together, breaks the headline claim. They are the strongest
findings against the record, in descending order of severity:

1. **D1 is a self-serving reading of the practice's own pre-registration**, decided by the practice
   itself in the practice's own favor, and the tension is disclosed unevenly: fully in `RESULT.md` and
   `DEVIATIONS.md`, not at all in `CONCEPT.md` — the document this gate is actually judging. On the
   strictest reading of the pre-registration's own words, K1 fires and the concept in this form should
   have parked. I do not think this single interpretive dispute should kill the concept outright — the
   underlying corpus of 2,201 credential-free, independently reproducible ids is real regardless of how
   it is categorized — but it is a genuine integrity gap in the front-page document, not a footnote.
2. **The geographic-vantage-point gap is real, unaddressed, and specifically threatens the arc's
   central promise** ("each disappearance pinned to the day it happened"): a single-egress instrument
   cannot distinguish a real disappearance from a change in vantage, and geo-restriction is on the
   practice's own list of things the 400 cannot explain.
3. **The age effect is real in aggregate but is asserted with more statistical polish (r, t, df, p) than
   the underlying relationship supports** — it is visibly non-monotone in the practice's own tables, and
   no confound check (edition, topic type) appears anywhere in `DERIVED.md`. I ran the edition check
   myself; it mostly, not uniformly, holds.
4. **The "stranger can feel it" bar claim is unearned** — it describes the maker's behavior, not a
   property the artifact exhibits to a viewer.

## What I could not move

- I could not test from a second network vantage point; the geo-restriction question is open, not closed,
  in either direction.
- I could not classify the corpus by topic type (person vs. event) to test that confound on the age
  effect; time and tooling did not permit hand-coding 1,563 articles.
- I could not find a public statement from AI Forensics, positive or negative, about whether they want or
  would use an artifact like this — the practice's own rule (no contact) makes this permanently
  untestable from outside, by design, and I respected the same constraint.
- I could not find a seventh instance of the practice's named signature error (quote-not-read-to-the-end
  / search-failure-as-world-fact), despite specifically hunting for one across every document.
- I could not break a single one of the headline arithmetic claims — sample stats, census stats,
  reliability, K3 arms, corpus counts, article counts, the dashboard-timestamp validation — under
  independent re-derivation from raw JSON and independent live re-fetches of every quoted primary source.

## VERDICT

**STANDS WITH CONDITIONS**

Conditions:

1. `CONCEPT.md` itself (not only `RESULT.md`/`DEVIATIONS.md`) must state, on its own front page, that
   on the strict reading of its own pre-registration the corpus route fails K1 (English Wikipedia alone:
   853 < 1,000), and must not report "P2 holds" without that qualifier where P2 is scored.
2. The record must state plainly, before the daily arc runs, that all measurements share a single,
   unlogged network vantage point, and that the arc cannot yet distinguish a real day-to-day change from
   a vantage-point or infrastructure change unless egress is fixed or logged per run.
3. The age-effect statistics (r, t, p) must be presented alongside the non-monotonicity already shown in
   the same tables, with the same prominence, not as a headline figure whose caveat trails behind it —
   and any future write-up should attempt at least the edition-level stratification check this review
   performed independently, since it changes the effect's credibility non-trivially.
4. The K5 receiver argument must state, as load-bearing text, that the artifact is an input to an audit
   (a credential-free half needing pairing with the receiver's own credentialed comparison) and not an
   audit in itself — the concept's current "honest failure mode" framing hedges this in a way that reads
   as pre-emptive defense rather than as the artifact's actual, stated limit.
5. Drop or rewrite "a stranger can feel it in one sentence: this thing was still watching 209 days after
   the last person stopped" — it names a claim about the maker's persistence, not a property of the
   artifact a stranger encounters.

## (b) The hostile critique

**So what?**

Strip the framing and the object is this: a script that asks TikTok's oEmbed endpoint, once a day,
whether ~2,200 videos that happen to be cited on Wikipedia still resolve. That is a link checker. A
competent undergraduate could write the core of it — corpus fetch, id decode, HTTP loop, binary
retrievable/not — in an afternoon, and this practice's own scripts total under 470 lines across six
files. The interesting work in this record is not the daily series; it is the incidental discoveries made
while building it (the handle field is entirely ignored by the endpoint; the 400 carries no error
granularity at all; the platform's own crawl-block excludes the largest free web archive from ever seeing
a TikTok video page). Those are one-time findings. The thing that is supposed to justify weeks of running
— the daily ledger — is, on its own numbers, likely to move by low single-digit percentage points a day,
if that, since 89.3% of a mostly-stable citation corpus checked once is not a population with a high
daily churn rate. Day 14 of this arc is very likely to look almost exactly like day 1. A critic will ask,
correctly, what the fourteenth identical-looking data point is actually for.

The name is doing a lot of the work the substance doesn't fully back up. "The Arm That Was Missing"
frames a Wikipedia-citation availability checker as necessary complementary infrastructure to a legally
mandated researcher-access regime. It isn't that, and the concept's own "honest failure mode" paragraph
half-admits it: without the credentialed side, which this practice explicitly can never obtain, the
artifact cannot itself demonstrate a Research API coverage gap. It can only ever say "video X existed
publicly on day Y" — which is necessary but not sufficient, and is being sold with the rhetorical weight
of the whole missing arm rather than one bone in it.

The survivorship-bias comparison is close to a rhetorical sleight of hand even though it's technically
disclosed. Comparing "87.7% of videos cited in an encyclopedia are still up after up to eight years" to
"17.7–23.3% of feed-served posts vanish within weeks" and displaying them side by side invites exactly the
wrong inference — that TikTok content is durable — when what's actually being measured is that content
someone bothered to cite as a source tends to stay up, which is closer to a tautology about what gets
cited than a finding about the platform. The concept says this in words ("not a random sample of the
platform") but then puts the two numbers in the same sentence anyway, which is how a reader's eye actually
works.

The self-awareness is itself a tell. The document spends more sentences pre-empting an adversary
("retired," "the adversary's, not ours," "read to the end this time," "this is on the concept's front
page, not in a footnote") than it spends making an affirmative case that anyone outside this house should
care. That is what a document written primarily to survive its own gate reads like — legally
defensible, thoroughly hedged, procedurally immaculate, and largely uninterested in whether the resulting
artifact is something a stranger would bookmark. Given that the pre-registration itself says this
practice is on a short leash after five failed forecasts, that orientation is understandable. It is also,
on the evidence in front of me, the accurate read of the document: rigorous to a degree that few
link-checkers ever are, and not obviously interesting to anyone who isn't already inside the argument
about whether it should exist.

## Commands I ran

```bash
# instrument / robots / dashboard / changelog / EC page — fresh, independent fetches
curl -sSI -m 30 "https://www.tiktok.com/robots.txt"
curl -sS  -m 20 "https://www.tiktok.com/robots.txt" -o /tmp/robots.txt   # byte-identical to committed copy
curl -sS  -m 20 "https://aiforensics.org/work" -o /tmp/aif-work.html
curl -sS  -m 20 "https://aiforensics.org/work/artificial-elections-2.0" -o /tmp/ae2.html
curl -sS  -m 20 "https://aiforensics.org/work/dutch_parliamentary_elections_2025" -o /tmp/dutch.html
curl -sS  -m 20 "https://playground.tiktok-audit.com/api-na/" -o /tmp/dashboard.html
curl -sSL -m 25 "https://digital-strategy.ec.europa.eu/en/news/commission-holds-roundtable-data-access-vetted-researchers" -o /tmp/ec-roundtable.html
curl -sSL -m 30 "https://developers.tiktok.com/doc/changelog" -o /tmp/changelog.html
curl -sSL -m 25 "https://arxiv.org/abs/2601.12390" -o /tmp/arxiv-abs.html
curl -sSL -m 30 "https://arxiv.org/html/2601.12390v1" -o /tmp/arxiv-full.html

# CommonCrawl CDX API — direct, independent of their byte-range approach (theirs reset; this worked)
curl -sS -m 20 "https://index.commoncrawl.org/collinfo.json"
curl -sS -G -m 25 "https://index.commoncrawl.org/CC-MAIN-2026-30-index" \
     --data-urlencode "url=tiktok.com/*" --data-urlencode "output=json" --data-urlencode "limit=1000" \
     -o /tmp/cc-tiktok.json                      # 339 lines, all urlkey == com,tiktok)/robots.txt
curl -sS -G -m 25 "https://index.commoncrawl.org/CC-MAIN-2026-30-index" \
     --data-urlencode "url=tiktok.com/*/video/*" --data-urlencode "output=json"   # 404 "No Captures found"

# live oEmbed probing — my own tests, not theirs
curl -sS -m 20 "https://www.tiktok.com/oembed?url=...%40wassupann%2Fvideo%2F7279205800122305798"     # 200
curl -sS -m 20 "https://www.tiktok.com/oembed?url=...%40esse_magazine%2Fvideo%2F7403302339337080097" # 400
curl -sS -m 20 "https://www.tiktok.com/oembed?url=...%40totallywronghandle999%2Fvideo%2F7279205800122305798" # 200 — handle ignored
curl -sS -m 20 -A "Mozilla/5.0 ..." "https://www.tiktok.com/oembed?url=...esse_magazine...7403302339337080097" # still 400
curl -sS -m 20 "https://www.tiktok.com/oembed?url=https%3A%2F%2Fwww.tiktok.com%2Fvideo%2F7279205800122305798" # 200, no handle at all
curl -sSI -m 15 "https://www.tiktok.com/oembed?url=...wassupann...7279205800122305798"  # HEAD -> 404 (noted, not load-bearing)
curl -sS -m 15 https://ipinfo.io/json                          # egress: Columbus OH, AS396982 Google LLC
python3 - <<'PY'   # concurrent burst test: 20 requests, 4 known-good ids -> 20/20 200
python3 - <<'PY'   # concurrent burst test: 15 requests, 3 known-bad ids  -> 15/15 400
PY

# web search for independently-sourced live videos, and for closer neighbours
# (WebSearch tool) "tiktok.com/@khaby.lame/video/" most viewed video id
# (WebSearch tool) TikTok videos cited Wikipedia sources link rot availability study
# (WebSearch tool) continuous daily monitoring TikTok video availability dataset dashboard research
curl -sS -m 20 oembed?...khaby.lame/6953610726955126022        # 200
curl -sS -m 20 oembed?...funny_moments439/7534391463745047830  # 200
curl -sS -m 20 oembed?...joy.of.everything/7400806185143651627 # 200

# independent recomputation from raw JSON (own Python, not theirs)
python3 -c "... corpus-merged.json distinct ids / by-year / cross-edition duplication ..."
python3 -c "... probe-results.json point-biserial r,t,df; per-year table; handle mismatches ..."
python3 -c "... census-results.json point-biserial r,t,df; pooled rates; per-edition stratification ..."
python3 -c "... probe/census intersection -> 295/295 reliability ..."
python3 -c "... reverify-results.json arm A/B/C counts and per-video resolution ..."
python3 -c "... dashboard.html: extract 11 'Created:' timestamps, decode ids, apply Berlin offset,
             compare to displayed dates -> 9/11 exact-minute match, 2 disagree by 49 and 30 days ..."
python3 -c "... census article-level aggregation -> 1546/1563 usable articles, 196 with >=1 unavailable,
             157 all-unavailable, reconciling the RESULT.md denominator ..."
python3 -c "... timestamp-validation.json summary re-read for consistency (160 pairs, 6 violations) ..."
```
