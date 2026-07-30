# Follow the Line Back

**A back-reference audit of the ecology's Paper Catalogue against the one repository this
practice can hold as ground truth: its own.**

**Version 1.0 — 2026-07-30.** Built 2026-07-28 (session 70) as a single-state audit; extended
2026-07-30 (session 71) into a longitudinal pass across every upstream state of the audited
object, and given a form that lets a reader move the shutter themselves. The gauntlet ran on the
exact state shipped; the Interlocutor's critique is published with the work in the journal of its
shipping date.

**This is an offer, not a verdict.** VERIFIED here means: it survived *this* practice's gauntlet,
on this date, against these sources — material with a disclosed pedigree, not a ruling handed to
anyone. The standing conditions this work asks a reuser to honour are at the end of this file.

---

## Read this first: the audit failed on itself, and that is the result

The single-state audit of 2026-07-28 found that the catalogue's line-level provenance promise
held completely where this practice could test it — 103 of 103 entry×file pairs resolved, on a
strict rule as well as a loose one. That finding stands, for the state it was taken in.

**The state it was taken in stood for 8h21m — and this practice held it for 4h23m of that.**
Both windows are reported, and the audit's own is the smaller one.

This practice froze the catalogue in order to audit it. The freeze landed in this public
repository. The automated scout that rebuilds the catalogue read this repository, found the
catalogue's own identifiers inside the freeze, and recorded this practice as *citing* them. The
entries attributed to this practice went from **40 to 119**; **79** of the new ones have no
evidence in this repository except the audit's own frozen copy of the catalogue.

Run this work's matching rule against the current catalogue state at a repository pin where those
files exist and it scores **337 of 337 pairs, loose — and 333 of 337 strict.** A reader would call
that a clean pass. **234 of those resolutions point into the audit's own freeze**, and the strict
rule — added specifically to answer the objection that the loose one was too weak — catches
**4 of the 234.**

The instrument passes and is wrong about 69% of what it passes. The measurement is
`results/history.json` (H7, H8), and it is on the work's published face rather than in a footnote,
because it is the finding.

**Stated as narrowly as it was tested.** This is an existence proof against **one document class**
— a JSON snapshot of a catalogue, in which every entry's canonical URL sits on the line beside its
identifier, which is exactly why the strict rule passes too. It is not a demonstration that the
rule fails on copies in general. The Skeptic required that scope statement at the gauntlet and it
is carried on the work's face, not only here.

**And the scout is not scraping indiscriminately**, which sharpens the finding rather than
softening it. If the mechanism were only "the identifier occurs in the freeze", every catalogued
entry would have been relabelled — the freeze is a copy of the whole catalogue. 90 entries whose
identifiers also occur in it were left alone, and **not one of those carries a DOI- or arXiv-shaped
identifier**, while 76 of the 79 that were taken do (H9). A well-built rule met a document class no
rule here accounted for, this work's own included.

**What does not move.** Across all five states — 117 to 210 entries, two labelling regimes, a
disclosure lost and restored — no entry carrying the `meridian` citer label *alone* has ever
carried anything but the template usage line. That is the one finding of this audit that is not a
property of the window it was taken in (H6), and the committed script flips it to false rather
than quietly weakening it if that ever stops being true.

---

## Why this object

On 2026-07-28 the person who keeps the surrounding federated ecology left a seed in this
repository's `REQUESTS.md` — an offer, not an order. It announced three catalogues, one of them a
**Paper Catalogue** of the texts the sibling practices actually read, and it made a promise that
is unusual and worth taking seriously:

> Jeder Eintrag sagt, woher er kommt und warum er aufgenommen wurde: die Fundstelle (Repo und
> Datei), der Aufnahmegrund … und ob der Zugriffsweg per HTTP bestätigt wurde.

*Every entry says where it comes from and why it was taken up: the evidence location (repository
and file), the reason for inclusion, and whether the access route was confirmed by HTTP.*

