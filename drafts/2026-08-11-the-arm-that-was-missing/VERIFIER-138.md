# Verifier 138 — published unedited

*Convened by session 138, 2026-08-29, against the state frozen at `FROZEN-138.sha256`. Its stated
reason, written before it ran: this session's entire result rests on five hand counts taken by a
role it convened and on a diagnostic script it wrote whose own validation assertion FAILS and which
it deliberately did not fix — both need checking against the sources and the data, never against the
reasoning that produced them. Reproduced below exactly as returned.*

---

## VERDICT: PASS WITH FINDINGS

All findings below are NON-BLOCKING. I found no blocking defect: the draw reproduces exactly, all five hand counts I performed independently match the published counts and verdicts, the diagnostic script reproduces byte-for-byte including its validation failure, and every arithmetic and quotation claim I traced had a retrievable basis in the repository.

---

### Findings

**1. NON-BLOCKING — `INCREMENT-26.md` §1: "`PREREGISTRATION-138.md` pushed... **03:39:24**" vs. actual commit time.**
Check: `git log --format='%ad' --date=iso-strict` on commit `dc06bd5` (the only commit touching `PREREGISTRATION-138.md`).
Found: AuthorDate = CommitDate = `2026-08-29T03:39:23+00:00`, one second before the claimed `03:39:24`. Trivial and does not disturb the ordering claim (the probe fired at `03:41:00Z`, confirmed below, so the push still precedes it by ~97 seconds either way).

**2. NON-BLOCKING — commits are unsigned; timestamp ordering is not cryptographically non-repudiable.**
`git log --show-signature dc06bd5` returns "No signature." The sequencing argument in `INCREMENT-26.md` §1 ("checkable from the commit times without asking this practice anything") rests entirely on local commit timestamps, which are self-reported by the committing process and not independently attestable. I found no evidence of tampering — the ledger `.partial` file's own `fetched_utc: "2026-08-29T03:41:00Z"` and the run-lock's `started_utc` corroborate the same clock independently — but "checkable" overstates what an unsigned git log actually proves. Recorded under "what I could not check," not as a defect in the practice's honesty.

