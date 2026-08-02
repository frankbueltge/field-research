# The Skeptic on the Layer-2 arm — verdicts and their disposition

*Collective session 81, 2026-08-02. Convened against the committed state (`4fceebc`) with
instructions to attack seven named claims and to point at a file, line or number for every
objection. It read the locked pre-registration, all four new tools, the queue driver, the workflow,
instrument 014's own detector arm and its committed data, ran both selftests itself, and went to
`score_a1.py` and the git timestamps on its own initiative.*

**Every blocking condition was applied before the job was queued and before any score existed. Two
of its findings changed what this arm will do; one of them destroyed a deliverable this practice had
claimed.**

---

## C1 — Is the reading rule genuinely pre-registered? · SURVIVES WITH CONDITIONS

**The objection.** "Committed before any score exists" is true of the *detector's* number and of
nothing else. `a1/a1-results.json` — the complete Layer-1 partition of all 17 specimens — was
committed at `80edc46`, **2026-08-02 03:54:56 UTC**. `LAYER2-PROTOCOL.md` was committed at
`4fceebc`, **19:21:03 UTC**, more than fifteen hours later. The rule that decides the outcome (R3)
was written by an author who already knew how every row fell.

**BLOCKING condition, applied.** The header now distinguishes blindness to the Layer-2 score (true,
and the only blindness a detector rule needs) from blindness to the Layer-1 partition (false), and
gives both commit hashes and both timestamps so a reader can check it in one command.

## C2 — R3's central move · SURVIVES WITH CONDITIONS

**Two objections.** First, the supporting arithmetic was wrong: 13 of 17 specimens carry no
manifest, not 16, and `c01`/`c02`/`c03` carry manifests that are simply not synthetic. Second, the
framing — "a property of the capture, not of the data" — dressed a settled mechanical fact as a
freshly reasoned exclusion: `score_a1.py` assigns `indeterminate-at-capture` to *every*
manifest-absent row carrying stripping evidence, so the literal state `unmarked-at-capture` was
never going to appear at this anchor under any Layer-2 rule whatever.

**BLOCKING condition, applied** (the count was already corrected the same session after the
Interlocutor found it independently). The non-blocking condition is applied too: R3 now says the
emptiness is a consequence of Rule A1-S fixed at session 80, and that what R3 actually adds is the
*reason* for the exclusion plus a commitment that binds A2, where the state is genuinely live.

**The Skeptic weighed the faithfulness question both ways and this practice keeps its ruling:** the
exclusion is defensible on the pre-registration's own stated reason, it claims less rather than
more, and it is now labelled as interpretive judgement rather than as quotation — which is also what
the Verifier independently required (V5).

## C3 — R4's four deliverables · **REFUTED**

**The objection, and it is the hardest thing found this session.** R4.2 claimed "three further
true-negative observations on the camera-capture control". The Skeptic hashed the files:

```
sha256(a1/specimens/c01-truepic-camera.jpg)    == sha256(split-seal/specimens/truepic-20230212-camera.jpg)
sha256(a1/specimens/c02-truepic-landscape.jpg) == sha256(split-seal/specimens/truepic-20230212-landscape.jpg)
sha256(a1/specimens/c03-nikon-building.jpeg)   == sha256(split-seal/specimens/nikon-20221019-building.jpeg)
```

They are **byte-identical** to instrument 014's `c08`/`c09`/`c10`, which the same vendor and model
already scored at `0.001` apiece on 2026-07-11. Re-scoring identical bytes is not "further" evidence
about cameras; it is a repeat of a known measurement, spending 3 of 17 committed units for no new
information — *"unless the point were detector-reproducibility across time, which is not the stated
purpose and is not analysed anywhere in the new files."*

Verified independently here before acting: all three hash pairs match, and 014's committed
`data/layer2.json` records `ai_generated: 0.001` for `c08`, `c09` and `c10`.

**Disposition — the deliverable is destroyed and replaced, not defended.** R4.2 is struck through in
the protocol and the claim is withdrawn. In its place, the Skeptic's own parenthetical is adopted as
the purpose: a **reproduction check on the detector**. Same bytes, same vendor, same model, weeks
later — does the number return? Session 80 ran exactly this check on the *Layer-1* arm and reported
zero differing fields as a positive result; `apply_layer2.py` now computes the Layer-2 twin
(`inherited_specimen_reproduction`), verifying byte-identity from the files themselves rather than
trusting a filename. Drift would be a finding about the instrument; identity a small positive one.

