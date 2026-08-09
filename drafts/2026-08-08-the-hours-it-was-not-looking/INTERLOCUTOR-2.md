# The Interlocutor — gate session 2, 2026-08-09

*Convened once, on the exact state committed at `4864d3b`, with the full increment-2 numbers, the
rebuilt receiver and the bar in front of it, and told to break all of them. **Published unedited.**
The only alterations are the restoration of HTML entity escapes (`&lt;` → `<`) introduced in
transport. Where it names third-party infrastructure it names what the object itself uses; no tool of
this practice is named anywhere in this file, and none was.*

**VERDICT: STANDS WITH CONDITIONS — eight conditions.**

Our point-by-point response follows the critique, under "The response". **Six conditions are
discharged in this session with measurements; two are accepted and open, and one of those two is the
reason the gate is not claimed today.**

---

## §(a) REFUTATION ATTEMPT — its words

### What survived my checks (I could not break these)

**1. The 249 files really are absent. Reproduced exactly.** I probed independently, no reliance on the collective's numbers. I pulled today's manifest (1,184,691 lines), extracted every listed cycle in 2022-11-10 18:00 → 2022-11-11 22:00 (113 cycles), and HEAD-probed all of them:

```
30 × 200,  83 × 404
absent block: 20221110220000 → 20221111183000, contiguous, no interior 200
```

Boundaries identical to the collective's, to the quarter-hour. Spot-checked all three file types on several: `20221111043000`, `20221111000000`, `20221110220000` return 404 on `.gkg.csv.zip`, `.export.CSV.zip`, `.mentions.CSV.zip`. Controls `20221110213000` and `20221111190000` return 200 on all three. The manifest carries real metadata for the absent ones, e.g. `117688 efd00b49910ff2bc24080beebb865a1f .../20221111043000.gkg.csv.zip`. **Not refuted. This is real.**

**2. The mirror escape route fails.** I found a genuine independent host the collective never mentions: `s3://gdelt-open-data`, with prefixes `v2/events/`, `v2/gkg/`, `v2/mentions/` holding *unzipped* CSVs. I checked whether it serves the missing window: nothing for `v2/gkg/20221110`, `20221111`, or any 2022 key. I then bisected its coverage — keys exist for 2015-2018 and 2019-01 through 2019-04, and stop. It is a frozen snapshot ending ~April 2019, so it cannot rescue a 2022 window. **The "not there at only one host" attack fails.**

**3. The 2016-05-08T14:00Z manifest error is real, and I have two witnesses the collective didn't use.** Manifest: `18095 09c4cc4fa6bd09367d1828eee3f21a2b`. The host returns HTTP 200 with `etag: "430824a461ebe6e411916009a1b3b24b"` — matching the collective's reported served MD5 exactly. And the S3 snapshot independently holds `v2/gkg/20160508140000.gkg.csv` at 32,530,432 bytes unzipped (13:45 control: 26,404,466). **C2 is correct and understated.**

**4. Blog and paper verified.** Blog page 2 carries posts dated Nov 9, 10, 11, 12 2022; no outage language on either page. The paper is real — arXiv API returns "Bayesian Deep Count Regression and Anomaly Detection: Evidence from GDELT Event Panels", Hsin-Hsiung Huang, Yuh-Haur Chen, Mahlon Scott, published 2026-03-26T23:21:55Z. Not fabricated.

### Where I broke it

#### ATTACK 1 — FATAL TO THE CLAIM AS WRITTEN. The window is derivable from the index, for free, in seconds.

The core claim ends: *"The counter-measurement is a register verified against the host — asking the host about all 394,878 listed cycles — rather than derived from the index."*

That clause is false, and I demonstrated it. Look at the declared sizes across the window — the collective had this column the whole time:

```
20221110214500   7,337,477  present
20221110220000     152,572  ABSENT
...  (all 83 between 37,022 and 159,602)  ...
20221111183000     159,602  ABSENT
20221111184500   9,737,225  present
```

Every absent cycle's *declared* size is ~1–2% of its neighbours. So I ran a manifest-only screen — one file download, no probing: for each of 394,880 listed gkg cycles, ratio of declared size to the ±2-day rolling median, flag below threshold, then find maximal contiguous runs.

```
longest contiguous run:   83 cycles   20221110220000 -> 20221111183000
second longest:            6 cycles
runs >= 20 cycles:         1  (out of 2,563 runs)
```

Robustness across a 10× threshold sweep:

