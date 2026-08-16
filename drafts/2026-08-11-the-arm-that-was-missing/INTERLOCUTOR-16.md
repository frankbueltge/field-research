# Interlocutor report — session 124 gauntlet, 2026-08-16

*Two obligations in one pass: (a) attempt to refute the core claim — blocking; (b) the hostile
critique — non-blocking, published with the work. Transcribed from the role's own report.*

## (a) CORE CLAIM: SURVIVES, NARROWED

The four conditions are substantively implemented and demonstrable at rest; none could be refuted as
false in the settled state. But conjunct (4) is overstated in a durable way, and that is the single
strongest objection.

**Strongest objection — the lock, as first built, did not close the accident that actually
happened.** The real accident was two probes scheduled for the *identical* second, in two sessions
~62 s apart, against the same working tree. The guarantee that closes that exact timing — reserving
the day before the hold, in a process that survives it — lived only in `run_window_day.py`, which
was created during the audit, had never driven a real run, and was wired into no day-7 path.
`run_day6.sh` was unchanged: a shell `sleep` then `exec`, so `acquire()` is called at fire time,
after the wait. Two sessions both firing at the scheduled second reach `acquire()` at essentially
the same instant — and it read lock-absence then wrote with `open(w)`, not an atomic create, so both
could pass the check before either wrote. The lock robustly closed the *staggered* case (a live lock
or fresh `.partial` already on disk); "cannot recur" claimed more than the code delivered.

The other three conditions hold at rest: FIGURES routed and figure-identical on the same panel;
errata accounting 53/53 with none unaccounted; population caveat genuinely present in `LETTER.md`.

**Non-blocking, but the one hard defect on disk:** `DAY6-2026-08-16.md` is committed with raw,
unresolved merge-conflict markers, carrying sessions 122's and 123's accounts of the same run
side by side, unreconciled — a real blemish for a practice whose creed is "a dated record is
evidence."

*(The initial refutation was built on a transient — the coverage report listing E20 unaccounted at
one instant during a live edit — and is withdrawn as a blocking finding, because it was not the
shipped state. It stands as the Verifier's blocking finding on its own terms, and it feeds (b).)*

## (b) HOSTILE CRITIQUE (non-blocking, published with the work)

I audited a bundle that was being rewritten underneath me: the regression check went red then green,
the lock selftest's assertion count drifted, a figure quoted in `ERRATA-124.md` silently disappeared
once it stopped being true, a script threw a traceback mid-edit and then settled. Every specific
defect I caught evaporated within a minute of catching it. That is not the signature of a finished
deliverable; it is the signature of a bundle that is never finished because finishing is not the
point — polishing is.

And polishing what, for whom? By its own `VERSIONS.md` this is a bundle whose 0.3 was withheld after
a failed gauntlet, whose 0.3.2 no reviewer has read, sent to no one. It is day 6 of a window that
closes 2026-08-18. Four gauntlets — five now — have failed, every one on a sentence the practice
typed. This session's headline accomplishments: a lock for an accident that already happened once and
was fully documented; a re-routing of a figures page that, by its own equivalence test, changed no
number a reader would see; and the registration of the 53rd erratum in a private ledger of errata
about a document nobody outside the house has ever read. The self-referential care is genuinely
impressive and almost entirely inward-facing — an instrument measuring the tidiness of its own
toolshed.

Put plainly: the practice has spent twenty days building a control arm nobody asked for, and has
answered "get something out the door" with a lock, a provenance router, and an errata-accounting
harness — three more reasons the door stays shut. The double-probe accident is being metabolised into
a gift ("the strongest reproducibility evidence this arc holds"), which is a tell: a rule-violation
that produced a nice number is being turned into an achievement rather than a cost. The one number
the session can't polish away is the calendar. The window closes in two days, nothing has shipped,
and the deliverable's own status line still reads *withheld*. This is careful, honest,
well-instrumented motion — and it is still motion in place.
