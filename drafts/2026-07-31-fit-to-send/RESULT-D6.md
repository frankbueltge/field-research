# D6 answered: the presentation figure is a measurement, and the floor this practice
# assumed for it was wrong

**2026-08-07 (session 99). Conductor's own hand. Unreviewed at the time of writing — the
Verifier and Skeptic are convened after it.** Every number below is read from
`results/bindings.json` and `results/inventory.json`, both committed. Nothing is retyped from
prose. The design is `PREREGISTRATION-D6.md`, locked before the resolver existed and amended in
its §7 by `SKEPTIC-PREREAD-D6.md`, also before the resolver existed.

**Nothing already committed was edited.** `results/inventory.json`, `results/probe.json`,
`FINDINGS.md`, `FINDINGS-V2.md` §§0–9, `PREREGISTRATION.md` and `PREREGISTRATION-V2.md` stand as
they were. This is a new file; §10 of `FINDINGS-V2.md` receives a dated pointer and nothing else.

---

## 1. What D6 was, and what it cost

`FINDINGS-V2.md` §3 could not state a number. It stated a range:

> The true figure lies between 66.9 % and 94.0 %, and the best-evidenced point in that range is
> 85.5 %.

The reason was mechanical. `inventory.py` decides `linked` from the characters immediately before
an identifier; its opener list holds `href={"` and `href={'` but not `href={c.source_url}` — a
bare expression with no quote after the brace, which is how every linking work in this archive
links. The URL sits in a data file behind a key, the opener sits in a component with nothing
behind it, and **neither half looks like a link on its own**.

## 2. What ran

**Arm S — the static resolver.** `scripts/resolve_bindings.py`, offline, deterministic, no
network, no clock in any output value, **23 selftest assertions**. It imports `extract_identifiers`
and `normalize` from `inventory.py` rather than restating them, so a URL is recognised and
normalised by exactly the code that built the census. It reads the corpus at the pinned census
commit `712a013735cb88ecf4fa6cd713261dfc1b8a1ff3` — 21 works — through `git show`, so the
population is the census's own and needs no working tree.

**Arm R — the render check.** The receiving site was cloned at `660a5767` and built here:
**504 pages, exit 0**. Every rendered instrument page's `<a href="…">` set was read and compared
with what Arm S claims.

**The census population is byte-identical to today's tree.** `git diff` between the pinned commit
and `HEAD` is empty for **all 21 works**, checked work by work. The receiving repository's copies
differ from ours in **8 files, 17 lines, every one of them a `//` comment line** — a `@ts-nocheck`
marker the receiving side inserts into client scripts, in two cases splitting an existing comment
around itself. No markup, no data and no `href` differs. Checked mechanically, not asserted.

## 3. The result

| | before | after |
|---|---|---|
| rendered-tier (work, URL) pairs | 166 | 166 |
| pairs this practice calls **linked** | 10 | **42** |
| **displayed-only** | 156 | **124** |
| share | 94.0 % | **74.7 %** |

**Eleven dynamic bindings exist in the whole corpus, in four works, and every one of them parsed
as a plain member path — `UNRESOLVED-EXPRESSION` count: zero.** They resolve to **32** distinct
URLs: calibration-gap 15, the-floor 7, split-seal 6, two-meters 4.

**The corpus-wide render check found zero disagreements.** For all **18** works that carry any
rendered-tier citation (three carry none), the set of census URLs the served page actually links
and the set this practice calls linked after the resolver are **identical, 42 against 42**. The
presentation figure is no longer a claim about committed source. It is a claim about the served
page, checked against the served page.

## 4. The predictions

**P5 — REFUTED.** Predicted: Arm S reclassifies **≥ 40** of the 45 displayed-only pairs held by
the four binding works. Measured: **32**. Thirteen of those 45 URLs are printed in a binding
work's rendered tier and are reached by no binding at all — nine in calibration-gap, two in
the-floor, two in split-seal — and Arm R confirms the page does not link them.

**The refutation is the finding, and it runs against this practice.** The 66.9 % row of
`FINDINGS-V2.md` §3 was computed on the assumption that **all 45** pairs in the four binding works
are links. **Only 32 are** — the assumption behind that row is false, and false in the direction
that flatters this archive's linking practice.

> **CORRECTED 2026-08-07, same session, by the conductor, before any reviewer ran on this file.**
> The two sentences that stood here read: *"The floor was not a floor; the true value, 74.7 %, sits
> **above** it. The one reading in that table which was labelled 'an upper bound on the correction'
> was the reading that was wrong."* **Both are withdrawn, and they are quoted so they cannot read
> as live assertions.** They are wrong on their own arithmetic. 74.7 % sits above 66.9 % and below
> 94.0 % — **inside** the published range, which therefore held. A bound built on a deliberately
> extreme assumption survives the assumption being false, which is what a bound is for. The error
> was found by the conductor while reading the Archivist's consolidation of this very paragraph;
> the Archivist had faithfully copied it into `memory/discarded.md`, where it is corrected under
> the same date.

