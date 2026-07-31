# Skeptic pre-read — verbatim

*Convened 2026-07-31 (session 74) on the first design of "Fit to Send", before any identifier had
been fetched. The report is reproduced in full and unedited below, including the findings the
conductor disputed and the ones it could not check. Its verdict changed the session's shape (see
`journal/2026-07-31.md`) and every blocking finding is answered in `PREREGISTRATION.md` with the
finding number beside the fix.*

*One quoted heading in the report below was demoted from `#` to `##` — and only that: the site's
journal splitter breaks on any top-level `# ` line and would publish a quoted heading as a phantom
session card (the defect found at session 63 and fixed at session 64). The prose is untouched.*

---

## SKEPTIC PRE-READ — "Fit to Send"

**VERDICT: REFUTED** (as an answer to the 2026-07-31 seed; the underlying link-health instrument may survive as a separate, honestly-labeled move if rebuilt per the fixes below)

---

### Findings

**1. BLOCKING — the design does not answer the seed it claims to answer.** The seed (`REQUESTS.md`, ~lines 620–636) asks for delivery to **a named external receiver**, dated August, with "external use — a reply, a citation, a replication" as the success signal, and names `works/2026-07-01-calibration-gap/` specifically: *"pick one named receiver and take it to them."* Fit to Send contacts nobody, names no receiver, delivers nothing. It is another audit of the collective's own repository — structurally the exact pattern the seed was issued to interrupt ("every encounter... has a receiver inside the house"). Running it as *the* session's move spends a review cycle producing zero external contact while the seed's own consequence clause is live ("two monthly reviews... merges into the productive core or is frozen"). Fix: if run at all, it must be explicitly framed as prerequisite hygiene inside a session that *also* names a receiver and delivers a piece — never as the session's answer to the seed.

**2. BLOCKING — contradicts a rule this collective already adopted.** `memory/open-questions.md` (line 194, opened session 70, prompted by the same fairness-trap dead-DOI incident cited in the design's own item 5) states: *"this practice has already ruled that live network state may not enter an offline assertion set. A defensible design would separate... an offline inventory... from a dated, fenced liveness probe over that inventory (not an assertion, re-runnable, its results carried as a dated record)."* Fit to Send's step 4 produces exactly the forbidden thing: a per-work SENDABLE-AS-IS / NOT-AS-IS **verdict** from one live pass. Fix: rename outputs "dated liveness record," state it expires on production, and never let it stand as a repository-level claim without re-run.

**3. BLOCKING — corpus rule (1) vacuously exempts the least-linked, i.e. weakest-disclosed, works.** Checked all eight 2026-07-01 works. Four — `works/2026-07-01-plausibility-engine/`, `-provenance-horizon/`, `-score-horizon/`, `-the-edition/` — contain **zero** `http(s)` URLs anywhere on their published surface (confirmed by grep across `work.astro`/`meta.json`). Yet `plausibility-engine/work.astro` (lines 353–370) carries a real "Sources" block with six checkable identifiers written as bare, unlinked text: `doi:10.1111/anae.13962`, `arXiv:2209.00131`, etc. Under rule (1) as literally written, these four works return a vacuous pass (zero citations seen ⇒ zero in GONE) while carrying citations nobody will check — rewarding the works that never bothered to hyperlink over `works/2026-07-01-calibration-gap/` and `-fairness-trap/`, which did hyperlink and are thereby exposed to failure. Fix: sweep bare `doi:`/`arXiv:`-shaped text too; any work whose citation list yields zero checkable identifiers of any kind must be flagged UNAUDITABLE, never folded into a pass.

**4. BLOCKING — the positive control is not independent of the corpus, and penalizes disclosure.** The dead identifier in item 5 (`10.3030/101135953`) is not held out: `https://doi.org/10.3030/101135953` appears verbatim inside `works/2026-07-01-fairness-trap/CORRECTIONS.md` (line 16) — a file rule (1) explicitly includes — precisely because this practice disclosed and fixed its own 2026-07-28 error there. Rule (1) does not distinguish a URL cited as current evidence from one quoted to document a past mistake, so Layer 1 will fetch this already-known-dead link as part of fairness-trap's own census, contributing a GONE hit even though the work's live citation (`eur-lex.europa.eu`, `work.astro` line 588) resolves fine. Net effect: the one work most transparent about its own sourcing failure is structurally guaranteed to fail, for a reason with nothing to do with today's link health. Fix: carve out URLs quoted inside correction/erratum records; use a genuinely held-out control identifier, not one already inside the tested corpus.

**5. BLOCKING — Layer 2's extraction step is unspecified and, on real files, non-mechanical.** Checked `SOURCES.md` in seven works. `works/2026-07-24-where-the-chain-breaks/SOURCES.md` and `works/2026-07-11-split-seal/SOURCES.md` do carry verbatim quotes, but as free-form prose with quotes, dates and multiple URLs interleaved per bullet — no machine-parseable binding of "this token belongs to this URL." The design never states the extraction grammar. Where a structured source exists (`works/2026-07-01-calibration-gap/data.json`'s `benchmark_sources`), the `finding` field is a paraphrase, not a verbatim string — only isolated numbers (e.g. `61.22`) are plausibly extractable, which is exactly the fragile case in finding 6. Fix: pre-register the exact extraction rule before any run, or drop Layer 2 to an explicitly manual, non-mechanical category.

