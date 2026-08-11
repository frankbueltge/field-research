# Deviations, and things declined — session 109, 2026-08-11

*Written as they happened, not assembled at the end. A deviation recorded is not an excuse; it is
the part of the record that lets someone else judge whether the result survives it.*

## D1 — The pre-registered corpus route died and was replaced, and the replacement is broader than the words allowed

`PREREGISTRATION.md` §2 named the public web-crawl index as the corpus route and allowed *"at most
two alternative credential-free dated sources … tried and named"*.

- Alternative 1: the public web archive's index API — **HTTP 403 "Blocked by egress policy"**, and
  the plain host reset the connection. Fifth consecutive session that host is unreachable from here.
- Alternative 2: the MediaWiki external-link index.

**The deviation:** alternative 2 was queried across **21 language editions**, not one. This practice
treats the MediaWiki external-link index as *one* source queried in 21 places, because it is one
API, one query, one namespace rule and one data model. That reading is stated rather than assumed,
and anyone who reads the pre-registration as "two endpoints" should discount the corpus size
accordingly: **English Wikipedia alone yields 853 distinct ids**, which is below the 1,000 that
prediction P2 and kill criterion K1 name. **On the strictest reading of our own pre-registration,
P2 fails and K1 fires.** On the reading above, both pass with 2,201. Both readings are published; the
adversary decides.

## D2 — The timestamp validation was wrong on its first run, and the fix is in the file

The first version of `validate_timestamps.py` collected citation dates from a ±400-character window
around each link and reported **47 ordering violations out of 182 pairs** with outliers of ±16,000
days. That is a bug, not a finding: a character window picks up the dates of neighbouring citations.
Rescoped to the **enclosing template only** (and skipping nested templates rather than guessing), the
same check gives **6 violations out of 160**. The wrong number was never published as a result; it is
recorded here because it was computed, and because the corrected script carries the reason in a
comment at the line that changed.

## D3 — A source reported by a search fan-out that this practice could not re-open

The European Commission press release of **2025-12-05** (IP/25/2940) is reported by a search fan-out
as stating that the researcher-data-access strand of the TikTok proceedings *"continues"*. **This
practice could not re-open it.** The PDF fetches (HTTP 200, 40,505 bytes) but no PDF text extractor
on this machine works — the installed library fails at import with a native-binding error, and no
command-line extractor is present. The press-corner HTML page renders its content in script and
returned only the site title.

It is therefore recorded as **second-route material carrying no load**: nothing in `CONCEPT.md` or
`RESULT.md` depends on it. What *is* used for the regulatory frame was re-opened here by hand — the
Commission's roundtable page of 2026-05-20 (HTTP 200, 5,053 characters of text, read to the end) and
the platform changelog (HTTP 200, 751,085 bytes, the 2026-02-26 entry quoted verbatim from the raw
fetch).

## D4 — The census exceeds the pre-registered sample, deliberately, and is reported separately

`PREREGISTRATION.md` fixed **n = 300**. After the sample was measured and the K3 control run
completed, the **whole corpus of 2,201** was put through the same probe. This is *more*, not
*different*: the pre-registered sample's result is reported as the pre-registered result, and the
census is reported beside it as an additional measurement, in its own section, whatever it says. It
was launched **before** the sample's numbers were written up as a claim, and it could not be
selected against — it is the entire population.

## D5 — What the probe does to a third party, considered before it ran

The probe issues one request per video to a commercial endpoint. `robots.txt` was fetched and read
to its end **before** the first probe request. The `User-agent: *` group disallows fifteen paths;
`/oembed` is not among them, and this client is none of the 25 named agents. The run is sequential
at roughly one request per second, and a throttling response ends the run rather than triggering
retries. The arc's steady state would be ~2,201 requests per day, an average of 0.025 requests per
second. The consideration is recorded rather than assumed; a reader who thinks the balance is wrong
can see exactly what was weighed.

## D6 — Two of eleven independent date checks disagree, and no explanation is offered

Validating the identifier decoding against the dark dashboard's own displayed creation dates gives
**9 of 11 agreeing to within 60 seconds** once the dashboard's times are read as Europe/Berlin local
time — which is itself inferred from the offsets (+1 h in November and March, +2 h in May, June,
July and August) and not stated by the page. **Two disagree**, by 30 and 49 days
(`7332960275127110954`, `7361448925972155679`). This practice does not know why, does not speculate,
and does not use those two rows for anything.

## D7 — One token redacted from a verdict this practice publishes unedited, and why

`INTERLOCUTOR-1.md` is published **unedited** — that is the constitution's rule and it exists so that
criticism cannot be softened. **One token in it is redacted:** in the command list, the adversary's
comment on the egress query named the autonomous system's registrant. This practice's naming rule
forbids naming commercial vendors in its texts, and the registrant is a hosting company incidental to
everything measured. The redaction is marked in place, the **AS number is left intact** so anyone can
resolve the name themselves in one query, and **nothing about the adversary's argument, evidence or
verdict is touched.** Recorded here rather than done quietly, because a document whose whole authority
comes from being unedited must account for the one character range where it is not.

**A related case that is *not* a deviation:** `tiktok-robots-2026-08-11.txt` is a primary source
fetched verbatim, and it lists 25 crawler agent names, several of them commercial products. It is
evidence — finding F2 rests on the presence of one of those names in it — and evidence is quoted as
found. The naming rule governs what this practice calls itself and its tools, not what a source it
fetched happens to say.
