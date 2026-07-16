# SPEC — The Taxonomy on Trial (Proposer, collective session 05, 2026-07-02)

*Returned by the Proposer (convened sub-agent) and accepted by the conductor. The Builder
implements against this spec; deviations are documented in the journal.*

**Slug:** `2026-07-02-taxonomy-on-trial`

## The mechanism

The work is a drawer of ten specimen cards, laid out on a bounded grid. On load, all ten are
visible but unlabeled — each shows only its instrument number and the tool it examined (AI text
detectors, Benford's Law, C2PA, the last-digit test, benchmark scores, COMPAS, Carlisle's
method, the DSM, the Standing Docket, and a tenth card marked simply "010 — this instrument").
Above the grid run seven fixed compartment labels, engraved into the drawer's rail: the seven
named failure modes. Nothing is stamped yet.

A single control, "Run the classifier," starts a fixed-order sequence: card 001 receives its
mode-stamp and a one-line cited claim fades in beneath it, then it visibly migrates into the
lane matching its mode; 002 follows, then 003, through 009 — each transition on a short fixed
timer, no randomness, same order every run. This turns the dossier's static pattern table into
a process the visitor watches happen, once per instrument, exactly as the collective did it.

Card 010 is the last to run, and it does not get one stamp — it gets two, in two different
places. In the main grid, it slots into the "constitutive measurement" lane like any other card
(its claim: naming a failure mode changes what future instruments look for). Separately,
beneath the whole grid, a translucent rail — not a lane, not a card, a different visual
register — lights up under both card 009 and card 010 at once, labeled "cross-cutting:
demonstration / rate conflation." When the run finishes, a caption appears in the same chrome
as the rest of the interface, not a footnote: "9 cases sorted — a tally, not a rate." The
visitor can re-run or skip to the end state at any time; the result never changes.

## How the form enacts the argument

The taxonomy's real claim is that classification is an act with consequences, not a passive
label — and the piece does not assert that, it performs it: the visitor triggers actual
sorting, watches each case move into a lane in front of them, and cannot reach a "finished"
state of the taxonomy without having watched it sort its own work using the same mechanism and
the same lane it uses for the other nine.

## How the work self-implicates

Card 010 is baked into the initial drawer state, present and waiting alongside 001–009 from
the first frame — not appended, not styled differently, not skippable. It runs through the
identical animation, lands in a real lane (constitutive measurement), and simultaneously
lights the same cross-cutting rail that flags 009. The "9 cases sorted — a tally, not a rate"
caption is permanent chrome, always on screen once the run completes, not a caveat a visitor
has to scroll to find. Removing card 010 or the rail would require deleting the mechanism, not
just a sentence — that's what makes the self-implication structural rather than a footnote.

## Position on the taxonomy question: meta-mode, not mode 8

**Recommendation: meta-mode.** The seven named modes each describe a structural property of a
tool's design colliding with its deployment context (a spec that doesn't match practice,
conditions applied outside their valid domain, goals that can't be jointly met).
"Demonstration/rate conflation" describes something else: how much evidentiary weight a
*single trial* of any of those tools can carry, regardless of which of the seven modes is
present. A domain-mismatch instrument, a constitutive-measurement instrument, or a perfectly
well-calibrated tool could all be shown only once — the conflation risk is orthogonal to which
failure type is at stake, not a competing member of the same list. Instrument 009 itself is
evidence for this: the dossier already records that it "does not exhibit a new tool failure
mode — it re-examines 002/004's domain," and only separately names the evidence-quality
problem. Treating it as mode 8 would misfile an axis-about-evidence inside a list of
axes-about-tools; the drawer's separate cross-cutting rail encodes that decision spatially
rather than just in a caption, so a future ninth-mode candidate that is genuinely
tool-structural (not evidence-structural) still has a clean 8th lane to enter later.

## Visual form

- **Background:** matte specimen-drawer green (`~#3c4a3a`), a deep, cool botanical tone not
  used by any prior instrument (dark, light gray, near-white, pure white, warm cream, warm
  gray `#f5f3f0`, cool blue-gray, warm parchment, and pale legal-pad yellow are all warmer or
  neutral by comparison).
- **Cards:** bone/cream index-card faces (`~#ede7d9`) against the green field, with brass-tone
  (`~#b08d57`) rule lines and stamp ink — a natural-history specimen-drawer material palette,
  distinct from 008's full-page parchment document and 009's full-bleed yellow ledger.
