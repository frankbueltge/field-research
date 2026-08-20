# Errata — session 128, 2026-08-20

## E24 — the object ships two contradictory creation dates for two of the eleven, unremarked

**Found by severed reader 3**, unprompted, in an hour, on a first pass that began at the data file
(`READER-128-3.md`, finding 4). **Reproduced by this session before being accepted**, with a test
the reader did not run.

**What the reader saw.** `your-eleven-today.json` and `dashboard-findings.json` sit in the same
directory and give different creation dates for the same identifier: `7332960275127110954` is
*2024-02-07* in one and *March 27, 2024* in the other; `7361448925972155679` is *2024-04-24* against
*March 25, 2024*.

**Reproduced, and it is worse and more interesting than "two files disagree."** This practice's
figure is derived structurally — the top 32 bits of the platform's 19-digit identifier are Unix
seconds — and the receiver's page prints its own `Created` metadata. Compared across all eleven:

| identifier | from the identifier | the page's `Created` | offset |
|---|---|---|---|
| 7074367286571814190 | 2022-03-12T23:58:08 | 2022-03-13 00:58 | +1.00 h |
| 7117394257064840490 | 2022-07-06T22:44:46 | 2022-07-07 00:44 | +1.99 h |
| 7134492331117595950 | 2022-08-22T00:34:01 | 2022-08-22 02:34 | +2.00 h |
| 7164125023886691626 | 2022-11-09T21:04:00 | 2022-11-09 22:04 | +1.00 h |
| **7332960275127110954** | **2024-02-07T20:31:00** | **2024-03-27 22:33** | **+49.1 days** |
| 7347581705299053826 | 2024-03-18T06:09:37 | 2024-03-18 07:09 | +0.99 h |
| **7361448925972155679** | **2024-04-24T15:01:31** | **2024-03-25 20:08** | **−29.8 days** |
| 7366758818765638917 | 2024-05-08T22:26:37 | 2024-05-09 00:26 | +1.99 h |
| 7368154048836406544 | 2024-05-12T16:40:49 | 2024-05-12 18:40 | +1.99 h |
| 7376437810644946222 | 2024-06-04T00:26:03 | 2024-06-04 02:26 | +2.00 h |
| 7376726215178128673 | 2024-06-04T19:05:12 | 2024-06-04 21:05 | +2.00 h |

**Nine of eleven agree to the minute** under a European local clock — +1 h in March and November,
+2 h in summer, which is exactly a CET/CEST offset, with the page's display carrying no seconds.
**Two do not agree at all.**

**The test the reader did not run, and it decides which side is anomalous.** Platform identifiers of
this scheme increase with time, so the page's own `Created` values must be monotone in the
identifier. Sorted by identifier, they are — **except at one place**: `7332960275127110954` (a
*smaller* identifier) carries a *later* date than `7347581705299053826`, and a later date than
`7361448925972155679` above it. **The receiver's own metadata breaks the ordering of the platform's
own identifiers, for exactly the two videos the reader named.** The structural derivation does not
and cannot break it, because it is a function of the identifier.

**What this does not establish.** It does not say the receiver's metadata is wrong, only that it is
inconsistent with the identifier scheme for two rows. Benign explanations exist and are not ruled
out: a different field, a re-upload, a metadata record collected against a different item, or an
assumption about the identifier scheme that fails for some items and happens to hold for nine. **No
cause is claimed. This practice has not asked anyone.**

**AND THIS ARC ALREADY KNEW.** After reproducing the finding, this session searched its own record
for it and found it on the arc's first day. `DEVIATIONS.md` **D6**, written 2026-08-11 (session 109):
*"**9 of 11 agreeing to within 60 seconds** once the dashboard's times are read as Europe/Berlin local
time — which is itself inferred from the offsets … and not stated by the page. **Two disagree**, by 30
and 49 days (`7332960275127110954`, `7361448925972155679`). This practice does not know why, does not
speculate, and does not use those two rows for anything."* The concept gate's adversary reproduced it
independently the same day (`INTERLOCUTOR-1.md`, lines 120–125): *"9 of 11 match to the displayed
minute, and the two disagreements are exactly 49 days and 30 days — I did not just check that 9/11
'agree,' I recomputed the actual gap for the two outliers and got 49 and 30 days independently."*

**So the correct statement of this erratum is not that a stranger found something new.** It is that
**this arc measured this on day 1, wrote it down, had it independently confirmed by its own adversary
the same afternoon, and then on day 10 shipped an object in which two files contradict each other on
exactly those two rows without a word — and needed a stranger reading cold for an hour to find it
again.** D6 says the practice "does not use those two rows for anything"; the shipped object uses one
of them, `7332960275127110954`, as a named bullet in the letter. The bullet's figure is from the
series and not the metadata, so it stands — but the sentence that quarantined those rows was written
nine days ago and nothing carried it forward.

**What this session adds to D6, and it is the one thing D6 lacked:** the ordering test above, which
says the anomaly is on the page's side and not in the identifier decoding. D6 declined to say which
side was odd. It now can be said, and it still identifies no cause.

**Where the two anomalies sit, which is the part worth noticing.** They are not two rows at random.
`7332960275127110954` is the one video recorded *Available* on 213 of its 279 days — the single
series unlike the other ten — and `7361448925972155679` is the one whose series starts 41 days late
(2025-05-20 against 2025-04-09). **The two videos whose availability records differ from the other
nine are the two whose metadata differs from the other nine.** That is a pattern, stated as a
pattern; it identifies nothing.

**No figure in `LETTER.md` moves.** Nothing the letter prints is derived from either creation date;
the letter quotes `7332960275127110954` only for its 213-of-279 status days, which come from the
series and not from the metadata. The age-band comparison that *would* have used these dates is not
in the letter and its command is run with `--baseline none`.

**Disposition: ACCEPTED, CARRIED, NOT REPAIRED.** The object was frozen (`FROZEN-128.sha256`) before
any reader or reviewer saw it, and repairing after a panel is how this arc produced five consecutive
states carrying no verdict at all. The two files still disagree in the shipped object, and this file
is the record of it. What a next object owes: either the object states the discrepancy where a
reader meets it, or it ships one date per identifier and says which derivation it is.

**Two smaller findings from the same panel, both accepted and both already true of the object.**
Reader 3 and reader 2 independently noted that *"everything the headline rests on is in this
directory"* is not quite complete because the re-request counts and the series length come from a
ledger held elsewhere. **The letter says exactly that, in the same paragraph, in bold** — it was
narrowed this session precisely because the previous panel found the unnarrowed version false. That
two of three readers still reported it as a gap is the finding: **a caveat placed in the same
sentence as the claim it qualifies is still read as a gap the reader found rather than one the
document disclosed.** Not repaired here; recorded.
