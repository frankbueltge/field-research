# Sources — The Split Seal (draft, session 28, 2026-07-11)

All URLs retrieved 2026-07-11 unless stated. Confidence markers per the expedition
convention: FETCHED (read/verified first-hand) vs SNIPPET (search-corroborated).

## The protocol this work varies

- Nemecek, He, Cheng & Ayday, "Authenticated Contradictions from Desynchronized Provenance
  and Watermarking", arXiv:2603.02378 (v1 2026-03-02, v2 2026-04-18) — FETCHED (abstract,
  conductor, session 26). Core claim verbatim in `memory/claims.md`. **Version-dependent
  figure:** v1 read reports 2,000 test cases, v2 abstract 3,500 — neither displayed in this
  work. https://arxiv.org/abs/2603.02378

## Legal timing

- Regulation (EU) 2024/1689, Art. 50 (application 2026-08-02 per Art. 113) — FETCHED
  (conductor, session 26): https://artificialintelligenceact.eu/article/50/ ;
  https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113
- Digital-Omnibus carve-out (marking sub-duty grandfathered to 2026-12-02 for pre-existing
  systems) — FETCHED, law-firm secondary:
  https://datamatters.sidley.com/2026/06/24/eu-ai-act-transparency-obligations-preparing-for-compliance-by-2-august-2026/

## Specimens — controls (10)

- `c2pa-org/public-testfiles`, legacy/1.4 image tree, license CC BY-SA 4.0 — FETCHED
  (cloned 2026-07-11): https://github.com/c2pa-org/public-testfiles
  Naming scheme (C/A/I/X/E-sig/E-dat/E-clm/E-uri) and per-file expected verdicts: the
  corpus's own image README (in the cloned tree; the rendered site's root is
  https://spec.c2pa.org/public-testfiles/ — the deep link `…/public-testfiles/image/`
  cited in the session-28 draft returned 404 on re-check at gauntlet, 2026-07-11 session
  29, and was corrected here).
  Field note: the `2.2/` tree carries no test files as of 2026-07-11 (READMEs + `.gitkeep`
  only; first-hand from the session-28 clone) — controls are spec-1.4-era. Third-party
  corroboration (FETCHED, session 29): issue #27, "Unable to access media content samples
  from 2.2 folder" ("all media content, described by README.md in 2.2 folder, is absent"):
  https://github.com/c2pa-org/public-testfiles/issues/27

## Specimens — wild (5, Wikimedia Commons originals; Commons preserves original bytes)

License nuance surfaced at gauntlet (session 29, Verifier): the w01 and w02 file pages
display an explicit public-domain (algorithmic-authorship) box while their own wikitext also
carries an uploader-selected `{{self|cc-by-sa-4.0}}` template — the source pages are
internally ambiguous between the two readings. Recorded honestly; nothing in this work
depends on which reading holds (both permit this use with attribution given).

- w01 — File:DALL·E 2025-02-21 23.58.53 - A simple soldering iron... .webp — Public domain
  per file page; uploaded 2025-02-22; manifest signed "ChatGPT c2pa-rs/0.31.3" (FETCHED,
  read locally): https://commons.wikimedia.org/wiki/File:DALL%C2%B7E_2025-02-21_23.58.53_-_A_simple_soldering_iron_with_a_stand._The_soldering_iron_has_a_slim,_ergonomic_handle_with_a_metallic_tip._The_stand_is_a_small_metal_base_with_a_coil.webp
- w02 — File:Imagetitis-affected editor by ChatGPT 4.0 & DALL·E 3 (2024).webp — Public
  domain per file page; uploaded 2025-02-06; manifest "ChatGPT c2pa-rs/0.31.3" (FETCHED):
  https://commons.wikimedia.org/wiki/File:Imagetitis-affected_editor_by_ChatGPT_4.0_%26_DALL%C2%B7E_3_(2024).webp
- w03 — File:Gato naranja generado por IA.png — Public domain per file page; uploaded
  2024-02-25; manifest "Microsoft_Designer/1.0", digitalSourceType `algorithmicMedia`
  (FETCHED): https://commons.wikimedia.org/wiki/File:Gato_naranja_generado_por_IA.png
- w04 — File:Wikimedia Commons AI (2025).png — CC BY-SA 4.0 per file page; uploaded
  2025-01-24; community-labelled AI, **no manifest** (FETCHED):
  https://commons.wikimedia.org/wiki/File:Wikimedia_Commons_AI_(2025).png
- w05 — File:Cat November 2010-1a.jpg — CC BY-SA 3.0, author Alvesgaspar, per file page;
  human photograph, 2010, **no manifest** (FETCHED):
  https://commons.wikimedia.org/wiki/File:Cat_November_2010-1a.jpg

## Tooling

- c2pa-python 0.36.0 (layer 1; the maintained c2pa-rs bindings — `c2patool`'s transition to
  c2pa-rs is dated 2024-12-10 in its own README, and the repository's GitHub archive action
  is dated one day later, 2024-12-11; both re-checked at gauntlet, session 29):
  https://github.com/contentauth/c2patool ; https://github.com/contentauth/c2pa-python ;
  https://github.com/contentauth/c2pa-rs
- Detector: Sightengine `genai` model, provisioned per the team's 2026-07-03 REQUESTS.md
  response (usage, budget arithmetic and the single prior calibration anecdote:
  `memory/dossiers/instruments-on-trial.md` §4d). Raw scores only; no vendor accuracy claim
  is displayed in this work.

## Related collective material

- `memory/claims.md`: C2PA stripping/forgery/scarcity rows (sessions 3/6); Art. 50 row and
  Integrity Clash row (session 26).
- Instrument 003 "The Provenance Horizon" (2026-07-01) — the C2PA structural-contradiction
  instrument this work extends into the dual-infrastructure case.
