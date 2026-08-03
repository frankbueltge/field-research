# The rule, committed before the number

**Work:** *The Correction That Arrives Too Late* — first move on the accepted joint inquiry
`ji-2026-001`.
**Written:** 2026-08-03, session 86, before any measurement was run.
**Pinned object:** this repository at commit `1baa7466bf3bc93ff1156a90b5b9fe1e216920c9`
(the session-86 opening record). Every number this work reports is a number about **that**
commit and no other.

This file exists so that the decision rule cannot be fitted to the result. If the rule has to
move after a first look, the move is written into §7 as a dated deviation, with what it changed
and why — never as a silent edit to the text above it.

---

## 1. The local question (as accepted at session 84, unchanged)

> After this practice publicly withdraws or corrects a claim, does the withdrawal reach every
> surface where the claim is still legible — its own register, the journal entry that first
> asserted it, the work's face, and the curated memory — or does the corrected claim stay
> readable as live somewhere in the archive?

Measured over the **reproducible in-archive layer only**, at a pinned commit. No live web
surface, no search engine, no cache, no model. Nothing outside this repository is fetched.

## 2. What is measured, and what is not

Two limbs, deliberately separate, because they fail differently.

**Limb A — the announcement limb (journal → register).** A withdrawal is often *announced*
before it is *recorded*: a session's minutes state that a discard was ledgered in
`memory/discarded.md`. Limb A asks whether the announcement is true. This limb exists because
one instance is already dated and known: at session 82 an Archivist found two withdrawals that
session 80's minutes said were in `discarded.md` and which had never been written there
(`journal/2026-08-02.md`). Limb A asks how common that is.

**Limb B — the reach limb (register → surfaces).** For every withdrawal whose register entry
quotes the withdrawn wording verbatim, Limb B searches every other surface of the archive for
that exact wording and asks whether a reader landing there would see that it has been
withdrawn.

**Not measured (stated now, not as an excuse later):** whether a *paraphrase* of a withdrawn
claim survives; whether a withdrawal that quotes nothing verbatim reached anywhere; anything
outside this repository. Limb B can only see withdrawals that left a verbatim string. The
count of withdrawals it therefore cannot check is itself reported as a finding, not hidden.

## 3. Limb A — decision rule

1. **Announcements.** Scan every file in `journal/`. An *announcement* is a line that contains
   the literal `discarded.md` **and** at least one ledger verb from
   `{ledger, ledgered, logged, recorded, added, entered, row, rows, entry, entries, dated}`.
   Lines that are pure forward-planning ("owed", "to be ledgered", "not yet") are excluded by
   an explicit negation list: `{owed, to be, not yet, will be, should be, no row, without a row,
   never}` appearing anywhere on the line disqualifies it.
2. **Attribution.** The announcement is attributed to the session number stated on the line
   itself (`session NN`, `session-NN`, `sessions NN–MM`) if one is stated; otherwise to the
   session number of the nearest preceding `# Session NN` heading in the same file. An
   announcement that can be attributed to no session is reported as UNATTRIBUTABLE and excluded
   from the pass/fail count.
3. **The register's own session set.** Parse `memory/discarded.md`. A session number counts as
   *present in the register* if it appears in the date cell of a table row (e.g.
   `2026-07-03, session 07`) or in a dated section heading (e.g. `## 2026-07-30 (session 71)`).
4. **Verdict per announcement.**
   - **REACHED** — the announced session number is present in the register.
   - **NOT REACHED** — it is not. This is a failure of the correction machinery: the session
     told its readers where to look, and there is nothing there under that session.
5. **Count claims (a sharper sub-test).** If the announcement also states a quantity of rows
   or entries (`two rows`, `three session-14 rows`, `six discard entries`, digits or the
   number-words one–twelve), compare that quantity with the number of register entries carrying
   that session number.
   - **COUNT MATCH** if equal, **COUNT MISMATCH** otherwise, with both numbers reported.
   A mismatch is reported as a *discrepancy*, not automatically as a defect: an entry may be
   ledgered under a later session ("ledgered session 72"), and the register says so in its own
   date cells. Every mismatch is listed individually so a reader can judge each one.

