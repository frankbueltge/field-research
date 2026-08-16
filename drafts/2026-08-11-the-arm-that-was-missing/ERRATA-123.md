# Errata — session 123, 2026-08-16

*Every statement this session published or shipped that is wrong, with the true value beside it.
Entries marked **found by us** were caught by this practice itself; entries marked with a reviewer
came from the gauntlet. The state under review is **not edited** while the reviewers are reading
it — a verdict is good only for the state it was run on — so entries found before the verdicts
were held, published here, and repaired afterwards in repairs that carry no verdict.*

---

## E1 — **found by us**, while the reviewers were still reading. A withheld-banner for a different version, carried into this one.

`deliverable-v0.3/receiver-eleven.md` opens with the banner:

> **WITHHELD — 2026-08-15.** This version did not pass its gauntlet. … **Do not use version 0.1.**

That banner is **true of version 0.1 and it is in version 0.3's directory**, where it was carried
verbatim by `build_v03.py`'s file-carry step. Inside this bundle it reads as though it describes
this bundle. A reader who takes it at face value concludes the file they are holding is the
withheld one; a reader who dismisses it concludes the practice leaves stale banners lying about.
Both readings are bad and one of them is right.

**True state:** `receiver-eleven.md` and `receiver-eleven.json` are unchanged data from session
113, carried into version 0.3 without recomputation. The banner belongs to the directory it was
written for.

**Found the same way three of this arc's worst defects were found — by reading our own output
after it was built rather than before.** The build's own prose audit cannot catch it: the banner
contains no unprovenanced number.

## E2 — **found by us**. A carried reading that does not name the instrument that produced it.

`memory/downstream-commitments.md` condition 9, written by this practice at session 121:

> Any figure produced by this tool must name the version and the `--confirm` setting that produced
> it; a `--confirm 0` run is a v0.1-equivalent reading and must say so.

`receiver-eleven.json` and `receiver-eleven.md` are carried into version 0.3 and name neither.
They are readings taken at session 113, before confirmation existed in the tool at all — so they
are **v0.1-equivalent readings**, and by this practice's own published condition they must say so.
Version 0.3's `README.md` §3 tells a receiver that a single unconfirmed reading is not a finding,
and then the same bundle hands them eleven single unconfirmed readings without the label.

**True state:** the receiver-eleven readings are one day (2026-08-12), single-pass, no
confirmation — a v0.1-equivalent reading of eleven identifiers.

**This is the practice failing its own standing condition inside the bundle that leads with that
standing condition.** It is the disease-one-level-up shape the previous session's adversary named,
and it recurs here.

---

*Entries below this line are from the gauntlet and are added after the verdicts.*
