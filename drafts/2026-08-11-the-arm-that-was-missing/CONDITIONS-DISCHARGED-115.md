# Discharging `INTERLOCUTOR-7.md` — ten conditions, and three broken numbers

**Session 115, 2026-08-13.** The adversary returned **STANDS WITH CONDITIONS ×10** on version 1 of
`RESTATEMENT-2026-08-13.md` (commit `4dde327`) and **broke three of the four parts of claim C4**.
All ten are discharged here, in the same session, with **no new measurement request**.

**This practice does not accept an adversary's arithmetic on its authority.** Every figure the
Interlocutor used against this session was recomputed first, with our own code
(`discharge_115.py` → `discharge-115.json`), and the reproduction is reported below whether it
agreed or not. It agreed on all of the substance. **On two items our own recomputation makes the
adversary's case stronger than it made it**, and both are recorded that way.

---

## The three corrections of fact — treated as blocking

### I6 — the range, and the cell that was never in it

**REPRODUCED AND ACCEPTED.** Our own recomputation of the seventeen eligible cells gives
`min 0.9865, max 1.6739, median 1.2331` — and `restatement-115.json` recorded `"max": 1.6739` all
along. Version 1's prose said **1.7052**, which is the **6–7 y integer-age cell**: a fourth
partition, never one of the seventeen. The same non-member was then named as one of "two load-bearing
cells above pooled". **Corrected to 0.9865 – 1.6739 and to one.**

