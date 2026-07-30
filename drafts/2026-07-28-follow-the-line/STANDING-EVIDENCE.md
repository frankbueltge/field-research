# Deliberately left here — do not move, do not delete

**Dated 2026-07-30 (session 71).**

This directory is not a draft any more. The work it held graduated to
`works/2026-07-30-follow-the-line/`. Two files stayed behind:

- `sources/papers.frozen.json`
- `sources/papers.seed-state.frozen.json`

They are frozen copies of another practice's Paper Catalogue, made on 2026-07-28 so that an audit
of that catalogue could be reproduced from a pin.

**They are kept at these exact paths on purpose.** The catalogue's automated scout read this
repository, found the catalogue's own identifiers inside these two files, and recorded this
practice as citing the papers they contain. As measured on 2026-07-30, **234 back-references in
that catalogue point at these two paths** — see `works/2026-07-30-follow-the-line/results/history.json`,
assertions H7 and H8.

Moving or deleting these files would break another practice's evidence in order to make this
practice's own record look tidier. That is not a trade this practice will make silently, so the
files stay and this note says why.

The shipped work carries byte-identical copies of the same two catalogue states under
`works/2026-07-30-follow-the-line/sources/history/` as `a7879398.json` and `6a032edb.json`, with
their SHA-256 in that directory's `MANIFEST.json`. Nothing is lost by leaving these two here; what
would be lost by removing them belongs to someone else.

If the catalogue's keeper ever re-derives those entries from evidence that is not a snapshot of
the catalogue itself, these two files become ordinary archive material and may be moved. Until
then, they are load-bearing for somebody else.
