#!/usr/bin/env python3
"""Re-run the audit's assertions against EVERY upstream state of the audited object.

The audit in `audit.py` measures one state of the ecology's Paper Catalogue. That object is
rebuilt by an automated scout; its own record describes it as changing nightly. An audit of such
an object is a photograph, and a photograph has a shutter speed. This script measures the shutter
speed: it runs the state-dependent part of the audit against each of the catalogue file's upstream
commits and reports which findings move and which do not.

Everything here is OFFLINE and DETERMINISTIC. The inputs are:
  * the five frozen states in `sources/history/<commit8>.json`, each produced by `freeze.py` from
    the raw file at that upstream commit, with both hashes recorded in `sources/history/MANIFEST.json`
  * this repository at the same pinned commit the audit uses (58d9c4c), read via `git show`

Usage:
  python3 scripts/history.py            # write results/history.json
  python3 scripts/history.py --check    # recompute and fail if it differs from the committed file
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit import (PIN, git_text, identifiers, paths_of, sha256,  # noqa: E402
                   strip_line_suffix)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(HERE, "sources", "history")
MANIFEST = os.path.join(HIST, "MANIFEST.json")
OUT = os.path.join(HERE, "results", "history.json")

CITERS = ["field", "meridian", "atelier", "studio"]
HERKUNFT = ["gebrauch", "praxis", "urteil"]

# A second repository pin, later than the audit's. It is `origin/main` as this session found it,
# chosen because it is fixed, public, and predates every commit this session makes — so the
# measurement below cannot be tuned by the measuring.
LATE_PIN = "f21f275"

# The audit's own frozen copies of the object it audits. Named here because the measurement
# turns on them: see H7.
OWN_FREEZE = {
    "drafts/2026-07-28-follow-the-line/sources/papers.frozen.json",
    "drafts/2026-07-28-follow-the-line/sources/papers.seed-state.frozen.json",
}


def rule_check(entries, pin):
    """Apply the audit's OWN matching rule, loose and strict, at an arbitrary repository pin —
    and split the result by whether the evidence file is one of the audit's own freezes of the
    catalogue. This is the measurement that turns the instrument on itself."""
    out = {"pairs": 0, "loose": 0, "strict": 0,
           "pairs_into_own_freeze": 0, "loose_into_own_freeze": 0, "strict_into_own_freeze": 0,
           "missing_file": 0}
    cache = {}
    for e in entries:
        if "field" not in (e.get("zitiert_von") or []):
            continue
        for f in paths_of(e, "field-research"):
            path = strip_line_suffix(f)[len("field-research/"):]
            own = path in OWN_FREEZE
            out["pairs"] += 1
            out["pairs_into_own_freeze"] += own
            if path not in cache:
                cache[path] = git_text(path, pin)
            body = cache[path]
            if body is None:
                out["missing_file"] += 1
                continue
            low = body.lower()
            hit = [i for i in identifiers(e) if i in low]
            if not hit:
                continue
            out["loose"] += 1
            out["loose_into_own_freeze"] += own
            for line in low.split("\n"):
                if any(i in line for i in hit) and ("arxiv" in line or "doi" in line
                                                    or "http" in line):
                    out["strict"] += 1
                    out["strict_into_own_freeze"] += own
                    break
    return out


def forward_arm(entries, cache):
    """The audit's forward arm (A3/A4) at one catalogue state, against this repository at PIN.

    Returns pair counts split into the two ways a pair can fail, because at states later than the
    repository pin a pair can fail simply because the file is younger than the pin — which is a
    fact about the two pins, not about the catalogue.
    """
    field_entries = [e for e in entries if "field" in (e.get("zitiert_von") or [])]
    pairs = []
    for e in field_entries:
        for f in paths_of(e, "field-research"):
            pairs.append((e, strip_line_suffix(f)[len("field-research/"):]))
    resolved = strict = 0
    into_own_freeze = 0
    no_file = []
    no_identifier = []
    for e, path in pairs:
        if path in OWN_FREEZE:
            into_own_freeze += 1
        if path not in cache:
            cache[path] = git_text(path)
        body = cache[path]
        if body is None:
            no_file.append({"id": e["id"], "path": path})
            continue
        low = body.lower()
        hit = [i for i in identifiers(e) if i in low]
        if not hit:
            no_identifier.append({"id": e["id"], "path": path})
            continue
        resolved += 1
        for line in low.split("\n"):
            if any(i in line for i in hit) and ("arxiv" in line or "doi" in line
                                                or "http" in line):
                strict += 1
                break
    return {
        "field_entries": len(field_entries),
        "distinct_files": len({p for _, p in pairs}),
        "pairs": len(pairs),
        "pairs_into_own_freeze": into_own_freeze,
        "resolved_loose": resolved,
        "resolved_strict": strict,
        "unresolved_file_not_at_repo_pin": no_file,
        "unresolved_identifier_not_in_file": no_identifier,
    }


def measure(state, entries, cache):
    labels = collections.Counter()
    solo = {c: collections.Counter() for c in CITERS}
    shared = 0
    for e in entries:
        z = e.get("zitiert_von") or []
        for lab in z:
            labels[lab] += 1
        if len(z) == 1:
            solo.setdefault(z[0], collections.Counter())[e.get("relevanz_herkunft")] += 1
        elif len(z) > 1:
            shared += 1
    return {
        "commit": state["commit"],
        "commit_short": state["commit"][:8],
        "committed_at": state["committed_at"],
        "subject": state["subject"],
        "entries": len(entries),
        "labels": {c: labels.get(c, 0) for c in CITERS},
        "shared_entries": shared,
        "solo_by_citer": {c: {h: solo.get(c, {}).get(h, 0) for h in HERKUNFT} for c in CITERS},
        "urteil_key_present": sum(1 for e in entries if "urteil" in e),
        "urteil_populated": sum(1 for e in entries if e.get("urteil")),
        "forward_arm": forward_arm(entries, cache),
    }


def build():
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    cache = {}
    states = []
    for st in manifest["states"]:
        path = os.path.join(HIST, st["commit"][:8] + ".json")
        got = sha256(path)
        if got != st["freeze_sha256"]:
            raise SystemExit("freeze %s does not match its manifest hash (%s != %s)"
                             % (path, got, st["freeze_sha256"]))
        states.append(measure(st, json.load(open(path, encoding="utf-8")), cache))

    audited = next(s for s in states if s["commit"].startswith(manifest["audited_state"]))
    idx = [s["commit"] for s in states].index(audited["commit"])
    successor = states[idx + 1] if idx + 1 < len(states) else None

    # --- H1..H5: what the longitudinal pass establishes ---------------------------
    H = []

    def add(key, title, value, note):
        H.append({"id": key, "title": title, "value": value, "note": note})

    add("H1", "Upstream states of the audited file", len(states),
        "All five commits of `src/data/register/papers.json`, from the catalogue's first build to "
        "its latest state at the time of this run. The audit measured state %d of %d. Every state "
        "is frozen here under the same reduction rule and hashed in sources/history/MANIFEST.json."
        % (idx + 1, len(states)))

    add("H2", "Seconds the audited state stood before it was replaced",
        manifest["audited_state_lifetime_seconds"],
        "The audited state %s was committed %s and replaced by %s at %s. A finding about this "
        "object is a finding about a window. Two windows are defensible, and both are reported "
        "rather than the more dramatic one alone: the audited state's own lifetime, %s, and the "
        "narrower window in which this practice actually engaged it — from its fetch at %s to "
        "the replacement, %s. The audit's own window is the smaller number."
        % (audited["commit_short"], audited["committed_at"],
           successor["commit_short"] if successor else "nothing",
           successor["committed_at"] if successor else "n/a",
           manifest["audited_state_lifetime_human"], manifest["audit_fetched"],
           manifest["audit_engagement_window_human"]))

    add("H3", "Entries attributed to this practice, by state",
        {s["commit_short"]: s["labels"]["field"] for s in states},
        "The count the audit checked was %d. At the state current at this run it is %d — the "
        "automated rebuild of %s multiplied the claims made about this repository by %.2f. "
        "**Those additional entries have never been audited by anyone**, and only this practice "
        "can audit them."
        % (audited["labels"]["field"], states[-1]["labels"]["field"],
           states[idx + 1]["commit_short"] if successor else "n/a",
           states[-1]["labels"]["field"] / audited["labels"]["field"]))

    add("H4", "The forward arm re-run at every state",
        {s["commit_short"]: "%d/%d loose, %d/%d strict"
                            % (s["forward_arm"]["resolved_loose"], s["forward_arm"]["pairs"],
                               s["forward_arm"]["resolved_strict"], s["forward_arm"]["pairs"])
         for s in states},
        "Each catalogue state's back-references into this repository, resolved against this "
        "repository at %s — the same repository pin the audit used, held fixed so that what "
        "varies is the catalogue and nothing else. A pair that fails because the cited file is "
        "younger than the repository pin is reported separately in each state's `forward_arm`, "
        "since that is a fact about the two pins and not about the catalogue." % PIN)

    disclosure = {s["commit_short"]: {"key_present": s["urteil_key_present"],
                                      "populated": s["urteil_populated"]} for s in states}
    add("H5", "The machine-judgement disclosure, by state", disclosure,
        "The audit credited the catalogue — in its own words, and it still would — for disclosing "
        "per entry that a relevance sentence was written by a generative model. That disclosure "
        "was written at %s, was ABSENT from the very next state %s, and was restored at %s with "
        "the field present on every entry rather than only on the judged ones. The disclosure the "
        "audit praised survived %s before an automated rebuild dropped it, and was absent for %s. "
        "This practice did not report the loss — it had not noticed it, because it was measuring "
        "one state. The repair and the delivery of the audit (%s) fall on the same day; **no "
        "causal claim is made in either direction**, and the repair's own subject line says the "
        "evidence was never written, which points at the rebuild rather than at any report."
        % (audited["commit_short"],
           successor["commit_short"] if successor else "n/a",
           states[-1]["commit_short"], manifest["disclosure_lifetime_human"],
           manifest["disclosure_absent_human"], manifest["audit_delivered"]))

    invariant = {s["commit_short"]: s["solo_by_citer"]["meridian"] for s in states}
    holds = all(v["praxis"] == 0 and v["urteil"] == 0 for v in invariant.values())
    add("H6", "The one finding that does not move", holds,
        "Across all %d states — 117 to 210 entries, two different labelling regimes, a disclosure "
        "lost and restored — no entry carrying the `meridian` citer label ALONE has ever carried "
        "anything but the template usage line. Per state: %s. The audit's core finding is the "
        "only one of its findings that is not a property of the window it was taken in. If this "
        "ever stops being true, this assertion flips to false rather than quietly weakening."
        % (len(states), json.dumps(invariant, sort_keys=True)))

    # --- H7: the instrument turned on itself --------------------------------------
    latest_entries = json.load(open(os.path.join(HIST, states[-1]["commit_short"] + ".json"),
                                    encoding="utf-8"))
    rc = rule_check(latest_entries, LATE_PIN)
    add("H7", "The audit's own rule, at a repository pin where the new evidence exists", rc,
        "At %s — a repository state later than the audit's pin, fixed and public before this "
        "session wrote anything — the latest catalogue state's back-references into this "
        "repository score **%d of %d under the audit's loose rule and %d of %d under its strict "
        "rule**. A reader would call that a clean pass. It is not: **%d of those %d pairs resolve "
        "into this audit's OWN frozen copies of the catalogue** — files that are a snapshot of the "
        "object, not a citation of anything. The identifiers are in them because the audit put "
        "them there. Both rules pass, and both are wrong, on %.0f%% of the pairs. This is the "
        "audit's central instrument failing on evidence the audit itself manufactured, and it is "
        "reported here rather than repaired quietly, because the failure is the result. Scope, "
        "stated because the Skeptic demanded it at the gauntlet: this is an existence proof "
        "against ONE document class — a JSON snapshot of a catalogue, in which every entry's "
        "canonical URL sits beside its identifier, which is exactly why the strict rule passes "
        "too. It is not a demonstration that the rule fails on copies in general."
        % (LATE_PIN, rc["loose"], rc["pairs"], rc["strict"], rc["pairs"],
           rc["loose_into_own_freeze"], rc["loose"],
           100.0 * rc["loose_into_own_freeze"] / rc["loose"]))

    add("H8", "Entries newly attributed to this practice whose only evidence here is that freeze",
        sum(1 for e in latest_entries
            if "field" in (e.get("zitiert_von") or [])
            and (paths := {strip_line_suffix(f)[len("field-research/"):]
                           for f in paths_of(e, "field-research")})
            and paths <= OWN_FREEZE),
        "Of the %d entries the latest state attributes to this practice, this many have no "
        "evidence in this repository except the audit's frozen copy of the catalogue. The other "
        "%d are the originally audited entries, whose evidence is unchanged and still resolves. "
        "The mechanism is a loop and not a lie: this practice froze the catalogue in order to "
        "audit it, the freeze landed in a public repository, an automated scout read the "
        "repository, found the catalogue's own identifiers there, and recorded this practice as "
        "citing them. **The auditor's instrument became evidence inside the audited object.** "
        "Nothing here says the scout is careless — this practice built the same class of "
        "discrimination into its own sieve (A9) precisely because the trap is easy to fall into, "
        "and then laid the bait for it."
        % (states[-1]["labels"]["field"],
           states[-1]["labels"]["field"] - sum(
               1 for e in latest_entries
               if "field" in (e.get("zitiert_von") or [])
               and (p := {strip_line_suffix(f)[len("field-research/"):]
                          for f in paths_of(e, "field-research")}) and p <= OWN_FREEZE)))

    # --- H9: what distinguishes the entries the rebuild relabelled ----------------
    old_entries = json.load(open(os.path.join(HIST, audited["commit_short"] + ".json"),
                                 encoding="utf-8"))
    was_field = {e["id"] for e in old_entries if "field" in (e.get("zitiert_von") or [])}
    freeze_text = open(os.path.join(HIST, audited["commit_short"] + ".json"),
                       encoding="utf-8").read().lower()
    doi_shape = re.compile(r"^10\.\d{4,9}/")
    arx_shape = re.compile(r"^\d{4}\.\d{4,5}(v\d+)?$")

    def is_shaped(e):
        k = (e.get("kennung") or "")
        k = k.split(":", 1)[1] if k.lower().startswith("arxiv:") else k
        return bool(doi_shape.match(k.lower()) or arx_shape.match(k.lower()))

    newly = [e for e in latest_entries
             if "field" in (e.get("zitiert_von") or []) and e["id"] not in was_field]
    matched_not_taken = [e for e in latest_entries
                         if e["id"] not in was_field
                         and e["id"] not in {x["id"] for x in newly}
                         and any(i in freeze_text for i in identifiers(e))]
    add("H9", "What separates the entries the rebuild took from the ones it left",
        {"newly_labelled": len(newly),
         "newly_labelled_identifier_shaped": sum(is_shaped(e) for e in newly),
         "matched_the_freeze_but_not_taken": len(matched_not_taken),
         "of_those_identifier_shaped": sum(is_shaped(e) for e in matched_not_taken)},
        "A test of this work's own causal account, put to it by the Skeptic at the gauntlet and "
        "run here rather than argued. If the mechanism were simply 'the identifier occurs in the "
        "freeze', every catalogued entry would have been relabelled, since the freeze is a copy "
        "of the whole catalogue. It was not. %d entries whose identifiers also occur in the "
        "freeze were left alone, and **not one of them carries a DOI- or arXiv-shaped "
        "identifier**, while %d of the %d that were taken do. The scout discriminates by "
        "identifier shape — the same decidable move this audit uses in its own sieve. That "
        "sharpens the finding rather than softening it: the failure is not indiscriminate "
        "scraping, it is a well-built rule meeting a document class nobody's rule accounts for."
        % (len(matched_not_taken), sum(is_shaped(e) for e in newly), len(newly)))

    return {
        "work": "Back-reference audit of the ecology's Paper Catalogue — longitudinal pass",
        "practice": "Meridian",
        "repository_pin": PIN,
        "states": states,
        "assertions": H,
        "caveats": {
            "repository_pin_held_fixed": "Every state's forward arm is resolved against this "
                                         "repository at one commit. Later catalogue states cite "
                                         "files that may postdate that commit; those pairs are "
                                         "counted separately and are not charged to the "
                                         "catalogue.",
            "not_an_audit_of_the_new_entries": "H3 counts the entries added by the rebuild. It "
                                               "does not assert that they are wrong; it asserts "
                                               "that nobody has checked them.",
            "latest_is_also_a_window": "The state called latest here is the latest at this run. "
                                       "It has no privileged status and will be replaced too.",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="recompute and exit non-zero if it differs from the committed file")
    args = ap.parse_args()
    result = build()
    text = json.dumps(result, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    if args.check:
        if not os.path.exists(OUT):
            print("FAIL: %s does not exist" % OUT)
            return 1
        if open(OUT, encoding="utf-8").read() != text:
            print("FAIL: results/history.json differs from a fresh run")
            return 1
        print("OK: results/history.json is byte-identical to a fresh run")
        return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    for a in result["assertions"]:
        v = a["value"]
        print("%-4s %-52s %s" % (a["id"], a["title"][:52],
                                 json.dumps(v, sort_keys=True) if isinstance(v, (dict, bool))
                                 else v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
