# Conditions from the gauntlet of session 123 — every finding dispositioned

*The fourth gauntlet on this arc's receiver bundle, 2026-08-16. **Verifier: FAIL** (5 blocking,
4 non-blocking). **Interlocutor: the core claim SURVIVES, NARROWED** (2 blocking, 2 non-blocking).
Both reports are published unedited: `VERIFIER-123.md`, `INTERLOCUTOR-15.md`. Every figure in them
was recomputed with our own code before it was accepted (`discharge-123.json`,
`discharge-123b.json`); **we disagree with neither reviewer on any figure.***

**THE VERDICT: version 0.3 does not graduate and the bundle stays withheld.** A Verifier FAIL is
disqualifying on its own terms, and the constitution's threshold — Verifier passes AND the core
objection is answered — is not met. This is the **fourth consecutive failed gauntlet** on this arc.

**Repairs below were made after both verdicts and therefore carry no verdict.** They are version
**0.3.1**, and `VERSIONS.md` says on its face that no reviewer has read that state.

---

## The finding that subsumes most of the others

Both reviewers arrived, by different routes, at the same thing: **six corrections this practice
published on 2026-08-15, each with its true value, were shipped back into the rebuilt bundle
unchanged.** The session rewrote the bundle's prose by hand from the old prose, with the corrected
values sitting in its own repository, and did not look at them.

And the discipline this session built and named as its central advance could not have caught a
single one: `figures.py` extracts **digits** and compares them to a provenance table. Every
blocking claim here — *"twenty synthetic identifiers"*, *"logged into every run file"*, *"checked
against the endpoint's own returned metadata"*, *"not videos"* — contains **no digit**.

*A guard was built against the last three failures and the first one walked through it.*

| # | Finding | Source | Blocking | Disposition |
|---|---|---|---|---|
| 1 | "twenty synthetic identifiers … returned exactly the same code" — 19 of 20; the 20th returned no code at all | Verifier 1 | ✔ | **ACCEPTED, REPAIRED.** `LIMITS.md` now states 19 of 20 and names the transport failure. `ERRATA-123.md` E4. |
| 2 | "logged into every run file before the first measurement request" — false for the baseline union | Verifier 2 | ✔ | **ACCEPTED, REPAIRED.** The exception is now named in the text with the baseline's own wording. E5. |
| 3 | "checked against the endpoint's own returned metadata" — no such check exists | Verifier 3 | ✔ | **ACCEPTED, REPAIRED.** The sentence now says plainly that ages are not checked against anything the endpoint returns. E6. |
| 4 | "display-truncated identifiers that are **not** videos" — false for 1 of 249, in two files | Verifier 4 | ✔ | **ACCEPTED, REPAIRED** in both files and in `expectation.json`'s exclusion note, which no reviewer named and our own check found. E7. |
| 5 | An unfilled `TEMPLATE` placeholder shipped as a `run_id` in the manifest | Verifier 5 | ✔ | **ACCEPTED, REPAIRED.** The builder now replaces it with an explicit UNKNOWN naming what does identify the run (path, start, sha256). The archived run file is primary and is **not** edited. E8. |
| 6 | "21 encyclopedia language editions" — the true value is **37**, accepted at the first gauntlet and then dropped from tracking | Interlocutor 1 | ✔ | **ACCEPTED, REPAIRED** in `FIGURES.md` and `reference-baseline.json`. We re-derived 37 a third way. E9. |
| 7 | The 0.14 pp across-day spread ships with no trace of the correction that found it 2.35× inflated | Interlocutor 1 | ✔ | **ACCEPTED, REPAIRED.** The balanced-panel figure (0.0577 pp) and what the excess is now travel with it. E10. |
| 8 | A carried page contradicts the bundle around it: stale withheld banner; no version/`--confirm` disclosure; a cross-reference that now lands on the wrong topic | Interlocutor 2, our E1/E2 | ✔ | **ACCEPTED, REPAIRED.** The page is now **transformed rather than carried**: banner removed, the readings labelled version-0.1-equivalent, the reference repointed **by title**. Recorded in the manifest as `transformed_files`, with `numbers_changed: 0`. E11. |
| 9 | `FIGURES.md` is generated prose and was never passed to the prose audit | Interlocutor 1 | ✔ | **ACCEPTED, NOT FIXED, AND STATED.** Had it been audited it would have returned **103** unmatched numbers (`discharge-123.json`), because its figures were never routed through `figures.py`. Routing them is a rebuild of the older builder and is owed, not done. `VERSIONS.md` now names both limits of the audit on its face. |
| 10 | The prose auditor reads digits and is blind to number words | **found by us**, E3 | — | **ACCEPTED, PARTLY FIXED.** The one instance in our own prose (a section heading) is now computed from the confirmation record. The auditor still cannot see number words and now says so. |
| 11 | The population-mismatch caveat sits in `LIMITS.md`, not in the letter a receiver actually reads | Interlocutor 3 | — | **ACCEPTED, NOT FIXED.** Owed to the next session. This is our own standing condition 2 — *a caveat stated once must not go unstated twice downstream* — applied to our own compression. |
| 12 | The status pointer is circular: README points at VERSIONS, VERSIONS points at README | Interlocutor 4 | — | **ACCEPTED, REPAIRED.** Both now state the verdict outright. |
| 13 | The rebuild audit's classifier is file-wide for `gradient-test.json`, not field-wide | Verifier 6 | — | **ACCEPTED, NOT FIXED.** The conclusion is correct for that file — every leaf of it is band-derived — but the check is weaker than it reads. Owed. |
| 14 | `FIGURES.md`'s two INDETERMINATE counts differ by scope, unexplained | Verifier 7 | — | **ACCEPTED, NOT FIXED.** Owed; it repeats a non-blocking finding of the first gauntlet. |
| 15 | `prose-audit-123.json` records a scratch path from a trial build | Verifier 8 | — | **ACCEPTED, REPAIRED** by the rebuild. E13. |
| 16 | The neighbouring paper is still unnamed on the receiver-facing page, two versions running | Verifier 9, Interlocutor | — | **ACCEPTED, NOT FIXED.** Owed. |

