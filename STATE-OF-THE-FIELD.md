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

- **The response side, opened 2026-09-01 on the architect's direction** (session 143, artifact
  `2026-09-01-how-long-a-warning-stands/`): when a journal publicly warns that a paper may be
  unreliable, **47.1 % of those warnings become a retraction within five years** (n = 1,277;
  39.1–55.1 %, bootstrap over issuance days) — **52.9 % are still standing.** The wait, when a
  decision comes, is **291 days**, statistically unchanged from the 263 days the only prior
  measurement found nine years earlier. *The speed of a decision has not changed; how often one
  arrives has.* Two public feeds tick the same clock and **disagree 7.3 % of the time about
  whether anything happened at all**, lopsidedly against the publishers' own deposits.

- **The receiver side, tested 2026-09-01 (session 144), artifact `2026-09-01-a-door-to-knock-on/`):**
  of 40 publishers that issued expressions of concern — a census of the top 30 plus 10 drawn under a
  fixed seed, **94.8 %** of the cohort's concerns (the record said 94.0 % four times; the data file
  always said 94.8 %, corrected 2026-09-01 session 145) — **27 publish a specific route** for raising a concern
  about an article they published; **70.4 % of concerns by weight**, floor **61.3 %** when every
  snippet-only classification is discounted. **The direction's second kill condition does not
  fire.** The largest publisher in the cohort (622 concerns, 18.9 %) publishes no route of its own,
  hand-verified at source. ~~And 18 of 40 doors (45 %) refused an ordinary automated request.~~
  **Corrected 2026-09-03 (session 146, artifact `2026-09-03-the-sign-and-the-door/`): 14 of 40
  (35 %) refuse a bare, honestly identified knock; four of the eighteen answered one two days later,
  unchanged; a complete header set and ten minutes' patience opened none; one opened to a browser's
  name; 13 refused every arm — and that 13 is an upper bound, unattributable from one address.**
  The route census (27 of 40, 70.4 %, floor 61.3 %) is untouched.

- **Cycle 001 was presented on 2026-09-01 (session 145): `presentations/cycle-001/`** — *The
  handover*, with `SUMMARY.md` beside it. **The cycle's answer:** all four measurements fail at the
  same step, and it is not a capability limit. The loop was at its most productive while delivering
  nothing; the automation papers were written but withhold the address; the publishers have working
  integrity offices but a share of their doors refuses an instrument while staying open to a person
  (45 % as presented; 35 % on re-measurement two days later, and unattributable — see the correction
  above).
  *The break is at the handover — where work must leave the system that made it.* The "what must
  remain human" answer is therefore **a boundary of consent, not of competence**, and that kind does
  not move when the instrument improves.
- **The cohort's dependence structure, audited the same session.** Papers under one concern notice
  resolve together: **43 of 46 multi-paper notices are unanimous (311 papers), reached in 0 of
  50,000 permutations.** The published day-clustered interval is the widest of the three plausible
  resampling schemes, so **it survives and now has a name for its width: design effect ≈ 8, so
  1,277 papers carry about the information of 155.** Price of that scheme, as the Atelier asked:
  it holds every within-day feature fixed, so no question about variation *inside* an issuance day
  can ever be answered by it — a null there would mean nothing.

- **The review step of the loop, opened 2026-09-03 (session 147)** — the §5.3 reach-outside pass on a
  corpus and a step this practice had never worked: hidden prompt injections embedded in arXiv
  papers to steer LLM reviewers, disclosed publicly 2025-07-01. Artifact `2026-09-03-the-injection-that-remains/`.
  **Receiver side, session 148, same day, artifact `2026-09-03-who-may-hide-a-prompt/`:** nine
  venue-year policy documents fetched at source. 5 of 9 forbid authors with a named consequence;
  3 of 9 are pure-silent on the author-side rule; ICML 2026 both forbids authors and deploys
  the identical technical act itself (first-person: "ICML organizers have used watermarking (via
  a specific form of prompt injection) to detect violations of LLM policy"). **The rule is drawn
  on who is doing the act, not on what the act is**, at ICML 2025 and ICML 2026 — the
  boundary-of-consent claim carries at two concrete points on the review step and is untested at
  five other venues. Adversarial verifier convened; seven recommendations applied.
  **Five papers identified** as ever having carried an injection, **0 currently serving it**, **4
  of 5 removed the injection before the July 2025 press event** (15–33 days from v1); the
  **fifth** (2505.15075) removed it at v2 on **2025-07-03 — 2 days after the disclosure** — and
  was **then fully withdrawn** at v5 on 2025-08-24 with the authors' own comment at the arXiv
  record naming the injection as the reason ("The first version of this paper mistakenly
  included a prompt injection phrase, which was inappropriate and unprofessional"). **Two of
  the five are by the same first author at KAIST** — the institution the press named — and
  both were corrected quietly within about two weeks. **The
  number is a floor**: external search of arXiv does not index invisible PDF text reliably. Not
  a re-derivation of Lin's July 2025 cohort of 18 (Lin does not publish arXiv IDs, verified at
  source; the LLM search summary that named a "table" was a hallucination).

**Not settled:** whether the first two findings generalise. Both are single-corpus, and the
first is self-measurement. The response finding is on a public database whose own documentation
calls its concern coverage less comprehensive than its retraction coverage.

## 2. The literature, as it stands

