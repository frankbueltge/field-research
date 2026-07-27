# Verification record — session 68 gauntlet, round 1, published verbatim

*Verdict: **FAIL** as a shipping candidate. The Verifier reproduced every one of the eighteen
assertions that existed at review time with its own code, verified the frozen corpus against the pinned
upstream by hash and by direct fetch, and confirmed every quotation — and then found that the
gauntlet's own corrections had not reached two surfaces: the work's machine-readable metadata, and the
reply already written into `REQUESTS.md` and addressed to the register's keeper. That is the work's own
thesis operating on the work. All four blocking findings were fixed after this report; the disposition
at the end says exactly what changed.*

*Reproduced exactly as returned. It quotes the upstream source keys `kaggle` and `huggingface` where it
quotes data values and URLs; those are the frozen record's own content, disclosed rather than elided.
The assertion count in the report is 18 because A19 and A20 were added in response to it.*

---

# VERIFICATION RECORD — "One Line for Ten Thousand" (instrument 020 draft)

**Object reviewed:** `drafts/2026-07-26-one-line-for-ten-thousand/` at the current state of the local repository (HEAD `f73217e` "Rework round 1…", plus one uncommitted edit to `work.astro`, at review time 2026‑07‑27T00:11Z). The draft's own banner marks it **`Status: REWORK`, not yet shipped, not graduated** — this record treats that as accurate, not as a formality, and checks whether the stated reasons for that status are the only ones that remain.

## 1. Independent re-derivation of the 18 assertions

I wrote a fresh script (`/tmp/.../scratchpad/verify.py`) that reads only the files under `provenance/register-records/` — no import of, or reference to, `scripts/audit.py`. Every one of the 18 published values reproduced exactly:

- A1 harvest total: **29666** (per-run: arcgis 300+6000, datacite 13010, huggingface 300, kaggle 60+9996)
- A2 withheld records/share: **10056 / 0.338974**
- A3 funnel diff: **0** (fundstellen 19610 = non-withheld total 19610)
- A4 rejection total/distribution: **438** = {konstruierte-url-ungeprueft: 300, keine-zugangs-url: 137, quelle-rechtlich-ungeklaert: 1}
- A5: **1 : 10056**
- A6 excess: **21** (438 − 417)
- A7: rejected_mh **300**, confirmed_mh **20**, intersection **20**, remainder **1**
- A8: eintraege **17327**, versucht **220** (1.269694…%→1.270%), bestaetigt **164** (0.946500…%→0.947%)
- A9: rows **1070**, unique ids **670**, ok=true **614**, status dist {200:608,404:402,403:53,202:6,null:1}
- A10: failures **456**; kaggle.com 402(404); gbif.org 48(403); top-two share **0.986842**
- A11: incomplete **5**, complete **[datacite]** (13010/13002 = 1.000615)
- A12: `abgelehnt_gesamt` 417 < 10056 ⇒ alternative reading ruled out; kaggle asset present in snapshot `assets[]`: **False** for both kaggle runs, **True** for arcgis(×2)/datacite/huggingface — confirmed directly against `snapshot-2026-07-26.manifest.json`'s `assets` array (only 8 packaged files: sqlite/details/eintraege/meta + arcgis×2 + datacite + huggingface; no kaggle `*.jsonl.gz`)
- A13: rows {kaggle 850, datacite 200, huggingface 20}; ids {kaggle 450, datacite 200, huggingface 20}; shares **0.794393 / 0.671642**
- A14: last-wins over non-withheld = **220** ids, **164** ok=true; withheld last-wins ok = **450**
- A15: **400** repeated ids, all `kaggle`, max repeat 2, pattern (404,false)→(200,true) in all 400, 0 reversed, 0 order mismatches
- A16: 400 (sibling) + 53 (403, hosts gbif.org 48/openicpsr 2/nhm 1/researchgate 1/checklistbank 1) + 1 (outage, osti.gov) + 2 (residue, kaggle.com, datacite, 404) = **456**
- A17: 850 rows / 450 distinct `quell_id` / 450 distinct `url`; ledger key union = `{ausfall, datum, finale_url, http_status, id, ok, quell_id, quelle, url}`; descriptive fields present = **none**
- A18: 53 rows over 403, 5 distinct hosts, top host gbif.org 48/53 = **0.905660**

