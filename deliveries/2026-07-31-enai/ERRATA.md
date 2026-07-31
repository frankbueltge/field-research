# Known defects and corrections — instrument 001, as of 2026-07-31

*Assembled by the conductor of Meridian at session 75, 2026-07-31, while preparing this delivery.
Every check below was run first-hand today. Nothing here has been silently patched into the work:
this practice's constitution requires that a correction be a new, dated event that stays visible
beside what it corrects (`PROTOCOL.md`, "Legal hygiene", item 6), and editing a shipped work would
also invalidate the review verdict it shipped under. So the work goes as it stands and this sheet
travels with it.*

**Who found these.** All of them were found by this practice, checking its own piece before sending
it — not by a reader, and not by the receiver. Four of the six had been standing on a published page
since 2026-07-01.

---

## 1. Four load-bearing sources are cited with no retrievable identifier

This is the largest defect and the reason this sheet exists. Instrument 001 displays a `MEASUREMENT
SOURCES` block listing five studies with links. But four further externally-authored sources carry
figures that appear **on the chart itself or in the work's rendered correction notes**, and none of
the four is given a URL, DOI or arXiv identifier anywhere in the work.

A reader cannot follow them. The link census this practice ran the same morning
(`drafts/2026-07-31-fit-to-send/`) could not see them either: it inventories identifiers that exist
and checks whether they resolve. A claim cited with **no** identifier is invisible to it. That is a
gap in the instrument, recorded here as a finding against ourselves.

The four, with the identifiers supplied — each verified first-hand today, with what was found:

| Cited in the work as | What it is | Identifier | Verified today |
|---|---|---|---|
| "Ibrahim et al., Scientific Reports 2023" — the source of GPTZero's **18 %** measured bar | Ibrahim H. et al., *Perception, performance, and detectability of conversational artificial intelligence across 32 university courses*, **Scientific Reports** 13, 12187 (2023-08-24) | `doi:10.1038/s41598-023-38964-3` | **Holds, verbatim.** The paper reads: *"GPTZero has a higher false positive rate (18%), but a lower false-negative rate (32%)"*, and the paraphrase attack raises that false-negative rate *"from 32% to 95%"* — all three figures as the work states them. An author correction exists (`doi:10.1038/s41598-023-43998-8`, 2023-10-10); it corrects one author's affiliation and touches no figure. |
| "Perkins et al. 2024 (46.1 %, baseline, non-adversarial)" | Perkins M. et al., *Simple techniques to bypass GenAI text detectors: implications for inclusive education*, **International Journal of Educational Technology in Higher Education** (2024-09-09) | `doi:10.1186/s41239-024-00487-w` | **Holds.** Table 7 ("Baseline testing") gives ZeroGPT a mean of **46.1 %** across the paper's three accuracy computations (binary 40, semi-binary 46, logarithmic 52.3). The work's word "baseline" is the table's own. |
| "Weber-Wulff et al. Dec 2023 (59 %)" | Weber-Wulff D., Anohina-Naumeca A., Bjelobaba S., Foltýnek T., Guerrero-Dib J., Popoola O., Šigut P., Waddington L., *Testing of detection tools for AI-generated text*, **International Journal for Educational Integrity** 19:26 (2023-12-25), CC BY 4.0 | `doi:10.1007/s40979-023-00146-z` · `arXiv:2306.15666` | **Holds — and is under-specified.** See §2. |
| "Turnitin's own admission" / "Turnitin's own blog" — the source of the **4 %** bar and of the quoted sentence about false positives below a 20 % detected-AI share | The vendor's own published pages, both by its Chief Product Officer | `https://www.turnitin.com/blog/understanding-the-false-positive-rate-for-sentences-of-our-ai-writing-detection-capability` (14 June 2023) and `https://www.turnitin.com/blog/ai-writing-detection-update-from-turnitins-chief-product-officer` | **Both read first-hand today (HTTP 200), and both hold verbatim.** The first: *"Our document false positive rate — incorrectly identifying fully human-written text as AI-generated within a document — is less than 1% for documents with 20% or more AI writing. Our sentence-level false positive rate is around 4%."* The second: *"we've determined that in cases where we detect less than 20% of AI writing in a document, there is a higher incidence of false positives."* These are **vendor claims about a vendor's own product**, not independent measurements, and the work's chart treats them as the specification side of the comparison. |

## 2. The "59 %" is one of three numbers the same paper reports for the same tool

Instrument 001 cites *"Weber-Wulff et al. Dec 2023 (59 %)"* for ZeroGPT's detection accuracy, without
naming which of that paper's three accuracy computations it comes from. Read first-hand today, the
paper reports for ZeroGPT:

- **59 %** — Table 7, the **binary** approach (partially-correct classifications count as wrong);
- **74 %** — Table 8, the **binary inclusive** approach;
- **67 %** — Table 9, the **semi-binary** approach (partially-correct classifications score 0.5).

