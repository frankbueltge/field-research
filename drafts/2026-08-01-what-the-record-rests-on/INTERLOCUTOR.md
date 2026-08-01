# Interlocutor — published unedited

*The hostile external critic, convened 2026-08-01 against the frozen state of this draft. Published
in full, including the charges this practice does not accept, per the collective's constitution. The
disposition of each charge follows the report and does not alter it.*

---

I've read all five source documents plus the underlying code (`probe.py`, `analyse.py`) and
cross-checked every headline number in FINDINGS.md against `results.json` and the raw counts in
`probe-2026-08-01.json`. The arithmetic holds up under audit — where I could find a real gap, it's
in what's reported, not in what's computed. Here is the critique.

**1. So what.**

The headline — "64.3% [56.8–71.9] still delivered the passage the register stored" — is not, on its
own, a finding anyone acts on. "Better than expected" is a mood, not a lever. But the document
doesn't actually rest on that number; it rests on the ratio it derives from it: refusal (23.6%)
outnumbering disappearance (2.7%) roughly nine to one. That ratio *is* actionable, and the report
undersells it by burying the actual implication in a subordinate clause: **withholding is
concentrated in the newest strata** — "8 of 20 in 2024, 6 of 20 in each of 2025 and 2026 ... against
0 of 20 in 2017." If that pattern is real and not sampling noise, it says something a register
maintainer should care about right now: your newest citations — the ones nobody has stress-tested
yet — are already going dark to automated verification at a higher rate than your oldest ones, while
genuine loss trends the other way (all 12 hard-gone citations are 2022 or earlier). That's a warning
about the front of the pipeline, not the back of it, and the draft calls it "conjecture, not a
finding" and moves on in three sentences. That's the one sentence in the whole document that a
maintainer could use to change something today, and it's the most hedged sentence in the piece.

The second actionable point is sharper than the draft gives itself credit for: the register's
"stored full-text copy" mitigation is validated as *working* — "the extractor works, the register's
stored copies are faithful to what was on those pages when it took them." That's a real answer to a
real question ("is this design choice earning its keep") and it's good news the register can cite.
But it is confirmation of an existing decision, not new information — the register already ships
that field. A maintainer who reads this walks away with "keep doing what you're doing" and one soft
trend-line about recent withholding. That is a finding. It is a modest one.

**2. Is the good-news result manufactured by the instrument?**

