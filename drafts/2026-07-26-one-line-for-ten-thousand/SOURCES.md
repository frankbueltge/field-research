# Sources — One Line for Ten Thousand

Everything load-bearing in this work comes from **one object**: the Dataset Register of the
federated research ecology, read at a pinned commit. There is no secondary literature, because the
work is a measurement of that object's own records, not an argument about the world.

## The pin

- Repository: `frankbueltge/dataset-hub`
- Commit: **`a7024008ec337118b2aeebb87065ded83ed23413`** — `2026-07-27T01:30:20+02:00`, subject
  `feat(werkzeug): Abfrage-Werkzeug für die Praxen und Bedarf-Rückkanal`; this was `refs/heads/main`
  at the time of the audit, established first-hand with `git ls-remote`.
- Snapshot release tag: **`snapshot-2026-07-26`** = `8be62d8b86f2b5ce3690f44a983497adac7957d6`.
- Every URL below is of the form
  `https://raw.githubusercontent.com/frankbueltge/dataset-hub/a7024008ec337118b2aeebb87065ded83ed23413/<path>`
  and each was fetched first-hand on 2026-07-26 (HTTP 200 recorded per path); the browsable form is
  `https://github.com/frankbueltge/dataset-hub/blob/a7024008ec337118b2aeebb87065ded83ed23413/<path>`.

## Records the audit computes on — frozen, CC0

Vendored into `provenance/register-records/`, hashes in `provenance/SHA256SUMS.txt`, recomputed by
`scripts/audit.py` on every run. The register dedicates its catalogue metadata — "the compilation,
its records and enrichments created in this repository, including released snapshots" — to the
public domain under **CC0 1.0** (`LICENSE.md`), which is what makes this freeze redistributable.

| Frozen file | Upstream path |
|---|---|
| `snapshot-2026-07-26.manifest.json` | `snapshots/snapshot-2026-07-26.manifest.json` |
| `manifeste/*.json` (6 files) | `fundstellen/manifeste/*.json` |
| `ablehnungen.jsonl` | `register/ablehnungen.jsonl` |
| `ausfaelle.jsonl` | `register/ausfaelle.jsonl` |
| `aufloesungen.jsonl` | `pruefungen/aufloesungen.jsonl` |
| `entscheidungen.jsonl` (empty upstream) | `journal/entscheidungen.jsonl` |

## Code read, quoted, not vendored (Apache 2.0)

- `pipeline/baue_bestand.py` — the build. Load-bearing for the last-wins reduction the audit
  reproduces in A14: the builder reads the resolution ledger into a dict keyed by entry id
  (`aufloesungen[z["id"]] = z`), so the last row for an id in file order is the one that reaches
  the entry, and for the two counters `aufgeloest_versucht` / `aufgeloest_bestaetigt`, which it
  computes over entries rather than over ledger rows.
- `pipeline/schranken.py` — the admission barrier. Load-bearing for the withheld-source mechanism
  (`QUELLEN_ZURUECKGEHALTEN = {"kaggle": "quelle-rechtlich-ungeklaert"}`) and for the
  constructed-URL rule that produced the 300 rejections of the model-hosting source
  (`konstruierte-url-ungeprueft`).
- `werkzeug/frage_register.py` — the query tool offered to the practices. Load-bearing for the
  semantics of the two filters this practice's evidence rule needs: `--geprueft` selects
  `e.zugang_geprueft IN ('landing','download')`, `--offen` selects licence ids matching
  `cc0% / cc-by% / pddl% / odbl%`. Its own gloss on a refusal, verbatim:
  > bei 403 meist Bot-Schutz, kein toter Link

  ("with a 403 usually bot protection, not a dead link".)

## Prose read and quoted (CC BY 4.0, attribution: Frank Bültge, https://frankbueltge.de)

**`README.md` — the register's binding rule this work takes seriously:**
> **Record rejections with reasons.** The rejection register measures the process against itself.

**`messungen/register.md`, §"Kaggle: zurückgehalten (2026-07-26)"** — the documented legal ground
for the withheld harvest, and the deletion it entailed. Verbatim, with the source's name elided per
this practice's naming rule:
> Die 9.991 Einträge sind **aus dem Bestand genommen** (`schranken.py:
> QUELLEN_ZURUECKGEHALTEN`, Grundcode `quelle-rechtlich-ungeklaert`), und die Inhalte
> sind **gelöscht** — Rohernten aus Release und Arbeitsverzeichnis, Kennungen aus
> Ablehnungs- und Fundstellen-Tabelle.

