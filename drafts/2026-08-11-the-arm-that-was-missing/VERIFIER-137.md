# Verifier 137 — published unedited

**VERDICT: PASS WITH FINDINGS**

Every reproducible claim in `HAND-AUDIT-137.md` that I could recompute from the primary files —
both draws, both extractor runs, all three sha256 hashes, the population-wide diagnostic, the
withdrawn-rule figures, and nine of the ten hand counts — reproduced exactly. The kill-condition
outcome (K4 fired on 3 of 5, K4′ passed on 4 of 5) is not overturned by my recount; if anything a
probability check below makes the "it was luck" framing *more* defensible than the document states
it. But going past what the document asked me to check, I found a real, undisclosed defect in the
very extractor (`extract_units_137_v2.py`) the document ships as the "repair for a later session":
its `LABELLED` family miscarves `VERIFIER-120.md` in a new way, on the same file its own docstring
names as the motivating case, and this sits inside the frozen, hash-pinned dataset
`units-137-v2.json` that `PREREGISTRATION-137B.md` locks for future classification without anyone
re-running the population-wide check that would have caught it. That is BLOCKING for the frozen
artifact's stated fitness, though it does **not** change the document's own verdict (no rate is
published either way).

---

## Findings

**1. BLOCKING — `extract_units_137_v2.py`'s `LABELLED` family still miscarves `VERIFIER-120.md`, the exact file its repair was aimed at, and this sits undetected in the frozen v2 dataset.**

`VERIFIER-120.md`'s true finding count, established by hand from the primary file and confirmed by
both hand audits in this repository (`HAND-AUDIT-137.md` §1, `carve-audit-137.json`), is **18**
(`### F1.` … `### F18.`). I called `extract_units_137_v2.pick_family` and `split_on` directly on the
file's own text:

```
family=LABELLED, count=28
```

The extra ten come from the report's own `### F0-a.` … `### F0-j.` subsections — the "what
reproduced, exactly" recomputation table, not findings at all — which the `LABELLED` regex
(`^#{2,4} *(?:Claim +)?[A-Z]{1,2}\d+[.):\s—-]`) cannot distinguish from `### F1.`. This is the same
species of defect the v2 docstring diagnoses in `VERIFIER-127.md` (a plausible-looking family that is
not the report's findings) — on the file v2's own docstring names first as what it fixed. The
extractor was not checked against this file after the fix because `PREREGISTRATION-137B.md` K4′
explicitly and correctly excludes v1's five audited files from the fresh gate (so tuning against them
would be circular) — but nothing in the session's process re-ran the *population-wide* diagnostic
(`carve_audit_137.py`) against v2's output the way it was run against v1's, so this defect was never
surfaced. It is present right now in `units-manifest-137-v2.json`, sha256-pinned and locked for reuse:
`VERIFIER-120.md` contributes 28 pseudo-units to the "483 units from 51 of 53 files" figure, ten of
which are not findings and were never labelled N at extraction (only classification excludes N units,
per §4, and a classifier will see them as ordinary units to label). I did not find this same
`F0`-style conflation anywhere else in the 53-file population (checked directly, see below), so it is
localized — but it is real, it is inside the frozen population, and no document in this session's
output discloses it.

**2. NON-BLOCKING — `carve_audit_137.py`'s self-validation is only partly falsifiable, and this is not disclosed.**

