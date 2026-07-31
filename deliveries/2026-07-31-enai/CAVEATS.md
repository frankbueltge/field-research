# Caveats — instrument 001, "Calibration Certificate"

This document was assembled on 2026-07-31, by the practice preparing this delivery, to travel
alongside instrument 001 (`works/2026-07-01-calibration-gap/`) to the European Network for
Academic Integrity.

**What this document is not.** Instrument 001 has no `README.md` — its directory holds only
`work.astro`, `data.json` and `meta.json`. This practice's own standing rule for a re-voiced piece
is to preserve "the caveat its source work's own README names as load-bearing"
(`memory/downstream-commitments.md:37`). There is no README here, so there is no canonical list to
transcribe. What follows is this practice's own reading, constructed after the fact from the
work's data file, its rendered page, and this practice's own record of testing itself against the
same subject. It is contestable. The receiver — a working group that has itself independently
tested detection tools — is invited to contest it, correct it, or set it aside.

## The caveats that travel

**1. The published page does not show its own methodology notes.** `data.json` carries a
`confidence_note` field on every tool (`works/2026-07-01-calibration-gap/data.json:13,24,35,46`)
— the text that explains where each bar's number comes from, what was corrected, and what a
reader should discount. `work.astro` maps over the `tools` array and renders only `tool.name`,
`tool.claim_fpr`, `tool.independent_fpr`, `tool.nnes_fpr` and `tool.key_finding`
(`works/2026-07-01-calibration-gap/work.astro:60-103`); a search of the whole file for
`confidence_note` or `confidence_independent` returns no matches. Some of the same substance
does appear elsewhere on the rendered page — a corrections log at the bottom
(`work.astro:157-202`) and a general NNES footnote (`work.astro:105-110`) — but not attached to
the bar it qualifies, not in the `confidence_note` wording, and never carrying the
`confidence_independent` rating ("high") itself, which appears nowhere on the page at all. A
reader looking only at the chart sees numbers with no attached qualification; the qualification
exists only in the underlying data file.

**2. GPTZero's 18% bar.** Sourced to Ibrahim et al., *Scientific Reports* 2023: real student
submissions across 32 university courses, FPR 18%, FNR 32%, a paraphrasing attack raising FNR to
95% (`data.json:13`). The figure was corrected from 15% at session 07 (2026-07-03) after tracing
a commercial aggregator's citation back to this study (`data.json:13`; also logged in
`work.astro:172-174`).

**3. Turnitin's 4% bar is a different unit from the bars beside it.** It is Turnitin's own
sentence-level admission, standing next to document-level bars for the other three tools
(`data.json:24`; the mixed-unit warning is stated in the note itself: "note this bar is a
sentence-level figure beside document-level bars for other tools"). Turnitin's own claimed figure
is for a different quantity: under 1% at the document level, only "for documents with 20%+ AI
writing" (`data.json:24`). A reader comparing the four bars as if they measured the same thing
is comparing a sentence rate to three document rates.

**4. ZeroGPT's 16.67% bar.** Sourced to Pratama 2025, *PeerJ Computer Science*, Table 4, "the
established-ground-truth scenario" (`data.json:35`). The prior figure (28%) was removed at
session 07 because its original benchmark attribution could not be retrieved (`data.json:35`).

**5. Originality.ai: the vendor's own spec holds on the tested clean corpus; the gap is
elsewhere.** The vendor claims "under 3%" false-positive rate and 99% accuracy for its Turbo
model (`data.json:46`). Independent measurement on the RAID benchmark's clean human corpus
(Dugan et al., ACL 2024, Table 4) puts FPR at 0.25%, inside the claimed range
(`data.json:43,46`). The tool's problem, per this row's own `key_finding`, is not the false-
positive spec but accuracy under distribution shift: 8.5% on Python code and 55.8% overall on
RAID's unseen extra domains, against a 99% accuracy claim (`data.json:47`, citing RAID Tables 4
and 7). Presenting this row as "the vendor's number is wrong" would misstate what was measured;
the vendor's false-positive number is not what fails here.

**6. The removed non-native-speaker (NNES) bars.** Every tool in `data.json` carries
`"nnes_fpr": null` (`data.json:11,22,33,44`) — no per-tool detector-specific NNES false-positive
rate survived the 2026-07-03 re-verification (session 07). The 61.22% figure that does appear in
this work is a **seven-detector average** from Liang et al. (*Cell Patterns*, 2023), not any one
tool's rate (`data.json:13,56`; restated in the page footnote at `work.astro:105-109`). An
earlier draft of this same work had displayed 61% as if it were GPTZero-specific and had
misstated a companion figure ("one detector flagged 98%" instead of the correct reading — 97.8%
of essays flagged by *at least one* of seven detectors, a union statistic); both errors are
logged as corrected (`data.json:56`; `work.astro:163-167`).

**7. The `claim_accuracy` and `claim_fpr` fields are vendor specifications, not
measurements.** `data.json` labels them exactly that in field name, and the `independent_fpr` /
`key_finding` fields are the only place independent measurement appears
(`data.json:8-10,19-21,41-43`; note ZeroGPT has no vendor claim retrievable at all —
`claim_accuracy` and `claim_fpr` are both `null` at `data.json:30-31`). The chart's "spec" bars
are self-reported by the companies whose tools they describe; this work did not measure vendor
accuracy claims independently, only the false-positive rates set against them.

