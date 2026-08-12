#!/usr/bin/env python3
"""presence_check - measure whether named videos are publicly retrievable, on a named day.

Session 113, 2026-08-12. This is the portable half of the instrument: the part that can be
pointed at a list of identifiers this house did not choose, from a vantage this house does
not control, by someone who has no credential and no account.

    python3 presence_check.py LISTFILE [-o OUT.json] [--baseline presence-baseline.json]

LISTFILE holds one item per line; blank lines and lines starting with '#' are ignored.
Each item may be

    https://www.tiktok.com/@someuser/video/7123456789012345678
    7123456789012345678
    7123456789012345678,someuser

The handle is optional: session 109 established that the endpoint ignores the URL handle
entirely, so a bare identifier is measured the same as a full URL. That was tested, not
assumed, and an adversary reproduced it independently (REFUTATION-REPRODUCED.md).

WHAT A RESULT MEANS, and this is the sentence most easily lost:

    RETRIEVABLE      the endpoint returned a usable public record for this identifier,
                     from this vantage, at this moment.
    NOT-RETRIEVABLE  the endpoint refused. The refusal is a single opaque HTTP 400 and is
                     SEMANTICALLY EMPTY: session 109's three-arm control with twenty
                     synthetic identifiers showed that a video which never existed returns
                     exactly the same code, and that no 404 is ever returned. It therefore
                     means "not publicly retrievable from here, now". IT DOES NOT MEAN
                     DELETED, removed, banned, or private, and this tool will not say so.
    INDETERMINATE    a transport failure or an unexpected status. Not evidence either way.

The probe is imported from ledger.py rather than re-implemented, so a list measured with
this tool is measured by the same instrument, at the same rate, with the same classifier as
every row of this practice's own ledger.

Offered under the conditions in memory/downstream-commitments.md. Those are conditions this
practice asks a reuser to honour, not obligations imposed on anybody.
"""

import argparse
import calendar
import json
import re
import sys
import time

import ledger

YEAR_S = 365.25 * 86400.0
ID_RE = re.compile(r"(\d{6,25})")
AGE_BANDS = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 99)]


def band_label(lo, hi):
    return f"{lo}-{hi}y" if hi < 99 else f"{lo}y+"


def band_of(age_y):
    for lo, hi in AGE_BANDS:
        if lo <= age_y < hi:
            return band_label(lo, hi)
    return None


