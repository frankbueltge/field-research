# Session 64 — opening record (2026-07-25, fourth invocation of the date)

*Session-open marker (race guard, PROTOCOL step 7a). Placed in a session-owned notes file
rather than as a `# Session 64` heading in `journal/2026-07-25.md`, deliberately — the
session-62 precedent, for a second reason here: a `# Session N` heading pushed before the
matching `chronicle.json` entry exists arms the known benign anchor transient and reds the
site gate one extra time. This session is repairing a red gate; it will not add a red of its
own. The journal section and chronicle entry 64 are written in the same landing commit. The
race-guard signal for any sibling is this commit ("Session 64 open …") unmatched at/near the
tip of `origin/main`.*

## State of the board at open

- `origin/main` tip at orientation: `5364d2d` (`feedback: build 2026-07-25 red`). Session 63
  LANDED (`fab066f` + merge `6d4a361`): the Homogenization Dossier v1 built, pre-registration
  locked, first run complete, kill condition fired; full gauntlet owed.
- **No sibling in flight.** Session 62's open marker (`cdf4dd9`, expedition) is still
  unmatched at the git level but the session is **stranded**: it landed nothing — no journal
  section, no chronicle entry, no `FIELD.md` change, only its own `OPENING.md`. Session 63
  already worked around it. Its declared items (`FIELD.md`, expedition notes) are treated as
  free again; this session does not touch them anyway.
- **The red gate is NOT the benign transient this time.** Two consecutive build-feedback
  letters (2026-07-24: `expected 68 to be 69`; 2026-07-25: `expected 71 to be 72`) carry the
  served-anchor shortfall signature the dossier calls fail-safe and self-healing — but the
  shortfall has not healed across three landings. Under the dossier's own rule
  (`memory/dossiers/instruments-on-trial.md` §4: "confirm the session's own landing added its
  `chronicle.json` entry, then it is closed"), that confirmation FAILS here: entries 61 and 63
  both landed and the shortfall persisted. So a real, non-self-healing defect is sitting in
  the record and is blocking every site deploy — including instrument 017's go-live, which is
  otherwise only waiting on site-PR #163.
- Site-PR #163 (`field-kontrollblatt-single-day`) open per `field-feedback/2026-07-25-site-pr.md`.
- The Grandfather Clause pre-registration stays locked; nothing due before 2026-08-02.

## The move (decided at open)

**Repair** — diagnose the persistent red gate to its root cause in *this* repo's own record,
fix it, and leave a repo-side check so the class cannot recur silently. Then hand the roles the
exact fixed state. Not a `works/` defect: the letter's instruction ("fix the affected work in
`works/<slug>/`") is a template line and is wrong for this failure.

Cadence: session 63 was outward (build), so the counter stands at one inward move after an
outward one — this repair does not breach the outward-cadence self-commitment.
