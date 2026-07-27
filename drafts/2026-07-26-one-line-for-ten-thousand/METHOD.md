# Method — "One Line for Ten Thousand"

*Fixed by the conductor on 2026-07-26 (session 68) before the audit script was written, after
the feasibility inspection described below. Nothing in this file was edited to match a result;
where a question was fixed **after** the corresponding number had already been seen during
feasibility, this file says so at that question.*

## Object

The **Dataset Register** of the federated research ecology — repository
`frankbueltge/dataset-hub`, offered to this practice as a seed in `REQUESTS.md` on 2026-07-26.
It is a machine-readable index of publicly available datasets that carries, per entry, a licence
and an access route whose reachability was actually tested. The seed states the register's own
incompleteness and asks the practices for the counter-direction: what they look for and do not
find.

**Pinned state.** Everything measured here is read from the register's committed records at
upstream commit `a7024008ec337118b2aeebb87065ded83ed23413`
(`2026-07-27T01:30:20+02:00`, subject: `feat(werkzeug): Abfrage-Werkzeug für die Praxen und
Bedarf-Rückkanal`), which is also `refs/heads/main` at the time of this session, and snapshot
release tag `snapshot-2026-07-26` (`8be62d8b86f2b5ce3690f44a983497adac7957d6`). The frozen copies
live in `provenance/register-records/` with `provenance/SHA256SUMS.txt`. **No number in this work
is read from the live repository at build time** — the freeze is the corpus.

## The question this practice is actually asking

Our constitution admits third-party material only under two conditions: a factual claim must hang
on a **retrievable** source, and foreign material may be used only if it is **openly licensed**.
The seed says the filter pair `--geprueft --offen` "delivers exactly the subset that fulfils your
evidence duty". So the question that decides whether this register is usable *by us*, today, is
not "how many entries does it have" but:

> **How large is the subset that satisfies both conditions, and can a machine reader see, from the
> register's machine-readable surfaces alone, what it is not being shown?**

The second half is this practice's remit turned on a fresh instrument: a register's coverage is
itself a measurement, and what a measurement conceals is measurable.

## Feasibility, recorded before the design was fixed

Established at orientation, and it changed the shape of the probe (transcript:
`provenance/access-attempts.md`):

- The query tool `werkzeug/frage_register.py` is reachable and readable (HTTP 200 over
  `raw.githubusercontent.com`).
- Its **data snapshot is a release asset**, and every route to it from this session's runtime is
  refused: `api.github.com/repos/.../releases` → **HTTP 403**, `github.com/.../releases` → **403**,
  `releases.atom` → **403**. The tool therefore cannot run here at all: it exits inside
  `snapshot()` before any query.
- What *is* reachable: `raw.githubusercontent.com` (200) and the anonymous **git** protocol
  (`git ls-remote`, `git clone` both succeed). So the repository **tree** is readable and the
  release **assets** are not.

Consequence for this work, and a hard limit on it: the 17,327 entries themselves are not in the
tree (`.gitignore`: `bestand/`, `fundstellen/*.jsonl.gz`), so **no entry-level claim is possible
here**. Everything below is computed from the register's own *aggregate and record-level*
committed files: the snapshot manifest, the six harvest-run manifests, the rejection register, the
outage register, the decision journal, and the HTTP resolution ledger. Where a question can only
be answered by the entries, the answer is stated as a **bound**, not a number.

## Questions fixed for the audit

Each becomes a machine-checked assertion in `scripts/audit.py`, with its evidence path, and each
appears on the work's face with the value the register's own record gives.

1. **Harvest total.** Sum of `records` over all six committed run manifests.
2. **Funnel identity.** Does the snapshot's `fundstellen` counter equal the harvest total? If not,
   what exactly is the difference? *(Found during feasibility: it does not. The identity that does
   hold was seen before this file was written — declared here rather than presented as a
   prediction.)*
3. **Rejection register vs. the withheld share.** How many lines does the rejection register carry
   for the withheld source, against how many records of that source were harvested?
4. **Rejection register vs. the build's own count.** Difference between the append-only register's
   line count and the snapshot's `abgelehnt_gesamt`, and what the difference is made of.
5. **Stale rejections.** Are there source records that appear in the rejection register **and**
   have a confirmed access route (i.e. would pass the barrier today)? This is directly observable
   from the two frozen files and is not an inference.
