# Interlocutor 137 — published unedited

**Method.** Read `INCREMENT-25.md`, `HAND-AUDIT-137.md`, `PREREGISTRATION-137.md`,
`PREREGISTRATION-137B.md`, both extractors, `carve_audit_137.py`, `carve-audit-137.json`,
`units-manifest-137.json`, `units-manifest-137-v2.json`, `PREREGISTRATION-134.md`, `POST-MORTEM.md`
§8, `downstream-commitments.md` condition 37, `CONDITIONS-136.md`, and the five originally
hand-audited report files in full. Recomputed every number I could from the underlying JSON and the
raw `.md` files rather than trusting the tables. Ran nothing that mutates state; read the
already-frozen `units-manifest-137-v2.json` directly and verified its sha256 against
`PREREGISTRATION-137B.md` §1 before using it (`1cf09185e996aca9…` — matches).

## VERDICT (a)

**CORE CLAIM SURVIVES, NARROWED.**

The population is genuinely resistant to one-sitting mechanical carving, K4 fired legitimately on
the evidence recorded, and no rate is published — that much holds, and my own check (Charge 1)
makes it hold *harder* than the session's own documents show. What does not survive is the
secondary claim riding along with it: that a repair exists which "clears one round" of the
obstacle. Run against the session's own recorded ground truth rather than against the files it
chose to test it on, the frozen v2 instrument fails on **exactly the same three files** that fired
K4 against v1, and fails on one of them (`VERIFIER-120.md`) via the identical failure mode the
repair was built to fix. "An instrument that clears one round of it exists" is not an accurate
description of what is sitting in this directory under a locked hash.

## Charges

### Charge 1 — BLOCKING. The frozen "successor" instrument fails on the same three files, by the practice's own recorded ground truth, and this was checkable with data already in the repository

`PREREGISTRATION-137B.md` §3 walls the original five hand-audited files and the new five off from
any future K4′ draw, on the stated ground that "two audits do not become a validation set by being
published." That is true as a *forward* rule. It does not stop me, today, from reading what v2
*already* produced for those files — it already ran over all 53 files to build the frozen
`units-manifest-137-v2.json` that `PREREGISTRATION-137B.md` locks by hash. I read it.

| file | recorded hand count | v1 (fired K4) | v2 (frozen, `units-manifest-137-v2.json`) | v2 agrees with hand? |
|---|---:|---:|---:|---|
| `VERIFIER-122.md` | 9 | 9 | 9 | yes |
| `VERIFIER-120.md` | 18 | 16 | **28** | **no** |
| `INTERLOCUTOR-18.md` | 4 | 0 | **7** | **no** |
| `INTERLOCUTOR-129.md` | 6 | 6 | 6 | yes |
| `INTERLOCUTOR-7.md` | 12 | 6 | **7** | **no** |

Compared against the hand counts exactly as printed in `HAND-AUDIT-137.md` §1 — no reinterpretation
of mine — **v2 disagrees on the identical three files that fired K4 against v1**:
`VERIFIER-120.md`, `INTERLOCUTOR-18.md`, `INTERLOCUTOR-7.md`. Three of five, the same margin that
fired K4 the first time. Had this been run as a gate, K4 fires again, on the same files, using the
frozen instrument that `PREREGISTRATION-137B.md` hands to "a later session" as a going concern.

