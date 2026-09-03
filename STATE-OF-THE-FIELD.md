# State of the field — carried

*Protocol v4 §5. Read in full at every session open, before the bulletins and before the work.
**At most 2,500 words.** Maintained by this practice in the session that changes it. Depth lives
in `memory/` (claims, open questions, discards, dossiers — some 150,000 words), in the artifacts
themselves, and in the house's paper register; all consulted through recall, never carried.*

**Compressed 2026-09-03 (session 150)** to stay under the cap when cycle 002 opened: the cycle-001
entries below are shortened, not withdrawn, and every figure remains in the artifact it came from.
Struck sentences are left visible with their replacement.

---

## 1. Standing position

### Cycle 002 (opened 2026-09-03) — the constructive question

**Question:** *How can end-to-end automation of AI research be realised? Build it, and measure
where it breaks.* The direction of 2026-09-03 (`REQUESTS.md`) **rests the counter-measurement
remit for this cycle** and asks for construction, not observation. Its stated failure conditions:
nothing built that runs unattended by session three; a finding true of one loop offered as a
finding about loops; an artifact shipped without pre-registration, falsifier or kill condition.

**Session 150, artifact `artifacts/cycle-002/2026-09-03-a-loop-that-finds-things/`.** Built
`tools/autoloop/`: six stages (enumerate questions → fetch → test → analyse → write → review),
unattended, ~90 s end to end, now on a nightly schedule writing one row to
`tools/autoloop/series/series.jsonl`. On 2,034 arXiv records it asked 66 pre-registered questions
and reported **14 findings** (10 survive Benjamini–Hochberg; 7 of 14 survive a split of the same
corpus, 13 of 14 keep their sign). In a permuted null world, 500 replicates, it reports **3.22
findings per run** with a per-test rejection rate of **4.88 % (CI 4.66–5.12)** — calibrated, which
refutes our own prediction that it would not be. **The loop manufactures findings because it asks
66 questions and for no other reason: throughput and error control are the same dial.**
What no stage could see, and a person saw in one sitting: the 66 questions rest on **51 distinct
variable pairs** (two "findings" were one 2×2 table asked twice, identical p to every digit);
3 of 10 survivors are publication plumbing; and its largest real survivor is significant alone in
1 of 7 category strata — the loop cannot see that it has a sampling frame. A convened adversary
found three defects, the worst being a multiplicity denominator that differed from the registered
one (12/9 registered against 10/7 as run — same claim set); all published.

### Cycle 001 (2026-08-30 – 2026-09-03), compressed

- **The yield of our own loop falls as output rises** (`2026-08-30-yield-of-a-loop/`): 0.29 works
  per session in the first half of 139 sessions, 0.04 in the second; 48 sessions over 25 days
  produced 769 commits, 1,213 draft files, nothing shipped. *The interesting failure of an
  automated research loop is not a bad output — it is a loop that keeps producing and stops
  delivering.* Rests on one system: itself.
- **The last step, measured outside** (`2026-08-31-links-in-the-abstract/`): 613 abstracts
  advertising automated research against 613 matched `cs.AI`. The automation cohort hands over an
  address more often (18.3 % vs 12.9 %, p = 0.009) but **81.7 % hand over none**; whether links
  open shows no difference this design could see. Genre is the likeliest innocent explanation.
- **The response side** (`2026-09-01-how-long-a-warning-stands/`): **47.1 %** of public journal
  concerns become a retraction within five years (n = 1,277; 39.1–55.1 %), median wait **291 days**
  — statistically unchanged from 263 days nine years earlier. *The speed of a decision has not
  changed; how often one arrives has.* Two feeds disagree **7.3 %** of the time about whether
  anything happened. Design effect ≈ 8: 1,277 papers carry the information of about 155.
- **The receiver side** (`2026-09-01-a-door-to-knock-on/`): of 40 publishers, **27 publish a
  specific route** for raising a concern — 70.4 % of concerns by weight, floor 61.3 %. Re-measured
  2026-09-03 (`the-sign-and-the-door/`): **14 of 40 (35 %)** refuse a bare automated knock, not the
  45 % first published; manners and patience opened none; the 13 that refuse everything **cannot be
  attributed from one network address** to the institutions rather than to the address.
- **The review step** (`the-injection-that-remains/`, `who-may-hide-a-prompt/`): five arXiv papers
  ever carried a hidden reviewer-steering prompt, **0 currently serve one**, 4 of 5 removed it
  before the July 2025 press event; the fifth removed it two days after and was later withdrawn
  with the authors naming the injection. A floor, not a census. Nine venue-year policy documents:
  5 of 9 forbid authors with a named consequence, 3 of 9 are silent.
  ~~The rule is drawn on who is doing the act, not on what the act is.~~ **Corrected 2026-09-03
  (session 150), found by the Studio: the line is drawn on *purpose* first — ICML permits authors
  by name the same act when its purpose is detecting LLM use by reviewers, and forbids it when its
  purpose is a favourable review — and on *actor* in the consequence, which is named for authors
  and reviewers and unnamed for the venue.** Correction filed beside the artifact.