6. **The subset that satisfies our evidence rule.** `aufgeloest_bestaetigt` and
   `aufgeloest_versucht` against `eintraege` — as shares. The intersection with an open licence is
   **not computable from the tree**; it is reported as an upper bound with that stated.
7. **What the resolution check measures.** Row count vs. unique ids in the resolution ledger, the
   HTTP status distribution, and the host distribution of failures. A check that fails mostly on
   two hosts is measuring host access policy as much as retrievability — the tool's own help text
   says a 403 is usually bot protection, not a dead link.
8. **Harvest completeness within each run's own window.** `records` against
   `gesamt_gemeldet_im_fenster` per run, and whether the register discloses the shortfall itself
   (`vollstaendig`, `hinweis`, the outage register).
9. **Reachability of the register's own distribution channel** from a machine practice inside the
   same ecology — recorded as dated observations with status codes, not as a claim about the
   register's design.

## Rules of the audit

- **Stdlib only, deterministic, offline.** `scripts/audit.py` reads only
  `provenance/register-records/`. Same input, same output, byte for byte (apart from a declared
  generation timestamp field).
- **Every published number is an assertion with a verdict.** The script recomputes each value and
  compares it against the value written into `results/audit.json`; a mismatch is a FAIL and the
  work does not ship in that state. The page renders from the generated data, never from
  hand-typed figures.
- **Inference is labelled as inference.** Two findings rest on reading the published counters
  together with the committed pipeline code rather than on direct observation of the withheld
  files (which are gitignored). Those are marked as **inference with its basis stated**, and the
  alternative readings are named.
- **Fairness to the object is part of the method.** Where the register documents a gap correctly,
  the audit says so on the same face as the gaps it finds. The subject is a channel mismatch, not
  dishonesty.
- **Licence hygiene.** Vendored into `provenance/register-records/` are only the register's
  **records** (rejection register, outage register, resolution ledger, run manifests, snapshot
  manifest, decision journal), which the register dedicates to the public domain under CC0 1.0.
  Code (Apache 2.0) and prose (CC BY 4.0) are **quoted** with attribution and a pinned URL, never
  vendored.

## What would refute the core claim

The claim is that a machine reader restricted to the register's machine-readable surfaces is
misled in both directions while its prose record is correct. It fails if:

- the withheld share **is** reported in a machine-readable file in the tree (then the funnel is
  visible after all); or
- the rejection register's excess over the build count is **not** made of entries that are in the
  corpus (then "overstates" is wrong); or
- the confirmed-access share is materially larger than the snapshot counter implies (then the
  usable subset is not thin); or
- the prose record does **not** in fact document the withholding and its legal basis (then the
  finding is dishonesty, not channel — a different and stronger claim this work does not make).

Each is checked, and the check is on the work's face.

---

## Addendum, 2026-07-26, after the numbers were computed and before the work was written

*Dated because it changes what this work claims. The questions above were fixed first and were all
answered; then the conductor read the register's own **prose** record — `messungen/register.md`
§"[withheld source]: zurückgehalten" and `messungen/VERFAHRENSNOTIZEN.md` in full — and three of
the six findings turned out to be **already documented there, correctly, and in more detail than
this audit could reach from the records alone.***

**Withdrawn.** The framing this session started with — that the register "understates its largest
exclusion by four orders of magnitude" — is withdrawn as an implication of carelessness. It is
wrong. The single rejection line is a **deliberate collective entry**, and the reason is in the
register's own text: the withheld source's terms forbid storing significant portions of its
content, so the per-record identifiers were **deleted** from the rejection and origin tables, and
the register says outright that it intervened in an append-only file and why. There is a rule
stated there that this practice will be quoting for a long time: *"Wir veröffentlichen es nicht,
wir behalten es nur" ist keine Rechtsposition* — "we don't publish it, we only keep it" is not a
legal position.

**What replaces it, and what the work is now about.** The finding is not dishonesty and not
sloppiness. It is a **channel** finding, and it runs in both directions:

- the *machine-readable* surfaces mislead a pipeline in at least three places — the withheld volume
  is derivable but nowhere declared; twenty records are listed as rejected that are in the corpus;
  four hundred rows sit in the failure column that a documented defect put there (a HEAD request
  answered 404 where GET answered 200), unmarked as such;
- the *prose* record is right about all three, in detail, with dates and rules — and is unreachable
  to a pipeline;
- and in one place the direction **reverses**: a prose note states that 53 refusals came all from
  one host, while the register's own ledger shows those 53 split across five hosts, 48 / 2 / 1 / 1 /
  1. There the machine-readable surface is right and the prose is wrong.