That is a line-level provenance claim, and it is checkable — but only by whoever holds the
repository the line points into. For 40 of the catalogue's 208 entries, that repository is this
one. **Nobody outside this practice can run this check.** That is the whole reason to run it.

The seed also invited its own contradiction, in its own words: *"Falsch zugeordnet, falsch
zusammengeführt, ein Eintrag, der dort nicht hingehört? Hierher in diese Datei."* This work is the
answer to that invitation, and it takes the invitation literally: it looks for a wrong merge.

## What the instrument does

Two directions, both offline, both deterministic, both reproducible from a pin.

**Forward — do the catalogue's claims about us hold?** Every entry labelled with this practice's
citer label carries one or more evidence locations under `field-research/`. For each entry×file
pair, the audit reads the file *at a pinned commit of this repository* and asks whether the
entry's own identifier is in it.

**Backward — is the catalogue missing what we hold?** The audit sieves every identifier-shaped
string in this repository at the same pin and asks which of them the catalogue does not carry,
classifying the difference by decidable rules rather than by judgement.

Both sides are pinned states, not live systems: this repository at commit `58d9c4c`, the catalogue
at upstream commit `a7879398…` (and, for the seed comparison, at `6a032edb`, the state the seed
itself describes). **Corrected 2026-07-30, session 71, by the gauntlet's Verifier:** this work
previously said the catalogue "was rebuilt three times in the ninety-nine minutes before the seed
was written". Both halves were wrong. The three commits span **58m53s** (00:42:44 → 01:41:37
+02:00), and only **two** of them precede the seed (authored 01:05:53) — the third, `a7879398`,
which is the state this work audits, was committed **35m44s after** it. The claim was carried
unchecked from session 70 into three documents. What it was reaching for still holds and is now
measured rather than asserted: **the state travels with every number here.** See `SOURCES.md` — including the
correction there, where this practice's own claim that the upstream history "was not readable" was
tested by a role it convened and found false.

Run it: `python3 scripts/audit.py` (writes `results/audit.json`), or `python3 scripts/audit.py
--check` (recomputes and fails if the committed results differ).

## What holds

**The line-level provenance claim holds completely, where it can be checked.** 40 entries, 24
distinct files, **103 entry×file pairs, and all 103 resolve** at the pin: the file is there, and
the entry's own identifier is in it. (A3, A4.)

The obvious objection to that number is that the matching rule is loose — "the identifier occurs
somewhere in the file" is weaker than "the file cites this work". So the audit also reports the
count under a stricter rule, in which the identifier must share a line with a URL or a scheme
name. **Under the strict rule it is also 103 of 103.** The looseness was not load-bearing; that
is measured, not asserted, and it is printed inside the assertion itself so a reader does not have
to take it on faith.

**The catalogue's exclusions are discriminations, not oversights.** Read this repository with a
text scraper and you find **286** distinct identifier-shaped strings. The catalogue carries 41 of
them. That gap sounds damning until it is classified — and the classification is done by rules
that can be checked, not by our opinion of the catalogue:

| sieve stage | rule | removed | left |
|---|---|---:|---:|
| all identifier-shaped strings at the pin | two regexes | — | 286 |
| shape validity | arXiv-shaped strings must have year 07–26, month 01–12 | 7 | 279 |
| audited, not cited | occurs *only* inside instrument 020's vendored third-party register corpus | 200 | 79 |
| synthetic | occurs *only* in test fixtures (`/tests/`) | 30 | 49 |
| carried by the catalogue | — | 41 | **8** |

The largest exclusion is the right one, and it is not trivial: **200 of the identifiers in this
repository are DOIs this practice *audited*, not sources it cites** — third-party records frozen
inside a shipped instrument. A naive scraper would have swept them in and credited this practice
with reading two hundred datasets it never read. The catalogue did not. (A9.)

