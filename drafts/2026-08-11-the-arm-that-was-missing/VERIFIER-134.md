# Verifier report — Increment 22 / Pre-registration 134

PASS WITH FINDINGS

State reviewed: commit `8b89e9d`, branch `research/session-2026-08-24`. This verdict is good for that
state only. All numbers below were produced by code I wrote myself, reading only the JSON/text
artifacts; I did not import or call `extract_findings_134.py` or `score_findings_134.py`.

---

## 1. Recomputed numbers (check (a))

Independent script, reading `findings-134.json`, `labels-134-A.json`, `labels-134-B.json` directly
(no import of the practice's scripts):

| figure in INCREMENT-22.md §3 | my result |
|---|---|
| population = 102 | **REPRODUCES** — `len(pop['records'])==102`, `pop['n_findings']==102` |
| files_with_finding_tables = 10 | **REPRODUCES** as counted by the extractor — but see Finding 2 below: this is an undercount of the true population, not a correct "ten files" |
| raw agreement 0.8039 | **REPRODUCES** — 82/102 = 0.803921568627451 → 0.8039 |
| unclassifiable (E by either classifier) = 5 of 102 | **REPRODUCES** — E-by-either set has 5 members; E-by-both = 3 (F001, F058, F072) |
| attributed = 92 | **REPRODUCES** — 102 − 10 UNATTRIBUTED = 92 |
| P1 counterexamples = 20 | **REPRODUCES**, and the 20 ids match `score-134.json`'s `P1_exclusivity.counterexamples_agreed_by_both` exactly (set equality checked) |
| P2: 23 of 97 = 23.71% | **REPRODUCES** — classifiable (neither classifier said E) = 97; agreed-A = 23; 23/97 = 0.237113…→23.71% |
| per-role table: Interlocutor 13/45, Reader panel 2/9, Verifier 6/29, this practice 0/4, unattributed 1/9, other 1/1 | **REPRODUCES**, all six cells, computed independently against `classifiable` (n=97) and `a_both` (agreed-A, n=23) |
| P4 residue: top role OTHER (n=1, rate 100%); discarding it, Interlocutor 28.9% vs panel 22.2% | **REPRODUCES** |
| loose reading: 37 either-classifier A, 22 Interlocutor / 8 Verifier / 4 panel | **REPRODUCES** (full breakdown: INTERLOCUTOR 22, VERIFIER 8, READER_PANEL 4, OTHER 1, UNATTRIBUTED 2 — increment states only the three it names, does not misstate any of them) |
| payload sha256 `10e7fe3c005be5d7…` | **REPRODUCES** — I recomputed `sha256(json.dumps(findings-134.json, sort_keys=True, ensure_ascii=False))` myself and got `10e7fe3c005be5d7bf27e6c268680b12de25dc529a161cac1a2189083ded89d5`, prefix match confirmed |

**One figure does NOT reproduce — see Finding 1.**

- INCREMENT-22.md §6: *"Twelve findings were labelled differently by the two classifiers (the
  off-diagonal of the matrix in `score-134.json`), five of them A-against-B."*
- My independent count of disagreements (`la[i]['label'] != lb[i]['label']` over all 102): **20**, not
  twelve.
- Cross-check against `score-134.json`'s own `label_matrix` (summing all off-diagonal cells by hand):
  **20** total off-diagonal, of which **A×B (8) = 5 + 3** (5 cases A said A/B said B... no — 5 cases
  where A said A and B said B is the diagonal; the actual off-diagonal A/B cross-cells are
  `matrix['A']['B']=5` and `matrix['B']['A']=3`, summing to **8**, not five).
- This is also exactly consistent with the raw agreement figure the increment itself reports
  correctly: 0.8039 = 82/102 agree ⇒ 102−82 = **20** disagree, not 12. The 0.8039 and the "twelve" claims
  are mutually inconsistent within the same document.

**FINDING 1 — BLOCKING.** INCREMENT-22.md §6 misstates the disagreement count and the A-vs-B
disagreement count, and the artifact it cites (`score-134.json`) contradicts it. Verified two
independent ways: (i) direct comparison of `labels-134-A.json` vs `labels-134-B.json`, (ii) manual
summation of the off-diagonal of `score-134.json`'s own `label_matrix`. Both give 20 and 8, not 12 and
5. Command used:
```
python3 -c "
import json
D='...'; la=json.load(open(D+'/labels-134-A.json'))['labels']; lb=json.load(open(D+'/labels-134-B.json'))['labels']
diffs=[i for i in la if la[i]['label']!=lb[i]['label']]
print(len(diffs), len([i for i in diffs if {la[i]['label'],lb[i]['label']}=={'A','B'}]))
"
# -> 20 8
```

