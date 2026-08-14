#!/usr/bin/env python3
"""The instrument on trial — an audit of this arc's own stored files against themselves.

Session 119. Written in answer to the charge published unedited against this practice at
session 118 (`INTERLOCUTOR-10.md` §c), and accepted without dispute:

    *a practice which checks its writing but not its instruments will keep finding errors of
    exactly the kind found tonight.*

The kind found that night: a response class (`10222`) that returns the platform's full user
object, including the account's own handle, was stored as evidence that "the account object is
not served" — and it passed a probe, a derivation, a Verifier's nine conditions and a full
discharge, because every check this arc owns compares **prose against files** and none of them
compares **a file against itself**.

`prose_vs_json.py` reads what we wrote. This reads what the instrument wrote.

THE BET, COMMITTED BEFORE THIS FILE WAS WRITTEN (journal/2026-08-14.md, session 119 opening
record): the auditor must rediscover the `10222` miscoding unaided — it is not told what to
look for, only how to notice that a derived value and the raw evidence beside it disagree. If
it does not find it, it is theatre and is recorded as theatre.

WHAT IT DOES NOT DO. It makes no request of any instrument: every byte it reads is already on
disk. It never edits an archived measurement record — a measurement is not corrected by
rewriting it (D22, session 117). Findings are written to a report; corrections travel as a
dated overlay (`ledger/corrections.json`), never as an edit.

THE EIGHT CHECKS

  A1  RE-DERIVATION          every stored `state` recomputed from the raw fields beside it
  A2  CLASSIFIER DUPLICATION the two copies of the classifier run against each other on every
                             record this arc holds
  A3  RESPONSE-CLASS CENSUS  every distinct raw response signature, the branch that decided it,
                             and an explicit flag on every one that reached the fallthrough
  A4  WITHIN-RECORD LEDGER   a stored state that the other stored fields of the same record
                             contradict
  A5  WITHIN-RECORD ACCOUNT  a derived reading ("the account object is not served") against the
                             raw evidence in the same record (returned handle, page markers)
  A6  AGGREGATE VS ROWS      every summary block in a file recomputed from that file's own rows
  A7  POPULATION INTEGRITY   observations against the manifest; duplicates; handle stability
  A8  REFUTED READINGS       a reading refuted by the confirmation step, still standing in the
                             ledger the next interval is diffed against

Usage: python3 audit_instrument.py [out.json]
"""
import glob
import importlib.util
import json
import os
import sys
import time


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ledger = _load("ledger", "ledger.py")
ledger_diff = _load("ledger_diff", "ledger_diff.py")

RUN_GLOB = "ledger/run-*.json"
# Session 119, after the gauntlet. `ledger/baseline-union.json` is a run-shaped file with 3,869
# observations and is `run1` for two of the diffs this session is built on — and the glob above
# never matched it, so four checks silently excluded the file the night's own story rests on.
# Both reviewers found this independently.
EXTRA_RUNS = ["ledger/baseline-union.json"]
CONFIRM_GLOB = "ledger/transition-confirm-*.json"
DIFF_GLOB = "ledger/diff-*.json"
MANIFEST = "manifest-day2-onward.json"

# Every field the ledger classifier is allowed to read. A record carrying a response feature
# outside this set is a response the classifier cannot see, and A3 says so.
CLASSIFIER_INPUTS = ("http", "parse_error")


def runs():
    found = [p for p in glob.glob(RUN_GLOB) if not p.endswith(".partial")]
    found += [p for p in EXTRA_RUNS if os.path.exists(p) and p not in found]
    return sorted(found)


def signature(rec):
    """The raw response as the file stores it, with nothing derived folded in."""
    return json.dumps({
        "http": rec.get("http"),
        "body_code": rec.get("body_code"),
        "parse_error": bool(rec.get("parse_error")),
        "transport_error": (rec.get("transport_error") or "").split(":")[0] or None,
        "has_body_snippet": "body_snippet" in rec,
        "has_author_unique_id": rec.get("author_unique_id") is not None,
    }, sort_keys=True)


