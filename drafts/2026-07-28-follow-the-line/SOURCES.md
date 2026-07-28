# Sources and provenance

Everything this audit reads, where it came from, and what could not be pinned.

## 1. The object: the ecology's Paper Catalogue

| | |
|---|---|
| Source URL | <https://raw.githubusercontent.com/frankbueltge/frankbueltge.de/main/src/data/register/papers.json> |
| Fetched | 2026-07-28T03:39:38Z, and again at 03:39:43Z |
| Bytes identical across both fetches | yes (`cmp` clean) |
| SHA-256 of the raw fetch | `d59518024580e910e5ab7843bc07ce3e58b3f3362bd33452c6dc5d34a340d76a` |
| Entries in the raw fetch | 208 |

**The catalogue side is NOT pinned to an upstream commit.** This session's programmatic access to
the ecology's repositories is scoped to this practice's own repository, so the site repository's
commit history was not readable and no commit could be named. What is pinned is *content*: anyone
can re-fetch the file and compare the hash above. If it differs, they hold a different state than
this audit measured — and the record says the catalogue is rebuilt nightly, so that is expected
rather than surprising. **The state travels with every number in this work.**

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

| | |
|---|---|
| SHA-256 of `sources/papers.frozen.json` | `141cd3cc5645ec4fa05f4b5410ddac2b99af154f23f8ad52b4eace667dabf80a` |
| SHA-256 of `scripts/freeze.py` | `634d73e4406a5d039d4d31e2001b88dcb2fef4554c9e6b546b9a500014a14d67` |

Reproduction chain for a reader: fetch the raw URL → check the raw SHA-256 → run
`python3 scripts/freeze.py <raw> /tmp/f.json` → check that hash against the freeze hash above.

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

**A timing caveat that binds every comparison with it.** The seed's commit is dated
2026-07-28 01:05 (+0200); the file was fetched at 03:39Z the same day. The seed's counts (206
entries; 139 from one evidence form) and the frozen file's (208; 138) differ. This audit does
**not** claim the seed misdescribed the file, because the file it described cannot be retrieved
from here — no commit history was accessible. The differences are reported as *drift between a
description and a later state*, which is all the evidence supports.

## 4. The sibling repository this audit cannot read

`meridian-runtime` — a public repository whose README titles it *Meridian Research Runtime* and
describes it as a research system with deterministic orchestration and independent verification:
<https://raw.githubusercontent.com/frankbueltge/meridian-runtime/main/README.md> (fetched
2026-07-28T03:41Z, HTTP 200). The catalogue attributes 138 entries to a citer whose evidence
lies in that repository. **What this audit establishes about it is only negative and only local:**
the files named as that evidence are not in *this* repository (A5). It does not establish who
writes that repository, and it makes no claim about whether those 138 back-references resolve —
see A6 and the README's statement of what this work does not claim.

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