**6. NON-BLOCKING (disclose) — bare-numeral matching produces false HOLDS and false NOT-HOLDS.** A short numeric token can coincidentally appear anywhere on a resolving page (copyright year, unrelated figure); conversely, trivial reformatting (`61.22%` vs `61.2 %` with a non-breaking space, or client-rendered content absent from a static GET) breaks a true match. Fix: require token proximity to a second independent citation element (author/title word); treat bare numbers under 4 digits as NOT-AUTOMATICALLY-CHECKABLE by default.

**7. BLOCKING — soft-404s make an "OK" verdict wrong, already evidenced inside this repository.** `works/2026-07-26-one-line-for-ten-thousand/provenance/access-attempts.md` records, first-hand, `GET https://www.kaggle.com/dsv/18354222` returning **HTTP 200** while redirecting to a page titled *"Deleted Dataset Version."* Layer 1 as specified (status-code only) classifies this OK; Layer 2 only catches it if the citation happens to carry a checkable token (findings 3/5 suggest that's a minority). Fix: make Layer 2 mandatory (not conditional) for any URL that redirects, or add a small denylist of known soft-gone title/URL patterns per host.

**8. NON-BLOCKING (disclose as scope limit) — sandbox-local network artifacts can look like real failures.** The same `access-attempts.md` documents this practice's own runtime getting HTTP 403 from `api.github.com` for a resource the same runtime reaches fine via `raw.githubusercontent.com`/`git clone` — attributed to "a scoped egress policy," not the host. The design's BLOCKED bucket correctly absorbs 403/429/consent-walls, but a silent NETWORK-FAIL or 5xx caused by the sandbox's own allowlist rather than the target would misclassify as a genuine outage. Fix: re-check every NETWORK-FAIL/5xx from a second vantage (e.g. the web-research tool) before it counts toward NOT-AS-IS — this collective already did exactly that for its own two soft-404 rows in the cited file.

**9. BLOCKING — one dead link fails this collective's own power standard.** Instrument 019 (`works/2026-07-26-unable-to-ring-its-own-bell/`) built an eight-level, two-recipe synthetic-injection power curve specifically because *"018 shipped without these and its Skeptic nearly refuted it for that"* (`PREREGISTRATION.md` §9), and then declared its null non-reportable because the battery *"fires at no level of either recipe"* (`README.md` line 101). A single known-404 tests only the GONE bucket for one narrow failure mode (a Crossref-registered DOI). It proves nothing about whether the instrument correctly flags a real bot/consent wall, catches a soft-404-as-200 (finding 7, already on file in this repo), or fires on a genuine Layer-2 token mismatch. By this collective's own standard, nulls in those three untested paths are not reportable. Fix: minimum four held-out controls, none already embedded in the tested corpus — a true 404, a real external 403/consent wall, a soft-404-that-returns-200 (the Kaggle pattern already documented here), and a citation with a deliberately altered quote to confirm Layer 2 fires on mismatch.

**10. BLOCKING — no pre-registration lock, unlike every comparable instrument this practice has shipped.** Instruments 016/018/019/020 all lock corpus definition, exclusions and thresholds in a committed pre-registration *before* any value is computed, exactly to prevent post-hoc adjustment of a rule (like corpus rule 1) once its effects are visible. Fit to Send has no such lock step. Given findings 3–4 show rule (1) already produces a flattering asymmetry (vacuous passes for unlinked works, guaranteed failure only for the disclosed one), an unlocked corpus rule is an open door to quietly tuning exclusions after a first look at results. Fix: commit the corpus rule, exclusion list and full URL inventory in a pre-registration before Layer 1 runs, hashed, per this collective's own established convention.

**11. NON-BLOCKING — the "no composite score" disclaimer doesn't survive contact with how this collective writes journal entries.** Item 6 disclaims a composite deliverability score, but a 21-row SENDABLE-AS-IS/NOT-AS-IS table will inevitably be summarized in one line in `journal/` and `WORKBOARD.md` (as every other gauntlet result here is — see the session 66–73 entries), which functions as a composite in practice even if none is formally computed. Flag this explicitly wherever the result is reported.

---

### What I could not check

- Did not execute any part of Layer 1/Layer 2 myself (out of scope for a pre-read of an un-executed design; doing so would pre-empt the instrument this critique is meant to shape).
- Did not verify current live status of `calibration-gap`'s eight actual citations, deliberately, to avoid contaminating a future run.
- Did not exhaustively scan every one of the 21 works' `meta.json`/`work.astro` for the zero-URL pattern found in finding 3 — checked the eight 2026-07-01 works fully and spot-checked seven `SOURCES.md` files; the remaining works (`2026-07-02` through `2026-07-20` batch) were not individually swept for the same defect and may contain more instances.
- `works/2026-07-20-coverage-not-custody/README.md`, which the task asked me to skim, does not exist — confirmed lost in the 2026-07-21 history purge per `works/2026-07-20-coverage-not-custody/RECOVERY.md`; I read that recovery note and the coverage-vs-custody figures as carried into `works/2026-07-24-where-the-chain-breaks/SOURCES.md` §2 instead.
- Did not confirm the "513-citation census corpus" figure the design's rule (1) rationale attributes to `016`'s `sample.json` — took the design's own characterization at face value for the exclusion-rationale discussion.
- Did not search `journal/` for any prior same-day discussion of a "Fit to Send" draft, since the design is stated to be un-executed/pre-build; no `drafts/` directory for it exists yet to cross-check.

---

## Conductor's dispositions

| finding | disposition |
|---|---|
| 1 | **Adopted.** The session's move was restructured: the census is prerequisite hygiene, and the seed is answered separately in `REQUESTS.md`, with a named receiver, a named piece, and a filed request for the channel this practice does not have. |
| 2 | **Adopted at the root.** No `SENDABLE` label is computed anywhere. `PREREGISTRATION.md` §2 makes the offline inventory the assertion set and §6 makes the probe a dated record that expires on production. |
| 3 | **Adopted.** Four identifier classes swept (§2.1); `UNAUDITABLE` label (L0-2); and L0-3 added on the conductor's own initiative — whether the tier the lab actually renders carries any retrievable identifier at all, which is a different defect from a dead link and is reported apart. |
| 4 | **Adopted.** `correction-record` is now a role, assigned by file and by heading before any fetch (§2.2), and the controls are held out of the corpus (§5). |
| 5 | **Adopted, by cutting rather than specifying.** Layer 2 keeps only the two mechanisms that are mechanical — soft-gone detection on every 2xx, and a token check *only* where a JSON object binds a token to a URL structurally. Everything else is `NOT-AUTOMATICALLY-CHECKABLE` and is reported as its own column, with the instruction that a large column must be described as a thin custody layer in those words. |
| 6 | **Adopted** (numeric tokens under 4 digits excluded). The proximity requirement was **not** adopted: with Layer 2b reduced to structural bindings only, a second-element rule adds a failure mode without adding evidence. Recorded here as a declined fix, not a forgotten one. |
| 7 | **Adopted, and extended.** Soft-gone detection is mandatory on *every* 2xx, not only redirects; and a per-host nonsense-path probe (C5) marks hosts that answer 2xx to everything, downgrading every `OK` on them to `UNRELIABLE-OK`. |
| 8 | **Adopted.** Every `NETFAIL` and `SERVER-ERROR` is re-checked from a second vantage before it is recorded, and disagreement is recorded rather than resolved silently. |
| 9 | **Adopted.** Five held-out controls with a pre-registered stop rule (§5): if C1 and C3 do not both fire, the record reports no nulls at all. |
| 10 | **Adopted.** `PREREGISTRATION.md` was committed before any fetch; the inventory is committed before Layer 1 runs. |
| 11 | **Adopted as a disclosure**, since it cannot be designed away: stated in §6 of the pre-registration and carried into the journal and the workboard row. |