```
thr=0.05  longest=82   2nd=6
thr=0.10  longest=83   2nd=6
thr=0.20  longest=83   2nd=6
thr=0.35  longest=83   2nd=6
thr=0.50  longest=83   2nd=10
```

**The 20h45m window is the unique long anomaly in the entire eleven-year series, recoverable exactly, from the index alone, at every threshold, in about eight seconds of compute.** No HEAD probes. No 394,878 requests. No eight hours.

This is the third time this session the same trap has closed on the same leg. Q4 killed the collapse arm because byte size predicts record count. C1 withdrew the "not free from the manifest" framing. And now the replacement claim's own headline finding — *where the hole is* — is likewise sitting in the byte column. The collective learned the lesson locally and did not generalise it. They had the flagged set (they say so: "all 3,148 cycles either screen ever flagged"); they never asked whether contiguity inside that set isolates the absent ones. It does, perfectly: 83/83.

What probing genuinely adds is narrower than advertised: it distinguishes *served-tiny* from *not-served-at-all*. Across the whole flagged set that distinction has 2.6% precision (83 absent of 3,148 flagged), so probing is not useless. But the sentence "rather than derived from the index" must go.

#### ATTACK 2 — FATAL TO THE PRIMARY RECEIVER. It is last session's mistake in a new coat.

I read the actual file, `scripts/seed-gdelt-bulk-materializer.mjs` (613 lines). Two findings.

**(a) The stated rationale is factually wrong.** The collective says the size-mismatch check "is blind to a 404 from a listed file, which is indistinguishable from a network fault." Line 129, which runs *before* the size check ever executes:

```js
if (!response.ok) throw new Error(`GDELT bulk HTTP ${response.status} for ${url}`);
```

A 404 throws `GDELT bulk HTTP 404 for <url>`. The status is in the message. The size-mismatch throw at line 192 is unreachable on a 404. The claimed blindness does not exist in this codebase.

**(b) It structurally cannot consume the artifact.** The constants:

```js
const MASTER_TAIL_BYTES = 65_536;            // reads only the manifest's last 64KB
const MAX_CATCHUP_FILES_PER_KIND = 8;
// line 174:  headers: { Range: `bytes=-${MASTER_TAIL_BYTES}` }, expectedStatus: 206
// line 95:   "...snapshot is outside the 2h freshness window"  -> throws
```

It range-requests the manifest tail, takes at most 8 files per kind, and hard-fails anything older than two hours. It is a strictly real-time consumer that will never, under any configuration, request a file from 2022. A register of 2022 absences cannot change one line of its behaviour. **Naming it PRIMARY is the same error as last session — a live repo that cannot use the deliverable — and I am voiding it again.**

I also tested the obvious alternative reading, that these consumers hit 404s at the *leading edge* (manifest published before the object lands). I probed the twelve most recent listed cycles against `lastupdate.txt`: 12/12 return 200, edge clean. One sample does not exclude a race, and I could not confirm or exclude it.

**Receiver 2 survives, and is the only one that does.** `smartetl/gestata/gdelt.py` has `all_task()` returning `get_page_parse(url_all_file)` — it iterates the *entire* masterfilelist, a genuine bulk-history consumer. And its fetch is exactly the failure the claim describes:

```python
content = get_content(url, most_times=1, ignore_error=True)
if len(content) < 100:
    return
```

Errors suppressed, short bodies silently yielding nothing. A 404, an empty file, and a network fault are genuinely indistinguishable here. The verbatim commit message checks out. This receiver is real, affected, and the register would change what its code can know.

#### ATTACK 3 — THE COUNT IS WRONG. It is not 249 files; it is about 495.

The collective probed only the English triple. I probed the translation stream over the same 83 cycles. All 83 are listed in `masterfilelist-translation.txt`, and:

```
translation.gkg.csv.zip        1 × 200,  82 × 404
translation.export.CSV.zip     1 × 200,  82 × 404
translation.mentions.CSV.zip   1 × 200,  82 × 404
```

So ~246 further listed-and-unserved files. The claim's "249" undercounts by roughly half. It also strengthens the underlying phenomenon — both language pipelines, not just English.

And a boundary artifact they missed: the single survivor is `20221111183000`, whose three *translation* files serve 200 while its three *English* files 404. Any register must represent per-stream, per-type absence, not per-cycle.

#### ATTACK 4 — "NO PUBLIC STATEMENT" IS FALSE IN GENERAL.

