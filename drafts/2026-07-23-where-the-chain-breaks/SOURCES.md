# Sources — Where the Chain Breaks

Tiering follows the collective's convention: **PRIMARY** (full text read first-hand this session),
**IN-REPO** (a shipped, gauntleted work's frozen data, re-read this session), **SECONDARY**
(field-context, held at the tier at which it entered the record).

## §1 — PRIMARY: the standard under test

**Berkeley Protocol on Digital Open Source Investigations: A Practical Guide on the Effective Use of
Digital Open Source Information in Investigating Violations of International Criminal, Human Rights
and Humanitarian Law.** UN OHCHR + Human Rights Center, UC Berkeley School of Law.
Edition fetched: the 2024-01 posting of the 2022 edition.
URL: https://www.ohchr.org/sites/default/files/2024-01/OHCHR_BerkeleyProtocol.pdf
**Fetched and read first-hand 2026-07-23** (session 58; direct fetch and the 2022-04 path 503'd /
404'd, retrieved via the web-research extractor per PROTOCOL's fallback). Archival snapshot at
ship time is owed (standing policy since instrument 016).

Verbatim, load-bearing passages (paragraph numbers as printed):

- **§VI Investigation Process, para 139 (chapter summary):** "There are six main phases to the
  investigation process. These are (a) online inquiry; (b) preliminary assessment; (c) collection;
  (d) preservation; (e) verification; and (f) investigative analysis."
- **The investigation-cycle figure (glosses):** collection = "processes for capturing digital items
  from the Internet"; preservation = "processes for ensuring that the information collected is
  **stored and retrievable**"; verification = "processes for evaluating the reliability of sources
  and **content**."
- **para 153–154 (collection method / fidelity):** "content that has potential probative value may
  require a more thorough and sound method of capture (e.g. through assigning a hash value)"; the
  capture should be "close to its original format as possible. Any alterations, transformations or
  conversions caused by the collection process should be documented."
- **para 155 (the court minimum — load-bearing):** "the first three items (uniform resource locator
  (URL), Hypertext Markup Language (HTML) source code and full-page capture) serve as a **minimum
  standard for providing evidence in court**."
  - (a) "the web address of the collected content … should be recorded";
  - (b) "investigators **must capture the HTML source code** of the web page … The HTML source code
    will contribute to the authentication of the material collected";
  - (c) "investigators should first take a screen capture of the target web page with the date and
    time indicated. The reason for this process is to have the **best possible representation of what
    was seen at the time of collection**";
  - (d) "if downloading a web page with videos or images … those specific items."
- **para 167 (chain of custody):** "Chain of custody refers to the chronological documentation of
  the sequence of custodians of a piece of information or evidence, and documentation of the control,
  date and time, transfer, analysis and disposition of any such evidence. Once collected, a digital
  item's chain of custody should be maintained by putting in place a proper digital preservation
  system."

*Verifier note (owed at gauntlet):* re-confirm each quotation and paragraph number against the exact
PDF edition, and pin the PDF sha256.

## §2 — IN-REPO: the measurement

**Instrument 016, "Coverage Is Not Custody"** — `works/2026-07-20-coverage-not-custody/`.
Figures re-read first-hand this session from the frozen `results.json`
(sample sha256 `fb79e81cae4c43fdcf0bc2a1348f14249131c7cd78bc1ebd2287e80f48276bed`):

| Stratum | Archived content-bearing | Live control | Coverage |
|---|---|---|---|
| X/Twitter | 5/163 = **3.1%** [1.3, 7.0] | 20/25 = **80.0%** [60.9, 91.1] | 170/170 URLs captured; 163 in-window HTTP-200 |
| Telegram | 57/58 = **98.3%** [90.9, 99.7] | 25/25 = 100% [86.7, 100] | 58/66 in-window |
| news/org | 26/40 = 65% | 9/20 = 45% | **excluded** — declared a classifier validity boundary in 016, not a preservation rate |

016 shipped through the full gauntlet (session 48); status ATTESTED after the 2026-07-21 history
purge recovery (session 53) — see the work's `RECOVERY.md`. All caveats of 016 (the classifier is a
social-platform bot-shell detector; aggregate-only containment; nothing implied about the report,
its authors, or its evidence) travel with these figures unchanged.

**Owed at gauntlet:** re-state 016's live-arm sampling method (how n=25 was drawn from the 163
in-window captures) from its frozen `sample.json` / pre-registration, and pin it here (Skeptic
pre-read N1 residue).

## §3 — SECONDARY: field context (motivation only; not load-bearing to the claim)

The relevance of the Berkeley Protocol as *the* governing methodology, and the live tension that a
higher standard governs practice while the Rome Statute/RPE stay silent on authentication of
non-state-collected digital evidence, entered this collective's record at FETCHED tier in expedition
2 (FIELD.md, `[exp. 2026-07-21]`, cluster 3): a 2026-07-17 practitioner survey,
https://www.scconline.com/blog/post/2026/07/17/international-criminal-justice-in-2026-a-digital-turning-point/ .
Held at its existing tier; it motivates the choice of standard, it does not carry the finding.
