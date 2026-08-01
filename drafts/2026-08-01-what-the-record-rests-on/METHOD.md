# Method — What the Record Rests On

*Draft, 2026-08-01. Built by the collective Meridian. Not shipped; no gauntlet verdict. Every
number in `results.json` is produced by the scripts in this directory and by nothing else.*

## The question

A public register of AI harms is evidence infrastructure. It exists so that somebody — a
journalist, a regulator, a researcher, a court — can establish that a particular thing happened,
and it does that by pointing at documents held by other people. **This measures what is left at
the other end of those pointers, and what the register still holds if the answer is nothing.**

## The object, and why this one

The AI Incident Database (`https://incidentdatabase.ai/`) is measurable in a way most registers
are not: it publishes weekly, complete database snapshots (`https://incidentdatabase.ai/research/
snapshots/`) under CC BY-SA 4.0, and its report records carry a **stored full-text copy** of the
cited document alongside the URL. The stored copy is what makes layer 3 possible at all: without
it, one can ask whether a link resolves, but not whether what it resolves to still says what was
cited.

The register's own founding paper (McGregor, S., 2021, *Preventing Repeated Real World AI Failures
by Cataloging Incidents: The AI Incident Database*, IAAI-21, https://doi.org/10.1609/aaai.v35i17.17817)
describes the architecture, the editorial pipeline and the taxonomy. It does not discuss link rot,
archiving or source durability.

**Pinned input.** One snapshot, `backup-20260727110451.tar.bz2`, 104,995,975 bytes,
`sha256 fa13c2093c09ce039a9576ef7d69ef892b4e5e8dd47fd0b3b73badab7643d2f7`, `Last-Modified` Mon,
27 Jul 2026 11:05:46 GMT, retrieved 2026-08-01T03:38Z. The snapshot is **not** committed here — it
is pinned, and `build_inventory.py` verifies the hash and refuses to read a field if it does not
match. This instrument proves the provenance of its input, not only the determinism of its output.

**What is not committed, deliberately.** The register's stored copies are third-party documents
under their own rights. This repository never contains them. What it contains instead is a
**one-way fingerprint** per sampled record: the sorted, deduplicated set of SHA-1-derived hashes
(12 hex characters) of every 8-word shingle of the normalised text. The text cannot be
reconstructed from it. A live page can still be scored against it.

## The population and the inclusion rule

Stated once, applied once, in `build_inventory.py`:

> **Included:** a report record whose `url` field begins with `http://` or `https://`.

- Records in the snapshot's `reports.csv`: **7,408**
- Included (sourced report records): **6,602**, over **6,541** distinct URLs
- Excluded: **806**

Every excluded record carries a tag with a `variant:` prefix and has an empty title and an empty
description. The class is **not** homogeneous, and this is recorded rather than smoothed over: most
hold 40 characters or less of stored text — many hold the single character `1` — while 126 hold
more, and those read as substantive accounts of an incident. At least one, report 2587, holds
placeholder fixture prose beginning *"New text example… Lorem ipsum"*. The register's published
glossary uses "variant" for a taxonomic relationship between incidents; **whether the tag on these
records means the same thing is not established here and is not asserted.** They are excluded for
one reason only: a citation census cannot measure a record that makes no citation.

**Declared subclasses kept in the population**, checked rather than assumed:

- URLs pointing at a web archive or cache, which would make layer 2 circular: **0 found**.
- URLs pointing back at the register's own site: **1**.
- Language: 6,358 of 6,602 English; the rest across at least nine other languages. Lexical overlap
  behaves differently across languages, and any non-English record in the sample carries that caveat.
- Records sharing a URL with another record: **119 records over 58 URLs** (~1.8% of included
  records). **The unit of analysis is the report record — the citation — not the distinct URL.**

**Two integrity classes**, both found by the design's own pre-read and both carried into the
results rather than quietly filtered:

1. **19 records (0.29%) have `date_published` later than `date_downloaded`** — a document cannot be
   downloaded before it is published. Layer 2's precedence test compares a capture date against
   `date_downloaded`, so that field's error rate is not zero. Those records are flagged and are
   dropped from the precedence estimate.
2. **46 records declare, in their own stored text, that what the register holds is a stand-in** —
   an editor's note saying the report is a placeholder for a video, an interactive feature, or a
   post to be read at the source. Scoring these for drift would report the register's own disclosed
   incompleteness as a change in somebody else's page. They are measured at layers 1 and 2 and
   **excluded from layer 3**.

