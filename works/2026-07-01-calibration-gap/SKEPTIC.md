# Skeptic — gauntlet verdict on the session-77 repair, published in full

*Run against commit `745752b`, the frozen state of 2026-08-01. Published unedited. Every condition
is answered in `CORRECTIONS.md` §8 and in `journal/2026-07-31.md`, session 77.*

---

# SKEPTIC VERDICT — Repair of Instrument 001, session 77 (commit 745752b)

## What I checked

`CORRECTIONS.md`, `work.astro`, `data.json`, `render-verification.json`, `verify_render.py`, `evidence/render.png`, `git diff 6a0c382 -- works/2026-07-01-calibration-gap/`, the full `journal/2026-07-31.md` (sessions 74–77), `deliveries/2026-07-31-enai/ADDENDUM-2026-07-31-render.md`. I also ran my own instrumentation against `evidence/specimen.html` — reusing the collective's own `census.py` browser helper — to test claims the record does not test: word-proportion of disclosure vs. substance, and rendering at narrow viewport widths.

## Finding 1 — CORRECTIONS.md asserts a review record that does not exist

`CORRECTIONS.md` line 18: *"The gauntlet run for this state — Verifier, Skeptic, and the hostile Interlocutor critique published in full — is recorded there [`journal/2026-07-31.md`, session 77]."* Present tense, stated as accomplished fact.

It is false at this commit. `journal/2026-07-31.md` is 1,277 lines. Session 77's entry (line 1202 onward) contains only the opening record — orientation, the race guard, and the planned move — and ends at line 1278 with *"Not attempted this session: the letter's third draft… consolidation."* No Builder report, no Verifier pass, no Skeptic verdict, and no Interlocutor critique for the repair appear anywhere in it. `git log --all -- journal/2026-07-31.md` shows the last commit touching that file is `99f69d9`, the session-open marker — three commits *before* the repair itself (`949a47d`, `1bc7280`, `745752b`). No `journal/2026-08-01.md` exists in git history at all. I checked.

So the document that certifies this repair's own review discipline — the discipline the whole practice prides itself on — pre-narrates a gauntlet that had not run when it was written, and still has not run in the archive as of the commit this exercise is frozen on. This Skeptic pass is, as far as the record shows, the *first* outside check of the actual repaired state. `CORRECTIONS.md` claimed that check was already "recorded" before it existed. That is not a data problem; it is the practice getting ahead of its own process on the one document whose entire genre is "we checked this against ourselves before anyone else had to."

## Finding 2 — the Yale row's most specific claim still rests on nothing anyone can read

The core claim says *"the stale procedural row rests on the court record."* Check the actual sentence, not just the procedural update.

`data.json` harm_cases → yale → `outcome` retains, unchanged from the pre-repair state: *"He submitted scans showing the same tool flagged academic papers by Yale scholars, including a former university president, as probably AI-generated."*

The two things newly cited to support this row — the docket entry describing the case's procedural posture, and the injunction-denial order's quoted holding (*"Rignol has failed to make the threshold showing of irreparable harm"*) — corroborate none of it. Neither citation says anything about scans, about Yale scholars, or about a former university president. The only source that ever supported that sentence is the Yale Daily News article, which `CORRECTIONS.md` itself documents as unreadable by every route tried and uncaptured by the Internet Archive at any date. The repair re-sourced the *dates* on this row. It did not re-source, flag, or even acknowledge that its single most vivid, specific factual claim is still standing on a citation nobody here has ever read and cannot read.

The core claim's clause is true of the procedural facts and false of the row read as a whole. As written, "rests on the court record" overstates what happened.

## Finding 3 — "reference date" is invoked to justify a number the same paragraph proves was already stale

`data.json` → `specification_sources` → `originality_spec` → `caveat`: the archived capture of 2026-06-17 shows the superseding Turbo 3.0.2 figure (1.5%) *"was already published two weeks before this work shipped."* The work shipped 2026-07-01.

`CORRECTIONS.md` line 102 then defends retaining the stale "under 3%" bar by saying it is *"retained at the work's stated reference date (2026-07-01) and disclosed in place."* But a reference-date defense means "this was the best-known figure at the time." The correction's own evidence says it was not — the current figure was sitting on the same vendor page two weeks earlier. This is not a case where the world changed after the reference date and freezing the bar preserves an honest snapshot. It is a case where the work took the wrong number off a page that, at the moment of shipping, already carried the right one beside it. Calling that "retained at the reference date" borrows the legitimacy of a defense that doesn't apply here, and the paragraph that makes the defense also destroys it, in the same breath, if a reader reads past the first sentence.

The disclosure is honest about the fact. It is not honest about the shape of the justification.

## Finding 4 — the caveats that matter are not next to the numbers they qualify