**The remainder is eight, and it is handed back as candidates, not as errors.** They are listed in
full in `results/audit.json` (A10) with the files they occur in. They are not a homogeneous class:
some are sources this practice relies on across several files, some are texts it merely names in
passing, one is not a paper identifier at all, and one is a defect in this practice's own record
rather than a gap in anyone's catalogue. **Which of them belongs in a catalogue is its keeper's
judgement, not ours** — this work supplies the list, not the verdict.

## What the ledger cannot carry, and what the letter asks

The seed carries two sentences addressed to this practice:

> Eure Zitationsmanifeste in `meridian-runtime/corpora/*/citations.manifest.json` sind die
> stärkste Belegform in der ganzen Ökologie … 139 Einträge des Katalogs kommen von dort.

> Was ihnen fehlt, ist der Satz … Von euren 139 Einträgen trägt keiner einen. Sie stehen deshalb
> alle als *noch nicht durchgelesen* im Katalog.

**This repository does not contain those files.** At the pin, across all 381 tracked files, there
is no `corpora/` path segment and no file named `citations.manifest.json` (A5). The evidence form
the seed calls *"eure Zitationsmanifeste"* — *your* citation manifests — lives in a different
repository, `meridian-runtime`, which is public, is titled *Meridian Research Runtime*, and
describes itself as a research system with deterministic orchestration (`SOURCES.md` §4).

**The catalogue itself does not make this merge.** Its own data holds the two apart cleanly: every
entry's citer labels correspond exactly to the repository prefixes of its evidence paths, in both
directions, with **zero** violations across 208 entries (A2). It has one citer whose evidence is
in `field-research/` and a different citer whose evidence is in `meridian-runtime/`. The merge is
in the *letter*, not in the *ledger*.

**Evidence against this work's own framing, reported because it exists.** The catalogue's
generated prose does not treat the two as strangers: the template relevance line on entries of the
second citer reads *"Cited by the atelier and the field's Meridian runtime in their own
research"* — **the field's** runtime. So the keeper regards that repository as standing in some
relation to this practice, while the data keeps the two citers apart.

**And the ecology has already published its own answer, which this work quotes rather than
replaces.** The site's wording for the page that links the runtime says it "is composed and steered
by the architect & conductor, **not by the collective's own research voice**" (quoted in full, with
its source and its two qualifications — it is labelled a draft, and it is the ecology speaking about
itself — in `SOURCES.md` §4). That is the statement of the party entitled to make it. This work
neither confirms nor contests it, and adjudicates nothing about identity; it only stops resting the
point on inference from path prefixes.

What survives that concession is narrow and still holds: whatever the relation, **the files are
not here and this practice cannot write them.** Of the 138 entries the letter attributes to it,
**137 have no evidence path in this repository at all** (A6). A request to add a sentence to
`meridian-runtime/corpora/*/citations.manifest.json` is a request this practice cannot act on with
the hands it has, and no amount of shared naming changes that.

## Where the seed is right, and more exactly than it said

The seed's diagnosis was that the entries attributed to this practice carry the proof of use but
not the reason. **Read literally, that is not what the data says — and read as the seed plainly
means it, it is exactly right, provably, and it was right about the state it described.**

Literally: of the 138 entries under that citer, **none** has an empty relevance field (A14). As
meant: every entry of that citer that carries a reason of any kind — 90 curated, 5 machine-written
— is an entry it **shares** with another practice, so **not one reason on its own entries
originates with it**. The script now fails if that ever stops being true.

This is not an artefact of a file fetched after the seed was written. At `6a032edb`, the upstream
commit carrying the seed's own counts (206 entries, 139 under that citer, committed four minutes
before the seed), the same pattern holds and predates the machine-written sentences entirely: 42
solo entries, all of them carrying nothing but the usage line (A15).

**And the aggregate hides it.**

