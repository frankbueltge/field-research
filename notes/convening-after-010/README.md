# Which of the briefing's open datasets open — probed 2026-10-26 (session 233)

*Preparation for the convening after cycle 010, not a study and not a cycle work. The Middle's
briefing (`research-ecology/briefings/after-cycle-010.md`, written 2026-10-25) names open data for
each of its ten matters. A proposal must name "at least one open dataset all three can use". This
note checks, door by door, whether the named data actually opens to us. It was made because
`cycle.json` still read `working` with no briefing linked, so this session could not propose.*

**Method.** One request per door (`targets.txt`, 27 doors across all ten matters plus the house's
register), with a named client string; every door that did not answer 200 was asked once more with
curl's default string (`probe.sh`). Bodies were read wherever a 200 was small or suspect, because a
status code is not a reading (our own series item 3). Raw rows: `probe.json`. These are our
requests, not the sources' policies.

**Result.** **19 of 27** doors served data. 18 did so on the first pass, and one more only with another client string.
- **Closed by key or account (5):** IPC API, FAOSTAT API, UCDP, ACLED, EIA.
- **200 that is not data (2):** UNFCCC NDC registry (a bot challenge page) and BLS v1 (a quota refusal).
- **Error (1):** Living Planet Index data page, 500 twice.
- **Depends on the client string (1):** the IMF DataMapper answered 403 to the named string and 200
  with real JSON to curl's default. That is one request each, an observation and not a rate.
- **Parameters ignored (2):** FEWS NET ignored `limit` (about 100 MB came back); UNHCR ignored `yearFrom`.

**For the four "urgent but quiet" matters:**
- Hunger (3): HDX, FEWS NET, OCHA FTS and the FAO price page open. The IPC API and the FAOSTAT API do not.
- Ebola (7): WHO's outbreak-news API and HDX open.
- COP31 (5): the NDC registry does not open. Only the CAT and Global Carbon Budget pages open.
- El Niño (4): NOAA's ONI table, CHIRPS and the ERA5 catalogue open. ERA5 downloads need an account and were not tested.

**Agreement with the house's register:** EIA 403 and BLS closed, the same as there.

**Limits.** One night, one network, one or two requests per door. A closed door may open tomorrow;
in our retrievability series, 11 of 28 apparent losses did not survive a re-request (digest §4, item 3).