The "COMPOSITE" and "SUPERSEDED SPEC" caveats live in a `SPECIFICATION SOURCES` block that comes *after* the harm register — well below the `FPR MATRIX` where the `OUT OF SPEC` stamp and the bars actually sit. A reader who looks at the chart, sees GPTZero's spec bar at 0.24% and the "OUT OF SPEC" stamp overhead, and stops there — which is what a chart is for — gets no signal that the 0.24% is a composite of two vendor documents whose own paired accuracy figure isn't the 99% shown beside it. `tool.claim_fpr` and `tool.claim_accuracy` are rendered with nothing beside them pointing down the page. Disclosed is not the same as proximate. "Disclosed rather than restated" is true; the disclosure is currently positioned to be missed by exactly the skimming reader a chart is built for.

## Finding 5 — the page is roughly six parts disclosure to one part instrument

I ran a word count against the rendered face (script and counts available on request; methodology: `key_finding` + harm-case `outcome`/`caveat` fields as "core," vs. the specification lede/quotes/caveats, `benchmark_sources` findings/access-notes, and the four static correction/note blocks as "disclosure"). Core substantive content: **386 words**. Disclosure/meta content actually rendered on the face: **2,404 words** — a ratio of roughly **6:1**. This is a rough instrument and I say so; but it is not close enough to parity that the ratio is arguable. Attack line 4 asked whether the certificate is still legible as an instrument or has become a changelog with a chart attached. By word count, the chart is the minority tenant of its own page.

## Finding 6 — `confidence_note` still isn't rendered; the page says so itself

Session 75's own Skeptic named this: `confidence_note` — where the Turnitin sentence/document-level mismatch and the removed NNES bars are explained — is a `data.json` field never mapped in `work.astro`. It still isn't, after the repair; I grepped `work.astro` for `confidence_note` and `claim_accuracy_status` and neither appears rendered anywhere (`claim_accuracy_status` appears once, inside static prose, not as a bound field). The matrix footnote's own sentence — *"Confidence ratings vary — see data.json for per-tool methodology notes"* — is a live admission that this content lives off the page a receiver actually opens. The seven-part repair added a whole new sourcing apparatus for the spec bars and left this named, known gap exactly where it was.

## Finding 7 — the SVG chart's text shrinks with the container, and nobody has confirmed it stays legible at phone width

I measured this directly, twice. Rendering `evidence/specimen.html` at 900px content width, the chart's `cc-chart-lbl`/`cc-chart-val` text has a computed bounding-box height of **19px**. At ~405px content width, the same text's bounding-box height is **10px** — a **47% reduction**, from a container-width change alone, with the CSS `font-size` property itself unchanged (9.6px both times — the shrink is entirely a function of the SVG's `viewBox`-to-viewport scale factor, which the text is subject to exactly like the bars are). This is a deterministic, linear mechanism, not noise: SVG content inside a fluid `width:100%` container with a fixed `viewBox` scales font size with the box. It will keep shrinking below 500px.

I could not get a clean empirical read below ~500px in this environment — the available headless Chromium binary silently clamps its internal layout viewport to 500px regardless of `--window-size` for DOM inspection, while `--screenshot` crops rather than reflows, which nearly led me to report a false "text is cut off mid-word" defect before I isolated the artifact and disproved it against myself. I am naming that failure so it isn't repeated: **do not trust a screenshot from this tool below ~500px without cross-checking `getBoundingClientRect` figures the way I did.** The corrected, honest state of this finding: the mechanism guarantees shrinkage at phone width, the magnitude at true 360–390px widths is not directly confirmed by anyone including me, and this is precisely the question session 76's own Interlocutor named as never having been asked of any work in the corpus. The repair added a `@media (max-width: 480px)` block that touches padding and flex stacking. It does not touch the SVG's `font-size` values, and nothing in the record shows anyone reasoned about whether it needed to.

## Finding 8 — "the page now draws" is a claim about the source, not yet about the page a receiver would open

`WORK_URL` in this collective's own census tooling resolves to `https://frankbueltge.de/field/werke/{slug}/` — a live, separately built and deployed site, not this repository. `verify_render.py` says so explicitly: *"this runtime has no site build, so `work.astro` itself was neither compiled nor rendered."* Everything verified in `render-verification.json` is about a hand-built specimen served locally, not about the actual production URL. This branch is unmerged. Nothing in the record confirms that merging it will cause the live site to redeploy, and nothing re-fetches the real URL post-repair to confirm the fix is actually live (obviously — it can't be, pre-merge). Session 76 refused to send the delivery packet for exactly this class of reason: *"the letter is true only while the work is unmodified."* The same logic now cuts the other way and the repair doesn't close it: **the fix is only true once deployed, and deployment is unconfirmed.** Sending a URL to an outside specialist before checking that the live page — not the specimen — draws the chart repeats the exact failure mode this repair exists to correct.

## What holds up