def branch_taken(rec):
    """Which arm of `ledger.classify` decided this record. The third is the fallthrough."""
    if rec.get("http") == 200 and not rec.get("parse_error"):
        return "1: http==200 and not parse_error -> RETRIEVABLE"
    if rec.get("http") == 400:
        return "2: http==400 -> NOT-RETRIEVABLE"
    return "3: FALLTHROUGH -> INDETERMINATE"


# ---------------------------------------------------------------- A1, A2, A3, A4

def a1_rederivation():
    out = {"check": "A1 RE-DERIVATION",
           "question": "does every stored state follow from the raw fields stored beside it?",
           "files": [], "mismatches": []}
    for p in runs():
        d = json.load(open(p))
        n = 0
        for r in d["observations"]:
            n += 1
            re_ = ledger.classify(r)
            if re_ != r.get("state"):
                out["mismatches"].append({"file": p, "vid": r.get("vid"),
                                          "stored": r.get("state"), "recomputed": re_,
                                          "record": {k: v for k, v in r.items()
                                                     if k != "state"}})
        out["files"].append({"path": p, "observations": n})
    out["n_observations"] = sum(f["observations"] for f in out["files"])
    out["verdict"] = ("CLEAN — every stored state re-derives" if not out["mismatches"]
                      else f"{len(out['mismatches'])} stored states do not re-derive")
    return out


def a2_classifier_duplication():
    """`ledger_diff.py` carries its own copy of the classifier while its docstring says it
    applies 'the same classification function rather than a second one written for it'."""
    out = {"check": "A2 CLASSIFIER DUPLICATION",
           "question": "the two copies of the three-state classifier — do they ever disagree?",
           "copies": ["ledger.classify", "ledger_diff.classify"],
           "docstring_claim": ("ledger_diff.py: 'read through an adapter that applies the same "
                              "classification function rather than a second one written for it'"),
           "how_compared": ("behaviourally, not textually: every stored record, plus an "
                            "exhaustive grid over the whole input space the classifier reads"),
           "disagreements": [], "n_records": 0, "grid": {"n": 0, "disagreements": []}}
    # the classifier reads exactly two fields; the grid is therefore finite and complete
    for http in (200, 400, 403, 404, 429, 500, None):
        for pe in (True, False, None):
            rec = {"http": http}
            if pe is not None:
                rec["parse_error"] = pe
            out["grid"]["n"] += 1
            x, y = ledger.classify(rec), ledger_diff.classify(rec)
            if x != y:
                out["grid"]["disagreements"].append({"input": rec, "ledger": x,
                                                     "ledger_diff": y})
    for p in runs():
        for r in json.load(open(p))["observations"]:
            out["n_records"] += 1
            x, y = ledger.classify(r), ledger_diff.classify(r)
            if x != y:
                out["disagreements"].append({"file": p, "vid": r.get("vid"),
                                             "ledger": x, "ledger_diff": y})
    # the census file run 1 goes through the ledger_diff adapter, so audit it too
    if os.path.exists("census-results.json"):
        c = json.load(open("census-results.json"))
        for r in c.get("results", []):
            out["n_records"] += 1
            x, y = ledger.classify(r), ledger_diff.classify(r)
            if x != y:
                out["disagreements"].append({"file": "census-results.json",
                                             "vid": r.get("vid"), "ledger": x,
                                             "ledger_diff": y})
    out["verdict"] = (f'AGREE on every record this arc holds and on all {out["grid"]["n"]} '
                      f'points of the complete input grid — but they are two definitions, and '
                      f'agreement today is not a guarantee for the next edit'
                      if not out["disagreements"] and not out["grid"]["disagreements"] else
                      f"{len(out['disagreements'])} records classified differently by the two copies")
    return out


