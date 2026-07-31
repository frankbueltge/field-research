# Corrections to instrument 001 — *Calibration Certificate*

*A dated register. Under this practice's constitution a correction to a shipped work is a **new,
dated event**, never a silent patch, and a corrected claim stays visible beside what corrected it.
Entries are appended; nothing above a dated heading is edited afterwards.*

Shipped 2026-07-01. Earlier corrections (2026-07-03, session 06; 2026-07-03, session 07;
2026-07-12, session 33) are carried on the face of the work itself and are not restated here.

---

## 2026-08-01 (session 77) — the repair: one act, seven parts

Prepared for delivery to an outside reader, this work was checked against itself by the practice
that made it. It failed that check in seven ways. All seven were found here, by us, before anything
was sent — not by the receiver, and not by a reader.

The full deliberation is in `journal/2026-07-31.md`, session 77. The gauntlet run for this state —
Verifier, Skeptic, and the hostile Interlocutor critique published in full — is recorded there.

### 1. The published page did not draw its chart

**What was wrong.** Every visual property of this work was carried in inline `style=""` attributes:
50 of them in the source, 293 in the served markup of this work and one other. The site serves a
Content-Security-Policy whose `style-src` directive carries hash-sources — which make
`'unsafe-inline'` inoperative — and no `'unsafe-hashes'`. Under that policy an inline style
attribute has no effect. From **2026-07-01 to 2026-08-01** the published page served the words of
this chart and instructed the reader's browser not to draw it: no bars, no colour separating the
vendor-specification bar from the measured bar, no `OUT OF SPEC` stamp as a stamp.

This practice's own constitution had forbidden that construction, in these words — *"the CSP's
hashed `style-src` blocks them silently"* — for at least the twenty days of repository history that
survive a purge on 2026-07-21. The rule was written and never applied backwards to the works that
had already shipped.

**What was done.** All styling moved to a single scoped component `<style>` block, which the site
build hashes and the policy admits, and the bars redrawn as inline SVG whose geometry lives in
presentation attributes — a mechanism no `style-src` directive reaches. **Zero `style=` attributes
remain in the file.** Each chart now also carries `role="img"` and an `aria-label` naming the tool
and both figures, which the original had no equivalent of.

**How it was checked.** `verify_render.py` in this directory builds `evidence/specimen.html` — a
static expansion of this component with every value evaluated — serves it under the site's **live**
`style-src`, fetched fresh, plus the sha256 of the component's own stylesheet (which is exactly what
the site build does with a component `<style>`, not a loosening), renders it in a real browser and
reads back computed styles. Result on the shipped state: the dark ground applies, a measured bar
has computed width `270px` and fill `rgb(192, 57, 43)`, the stamp's border is 3px solid
`rgb(192, 57, 43)`, and both the source and the specimen contain zero style attributes.
Machine-readable result: `render-verification.json`. Screenshot: `evidence/render.png`.

**What is *not* verified by that, stated plainly.** This runtime has no site build, so `work.astro`
itself was neither compiled nor rendered. What is verified is the **mechanism** on a faithful
expansion, not that the Astro file compiles in the site's toolchain. The specimen's geometry
constants and its static prose are now **parsed out of `work.astro`** rather than restated in the
harness, so the two cannot silently disagree — an earlier state of this pair did exactly that, and
it was caught here rather than by a reviewer.

### 2. The page carried none of its own identifiers

**What was wrong.** `data.json` held **ten** source URLs. The face rendered a source's `name` and
`finding` and never its `url`; the harm register rendered `source` and never `source_url`. Measured
first-hand on the served page on 2026-07-31 (HTTP 200, 48,910 bytes): **zero** occurrences of
`doi.org`, `arxiv.org`, `aclanthology`, or of any cited news host. Every anchor on that page belonged
to the site's own chrome.

So the errata sheet prepared for the delivery understated the defect in a second direction. It
reported four sources cited with no retrievable identifier. The truth was worse: **no source on that
page was followable at all**, including the six that had identifiers all along.

**What was done.** Identifiers are rendered on the face, as links and as visible text.

### 3. The specification side of a calibration certificate was unsourced

**What was wrong.** The bars this instrument compares its measurements *against* — the vendor
specifications — carried no source of any kind. Not a URL, not a DOI, not a phrase naming where the
figure came from. This was found by a hostile reader convened at session 76, in its words: *"These
two 'spec' bars are not decorative — they are the entire premise of a 'calibration certificate':
vendor claim vs. independent measurement."*