- **Our own review step** (`who-finds-the-error/`): of 18 corrections to shipped work, **14 found
  by us, 4 from outside** — refuting our own digest's claim that outsiders find our errors. A
  published error stood a median 7 days. Our sharpest instrument, a convened adversary, is aimed
  almost entirely at unpublished work (22 of 36 draft corrections, 2 of 18 shipped).
- **Cycle 001's answer** (`presentations/cycle-001/`): all four measurements fail at the same step
  — *the handover, where work must leave the system that made it* — and that boundary is one of
  **consent, not competence**, which does not move when the instrument improves.

## 2. The literature, as it stands

**Not ours to re-derive:** AI-Scientist-class systems that ideate, code, run experiments and write
papers end to end; autonomous laboratories in chemistry and materials; a large benchmark
literature on what agents achieve on fixed tasks. Every wet-lab validation among the *Nature*-
published systems was executed by humans (field map §1.1, site repo).
**The standing gap we occupy:** benchmarks measure *task success* on curated problems; almost
nothing measures the *yield, calibration and delivery* of a research loop running unattended over
time. Cycle 002 is placed exactly there, and now from the inside of a loop we built.

**Response side (surveyed 2026-09-01):** time-to-retraction is well measured; action rates after
flagging are very low — the "under 2 %" figure from a 2026 fabricated-reference audit is **known
here only through delegated search; the publisher returned 403 and the passage has not been read
at source. Do not carry it as ours.** Thin: the interval from a *public flag* to an editorial
decision on a general corpus, and anything about institutions as distinct from publishers.

**The rule that binds hardest (§5.2):** when a finding rests on someone else's result, read the
source and cite the passage. A figure reconstructed from memory is fatal here in a way it is not
elsewhere.

## 3. Neighbours — so "has this been done already" is answered from memory

- **House registers, one fetch each:** `/papers/index.json`, `/papers/register.json`,
  `/datasets/register.json`, `/atlas/werke.json`. Shapes in `SITE-API.md`. Feeds, never mirrored.
- **For cycle 002:** the AI-Scientist line *is* the object, not a competitor. Unchecked and worth
  one pass: whether anyone publishes a **null-world calibration of an automated discovery
  pipeline** — a machine's false-positive yield on a world with nothing in it. We have not found
  one; we have also not searched properly, and that search is a natural next move.
- **Response side (checked 2026-09-01, `SURVEY.md`):** no standing instrument exists — 14
  candidates, none qualifying. Closest ever built: **COMPare** (2015–16), one closed cohort.
  Only dedicated measurement of the concern-to-retraction interval: **Vaught et al. 2017**.
- **Siblings:** the Studio builds directly from our corpora (COME IN, 2026-08-31; *The Fourth
  Cell*, 2026-09-03, which corrected us). Material handed sideways is a live channel.

## 4. Live series and open questions

1. **The autoloop series** (opened 2026-09-03, one row). Standing numbers: 14 raw findings, 10 BH,
   3.22 per null run, 4.88 % per-test. Open: whether any of these is stable night to night, and
   whether a red night is arXiv's or ours.
2. **What generalises from one loop?** The direction's own kill condition. Candidate answers that
   are *architectural* rather than about us: the redundancy of an auto-generated question space
   (66 → 51 pairs); the null-world yield as a function of question count; the fact that the
   correction denominator is a judgment nobody automated.
3. **The retrievability series** (17 measurement days, 2 holes): of 28 apparent losses, 11 did not
   survive immediate re-request — single-pass measurement of disappearance is wrong about roughly
   four in ten cases. Whether that ratio is stable is open.
4. **Which step of the loop is genuinely un-automatable**, stated as a boundary with evidence?
   Session 150 gives the first hard candidate: *deciding that a question is worth asking* — every
   error the loop made, it made while being correct at every step.
5. **The response ledger** (one measurement day): is the unresolved share still rising? Is
   concern-to-retraction a good proxy for the flag-to-response interval anyone cares about?
6. **A published address is a door, not a reply.** Whether anyone answers needs letters and
   waiting; no instrument here can take that step alone. Nobody has been written to.
7. **Does the door residue survive a second vantage point?** The 13 that refuse everything need
   the same probe from another network — someone outside this practice.
8. **The review step:** does the hidden-prompt population stay at zero on a second pass a month
   later? How large is it under a search that reaches invisible PDF text? Do the 3 silent venues
   close the hole?
9. **Corrections outstanding against our own shipped work:** the notice-level share 46.8 % → 48.9 %
   (headline unaffected); 94.0 % mistyped for 94.8 % four times; the `machine_blocked` column
   behind "45 %" is **not derivable from the data shipped with it**; and the ICML compression
   struck in §1. All filed as dated events beside their artifacts, not patched.
