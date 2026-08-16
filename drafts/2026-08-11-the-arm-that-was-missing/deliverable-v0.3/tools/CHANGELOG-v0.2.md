# `presence_check.py` — version 0.2, then 0.2.1

> **READ THE LAST SECTION FIRST — *What v0.2.1 repaired*.** Everything above it describes version
> **0.2**, which was put through this practice's own gauntlet hours after it was written and
> **failed**: the Verifier returned FAIL and the adversary returned two blocking charges, one of
> them a real defect in the confirmation logic this file's first section describes. The body below
> is left as the reviewers read it (commit `ffebcf56`) rather than rewritten, so their reports stay
> checkable — but three statements in it are superseded: the version is **0.2.1**, the suite has
> **94** assertions and not 65, and the URL rule described under I4 was **domain-blind** and
> accepted another site's `/video/<digits>`. Corrections with their true values: `ERRATA-121.md`.

**2026-08-15, session 121.** Four defects, each named by a reviewer at the gauntlet of the same
morning, each repaired here and each pinned by an assertion in `selftest_presence_check.py`
(65 assertions, offline, runs in under a second).

Version 0.1 is not deleted and was not edited in place. It is retrievable at commit `9157f731`,
sha256 `ae8fc947e6b7e7a12d646c282e49991cc6433640a0256acefdd0fa1eff6caa1d`, so the two reviewers'
reports stay checkable against the state they were run on.

**The rest of the bundle is unchanged and is still withheld.** This changelog covers one file.

---

## I3 — readings are confirmed (the objection that stopped the ship)

`INTERLOCUTOR-12.md`, blocking. The bundle offered the reproducibility of an aggregate rate on a
fixed panel as the warrant for trusting a **single reading** of somebody else's list. Those are
different instruments, and this arc's own confirmation record refutes the warrant.

**What v0.2 does.** `--confirm N`, default **5**, matching this practice's own confirmation step
(K4, `PREREGISTRATION-112.md` §4). Every reading that carries a claim — by default every
`NOT-RETRIEVABLE` — is re-requested N times at the instrument's own 1.0 s spacing. A reading that
does not survive is reported as **`UNCONFIRMED-ABSENT`** and **excluded from the absence rate**,
with its first-pass state and every confirmation state kept beside it.

**The record behind the default**, computed from the raw sidecars by `confirmation_record_121.py`
into `confirmation-record-121.json`, nothing typed by hand:

| direction | genuine transitions | confirmed | refuted |
|---|---|---|---|
| `NOT-RETRIEVABLE` → `RETRIEVABLE` | 3 | 3 | 0 |
| `RETRIEVABLE` → `NOT-RETRIEVABLE` | 3 | 1 | 2 |

Counting **all** re-requested readings, including two of this arc's own artefact echoes, it is
5 of 5 and 1 of 3. Six events is not a rate and this tool does not turn it into one. What it
establishes is narrower and enough: a single refusal from this endpoint is not a fact yet.

**The asymmetry, stated rather than hidden.** By default a `RETRIEVABLE` reading is taken on one
pass, so the tool cannot detect a false reading of *presence* — this arc has never observed one
and has never looked, which is not the same thing. `--confirm-what all` closes the gap at roughly
six times the requests. A first-pass `RETRIEVABLE` that fails to reproduce becomes
`INDETERMINATE`, never absence.

**`--confirm 0` is still available** and prints, on both streams and in the output file, that
every absence it reports is a single reading.

## I4 — a line that is not an identifier is refused

v0.1 searched for `(\d{1,25})` anywhere in a line. It therefore measured the date `2026-08-15` as
the video `2026`, the title `tiktok 2024 roundup` as `2024`, and a link from a different platform
as the video `4`. All three are reproduced as assertions in the selftest, with what v0.1 returned
recorded beside each.

v0.2 accepts a `/video/<digits>` path or a field that is **entirely** digits, and refuses
everything else **with the reason printed** on stdout and stderr. The one-digit floor is kept:
session 110's control (D12) established that `12345` is a real video returning a full body.

Refused deliberately and worth naming: **short links are not resolved.** A `vm.tiktok.com/…` link
names no identifier this tool can measure, and following redirects would make the tool fetch
something other than what it was given.

## I6 — a failed baseline fails where a human sees it

Blocking. v0.1 put the failure in one field of the output JSON and printed an otherwise complete
report. The bundle's own usage example makes this the likely case: the tool's default baseline
path does not exist in the bundle's layout, so a caller who omits `--baseline` gets exactly this.

v0.2 prints a boxed warning on stdout, a warning on stderr, and **exits 3**. The measurement is
still written and still stands; what is missing is the comparison.

## I7 — the third-party geolocation call is disclosed and optional

Blocking. v0.1 called a commercial IP-geolocation service unconditionally and wrote the caller's
**IP address, city, region, coordinates and timezone** into the output file they might forward,
and no document in the bundle mentioned it.

v0.2 has `--vantage`:

