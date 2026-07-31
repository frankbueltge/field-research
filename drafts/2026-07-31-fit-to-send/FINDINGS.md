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

## 2. The two network failures are real — and what this section first said about them was false

> **CORRECTED 2026-07-31, after the Verifier's pass and by the conductor's own hand.** This section
> originally ended: *"Two shipped works have been handing readers a security warning and a reset
> since 2026-07-01."* **That is false.** Neither failing string is a link. The corrected account is
> below; the withdrawn sentence is quoted here so it cannot read as a live assertion anywhere.
>
> The Verifier confirmed every fetch result in this section and did not catch the error, because it
> was asked to check whether the URLs behave as claimed — which they do — and not whether the works
> *link* the failing form. Nobody checked the one thing that decided what the finding meant.

Both were re-checked from a second vantage inside the probe (which agreed) and then a third by hand:

- `https://jabfm.org/content/32/5/732` (cited in `works/2026-07-01-digit-mirror/work.astro`) —
  connection reset from two vantages. **`https://www.jabfm.org/content/32/5/732` returns HTTP 200.**
- `https://marcellodibello.com/algorithmicfairness/handout/impossibility.html` (cited in
  `works/2026-07-01-fairness-trap/work.astro`) — TLS failure, *"certificate is not valid for
  'marcellodibello.com'"*, from two vantages. **`https://www.marcellodibello.com/…` returns HTTP
  200.**

Both failing strings were then read in the files that carry them, which is what should have happened
before the first version of this section was written:

- `works/2026-07-01-fairness-trap/work.astro:610` — the `href` is
  **`https://www.marcellodibello.com/…`**, the working form. Only the *link text* on line 611 is the
  bare host. **A reader who clicks arrives.**
- `works/2026-07-01-digit-mirror/work.astro:372` — the SOURCES block contains **no links at all**.
  `jabfm.org/content/32/5/732` is plain display text beside `doi:10.3122/jabfm.2019.05.190085`, and
  that DOI resolves: HTTP 200, final URL `https://www.jabfm.org/content/32/5/732`. **A reader who
  follows the identifier arrives.**

**So there is nothing here to repair on either work, and the session's impulse to repair it would
have been a fix to a defect that does not exist.** The true and much narrower statement:

> Two citation strings *displayed* on shipped works do not resolve when copied, while the link or
> identifier printed beside them does.

**D4 — and it is the largest defect in this instrument.** The sweep reads what a page *displays*, not
what it *links*. Every `OK`, `GONE` and `BLOCKED` in this census is therefore a verdict about a
**string shown to a reader**, not about a hyperlink. That is a legitimate object — it is what a reader
who copies a citation gets, and this archive prints many citations as bare text — but it is not the
question "do this work's links work", and until this correction the record read as though it were.
The three cases now form one family: a bare-host display beside a working link (006), a bare display
string beside a working identifier (004), and an ellipsis-abbreviated display string whose full form
lives only in the repository (017, §4).

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
- **Two citation strings a reader cannot follow if they copy them** (§2) — beside a working link and a
  working identifier respectively. **Nothing to repair.**
- **One soft-gone**, already known and disclosed by this practice.
- **26 of 162 — 16 % — `BLOCKED`**: the archive's link health at those identifiers is not knowable
  from where this practice stands, and no number that hides them is honest.
- **Custody is thin, and thinner than the binding count suggests.** The corpus yields **25 structural
  token bindings over 21 unique URLs — and only 15 were mechanically resolved.** Six were downgraded
  to `NOT-AUTOMATICALLY-CHECKABLE` because the response is not text-like, and **one of those six is
  the standard PDF at the centre of §4**, so nobody has checked whether it still holds what
  instrument 017 says it holds. Final tally at Layer 2: **1 `HELD`, 14 `NOT-HELD`, 147 of 162
  `NOT-AUTOMATICALLY-CHECKABLE`.** *(Reconciliation added 2026-07-31 after the Verifier's finding F1:
  this section previously cited "25 structural token bindings" without disclosing that only 15
  resolved — a reader could have believed the standard's custody was checked. It was not.)*
  **In those words: the custody layer of this instrument is thin, and its `OK` means "something
  answered", not "the source still says what we said it says".**

The honest one-line reading — knowing that a one-line reading is itself the composite the Skeptic
warned about — is: **the archive's citations are not rotting; several of the citation strings it
prints for readers to copy do not work, while the links beside them do; and one sixth of them cannot
be checked from here at all.**

*(Ecology-internal identifiers: 7 of the 162 unique URLs point inside this ecology on the conductor's
reading, which counts a sibling repository the practice audits; the probe's own `self` flag is
narrower and marks 3. Both are stated because they answer different questions — Verifier finding F2.)*

## 6. For the delivery this session is preparing

Instrument 001, the *Calibration Certificate*: **10 evidence identifiers, 8 `OK`, 0 `GONE`, 0
`SOFT-GONE`, 2 `BLOCKED`** — one DOI answering 403 and one news article answering 429 to this
runtime. Nothing in it is shown dead; two of its ten sources are undecidable from here and must be
opened by hand before it goes to anyone. That is a two-minute task for a human with a browser, and it
is now a named precondition rather than an assumption.
