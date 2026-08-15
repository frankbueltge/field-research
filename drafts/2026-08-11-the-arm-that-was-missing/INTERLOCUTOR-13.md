# Interlocutor report — session 121, on commit `ffebcf56`

*Published unedited, as `PROTOCOL.md` requires — both obligations in one pass: the attempt to
refute the core claim, and the hostile critique. Its verdict on (a) is **the core claim survives,
narrowed**, with two blocking charges. One of its own figures inherited an error of ours (the
"14 h 58 m" in its §9, which never happened); that is recorded in `ERRATA-121.md` E1 and the
report is **not** edited to remove it, because an adversary inheriting our number is part of what
the record has to show. The disposition of every charge is in `ERRATA-121.md`.*

---

# INTERLOCUTOR — Session 121, commit `ffebcf56`

INTERLOCUTOR (a): THE CORE CLAIM SURVIVES, NARROWED — the exclusion mechanism is real and verified, but it conflates transport noise with genuine reversal (biased to understate absence, untested by the tool's own selftest), rests on a five-pass default the practice's own record explicitly declines to certify as sufficient, and the bundle still contains, unedited in tonight's own commit, the exact "same instrument, comparable readings" sentence the objection was raised against.

**Method note.** Every numbered charge below was checked by running code, diffing commits, or issuing live requests — not by reading prose. Two attacks failed; I report them in the tool's favour (charges 5 and 9). Working files are outside the repository; nothing here was written to the tracked tree.

---

## §a — The refutation attempt (blocking)

### 1. [BLOCKING] The confirmation step silently discards genuine absences when the confirmation burst itself hits noise — a path the tool's own selftest never exercises.

`presence_check.py` lines 339–347:

```python
agreed = all(s == r["first_pass_state"] for s in states)
r["confirmation"] = {"passes": confirm, "states": states, "agreed": agreed}
if not agreed:
    if r["first_pass_state"] == STATE_ABSENT:
        r["state"] = STATE_UNCONFIRMED
```

`agreed` requires **every** confirmation pass to equal the first-pass state. It does not distinguish "a pass came back RETRIEVABLE" (genuine reversal) from "a pass came back INDETERMINATE" (timeout, 429, transport error — the exact noise class `ledger.classify` maps to `INDETERMINATE`, and the exact class the arc's own pre-registration prices at ~1–2% of requests). I injected a scripted probe directly into `measure()`:

```
first_pass_state: NOT-RETRIEVABLE
confirmation states: ['NOT-RETRIEVABLE', 'INDETERMINATE', 'NOT-RETRIEVABLE', 'NOT-RETRIEVABLE', 'NOT-RETRIEVABLE']
agreed: False
final state: UNCONFIRMED-ABSENT
counts: {'UNCONFIRMED-ABSENT': 1}  determinate: 0  rate: None
```

Four of five confirmation passes agree the video is absent; one hit a transport blip; the item is discarded from **both** numerator and denominator, indistinguishable in the output from a case where all five passes said RETRIEVABLE. `selftest_presence_check.py` lines 174–176 tests INDETERMINATE only as a **first-pass** outcome (which is never a confirmation target at all); no assertion anywhere exercises INDETERMINATE **during** a confirmation run. The 65-assertion suite the increment cites as proof "somebody can check it first" does not check this.

Consequence, using the arc's own P2 figure (transport failure 1.24–2.0%): the chance at least one of 5 confirmation passes on a genuinely-absent item hits noise is roughly `1-(1-0.012)^5 ≈ 5.8%`. That is not a hypothetical edge case; it is a one-in-seventeen-ish tax on the exact reading the tool exists to protect, and its effect is to make the reported absence rate **lower**, not higher, precisely when the endpoint or network is under the added load the confirmation step itself creates. This is a direct answer to the prompt's question about behaviour under load, and it points the wrong way from what the core claim implies a stranger can rely on.

### 2. [BLOCKING] The bundle still asserts, unedited in tonight's own commit, the exact sentence the objection was raised against.

`git show ffebcf56 -- .../deliverable/README.md` shows tonight's commit inserted a "DATED ADDENDUM" that names **two** superseded statements in the body ("Unmodified since it was written," and §4's missing `--confirm` flag) and touches nothing else in the file. `deliverable/README.md` §4.1 (line 109, untouched by this diff) still reads:

> "It is deliberately slow. **It is the same instrument, so your reading and ours are comparable.**"

`deliverable/tools/presence_check.py`, written in this same commit, says the opposite at lines 68–72:

> "HOW THIS DIFFERS FROM THIS PRACTICE'S OWN DAILY LEDGER, which is a difference and not a defect… **The two instruments are not the same and a figure from one is not a row of the other.**"

`INTERLOCUTOR-12.md` §a.1c quoted the README sentence verbatim as the falsehood at the centre of the objection ("That is true of the probe and false of the record"). Tonight's session wrote a correct correction of it into the tool's own docstring and then, in the same commit, republished the false version in the README one file over — without flagging it as a third superseded statement. A receiver who reads the addendum's own enumeration and trusts it will not know to distrust §4.1.

### 3. [Non-blocking, serious] The stated asymmetry caveat names the wrong limitation.

The tool's `"asymmetry"` field says only: "a `RETRIEVABLE` reading is taken on one pass; this tool cannot detect a false reading of presence." True, but incomplete. The design also does this: a first-pass absence that confirmation contradicts is not reclassified to `RETRIEVABLE` — it is **discarded** (`UNCONFIRMED-ABSENT`, excluded from both numerator and denominator). Combined with never re-testing `RETRIEVABLE` readings, the reported rate can only ever be pushed **down** relative to what a fully symmetric confirmation regime would show — a false `RETRIEVABLE` stays uncorrected forever and stays in the denominator's favourable side; a corrected false-absent is removed from the picture rather than moved to the side it belongs on. The direction of this bias is forced by the code, not measured, and nothing in the tool states it.

### 4. [Non-blocking, narrows the claim] "Matching this practice's own K4 step" borrows a validation the practice's own record explicitly declines to give it.

`PREREGISTRATION-119-overlay-use.md`: *"Also not claimed: that K4's five re-requests are **the right test**. They are **the pre-registered test**."* Tonight's `CHANGELOG-v0.2.md` and `presence_check.py` both present `--confirm 5` as "matching this practice's own K4 step" — true as precedent, but the practice's own document says in as many words that precedent is all it is. The entire warrant rests on 6 historical events (`confirmation-record-121.json`, verified by direct read: NOT-RETRIEVABLE→RETRIEVABLE n=5/3, RETRIEVABLE→NOT-RETRIEVABLE n=3/3 all-readings/genuine). The tool is honest that "six events is not a rate," but the choice of *five passes specifically* has never been tested against anything, including the one thing I could cheaply test myself (next item).

### 5. Attack that FAILED, reported in the tool's favour: five rapid re-requests are not a cache replay.

I suspected 1.0-second-spaced re-requests might just be re-serving one cached edge answer, which would make "5/5 agree" far weaker evidence than presented. I issued two live requests, 1 second apart, against the arc's own persistently-absent identifier (`7234106298021727515`) and inspected headers:

```
0: Cache-Control: max-age=0, no-cache, no-store | X-Cache: TCP_MISS from a23-33-30-21...akamaitechnologies.com | Server-Timing: cdn-cache; desc=MISS, edge; dur=20, origin; dur=83
1: Cache-Control: max-age=0, no-cache, no-store | X-Cache: TCP_MISS from a23-54-205-36...akamaitechnologies.com | Server-Timing: inner; dur=45
```

Two different Akamai edge machines, both explicit `TCP_MISS`, distinct `X-Tt-Logid` each time, no caching directive. I could not break the independence of confirmation passes this way. Reported at full weight against my own case.

### 6. [Non-blocking, regression of the same class] The URL-acceptance path is domain-blind, reproducing I4's defect through a different door.

```
'https://www.youtube.com/video/7123456789012345678'          -> ('7123456789012345678', 'x', None)
'https://example.com/video/7123456789012345678/watch'        -> ('7123456789012345678', 'x', None)
'https://vimeo.com/video/7123456789012345678'                -> ('7123456789012345678', 'x', None)
```

`VIDEO_PATH_RE` (`presence_check.py` line 102) matches `/video/(\d{1,25})` anywhere in the string, with no host check. A YouTube, Vimeo, or arbitrary-domain URL that happens to carry `/video/<digits>` is silently accepted and measured against the TikTok oEmbed endpoint as if it named a TikTok identifier — structurally the same failure I4 was written to close (an out-of-scope string becomes a measured "video"), now via the accepted path instead of the rejected one. `INCREMENT-11.md` and the changelog describe I4 as closed; it is closed for bare-digit coercion and open for this.

### 7. [Non-blocking] The new strictness refuses several plausible real list formats.

Verified directly against `parse_line`:

```
'7123456789012345678\tsomeuser'   (tab-separated)      -> refused
'7123456789012345678;someuser'    (semicolon CSV)       -> refused
'7123456789012345678 someuser'    (space-separated)      -> refused
'https://m.tiktok.com/v/7123456789012345678.html'        -> refused, reason: "a short link or a link
                                                              from another platform" — FALSE for this
                                                              case; it is the same platform and the id
                                                              is a plain substring, not a redirect target
```

Tab- and semicolon-separated pairs are ordinary spreadsheet-export formats; the printed refusal reason for the mobile share URL is simply wrong about what kind of link it is.

### 8. [Non-blocking] The confirmation apparatus validates itself with instances of itself.

The "artefact echo" logic (`confirmation_record_121.py`) is real and correctly implemented — I traced its output against the raw sidecars by hand and it reconciles exactly. But every "genuine transition" in the confirmation record is itself downstream of an earlier five-pass confirmation subject to the same untested noise-conflation risk as charge 1. There is no independent check anywhere in this arc's history of whether a five-pass "confirmed" verdict is actually correct — only of whether it is internally consistent over a handful of seconds.

### 9. What survives outright.

`selftest_presence_check.py`'s 65 assertions ran clean (I re-ran them: exit 0). The I6 baseline-failure and I7 vantage-disclosure repairs are real, demonstrated, and correctly wired to exit codes and stdout/stderr. `confirmation-record-121.json`'s arithmetic reconciles against the raw sidecars exactly. The functional test's re-confirmation of `avfcofficial` 14h58m apart from two different Akamai edges is genuine independent evidence, not a construction. None of that is in dispute.

---

## (b) The hostile critique

Is it slop? No — the file that mattered got worked, and it got worked with the right instinct: run the fix, don't just narrate it. The selftest suite, the raw-sidecar recomputation, the live functional test, the addendum that admits a mixed state instead of hiding it — this is a session behaving like it has read its own gauntlet.

But look at what actually happened tonight against a 21-day clock with nothing sent: the practice spent an entire session hardening a tool nobody outside the house has touched yet, closed four of thirty-two carried conditions, left twenty-six untouched, did not run today's window measurement, and shipped a fix whose central new mechanism has a demonstrable hole its own 65-assertion suite doesn't cover. The two things named explicitly as still broken — frozen-reference drift, and a four-day series too short to show the temporal claim rather than assert it — are exactly the two things a stranger would need fixed before this is usable, and neither moved. The thing that did move is the thing furthest from a receiver's hands: whether a tool nobody has downloaded yet handles its own edge cases.

A serious critic reading this bundle tonight finds a house still perfecting its own confirmation logic while the artifact a named receiver could act on sits withheld for a fourth session running. The "same instrument" sentence sitting live and uncorrected one file away from tonight's own fix is the kind of thing that reads, from outside, as evidence the house checks its code more carefully than it checks its own text — exactly the asymmetry a hostile reader would go looking for first.

The honest version of tonight's accomplishment is narrower than the increment states it: the tool got harder to fool, not more correct. Those are not the same thing, and the gap between them is where the next reviewer should start.

---

## §c — Conditions

1. **[BLOCKING]** Fix or explicitly scope the confirmation-agreement logic so that an `INDETERMINATE` confirmation pass is not treated the same as a genuine-reversal pass. At minimum, report whether a disagreement was `INDETERMINATE`-caused or state-reversal-caused, and consider not discarding a majority-agreeing absence over one noisy pass. Add a selftest assertion that scripts an `INDETERMINATE` pass **mid**-confirmation (not first-pass) and pins the resulting state and rate treatment.
2. **[BLOCKING]** Correct `deliverable/README.md` §4.1 ("It is the same instrument, so your reading and ours are comparable") to match what `presence_check.py`'s own docstring now says, or add it as a third superseded statement in tonight's addendum. It cannot stand unedited beside a same-commit file that contradicts it.
3. State the direction of the reported-rate bias created by discard-rather-than-reclassify of confirmed-false absences, next to the existing "cannot detect a false reading of presence" caveat.
4. Either publish some empirical basis for five passes specifically (a repeat-request stability check at 3 vs 5 vs 10, even a small one) or soften "matching this practice's own K4 step" so it does not read as validation the practice's own record disclaims.
5. Fix the domain-blind `/video/<digits>` match, or state plainly that any host is accepted.
6. Restore or explicitly refuse-with-guidance the tab/semicolon/space-separated formats, and correct the `m.tiktok.com/v/<id>.html` refusal reason, which is factually wrong about what that link is.
7. Land the frozen-reference drift fix (V1/V2) before another session is spent on the tool — it is the one defect a reviewer said will quietly move somebody else's number, and it has now been carried across two full sessions.
8. Answer, plainly, whether hardening a not-yet-shipped tool was the right use of a session with 21 days left and nothing sent — the increment names this tension itself and does not resolve it.
