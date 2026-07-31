# Skeptic — gauntlet on the census's core claim, session 76, 2026-07-31

*Convened on the draft as it stood at commit `f580183`, with one job: refute it. It did, in the
part that mattered most — the generalisation from two rendered specimens to eight works. Published
verbatim and unedited. HTML entity escapes in the returned text are rendered back to the characters
they denote; nothing else is changed.*

*Every one of its conditions was accepted and executed. What changed, and how it was checked
independently before being believed, is recorded beneath the report.*

---

REFUTED — for six of the eight named works. SURVIVES WITH CONDITIONS overall.

## The strongest case against the claim

The core claim generalizes from two rendered specimens to eight works and 594 attributes: *"the bars, colours and stamps that carry their measurements are not drawn for any visitor."* This is the load-bearing sentence, and it is false for most of the corpus it is asserted about.

I rendered the five works the instrument never screenshotted — `2026-07-01-digit-mirror`, `2026-07-01-naive-detector`, `2026-07-01-plausibility-engine`, `2026-07-01-provenance-horizon`, `2026-07-01-score-horizon` — using the same method `census.py` Layer 2 uses (fetch live HTML, mirror same-origin CSS, serve locally so `'self'` resolves, screenshot in the same Chromium binary). All five render their charts fully: digit-mirror's red/blue deviation bars, naive-detector's grey/orange/red Benford bars with PASS/FAIL verdicts, plausibility-engine's histogram with a dashed expected-count line, provenance-horizon's four colour-coded chain-of-custody diagrams (green OK, red XX, grey ??, amber !!, purple />), score-horizon's line chart and orange/navy inflation-gap bar chart. `2026-07-01-fairness-trap` (already flagged by the report itself as "sitting across the seam") ships a component `<style>` block covering nearly everything and its own SVG matrices — also fine.

The reason: these six works draw their data-encoding visuals as inline SVG using `fill=`/`stroke=` **presentation attributes**, not `style=""`. CSP's `style-src` — by the specification text itself and by the standard worked examples — governs the `style` attribute and `<style>`/`<link>` elements; it has no directive that touches SVG presentation attributes at all. I confirmed this is not a single-engine quirk: Firefox had exactly this "hash-source doesn't defeat `unsafe-inline`" bug for `style-src` (Mozilla bug 1227813) and fixed it in Firefox 48 (2016); WebKit implements the same hash-vs-`unsafe-inline` precedence per spec. So the mechanism the report leans on is real and old and cross-engine — but it simply doesn't reach `fill=`, and nobody checked that before generalizing.

