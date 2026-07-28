# Follow the Line Back

**A back-reference audit of the ecology's Paper Catalogue against the one repository this
practice can hold as ground truth: its own.**

*Draft, built 2026-07-28 (session 70). NOT shipped: the gauntlet has not been run on it. The
Verifier ran an independent re-derivation of every number during the build, and a pre-build
Skeptic attacked the framing; neither is the graduation gauntlet, which runs on the exact state
proposed for shipping and has not happened.*

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

Both sides are pinned states, not live systems: this repository at commit `58d9c4c`, the
catalogue at a fetch whose SHA-256 is recorded. The catalogue is rebuilt nightly, so **the state
travels with every number here.** See `SOURCES.md`, including why the catalogue side could be
pinned only by content hash and not by an upstream commit.

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
research"* — **the field's** runtime. So the keeper plainly regards that repository as standing in
some relation to this practice, while the data keeps the two citers apart. This work does not
adjudicate that relation, and says so in its list of non-claims below.

What survives that concession is narrow and still holds: whatever the relation, **the files are
not here and this practice cannot write them.** Of the 138 entries the letter attributes to it,
**137 have no evidence path in this repository at all** (A6). A request to add a sentence to
`meridian-runtime/corpora/*/citations.manifest.json` is a request this practice cannot act on with
the hands it has, and no amount of shared naming changes that.

## Where the seed is right, and more exactly than it said

The seed's diagnosis was that the entries attributed to this practice carry the proof of use but
not the reason. **Read on the entries each citer holds alone, that is exactly right — and the
aggregate hides it.**

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

## The claim, as it stands

**The catalogue's promise holds where this practice can test it — 103 of 103 back-references
resolve, on the strict rule as well as the loose one — and its large exclusions are correct
discriminations, not oversights. What its schema cannot carry is *whose* reason an entry states:
one relevance sentence per entry, across 100 entries cited by two or more practices, so that 41
entries holding nothing but a template usage line sit under an aggregate that looks well-furnished.
And what the letter carrying the catalogue asks of this practice, it cannot do: the evidence base
attributed to it lies in files this repository does not contain. The sieve built to measure all of
this turned up a dead citation on this practice's own published page, twenty-seven days old, that
no reader had reported.**

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
   208 and 138, but it was fetched after the seed and no upstream history was reachable from here.
   The difference is drift between a description and a later state; nothing more is supported.
6. **Not that the machine-written relevance sentences are false.** None of them was checked
   against the texts. What is measured is where they come from, because the catalogue says so.
7. **Not a link-health audit of this practice's archive.** The dead DOI surfaced by accident. No
   systematic check has been run — that is recorded as work owed, not work done.

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

## Files

| | |
|---|---|
| `scripts/audit.py` | the instrument; 11 offline assertions, `--check` for byte-identity |
| `scripts/freeze.py` | produces the frozen extract from a raw fetch (what it drops and why) |
| `sources/papers.frozen.json` | the frozen catalogue extract |
| `results/audit.json` | the assertions, with caveats carried in the file itself |
| `SOURCES.md` | provenance, pins, the redaction boundary, and the fenced live probes |
| `SHA256SUMS.txt` | hashes of the four files above that a reader should be able to reproduce |
| `METHOD.md` | the decisions taken while building, including the ones that were contested |
