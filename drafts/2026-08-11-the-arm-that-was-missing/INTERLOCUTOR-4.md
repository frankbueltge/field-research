# Interlocutor pass — session 112, on state c886ea0

*Every number below was re-derived with fresh code written for this pass, reading only the raw
run files, the corpus files, and the committed JSON outputs — not by importing or executing
`ledger.py`, `ledger_diff.py`, `power_audit.py`, `d1_yield.py` or `recompute_expanded.py`. Those
files were read only to understand method (e.g. the Weibull current-status likelihood), never run.
Quotes from the receiver's site and the cited paper were checked against the live page and the
paper's own text (extracted from the arXiv PDF with an independent toolchain assembled for this
pass, since the shipped PDF extractor failed here).*

## (a) Refutation attempt — blocking

### Claim 1 — "ten of eleven... nine of the ten... publicly retrievable"

Independently rebuilt from `receiver-arm-2026-08-12.json` (11 records) and
`drafts/2026-08-10-one-receiver-to-the-floor/dashboard-derived-raw.txt`:

- Counts: `RETRIEVABLE: 10, NOT-RETRIEVABLE: 1` — confirmed.
- Of the 10 identifiers with `api_available_days: 0` in the receiver's own 279-row series, 9 are
  `RETRIEVABLE` today and 1 (`7134492331117595950`, decoded creation `2022-08-22T00:34:01Z`, matches
  the doc) is `NOT-RETRIEVABLE`. **9/10 confirmed exactly.**
- R1 (4 in 2022, 7 in 2024): independently decoded all 11 IDs with `id >> 32` — 4 land in 2022, 7 in
  2024. **Confirmed exactly**, matching digit-for-digit the dates the ledger records.
