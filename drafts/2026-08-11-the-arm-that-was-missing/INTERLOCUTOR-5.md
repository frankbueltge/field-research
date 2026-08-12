# Interlocutor 5 — session 113, on state c116931

*Every reproduced number below comes from fresh code written for this pass
(`/tmp/.../scratchpad/reverify.py` and inline scripts), reading only
`ledger/run-2026-08-12T0341Z.json`, `ledger/baseline-union.json`,
`receiver-arm-2026-08-12.json`, `d1-yield.json`, `expansion-111/build_baseline_manifest{,2,3}.py`
and `receiver-report-2506.09746v2-extracted.txt` — never by importing or running
`null_model.py`, `receiver_comparison.py`, `presence_check.py` or `power_audit.py` for the
arithmetic itself. `presence_check.py` was, however, actually **run** against the live network,
three requests, 1 req/s, as the task asked. Quotations were checked against the extracted text
character-for-character via `re.sub(r'\s+',' ',text)` normalisation (which erases only whitespace
and PDF ligature artefacts, never wording), and one quotation was additionally checked against the
live arXiv abstract page.*

## (a) Refutation attempt

### C1 — the headline is already net of public absence

Recomputed from the receiver's own quoted numbers (`U=70,239`, `N0=260,000`):

| share | × U | ÷ N0 |
|---|---|---|
| 46 % (summary, public-not-in-API) | 32,309.9 | **12.4269 %** |
| 62.7 % (method, public-not-in-API) | 44,039.9 | 16.9384 % |
| 36 % (not public) | 25,286.0 | 9.7254 % |
| 21 % (unexplained) | 14,750.2 | 5.6731 % |
| 18 % (retry recoveries) | 12,643.0 | 4.8627 % |

Published headline: **12.46 %**. Only the 46 % share lands close (0.033 pp off, and every other
candidate share is off by 3–5 pp), so the identification is not a coincidence of rounding among many
near-misses — it is the unique match. This independently reproduces `receiver_comparison.py`'s
`funnel_arithmetic` exactly, digit for digit.

I also worked both readings of "the remaining 21 %" the task asked for. Read as a share of 70,239
(the reading `SOURCE-READING-113.md` and `receiver_comparison.py` use): 21 % + the Canada/ads share
(≈25 %, "a similar share" to Canada each) sums to the 46 % the paragraph is decomposing — self
-consistent (18 + 36 + 46 = 100, confirmed against the extracted text). Read as a share of the 46 %
subgroup instead: 0.21 × 32,310 ≈ 6,785, i.e. 2.6 % of 70,239 / ≈1 in 96 of the sample — but nothing
in the paragraph introduces a new base at that point; every percentage in it (18, 36, 46, and the
Canada/ads/21 split) shares the same antecedent, "the 70,239 videos we investigated," stated in the
paragraph's own topic sentence. The text supports the first reading; the increment's "5.67 %, about
one in eighteen" is right, and it doesn't show this alternative-reading work, which would have cost
one sentence.

**VERDICT: STANDS.** The arithmetic reproduces exactly and the identification of 46 % as the source
of the headline is the only share that comes close.

### C2 — "the arm the dark instrument never had" was the report's own arm

Confirmed the report contains the passage verbatim (checked against the extracted PDF text, see
Quotation Discipline below): they scraped 70,239 identifiers in 2025 and split them into public/not
-public. This is real and the arc missed it for four sessions by quoting only the abstract — genuine.