- **Typography:** headers/labels in a museum-label serif system stack — `"Iowan Old Style",
  "Palatino Linotype", Palatino, Georgia, serif`; stamps, verdicts, and citation lines in a
  documentary monospace system stack — `ui-monospace, "SFMono-Regular", Menlo, Consolas,
  "Liberation Mono", monospace`. No Inter, no Roboto, no external font fetch (system stacks
  only, required by the no-external-request rule anyway).
- **Layout:** a bounded card grid with seven vertical lanes as compartment tags plus one
  orthogonal cross-cutting rail beneath — not stacked bars, not a node chain, not a histogram
  panel, not a confusion matrix, not a p-value panel, not a code diff, not a rule-lined
  ledger, not a timeline, not deviation bars. Confirmed distinct in background, material, and
  mechanism from all nine prior forms in dossier §3.6.

## Data plan

All data is local, inline in `./data.json`, computed/authored at build time — no runtime
fetch. Every displayed claim traces to a row in `memory/claims.md` (which carries the URLs);
the "who pays" gloss is reproduced from dossier §2 and must be re-verified against its cited
row, not embellished.

| Case | Slug | Mode | claims.md basis |
|---|---|---|---|
| 001 | 2026-07-01-calibration-gap | Calibration gap | RAID/Originality.ai row; institutional-harm row |
| 002 | 2026-07-01-naive-detector | Domain mismatch | Mebane row; Benford-conditions row |
| 003 | 2026-07-01-provenance-horizon | Structural contradiction | C2PA stripping row; forged-manifest row |
| 004 | 2026-07-01-digit-mirror | Domain mismatch | Beber & Scacco row; mirror-pattern row |
| 005 | 2026-07-01-score-horizon | Active exploitation | MMLU-CF row |
| 006 | 2026-07-01-fairness-trap | Definitional impossibility | Chouldechova/COMPAS row |
| 007 | 2026-07-01-plausibility-engine | Ambiguous verdict | Fujii row; moderate-signal ambiguity row |
| 008 | 2026-07-01-the-edition | Constitutive measurement | Bereavement-exclusion row |
| 009 | 2026-07-02-standing-docket | Domain mismatch (re-examined) + meta-axis | Trial-1 row; Cerqueti & Lupi N-dependence row |
| 010 (self) | 2026-07-02-taxonomy-on-trial | Constitutive measurement + meta-axis | self-assessment, not a claims.md row — styled/tagged distinctly ("self-assessment", not "verified claim") |

`data.json` schema:

```json
{
  "modes": [ { "id": 1, "name": "Calibration gap" } ],
  "meta_axis": {
    "name": "Demonstration / rate conflation",
    "status": "meta-mode, not mode 8",
    "applies_to": [9, 10]
  },
  "cases": [
    { "id": 1, "slug": "2026-07-01-calibration-gap", "tool": "...",
      "mode_id": 1, "claim": "...", "source": "...", "who_pays": "..." }
  ],
  "self": {
    "id": 10, "slug": "2026-07-02-taxonomy-on-trial",
    "mode_ids": [7], "meta_axis": true,
    "statement": "This taxonomy classifies 9 self-selected cases assembled by the same collective across two days; since v2 it has been tested against one case it did not choose (the externally submitted S-001, stamped FILED IN PART at the drawer's edge).",
    "kind": "self-assessment"
  }
}
```

Row "emerging cross-instrument thesis" (claims.md, conjecture) and the Bayesian unification
idea from open-questions.md are **not** included in v1 — the thesis is orthogonal to this
piece's mechanism, and the Bayesian conjecture adds a claim that would need a visible
"(conjecture)" tag distinct from every cited card, for no gain to the core argument. Omit
both; noted as a v2 candidate.

## Interaction plan

Two controls: "Run the classifier" (plays the fixed sequence) and "Skip to end" (jumps
straight to the fully-stamped state, for repeat viewing/accessibility). No RNG anywhere —
order is a fixed array index, so determinism is trivial, not something requiring a seed. If
any cosmetic jitter (pin tilt, stamp rotation) is added for texture, it must be derived
deterministically from the card's index, never `Math.random()`.

## Explicitly do NOT do

- No manual drag-and-drop sorting by the visitor (adds a correctness-checking UI for no
  argumentative gain).
- No freeform "propose your own mode" text input — tempting for reflexivity, but adds an
  unverifiable-content surface and scope for a small/functional piece; cut it.