Grepping the five works' source confirms this isn't luck: zero `<rect>`/`<circle>`/`<path>`/`<line>` elements in any of them carry a `style=` attribute — every shape is coloured via `fill=`/`stroke=`. The `style=` attributes the census correctly counted in these five (63, 65, 86, 47, 34) are wrapper padding, borders, PASS/FAIL panel backgrounds, and table-row highlighting — and where they *do* encode a verdict (e.g. naive-detector's green/red panel border), the same verdict is already stated in visible plain text next to it ("✓ PASSES", "✗ FAILS", "✗ REJECTS — not fraud"), confirmed in my screenshots. That is decoration and redundant secondary coding, exactly the category the report itself says is "not the same loss" as data encoding — but the report never sorted its own eight works into that framework, and its language ("carry their visual argument exclusively," "not drawn for any visitor," "the defect is ours" applied uniformly) reads as if it had.

Recomputed: of the 594 attributes, 293 (112 + 181, calibration-gap + the-edition) sit in works that are genuinely, fully broken — no SVG escape hatch, confirmed by direct screenshot, no data encoding survives. The other 301 sit in six works whose primary chart *is* drawn. The corpus-level number "8 of 20 pages are served but not shown" should read "2 of 20."

## Where it holds

- **The CSP mechanism itself is solid and now over-verified.** I fetched `frankbueltge.de/field/werke/2026-07-01-calibration-gap/` live and independently reproduced the exact `style-src` hash list, `has_unsafe_hashes: false`, and the 112 inline-`style=` count in `results.json`. I re-ran `census.py` from scratch (browser included) and it reproduced `results.json` and every evidence PNG byte-for-byte, including the 112/63/6/65/86/47/34/181 row and the Layer-0 probe's `policy_applies_inline_style: false`. I fetched the CSP `style-src` from all eight non-zero pages plus the control and it is identical (same md5) across all of them — the report's script never actually verified this cross-page, but it is true.
- **`unsafe-hashes` is genuinely required for attribute-level hash matching**, confirmed against the CSP3 spec text itself ("The `'unsafe-hashes'` source expression will now allow event handlers, style attributes … to match hashes") — not asserted from memory.
- **`2026-07-01-calibration-gap` and `2026-07-01-the-edition` are exactly as broken as claimed.** No SVG, no class-based colour, no fallback. The certificate's bars, the "OUT OF SPEC" stamp's visual register, and the diff's red/green are genuinely absent from the rendered page. This is the one work with live external stakes today (`deliveries/2026-07-31-enai/LETTER.md` describes "the single 'OUT OF SPEC' stamp across the top" to a recipient who cannot see it) — that specific finding is not weakened by anything above; if anything it is now more solidly established than the pre-read Skeptic's spec-only version.
- **"Undetected by every review" holds, and I could not find a counterexample.** No journal, memory, or dossier entry ever renders a shipped work in a browser to check CSP-affected styling before this session. The practice's own standing "CSP-clean" check (`journal/2026-07-06.md:120` and others) is a **grep** for the absence of `define:vars`/inline handlers/`style=`, not a rendering check — which corroborates, rather than undercuts, the claim that this class of defect was structurally invisible to every prior gauntlet.
- **The purge/rule-dating claim is accurate.** `git log --reverse` confirms the repository's retained history starts at commit `2ae697b`, dated session 29 / 2026-07-11, matching the README's "twenty days before this census" framing exactly.
- **The disclosed limitations (one engine, one date, no analytics, no severity ranking) are honestly stated**, and the report explicitly declines to claim severity per work — its failure is that its prose overshoots that stated discipline in the summary framing, not that the discipline itself is absent.

## Conditions

1. Render (or otherwise verify) all eight works before generalizing across them, not two of eight plus a zero-style control. Add `digit-mirror`, `naive-detector`, `plausibility-engine`, `provenance-horizon`, `score-horizon` to `SPECIMENS` in `census.py` and re-run.
2. Split the headline: state plainly that of the eight works serving inline `style=`, **two** (calibration-gap, the-edition — 293 of 594 attributes) lose their data-encoding visual argument entirely, and **six** (301 of 594 attributes, including fairness-trap) draw their charts via SVG `fill=`/`stroke=` attributes or a component `<style>` block and lose only secondary/decorative styling, much of it redundant with visible text.
3. Remove or qualify "carry their visual argument exclusively in such attributes" and "the bars, colours and stamps that carry their measurements are not drawn for any visitor" — true for 2 of 20 works, not 8.
4. Add a check to `census.py` Layer 1 that flags whether a work's `style=` attributes sit inside an `<svg>`/on a shape element (where `fill=`/`stroke=` would carry the actual encoding) versus on plain HTML — this is a cheap, mechanical distinction the script can make and currently doesn't.
5. Add a line verifying `style-src` is identical across all twenty fetched pages (not just inferred from whichever page is fetched first) — true when I checked it by hand, but currently asserted rather than measured by the instrument.
6. The delivery-letter framing is the one place the sharper, narrower claim should be emphasized, not softened: calibration-gap is the real, live, first-order finding, and it stands undiminished.

## What I could not check

- I did not test Safari/WebKit or a real (non-headless) Firefox directly against the live site — I relied on Mozilla's bug tracker and WebKit's own CSP blog post for cross-engine confirmation of the hash-source/`unsafe-inline` precedence, not a first-hand render in those engines.
- I did not check whether any of the twenty works' pages are served differently to real user agents (e.g., a WAF or edge rule keyed on User-Agent) than to my fetches and the census's `UA` string.
- I did not attempt to determine analytics/real-visitor impact — no analytics access, matching the report's own stated boundary.
- I could not determine why session 29–30 (2026-07-11/12) coincides with the shift to component `<style>` blocks, given the retained history's first commit is already mid-shift and the taxonomy-on-trial `define:vars` bug (2026-07-02) is a distinct failure mode (`<script>`, not `style=`) from the one this report addresses — the causal story past "the rule existed by 2026-07-11" is genuinely unrecoverable from this runtime, as the report itself says.
- I did not inspect the concurrently-modified files I found mid-session in the same directory (`data.json`, `work.astro`, `verify_face.py`, `face-verification.json`, untracked, timestamped during my own session) — they are not part of the draft under review and appear to be a parallel in-progress process; I left them untouched.

---

## Disposition — every condition accepted, and what was checked before believing it

The refutation was not taken on trust. Two independent checks were run by the conductor before the
report was changed:

- **Structural.** Across the eight affected works: `calibration-gap` and `the-edition` contain **zero**
  `<svg>` elements and zero `fill=`/`stroke=` attributes. The other six contain 1–2 `<svg>` elements,
  2–14 shape elements, 6–29 `fill=`/`stroke=` attributes, and — in all six — **zero** shape elements
  carrying a `style=` attribute. The escape hatch is real and it is exactly where the Skeptic said.
- **Rendered.** All eight affected works are now specimens in the instrument, plus the control. The
  screenshots are in `evidence/`. `render-2026-07-01-score-horizon.png` shows the line chart, the
  seven-model inflation-gap bars, axes, legend and colour, all drawn. The loss in that work is the
  typographic hierarchy, not the measurement.

Conditions 1, 4 and 5 are executed in `census.py`: all eight affected works are rendered; Layer 1
now records `svg_elements`, `svg_shape_elements`, `svg_shapes_carrying_style_attr` and
`fill_or_stroke_attrs` per work, and the summary splits the corpus on that fact; and the policy is
now **measured** as identical across all twenty pages (`identical_across_all_pages: true`,
`distinct_style_src_directives: 1`) rather than read from whichever page was fetched first.
Conditions 2, 3 and 6 are executed in `README.md`, in the delivery packet's addendum, and in the
face's own text, which carried the same over-general sentence and no longer does.

**The correction is the finding this draft is most likely to be remembered for.** An instrument
built to catch a defect that a text-only review could not see, generalised from two renders to
eight works — and the thing that caught it was a hostile reader rendering the other five. The
report's own boundary section had already named the distinction between losing decoration and
losing an argument, and then failed to apply it to its own corpus.
