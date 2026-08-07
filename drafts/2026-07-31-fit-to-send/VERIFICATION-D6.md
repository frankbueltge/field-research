# Verifier on the D6 result — verbatim

*Convened 2026-08-07 (session 99) against `RESULT-D6.md` and `results/bindings.json` at commit
`192775a`. **Scope is narrower than it should have been, and the reason is infrastructure, not
judgement:** two fuller dispatches of this check — and a Skeptic against the core claim — were
lost mid-run to worker restarts. This third dispatch was deliberately cut to the four load-bearing
arithmetic checks so it would return. **What it does not cover is listed by the Verifier itself at
the end and is owed.** Reproduced unedited.*

---

VERDICT: PASS

1. CHECK 1 — headline census counts.
(a) Claim: 166 unique (work, normalized_url) evidence+site pairs; 156 of them not linked anywhere in their own work.
(b) Computed independently from `results/inventory.json` `identifiers` array: built the set of (work, normalized_url) with role="evidence" and tier="site" → 166. For "linked anywhere in their own work," matched against other identifier rows sharing the same (work, url, role=evidence, tier=site) — duplicates exist (34 pairs have >1 occurrence, 7 with mixed presentation, e.g. `2026-07-01-fairness-trap` / propublica COMPAS URL: `displayed` in `meta.json:15`, `linked` in `work.astro:559`) — giving linked=10, not-linked=156. Script: `/tmp/.../scratchpad/verify/check1.py`.
(c) non-blocking (reproduces).
(d) None needed. Note: a naive "any row anywhere in the work regardless of role/tier" reading gives 25 linked/141 not-linked instead — the correct reading is scoped to the evidence+site population itself, and only that reading reproduces the claim; worth stating explicitly since "anywhere" is ambiguous on first read.

2. CHECK 1 — after-figures from `_arm_s[<work>].linked_by_binding`.
(a) Claim: 42 linked, 124 displayed-only, 74.7%.
(b) Took `linked_by_binding` from `results/bindings.json` `_arm_s` as given (32 unique pairs, all confirmed ⊆ the 166-pair population, zero overlap with the 10 already-linked). Union with the 10 from Check 1 gives 42 linked / 124 displayed-only / 74.7%. Same script.
(c) non-blocking (reproduces exactly).
(d) None needed.

3. CHECK 2 — render check across the 18 works.
(a) Claim: 42 against 42, zero disagreements.
(b) For each of the 18 works carrying ≥1 site-tier evidence URL (independently confirmed to be 18, summing to 166), parsed `dist/field/werke/<slug>/index.html` with Python's `html.parser`, restricted extracted hrefs to that work's census URLs (any tier/role), removed the 4 chrome URLs from `bindings.json` `_arm_r.pages._chrome_links_excluded`, and compared to "census linked ∪ linked_by_binding" for that work. Cross-checked my extractor against the builder's own recorded `linked_urls_before_chrome_exclusion` for `2026-07-01-calibration-gap` — identical set. Totals: 42 rendered-census-links found, 42 practice-claimed-linked, zero per-work disagreements. Script: `/tmp/.../scratchpad/verify/check2.py`.
(c) non-blocking (confirmed).
(d) None needed.

4. CHECK 3 — chrome-link universality.
(a) Claim: 4 URLs are chrome, universal across rendered instrument pages.
(b) Extracted hrefs from every page under `dist/field/werke/` (22 directories present, one more than the 21-work pinned census — an extra work `2026-08-05-the-second-reader` outside the population). All 4 listed chrome URLs (`creativecommons.org/licenses/by/4.0/`, `frankbueltge.de`, `github.com/frankbueltge`, `github.com/frankbueltge/field-research`) present on 22/22 pages, including the out-of-population one. Script: `/tmp/.../scratchpad/verify/check3.py`.
(c) non-blocking (confirmed).
(d) None needed.

5. CHECK 4 — the-floor `??` case.
(a) Implicit claim: report[0] has both `official_url` and `pdf_mirror_extracted` non-null, and only the former is rendered as a link.
(b) `works/2026-07-09-the-floor/data.json` `subject.reports[0]`: `official_url` = `https://sustainability.google/reports/google-2025-environmental-report` (non-null), `pdf_mirror_extracted` = `https://www.smartenergydecisions.com/wp-content/uploads/2025/07/google-2025-environmental-report-1.pdf` (non-null). Parsed the rendered page's `<a href>` set: `official_url` present, `pdf_mirror_extracted` absent (a different report's PDF URL, from `reports[1]`, is present instead, confirming the extraction is not simply missing all PDFs).
(c) non-blocking (confirmed).
(d) None needed.

WHAT I DID NOT CHECK — out of scope for this dispatch: `scripts/resolve_bindings.py` itself (not run or read, per instruction); the 23 selftest assertions of Arm S; the `git diff` byte-identity claim between pinned commit and HEAD across all 21 works; the receiving-site's 8-file/17-line `@ts-nocheck` diff claim; the P5–P8 prediction narrative and the Skeptic's pre-read reasoning; `tools/record_ceiling_check.py` word-count figures in §7; the `2026-08-05-the-second-reader` work (outside the 21-work pinned population, present in the build but not examined further); anything in `FINDINGS.md`, `FINDINGS-V2.md`, or `memory/discarded.md`.

---

## The collective's answer, on the record

**The verdict covers the four checks it names and nothing else, and this file says so at the top
rather than letting a PASS read as coverage it does not have.** In particular: **no Skeptic ran
against the core claim on this state**, and the resolver's own code was neither read nor run by any
reviewer. Both are owed before this draft can ship, along with the Interlocutor.

**Finding 1(d) is taken and worth keeping.** "Not linked anywhere in its own work" is ambiguous
between two populations, and only one of them reproduces 156. The census's own rule
(`inventory.py`, the L0-4 block) is the scoped reading — evidence occurrences, any tier, against
that work's site-tier evidence URLs — and the Verifier's alternative reading is a genuinely
different question that would give 141. The phrase is now known to be load-bearing; a future
version of this record should state which population it means in the sentence itself.

**One further check exists and is not a Verifier's.** The conductor re-derived 166 / 156 / 42 /
124 / 74.7 %, the 5 linking works, the 19 remaining displayed citations inside them and the 18
works carrying a rendered-tier citation, with code written without importing
`scripts/resolve_bindings.py`. Every figure reproduced. **That is the builder checking the builder
and is recorded as such — it is not independence, and it does not stand in for what was lost.**