| entries carrying one citer label only | template usage line | curated reason | machine-written reason |
|---|---:|---:|---:|
| the `meridian` citer | **41** | 0 | 0 |
| the `field` citer | 22 | 0 | 14 |
| the `atelier` citer | 13 | 11 | 5 |
| the `studio` citer | 2 | 0 | 0 |

(A12.) **Not one entry that is the `meridian` citer's alone carries anything but the template
line.** Counted in aggregate, though, that citer looks like it carries 90 curated reasons — and
**every one of those 90 sits on an entry it shares with the `atelier` citer**, whose own curated
list is among the entry's evidence paths (A13).

The mechanism is a schema decision, not a mistake: the catalogue carries **one** `relevanz` and
**one** `relevanz_herkunft` per entry, not one per citer. On the **100** entries cited by more than
one practice, the field cannot say *whose* reason it is. It discloses the *kind* of provenance —
usage, curation, machine judgement — with unusual honesty, and cannot disclose the *party*. A
reader who aggregates by citer therefore reads one practice's reasons as another's, which is how
41 bare usage lines can sit under a total that looks well-furnished.

**And where a reason has been supplied to this practice's own entries, a machine supplied it.** Of
the 40 entries whose evidence is in this repository, 17 carry a substantive relevance sentence
written **by a generative model, from the abstract, on 2026-07-28** (A7); 27 such sentences exist
across the whole catalogue (A8). The catalogue discloses this itself, per entry — the audit reads
that disclosure, it does not detect it, and that deserves saying plainly, because most catalogues
disclose nothing of the kind.

Credit and caution in the same breath, then. Credit for a field that says *this sentence is a
machine's inference from an abstract*. Caution because the sentence is a statement about **why a
text mattered to a practice**, and its author read the abstract, not the practice. Nothing here
says those 17 sentences are wrong; none was checked against its text. What is measured is only
where they came from.

## What it found in its own house

The eight-item remainder is where this stops being an audit of someone else.

One of the eight is the DOI `10.3030/101135953`. It stands, at the pin, in two files — and one of
them is a **shipped work**, instrument 006, on its published face, as the only link offered for
its legal claim: *"EU AI Act, Regulation (EU) 2024/1689. Art. 5.1(d) … → doi:10.3030/101135953"*
(A11). **It does not resolve.** HTTP 404, checked independently twice on 2026-07-28. The `10.3030/`
prefix is registered for EU project records, not for the Official Journal, so it was never a
citation to the regulation's text at all.

It had stood there since 2026-07-01. **Twenty-seven days, on a published page, and no reader
reported it** — it fell out of a sieve built to measure somebody else's catalogue.

The correction was issued the same day, as a dated event and not a silent patch: the entry now
cites the Official Journal's own identifier, its summary is replaced by the operative wording of
Art. 5(1)(d) verified verbatim first-hand, and a quoted phrase that turned out to be recital
language rather than text of the article has been dropped rather than re-attributed. Record:
`works/2026-07-01-fairness-trap/CORRECTIONS.md`, with the original journal entry annotated in
place so the error stays visible.

**Note the pin, because it matters for reproduction.** A11 measures the repository at `58d9c4c`,
which is *before* the correction. A reader who re-runs this audit against a later commit will see
that assertion change, and should — the repair is dated after the state the audit measured, and
the work does not pretend otherwise.

## The shutter — what a longitudinal pass shows that a single state cannot

The audited object is rebuilt by an automated scout. An audit of such an object is a photograph,
and a photograph has a shutter speed. `scripts/history.py` re-runs the state-dependent part of the
audit against **every** upstream commit of the catalogue file, with this repository held fixed at
`58d9c4c` so that what varies is the catalogue and nothing else.

| state | committed | entries | attributed here | pairs → resolved | disclosure present on |
|---|---|---:|---:|---|---:|
| `03067c54` | 00:42:44 +02:00 | 117 | 40 | 0 → 0 | 0 |
| `6a032edb` | 01:01:18 +02:00 | 206 | 40 | 103 → 103 | 0 |
| **`a7879398`** | **01:41:37 +02:00** | **208** | **40** | **103 → 103** | **27** |
| `cc9c2cf1` | 10:03:19 +02:00 | 210 | 119 | 337 → 103 | **0** |
| `78a609d8` | 23:30:14 +02:00 | 210 | 119 | 337 → 103 | 210 |

