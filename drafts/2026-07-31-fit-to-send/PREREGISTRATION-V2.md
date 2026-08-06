# Fit to Send — second pre-registration (the amended census)

**Locked 2026-08-06 (session 93), before a single line of the scripts was changed and before any
re-run.** Git history is the timestamp: this file is committed in a state whose parent commit
contains neither an amended script nor a v2 result. Written by the conductor. No role had been
convened when it was written.

**It does not edit `PREREGISTRATION.md`.** That lock stands exactly as it was, and the v1 results it
governs stand with it, including the parts `FINDINGS.md` shows to be wrong. A rule changed in the
light of results is not a rule; a rule *replaced in the open, with the defect that forced it named
and the outcome predicted first*, is one.

---

## 0. What is already known, and therefore cannot be claimed afterwards as a prediction

Stated here because hiding it would make this document a decoration:

1. The five `GONE` verdicts of the v1 census and their hand-checked causes, adjudicated in
   `FINDINGS.md` §1 on 2026-07-31: **not one was a dead source.**
2. The four design defects those five exposed — D1, D2, D3 (`FINDINGS.md` §1) and D4 (`FINDINGS.md`
   §2), where D4 is that the sweep reads what a page **displays**, not what it **links**.
3. The corpus has grown: **21 work directories under `works/`**, not the 20 the v1 pin names.
4. `works/2026-07-31-fit-to-send` is not among them. This draft is not in its own census.

What is **not** known to the conductor at the time of writing, and is what the predictions below put
at risk: any v2 verdict, any count of re-classified identifiers, and every number in §4.

---

## 1. The object, re-pinned

The **21** work directories under `works/` at the commit that is this session's opening marker on
branch `research/session-2026-08-06`. The pin is written into `scripts/inventory.py` as before, and
the per-file SHA-256 record is what makes the pin checkable rather than decorative.

---

## 2. The four amendments, each against the defect that forced it

### A1 — inline corrections (answers D1)

**The defect.** `correction-record` was assigned **by file** and by markdown **heading**. A
correction written inline on a rendered surface is invisible to both. The case:
`works/2026-07-01-fairness-trap/work.astro:590` reads *"Correction, 2026-07-28. Until this date the
entry cited doi:10.3030/101135953…"*. v1 counted that withdrawn DOI as a fresh dead source against
the one work most transparent about its own error — the exact inversion the v1 role rule existed to
prevent, one level down.

**The amendment.** An identifier is `correction-record` if a **correction marker** occurs in the
text *before* it and *within the same block*.

- **Marker list — the v1 heading list, plus one word.** v1's locked list is
  `corrected · withdrawn · was wrong · superseded · discarded`. The case that forced D1 uses the
  **noun**, so `correction` is added and nothing else. Extending an already-locked list to a new
  scope is the least post-hoc move available; inventing a fresh list in the light of results is the
  most.
- **Scope — forward only, to the end of the block.** From the marker's character offset to the
  first of: a blank line, or a block-break token (`<br`, `</p>`, `<p `, `<li`, `</li>`, `<h`).
  Forward-only is what keeps the *live* citation one line above the marker
  (`work.astro:589`, the working `eur-lex` link) out of the correction bucket.
- v1's file rule and heading rule are unchanged and still apply.

**Over-catching is the risk this amendment carries**, because `discarded` and `was wrong` are
ordinary words in this archive's prose. So the re-run **must publish the full list of identifiers
whose role changed from `evidence` to `correction-record`**, one line each, with file and line
number, so that a reviewer can dispute any of them individually. A silent role change is a
suppressed citation.

### A2 — an identifier that is a method, not a document (answers D2)

**The defect.** v1 had `NOT-A-LOCATOR` for syntactic placeholders and nothing for a citation that
is a *method*: a query endpoint or a directory path. Three of the five `GONE` were these.

**The amendment.** A pre-fetch bucket **`NOT-A-DOCUMENT`**, assigned from the normalised string
alone, before any request, in two named sub-rules:

- **`BASE-PATH`** — the path ends with `/` **and** carries at least two non-empty segments. (A host
  root, `https://example.com/`, has zero and stays in the census: a site root is a document.)
- **`QUERY-ENDPOINT`** — the host begins `api.` **or** the path carries a segment exactly `api`,
  **and** the URL has **no query string**. A parameterless endpoint is a method; the same endpoint
  carrying parameters returns a document and stays in the census.

