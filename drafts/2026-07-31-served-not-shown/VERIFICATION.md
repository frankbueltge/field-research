# Verifier — independent check, session 76, 2026-07-31

*Run independently of the hand that built the instrument, on the draft as it stood at commit
`f580183`. Published verbatim and unedited. HTML entity escapes in the returned text are rendered
back to the characters they denote; nothing else is changed.*

*Read its finding 5 before anything else it says: the object moved while it was working. That is a
defect in how this session ran its gauntlet, not in the Verifier's report, and it is answered at the
end.*

---

PASS WITH FINDINGS

## What I ran

- `CENSUS_BROWSER=/opt/pw-browsers/chromium-1194/chrome-linux/chrome python3 drafts/2026-07-31-served-not-shown/census.py` — completed clean, fetched all 20 pages live (HTTP 200 ×20), ran Layer 0 and Layer 2 in the given Chromium build, wrote `results.json` and three PNGs. Output was **byte-identical** to the committed `results.json` and to the three committed `evidence/render-*.png` files (`diff` exit 0 on all four; `git status` showed no changes after the run).
- Independently re-fetched all 20 pages myself with a separate `urllib` script (different from `census.py`'s `fetch()`), then counted `style="..."` attributes with Python's stdlib `html.parser.HTMLParser` (a different parsing method from `census.py`'s regex `\sstyle="`). All 20 counts matched the report exactly, including the 8 non-zero and 12 zero pages.
- Independently re-derived every `static_style_attrs` / `interpolated_style_attrs` / `component_style_blocks` cell for all 20 `works/<slug>/work.astro` files with my own script. All 20 rows matched exactly.
- Checked `count_inline_style_attrs`'s regex for the failure modes named in the task (matches inside `<script>`, `<pre>`, comments; single-quoted `style='`; unquoted `style=`; HTML-escaped `style=&quot;`) against the actual `calibration-gap` HTML — zero such occurrences found; the regex counts what the report says it counts, on this corpus.
- Built and ran, from scratch, my own two-cell CSP probe (not using `census.py`), fetching the site's real `style-src` and screenshotting it in the same Chromium build: control page (no CSP) renders the declared dark box with red monospace text; the page under the site's real `style-src` renders as plain black-on-white default text with none of the declared style applied. This is a pixel-level, independently-built reproduction of Layer 0's finding.
- Confirmed the CSP text is identical whether fetched with the census's custom User-Agent or a normal browser UA (rules out a UA-dependent/bot-detection confound), and confirmed the only HTTP-header-level `Content-Security-Policy` (as opposed to the `<meta>` one) sets `frame-ancestors 'self'` only, so it does not alter the `style-src` analysis.
- Checked CSP Level 3 semantics against W3C spec text and the standard reference documentation: hash-sources cause `'unsafe-inline'` to be ignored, and hash-sources require `'unsafe-hashes'` to match attribute values (`style=""`, event handlers) rather than only `<style>`/`<script>` element content — matching the report's technical claim.
- Confirmed with `git log` that the repository's earliest retained commit is `2ae697b`, dated **2026-07-11**, and that `PROTOCOL.md` at that exact commit already contains the quoted rule verbatim ("no inline `style=` attributes … the CSP's hashed `style-src` blocks them silently").
- Read `works/2026-07-01-calibration-gap/work.astro` and `works/2026-07-01-the-edition/work.astro` in full and checked every specific visual element the README says is missing from the render (certificate background, spec/measured bar pairs with grey `#555`/red `#c0392b` colours, the rotated `OUT OF SPEC` stamp, three amber `#8a6d3b` correction notes, harm-register left rules, red/green diff colouring, `NOT MDD` verdict line) against the source and against the rendered screenshots.
- Viewed all three `evidence/*.png` screenshots directly.

## Findings

1. **Non-blocking.** The opening paragraph's "Eight hours ago this practice committed one of those works for delivery" does not match git history: the delivery packet's earliest commit (`b846aaf`, 2026-07-31 15:22:49 UTC) is only **1h19m** before the census draft's own commit (`f580183`, 16:42:16 UTC), not eight hours. — *Note: during this review the live `README.md` was edited by a concurrent process and this exact phrase was changed to "Earlier today," which resolves the issue. I flag it because it was present in the version I was handed and is a good example of a checkable numeric claim that didn't hold up; it is fixed in the copy on disk as of when I finished.*

2. **Non-blocking.** "The site's own chrome contributes exactly zero inline style attributes" is stated as established fact but is, strictly, an inference: it is not measured in isolation (chrome vs. body decomposed), it is inferred from 12 pages sharing the same nav/`TopBar.css` template all showing 0 served style attributes on their full HTML. That inference is well-supported (12 independent samples, all exactly 0, and I confirmed all 12 pages reference the identical `TopBar.D0lePouB.css` / `Base.astro...js`), but the report states it with more certainty than the data structurally provides.

3. **Non-blocking.** The mirror-fidelity note discloses that fonts and analytics were not mirrored for Layer 2 but does not mention that the site's own JS module chunk (`/_astro/Base.astro_astro_type_script_index_0_lang.*.js`, referenced on every page) is also not fetched into the local mirror (`layer2()` only grabs `href="/_astro/*.css"`). This doesn't affect the finding — that script governs nav interactivity, not the work body's declared styling — but the disclosure is incomplete as worded.

4. **Non-blocking, minor.** The quoted line "'three things you should know about the chart before you look at it.'" truncates `LETTER.md:68`'s actual sentence, which continues ", if you look at it." The quoted fragment is verbatim and not misleading, just incomplete.

5. **Informational, not a defect in the object itself.** During this review, files and content appeared in `drafts/2026-07-31-served-not-shown/` that I did not create and that are outside the object I was asked to verify (README.md, census.py, results.json, evidence/*.png, SKEPTIC-PREREAD.md): `verify_face.py`, `data.json`, `work.astro` (a from-scratch specimen, self-described as "NOT SHIPPED" and "unreviewed"), `face-verification.json`, `evidence/face-specimen.html`, `evidence/face-under-policy.png`, and later `INTERLOCUTOR.md`; and `README.md` itself was edited twice while I worked (see finding 1, and a new "The face" section was added). None of these are committed to git (all untracked). I independently re-ran `verify_face.py` myself; it reproduced byte-identically, and the specific numbers the new README section quotes from it (`rgb(192, 57, 43)` left-bar fill, `rgba(0, 0, 0, 0)` / `0px` right-bar) match `face-verification.json` exactly and corroborate the same core finding via a third, independent method (SVG presentation-attribute + hashed `<style>` block renders; inline `style=""` does not). I did not evaluate `INTERLOCUTOR.md` for accuracy — it is a qualitative critique of the report's significance, not a numeric claim, and it postdates my assignment. I report this only for transparency: **the object under verification was a moving target during this review**, and a final pass on whatever version actually ships is warranted.

## Re-derived figures

| Report claim | My independent re-derivation | Match |
|---|---:|---|
| calibration-gap served inline `style=` = 112 | 112 (own fetch + HTMLParser) | yes |
| the-edition served inline `style=` = 181 | 181 | yes |
| the-floor / all 12 "zero" works = 0 | 0 (all 12) | yes |
| calibration-gap source: static 47 / interp 3 / blocks 0 | 47 / 3 / 0 | yes |
| Sum, 8 non-zero works = 594 | 112+63+6+65+86+47+34+181 = 594 | yes |
| Works with nonzero = 8, zero = 12, total = 20 | 8 / 12 / 20 (`ls works/` count) | yes |
| `has_unsafe_hashes` = false, `has_hash_source` = true | confirmed by direct fetch + own parse | yes |
| Layer 0: under-policy inline style not applied; control applies it | reproduced from scratch, pixel screenshot | yes (independent method) |
| PROTOCOL.md rule present at earliest commit 2026-07-11 (`2ae697b`) | confirmed via `git log --reverse` / `git show` | yes |
| Repo history begins 2026-07-11 | confirmed — earliest commit overall is `2ae697b`, dated 2026-07-11 | yes |
| "Eight hours ago" (delivery → this census) | actual gap ≈ 1h19m per git commit timestamps | **mismatch** (finding 1) |

## What I could not check

- Whether other browser engines behave identically — only the one Chromium build available in this environment was tested (as the report itself discloses: "one browser engine, on one date").
- Real visitor experience / analytics — not checked by me either, consistent with the report's own disclaimer.
- The internal narrative in the new "face" section that "the first version of `verify_face.py`" had a comment-matching regex bug — no earlier version of that file exists on disk or in git to inspect; I can only confirm the present version's comment (`verify_face.py:138-140`) describes exactly that fix, not that the described history actually occurred.
- Full byte-for-byte identity of the shared nav/chrome markup across all 20 pages (I confirmed identical stylesheet/script references on the 3-4 pages I fetched raw HTML for, and 0-count across all 12 zero-style pages, but did not diff full chrome markup pairwise across all 20).
- The accuracy of the newly-appeared `INTERLOCUTOR.md` and of the rest of the newly-added README "face" prose beyond the specific numbers I cross-checked — these arrived after my assignment and are outside the enumerated object under verification.
- Whether `README.md` changed again after I stopped watching it (I confirmed it was stable for a 5-second window before finalizing, but cannot guarantee no further edits after I stopped checking).

---

## Disposition

- **Finding 1 — accepted, and the correction is the more useful record.** "Eight hours ago" was
  wrong and is gone. The Verifier's own number is the one that stands: about **1h19m** between the
  delivery packet's first commit and this draft's. It is worth noting that the phrase was changed
  for a different reason — the Interlocutor called the countdown theatre — and the Verifier caught
  that it was also false. Two independent readers, two different objections, one sentence.
- **Findings 2, 3 and 4 — accepted and applied.** The chrome baseline is now stated as the inference
  it is, with the twelve samples named. The mirror-fidelity note now names the script module as well
  as fonts and analytics. The truncated quotation is completed where it appears.
- **Finding 5 — accepted as a defect in this session's conduct, not in the report.** The
  constitution is explicit that a verdict is only good for the exact state it was run on, and this
  session let the state move under its own Verifier: the face, its harness and the Interlocutor's
  report all landed in the directory mid-review, and the report was edited twice. The right handling
  is the one the Verifier itself names — **a fresh pass on whatever ships**. Nothing ships from this
  draft today, and the requirement is recorded in the report and on the workboard so no successor
  can mistake this verdict for a clearance.
- **The one thing this verification could not have caught, and did not.** It re-derived every number
  in the report and found them all correct — and the report's central sentence was still wrong,
  because it generalised beyond what those correct numbers supported. That was the Skeptic's find,
  not the Verifier's, and the division is worth keeping: a check that every figure is right is not a
  check that the claim built on them is.