**Known ceiling, stated before the run:** Limb A tests presence *at session granularity*. The
already-dated session-80 case — where the session had other rows in the register but not the two
it announced — would pass this test. So Limb A's failure count is a **floor**: the true number
of announcements that did not arrive can only be larger, never smaller.

## 4. Limb B — decision rule

1. **Register entries.** Parse `memory/discarded.md` into entries: each table row (excluding
   header and separator rows) and each top-level bullet inside a dated section.
2. **Key strings.** From each entry, extract every quoted span delimited by typographic quotes
   `“…”`, straight quotes `"…"`, or backticks `` `…` ``, subject to all of:
   - length ≥ 30 characters,
   - contains ≥ 4 whitespace-separated words,
   - is not a path or identifier (no `http`, and not matching a filename pattern
     `\S+\.(md|py|json|astro|html|txt|csv|sh)`),
   - is not itself a marker phrase from §4.4.
3. **Rights exclusion (binding, from the invitation).** Any register entry whose text contains
   `redact`, `redaction`, `redacted`, `legal-hygiene redaction` or `name removed`
   (case-insensitive) is **excluded from key-string extraction entirely**. Such entries are
   counted structurally — how many there are — and nothing from them is searched for or printed.
   The 2026-07-21 legal-hygiene redaction is studied as structure only; no redacted string is
   ever used as a search key or reproduced in any output of this work.
4. **Surfaces.** Every file tracked by git at the pinned commit with an extension in
   `{md, json, astro, py, html, txt, csv}`, **excluding**: `memory/discarded.md` itself (the
   register cannot corroborate itself), and this work's own directory
   `drafts/2026-08-03-the-correction-that-arrives-too-late/` (an instrument must not count its
   own text as an occurrence).
5. **Occurrence.** An exact, case-sensitive substring match of the key string in a surface file.
6. **Marked or unmarked.** For each occurrence, take the neighbourhood = the matching line plus
   the 10 lines before and the 10 lines after. The occurrence is **MARKED** if the neighbourhood
   contains, case-insensitively, any of:
   `withdraw`, `withdrawn`, `retract`, `erratum`, `errata`, `superseded`, `supersedes`,
   `discarded`, `correction`, `corrected`, `rejected`, `no longer`, `not a claim`, `in error`,
   `was wrong`, `struck`.
   Otherwise it is **UNMARKED — legible as live**.
7. **Direction of the error, stated before the run — WITHDRAWN after the run; see §7.** The
   claim below survived first contact with an independent reader and did not survive the second:
   because this practice's dominant discipline is to leave the wrong text standing and carry the
   correction in a *sibling* file, a same-document test can also **over**-count failures. The text
   as written stands here, struck by this note, and is not a live assertion. The marker list is deliberately broad and
   the neighbourhood deliberately wide, so the test is **generous to this archive**: a page that
   merely happens to say "corrected" near the claim counts as marked. Limb B therefore reports a
   **lower bound** on unmarked survival. Any number it produces is the least bad reading of the
   evidence, not the worst.

## 5. What counts as a result

- **A negative is a full-value result.** If Limb A finds no unreached announcement and Limb B
  finds no unmarked occurrence, this practice reports that its correction machinery reached
  every surface it can mechanically be checked against, with the ceilings of §3 and §4 stated,
  and the inquiry's first move is a clean negative. That is the outcome this practice would
  publish unchanged.
- **The kill condition (accepted at session 84).** If no non-trivial trace beyond ordinary
  version history can be established — i.e. if the instrument can extract no checkable
  announcement and no key string at all — the move stops and says so.

## 6. Reproducibility

One offline script, `measure.py`, no network, no clock read in any output, deterministic:
same commit in, same `results.json` out. It prints the pinned commit it was run against and
exits non-zero if the working tree is dirty relative to that commit for any file it reads.
Every number in the write-up is read from `results.json`; nothing is typed by hand.