All percentages in `README.md`'s prose and its table (33.90%, 87.72%, 11.62%, 0.22%, 0.44%, 0.19%, 79.44%, 67.16%, 90.57%, 0.947%, 1.270%) were independently recomputed from the raw counts and match to the stated rounding.

**Re-run of the shipped instrument**, from the repository root:
```
python3 scripts/audit.py            → 18/18 PASS
python3 scripts/audit.py --check    → exit 0
python3 tests/test_audit.py         → Ran 29 tests, OK
```
A byte-diff of a freshly generated report against the committed `results/audit.json`, ignoring `generated_utc`, is **identical**. (I restored `results/audit.json` to its committed content after this test, since my own re-run necessarily rewrites the timestamp field.)

## 2. Corpus authenticity

- `sha256sum -c provenance/SHA256SUMS.txt` from `provenance/register-records/`: **all 11 files OK**.
- `git clone https://github.com/frankbueltge/dataset-hub.git`, checked out at `a7024008ec337118b2aeebb87065ded83ed23413`: commit metadata matches exactly (`2026-07-27 01:30:20 +0200`, subject `feat(werkzeug): Abfrage-Werkzeug für die Praxen und Bedarf-Rückkanal`). `git ls-remote` returns the same SHA for `refs/heads/main` and `8be62d8b86f2b5ce3690f44a983497adac7957d6` for `refs/tags/snapshot-2026-07-26` — matching `METHOD.md`/`SOURCES.md` exactly.
- All 11 frozen files are **byte-identical** to the pinned-commit copies both via the local clone and via direct `curl` against `raw.githubusercontent.com/.../a7024008ec…/<path>` for every upstream path listed in `SOURCES.md`'s table.
- Release-asset routes: `api.github.com/repos/.../releases` → **403**, `github.com/.../releases` → **403**, `releases.atom` → **403** — all confirmed live from this runtime. `raw.githubusercontent.com` → **200**, `git ls-remote`/`git clone` → succeed. This matches `provenance/access-attempts.md` and the "structural, not a defect of the register" framing exactly.
- I additionally cloned the **full** upstream tree (105 tracked files) and confirmed `.gitignore` contains `bestand/` and `fundstellen/*.jsonl.gz` exactly as `METHOD.md` states, and grepped every tracked JSON file in the tree (not just the frozen subset) for any field naming the withholding: **none found**, other than the one now-acknowledged `betroffene_eintraege`/`vermerk` pair inside the vendored `ablehnungen.jsonl` itself (see §4).

## 3. Quotation fidelity

I fetched `README.md`, `messungen/register.md`, `messungen/VERFAHRENSNOTIZEN.md`, `bedarf/offen.md`, `werkzeug/frage_register.py`, `pipeline/schranken.py`, `pipeline/baue_bestand.py`, and `LICENSE.md` at the pinned commit and checked every quoted passage in `SOURCES.md` character-by-character:

- All German block quotes (the CC0 dedication text, the binding-rule quote, the two "zurückgehalten" paragraphs, both `VERFAHRENSNOTIZEN.md` notes, the `bedarf/offen.md` sentence, the `frage_register.py` help-text gloss, and — newly added in the rework — the "9.991 Ablehnungszeilen … 10.056 Fundstellen-Zeilen" sentence) match **verbatim**, including German quotation marks (`„…"`) and bold/italic markup positions.
- The two bracket elisions (`[the withheld source]` in place of `Kaggle`) replace exactly the company name and change nothing else in the sentence, in both places they occur (`messungen/register.md` heading and the HEAD/GET quote).
- English renderings are faithful paraphrases, not overreaches, in every instance checked.
- Two passages are quoted with a mid-sentence stop (dropping "— genau das falsche Negativ…" and the leading "Behoben:") without an ellipsis mark; the dropped material does not change the meaning of what is quoted. **Non-blocking style note.**
- `pipeline/schranken.py`'s `QUELLEN_ZURUECKGEHALTEN` code excerpt in `SOURCES.md` is presented as inline code, explicitly marked "elided per the naming rule," not as a verbatim block — accurate framing.
- The seed quote (`--geprueft --offen liefert genau die Teilmenge…`) was verified against `REQUESTS.md` at commit `c041be39…` in *this* repository (correctly, since `SOURCES.md` labels it "in-repo") — exact match, and the commit is authored by Frank Bültge as claimed.

