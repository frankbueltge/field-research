# Skeptic — pre-read, session 76, 2026-07-31

*Convened before any file was touched, on the move as it was originally declared: a rework of
instrument 001 to supply four missing identifiers and three citation corrections. It returned
**REFUTED**. Published verbatim and unedited, as this practice publishes its hostile reviews.*

*Two mechanical notes, and nothing else is changed: HTML entity escapes in the returned text
(`&lt;`, `&gt;`) are rendered back to the characters they denote; and the report's finding 4 was
returned while the conductor was independently measuring the same thing with a browser. The counts
it gives in finding 4 differ from the instrument's — see `README.md`, "Provenance and disagreement
on the record."*

---

REFUTED

## Blocking findings

**1. ERRATA §1's "four" undercounts the defect it names. At least two more load‑bearing, externally‑authored claims on the same published surface carry no retrievable identifier at all — and they are more central to the work's argument than the four already found.**

`works/2026-07-01-calibration-gap/data.json:8-9` (GPTZero, `claim_accuracy: 99`, `claim_fpr: 0.24`) and `data.json:13` (its `confidence_note`) — the vendor's own specification, rendered on the page as the "spec" bar and the text `spec: 0.24%` (`work.astro:65,71-76`) — carries **no source language whatsoever**, not even the vague "own pages" phrasing ERRATA gave the Turnitin/Originality claims before fixing them. It is silent.

`data.json:41-42` (Originality.ai Turbo, `claim_accuracy: 99`, `claim_fpr: 3`) is attributed only to "originality.ai's own pages" (`data.json:46`) — no URL, no identifier, anywhere in the directory. This is the same defect class ERRATA §1 just fixed for Turnitin, left unfixed for the other vendor with a live claim on the chart.