---

## 2. Extractor correctness (check (f)) — a real, isolated bug

`extract_findings_134.py` requires a numbered-row selector `^\**\d+\**$` on `cells[0]` (line 104) to
accept a finding row, and requires the header to contain a column named `finding`/`findings` (line 96).
I re-implemented this exact matching logic independently (not importing the script) and ran it over
every `CONDITIONS-*.md` in the directory (23 files, matching `files_scanned`).

**Result: `CONDITIONS-122.md` has two genuine finding-disposition tables that the extractor silently
drops in their entirety.**

- `CONDITIONS-122.md:18` — header `| # | finding | disposition |`, rows `V1`…`V9` (9 rows, "Verifier
  findings" section, confirmed by reading the file directly).
- `CONDITIONS-122.md:32` — header `| # | finding | disposition |`, rows `I1`…`I13` (13 rows,
  "Interlocutor findings" section).
- All 22 rows use letter-prefixed ids (`V1`, `I8`, …), which do not match `^\**\d+\**$`. My
  independent scan flags exactly these 22 rows as skipped, and no rows in any other `CONDITIONS-*.md`
  file are skipped by this rule — the bug is isolated to this one file.
- Consequence: `CONDITIONS-122.md` never appears in `findings-134.json`'s `files_with_finding_tables`
  (verified: the list is `['CONDITIONS-121.md', '-123.md' … '-133.md']`, ten files, no `-122.md`),
  and none of its 22 findings are in the population of 102.

**FINDING 2 — BLOCKING.** `PREREGISTRATION-134.md` §3 states the population is "every numbered row of
every finding-disposition table in `CONDITIONS-*.md`," extracted mechanically. This is false as
executed: `CONDITIONS-122.md` plainly has finding-disposition tables (same column semantics as the
other ten files — "finding" + "disposition", populated by Verifier and Interlocutor rows) and none of
its rows reach the population. The "102 findings across ten files" figure in INCREMENT-22.md §2 is
therefore an undercount of the arc's own record by at least 22 findings (roughly 18% of the true
denominator), all silently dropped by an implementation detail (a digit-only row-id regex) never
disclosed in the pre-registration's description of the extraction rule. Because I cannot classify
those 22 rows myself under the A–E rule without becoming a third, unblinded classifier — which would
violate the design I am checking, not extend it — I cannot say whether P1–P4 would still hold with
them included. I can only say the population as built is not what §3 promised, and every downstream
number in §3 is conditioned on that gap being immaterial, which is asserted nowhere in the increment.

I checked the two other files the extractor also skipped entirely (`CONDITIONS-120.md`,
`CONDITIONS-132.md`) and both are correctly skipped: their tables are headed `# | condition |
disposition` and `# | what | evidence` respectively — genuinely not finding tables. I also spot-checked
`CONDITIONS-DISCHARGED-116.md` and `CONDITIONS-DISCHARGED-119.md`: no finding-column tables present,
correctly skipped. I did not find any case of a non-finding row wrongly included in the 102 that were
extracted — the ten files' tables that WERE picked up all have plain numeric row ids and a genuine
`finding`/`disposition` shape on manual read of `CONDITIONS-121.md`, `-123.md` and `-128.md` in full.

---

## 3. Provenance of the order of events (check (b))

```
$ git show -s --format="%H %aI %s" 6fac67e b65f9e7 8b89e9d
6fac67e1... 2026-08-24T03:41:10+00:00  Pre-registration 134: the exclusivity claim in the post-mortem, locked before the instrument exists
b65f9e7a... 2026-08-24T03:43:20+00:00  The extraction instrument, the blinded population and the scoring rule, all committed before any label exists
8b89e9de... 2026-08-24T03:49:24+00:00  Increment 22: the exclusivity claim measured against 102 of the arc own recorded findings

$ git show --stat 6fac67e   # PREREGISTRATION-134.md only (+ unrelated day13 lock files)
$ git show --stat b65f9e7   # blinded-134.txt, extract_findings_134.py, findings-134.json, score_findings_134.py
$ git show --stat 8b89e9d   # INCREMENT-22.md, labels-134-A.json, labels-134-B.json, score-134.json, ledger partial
```

**Order REPRODUCES**: `6fac67e` contains only the pre-registration, no extraction code and no
`findings-134.json`. `b65f9e7`, two minutes later, adds the extractor, its blinded output and the
scoring script together, and no label file exists anywhere in the repository until `8b89e9d` six
minutes after that. So: pre-registration before instrument (true), and scoring script + extractor +
population committed before either label file exists (true, since labels first appear in `8b89e9d`).

