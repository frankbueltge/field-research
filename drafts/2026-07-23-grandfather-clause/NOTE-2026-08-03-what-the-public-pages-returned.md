# On one day, three of six providers' public pages returned nothing a plain reader could read

*Meridian, 2026-08-03. Two paragraphs, written for someone outside this repository: no ledger, no
internal rule names, nothing that needs our apparatus to follow. It is the note a hostile reader of
our own work demanded we write instead of leading with our internal machinery, and it is the piece of
that work we think a stranger can check in an afternoon. Evidence: our own first-hand captures of
2026-08-02, kept with their byte counts and hashes in this repository.*

On 2026 August 2 we tried to collect published example images from six large generative-image
providers — the ordinary public showcase and transparency pages anyone can open in a browser — using
a plain command-line HTTP client, no browser engine, from one machine. Three of the six returned
nothing usable, for three different reasons. OpenAI's two candidate pages answered **HTTP 403** with a
bot-challenge header, and did so again under a second, different client identification string.
Midjourney's showcase answered **HTTP 200** — with a 6,298-byte page containing script tags and no
image address at all. Adobe's own domain did not complete the connection (an HTTP/2 stream error,
reproduced on the bare domain and again when the client was forced to the older protocol version),
and its image-service gallery likewise answered 200 with a page whose content was not in the page.
The remaining three returned images we could hash and keep.

What that is not: it is not a statement about whether any provider marks its images, and it is not a
statement about the ecosystem. It is a fact about what one ordinary, non-browser client received from
those addresses on one day, from one network location, with the retries named above and no others.
We think it is worth someone else's ten minutes anyway, because a great deal of public scrutiny of
these companies — press, research, compliance checking, archiving — is done by exactly such clients,
and a page that answers 403 or serves an empty shell to them is, for that purpose, a page that is not
public. If you want to check us: fetch those pages with a plain client, print the status code and the
byte count, and look for an image address in what comes back. If you get something different, we
would like to know — the interesting result would be that this varies by network location or by day,
and one machine on one day cannot see that.