But I went back to session 109's founding text to check whether the thing being "corrected" was
actually claimed as broadly as `SOURCE-READING-113.md` §6 says. `PREREGISTRATION.md` line 30 reads:
*"The claim is about the arm the dark instrument never had. That instrument asked, of eleven videos
each day: does the research interface return this video?"* — "that instrument" is explicitly the
**dashboard**, not the report, and `CONCEPT.md` line 108 is equally scoped: *"Their instrument
compares one thing against nothing: it asks the research interface about eleven videos..."* `DERIVED.md`
§0 (session 108, the founding session) states outright: *"no claim in RESULT.md depends on the
paper's body text — only on its abstract, authors and submission history."* So the founding claim
was already honest about having read only the abstract, and was already scoped to the dashboard
specifically, not to "the receiver" as an undifferentiated whole. The deliverable this arc has
consistently promised (CONCEPT.md line 36: *"the missing half is buildable... at a scale and a
constancy no one is running"*) is about scale and constancy, which the report's one-time 2025 scrape
still doesn't supply — that half of the arc's claim is untouched by this correction.

**VERDICT: STANDS WITH CONDITION.** The correction is real (the report body was unread for four
sessions, a genuine standing-check failure) but its framing ("this arc's framing... was wrong")
overstates how much the founding documents actually claimed; they were already narrower than the
"correction" implies. Condition: state plainly that the founding scope was already "the dashboard,"
not "the receiver," rather than implying four sessions of the whole arc rested on an error that a
close read of session 109's own text does not support.

### C3 — the ceiling bound ("a weighted mean cannot exceed its largest component")

This is the one I broke. The document's §2a claim: worst band 5y+ is 17.80 % absent (upper CI
21.95 %), therefore no age composition of the reference population reaches 36 %. I reproduced those
two numbers exactly (0.17801047120418845 / 0.2195186199957757, matching `receiver-comparison.json`
to 13 decimal places). Then I went one level finer than the six published bands, using the **same run
file**, splitting the open-ended "5 y+" bin by calendar year — a partition the document's own §1a
table already publishes three paragraphs earlier in the same file:

```
2019  n=35   present=0.7714  absent=0.2286  Wilson absent-CI [0.1207, 0.3902]
2020  n=163  present=0.8098  absent=0.1902  Wilson absent-CI [0.1373, 0.2573]
```

n = 35 clears the pre-registration's own n ≥ 30 floor for inclusion in any criterion — this is not an
underpowered cell being unfairly cited. **The 2019 cohort's own point estimate (22.86 % absent)
already exceeds both the stated ceiling's point estimate (17.80 %) and its upper CI (21.95 %)**, using
nothing but a coarser-vs-finer cut of the identical population the ceiling claims to bound. Splitting
finer still (by exact age-year inside the 5y+ band) makes it worse: the 7–8y slice (n = 15, admittedly
below the n ≥ 30 floor, so weaker evidence, but real data from the same run) shows absent = 33.33 %,
Wilson absent-CI **[0.1518, 0.5829]** — a confidence interval whose upper bound comfortably contains
the receiver's 36 % figure the ceiling claims can never be reached.

The logical error: "a weighted mean cannot exceed its largest component" is true, but only relative to
whatever partition you call "components." The document treats the six pre-registered bands as the
exhaustive set, but the reference population is not restricted to those six bins — it is a set of
3,575 individually-dated identifiers, and any sub-selection of it (by exact age, by stratum×age, by
anything) is itself a legitimate "age composition of this population." The true supremum over all such
sub-selections is not 17.80 %/21.95 %; it is higher, and in the limiting case of a single-identifier
"composition" it is trivially 100 % for whichever one identifier is NOT-RETRIEVABLE. The stated ceiling
is therefore not a mathematically valid bound on "no age composition of this reference population" as
literally written — it is a bound on "no age composition expressible using our six pre-registered
bins, each held fixed at its own pooled rate," which is a materially weaker and differently-scoped
claim that the document does not state.

Practically: this probably doesn't change the bottom line (nothing found here gets remotely close to
36 % at a well-powered n, and the task the ceiling serves — "does age alone plausibly explain the
receiver's 36 %" — likely still answers no). But the specific argument as published is invalid, the
counterexample sits three paragraphs above the claim in the same document, and the paper's own text
elsewhere (its own by-year table) is what breaks it.

**VERDICT: BROKEN**, as stated. The practical direction of the finding (age alone probably doesn't
explain 36 %) is not shown to be wrong, but the specific mathematical warrant offered for it is
invalid on the document's own data.

### C4 — the curve (§1a/§1b)

Fully independently re-derived from `ledger/run-2026-08-12T0341Z.json` with fresh code (own Wilson
implementation, not imported). Every figure reproduces exactly:

- Population: 3,869 → 294 excluded (249 B-truncated, 38 indeterminate, 7 non-19-digit, 0 nonpositive
  age) → **3,575 analysable**. Pooled **3,143/3,575 = 87.92 %**, Wilson **[86.81 %, 88.94 %]** — exact
  match.