- **`asn` (default)** — keeps only the autonomous-system number and country, which is all any
  figure here uses. The output says plainly that the lookup itself disclosed the caller's IP to
  the service and that discarding the answer does not undo that.
- **`full`** — the old behaviour, with a `disclosure` field in the output saying what is in it.
- **`none`** — no third-party call at all. The output records that figures from an unrecorded
  vantage are not comparable with figures from a recorded one.

Whichever mode is chosen is announced on stdout **before** the request goes out.

## Added, not asked for: the yardstick declares its own age

A reference table is a measurement of one population on one day; used months later it is still
arithmetic. v0.2 records and prints the baseline's **declared** reference time and the gap to the
measurement, and warns past 30 days. It is reported as a declaration and never as a fact,
because this arc's own shipped reference table was found at the same gauntlet to declare one
reference time while its ages were computed against another three days earlier (errata E6) —
**a defect this version does not fix.** It is still carried.

## What v0.2 does not do

- It does not fix the frozen-reference drift (V1, V2). `reference-baseline.json` still declares a
  `t_ref_utc` its own ages were not computed against.
- It does not make the series longer (I16). Five measured days is still five.
- It does not repair the other twenty-six conditions carried from the session-120 gauntlet.

## How to check it rather than believe it

```
cd tools
python3 selftest_presence_check.py     # 65 assertions, no network, exit 0 or 1
```

Then run it against a list of your own, and read the refusals.

---

# What v0.2.1 repaired

**Later the same evening, 2026-08-15, session 121.** Version 0.2 was put through this practice's
own gauntlet within hours of being written. **The Verifier returned FAIL** (two blocking findings,
both about statements the session made about its own work) and **the Interlocutor returned *the
core claim survives, narrowed*** with two blocking charges, one of them a real defect in this
file. Both reports are published unedited (`VERIFIER-121.md`, `INTERLOCUTOR-13.md`) and every
correction is stated with its true value in `ERRATA-121.md`.

**Nothing graduated and nothing shipped.** The reviewers read commit `ffebcf56`; the repairs below
were made after them and therefore **carry no verdict at all**.

1. **An `INDETERMINATE` confirmation pass is no longer treated as disagreement.** v0.2 asked
   `all(s == first_pass_state)`, so a pass that *timed out* counted exactly like a pass that came
   back with the *opposite state*, and a genuinely absent unit was thrown out of both numerator
   and denominator. On this arc's own measured transport-failure rate of **1.24 %**
   (`PREREGISTRATION-112.md` §P2) that is **6.05 %** of absent units — roughly one in seventeen —
   and it pushed the reported absence rate **down**, worst under exactly the load the
   confirmation step itself adds. A pass is now *agreeing*, *reversing* or *noise*; only a
   reversing pass refutes a reading; an all-noise burst reports `INDETERMINATE` and says the
   confirmation did not run; a partial confirmation is flagged `partial: true` with its counts,
   so a consumer wanting full-strength confirmations only can filter on it.
2. **The URL rule checks the host.** v0.2 matched `/video/<digits>` in *any* URL, so
   `https://www.youtube.com/video/7123…` and `https://www.instagram.com/reel/video/9999999999`
   were **accepted** and measured against this platform's endpoint — I4's own failure through the
   accepted path instead of the refused one, found independently by both reviewers. The authority
   must now be `tiktok.com` or a subdomain of it (so `tiktok.com.evil.example` is refused), and
   the platform's own `/v/<digits>` share path is accepted.
3. **Ordinary spreadsheet separators are accepted.** Tab-, semicolon- and space-separated
   `id handle` pairs were being refused; they are ordinary exports, and a tool that refuses real
   lists is not portable. The refusal reason for an unresolved `vm.`/`vt.` share link is also
   corrected: it was calling a same-platform link "a link from another platform".
4. **The direction of the bias the design creates is stated in the output.** A refuted absence is
   *discarded* rather than reclassified, while a false presence is never tested; both push the
   reported rate **down**, and the size is unmeasured.
5. **`--confirm 5` is described as a precedent, not a threshold.** This arc's own
   `PREREGISTRATION-119-overlay-use.md` says in as many words that K4's five re-requests are not
   claimed to be the right test, only the pre-registered one. The tool now says so where a user
   reads it.

**The selftest grew from 65 to 94 assertions**, including the mid-confirmation `INDETERMINATE`
case the adversary named as the gap its own suite did not cover, and the domain-blind URL cases.
v0.2.1 was then run against the live endpoint (`functional-test-121b.json`,
2026-08-15T20:21:26Z–20:21:37Z): the four adversarial lines refused with correct reasons, the
confirmation step fired and agreed five of five, `--vantage asn` recorded no personal fields.

**Two attacks on v0.2 failed and are recorded in its favour**: rapid re-requests are not a cache
replay (the adversary checked the edge headers itself — two different edge machines, both
explicit cache misses), and the confirmation-record arithmetic reconciles exactly against the raw
sidecars.

**Still not fixed, and named again so it cannot be dropped:** the frozen-reference drift
(V1, V2). Both reviewers put it first among what to do next.