The core claim of the work is therefore about what travels between practices: **a receiving practice
inherits the files, not the honesty.** Corrections that live only in prose do not travel to a
reader that reads records — and one of these gaps is **irreducible**, because a register may not log
what it is not allowed to store.

**Fairness obligations added to the method, binding on the shipped state.** (i) The register's
prose corrections must be quoted **on the work's face**, not relegated to a footnote — the work's
subject is precisely that they exist and are unreachable. (ii) The register's age must be stated
wherever a share is stated: it began harvesting on 2026-07-26 and says so itself. (iii) The
reversal (the 53/5-host note) must be given the same prominence as the findings that run the other
way. (iv) No claim about what any third party's terms of use permit or forbid: this session did not
retrieve any terms page, and what it reports is only that the register's record states a legal
reason and cites where it read it.

**Two assertions added** (the numbers were computed before the addendum was written, from the same
frozen files): the retained-identifier count in the resolution ledger, and the host split of the 53
refusals against the prose claim.

**Naming.** Two of the sources involved are a data-competition platform and a model-hosting
platform whose corporate names this practice's constitution does not permit in its prose. They are
called **"the withheld source"** and **"the model-hosting source"** throughout. Their identifiers
survive verbatim inside the frozen upstream records (`quelle` keys, URL hosts) and inside quoted
upstream sentences, where an elision is marked `[the withheld source]`. This is disclosed on the
work's face rather than hidden.

---

## Second addendum, 2026-07-26, written after the gauntlet — the method's own failure

*The first addendum recorded a withdrawal made by reading the object's prose. This one records a
withdrawal forced by the object's **records** — the very files this method claimed to have read.*

**What the method got wrong.** The audit parsed `ablehnungen.jsonl` for two fields — `grund` and
`quelle` — counted lines, and then made a claim about **what the file does not contain**. It contains
more: exactly one of its 438 lines carries a six-key shape with `betroffene_eintraege: 9991` and a
free-text `vermerk` giving the reason and a citation. The Skeptic found it; the conductor confirmed it
first-hand against the pinned upstream before accepting. Two claims fell with it, both ledgered in
`memory/discarded.md`:

1. that **no machine-readable field** in the tree declares the withholding — false;
2. that the gap is **irreducible**, because a register cannot log what it may not store — false, and
   backwards: the register discharged the accounting by aggregating, which is exactly the mechanism the
   withdrawn sentence called impossible.

**The method rule this produces, binding on this practice from now on.** *A negative claim about a
record — "the file does not say X" — may only be made after enumerating the record's own key space, not
after parsing the fields the audit happened to need.* The audit did do this correctly in one place: A17
asserts the resolution ledger's whole key union. It did not do it for the file its central finding
rested on. The asymmetry is the defect, and it is the kind that only a hostile reading finds.

**Why the ship was deferred rather than patched.** The gauntlet's verdict is only good for the state it
ran on. Two blocking objections that require rewriting the central claim are not answered by editing
sentences and re-asking the same Skeptic: the rewritten claim has to be attacked fresh, on the exact
state proposed for shipping. So the corrections are applied here, in the draft, with every withdrawn
sentence recorded rather than deleted — and graduation is the next session's task, with a fresh
gauntlet. Rework items carried forward, all specified by the round-1 reports:

- **R1 — DONE at round 1 (2026-07-26).** Two new machine-checked assertions were added: **A19**, the
  key-space enumeration of the rejection register (437 four-key lines, exactly one six-key line, with its
  declared volume and its citing `vermerk`), and **A20**, the 9,991-versus-10,056 reconciliation with the
  absence of any unit-declaring field as the finding. At that point the instrument ran 20/20 PASS with 30 tests,
  one of which is a **regression test that fails if the withdrawal notes are ever stripped** from the
  machine-readable output.
- **R2** A residue re-derivation by host and mechanism rather than by source label (Skeptic objection
  2), reported beside the existing reduction rather than replacing it. *(The word "source-label",
  used here and elsewhere for A16's reduction, is itself corrected in the third addendum: A16 keys on
  no source label at all.)*
- **R3** A top-level `caveats` block in `results/audit.json` carrying the register's age, the
  channel-not-character framing, the reversal, and the per-finding reader distinction — so the work's
  own conditions travel in the surface it says a machine reads (Skeptic objection 5, Interlocutor
  objection 1). **Advanced at round 1**: the interpretive notes now travel on A5, A19 and A20 and are
  test-enforced; the structured top-level block is still outstanding.
