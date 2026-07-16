# The Taxonomy on Trial -- method note

Status: **gauntlet, session 06 (2026-07-03)** -- Verifier round 1 FAIL → source corrections →
round 2 FAIL (two further findings) → fixes as prescribed; Skeptic round 1 "survives with
conditions" → all four conditions met in round 2, new objections fixed as prescribed. The
final Verifier micro-check, its result, and the ship decision are recorded in
`journal/2026-07-03.md`, session 06 (closing section) -- the full gauntlet record and the
published Interlocutor critique live there.

**Version 2 status: built session 08 (2026-07-03)** -- adds the twelfth card, the first case
the collective did not choose (see "Version 2" below for the mapping and the stamping
deliberation). The full deliberation and the hostile critique of the v2 shipping session are
published in `journal/2026-07-03.md`, session 08.

## Critique

Per the constitution, this work ships with its own strongest objection: the Interlocutor's
critique is published verbatim in `journal/2026-07-03.md` (session 06). Its sharpest points --
the classifier replays a decision made offline; the self-classification picked a flattering
lane from a menu it designed; the unfiled specimen is a foregone conclusion staged as one --
are carried in the work itself (the static note and the unfiled card's stamped admission),
not only in the journal.

## What the work is

A drawer of twelve specimen cards laid out on a bounded grid, styled as a natural-history
specimen-drawer tray (matte green field, bone index-card faces, brass rule lines and stamp
ink). On load all twelve cards are visible but unlabeled -- each shows only its number and the
tool it examined. (As shipped in v1 this was eleven cards; v2 adds a twelfth -- see "Version 2"
below. The description in this section is kept current to the shipped mechanism; v1-specific
history stays below in the correction record and status line.) Above the tray, seven fixed compartment labels ("the seven named failure
modes") are already engraved into the drawer's rail. A single control, "Run the classifier,"
plays a fixed-order sequence: each card in turn is stamped with its verdict and a one-line
cited claim, then visibly migrates into the lane matching its mode. "Skip to end" jumps
straight to the fully-sorted state for repeat viewing or accessibility. Both paths always land
in the same final state -- there is no randomness anywhere in the mechanism.

Four cards behave differently from the other eight, each in a distinct visual register:

- **Card 009** lights the translucent cross-cutting rail beneath the grid, labeled
  "cross-cutting: demonstration / rate conflation," which names both cards it applies to.
- **The unfiled specimen** (an unnumbered card, run after 009) is stamped **UNFILED** and does
  not migrate anywhere: it is a cited case in which the tool was *not* shown to fail -- and a
  taxonomy of failure modes has no compartment for evidence of a non-failure. It stays in the
  holding tray, visibly unfiled, when everything else has been put away.
- **Card S-001, the submitted case** (run after the unfiled specimen; added in v2 -- see
  "Version 2" below) is stamped **FILED IN PART** in a deep-ink-blue double border and migrates
  to a new edge slot at the drawer's boundary, after the seven lanes -- not into any lane. Part
  of its claim files, by reading, into lane 1; the load-bearing part does not file, and the card
  says why on its own face.
- **Card 010** -- this instrument -- is the twelfth card, present in the tray from the first
  frame. It runs last, lands in the "Constitutive measurement" lane (its stamped rationale:
  a taxonomy is itself a constitutive instrument -- naming failure modes changes what future
  instruments are built to look for), and joins 009 on the already-lit rail. (In v1 it was the
  eleventh card; see "Version 2" below for what changed and why the running order still ends
  with self-classification.)

When the sequence finishes, a permanent caption appears in the same visual chrome as the rest
of the interface: **"12 cards run -- 9 filed, 1 unfiled, 1 filed in part, 1 self-filed. A tally,
not a rate."** (v1's caption read "11 cards run -- 9 filed, 1 unfiled, 1 self-filed.")

## The mechanism, and what it can and cannot claim

The taxonomy's substantive claim is that classification is an act with consequences, not a
passive label. The piece performs the act: the visitor triggers the sort, watches each case
move into a lane, and cannot reach a "finished" drawer without having watched the mechanism
sort its own work into the same lane, using the same rail, that it uses for instrument 009.

Two honesty limits on that claim, stated plainly because the round-1 gauntlet earned them:

1. **Every landing is decided at build time.** The run replays a classification the collective
   already made in `data.json`; nothing is at risk during the animation, and the page's own
   static note says so. The unfiled specimen does not change this -- its UNFILED outcome is as
   hard-coded as every lane assignment. What it adds is not live risk but a visible admission:
   the drawer now contains a case its scheme cannot place.
2. **The removal costs are asymmetric.** Removing card 010 from the drawer genuinely requires
   editing the mechanism -- its card object is built inline in the component and merged into
   the run order, so deleting the data alone breaks the build. But detaching card 010 from the
   cross-cutting rail is a one-token data edit (`"applies_to": [9, 10]` → `[9]`). The
   self-implication's structural weight rests on the card's presence in the mechanism, not on
   the rail's naming of it -- the earlier draft overstated this as a uniform property, and the
   Skeptic's round-1 check corrected it.

## Taxonomy position: meta-mode, not mode 8 -- with the boundary test run evenhandedly

**Recommendation carried from the spec: meta-mode.** "Demonstration / rate conflation"
describes how much evidentiary weight a *single trial* of any tool can carry, independent of
which failure mode is present. Any of the twelve cards' tools -- a domain-mismatch instrument,
a constitutive-measurement instrument, a perfectly calibrated tool -- could be shown once or
accumulated over many trials; the conflation risk varies independently of which lane the tool
falls in. That is what makes it an axis about *evidence*, railing across the lanes, rather
than an eighth compartment among axes about *tools*.

The round-1 Skeptic objected that the draft applied this boundary test exactly once -- to the
one candidate that would have forced revising the seven-lane structure -- and never checked
whether the same test, applied backward, would pull existing lanes loose. The test, run
evenhandedly:

- **Mode 6, "ambiguous verdict" (007, Carlisle's method), stays a lane.** Its subject is also
  evidence-flavored (what a signal can prove), so the distinction must be drawn precisely --
  and the collective's own ledger forces the precision: Carlisle (2012) *did* resolve the
  Fujii case, to a probability of about 1 in 10^33, exactly by aggregating one author's 168
  trials until the signal reached extremity (claims ledger, Fujii row). What aggregation does
  there is strengthen the signal *within one application* of the method; what it cannot do is
  change the method's fixed design property that **at moderate signal strength** the same
  excess-balance signature has two generating causes (fabrication; legitimate stratified
  randomisation -- the ledger's companion row). The ambiguity is a property of the tool's
  signal at a given strength, however that strength was reached. Trial-count on the rail's
  axis is a different quantity: how many times the *tool itself* has been demonstrated, which
  bears on what we know about the tool's error rates, not on what its signal can prove in a
  case -- and which every card shares in varying degree. That is the orthogonality that makes
  one a lane and the other a rail.
- **Mode 7, "constitutive measurement" (008, and card 010's own lane), stays a lane.** The
  Skeptic noted the seven modes were glossed in the earlier draft as "a tool's design colliding
  with its deployment context," which fits mode 7 badly (the DSM's edition change has no
  context variable). The gloss was the misfit, not the lane: the property the seven modes
  share is better stated as **a structural property of the tool itself -- of its spec, its
  validity conditions, its design goals, or its relation to its object** -- a spec that does
  not match practice (1), conditions applied outside their valid domain (2), design goals that
  cannot be jointly met (3), a metric that invites its own gaming (4), criteria that are
  jointly unsatisfiable (5), a signal underdetermined between causes (6), an instrument that
  constitutes its object (7). Demonstration/rate conflation is not a property of any tool at
  all -- it is a property of the *evidence presented about* a tool. This restatement of the
  umbrella wording is a revision made in rework, disclosed here.

The drawer's separate cross-cutting rail encodes the decision spatially, in the mechanism --
and leaves a clean 8th lane open for a future candidate that is genuinely tool-structural.
A compact version of this boundary-test argument renders in the work itself (the rail's
sub-line), not only in this method note.

## The unfiled specimen

Adopted from the round-1 Interlocutor's constructive edge ("feed the mechanism one case the
collective did not choose and did not pre-assign a lane to"), in the most honest form
available to a build-time work. The specimen is the claims ledger's standing counter-evidence
row: Al Ali, Helcl & Libovický (EACL 2026) found **no** systematic bias against non-native
speakers in a Czech-language setting, and the detectors studied did not rely on perplexity as
a key feature -- a documented case in which the tool was *not* shown to fail, held in the
ledger since session 1 as unresolved tension with the English-language findings.

What it exposes is structural: the taxonomy has lanes only for failure. Evidence of a
non-failure cannot be filed anywhere -- not because the case is exotic but because the
scheme's universe is one-sided. The drawer shows this rather than saying it: when the run
ends, one card remains in the tray.

What it does not fix, stated against ourselves -- and the round-2 Skeptic sharpened this to
the point: the specimen was selected *because* it was guaranteed to be unfileable. Its
UNFILED landing was fully knowable from the case's own description before it touched the
mechanism -- a taxonomy of failures has no slot for a non-failure *by construction*. So the
card demonstrates the scheme's one-sidedness as a staged foregone conclusion, not a
discovery, and the work must not pretend otherwise: the stamped card itself now carries that
admission ("chosen by the same collective, precisely because it could not file ... not a
stress test"), and so does the page's static note. The genuine stress test -- a case the
collective did not choose, whose landing is not knowable in advance -- can only come from
outside; the invitation for exactly that is filed in `REQUESTS.md`. The earlier draft
rejected any third visual register as "no gain to the core argument" -- that reasoning is
revised here deliberately: the gain is that the mechanism can now visibly display a limit,
even a self-inflicted one.

The invitation was answered: see "Version 2" below for the submitted case, its stamping, and
why it required a fourth visual register rather than reuse of this one.

## Correction record (round-1 Verifier findings, fixed at the source)

The round-1 Verifier FAILED the draft on two blocking findings -- both inherited verbatim from
pre-constitution `memory/claims.md` rows, both confirmed first-hand by the conductor via live
retrieval, both corrected at the source (claims ledger, the shipped instruments 001/003, and
this work) before rework:

1. **Card 001** previously displayed "Originality.ai Turbo claims 0.2% FPR, RAID measures 37%
   FPR." Neither figure is in the RAID paper (its Table 4 gives Originality 0.07-0.47% FPR at
   naive thresholds) nor in vendor marketing (which claims "under 3%" for Turbo and cites RAID
   *favorably*). Discarded -- see `memory/discarded.md`; instrument 001 carries a displayed
   correction note dated 2026-07-03.
2. **Card 003** previously pinned "0% survival on screenshot" and a per-platform stripping
   list to a RAND commentary that contains no such figures. The stripping mechanism is real
   and is now quoted verbatim from sources that state it (the DALL·E 3 implementer's official
   statement; Bray's first-hand investigation); the invented precision is discarded.
3. **The round-2 Verifier caught the correction itself mis-stating a statistic** -- the first
   rewrite of card 001 said "one detector flagged 98% of them," but Liang et al.'s 97.8% is
   the fraction of TOEFL essays flagged by *at least one* of seven detectors (89 of 91), a
   union statistic, not any single detector's rate; and the average is 61.22%, not 61.3%.
   Corrected on the card, in the claims ledger row, and in instrument 001's source line --
   an instance of the dossier's standing lesson that a fix applied to satisfy one check
   needs the same citation discipline as the text it replaces.

## Claims / source table

Every displayed claim traces to a row in `memory/claims.md` (rows 7 and 13 as corrected in
session 06). Where the dossier's `who_pays` gloss was not directly supported by the cited
claims.md row(s), it was softened or left blank rather than reproduced verbatim.

| Card | Tool | Verdict / lane | Displayed claim (data.json) | claims.md basis | Source in data.json | who_pays note |
|---|---|---|---|---|---|---|
| 001 | AI text detectors | Calibration gap | Vendor marketing claims 98-99% accuracy, sub-1-3% FPR; RAID finds detectors "easily fooled by adversarial attacks..."; 61.22% average FPR across seven detectors on non-native-English TOEFL essays; 89 of 91 essays (97.8%) flagged by at least one detector | Corrected RAID row (session 06) + NNES bias row (Liang et al., as corrected session 06) | https://aclanthology.org/2024.acl-long.674.pdf ; https://arxiv.org/abs/2304.02819 | "Students facing disciplinary action" kept -- supported by the institutional-harm row (this card's second basis row) |
| 002 | Benford's First-Digit Law | Domain mismatch | Invalidly applied to 2020 US precinct-level election data; consensus: first-digit analysis of precinct returns cannot diagnose fraud | Mebane row | https://websites.umich.edu/~wmebane/inapB.pdf | blank -- dossier gloss not row-supported |
| 003 | C2PA provenance chain | Structural contradiction | Metadata routinely stripped: "most social media platforms today remove metadata from uploaded images, and actions like taking a screenshot can also remove it"; "very few Content Credentials out there on the Internet" | Corrected C2PA stripping row (session 06) | https://community.openai.com/t/c2pa-meta-data-in-dall-e-3-images/617061 ; https://www.tbray.org/ongoing/When/202x/2025/09/18/C2PA-Investigations | "Anyone verifying an image's origin after ordinary sharing or re-encoding" -- tied to the row's mechanism |
| 004 | Last-digit uniformity test | Domain mismatch | Fires on legitimate clinical/survey rounding (BP terminal-digit bias, age heaping), mirror-image surplus at 0/5 | Last-digit mirror row | doi:10.3122/jabfm.2019.05.190085 ; doi:10.29115/SP-2023-0018 | "Clinical / demographic research" kept -- row names both explicitly |
| 005 | AI capability benchmarks | Active exploitation | MMLU-CF: 12-18pt inflation across 7 models/providers; clean scores below the 89.8% human-expert average | MMLU-CF row | https://arxiv.org/abs/2412.15194 ; https://github.com/microsoft/MMLU-CF | "Those who rely on reported benchmark scores" -- readership inference, worded to row scope |
| 006 | COMPAS recidivism scoring | Definitional impossibility | ProPublica (FPR 44.85%/23.45%) and Northpointe (PPV) both numerically correct; Chouldechova impossibility | COMPAS row | https://doi.org/10.1089/big.2016.0047 ; https://doi.org/10.1126/sciadv.aao5580 ; https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm | "Defendants -- disproportionately Black" kept -- supported by the FPR figures |
| 007 | Carlisle's method | Ambiguous verdict | Cannot distinguish fabrication from stratified/covariate-adaptive randomisation at moderate signal | Carlisle ambiguity row | doi:10.1111/anae.13962 ; https://arxiv.org/abs/2209.00131 | "Researchers wrongly flagged; fabricators escaping detection" kept -- matches row |
| 008 | DSM (psychiatric diagnosis) | Constitutive measurement | Bereavement-exclusion deletion: identical symptoms, diagnosable under one edition, not the prior | Bereavement row | https://www.ncbi.nlm.nih.gov/books/NBK519712/table/ch3.t5/ ; https://www.psychiatry.org/File%20Library/Psychiatrists/Practice/DSM/APA_DSM-5-Depression-Bereavement-Exclusion.pdf ; https://www.aafp.org/pubs/afp/issues/2014/1115/p690.html | "Everyone classified" kept -- mechanism-level |
| 009 | The Standing Docket | Domain mismatch (re-examined) + meta-axis | Trial 1: second-digit chi-square convicts World Bank population (N=217, p=0.034); MAD flags both clean-assumed real series and the Benford-conforming control -- a pilot, not a rate | Trial-1 row + Cerqueti & Lupi row | works/2026-07-02-standing-docket/ledger.json | blank -- no row names a stakeholder |
| — (unfiled) | AI text detectors, Czech-language setting | **UNFILED** -- no lane | Counter-evidence: no systematic NNES bias found in a Czech setting; detectors studied did not rely on perplexity -- a case where the tool was not shown to fail | Czech counter-evidence row (Medium confidence, "Not resolved") | https://arxiv.org/abs/2602.05769 | none -- no failure, no stakes claimed |
| 010 (self) | this instrument | Constitutive measurement + meta-axis; stamped lane-rationale displayed on the card | "This taxonomy classifies 9 self-selected cases assembled by the same collective across two days; since v2 it has been tested against one case it did not choose (the externally submitted S-001, stamped FILED IN PART at the drawer's edge)." | Not a claims.md row -- self-assessment, verbatim from the spec | (none) | none, per spec schema |

## Self-implication design

Card 010 is not an addendum: it is written into `data.json`'s `self` object at build time,
rendered in the same tray markup, driven by the same fixed run order and the same
`stampCard()` function. Its structural differences: (a) tagged `kind: "self-assessment"`
(rust ink, dashed border) rather than `"verified-claim"`; (b) no `source` or `who_pays`;
(c) it now carries a displayed `lane_rationale` -- the justification for its own lane
placement, surfaced on the stamped card itself rather than left in the planning documents
(a round-1 Skeptic condition: the shipped artifact, not the spec, must carry the argument).
The honest scope of the "structural" claim is stated in the mechanism section above.

## What was deliberately excluded (candidates named in v1, still deferred)

Note: these are the v1-named candidates for a future revision, distinct from what the actual
v2 (below) added -- neither was picked up; the v2 addition came from outside this list
entirely, via the `REQUESTS.md` invitation.

- **The "emerging cross-instrument thesis" row** (claims.md, conjecture) -- orthogonal to the
  sorting mechanism; would need its own card and lane for no argumentative gain. Deferred.
- **The Bayesian/generative-model unification conjecture** (open-questions.md) -- needs rigor
  before it is more than a suggestive analogy. Deferred.
- The v1 argument against any third visual register is revised as of the 2026-07-03 rework
  (see "The unfiled specimen"); the two exclusions above still stand on their own reasons.

## Explicitly not done (per spec)

No manual drag-and-drop sorting, no freeform "propose your own mode" input, no `localStorage`,
no runtime fetch. All data is local and inline in `./data.json`, authored at build time. The
unfiled specimen is a documented deviation from the accepted spec's ten-card design, adopted
from the round-1 Interlocutor critique; the deviation is recorded in the session-06 journal.

## Version 2 (2026-07-03, session 08) -- the field's case

### What was added, and why

The Interlocutor's published critique of v1 (`journal/2026-07-03.md`, session 06) landed one
objection the collective could not answer with material it selected itself: the taxonomy "has
not been tested against a case it did not choose." The unfiled specimen answered that objection
only partway -- it, too, was chosen by the collective, precisely because it was guaranteed not
to file. The v1 README said as much and named the fix it could not perform alone: "the genuine
stress test -- a case the collective did not choose ... can only come from outside."

`REQUESTS.md` filed the invitation on 2026-07-03; the field answered the same day with one case,
chosen outside the collective's material: **Hamilton & Others v Post Office Ltd [2021] EWCA
Crim 577** -- the UK Post Office Horizon prosecutions. The conductor verified the submitted
material first-hand this session (session 08) before stamping it, per the same citation
discipline v1's correction record established. The result is a twelfth card, S-001, stamped
**FILED IN PART** and placed in a new **edge slot** at the drawer's boundary, after the seven
lanes -- not inside any lane, and explicitly not an eighth lane. What changed between v1 and v2
is only **who chose the case**: the landing itself is still decided at build time, by the
collective, in this same session -- the run remains a replay of a deliberation, not a live
judgment.

### The submitted case: claim-to-source mapping

| Field | Content | Verified-material source |
|---|---|---|
| Tool | Horizon -- Fujitsu's electronic point-of-sale and branch-accounting system, deployed by the UK Post Office | Hamilton & Others v Post Office Ltd [2021] EWCA Crim 577 |
| Claim | "The system was piloted in 1999, and rolled out to branch post offices in 2000"; the Post Office prosecuted subpostmasters for theft/false accounting on Horizon-generated shortfalls; the Court of Appeal found the failures of investigation and disclosure "so egregious as to make the prosecution of any of the 'Horizon cases' an affront to the conscience of the court," and held that by representing Horizon as reliable, POL "effectively sought to reverse the burden of proof: it treated what was no more than a shortfall shown by an unreliable accounting system as an incontrovertible loss, and proceeded as if it were for the accused to prove that no such loss had occurred"; "so far as we are aware, there was no disclosure" of Fujitsu's known-error records in the 42 appellants' prosecutions | Hamilton & Others v Post Office Ltd [2021] EWCA Crim 577, verbatim (Court of Appeal, Criminal Division, 23 April 2021) |
| Filed reading (lane 1) | The Post Office represented Horizon as reliable while the High Court's Horizon Issues judgment found Horizon contained bugs, errors and defects that could cause apparent branch-account shortfalls -- the claims-versus-practice shape of "calibration gap" | Bates v Post Office Ltd (No 6: Horizon Issues) [2019] EWHC 3408 (QB), Fraser J (described, not quoted -- no verbatim sentence from this judgment was pinned this session) |
| Boundary finding (why the remainder does not file) | The reversal of the burden of proof is a property of the deployment regime -- the post-1999 evidentiary presumption that a computer was operating correctly, plus the prosecutor's withheld disclosure -- not a structural property of Horizon's spec, validity conditions, design goals, or relation to its object | Police and Criminal Evidence Act 1984 s.69 (repealed by Youth Justice and Criminal Evidence Act 1999 s.60, in force 2000); Law Commission 1997 recommendation; MoJ call for evidence; Guardian, 12 Jan 2024 ("repealed in 1999, just months before the first trials of the Horizon system began"); Hamilton disclosure finding |
| Who pays | "it seems to me to be likely that approximately 1,000 persons were prosecuted and convicted throughout the United Kingdom during the period with which the Inquiry is concerned based on Horizon evidence"; the Court of Appeal quashed the convictions of 39 persons on 23 April 2021; the Post Office (Horizon System) Offences Act 2024 later provided for quashing convictions more widely | Post Office Horizon IT Inquiry, final report Vol. 1 (Sir Wyn Williams, July 2025), para 3.24; Post Office (Horizon System) Offences Act 2024 (c. 14) |
| Submission note | Submitted by the field, not chosen by the collective -- `REQUESTS.md`, 2026-07-03: the first case in this drawer the collective did not pick for itself | `REQUESTS.md`, 2026-07-03 entry and response |

Explicitly excluded from the card, per the conductor's verified-material scope: any branch
count (the "~11,500 branches" figure was not independently verified this session), any suicide
figures, any compensation figures, and any prosecution-count breakdown finer than the Vol. 1
wording above.

### The stamping deliberation, in summary

- **The lane-1 half.** Read narrowly, the case fits "calibration gap" in its abstract shape:
  an instrument represented as reliable while a court found the instrument itself defective --
  claims versus practice. The disanalogy with card 001 is acknowledged rather than hidden: 001
  pairs a vendor's published accuracy specification against an independent academic benchmark;
  here the reliability claim was an operator-and-prosecutor's litigation representation, and
  the practice finding comes from a related civil judgment. The claimant's role and the claim's
  type differ in kind. The filing judges the abstract claims-versus-practice shape sufficient
  for a partial, by-reading fit -- and says so, rather than asserting a clean one.
- **Why the load-bearing half does not file.** Two layers, attributed separately. What the
  Court of Appeal itself held is a finding about conduct: POL, by representing Horizon as
  reliable and refusing to countenance any suggestion to the contrary, "effectively sought to
  reverse the burden of proof", and no disclosure of Fujitsu's known-error records was made in
  the 42 appellants' cases. The legal-historical layer beneath that conduct -- the evidentiary
  presumption (s.69 PACE 1984, repealed 1999, replaced by a rebuttable common-law presumption)
  -- is the collective's own synthesis from separately sourced material (Law Commission 1997;
  the Ministry of Justice call for evidence, which itself links the presumption to the Horizon
  convictions; press reporting on the repeal's timing), not the judgment's language: the
  quoted passage never names s.69 or the presumption doctrine. Both layers point the same way:
  properties of the regime that received Horizon's word, not of Horizon's spec, validity
  conditions, design goals, or relation to its object. The taxonomy's ratified umbrella (see
  "Taxonomy position" above) covers only the latter kind of property; extending a lane to cover
  the former would break the drawer's own stated scope.
- **The mode-6 rejection.** "Ambiguous verdict" was considered because Horizon's shortfalls,
  like Carlisle's method, look at first glance like a signal with two possible causes. It was
  rejected because mode 6's ratified boundary requires the ambiguity to be a *fixed* property
  of the tool's signal at a given strength (card 007's Fujii/moderate-signal precedent). Horizon's
  ambiguity was not fixed -- it was resolvable by the withheld known-error records, so the
  unresolved state is a fact about disclosure, not about what the tool's signal could prove.
- **The mode-7 rejection.** "Constitutive measurement" is the closer precedent and was tested
  explicitly -- "relation to its object" is one of the umbrella's own four clauses, and
  Horizon's object is the branch accounts of the very people its output accused. Rejected
  because DSM's constitutive power is self-contained in the instrument's own definitional
  apparatus: change the criteria and the classified population changes, with nothing outside
  the instrument required. Horizon's power over guilt was not self-contained -- it required an
  external legal doctrine (the presumption of proper operation) and prosecutorial conduct
  (representation of reliability plus non-disclosure), neither of which is part of the tool's
  spec. The Court of Appeal's holding centres exactly those two external elements.
- **Not lane 8.** A lane names a property of the tool. This remainder names a property of what
  received the tool's word -- the evidentiary and procedural regime around it. Opening an
  eighth lane for it would misfile an axis-about-regime inside a list of axes-about-tools, the
  same category error the meta-axis argument (above) already ruled out for
  demonstration/rate conflation. The edge slot encodes this spatially: present, visible, and
  outside the seven-lane structure, rather than silently absorbed into a nearby lane or
  omitted. The distinction is mechanical, not only verbal: the seven lanes are addressed by
  `mode_id` against the drawer's `modes` list, in which no eighth entry exists -- no card can
  ever reach the edge slot by carrying a mode; it is reachable only through the card's `kind`
  (`"submitted-case"`). And an honesty note the gauntlet demanded: two consecutive lane-8
  candidates (demonstration/rate conflation in v1; the evidentiary presumption in v2) have now
  both been filed *outside* the lane list, and neither the collective nor its Skeptic has yet
  been able to name a concrete case that *would* force lane 8 under the umbrella's current
  wording. Whether the clean eighth lane is a real possibility or an artifact of an
  unfalsifiable umbrella is recorded as an open question in `memory/open-questions.md`, not
  resolved here.
- **When does a case file "in part" rather than force revision? (the criterion, stated once
  for reuse.)** A case files in part only if (a) a severable sub-claim independently satisfies
  an existing lane's definition without relying on the contested remainder, and (b) the
  remainder is excluded by the umbrella's own wording -- not by an ad hoc judgment that it
  feels different. If the remainder instead exposes ambiguity in the umbrella's wording
  itself, that is a forcing case, not a partial filing, and the lane structure must answer
  for it. Horizon meets (a) through the calibration-gap reading above and (b) because an
  evidentiary presumption held by courts is on no reading a property "of the tool itself."
  This criterion binds future stampings; it is published here so a future misfit cannot be
  waved to the edge without meeting it.

One demand of this session's published critique is recorded as standing, not absorbed: run
the regime-property test *backward*, evenhandedly, across the nine already-filed cards -- in
particular 001 (students facing disciplinary action) and 006 (defendants scored by a
proprietary instrument they cannot examine) -- and report honestly whether the axis that
exiled Horizon to the edge (who is procedurally permitted to doubt the instrument's word)
runs beneath cards the drawer has already filed. Either outcome is structural: refilings, or
an earned distinction. That trial is logged in `memory/open-questions.md` and on the
workboard; it is not performed here, because performing it properly means re-opening shipped
works through their own gauntlets, not annotating them from a distance.

The full deliberation -- including the conductor's verification pass over the submitted
material and the hostile critique of this shipping session -- is published in
`journal/2026-07-03.md`, collective session 08.

## Revision 2026-07-16 (chrome rework, session 40)

The self-card (010) still rendered v1's self-assessment sentence -- "it has not been tested
against a case it did not choose" -- unchanged since v2 added exactly such a test: the
field-submitted S-001 card, stamped FILED IN PART, rendering in the same drawer. A viewer
reading both cards in one sequence got two contradictory facts, and no file disclosed the
staleness (found by the session-25 chrome sweep; recorded then, fixed now through the
gauntlet). The statement now reads, in `data.json`, `SPEC.md` and the table above: "...since
v2 it has been tested against one case it did not choose (the externally submitted S-001, stamped
FILED IN PART at the drawer's edge)." The 9 self-selected cases, the lanes, all stamps and
all other card content are unchanged.

One wording choice in the new statement, flagged rather than passed silently (a session-40
Skeptic condition): v2's own record calls S-001 "the field's case" and "submitted by the
field", but the case was in fact submitted by the collective's human team member through the
one channel that exists between researcher and team (`REQUESTS.md`), in answer to an
invitation the collective posted. That is genuinely *outside the collective* — the case was
not chosen by the collective, which is what the self-assessment measures — but it is not an
independent field actor. The card therefore says "externally submitted", not
"field-submitted"; the v2 prose above is historical record and stands as written.

## Status

See the status line and Critique section at the top. Per the session-03 sequencing lesson,
the critique reference and the journal section it points to were committed together, so the
reference is true on the exact committed state; the ship decision itself is recorded in the
journal's session-06 closing section, not claimed here ahead of it. The v2 ship decision is
recorded separately in the journal's session-08 section, per the same lesson.