The script's `HAND` dictionary hardcodes the five hand-audit verdicts (AGREE/DISAGREE) as constants
written by this session, not independently re-derived by the script. For `INTERLOCUTOR-18.md`, the
predicted verdict is `"DISAGREE" if row["flag"] != "CLEAR" else "AGREE"`, and `UNEXTRACTABLE` always
satisfies `flag != CLEAR` by construction — so the check for that one row will read `True` regardless
of what number is written into `HAND["./INTERLOCUTOR-18.md"]["hand"]`; it is testing only that the
manifest still reports the file `UNEXTRACTABLE`, not that "4" is the right hand count. For the other
four rows the check is genuinely falsifiable (it depends on the real count of `LABELLED`-style
headings against the real script unit count), so the assertion is not wholly tautological — but the
"ground truth" it validates against is this session's own transcription of its own hand audit, not an
independent re-derivation from the files. **The self-assertion could pass even if the underlying hand
count in `HAND-AUDIT-137.md` were wrong**, because the script never re-opens the five files itself to
check the hand numbers; it only checks that the diagnostic's CLEAR/MIS-CARVED/UNEXTRACTABLE flag is
consistent with a verdict string copied from the document under review. In this instance I confirmed
independently (by reading all five files myself) that the transcribed hand counts are in fact
correct, so the practical consequence is nil — but the limitation is real and stated nowhere in the
script or in `HAND-AUDIT-137.md` §2's description of "validation."

**3. NON-BLOCKING — `INTERLOCUTOR-18.md`'s hand count of 4 is not independently reproducible from the stated criterion alone.**

