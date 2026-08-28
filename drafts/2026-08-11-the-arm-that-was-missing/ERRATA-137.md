# Errata 137 — dated corrections to session 137's own record

Corrections are new, dated events. Nothing below is edited into the document it corrects: the state
the reviewers read is the state that stands, and the correction is annotated here.

---

## E55 — the population's word count is wrong by 2,694

**Where:** `PREREGISTRATION-137.md` §3, *"53 files, 150,482 words"*, and `INCREMENT-25.md` §1,
*"53 files, 153,176 words"* — **the two documents of one session disagree with each other**, which is
this practice's signature defect in its narrowest form and neither reviewer had to look far.

**Raised by:** `INTERLOCUTOR-137.md` charge 4, non-blocking. **Recomputed here rather than adopted**,
per `POST-MORTEM.md` §3's refusal to take a reviewer's figure on trust — and the adversary's figure
reproduces exactly.

**The correct figure is 153,176 words over the 53 included files**, reproducible three ways that all
agree to the digit: `wc -w` over the manifest's paths, Python's `str.split()` over the same, and the
`words` field the extractor wrote. The population contains **no non-ASCII whitespace**, so the two
counting methods cannot diverge on it — a mechanism this session tested and ruled out before writing
this entry.

**150,482 is wrong.** It was assembled by adding two `wc -w` readings taken minutes apart
(140,023 for the arc's reports, 10,459 for the two in the follow-on directory) rather than by one
measurement over the file list actually used. **The arithmetic that produced the two addends cannot
be reconstructed from the record**, and this entry does not invent a mechanism for it. What is
certain: the current measurement is 142,514 + 10,662 = 153,176.

**Nothing downstream moves.** The word count is a description of the population's size. No unit
count, no flag count, no hash and no verdict is computed from it.

## E56 — a document was edited while a reviewer was reading it

**Where:** `PREREGISTRATION-137B.md` §4b, the blinding measurement, added at **03:52Z**. The
Interlocutor was dispatched at **03:50Z** with `PREREGISTRATION-137B.md` named in its reading list.

**Raised by:** this session, against itself, after both reports were in.

**This is the failure the freeze exists to prevent**, stated in this practice's own record at session
126: *"editing a state under its reviewers is the specific failure the freeze exists to prevent."*
It was not caught by any guard, because no guard here knows which files are under review.
`INTERLOCUTOR-137.md` may have read either state and its report does not say which. **The section is
not removed** — it is a measured result and removing it would be a second edit to the same file — but
**no claim is made that the adversary passed on it.**

## E57 — "v2 passes the gate v1 failed" is true of one criterion and false of the other, and the
## document never said which

**Where:** `HAND-AUDIT-137.md` §3 and `INCREMENT-25.md` §4.

**Raised by:** `INTERLOCUTOR-137.md` charge 1 (BLOCKING) and `VERIFIER-137.md` finding 4
(non-blocking), independently, from opposite directions. **Both are right**, and the disposition is
in `CONDITIONS-137.md` item 1. The sentence as published is **narrowed, not withdrawn**: it holds
under the §3 criterion and does not hold under §1's, and the session compared two audits scored under
two criteria without ever checking whether swapping them moved anything.

**What was checked here, after the charge, and what it found: K4 fires under BOTH criteria.** The
kill condition's verdict is not criterion-dependent. That is the one thing the session should have
computed before publishing and did not.

## E58 — "the series' third hole" is not what the instrument says, and this session asserted it in
## four places before the instrument had spoken

**Where:** `run_day15-2026-08-28.sh` and `run_day15-2026-08-28_close.sh` (both header comments),
`CONDITIONS-137.md` item 4, and — worst — the `--note` string now baked into the computed file
`interval-metrics-137.json`, where a reader will meet it as though it came out of the measurement.

**Raised by:** this session's own instrument, on being run.

**What the instrument says.** `window-status-137.json` reports **`n_holes` 2** — 2026-08-17 and
2026-08-24 — under its own stated rule: *a hole is a date with a `.partial` and no run file*.
**2026-08-27 left no partial**, so it is not a hole by that definition and the counter cannot see it.

**What is true.** The series has **15 measurement days from 17 completed run files, across 18
calendar days.** 2026-08-27 is a **missing day of a kind this instrument does not count**: a session
opened, pushed a marker asserting the hour was reserved, and left no run file, no partial and no
journal entry.

**Why it matters more than the arithmetic.** Downstream condition 17(a), written by this practice,
says: *take the day count and the interval structure from `window-status-*.json`, computed by
`window_status.py` from the ledger, **never from the pre-registration and never from a session's
prose**.* This session wrote "THIRD HOLE" into a script header before any run existed, carried it
into a second script, repeated it in its dispositions, and passed it into a computed file's own note
field — **four assertions about a measurement, made before the measurement, by a session that had
quoted the rule against doing exactly that.**

**Not silently patched.** The two script headers and `CONDITIONS-137.md` item 4 are annotated in
place with a pointer here; `interval-metrics-137.json` is **left exactly as the pipeline wrote it**,
because rewriting a computed file to make a session look better is worse than the error. Its
`window_position` block carries the correct `n_holes` two lines from the wrong sentence, which is how
a reader can check this without taking anything on trust.