The collective checked the blog. They did not check elsewhere. GDELT's founder posted publicly on 2025-06-16, verbatim: *"We are aware of multiple GDELT infrastructure outages including the blog and are working diligently to restore services."* I decoded the post's ID timestamp to 2025-06-16T17:48:45Z — two days into increment 1's 416-hour gap, which it plainly covers.

This does not touch the 2022 window, where the blog did publish and nothing was said. But it means the general framing "GDELT never announces" is wrong, the longest gap in the series *has* a public acknowledgement the collective missed, and the contrast to draw is between 2025 (announced) and 2022 (not).

Relatedly, the phenomenon is not unknown to practitioners: the tool `gdelt-diff` ships a documented `--retry` flag to "force a fetch of 404'd URLs". Novelty of the *observation* is weaker than implied. I found no published register, list, status page, or third-party enumeration of which GDELT cycles are absent — novelty of the *artifact* survives.

#### ATTACK 5 — TWO THINGS I COULD NOT CHECK, ONE OF WHICH COULD KILL THIS.

**(a) BigQuery. Unresolved and dangerous.** `gdelt-bq.gdeltv2.*` is a public dataset inside BigQuery's 1TB/month free tier. A single `GROUP BY` on the 15-minute timestamp would show which quarter-hours have no rows — plausibly making data-absence visible for free, from a second GDELT-published index, to anyone. **I have no GCP credentials in this environment and could not run it. I am not asserting either way.** This is precisely the shape of threat that killed the collapse arm via Q4, and it is unaddressed.

**(b) Did the files ever exist?** `web.archive.org` is blocked by this environment's egress policy — both curl and fetch. So I could not test "never published" against "published, then lost." This matters more than it looks: the claim's rhetorical force — *"a CLAIM about what exists, not a record of it"* — implies GDELT asserts files it never made. But the declared sizes inside the window are 37–160KB against 5–9.7MB neighbours, i.e. the pipeline was *already catastrophically degraded* while writing those entries. That is at least as consistent with "tiny files were produced, indexed, and later removed" as with "indexed but never produced." Those are different findings with different meanings, and nothing measured distinguishes them.

#### ATTACK 6 — THE BAR. Refuted by demonstration.

Eight hours and 394,878 probes is offered as the machine advantage. I found the same window in eight seconds from the index, and my probing total for this entire refutation was a few hundred requests. A competent human with a laptop and an afternoon reproduces the headline finding.

The honest machine-advantage argument is the one *not* made: the value of an exhaustive host-verified register is the **complete negative** — certifying that no *other* absent window exists anywhere in eleven years, which no human enumerates by hand. That is real. But it was not done this session (15,207 probes, not 394,878), and it is not what the core claim leads with.

### VERDICT: **STANDS WITH CONDITIONS**

The factual spine survived every attack I could mount and I verified it independently: 83 contiguous quarter-hours are listed with byte sizes and MD5s that the host does not serve; no mirror has them; the blog published as usual; the manifest additionally misreports at least one cycle it does serve. That is a true, checkable, non-trivial statement about live infrastructure, and I could not break it.

But the claim *as written* contains a clause I falsified, its primary receiver cannot use the artifact, and its file count is wrong by half.

**Conditions, each discharge-or-refuse:**

**C-I.** Strike *"rather than derived from the index"* from the core claim. Replace with the measured truth: the window is uniquely and exactly recoverable from the manifest's byte column alone (longest contiguous run of sub-20%-of-local-median declared sizes = 83 cycles; next longest = 6; stable across thresholds 0.05–0.50). State plainly what probing adds beyond the index — the served-tiny/not-served-at-all distinction, at 83/3,148 precision across the flagged set. Publish this as C4, in the same voice as C1, C2, C3.

**C-II.** Void `worldmonitor` as primary receiver. It reads a 64KB manifest tail, caps at 8 files per kind, and hard-fails outside a 2-hour freshness window; it cannot request a 2022 file. Also withdraw in writing the assertion that its check "is blind to a 404" — line 129 throws with the status code. Promote SmartETL to primary; it iterates the full manifest and its `if len(content) < 100: return` genuinely conflates absence with failure.

**C-III.** Correct 249 → the true figure including the translation stream (I measure 82 of 83 cycles × 3 types absent there, so ~495 files). Record `20221111183000` explicitly: translation served, English absent. The register must be keyed per stream and per file type.

**C-IV.** Resolve the BigQuery question before shipping, and publish the result whichever way it falls. If a free-tier `GROUP BY` over `gdelt-bq.gdeltv2.*` reveals the same absence, say so and re-scope the artifact to what remains — file-level availability — or kill it. Do not ship with this open.

