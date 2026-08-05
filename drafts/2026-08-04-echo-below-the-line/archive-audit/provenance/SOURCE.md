# Where this audit's material comes from

All of it is public and committed by the audited instrument itself. Nothing here was produced by us
except the digests, which anyone can recompute.

## The dated snapshots

`provenance/consensus/*.json` — copied verbatim from the site repository at
`src/data/consensus/`, repository `frankbueltge/frankbueltge.de`, commit
**`cbd8ca22c39913bf38aaf983811abb632b220757`** (dated 2026-08-05 14:04:34 +0200), cloned
2026-08-05 ~12:57 UTC.

- 47 files copied: 46 dated snapshots `2026-06-21 … 2026-08-05`, plus `latest.json`, which duplicates
  a dated file and is excluded by the extractor (`scripts/extract_clusters.py` accepts only
  `YYYY-MM-DD.json`).
- Combined sha256 over the 47 files, in sorted filename order:
  `0fb3723d4bde94aef6775770e69ba2dab828865599c54b55a6b017346c7fb3d3`
- Per-file sha256 digests are recorded in `results/clusters.json` under `source_files`.

The instrument's own method sheet names this the canonical artefact:
> "Canonical artefact: versioned JSON in src/data/consensus/ — git is the archive."
(https://frankbueltge.de/werke/consensus/, fetched 2026-08-04, copy at
`../provenance/consensus-method-sheet-2026-08-04.html`.)

## The instrument's own pipeline source

`pipelines/consensus/refresh.py` at the same commit, sha256
`08f991a7e8b04eaef9457b62bd20ebc407ffa183a094955853f0afdcbb47499c`, permalink:
https://github.com/frankbueltge/frankbueltge.de/blob/cbd8ca22c39913bf38aaf983811abb632b220757/pipelines/consensus/refresh.py

Read first-hand rather than inferred from the published fields. The four facts this audit takes from
it, each with its line in that file at that commit:

| fact | line | text |
|---|---|---|
| the echo threshold | 40 | `MIN_DOMAINS = 3        # ein "Echo" gilt ab drei verschiedenen Quellen` |
| the phrase length | 39 | `SHINGLE_N = 6` |
| **the masthead cap** | 294 | `"mastheads": sorted(doms)[:40],` |
| the evidence-track cap | 289 | `evidence = sorted(per_dom.values(), key=lambda e: (e["at"] or "9999", e["domain"]))[:40]` |
| the near-duplicate threshold | 121 | `SOFT_TAU = 0.72  # Cosinus-Schwelle für „paraphrasierte" Koordination (v2)` |

And two behaviours, quoted from the same file:

- **`soft_echo_index` is the implemented v2 near-duplicate index**, seeded with the verbatim clusters
  so that it can only be larger: `soft_clusters(...)`'s docstring says the verbatim clusters are
  unioned first "damit wortgleiche Artikel garantiert zusammenbleiben (soft ⊇ verbatim) — TF-IDF
  mergt nur Paraphrasen obendrauf" (line 182). `soft_echo_index = round(len(soft_idx) / len(articles), 3) if articles else 0.0` (line 317).
- **`syndication.label` is a TLD-and-time heuristic, not an ownership judgement**:
  `classify_syndication` (line 129) computes the share of the most common **country TLD** across the
  mastheads and whether the spread is `span_hours <= 6`; `tld_share >= 0.8 and tight` →
  `"wire/chain syndication"`, else `distinct_tlds >= 3` → `"scattered placement"`, else `"mixed"`.

## The served pages

`provenance/pages/` and `../day2/provenance/` — the archive overview
(https://frankbueltge.de/consensus/archive/) and the day page
(https://frankbueltge.de/consensus/), both fetched 2026-08-05. Attempts to fetch per-day archive
URLs (`/consensus/archive/<date>/`) returned **HTTP 404**: the archive is one page, not one page per
day. Those two 404s are recorded rather than hidden, because a reader may reasonably expect the
per-day URL to exist.

## What we measured ourselves

- `provenance/dns-ns.json` — authoritative nameserver sets for all 596 domains, over DNS-over-HTTPS
  (resolvers `dns.google`, fallback `cloudflare-dns.com`), 596/596 answered, queried 2026-08-05
  ~13:03 UTC, each record carrying its own timestamp.
- `provenance/http-final.json` — the host each domain lands on after redirects; 519 of 596 answered,
  checked 2026-08-05 ~13:05 UTC. The 77 that did not answer contribute no redirect evidence and are
  recorded as failures.
