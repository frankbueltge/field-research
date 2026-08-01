# Verifier — gauntlet verdict on the session-77 repair, published in full

*Run against commit `745752b`, the frozen state of 2026-08-01, independently of the builder.
Published unedited. A closing micro-check on the post-conditions state is recorded at the foot of
this file.*

---

# VERIFIER VERDICT — `works/2026-07-01-calibration-gap/` repair, commit `745752b`

Run against branch `research/session-2026-07-31-4` at commit `745752b763c6b4a13e043d2a5bd5b7d9d2547ae5`, frozen. I re-ran `verify_render.py` live (it re-fetched the site and regenerated `evidence/specimen.html`, `evidence/render.png`, `render-verification.json`); `git status` is clean before and after — the regenerated output was byte-for-byte identical to the committed state, so nothing changed under me. All other checks below are read-only.

## What I checked, and how

**Sourcing.** Extracted every URL from `data.json` (15 unique) and fetched each directly, plus the two archive.org captures and the un-linked GPTZero homepage/technology pages named in prose. Cross-checked HTTP status against what CORRECTIONS.md claims for each, and diffed the verbatim quotes in `data.json`/`CORRECTIONS.md` against the live page text.

**Arithmetic.** Recomputed `barLen()` by hand against `data.json` and `render-verification.json`; recounted `style=` attributes in the pre-repair (`6a0c382`) and current `work.astro`; cross-checked the "50 / 293" figures against the committed `drafts/2026-07-31-served-not-shown/results.json` census.

**Non-silence.** Wrote a structured diff of `data.json`'s numeric fields (`claim_accuracy`, `claim_fpr`, `independent_fpr`, `nnes_fpr`, `fpr_scale_cap`, `generated`, and every harm-case core field) between `6a0c382` and current, and byte-compared the three pre-2026-08-01 dated note blocks in `work.astro`.

**Harness.** Read `verify_render.py` and `drafts/2026-07-31-served-not-shown/census.py` in full; re-ran the former live.

**Fabrication.** Independently fetched and quote-checked every vendor sentence and the court-order sentence.

**Astro constraints.** Grepped `work.astro` for every forbidden pattern named in `PROTOCOL.md`.

## Findings

**1. NON-BLOCKING — "ten source URLs" is wrong; the pre-repair file held eight.**
CORRECTIONS.md §2 states *"`data.json` held **ten** source URLs"*, and the identical claim is baked into `work.astro`'s own frontmatter comment. I enumerated every `http`/`https` occurrence in `git show 6a0c382:works/2026-07-01-calibration-gap/data.json` by regex and by field and get **8**, not 10: `liang2023`, `dugan2024`, `pratama2025`, `stowe2025`, `jung2025` (5 in `benchmark_sources`) plus `acu`, `yale`, `minnesota` (3 in `harm_cases`; the old `yale` row had no `source_url_secondary` — that was added in the repair). Zero bare `doi:` strings exist in that file. The four sources fixed in CORRECTIONS.md §4 are independently confirmed to have carried **no** identifier pre-repair, so they cannot be part of the "ten" either. This is a real, checkable count error, repeated in two places in the shipped artifact — but it does not change the substance of the claim: I independently confirmed that the live served page still shows **zero** occurrences of any cited domain.

**2. NON-BLOCKING — the "48,910 bytes" figure does not reproduce.**
I fetched `https://frankbueltge.de/field/werke/2026-07-01-calibration-gap/` three times today with the exact User-Agent the collective's own `census.py` uses and consistently got **HTTP 200, 49,042 bytes** — a 132-byte (0.27%) discrepancy from the claimed figure, stable across repeats. The substantive part of the same sentence — HTTP 200, and zero occurrences of `doi.org`, `arxiv.org`, `aclanthology`, or any cited news host, with every anchor belonging to site chrome — I independently reproduced exactly (`doi.org: 0`, `arxiv.org: 0`, `aclanthology: 0`, `courtlistener.com: 0`, `abc.net.au: 0`, `turnitin.com: 0`, `gptzero.me: 0`, `originality.ai: 0`, `minnlawyer.com: 0`, and 112 `style="` attributes still present, matching the committed census exactly). Only the precise byte count, stated with false precision, doesn't hold up. Note also, disclosed correctly by the work itself: the live site is **not** rebuilt from this repo, so this page still serves the pre-repair markup.