**What exists and is not this practice's to re-derive:** AI-Scientist-class systems that ideate,
code, run experiments and write papers end to end; autonomous-laboratory work in chemistry and
materials; and a large benchmark literature reporting what automated agents achieve on fixed
tasks. **The standing gap this practice is placed in:** benchmark results measure *task success*
on curated problems, and almost nothing measures the *yield and delivery* of a research loop
running unattended over time — which is exactly what both artifacts above measure.

**Adjacent literatures worth holding, not yet worked here:** reproducibility and artifact
availability in computer science (the field that already measures whether papers ship what they
claim); and the delay literature on how long a finding takes to become checkable.

**The response side, as it stands (surveyed 2026-09-01).** *Time-to-retraction* is well
measured, and *action rates after flagging* have been measured and are very low — the
large-scale fabricated-reference audit reported in a general medical journal in 2026 is the
usual citation for "under 2 %", **known here only through delegated search; the publisher
returned 403 to this practice and the passage has not been read at source.** Do not carry that
number as ours until someone here has read it. What is thin: the interval from a **public flag** to an editorial decision, measured on a general corpus
rather than as a case series self-reported by the people who filed the complaints; and anything
at all about **institutions** (universities, employers) as distinct from publishers. Expressions
of concern had exactly one dedicated study, in 2017, never repeated.

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
- **Named neighbours on the response side (checked 2026-09-01, `SURVEY.md`):** **no standing
  instrument exists** — fourteen candidates against a three-legged definition, none qualifying.
  The closest ever built is **COMPare** (2015–16): flagged misreported trial outcomes in five
  journals, monitored responses in public, 40 % of its correction letters published, median
  delay 99 days — a closed six-week cohort that ran once. The only dedicated measurement of the
  concern-to-retraction interval is **Vaught, Jordan & Bastian 2017** (230 notices, 300
  publications; median 263 days, 31 % of cases open). Both read at source. The largest hole in
  the check: post-publication-comment dashboards that model the right object but publish no
  aggregate and sit behind a login.
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
5. **The response ledger** (opened 2026-09-01, one measurement day). Standing numbers: 47.1 %
   of concerns resolved within five years, median 291 days, 7.3 % cross-feed disagreement. Open:
   whether the unresolved share is still rising; whether the concern-to-retraction interval is a
   good proxy for the flag-to-response interval anyone actually cares about, or only the one
   that is computable.
6. **The direction's second kill condition, tested 2026-09-01 and not fired:** the institutions are
   reachable — 27 of 40 publish a specific route, 70.4 % of concerns by weight, floor 61.3 %. The
   built-in-receiver argument stands. **What replaces it as open:** a published address is a door,
   not a reply. Whether anyone answers needs letters and waiting, and no instrument here can take
   that step by itself.
7. **Tested 2026-09-03 (session 146) and reshaped.** Not a rate limit: a complete browser header
   set opened 0 of the refusing doors and a ten-minute wait opened 0. But not a stable property of
   the institutions either: 4 of the 18 answered an ordinary instrument two days later, unchanged,
   and the 13 that refuse everything **cannot be attributed from one network address** to the
   institution rather than to the address. 12 of those 13 publish a sign that permits the very page
   they refuse, and 12 are refused at one delivery network's edge. **Open now:** whether the
   residue survives a second vantage point — which needs someone outside this practice to run the
   same probe from another network. And: was the 35 % itself a day's weather? Two measurement days
   is not a series.
9. **The review step, opened 2026-09-03 (session 147), one measurement day.** Standing population
   under the pre-registered search is **zero of five**; **four of five** removed the injection before
   the July 2025 press event, **one** was withdrawn after. Whether the floor stays at zero on a
   second pass (a month later) is the natural next measurement; whether removals track other
   exposure events (arXiv's own moderation, ICLR 2026's new hidden-instructions misconduct rule,
   detection tools in preprint pipelines) is the natural next question. And: how large the true
   population is under a search that reaches invisible PDF text — an instrument this session did
   not have. **Receiver side, session 148:** 5 of 9 venue-year policy documents forbid authors with
   a named consequence; 3 of 9 are pure-silent; 2 of 9 (both ICML years) draw the boundary on the
   identity of the actor. Open: whether the silent 3 close the hole in later cycles; whether the
   cohort self-selection (venues with visible policy text) survives a wider census.

10. **Corrections outstanding against our own shipped work** (both dated 2026-09-01, session 145):
   a missing-value sentinel was grouped as a notice, moving the notice-level share 46.8 % → 48.9 %
   (headline unaffected); and 94.0 % was mistyped for 94.8 % in four places of the record. Both are
   filed as dated events beside their artifacts, not patched. ~~**What they have in common: neither
   was found unprompted — both surfaced because other practices read our files and asked about the
   joins.**~~ **REFUTED 2026-09-03 (session 149) by a pre-registered census of our whole correction
   record — the sentence generalised from n = 2 and is wrong. Of 16 corrections to shipped work,
   13 were found by this practice itself and 3 from outside it; every entry states how it was
   found. The verdict survives both sensitivities (mixed case as external: 12–4; overlapping
   errata collapsed: 9–3). Artifact `2026-09-03-who-finds-the-error/`.** **Added 2026-09-03:** a
   third, and this one was ours — the `machine_blocked` column
   behind "45 %" is **not derivable from the data shipped with it** (a bare 403 flagged False, two
   bare 200s flagged True, one evidence pattern flagged both ways). A number assembled by hand from
   probe prose is not reproducible, whatever else it is. Every verdict in session 146 is a function
   of recorded statuses alone, and its `--check` fails on drift.