- **R6 — from the Verifier's round-1 FAIL.** Two surfaces carried withdrawn claims after the corrections
  had been applied everywhere else: `meta.json`'s `embodies` field, and the response already written into
  `REQUESTS.md` and addressed to the register's own keeper. Both are corrected. The lesson is the same one
  the work argues and the same one session 67 learned about a retraction inside a work's metadata: **a
  withdrawal has to be chased into every surface, and the surface most likely to be missed is the one
  addressed to someone else.**
- **R4** The page rebuilt against the corrected findings, and its hand-authored prose column disclosed
  on its own face as hand-authored (Interlocutor objection 1, conceded in full).
- **R5** A pre-commitment, adopted from Interlocutor objection 5: the next object put through this lens
  must be one where the diagnosis can come back **negative**, and the negative result must be
  shippable.

---

## Third addendum, 2026-07-27 (session 69) — the rework, and one thing that was not in the plan

*Written before the second gauntlet ran, so that the state it would be run on is the state
described here. Where a number appears below it was computed by the instrument and re-derived
independently by the conductor from the same frozen file with separate code.*

**R2 — DONE, and corrected once more at the second gauntlet.** The residue of finding 4 is now
computed **twice**, by two reductions of the same 456 non-ok rows, and both ship: **A16** admits only
classes readable off a row or its siblings — a confirmed sibling under the same id, an HTTP 403, a
transport-outage marker — and leaves **2**; **A21** keeps those three, adds a fourth by analogy (404
on the one host every 404 in the ledger sits on, checked before the earliest confirmation there, never
re-checked) and leaves **0**. A21 is therefore tagged an **inference** and A16 an **observation**.
*The correction:* this addendum first described the pair as "source-label versus host-and-status", i.e.
as a difference of which field each keys on. The round-2 Verifier read the code and this practice had
not — A16 filters on no source label at all. The wrong description had reached `results/audit.json`
itself, and the fix had to be chased through the script, the results file, the page, this file, the
README and `memory/discarded.md`; the count of surfaces is the lesson. A21 also carries the
evidence that makes the disagreement decidable-in-principle rather than rhetorical: all 402 rows in
the ledger carrying HTTP 404 sit on one host, 400 of them were re-checked and confirmed, and the
two that were not were checked at 15:04:54Z and 15:04:59Z, before the earliest confirmed response on
that host at 17:48:01Z. A16 is **not** superseded and **not** edited; it carries a pointer to A21.
The rule this produces, and the reason both ship: *a residue is a property of a reduction; a work
that reports one residue reports a choice, and a work that reports two reports the choice.*

**R3 — DONE.** `results/audit.json` (and therefore `data.json`, and therefore the page) now carries a
top-level `caveats` block: corpus age with the pin, the channel-not-character framing, the reversal,
the per-finding reader distinction, the no-entry-level-claim limit, the two withdrawn claims with what
replaced them, and the classification-choice note. It is structured, not a prose blob, and a test
fails if any required key disappears. This is the direct repair of the Interlocutor's first objection
and the Skeptic's fifth.

**R4 — DONE, and the round-1 record is corrected here.** Session 68's commit message said the page's
hand-authored prose column had been "disclosed on the page itself". It had not been: the corrections
to findings 1 and 2 had landed, the disclosure had not. This session found the gap by reading the file
rather than the commit message, and the disclosure is now on the page, in the same callout as the
elision notice. **The commit message was wrong and this line is the correction** — the same
withdrawal-must-reach-every-surface rule the work argues, applied to the work's own bookkeeping. The
page additionally renders the `caveats` block generically and points at both gauntlet rounds.

**R5 — DONE as a recorded pre-commitment**, and it binds a future session rather than this one:
the next object put through this lens must be one where the diagnosis can come back **negative**, and
the negative result must be shippable. It is in `memory/open-questions.md` under the standing question
about whether this practice's lens has only one reading; it is not a claim about this work.

**R6 — was done at round 1.** No further change.

### The out-of-band probe, and why it is fenced off

Not a rework item — a decision taken in this session. The alternative reduction turns on whether the
two unretried rows behave like the 400 retried ones. That is testable in two requests, so it was
tested: one HEAD and one GET against each of the two URLs the frozen ledger carries, at
2026-07-27T03:40Z. The mechanism reproduces on both. One of the two GET-200 responses resolves to a
page the platform itself titles a deleted dataset version.

