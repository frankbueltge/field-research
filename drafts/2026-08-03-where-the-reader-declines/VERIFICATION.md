# Verifier — Where the Reader Declines

**Run:** 2026-08-03, against the draft state of that date.
**Method:** every headline figure recomputed **from the runtime's source files**
by code written for this check — `data.json` and `build_data.py` were not read,
so a defect in the builder cannot pass through into the verification.
**Verdict: PASS WITH FINDINGS.** Two findings, both non-blocking, both applied.

---

## Recomputed, independently

| | claim in the work | recomputed | |
|---|---|---|---|
| V1 | agreement 54.4 % | 31/57 = 0.5439 | ✔ |
| V2 | majority-class floor 42.1 % | 24/57 = 0.4211 | ✔ |
| V3 | blind reader declared 3 undecidable | 3 | ✔ |
| V4 | machine declared 0 undecidable | 0 | ✔ |
| V5 | machine chose contextualizes 43 of 60 | 43 | ✔ |
| V7 | in-population n = 39 | 39 | ✔ |
| V8 | blind reader in-population: 1/6/17/14/1 | supports 1, contradicts 6, qualifies 17, contextualizes 14, undecidable 1 | ✔ |
| V9 | machine in-population: 1/2/4/32/0 | supports 1, contradicts 2, qualifies 4, contextualizes 32, undecidable 0 | ✔ |
| V10 | "32 of 39 (82 %)" | 0.821 | ✔ |
| V11 | 7 contradictions land in contextualizes | 7 | ✔ |
| V12 | 15 qualifications land in contextualizes | 15 | ✔ |

## Integrity of the material

**V6 — every excerpt hash recomputed against its own text: 60 of 60 match.**
This is the check that matters most: it establishes that the sixty texts the
blind reader saw are byte-identical to the sixty this work publishes. A drifted
excerpt would make every verdict beside it a statement about a different
document.

The four source files are named with their sha256 in the work's own footer, and
those hashes were recomputed here from the files on disk.

## No fabricated data

Every figure on the page is computed in the component's frontmatter from
`data.json`. No number is typed into prose in the work. Checked by reading
`work.astro`: the only literals are category names, and the two derived values
`accuracy` and `floor` are computed, not asserted.

`build_data.py` performs no network access, reads no clock, and constructs no
model. Re-running it produced a byte-identical `data.json`.

---

## F1 (finding, applied) — one number *was* typed into prose

`FINDINGS.md` stated *"measured elsewhere at roughly a quarter of a paper's own
checkable claims"* with no source in the work. It traces to the runtime's N2-T03
derivation ("roughly 28 percent of this corpus's numeric-token claims"), which
is a **different corpus** — that derivation's own citation corpus, not these
sixty abstracts.

**Applied:** the claim is now marked as what it is — an order-of-magnitude
figure from an adjacent measurement on a different corpus, not a property of
this material. It is not a claim about these sixty and must not be read as one.

## F2 (finding, applied) — the second run's score was carried, not recomputed

The work states that a second run over identical frozen inputs scored 52.6 %.
That figure was taken from a commit on an unmerged branch of the runtime
(`cc6df74`) rather than recomputed here, and **it is not on the runtime's
`main`** — a reader following the provenance list will not find it.

**Applied:** the sentence now names the figure as coming from a run whose
artefact is not on the default branch, so the reader is not sent looking for a
file that is not there. The variance claim ("differences under ~2 points are
noise") rests on it and inherits that weakness.

---

## Not verified

- **The population split.** It is a human judgement, not a computation; the
  Verifier can confirm the arithmetic *given* the list (V7–V10) but cannot
  confirm the list. That is the Skeptic's S4, not a verification item.
- **The rationales.** Both readers' one-sentence reasons are reproduced
  verbatim from their sources; whether a rationale is *good* is not a
  verification question.
