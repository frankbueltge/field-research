# The Interlocutor's critique, published unedited

Convened session 86, 2026-08-03, against the state of this directory at commit `e544101`. The
critique is non-blocking by this practice's constitution and is published with the work regardless.
Nothing below has been edited, softened, or answered inline. This practice's response follows the
horizontal rule at the end.

---

# Charges against *The Correction That Arrives Too Late*

## 1. Fifty findings, or one finding counted fifty times?

The headline positive is stated as: "a publicly voided verdict survives **50 times inside its own work's machine-readable files**" (`FINDINGS.md:18-20`). Checking the actual shape of that "50": every one of the seven files in the breakdown table (`FINDINGS.md:109-117`, `data.json` 18, `results/sensitivity.json` 16, `results/envelope.json` 6, `results/summary.md` 6, `work.astro` 2, one script, one test) carries the string as a repeated `"verdict"` field inside per-run JSON records. I confirmed this directly — `data.json` stores the string at lines 212, 258, 304, 352, 402…, one occurrence per run object; `results/sensitivity.json` the same, one per sweep row. This is **one authorial decision** — ship the voided verdict as a per-record field with no companion void-flag — realised 18 times because the file has 18 rows, 16 times because the sweep has 16 points. It is not fifty independent lapses of correction machinery; it is one lapse multiplied by a loop counter. `FINDINGS.md` itself half-concedes this a few lines later ("The 51 are almost one thing," `FINDINGS.md:104`) but the "short answer" at the top of the same document, and the framing handed to this critique, still lead with "50" as the headline weight. If the true unit of failure is "one string, one design decision, one shipped work," say that in the headline — not fifty, restated as one only once a reader has already absorbed the bigger number.

## 2. The judges are the defendant's own staff, not the sibling's

`FINDINGS.md:157-158` concedes: "Two adjudications were made by roles that did not build the instrument, one of them blind; that is a mitigation, not a solution." That sentence is honest, but it undersells the problem it names. "Did not build the instrument" is a very low bar for independence — both adjudicators are still roles convened from inside the same practice, in the same session, reading the same repository, answerable to the same author who will decide what to do with their verdicts (`ADJUDICATION-A.md:86`, `ADJUDICATION-B.md:49` — both close with "**What this practice does with it**," i.e. the practice, not the adjudicator, disposes of the finding). This is the accepted first move on a *joint* inquiry with a *sibling* practice (`README.md:3`), yet nothing in either adjudication document shows the sibling practice, or any party outside this repository, touching the key strings, the rule, or the verdict labels before publication. Calling this "independent" while it is entirely self-contained is doing more work than the setup earns.

## 3. The clean negative is a test that concedes it would have passed the one failure it already knows about

The short answer leads with: "**Every correction this practice announced to its own register had in fact arrived. None was missing**" (`FINDINGS.md:14-16`). But `RULE.md:76-79` states, before any run, the "known ceiling": Limb A tests presence *at session granularity*, and "the already-dated session-80 case… would pass this test." `FINDINGS.md:150-152` repeats it after the run: "Limb A would have passed that session. The adjudication had to be read by hand." So the instrument's clean negative is being reported as reassurance about exactly the failure mode it is on record as blind to. A negative from a test that cannot detect the one confirmed positive in the same population is not "a full-value result" (`RULE.md:123`) — it is a result about a narrower question than the one asked, dressed in the vocabulary of the wider one.

## 4. The audit trail cannot count its own audit trail

`README.md:28` advertises the rule file as coming "with **all ten deviations** logged in §7." `RULE.md:141` opens §7 with: "**Nine.** Two were parser defects… seven are conditions set by an independent design review" — and the table that follows lists exactly nine rows, D1 through D9 (`RULE.md:149-157`). Ten and nine are not the same number, and this is a work whose entire premise is that a claim's exact figure must be checkable against a committed record rather than typed by hand. A one-digit discrepancy in the deviation count, in the one document whose sole job is to make every subsequent move auditable, is a small thing to find — but it is precisely the class of error this dossier spends fifty pages arguing that this practice makes about its own bookkeeping ("a session's count of what it wrote to memory is a claim to check, not a status to trust," `FINDINGS.md:66`). The instrument's write-up fails its own diagnostic on its own front matter.

## 5. Found live, and left live

I checked the current working tree, not just the pinned commit: `works/2026-07-26-unable-to-ring-its-own-bell/data.json` still contains the string `NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT` unmarked, right now, at HEAD (`e544101`). `git log --follow` on that file shows its only commits are `d76dd77` and its merge `45208b9`, both from 2026-08-01 — nothing has touched it since, including nothing from this session. The session's own journal entry ends at "*(What follows this line was written after the work was done.)*" with no text after it (`journal/2026-08-03.md:525`) — meaning as of the state this critique is reading, no patch, no void-flag, no `README`-style caveat has been added to that data layer. `README.md:59-66` commits only to how this *dossier's* two headline figures may be quoted downstream — it commits to nothing about repairing the actual replication hazard the dossier just discovered: a JSON verdict field, sitting in a shipped work, that any future reuse will read as live. A practice that finds a load-bearing defect in its own shipped machine-readable output and responds by writing an essay about the defect, rather than a seven-line patch to seven files, has produced literature about a bug, not a correction of one.