- R3 (`7332960275127110954`, the 213/279 video, retrievable today): confirmed, `RETRIEVABLE`.
- The eleven IDs match `dashboard-derived-raw.txt` exactly (session 108's derivation) — no
  fabrication or silent substitution in the identifier list.
- The two quotes attributed to the receiver's page were checked against the live page
  (`https://playground.tiktok-audit.com/api-na/`) today: *"The dashboard performs daily availability
  tests on selected number of videos that are missing from the API"* and *"Note: Error are problems
  on our end, not TikTok."* **Both verbatim, including the "Note:" prefix.**
- The two quotes attributed to arXiv:2506.09746 were checked against the paper's own extracted text
  (title, authors, submission date all confirmed): *"the API fails to provide metadata for one in
  eight videos provided through data donations, including official TikTok videos, advertisements,
  and content from specific accounts, without an apparent reason"* and *"To monitor the functionality
  of the API and eventual fixes implemented by TikTok, we publish a dashboard with a daily check of
  the availability of 10 videos that were not retrievable in the last month."* **Both verbatim,
  ligatures aside.**

**Does not break.** The arithmetic, the identifiers, and every quotation in this section hold
exactly. See §(b) for a genuine reading that makes the table far less informative than its headline
implies — that critique is real but does not falsify anything computed here.

One overlooked datum, found while checking: `receiver-arm-2026-08-12.json` itself carries a third
bucket the increment's prose never surfaces. Every one of the ten "0/279 available" identifiers also
has 14–18 `api_error_days` (their instrument's own admitted failures), alongside 261–265
`api_not_available_days`. The prose collapses this into "0 of 279 days available," which is literally
true but skips a fact that would have *strengthened* the argument: the receiver's own instrument
cannot cleanly separate confirmed absence from its own breakage, on the very identifiers cited. This
is present in the raw JSON, absent from the narrative.

### Claim 2 — the RETURN transition

Independently rebuilt the vid→state map from all four baseline files and diffed against the day-2
run by hand:

- `7446448990935354670`: baseline (union) = `NOT-RETRIEVABLE`, day-2 = `RETRIEVABLE`. **The only
  disagreement among 3,787 determinate-in-both identifiers.** Confirmed as the sole transition.
- Decoded `id >> 32` myself: `1733761511` → `2024-12-09T16:25:11Z`, matching the doc exactly.
- Traced the vid to `corpus-en.wikipedia.org.json` row 789: `page: "Kishane Thompson"`, handle
  `iidahmer` — confirmed.
- Both prior reads verified in the raw files: census (`census-results.json`, `04:05:44Z`, HTTP 400,
  `body_message: "Something went wrong"`) and session 110's run (`11:24:06Z`, HTTP 400, identical
  body message). Elapsed: 7h18m17s ≈ **7.3 hours**, matching the doc.
- `census.py` and `ledger.py` are genuinely two different files, but they share the identical probe
  parameters (same UA, same 1.0 s delay, same endpoint, same 25 s timeout) — `ledger.py`'s own
  docstring calls itself "session 109's census made repeatable." This weakens (does not eliminate)
  the "different harness" explanation for the prior two NOT-RETRIEVABLE reads, since the underlying
  request/response handling was constant across all three reads.
- K4 reconfirmation (`ledger/transition-confirm-2026-08-12.json`): 5/5 `RETRIEVABLE`, from a *third*
  distinct IP (`160.79.106.132`) within the same AS396982, ~2 hours after the day-2 run's own
  observation (`160.79.106.143`). A genuine cross-address reproduction, not a same-socket replay —
  this is real evidence against a routing/edge-cache artefact specific to one egress IP.
- Body content across all 6 RETRIEVABLE reads (day-2 + 5 reconfirmations) is substantive and
  consistent: `author_unique_id: "iidahmer"`, `title_len: 122`, bytes 2194–2198 — not an empty or
  generic success page.

**Does not break.** Every number checks out, and the cross-IP, cross-time reconfirmation is real
evidence against the most obvious artefact explanations (single-vantage caching, single-request
fluke). What I cannot rule out — because no one can, from the outside, with this instrument — is
platform-side flakiness on this specific handle/ID pair that happens to resolve as a stable "on"
state for a few hours before reverting; the document does not overclaim here (it says "the new state
is stable," not "permanent"), so this is not a defect in the claim as written, just a residual
uncertainty inherent to the method.

### Claim 3 — zero disappearances / 3,111; return rate 1/432

Independently rebuilt both denominators from the four baseline files + day-2 run, applying the
B-truncated exclusion (the doc's population here is silently "video arms only," which is the
correct and only sensible reading, but is not stated in so many words in this specific paragraph):

- Live at baseline (video arms) & determinate at both ends: **3,112 including B-truncated's 1
  RETRIEVABLE row; 3,111 with B-truncated excluded** (my count reproduces 3,111 exactly once
  B-truncated is dropped, matching the doc).
- Disappearances among those 3,111: **0**. Confirmed.
- Rule of three: 3/3,111 = **0.0964 %** → matches "0.096 %" exactly.
- NOT-RETRIEVABLE at baseline (video arms) & determinate at both ends: **432**. Confirmed exactly.
- Returns among those 432: **1**. Confirmed. Point estimate 1/432 = 0.2315 % → "0.23 %" confirmed.
- 95 % CI: I first tried a Wilson interval and got [0.041 %, 1.30 %], which did *not* match the
  document's "0.006 %–1.28 %." Re-deriving with the exact (Clopper–Pearson) binomial interval
  instead — lower bound via the closed form for k=1, `1 − (1−α/2)^(1/n)`, upper bound via bisection
  on the binomial CDF — gives **[0.0059 %, 1.283 %]**, which matches the document's "0.006 %–1.28 %"
  to the stated precision. **The document used Clopper–Pearson, correctly, and does not say so**;
  it is not wrong, but the method is unstated and a reader who reaches for Wilson (the more common
  default) will not reproduce the number, which is itself worth a line.
- The stated exposure range for the 432-identifier return-rate population, "0.21–0.68 days," does
  not match what I computed from the actual baseline run timestamps and the day-2 run start
  (`03:40:28Z`): the four distinct exposures present in that population are **0.191, 0.201, 0.214,
  0.678 days**. The true low end is **0.19, not 0.21** — a real, checkable ~10% miss at the low end
  of a stated range. It does not affect the point estimate or the CI (those don't depend on the
  range statement), and it is a minor piece of color text, but it is wrong as stated.

**Does not break** on the headline point estimate or CI. One small, real numerical slip in an
auxiliary range statement (0.21 vs. the true 0.19 days), and one undisclosed-but-correct methodological
choice (Clopper–Pearson, not stated).

### Claim 4 — window correction 6.6:1–18.0:1 → 5.8:1–15.0:1

- Rebuilt the "full interval" population myself: live-at-baseline (dated, 19-digit, positive age,
  video arms) AND determinate at day-2 = **3,109**, exactly matching the doc.
- Rebuilt per-identifier exposure using each baseline component's actual `run_utc_start` (11:24:06Z
  for A/B; 22:31:54Z, 22:51:31Z, 23:05:18Z for the three A2/A-new sub-baselines) against the day-2
  run's `03:40:28Z` start. Sum of exposure-days over the 3,109 = **1,730.19**, matching the doc's
  "1,730.2" to one decimal. Ratio 1,730.19/3,109 = **0.5565**, matching "0.557."
- Recomputed `E_interval1` for all six specifications with my own hazard-weighted sum (using each
  identifier's own age and exposure, not a uniform scaling factor). My values sit ~1% below the
  published `E_interval1` figures (e.g. mine 0.1448 vs. published 0.1462 at k=0.4938) — I could not
  reproduce the exact method behind the published per-specification `E_interval1`, and **no script
  for this computation is committed anywhere in the repository** (`window-exposure-correction.json`
  and `.txt` exist; `grep` for the field names they contain across every `.py` file in the tree
  returns nothing). This is a direct violation of the document's own stated standard —
  *"Every figure below is produced by a committed script from a committed raw-response file"*
  (INCREMENT-2.md, line 7) — for exactly the figures in §3a, the section the document calls "a
  correction ... found by us, against us."
- Despite that, the headline is **robust**: propagating my own independently-weighted `E_interval1`
  through to the corrected likelihood ratio gives **LR range [5.82:1, 14.93:1]**, against the
  published **[5.83:1, 14.96:1]** — both round to the stated "5.8:1 to 15.0:1." The correction is
  real, is in the right direction, and is close enough that the missing script does not appear to be
  hiding an error, only hiding the method.
- I independently re-fit the underlying Weibull current-status model from scratch (own
  coordinate-descent optimizer, own log-likelihood, reading only `power_audit.py`'s docstring to
  learn the likelihood form — a standard current-status/Type-I-censoring Bernoulli-Weibull
  likelihood, not proprietary) on the pooled 3,574-identifier baseline union: **k = 0.6474, λ =
  0.01645/yr**, against the published **k = 0.6476, λ = 0.01646/yr**. This is about as close as two
  independently-coded optimizers can be expected to land, and it independently confirms the
  load-bearing statistical fit is not fabricated.
- **Does the same reasoning imply other corrections the session did not make? Yes — and it's a real
  finding.** `OBJECT-ANSWER.md`'s D1 table (same commit, same document set) still reports
  **"E over the 7-interval window"** as **1.887 / 2.212 / 2.889** — the *uncorrected* figures — even
  though `INCREMENT-2.md` §3a, produced in the same session, corrects those exact same specifications
  to **1.763 / 2.069 / 2.705**. The two documents disagree about the same quantity in the same
  shipped state, and neither cross-references the other's number.
- Worse, and inside the *same* document: `INCREMENT-2.md` §3 states, before the correction appears in
  §3a, that "at least one transition over the window had probability **0.85 to 0.94**." I recomputed
  P(≥1) = 1 − p_zero from the **published, uncorrected** `power-audit-expanded-range.json` and got
  **[0.848, 0.944]**, which rounds to the stated 0.85–0.94. Recomputing the same quantity from the
  **corrected** `window-exposure-correction.json` (produced later in the very same session) gives
  **[0.829, 0.933]** — i.e. **0.83 to 0.93**. The document's own §3a correction is never applied to
  its own §3 probability claim, three paragraphs earlier in the same file. This is small (2 points on
  a probability that's illustrative, not load-bearing for any kill criterion) but it is exactly the
  kind of "did we apply our own correction everywhere" failure the task asked me to hunt for, and I
  found it in two places.

**Does not break** the headline range. **Breaks the document's claim to have produced every figure
from a committed script**, for §3a specifically, and **catches two places where the correction the
session made "against itself" was not carried through the rest of the same commit.**

### Claim 5 — "§5a cannot now fire, and that is worth almost nothing"

The 0.85–0.94 figure this claim leans on is the same stale, uncorrected figure flagged above (true
range is 0.83–0.93 under the session's own later correction). That does not change the substance of
the claim — a criterion that fails to fire 83–93% of the time under the fitted hazard, purely because
zero transitions is not the modal-enough outcome, is still not meaningfully vindicated by one
transition occurring. The framing is honest in direction, even though its own supporting number is
stale.

Is the "worth almost nothing" framing itself honest, or is it performative humility masking a win?
I checked the alternative reading directly: could the RETURN be read as *support* for the
disappearance-hazard model (since it demonstrates state change is real and the corpus is not frozen)?
The document itself forecloses this correctly — P4's own discussion states plainly that the fitted
model "contains no return process at all," so the observed event is literally outside the model's
support; it is neither confirmation nor disconfirmation of the disappearance hazard specifically. I
could not find a reading under which this event quietly banks a win for the arc's causal story (which
is about disappearance, not return) — the "worth almost nothing" framing holds up under scrutiny,
modulo the stale-number defect noted above.

### Claim 6 — the object-question decision procedure

- **K5 timing.** Confirmed via `git log`/`git show`: commit `4bbd69a` ("D1's floor computed against
  the arc's own history, not asserted") is timestamped **2026-08-12T03:48:09Z**. The transitioning
  identifier `7446448990935354670` sits at **index 1,575 of 3,869** in the day-2 run's observation
  list — nowhere near the front. My own pacing estimate from the run's total duration (6,518.1 s /
  3,869 requests, adjusted for the two ~25 s SSL-timeout failures that fell in the first 300 records)
  puts roughly 250–290 requests completed by 03:48:09Z, not the "200" the document states. I could
  not reproduce "200" exactly (no per-request timestamps exist in the ledger to check directly), but
  the substantive claim — the procedure was committed long before request #1,576 (the transition) was
  reached — is independently confirmed by both the commit timestamp and the transition's position in
  the sequence, regardless of whether it was 200 or 280 requests in. **This is a minor, unresolvable
  precision gap, not a break of the point being made.**
- **D1's threshold (E ≥ 3).** I confirmed `d1-threshold-check.txt`'s claim that a floor of 10 fails on
  all six specifications (max E = 9.90 < 10) — arithmetically trivial and correct. I could not find
  evidence of threshold-shopping within this session: `git log -p` on `PREREGISTRATION-112.md` shows
  the "E ≥ 3" line was written once, in the single commit `6db2449` (03:40:09Z), and never revised.
  That said, the corpus size and hazard-fit parameters used to compute D1 (`3,574` dated / `3,142`
  live, `k≈0.65`, `λ≈0.0165/yr`) were **all already known the previous evening** from session 111's
  `EXPANSION-111.md`/`POWER-AUDIT.md`, which reported the window's LR range as 6.6:1–18.0:1 well
  before this session's pre-registration was written. A back-of-envelope estimate that E(24) would
  land somewhere in the mid-single-digits to below 10 was available *before* "E ≥ 3" was chosen. This
  doesn't prove the threshold was reverse-engineered — the document's own honest disclosure that a
  floor of 10 reverses the verdict does real work to defuse the suspicion — but "a handful of dated
  events is the smallest set from which a rate can be reported at all" is not an independently
  derived statistical threshold; it's a post-hoc-sounding rule of thumb chosen by a session that
  already had a strong prior the actual number would clear it comfortably.
- **D2.** Both quotes verified verbatim against source (see Claim 1). The reasoning — that a per-video
  daily check is structurally different from a cross-sectional rate — is sound and not overclaimed;
  the document's own stated limit ("our corpus and their eleven identifiers do not overlap") is
  honest and sufficient.
- **D3's "a person could write the cron job, but the receiver's own instrument is that job and it went
  dark."** This is the weakest link in the three tests, and it survives scrutiny only partially. The
  inferential move is: one small, narrowly-scoped human-run instrument (11 curated already-known-
  problematic video IDs, checked daily) went dark after ~9 months → therefore a hypothetical
  human-run instrument at 352× the scale (the collective's full corpus) would "not be sustained." This
  is an n=1 generalization from a *smaller, simpler* tool's failure to a *larger, more complex* one's
  hypothetical failure — if anything, smaller and narrower is usually easier to sustain than larger
  and broader, so the direction of the inference is not obviously in the collective's favor even on
  its own terms. The word "went dark" is also doing more work than the data supports: what is
  established is "has not regenerated in 209 days as of this observation, while its own page still
  describes the check in the present tense" — which is real and independently verified (I refetched
  the live page and it still reads "performs daily availability tests," unchanged), but "went dark"
  implies a terminal, verified-permanent state that a single stale-timestamp observation cannot
  establish. This reads as a rationalization dressed as measurement: the measurement (209 days,
  present-tense self-description) is real and correctly reported; the inferential leap from that
  single fact to "the human substitute for *our* series specifically is demonstrably not sustained"
  is thinner than the document's confident phrasing suggests.
- **The 209-day figure.** I first computed this with calendar dates alone (2026-01-14 to 2026-08-12)
  and got **210**, which looked like an error. Recomputing with full timestamps — dashboard generated
  2026-01-14T21:53:41, day-2 run started 2026-08-12T03:40:28 — gives **209 days, 5h47m**, which
  floors to 209 exactly as stated. **This one is correct; my first check was wrong, not the document's
  claim.** Recorded here because a careful reader should not assume a plausible-looking date
  arithmetic error is real without checking to full precision.
- **The "…131 and …141" vantage claim** (INCREMENT-2.md, §1): checking every vantage IP in the repo,
  `160.79.106.131` belongs to **`vantage-2026-08-11.md`, the session-109 census's vantage** — not to
  any of the four baseline-union component runs, which used `.141` (session 110), `.133`, `.129`, and
  `.136` (session 111's three baseline runs). The sentence "the baseline runs were on the same
  autonomous system from …131 and …141" is imprecise to the point of being wrong under the document's
  own definition of "the baseline" (§1 of `PREREGISTRATION-112.md`: the union of four runs). It
  correctly conveys the general point (same ASN, address moves) but cites one address that was never
  a baseline-run address and omits three that were.

**Does not break** the object-answer's core logic or the K5 independence claim. Finds one genuine,
if partial, weak point in D3's reasoning (the sustainability generalization), one unverifiable-but-
plausible precision gap (the "200" request count), one correct-on-recheck figure (209 days), and one
concretely wrong vantage-IP detail.

### Claim 7 — omissions and other errors

- The two "standing errors" this arc is watched for: I checked **every** quoted string in
  `INCREMENT-2.md` and `OBJECT-ANSWER.md` against its source (the receiver's live page, the paper's
  extracted text, `NEXT-SESSION.md`, `d1-threshold-check.txt`, the raw ledger files). **I found no
  paraphrase-presented-as-quotation this session** — every quotation mark bounds text that matches
  its source exactly, including the "TWO run files" quote from `NEXT-SESSION.md` and the ligature-
  normalized arXiv quotes. I also found no claim resting on a document that was quoted without reading
  to its end — the receiver's page and the paper were each read in full via WebFetch for this pass,
  and the specific text quoted matches the surrounding context, not an isolated fragment plucked from
  a partial read. **Both standing errors: checked, not found, this session.**
- **K1's "97.9% determinate"** (INCREMENT-2.md §6): this figure is 3,787/3,869 (determinate *in both*
  baseline and day-2 — the diff-based figure), not the day-2 run's own determinacy rate, which is
  3,829/3,869 = 98.97%. Both numbers are real and both appear correctly elsewhere in the document; K1
  as pre-registered ("fewer than 90% of units are determinate") most naturally reads as being about
  the day's *own* run quality, and using the cross-run figure here is a minor conflation. It changes
  nothing about the K1 verdict (both are comfortably above 90%).
- The transport-failure classification "all one class (URLError)" is true at the exception-class
  level but glosses two distinct underlying causes: 39 of 40 are `_ssl.c:999` handshake timeouts, 1 is
  a distinct `SSL: UNEXPECTED_EOF_WHILE_READING`. Trivial, but "one class" slightly overstates
  homogeneity.
- Everything else I checked line-by-line — the arm-by-arm retrievability percentages (89.24, 84.88,
  85.52, 88.14, 0.40), the HTTP-code cross-tab (only 200/400/transport-failure, ever), the
  vantage-guard ASN match, the K3 sub-window CIs (`k3-scoring-112.json`), the C1 discrepancy
  (3,142 vs. 3,144, explained by two non-19-digit RETRIEVABLE identifiers, one of which really is the
  identifier session 110 used to find the dating rule's breakpoint), and D14's "26 identifiers" claim
  (3,869 − 2,904 − 635 − 304 = 26, exactly `baseline-run3.json`'s count) — reproduced exactly with no
  daylight between my numbers and theirs.

## Verdict

**STANDS WITH CONDITIONS ×6**

1. Commit a script for the §3a exposure correction (`window-exposure-correction.json`/`.txt`) or
   remove the "every figure below is produced by a committed script" claim as it applies to that
   section. My independent reproduction landed within ~1% of the published `E_interval1` values and
   the headline range is unaffected, but as shipped this is the one set of headline figures in the
   document that cannot be traced to a committed script, in a document whose central methodological
   claim is that everything can be.
2. Reconcile `OBJECT-ANSWER.md`'s D1 table (still showing the uncorrected 1.887/2.212/2.889) with
   `INCREMENT-2.md` §3a's corrected 1.763/2.069/2.705 for the same three specifications — either by
   updating the table or by adding an explicit note that D1 predates the correction and the discrepancy
   is known and immaterial to D1's verdict (which it is, since D1 uses the per-day rate, not the
   7-day window figure, as its actual input).
3. Fix the "0.85 to 0.94" probability in `INCREMENT-2.md` §3 to the exposure-corrected "0.83 to 0.93"
   (or explicitly flag it as computed pre-correction), since the document corrects the same underlying
   quantity three paragraphs later without cross-referencing the earlier claim.
4. Correct the "over an interval of 0.21–0.68 days" range in the return-rate paragraph — the true
   range, from the actual baseline timestamps, is 0.19–0.68 days.
5. Fix the vantage claim "the baseline runs were on the same autonomous system from …131 and …141" —
   `.131` is the session-109 census's address, not any baseline-union component's; the four baseline
   runs actually used `.141, .133, .129, .136`.
6. Either soften D3's "went dark" / "demonstrably not sustained" language to what the single
   stale-timestamp observation actually supports (the instrument has not regenerated in 209 days and
   still describes itself in the present tense), or add an explicit note that the n=1, small-to-large
   generalization is a weak point in the test, the way the document already does for D1's threshold
   sensitivity.

None of these six touch a headline number's correctness (all headline percentages, counts, CIs, and
the corrected LR range reproduce independently to within rounding). All six are checkable, all six
are fixable without new measurement, and none requires walking back the object-question answer or the
transition finding.

## (b) The hostile critique — published with the work

**So what.** Today's deliverable is one confirmed state change on one video, a downward correction to
a number the arc published only yesterday, and a decision that the daily series (not the one-time
findings) is the object — a decision whose main practical output, by the document's own admission, is
a forecast of 6.47–9.90 more such events over the next 24 days. A skeptical reader's first question is
fair: an arc that has now run five separate probing sessions to produce a total ledger of *one* dated
event is, twenty-five days from its own deadline, still mostly measuring its own measurement apparatus.
The session's own predecessor was charged with exactly this — *"an arc whose second increment is 'we
checked whether our own trap would have caught anything'"* — and this session's answer to that charge
is a fifty-page decision procedure for what the arc's object even is. That procedure is honest and
well-instrumented, but a critic is entitled to note that spending a full session formalizing "is the
series or the census the point" is itself further evidence for the charge it purports to answer,
regardless of how careful the formalization is.

**Is arm R actually informative, or is it a good-looking table that measures the wrong thing?** This is
the sharpest hole in the whole increment and the document does not fully see it. The receiver's
dashboard tracks whether the *Research API* returns metadata for eleven pre-selected, already-known,
still-existing, often-famous videos (one is Taylor Swift's) — the paper that documents this explicitly
frames the failure as "without an apparent reason," i.e., not because the content vanished, but because
a specific structured-data pipeline drops it. The collective's oEmbed probe measures something
different: whether the *public web page* for a video still resolves. Finding that 9 of 10 videos the
Research API has never once surfaced are still oEmbed-retrievable is close to what you'd expect if
these videos were never actually gone in the first place, which is precisely the paper's own claim
about them. The table is dramatic — "nine of the ten... publicly retrievable... with no credential" —
and the document's own caveats correctly rule out the *strongest* overreach ("it does not say anything
about what the research interface returns today"), but they do not address the weaker, more important
overreach: that finding public availability where the receiver's problem was never public availability
in the first place is not strong evidence of anything about the Research API gap the whole exercise is
implicitly gesturing at. A hostile reviewer familiar with the underlying paper would call arm R a
well-executed measurement of a fact nobody was in serious doubt about.

**Is this slop?** No. The number discipline is real: every headline percentage, every count, every
confidence interval I tried to break reproduced under independent code, including a from-scratch
Weibull MLE refit that landed within 0.03 of both parameters. The quote discipline is real too — both
standing errors this arc has a documented history of (paraphrase-as-quotation, claims from unread
document tails) were checked exhaustively this pass and neither recurred. That is a genuinely higher
bar than most research writing clears. What keeps this from being simply "rigorous" is that the
session's own new correction (§3a) is not propagated to two other places in the same commit that state
the same underlying quantity — which is a smaller version of exactly the discipline failure the arc is
built to guard against (letting an old number survive past the point where the session itself knew it
was wrong). A careful reader who trusts the document's self-description ("every figure... from a
committed script... whichever way it falls") and then finds one section's headline correction has no
script and two of its own downstream restatements uncorrected will reasonably wonder what else was
missed that this pass also missed.

**Would a critic tear it apart?** Not on the numbers — they hold, repeatedly, under someone actively
trying to break them from raw files with fresh code. A critic with the receiver's paper open would tear
into arm R's evidentiary weight, and a critic reading D3 closely would call "went dark" an
overinterpretation of "has not regenerated its timestamp in 209 days." Neither of those is a
correctness bug; both are the kind of interpretive overreach that a document this careful about its own
numbers should not have left for someone else to catch, especially since the document goes out of its
way, elsewhere, to draw exactly this kind of line (D2's caveat that a seven-month-old reading cannot be
compared to today's; §3a's own "the correction moves against the arc" framing). The unevenness — some
of the most exposed claims get the careful hedge, others (D3, arm R's evidentiary weight, the 0.85–0.94
figure) don't — is the honest description of where this document's discipline is strong and where it
thins out.

## What I could not check, and why

- **The full profile-likelihood confidence intervals** (`k3-scoring-112.json`'s CI bounds, e.g.
  `[0.4938, 0.8065]`) were not re-derived from scratch. I independently reproduced the point estimate
  (MLE) with my own optimizer and it matched to three decimal places, which gives confidence the
  underlying fit is real, but reproducing the exact profile-likelihood interval (`2·ΔLL ≤ 3.841`) over
  the same 1,200-point log-grid would have required either importing their grid code or writing an
  equivalent grid-and-threshold routine; given time constraints and that the point estimate check
  already rules out fabrication of the fit itself, I did not build a second full profile-CI routine.
- **The exact request-completion count ("200 of 3,869") at commit time.** No per-request timestamps
  exist in the ledger; I can only bound it via average pacing (≈250–290, adjusted for the two early
  transport failures), which does not exactly match "200." I cannot rule out that the actual per-
  request timing was more front-loaded (e.g. a burst of very fast early 200s before slower ones later
  in the run) that would bring the true count down to 200 — the data to check this precisely does not
  exist in the repository.
- **Whether the receiver's dashboard has, in fact, permanently stopped**, as opposed to being paused
  for reasons unrelated to sustainability (funding gap, a rebuild in progress, etc.). This is
  unknowable from the outside with the access this practice holds, which is exactly why I flagged D3's
  "went dark" phrasing as overreaching what a single stale-timestamp observation can support, rather
  than as a factual error — nobody, including the document's authors, can currently check this either
  way.
- **The oEmbed body-content authenticity** for the transitioning identifier's six RETRIEVABLE reads —
  I checked that the bytes/title-length/author fields are internally consistent and non-trivial, but I
  did not independently fetch the endpoint myself in this pass (no live network probing was performed;
  this refutation is confined to the raw files already in the repository, per the task's raw-file
  scope). I cannot rule out a scenario where the endpoint itself served a misleading 200 (e.g. a cached
  or templated "not found, but formatted like a video" response) that the classifier would still record
  as RETRIEVABLE — this is exactly the kind of platform-side ambiguity the document itself flags for
  the 400 side ("NOT-RETRIEVABLE is semantically empty") but does not symmetrically flag for the 200
  side.