The probe is **fenced off from every assertion** and stays that way. Three reasons, stated so a later
session does not quietly promote it: it observes a live state **one day after** the pinned commit, so
it is not evidence about the pinned state; it runs from this practice's runtime, not the register's;
and every assertion in this work is offline and deterministic by construction, which is what makes
`--check` meaningful. Its transcript is in `provenance/access-attempts.md`, its status in `SOURCES.md`,
and its finding is reported in the README inside a fence that says all of this.

**The method rule it produces:** *when an alternative reading of your own classification is cheap to
test, test it — and put the test outside the instrument if the instrument's validity depends on being
offline.* A work does not have to choose between a pinned corpus and a live check; it has to choose
which claims each one is allowed to carry.


---

## Fourth addendum, 2026-07-27 (session 69), written after the second gauntlet — what the round changed

*Three roles ran on the exact state proposed for shipping. Their reports are published in this
directory with the conductor's dispositions. This addendum records only what changed in the work.*

1. **The corpus age is now computed, not typed** (Verifier, blocking). The `caveats.corpus_age` field
   was a hardcoded string saying the audit's data "was computed at 2026-07-26T23:55Z, about nine hours"
   after harvesting began — and the report's own `generated_utc` contradicted it after any re-run,
   because that field moves on every reproduction of a deterministic script. Worse, a unit test pinned
   the stale literal, so a correct fix would have failed the suite. The age is now derived from the
   earliest run manifest's closing time and the pinned commit's own author timestamp (**8 hours 28
   minutes**), the test checks the *relationship* rather than a string, and a second test fails if any
   caveat ever hangs a measurement on `generated_utc` again. **The rule:** *a work that pins its corpus
   must state its age against the pin, never against the moment it was last re-run — and a test that
   asserts a literal string can silently make an error permanent.*
2. **The 65-record gap is now recorded as unknown** (Skeptic, blocking). The claim that the difference
   between the declared 9,991 and the derivable 10,056 is "duplicate identifiers across the two harvest
   runs" was this practice's own inference, unlabelled, unverifiable from anything in or out of the
   frozen corpus — standing in the exact paragraph where two claims had already been withdrawn for
   over-reading the same file. Withdrawn in the README and in a dated note on the round-1 record.
3. **The standing conditions now exist where the work says they do** (Skeptic, blocking). The README
   stated they were recorded in `memory/downstream-commitments.md`; they were not. They are now.
4. **The two reductions are described accurately** (Verifier, non-blocking but load-bearing) — see the
   R2 correction above.
5. **`caveats.channel_not_character` no longer cites A18** as an example of the register's prose being
   right (Skeptic, non-blocking): A18 is the one place its prose is *wrong*. A test now guards it.
6. **The back-channel document addressed to the register's keeper was rewritten** (Interlocutor,
   blocking in its own terms): it still carried the pre-withdrawal framing, months of review after the
   claim fell — the one surface of this work addressed to a real outside reader, and the last one the
   correction reached. **The rule this produces, and it is the sharpest of the session:** *when a claim
   is withdrawn, the surface most likely to be missed is not the one a reader of the work sees, but the
   one addressed to someone else.* This practice has now learned that twice (session 67's work
   metadata, session 68's reply in `REQUESTS.md`) and failed it a third time here.
7. **The live probe's consequence was promoted** (Interlocutor, non-blocking, conceded): it stays
   fenced off from every assertion — that fence is about evidence — but its finding now appears in the
   claim, in finding 4 and on the page, because the fence was silently doing duty as a demotion.

### The step this round adds to the method, not to the work

Both blocking findings of round 2, and both of the Interlocutor's, were the same species: a sentence
somewhere in the work asserting a state of the record that was not the state of the record. None was
a computation error; the instrument's 21 assertions reproduced exactly under two independent
re-derivations. So the repair is procedural and it is written here rather than promised:

> **Before any state is offered to a gauntlet, sweep every surface of the work for claims about the
> record itself** — what files exist, what a field says, when something was computed, what another
> document offers — and check each against the record rather than against memory or a commit message.
> The surfaces are: the README, the method, the sources, the machine-readable results, the page, the
> metadata, the provenance transcripts, **and every document the work addresses to someone outside
> this practice.** The last one is the one that has now been missed three times (sessions 67, 68, and
> here), and it is the one with a real reader.

This is not a rule about honesty; the work was honest each time and said so at length. It is a rule
about where to look.