**3. NON-BLOCKING — a post-freeze self-correction exists that touches the two files I was asked to fabrication-sweep, and it is not among the frozen/reviewed set.**
`PREREGISTRATION-138.md` §5 says "The debt is now **four sessions** old"; `PREREGISTRATION-138B.md` §6 says "the debt is now **five sessions** old" — both verified verbatim by direct grep. A later commit (`c159daa`, `03:52:35Z`, after `INCREMENT-26.md`'s `03:49:58Z`) adds `ERRATA-138.md` E59, which catches this exact inconsistency, traces the correct reading from the session-134-through-138 record, and states explicitly that neither frozen file is edited and nothing downstream depends on the figure. This is good practice, not a violation — I flag it only because it exists outside `FROZEN-138.sha256` and outside my assigned reading list, and a reader of the frozen files alone would see the unresolved discrepancy without the explanation.

**4. NON-BLOCKING — `carve_audit_138.py`'s detectors have real mechanism-specific blind spots the docstring's general "lower bound" language doesn't spell out.**
Reading D2–D5 against their code: (a) D2 (`d2_heterogeneous`) only ever fires when the *chosen* family is `LABELLED` — it never checks `CHARGE`, even though `CHARGE`'s regex also merges `Charge|Finding|Objection|Defect` into one family and could in principle mix two logically distinct numbered lists the same way `VERIFIER-120.md`'s `F0-`/`F` mix does. (b) D5's `SUMMARY_HEAD` regex requires the heading to end at `SUMMARY OF (THE) FINDINGS` / `FINDINGS SUMMARY` / bare `(THE) FINDINGS` with nothing trailing but `**`/whitespace — I confirmed by direct regex trace that it would **not** match `VERIFIER-133.md`'s actual heading `## Findings (blocking / non-blocking)` (line 39), which is structurally the same "chapters/table vs. findings-list" shape D5 is built to catch. That file is caught only because D3 happens to also fire on it. (c) D3's contiguous-run grouping (`gap <= 6` lines) is an undisclosed heuristic. None of this contradicts the docstring's explicit "a lower bound, not a measurement... a sixth kind of mis-carve is invisible to it," but that disclaimer is general where these are specific, checkable mechanisms a later session should know about before trusting a clean D5/D2 result on a new file.

---

### What I recomputed and found correct

- **Hashes.** All eight `FROZEN-138.sha256` entries recomputed with `sha256sum` and matched exactly. No file has moved.
- **The draw.** `random.Random(1380).sample(sorted(eligible), 5)` over the 53 manifest files minus the ten named exclusions gives eligible = **43** and the same five files as `k4prime-draw-138.json`: `INTERLOCUTOR-11.md`, `INTERLOCUTOR-15.md`, `READER-128-3.md`, `VERIFIER-125.md`, `VERIFIER-134.md`.
- **Timing.** `PREREGISTRATION-138.md` committed `03:39:23Z`; the daily probe's own vantage record (`ledger/run-2026-08-29T0341Z.json.partial`, `run-lock` file, `day16-2026-08-29-stderr.txt`) independently confirms it fired/started at `03:40:59Z`–`03:41:00Z`, reserved at `03:36:33Z`. The preregistration precedes the probe.
- **The five hand counts, recomputed by me directly against the files, with delimiters:**
  - `INTERLOCUTOR-11.md`: 5 (`**Claim 1 — …**` … `**Claim 5 — …**` at lines 17, 36, 48, 55, 75; the `# CONDITIONS` list at lines 82–87 is 6 remedies, correctly excluded). v2=6 (LISTNUM). **DISAGREE**, confirmed.
  - `INTERLOCUTOR-15.md`: 4 (`## Charge 1` … `## Charge 4` at lines 33, 102, 163, 181). v2=4 (CHARGE). **AGREE**, confirmed.
  - `READER-128-3.md`: 6 (numbered questionnaire items `## 1.`…`## 6.`). v2=6 (HEADNUM). **AGREE**, confirmed.
  - `VERIFIER-125.md`: 5 (`### Finding 1`…`### Finding 5`, line 18–140; the alternative 26-item "What I RECOMPUTED" list, lines 160–216, verified to be exactly 26 items). v2=5 (CHARGE). **AGREE**, confirmed.
  - `VERIFIER-134.md`: 6 (`## Summary of findings` items 1–6, lines 240–257; the seven `## N.` chapter headings are lines 11, 61, 105, 140, 164, 197, 210). v2=7 (HEADNUM). **DISAGREE**, confirmed.
  - K4′ fires: 2 of 5 > 1. Confirmed.
- **BOLDLEAD mechanism.** Confirmed in `extract_units_137_v2.py`'s `pick_family()`: SPECIFIC (CHARGE, LABELLED) checked first, then the best of GENERIC (HEADNUM/BOLDNUM/LISTNUM) if ≥ MIN_UNITS, and only then BOLDLEAD. For `INTERLOCUTOR-11.md`, LISTNUM=6 (≥3) wins before BOLDLEAD (=11) is ever considered — exactly as claimed.
- **The diagnostic.** Re-ran `carve_audit_138.py units-manifest-137-v2.json /tmp/recheck-138.json`: output `files 53 extracted 51 FLAGGED 11 contested 34`, D2=1/D3=8/D4=1/D5=1, exit code 1, single failure `VERIFIER-133.md: hand AGREE, but flagged D3_TABLE_UNCOVERED`. `diff` against the committed `carve-audit-138.json` (JSON-normalized): **identical**.
- **Arithmetic.** 11/53 = 20.75...% → 20.8% ✓. 34/53 = 64.15...% → 64.2% ✓. Per-role contested: interlocutor 21/26, verifier 11/16, reader 2/11 — all recomputed directly from `carve-audit-138.json`'s rows and matched.
- **Fabrication sweep.** The three sha256 pins of `PREREGISTRATION-137B.md` §1 recomputed and matched current files exactly. The "137 of 483 units (28.4%)" blinding figure independently reproduced from `units-137-v2.json`/`units-manifest-137-v2.json` using the four named tokens (Charge N, Finding N, BLOCKING, verdict vocabulary): got 137/483 = 28.36%→28.4%, split 69 interlocutor/68 verifier/0 reader — exact match. "Three of ten fresh files disagreed": traced the ten (five builder-counted at seed 1372, five independently counted at seed 1380) and the three (`VERIFIER-127.md`, `INTERLOCUTOR-11.md`, `VERIFIER-134.md`) — arithmetic and membership both check out. `PREREGISTRATION-137B.md` §3's "three files" naming five is a real slip, confirmed by direct read of that file. The line-number correction in `HANDCOUNT-138.md`'s closing parenthetical checked against both files with a consistent constant offset (FILE-1: +1, FILE-5: +718) at every delimiter — accurate.
- **CONDITIONS-137.md items 1–8**: each checked against this session's actual output. Item 1 (defect disclosed beside every figure): honored in both PREREGISTRATION-138.md §1 and INCREMENT-26.md §6. Item 2 (population-wide v2 diagnostic before any rate): discharged, confirmed by reproduction. Item 3 (hand count not taken by the extractor's builder): honored per HANDCOUNT-138.md's stated process. Item 4 (instrument hour at 03:41:00Z): confirmed by ledger/run-lock. Item 5 (run as first act near session open): honored, session opened 03:36:09Z, reserved 03:36:33Z. Item 6 (nothing ships): confirmed — neither commit touches `deliverable/`, `deliverable-v0.3/`, `letter/`, or `offer/`. Item 7 (no dead-session script mining): no violation found. Item 8 (session-open marker at repo root, not `journal/`): confirmed, `.session-open-2026-08-29.md` at repo root.

### What I could not check and why

- Whether the convened hand-counter in `HANDCOUNT-138.md` was genuinely blind to the extractor's output and to this practice's motives, as claimed — this is an assertion about a process I cannot observe directly; I can only confirm the counter's *output* is internally consistent and correct against the files, which I did.
- Whether git commit timestamps could have been backdated — no GPG/SSH signatures exist on these commits, so ordering rests on trust in the local clock, corroborated only by the internally-consistent probe-vantage timestamp inside the same working tree (not an independent external clock).
- Whether `blinding_check_137.py` and `carve_audit_138.py` were run exactly as shown with no discarded intermediate runs — I re-ran both from the pinned inputs and got identical output, which is the strongest available check short of live process monitoring.