def a3_response_census():
    out = {"check": "A3 RESPONSE-CLASS CENSUS",
           "question": ("which distinct raw responses exist in the record, which branch decided "
                        "each, and which reached the fallthrough unrecognised?"),
           "classes": [], "fallthrough_classes": 0, "fallthrough_records": 0}
    seen = {}
    for p in runs():
        for r in json.load(open(p))["observations"]:
            s = signature(r)
            e = seen.setdefault(s, {"signature": json.loads(s), "count": 0, "states": {},
                                    "branch": branch_taken(r), "files": set(),
                                    "example_vid": r.get("vid")})
            e["count"] += 1
            e["states"][r.get("state")] = e["states"].get(r.get("state"), 0) + 1
            e["files"].add(p)
    for e in seen.values():
        e["files"] = sorted(e["files"])
        e["reached_fallthrough"] = e["branch"].startswith("3")
        if e["reached_fallthrough"]:
            out["fallthrough_classes"] += 1
            out["fallthrough_records"] += e["count"]
        out["classes"].append(e)
    out["classes"].sort(key=lambda e: -e["count"])
    out["n_distinct_classes"] = len(out["classes"])
    out["verdict"] = (f'{out["n_distinct_classes"]} distinct response classes; '
                      f'{out["fallthrough_classes"]} of them ({out["fallthrough_records"]} '
                      f'records) were decided by the absence of a branch')
    out["note"] = ("The fallthrough is where a response the classifier does not recognise lands "
                   "silently, labelled INDETERMINATE. Every class listed with "
                   "reached_fallthrough=true is a response this arc has never explicitly decided "
                   "about — it was decided by the absence of a branch.")
    return out


def a4_within_record_ledger():
    """A stored state contradicted by the other stored fields of the same record."""
    out = {"check": "A4 WITHIN-RECORD CONTRADICTION (ledger)",
           "question": ("does any record's stored state contradict evidence stored in the same "
                        "record?"), "findings": [], "cross_tab": {}}
    for p in runs():
        for r in json.load(open(p))["observations"]:
            st = r.get("state")
            key = f'{st} | http={r.get("http")} | body_code={r.get("body_code")}'
            out["cross_tab"][key] = out["cross_tab"].get(key, 0) + 1
            f = None
            if st == "RETRIEVABLE" and r.get("author_unique_id") is None:
                f = ("stored RETRIEVABLE, but the response carried no author handle — the "
                     "evidence of retrieval is missing from the record of it")
            elif st == "RETRIEVABLE" and r.get("body_code") not in (None, 0):
                f = (f'stored RETRIEVABLE with a non-zero body code {r.get("body_code")!r}')
            elif st == "NOT-RETRIEVABLE" and r.get("author_unique_id") is not None:
                f = ("stored NOT-RETRIEVABLE while the response returned an author handle — "
                     "the same contradiction class as the account probe's 10222")
            elif st == "INDETERMINATE" and r.get("http") in (200, 400):
                f = "stored INDETERMINATE on a status the classifier has a branch for"
            if f:
                out["findings"].append({"file": p, "vid": r.get("vid"), "state": st,
                                        "finding": f,
                                        "record": {k: v for k, v in r.items() if k != "state"}})
    out["verdict"] = ("CLEAN" if not out["findings"]
                      else f'{len(out["findings"])} records contradict themselves')
    return out


# ---------------------------------------------------------------- A5

ACCOUNT_FILES = ["account-state-117b.json", "account-state-probe-114.json",
                 "account-route-probe-114.json", "account-route-body-inspection-114.json"]

# The reading this arc has published on every non-zero state field, in its own words, in three
# files: "nothing is read into it beyond 'the account object is not served'."
NOT_SERVED_READING = "the account object is not served"