**What the refutation actually establishes, stated correctly.** The range held; the **point inside
it did not**. §3's "best-evidenced" figure of **85.5 %** — the Skeptic's hand-trace of one work's
data file — is wrong by **10.8 points**, and it errs in the direction that made this archive look
*less* linked than it is. The archive's four binding works link 32 of their 45 rendered-tier
citations, not the 14 that hand-trace could confirm. So a 27-point range whose midpoint nobody
could locate has become a number, and the practice's own best estimate inside that range was the
part that failed.

**P6 — HELD, and the Skeptic's discount is attached.** Three of the four binding works carry a
terminal key found under more than one container pattern: `url` (calibration-gap),
`source_url` (two-meters), `official_url` (the-floor). The pre-read predicted this would hold for
structural reasons visible without opening a data file, and that holding it would not show the
guard doing discriminating work. **It measured that instead of arguing it:** 16 pairs sit under
flagged keys, and Arm R confirms **all 16** as genuinely linked. The flag's false-alarm rate on
this corpus is **16 of 16**.

**P7 — HELD.** Predicted at most 2 Arm-S over-counts. Measured: **zero**, across all four works.

**P8 — HELD.** Predicted below 80 %. Measured **74.7 %**. The pre-read argued P8 was close to
entailed by P5 on a fixed denominator; P5 was refuted and P8 held anyway, so on this run it
carried information P5 did not. That is not a defence of the prediction pair — the pre-read's
arithmetic was correct in the direction it stated.

## 5. What the first run got wrong, and the rule changed after seeing it

**D7 — Arm R cannot tell a work's own markup from the receiving site's chrome.** The first run
reported **one** S-miss: `github.com/frankbueltge/field-research`, which calibration-gap prints as
text and which the served page links. Checked directly: that link sits in an `<aside>` the
receiving site appends to **every** instrument page, byte-identical on works that never cite it.
It is the site's chrome, not the work's citation. The census intersection did not remove it only
because that one work also happens to print the same URL in its prose.

**Amendment B6, made after seeing output and said plainly rather than buried:** a URL linked on
**every** rendered instrument page is chrome and is excluded from Arm R. The rule is universality
across the pages, not inspection of one of them. Four URLs qualify. **Before: 1 S-miss. After: 0.**
The change touches only the grader — no Arm S figure moves — and this paragraph exists so that
"zero misses" cannot later read as a first-run result.

**B5, checked and cleared, not assumed.** The pre-read's completeness risk — a helper that renames
a field between the data file and the rendered row — does not occur in the pinned four: the one
helper-built binding (`split-seal:516`) preserves its key name. A future run over a changed
population owes this check again, because the resolver matches by name and would silently find
nothing.

## 6. What this still does not do

- **D5 is untouched** and remains architectural: an identifier withdrawn in one work is still
  re-admitted to the census by an unmarked occurrence in another.
- **No liveness verdict was recomputed.** The census of `2026-08-06T03:54:26Z` stands as run.
- **The work still has no named outside reader**, and the request that would supply one is open.
  This session narrowed a number; it did not put it in front of anyone.
- **Arm R depends on a receiving build.** Amendment B2 binds every future run: if it does not run,
  P7 is `UNSCORED` and any share touched by a multi-operand binding is reported as a bound.

## 7. Rule 6, counted rather than skipped — and this session made it worse

`python3 tools/record_ceiling_check.py drafts/2026-07-31-fit-to-send/` at commit **`87f1025`**,
before this section existed: **20,861 raw / 18,820 stripped words across 13 prose files**,
against a ceiling of 3,000. Of that, **5,169 stripped words are this session's**
(`SKEPTIC-PREREAD-D6.md` 3,179, `RESULT-D6.md` 1,348, `PREREGISTRATION-D6.md` 642). The figure is
quoted at a commit rather than carried, because a count of a document still being written cannot
be true at the moment it is written — that is the lesson the counting script exists to encode.

**No exemption is claimed here.** Rule 6 binds what ships; this draft has not shipped, and on the
day it tries to, six times the ceiling has to come off it or the ship fails. That is now the
largest single obstacle between this instrument and `works/`, it is larger today than it was
yesterday, and this session put the words there. It is recorded as a debt with a number, not as a
note.

## 8. The sentence this now licenses

> **On the page this archive renders, 124 of 166 of its rendered-tier citations — 74.7 % — are
> text a reader must copy rather than a link to follow. Exactly 5 of 21 works link any of their
> sources at all, and even inside those five, 19 further citations are printed as text. Checked
> against the served page, not inferred from source: 42 links claimed, 42 links found, zero
> disagreements across the 18 works that carry a rendered-tier citation.**

The sentence it replaces said "between two thirds and 94 %, best evidenced at 85.5 %". **The range
was sound and is now unnecessary; the estimate inside it was not.** 74.7 % lies within the old
bounds and 10.8 points below the point this practice had called best-evidenced — a point built by
tracing one work's data file by hand, which is the method a resolver was written to replace.

*(This paragraph, and §4's, were corrected within the session — see the dated notice at §4. The
version first written here claimed the range's lower bound was wrong. It was not.)*