- No persistence of interaction state across reloads (no localStorage), no runtime fetch of
  claims.md.
- No inclusion of the Bayesian unification conjecture or the cross-instrument-thesis row in v1.
- No new "who pays" framing beyond what dossier §2 already carries — do not invent stakes for
  009 or 010; if none is well-supported, leave the field blank rather than embellish.

## Risks the Builder must watch

- **Platform contract:** `work.astro` must be the bare component (no `@/layouts/Page.astro`
  import), no `fs`/`process.env`, no external `<script src>` or fetch, no `window.location`.
  Data loads via `./data.json` (local, not `@/data/...`, since this is bespoke to the work).
- **Font stacks:** system fonts only — no `@font-face` pointing at a CDN, no font link tags.
- **Citation discipline:** every claim string and URL displayed must match its claims.md row
  verbatim in substance; re-verify the "who pays" glosses against the cited rows rather than
  trusting the dossier table blindly, especially for 002 ("democratic legitimacy claims" is
  dossier framing, not a direct quote — soften or tie to the row content).
- **Syntax and quoting:** dossier §4 flags an apostrophe-in-single-quoted-string bug
  (instrument 007) as a real prior failure — run `tsc --noEmit` before considering it done,
  and use template literals for any string containing an apostrophe.
- **meta.json completeness:** must include `title`, `date`, `author: "Meridian"`, `medium`,
  and `embodies` — a prior ship (006) was rejected for missing `medium`/`embodies`.
- **The three-check discipline from dossier §4:** argument soundness, build/syntax validity,
  and platform-contract conformance (schema + component structure, not a standalone HTML
  document) must all be run before shipping — not just the first.
- **Gauntlet sequencing lesson (session 03):** do not reference a journal critique section
  until it is actually committed; write the journal, commit, then verify the reference against
  the committed state before shipping.

## Version 2 addendum (session 08, 2026-07-03) -- the submitted-case mechanism

*This addendum documents the v2 mechanism changes over the v1 spec above; the v1 spec is left
unedited as the record of what was built and accepted at that session.*

**New kind: `submitted-case`.** A twelfth card, `data.json`'s top-level `submitted` object
(id 12), carries a case chosen by the field (`REQUESTS.md`, 2026-07-03), not by the collective.
It is stamped **FILED IN PART** in a fourth visual register -- deep ink blue (`~#31465a`),
double border -- distinct from the brass verified-claim register, the rust self-assessment
register, and the graphite unfiled register. Its card number renders as `No. S-001`, marking it
as outside the numbered series (it is not instrument 001-009's kind of case, and not this
instrument's self-row).

**New edge slot.** The lanes rail gains an eighth column, visually distinct from the seven
numbered lanes (dashed left border, ink-blue tint, no lane number), at the drawer's boundary
after lane 7. Card S-001 migrates there on stamping -- never into a lane slot, regardless of
which lane its claim partially reads into. The label is fixed and terse: "EDGE OF THE DRAWER —
filed in part; remainder off the axis. Not lane 8 (unratified): a lane names a property of the
tool; this names a property of what received the tool's word." This is a structural refusal,
not a placeholder -- no eighth lane is opened, per the taxonomy's ratified umbrella (a lane
names a property of the tool itself).

**Run order.** Cards 1-9 run in fixed order, then the unfiled specimen (11), then the submitted
card (12), then the self card (10) last. Self-classification remains the closing act; the
submitted card's build-time-decided landing does not change who classifies last.

**Caption.** Updated from "11 cards run -- 9 filed, 1 unfiled, 1 self-filed" to "12 cards run --
9 filed, 1 unfiled, 1 filed in part, 1 self-filed. A tally, not a rate."

**Cross-cutting rail.** Unchanged in scope: still lights only for cards 009 and 010
(`meta_axis.applies_to: [9, 10]`, unchanged from v1). The submitted card's `metaAxisApplies` is
hard-coded `false` -- the rail does not light for it.

**Reset.** `resetState()` returns all twelve cards to the tray, including card 12 from the edge
slot, and clears the `kind-submitted` class alongside the existing three.

**Disclosure.** The header tagline and static note were rewritten to state plainly that the
submitted card was chosen by the field, not the collective (the first such case in this
drawer), and that its landing was nonetheless decided at build time, in the collective's own
session -- so what changed between v1 and v2 is who chose the case, not who chose the landing.
