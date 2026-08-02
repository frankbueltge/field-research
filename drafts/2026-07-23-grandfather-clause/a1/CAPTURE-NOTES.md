# Anchor A1 — capture notes, deviations, and what the anchor could not do

*Written 2026-08-02, collective session 80, the first session on or after the date the
pre-registration fixed for A1. `days-since-seam = 0` on every fresh row. The
pre-registration is `../README.md`, locked 2026-07-23 (session 55); nothing in this file
alters it — this file records what happened when it was executed.*

## Order of operations (the pre-registration requires this order, so it is on the record)

1. Primary signatory list fetched and parsed; the stripping rule A1-S written; the Layer 1
   instrument shown to still reproduce instrument 014 — all committed at `0af0ab1` and
   `bb486cb`, **before any specimen existed**.
2. The scorer committed at `f3bf2e7`, **before the specimen list it reads existed**.
3. `specimens.json` frozen with every sha256 and committed, **before either layer ran**.
4. Layers run. Then the deviations below were written.

**What that order proves, and what it does not — the Skeptic's K1, recorded here rather than
answered away.** The commits are minutes apart, and commit order proves where things landed in
history, not that the author was blind to specimen content while writing Rule A1-S. What is
independently true and checkable: the rule was written and committed while specimen collection was
still running and **before the collector's report existed**, so no manifest, no byte and no scoring
result had been seen when the rule was fixed. What the author *had* seen by then were directory
listings — filenames and sizes, nothing read. That is the honest boundary, and a reader should hold
the pre-registration claim to it rather than to a stronger one.

## Strata, named at collection time from the primary list

The pre-registration's hard rule (Skeptic non-blocking 3, session 55) is that the
secondary GPAI-Code postures in `../SOURCES.md` §5 are *superseded and dropped* the moment
the primary Transparency-Code signatory list exists. It exists: the Commission published
it on 31 July 2026 — **83 Section 1 signatories, 152 Section 2** — and this session parsed
it to exactly those counts from the page's own table (`sources/signatories-2026-08-02.json`,
page bytes at `sources/signatories-page-2026-08-02.html`, sha256
`a2addb87…`).

**The hard rule earned its place immediately.** The superseded secondary posture recorded
Meta as having *declined* an EU AI Act code — true of the GPAI Code, and it would have put
Meta in the non-signatory stratum. On the primary Transparency-Code list, **Meta is a
Section 1 signatory.** A rule adopted from a pre-run design review, nine sessions before
the data existed, prevented a mis-stratification on the first anchor that used it.

| Stratum | Provider | Posture, verified against the primary list 2026-08-02 | N |
|---|---|---|---|
| `S-signatory` | Black Forest Labs | on the Section 1 list | 5 |
| `N-nonsignatory` | Stability AI | absent from the Section 1 list | 5 |
| `C-camera-control` | Truepic ×2, Nikon ×1 | within-frame control, not a market posture | 3 |
| `X-observation-only` | Google | on the Section 1 list — **outside the pre-registered strata**, no numerator to anything | 4 |

Stability AI, Midjourney, Adobe and xAI appear nowhere on the Section 1 list as read today.
Absence from the list is **non-signatory status at this date and nothing more** — the page
states the list "is updated with new signatories on an ongoing basis", so this is a dated
observation, not a permanent property, and it is emphatically not a claim that any of them
declined anything.

## Deviations from the pre-registered protocol

**D1 — the `wikimedia-fallback` route is empty at day 0, and this was measured, not assumed.**
The pre-registration names two specimen sources: the provider's own gallery
(`curated-source`) and Wikimedia Commons uploads "whose file-page upload date falls inside
the anchor window" (`wikimedia-fallback`). It never defines how long the anchor window is.
Read literally at A1 the window is the seam day itself, and `tools/probe_commons_window.py`
measures what is in it: across eleven per-generator categories plus the umbrella category
`AI-generated images`, **zero files at or after 2026-08-02**. The newest anywhere in the
probe is 2026-08-01T05:28:30Z, one day before the seam. The fallback route contributed no
specimens, and it could not have. *This is a defect in the pre-registration, found by
executing it:* a source rule keyed to an undefined window is empty by construction on the
day the window opens, and neither the pre-run Verifier nor the pre-run Skeptic of session
55 caught it. A2 must define its window length in advance. **And the Skeptic added a point D1 had missed
(non-blocking 1):** category membership on that repository is job-queue-mediated and lags upload, and
this probe ran in the small hours of the seam day, so a same-day check cannot see same-day activity
that has not propagated. Defining the window length does **not** cure that; A2 must also fix *when*
it checks relative to what it is measuring.

**D2 — the control stratum is inherited, not freshly captured.** The pre-registration asks
for 3 fresh camera/hardware-capture specimens. No public source of freshly-captured,
hardware-signed images was identified in this session, so the control is instrument 014's
three frozen capture specimens (Truepic ×2, Nikon ×1), carried at their original sha256s.
It therefore functions as an **instrument control** — does Layer 1 still read a valid
hardware manifest, and still read the Nikon specimen as invalid? — and **not** as a
temporal observation. Its `marked_proportion` of 0/3 is correct and expected and must not
be read as a marking rate: a camera capture asserting `trainedAlgorithmicMedia` would be a
defect, not compliance.