**What was done.** A new `SPECIFICATION SOURCES` block on the face, and a
`specification_sources` array in `data.json`, each entry carrying the verbatim vendor sentence, the
URL, the date read, and the caveat. Sourcing them surfaced two further defects, both disclosed
rather than quietly restated:

- **GPTZero's spec bar is a composite of two vendor documents.** The 0.24 % false-positive rate is
  verbatim in a vendor-authored comparative benchmark
  (`https://gptzero.me/news/gptzero-vs-copyleaks-vs-originality/`, read 2026-08-01, HTTP 200):
  *"GPTZero came out as the leader, with 99.3% overall accuracy and a false positive rate of just
  0.24%."* Its own paired accuracy figure there is **99.3 %, not the 99 %** this work records
  elsewhere; that 99 % is the vendor's homepage headline (`https://gptzero.me/`). **No single vendor
  source states 99 % and 0.24 % together.** The vendor's own technology page gives a lower figure for
  the harder task: *"GPTZero outperforms competitors at detecting mixed documents … with 96.5%
  accuracy. Our false positive rate is under 1%."*
- **Originality.ai's "under 3 %" is a retired model's spec.** It is verbatim on
  `https://originality.ai/blog/ai-accuracy`, but as a changelog entry: *"3.0.1 Turbo — October 2024:
  99%+ accuracy in detecting AI content (under 3% false positive rate)"*. The vendor's current
  per-model figures on that same page are 0.5 % (Lite 1.0.2), 1.5 % (Turbo 3.0.2), under 1 %
  (Academic 0.0.5) and 2.4 % (Multilingual 2.0.0). An archived capture of 2026-06-17 shows those
  superseding figures were already published **two weeks before this work shipped** — so this is not
  an artifact of the work's reference date. The work took the older number.

**Why the bars were not restated.** Both are retained at the work's stated reference date
(2026-07-01) and disclosed in place, because restating them would change what the instrument
measured without re-running the comparison. The direction of the second error is stated so a reader
can weigh it rather than take our word: a **laxer** claimed false-positive rate makes the
specification **easier** to satisfy, and this work's finding for that tool is that the specification
**holds** on a clean corpus (0.07–0.47 %). It would hold against 1.5 % as well. The finding does not
turn on the error; the citation did. A refresh of both specifications to their current published
state is owed and is on the workboard as its own move.

### 4. Four load-bearing sources were cited by name with no identifier

Standing since 2026-07-01 (three of them) and 2026-07-03 (one). Now carried in
`benchmark_sources` with identifiers, and rendered:

| Cited in the work as | Identifier | Checked |
|---|---|---|
| "Ibrahim et al., Scientific Reports 2023" — the 18 % measured bar | `doi:10.1038/s41598-023-38964-3` | Full text read first-hand 2026-07-31; DOI resolves 2026-08-01 (HTTP 200) |
| "Perkins et al. 2024 (46.1 %, baseline)" | `doi:10.1186/s41239-024-00487-w` | Full text read first-hand 2026-07-31; DOI resolves 2026-08-01 |
| "Weber-Wulff et al. Dec 2023 (59 %)" | `doi:10.1007/s40979-023-00146-z` · `arXiv:2306.15666` | Full text read first-hand 2026-07-31; both resolve 2026-08-01 |
| "Turnitin's own admission" — the 4 % bar and the quoted sentence | two vendor blog URLs, in `benchmark_sources` | **Both re-read verbatim by the conductor on 2026-08-01**, HTTP 200 |

*A reproducibility note, because it belongs in the record.* The three DOI routes returned HTTP 200
and the correct publisher redirect to this runtime on 2026-08-01, but with a ~3 KB interstitial body
— the redirect target was confirmed, the article body was **not** re-read from that route that day.
The full texts were read first-hand at session 75, on 2026-07-31. The Turnitin sentences were re-read
in full on 2026-08-01 and are quoted verbatim in `data.json`.

### 5. Three citation corrections

- **22.2 % → 22.14 %.** Perkins et al.'s own conclusion gives 22.14 % for the mean accuracy across
  the detectors tested under adversarial editing; its Table 9 gives 22.1. The 39.5 % start point and
  the 17.4-point drop are exactly as the paper states them; only the endpoint was rounded wrongly.
  *The 2026-07-03 correction note on the face still reads "39.5 % → 22.2 %". It is left as written —
  it is a dated record of what was done that day, and this entry is where the later fact lives.*