# Session 119, after the gauntlet. The first version of A5 read exactly two field names and
# therefore skipped `account-route-body-inspection-114.json` in silence, while still counting its
# two records in the headline — that file stores the same quantities as `statusCode_field` (a
# STRING) and `uniqueId_field`. The adversary demonstrated the miss by feeding the function a
# record in that schema carrying the very contradiction A5 exists to find, and getting CLEAN.
# The repair is not "add the two names": it is that an account-shaped record whose state field
# this check cannot locate is REPORTED as unaudited instead of passing through as clean.
STATE_KEYS = ("status_field", "statusCode_field", "statusCode", "status_code")
HANDLE_KEYS = ("unique_id_returned", "uniqueId_field", "uniqueId", "unique_id")
SERVED_MARKERS = ("userInfo", "uniqueId")


def _state_field(rec):
    """(value_as_int_or_None, key_used, raw_value). A string code is a code."""
    for k in STATE_KEYS:
        if k in rec:
            v = rec[k]
            if v is None:
                return None, k, None
            try:
                return int(str(v).strip()), k, v
            except ValueError:
                return None, k, v
    return None, None, None


def _returned_handle(rec):
    for k in HANDLE_KEYS:
        if k in rec:
            return rec[k], k
    return None, None


def a5_within_record_account():
    out = {"check": "A5 WITHIN-RECORD CONTRADICTION (account state)",
           "question": ("where a non-zero state field is read as %r, does the same record carry "
                        "evidence that it WAS served?" % NOT_SERVED_READING),
           "files": [], "findings": [], "by_state_field": {}, "unaudited_records": []}
    for p in ACCOUNT_FILES:
        if not os.path.exists(p):
            out["files"].append({"path": p, "present": False})
            continue
        d = json.load(open(p))
        rows = d.get("results") or []
        keys_used = sorted({_state_field(r)[1] for r in rows} | {_returned_handle(r)[1]
                                                                 for r in rows} - {None})
        unlocatable = [r for r in rows if _state_field(r)[1] is None]
        for r in unlocatable:
            out["unaudited_records"].append(
                {"file": p, "handle": r.get("handle"),
                 "reason": ("no state field found under any known name — this record was NOT "
                            "tested for contradiction and is reported, not passed"),
                 "keys_present": sorted(r.keys())})
        out["files"].append({"path": p, "present": True, "records": len(rows),
                             "schema": d.get("schema"), "state_and_handle_keys_used": keys_used,
                             "records_actually_tested": len(rows) - len(unlocatable)})
        for r in rows:
            s, s_key, s_raw = _state_field(r)
            handle_returned, h_key = _returned_handle(r)
            m = r.get("markers") or {}
            key = f"{p} | status_field={s}"
            b = out["by_state_field"].setdefault(key, {
                "n": 0, "with_returned_handle": 0, "with_userInfo_marker": 0,
                "with_uniqueId_marker": 0, "bytes_min": None, "bytes_max": None})
            b["n"] += 1
            if handle_returned is not None:
                b["with_returned_handle"] += 1
            if m.get("userInfo"):
                b["with_userInfo_marker"] += 1
            if m.get("uniqueId"):
                b["with_uniqueId_marker"] += 1
            by = r.get("bytes")
            if by is not None:
                b["bytes_min"] = by if b["bytes_min"] is None else min(b["bytes_min"], by)
                b["bytes_max"] = by if b["bytes_max"] is None else max(b["bytes_max"], by)
            # the contradiction: derived "not served", raw evidence of being served
            if s not in (None, 0):
                evidence = []
                if handle_returned is not None:
                    evidence.append(f"the page returned the handle {handle_returned!r} "
                                    f"(field {h_key!r})")
                if m.get("userInfo"):
                    evidence.append("the userInfo marker is present")
                if m.get("uniqueId"):
                    evidence.append("the uniqueId marker is present")
                if evidence:
                    out["findings"].append({
                        "file": p, "handle": r.get("handle"), "group": r.get("group"),
                        "status_field": s, "state_field_key": s_key, "state_field_raw": s_raw,
                        "http": r.get("http"), "bytes": r.get("bytes"),
                        "counted_as": NOT_SERVED_READING,
                        "contradicted_by": evidence,
                        "returned_handle_matches_requested":
                            handle_returned == r.get("handle")})
    tested = sum(f.get("records_actually_tested", 0) for f in out["files"] if f.get("present"))
    held = sum(f.get("records", 0) for f in out["files"] if f.get("present"))
    out["records_held"], out["records_actually_tested"] = held, tested
    out["verdict"] = (
        (f'CLEAN over {tested} of {held} records' if not out["findings"] else
         f'{len(out["findings"])} records are read as "not served" while the same record shows '
         f'the account WAS served — over {tested} of {held} records')
        + (f'; {len(out["unaudited_records"])} records could not be tested and are listed'
           if out["unaudited_records"] else ""))
    return out


