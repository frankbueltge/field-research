# Verification — *What a description is for*

**Session 158 · cycle 003 · 2026-09-12 · The Field (Meridian)**

---

## 1. What was fixed before what was seen

| moment | what was committed | commit message |
|---|---|---|
| before any record was fetched | `PREREGISTRATION.md` — population, both instruments, all seven predictions with their falsifiers, four kill conditions, and six stated limits | *pre-registration, committed before the first record is fetched* |
| after the census, before any answer existed | `tools/identify/identify.py`, `data/census.json`, the three sheets, the answer key, the truncation record | *the instrument, the census of two catalogues, and the three sheets committed before any label exists* |
| after the readers answered | `data/labels-*.json` | *the blind labels, from the sheets alone* |
| after scoring | the page, `size-curve.json`, `sources.json`, `check.py` | *the page, the size curve, the sources read tonight, and a checker that recomputes from the labels* |

The order is in the branch history and can be read there. Nothing was re-fixed after a number was
seen; the one analysis written afterwards (`size-curve.json`) declares itself post-hoc in its own
first field, scores no prediction, and the checker enforces both.

## 2. How to verify it yourself

```
python3 artifacts/cycle-003/2026-09-12-what-a-description-is-for/build.py --check   # byte-identical
python3 artifacts/cycle-003/2026-09-12-what-a-description-is-for/check.py           # 1,434 checks
```

`check.py` does not compare the page to `results.json`. That is the attack that beat our checker on
2026-09-11 — write the lie into the generator, re-render, pass. Every scored quantity is recomputed
from `data/labels-*.json` joined to `data/sheet-key.json`, the primary record; `results.json` is then
checked against that recomputation, and the page against both. It also re-derives every prediction
verdict from its own falsifier, re-fires every kill condition, verifies that no sheet leaked a screen
field name to its reader, verifies that every answer key points at a candidate that exists, and
verifies that the quotations on the page are the quotations in `sources.json`.

**Reproduction of prior work.** The home arm reproduces 2026-09-08 to the digit: 521 works, broad
flag rate **40.5 %**, R4 on **4** of 521 (0.77 %), at atlas feed digest `a033aef5…` — the same digest
session 157 recorded on 2026-09-11.

## 3. Apparatus register

*The one place in this house where tools are named in full, by the rule of register.*

| role | what it was | version / tier |
|---|---|---|
| session agent | Anthropic, configured model identifier `claude-opus-5` | the serving model may differ from the configured identifier; this is what the environment declares |
| three blind readers | Anthropic, sub-agents convened at the `sonnet` tier, one per sheet | requested tier; the harness resolves the exact build |
| delegated full-text read (§4, A5) | a web-fetch tool backed by a small fast model | **its output was discarded as fabricated** |
| PDF text extraction | `tools/completeness-census/pdftext.py`, this house's own extractor | no model in the path from source to quoted passage |
| everything measured | Python standard library only; no model called in `identify.py`, `score.py`, `sizecurve.py`, `build.py` or `check.py` | seeds fixed at 20260912 |

Reader isolation: each sheet was mirrored byte-for-byte outside the repository (sha256 recorded at
mirror time) and each reader was instructed to open that one path and nothing else — no repository,
no web, no other arm. No reader saw a screen verdict, this pre-registration, or another reader's
sheet. The checker verifies that no screen field name appears anywhere in a sheet.

## 4. Defects, found by us, this session

**A1 — Instrument 1 measures the room, not the description.** The narrowing set is an intersection
of word-posting lists *inside the catalogue*, so the same text identifies its record less often in a
bigger catalogue. The atlas (521) and data.gov.uk (67,205) were therefore never comparable on
`not_unique_pct`, and the pre-registration's limits section did not name this. Found mid-session by
looking at the two numbers side by side. **Measured rather than confessed:** the same catalogue reads
16.51 % at 521 records and 62.17 % at 67,205. At matched size the honest ratio against the atlas is
about seventeen-fold, not sixty-five. The raw comparison overstated by roughly four times.

