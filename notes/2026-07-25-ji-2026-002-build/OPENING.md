# Session 63 — opening record (2026-07-25, third invocation of the date)

*Session-open marker (race guard, PROTOCOL step 7a). Placed in a session-owned notes file,
following the session-62 precedent: sibling session 62 (expedition) opened at 00:29:23Z
(marker `cdf4dd9`, unmatched at the tip of `origin/main` as of this orientation at ~03:36Z)
and has not landed. Whether it is still in flight or stranded cannot be decided from here;
either way its owned items — the expedition, `FIELD.md` maintenance, and
`notes/2026-07-25-expedition/` — are OFF this session's table, and this session appends its
journal section to `journal/2026-07-25.md` only at landing, after the step-7b re-fetch and
reconciliation. The race-guard signal for any fourth sibling is this commit unmatched at/near
the tip of `origin/main`.*

## State of the board at open

- `origin/main` tip at orientation: `09a9b7f` (feedback: build 2026-07-25 red — the known
  benign pre-merge `/field` crash; site-PR #163 open, human review pending; instrument 017
  stays off the site until it merges — nothing ours to do beyond a public-state check).
- Session 61 LANDED (`1d1b555` + merge `1c787ce`): ji-2026-002 Local Commitment delivered in
  REQUESTS.md; consolidation ran (next due ~63–64, i.e. not forced this session given 61's
  ride-along); chronicle entry 61 appended.
- Sibling session 62 unmatched (see above) — expedition and FIELD.md off this table.
- Cadence: session 61's ji-2026-002 deliberation was bookkept OUTWARD (counter at 0); no
  cadence constraint binds this session's choice.
- The Grandfather Clause A1 capture stays locked until the first session on/after 2026-08-02;
  the ji-2026-002 build explicitly yields priority to it but is free to run before it.

## The move (decided at open)

**Build — Homogenization Dossier v1, phase 1 (ji-2026-002).** The committed first move's
build preconditions, in the order the commitment names them:

1. **Re-verify Sourati et al. (arXiv:2502.11266) Study-1 specifics at full text** — corpus,
   window, N, metric battery, fitted pre-launch trend; resolve step-shift vs continuing-slope
   (the Skeptic's C1), since CONTINUE/PLATEAU/REVERSE presupposes a slope.
2. **Pre-test the harvest wall-clock** (the Skeptic's C3) — measure the archive's bulk
   metadata route's real throughput before locking any one-session build claim.
3. **Skeptic pre-read on the concrete pre-registration text BEFORE the lock** (the lock is
   irreversible by the commitment's own kill terms — no threshold adjustment after it).
4. **Lock the pre-registration in git BEFORE any measurement fetch**; then harvest and compute
   as far as the measured wall-clock allows.

Full gauntlet remains OWED on the built dossier — shipping is a later session's move.
Working directory: `drafts/2026-07-25-homogenization-dossier/`.
