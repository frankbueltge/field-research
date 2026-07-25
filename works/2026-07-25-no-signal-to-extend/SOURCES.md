# Sources — No Signal to Extend (Homogenization Dossier v1)

Every URL below is already present in this collective's records (the pre-registration, results
note, verification memo, or `memory/claims.md`) — none was fetched fresh for this document.

## The published series being extended

- **Sourati, Karimi-Malekabadi, Ozcan, McDaniel, Ziabari, Trager, Tak, Chen, Morstatter, Dehghani
  — "The Shrinking Landscape of Linguistic Diversity in the Age of Large Language Models."**
  Abstract page: https://arxiv.org/abs/2502.11266v1 · Full text (re-verified first-hand,
  2026-07-25): https://arxiv.org/html/2502.11266
  Load-bearing for: the finding this instrument extends (arXiv cs.CL/cs.CV corpus, Jan
  2018–Nov 2024, N=80,238 papers); the ONSET/POST/Time regression coefficients quoted in "The
  question"; and the Scope-boundary section's claim that the published quantity is
  between-document variance of five complexity features (Cronbach's α=.965), not a level metric.

## The marker channel (attribution context)

- **Kobak, González-Márquez, Horvát & Lause (2025), "Delving into LLM-assisted writing in
  biomedical publications through excess vocabulary," Science Advances 11(27), eadt3813.**
  https://www.science.org/doi/full/10.1126/sciadv.adt3813
  Load-bearing for: the paper of origin of the excess-vocabulary marker list.
- **The marker list itself**, `results/excess_words.csv` in the authors' public repository:
  https://raw.githubusercontent.com/berenslab/llm-excess-vocab/main/results/excess_words.csv
  (repository: https://github.com/berenslab/llm-excess-vocab), fetched 2026-07-25, sha256
  `f5786f3cc83f9578043aaecf2774c6200cb68b5e774afc3afe40af4eb0cf8285`.
  Load-bearing for: the exact 407 `type=="style"` words used as this instrument's marker set
  (pinned pre-lock; the list's own PubMed-baseline excess rates are never imported, only the
  word list travels — this instrument re-baselines on its own 2015–2022 corpus rates).
- **Fitterer, Gangl & Ulbrich, ACL 2025 Student Research Workshop.**
  https://aclanthology.org/2025.acl-srw.95/
  Load-bearing for: the published news-corpus dissociation (marker/style-word ratio and MTLD
  both rising, two other diversity metrics flat) that this Dossier's own mixed-signal reading
  replicates on a much larger academic corpus.

## The harvest route and its licensing (pre-registration deviations D1/D1a)

- **The archive's query API**, the harvest endpoint actually used after the route switch:
  https://export.arxiv.org/api/query
  Load-bearing for: the corpus of 338,151 records this instrument's four margin metrics and
  marker channel are computed on.
- **The archive's API terms of use** (re-verified first-hand before the D1 route switch,
  2026-07-25): https://info.arxiv.org/help/api/tou.html
  Load-bearing for: the CC0 licensing of the harvested metadata (including abstract text),
  confirmed to hold under the substitute route exactly as it held under the originally
  pre-registered OAI-PMH route.

## In-repo, load-bearing for this work's own claims

- `./PREREGISTRATION.md` — the locked instrument spec
  (corpus rules, four margin metrics, null model, decision rule, control-validity gate, kill
  condition, deviations log D1/D1a).
- `./RESULTS-NOTE.md` — the first-run record (harvest
  counts, contamination ceilings, marker-channel and MTLD observations).
- `./results/summary.md` and `results/results.json` —
  the exact per-metric, per-stratum tables reproduced in this work's Result section.
- `./VERIFICATION-sourati.md` — first-hand re-verification
  of the Sourati et al. Study-1 specifics against the paper's full text, including the exact
  regression coefficients quoted above.
- `memory/downstream-commitments.md` — the standing conditions this work travels under, and the
  governing principle ("a caveat stated once here must not go unstated twice downstream") this
  work's own load-bearing caveat is stated against.
