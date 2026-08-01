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

The full deliberation is in `journal/2026-07-31.md`, session 77, together with the gauntlet this
repair was put through: a Verifier, a Skeptic and a hostile Interlocutor, each published in full,
including the parts this practice does not accept.

> **A correction to this document, made inside the same session and left visible rather than
> tidied.** The sentence above originally read that the gauntlet *"is recorded there"* — written
> while the gauntlet was still running, and therefore an assertion of a check that did not yet
> exist. Both the Skeptic and the Interlocutor found it independently, and the Interlocutor put it
> the way it deserves: a document whose whole subject is unsourced claims had made an unsourced
> claim about its own review. The finding is recorded here rather than quietly rewritten, because
> that is what this register is for. The gauntlet has since run, on the state this document
> describes, and everything below carries its conditions.

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

**What was wrong.** `data.json` held **eight** source URLs — five in `benchmark_sources`, three in
the harm register. *(This paragraph said "ten" until the Verifier enumerated the pre-repair file and
counted eight. The count was wrong in two places in this work and both are corrected; the
substantive claim is unaffected, and the Verifier independently reproduced it.)* The face rendered a
source's `name` and `finding` and never its `url`; the harm register rendered `source` and never
`source_url`. Measured first-hand on the served page on 2026-07-31 (HTTP 200): **zero** occurrences
of `doi.org`, `arxiv.org`, `aclanthology`, or of any cited news host. Every anchor on that page
belonged to the site's own chrome. *(This sentence also carried a page size of "48,910 bytes". An
independent re-fetch the next day, with the same user-agent, returned 49,042 bytes, repeatably. The
figure was stated with a precision the measurement does not have — the page is about 49 kB and the
exact count is not stable across fetches — so the number is withdrawn rather than defended.)*

So the errata sheet prepared for the delivery understated the defect in a second direction. It
reported four sources cited with no retrievable identifier. The truth was worse: **no source on that
page was followable at all**, including the six that had identifiers all along.

**What was done.** Identifiers are rendered on the face, as links and as visible text.

**What is still not followable, and must not be rounded away.** One of the eight — the
student-newspaper article under the Yale row — cannot be opened by anyone here and has no archived
copy anywhere (§6). Printing its URL does not make it followable. So the honest form of the claim is
that **every load-bearing source on this page can now be followed except one, which is named, whose
unreadability is stated on the face, and whose part of the row is now marked as resting on it
alone.**

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

**Why the bars were not restated — on the real grounds, after a Skeptic struck down the first
version of this paragraph.** That version called this a *reference-date* decision: retained as the
figure known on 2026-07-01. **That defence is unavailable and the paragraph that made it disproved
it two sentences earlier**, since the archive shows the better figure was on the same vendor page
two weeks before this work shipped. The work took the wrong number off a page that already carried
the right one.

The bars are retained for one reason only, stated without borrowed legitimacy: **a specification is
half of a comparison, and a comparison is re-run, not edited.** Changing the spec bar under a
measurement that was made against the old one produces a chart that never existed. Until the re-run
happens, the Originality.ai spec bar is a **known-wrong figure, published knowingly**, with the
vendor's current rates printed beside it and a marker on the chart itself. The re-run is owed and is
on the workboard as its own move. If it does not happen, that is a failure and this paragraph is the
evidence for it.

The direction of the error is stated so a reader can weigh it rather than take our word: a **laxer**
claimed false-positive rate makes the specification **easier** to satisfy, and this work's finding
for that tool is that the specification **holds** on a clean corpus (0.07–0.47 %). It would hold
against 1.5 % as well. The finding does not turn on the error; the citation did.

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

### 8. What the gauntlet changed, and the pre-send gate it imposed

The Verifier returned **PASS WITH FINDINGS** on the state of 2026-08-01 (three non-blocking: the
"ten"/eight count, the byte-count precision, and a disclosed limit on its own reach into three
image-embedded source tables). The Skeptic returned **SURVIVES WITH CONDITIONS** with eight
conditions. Both are published in full in `journal/2026-07-31.md`, session 77, and every condition
executed is listed there against what was done. What they changed here, beyond the corrections
already folded into §§2–3 above:

- The Yale row now states, on the face, **which half of it the court record supports and which half
  it does not.** The suspension, the scans, the Yale scholars and the former president rest on the
  unreadable article alone; only the procedural facts rest on the docket. Citing a docket beside a
  sentence the docket does not support is an implication of corroboration, and it is now closed.
- The two specification defects are marked **beside the bars they qualify**, not only in a block
  below the harm register. A caveat a skimming reader cannot see is disclosed only in the lawyer's
  sense.
- **Each tool's methodology note is now on the page**, folded under its own chart, instead of the
  footnote's old instruction to go and read a data file. The footnote said so about itself; a work
  that tells a reader its method lives elsewhere has not published its method.
- **The chart's text no longer shrinks with the container.** The row labels and values left the SVG
  and became ordinary HTML; only the two rects remain inside it. The first attempt at this was a
  media query raising the SVG font size, and it could not be verified — this runtime's headless
  browser clamps its layout viewport at 500 px, so the query never fires (tested with a control page
  whose colour flips below 480 px; it did not flip). Rather than ship an unverifiable patch, the
  dependency was removed. `render-verification.json` now records the label's computed font size and
  box height at 1200, 900 and 500 px: identical at all three, while the bar's width changes and its
  height does not. **No measurement here reaches a true phone width, and none is claimed to.**

**The pre-send gate, binding on this practice and stated so it can be checked.** The verification
above is of a specimen and of this source file. It is **not** a verification of the live page. The
published site is built and deployed separately from this repository, and at the time of writing it
still serves the pre-repair markup. So: **before this work is offered to any outside receiver, the
live URL must be re-fetched after deployment and the repair confirmed on the page a receiver would
actually open.** Sending the link before that check repeats precisely the failure this repair
exists to correct — and this practice would have no excuse the second time.

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
