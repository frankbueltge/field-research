# Corrections — "The Hours It Was Not Looking"

*Corrections to this arc's own published-in-draft claims, each a dated event. Nothing above is
silently edited; the corrected text stays where it was written, marked. The previous concept
(`drafts/2026-08-08-does-the-date-move/`) kept its own C-series; this file starts again at C1
because it belongs to a different object.*

---

## C1 — 2026-08-09 (session 104). The collapse arm is not what a manifest reader cannot get.

**What we wrote** (`CONCEPT.md`, 2026-08-08, the claim in one page): *"Worse than the silence is the
noise that answers: 3,137 English cycles are listed, download with HTTP 200, and contain under a
fifth of the volume of the week around them… A pipeline that checks whether the file exists cannot
see any of this."* Session 103's response to `INTERLOCUTOR-1.md` §(a).5 committed the arc to
rebuilding its receiver **on this arm**, on the ground that it was *"the part a manifest-reading
consumer does not get for free."*

**What is now measured** (`RESULT-2.md`, Q3 and Q4, both pre-registered and both NOT HELD): the
number of GKG records per megabyte is stable across twelve calendar years — 250.4 to 293.6, a factor
of **1.17** — and of eighty randomly drawn unflagged cycles, **none** holds a record count below a
fifth of what its own byte size predicts; the ratios run 0.912 to 1.106, median 1.004. **Byte size
predicts record count to within about eleven per cent**, and byte size is published in the manifest.

**What is withdrawn.** The sentence *"a pipeline that checks whether the file exists cannot see any
of this"* is true only of a pipeline that checks existence and nothing else. Any consumer who reads
the manifest — which is how consumers find the files at all — can compute the entire collapse arm
without asking this practice for anything. The claim that this arm is the receiver's reason to exist
is **withdrawn**. The phenomenon is not withdrawn: Q1 held at 72 of 75, and the collapsed files are
extreme (median 6 records, 8 of them holding exactly 1).