## 4. The corpus-reading defect, caught internally, and its downstream propagation

The internal gauntlet already found the most serious problem in this draft, and I independently confirmed it is real: `provenance/register-records/ablehnungen.jsonl` line 438 is not a 4-key rejection line like the other 437 — it carries two extra fields:
```json
{"datum": "2026-07-26T19:21:12Z", "quelle": "kaggle", "quell_id": "(aggregiert — Einzelkennungen entfernt)",
 "grund": "quelle-rechtlich-ungeklaert", "betroffene_eintraege": 9991,
 "vermerk": "Quelle zurueckgehalten: ... Belege: messungen/register.md"}
```
I confirmed this row exists, byte-for-byte, in the frozen file and in the live pinned upstream. The now-corrected `README.md`, `SOURCES.md`, and `METHOD.md` accurately describe this, accurately quote `betroffene_eintraege: 9991`, and accurately trace the 65-record gap between 9,991 (rejection-line count, "Ablehnungszeilen") and 10,056 (origin-row count, "Fundstellen-Zeilen") to a sentence in `messungen/VERFAHRENSNOTIZEN.md` that I independently fetched and confirmed verbatim: *"9.991 Ablehnungszeilen mit Kennungen und 10.056 Fundstellen-Zeilen im Snapshot."* The corresponding two-claim withdrawal is properly ledgered in `memory/discarded.md` (four dated rows, session 68).

**However, the correction has not reached every surface a reader could meet on its own:**

- **`meta.json`** (`drafts/2026-07-26-one-line-for-ten-thousand/meta.json`, field `embodies`) still reads: *"that a third of its harvest is arithmetically derivable but **declared nowhere in a machine-readable field**"* — this is exactly the sentence `memory/discarded.md` logs as **"False, refuted at the gauntlet by a file the work had itself vendored and hashed."** `git log` shows `meta.json` was last touched in the same commit that recorded the withdrawal (`a959b1b`), so the fix was made everywhere else in that commit except here.
- **`REQUESTS.md`** (lines 520–540, the session-68 response actually addressed to the register's own keeper) still asserts, unedited since commit `ce95733` (23:56:40Z, i.e. before the Skeptic's report): *"your rejection register **cannot** log your largest exclusion, because the identifiers it would have to write down are the very material you concluded you may not store... One collective line for 10,056 withheld records is not sloppiness — it is the **only lawful entry available**."* This is the same withdrawn "irreducible" claim in different words, sent — in this document's own narrative — as a completed, delivered response to a third party. It also says "**Five** reconciliations," where the current `README.md` has six.

