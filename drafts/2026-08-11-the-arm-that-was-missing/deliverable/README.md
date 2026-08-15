# The Control Arm — a credential-free public-presence ledger

**Version 0.1 · 2026-08-15 · Meridian, an autonomous research practice**

A dated record of whether named videos on a very large video platform were **publicly
retrievable**, taken without any credential, together with a reference population large enough
to give a single reading an expectation.

**Read `LIMITS.md` before you use a number from this bundle.** It is short, it is present-tense,
and every serious misuse of this data is a misuse it names.

---

## 1. What this is, in one paragraph

A very large video platform is required by law to give vetted researchers access to its publicly
available data. Whether it does is an empirical question with two halves: **what the research
interface returns**, and **what was actually public**. The first half is credentialed and
closed. The second half is free — it needs no account and no allow-list — and it was not being
run as a continuous, published series. This bundle is that second half: a fixed panel of
publicly cited video identifiers, probed once a day through the platform's own credential-free
oEmbed endpoint, published as data, with the code and the run files that produced it.

It is **the control arm of a comparison**. On its own it settles nothing about any research
interface. Held beside the credentialed half, it turns a bare observation into a comparison.

## 2. What is in the bundle

| file | what it holds |
|---|---|
| `LIMITS.md` | **what this bundle cannot show.** Load-bearing; travels with any re-use. |
| `FIGURES.md` | every table, **generated from the data by `build_deliverable.py`** — not hand-typed |
| `expectation.json` | the reference absence rate per day: pooled, by video age, by source, by year, and the age gradient crossed with source |
| `reference-baseline.json` | the newest day's table in the exact shape the shipped tool reads |
| `series/presence-series.csv` · `.json` | one row per identifier, one column per measured day — the raw record |
| `series/presence-series-corrected.csv` | the same with the refuted-reading overlay applied |
| `receiver-eleven.md` · `.json` | the eleven identifiers of one existing public dashboard, measured from the public side |
| `MANIFEST.json` | every source run file with its sha256, so the bundle can be checked against the record |
| `tools/presence_check.py` | **point it at any list of your own.** Unmodified since it was written. |
| `tools/ledger.py` · `tools/power_audit.py` | the probe and the interval arithmetic the tool imports |
| `LETTER.md` | the covering letter, written to be forwarded unedited |

## 3. The three things the data says

**(a) The panel's public-absence rate is stable to a tenth of a percentage point across
consecutive days.** That is what makes it usable as a yardstick: a reading taken on any one day
is not an artefact of that day's network conditions. It is *reproducibility*, not sampling
error — `LIMITS.md` §5 — and the per-day Wilson intervals in `expectation.json` are the
sampling uncertainty.

**(b) Public retrievability falls with the age of the video, and the fall is not an artefact of
where the identifiers came from.** Videos under a year old are absent at roughly a quarter the
rate of videos over five years old. The progression across the six age bands **rises but is not
strictly monotone** — there is a flat step near four years — so what the bundle tests is the
endpoints: youngest band against oldest, pooled and inside each source stratum separately. The
direction and the rough size of the effect hold in **all three** strata; the difference reaches
conventional significance in two of them and **not** in the third, whose two cells hold about
fifty identifiers each and cannot settle it either way. `FIGURES.md` §§2–3 and
`gradient-test.json` carry the arithmetic.

**(c) The instrument is quiet enough for its answers to be about the videos.** Around one per
cent of requests end in a transport failure, and the same identifier is almost never affected
twice — so that noise is a property of the request, not of the video. Over the measured days
only a handful of identifiers in the whole panel change determinate state at all, and every one
is named in `FIGURES.md` §5 so the claim can be checked rather than believed.

## 4. How to use it on a list of your own

```
cd tools
python3 presence_check.py YOUR-LIST.txt \
        --baseline ../reference-baseline.json \
        --label "my list" -o my-reading.json
```

`YOUR-LIST.txt` holds one item per line — a full video URL, a bare numeric identifier, or
`identifier,handle`. Blank lines and `#` comments are ignored. The tool prints each identifier's
state, the observed absence rate of your list, and **the absence rate that would be expected for
your list's age profile** if it behaved like the reference population.

Three things to know before you read the output:

1. The tool requests **one identifier per second**, sequentially, with the same user agent and
   the same timeout as every row of our own ledger. It is deliberately slow. It is the same
   instrument, so your reading and ours are comparable.
2. **The expectation is a yardstick, not a verdict.** It says what share of comparable
   identifiers we could not retrieve. It never says which of yours should be absent.
3. On a short list the expectation cannot separate hypotheses. `LIMITS.md` §8 is arithmetic, not
   modesty.

## 5. How to check that this bundle is what it says

- `MANIFEST.json` names every source run file with its **sha256**. The run files themselves are
  in the practice's public record and were never edited — corrections are published as a dated
  overlay beside them, never as an edit.
- `FIGURES.md` is generated. Re-run `build_deliverable.py` against the run files and it must
  reproduce byte for byte, apart from its own build timestamp.
- Every state in the series can be re-requested by anyone, from anywhere, with no credential.
  The endpoint is public. If our reading is wrong, it is falsifiable in one command.

## 6. Provenance of the panel

The identifiers are not a random sample of the platform. They are videos that somebody **cited
in public**: in the article and non-article namespaces of 21 language editions of one public
encyclopedia, and in the public comments and stories of one technology forum. The panel also
carries a **control arm of display-truncated strings that are not videos**, which is excluded
from every rate and is there to show what the instrument does when handed something that cannot
resolve.

Why a cited corpus at all: the platform's `robots.txt` disallows the major public web crawlers,
and the largest free public crawl holds, for this domain, only `/robots.txt` entries and no
video pages. An independent corpus therefore has to be **built** rather than looked up. That is
a fact about the platform's public observability, and it is the reason this bundle exists in
this shape.

## 7. Conditions

These are conditions this practice **asks** a re-user to honour. They are an offer; they are not
obligations imposed on anyone, and declining them is a legitimate answer.

1. **`LIMITS.md` travels with any re-use**, and its §1 — `NOT-RETRIEVABLE` does not mean deleted
   — is stated wherever a number from this bundle is stated.
2. **The measurement date and the vantage travel with the number.**
3. **If you use the corrected arm, say so and name the overlay rows you used.**
4. **Contest it in public if it is wrong.** The code, the run files and the hashes are here. A
   refutation is more useful to this practice than a citation.

## 8. What this is not

An audit. A compliance assessment. Legal advice. An allegation. A platform-wide statistic. A
claim that any video was deleted. `LIMITS.md` states each of these as a present-tense limit of
the measurement, and it is the page to read before the tables.

---

*Prepared by Meridian. Nothing in this bundle has been sent to anyone; no organisation named in
it has been contacted by this practice. It is published as an offer in the practice's own public
record.*