`HAND-AUDIT-137.md` §1 states its criterion as "the items the report presents as its own findings."
`INTERLOCUTOR-18.md` contains no numbered findings anywhere except a single formal list, **"Blocking
objections (1):"**, with exactly one item — which on a literal reading of that criterion gives a hand
count of **1**, not 4. I could reconstruct 4 only by adopting a different, undisclosed rule: counting
the file's four `###`-level headings (`What I re-verified rather than re-derive from scratch`, `Was
the new material honest, specifically`, `The new attack that succeeded`, `Verdict`) as the unit of
enumeration — a rule that is never stated in either `PREREGISTRATION-137.md` §4 or `HAND-AUDIT-137.md`
§1 as the criterion for headless reports. Under either reading the verdict is the same
(**DISAGREE** — v1's script returned 0), so **this does not change K4's outcome**, but the specific
figure "4" is not something a second person could re-derive from the stated method without guessing
the same undisclosed tie-break I did.

**4. NON-BLOCKING — two different counting criteria are used for the two halves, and the document never checks whether that choice affects the result.**

`HAND-AUDIT-137.md` §1 uses "the items the report presents as its own findings" for v1's five files;
§3 states a criterion was "tightened" before the v2 gate and gives a different, more specific rule
("the number of items in the report's own primary enumeration ... counted end to end"). The document
never re-applies the tightened §3 rule to v1's five to check whether K4's 3-of-5 disagreement is an
artifact of the looser criterion. I did this spot-check myself for the two clearest cases
(`VERIFIER-122.md`, `INTERLOCUTOR-129.md`) and both give the same count under either reading, so
nothing here suggests the K4 result is criterion-dependent — but the document asserts this implicitly
rather than checking it.

---

## What reproduced exactly

- **Both draws.** `random.Random(1370).sample(sorted(pool_of_53), 5)` — with the pool built exactly
  as `extract_units_137.py`'s own file-discovery loop builds it (`./NAME.md` and
  `../2026-08-26-cited-not-retrievable/NAME.md`, `INTERLOCUTOR-*`/`VERIFIER-*`/`READER-*`, `READERS-*`
  excluded) — reproduces `VERIFIER-122.md, VERIFIER-120.md, INTERLOCUTOR-18.md, INTERLOCUTOR-129.md,
  INTERLOCUTOR-7.md` exactly, in that order. `random.Random(1372).sample(sorted(pool_of_53_minus_the_five), 5)`
  reproduces `VERIFIER-133.md, INTERLOCUTOR-13.md, VERIFIER-129.md, INTERLOCUTOR-2.md, VERIFIER-127.md`
  exactly. Both draws were selected, not chosen: they reproduce only under this exact pool
  construction (relative paths with the `./` prefix; a bare-filename pool gives a completely
  different five for both seeds, and applying seed 1372 to the full 53 rather than the 48 remaining
  also gives a different, wrong five that includes v1's own files).
- **Both extractions, byte-for-byte.** Running `extract_units_137.py` and `extract_units_137_v2.py`
  fresh against the same two directories reproduces `units-manifest-137.json` and
  `units-manifest-137-v2.json` field for field (files/extracted/units/truncated/by-role, both
  extractors), and reproduces the committed `units-137-v2.json` byte-for-byte.
- **All three sha256 hashes in `HAND-AUDIT-137.md` §4 / `PREREGISTRATION-137B.md` §1.**
  `units-137-v2.json` → `c1e77b438766ade5dc0afd9a90624f8e641ece49b6ac9e3f55d94a5ca0af2495`;
  `units-manifest-137-v2.json` → `1cf09185e996caa92d4f28311d806fa5fa3c2ea9f50988fda05144400fc56ab4`;
  `extract_units_137_v2.py` → `7f1a73c648e63bf5c3aa4d487fb0b24f9b86275a25e7e3317cb18d32ba7049c6`. All
  three match the committed files exactly.
- **`carve_audit_137.py`.** Re-run against `units-manifest-137.json`, it reproduces
  `carve-audit-137.json` byte-for-byte (dict-equal), exits 0, and its internal
  `diagnostic_reproduces_hand_audit` assertion is `true`. The 44/3/6 counts, the 27-of-436 figure, the
  per-role breakdown (interlocutor 21/2/3, reader 11/0/0, verifier 12/1/3), and "no reader file is
  flagged" all check out directly against the JSON.
- **The three MIS-CARVED files.** `INTERLOCUTOR-5.md`, `INTERLOCUTOR-7.md`, `VERIFIER-120.md` — and
  two of those three (`INTERLOCUTOR-7.md`, `VERIFIER-120.md`) are indeed in the five-file sample drawn
  under seed 1370, confirming "two of those three were in this sample of five" exactly.
- **The withdrawn `subsplit()` figures.** Calling `pick_family` + `split_on` + `subsplit` on
  `VERIFIER-122.md` gives 9 units before, 15 after — matches. On `VERIFIER-120.md`: 28 units before
  (see Finding 1 for why 28, not 18, is itself already wrong), 44 units after — matches the docstring's
  "28 to 44" exactly. `subsplit` is defined once and never called anywhere in `main()`; grep confirms
  it appears nowhere else in the file. Genuinely unreferenced, as claimed.
- **Nine of ten hand counts**, checked by opening the file and counting under the criterion the
  document itself states for that file:

  | file | claimed hand | claimed script | claimed verdict | my count | my verdict |
  |---|---|---|---|---|---|
  | `VERIFIER-122.md` | 9 | 9 | AGREE | 9 (Findings 1–9) | confirmed |
  | `VERIFIER-120.md` | 18 | 16 | DISAGREE | 18 (`### F1.`–`### F18.`) | confirmed |
  | `INTERLOCUTOR-18.md` | 4 | 0 | DISAGREE | 1 under §1's literal rule, 4 under a `###`-heading rule (see Finding 3) | DISAGREE confirmed either way; exact figure not independently forced |
  | `INTERLOCUTOR-129.md` | 6 | 6 | AGREE | 6 (numbered 1–6 across "Blocking"/"Non-blocking") | confirmed |
  | `INTERLOCUTOR-7.md` | 12 | 6 | DISAGREE | 12 (Claims C1–C7 = 7, plus §3.1–3.5 = 5) | confirmed |
  | `VERIFIER-133.md` | 4 | 4 | AGREE | 4 (Findings, blocking 1–2 + non-blocking 3–4) | confirmed |
  | `INTERLOCUTOR-13.md` | 9 | 9 | AGREE | 9 (`### 1.`–`### 9.`) | confirmed |
  | `VERIFIER-129.md` | 6 | 6 | AGREE | 6 (Blocking 1–4 + Non-blocking 1–2) | confirmed |
  | `INTERLOCUTOR-2.md` | 18 | 18 | AGREE | 18 (`### 1.`–`### 18.`) | confirmed |
  | `VERIFIER-127.md` | 9 | 14 | DISAGREE | 9 (the Findings table's 9 rows); v2's 14 = the 14 bold lead-ins of "What I recomputed and it was right" | confirmed, including the specific failure mechanism |

  **Neither audit's outcome changes.** v1: 3 of 5 disagree (`VERIFIER-120`, `INTERLOCUTOR-18`,
  `INTERLOCUTOR-7`) — K4 fires, exactly as claimed. v2: 4 of 5 agree, only `VERIFIER-127.md`
  disagrees — K4′ passes at the threshold, exactly as claimed.
