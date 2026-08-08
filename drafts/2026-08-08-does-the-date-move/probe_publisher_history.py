"""UNREGISTERED EXPLORATORY PROBE — not part of PREREGISTRATION-2.md and not scored against it.

Question: if the public capture record cannot see document pages densely enough to compare a page
against itself, is there a route to the same question that does not go through an archive at all?

One authority in the census sample publishes a machine-readable change history per document
(GOV.UK's content API, https://www.gov.uk/api/content/<path>): `first_published_at`,
`public_updated_at`, and `details.change_history` — a list of publisher-authored notes, each with a
`public_timestamp`. This probe measures only whether that route exists and how deep it goes, on the
same sample of documents the census measured. It fetches no archive and makes no fidelity claim.

Sample: recomputed from frames.json with the pre-registration's own seed and rule, so it is exactly
the census sample — no second draw.
"""
import json, random, time, statistics as st
import urllib.request

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
UA = "field-research/1.0 (non-commercial research; polite, rate-limited)"
SEED, SAMPLE = 20260808, 80


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


frames = json.load(open(f"{BASE}/frames.json"))
frame = sorted(set(frames["govuk"]))
urls = sorted(random.Random(SEED).sample(frame, SAMPLE)) if len(frame) > SAMPLE else frame

out = []
for i, u in enumerate(urls, 1):
    path = u.replace("https://www.gov.uk", "")
    rec = {"url": u}
    try:
        j = json.loads(get("https://www.gov.uk/api/content" + path))
        ch = (j.get("details") or {}).get("change_history") or []
        rec.update({
            "ok": True,
            "first_published_at": j.get("first_published_at"),
            "public_updated_at": j.get("public_updated_at"),
            "updated_at": j.get("updated_at"),
            "n_change_notes": len(ch),
            "newest_note_ts": ch[0].get("public_timestamp") if ch else None,
            "oldest_note_ts": ch[-1].get("public_timestamp") if ch else None,
            "document_type": j.get("document_type"),
        })
    except Exception as e:  # noqa: BLE001
        rec.update({"ok": False, "error": f"{type(e).__name__}: {e}"})
    out.append(rec)
    print(f"[{i}/{len(urls)}] notes={rec.get('n_change_notes')} {u}", flush=True)
    time.sleep(0.6)

ok = [r for r in out if r.get("ok")]
have = [r for r in ok if r["n_change_notes"] > 0]
summary = {
    "sampled": len(out), "fetched": len(ok), "errors": len(out) - len(ok),
    "with_change_history": len(have),
    "with_change_history_pct": round(100.0 * len(have) / len(ok), 1) if ok else None,
    "notes_median": st.median([r["n_change_notes"] for r in have]) if have else None,
    "notes_max": max([r["n_change_notes"] for r in have]) if have else None,
    "notes_total": sum(r["n_change_notes"] for r in have),
    "with_public_updated_at": sum(1 for r in ok if r.get("public_updated_at")),
}
json.dump({"summary": summary, "records": out},
          open(f"{BASE}/publisher-history-probe.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