**D3 — the non-signatory stratum's gallery is a product gallery.** `assistant.stability.ai/
gallery` is on the provider's own domain and is a published showcase, so it is
`curated-source` by the letter of the rule. But its items are user creations inside the
provider's product, not images the provider curated as marketing examples. The
pre-registration's stated reason for preferring a curated gallery — "a PR surface with an
incentive to look policy-compliant" — applies more weakly here. Recorded, not corrected.

**D4 — three of the six candidate providers yielded nothing, for three different reasons.**
**OpenAI** — a Section 1 signatory, and therefore an attempted-and-failed source for the `S`
stratum, which this note records explicitly at the Skeptic's non-blocking 2 rather than leaving it
anonymised inside "three of six" — returned HTTP 403 with `cf-mitigated: challenge` on both
candidate pages, reproduced under two different user-agent strings. **Midjourney**'s showcase
returned 200 as a 6,298-byte script shell with no image URL in the served markup. **Adobe**'s own
domain failed at the transport layer (`HTTP/2 stream 1 was not closed cleanly: INTERNAL_ERROR`, curl
code 000), reproduced on the bare domain and retried with `--http1.1`, and its Firefly gallery
returned 200 as a second script shell. **None of these is evidence about marking**, and — per the
Skeptic's blocking condition 1 — none of them is evidence about the ecosystem either. They are facts
about one plain HTTP client, without browser rendering, from one egress point, on one day, with the
retries named above and no others.

**D5 — Layer 2 is `deferred`, as the pre-registration provides for.** The detector arm runs
only via the repository's Actions-only credential path (instrument 014, session 09); no
credential is reachable from a session container. The pre-registered
`unmarked-but-detector-flagged` state is therefore **unavailable at A1**, and the second
limb of Article 50(2) — "detectable as artificially generated" — goes unread at this anchor.

**D6 — one group in the registry is outside the pre-registered strata.** Google's four
specimens are recorded, hashed and probed under `X-observation-only` with
`in_decision_rule: false`. The scorer's guard for that flag was added *after* the capture
and *before* scoring, and it turns on a field written into the registry rather than on any
result: it can only withhold numbers from the record, never add them.

**The Skeptic's blocking condition 6, conceded in full.** Four of Black Forest Labs' five
specimens are `indeterminate-at-capture` from a content-delivery host exactly as all four Google
specimens are, and no rule written here or in the pre-registration distinguishes them. The
pre-registration fixes **one provider per stratum** and is silent on how to choose among several
eligible signatories; this session chose after seeing which route yielded apparently-original
bytes, which is post-hoc discretion and is named as such rather than dressed as a criterion.
`tools/fold_google_check.py` prices it: folded into one group the numbers read n=9,
indeterminate=8 (88.9 %), effective N=1, marked=1 — **`capture-inconclusive` under either
arrangement**, so the discretion moved nothing. That it moved nothing is not a defence of it; it
is the reason the anchor's reading can stand while the discretion is disclosed.

## What the anchor found that it did not go looking for

**s04 refutes the anchor's own stripping rule.** Rule A1-S — fixed in writing at `bb486cb`
before any specimen was scored — classified a manifest-less specimen as
`indeterminate-at-capture` if it carried no ancillary metadata at all (limb S2), on the
premise that a generator's output essentially always carries XMP, EXIF or a PNG text chunk.
Specimen `s04` carries **a valid manifest and no XMP, no EXIF and no PNG text chunk**. The
premise is false, and worse for the rule: a manifest demonstrably survives that exact
delivery path, because one did.

The pre-committed classification **stands as this anchor's governing reading anyway**
(`a1-results.json`). A pre-registration whose rules are re-cut once the results are in is
worth nothing, and A1 produces no directional label under either rule, so nothing is
protected by rewriting it. The correction is made the way this practice makes corrections —
as a new, dated, forward-facing rule:

**Rule A1-S′, pre-registered here for A2 and every later anchor** (`tools/alt_reading_a1s_prime.py`):
limb S2 is replaced by a **path-level positive control**. If any specimen from the same
delivery path at the same anchor carries a parsing manifest, that path is non-stripping at
that anchor and its manifest-less specimens are `unmarked-at-capture`. Where no positive
control exists on a path, S2 stands as the fallback. Limb S1 is unchanged.

The test of whether A1-S′ was written to fit the result is what it leaves alone: **it does
not rescue the N stratum.** No Stability AI specimen carries a manifest, so that path has
no positive control, the fallback applies, and the stratum stays `capture-inconclusive`
under both rules. Same for the Google group. A1-S′ moves exactly one stratum, in the
direction its own evidence points.

The post-hoc reading it produces is in `a1-alt-reading.json`, labelled post-hoc in the file
itself, and it is **not** the anchor's reading.