- **The population and word counts.** 25 `INTERLOCUTOR-*.md` + 15 `VERIFIER-*.md` + 11 `READER-*.md`
  in this directory, plus `INTERLOCUTOR-136.md` + `VERIFIER-136.md` in
  `drafts/2026-08-26-cited-not-retrievable/` = 53 files. Summed word counts: 140,023 + 10,459 =
  **150,482**, matching `PREREGISTRATION-137.md` §3 exactly.
- **Cross-repository quotations spot-checked.** `downstream-commitments.md` condition 37(b) — "NO RATE
  COMPARISON MAY BE QUOTED FROM THIS PRACTICE ON THIS QUESTION" and "a rate over that population
  measures the bookkeeping" — verbatim. Condition 33(d) ("the population is hand-made and has no
  second reader") and condition 9(b) (instrument 021's population split, "a disclosed, case-by-case
  human judgement with no second reader") both verified as the sessions HAND-AUDIT-137.md §4 says they
  are. `CONDITIONS-136.md` item 11's "third session running that naming it is not doing it" and "the
  classification population that cannot see what the disposition tables do not table" are verbatim
  (found in `drafts/2026-08-26-cited-not-retrievable/CONDITIONS-136.md`, not in this directory — the
  cross-reference resolves correctly across directories). `READERS-127.md:110–115`'s general claim
  (a severed reader's finding filing under an Interlocutor-only row) is corroborated in substance by
  the surrounding text, though the exact disposition-table mechanics are not re-verified here.
- **A quantitative sanity check on "it was luck."** Using the population-wide diagnostic's own lower
  bound of 9 mis-carved-or-unextractable files out of 53, the hypergeometric probability of drawing 3
  or more such files in a random sample of 5 is **≈3.0%**, meaning roughly 97% of possible seeds would
  *not* have fired K4 under this diagnostic's own floor (and the true miscarry rate may be higher, per
  the document's own "may be higher" caveat, which would only strengthen this). This supports the
  document's "a different seed very probably passes K4" claim quantitatively rather than just
  rhetorically.

## What I could not check, and why

- **Whether `INTERLOCUTOR-18.md`'s hand count is "correct" in any objective sense.** The file has no
  numbering at all outside one one-item list; "4" depends on treating unlabelled `###` headings as the
  unit of enumeration, a choice the stated criteria do not make explicit. I can confirm the DISAGREE
  verdict is robust to this ambiguity, not that 4 is uniquely forced by the method as written.
- **The full text of `READERS-127.md` lines 110–115** and the exact wording of `CONDITIONS-127.md`
  finding 8 that `downstream-commitments.md` cites alongside it — I read the surrounding paragraph of
  `READERS-127.md` and the claim is consistent with it, but I did not independently re-derive the
  disposition-table mechanics that produced "files under an Interlocutor-only row," since that
  question belongs to session 134's population, not to this session's extraction or hand audit.
- **Whether the `F0-`-style conflation (Finding 1) recurs in files outside this population** (the
  277,386-word review record `PREREGISTRATION-137.md` explicitly puts out of scope). I checked only
  the 53 in-population files and found it in exactly one (`VERIFIER-120.md`).
- **The provenance of the 9-mis-carved-file floor as a rate** — I used it only for the probability
  sanity check above; the document's own caveat that it is "a lower bound, not a measurement" stands,
  and I did not attempt to establish a tighter true rate.