## The sample

Stratified by publication year: 2015 … 2026, plus one pooled stratum for everything published 2014
or earlier (earliest publication year in the pooled stratum: 1996). **Equal allocation, 20 report
records per stratum, 13 strata, n = 260**, drawn with the fixed seed
`meridian-2026-08-01-what-the-record-rests-on`. Same seed, same sample.

Population sizes are very unequal (112 in the pooled stratum, 1,448 in 2025). Equal allocation
therefore buys equal precision per stratum and **does not** produce a self-weighting corpus
estimate. Every corpus-wide number in `results.json` is a stratum-size-weighted estimate reported
with:

- per-stratum population, sampled n, and count with the property,
- the weights,
- a stratified 95% interval with a finite-population correction,
- the design effect from unequal weighting, and the effective sample size it implies.

A bare percentage without those is not a corpus rate, and this instrument does not print one.

## The layers

**L0 — inventory (offline, assertable).** Everything above. Deterministic; `--check` re-derives it
from the pinned snapshot and fails on any difference.

**L1 — does the citation resolve?** One GET per sampled record, redirects followed, 25-second
timeout, at most 3 MB read. Classes: `HTTP_200`; `REDIRECT_TO_ROOT` (a 200 whose final path is the
site root while the cited path was not — the soft-404 case, counted separately and never as a
success); `HTTP_404` / `HTTP_410`; `HTTP_401` / `402` / `403` / `451` (**withheld from this
vantage**, which is not the same as gone); other 4xx/5xx; `DNS_FAIL`, `CONNECT_FAIL`, `TLS_ERROR`,
`TIMEOUT`, `REDIRECT_LOOP`.

**Every non-200 is retried once with a self-identifying research user-agent**, and both outcomes are
recorded, so a bot wall can be told from a dead document instead of guessed at. The primary request
identifies as a current desktop browser, as the comparison literature does; both strings are printed
in the probe file.

**L2 — does anyone else hold it?** One query per URL to a public web archive's capture index,
collapsed to one row per month. Recorded: whether any capture exists, the first and last capture,
how many captures returned 200, and **whether a capture exists at or before the date the register
recorded downloading the document**. That last one is the question that matters: an archive that
first captured a page a year after it was cited is not evidence of what was cited. Index
unavailability is retried with backoff and, if it persists, recorded as `CDX_UNAVAILABLE` — never
as an absence of captures.

**L3 — does the resolving page still hold what was cited?** For records whose URL served this
vantage a document: extract text (scripts, styles and head removed), normalise identically to L0,
form 8-word shingles, hash them the same way, and score the **share of the register's stored
shingles that are present live**. Classes: `HOLDS` ≥ 0.50, `PARTIAL` 0.10–0.50, `ABSENT` < 0.10;
`SHELL` for a 200 that yields fewer than 100 words; `BOT_WALL` for a 200 that yields fewer than 300
words *and* carries a challenge-page marker; `REGISTER_STAND_IN` for the 46 declared placeholders;
`NON_HTML`, `NO_HELD_TEXT`, `NOT_APPLICABLE`.

**L3c — the control on our own extractor.** The pre-read's blocking objection: a low overlap
between a stored copy and a page extracted today cannot by itself tell drift from a mismatch
between two extraction pipelines. So the page is taken out of the comparison. For every case where
the live page did **not** clearly still hold the stored passage, the archived capture nearest to and
not after the register's own download date is fetched (raw stored bytes), run through **the same
extractor** and scored against **the same fingerprint**.

- archived copy scores high, live page scores low → the loss is on the live web.
- archived copy also scores low → the mismatch predates today; it is ours or the register's, and
  calling it drift would be false.

L3c is run only where it can decide something, so it is a control and **not a sample of anything**.
No rate from it is a corpus rate, and `results.json` prints it as counts.

## What this cannot say — standing scope exclusions

- **Nothing about why.** No class here distinguishes ordinary expiry from deliberate removal, and no
  such claim is made.
- **No comparison corpus.** There is no matched set of contemporaneous citations on other subjects,
  so nothing here says whether citations about AI harm decay faster or slower than citations in
  general. Published cross-sectional benchmarks are quoted in the findings for orientation only;
  they are different populations measured by different rules.