The work quotes the strictest of the three and names neither the table nor the approach. The figure is
not wrong; the citation is incomplete in a way that matters, because choosing among three published
computations without saying so lets a single number look more settled than the paper makes it. The
same pattern recurs in Perkins et al., where ZeroGPT is 46.1 % in Table 7 (baseline) and 31.3 % in
Table 8 (non-manipulated output, averaged differently) — the work cites the first and does not mention
the second.

**Correction, dated 2026-07-31:** the figure should read *"59 % (binary approach, Table 7; the same
paper also reports 74 % and 67 % for the same tool under its two other accuracy computations)"*.

## 3. A wrong table number, on the receiver's adjacent subject

`works/2026-07-01-calibration-gap/data.json` attributes the GPTZero over-detection figures — **25.00 %**
of non-native-authored AI-assisted abstracts labelled 100 % AI, against **11.11 %** for native authors —
to *"Table 4"* of Pratama (2025). Read first-hand today at the open-access full text, they are in
**Table 6** ("Overall performance metrics from Scenario 2: AI-assisted abstracts"). Table 4 is Scenario 1
and carries the other Pratama figures the work uses (ZeroGPT accuracy 64.35 %, false-positive rate
16.67 %; DetectGPT 54.63 %).

The figures themselves are correct, and so is the work's description of what they mean: the paper defines
its Over-Detection Rate as *"The percentage of AI-assisted abstracts labeled as 100 % AI by the tool,
incorrectly attributing the entire text to AI and disregarding human contribution."* Only the table
number is wrong.

**Correction, dated 2026-07-31:** Table 4 → **Table 6** for the 25.00 % / 11.11 % pair.

*Source detail worth having:* Pratama A. R., *The accuracy-bias trade-offs in AI text detection tools and
their impact on fairness in scholarly publication*, **PeerJ Computer Science** 11:e2953 (2025-06-23),
CC BY 4.0, `doi:10.7717/peerj-cs.2953`. The DOI route was **not readable** from this practice's runtime
today — it returns HTTP 403 behind an interstitial challenge. The full text is readable at the Europe PMC
mirror, `https://europepmc.org/articles/PMC12453642`, and that is where it was read. An open-access paper
whose canonical identifier is unreadable to an automated check while an open mirror serves it is worth
noting in its own right.

## 4. A precision slip: 22.2 % should be 22.14 %

The work states that under adversarial editing mean accuracy across the detectors Perkins et al. tested
falls *"from 39.5 % to 22.2 %"*. The paper's own conclusion gives **22.14 %**, and its Table 9 gives
22.1. The 39.5 % and the 17.4-point drop are exactly as the paper states them; only the endpoint is
rounded wrongly. Small, and corrected here rather than left for a reader to catch.

## 5. One cited source could not be opened, and this sheet does not pretend otherwise

One row of the harm register cites a student-newspaper article. That URL returns **HTTP 429** to this
practice's runtime — a rate-limit or bot wall — and it was **not opened, not read, and not verified
today.** It is not shown to be dead; it is unreadable from here, which is a different thing and is
recorded as such.

What was verified today, by a different route, is the underlying case: the docket exists and is live —
*Rignol v. Yale University*, United States District Court for the District of Connecticut, docket
**3:25-cv-00159**, filed 2025-02-03, assigned to Judge Vernon D. Oliver, with an amended complaint
entered 2026-06-12. That is independent corroboration of the case, **not** verification of the cited
article, and the two are not interchangeable. The docket's own human-readable page also refused an
anonymous request (HTTP 403); the facts above come from the public court-data API.

**Consequence for the work:** the row's procedural description ("Federal lawsuit pending … Injunction
denied May 2025") is incomplete as of today — the case has moved since. This sheet does not restate the
case; it records that the row is dated and that a reader checking it in 2026 will find a later state.

## 6. What was checked and holds

Stated because a defect list without it would be misleading. Verified first-hand today, unchanged:

- GPTZero's **18 %** false-positive rate and **32 % → 95 %** false-negative rate under paraphrase (Ibrahim et al.).
- ZeroGPT's **16.67 %** false-positive rate and **64.35 %** accuracy; DetectGPT's **54.63 %**, and the paper's own verdict on it, verbatim: *"This makes it virtually no better than random guessing."* (Pratama 2025, Table 4 and text.)
- The GPTZero over-detection pair **25.00 % / 11.11 %** and the definition behind it (Pratama 2025, Table 6).
- ZeroGPT's **46.1 %** baseline accuracy and the **39.5 %** / **17.4-point** adversarial figures (Perkins et al., Tables 7–9 and the conclusion).
- ZeroGPT's **59 %** (Weber-Wulff et al., Table 7, binary approach).
- The Turnitin document-level **<1 %** claim, its below-20 % qualification, and the sentence-level **~4 %** figure, on the vendor's own pages.

The remaining sources on the work's face — the five in its `MEASUREMENT SOURCES` block and the two other
harm-register sources — were checked for resolution, not re-read, in the census of 2026-07-31
(`drafts/2026-07-31-fit-to-send/`): of instrument 001's ten linked identifiers, eight answered, none was
found dead, and two were walled (the Pratama DOI at §3 and the newspaper article at §5). That census
measures whether a link answers. It does not establish that a page still says what the work says it says.
