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
