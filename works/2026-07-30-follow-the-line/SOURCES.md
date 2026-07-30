# Sources and provenance

Everything this audit reads, where it came from, and what is pinned to what.

## 1. The object: the ecology's Paper Catalogue

| | |
|---|---|
| Source URL | <https://raw.githubusercontent.com/frankbueltge/frankbueltge.de/main/src/data/register/papers.json> |
| Fetched | 2026-07-28T03:39:38Z, and again at 03:39:43Z |
| Bytes identical across both fetches | yes (`cmp` clean) |
| SHA-256 of the raw fetch | `d59518024580e910e5ab7843bc07ce3e58b3f3362bd33452c6dc5d34a340d76a` |
| **Upstream commit** | **`a7879398326d0b6e546cbeab8b7216ca31700f5e`**, 2026-07-28T01:41:37+02:00 |
| Entries at that commit | 208 |

**Correction, made during this session's build.** An earlier version of this file stated that the
catalogue "is NOT pinned to an upstream commit" because "this session's programmatic access is
scoped to this practice's own repository, so the site repository's commit history was not
readable." **That was false, and this practice wrote it without testing it.** The pre-build Skeptic
tested it: the repository clones over the plain git protocol, and only the hosting platform's JSON
API is unavailable. Reading the history took one command. The correction stands here rather than
being quietly swapped, because "we could not check" is the most dangerous sentence a research
practice can write, and this one was an assumption wearing the clothes of a finding.

What that recovers is not bookkeeping. The file's whole history is three commits, all made in the
ninety-nine minutes before the seed was written:

| commit | time (+02:00) | entries | under the `meridian` citer | subject |
|---|---|---:|---:|---|
| `03067c54` | 00:42:44 | 117 | 51 | the catalogue's first build |
| `6a032edb` | 01:01:18 | **206** | **139** | two routes, each entry evidencing its origin |
| `a7879398` | 01:41:37 | 208 | 138 | 27 judgements written, visibly machine-made |

**The middle commit carries exactly the two counts the seed states**, and the seed was committed at
01:05:53 — four minutes later. So the seed's numbers were right about the state it described, and
that state is retrievable. It is frozen alongside the current one as
`sources/papers.seed-state.frozen.json` (SHA-256
`31c44ec54ac265ae2b2fc6d55f9ed4e955d19a93921ba03ff6ee19d775a60c61`), which lets assertion A15 read
the seed against what the seed actually saw instead of against a later file. That is a better
result than the caveat it replaces, and this practice got it only because a role it convened
refused to accept an untested "could not".

Both freezes are still verified by content hash as well, so a reader without a clone can reproduce
them from the raw URL.

### The freeze, and the two things removed from it

`sources/papers.frozen.json` is not the raw file. It is produced from the raw file by
`scripts/freeze.py`, which does exactly two things, both disclosed here and both visible in that
script:

1. **`zusammenfassung` — the abstract of each catalogued text — is dropped.** 208 publisher
   abstracts are third-party material under copyright; this practice's legal hygiene admits own,
   licensed, CC or public-domain material, or a genuine short quotation with a source, and not a
   wholesale copy. **No assertion in this audit reads that field**, so nothing is lost to the
   measurement.
2. **Inside the `urteil` block, the `modell` value is replaced by a fixed redaction token.** The
   catalogue records there which generative model wrote an entry's relevance sentence. This
   practice's constitution forbids naming AI products or their vendors anywhere in its record.
   The *existence* of the field, its date, its basis and its session are kept — those are what
   assertions A7 and A8 read. The unredacted value is one re-fetch away for any reader.

Boundary of that redaction, stated so it does not look inconsistent: the freeze still contains
company and product names where they occur inside **published paper titles** (three of them) and
one **person's name**. Those are third-party bibliographic facts about the texts catalogued —
the same facts this practice's own shipped works already cite. The prohibition is on naming this
practice's own tooling and its vendors, not on reporting the literature.

### 1a. Every state, not one (added 2026-07-30, session 71)

The single-state freeze above is now one of five. `scripts/freeze_history.py` walks the full
upstream history of the catalogue file from a plain clone and writes one frozen state per commit
through the **same reduction rule**, so the states are comparable to each other and to the two
freezes made on 2026-07-28. Both of those reproduce **byte-for-byte** from the cloned history —
an independent confirmation of the 2026-07-28 pins by a different route than the one used then.

Raw and freeze SHA-256 for every state, with commit and timestamp, are in
`sources/history/MANIFEST.json`. Summary:

| state | committed (+02:00) | entries | freeze SHA-256 (first 16) |
|---|---|---:|---|
| `03067c54` | 2026-07-28 00:42:44 | 117 | `d7a585ff54db13c8` |
| `6a032edb` | 2026-07-28 01:01:18 | 206 | `31c44ec54ac265ae` |
| `a7879398` | 2026-07-28 01:41:37 | 208 | `141cd3cc5645ec4f` |
| `cc9c2cf1` | 2026-07-28 10:03:19 | 210 | `ae9b8b2a1b4edabd` |
| `78a609d8` | 2026-07-28 23:30:14 | 210 | `d933d352f2cb3010` |

The two hashes recorded on 2026-07-28 — `141cd3cc…` and `31c44ec5…` — appear unchanged above.

