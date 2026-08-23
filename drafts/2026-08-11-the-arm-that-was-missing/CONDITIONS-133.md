# Conditions 133 — the two roles of this session, dispositioned

**Session 133, 2026-08-23. This is not a gauntlet.** Nothing shipped, nothing graduated, no packet
exists at any status, no file under `offer/`, `deliverable/` or `deliverable-v0.3/` was touched, and
none of the ninth gauntlet's fifteen findings was repaired.

**Two roles were convened**, and the reason is stated rather than assumed: the move was not a
measurement run but a **classificatory claim about this practice's own instruments** — which of them
measure the record plus themselves. Session 132 convened nobody, correctly, because *"a session whose
move is a measurement run does not need an adversary to tell it whether the measurement ran."* That
reasoning does not reach here. A verdict like `READ-ONLY` is a judgement an adversary can contest,
and both roles contested it to good effect.

**The state reviewed:** `INCREMENT-21.md` and the twelve-invocation `convergence-audit-133.json` at
commit `226d590`. **Both verdicts are good only for that state, which no longer exists** — acting on
the charges grew the population to fifteen invocations of fourteen checks and moved three of the
figures the recomputation checked. Both reports are published **unedited**, with that noted in a
dated header and nothing else altered.

| verdict | who | result |
|---|---|---|
| **Interlocutor (a), refutation** | `INTERLOCUTOR-133.md` | **CORE CLAIM SURVIVES NARROWED** — two blocking charges, both upheld, both acted on |
| **Interlocutor (b), hostile critique** | same file, published unedited | **one charge accepted in full and named in the increment for the first time** |
| **Verifier, independent recomputation** | `VERIFIER-133.md` | **PASS WITH FINDINGS** — two blocking, both this practice's own defects, both fixed structurally |

**Four accepted findings, two of which changed the result. Nothing refused. One correction made in
the adversary's favour on the fact that mattered, and one made against its wording.**

---

## The dispositions

| # | finding | from | reproduced | disposition |
|---|---|---|---|---|
| 1 | **The population omits `audit_instrument.py`** — a live, self-referential instrument in this same arc, whose own record says session 120 caught it silently overwriting a dated evidence file. The increment's generic concession that the population is hand-made does not cover the single most on-point omission available. | Interlocutor, charge 1, **BLOCKING** | ✔ every citation re-read at source; the file, its docstring and its `main()` are as quoted | **ACCEPTED IN FULL, AND ACTED ON RATHER THAN CONCEDED.** `audit_instrument.py` and `power_audit.py` added. **The charge produced the session's sharpest finding**: `audit_instrument.py` exits 0, then 1, then 1 — it **refuses to overwrite the dated evidence file its own first run wrote**. Graded by the audit's criterion, that was a failure to converge. **It is the opposite of a failure, and the criterion was wrong.** `DECLINED-TO-REPEAT` added, detected mechanically. Conceding this charge would have produced none of that. |
| 2 | **`guard_claims.py --check` has a second, data-dependent write path** — on the FAIL branch the same invocation writes `guard-claims-expected.txt` into the arc directory with no cleanup. "Exactly one" is contingent on tonight's record passing, and nothing said so. | Interlocutor, charge 2, **BLOCKING** | ✔ read at `guard_claims.py:209-214`, **then forced and measured** rather than argued about | **ACCEPTED, AND MEASURED.** The branch is now forced in `audit_checks.py` by corrupting the claims block in a working copy. The persistent write is confirmed — **and forcing it found something neither party predicted: the branch then crashes** (`TypeError`, `subprocess.call(..., input=...)`), so the guard cannot print its diff when it fires (`ERRATA-133.md` E42). **One correction against the charge's wording, in this practice's favour and stated as such:** the adversary called it *"the e34_sweep shape exactly"*; on the measurement it is not, because that check enumerates no directory — the persistent file is a hazard to its **neighbours**, not a self-reference. The fact that matters is the adversary's and stands: **the file is left behind, and nothing before this session said so.** |
| 3 | **The population table is wrong in 4 of 12 rows against the JSON it cites as its source**, and the same stale figures were copied into a second file's docstring. | Verifier, blocking 1 | ✔ recomputed from the artifact, all four confirmed | **ACCEPTED. THIS PRACTICE'S DEFECT, AND THE WORST-PLACED ONE OF THE SESSION** — it is the exact failure `tools/record_ceiling_check.py` exists to prevent, committed inside a document about hand-carried numbers. **Fixed structurally, not by retyping:** `table_133.py` generates the table from the artifact, and every report carries the sha256 of the tree it is good for. `ERRATA-133.md` E39. |
| 4 | **"Checks 4, 9 and 10 enumerate the repository"** is contradicted by the artifact: `prose_vs_json` enumerates only the arc directory. | Verifier, blocking 2 | ✔ | **ACCEPTED AND CORRECTED.** `ERRATA-133.md` E40. |
| 5 | **"A three-line exclusion… a list of names"** overstates `e34_sweep.py`'s guard, which is two lines testing one hardcoded filename. | Verifier, non-blocking 3 | ✔ | **ACCEPTED.** The correction **strengthens the finding against this practice**, and is made for that reason as much as for accuracy. `ERRATA-133.md` E41. |
| 6 | **The tracer double-counts one `subprocess.run` as two child processes.** | Verifier, non-blocking 4 | ✔ | **RECORDED, NOT FIXED.** No figure this practice publishes rests on that count. Named here so the next session does not rediscover it. |
| 7 | **"Half this increment is the practice checking its own checker" — and this is the third session running, unacknowledged.** | Interlocutor (b) | ✔ against `CONDITIONS-131.md` finding 7 and the session-129 record | **ACCEPTED AND NAMED FOR THE FIRST TIME**, in `INCREMENT-21.md` §6. The defence offered is narrow and does not defend the length: the object under audit **is** this practice's checks, so an audit of the auditor is the same subject — and all five of this session's instrument defects would otherwise have been published as findings about somebody else's script. |
| 8 | **"Byte-identical reports" claims more than the instrument compares** for written files. | Interlocutor, charge 3, non-blocking | ✔ the code says so in its own comment | **ACCEPTED AS FAIR.** Not repaired; the wording in the rewritten increment is confined to exit status, stdout and stderr, which is what is actually compared. |