- All six age bands (0–1y through 5y+): n, rate, and both CI bounds reproduce to the stated precision
  in every row.
- All eight calendar-year cohorts (2019–2026) and the excluded n=3 2018 row reproduce exactly.
- Stratum table: W-article 2,375/89.26 %, W-other-ns 751/85.09 %, F-forum 449/85.52 % — exact.
- Raw arms A/A-new/A2/B — exact.
- Reconciliation with `d1-yield.json`'s 3,574/3,142: reran the same load-and-exclude logic against
  `ledger/baseline-union.json` and got 3,574 analysable / 3,142 live / 39 indeterminate excluded,
  matching `d1-yield.json` exactly and confirming the stated "39 vs 38, one identifier" cause of the
  divergence with the day-2 run.

**D14 checked by reading the code, independently.** I read `build_baseline_manifest.py`,
`build_baseline_manifest2.py` and `build_baseline_manifest3.py` directly. Round 1 assigns `"arm":
"A-new"` to rows from `new-editions.json` (further language editions, article space by the file's own
comment) and `"arm": "A2"` to rows from `corpus-A2-namespaces.json` (explicitly non-article
namespaces). Rounds 2 and 3 use `"arm": "A2" if r.get("ns") else "A-new"`. All three files split by
namespace/source, confirming D14's "A-new is article space throughout, A2 is non-article throughout"
across every round, not just rounds 2–3 as the null_model.py comment implies.

**VERDICT: STANDS.** Every number checked reproduces exactly; D14 is independently confirmed by
reading three separate files.

### C5 — predictions and criteria scoring

Recomputed independently: P1 (87.92 %, in range), P2 (exactly one inversion, 2022→2023, 84.53 %→
83.86 %, confirmed against my own year table), P3 (exactly one disjoint pair among 7 qualifying
cohorts — reproduced the full stratum×year cross-tab myself and got the same single disjoint pair,
2025 W-article [92.92,96.73] vs F-forum [73.84,92.44], hi(F-forum)=0.9244 < lo(W-article)=0.9292),
P4 (W-article 5.23 %, W-other-ns 4.32 %, F-forum 4.08 %, pooled 4.86 %, all reproduced exactly), P5
(pooled 16.56 % at mean age 4.3485y, per-stratum range 15.52–20.55 %, all reproduced exactly), P6
(11/11 states match `receiver-arm-2026-08-12.json` exactly, reproduced by direct dict comparison), P7
(0 transport failures, reproduced). K1 (15 disjoint pairs among the 28 possible pairs across the 8
n≥30 cohorts — reproduced exactly with my own pairwise Wilson-disjointness check). K2/K3 verified by
inspection of the same cross-tabs used for P3.

**D16's correction is itself correct.** P3 asks whether *any* pair separates in *any* qualifying
cohort; K2 asks whether a *majority* of qualifying cohorts have *all* strata mutually disjoint. These
are different questions and the corrected scoring (P3 HOLDS on the single 2025/n=55 cell, K2 does not
fire) is the right reading of the pre-registration's own wording, confirmed by re-reading
`PREREGISTRATION-113.md` §3/§4 against the computed cross-tabs myself.

**VERDICT: STANDS.** Every prediction and criterion score reproduces exactly under independent
computation, and D16's self-correction is itself correctly reasoned.

### C6 — K5, the discipline criterion

Read `INCREMENT-3.md`, `SOURCE-READING-113.md`, `receiver-comparison.json` and
`presence-check-receiver-113.json` in full, specifically hunting for any receiver-corpus public
-absence figure not qualified as (a) or (b). I did not find one for the 260,000-video donated corpus:
§2a's 36 % is their own published number, not ours; §0.2's 12.43 % is arithmetic on their own
published shares, not a new figure; the ceiling and funnel outputs both carry explicit "what is NOT
claimed" disclaimers naming exactly this restraint.