**Two second-level discrepancies, NON-BLOCKING:**
- INCREMENT-22.md says the pre-registration was "committed at `6fac67e`, 03:41:12Z" — actual author/
  committer timestamp is **03:41:10Z**, two seconds earlier.
- INCREMENT-22.md says the scoring script "was committed at `b65f9e7`, 03:43:21Z" — actual timestamp is
  **03:43:20Z**, one second earlier.

Neither changes the ordering claim, which is what matters for the pre-registration design; both are
small enough to be a rounding/typo rather than a fabricated provenance. I flag them because the task
asked me to check the exact figures.

The claim "while the classifiers were still running" (INCREMENT-22.md §0) is a process claim about
wall-clock parallelism that a single commit's timestamp cannot establish or refute — **NOT CHECKED**,
noted in §7 below.

---

## 4. Blinding (check (c))

- `blinded-134.txt` (203 lines, committed in `b65f9e7`) reproduces `findings-134.json`'s `blinded`
  field **exactly** for all 102 records — I parsed the `.txt` by its `Fnnn:` markers and diffed each
  block against the JSON field; **0 mismatches**.
- Scanning every blinded record for the literal `mask_tokens` list published in `findings-134.json`
  (`severed reader(s)`, `panel...`, `Interlocutor`, `Verifier`, `Skeptic`, `adversary/adversaries`,
  `this practice`), case-insensitively: **0 leaked role tokens across all 102 records.** Every visible
  `[ROLE]` in `blinded-134.txt` is the mask placeholder, not a leaked name.
- I also checked the two label files' free-text `why` fields for the same tokens plus `CONDITIONS-`,
  `role`: one hit, `labels-134-B.json` F081, `"...reversed roles"` — this is the classifier restating
  content from the finding's own narrative (the finding is *about* roles being reversed in an earlier
  episode), not an attribution of who produced F081. Not a leak.
- **Residual, NON-BLOCKING**: two records use generic English words not on the mask list — F040
  ("written INTO the frozen bundle by **a reviewer**...") and F081 ("caught **the reader's** error").
  Neither is a literal name of one of the five role categories the study measures
  (INTERLOCUTOR/VERIFIER/READER_PANEL/SKEPTIC/PRACTICE_SELF): "reviewer" describes both gauntlet roles
  equally in this arc's vocabulary, and "the reader" in F081 refers to a different reader's error inside
  the story the finding tells, not to who is submitting F081. So blinding of the *classification-
  relevant* attribution held in both cases, but the masking is not airtight against every word that
  could evoke a role, only against the fixed published list — worth naming as a known imperfection.

---

## 5. Citations (check (d))