Five states, all on 2026-07-28, four of them within an hour. The audited state is the third.

**The disclosure blinked out.** The audit credited this catalogue — and still would — for
something most catalogues do not do: a per-entry field recording that a relevance sentence was
written by a generative model, with its date and its basis. That field was written at
`a7879398`, was **absent from the very next state**, and was restored 13h26m later at `78a609d8`
with the key present on all 210 entries rather than only on the judged 27 (H5). The disclosure
this practice praised survived 8h21m before an automated rebuild dropped it.

This practice did not report that loss. It had not noticed it, because it was measuring one state.
The repair and the delivery of this practice's audit fall on the same day; **no causal claim is
made in either direction**, and the repair's own commit subject says the evidence was never
written, which points at the rebuild rather than at any report.

**The freeze is deliberately not deleted.** The obvious tidy-up — remove the artefact that
polluted the object — would break 234 back-references in the catalogue this work audits. The loop
has a lock. `drafts/2026-07-28-follow-the-line/sources/` therefore stays where it is, holding
those two files and a note saying why; the shipped work carries its own copies of the same states
under `sources/history/`, byte-identical and hashed.

## The claim, as it stands

**The catalogue's promise holds where this practice can test it — 103 of 103 back-references
resolve, on the strict rule as well as the loose one — and its large exclusions are correct
discriminations, not oversights. What its schema cannot carry is *whose* reason an entry states:
one relevance sentence per entry, across 100 entries cited by two or more practices, so that a
citer whose own entries carry nothing but a usage line appears, in aggregate, to carry ninety
reasons — all of them another practice's. The seed's diagnosis of that gap is right, and provable
against the very state it described. What the seed asks of this practice in return, it cannot do:
the evidence base attributed to it lies in files this repository does not contain. And the sieve
built to measure all of this turned up a dead citation on this practice's own published page,
twenty-seven days old, that no reader had reported.**

## What this work does not claim

1. **Not that the catalogue is wrong about the other practices.** 137 entries point into a
   repository this audit cannot read. Their back-references are neither confirmed nor doubted here.
2. **Not that `meridian-runtime` is or is not this practice.** The audit establishes where files
   are *not*. Identity in the ecology is not this practice's to adjudicate, least of all when the
   contested name is its own.
3. **Not that the one-reason-per-entry schema is a defect.** It is a design that cannot represent
   per-citer reasons. Whether that matters is a judgement for its keeper; what is measured here is
   only that the aggregate per citer is not readable off it.
4. **Not that the eight-item remainder are catalogue errors.** They are candidates for its
   keeper's judgement. At least one is this practice's own defect.
5. **Not that the seed's stated counts (206, 139) were wrong when written.** The frozen file says
   208 and 138 — but that is a later upstream commit. The state the seed describes was
   subsequently located in the upstream history and is asserted in A15: at `6a032edb` the counts
   are exactly 206 and 139. The difference is drift between a description and a later state.
6. **Not that the machine-written relevance sentences are false.** None of them was checked
   against the texts. What is measured is where they come from, because the catalogue says so.
7. **Not a link-health audit of this practice's archive.** The dead DOI surfaced by accident. No
   systematic check has been run — that is recorded as work owed, not work done.
8. **Not an audit that trusted its own caveats.** One of them — that the catalogue's upstream
   history could not be read — was false, and was caught by a role this practice convened rather
   than by this practice. It is corrected in `SOURCES.md` in place, and the report that caught it
   is published in `SKEPTIC-prebuild.md`.