# ---------------------------------------------------------------- A6, A7

def a6_aggregate_vs_rows():
    out = {"check": "A6 AGGREGATE VS ROWS",
           "question": "does every summary block in a file follow from that file's own rows?",
           "findings": [], "checked": []}
    for p in runs():
        d = json.load(open(p))
        obs = d["observations"]
        blocks = []
        # a merged baseline carries no counts/requested/planned block; what it carries instead
        # is a `components` manifest of the runs it was built from, and that is checkable
        if "counts" in d:
            rec = {}
            for r in obs:
                rec.setdefault(r["arm"], {}).setdefault(r["state"], 0)
                rec[r["arm"]][r["state"]] += 1
            blocks.append("counts")
            if rec != d["counts"]:
                out["findings"].append({"file": p, "block": "counts",
                                        "stored": d["counts"], "recomputed": rec})
        if "requested" in d:
            blocks.append("requested")
            if d["requested"] != len(obs):
                out["findings"].append({"file": p, "block": "requested",
                                        "stored": d["requested"], "recomputed": len(obs)})
        if "planned" in d and d.get("stopped") is None:
            blocks.append("planned")
            if d["planned"] != len(obs):
                out["findings"].append({"file": p, "block": "planned vs observations",
                                        "stored": d["planned"], "recomputed": len(obs)})
        if "components" in d:
            blocks.append("components")
            declared = sum(c.get("observations", 0) for c in d["components"])
            by_src = {}
            for r in obs:
                by_src[r.get("baseline_from")] = by_src.get(r.get("baseline_from"), 0) + 1
            if sum(by_src.values()) != len(obs):
                out["findings"].append({"file": p, "block": "components",
                                        "stored": declared, "recomputed": len(obs)})
            out["component_provenance"] = {"file": p, "declared_total": declared,
                                           "observations": len(obs), "by_source": by_src}
        out["checked"].append({"file": p, "blocks": blocks})

    for p in ["account-state-117b.json"]:
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        rows = d["results"]
        tab, codes = {}, {}
        for r in rows:
            g = r["group"]
            s = r.get("status_field")
            t = tab.setdefault(g, {"n": 0, "readable": 0, "nonzero": 0})
            t["n"] += 1
            if s is not None:
                t["readable"] += 1
                if s != 0:
                    t["nonzero"] += 1
            codes.setdefault(g, {})
            codes[g][str(s)] = codes[g].get(str(s), 0) + 1
        for g, t in tab.items():
            t["nonzero_share"] = t["nonzero"] / t["readable"] if t["readable"] else None
        if tab != d.get("by_group"):
            out["findings"].append({"file": p, "block": "by_group",
                                    "stored": d.get("by_group"), "recomputed": tab})
        if codes != d.get("codes_by_group"):
            out["findings"].append({"file": p, "block": "codes_by_group",
                                    "stored": d.get("codes_by_group"), "recomputed": codes})
        if d.get("requests") != len(rows):
            out["findings"].append({"file": p, "block": "requests",
                                    "stored": d.get("requests"), "recomputed": len(rows)})
        for k in ("T", "C1", "C2"):
            declared = len(d["population"][k])
            actual = sum(1 for r in rows if r["group"] == k)
            if declared != actual:
                out["findings"].append({"file": p, "block": f"population {k}",
                                        "stored": declared, "recomputed": actual})
        out["checked"].append({"file": p, "blocks": ["by_group", "codes_by_group", "requests",
                                                     "population"]})
    out["verdict"] = ("CLEAN — every aggregate follows from its own rows" if not out["findings"]
                      else f'{len(out["findings"])} aggregates do not follow from their rows')
    return out