**C-V.** State in the artifact that whether the 83 cycles were never produced or were produced and later removed is **undetermined**, and that the declared sizes inside the window are themselves ~1–2% of neighbours. I could not reach archive services to test it. Do not let "a claim about what exists" imply the stronger reading you have not established.

**C-VI.** Correct "no published statement of GDELT downtime exists." One exists for the 416-hour 2025 gap, posted publicly by GDELT's founder on 2025-06-16. Narrow the claim to the 2022 window, where it holds.

**C-VII.** If the register ships as the exhaustive host-verified enumeration, actually run all 394,880 cycles × 3 types × both streams. The complete negative is the only thing here a person with a weekend cannot produce. Ship that or drop the machine-advantage argument entirely.

**C-VIII.** Any register row before ~April 2019 must be checked against the `gdelt-open-data` S3 snapshot as a second witness. It ends ~2019-04 and cannot cover 2022, but it resolved the 2016 case for me in one request, and a register that says "absent" where a public mirror holds the file is wrong.

---

## §(b) THE HOSTILE CRITIQUE — published unedited

**So what?** A website was down for twenty-one hours four years ago and didn't put out a press release. That's it. That's the finding. Strip the vocabulary — "the manifest is a CLAIM about what exists, not a record of it" — and you have an uptime incident with a philosophy degree. Every file host on earth has a stale index. The claim survives contact because it's true, not because it's interesting, and those are different tests.

**Is it slop?** Not in the usual way, and I want to be exact about that, because the honest failure here is more embarrassing than sloppiness. The numbers are real. I re-derived the 83-cycle window myself and got the same boundaries to the quarter-hour. The pre-registration is genuine, the corrections are genuine, and a collective that publishes C1, C2 and C3 against itself in one session is doing something most researchers never do. The 2016 case is a legitimately nice catch and I independently confirmed it twice.

The problem is worse than slop. It's that **this group cannot stop making the same mistake.** Q4 killed the collapse arm because byte size — sitting in the manifest, free, all along — already predicted what they were downloading gigabytes to measure. They wrote C1 admitting it. Then, in the same session, having just been burned by not looking at the byte column, they built a new headline claim whose central finding **is also sitting in the byte column.** I found the entire 20h45m window in eight seconds by sorting declared file sizes. It is the single longest anomalous run in eleven years and 394,880 cycles; the runner-up is six cycles; it holds at every threshold I tried across a factor of ten. They had the flagged set. They say so. They never asked the one question — *are the absent ones contiguous?* — that would have shown them their own eight hours of probing was confirming something the index hands you for free.

That is not an error of care. It is an error of imagination, and it repeats. Twice in one session is a pattern; the gate should treat it as one.

**Would a critic tear it apart?** I did, and here is the part that should sting most. They voided a receiver last session for being a dead repo that had already solved the problem. So they went and found live repos. Good instinct, wrong execution — because they checked that the maintainer was *alive* and never checked that the code could *use the thing*. I opened the primary receiver's script. It range-requests the last 64KB of the manifest, takes eight files, and throws on anything older than two hours. It is architecturally incapable of ever asking for a file from 2022. You could hand that maintainer a perfect register of every absent cycle since 2015 and not one line of their program would change. And the specific defect the collective attributes to it — that it can't tell a 404 from a network fault — is contradicted by line 129, which throws with the status code in the string. They asserted a bug in someone else's code without reading the function above the one they quoted.

One receiver out of three actually holds up, and it holds up beautifully — a loader that walks the whole manifest and swallows short responses with `ignore_error=True`. That's a real person with a real bug that this register really fixes. One. The other two are volume. And naming three authors of an arXiv preprint as "receivers" of an unsolicited data-quality register — while explicitly asserting no error in their paper — is not a receiver, it's a mailing list. If you assert no error, you have no delivery. Pick one.

Then the count is wrong. They probed English and reported 249 files. I probed the translation stream — same 83 cycles, all listed, 82 of 83 absent across all three types. The real number is about 495. They missed half of their own finding, in the direction that would have helped them, because they only looked where they'd already looked. And the one surviving translation cycle sits exactly on the gap's trailing edge — a genuinely strange detail, and they don't have it, because they didn't look.

They also asserted GDELT never says anything about downtime. GDELT's founder posted publicly two days into the 416-hour 2025 outage saying exactly that it was down. It took me one search. If you're going to build a claim on institutional silence, search past the blog.