- **One vantage, one day.** Every live number is what a datacenter address behind a forward proxy
  saw on 2026-08-01. Refusals to this vantage are their own classes and are never counted as removal.
- **Lexical, not semantic.** A rewritten, re-edited or translated page that says the same thing
  scores as loss. That is a limit of the measure, not a finding about the page.
- **Not an editorial audit.** Nothing in HTTP status data supports any claim about the register's
  editorial practice or intent. The stored-copy field is, on its face, a mitigation this register
  built against exactly this problem.

## Where this sits in the literature — the method is not new, the object is

Reference rot and content drift are established, measured phenomena with a twelve-year literature.
This instrument re-runs a well-precedented design against an object nobody appears to have run it
against.

- **Klein, M., Van de Sompel, H., Sanderson, R., Shankar, H., Balakireva, L., Zhou, K., Tobin, R.
  (2014). "Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot." PLOS ONE
  9(12): e115253.** https://doi.org/10.1371/journal.pone.0115253 — the reference design for layer 1
  at scale, over ~3.5M articles and >1M web-at-large references.
- **Jones, S.M., Van de Sompel, H., Shankar, H., Klein, M., Tobin, R., Grover, C. (2016). "Scholarly
  Context Adrift: Three out of Four URI References Lead to Changed Content." PLOS ONE 11(12):
  e0167475.** https://doi.org/10.1371/journal.pone.0167475 — the direct precedent for layer 3, using
  an aggregate of four full-text similarity measures against archived snapshots, and the paper that
  gave the field the term *content drift*.
- **Zittrain, J., Albert, K., Lessig, L. (2014). "Perma: Scoping and Addressing the Problem of Link
  and Reference Rot in Legal Citations." Legal Information Management 14: 88–99** (reprint of 127
  Harv. L. Rev. F. 176). https://doi.org/10.1017/S1472669614000255 — the earliest large study to
  separate "returns 200" from "still holds the cited material", by hand. Layer 3 does at scale, and
  imperfectly, what that study did by human judgement.
- **Reyes Ayala, B., Du, Q., Han, J. (2022). "Detecting Content Drift on the Web Using Web Archives
  and Textual Similarity." TPDL 2022, CEUR-WS Vol-3246, paper 10.**
  https://ceur-ws.org/Vol-3246/10_Paper3.pdf — drift rates varying from 9.6% to 33.2% *by collection
  type*, which is why no single external rate is a fair benchmark for a news-heavy corpus.
- **Chapekis, A., Bestvater, S., Remy, E., Rivero, G. (2024). "When Online Content Disappears." Pew
  Research Center, 17 May 2024.** https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/
  — read first-hand: 25% of sampled pages from 2013–2023 no longer accessible as of October 2023;
  38% of pages that existed in 2013 gone a decade later; 23% of news webpages contain at least one
  broken link; 54% of Wikipedia pages contain at least one dead reference link, and 11% of all
  Wikipedia reference links are no longer accessible. The closest published comparator for a
  news-heavy citation base, measured by a deliberately conservative rule.
- **Paeth, K., Atherton, D., Pittaras, N., Frase, H., McGregor, S. (2024). "Lessons for Editors of
  AI Incidents from the AI Incident Database." arXiv:2409.16425.** https://arxiv.org/abs/2409.16425 —
  the register's editorial process reviewed against two taxonomies; source durability is not its
  subject.
- Two further items are named because they are relevant and because their identifiers were checked:
  **Nyayachavadi, A., Zhu, J., Madhyastha, H.V. (2022), "Characterizing 'Permanently Dead' Links on
  Wikipedia," IMC '22,** https://dl.acm.org/doi/10.1145/3517745.3561451, and **Bowers, J., Stanton,
  C., Zittrain, J. (2021), "The Paper of Record Meets an Ephemeral Web,"**
  https://doi.org/10.2139/ssrn.3833133. **Both were withheld from this vantage (HTTP 403) and have
  not been read here.** No figure from either is quoted anywhere in this work.

**The honest positioning.** None of the three live layers is a novel measurement instrument; each
has a direct precedent above. What has not been done, as far as this practice could establish, is to
run any of it against a register whose entire evidentiary function is to point at the specific place
a harm was documented. Two searches for such a study — one across the literature, one across the
register's own published list of related work — found none. That is an unverified negative, and it
is stated as one.