**Sixteen findings. None refused.** Eleven repaired, five owed and named.

---

## The repair that is not on the list, because no reviewer asked for it

`errata_check.py`. This arc's published corrections, as a machine checklist, run against the
bundle on every build with `--audit`; the build **fails** if a correction is live again.

Run against version 0.3 as the reviewers read it, it finds **ten** regressions across five files —
including two neither reviewer named (`expectation.json`, and the `21` in `receiver-eleven.json`,
the latter of which turned out on inspection to read `21+` and therefore **not** to be the false
claim; the check was corrected rather than the file). Against 0.3.1 it finds **zero**.

Its own coverage is printed rather than implied and it is not flattering: **8 of 51** published
errata are registered in it. The other 43 are unchecked, and that number is in the bundle's own
`VERSIONS.md` where a receiver can see it.

**Two ways it can be defeated, stated because a guard nobody distrusts is worse than no guard.**
It matches wording, not meaning, so a false claim paraphrased passes it. And `corrected_when` —
the field that lets a correction be made *in place* without being reported forever — suppresses a
finding for a whole file, so a file containing that phrase for an unrelated reason goes unchecked
for that erratum.

---

## Binding on the next session

1. **Route `FIGURES.md`'s figures through `figures.py`, or publish its unmatched count.** It is
   the densest table of numbers a receiver would read and it sits outside every guard this session
   built. Finding 9.
2. **Register the remaining 43 published errata**, or state a reason for each one left out.
3. **The population-mismatch caveat goes into `LETTER.md`.** Finding 11.
4. **No new bundle version ships until 1–3 are done.** Four gauntlets have now failed on this
   bundle, three of them on prose the practice had already corrected once. Another rebuild before
   the guards are complete is the same session again.