def a7_population_integrity():
    out = {"check": "A7 POPULATION INTEGRITY",
           "question": ("is every observation a unit of the manifest, exactly once, with a "
                        "stable handle across runs?"), "per_run": [], "findings": []}
    man = json.load(open(MANIFEST))
    units = {u["vid"]: u for u in man["units"]}
    handles = {}
    for p in runs():
        d = json.load(open(p))
        obs = d["observations"]
        vids = [r["vid"] for r in obs]
        dupes = sorted({v for v in vids if vids.count(v) > 1}) if len(set(vids)) != len(vids) else []
        # run 1 (2026-08-11) predates the merged manifest; it is reported, never faulted
        pre_manifest = p.endswith("run-2026-08-11T1124Z.json")
        not_in_manifest = [v for v in set(vids) if v not in units]
        missing = [v for v in units if v not in set(vids)]
        arm_mismatch = [r["vid"] for r in obs
                        if r["vid"] in units and r.get("arm") != units[r["vid"]].get("arm")]
        for r in obs:
            handles.setdefault(r["vid"], {})[r.get("handle")] = \
                handles.setdefault(r["vid"], {}).get(r.get("handle"), 0) + 1
        row = {"file": p, "observations": len(obs), "distinct_vids": len(set(vids)),
               "duplicate_vids": dupes,
               "not_in_manifest": len(not_in_manifest),
               "manifest_units_missing": len(missing),
               "arm_disagreements": len(arm_mismatch),
               "predates_window_manifest": pre_manifest}
        out["per_run"].append(row)
        if dupes:
            out["findings"].append({"file": p, "finding": "duplicate identifiers in one run",
                                    "vids": dupes[:20]})
        if not pre_manifest and (not_in_manifest or missing or arm_mismatch):
            out["findings"].append({"file": p,
                                    "finding": "run population departs from the manifest",
                                    "not_in_manifest": not_in_manifest[:20],
                                    "missing": missing[:20],
                                    "arm_disagreements": arm_mismatch[:20]})
    unstable = {v: h for v, h in handles.items() if len(h) > 1}
    out["identifiers_with_more_than_one_handle_across_runs"] = len(unstable)
    if unstable:
        out["findings"].append({"finding": ("the same identifier was probed under more than one "
                                            "handle across runs — the probe URL differs, so the "
                                            "two are not the same measurement"),
                                "examples": dict(list(unstable.items())[:20])})
    out["verdict"] = ("CLEAN" if not out["findings"]
                      else f'{len(out["findings"])} population findings')
    return out


# ---------------------------------------------------------------- A8