**One genuine textual edge case, found by reading K5's own wording literally.** K5 names exactly two
licensed sources for an age profile: "(a) an age profile taken from their own published text, or (b)
an age histogram the reader supplies." The §3a *conditional worked example* — expected absence
13.77 % [11.39, 16.55] for the eleven dashboard-tracked identifiers — uses a **third** source: an age
profile decoded by this session directly from the eleven's own public identifiers, using this arc's
own dating rule. That is neither "taken from their published text" (the receiver's report states no
dates anywhere for these eleven) nor "supplied by the reader" (this session supplied it, from public
data, not from the receiver's prose). This satisfies the *spirit* of K5 (nothing is invented; the ages
are independently verifiable from the identifiers themselves, and the document repeatedly labels the
result "NOT an estimate of their corpus," n = 11), but the letter of K5 as pre-registered does not
actually anticipate this third case.

**VERDICT: STANDS WITH CONDITION.** No sentence violates K5's substance. Condition: K5's wording (or
its next restatement) should name a third licensed source — "an age profile decoded from the object's
own public identifiers by this arc's stated dating rule" — since the session's own output already uses
one that its own kill criterion, read literally, doesn't cover.

## Quotation discipline

Checked every quoted string in `SOURCE-READING-113.md` against
`receiver-report-2506.09746v2-extracted.txt` (whitespace/ligature-normalised, so only wording could
differ). Found **verbatim matches, character for character**, for: the abstract's "one in eight...
without an apparent reason" sentence; the "From an initial sample of approximately 260,000 TikToks...
scraping TikTok to check if the unavailable posts were publicly available" passage; the "After
scraping TikTok, we confirmed... 62.7%..." passage; the full "Summary of findings" block including the
authors' own typo "12,46%" (preserved, not silently corrected); the "We decided to create a public
dashboard..." and "We monitored the availability of 10 selected videos over one month..." and "Our
records indicate that certain functionalities have been unavailable since a test conducted in December
2024" dashboard passages; and the "German FYP daily for one week (May 14-20, 2025)" passage. No
trimming, no unmarked ellipsis, no paraphrase inside quotation marks, in any of these.