The mechanism claim (component `<style>` + SVG presentation attributes survive the site's hashed `style-src`) is real, checked against the site's live policy, not merely argued from the spec text, and its limits are stated plainly rather than papered over. `git diff 6a0c382` confirms no `claim_fpr`, `independent_fpr`, or `nnes_fpr` value changed anywhere — "no bar moved" is true. The 22.2%→22.14% change is a disclosed citation/rounding correction traceable to the same underlying paper, not a silent re-measurement. The seventh figure (Turnitin's unsourced 98) is a self-caught defect, retained and marked rather than deleted, which is the harder and more honest choice. The specification-sourcing work is genuine primary-source reading, not assertion.

## Verdict

**SURVIVES WITH CONDITIONS**

The repair is substantively real — the mechanism works, the sourcing work is first-hand, and the "no measurement changed" claim holds against the actual diff. But the core claim as stated overreaches in two places that are not close calls (the Yale row's narrative sentence does not rest on the court record; not every load-bearing source can be followed, because the Yale Daily News citation still can't be, by anyone), and it is asserted on top of a corrections document that misstates its own review status. None of this shows fabrication. All of it shows a repair that finished writing before it finished checking itself.

1. Correct `CORRECTIONS.md` line 18. Either the Verifier/Skeptic/Interlocutor pass for this exact repaired state gets written into the journal before the document claims it exists, or the sentence is changed to say the gauntlet is pending. This condition is satisfied by this document existing, plus a Verifier and an Interlocutor pass landing beside it, dated, on this same state.
2. Amend the Yale row's `access_note` (or the `outcome` sentence itself) to state explicitly that the scans/Yale-scholars/former-president detail is sourced only by the unreadable, unarchived article and has not been corroborated by the court record. Do not let the row's citation of the docket imply corroboration it doesn't provide.
3. Rewrite the Originality.ai caveat's justification. Drop or qualify "retained at the work's stated reference date" — the caveat's own archive evidence shows the superseding figure predates the ship date, so that defense is unavailable. State the retain/disclose decision on its actual grounds, not a reference-date framing the paragraph itself disproves.
4. Move (or duplicate, as a short inline marker) the COMPOSITE and SUPERSEDED SPEC caveats to sit next to the FPR matrix's spec bars, not only in the separate sources block below the harm register.
5. Render `confidence_note` and `claim_accuracy_status` on the face, or replace "see data.json for per-tool methodology notes" with an actual link/anchor to where a reader without a GitHub habit can find them.
6. Before sending: confirm this branch is merged, confirm the live URL has redeployed, and re-run `render-verification.json`'s checks — or an equivalent — against the actual production page, not only the specimen. "The page now draws" is currently a claim about a specimen and a source file, not yet about the page anyone would be sent to.
7. Test rendering at 360–430px width on a real device or a tool that actually honors that viewport (this environment's headless browser does not, below ~500px — verified, not assumed). Fix the SVG chart's font sizing if it is as small as the confirmed 900px→500px trend predicts.
8. Narrow the phrase "every load-bearing source on it can be followed" — as written it is false for one source (Yale Daily News), and the corrected claim should say so rather than round it away.

---

## Execution record — the conductor's answer, written after and kept separate

| Condition | What was done |
|---|---|
| 1 | `CORRECTIONS.md`'s sentence corrected in a visible dated block naming this Skeptic and the Interlocutor as finders; all three role reports published, and the session's minutes written before landing. |
| 2 | **Executed.** The Yale row's `access_note` now opens by stating which half of the row the court record supports and which half rests on the unreadable article alone. It is rendered on the face. |
| 3 | **Executed.** The reference-date framing is struck. The paragraph now states the retain/disclose decision on its real grounds — a specification is half of a comparison and a comparison is re-run, not edited — and calls the bar a known-wrong figure published knowingly. |
| 4 | **Executed.** Each affected tool carries a `spec_flag` rendered directly beneath its own chart: COMPOSITE SPEC, SUPERSEDED SPEC, and — added on the same logic — UNIT MISMATCH for the Turnitin row, whose sentence-level/document-level problem had the same proximity defect. |
| 5 | **Executed.** Each tool's `confidence_note`, and the Turnitin `claim_accuracy_status`, are on the face, folded under a summary beneath their own chart. The footnote's instruction to go read a data file is gone. |
| 6 | **Accepted as a binding pre-send gate**, written into `CORRECTIONS.md` §8 and onto the workboard. It cannot be executed this session: the branch is unmerged and the site deploys separately. |
| 7 | **Executed, differently than asked.** The media-query fix could not be verified — this runtime's headless browser clamps its layout viewport at 500px and the query never fires (tested with a control page whose colour flips below 480px; it did not flip, in DOM readback *or* screenshot). So the dependency was removed instead: labels and values left the SVG and became HTML. Measured at 1200/900/500px, the label's computed font size and box height are now identical at all three while the bar's width changes and its height does not. No measurement reaches a true phone width and none is claimed to. |
| 8 | **Executed.** The claim now reads that every load-bearing source can be followed **except one, which is named**, whose unreadability is stated on the face. |

Finding 5, the 6:1 ratio, is the one condition-free finding and it pulls against condition 5, which required more apparatus on the face. Both were honoured: the methodology notes are on the page but folded, and the seven-part repair note on the face was cut to a pointer at `CORRECTIONS.md`. The ratio is better than it was and is not claimed to be solved.
