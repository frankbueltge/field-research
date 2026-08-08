"""Probe B-2 — reading the table Probe B counted. UNREGISTERED, like Probe B.

The Interlocutor's charge, verbatim from INTERLOCUTOR-2.md: "Reporting the row counts of a table you
haven't read is not evidence, it's inventory." It is correct, and this answers it with a measurement
rather than a paragraph.

Sample: 12 documents drawn from Probe B's own 80 with the same seed, and from each the 5 most recent
change notes (fewer if the document has fewer). Every sampled note is written out verbatim in
notes-read.json so a reader can re-judge every call made here.

Classification rule, fixed before the notes were read:
  SUBSTANTIVE   - the note names a change to the information itself (new/removed/revised content,
                  new data, changed figures, new designations, new guidance).
  PRESENTATIONAL- the note names only format, accessibility, file attachments, links, translation,
                  contact details or metadata.
  UNDECIDABLE   - the note text alone does not say which.
The classification is applied by hand, by the session, to the PUBLISHER'S DESCRIPTION of the change
-- not to the change. A publisher who writes a vague note gets UNDECIDABLE, which is a fact about
the note, not about the edit.
"""
import json, random, time
import urllib.request

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
UA = "field-research/1.0 (non-commercial research; polite, rate-limited)"
SEED, NDOCS, NNOTES = 20260808, 12, 5


def get(u, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    raise last


probe = json.load(open(f"{BASE}/publisher-history-probe.json"))
docs = [r["url"] for r in probe["records"] if r.get("ok") and r.get("n_change_notes", 0) > 0]
picked = sorted(random.Random(SEED).sample(sorted(docs), min(NDOCS, len(docs))))

out = []
for i, u in enumerate(picked, 1):
    path = u.replace("https://www.gov.uk", "")
    j = json.loads(get("https://www.gov.uk/api/content" + path))
    ch = (j.get("details") or {}).get("change_history") or []
    for n in ch[:NNOTES]:
        out.append({"url": u, "public_timestamp": n.get("public_timestamp"),
                    "note": (n.get("note") or "").strip()})
    print(f"[{i}/{len(picked)}] {len(ch[:NNOTES])} notes  {u}", flush=True)
    time.sleep(0.6)

json.dump({"documents": picked, "notes": out}, open(f"{BASE}/notes-read.json", "w"), indent=1)
print(f"\n{len(out)} notes from {len(picked)} documents\n")
for n in out:
    print(f"- [{n['public_timestamp'][:10]}] {n['url'].split('/')[-1][:44]:44s} | {n['note'][:150]}")