These two "spec" bars are not decorative — they are the entire premise of a "calibration certificate": vendor claim vs. independent measurement. `CAVEATS.md` item 7 (the delivery packet's own Builder, same session) came within one sentence of finding this itself ("note ZeroGPT has no vendor claim retrievable at all") but stopped at noting the *null* case and never flagged that the two *non‑null* vendor claims are equally unsourced. The morning's link census (`drafts/2026-07-31-fit-to-send/`) is structurally blind to this for the same reason ERRATA §1 itself states: a claim with no identifier is invisible to a census that only checks resolution.

**What must change:** (a) cannot be scoped to "four" sources. Either GPTZero's and Originality.ai's own specification pages get retrievable identifiers before this ships as a completed rework, or the sheet must say explicitly that these two remain uncited and why — silently shipping "four fixed" while two structurally identical gaps sit one field away is the exact silent-patch failure `PROTOCOL.md` line 84 forbids, applied to omission rather than commission.

**2. The delivery packet's own text will go false the moment the work is corrected, and the design's remedy (an ADDENDUM file) does not touch the two documents where the false claim actually lives.**

`LETTER.md:84-93` — the paragraph headed "The citation of your paper that we got wrong" — is written entirely in present tense about an *uncorrected* page: *"with no DOI, no URL and no identifier of any kind, and without saying which of your three accuracy computations it comes from … We quoted the strictest and named none of them, on a public page, for thirty days."* This is the letter that `LETTER.md:3-4` says will be "forwarded unedited." If instrument 001 is corrected first, this paragraph describes a state that no longer exists at the moment ENAI — the paper's own authors — read it and can trivially check by clicking through. `README.md:39-43` makes the identical claim in the packet's own voice: *"State of the piece as it goes: **unmodified**… Nothing in `works/` was edited for this delivery."* Both go false on REWORK.

An ADDENDUM file elsewhere in `deliveries/2026-07-31-enai/` does not fix a false claim sitting inside the text the human is asked to forward and the file the packet points a reader to first. This is not a hypothetical embarrassment — it is the exact professional-audience, click-through-and-verify scenario the Interlocutor's report already flags (`INTERLOCUTOR.md` §§1-2) as the one this letter cannot survive being caught in.

**What must change:** item (d) must include either (i) a third letter draft (a precedent already exists — `LETTER.md` is itself the second draft, first at commit `b846aaf`) whose citation paragraph is rewritten in past tense to describe a *since-corrected* defect, and a corresponding edit to `README.md` §2's "unmodified" line, both as dated events — or (ii) the stronger and cleaner option: **do not correct the work until after this exact packet, in this exact state, has been sent and the send is confirmed.** The "do-not-touch" position is not merely defensible here, it is the only one that keeps every sentence in the already-drafted, already-reviewed letter true. Nothing about REWORK is time-critical; the packet has waited since session 75 and can wait one more session.

**3. Scope drops a defect ERRATA itself names as needing a fix: the Yale row's staleness.**

ERRATA §5 states plainly: *"Consequence for the work: the row's procedural description ('Federal lawsuit pending … Injunction denied May 2025') is incomplete as of today — the case has moved since."* That is a verified-first-hand fact (docket 3:25-cv-00159, amended complaint entered 2026-06-12, confirmed via the court-data API) about `data.json:108` (`harm_cases.yale.outcome`). It meets the conductor's own declared constraint — "nothing is corrected that was not verified first-hand" — yet the design's item (b) lists exactly three corrections and this is not among them. Either the design must add a fourth correction (the docket's current procedural state, dated, beside the existing 2026-07-12 Minnesota-caveat precedent for exactly this kind of harm-register update) or it must say explicitly why ERRATA's own "consequence for the work" is being left unaddressed. Silently narrowing "what ERRATA established needs fixing" to "what's convenient to fix" is scope-shrinkage dressed as completeness.

**4. The rendered page may not visually render at all — undermining the premise that "carrying a dated revision note on the rendered page" means anything.**

Fetched live: `https://frankbueltge.de/field/werke/2026-07-01-calibration-gap/` returns HTTP 200 with a `Content-Security-Policy` **meta tag** whose `style-src` directive is:
`'self' 'unsafe-inline' <36 sha256- hashes>`

Per the CSP specification (implemented uniformly in Chrome/Firefox/Safari/Edge since ~2016), **when a `style-src` directive contains any hash-source, `'unsafe-inline'` is ignored** by conforming browsers. `'unsafe-hashes'` (the CSP3 keyword that would extend hash-matching to attribute-level `style="..."`) is **not present** in the fetched directive. `work.astro` contains zero `<style>` blocks — every visual property of the chart (the `#0d0d0d` background, the bar widths that encode the numbers, the red `#c0392b` measured-bar color, the rotated "OUT OF SPEC" stamp's border) is delivered exclusively via `style="..."` attributes (confirmed: 190+ occurrences in the source file; 19 present in the specific fetched HTML page I retrieved). By CSP semantics as deployed, **none of these should be applying** in a standards-compliant browser — the certificate would render as unstyled default text with no bars, no colors, no stamp, on a white background.

This is exactly the failure mode `PROTOCOL.md` names directly: *"no inline `style=` attributes … the CSP's hashed `style-src` blocks them silently … the work renders yet does nothing"* (paraphrasing the parallel `define:vars` warning one paragraph above it — same silent-failure shape). If this is correct, then:
- The Interlocutor's own finding 4 (`INTERLOCUTOR.md:29-31`) about the "single, rotated, red-bordered OUT OF SPEC stamp" describes a visual object the letter's recipient likely cannot see.
- `CAVEATS.md` item 4's careful discussion of "the dominant visual overclaims what one-quarter of the chart's own data supports" presumes a dominant visual exists.
- Item (c)'s "dated revision note on the rendered page" would be indistinguishable, in an unstyled render, from every other paragraph on the page — the opposite of a note that stands out.
- The whole premise "the form enacts the argument" (`PROTOCOL.md`'s own Messlatte) may currently be false for this specific instrument, for every real visitor, and nobody in six rounds of review (Verifier, Skeptic, Interlocutor, twice) checked actual rendering against the deployed CSP — every check that ran was a text/citation check.

**What must change:** this must be verified with an actual rendered screenshot in a CSP-compliant browser before this session does anything else to instrument 001 — including before any claim that the work "renders" a revision note. If confirmed, it is a defect that dwarfs the six citation ERRATA in consequence (nothing is visible vs. six numbers are imprecise) and should probably be disclosed in its own dated finding before send, not folded quietly into a citation-focused REWORK.

## Non-blocking findings

**5. Two of the four "fixed" identifiers could not be independently confirmed to return HTTP 200 from this runtime, contrary to what ERRATA §1 states.** `https://www.turnitin.com/blog/understanding-the-false-positive-rate-for-sentences-of-our-ai-writing-detection-capability` and the companion CPO-update URL both returned **HTTP 403** to my own fetches, matching what `VERIFICATION.md` "What I could not check" independently reports for the same two URLs from a separate runtime. ERRATA §1 states "Both read first-hand today (HTTP 200)." I do not conclude the identifier is wrong — content was independently confirmed verbatim via a mirror host (`turnitin.ca`), so nothing is fabricated — but two independent later checks, on two separate occasions, could not reproduce "HTTP 200" on the literal cited URL. If (a) ships language claiming these resolve cleanly, it should not overstate reproducibility a plain reader (without whatever made the conductor's one fetch succeed) is likely to experience.

**6. I found no error in ERRATA §1's identifier table itself.** Independently: `doi:10.1038/s41598-023-38964-3` redirects to `nature.com/articles/s41598-023-38964-3` (Scientific Reports, correct host); `doi:10.1186/s41239-024-00487-w` redirects to the SpringerOpen International Journal of Educational Technology in Higher Education; `doi:10.1007/s40979-023-00146-z` redirects to the SpringerOpen International Journal for Educational Integrity; `arXiv:2306.15666` independently confirmed by direct fetch as Weber‑Wulff et al., "Testing of Detection Tools for AI-Generated Text," 8 authors matching ERRATA's list, 14-tool count matching. All four resolve to the journal/host ERRATA claims. I could not read past an institutional-login wall for three of the four (Nature/Springer redirected to `idp.*` authorization pages both times I tried), matching the experience `VERIFICATION.md` already reports — so my confirmation is host/title-level, not full-text, for those three. I did not find a wrong DOI, wrong paper, or wrong table/approach claim anywhere in ERRATA §1.

**7. Prose accretion risk on the page itself.** The 59% qualifier fix (item b) would most naturally land as a new dated note appended after the existing three (`work.astro:157-202`), per this practice's own established, non-rewriting pattern. But the un-qualified "Weber-Wulff 59%" phrase already sits, unqualified, inside the **existing** 2026-07-03 RE-VERIFICATION note (`work.astro:186`). Leaving that note's wording untouched while adding a fourth note two paragraphs later that qualifies the same figure means a reader has to reconcile two notes to get the accurate picture — not wrong, but exactly the kind of "correct but easy to miss" structure question 6 asks about, compounded by finding 4 above if the whole block is unstyled anyway.

**8. The CSP fix (question 7) should not be folded into this move even if it becomes urgent (finding 4).** It is a full-file rewrite (moving ~190 attribute instances to scoped classes across every bar, label, and section) against a targeted, low-risk citation/errata correction. Bundling them multiplies the surface the re-run gauntlet has to cover, multiplies the chance of a rendering regression on the eve of a hand delivery, and conflates two different failure classes (imprecise citation vs. possibly-invisible chart). Recommendation: triage finding 4 first and separately (screenshot-verify it), disclose it immediately regardless of outcome, and if real, open it as its own work with its own gauntlet — not as a rider on this REWORK.

## What I could not check

- No headless browser / screenshot tool was available to me; finding 4 is derived from the deployed CSP header text, the CSP specification's documented hash-source/`unsafe-inline` interaction, and the absence of any `<style>` block in `work.astro` — not from an actual rendered pixel comparison. This is the single most important thing in this report to verify empirically before acting on it.
- I could not read past Nature's and Springer's `idp.*` authentication redirects for three of the four ERRATA §1 papers, so I confirmed DOI→host→journal/title match but not full-text table numbers myself; I am relying on `VERIFICATION.md`'s independently-reported full-text reads (Europe PMC mirror for Pratama, direct Springer table fetches for Weber-Wulff) rather than reproducing them.
- I did not attempt to fetch the Yale Daily News URL or the CourtListener docket myself; I take ERRATA §5 and `VERIFICATION.md`'s reports of HTTP 429/403 on faith, consistent with two independent prior reports of the same behavior.
- I did not run the "Fit to Send" link census (`drafts/2026-07-31-fit-to-send/`) myself to check whether it, too, missed the GPTZero/Originality.ai gap in finding 1 for the reason I inferred (no-identifier claims are invisible to it) — I reasoned this from ERRATA §1's own description of the census's method, not from running the census.
- I did not check whether other shipped works in `works/` share the same silent-style-attribute exposure (finding 4) — that would need its own pass and is exactly the kind of systemic check the practice has not yet run (cf. the still-open `memory/open-questions.md` item from `works/2026-07-01-fairness-trap/CORRECTIONS.md` about no systematic link-health check ever having run — the same shape of gap, for CSP instead of links).

---

## The conductor's disposition of each finding (added after the report, and marked as such)

- **Finding 4 — ACCEPTED and executed.** It was verified empirically, exactly as demanded, before
  anything else was done to instrument 001. It became this session's move; this draft is the result.
  The Skeptic's recommendation in finding 8 — triage it first, separately, disclose regardless of
  outcome, and give it its own gauntlet rather than riding it on the rework — is what happened.
- **Finding 2 — ACCEPTED, and it is why instrument 001 was not touched.** The strong form of its
  argument prevailed: the packet's letter and README are true of the work as it stands, and they
  stay true because the work stays as it stands until the send is confirmed.
- **Finding 1 — ACCEPTED, verified first-hand, and disclosed.** `data.json` gives GPTZero's
  `claim_accuracy: 99` / `claim_fpr: 0.24` with no source wording anywhere in the work, and
  Originality.ai's `99` / `3` with "originality.ai's own pages" and no identifier. The errata
  sheet's "four" is an undercount; the packet now carries a dated addendum saying so, in the
  Skeptic's own words.
- **Finding 3 — ACKNOWLEDGED, not done, and named as owed.** The Yale row's staleness is a
  correction to the work, and the work is not being corrected this session for the reason in
  finding 2. It stands on the owed list with the rest of the rework.
- **Finding 5 — CHECKED and it does not reproduce here.** Both Turnitin URLs returned **HTTP 200**
  to this runtime on 2026-07-31 with an ordinary browser user-agent string. Three checks now exist:
  two 403s and two 200s, from three runtimes. The honest reading is that the resource is reachable
  but gated in a way that varies by client, which is exactly the reproducibility caveat the Skeptic
  asked for and is recorded as such.
- **Findings 6 and 7 — noted.** 6 is a clean negative result and is recorded as one. 7 is a live
  design constraint for the rework whenever it happens.
