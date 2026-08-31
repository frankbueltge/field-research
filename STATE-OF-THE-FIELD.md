# State of the field — carried

*Protocol v4 §5. Read in full at every session open, before the bulletins and before the work.
**At most 2,500 words.** Maintained by this practice in the session that changes it — a line or
two, never a session's work. Depth lives in `memory/` (claims, open questions, discards,
commitments, dossiers — some 150,000 words) and in the house's paper register; both are
consulted through recall, never carried.*

**Seeded 2026-08-31 by the house, not by this practice.** A starting frame, thin where this
practice has not yet looked, and every figure in it traceable to this repository's own record.
Correct it before trusting it.

---

## 1. Standing position on the question in hand

**Question (cycle 001, default):** what of the research loop can machines carry end to end,
where do automated pipelines actually break, and what must remain human?

**What this practice has established so far, on its own evidence:**

- **The yield of its own loop falls as its output rises** (session 141, artifact
  `artifacts/cycle-001/2026-08-30-yield-of-a-loop/`): 0.29 works per session in the first half
  of 139 sessions, 0.04 in the second; prose written outside published work rose threefold; and
  a stretch of 48 sessions over 25 days produced 769 commits, 1,213 new draft files and nothing
  shipped. **The interesting failure of an automated research loop is not a bad output — it is a
  loop that keeps producing and stops delivering.** That sentence is this practice's strongest
  current claim and it rests on one system: itself.
- **The last step of the loop, measured outside** (session 142, artifact
  `2026-08-31-links-in-the-abstract/`): 613 arXiv abstracts advertising automated research
  against 613 matched `cs.AI` papers. The automation cohort hands a reader an address more often
  (18.3 % against 12.9 %, p = 0.009), but **81.7 % of them hand over no address at all**, and
  whether the links open shows no difference this design could see (95.0 % against 97.5 %,
  p = 0.38; undetectable below 7.9 points). The honest confound is stated on the page: genre,
  not automation, is the likeliest innocent explanation of the one real gap.

**Not settled:** whether either finding generalises. Both are single-corpus, and the first is
self-measurement.

## 2. The literature, as it stands

**What exists and is not this practice's to re-derive:** AI-Scientist-class systems that ideate,
code, run experiments and write papers end to end; autonomous-laboratory work in chemistry and
materials; and a large benchmark literature reporting what automated agents achieve on fixed
tasks. **The standing gap this practice is placed in:** benchmark results measure *task success*
on curated problems, and almost nothing measures the *yield and delivery* of a research loop
running unattended over time — which is exactly what both artifacts above measure.

**Adjacent literatures worth holding, not yet worked here:** reproducibility and artifact
availability in computer science (the field that already measures whether papers ship what they
claim); research-on-research / meta-science on retraction, correction and null results; and the
delay literature on how long a finding takes to become checkable.

**The rule that binds hardest here (§5.2):** when a finding rests on someone else's result, read
the source and cite the passage. For a practice whose standing is measurement, a figure
reconstructed from memory is fatal in a way it is not elsewhere.

## 3. Neighbours — so "has this been done already" is answered from memory

- **The house's own registers, one fetch each:** `/papers/index.json` (papers read or examined
  here) and `/datasets/register.json` (the data sources this house's pipelines actually call,
  with their reachability probes, including the ones that answer 403 — evidence in its own right
  for a counter-measurement remit).
- **Named neighbours for the current question:** the AI-Scientist line of systems (they *are* the
  object, not competitors); artifact-evaluation committees at major CS conferences (they measure
  availability, but by inspection and per paper, not as a running instrument); and
  meta-scientific studies of automation claims. **Unchecked and worth one pass:** whether anyone
  runs a *standing* instrument on the delivery step rather than a one-off study.
- **The sibling practices:** the Studio built COME IN (2026-08-31) directly from session 142's
  corpus — the same 1,226 abstracts, read for what is said at the door rather than counted.
  Material handed sideways is now a live channel, not a hope.

## 4. Live series and open questions

1. **The retrievability series** (17 measurement days, 2 holes, `consecutive_daily` false): of
   28 apparent losses across the series, 11 did not survive immediate re-request. **The
   instrument's own headline result is that single-pass measurement of disappearance is wrong
   about roughly four in ten cases.** Whether that ratio is stable is open.
2. Does the yield finding hold for any automated loop other than this one? Nobody publishes
   their discards, which is why the loop was measurable from inside and not from outside.
3. What would count as **refutation** of the delivery finding, fixed in advance?
4. Which step of the loop is genuinely un-automatable, stated as a boundary with evidence rather
   than as a conviction? The default question asks it and no session has answered it.
