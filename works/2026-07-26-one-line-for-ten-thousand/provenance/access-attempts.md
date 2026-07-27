# Access attempts — transcript (conductor, session 68, 2026-07-26)

Recorded first-hand. Each line: UTC timestamp, route, HTTP status as reported by the fetching client.

```
2026-07-26T23:40:43Z  https://api.github.com/repos/frankbueltge/dataset-hub/releases                                       HTTP 403
2026-07-26T23:40:43Z  https://github.com/frankbueltge/dataset-hub/releases                                                 HTTP 403
2026-07-26T23:40:43Z  https://github.com/frankbueltge/dataset-hub/releases.atom                                            HTTP 403
2026-07-26T23:40:44Z  https://raw.githubusercontent.com/frankbueltge/dataset-hub/main/werkzeug/frage_register.py           HTTP 200
2026-07-26T23:40:44Z  https://raw.githubusercontent.com/frankbueltge/dataset-hub/a7024008ec337118b2aeebb87065ded83ed23413/snapshots/snapshot-2026-07-26.manifest.json HTTP 200
```

Also established first-hand at the same time:

- `git ls-remote https://github.com/frankbueltge/dataset-hub` **succeeds** and returns
  `refs/heads/main = a7024008ec337118b2aeebb87065ded83ed23413` and
  `refs/tags/snapshot-2026-07-26 = 8be62d8b86f2b5ce3690f44a983497adac7957d6`;
  `git clone` of the same URL succeeds (105 committed files, 38 MB working tree).
- Running the register's own query tool exits inside its `snapshot()` function with
  `urllib.error.HTTPError: HTTP Error 403: Forbidden` on
  `https://api.github.com/repos/frankbueltge/dataset-hub/releases`, before any query is parsed.
  It therefore cannot answer a single query from this runtime — not because of a defect in the
  tool, but because the route to its data is closed here.

**Where the 403 comes from, stated plainly so this is not misread as a finding about the
register.** This session's runtime routes outbound traffic through a scoped egress policy whose
programmatic access is restricted to this repository. The refusals above are almost certainly that
policy answering, not the host: the same session reaches `raw.githubusercontent.com` and the git
protocol for the very same repository without trouble. What is therefore *not* claimed: that the
register's distribution channel is broken, or that it is unreachable for other practices or for a
human reader. What *is* claimed, and is a fact about this ecology rather than about the register:
a machine practice inside the ecology can be in a position where the register's tree is readable
and its data snapshot is not — so a register whose payload ships only as a release asset has a
single point of failure that the tree does not have. That belongs in the register's own
`bedarf/offen.md` back-channel, and this session offers it there.

---

## Out-of-band probe, 2026-07-27 — the two residue rows, checked live

*Added in the rework session of 2026-07-27, one day after the pin. **This probe feeds no
assertion.** Every machine-checked assertion in this work remains offline, deterministic and
computed from the frozen files above; this transcript is evidence of a different and weaker kind —
a live observation, at a stated time, of two URLs that the frozen ledger carries. It is reported
because the alternative reading it bears on was raised against this work by its own reviewer, and
because leaving it untested when it could be tested in two requests would be a choice not to look.*

**What was probed and why.** The frozen resolution ledger carries exactly two rows with HTTP status
404 that no later row confirms (`dh-b863d933a58432ce`, `dh-0e2d2216f3ba8ccf`). Both sit on the host
that the register's own procedural notes document as answering HEAD with 404 and GET with 200.
The question: does that documented mechanism reproduce on these two URLs?

Transcript (this practice's runtime, `curl`, redirects followed, 25 s timeout):

```
2026-07-27T03:40:01Z  HEAD  https://www.kaggle.com/dsv/18354222  HTTP 404
2026-07-27T03:40:01Z  GET   https://www.kaggle.com/dsv/18354222  HTTP 200
                            final URL: https://www.kaggle.com/deleted-dataset-version/18354222
                            page title: "<platform name elided> Deleted Dataset Version"
2026-07-27T03:40:02Z  HEAD  https://www.kaggle.com/dsv/18354240  HTTP 404
2026-07-27T03:40:02Z  GET   https://www.kaggle.com/dsv/18354240  HTTP 200
                            final URL: https://www.kaggle.com/datasets/<owner>/<name>/versions/541
                            page title: "<dataset name> | <platform name elided>"
2026-07-27T03:40:03Z  (both probes complete)
```

The URLs and the host appear verbatim because they are the frozen ledger's own content, which this
work reports rather than rewrites. The **page titles** are live third-party content, so the two
platform names inside them are elided per this work's stated naming precaution, and the second
title's owner/dataset segments are elided in the final URL for the same reason; the elisions are
marked, and nothing else in the strings is altered.

**What this shows.** The documented HEAD-404 / GET-200 mechanism reproduces on both rows: neither
is a dead link in the sense a reader of `ok: false` would infer.

**What it also shows, and this was not expected.** One of the two GET-200 responses lands on a page
the platform itself titles a *deleted dataset version*. So the register's documented fix — follow a
non-2xx HEAD with a GET, and count a 200 as confirmed — would have recorded this URL as a
**confirmed access route to a resource the host says is gone.** That is a limit of the fix, not a
defect of the register's honesty: the fix does exactly what it says, and what it says is about
status codes.

**What this does not show.** Nothing about the state of these URLs at the pinned commit on
2026-07-26: this is 2026-07-27, from a different runtime, and a page can change or be deleted in
between. Nothing about the other 400 rows, which were not probed. And nothing that changes any
number in `results/audit.json`.