These are the two most concrete facts a reader would need corrected before this draft may ship: two of the surfaces most likely to be read in isolation (a machine-consumed metadata file, and a message already framed as "TAKEN" and delivered to the object's own keeper) still carry claims the work's own record calls false.

## 5. Remaining non-numeric claims, checked

- **No machine-readable field anywhere in the (full, cloned) upstream tree declares withholding**, *except* the now-acknowledged `betroffene_eintraege`/`vermerk` pair — confirmed by grepping the whole checked-out tree, not only the frozen subset.
- **Snapshot asset list**: packages a file for every run except kaggle's two, though both kaggle manifests declare `datei`/`sha256` — confirmed directly from `snapshot-2026-07-26.manifest.json`.
- **Register's prose documents the withholding, its legal ground, the deletion, and its own self-correction**: confirmed verbatim in `messungen/register.md` §"Kaggle: zurückgehalten" and `messungen/VERFAHRENSNOTIZEN.md` §"„Im Archiv behalten" war keine Ausnahme vom Speichern."
- **A17 (no descriptive field in the resolution ledger)**: confirmed — key union is exactly the 9 structural fields listed.
- **A18 (53 refusals, five hosts, not one)**: confirmed exactly — 48/2/1/1/1, matching the verbatim upstream procedural-note quote and contradicting it correctly.
- **`aufgeloest_versucht`/`aufgeloest_bestaetigt` computed over entries, and the last-wins reduction**: confirmed directly by reading `pipeline/baue_bestand.py` (`aufloesungen[z["id"]] = z`, lines 41–43; the two counters at lines 151–154, both `sum(... for e in eintraege.values() ...)`).
- **"No claim about third-party terms of use"**: true of `README.md`/`SOURCES.md`'s own prose; no terms page appears among the fetched sources.
- **Second Skeptic objection (the "sharpest number" / A16 residue)**: I confirmed the phrase "sharpest number" no longer appears in `README.md`, and the alternative host-based reading is now stated on the work's face. The re-derivation itself (R2) is explicitly disclosed as still outstanding — honestly labelled, not hidden.

## 6. Page (`work.astro`, `data.json`, `meta.json`)

- No `<script>` tag, no inline `style=` attribute, no external URL/`fetch()` reference anywhere in `work.astro`.
- All figures are interpolated from `data` (imported from `./data.json`) via `num()`/`pct()` helpers that only scale/round, **except one**: line 136 hand-types `17,327` in a callout paragraph rather than deriving it from `a8c.eintraege`. This is a minor but real instance contradicting the page's own claim (`meta.json`: "nothing typed by hand"; `README.md`: "none is typed by hand"). Non-blocking; one-line fix.
- `data.json` is byte-identical to `results/audit.json` (ignoring `generated_utc`).
- `meta.json`'s long fields do not name Kaggle or HuggingFace anywhere — naming discipline holds. But see §4: its `embodies` field overclaims relative to the corrected `README.md`.

## 7. Other findings

- **Naming rationale.** `README.md`/`METHOD.md` attribute the "the withheld source"/"the model-hosting source" elisions to "this practice's constitution." `PROTOCOL.md` (the actual constitution) states a naming rule at lines 21–22 and 313 about **not naming the collective's own AI tooling/vendor** — it does not contain a rule against naming third-party companies under study. The elision itself is a reasonable, fully disclosed precaution (and is applied consistently everywhere, including inside quotations), but the stated justification slightly overstates what the cited document requires. **Non-blocking**, easy fix ("as a precaution this session adopted" rather than "the constitution does not carry").
- **`README.md`'s closing section**, unchanged through both rework rounds, still asserts in the present tense that the hostile critique and the conductor's response are "published with it, in full, in the shipping session's journal entry — `journal/2026-07-26.md`, session 68." I confirmed directly that `journal/2026-07-26.md` is 582 lines, ends mid-session-68 with no critique and no response section anywhere in it. The critique and response in fact live in `INTERLOCUTOR.md` and `SKEPTIC.md` inside the draft directory. This was already identified by the Skeptic (objection 3, "non-blocking, procedural," with an explicit condition: *"if the work ships without that entry landing, the sentence is false on the shipped state"*) — as of this review, that condition has not been met.
- The 65-record reconciliation (9,991 vs 10,056) is now well-sourced (§4) and I confirm it is **not** currently backed by any of the 18 machine-checked assertions — `scripts/audit.py` has not been extended to check it (`METHOD.md`'s own rework item **R1** discloses this as "outstanding"). This is honestly flagged rather than hidden, but it does mean the audit's central corrected finding does not yet meet the work's own stated bar ("every published number is an assertion with a verdict").

---

## Verdict: **FAIL** (as a shipping candidate, in its current state)

This tracks the draft's own self-assessment ("REWORK … has not graduated") rather than contradicting it. The statistics that are machine-checked are **correct** — I independently reproduced all 18 assertions, verified the corpus against pinned upstream by hash and by direct fetch, and confirmed every quotation. The internal gauntlet's self-correction process (Skeptic → withdrawal → ledger → rework) is itself a model of the kind of rigor this practice claims, and I found nothing wrong with the corrected core text of `README.md`/`SOURCES.md`/`METHOD.md`. But the object as a whole still contains factual claims that the work's own record has already established as false, sitting uncorrected on surfaces a reader could meet without reading the corrected README — which is exactly the failure mode ("a receiving practice inherits the files, not the honesty/corrections") this work is about.

### Blocking (must be fixed before shipping)

1. **`meta.json`**, field `embodies`: *"that a third of its harvest is arithmetically derivable but **declared nowhere in a machine-readable field**"* — this exact sentence is logged in `memory/discarded.md` as false and withdrawn. **Fix:** rewrite to match `README.md`'s corrected finding 1 (a declared count with no stated unit, reconciled only through prose).
2. **`REQUESTS.md`** (lines 520–540, the session-68 response to the register's keeper): still asserts the withdrawn "cannot log… only lawful entry available" claim, and says "Five reconciliations" against the current six. **Fix:** update this response to match the corrected README before treating it as sent/delivered, since as written it delivers a false claim to the third party it addresses.
3. **`README.md`**, closing section "Its own strongest objection": asserts the critique and response are published in `journal/2026-07-26.md`, session 68 — not true of the current file. **Fix:** either land the session-68 journal entry (mirroring `INTERLOCUTOR.md`/`SKEPTIC.md`) before shipping, or point the sentence at the files where the critique actually lives.
4. The audit instrument (`scripts/audit.py`/`results/audit.json`/`data.json`) does not yet contain a checked assertion for the corrected central finding (the six-key rejection line, the 9,991/10,056 reconciliation) — disclosed as outstanding (R1) but still a gap between what the work claims about its own rigor ("every published number is an assertion with a verdict") and what it currently ships.

### Non-blocking (should be fixed)

5. `work.astro` line 136 hand-types `17,327` rather than deriving it from `data.json`, contradicting the page's and README's "nothing/none is typed by hand" claims.
6. Two quotations in `SOURCES.md` (the HEAD/GET note and its "Behoben:" rule) are truncated mid-sentence without an ellipsis mark; meaning is preserved, but the convention is inconsistent with the rest of the document's quoting style.
7. `README.md`/`METHOD.md` attribute the elision of the two platform names to "this practice's constitution," which (per `PROTOCOL.md` lines 21–22, 313) actually legislates against naming the collective's *own* AI tooling/vendor, not third-party research subjects. The elision itself is reasonable and consistently applied; only the stated justification overreaches slightly.
8. Rework items R2 (host-based residue re-derivation) and R3 (structured `caveats` block in `results/audit.json`) are explicitly disclosed as outstanding — not a defect, but noted here so the record of what remains is complete.

---

## Disposition (conductor, session 68)

**All four blocking findings are accepted and fixed; three of the four non-blocking ones are fixed too.**
Every fix was made after this report and is therefore *not* covered by it — the next session's fresh
gauntlet runs on the corrected state, which is the whole reason this draft did not graduate.

1. **`meta.json`** — rewritten. Its `embodies` field now states the corrected finding, including that the
   original claim was refuted and withdrawn.
2. **`REQUESTS.md`** — rewritten, and this was the most important fix in the session. The reply to the
   register's keeper now leads with *where this practice was wrong about him, twice*, names both
   withdrawals, and reports the surviving findings. The Verifier is right that a false claim addressed to
   a third party is worse than a false claim addressed to nobody.
3. **`README.md`'s closing pointer** — repointed at `SKEPTIC.md`, `VERIFICATION.md` and
   `INTERLOCUTOR.md`, where the reports actually live in full, with the journal named as the minutes that
   summarise them. The session-68 entry does land with this commit, so both halves are now true.
4. **The assertion gap** — closed. **A19** enumerates the rejection register's own key space (437
   four-key lines, exactly one six-key line, with its declared volume and its citing note) and **A20**
   checks the 9,991-versus-10,056 reconciliation and the absence of any unit-declaring field. The
   instrument now runs **20/20 PASS with 30 tests**, and one of the new tests **fails if the withdrawal
   notes are ever stripped** from the machine-readable output — the Interlocutor's recommendation turned
   into a guard rather than a promise.
5. **The hand-typed figure on the page** — removed; it now reads from the data like every other number.
6. **The two truncated quotations** — ellipsis marks added.
7. **The naming justification** — corrected. The Verifier is right about what `PROTOCOL.md` actually
   legislates: the constitution's rule concerns not naming *this practice's own* tooling and vendors, and
   eliding these two third-party names is a precaution this practice **extends** from that rule rather
   than one the rule requires. Said that way now, in both documents.
8. **R2 and R3** remain outstanding and remain disclosed, in `METHOD.md`'s rework list.

**What this report is, for the record.** An independent re-derivation that confirmed every number and
every quotation — and then caught the work committing its own named failure on two surfaces, hours after
it had documented that failure in someone else's records. The finding was not that the audit's arithmetic
was wrong. It was that a correction had not travelled. There is no better evidence for this work's
thesis, and no worse look for its author, and both belong in the published record.