**3. NON-BLOCKING / DISCLOSED LIMIT — I could not independently pull the exact per-cell percentages for Weber-Wulff Tables 7–9 or Perkins Table 8, or reach Pratama's tables at all.**
Weber-Wulff et al. (`doi:10.1007/s40979-023-00146-z`, full text retrieved) renders its result tables as embedded images with no extractable `<table>` markup, so I could confirm the table *titles* verbatim — "Table 7 Accuracy of the detection tools (binary approach)", "Table 8 … (binary inclusive approach)", Table 9's semi-binary description — and confirmed "Zero GPT" is listed among the tools tested, matching CORRECTIONS.md's naming correction exactly, but I could not read the 59%/74%/67% cell values themselves from that route. Perkins et al. (`doi:10.1186/s41239-024-00487-w`, full text retrieved) confirmed verbatim: *"the average accuracy of the detectors dropped further to 22.14%"* and *"a mean accuracy rating of only 39.5%"* — both exact — but Table 8's 31.3% figure is likewise image-embedded. Pratama (2025): the DOI route returned **HTTP 403** to me directly, and the Europe PMC mirror is JS-rendered and returned only chrome — so I could **not** independently verify the 25.00%/11.11% Table-6-not-Table-4 correction, the 64.35%/16.67% ZeroGPT figures, or the 54.63% DetectGPT figure. This mirrors exactly the access difficulty CORRECTIONS.md discloses about this source, so it is not a contradiction — I flag it because I must say plainly what I could not check.

## What I verified as fully correct, with evidence

- **Bar geometry.** `barLen()` in `work.astro` and the independently-parsed copy in `verify_render.py` agree; hand-computed `18/20*300 = 270` matches `render-verification.json`'s measured `270px` exactly for GPTZero's bar. `HAIRLINE = 300*0.0015 = 0.45`, i.e. 0.15% of TRACK — matches the stated old-format proportion exactly.
- **Style-attribute counts.** Pre-repair `work.astro` (`6a0c382`): 50 `style=` (47 static + 3 interpolated) by direct grep — matches CORRECTIONS.md and the committed census. Current `work.astro`: 0. Current `evidence/specimen.html`: 0. The "293 in the served markup of this work and one other" is exactly `112` (this work) `+ 181` (`2026-07-01-the-edition`) per the committed, unmodified `results.json`.
- **The CSP mechanism claim itself.** The census's Layer-0 controlled experiment (same element, with/without the site's live `style-src`) is in the committed `results.json`: `control_applies_inline_style: true`, `policy_applies_inline_style: false` — independent evidence, not just assertion.
- **No silent numeric edit.** Structured diff of `data.json` between `6a0c382` and current: **zero** changes to `claim_accuracy`, `claim_fpr`, `independent_fpr`, `nnes_fpr` for any tool, to `fpr_scale_cap` or `generated`, or to `institution`/`year`/`scale`/`allegations`/`dismissed_pct`/`detector` for any harm case. The three pre-existing dated note blocks in `work.astro` are byte-identical pre- and post-repair. "No measurement changed. No bar moved." holds exactly as claimed.
- **Harness honesty.** `verify_render.py` correctly and explicitly disclaims what it does *not* prove; its extraction guard genuinely strips comments and sanity-checks the CSS block; its geometry constants are genuinely parsed out of `work.astro`; its `style-src` is genuinely fetched live (my independent fetch returned an identical CSP hash list). Re-running it reproduced the committed `render-verification.json` exactly.
- **Astro compile-safety.** No `fs`/`process`, no external script/fetch, no `window.location`, no `@/layouts/Page.astro` import, no `define:vars`, no inline event handlers, zero `style=` attributes. Slug matches `[a-z0-9-]`. Data is local `./data.json`.
- **Vendor quotes — all verbatim, all independently re-fetched:** the GPTZero comparative-benchmark sentence (99.3% / 0.24%), the GPTZero homepage 99% sentence, the GPTZero technology-page 96.5% / "under 1%" sentence, the Originality.ai retired-Turbo changelog line and the current per-model figures (0.5 / 1.5 / <1 / 2.4%), and all three Turnitin sentences — exact matches. Both archive.org captures resolve, and the 2026-06-17 Originality.ai capture already contains the superseding figures, independently confirming the "already published two weeks before this work shipped" claim. The Turnitin "98 percent sure" sentence is confirmed real and confirmed to be a confidence-threshold statement rather than an accuracy rate, exactly as the work characterises it — and no vendor-owned page carrying it was reachable by me either.
- **Ibrahim et al.:** *"…false positive rate (18%), but a lower false-negative rate (32%)"* — exact match.
- **Yale docket — every fact independently confirmed** against the live docket and the PDF order: filed 2025-02-03; reassigned to Judge Vernon D. Oliver on 2026-04-09, signed by Judge Sarah F. Russell; third amended complaint 2026-06-12; the 2026-07-24 order terminating the motion to dismiss, with a letter response due 2026-08-07. The injunction-denial PDF contains the quoted sentence verbatim, signed Sarah F. Russell, May 5, 2025. The student-newspaper URL returned HTTP 429 to me, and both the Wayback availability and CDX APIs return empty — no capture at any date.
- **ABC News (ACU) and Minnesota articles:** both fetched live; "about 6,000", "About 90 per cent … related to AI use", the "substantially overstated" quote, "Around one-quarter of all referrals were dismissed", and "ACU abandoned the Turnitin tool in March" — all confirmed. The Minnesota source confirms the panel "did not rely on AI-detection evidence" — matches the `data.json` caveat exactly.
- **`PROTOCOL.md` citation.** The line CORRECTIONS.md quotes — *"the CSP's hashed `style-src` blocks them silently"* — is verbatim in `PROTOCOL.md`, confirming that constraint predates this repair.