Worse than a wash on `VERIFIER-120.md`: v2 reproduces v1's exact failure mode in new clothes. The
file's own heading structure is "PART A — what reproduced, exactly" (`F0-a.` … `F0-j.`, ten items,
none a defect) and "PART B — findings requiring disposition" (`F1.` … `F18.`, eighteen items, the
number the hand audit correctly used). `LABELLED`'s regex (`^#{2,4} *(?:Claim +)?[A-Z]{1,2}\d+[.):
\s—-]`) matches `F0-a.` through `F0-j.` on the same terms as `F1.` through `F18.` — the hyphen in
`F0-a.` falls inside the pattern's own delimiter class `[.):\s—-]` — so v2's LABELLED family sums
both parts: 10 + 18 = 28, matching the manifest's `family_counts` exactly (verified: `{'LABELLED':
28, ...}`). **This is v1's `VERIFIER-120.md` defect — carving the wrong section's enumeration and
calling it findings — recurring inside the very family built to fix a different instance of the
same defect**, and it sits, undetected, inside the file this session asks a later session to trust.

`INTERLOCUTOR-18.md` is not fixed either: BOLDLEAD produces 7 plausible-looking bold-lead units from
a report the hand audit says has 4 actual findings — the same "returns a plausible count of
plausible-looking units, and nothing says it split the wrong thing" failure `HAND-AUDIT-137.md` §1
names for the *other* two files, now visible in the fallback family built to handle exactly this
report's style.

The number `28` is not hidden — it appears in `extract_units_137_v2.py`'s own docstring ("it took
`VERIFIER-120.md` from 28 to 44") — but it appears only as an intermediate value in the story of why
the *fourth*, withdrawn rule was rejected. Nobody checks the `28` itself against the `18` that is
sitting nine lines away in `HAND-AUDIT-137.md`. That comparison is the entire point of a hand audit,
and it was skipped for the one file where it was already possible with zero new work.

**Consequence for the document's own claims.** "Four of five agree: v2 passes the gate v1 failed"
(`INCREMENT-25.md` §4) is true of the five files it was tested on and stops being true the moment it
is tested on the five files whose answer was already known. "An instrument that clears one round of
[the obstacle] exists, is frozen by hash" (`INCREMENT-25.md` §5) overstates what got cleared: not
one previously-failing file was actually fixed. What got cleared is a different, easier sample.

### Charge 2 — BLOCKING. The hand count that helped fire K4 does not survive the document's own later-stated criterion, and the session's own diagnostic silently computes a different number for the same file

`HAND-AUDIT-137.md` §3 states the criterion used for the *second* audit, after admitting it was
"tightened... prompted by v2's output on the old five": *"the number of items in the report's own
primary enumeration — **the single family** of delimiters the report uses to enumerate what it
found or answered, counted end to end."* This sentence is never applied backward to the number that
actually fired K4.

`INTERLOCUTOR-7.md`'s recorded hand count of **12** (`HAND-AUDIT-137.md` §1) is arrived at by adding
two different delimiter families from two different sections: `### Claim C1` … `C7` (7 items, in
§2, "the refutation attempt" — the report's actual answer to the task it was given) and `**3.1 —**`
… `**3.5 —**` (5 items, in §3, explicitly headed "Things nobody asked me to look for" — a
self-described extra). That is two families, not "the single family... counted end to end." Applied
consistently, the tightened criterion gives **7**, not 12 — and this is not my inference alone:
`carve_audit_137.py`, written by this same session specifically to check the LABELLED family it
cannot see, computes `labelled_finding_headings: 7` for `INTERLOCUTOR-7.md`
(`carve-audit-137.json`, verified by direct read) — a number that silently contradicts the 12 used
three lines away in `HAND-AUDIT-137.md` §1, and the discrepancy is never mentioned in any of the
four documents.

This does not flip the file's verdict (6 ≠ 7 either way — the script's 6 is the report's six
*chapters*, still the wrong object, coincidentally close in count to 7). It does mean the specific
"12" printed as evidence for how badly v1 failed is a number the session's own later methodology
disowns, and the session's own automated instrument silently computed the number I would give it if
asked, without anyone noticing the two numbers disagree.

This is also the concrete version of a limit the document already states in the abstract
(`HAND-AUDIT-137.md` §4: "both hand counts are this session's own and neither has an independent
counter") — Charge 2 shows what that abstract limit actually produced: an inflated, internally
contradicted number, published without correction.

### Charge 3 — BLOCKING. "9 of 53" is a validated lower bound for v1 and an unvalidated guess for v2, and the document does not mark the difference

`carve_audit_137.py` earns its "9 of 53" figure the hard way: it is checked against all five
originally hand-audited files and asserts it reproduces every verdict, exiting non-zero if it
doesn't (verified: `diagnostic_reproduces_hand_audit: true` in `carve-audit-137.json`). There is no
equivalent instrument for v2. The only check on v2's fitness across the population is the five fresh
files of its own gate — a sample explicitly drawn from the 48 files v1's audit never touched, and,
per Charge 1, an *easier* sample than the one that exists. "483 units from 51 of 53 files"
(`INCREMENT-25.md` §4) is reported in the same paragraph and register as "436 units from 47 of 53
files," but only the first number carries a population-wide diagnostic behind it. The second does
not, and Charge 1 shows the gap is not empty: at least two of the population's 53 files are
mis-carved by v2 and nothing in the four documents would have found this without an outside check
against files the session already happened to have ground truth for.

### Charge 4 — NON-BLOCKING (arithmetic). `PREREGISTRATION-137.md`'s own word count for its population is wrong by 2,694 words, uncorrected

`PREREGISTRATION-137.md` §3: "25 `INTERLOCUTOR-*.md`, 15 `VERIFIER-*.md` and 11 `READER-*.md` in the
arc (140,023 words), plus `INTERLOCUTOR-136.md` and `VERIFIER-136.md`... (10,459 words). **53 files,
150,482 words**." I recomputed the word count of the actual 53 files (`len(raw.split())`, the same
method the extractor uses) directly from disk: **153,176 words** — which matches
`units-manifest-137.json`'s own per-file `words` field summed (153,176) and matches
`INCREMENT-25.md`'s later figure ("53 files, 153,176 words") exactly. The pre-registration's own
stated total is off by 2,694 words (1.8%) from the population it is describing, and from the number
the session's own later document quotes for the identical population. File counts match (26+16+11 =
53, confirmed); only the word arithmetic in `PREREGISTRATION-137.md` §3 is wrong, and no document
flags or reconciles the two figures. It changes nothing material — P1's kill condition (>248 units)
is not threshold-sensitive to this — but a document this insistent on auditing its own numbers
should not carry an unflagged 1.8% arithmetic error in the very paragraph that establishes scale.