("The 9,991 entries have been **taken out of the corpus** (`schranken.py:
QUELLEN_ZURUECKGEHALTEN`, reason code `quelle-rechtlich-ungeklaert`), and the contents are
**deleted** — raw harvests from the release and the working directory, identifiers from the
rejection and origin tables.")

> Erhalten bleiben nur die Ernte-Manifeste und ein Sammeleintrag im Ablehnungsregister: unsere
> Buchführung über unser eigenes Handeln, ohne Fremdinhalt.

("What is kept is only the harvest manifests and a single collective entry in the rejection
register: our bookkeeping about our own action, without third-party content.")

The same section records the legal reason as read by the register from the source's terms-of-use
page, and its own self-correction of an earlier version of that entry. **This session did not
retrieve any terms-of-use page and makes no claim about what any third party's terms permit or
forbid** — only that the register's record states a reason and names where it read it.

**`messungen/VERFAHRENSNOTIZEN.md`** — the register's log of what went wrong while building, whose
header states the principle:
> Was beim Bauen schiefging, mit Datum. Nach demselben Prinzip wie das Ablehnungsregister: nicht
> stillschweigend korrigieren, sondern mitschreiben.

("What went wrong during construction, with dates. On the same principle as the rejection
register: do not correct silently, write it along.")

Two notes in it are load-bearing for this audit, because they are the corrections that do not
travel:

1. The false negatives (§"HEAD ist kein Befund über die Ressource (400 falsche Negative)"):
   > **[The withheld source] antwortet auf HEAD mit 404 und auf GET mit 200** (nachgemessen an
   > derselben URL). Alle 400 Einträge waren erreichbar und wurden trotzdem als „geprüft, nicht
   > bestätigt (404)" vermerkt

   … and the rule drawn from it:
   > **Jedem Nicht-2xx aus HEAD wird jetzt mit GET nachgegangen.** Ein HEAD-Fehlschlag ist ein
   > Befund über die Methode, nicht über die Ressource. Nach der Korrektur: 450 von 450 bestätigt.

   ("**Every non-2xx from HEAD is now followed up with GET.** A HEAD failure is a finding about the
   method, not about the resource. After the correction: 450 of 450 confirmed.") The audit's A15
   and A16 recover exactly this event from the ledger alone — 400 ids, each first `(404, false)`
   then `(200, true)` — and A14 recovers the "450 von 450".

2. The refusal note (§"Erster Auflösungslauf: 403 ist kein toter Link"), whose count is right and
   whose host clause the register's own ledger contradicts:
   > 53 von 200 Zugriffswegen antworteten mit HTTP 403, alle vom selben Host (GBIF).

   ("53 of 200 access routes answered with HTTP 403, all from the same host (GBIF).") A18 finds the
   53 split across **five** hosts: GBIF 48, openICPSR 2, `data.nhm.ac.uk` 1, `researchgate.net` 1,
   `checklistbank.org` 1.

Also read and quoted for the register's own statement of the counter-direction it asks of the
practices (`bedarf/offen.md`):
> Ein Register, das nur wächst, wohin seine Adapter zufällig zeigen, misst am Ende sich selbst.

("A register that grows only where its adapters happen to point ends up measuring itself.")

## The offer this work answers

The seed in this practice's own `REQUESTS.md`, dated 2026-07-26 ("Seed: ein Register geprüfter
offener Datensätze steht bereit"), including the sentence that fixes this audit's central question:
> `--geprueft --offen` liefert genau die Teilmenge, die eure Nachweispflicht erfüllt

("`--geprueft --offen` delivers exactly the subset that fulfils your evidence duty".) In-repo,
`REQUESTS.md`, commit `c041be39b9c07f6378991ba8e539b3e5291bba98`.

## Retrievability and access, stated as measured

`provenance/access-attempts.md` carries the first-hand transcript with timestamps and status codes:
the tree is reachable from this practice's runtime over `raw.githubusercontent.com` and the git
protocol; the snapshot **release asset** is not (HTTP 403 on all three routes tried). That transcript
also states plainly that the 403 is this runtime's own scoped egress policy answering, not the host,
and that nothing here claims the register's distribution channel is broken for anyone else.

## Nothing else

No other source is cited, because none is needed and none was used. Two numbers appear in this work
that come from the register's prose rather than from its records — the prose's own count of the
withheld entries (9,991) and its 403 host claim — and both are marked as quotations being checked
against the records, not as this work's own measurements.
