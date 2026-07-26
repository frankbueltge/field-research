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