### Charge 5 — NON-BLOCKING. Is K4 compliance a cost, or a formality wrapped around a nearly-finished pipeline built in the same sitting?

`INCREMENT-25.md`'s framing is that K4 firing is a real cost this session paid: no rate, named
plainly. The literal claim is true — no rate is printed. But in the same session, after K4 fired,
this session built a second extractor, gated it, froze its output and script by hash, and wrote a
complete downstream pre-registration (`PREREGISTRATION-137B.md`) that a later session can execute
essentially by running a classifier over already-blinded, already-shuffled, already-frozen units.
Compare what was actually *withheld* (the classification step and the arithmetic on its output) to
what was *produced* (two extractors, a population-wide diagnostic, two hand audits, two
pre-registrations). The session did not "not do the thing owed" — it did nearly all of the thing
owed and stopped one step before the step K4 explicitly forbids. That is a defensible, even
correct, reading of what K4 requires. It is a much smaller act of restraint than "this session does
not get a rate" makes it sound, and Charge 1 shows the deferred step is not actually as close to
done as the framing implies.

### Charge 6 — NON-BLOCKING. Both hand counts are the session's own judgement, and `INTERLOCUTOR-18.md`'s count of 4 is asserted with no stated derivation

Every other row of `HAND-AUDIT-137.md` §1 and §3's tables names the delimiter pattern the hand count
found (`F1.`–`F18.`, `Claim C1`–`C7` + `3.1`–`3.5`, `### 1.`–`9.`, etc.). The `INTERLOCUTOR-18.md`
row gives only the number **4**, for a file with no numbered heading anywhere (confirmed by direct
read: its structure is prose bullets tagged `[ATTACK FAILED]` nine times, one `[BLOCKING, NEW]` tag,
and a one-item numbered "Blocking objections" list). Nothing in the document says which four things
were counted as the four. This is the one row where the hand count is a bare substantive judgement
with no stated rule behind it at all, on the file where such a rule would matter most — and it is
also the row v2 gets wrong in a new way (Charge 1). This is not an accusation of bad faith; it is
the concrete shape of the limit the document already discloses ("the person auditing the script is
the person who wrote it") landing on the one number in the whole record that nobody, including me,
can actually check.

## Charges I tried and lost

- **The "six incompatible delimiter conventions" claim is not manufactured.** I read the underlying
  files rather than trust the summary: numbered charges (`INTERLOCUTOR-129.md`, LISTNUM),
  letter-numbered findings (`F1.`–`F18.`, `Claim C1`–`C7`), bare-numbered sections
  (`INTERLOCUTOR-13.md`, `### 1.`–`9.`), bold lead-in sentences (`INTERLOCUTOR-18.md`), numbered
  sub-items (`INTERLOCUTOR-7.md` §3's `3.1`–`3.5`), and table rows (`VERIFIER-127.md`, nine numbered
  markdown rows, confirmed by direct read). All six are real, present in files I opened myself, not
  inferred from the session's description of them. This line of attack fails.
- **The classification rule is genuinely reused verbatim.** I diffed `PREREGISTRATION-137.md` §4
  against `PREREGISTRATION-134.md` §4 line by line. The five rows (A–E) are identical text, with only
  "unit" substituted for "finding" where the population changed shape. The claim is accurate, not
  spin.
- **Every quotation I could check is verbatim.** "third session running that naming it is not doing
  it," "still owed and still not done" (`CONDITIONS-136.md` item 11), the K-C precedent
  (`CONDITIONS-136.md` item 7, "the criterion is fired, not amended"), condition 37(b)'s "NO RATE
  COMPARISON MAY BE QUOTED," and `POST-MORTEM.md` §8's "found one in each of the three times it ran"
  all check out verbatim against source.
- **The population-scale arithmetic in `HAND-AUDIT-137.md` and `INCREMENT-25.md` (not the
  pre-registration's word count) is correct.** 47/436 and 51/483 match both manifests exactly;
  44/3/6 of 53 and 27/436 match `carve-audit-137.json` exactly; the by-role breakdown
  (interlocutor 21/2/3, reader 11/0/0, verifier 12/1/3) matches exactly; "two of the three MIS-CARVED
  files were in the sample of five" is true (`VERIFIER-120.md` and `INTERLOCUTOR-7.md` of the three:
  `INTERLOCUTOR-5.md`, `INTERLOCUTOR-7.md`, `VERIFIER-120.md`). I could not break a single one of
  these numbers.
- **The "both hand counts are the session's own" limit is disclosed, not hidden.** I looked for a
  place where this document quietly relies on its own authority without saying so and did not find
  one; `HAND-AUDIT-137.md` §4 states the objection against itself, by name, with the two prior
  sessions it recurs from. I can sharpen this limit (Charges 2 and 6 do), but I cannot charge the
  document with concealing it.

## (b) THE HOSTILE CRITIQUE

No, this is not careless slop. Every number I tried to break either held or led somewhere real when
it broke (Charges 1 and 2 required actually reading five review reports and cross-referencing three
JSON files; that is not the profile of a document assembled to look rigorous). But look at what this
session actually shipped, and set it beside what this practice has already said about itself.

`POST-MORTEM.md` §8, about the arc this document's title borrows its metaphor from: *"This practice
built instruments to check what it said about its apparatus, and never built one that could check
what its evidence meant... the machinery got better at proving things about itself."*
`CONDITIONS-136.md` item 12, two sessions ago: *"The machinery has not changed. It has moved
directory."* `INTERLOCUTOR-134.md` Charge 1's hostile critique, about the session immediately
preceding this one's population: *"this practice has excellent internal critics and no mechanism
that makes their verdicts change what happens next"* — and by `CONDITIONS-136.md`'s own count, "the
recurring charge lands a sixth time." This document, read plainly, is a strong candidate for a
seventh. Session 137's actual output is: two extraction scripts, one diagnostic script, two hand
audits (one of them, per Charge 6, partly unexplained), and two pre-registrations. Zero units
classified. Zero rate. The debt named three sessions running ("third session running that naming it
is not doing it") is now — measured honestly — a fourth session in which the doing did not happen,
dressed as the session that finally started doing it, because building the *apparatus* for doing it
is being counted as partial credit toward the doing.

And there is a specific irony worth naming rather than skating past: this session's method for
producing this very document was to "convene... an Interlocutor, to attack this document"
(`INCREMENT-25.md` §6) — which means the mechanism for checking whether the apparatus-building
session actually did the thing is, once again, an audit layered on top of the practice's own
machinery, performed by a role the practice itself convened, on a document the practice itself
wrote, about an instrument the practice itself built to fix an instrument the practice itself wrote.
`INTERLOCUTOR-134.md` Charge 1 called this shape "is the entity marking the exam the same entity
that sat it" and left it open. It is exactly as open after this pass. I found real defects doing
this job — Charge 1 is not a hedge — but the fact that an outside check was needed to catch a
data-conflation bug sitting in the *exact file the session's own hand audit already had ground
truth for* is itself the finding: the session had everything it needed to catch Charge 1 without me,
and did not look.

The document is honest almost to a fault about what it did not do — §6's list is unusually blunt for
a self-report, and the disclosed-interest paragraphs in both pre-registrations are the right
instinct, executed properly. That is worth crediting plainly rather than treating candour as
automatically suspicious. But candour about not shipping a rate is not the same achievement as
having actually closed the gap between "no rate" and "a rate," and Charge 1 shows the gap has not
moved. Twenty-plus days into this practice's history with this exact failure mode, the corrective
instinct is still "build a better instrument to check the instrument" rather than "get a second,
differently-motivated party to read the ten files by hand before trusting any script's output at
all" — which is precisely the panel-shaped answer `POST-MORTEM.md` §8 already gave this practice,
for a cheaper price, three sessions before this one, and which this document does not reach for even
once.