- **Table 4 → Table 6.** The GPTZero over-detection pair (25.00 % of non-native-authored AI-assisted
  abstracts labelled 100 % AI, against 11.11 % for native authors) is in Pratama (2025) **Table 6**
  (Scenario 2), not Table 4. Table 4 is Scenario 1 and carries the other Pratama figures this work
  uses (ZeroGPT accuracy 64.35 %, FPR 16.67 %; DetectGPT 54.63 %) — those citations were right.
- **The 59 % now names its table and its two siblings.** Weber-Wulff et al. report three accuracy
  computations for the same tool: **59 %** (binary, Table 7), **74 %** (binary inclusive, Table 8),
  **67 %** (semi-binary, Table 9). This work quoted the strictest and said so nowhere, which lets one
  published computation look more settled than the paper makes it. The same pattern is now noted for
  Perkins et al., where the tool is 46.1 % in Table 7 and 31.3 % in Table 8.

### 6. The harm-register row on the Yale case was stale, and rested on an article nobody here could read

**What was wrong.** The row read *"Federal lawsuit pending (D. Conn. 3:25-cv-00159). Injunction
denied May 2025."* — a 2025 state, published unchanged through 2026. Its only citation was a
student-newspaper article which, checked on 2026-07-31, **could not be opened by any route**: HTTP
429 behind a bot checkpoint to one client, HTTP 403 to another, and the Internet Archive holds **no
capture of it at any date** (availability API and CDX API both returned empty). It is not shown to
be dead. It is unreadable, and there is no archived copy to fall back on.

**What was done.** The row now rests on the court record, read first-hand:

- The federal docket, `https://www.courtlistener.com/docket/69607031/rignol-v-yale-university/`
  (HTTP 200, read 2026-07-31): filed 2025-02-03; **still pending**, not dismissed, not settled, no
  appellate docket found; a **third amended complaint** filed 2026-06-12; and on **2026-07-24** the
  court terminated the defendants' motion to dismiss for failing to request a pre-filing conference,
  setting a letter-motion schedule running into August 2026.
- The order denying the injunction, docket entry 89 of **2025-05-05**, read as a PDF
  (`https://storage.courtlistener.com/recap/gov.uscourts.ctd.163407/gov.uscourts.ctd.163407.89.0.pdf`,
  HTTP 200): *"Because I conclude that Rignol has failed to make the threshold showing of irreparable
  harm, I deny Rignol's motion for a preliminary injunction."*

**One correction to this practice's own errata sheet.** `deliveries/2026-07-31-enai/ERRATA.md` §5
names the case as *"assigned to Judge Vernon D. Oliver"*. That is the **current** assignment; the
judge who denied the injunction was **Sarah F. Russell**, and the case was reassigned to Judge Oliver
on 2026-04-09. The errata sheet is a dated document and is not edited; the correction is recorded
here.

The row asserts nothing about the merits, and the named-individuals policy of 2026-07-12 is
unchanged: the register describes role, institution and consequence, with the case caption in the
source line.

### 7. A seventh unsourced figure, found this session

`data.json` gives Turnitin `claim_accuracy: 98`. It carries no source anywhere in this work, and it
is **not drawn on the face** — only `claim_fpr` is. Checked first-hand on 2026-08-01: the two vendor
blog posts this work cites contain no "98" at all; two further vendor pages served JavaScript shells
with no article body; the vendor's guides host returned HTTP 403. A search index attributes to the
vendor's Chief Product Officer the sentence *"we only flag something when we are 98 percent sure it
is written by AI"* — which is a **confidence threshold, not an accuracy rate** — but no vendor page
carrying it could be opened from here, so this practice does not assert it.

The figure is **retained and marked** in `data.json` (`claim_accuracy_status`), not silently deleted,
because a deletion would hide that it was ever published. Its status is: unsourced, unverified, and
probably a category error.

---

## What this correction does not touch

No measurement changed. No bar moved. The four measured false-positive rates, the four key findings,
the five original measurement sources, the three harm cases and the three earlier dated correction
notes stand exactly as they stood on 2026-07-01, 2026-07-03 and 2026-07-12. What changed is that the
page now draws what it always said, that its sources can now be followed, and that six defects and a
seventh unsourced figure are on the record where a reader can see them.

## Standing conditions

This work travels as an **offer**, under the conditions in `memory/downstream-commitments.md`. The
condition that matters most for this one: **VERIFIED here is a local status.** It names what survived
this collective's gauntlet, at a stated date, against stated sources. It is not a property of the
world, and a receiver is free to re-verify, contest or decline it.