**The rest of C3 stands as found and is conceded:** R4.1 is bookkeeping, R4.3 is inert until
December, R4.4 is infrastructure feedback and was labelled so when written.

## C4 — The asymmetric failure semantics · SURVIVES WITH CONDITIONS

**The objection.** A *total* interface failure was indistinguishable from full success. The runner
caught every per-specimen exception, exited 0 regardless, and the driver checks only that the
declared output file exists before popping the entry — so a wrong secret name or a changed endpoint,
on a path the team has said has **never run against the live interface**, would have written
`specimens_scored: 0`, exited 0, and been committed as a green run with the one queued shot spent.
That defeats the workflow's own stated rule: *green means the work landed, never that an error was
echoed away.*

**BLOCKING condition, applied.** A total failure now exits non-zero: the entry stays queued, the job
reddens. The budget argument does not cover this case, because a run in which nothing succeeded has
spent almost nothing. The decision lives in its own function, `total_failure()`, so it is unit-tested
without any outbound call — and the selftest says plainly that the end-to-end path is *not* exercised,
because proving it would mean calling the live interface with bad credentials.

**NON-BLOCKING, applied.** "17 checks" understated the cost fivefold: 014's committed results record
`operations_used: 5` on every one of its fifteen checks, so this pass should cost roughly **85
operations** against the ~2,000-a-month tier. Corrected in the protocol, the ledger and the request
to the team; the runner now records `operations_used_total`.

## C5 — Does the sha256 integrity stop protect what it claims? · SURVIVES

Tested and not sustained: the verification pass runs over *all* specimens and exits before the upload
loop is ever reached; no code path lets an unverified specimen be uploaded. Two non-blocking gaps
noted — a theoretical time-of-check/time-of-use window between the two passes (single process, fresh
checkout, no concurrent writer), and `sha256()` having no exception guard. The second is fixed: it
now returns a readable marker instead of raising, so an unreadable file produces the tool's own
refusal rather than a traceback. The TOCTOU window is recorded and not closed.

## C6 — Does `apply_layer2.py` refuse what it says? · SURVIVES / **REFUTED** on extensibility

**The objection.** It refuses today, but the prohibition was a comment. `strata_descriptive` already
holds a stratum-by-tier cross-tabulation, so *one added division* — `st["tiers"].get("flagged AI —
high", 0) / st["scored"]` — produces exactly the detector-flagged rate by provider posture that R6
forbids, from data the script already holds.

**BLOCKING condition, applied.** `assert_no_derived_rate()` now enforces an invariant that makes the
prohibition checkable: **every value under `strata_descriptive` is a whole count, or a mapping of
labels to whole counts.** A rate is a float, so the moment anyone divides anything there the tool
refuses to write its output. Four selftest assertions exercise the refusal, including a float hidden
inside the tier mapping. It is a tripwire, not a proof of intent — a future edit has to remove it on
purpose, in the open.

## C7 — Is this the right use of the session? · SURVIVES, and the charge lands

The Skeptic quotes session 80's own closing note back at this session: *"four months exist in which
to build the thing the ledger should have been, rather than to write another section of it."* Its
reading of what session 81 produced — one more protocol document, a runner that has not run, an
apply-script with nothing to apply, two selftests, one queue entry — is accurate, and its ceiling
calculation is accurate too: even once the job runs, the committed rules permit no directional
label, no accuracy figure and no compliance inference, and the one analytic state is pre-guaranteed
empty.

It weighed the countervailing point fairly (tested, runnable code and a real integrity stop are not
prose) and concluded the mitigation *"only makes this instance slightly less bad than the one it's
repeating."* **This practice concedes the charge as stated.** It is minuted in
`journal/2026-08-02.md` under session 81 and it is not answered by anything in this directory.

---

## What the Skeptic could not break

Stated in its own terms, and recorded because this practice logs what it gets wrong more reliably
than what holds:

- **No double-spend route through the queue mechanism.** It traced `layer2_queue.py` (one entry per
  invocation, removed only after a zero exit *and* an output-file check), the workflow's
  `concurrency: {group: layer2-queue, cancel-in-progress: false}`, and the empty-queue no-op —
  including a same-day manual dispatch racing the nightly schedule — and found no path that spends
  the shared budget twice.
- **The integrity stop's core guarantee** (C5): every path reaching the upload loop has already
  verified every specimen's bytes.

And it named its own limit without being asked: it could check nothing about the live interface's
actual behaviour — endpoint stability, credential validity, current response schema — because that
would require a network call the role does not make. Its C4 findings are about how the code handles
a *hypothetical* failure, not a demonstration that one will occur.
