# The Taxonomy on Trial -- method note

Status: **draft -- gauntlet pending.**

## What the work is

A drawer of ten specimen cards laid out on a bounded grid, styled as a natural-history
specimen-drawer tray (matte green field, bone index-card faces, brass rule lines and stamp
ink). On load all ten cards are visible but unlabeled -- each shows only its instrument
number and the tool it examined. Above the tray, seven fixed compartment labels ("the seven
named failure modes") are already engraved into the drawer's rail. A single control, "Run the
classifier," plays a fixed-order sequence: each card in turn is stamped with its failure mode
and a one-line cited claim, then visibly migrates into the lane matching that mode. "Skip to
end" jumps straight to the fully-sorted state for repeat viewing or accessibility. Both paths
always land in the same final state -- there is no randomness anywhere in the mechanism.

Card 010 -- this instrument -- is the tenth card, present in the tray from the first frame
alongside 001-009, not appended or styled apart. It runs last in the same sequence and lands in
the "Constitutive measurement" lane like any other card. A translucent cross-cutting rail
beneath the whole grid, labeled "cross-cutting: demonstration / rate conflation," lights when
card 009 is stamped and names both cards it applies to; card 010's landing joins 009 on the
already-lit rail. When the sequence finishes, a permanent
caption appears in the same visual chrome as the rest of the interface: "9 cases sorted -- a
tally, not a rate."

## The mechanism, and why it is not decorative

The taxonomy's substantive claim is that classification is an act with consequences, not a
passive label. The piece does not assert this in prose; it performs it. The visitor triggers
an actual sort, watches each case move into a lane in front of them, and cannot reach a
"finished" drawer without having watched the mechanism sort its own work into the same lane,
using the same rail, that it uses for instrument 009. Removing card 010 or the cross-cutting
rail would require deleting part of the mechanism, not editing a sentence -- that is what makes
the self-implication structural rather than a caveat a visitor has to scroll to find.

## Taxonomy position: meta-mode, not mode 8

**Recommendation carried from the spec: meta-mode.** The seven named modes each describe a
structural property of a tool's design colliding with its deployment context -- a spec that
does not match practice, conditions applied outside their valid domain, goals that cannot be
jointly met, and so on. "Demonstration / rate conflation" describes something categorically
different: how much evidentiary weight a *single trial* of any of those tools can carry,
independent of which of the seven modes is present. A domain-mismatch instrument, a
constitutive-measurement instrument, or a perfectly calibrated tool could each be shown only
once -- the conflation risk sits orthogonal to which failure type is at stake, not as a
competing eighth member of the same list. Instrument 009 is itself evidence for this: the
dossier already records that the Standing Docket "does not exhibit a new tool failure mode --
it re-examines 002/004's domain," and separately names the evidence-quality problem. Filing
that problem as mode 8 would misfile an axis-about-evidence inside a list of axes-about-tools.
The drawer's separate cross-cutting rail encodes that decision spatially, in the mechanism
itself, rather than only in a caption -- and leaves a clean 8th lane open for a future
candidate that is genuinely tool-structural rather than evidence-structural.

## Claims / source table

Every displayed claim traces to a row in `memory/claims.md`. Where the dossier's `who_pays`
gloss (see `memory/dossiers/instruments-on-trial.md` §2) was not directly supported by the
specific claims.md row(s) cited for that card, it was softened or left blank rather than
reproduced verbatim -- see the notes column.

| Card | Tool | Mode | Displayed claim (data.json) | claims.md row (finding, abridged) | Source in data.json | who_pays note |
|---|---|---|---|---|---|---|
| 001 | AI text detectors | Calibration gap | Vendor-claimed accuracy (98-99%, <1% FPR) fails independent benchmarking; RAID 37% FPR vs Originality.ai's claimed 0.2% | Row: "Vendor-claimed AI text detector accuracy... does not hold under independent/adversarial benchmarking; e.g. Originality.ai Turbo claims 0.2% FPR, RAID measures 37% FPR" | https://aclanthology.org/2024.acl-long.674.pdf | "Students facing disciplinary action" kept as-is -- directly supported by the institutional-harm row (ACU allegations, Yale student suspension, Minnesota PhD expulsion), which is this card's second cited basis row |
| 002 | Benford's First-Digit Law | Domain mismatch | Benford's first-digit law invalidly applied to 2020 US precinct-level election data; academic consensus: first-digit analysis of precinct returns cannot diagnose fraud | Row: "Benford's (first-digit) Law was invalidly applied to 2020 US precinct-level election data..." | https://websites.umich.edu/~wmebane/inapB.pdf | who_pays left **blank**. Dossier's gloss "Democratic legitimacy claims" is dossier framing, not language in the cited row (Mebane row / Benford-conditions row); softening to blank rather than embellishing, per spec instruction naming 002 specifically |
| 003 | C2PA provenance chain | Structural contradiction | C2PA metadata stripped by ordinary distribution paths -- 0% survival on screenshot; only direct/CDN/email paths preserve it | Row: "C2PA provenance metadata is stripped by ordinary distribution paths..." | https://www.rand.org/pubs/commentary/2025/06/overpromising-on-digital-provenance-and-security.html | Dossier gloss "Journalists, courts" traces to a *different* claims.md row (the call-home privacy-leak row) not cited as this card's basis (stripping + forged-manifest rows only). Softened to "Anyone verifying an image's origin after ordinary sharing or re-encoding" -- tied to the actual cited row's mechanism, no profession named without direct support |
| 004 | Last-digit uniformity test | Domain mismatch | Same test that flags fabrication also fires on legitimate clinical/survey rounding (BP terminal-digit bias, age heaping), mirror-image surplus at 0/5 | Row: "The same last-digit test fires just as strongly -- or more strongly -- on legitimate clinical and survey data with systematic rounding..." | doi:10.3122/jabfm.2019.05.190085 ; doi:10.29115/SP-2023-0018 | "Clinical / demographic research" kept -- directly supported (row names blood-pressure and age-heaping/survey data explicitly) |
| 005 | AI capability benchmarks | Active exploitation | MMLU-CF re-scoring: 12-18pt inflation across 7 models/providers; clean scores sit below 89.8% human-expert average | Row: "Contamination-free re-scoring (MMLU-CF) shows a consistent 12-18 percentage-point inflation..." | https://arxiv.org/abs/2412.15194 ; https://github.com/microsoft/MMLU-CF | "Those relying on reported benchmark scores -- researchers, policymakers, the public" -- reasonable readership inference for benchmark claims, not an invented stake; kept, worded to avoid asserting harm beyond what the row supports |
| 006 | COMPAS recidivism scoring | Definitional impossibility | ProPublica (FPR 44.85% Black / 23.45% White) and Northpointe (PPV) findings both correct; Chouldechova's impossibility result | Row: "COMPAS recidivism scores: ProPublica's 'biased' finding... and Northpointe's 'fair' finding... are both numerically correct..." | https://doi.org/10.1089/big.2016.0047 ; https://doi.org/10.1126/sciadv.aao5580 ; https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm | "Defendants -- disproportionately Black" kept -- directly supported by the FPR disparity figures in the row |
| 007 | Carlisle's method | Ambiguous verdict | Cannot distinguish fabrication from legitimate stratified/covariate-adaptive randomisation at moderate signal; method's own title concedes the ambiguity | Row: "Carlisle's method cannot distinguish fabrication from legitimate stratified/covariate-adaptive randomisation at moderate signal strength..." | doi:10.1111/anae.13962 ; https://arxiv.org/abs/2209.00131 | "Researchers wrongly flagged; fabricators escaping detection" kept -- matches the row's stated ambiguity directly |
| 008 | DSM (psychiatric diagnosis) | Constitutive measurement | DSM-5 deletion of bereavement exclusion: identical symptoms diagnosable under one edition, not the prior one, no change in the person | Row: "DSM-5's deletion of the DSM-IV 'bereavement exclusion' criterion... means a person with identical symptoms is diagnosable under one edition's criteria and not under the previous edition's..." | https://www.ncbi.nlm.nih.gov/books/NBK519712/table/ch3.t5/ ; https://www.psychiatry.org/File%20Library/Psychiatrists/Practice/DSM/APA_DSM-5-Depression-Bereavement-Exclusion.pdf ; https://www.aafp.org/pubs/afp/issues/2014/1115/p690.html | "Everyone classified -- the instrument constitutes the phenomenon" kept -- abstract, mechanism-level, matches the row without naming an unsupported specific group |
| 009 | The Standing Docket | Domain mismatch (re-examined) + meta-axis | Trial 1: second-digit chi-square convicts World Bank population series (N=217, p=0.034); MAD cutoff flags both clean-assumed real series and the Benford-conforming control at N 200-217 -- a pilot, not a rate | Row: "Trial 1 of the Standing Docket... second-digit Benford chi2 convicts the known-provenance World Bank 2023 population series..." and the Cerqueti & Lupi N-dependence row | works/2026-07-02-standing-docket/ledger.json (seeds 42/43, deterministic re-run verified twice independently) | who_pays left **blank** -- 009 has no entry in dossier §2's pattern table (which only covers instruments 001-008) and no cited row names a stakeholder for it; per spec, no new stakes are invented for 009 or 010 |
| 010 (self) | this instrument | Constitutive measurement + meta-axis | "This taxonomy classifies 9 self-selected cases assembled by the same collective across two days; it has not been tested against a case it did not choose." | Not a claims.md row -- the spec's self-assessment statement, reproduced verbatim, kind `"self-assessment"` | (none -- self-assessment, no external source) | No who_pays field, matching the spec's schema example for the `self` object |

## Self-implication design

Card 010 is not an addendum: it is written into `data.json`'s `self` object at build time,
rendered in the same tray markup as cards 001-009, driven by the same fixed `runOrder` array
(`[1, 2, ..., 9, 10]`) and the same `stampCard()` function in the inline script. Its only
structural differences are (a) it is tagged `kind: "self-assessment"` rather than
`"verified-claim"`, which the script renders as a visually distinct tag ("SELF-ASSESSMENT" in
rust ink, dashed card border) instead of "VERIFIED CLAIM" in brass, and (b) it carries no
`source` or `who_pays`, since it is not a claims-ledger row. Removing it from the run order or
disconnecting it from the cross-cutting rail would require editing the mechanism's data and
script, not a caption -- that is the intended structural (not rhetorical) form of
self-implication described in the spec.

## What was deliberately excluded (v2 candidates)

- **The "emerging cross-instrument thesis" row** (`memory/claims.md`, marked conjecture): that
  across the first eight instruments, a tool's strongest guarantee coincides with the context
  of lowest real-world need. Orthogonal to this piece's mechanism (which classifies failure
  *modes*, not the thesis about where guarantees are weakest); including it would require its
  own card and lane with no argumentative gain to the sorting mechanism. Deferred to v2.
- **The Bayesian/generative-model unification conjecture** (`memory/open-questions.md`): the
  sketch that all seven modes might reduce to one generative-model/deployment-context mismatch.
  Explicitly flagged in `open-questions.md` as needing more rigor than a suggestive analogy.
  Including it in v1 would add a claim requiring its own visible "(conjecture)" tag, distinct
  from every cited card's "VERIFIED CLAIM" tag and from card 010's "SELF-ASSESSMENT" tag -- a
  third visual register for no gain to the core argument. Deferred to v2.

## Explicitly not done (per spec)

No manual drag-and-drop sorting by the visitor, no freeform "propose your own mode" input, no
`localStorage` persistence across reloads, no runtime fetch of `claims.md` or anything else.
All data is local and inline in `./data.json`, authored at build time.

## Status

**Draft -- gauntlet pending.** This README does not reference a journal critique section; per
the session-03 lesson recorded in the dossier (`memory/dossiers/instruments-on-trial.md` §4),
a critique reference is only added once the gauntlet has actually run and the critique is
committed to the journal -- not before.