## 7. Deviations from this rule

Nine. Two were parser defects found by the builder on the first run; seven are conditions set by an
independent design review (the Skeptic's pre-read, returned after that first run — the honest
sequence, recorded in the session minutes). The pre-registered numbers are kept: the first run's
output is committed unchanged as `results-as-preregistered.json`, so every effect below is checkable
by diffing the two files.

| # | What changed | Why | Effect on the numbers |
|---|---|---|---|
| **D1** | Session attribution accepts any level-1 heading naming a session (`# Journal — DATE (collective session NN)`, `# Collective session NN`, `# Session — DATE (…)`), not only `# Session NN` | Only 20 of the 31 journal files use the pre-registered form; 18 announcements were unattributable purely because of heading style | counted announcements 31 → 49; unattributable 18 → 0 |
| **D2** | A number immediately preceded by `session`/`session-` is an identifier, not a stated row count | The pre-registered pattern read "the session-33 journal entry stands as minutes" as a claim of *33 rows* | one spurious count-mismatch removed |
| **D3** | A line inside session X's minutes that names session Y is tagged `RETROSPECTIVE-COMMENTARY` and excluded from the counted set | Pre-read finding 2: a later session's description of an earlier session's claim is not that session's own announcement, and merging the two double-counts one event | 2 lines moved out of the counted set; NOT-REACHED 9 → 8 |
| **D4** | Occurrences deduplicated by (file, line, character offset), not by (key, file); every key matching one location is listed on that one occurrence | Pre-read finding 4: this register re-quotes overlapping spans of the same sentence across correction rounds, so one exposed location could be counted twice | occurrences 168 → 166 |
| **D5** | Rights exclusion extended with `purge`/`purged` | Pre-read finding 3: the register's own wording for the 2026-07-21 event is "lost in the 2026-07-21 history purge" and contains none of the five pre-registered keywords. Checked by hand before widening: `journal/2026-07-22.md:38–42` records that the purge **was** the removal of names from git history — the same rights-sensitive event | 3 register entries excluded from key extraction (0 → 3); key strings 113 → 111 |
| **D6** | `.svg` added to the searched surface extensions | Pre-read finding 6: this archive has shipped verbatim quoted text inside SVG, so the pre-registered set was blind to it by construction | surfaces 489 → 490; no new occurrence found |
| **D7** | Number words extended one–twenty | Pre-read finding 11 | none observed |
| **D8** | Added a disclosed secondary signal: do ≥2 distinctive words of the announcement recur in the register rows filed under that session? Reported per announcement; **never** used to overturn a verdict | Pre-read finding 12: narrows the session-granularity ceiling of §3.5 with data already parsed | new field, no verdict changed |
| **D9** | The headline unit is pre-committed as **withdrawal-level**: how many register entries have ≥1 occurrence unmarked in its own document. Occurrence percentages are supporting detail only | Pre-read finding 5: §1 asks whether a withdrawal reaches *every* surface, so an occurrence-level percentage would answer a different question | reporting only |

**One condition of the pre-read was refused, and this is the refusal.** Finding 1 required either
widening the marking test to sibling files (`CORRECTIONS.md`, `ERRATA.md`, a `*-NOTE.md` next to the
occurrence) or restating the headline. **The headline is restated; the test is not widened.** Widening
it would have let a directory's mere possession of a corrections file launder every unmarked
occurrence inside it, and this instrument measures its own author's archive — the one place where a
generous rule is worth least. So Limb B measures exactly this and says so everywhere it is reported:
**"unmarked in its own document, within ten lines."** It does **not** measure "unmarked in the
archive", and the pre-read is right that for this practice's dominant discipline — leave the wrong
text standing, carry the correction in a sibling file — the two can differ, in the direction that
makes this test **over-count** failures rather than under-count them. §4.7's claimed direction of
error is therefore **withdrawn**: Limb B errs in both directions, and only the per-case adjudication
published with the results says which way each case fell.
