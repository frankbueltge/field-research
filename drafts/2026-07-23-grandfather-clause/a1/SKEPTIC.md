# Skeptic — the refutation attempt on anchor A1, and what it changed

*Convened collective session 80, 2026-08-02, against the committed state `80edc46`, with instructions
to attack eight named claims and to point at a specific file, line or number for every objection. It
re-read the specimen bytes with the pinned library, re-derived the numbers, checked the git
timestamps, and read Articles 3(9) and 3(11) of the AI Act on its own initiative. **Six blocking
conditions were returned; all six are applied.** This file records the verdict and the disposition.*

## Verdict, per claim

| | Claim attacked | Verdict |
|---|---|---|
| K1 | The pre-registered order was followed | **SURVIVES WITH CONDITIONS** — the order is real in the git log, but the commits are minutes apart, so the order proves where things landed, not blindness to content |
| K2 | Nothing was re-cut to fit the result | **SURVIVES NARROWED** — the outcome survives; two pieces of post-hoc discretion in the *justification* do not |
| K3 | The guidance still calls the law a proposal | **SURVIVES WITH CONDITIONS** — the text is verbatim; "knowingly left inconsistent" is not licensed by a page-level update stamp |
| K4 | The enacted text is narrower than the guidance | **SURVIVES** — Art. 3(9) and 3(11) are genuinely different triggers, and the same Regulation uses the fuller phrase elsewhere |
| K5 | "The public surface … was mostly closed" | **REFUTED AS WRITTEN; SURVIVES NARROWED** |
| K6 | D1 is a defect in the pre-registration | **SURVIVES NARROWED** — and D1 missed a further problem of its own |
| K7 | s04 predates the seam by ~8.5 months | **SURVIVES NARROWED** — the library flags the timestamp authority as untrusted |
| K8 | Anything else | numbers reconcile; four further defects found |

**Its core objection, verbatim:** *"The anchor's single most quotable line … is a description of one
under-10-minute, single-attempt, plain-HTTP, single-network-egress capture session dressed up as a
finding about the world. The git timestamps that make this anchor's pre-registration discipline
verifiable (K1) are the same timestamps that undercut its rhetorical conclusion (K5)."*

## Disposition of the six blocking conditions — all applied

1. **Narrow the "mostly closed" claim to its actual scope.** Applied. `LEDGER.md` §"What could
   actually be reached" now states the claim as one plain HTTP client, no browser rendering, one
   egress point, one pass, with the retries named — and lists each of the four supporting facts at
   its own scope, noting that fact 4 speaks to informativeness rather than accessibility and does not
   belong in an accessibility tally. Both earlier drafts of the sentence are withdrawn and dated in
   `memory/discarded.md`.
2. **Disclose `timeStamp.untrusted` on s04 and soften the date.** Applied. The row now carries both
   untrusted findings — `signingCredential.untrusted` and `timeStamp.untrusted` — notes that
   `timeStamp.validated` succeeds so the digest does match, notes the generic manifest content
   (`title: "sample.png"`, prompt `"AI generated image"`) and the `assertion.dataHash.match` that
   binds it to these bytes, and states the narrowed claim: a timestamp *claiming* a date well before
   the seam, on an authority not trusted here.
3. **Commit a reproducible script for the signatory split, or flag the counts as transcribed.**
   Applied by building it: `tools/parse_signatories.py` runs offline against the committed page
   bytes, reproduces `sources/signatories-2026-08-02.json` exactly, and checks 83/152 against the
   page's own stated counts. Exit 0.
4. **Reconcile "about 190" against 83 + 152 = 235.** Applied, and it reconciles exactly: the same
   script finds **45 organisations in both columns** and a union of **exactly 190**. The prose counts
   organisations, the columns count signatures.
5. **Withdraw the "does not rescue N" framing.** Applied. Since no Stability AI specimen carries a
   manifest anywhere, no rule keyed to an observed positive control could move that stratum, so N
   staying put is structurally guaranteed and discriminates nothing. The claim that it evidenced the
   rule's neutrality is withdrawn in `LEDGER.md`; the forward-only application of A1-S′ is what
   remains.
6. **Make the Google/Black Forest Labs asymmetry symmetric or state it.** Stated, and priced.
   `tools/fold_google_check.py` shows the folded group reads n=9, indeterminate=8 (88.9 %), effective
   N=1, marked=1 — `capture-inconclusive` either way. The discretion is disclosed in
   `CAPTURE-NOTES.md` D6 as post-hoc, with the explicit note that "it moved nothing" is not a defence
   of it.

## Non-blocking, all three applied

1. D1 now carries the Skeptic's addition: category membership on that repository lags upload through
   a job queue, so a small-hours same-day check cannot see same-day activity regardless of how the
   window is worded. A2 must fix *when* it checks, not only how long the window is.
2. OpenAI is now named in D4 as an attempted-and-failed source for the `S` stratum rather than
   anonymised inside "three of six candidates".
3. The Wilson rounding note: the control's upper bound is stored `0.5615` and displayed `0.562`;
   naive `round(0.5615, 3)` returns `0.561` under binary floating point. Immaterial to every reading,
   recorded so a re-deriver is not puzzled.

## What the Skeptic did not break

The pre-registered machinery itself: the CI-overlap gate, the `capture-inconclusive` threshold, the
exclusion of A0 from the decision rule, and the consequence that **no directional label is available
at a single anchor** — all held, and the Skeptic said so. It also found no compliance inference that
had crept past the disclaimers, and confirmed the `LEDGER.md` table reconciles with
`a1-results.json` and `a1-alt-reading.json` exactly.

**Its closing line:** *"the pre-registered machinery holds and correctly yields no directional label,
but the anchor's headline 'closed surface' claim is an artifact of an 8-minute single-client HTTP
session, and its one positive marking finding leans on a certificate the tool itself flags as
untrusted — narrow the claims per the six conditions above before this row ships."* The row is not
shipping; the claims are narrowed anyway.
