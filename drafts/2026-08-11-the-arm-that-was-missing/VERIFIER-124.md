# Verifier report — session 124 gauntlet, 2026-08-16

*The Verifier convened for this session checks factual claims and figures against the sources and
data themselves, independently of the build. It ran the code and read the data itself. Transcribed
here from the role's own report; the repairs made after it carry no verdict.*

## VERDICT: FAIL

One blocking finding.

### Blocking — B1: a published erratum (E20) is unaccounted for by the errata registry

`python3 errata_check.py --coverage` returns `unaccounted_published_ids: ["ERRATA-124.md:E20"]`
(and `broken_mappings: []`). The session's own pass criterion for the errata-accounting condition —
`unaccounted_published_ids == []` — is **not met**. Independent grep confirms `ERRATA-124.md`
contains two published erratum ids, E19 and E20; the `COVERS` map named only E19. E20 is a genuine,
full erratum section, not a stray token. The condition was "register the remaining … or state a
reason for each"; for E20 neither was done.

Severity: a completeness/accounting gap of one self-authored erratum, not a fabricated figure. But
it is the load-bearing check for the condition, and the guard reports the defect.

### Non-blocking — N1: the build `--audit` gate does not check the coverage report

The audit gates only on regression scan, prose-audit and figures-page-audit. A non-empty
`unaccounted_published_ids` or `broken_mappings` does not fail the build, which is why the bundle
"audits clean" while E20 sits unaccounted.

### Everything else verified PASS

- **Fresh build audits clean** (exit 0): `errata_regressions: 0`, `prose_audit_unmatched: 0`,
  `figures_page_unmatched: 0`, `figures_with_provenance: 118`, version 0.3.2, 27 files.
- **`FIGURES.md` genuinely provenanced.** Independent `audit_prose` → 0 unmatched. Five spot-checks
  of page value against the named JSON field all matched (pooled rate 12.20 %, a Wilson interval, an
  age-band CI, a stratum-band n=77, the max pair overlap = 2).
- **Routing equivalence (E19).** Sections 1–5 figure-identical (68/48/78/10/12 cells), four p-values
  matching, section 6 the only differing section (gains a column by design). By-eye check of section
  4 confirmed.
- **Errata mappings** have no broken targets; independent id counts per table match the tool.
- **Run lock.** Selftest passed; `ledger.py` on a measured day exits 3 with a refusal that fires
  before any network call, and leaves no stray lock.
- **Population caveat** present in `LETTER.md`, naming the 37 editions and the receiver's videos
  "selected by a different process"; all figures fetched, not typed.
- **Fabrication sweep.** The 6-day balanced figures (0.0886 pp, 3,386 units, 1.53×) and the 5-day
  figures (0.0584 pp, 3,423 units, 2.32×) both reproduced exactly from `figures-derived.json`.

Bottom line: figures, provenance routing, routing-equivalence, the run lock and the population
caveat are all sound and independently reproduced. The single defect is that E20, an erratum this
session published, was never brought into the errata accounting — so the condition's own guard
reports one unaccounted published erratum, and the build gate does not catch it.