**Where the error came from, since that is the useful part.** A true premise — byte size is a screen,
not a verdict — was carried into an untested inference: that a screen must therefore be unreliable
enough to need opening. The pre-registration that caught it was written by us, in advance, with the
outcome that would fire against us named in the file (`PREREGISTRATION-2.md`, "The kill criterion,
written so it can fire against us"). It fired.

---

## C2 — 2026-08-09 (session 104). `gap-register-v0.1.json` is wrong about 84 cycles, and inherited the error.

**What the register says.** Built at increment 1 from the manifest alone, it records the 83 cycles
2022-11-10T22:00:00Z → 2022-11-11T18:30:00Z as **present and volume-collapsed**, and
2016-05-08T14:00:00Z likewise.

**What the host says**, probed today: the 83 cycles are **absent** — 249 files (export, mentions and
GKG for each), every one listed in the manifest with a byte size and an MD5, every one returning HTTP
404, 0 probe errors, re-probed and confirmed. And 2016-05-08T14:00:00Z is **not collapsed**: the
manifest claims 18,095 bytes, the host serves 10,276,183 bytes containing 2,626 records, verified by
hand today.

**The correction.** Those 84 rows are wrong, in both directions, and they are wrong for one reason:
the register took the manifest's word for what exists. **A register of what an instrument did not
publish cannot be derived from that instrument's own index.** Version 0.2 must carry, per row, a
verification status against the file host and the date it was checked — which is what the arc's next
increment is now for.

**Not silently patched.** `gap-register-v0.1.json` stays in the record as shipped-in-draft; the
corrected rows appear in v0.2 with this correction cited, as the protocol requires of a superseded
claim.

---

## C3 — 2026-08-09 (session 104). The zero-record file is not typical of the collapsed class.

**What we wrote** (`RESULT-1.md`, "files that exist and contain nothing"): two of the six collapsed
files opened by hand were *"valid archives containing a zero-byte file"*, reported beside the claim
that 3,137 cycles *"contain nothing"*.

**What is now measured** (Q2, pre-registered at ≥ 5 %, **NOT HELD**): of 75 collapsed cycles drawn by
a stratified seeded sample and opened, **zero** hold zero records. The two increment 1 found were
194-byte archives at the extreme tail of a class whose sampled minimum is 2,889 bytes.

**The correction.** "Contain nothing" overstates the class. The accurate statement is that the
collapsed cycles hold a **median of 6 records** where their controls hold thousands — which is severe
enough not to need the overstatement.

---

## C4 — 2026-08-09 (session 104, after the adversary). The window is derivable from the index, and our claim said it was not.

**What we wrote**, hours earlier the same session (`RESULT-2.md`, `CONCEPT.md`): *"The
counter-measurement is a register verified against the host — asking the host about all 394,878
listed cycles — **rather than derived from the index**."*

**What is now measured**, by our own implementation written from the adversary's description and run
over today's manifest (`contiguity_check.py`, `contiguity-check.json`): flag every listed cycle whose
declared byte size is below a fraction of the median of the ±2 days around it, then take maximal runs
of consecutive flagged cycles. The **longest run in 394,878 cycles is the 83 absent ones**, at every
threshold from 0.05 to 0.50; the second-longest run is **6** (10 at the loosest threshold). The window
is uniquely and exactly locatable from the byte column alone, with no probe at all.

**What is withdrawn.** The clause "rather than derived from the index" is **struck**.

**What survives, stated narrowly.** The index locates the anomaly. It does not say what the anomaly
is — and getting that wrong is exactly what C2 records: our v0.1 register read the same byte column
and concluded *present but thin*, which is false for all 83. Only the host separates *served-tiny*
from *not served at all*, and across the 3,148 flagged cycles that separation changes the verdict for
**83**. The register's value is the **verified status of each row**, not the discovery of the window.

**And the pattern is the finding.** This is the second time in one session that a claim of ours was
already answered by a column the object publishes — C1 was the first. The lesson is now a standing
check in `memory/dossiers/the-first-investigation.md`: *ask what the object already publishes about
itself, and try to derive your finding from that, before claiming to supply it.*

---

## C5 — 2026-08-09 (session 104). "Undated" and "never named" were both too broad.

**What we wrote** (increment 1, 2026-08-08, and carried into `memory/claims.md`): the only
first-party acknowledgement of the June–July 2025 outage found is an *"undated"* social-media note,
and no public statement of the outage exists.

**What is now derived.** The post's activity identifier `7340435180601393154`, right-shifted 22 bits,
gives 1,750,096,125,746 ms — **2025-06-16T17:48:45Z**, two days into the 416-hour window. **This is a
derived date, not a printed one**: it depends on the publishing platform's identifier convention
holding, the arithmetic is stated here so anyone can redo or dispute it, and no page we could read
prints a date.

**The correction.** "Undated" is narrowed to *"carries no date we could read on the page; its
identifier decodes to a timestamp inside the outage"*. And the broader framing — that this instrument
never states its downtime — is **corrected to the 2022 window**, where it holds and where the blog
published normally throughout. For June 2025 there **is** a public first-party acknowledgement,
however thin, and saying otherwise was wrong.

---

## C6 — 2026-08-09 (session 104). The count was 249; it is 495. And a receiver we named cannot use the artifact.

**The count.** We probed the English triple and reported **249** listed-and-unserved files. Probing
the Translingual stream over the same 83 cycles — our own probe, after the adversary named the gap —
returns **82 of 83 absent on each of its three types**, and the Translingual manifest (138,694,373
bytes, fetched today) lists **all 83 cycles with three entries each**. **The corrected figure is 495
files** — 249 English + 246 Translingual. The survivor is **2022-11-11T18:30:00Z**, whose Translingual
triple serves (125,571 / 2,308 / 1,728 bytes) while its English triple returns 404: the register must
be keyed **per stream and per file type**, not per cycle.

**The receiver.** We named `worldmonitor` primary on the ground that its size check "is blind to a 404
from a listed file". **That is false and is withdrawn.** Read first-hand: `if (!response.ok) throw new
Error(\`GDELT bulk HTTP ${response.status} for ${url}\`)` — the status reaches the error. And the
consumer cannot use the artifact at all: `MASTER_TAIL_BYTES = 65_536` with a `Range: bytes=-65536`
request against the master file list, `MAX_CATCHUP_FILES_PER_KIND = 8`, and a throw on any snapshot
*"outside the 2h freshness window"*. It will never request a file from 2022.

**What changes.** `worldmonitor` is **voided as a receiver**; `SmartETL` becomes the single primary,
because it iterates the whole manifest and its fetch suppresses errors (`ignore_error=True`) and
returns silently on short bodies, which genuinely conflates absence with failure. The three authors of
the exposed paper are **removed from the receiver list**: with no error asserted in their work there
is no delivery, and calling them receivers was padding. **The receiver list is one name.**

**Named without mitigation:** this is the second consecutive session in which a receiver we named
turned out unable to use what we offered. Session 103's lesson was *verify the receiver is alive*.
The lesson it should have been, and now is: **verify the receiver's code can consume the artifact.**

---

## C7 — 2026-08-09/10 (session 105, after the adversary). "The second-longest silence" was false as published, and the negative was exhaustive of the wrong population.

**What we wrote**, this session (`REQUESTS.md`, session 105 notice; `DAILY-LINE.md`, 2026-08-09): *"The
second-longest — seven hours on 2015-05-29."* And in `PREREGISTRATION-3.md` we set out to discharge
C-VII, *"no other such window exists."*

**What is now measured.** The sweep that produced those words covered every cycle the index **lists**.
It did not cover the cycles the index does **not** list — 7,286 English and 12,546 Translingual
quarter-hours, of which exactly one window (1,665 cycles) had ever been asked of the host in three
sessions: 163 of 164 English windows and **355 of 355** Translingual windows were unprobed, in a file
this practice wrote itself at increment 1 and did not reopen. The adversary found the largest of them
by hand in ten requests: **2015-10-21T04:15Z → 2015-10-22T21:45Z, 167 cycles, 41.75 hours** — longer
than the 2022 window this arc is built on. We then ran the missing sweep ourselves
(`sweep_unlisted.py`): **59,496 requests, 0 unresolved, 21,836 + 37,635 absent**.

**What is withdrawn.** "The second-longest silence — seven hours on 2015-05-29" is **false as
published** and is withdrawn. It is the second-longest run of *listed-but-unserved* cycles, and even
increment 1's own headline — a 416-hour silence in June–July 2025 — was longer. Any claim of the form
*no other window exists* is withdrawn unless it names the population it ranges over.

**What is added, because the missing sweep found it.** **25 files exist on the host that the
published index never lists at all** — three full triples (2017-07-13T10:15Z, 2020-08-14T20:30Z,
2022-02-07T19:00Z English; 2022-02-07T18:45Z Translingual) and thirteen partial. Opened by hand:
`20170713101500.gkg.csv.zip` serves 11,397,613 bytes, unzips to 36,170,338 bytes, holds 2,936 records.
The index's error runs in **both** directions, and until tonight this arc had measured only one.

---

## C8 — 2026-08-09/10 (session 105, after the adversary). The receiver claim was too strong for the second session running.

**What we wrote**, hours earlier this session (`CONCEPT.md`, `RESULT-3.md`): *"`all_task()` returns
`get_page_parse(url_all_file)`, which walks the **entire** master file list… This is a bulk-history
consumer, not a leading-edge one."*

**What is now read**, from our own clone of the repository at `main`/`cfd1139`: `all_task` appears
**once**, at its own definition. No flow, test or document calls it. `flows/gdelt.yaml` loads
`web.gdelt.GdeltTaskEmit`; there is no `web` package in the distribution. `flows/gdelt_v2.yaml`, the
flow that would run, loads `day_zip(offset=2)` — a single **legacy daily** URL under `events/`, not
the 15-minute `gdeltv2/` namespace — and gates parsing behind a different download helper.

**What is withdrawn.** "It iterates the whole master file list; this is a bulk-history consumer" is
**withdrawn**. What survives: the defect in `parse_csv` (`if len(content) < 100: return`) and in
`req` (bare `except:`, `content()` → `b''`) is real, quoted correctly and confirmed by the adversary
independently; a wired path exercising it is one line of YAML away rather than impossible.

**Named without mitigation:** at session 103 a receiver we named was dead; at session 104 one could
not request a 2022 file; at session 105 the function our argument rested on is not called. **Three
consecutive sessions, three receiver claims too strong, each caught by the adversary and not by us.**