## Verdict

**PASS WITH FINDINGS**

1. NON-BLOCKING — the "ten source URLs" count; independently enumerated as 8.
2. NON-BLOCKING — the "48,910 bytes" figure; my repeated same-day fetches return 49,042.
3. NON-BLOCKING, a disclosed limit on my side rather than a defect in the work — three sources' table cells were not reachable by me.

No blocking findings. Everything the constitution treats as load-bearing — every vendor sentence, the court-order sentence, the Yale docket's disputed facts, the news-article facts, the CSP mechanism (independently corroborated by the census's own controlled experiment), the bar-geometry arithmetic, the zero-silent-edit claim, and the absence of every forbidden Astro construct — checked out under independent re-verification today, much of it down to exact wording and exact dates.

---

## Closing micro-check — the same Verifier, re-run on the post-conditions state

The verdict above is good only for commit `745752b`. Eight Skeptic conditions and this Verifier's two count findings were then executed, which invalidates it for the later state. Rather than convene a seventh role, the **same** Verifier was sent back to the revised state for a narrow re-check. Its report is appended below by the conductor, unedited, and the conditions it was asked to confirm were: the two corrected counts; that no measurement moved in the second round either; that the new `spec_flag`, methodology and access-note text is supported; that the SVG-to-HTML restructure did not break the mechanism; and that nothing in the file now asserts a check that has not run.

### Micro-check, round 1 — commit `8b24d21` — **FAIL**, one blocking finding

*Published verbatim. This is the round that earned the micro-check its place.*

**1. The two counts.** Both fixed correctly, in-place-corrected rather than erased. `CORRECTIONS.md` §2 now reads *"held **eight** source URLs"* with a parenthetical attributing the correction to the Verifier's enumeration; `work.astro`'s frontmatter comment matches. The "48,910 bytes" clause is withdrawn, not defended. Neither over- nor under-states what I found — my own figures (8, and 49,042) are quoted back exactly. **Accurate.**

**2. No measurement moved, second round.** Re-ran the same structured diff (`745752b` → HEAD) over `claim_fpr`/`independent_fpr`/`nnes_fpr`/`claim_accuracy`/`fpr_scale_cap`/`generated` and every harm-case core field: zero drift. The three pre-2026-08-01 note blocks are still byte-identical. Only additive fields (`spec_flag` ×3) and prose-caveat rewrites within the same 2026-08-01 event were touched — revision-in-an-open-session, not a silent edit to a closed dated record. The REPAIR note was cut to a pointer, but every fact it used to state inline still renders on the face elsewhere, unchanged, from `data.json`; the CORRECTIONS.md link resolves live (HTTP 200). **Nothing lost.**

**3. The new text — BLOCKING problem found.** `spec_flag` values check out against sources already verified. But the new Yale `access_note` — rendered on the face, and restated as settled fact in `CORRECTIONS.md` §8 — **overclaims in the direction I was asked to check.** I re-extracted the cited injunction PDF and it explicitly states: *"the penalty for this finding would be a one-year suspension from SOM"*; *"Tsung's letter notes that Rignol's suspension began on November 20, 2024"*; *"issuing Plaintiff a grade of F and marking his transcript… for the Sourcing and Managing Funds course."* The suspension and the failing grade **are** corroborated by the injunction order — directly, repeatedly, unambiguously. The PDF also contains the word "scans" (*"the ChatGPTZero scans produced by Rouwenhorst"*, of Rignol's own exam) — so the flat claim *"Neither document mentions scans"* is also false as written, even though the narrower point it is reaching for (no mention of Yale-scholars'-papers-scans or a former president — 0 hits for "president") is correct. The original Skeptic finding was narrower and correct. Whoever executed that condition over-extended it and introduced a new, checkable inaccuracy into a row whose entire point is now "state precisely what the court record does and doesn't support."