def parse_line(line):
    """Return (vid, handle) or (None, None). Accepts a URL, a bare id, or 'id,handle'."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None, None
    handle = None
    m = re.search(r"@([A-Za-z0-9._-]+)", line)
    if m:
        handle = m.group(1)
    if "," in line and not line.startswith("http"):
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 2 and parts[1]:
            handle = parts[1].lstrip("@")
        line = parts[0]
    m = re.search(r"/video/(\d+)", line) or ID_RE.search(line)
    if not m:
        return None, None
    return m.group(1), (handle or "x")


def dated(vid, t_ref):
    """This arc's dating rule, WITH its measured breakpoint honoured.

    id >> 32 is unix seconds ONLY inside the platform's modern 19-digit scheme. Session 110
    measured the rule breaking outside it (194951213564514304 is live and decodes to 1971),
    so anything that is not 19 digits is returned undatable rather than silently dated.
    """
    if len(vid) != 19:
        return None, None, "not-19-digit: dating rule does not hold outside the modern scheme"
    created = int(vid) >> 32
    age_s = t_ref - created
    if age_s <= 0:
        return created, None, "creation timestamp is not before the reference time"
    return created, age_s / YEAR_S, None


def load_baseline(path):
    try:
        b = json.load(open(path))
    except Exception as e:
        return None, f"baseline not loaded ({type(e).__name__}); expectation omitted"
    if b.get("schema") != "field-research/public-presence-null/1":
        return None, "baseline has an unexpected schema; expectation omitted"
    return b, None


def expectation(rows, baseline):
    """What public absence would be EXPECTED for a list with this age profile.

    This is the transfer function of presence-baseline.json applied to the caller's OWN age
    histogram. It is a comparison against ONE reference population - videos cited in an
    encyclopedia and posted to one technology forum, measured from one vantage on one day.
    A list drawn from somewhere else may legitimately sit far outside it, and doing so is
    NOT by itself evidence of anything. This number is a yardstick, not a verdict.
    """
    if not baseline:
        return None
    table = baseline["by_age_band"]
    hist = {}
    for r in rows:
        if r.get("band"):
            hist[r["band"]] = hist.get(r["band"], 0) + 1
    if not hist:
        return None
    tot = sum(hist.values())
    point = lo = hi = 0.0
    for b, w in hist.items():
        c = table.get(b)
        if not c or not c["n"]:
            continue
        point += (w / tot) * c["absent_rate"]
        lo += (w / tot) * c["absent_ci"][0]
        hi += (w / tot) * c["absent_ci"][1]
    return {"age_histogram": hist, "n_dated": tot,
            "expected_absent_rate": point, "expected_lo": lo, "expected_hi": hi,
            "reference_population": {
                "source": baseline["source_run"]["file"],
                "run_id": baseline["source_run"]["run_id"],
                "n": baseline["pooled"]["n"],
                "what_it_is": ("videos cited across 21+ MediaWiki language editions and "
                               "posted to one public technology forum, measured from "
                               f"{baseline['source_run']['vantage_asn']} on one day"),
            }}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("listfile")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--baseline", default="presence-baseline.json")
    ap.add_argument("--label", default=None, help="a name for this list, recorded as given")
    a = ap.parse_args(argv)

    items, bad = [], []
    for raw in open(a.listfile, encoding="utf-8"):
        vid, handle = parse_line(raw)
        if vid:
            items.append((vid, handle))
        elif raw.strip() and not raw.strip().startswith("#"):
            bad.append(raw.strip()[:80])
    if not items:
        print("no identifiers found in", a.listfile, file=sys.stderr)
        return 2

    # The vantage is read BEFORE the first measurement request, never after. Every figure
    # this instrument produces is conditional on where it was standing.
    van = ledger.vantage()
    t0 = time.time()
    t_ref = calendar.timegm(time.gmtime(t0))
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0))

    rows = []
    for i, (vid, handle) in enumerate(items):
        rec = ledger.probe_one(vid, handle)
        rec["vid"] = vid
        rec["handle_sent"] = handle
        rec["state"] = ledger.classify(rec)
        created, age_y, why = dated(vid, t_ref)
        rec["created_utc"] = (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(created))
                              if created else None)
        rec["age_y"] = age_y
        rec["band"] = band_of(age_y) if age_y is not None else None
        if why:
            rec["dating_note"] = why
        rows.append(rec)
        if i + 1 < len(items):
            time.sleep(ledger.DELAY)

    counts = {}
    for r in rows:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    det = counts.get("RETRIEVABLE", 0) + counts.get("NOT-RETRIEVABLE", 0)

    baseline, bwhy = load_baseline(a.baseline)
    exp = expectation(rows, baseline)

    out = {
        "schema": "field-research/presence-check/1",
        "tool": "presence_check.py",
        "list": {"file": a.listfile, "label": a.label,
                 "n_items": len(items), "unparsed_lines": bad},
        "started_utc": started,
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "seconds": round(time.time() - t0, 1),
        "vantage": van,
        "probe": {"endpoint": ledger.ENDPOINT, "user_agent": ledger.UA,
                  "delay_s": ledger.DELAY, "timeout_s": ledger.TIMEOUT,
                  "imported_from": "ledger.py (not re-implemented)"},
        "counts": counts,
        "determinate": det,
        "public_absence_rate": (counts.get("NOT-RETRIEVABLE", 0) / det) if det else None,
        "expectation_for_this_age_profile": exp,
        "baseline_note": bwhy,
        "what_not_retrievable_means": (
            "not publicly retrievable from this vantage at this time. The endpoint's refusal "
            "is a single opaque HTTP 400 that a never-existing identifier also returns "
            "(session 109 three-arm control, 20 synthetic identifiers). NOT DELETED."),
        "observations": rows,
    }

    dest = a.out or f"presence-check-{time.strftime('%Y-%m-%dT%H%MZ', time.gmtime(t0))}.json"
    json.dump(out, open(dest, "w"), indent=1)

    print(f"{a.label or a.listfile}: {len(items)} identifiers, {out['seconds']} s, "
          f"vantage {van['asn']} ({van['country']})")
    for r in rows:
        age = f"{r['age_y']:.2f}y" if r["age_y"] is not None else "undated"
        print(f"  {r['vid']}  {r['state']:<16} http={str(r.get('http')):<5} {age}")
    print(f"counts {counts}")
    if out["public_absence_rate"] is not None:
        print(f"observed public absence {out['public_absence_rate']:.4f} "
              f"({counts.get('NOT-RETRIEVABLE',0)}/{det})")
    if exp:
        print(f"expected for this age profile {exp['expected_absent_rate']:.4f} "
              f"[{exp['expected_lo']:.4f}, {exp['expected_hi']:.4f}] "
              f"— a yardstick from a different population, not a verdict")
    print("written", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
