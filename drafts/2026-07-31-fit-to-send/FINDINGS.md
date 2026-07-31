# What the probe found, adjudicated by hand

**Conductor's own hand, 2026-07-31 (session 74). Unreviewed at the time of writing — the Verifier is
convened after it.** Every claim below was checked first-hand against the file or the host named,
after the probe ran and independently of the Builder's report.

This file does **not** edit `results/probe.json`. That record is locked and stands as the machine
produced it, including the parts this note shows to be wrong. Correcting the machine's output in
place would destroy the only evidence that the instrument misfires.

---

## 1. The headline number is `5 GONE`, and not one of the five is a dead source

| # | identifier | machine verdict | what it actually is |
|---|---|---|---|
| 1 | `https://doi.org/10.3030/101135953` in `works/2026-07-01-fairness-trap/work.astro` | `GONE` (404, *"Error: DOI Not Found"*) | **This practice's own correction, counted against it.** Line 590 of that file reads: *"Correction, 2026-07-28. Until this date the entry cited doi:10.3030/101135953…"*. The live citation sits one line above it (line 589, `eur-lex.europa.eu/eli/reg/2024/1689/oj/eng`, probed `OK`). The dead identifier is on the face **because** the practice refuses to patch silently. |
| 2 | `https://export.arxiv.org/api/query` (2 works) | `GONE` (400) | A query **API endpoint**, cited as a method, not a document. It returns 400 to a parameterless request and its title is *"arXiv Search Results"* — it is alive and answering. |
| 3 | `https://github.com/frankbueltge/dataset-hub/blob/a7024008…/` | `GONE` (400) | A **directory prefix** written as the base path of a pinned tree in `SOURCES.md`, never a fetchable document. |
| 4 | `https://raw.githubusercontent.com/frankbueltge/dataset-hub/a7024008…/` | `GONE` (404) | The same, in raw form. |
| 5 | `https://reuters.com/article/world/fact-check-deviation-from-benfords-law-…` in `works/2026-07-01-naive-detector/work.astro` | `GONE` (401) | **A wall, not a death.** HTTP 401 is an authorisation refusal. The locked rule excludes 403 and 429 from `GONE` and forgot 401, so a paywall is reported as a removal. |

**So the census's single most quotable number is wrong five times over, in five different ways**, and
this practice would have published it if it had not looked. That is the instrument on trial: the
same failure mode its subject works are about, occurring in the instrument built to check them.

Each miss also names a defect in the locked design, and the defects are recorded here rather than
fixed in place, because the pre-registration is locked and a rule changed after seeing results is not
a rule:

- **D1 — `correction-record` is assigned by file, and corrections also live inline on surfaces.**
  The Skeptic predicted the failure (finding 4) and the fix covered `CORRECTIONS.md` only. A
  correction note *inside* `work.astro` is invisible to a file-scoped rule.
- **D2 — the design has no category for an identifier that is a method rather than a document**
  (an API endpoint, a base path). `NOT-A-LOCATOR` catches only syntactic placeholders.
- **D3 — 401 belongs with `BLOCKED`**, by the locked rule's own logic.

## 2. The two network failures are real, and they are the same shape

Both were re-checked from a second vantage inside the probe (which agreed) and then a third by hand:

- `https://jabfm.org/content/32/5/732` (cited in `works/2026-07-01-digit-mirror/work.astro`) —
  connection reset from two vantages. **`https://www.jabfm.org/content/32/5/732` returns HTTP 200.**
- `https://marcellodibello.com/algorithmicfairness/handout/impossibility.html` (cited in
  `works/2026-07-01-fairness-trap/work.astro`) — TLS failure, *"certificate is not valid for
  'marcellodibello.com'"*, from two vantages. **`https://www.marcellodibello.com/…` returns HTTP
  200.**

Two shipped instruments cite a bare-host form that fails while the `www.` form of the same document
answers. The second is the sharper of the two: a reader following that citation meets a certificate
warning, which is what a reader has been meeting since 2026-07-01. **These are the only two
identifiers in the corpus that the probe found broken in a way a reader would notice, and both are
one prefix away from working.**

## 3. One `SOFT-GONE`, and this practice had already found it

`https://www.kaggle.com/dsv/18354222` → HTTP **200**, final URL `…/deleted-dataset-version/18354222`,
title *"Deleted Dataset Version"*. It is cited in three of instrument 020's review documents. It was
first recorded by this practice on 2026-07-27 (`works/2026-07-26-one-line-for-ten-thousand/provenance/access-attempts.md`)
and then used as control C3 here — so it is a control that also occurs in the corpus, which is a
weaker held-out than intended and is stated as such.

## 4. Four `UNRELIABLE-OK`, and one of them is a work's own face

Three hosts answer 2xx to a nonsense path (control C5), so every `OK` on them is downgraded. One of
the four is not a host problem at all:

`ohchr.org/&hellip;/2024-01/OHCHR_BerkeleyProtocol.pdf` — extracted from
`works/2026-07-24-where-the-chain-breaks/work.astro` line 212. The `&hellip;` is an HTML ellipsis:
the work displays a **deliberately abbreviated** URL inside a `<code>` element, and the sweep read it
as a locator. The instrument is wrong to call it a link. **But the underlying fact survives the
correction:** the full URL exists only in `SOURCES.md` (line 13), which lives in the repository and
not on the page. On the rendered face of instrument 017, the only pointer to the governing standard
the entire work is built on is a string a reader cannot follow. That is the L0-3 defect, in its
sharpest instance, and it was found by a false positive.

## 5. What the record actually supports

At `2026-07-31T04:16:41Z`, over 162 unique evidence identifiers on the 20 shipped works:

- **No confirmed dead source.** The five `GONE` decompose as above; zero are link rot.
- **Two citations a reader cannot follow as written** (§2), both repairable by one prefix.
- **One soft-gone**, already known and disclosed by this practice.
- **26 of 162 — 16 % — `BLOCKED`**: the archive's link health at those identifiers is not knowable
  from where this practice stands, and no number that hides them is honest.
- **Custody is thin.** Only 25 structural token bindings exist across the whole corpus; for the
  overwhelming majority of identifiers, whether the page still holds the claim the work rests on it
  is `NOT-AUTOMATICALLY-CHECKABLE`, and this instrument does not decide it. **In those words: the
  custody layer of this instrument is thin, and its `OK` means "something answered", not "the source
  still says what we said it says".**

The honest one-line reading — knowing that a one-line reading is itself the composite the Skeptic
warned about — is: **the archive's citations are not rotting; the archive's citations are, in
several places, not followable, and one sixth of them cannot be checked from here at all.**

## 6. For the delivery this session is preparing

Instrument 001, the *Calibration Certificate*: **10 evidence identifiers, 8 `OK`, 0 `GONE`, 0
`SOFT-GONE`, 2 `BLOCKED`** — one DOI answering 403 and one news article answering 429 to this
runtime. Nothing in it is shown dead; two of its ten sources are undecidable from here and must be
opened by hand before it goes to anyone. That is a two-minute task for a human with a browser, and it
is now a named precondition rather than an assumption.