**8. The harm register documents accusations and institutional consequences, not
detector-attributed court findings — read each row for what it actually shows.** Three rows:
Australian Catholic University (institutional, ~6,000 allegations, 25% dismissed, Turnitin
detection abandoned March 2025 — but the row's own outcome text notes "around 90% of the ~6,000
allegations were reported as AI-related — the displayed totals are not entirely detector-specific,"
`data.json:96`); an EMBA student at Yale (suspension, injunction denied May 2025, federal lawsuit
still pending as of the work's reference date — `data.json:108` — so this row describes an
ongoing, not a concluded, legal matter); and the University of Minnesota case (below).

**9. The Minnesota row carries its own load-bearing caveat, and it cuts against the intuitive
reading of the row.** The row's `caveat` field states plainly: "per the appellate record, the
disciplinary panel did not rely on AI-detection evidence — it credited graders' ability to
identify AI-written work, pointed to irrelevant sources, and cited missing citations and
inconsistent testimony. This row documents a case in which a detector figured in the accusation;
the courts did not attribute the consequence to the detector" (`data.json:121`). A reading of
this row as "a detector got a student expelled" is not what the appellate record, as summarised
here, supports.

**10. Named individuals do not appear in this register, deliberately, since 2026-07-12.** The
Yale and Minnesota rows read as role + institution + consequence; the official case captions sit
in the `source` field as citations, not in the outcome text
(`data.json:108-110,120-124`; policy recorded at `work.astro:190-202`, "REVISION (2026-07-12,
session 33)"). A re-telling that reinserts a name into the narrative text breaks a policy this
practice adopted on a binding steer, not an oversight — please do not add names back in.

**11. This practice ran its own exile-test against this exact subject and it came out
unresolved, against the easy reading — the caveat most likely to be dropped in a compressed
retelling.** A separate instrument, "The Backward Docket" (`works/2026-07-05-backward-regime-test/`,
instrument 011), tests whether a "reversed burden of proof" reading applies across this
practice's own filed material. Card 1 is AI text detectors in academic misconduct — the same
subject as this delivery. Its grade is **UNSETTLED**, its marks are `opacity: CLOSED`,
`presumption: UNPROVEN` (`works/2026-07-05-backward-regime-test/data.json:66`). The
`presumption_basis` field records that a sourcing expedition (session 19) found one retrievable
adjudication forum — the Office of the Independent Adjudicator for Higher Education (England &
Wales; a non-binding ombudsman) — and that its record **runs against** the reversal reading:
*"The responsibility is on the provider to prove that the student has done what they are accused
of doing, not on the student to disprove it"* (OIA casework note, quoted at
`works/2026-07-05-backward-regime-test/data.json:69`). Two limits on that finding, stated in the
same field: the OIA is non-binding, and it sits in a jurisdiction (England & Wales) different
from the two named US cases in this delivery's own harm register (Yale, Minnesota); the "pure"
scenario — detector output alone treated as dispositive, burden placed on the student — was
"never squarely adjudicated" in the record that was found (`data.json:69`). A prior attempt to
resolve the card to a cleaner grade on this same record was run and failed this practice's own
internal review as an overclaim (`data.json:79,199-200`). The honest summary: the retrievable
adjudication evidence does not support "detectors reverse the burden of proof" as a settled
finding, and it does not clear the opposite reading either. This is offered because it would be
easy to drop in a warm retelling of the certificate's headline finding — it complicates rather
than confirms the certificate's framing.

**12. The reference date and what it does and does not mean.** `data.json` is stamped
`"generated": "2026-07-01"` (`data.json:2`), and the page states "Reference date: {data.generated}"
(`work.astro:34`). The underlying studies cited throughout are dated 2023–2025 (Liang et al. 2023,
Dugan et al. 2024, Ibrahim et al. 2023, Pratama 2025 — `data.json:52-70`). Nothing in the work has
been re-measured since the 2026-07-01 reference date; the corrections logged on the page
(2026-07-03, 2026-07-12) are corrections to sourcing and framing of the same underlying studies,
not new measurements. A detector landscape that moves quickly should be assumed to have moved
since these studies were run; this work makes no claim about current-day tool behaviour beyond
what its cited studies measured at the time they were conducted.

## What we ask of a re-use, as offers not obligations

Two conditions this practice holds itself to for any re-use of its verified material
(`memory/downstream-commitments.md:33-41`), restated here in plain language and scoped to this
one instrument only:

- **If this work's status or any of its caveats change later, a re-use should update on the same
  cycle, or pause until it can.** A caveat frozen at today's snapshot, quietly carried forward
  after this practice has revised or corrected the underlying work, would misrepresent it.
- **A re-telling should keep the caveats above, not only the headline finding.** Compression is
  where a caveat gets dropped for pace, not from bad intent — that is the exact failure this
  document exists to guard against. If this work is ever the subject of an open rework or a
  contested status here, that status should be named by name in any derived account, not left as
  something a reader would have to chase back to this repository to discover.

These are offers. They bind nobody who has not accepted them. The receiver is free to decline
either or both, to use this material on its own terms, and to contest any part of this work or of
this caveat sheet — including the choices made in assembling it.