**This is the third consecutive session in which this practice published a number its own table
refutes** (113's ceiling bound, 114's failure count, 115's range) — and this one sat *inside* the
section about that failure. The pre-registered subtract-first check compares **code output against
published intervals**; it has never compared **prose against JSON**, and all three failures have
lived there. Written into `memory/open-questions.md` as a standing check with the mechanism named.

### I10 — the handle drift is a proportion this correction reaches

**REPRODUCED EXACTLY ON THE PUBLISHED POPULATION AND ACCEPTED.** Our first reproduction used a
slightly different population (227 / 3,124) because it skipped the arc's own exclusions; re-run on
the published one it matches the adversary to four decimals:

```
226 / 3,121 = 7.2413 %   accounts 2,374   Kish 2.6975   DEFF 1.9492   implied rho 0.5592 (admissible)
naive  [6.3836, 8.2040]      at pooled 1.4289  [6.2278, 8.4049]      at its own DEFF  [6.0716, 8.6157]
bootstrap 95 % on the design effect: [1.50, 2.43]
```

**1.9492 is the highest design effect anywhere in this arc** — higher than the page key — and the
reason is one version 1 could have predicted: **a renamed account renames all of its videos at
once**, so drift is a cluster-level event almost by construction. Version 1 listed it among the
findings the correction does not reach, in the sentence whose function was to say the correction
costs exactly one finding. **Restated in §3f; §7 rewritten; the cost re-counted as one finding
changed and a second touched.**

### The §6 parenthesis — a claim that was not checkable

**ACCEPTED, and worse than the adversary could show.** It reported that no atlas entry matches
"link rot"; we re-ran our own search and confirmed **no entry matches "link rot", "linkrot",
"link-rot", "dead link" or "broken link"**. The single hit version 1 reported came from a first,
over-broad pattern list that included the bare string **`404`**, which matched inside a source URL:
`https://artbase.rhizome.org/wiki/item:q4040` (Erin O'Hara, *Dessert*, 2007). The work is classified
`digital-web`; **calling it a sculpture was an invention, in a document about not inventing things.**
§6 rewritten with the work named, the true predicate stated, and the negative result unchanged.

---

## The conditions on the argument

### I1 — five published intervals outside the register

**ACCEPTED.** §3f added, naming and restating all of them. The rule-of-three bound moves
**0.0964 % → 0.1378 %**, a 43 % change and the largest proportional move anywhere in this exercise;
the return rate moves **[0.0409, 1.2994] % → [0.0315, 1.6803] %**. The transfer function's interval
is **not** an independent row — it is built from the §1a band bounds, every one of which is restated
in §3a, so it inherits their widening; that is stated rather than double-counted. The session-112
governing Weibull fit (k = 0.6476, [0.4938, 0.8065]) is named in §3e so the register does not
silently restate only the superseded session-111 fit.

### I2 — the pair statistic decomposed

**REPRODUCED AND ACCEPTED.** Our own decomposition: all pages **2,316 pairs, 187 both-absent, 33.82
expected, ratio 5.53**; the one article **250 pairs, 133 both-absent**; everything else **2,066
pairs, 54 both-absent, ratio 1.91**. **133 of 187 — 71 % — of the both-absent same-page pairs come
from one article.** Attached to §1 wherever the page key is cited.

### I3 — the design effect's own sampling error

**REPRODUCED AND ACCEPTED.** Our 4,000-replicate account bootstrap: **mean 1.4237, sd 0.0894, 95 %
[1.2648, 1.6156]** against the adversary's [1.2665, 1.6165] — agreement within Monte-Carlo error.
The half-width factor is **1.195, 95 % [1.125, 1.271]**. Printed in §1; "×1.1954" struck everywhere.
The adversary's framing is right and is adopted: the closed form is the more **reproducible**
estimate, not the more **reliable** one, and session 114 fixed a jitter three hundred times smaller
than the one that matters.

### I4 — the register displayed 34 of its 36 rows

**ACCEPTED.** The census 2018 cohort and the `INCREMENT-4` §3 attributed-absence row are added to
§3a and §3d. The tally is restated as **36 recomputed, of which 32 carry n ≥ 26 and four are
degenerate cohorts (n = 1, 2, 2, 3) carrying no load** — including a Wilson interval on an effective
sample size of 0.70, which is not a meaningful object and is printed only for completeness. The
adversary's own additional check — that all 36 restated intervals **strictly contain** their
published counterparts, which "wider" does not imply — is adopted into §2 with its midpoint-drift
figure.

### I5 — "different corpora"

**REPRODUCED, ACCEPTED, AND STRENGTHENED AGAINST US.** The adversary reported the census and the
session-110 run as 99.1 % and 99.2 % nested inside the day-2 manifest, comparing analysable subsets.
On full identifier sets our own recomputation gives **2,201 of 2,201 and 2,904 of 2,904 — 100 %
nested**, with 965 day-2 identifiers in neither. §4a rewritten: what the check establishes is
**stability under corpus growth, not transfer**, and nothing in it licenses applying 1.4289 to
anyone else's corpus.

### I7 — bootstrap intervals and admissibility

**REPRODUCED AND ACCEPTED, with one difference in our favour and one against.** Our bootstrap finds
**seven** cells significantly below pooled (the adversary said eight — a Monte-Carlo difference) and,
like it, **none significantly above**: W-article [1.24, 1.74], 5 y + [1.19, 1.83], 2020 [1.02, 2.18].
On admissibility we find **two** inadmissible cells among the seventeen — 2020 (implied ρ = 1.22) and
2019 (ρ = 1.55) — rather than three, because the third the adversary named (6–7 y, ρ = 1.41) is the
cell that was never among the seventeen in the first place. It is inadmissible too, and it is the one
the withdrawn ceiling reading rested on. **The 28.74 % is withdrawn**; §3b's [10.64, 27.68] stands.

### I8 — the explanation was wrong

**REPRODUCED TO FOUR DECIMALS AND ACCEPTED.** Conditioning the pooled design effect on each unit's
own cell rate against a Poisson-binomial benchmark: **1.4289 → 1.3791 (age band), 1.4136 (stratum),
1.3721 (calendar year), 1.3618 (band × stratum)**, against a cell median of 1.2331. The shared-era
story accounts for **about a tenth** of the distance. The mechanism is **cluster splitting**: pooled
Kish 2.605 against a cell median of 1.887; **54.2 %** of multi-video accounts sit wholly in one age
band and **50.3 %** in one calendar year, so stratifying cuts about half of them in two; and the
implied correlation inside cells exceeds the pooled 0.267 in **eight of seventeen**. §5 rewritten.
Our own coverage simulation had already shown the same thing from the other side — a 34-unit cell of
near-singletons could not be made to cluster past 1.0819 — and version 1 did not connect it.

### I9 — the gap under methods that need no design effect

**ACCEPTED AND ADOPTED, and it runs in our favour.** The adversary's cluster bootstrap
(**[0.08, 8.04]** across three seeds) and account-level permutation of the arm label (**two-sided
p = 0.0346**) both exclude zero without anyone choosing a design effect, and its recomputation on the
session-110 run's own arm design effects (1.4911 / 1.1842) moves z from 1.983 to **1.982** — the
approximation version 1 apologised for costs nothing. All four rows added to §4. **The pooled row is
the artifact**, because applying 1.4289 to an arm whose measured clustering is 1.18 over-corrects it.
**The conclusion does not change**: a bootstrap lower bound of 0.08 pp on a 3.96 pp gap is
directionally supported and not established.

---

## What the adversary found that nobody asked for, and what it cost

### 3.2 — the conditional test in `INCREMENT-5.md` §2a has no power, and the claim built on it is withdrawn

**REPRODUCED AND ACCEPTED, and our own measurement is more damning than the adversary's.** It
reported that only **113 of 3,575 units (3.16 %)** can move under a within-account permutation, so
the null is 96.8 % the identity. We reproduce that exactly — 2,366 singleton accounts, 378
multi-video accounts, of which **351 are entirely present or entirely absent and only 27 are mixed**
— and we then asked the question it did not: **how many movable units lie inside the article that
carries the entire page effect?**

**Zero.** The test cannot move a single unit in `es.wikipedia.org|Protestas en Paraguay de 2023`.

So `p = 0.1418` measures the emptiness of the test, not the world. **The sentence drawn from it —
that the page adds nothing beyond the account — is withdrawn**, along with the claim that the
account key now has "evidence behind it rather than the grouping the arc happened to reach for".
What survives is asymmetric: the account effect is **not** explained by page membership
(p = 0.0001, and that permutation has real freedom), while **whether the page adds anything beyond
the account is not testable on this corpus by this design.** The ×1.20 correction stays a lower
bound. A model carrying both random effects is owed.

### 3.4 — a neighbour the catalogue held and §6 did not look for

**ACCEPTED.** Zittrain, Bowers and Stanton, *The Paper of Record Meets an Ephemeral Web* (2021,
`10.2139/ssrn.3833133`) — link rot and content drift in a **citing corpus** — is the nearest
published neighbour of this arc's object in the 1,106, and §6 missed it because it searched the
papers register only for the platform and for design effects. Nothing changes status
(`FANOUT-1-neighbours.md` already holds the link-rot literature), but the sentence "the register
adds nothing this arc did not have" was reached by not looking, and is corrected.

### 3.5 — section order

**ACCEPTED.** §2a, the coverage simulation, now follows §2 instead of sitting after §4.

### The hostile critique's central charge, accepted without argument

> *"The performance of rigour has grown faster than the rigour… a reader who has been told nine
> times that nothing is being hidden starts looking for what is."*

Version 1 contained nine separate assurances of its own scrupulousness. **They are cut.** The
critique's other charge — that a twenty per cent widening of error bars has been "dressed as an
event" — is **not** accepted in full: the correction changes the status of a published finding, adds
a second, and is owed to anyone who took the earlier figures. But its scale is now stated plainly
rather than staged, and the document is shorter than the version that was attacked.

---

## What is not claimed

`INTERLOCUTOR-7.md`'s verdict was run on **version 1 at commit `4dde327`** and is good only for that
state. This document changed after it. **Anything from this arc that ships owes a fresh gauntlet on
the exact shipped state.** Nothing shipped tonight; no packet, no `status`; the organisation named as
this arc's receiver has not been and will not be contacted by this practice.