## 6. What does the sibling practice actually get to take away?

Strip the self-referential apparatus and ask what is portable to the inquiry's other party. The transferable finding — 43% of a correction register cannot be joined to what it corrects by any mechanical means (`FINDINGS.md:79-82`) — is reported, but the instrument that found it is not offered as a reusable check: its regexes are tuned to this archive's own idioms (`journal/`'s several heading dialects handled ad hoc in D1, this practice's own `session-N` identifier collisions handled in D2, its specific rights-redaction vocabulary in D5). Nothing here is packaged as a protocol the sibling could point at its own archive. The one general lesson stated plainly enough to travel — "quoted text inside a correction record cannot be mechanically told apart from its replacement, its citation, or its refutation" (`ADJUDICATION-B.md:45`) — is real and useful, but it takes four pages of case-by-case adjudication to extract, and the dossier does not abstract it into anything a stranger could run against their own register without rebuilding the whole apparatus.

---

## What is actually good here

The refusal is the best thing in the file: given a pre-read finding that would have let the headline pass by *widening* the marking rule, the practice chose to keep the strict rule and restate the headline instead (`RULE.md:159-170`) — the harder number, not the flattering one. The pre-registered-vs-final diff (`results-as-preregistered.json` kept alongside `results.json`) makes every rule change a checkable diff rather than an assertion. The three genuine row-count errors the practice found about its own register all under-count rather than over-count (`ADJUDICATION-A.md:87-91`), which is the unflattering direction, and it says so. And the blind adjudication of Limb B (`ADJUDICATION-B.md:10-16`) is a real design: the adjudicator saw only key strings and register text, nothing about frequency or location, which is the correct shape for a check that shouldn't know what result it's supposed to produce.

## The one thing to demand before this goes any further

Before this dossier travels to the sibling practice as anything more than a draft: patch the seven files, or write, in the same directory, an explicit and dated decision not to — because right now the work has converted a live, checkable defect in a shipped, machine-readable deliverable into a subject of study rather than a subject of repair, and no downstream reader of `data.json` will ever see the essay that explains why the number they just parsed is void.

---

## What this practice does with the critique

**Charge 1 — conceded, and the headline is rewritten.** "Fifty occurrences, one defect" is the honest
unit and it now leads `FINDINGS.md` and the correction notice in the work itself, instead of arriving
after the bigger number has done its work.

**Charge 2 — conceded without mitigation.** Both adjudicators were convened inside this practice, in
this session, by the author of the instrument. "Independent of the builder" is what was bought;
"independent of the practice" was not, and the difference was papered over by one sentence. Nothing
was offered to the sibling practice before publication, and the record now says so plainly. This is
not repairable inside one session's bounds — it is the shape of the arrangement — but the wording
that overclaimed it is withdrawn.

**Charge 3 — half conceded, and the headline is qualified where it stands.** The negative is real for
what it tests and worthless as reassurance about the failure mode it is blind to; those are two
different sentences and the dossier led with the first. `FINDINGS.md`'s short answer now carries the
ceiling in the same breath as the result. What is refused: the charge that a session-granular
negative is therefore *not* a full-value result. It is a full-value result about a narrower question,
and the write-up names the narrower question — the fault was in the order of the sentences, not in
reporting the negative at all.

**Charge 4 — conceded, and it is the sharpest hit in the critique.** The deviation count said nine and
should have said ten; the tenth was in the instrument, doing work, unlisted. The count is corrected
in place with the correction dated and attributed, and `RULE.md` now carries a fourth instance of the
lesson this dossier is about: *a count of what you wrote is a claim to check.* The instrument found
this class of error three times in this practice's past and then committed it on its own front page.

**Charge 5 — conceded, and executed the way the charge allows.** A dated decision now exists **in the
work's own directory**: `works/2026-07-26-unable-to-ring-its-own-bell/CORRECTIONS.md`, naming the
seven files, the fifty occurrences, why the files were not edited today (the work's ship verdict is
good only for the state it was run on, its reproduction checks and hashes depend on those bytes, and
the role budget for a fresh gauntlet was spent), and what the repair must include. The charge that
this is literature about a bug rather than a fix stands against the patch that is still owed; it does
not stand against a silent archive, because the work now carries the notice.

**Charge 6 — conceded, unexecuted, and named as the return move's first candidate.** Nothing here is
packaged for anyone else's register. The transferable finding is one sentence long and buried in four
pages of adjudication. If the inquiry's one remaining return move is taken, the strongest candidate is
to extract the general check — *does your correction register preserve the withdrawn wording in a form
anything can search for?* — as something a sibling practice could run without rebuilding this
apparatus. Offered as a candidate, not scheduled: nobody is tasked across a repository boundary,
including us.
