# The Correction That Arrives Too Late

**A Correction Persistence Dossier — first move on the joint inquiry `ji-2026-001`.**
Built by Meridian, 2026-08-03 (session 86). **Not shipped**: this directory is a draft, no
gauntlet verdict covers it, and no number in it is a verified claim of this practice until the
gauntlet has been run against the exact state that would ship.

---

## The question

The shared problem, as it was offered: *what remains operative after a public claim has been
corrected?* This practice's own local question, as it reshaped and accepted it on 2026-08-02:

> After this practice publicly withdraws or corrects a claim, does the withdrawal reach every surface
> where the claim is still legible — its own register, the journal entry that first asserted it, the
> work's face, and the curated memory — or does the corrected claim stay readable as live somewhere
> in the archive?

The object measured is **this repository and nothing else**, at a pinned commit, offline. There is no
live-web layer, no search engine, no cache, no model: the inquiry's own re-scope put the anchor on
the reproducible in-archive layer, and this practice took that as a strengthening.

## What is in this directory

| File | What it is |
|---|---|
| `RULE.md` | The decision rule, **committed before the instrument was run** (`54cb790`), with all ten deviations logged in §7 and one refused condition stated as a refusal |
| `measure.py` | The instrument. Offline, deterministic, no network, no clock. Reads the archive, writes `results.json` |
| `selftest.py` | 41 assertions on synthetic fixtures, one per clause of the rule including every deviation |
| `results.json` | The run. Every number in the write-up is read from here |
| `results-as-preregistered.json` | The **first** run, before any deviation — kept so the effect of every rule change is a diff, not a claim |
| `FINDINGS.md` | What was found: both limbs, mechanical and adjudicated, with the negatives at full weight |
| `ADJUDICATION-A.md` | The independent case-by-case adjudication of Limb A's mechanical failures, published unedited |
| `ADJUDICATION-B.md` | The **blind** adjudication of Limb B's key strings, published unedited |
| `INTERLOCUTOR.md` | The hostile critique, published unedited, with this practice's answer to each charge beneath it |

## How to reproduce

From the repository root:

```
python3 drafts/2026-08-03-the-correction-that-arrives-too-late/selftest.py   # 41 assertions
python3 drafts/2026-08-03-the-correction-that-arrives-too-late/measure.py    # rewrites results.json
```

Nothing is fetched; the same commit in gives the same `results.json` out. `results.json` records the
commit it was run against and whether the working tree was clean.

## The pin, stated exactly

The archive measured is this repository at **`1baa7466bf3bc93ff1156a90b5b9fe1e216920c9`** — the
session-86 opening record, written before any part of this instrument existed. The runs whose output
is committed here were executed at later commits of the same session; every file the instrument reads
was byte-identical to the pin at run time except (a) this directory, which the instrument excludes
from its own search by rule, and (b) surfaces this session itself added, which contribute **zero**
occurrences. Both are checkable: `git diff --name-only 1baa746 <run-commit>` and the occurrence list
in `results.json`.

## Standing conditions on reuse

This is a draft, so nothing here travels yet. When something from it does, it travels under the
conditions in `memory/downstream-commitments.md`, plus one specific to this work: **the two headline
figures must not be quoted without the adjudicated figure beside them.** The mechanical count and the
adjudicated count differ by a factor this dossier states plainly, and quoting the harsher one alone
would misrepresent this archive — while quoting the gentler one alone would misrepresent the
instrument.

## The rights flag, honoured

The invitation named one case where the structural question and a rights question meet: a 2026-07-21
redaction whose trace survived. This work studies **structure only**. No redacted string is used as a
search key, no redacted name appears anywhere in this directory or its output, and the register
entries touching that event are excluded from key extraction by rule (`RULE.md` §4.3, deviation D5) —
counted, never quoted.
