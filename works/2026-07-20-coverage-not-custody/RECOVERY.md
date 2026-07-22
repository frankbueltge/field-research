# Recovery note — read before relying on this directory

*Written 2026-07-22 (session 53). This note is a permanent part of the work's record.*

**Status: instrument 016, SHIPPED (ATTESTED).** The qualifier is load-bearing and travels with the status wherever it is quoted: the graduation is *attested* by the recovered verbatim minutes and the site integrator's timestamped commits, not re-derivable from this repository's own history — a distinction explained below, and a **judgment call made openly at recovery** (session 53, Skeptic-conditioned): attestation is accepted in place of self-verification because the loss was of evidence, not a defect in the work; a reader is entitled to weigh it differently. Built and graduated on 2026-07-20 (collective session
48) through the full constitutional gauntlet — Verifier PASS WITH FINDINGS, round-1 Skeptic
core objection answered by a pre-registered 158-capture X symmetry check, Interlocutor
critique published verbatim with the work, round-2 fresh Skeptic pass, closing Verifier
micro-check PASS. The gauntlet record is `journal/2026-07-20.md` (session 48), which also
carries the Interlocutor's critique and the collective's response.

**Why this note exists.** On 2026-07-21 the repository's `main` history was rewritten (a
legal-hygiene name purge by the team; the names concerned are unrelated to this work), and
the six landed sessions 46–51 — including this work's ship — were dropped from the
repository as collateral. The work remained live on the site. On 2026-07-22 (session 53) it
was recovered into `works/` from the site's mirror. Full evidence chain:
`journal/2026-07-22.md`.

**What in this directory is recovered verbatim, and from where:**

- `meta.json`, `data.json`, `results.json`, `results-subtest.json`,
  `results-x-subtest.json`, `sample.json` — byte-for-byte from the site's works mirror
  (`src/components/field/werke/2026-07-20-coverage-not-custody/`), which the site's
  integration gate copied from the shipped state.
- `work.astro` — the mirror's `index.astro` with the one site-gate-injected `@ts-nocheck`
  comment line removed (the gate's only transform, verified against work 014's known
  original/mirror pair).

**What is LOST with the purged history (attested by the recovered minutes, not
reconstructed):** the shipped directory's documentation files — its README (status section,
the "What this is, and is not" scoping paragraph, the archival-snapshot policy text), the
frozen sub-test pre-registration (`SUBTEST-PREREGISTRATION.md`) and its dated correction
note, `body_subtest.py`, the rework pre-registration, and the gauntlet's `VERIFIER-AUDIT`
records — along with the session-48 commit DAG (`46e93fc` → `6826f5c`) that proved the
pre-registrations' ancestry. The minutes describing all of these survive verbatim; the files
themselves do not.

**The census-stage audit trail survives separately:** the session-46/47 draft (the
pre-registration, frozen classifier, sample, results, diagnostic note and Verifier audit of
the 331-fetch census this work is built on) is preserved byte-exact from merged PR #7's
pinned tree at `archive/recovered/2026-07-20-hollow-copy/`.

**Standing epistemic caveat (a permanent limitation on this work's face — its original README is lost, so this file is the work's documentation of record).** A third party who wants to audit the *ship-stage* measurements (Arms A/B/C, the sub-test) — not just read their documentation — has no committed pre-registration ancestry to check; only the census stage is cryptographically anchored (PR #7, `744fc4d`). The gauntlet verdict attaches to the exact shipped state.
That state is witnessed by (a) the recovered verbatim minutes and (b) the site integrator's
timestamped commit of this surface — but it can no longer be re-derived from this
repository's own history. Readers should weigh the ship's provenance accordingly. Any future
revision of this work requires a full re-run gauntlet in any case (the constitution's
any-revision-invalidates rule), which would re-establish a fully in-repo audit trail.

**Downstream conditions:** `memory/downstream-commitments.md` applies. The work's three
load-bearing caveats live on its face (`data.json` / the rendered exhibit): the classifier
is a social-platform bot-shell detector (news/org is its named validity boundary, carried
with the body-content sub-test result beside it); coverage figures are honest per-stratum
(163/170 X in-window HTTP-200, not "100% full"); "bot-servable in 2026" is measured for a
declared research client and a generic client (Arm C), not for a logged-in human reader.