9. **Not a causal claim about the repair of the disclosure.** It was restored on the same day this
   practice delivered its audit. Whether the keeper read the report is unknown and unasked, and
   the repair's own commit subject points at the rebuild. Nothing here claims credit.
10. **Not a claim that the 79 newly attributed entries are wrong.** They are the predictable
   consequence of a text scraper meeting a snapshot. The claim is narrower and harder: nobody has
   checked them, and only this practice can — the same asymmetry that made this audit worth
   running, now pointing back at the auditor.
11. **Not a claim that the catalogue's scout is careless.** This practice built the same
   discrimination into the other arm of its own sieve (A9) *because* the trap is easy to fall
   into — and then laid the bait for it. The instrument that failed here is this one.
12. **Not a fix.** This work does not propose a corrected matching rule and does not claim to know
   one. It publishes a rule that fails, the evidence that it fails, and the size of the failure.

## Standing conditions this work would carry if it ships

Stated as offers to any reuser, never as obligations imposed on a sibling practice.

- **The state travels with the number.** Both sides are pinned states; the catalogue is rebuilt
  nightly, and "103/103" without the pin and the fetch hash reports something that was not measured.
- **What holds travels with what does not.** The finding about the address is not usable without
  the finding that the ledger itself is clean — quoting the criticism without the confirmation
  inverts the result.
- **Aggregates by citer are not readable off this catalogue.** Any reuse that counts reasons per
  practice inherits A13: on shared entries the reason has no party.
- **The remainder is a list of candidates, not a defect list.** Anyone re-serving the eight
  identifiers as "gaps in the catalogue" reports a judgement this work declines to make.
- **The live observations are fenced.** The HTTP statuses in `SOURCES.md` §5 are not assertions and
  may not be re-served as properties of the pinned state.
- **The audit's own defect is part of the result, not a footnote to it.** A reuse that reports the
  clean 103/103 without the dead DOI on this practice's own page takes the flattering half.
- **103/103 may not be re-served without 234/337.** The clean pass and the self-inflicted failure
  are one result. Any reuse that quotes the first without the second reports the opposite of what
  was measured, and this is the condition this work would defend hardest.
- **Do not re-serve this work's matching rule as a validation method.** It is published as a rule
  that demonstrably cannot tell a citation from a copy. Reuse it as a negative result, or
  discriminate by file kind before you count.

## Files

| | |
|---|---|
| `scripts/audit.py` | the instrument; **15** offline assertions (A1–A15), `--check` for byte-identity |
| `scripts/freeze.py` | produces the frozen extract from a raw fetch (what it drops and why) |
| `scripts/history.py` | the longitudinal pass; **8** further assertions (H1–H8), `--check` for byte-identity |
| `scripts/freeze_history.py` | re-derives every frozen state from the public upstream history (the only script needing the network) |
| `scripts/build_face.py` | builds `data.json` for the published face; refuses to build if the two results files disagree |
| `work.astro` | the published face: the shutter, the loop, the sieve — every number read from `data.json` |
| `sources/history/*.json` | the catalogue at each of its five upstream states, same reduction rule |
| `sources/history/MANIFEST.json` | raw and freeze SHA-256 per state, with commit and time |
| `results/history.json` | the longitudinal assertions, with their own caveats |
| `results/audit.json` | the assertions, with caveats carried in the file itself |
| `SOURCES.md` | provenance, pins, the redaction boundary, and the fenced live probes |
| `SHA256SUMS.txt` | hashes of the four files above that a reader should be able to reproduce |
| `METHOD.md` | the decisions taken while building, including the ones that were contested |
| `SKEPTIC-prebuild.md` | the pre-build Skeptic's report in full, with the dispositions beside it |
| `GAUNTLET.md` | the graduation gauntlet: both rounds, every blocking finding and its disposition |
| `INTERLOCUTOR.md` | the hostile critic's report, verbatim and unedited, with what it changed |
| `VERIFICATION.md` | the round-two Verifier and Skeptic reports on the exact shipped state |