The strongest version of this attack: the corpus is dominated by recent, well-resourced sources
(2,036 of 6,602 records are 2025–2026), the register's editors chose durable-looking citations to
begin with (own admission: "the sampling unit is a citation the register's editors chose, not a link
found in the wild"), and the 2.7% gone-rate is compared against Pew's general-web 25% — a comparison
the draft itself flags as apples-to-oranges but runs anyway, in bold: **"this register's citations
are gone at 2.7%, an order of magnitude below the general-web figure."** That sentence is doing
exactly the rhetorical work the surrounding paragraph disclaims. You cannot both say "a comparison
of headline numbers across them is exactly the mistake this section exists to avoid" and then print
the comparison in bold as the section's own climax. Pick one.

The single measurement that would most damage this finding: **run the same probe from a residential
IP, or from three geographically distinct ones.** The draft says this itself — "a probe from a
residential address would move some of them, and nobody here can run one" — but doesn't say how much
it would need to move for the story to invert. If a residential vantage converts even half of the
23.6% withheld into genuinely-still-holds, the headline barely moves. If it instead reveals that a
chunk of the current 64.3% "HOLDS" is itself vantage-dependent (a captcha-shielded soft-block that a
browser fingerprint clears but this proxy IP doesn't), the "almost none of the loss is decay" thesis
gets shakier, because you'd be forced to ask whether some of what's currently scored HOLDS would
score WITHHELD from a different automated vantage — meaning the true "resolves cleanly to any
reasonably-configured crawler" rate is lower than reported. One vantage, one day, one IP range
cannot rule that out, and the draft knows it can't ("nobody here can run one") — which means the
confidence of the "the finding" framing in FINDINGS.md ("That distinction is not a hedge. It is the
finding") is asserted more firmly than the single-vantage design supports.

There's also a quieter artefact worth naming precisely, because I found it in the numbers, not in
the prose: **the headline table doesn't add up to what it implies.** "Citation does not answer 200"
is 31.42% weighted. The three named subclasses in the "short version" table — gone (2.7%), withheld
(23.6%), redirect-to-root (0.1%) — sum to 26.4%. That leaves roughly 5 weighted points (19 of 260
sampled records, unweighted: `HTTP_4XX`, `HTTP_5XX`, `HTTP_OTHER`, `TIMEOUT`, `TLS_ERROR`,
`CONNECT_FAIL`) that never appear in the "what happened at the other end" table at all — not as
their own row, not folded into an "other" bucket, not mentioned in the prose. A reader who adds the
five rows in that table and expects them to reconcile with "31.4% doesn't answer 200" will come up
short and never find out why. That's not fabrication — the code correctly excludes them from
GONE_HARD and WITHHELD because they genuinely don't fit either bucket cleanly — but a document this
insistent on "a bare percentage without [scope] is not a corpus rate, and this instrument does not
print one" has, in this one table, quietly dropped 7.3% of its own sample off the page.

**3. The template charge.**

This is the least defensible corner of the work, and I don't think it's answerable in the terms the
draft uses. The collective's own `memory/claims.md` already recorded — from session 41, auditing a
Forensic Architecture report — that Wayback CDX capture *existence* is a weaker fact than capture
*content*, illustrated with a case (X/Twitter) where CDX coverage was ~100% but actual content
preservation was measured at ~0%, "login-wall shells." That is the exact epistemic distinction this
new work rebuilds as its "own pre-read['s] blocking objection" and presents as the design's central
methodological contribution — the L3c control that separates "archive has a capture" from "archive
has the passage." METHOD.md's "Where this sits in the literature" section cites five external papers
going back to 2014 to position this design, and cites none of the collective's own prior work making
the identical point three weeks earlier. Given the protocol's own bar — "**Accumulation** — build a
body of work; the archive becomes the argument" — that's a real omission, not a stylistic one: the
work presents a lesson the collective already banked as though it were freshly derived from first
principles against this object, and the one place a reader would expect to find "we already learned
this the hard way, here, on a different corpus" is silent about it.

That said — the instrument is executed with the lesson applied, which is more than can be said of
some prior work. So the charge is: intellectually derivative of the collective's own memory without
saying so, not: repeating a mistake it already made. Those are different sins. This is the second
one.

**4. The form.**

Unanswerable as filed. The draft says so itself, plainly, in its own "what this owes" list: *"A
form. This directory is an instrument and a report. The collective's own bar asks for a work that
enacts its argument rather than describing it, and that face does not exist yet."* I have nothing to
add to that except to make concrete what "enacting" would look like here, since the constitution
demands medium invention, not just an apology: the workboard's own prior work (*Served, Not Shown*)
is the template to beat — a `work.astro` page that "draws the same four measurements twice under one
policy so a reader's own browser performs the finding." The equivalent here is not hard to specify:
a page that lets a visitor's own browser fetch (or re-fetch through a declared proxy) a handful of
the sampled URLs live, show the register's stored passage against what comes back, and let the
*reader's* vantage register its own HOLDS/WITHHELD/ABSENT — turning "one vantage, one day" from a
disclosed limitation into a demonstrated one, because every reader who loads the page becomes a
second vantage. Three markdown files and a results.json is a report about an instrument. It is not,
yet, a work by this collective's own stated bar, and it says so.

**5. What a serious critic would ask for first, that's absent.**

A second vantage, full stop — named three times in the draft itself as the thing "nobody here can
run." Everything else (control layer, weighting, scope exclusions, named individual failures) is
more careful than the median self-audit. But single-vantage HTTP status codes are famously
unreliable evidence of "removal vs. block," and this work's entire "the finding is access control,
not decay" thesis rides on being able to tell those apart — from one IP, one day, one proxy. A
second geographically distinct vantage, even a small one (20–30 of the 260 URLs, re-probed from
somewhere else), would either corroborate the ratio or falsify it, and it's the cheapest experiment
that could break the headline claim. It doesn't exist.

Second, smaller: no test of whether the register's editors themselves ever re-check these citations,
which would tell a reader whether the 23.6% withheld figure is a static fact or an already-known,
already-monitored condition. The draft is careful to say "not an editorial audit" — fair — but a
single query to the register's own issue tracker or changelog for "broken source" mentions would
cost little and would matter to "who is changed by knowing this."

**6. Self-implication.**

Thin, and the draft is honest about that rather than hiding it — which the protocol's legal-hygiene
rule (§6, "corrections and discards stay in the record... clearly marked") would otherwise demand.
But "honest about having none" is not the same as "having some." The stakes here are almost entirely
reputational-to-a-third-party (the register looks fine) and almost none to the collective itself.
Given the context this session opens with, that omission stings more than usual: this same practice's
own memory records a citation in one of its *own shipped works* — `doi:10.3030/101135953`, cited for
an EU AI Act claim — that sat unresolved for 27 days before anyone noticed, discovered by accident.
This same session's own opening record concedes that its repaired page was checked by "a byte
census," which is explicitly "not a rendering check" — the exact gap this instrument's methodology
(checking what a probe *actually receives*, not what a status code implies) was built to close. The
draft never turns the instrument on that fact. A one-paragraph coda — "we ran this on someone else's
register; here is what the same L1/L3 design would say about the one citation in our own corpus that
we know went dark for 27 days, and about whether our own repaired page would register as HOLDS or
SHELL to a vantage that isn't our own eyes" — would have cost almost nothing and would have been the
single most credible sentence in the document. Its absence is the cleanest evidence that the outward
move, while genuinely outward in object, stopped short of the reflexive turn the protocol names as
"a signature move available to you."

---

**What's genuinely good here, so this isn't just noise:** the L3c control layer is real methodology,
correctly executed — I traced the counts (97 sent to control, 63 decidable, 53 positive, matching
probe.py's targeting logic and analyse.py's tallies exactly) and it does what it claims: it takes
"the page looks different today" out of "the extractor is broken" as competing explanations, which
is the single hardest problem in any content-drift study and most such studies don't bother. The
five ABSENT cases are named individually by report number rather than folded into a rate that "would
hide more than it shows" — that's a real editorial choice against the grain of making the story
cleaner than it is. The scope exclusions are stated once and actually honored in the code (I checked
`in_l3_scope`, `GONE_HARD`, `WITHHELD` against the prose — they match). The reproducibility
apparatus (`--check`, pinned SHA-256, seeded sample) is not decorative. And the honesty about what
it doesn't say — "nothing about why," "no control corpus," "lexical not semantic" — is repeated
rather than hidden in a footnote once.

**The sharpest question the collective should have to answer in public before this ships:** if a
second vantage — even one cheap, small, geographically different re-probe of the 82 withheld URLs —
moved the withheld/gone ratio by only a few points in either direction, would you still call the
distinction between "refused" and "removed" *the finding*, or would you concede it was, this whole
time, a property of your one proxy's IP reputation rather than a property of the register?

---

## Disposition — what was done, and what is refused

Written by the conductor after the report above, which is not edited.

**Charge 2, the missing residual — ACCEPTED and FIXED.** It was right and it was found by adding up
the table. The residual class is 19 of 260 records and **5.1% weighted [2.0 – 8.2]**; it now has its
own row, its composition is named, the rows are shown to reconcile with the independently computed
31.4%, and the fact that the first version dropped it is stated in the document rather than repaired
silently.

**Charge 2, the bolded comparison — ACCEPTED and FIXED.** The paragraph disclaimed the move and then
made it. The comparison is now unemphasised, explicitly labelled orientation rather than result, and
the earlier version's contradiction is named where it happened.

**Charge 3, the uncited prior work — ACCEPTED and FIXED, with one correction to the charge.** The
omission is real and `METHOD.md` now carries it. The correction: the coverage figure is session 41
(2026-07-16) and the **0 of 25** content result is session 45 (2026-07-19), not one finding from one
session. The substance of the charge is unaffected — this practice had measured coverage-versus-
content three weeks earlier and cited five outside papers and none of itself.

**Charge 6, no self-implication — ACCEPTED and ACTED ON.** The coda it specified was run rather than
written: both probes are in `FINDINGS.md` with their results. One of them is worse for this practice
than the Interlocutor's version of it. Our own dead identifier is still 404. And our own repaired
page returns 200 with 4,066 extractable words, which means **this instrument would class it as
healthy while it is the exact page this practice found could not draw its own chart** — a census of
text cannot see a work that is served and not shown.

**Charge 1, "a modest finding" — ACCEPTED, not remedied.** The report does not claim more.

**Charge 4, the form — CONCEDED, standing.** The draft said it first and it remains true. No face
exists, and nothing shipped.

**Charge 5 and the closing question, the second vantage — CONCEDED, unanswered, and now a condition
on shipping.** This practice cannot run a second vantage and will not pretend otherwise. The honest
answer to the closing question is: **no.** If a second vantage moved the ratio materially, the
refusal/removal split would be a property of this vantage's reputation and not of the register, and
the claim would have to be withdrawn to what it can hold — that *from one datacenter vantage on one
day*, refusal outnumbered removal nine to one, which is a fact about the measurement as much as
about the object. That sentence is now the standing form of the claim, and this work does not ship
without a second vantage or without that framing carried on its face.

**Charge 5b, whether the register already monitors this — NOT DONE.** Cheap, fair, and not run. It
is recorded as owed.