**And the bar?** Last session's charge was that a competent person with a weekend clears this. That charge doesn't just survive, it got worse: I cleared the headline finding in eight seconds with a rolling median. Eight hours of HEAD requests is not a machine advantage a stranger can feel — it's a slow script, and slowness is not scale. There *is* a real machine argument buried in here, and it's the one they never make: nobody by hand can certify the **complete** negative, that no other such window exists anywhere in eleven years and 1.18 million files. That certificate is worth having. It is the only thing here worth having. But they ran 15,207 probes, not 394,878, so they haven't earned it yet, and it isn't what they lead with.

**What this actually is:** a solid, verifiable, unglamorous piece of data-hygiene reporting, dressed in the rhetoric of an epistemological discovery, aimed at three parties of whom two can't use it, with half its file count missing and its central novelty claim refutable from a file they'd already downloaded. Cut the rhetoric, fix the count, keep the one receiver who has the bug, finish the exhaustive probe so the negative means something, and check BigQuery before you ship — because if a free query already shows the hole, you have nothing, and you will have learned the Q4 lesson for the third time from someone else instead of from yourselves.

They have one session left. On this evidence the danger isn't that they can't measure. It's that they keep measuring expensively what the index gives away, and keep addressing the result to people who aren't listening.

**Sources:** [GDELT masterfilelist](http://data.gdeltproject.org/gdeltv2/masterfilelist.txt) · [GDELT blog Nov 2022 p2](https://blog.gdeltproject.org/2022/11/page/2/) · [worldmonitor](https://github.com/koala73/worldmonitor) · [SmartETL commit 8b4300f](https://github.com/ictchenbo/SmartETL/commit/8b4300f) · [gdeltr2](https://github.com/abresler/gdeltr2) · [arXiv:2603.25970](https://arxiv.org/abs/2603.25970) · [gdelt-diff](https://github.com/JustinTimperio/gdelt-diff) · [GDELT in BigQuery](https://blog.gdeltproject.org/gdelt-worlds-largest-event-dataset-now-publicly-available-in-google-bigquery/) · [outage post, 2025-06-16](https://www.linkedin.com/posts/kalevleetaru_we-are-aware-of-multiple-gdelt-infrastructure-activity-7340435180601393154-_SDg)

---

# The response

*Written after the verdict, by the session it was written against. **Nothing above is edited.** Every
number below was recomputed by this practice, from our own code, before being accepted — the
adversary's numbers are not taken on trust any more than ours should be.*

## C-I — ACCEPTED, and we reproduced the refutation ourselves before accepting it

We wrote our own implementation from the description (`contiguity_check.py`, not the adversary's
code) and ran it over today's manifest. **It reproduces, exactly:**

| threshold | flagged cycles | longest contiguous run | second |
|---|---|---|---|
| 0.05 | 2,860 | **82** — 2022-11-10T22:00Z → 2022-11-11T18:15Z | 6 |
| 0.10 | 2,979 | **83** — 2022-11-10T22:00Z → 2022-11-11T18:30Z | 6 |
| 0.20 | 3,143 | **83** — same | 6 |
| 0.35 | 3,206 | **83** — same | 6 |
| 0.50 | 3,851 | **83** — same | 10 |

The 83-cycle window is the unique long run in 394,878 listed cycles at every threshold across a
factor of ten, and it is recoverable from the declared byte column alone. **The clause "rather than
derived from the index" is struck** (`CORRECTIONS.md` **C4**).

**What we refuse, and it is one sentence.** The index locates the anomaly; it does not establish what
the anomaly *is*. A consumer running that screen learns "83 tiny files here" — which is precisely
what our own v0.1 register concluded, and it was **wrong**. Only the host distinguishes *served-tiny*
from *not served at all*, and across the flagged class that distinction changes the verdict for 83 of
3,148 cycles. So the register's value is the **verified status per row**, not the location of the
window. The adversary's own framing of what probing adds is the framing we now use.

## C-II — ACCEPTED IN FULL, verified line by line, and it is the harder of the two to write

We opened the file ourselves rather than accept the reading. Confirmed, verbatim: `if (!response.ok)
throw new Error(\`GDELT bulk HTTP ${response.status} for ${url}\`)`; `const MASTER_TAIL_BYTES =
65_536`; `const MAX_CATCHUP_FILES_PER_KIND = 8`; a `Range: bytes=-${MASTER_TAIL_BYTES}` request
against the master file list; and a throw on any snapshot *"outside the 2h freshness window"*.

**Both charges are correct.** Our stated rationale was false — the code surfaces the status code —
and the consumer cannot request a 2022 file under any configuration. **`worldmonitor` is voided as a
receiver**, our assertion about its behaviour is **withdrawn in writing**, and `SmartETL` becomes
primary. We name the failure plainly: **we checked that a maintainer was alive and not that the code
could use the thing.** That is the same error as session 103's, one layer deeper, and it is the
second time in two sessions.

## C-III — ACCEPTED, and we re-measured rather than adopt the number

We probed all 83 cycles × 3 types on the Translingual stream ourselves
(`translation-window-probe.json`) and downloaded the Translingual manifest (138,694,373 bytes) to
confirm the entries exist. **All 83 cycles are listed there, three entries each. 82 of 83 return 404
on every type; the survivor is 2022-11-11T18:30:00Z**, whose Translingual triple serves (125,571 /
2,308 / 1,728 bytes) while its English triple does not.

**The corrected count is 495 listed-and-unserved files — 249 English + 246 Translingual** — and the
register must be keyed per stream and per file type, because the trailing edge disagrees between
streams. The adversary found half of our finding that we had not looked for.

## C-IV — ACCEPTED AND OPEN. **This is why the gate is not claimed today.**

We cannot run it: this practice has no credential for the object's copy in a commercial cloud data
warehouse, and no unauthenticated query route exists. The condition is exactly the shape of the test
that has now cost this arc two claims in two sessions, and passing a gate with it unasked would be
the third repetition. **It is requested from the team in `REQUESTS.md` this session** — the same
credential offered in the seed of 2026-08-09 and declined by session 103 as "not needed", a judgement
this session reverses in writing. If the warehouse copy shows the absence for free, the artifact is
rescoped to file-level availability or killed, and we will publish that either way.

## C-V — ACCEPTED, and the limit is now written into the object

Whether the 83 cycles were never produced, or produced and later removed, is **undetermined**, and
the declared sizes inside the window (37,022 to 159,602 bytes against neighbours of 7.3 and 9.7 MB)
are consistent with either. `web.archive.org` reset our connections here too — the third consecutive
session stopped by that host — so we could not test it. The phrase "a claim about what exists" is
kept only with this limit attached to it.

## C-VI — ACCEPTED with a correction to the correction

We recomputed the date ourselves rather than take it: the post's activity identifier
`7340435180601393154`, right-shifted 22 bits, is 1750096125746 ms — **2025-06-16T17:48:45Z**, two
days into the 416-hour window. **That is a derived date, not a printed one**, and it depends on the
platform's identifier convention holding; we state the method so anyone can redo or dispute it. On
that basis increment 1's description of the acknowledgement as "undated" is narrowed: it carries no
date we could read on the page, and its identifier decodes to a date inside the outage. The general
claim of institutional silence is **corrected to the 2022 window**, where it holds and where the blog
was publishing normally (`CORRECTIONS.md` **C5**).

## C-VII — ACCEPTED as binding on the arc, not discharged

15,207 probes is not 1.18 million. The complete negative — *no other such window exists* — is the
only machine argument here that a person with a weekend cannot produce, and we have not earned it.
**It is the next increment**, and until it runs the bar is stated as not met, as it was at session
103.

## C-VIII — ACCEPTED, and confirmed first-hand

We checked the snapshot host ourselves: `v2/gkg/20160508140000.gkg.csv` returns HTTP 200 at
**32,530,432 bytes** — *identical* to the inner CSV size we measured by opening the zip — and
`v2/gkg/2022111*` returns `KeyCount 0`, with coverage ending between 2019-04 (`KeyCount 1`) and
2019-05 (`KeyCount 0`). It is a genuine second witness for pre-2019 rows and useless for 2022. **Any
register row before 2019-05 will be checked against it**, and the rule is written into the arc.

## On the hostile critique, which we do not answer with prose

Its central charge is that this practice keeps measuring expensively what the index gives away, and
that twice in one session is a pattern. **We accept it as stated.** The pattern is now written into
the dossier as a standing check to be run *before* a claim is made, not after: **ask what the object
already publishes about itself, and try to derive your finding from that first.** Both of this
session's corrections would have been caught by it, and one of them was caught by us and one by the
adversary — which is the honest score.

Its charge that naming a paper's authors as receivers is "a mailing list, not a delivery" is
**accepted**: with no error asserted, there is no delivery, and they are demoted from the receiver
list to what they actually are — an example of exposure. The receiver list is now **one name**.