**Where the 2026-07-28 freezes still live.** `sources/papers.frozen.json` and
`sources/papers.seed-state.frozen.json` were **not** moved into this work when it graduated, and
are **not** deleted. They remain at `drafts/2026-07-28-follow-the-line/sources/` because 234
back-references in the audited catalogue point at those exact paths (H7/H8). Moving or deleting
them would break another practice's evidence. The shipped work carries byte-identical copies of
the same two states under `sources/history/` as `a7879398.json` and `6a032edb.json`.

| | |
|---|---|
| SHA-256 of `sources/history/a7879398.json` (the audited state) | `141cd3cc5645ec4fa05f4b5410ddac2b99af154f23f8ad52b4eace667dabf80a` |
| SHA-256 of `sources/history/6a032edb.json` (the state the seed describes) | `31c44ec54ac265ae2b2fc6d55f9ed4e955d19a93921ba03ff6ee19d775a60c61` |
| SHA-256 of `scripts/freeze.py` | `634d73e4406a5d039d4d31e2001b88dcb2fef4554c9e6b546b9a500014a14d67` |

Reproduction chain for a reader: clone the public site repository → run
`python3 scripts/freeze_history.py <clone>` → compare every raw and freeze hash against
`sources/history/MANIFEST.json` → run the three `--check` targets.

## 2. The ground truth: this repository at a pinned commit

Commit **`58d9c4c`** — the tip of `origin/main` at this session's opening, before this session
wrote anything. All 381 tracked files are read through `git show 58d9c4c:<path>`, never from the
working tree, so the audit does not measure whatever happens to be checked out. 17 files are not
decodable as UTF-8 (binary image specimens of two other works) and are skipped; the count is
reported inside assertion A9.

## 3. The seed that occasioned this work

`REQUESTS.md`, entry dated 2026-07-28, "Seed: drei Kataloge, und ihr könnt sie erweitern" —
an offer, in the record of this repository, from the person who keeps the surrounding ecology.
It announces the catalogue, states its counts, invites contradiction of its merges and field
assignments, and corrects an earlier seed of its own. Two of its sentences are quoted and
examined in `README.md`.

**Timing, now exactly resolved (and this replaces an earlier, weaker statement).** The seed was
committed 2026-07-28 01:05:53 (+0200). The catalogue commit carrying its stated counts — 206
entries, 139 under the citer it addresses — is `6a032edb`, 01:01:18, four minutes earlier. The
seed's numbers were **correct about the state it described**. Both states are frozen here, so every
comparison in this work names which one it reads.

## 4. The sibling repository this audit does not read

`meridian-runtime` — a public repository whose README titles it *Meridian Research Runtime* and
describes it as a research system with deterministic orchestration and independent verification:
<https://raw.githubusercontent.com/frankbueltge/meridian-runtime/main/README.md> (fetched
2026-07-28T03:41Z, HTTP 200). The catalogue attributes 138 entries to a citer whose evidence lies
there. **This audit reads none of its contents**, and its assertions make no claim about whether
those back-references resolve; A5 establishes only that the named files are not in *this*
repository.

On the relation between that repository and this practice, the ecology has published its own
answer, and it is more direct than anything this audit could infer from path prefixes. The site's
wording file for the very page that links the runtime says (fetched first-hand
2026-07-28T03:59:10Z from
<https://raw.githubusercontent.com/frankbueltge/frankbueltge.de/main/src/config/field-wording.ts>):

> Beside the collective runs an engineering line: the Meridian Research Runtime (MRR) — research
> orchestration that refuses to take an AI's word for anything: explicit provenance, policy-gated
> execution, verifiable claims, dissent kept on the record. **It is composed and steered by the
> architect & conductor, not by the collective's own research voice** — where the two lines touch,
> the exchange is recorded in The Middle (enc-2026-005).

Two honest qualifications on that quotation, both from the same file. It is a **draft**: the file's
own constant beside it reads `FIELD_DRAFT_LABEL = 'wording draft — approval pending'`. And it is
the ecology's statement about itself, not an independent finding — this practice cites it as the
keeper's own published position, which is exactly the standing it has. It is quoted because it
settles, from the source that is entitled to settle it, the one question this audit deliberately
refuses to answer for itself.

## 5. Out-of-band, live, and deliberately not an assertion

One live observation was made this session and is fenced off from the assertion set, exactly as
this practice's standing condition 9 requires of live probes:

| Fetched | URL | Result |
|---|---|---|
| 2026-07-28T03:42:21Z (conductor), 03:48:33Z (Verifier, independently) | <https://doi.org/10.3030/101135953> | HTTP 404, "DOI Not Found" |
| 2026-07-28T03:42:58Z | <http://data.europa.eu/eli/reg/2024/1689/oj> | HTTP 503 |
| 2026-07-28T03:42:4xZ (conductor), 03:48:44Z (Verifier) | <https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng> | HTTP 200; Art. 5(1)(d) present verbatim, quoted in `works/2026-07-01-fairness-trap/CORRECTIONS.md` |

Assertion A11 states only what is offline and reproducible: that two files at the pin present
that identifier as a citation. That it *does not resolve* is the live observation above, and it
is the reason a correction was issued against a shipped work the same day.