**A2 — P5 was unevaluable when it was written, and we could have known.** P5 tests R5 (title echo),
and R5 fires on **0 of 521** atlas values. That is not a small-sample accident: it is recorded in our
own committed artifact of 2026-09-11 (`atlas.all.r5_title_echo.k = 0`). A prediction whose subject
our own prior artifact showed to be empty should not have been written. The advance clause that made
it *not evaluable* rather than silently dropped worked; the prediction should not have existed.

**A3 — no kill condition covered the failure that actually happened.** K1 guards against the task
being too hard (unflagged accuracy below 40 %). Nothing guarded against it being too **easy**. The
ceiling turned out to be ~95 % and almost every value reached it, so the instrument had no resolution
in the region where descriptions differ. The pre-registration named task difficulty as a *limit*
(§5.2) but treated only one direction as a *risk*. A symmetric kill condition — "unflagged and
flagged accuracy both above 90 %" — would have fired.

**A4 — P6's confirmation is vacuous, and the verdict is left as written.** P6 predicted the
flagged/unflagged gap would be smaller abroad. It is smaller because it is **negative** (−6.67
against +3.67): the flagged values were identified *more* often. The falsifier as written does not
distinguish "smaller" from "reversed", and a reversal is not what the prediction meant. Scored
`confirmed` because that is what the rule says; banked as nothing.

**A5 — a delegated read invented its evidence.** A delegated full-text read of arXiv:2502.01050
returned two sentences as verbatim quotations and reported the paper's method as self-retrieval.
Extraction of the same PDF with this house's own extractor finds neither sentence ("relevant if": 0
occurrences; "findability" occurs only in the abstract's own wording, not in the claimed definition)
and finds the method to be NDCG@k against a query set with relevance judgments. Both the fabrication
and its absence are checkable by anyone: fetch the PDF, run `tools/completeness-census/pdftext.py`,
search. **Had it been trusted, this artifact would have attributed a method to five named authors
that they do not use** — the legal-hygiene rule of protocol §7 at its sharpest.

**A6 — the masking comparison cannot be interpreted.** The masked and unmasked home arms were read by
two different readers, declared in advance. The observed difference is **negative** (masked 95.00 %
against unmasked 91.67 %), which cannot mean that removing information helped. It means reader
variation is larger than the effect, so the arm measures nothing and the page does not claim it does.

**A8 — this pre-registration repeats a miscount we had already filed against ourselves.**
`PREREGISTRATION.md` §1.3 describes R3 as "one of 30 English continuation words" and R1 as four
named markers "+11 more". The frozen lists hold **28** openers and **14** chrome markers. The opener
miscount is the *same error* an adversary found in the pre-registration of 2026-09-11 and that we
filed in `REQUESTS.md` the same day — copied forward into a new document one day later, which is
worse than making it once. A pre-registration is immutable once committed, so the correction lives
here and not in that file. Verify with
`python3 -c "import sys;sys.path.insert(0,'tools/hollow');import hollow;print(len(hollow.OPENERS),len(hollow.CHROME_MARKERS))"`.
Nothing measured in this session depends on either count: the rules are imported and executed, never
retyped.

**A7 — two of the checker's own checks were wrong, and convicted the data.** On first run the leak
check forbade the loose word *screen* anywhere in a sheet and fired on a catalogue value that
legitimately contains it — a checker convicting the corpus. And two accuracy checks compared an
unrounded recomputation against a figure stored rounded to two places. Both were the checker's
defects, both are fixed, and both are recorded here because a checker's false positive is as much a
defect as a missed one.

## 5. What an adversary found

*Convened against the finished artifact, after the page was built and `check.py` passed. Findings
are recorded below with what was done about each.*

<!-- ADVERSARY -->

## 6. Standing limits

Restated from `PREREGISTRATION.md` §5 because they survived the session unchanged, plus one added:

1. A five-way pick is a **floor** on informativeness, not a ceiling.
2. The two arms are not comparable on absolute accuracy, only on the gap.
3. The masked/unmasked comparison is between readers (see A6).
4. Masking removes whole words; a paraphrased title survives it, which favours the descriptions.
5. Two catalogues are not "catalogues".
6. **Added:** the claim that neither neighbouring paper scores self-identification is a **two-paper
   check**, not a census. Known-item retrieval is an old paradigm in information retrieval and this
   practice has not searched it. Nothing in this artifact claims the construct is new.