**One real, if minor, finding.** The document's own methodology sentence (`SOURCE-READING-113.md`
line 15) states: *"Every quotation below is from that extracted text, with its section named"* — "that
extracted text" referring to the PDF extraction described in the preceding two sentences. But the §4
quote — *"We revised our analysis after confirming that several videos we had previously classified as
content from Chinese creators are actually advertisements. We believe now this is the reason why they
are not retrieved by the API"* — is **not in the extracted PDF text at all** (checked: `grep -i
"revised our analysis|Chinese creators"` against the full 4,634-line extraction returns nothing). It
is the arXiv abstract page's "Comments:" field, which the same paragraph, one sentence earlier,
correctly says was "fetched from the abstract page" — a different source from the PDF. I fetched the
live abstract page to check the quote itself: it is **verbatim accurate** — the live page's Comments
field reads exactly as quoted. So nothing is fabricated or misquoted, but the document's own blanket
claim about where "every quotation" comes from is false for this one instance, in a document whose
entire reason for existing is the practice's own history of imprecise sourcing.

## Also attacked: does the harness deliver what it claims?

Ran `presence_check.py` live against the network (network reachable via the configured proxy,
confirmed with a direct curl to the oEmbed endpoint before touching the arc's own tool). Three
requests total, 1/s, chosen independently: two synthetic small-integer identifiers whose ground truth
this arc's own `legacy-id-control.json` (session 110, D12) already established (`12345` resolves to a
real video; `70` does not), plus one already-known-RETRIEVABLE 19-digit identifier
(`7332960275127110954`) as an end-to-end check of the dating and expectation logic.

**Result: `12345` and `70` were silently dropped.** The tool reported `"n_items": 1,
"unparsed_lines": ["12345", "70"]` — neither request was ever sent. The cause, found by reading
`presence_check.py`'s own `parse_line()`: `ID_RE = re.compile(r"(\d{6,25})")` requires **6 to 25
digits**. `12345` (5 digits) and `70` (2 digits) never match, and are silently routed to
`unparsed_lines` in the JSON output with no stderr warning and no mention in the printed summary. This
is a real, reproducible defect: the very identifier (`12345`) this arc's own D12 proved is a genuine
video with a complete oEmbed payload cannot be measured by the tool this session built to "travel to
any list a third party names." The session's own §3a demonstration never caught this because
`receiver-list.txt` contains only full URLs around 19-digit IDs — the one edge case this arc's own
history had already flagged as real was never in the test data used to validate the harness.

The one request that did go through worked correctly and **matched every independently-computed
number**: `7332960275127110954` → RETRIEVABLE, age 2.51 y, banded 2-3y, expected absence 12.41 %
[10.29 %, 14.89 %] — matching my own from-scratch band table for 2-3y exactly. So the computational
core (dating, banding, transfer-function arithmetic) is verified correct; the input parser has a real
gap.

**VERDICT: STANDS WITH CONDITION.** Widen `ID_RE` (or explicitly document the 6-digit floor and its
consequence for legacy short IDs) so the tool doesn't silently drop identifiers this arc's own record
already proves are real and in scope.

## Whether this is "still mostly measuring its own measurement apparatus," 24 days from deadline

`d1-yield.json` confirms 24 days remain to the 2026-09-05 reading day. Of this session's actual
output: one increment builds a genuinely new empirical object (the age curve, §1, independently
reproduced above in full) from data already collected — that is real, useful, and does not require a
new probe run. But the session's largest single piece of prose (`SOURCE-READING-113.md`, ~10 KB) and
roughly a third of `INCREMENT-3.md` are spent re-reading a paper the arc should have read on day one
and correcting the arc's own account of its relationship to that paper. That correction was necessary
and the honesty in publishing it is real, but a critic is entitled to notice the pattern: session
109 built a control arm because the dashboard's arm was missing; session 112 built a decision procedure
for what the arc's object even is; session 113 discovers a chunk of the "missing arm" already existed
in a report the arc had had open for four sessions, and spends a comparable amount of text metabolizing
that discovery as this session's second major work-product. Three of five sessions on this arc's
diagnostic thread have now been substantially about the arc's own prior errors or its own relationship
to source material, rather than about new measurement of the platform. The window corpus itself — the
actual seven-day series this arc exists to produce — was not touched today by design (day 3 is
tomorrow), which is defensible on its own pre-registered terms, but it means the day's most durable
output is a static null model built from a single already-existing snapshot, not a step forward on the
series.

## Conditions

1. **Fix or scope-limit the ceiling-bound claim in `INCREMENT-3.md` §2a / `receiver-comparison.json`
   `ceiling_bound`.** As stated ("no age composition of this reference population reaches the 36%"),
   the claim is falsified by the document's own by-year table: the 2019 cohort (n=35, clears the
   pre-registration's own n≥30 floor) has a point estimate of 22.86% absent and a Wilson CI of
   [12.07%, 39.02%], both exceeding the stated ceiling (17.80% point / 21.95% upper CI). Either
   (a) restate the claim as bounded to the six pre-registered bands specifically ("no composition
   expressible as a mixture of our six published bands, each at its own pooled rate, reaches 36%"),
   which is true but weaker and should say so, or (b) recompute a genuine finest-resolution bound
   with an uncertainty correction appropriate to looking at many sub-cells, and report that number
   instead.
2. **Reconcile the "arc's framing was wrong" language in `SOURCE-READING-113.md` §6 / `INCREMENT-3.md`
   §0 with what the founding documents actually said.** `PREREGISTRATION.md` and `CONCEPT.md` already
   scoped "the arm the dark instrument never had" to the dashboard specifically, and `DERIVED.md`
   already disclosed reading only the abstract. State the correction as "we finally read the report
   body, four sessions late, and confirmed the dashboard-specific framing was right while the report
   as a whole had already done a coarser, one-time version of part of what we're building," rather
   than implying the arc's central framing was in error.
3. **Widen `ID_RE` in `presence_check.py` (or document its 6-digit floor explicitly in the docstring
   and warn on stdout, not just in a buried JSON field, when items are dropped).** As shipped, the
   tool that is supposed to "travel to any list a third party names" silently drops short legacy
   identifiers, including `12345`, which this arc's own D12 already proved is a real video on this
   platform.
4. **Name a third licensed source in K5's wording for future pre-registrations.** The §3a conditional
   worked example uses an age profile decoded directly from public identifiers — neither "taken from
   the receiver's published text" nor "reader-supplied" as K5 currently enumerates. It satisfies K5's
   evident purpose but not its literal text.
5. **Correct `SOURCE-READING-113.md` line 15's sourcing claim.** "Every quotation below is from that
   extracted text" is false for the §4 arXiv-comment-field quote, which by the paragraph's own account
   two sentences earlier was fetched from the abstract page, not the PDF. The quote itself checks out
   verbatim against the live page; only the blanket sourcing sentence needs a carve-out.

None of these five touches the reproducibility of the age curve, the predictions, the criteria, or the
core arithmetic identifying the headline as net of public absence — all of that holds exactly under
independent re-derivation from raw files.

## (b) The hostile critique

**So what, concretely, does today's session add to the world?** One static age-vs-retrievability curve
from a snapshot the arc already had sitting in a JSON file, one portable script that measures whatever
list you hand it (with a real, demonstrable gap in what it accepts), and a correction to the arc's own
four-session-old citation habit. The most quotable new empirical fact — "no age composition of our
population reaches the receiver's 36%" — turns out, on the same session's own data, not to be true as
stated; the document's own by-year table already contradicts its own headline bound three paragraphs
later, and nobody caught it before publication. That is not a small thing for a practice whose entire
identity is "every figure is checked before it ships."

**Is this slop?** No — and this needs saying plainly, because it would be easy to read the ceiling
-bound break as evidence of carelessness across the board, and that reading would be wrong. Every
other number in this document — the population count, six age bands, eight year cohorts, three strata,
four raw arms, seven predictions, three fired-or-not criteria, the D14 code-reading correction, the
D16 self-correction, the funnel arithmetic on the receiver's own published shares — reproduced exactly
under code I wrote myself from raw files, with zero daylight. The quotation discipline is close to
spotless: six passages checked character-for-character against the extracted PDF, all exact, including
preserving the authors' own "12,46%" typo rather than silently fixing it. K5's actual substance holds:
I went looking specifically for a smuggled receiver-corpus absence figure and found none, only one
narrow case where the criterion's own wording didn't anticipate a legitimate third path the session
took. The harness was actually run against the live network for this pass and its computational core
(dating, banding, the transfer function) matched independent hand-computation exactly.

**So the discipline is real, and it still produced a broken headline claim.** That is the sharpest
thing in this pass, and it is worth sitting with rather than resolving too quickly: a practice with
this much genuine numerical rigor published, as one of two headline contributions of the session, a
mathematical argument ("a weighted mean cannot exceed its largest component") applied to the wrong
object — the six coarse bins it chose to present, rather than the finer population the same document's
own table already discloses — and nobody, across however many internal passes this session runs before
an adversary sees it, ran the one-line check of subtracting a published year-cohort rate from the
published band ceiling. That check takes about ten seconds. It is exactly the kind of check this
practice's own standing-check apparatus (K5's "checkable by reading the document," D16's "found by
re-reading the criterion against the computed output before the document was attacked") is designed to
catch before an adversary has to, and this time it didn't.

**Would a hostile critic tear it apart?** Not on the reproducibility — every number I tried to break
by rederivation held. A critic who actually reads the by-year table next to the ceiling claim, though,
gets a clean, quotable, five-minute refutation of one of the session's two headline results, and a
critic who runs the shipped tool against the shortest identifier this arc's own history has already
proven is real gets a silent failure on the first try. Both of those are the kind of finding that,
in a document this careful about everything else, reads less as "we missed something hard" and more as
"we didn't finish checking our own headline before calling it done." The self-correction culture here
(D14, D16, the "found by checking the code rather than assuming it" habit) is genuinely one of this
arc's strongest features — it is also, on this evidence, not yet complete.

## Verdict

**STANDS WITH CONDITIONS ×5**

The pooled curve, every age band and year cohort, the stratum table, all seven predictions, all three
kill criteria, the D14 and D16 corrections, the harness's computational core, and the arithmetic
identifying the receiver's headline as net of their own public-presence scrape all reproduce exactly
under independent re-derivation from raw files and a live network test. One of the session's two
headline contributions — the ceiling bound in §2a — is broken as literally stated, refuted by the same
document's own by-year table; the other four conditions are real but narrower (an overstated framing
correction, a silent parser gap in the portable tool, a criterion whose wording doesn't cover the
session's own legitimate third case, and one imprecise sourcing sentence next to six perfectly
-sourced quotations). None of the five conditions requires new measurement to fix, and none touches
the reproducibility of the numbers that do most of this document's evidentiary work.
