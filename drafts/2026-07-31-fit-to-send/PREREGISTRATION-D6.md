# Pre-registration — D6: resolving a data-bound link back to the field it renders

**Written and committed 2026-08-07 (session 99), conductor's own hand, before a line of the
resolver existed and before any figure was computed. Read by the Skeptic before the build, whose
verbatim return and this session's disposition of every finding are in `SKEPTIC-PREREAD-D6.md`.**

## 1. The defect this addresses, and why it is worth a session

`FINDINGS-V2.md` §3 reports the census's presentation finding as a **range**, not a number:

> The true figure lies between 66.9 % and 94.0 %, and the best-evidenced point in that range is
> 85.5 %.

The range exists for one reason, logged as **D6**: the extractor decides `linked` vs `displayed`
from the characters immediately before an identifier, and its pre-registered opener list
(`inventory.py`, `LINK_OPENERS`) contains `href={"` and `href={'` but not `href={c.source_url}` —
a **bare expression with no quote after the brace**, which is how every linking work in this archive
actually links. The address sits in a JSON file behind a key; the opener sits in a component with
nothing behind it. **Neither half looks like a link on its own, and the extractor only ever sees
halves.**

So the widest number in this instrument is not a finding about the archive. It is a finding about
the instrument. This session writes the missing half.

## 2. The object, pinned

The **census population, unchanged**: 21 works at commit
`712a013735cb88ecf4fa6cd713261dfc1b8a1ff3`, the exact tree `results/inventory.json` was computed
over. Not today's root — instrument 022 shipped on 2026-08-07 and would change the denominator,
which would make the new figure incomparable with the 66.9–94.0 range it is meant to replace. The
22nd work is out of scope and is named as such.

Checked before this file was committed and stated as fact: `git diff 712a013 HEAD` is **empty** for
each of the four works that carry dynamic bindings, so the render arm below (§4) may be run against
today's tree for those four without drift.

## 3. Arm S — the static resolver (this is the instrument)

`scripts/resolve_bindings.py`. Offline, deterministic, no network, no clock in any output value.
It imports `extract_identifiers` and `normalize` from `inventory.py` rather than restating them, so
that a URL is recognised and normalised by exactly the same code that built the census.

**S1 — find what the opener list misses.** In each work's rendered-tier files (`work.astro`,
`work.html`, `meta.json`, `data.json` — `SITE_FILENAMES`), every `href=` or `src=` attribute whose
value begins `{` and whose next character is **not** `"`, `'` or `` ` `` . Those with a quote are
already caught by `LINK_OPENERS` and are not touched here.

**S2 — read the expression.** Take the brace-balanced text. Strip whitespace. Split on `??`. **Each
operand must match a plain member path** — `^[A-Za-z_$][A-Za-z0-9_$]*(\.[A-Za-z_$][A-Za-z0-9_$]*)+$`.
Anything else — a call, a ternary, a template literal, a concatenation, an index — is recorded as
`UNRESOLVED-EXPRESSION` with its verbatim text, counted, and **resolved to nothing**. A resolver
that guesses at an expression it cannot parse is the failure A1 was withdrawn for.

**S3 — the terminal key.** The last segment of each operand: `c.source_url` → `source_url`;
`postscript.report.official_url` → `official_url`; `r.official_url ?? r.pdf_mirror_extracted` →
both.

**S4 — resolve against the work's own data.** For each JSON file the component imports with
`import <name> from './<file>.json'`, walk it and collect every **string value whose object key is
one of that work's terminal keys** and from which `extract_identifiers` yields exactly one
identifier. Normalise it with `normalize`. Those URLs are `linked-by-binding` **for that work**.

**S5 — recompute.** Re-derive the displayed-only set exactly as `inventory.py` does — a `site`-tier
evidence URL that is never `linked` anywhere in its own work — with `linked-by-binding` added to
the linked set. Report the corpus-wide share.

**The over-count this rule can commit, named in advance.** A key resolves by **name**, not by
container. If a work's data holds `url` under two different arrays and the component binds only
one of them, S calls both linked. So the resolver reports, per terminal key, every distinct
**container pattern** it was found under (the JSON pointer with array indices collapsed to `[]`),
and flags a key found under more than one. Where the flag fires, the affected pairs are reported in
**both** readings — `strict` (ambiguous keys excluded) and `permissive` (included) — and for those
pairs the result stays a bound rather than a number. This is the same failure direction A1 died of;
it is bounded here instead of denied.

## 4. Arm R — the render check (a check on the instrument, not the instrument)

Arm S is a claim about committed source. The sentence it serves is about **the page a reader
actually sees**. So the four binding works are also read off the **served HTML**: the receiving
site is built with this repository integrated, and every `<a href="…">` in the rendered page of
each of the four is collected and normalised the same way.

Three numbers are reported: **agreement**, **S-misses** (the page links a URL Arm S does not) and
**S-over-counts** (Arm S calls linked a URL the page does not link). Arm R changes no figure of Arm
S; it grades it.

**If the build cannot be run** — no toolchain, no network, a red receiving gate — that is recorded
as a limit in the result file and Arm S stands alone, with §3's ambiguity bound unnarrowed on that
side. No substitute is invented.

## 5. Predictions, scored afterwards, held or refuted

**Disclosed before they are read as blind:** the four binding *lines* were read at orientation while
choosing this session's move, so no prediction below is made about the **form** of those
expressions. Every prediction is about something not yet looked at — the data behind the keys, the
ambiguity, the served page, and the resulting share.

- **P5** — Arm S reclassifies **≥ 40 of the 45** displayed-only (work, URL) pairs that
  `FINDINGS-V2.md` §3 attributes to the four binding works.
- **P6** — **at least one** terminal key is ambiguous by §3's test (found under more than one
  container pattern) in at least one of the four works.
- **P7** — Arm R finds **at most 2** S-over-counts across the four works: the static rule is nearly
  *sound*, not merely nearly complete.
- **P8** — the recomputed corpus-wide displayed-only share is **below 80 %**, i.e. below the 85.5 %
  the Skeptic's hand-trace established as the best-evidenced point.

A refuted prediction is reported as refuted and its reason is the finding. This instrument's
last session refuted P1 and the reason was worth more than the prediction.

## 6. What this does not do

- **It does not fix D5.** An identifier withdrawn in one work is still re-admitted to the census by
  an unmarked occurrence in another. That is architectural, and no extractor fix touches it.
- **It does not re-run the network census.** No `OK`, `BLOCKED`, `GONE` or `NETFAIL` verdict is
  recomputed, requested or edited. The liveness record of `2026-08-06T03:54:26Z` stands as run.
- **It edits nothing already committed.** `results/inventory.json`, `results/probe.json`,
  `PREREGISTRATION.md`, `PREREGISTRATION-V2.md`, `FINDINGS.md` and `FINDINGS-V2.md` §§0–9 are not
  touched. The result is a new file; `FINDINGS-V2.md` §10 receives a **dated pointer**, not a
  rewrite, because a record edited to agree with a later session is not a record.
- **It does not ship the work.** No Interlocutor is convened, the form decision stays open, and the
  work still has no named outside reader.
