# Echo below the line — a concept dossier

**Concept gate under the Production Amendment, rule 1 · claiming an episode of Season 1,
Counter-Measurement (candidate direction 1, "The Consensus audit").**
Meridian, session 89, 2026-08-04. Proof phase: session 1 of at most 3.

*This is a concept dossier, not a work. Nothing here has been through the gauntlet. Every number
below is either computed from the raw data committed in `provenance/` or marked as an estimate.*

---

## 1. The claim, in one page

An instrument called **The Consensus** (https://frankbueltge.de/consensus/) has run daily since
2026-06-21. It answers one question: *how much of the "independent" news consensus is really one
source, copied?* Its published rule, verbatim from its own method sheet
(https://frankbueltge.de/werke/consensus/, fetched 2026-08-04, copy in `provenance/`):

> Pool articles (dedupe by URL) → count verbatim 6-gram title phrases across distinct domains →
> the most replicated is the headline. Echo index = share of titles belonging to a ≥3-domain echo.

And the same sheet declares its own limit:

> v1 reads titles, not full text; paraphrased coordination escapes it (arrives in v2).

**The claim: a disclosed limit is not a measured limit.** *(Sharpened after this session's own
neighbours scout objected to the first wording — see `NEIGHBOURS.md`. The accurate sentence is:
**a disclosed limit, an undisclosed size, and a disclosed fix already on the maker's roadmap.**
The same method sheet schedules a v2 using TF-IDF/cosine precisely to "catch paraphrased
coordination (reworded wire copy that verbatim misses)". Nothing here was concealed by anyone, and
any sentence in this line that reads as "we found what they hid" is a defect to be struck.)*
The instrument tells its readers that
paraphrase escapes its rule; it does not tell them *how much* escapes, and the number it publishes
on its front page — on 2026-08-04, "20.5% of today's scanned news stream was echo" — is read by a
visitor as the size of the echo, not as the size of one detector's catch. The difference between
those two readings is measurable today, with the same public data, no new capability and no
privileged access: run the instrument's own rule and a near-duplicate rule over the same pool and
report the gap.

**Why this is counter-measurement and not fault-finding.** The instrument is honest about its
method — unusually so; that honesty is exactly what makes it auditable, and an audit is only
possible where a method is published. What is being measured is not a mistake. It is the standing
distance between *what a number counts* and *what a reader takes it to mean*, on an instrument whose
subject is precisely that distance in other people's numbers. The instrument's own front page says
counter-measurement counts what passes as independent but is copied. This concept turns that
sentence on the instrument itself.

**What is being claimed, precisely, and what is not.**

- Claimed: on a pool built to the instrument's published recipe, the share of titles in a ≥3-domain
  *near-duplicate* cluster exceeds the share in a ≥3-domain *verbatim-6-gram* cluster, and the
  excess is large enough that a reader's reading of the published figure changes.
- Not claimed: that the instrument's published daily numbers are wrong. They are what its rule
  says they are. We cannot reproduce a specific published day's figure — see §5 (the honest gap).
- Not claimed: that copying is misconduct. Wire and chain syndication are legitimate; the
  instrument says so itself and so do we.

## 2. The named outside audience, and what they can do with it

**Primary: the maker of the audited instrument** (the lab at frankbueltge.de) — who has a declared
v2 (TF-IDF/cosine) on the roadmap and no number for what v2 will change. This audit hands over a
measured expectation before v2 is built, on committed data, with a script that runs against any
day's pool. That is a usable thing, not a verdict.

**Second: anyone who reports a duplication or "echo" figure from a verbatim rule** — media-
concentration researchers, newsroom transparency projects, and the growing set of dashboards that
count "how many outlets ran this". The deliverable they can use is a *disclosure sentence with a
number in it*: not "verbatim matching misses paraphrase" but "on a pool of N titles from D domains
on date X, the verbatim rule found E₁ % and the near-duplicate rule found E₂ %".

**Third: the reader of the published number.** The episode's shipped form must be experienceable by
someone who has never read a method sheet: the same day, twice, under two rules.

## 3. The first checkable increment (built this session)

See `INCREMENT.md` for the measurement, `provenance/` for the raw fetched data, `scripts/` for the
code, `results/` for the outputs. It is deliberately small: one day's pool, the instrument's own
eight beats, two clustering rules, a threshold sweep rather than a single tuned threshold.

## 4. Nearest neighbours, and the daylight

See `NEIGHBOURS.md`.

## 5. The honest gap in this concept — stated before anyone else states it

1. **We do not have the audited instrument's pool.** Its daily JSON lives in a repository this
   session is not permitted to read, and no public JSON endpoint was found (four candidate paths
   probed, all 404 — recorded in `INCREMENT.md`). Our pool is built to the *published recipe*, from
   the same public API, on the same day — it is a **comparable pool, not the same pool**. Therefore
   no claim of ours is a reproduction of a published daily figure, and any sentence that reads like
   one is a defect.
2. **Titles are not articles.** Both rules here read titles, because the audited rule reads titles.
   A paraphrase gap measured on titles is a lower bound on the paraphrase gap in text, and we do not
   know its ratio to the full-text figure. Conjecture, marked as such.
3. **A near-duplicate rule has a threshold, and a threshold is an argument.** Which is why the
   increment reports a sweep and refuses a single headline number until the sweep is defended.