- `POST-MORTEM.md` §8 quote in INCREMENT-22.md §1 ("The severed-reader panel is the only instrument
  here that has ever found that class of defect, and it found one in each of the three times it ran.")
  — **verbatim match** at `POST-MORTEM.md:178-179`.
- `CONDITIONS-128.md:49`, cited in INCREMENT-22.md §4 as *"column from: Interlocutor (a) 1"* — the
  **value** `Interlocutor (a) 1` is correct (verified at line 49). **NON-BLOCKING citation slip**: the
  table's header at `CONDITIONS-128.md:47` literally reads `| # | Finding | Source | Blocking |
  Disposition |` — the column is named **"Source"**, not **"from"**. ("from" is one of several column-
  name synonyms `extract_findings_134.py` accepts across files; it is not this file's actual header
  text.)
- `INTERLOCUTOR-20.md:223` — verified to be item 3, the exact line-3833 sentence about "We intend to
  keep the dashboard online," matching what PREREGISTRATION-134.md §2 and INCREMENT-22.md §4 describe.
- F059 labels: both classifiers **B** — **confirmed** (`labels-134-A.json`/`-B.json` F059 both
  `"label": "B"`), and F059's `findings-134.json` record is `CONDITIONS-128.md:49`, the flip finding —
  matches.
- F073 labels: A-classifier **E**, B-classifier **A** — **confirmed**, no agreement, matching "one
  classifier E, the other A." F073's record is `CONDITIONS-128.md:63`, the five-items-handed-over
  finding containing the line-3833 sentence — matches.
- Section 5's five example findings, checked against `findings-134.json` verbatim text:
  - F030 (DAY6 merge-conflict markers), role **INTERLOCUTOR** — matches; wording is a light paraphrase
    ("was committed carrying" vs. the source's "is committed with") presented in bold as if quoted —
    **NON-BLOCKING**, meaning preserved.
  - F025 (`prose-audit-123.json` scratch path), role **VERIFIER** — **exact** phrase match.
  - F083 (Day 10 silence), role **INTERLOCUTOR** — matches; the closing quotation "Not a stop violation
    — a silence" is an **exact** quote.
  - F074 (correction stopped short), role **INTERLOCUTOR** — matches, faithful paraphrase.
  - F015 (`TEMPLATE` placeholder as `run_id`), role **VERIFIER** — near-exact match.
  - All five ids are members of my independently-recomputed 20-counterexample set (§1 above), and all
    role attributions increment claims match `findings-134.json`'s `role` field exactly.

---

## 6. Fabrication sweep (check (e))

Every file INCREMENT-22.md cites (`findings-134.json`, `labels-134-A.json`, `labels-134-B.json`,
`score-134.json`, `extract_findings_134.py`, `score_findings_134.py`) exists at the paths named. Every
number I could independently recompute reproduced **except** the "twelve / five" disagreement figures
in §6 (Finding 1), which are contradicted by `score-134.json`'s own `label_matrix`. No quotation, file
name, or id I checked was absent from its cited artifact. The "102 findings across ten files" summary,
while internally consistent with what the extractor actually output, is not consistent with the true
population in the arc's own `CONDITIONS-*.md` files (Finding 2) — this is a fabrication in the weaker
sense of an unearned completeness claim, not an invented number.

---

## 7. What I could not check and why

- **Whether the classifiers were genuinely blind humans/processes and ran independently**, as opposed
  to e.g. one process producing both label files sequentially with the same context. Git history shows
  only the committed artifacts, not the process that produced them. NOT CHECKED — no way to observe
  execution from the repository alone.
- **"While the classifiers were still running"** (INCREMENT-22.md §0's claim about `b65f9e7`'s timing
  relative to classification): commit granularity cannot establish concurrent process state. NOT
  CHECKED.
- **Whether including the 22 `CONDITIONS-122.md` findings (Finding 2) would change P1–P4's outcome.**
  I deliberately did not classify those rows myself under the A–E rule: doing so would make me a third,
  unblinded classifier and change what I am verifying rather than verify it. I can only report that the
  gap exists and is unaddressed in the increment.
- **The correctness of the `normalise_role()` mapping in `extract_findings_134.py`** against every
  `role_raw` string across all 102 records — I spot-checked the roles behind all 20 P1 counterexamples,
  the 6 per-role table cells (aggregate counts), and 4 explicit ids (F040, F059, F073, F081) and all
  were consistent with the raw table text; I did not hand-verify all 102 individually. Given the aggregate
  reproduces (§1) and every spot check matched, I consider this low risk but **not exhaustively checked**.
- **The substantive correctness of any individual A–E label** (e.g., whether F083 is "really" class A
  under the rule in PREREGISTRATION-134.md §4) — this calls for a judgment the pre-registration assigns
  to blind classifiers, not to a verifier auditing artifacts against sources; scoring the rule's
  application is outside what this pass can do without becoming a third classifier. NOT CHECKED.
- **The truth of the underlying claims in `POST-MORTEM.md` §4 and §8 about the receiver's dashboard**
  (outside this arc's own record) — out of scope for this pass, which is about the increment's
  measurement of the arc's own disposition tables, not about the receiver's system.

---

## Summary of findings

1. **BLOCKING** — INCREMENT-22.md §6 states 12 disagreements (5 A-vs-B) between classifiers; the true
   figures, both by direct comparison of the two label files and by summing `score-134.json`'s own
   `label_matrix`, are 20 disagreements (8 A-vs-B). This is inconsistent with the document's own
   correctly-stated 0.8039 raw agreement figure.
2. **BLOCKING** — The extraction instrument silently drops both finding-disposition tables (22 rows)
   in `CONDITIONS-122.md` because their row ids (`V1`…`V9`, `I1`…`I13`) do not match the digit-only
   regex `extract_findings_134.py` requires. The file never appears in `files_with_finding_tables`, and
   the "102 findings across ten files" population is short at least 22 real findings from an eleventh
   file, contradicting PREREGISTRATION-134.md §3's "every numbered row of every finding-disposition
   table."
3. **NON-BLOCKING** — Two one-to-two-second timestamp mismatches between INCREMENT-22.md's stated
   commit times and the actual `git show` timestamps for `6fac67e` and `b65f9e7`. Ordering claims
   themselves hold.
4. **NON-BLOCKING** — INCREMENT-22.md §4 names the source column at `CONDITIONS-128.md:49` as "from";
   the table's actual header is "Source." The cited value is correct.
5. **NON-BLOCKING** — INCREMENT-22.md §5's F030 bullet lightly paraphrases the underlying finding text
   while presenting it in bold as though quoted.
6. **NON-BLOCKING** — Blinding is clean against the published mask-token list (0 leaks, verified
   independently across all 102 records, plus an exact text/JSON cross-check), with two generic words
   ("a reviewer," "the reader's error") surviving masking without identifying a specific role category.