---

## Binding on the next session

1. **The stop is unchanged and unsoftened.** No delivery object, no repair pass on any bundle, no
   gauntlet, no packet from this arc before 2026-09-05. **This session added nothing to the licence
   and removed nothing from it.** The convergence instruments are new files under `tools/`, not a
   repair of anything under the arc's bundles, and no bundle file was opened.
2. **`guard_claims.py`'s FAIL branch is broken and is NOT repaired** (`ERRATA-133.md` E42). A guard
   that cannot report its own failure is exactly the kind of defect a session wants to fix on sight,
   and fixing it is a repair pass this arc does not have the licence for. **The next session with the
   licence should fix it, and until then nobody should read a green `guard_claims.py --check` as
   evidence that its failure path works** — that path has now been run twice and crashed both times.
3. **The instrument's hour stands at 03:41:00Z** until the architect rules otherwise. No session
   moves it; no substitute is measured at another hour; a day out of reach is a hole. Unchanged from
   `CONDITIONS-131.md` item 2 and `CONDITIONS-132.md` item 2. **Day 12 was reached, and that is not an
   argument for either course** — it is the second consecutive day delivered by a session that
   happened to open inside the licensed five minutes, which is luck about scheduling, not cadence.
4. **If a session opens near 03:41:00Z, the run is its first act.** Unchanged, and it is why day 12
   exists.
5. **The convergence question is answered in part and the four open parts are named**
   (`memory/open-questions.md`): the population is still hand-made with no second reader; only one
   check has had a second branch forced, and that one branch is where the session's newest defect
   was; `apparatus_ratio.py` cannot be cleared by this tracer; and the cross-check result covers one
   run of one order.
6. **Do not re-derive the schedule figures.** Unchanged from `CONDITIONS-131.md` item 4 and
   `CONDITIONS-132.md` item 4. This session did not.
7. **The open question is still with the architect** (`REQUESTS.md`, 2026-08-22). **Silence means the
   stop and the hour both stand.** This session added nothing to that request — deliberately. It has
   no new argument, the room it lives in has a word budget this practice measures itself, and a third
   restatement of *"we reached it again, and we draw no preference from that"* is words rather than
   evidence.
8. **Consolidation ran** (it last ran at session 131). Apparatus ratios, recomputed and published as
   the session-79 commitment requires: **8.32 : 1** everything outside `works/` to `works/` text;
   **61.12 : 1** to the face; **6.90 : 1** markdown prose outside to inside; **0.60 : 1** record and
   governance layer to `works/` text; unshipped text **57,377.6 KB** against **7,492.4 KB** shipped.
   **These four figures now carry a limit of their own** (`downstream-commitments.md` condition
   33(c)): the script that computes them reads the record through a child process this session's
   tracer cannot see inside, so its search-space-to-output relation is not established.


---

## The record ceiling, stated rather than hidden

**The minutes came in at 438 words against the constitution's 400.** Six passes of cutting took them
from 656 down; what remains cannot come out without dropping one of the session's findings, the day-12
result, or the sentence recording that this session's own table was wrong. **This practice would
rather be over a ceiling than quietly shorter than the truth**, so the overrun is named here for the
architect to read instead of being absorbed by trimming a finding.

The process record beyond committed code and data, for rule 6: `INCREMENT-21.md` (2,981 words at the
time it was rewritten, and the figure is not re-typed here — `tools/record_ceiling_check.py` computes
it), `ERRATA-133.md`, this file, and the two published reviews. **The two reviews are the
constitutionally mandated critique and the gate's own required deliverable, not process record**;
this session reads them out of the ceiling as sessions 89 and 90 did, and flags the reading rather
than assuming it.


**One figure from running that check, recorded because it was run and should not be quoted
selectively.** `python3 tools/record_ceiling_check.py drafts/2026-08-11-the-arm-that-was-missing`
returns **OVER**: a counted record of **366,455 words** against the 3,000-word ceiling, **363,455
over**. That is the whole arc directory — twenty-one increments, eleven gauntlet rounds, every
published review and every errata file — **not this session's process record**, and this session did
**not** investigate when the arc crossed the line or whether the ceiling was ever meant to cover an
accumulating instrument's whole working directory. **Naming it is not doing it**, and this session did
not do it. It is put here so the next session meets the number rather than rediscovering it, and so
that this session's own 414-word overrun above is not reported as if it were the only one.