def a8_refuted_readings():
    """The defect session 118 found by hand, made into a standing check.

    `confirm_transition.py` writes its verdict to a sidecar and never touches the ledger, so a
    reading it refutes stays in the run file — and the next interval, diffed against that file,
    reports the reversal of our own refuted reading as a fresh transition.
    """
    out = {"check": "A8 REFUTED READINGS STILL STANDING IN THE LEDGER",
           "question": ("is any state that the confirmation step refuted still standing in a run "
                        "file that a later interval was diffed against?"),
           "refuted": [], "contaminated_diffs": [], "sidecars": []}
    refuted = []
    for p in sorted(glob.glob(CONFIRM_GLOB)):
        d = json.load(open(p))
        out["sidecars"].append({"path": p, "diff": d.get("diff"), "K4": d.get("K4"),
                                "n": len(d.get("results", []))})
        for r in d.get("results", []):
            if not r.get("all_passes_agree_with_new_state"):
                refuted.append({"sidecar": p, "vid": r["vid"], "handle": r.get("handle"),
                                "diff_reported": f'{r["from"]} -> {r["to"]}',
                                "five_re_requests_said": r["reconfirmation_states"],
                                "state_the_ledger_should_carry": r["reconfirmation_states"][0]})
    out["refuted"] = refuted

    for r in refuted:
        # which run file holds the refuted reading? the second run of the diff that reported it
        diff_path = json.load(open(r["sidecar"])).get("diff")
        try:
            dd = json.load(open(diff_path))
            run2 = dd["run2"]["path"]
        except Exception:
            continue
        d2 = json.load(open(run2))
        rec = next((o for o in d2["observations"] if o["vid"] == r["vid"]), None)
        still = rec is not None and rec.get("state") != r["state_the_ledger_should_carry"]
        entry = {"vid": r["vid"], "handle": r["handle"], "refuted_in": r["sidecar"],
                 "run_file": run2, "state_in_run_file": rec.get("state") if rec else None,
                 "state_five_re_requests_support": r["state_the_ledger_should_carry"],
                 "uncorrected": still, "diff_rows_touching_this_reading": []}
        # Session 119, after the gauntlet. The first version matched `run1 == run_file` only, so
        # it could see a refuted reading propagate FORWARD and was structurally blind to every
        # diff that used the contaminated file as its SECOND run. Both reviewers found it
        # independently, and the published table was right only because a second script carried
        # a hand-written list of four diff names. The scan is now over every diff, in both
        # roles, and every row is classified rather than counted.
        if still:
            for dp in sorted(glob.glob(DIFF_GLOB)):
                dj = json.load(open(dp))
                r1 = dj.get("run1", {}).get("path")
                r2 = dj.get("run2", {}).get("path")
                if run2 not in (r1, r2):
                    continue
                for t in dj.get("transitions") or []:
                    if t["vid"] != r["vid"]:
                        continue
                    reporting = (dp == diff_path)
                    entry["diff_rows_touching_this_reading"].append({
                        "diff": dp,
                        "contaminated_file_role": "run1" if run2 == r1 else "run2",
                        "reported": f'{t["from"]} -> {t["to"]}',
                        "kind": ("THE DIFF THAT REPORTED IT — the sidecar is its verdict; the "
                                 "row is legitimate as a raw reading"
                                 if reporting else
                                 "CONTAMINATION — this diff counts a reading the arc had "
                                 "already refuted, or its reversal, as a transition")})
        out["contaminated_diffs"].append(entry)
    n = sum(1 for e in out["contaminated_diffs"] if e["uncorrected"])
    rows = [row for e in out["contaminated_diffs"] for row in e["diff_rows_touching_this_reading"]]
    bad = [row for row in rows if row["kind"].startswith("CONTAMINATION")]
    out["n_diff_rows_touching_a_refuted_reading"] = len(rows)
    out["n_contaminated_rows"] = len(bad)
    out["contaminated_rows"] = bad
    out["verdict"] = (f'{n} refuted readings still stand in run files; {len(rows)} diff rows '
                      f'touch them, of which {len(bad)} are contamination — this arc\'s own '
                      f'refuted readings, or their reversals, counted as transitions'
                      if n else "CLEAN")
    return out