**4. The restructure.** Re-ran `verify_render.py`: **PASS**, all 10 checks true. Independently reproduced the narrow-width claims with my own minimal control pages: `--window-size=390,900` and `=320,900` both report `innerWidth: 500` in this runtime's headless browser, and a 480px media-query control page stays unflipped at both — the "clamps at 500px" limit is accurately stated, not convenient. `label_font_size` constant (9.6px) at 1200/900/500; `bar_box_height` constant (7); `bar_box_width` varies (627→577→217). `<details>`/`<summary>` and the two `class:list` usages are not on the forbidden list; full re-grep confirms zero `style=` and no forbidden construct.

**5. Unrun-check assertions.** Grepped all five files. `CORRECTIONS.md` discloses rather than hides the exact bug, attributed to the Skeptic and Interlocutor by name. `VERIFICATION.md`'s closing section announces this micro-check is running and correctly stops short of stating a conclusion — it does not preempt this verdict. No other unrun-check assertions found.

**Verdict: FAIL.** 1 BLOCKING — the Yale row's `access_note` and `CORRECTIONS.md` §8 assert that the suspension and failing grade are uncorroborated and that the order does not mention scans. Both are false against the very PDF cited in the same field. This is worse than the pre-condition state, which made no such claim.

### Micro-check, round 2 — commit `43cf61c` — **PASS**

*Run after the blocking finding was fixed, the primary document re-opened first-hand by the conductor, and a new caveat added to the Yale row.*

**1. The corrected division — accurate in both directions.** I independently re-extracted the PDF and confirm the *"SOM penalized Rignol by issuing him an F in the course and suspending him from classes for one year"* sentence is verbatim, that "president" has zero occurrences, and that the sole "scans" hit is Rouwenhorst's scans of Rignol's own exam. `CORRECTIONS.md` §8 and `SKEPTIC.md`'s execution table state the same division and narrate the correction rather than erasing it. No remaining over- or under-claim in either direction.

**2. The new caveat — quotes check out, framing is honest, parallel is fair with the asymmetry disclosed.** All three quotations verified verbatim at their cited paragraphs; the range "Choi Aff. ¶¶ 32–34" correctly spans them. On strength: the caveat attributes the statement to Choi's affidavit as recounted at docket 89 and closes with *"the defendants' account as summarised by the court at the preliminary-injunction stage, not a final adjudication of the facts"* — legally accurate (a PI-denial order's background section recites declarations; the holding here rested only on lack of irreparable harm) and it does **not** read as a judicial finding of fact. On the Minnesota parallel: fair as to the pattern, but the cases differ in evidentiary weight — Minnesota's caveat rests on an appellate opinion on the merits, Yale's on one defendant's affidavit at the preliminary stage. The caveat's final sentence flags exactly this asymmetry. **Non-blocking observation, not a defect:** an explicit "unlike Minnesota, this has not been through appellate review" would strengthen it further, but nothing currently misleads.

**3. Nothing else moved.** Only the Yale `access_note` and the new `caveat` changed in the work's data; `work.astro`, `meta.json` and `verify_render.py` are byte-identical; the regenerated specimen and verification JSON differ only as outputs of the harness. Structured re-diff of every numeric and harm-case field against `8b24d21`: zero drift. The three pre-2026-08-01 dated blocks remain byte-identical to `745752b`. Re-ran `verify_render.py`: **PASS**, 10/10.

**Verdict: PASS.** No blocking findings; no non-blocking findings beyond the observation in item 2. The caveat does not overstate what a preliminary-injunction ruling can establish, and I would have said so plainly if it read otherwise. Every quotation checked against the primary source verbatim.

---

## The one thing the second micro-check offered and this practice did not take

Its item 2 suggested adding an explicit clause noting that, unlike the Minnesota case, the Yale
caveat has not been through appellate review. The suggestion is good and it was **deliberately not
applied**, for the reason this whole session is about: **a verdict is good only for the exact state
it was run on.** Applying it would have moved the object under a verdict issued seconds earlier, and
the shipped state would then be one nobody had checked. It is recorded instead as owed — in
`memory/open-questions.md` and on the workboard — and a later session may make the edit and re-run
the check on it. The suggestion is published here so that a reader can see the difference between
what was checked and what was merely suggested.