Every `NOT-A-DOCUMENT` is **listed in full** in the record, with its sub-rule, so each can be
disputed one at a time.

### A3 — 401 is a wall, not a death (answers D3)

**The defect.** The locked verdict table excluded 403 and 429 from `GONE` and forgot **401**, so a
paywall was published as a removal (`reuters.com`, v1 `GONE`).

**The amendment.** `BLOCKED` becomes **401, 403, 429**. **Considered and declined:** 402, 407 and
451. No case for any of them exists in this corpus, and widening a rule further than the defect that
forced it is how a locked design becomes a wish list.

### A4 — displayed is not linked (answers D4, and it is the largest)

**The defect.** Every v1 verdict is a statement about **a string shown to a reader**, not about a
hyperlink — and until `FINDINGS.md` §2 nobody had noticed, so the record read as though it answered
"do this work's links work". Both are legitimate questions. They are not the same question, and v1
could not tell them apart.

**The amendment.** Every identifier occurrence carries a **`presentation`** field, decided from the
characters immediately preceding it:

- **`linked`** — the occurrence sits in a markdown link target (`](`), an HTML/Astro `href=` or
  `src=` attribute value (with `"`, `'`, `{"` or `{'` delimiters), or an autolink (`<`).
- **`displayed`** — anywhere else: printed for a human to read, and to copy.

And a new offline assertion:

- **L0-4** — per work, per tier: `evidence` occurrences by presentation; and the set of
  **displayed-only** identifiers: normalised URLs that occur in a work's rendered `site` tier and
  are **never** `linked` anywhere in that work. That set is the population `FINDINGS.md` discovered
  by accident — what a reader gets who copies a citation off the page — and it has never been
  counted.

The Layer-1 record then reports its verdicts **split by presentation**, and the two questions are
answered apart for the first time.

---

## 3. What does not change

The layering (L0 assertable, L1/L2 a dated record that expires on production), the identifier
classes U1–U4, the tiers, the controls C1–C5, the stop rule, the second vantage on every `NETFAIL`
and `SERVER-ERROR`, the `NOT-AUTOMATICALLY-CHECKABLE` column, and the standing refusal to compute
any `SENDABLE` label or deliverability score. §6's disclosure binds this run too: **a one-line
summary of a 21-row table functions as a composite even though none is computed.**

---

## 4. The predictions — written before any amended line ran

Each names the number that would refute it. A refuted prediction is reported as refuted, in the
record, in these words.

**P1 — each amendment fixes the defect that named it, and no other.** All five v1 `GONE` leave the
`GONE` bucket, and each leaves it **by the amendment that names it**: the withdrawn DOI → A1; the
arXiv query endpoint and the two `dataset-hub` base paths → A2; the paywalled news article → A3.
**Refuted if** any of the five is still `GONE`, or if any of them is re-classified by an amendment
other than the one that names it.

**P2 — displayed-only citation is the archive's normal case, not its exception.** At least
**one third (≥ 33 %)** of the unique `evidence` identifiers that appear in the rendered `site` tier
are **displayed-only** — never linked anywhere in their own work. **Refuted if under 33 %.**

**P3 — and the distinction is load-bearing, not merely real.** The share of non-`OK` verdicts among
**displayed-only** identifiers differs from the share among **linked** identifiers by at least
**5 percentage points**. **Refuted if the two shares fall within 5 points of each other** — which
would mean A4 records a true distinction that does not change the census's answer, and the record
must say so.

**P4 — the amendments do not manufacture a clean sheet.** After all four, the census still reports a
non-empty `BLOCKED` bucket: identifiers whose health is **not knowable from where this practice
stands**. **Refuted if `BLOCKED` is empty**, which would mean the amendments had quietly converted
an admission of ignorance into a pass.

---

## 5. What this design could still be wrong about

Everything §7 of the v1 pre-registration concedes — one vantage, one moment, one user-agent, and
custody undecidable for almost every citation — stands unchanged and is not softened by any
amendment here. Two limits are added by these amendments themselves:

- **A1 can suppress.** A marker in a paragraph that also carries live evidence in the same block,
  after the marker, will bury that evidence in the correction bucket. The published change-list is
  the only defence, and it is a defence by inspection, not by construction.
- **A4 reads markup, not a browser.** An identifier made clickable by a client script, or by a
  component this extractor does not parse, is recorded as `displayed`. The claim it licenses is
  therefore *"not linked in the committed source"*, not *"not clickable in a browser"*, and the
  record must say the former.