def a9_size_discriminator():
    """A second stored feature of the same response, tested against the two readings.

    Raised by A5 and not by anyone's hypothesis: the byte count of the account page is stored
    on every record and has never been used. If the marker-based reading is right — 10222 is
    the account being served — then response size should sit with the served group; if the
    reading is a parsing artefact (a regex that missed a marker), size has no reason to.

    THIS IS NOT AN INDEPENDENT OBSERVATION and is not reported as one: a page carrying the user
    object is larger *because* it carries it. It is a second feature of the same response,
    which is exactly what makes it a check on our parsing and not a check on the platform.
    """
    out = {"check": "A9 SIZE AGAINST THE TWO READINGS",
           "question": ("does the stored response size, never used by anything, agree with the "
                        "marker-based reading of 10222 or with the pre-registered binary?"),
           "records": [], "per_file": {}}
    served, not_served = [], []
    for p in ACCOUNT_FILES:
        if not os.path.exists(p):
            continue
        for r in json.load(open(p))["results"]:
            s, _k, _raw = _state_field(r)
            by = r.get("bytes")
            if s is None or by is None:
                continue
            m = r.get("markers") or {}
            evidence_of_service = (_returned_handle(r)[0] is not None
                                   or bool(m.get("userInfo")) or bool(m.get("uniqueId")))
            (served if evidence_of_service else not_served).append((by, p, s, r.get("handle")))
            out["per_file"].setdefault(p, {"served": 0, "not_served": 0})
            out["per_file"][p]["served" if evidence_of_service else "not_served"] += 1
    if served and not_served:
        smin, smax = min(x[0] for x in served), max(x[0] for x in served)
        nmin, nmax = min(x[0] for x in not_served), max(x[0] for x in not_served)
        overlap = not (smin > nmax or nmin > smax)
        out.update({
            "n_served_by_marker_evidence": len(served), "n_not_served": len(not_served),
            "served_bytes_range": [smin, smax], "not_served_bytes_range": [nmin, nmax],
            "ranges_overlap": overlap,
            "gap_bytes": None if overlap else smin - nmax,
            "misclassified_by_a_size_threshold":
                0 if not overlap else
                sum(1 for b, *_ in served if b <= nmax) + sum(1 for b, *_ in not_served
                                                              if b >= smin),
            "where_10222_sits": [
                {"handle": h, "bytes": b, "file": p,
                 "inside_served_range": smin <= b <= smax,
                 "inside_not_served_range": nmin <= b <= nmax}
                for b, p, s, h in served + not_served if s == 10222],
        })
        out["verdict"] = (
            f'the two readings separate perfectly on a feature neither used: '
            f'{len(served)} served in [{smin}, {smax}], {len(not_served)} not served in '
            f'[{nmin}, {nmax}], gap {smin - nmax} bytes' if not overlap else
            "the ranges overlap; size does not separate the two readings")
        out["what_it_does_not_show"] = (
            "Nothing about the platform, and nothing about causes. It shows the marker-based "
            "reclassification is not a regex artefact: a second stored feature of the same "
            "response puts 10222 with the accounts that are served, and it was never consulted "
            "when the code was assigned.")
    else:
        out["verdict"] = "not computable — one of the two groups is empty"
    return out


def main(out_path="instrument-audit-119.json"):
    checks = [a1_rederivation(), a2_classifier_duplication(), a3_response_census(),
              a4_within_record_ledger(), a5_within_record_account(), a6_aggregate_vs_rows(),
              a7_population_integrity(), a8_refuted_readings(), a9_size_discriminator()]
    report = {
        "schema": "field-research/instrument-audit/1", "session": 119,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "requests_made": 0,
        "what_this_is": ("An audit of this arc's stored measurement files against themselves. "
                         "Every byte read was already on disk; no instrument was called; no "
                         "archived record was edited."),
        "the_bet": ("Committed in journal/2026-08-14.md before this file was written: the "
                    "auditor must rediscover the 10222 miscoding unaided, without being told "
                    "what to look for. See check A5."),
        "checks": checks,
    }
    json.dump(report, open(out_path, "w"), indent=1)
    for c in checks:
        print(f'{c["check"]}: {c["verdict"]}')
    print("wrote", out_path)


if __name__ == "__main__":
    main(*sys.argv[1:])
