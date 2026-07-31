#!/usr/bin/env python3
"""Layer 1 / Layer 2 — the dated liveness probe over the locked Layer-0 inventory.

Governed by drafts/2026-07-31-fit-to-send/PREREGISTRATION.md, sections 3, 4 and 5. This is a
**dated record, not an assertion**: it reports the state of the archive's outbound identifiers
at the UTC timestamp it ran, and it expires on production. `results/inventory.json` (Layer 0)
is read but never modified.

Order of operations, enforced by this script's control flow (not just by convention):
  1. Five held-out controls (§5), none of them inside the probed corpus. Written to
     results/controls.json and results/CONTROLS.md before any census request is made.
  2. Pre-registered stop rule: if C1 and C3 do not both fire correctly, the script refuses to
     report census nulls, writes a refusal record, and exits non-zero.
  3. The census: one GET per unique normalised `evidence` identifier, tiers site+repo, from the
     locked inventory (minus the pre-fetch NOT-A-LOCATOR bucket, §Q1).
  4. Second, independent vantage for every NETFAIL / SERVER-ERROR.
  5. Layer 2: soft-gone pattern matching on every 2xx; token check on the structural bindings.

Usage:
    python3 scripts/probe.py
"""

from __future__ import annotations

import argparse
import hashlib
import html as html_module
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_PATH = Path(__file__).resolve()
DRAFT_ROOT = SCRIPT_PATH.parents[1]
RESULTS_DIR = DRAFT_ROOT / "results"
INVENTORY_JSON = RESULTS_DIR / "inventory.json"
CONTROLS_JSON = RESULTS_DIR / "controls.json"
CONTROLS_MD = RESULTS_DIR / "CONTROLS.md"
PROBE_JSON = RESULTS_DIR / "probe.json"
PROBE_MD = RESULTS_DIR / "PROBE.md"

# ---------------------------------------------------------------------------
# Network configuration
# ---------------------------------------------------------------------------

# This sandbox's outbound HTTPS goes through a policy-enforcing egress proxy that re-terminates
# TLS; this is that proxy's CA bundle. TLS verification stays ON throughout — this is what makes
# it possible to keep it on. If the bundle is absent (a different environment), fall back to the
# platform's default trust store rather than disabling verification.
_CA_BUNDLE_PATH = "/root/.ccr/ca-bundle.crt"
VERIFY = _CA_BUNDLE_PATH if os.path.exists(_CA_BUNDLE_PATH) else True

USER_AGENT = (
    "field-research-link-check/1.0 "
    "(automated citation liveness probe; single GET or HEAD per URL; research use)"
)

TIMEOUT_S = 25
MAX_REDIRECTS = 5
MIN_HOST_INTERVAL_S = 1.5

# §4 L2-a: pre-registered pattern list, matched against final URL and <title> on every 2xx.
SOFT_GONE_PATTERNS = [
    "deleted", "removed", "no longer available", "page not found",
    "not found", "expired", "error 404", "410",
]

# §5 C1: a host that appears in the census; a path on it that cannot exist.
C1_URL = "https://arxiv.org/abs/9999.99999-nonsense-fit-to-send-c1-check"
# §5 C3: given verbatim by the preregistration.
C3_URL = "https://www.kaggle.com/dsv/18354222"
# §5 C2: a frozen x-twitter URL from the coverage-not-custody sample (object-data, outside the
# probed corpus).
C2_URL = "https://x.com/9_tzav"
C2_SOURCE = "works/2026-07-20-coverage-not-custody/sample.json (x-twitter stratum, object-data)"
# §5 C4: constructed, well outside the corpus. example.com's body text is stable and public.
C4_URL = "https://example.com"
C4_REAL_TOKEN = "documentation examples without needing permission"
C4_ALTERED_TOKEN = "documentation examples without needing PERMISSION-DENIED-XYZ-ALTERED"

# ---------------------------------------------------------------------------
# Q1 — NOT-A-LOCATOR: assigned BEFORE any fetch, on the normalised URL string alone.
# ---------------------------------------------------------------------------

_PLACEHOLDER_SEGMENTS = {"path", "owner", "repo"}


def is_not_a_locator(normalized_url: str) -> bool:
    """A citation that was never fetchable, decided from the string alone, before any network
    call. Three literal triggers plus a bare placeholder path segment, per the conductor's
    ruling on Q1."""
    if "..." in normalized_url:
        return True
    lowered = normalized_url.lower()
    if "<" in normalized_url or "%3c" in lowered:
        return True
    segments = [s.strip().lower() for s in normalized_url.split("/")]
    if any(s in _PLACEHOLDER_SEGMENTS for s in segments):
        return True
    return False


# ---------------------------------------------------------------------------
# Q2 — self-referential URLs: this practice's own repository / own rendered site.
# `frankbueltge/dataset-hub` is a *different* repository under the same account, treated
# throughout the works as an external register this practice audits, not as its own work
# product — so it is deliberately NOT included here. See the report's "flag" section.
# ---------------------------------------------------------------------------

SELF_HOST = "frankbueltge.de"
SELF_URL_PREFIXES = (
    "https://github.com/frankbueltge/field-research",
    "https://api.github.com/repos/frankbueltge/field-research",
    "https://raw.githubusercontent.com/frankbueltge/field-research",
)


def is_self(normalized_url: str) -> bool:
    parsed = urlparse(normalized_url)
    if parsed.netloc.lower() == SELF_HOST:
        return True
    return normalized_url.startswith(SELF_URL_PREFIXES)


# ---------------------------------------------------------------------------
# Politeness
# ---------------------------------------------------------------------------

_last_request_at: dict[str, float] = {}


def polite_wait(host: str) -> None:
    now = time.monotonic()
    last = _last_request_at.get(host)
    if last is not None:
        gap = now - last
        if gap < MIN_HOST_INTERVAL_S:
            time.sleep(MIN_HOST_INTERVAL_S - gap)
    _last_request_at[host] = time.monotonic()


# ---------------------------------------------------------------------------
# One HTTP observation
# ---------------------------------------------------------------------------

_SESSION = requests.Session()
_SESSION.max_redirects = MAX_REDIRECTS

_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
# "410" alone, not as part of a longer digit run (avoids matching inside e.g. an arXiv id).
_SOFT_GONE_RE = re.compile(
    "|".join(
        re.escape(p) if p != "410" else r"(?<!\d)410(?!\d)"
        for p in SOFT_GONE_PATTERNS
    ),
    re.IGNORECASE,
)


def extract_title(text: str) -> str | None:
    m = _TITLE_RE.search(text)
    if not m:
        return None
    title = re.sub(r"\s+", " ", html_module.unescape(m.group(1))).strip()
    return title[:300] if title else None


def matches_soft_gone(final_url: str, title: str | None) -> bool:
    haystack = final_url + " " + (title or "")
    return bool(_SOFT_GONE_RE.search(haystack))


def do_request(url: str, method: str = "GET") -> dict:
    """One HTTP request through the shared session. Never raises for network-class failures —
    those come back as ok=False with an error_kind."""
    host = urlparse(url).netloc
    polite_wait(host)
    t0 = time.monotonic()
    try:
        resp = _SESSION.request(
            method, url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_S,
            allow_redirects=True,
            verify=VERIFY,
        )
        elapsed = time.monotonic() - t0
        body_text = ""
        byte_count = 0
        if method == "GET":
            byte_count = len(resp.content)
            try:
                body_text = resp.text
            except Exception:
                body_text = ""
        return {
            "ok": True,
            "error_kind": None,
            "error_message": None,
            "final_url": resp.url,
            "status": resp.status_code,
            "byte_count": byte_count,
            "content_type": resp.headers.get("Content-Type"),
            "title": extract_title(body_text) if body_text else None,
            "elapsed_s": round(elapsed, 3),
            "n_redirects": len(resp.history),
            "_body_text": body_text,  # not serialised; used only for the L2-b check
        }
    except requests.exceptions.Timeout as e:
        return _fail_observation("NETFAIL", "timeout", e, time.monotonic() - t0)
    except requests.exceptions.SSLError as e:
        return _fail_observation("NETFAIL", "tls", e, time.monotonic() - t0)
    except requests.exceptions.TooManyRedirects as e:
        return _fail_observation("NETFAIL", "too-many-redirects", e, time.monotonic() - t0)
    except requests.exceptions.ConnectionError as e:
        return _fail_observation("NETFAIL", "connection", e, time.monotonic() - t0)
    except requests.exceptions.RequestException as e:
        return _fail_observation("NETFAIL", "other", e, time.monotonic() - t0)


def _fail_observation(kind: str, subkind: str, exc: Exception, elapsed: float) -> dict:
    return {
        "ok": False,
        "error_kind": f"{kind}:{subkind}",
        "error_message": str(exc)[:500],
        "final_url": None,
        "status": None,
        "byte_count": None,
        "content_type": None,
        "title": None,
        "elapsed_s": round(elapsed, 3),
        "n_redirects": None,
        "_body_text": "",
    }


# ---------------------------------------------------------------------------
# Verdict classification (§3 table + §4 L2-a folded in + C5 downgrade)
# ---------------------------------------------------------------------------

def classify_verdict(obs: dict, soft_404_hosts: set[str], host: str) -> str:
    if not obs["ok"]:
        return "NETFAIL"
    status = obs["status"]
    if status is None:
        return "NETFAIL"
    if status in (403, 429):
        return "BLOCKED"
    if 500 <= status < 600:
        return "SERVER-ERROR"
    if 400 <= status < 500:
        return "GONE"
    if 200 <= status < 300:
        if matches_soft_gone(obs["final_url"] or "", obs["title"]):
            return "SOFT-GONE"
        if host in soft_404_hosts:
            return "UNRELIABLE-OK"
        return "OK"
    # 1xx or 3xx-with-no-further-redirect-resolved (shouldn't normally reach here since
    # requests follows redirects) — treat conservatively as NETFAIL rather than invent a verdict.
    return "NETFAIL"


# ---------------------------------------------------------------------------
# Controls (§5)
# ---------------------------------------------------------------------------

def run_controls(census_urls: list[str]) -> dict:
    hosts = sorted({urlparse(u).netloc for u in census_urls if urlparse(u).netloc})

    # C1 — true 404 on a host in the census.
    c1_obs = do_request(C1_URL, "GET")
    c1_verdict = classify_verdict(c1_obs, soft_404_hosts=set(), host=urlparse(C1_URL).netloc)
    c1_pass = c1_verdict == "GONE"

    # C2 — login/consent wall. Whatever it produces IS the finding.
    c2_obs = do_request(C2_URL, "GET")
    c2_verdict = classify_verdict(c2_obs, soft_404_hosts=set(), host=urlparse(C2_URL).netloc)

    # C3 — soft-404 returning 200.
    c3_obs = do_request(C3_URL, "GET")
    c3_verdict = classify_verdict(c3_obs, soft_404_hosts=set(), host=urlparse(C3_URL).netloc)
    c3_pass = c3_verdict == "SOFT-GONE"

    # C4 — Layer-2b mismatch AND match, both directions.
    c4_obs = do_request(C4_URL, "GET")
    body = c4_obs.get("_body_text") or ""
    c4_held_real = C4_REAL_TOKEN.lower() in body.lower()
    c4_held_altered = C4_ALTERED_TOKEN.lower() in body.lower()
    c4_real_result = "HELD" if c4_held_real else "NOT-HELD"
    c4_altered_result = "HELD" if c4_held_altered else "NOT-HELD"
    c4_pass = (c4_real_result == "HELD") and (c4_altered_result == "NOT-HELD")

    # C5 — per-host nonsense-path sweep, one request per distinct census host.
    c5_rows = []
    soft_404_hosts: set[str] = set()
    for host in hosts:
        nonsense_url = f"https://{host}/fit-to-send-nonsense-path-c5-check-9f31a7e2"
        obs = do_request(nonsense_url, "GET")
        verdict = classify_verdict(obs, soft_404_hosts=set(), host=host)
        is_soft_404_host = obs["ok"] and obs["status"] is not None and 200 <= obs["status"] < 300
        if is_soft_404_host:
            soft_404_hosts.add(host)
        c5_rows.append({
            "host": host,
            "probe_url": nonsense_url,
            "status": obs["status"],
            "verdict": verdict,
            "soft_404_host": is_soft_404_host,
        })

    controls = {
        "C1_true_404": {
            "description": "nonsense path on a host in the census; expect GONE",
            "url": C1_URL,
            "status": c1_obs["status"],
            "verdict": c1_verdict,
            "error": c1_obs["error_message"],
            "expected": "GONE",
            "fired_correctly": c1_pass,
        },
        "C2_consent_wall": {
            "description": (
                "a frozen x-twitter URL, object-data, outside the probed corpus — "
                "whatever this produces is itself the finding"
            ),
            "url": C2_URL,
            "source": C2_SOURCE,
            "status": c2_obs["status"],
            "final_url": c2_obs["final_url"],
            "title": c2_obs["title"],
            "verdict": c2_verdict,
            "error": c2_obs["error_message"],
            "note": (
                "OK: the wall (if any) is invisible to a plain GET at Layer 1"
                if c2_verdict == "OK" else
                "not OK: this particular wall was visible at Layer 1"
            ),
        },
        "C3_soft_404": {
            "description": "known 200-but-deleted page; expect SOFT-GONE",
            "url": C3_URL,
            "status": c3_obs["status"],
            "final_url": c3_obs["final_url"],
            "title": c3_obs["title"],
            "verdict": c3_verdict,
            "error": c3_obs["error_message"],
            "expected": "SOFT-GONE",
            "fired_correctly": c3_pass,
        },
        "C4_token_check": {
            "description": "one stable page, checked once with its real text and once altered",
            "url": C4_URL,
            "real_token": C4_REAL_TOKEN,
            "real_token_result": c4_real_result,
            "altered_token": C4_ALTERED_TOKEN,
            "altered_token_result": c4_altered_result,
            "expected": "HELD for the real token, NOT-HELD for the altered one",
            "fired_correctly": c4_pass,
        },
        "C5_per_host_soft_404_sweep": {
            "description": "one nonsense-path request per distinct host in the census",
            "n_hosts_swept": len(hosts),
            "soft_404_hosts": sorted(soft_404_hosts),
            "rows": c5_rows,
        },
    }
    stop_rule_pass = c1_pass and c3_pass
    controls["stop_rule"] = {
        "rule": "C1 and C3 must both fire correctly, or no census null is reportable",
        "c1_fired_correctly": c1_pass,
        "c3_fired_correctly": c3_pass,
        "pass": stop_rule_pass,
    }
    return controls


def write_controls_md(controls: dict, path: Path) -> None:
    lines = []
    lines.append("# Controls — run before the census (§5)")
    lines.append("")
    lines.append("None of the five controls below are inside the probed corpus.")
    lines.append("")

    c1 = controls["C1_true_404"]
    lines.append(f"- **C1 (true 404)** — `{c1['url']}` -> status {c1['status']}, verdict "
                  f"`{c1['verdict']}` (expected `GONE`). "
                  f"{'PASS' if c1['fired_correctly'] else 'FAIL'}.")

    c2 = controls["C2_consent_wall"]
    lines.append(f"- **C2 (consent/bot wall)** — `{c2['url']}` (source: {c2['source']}) -> "
                  f"status {c2['status']}, title {c2['title']!r}, verdict `{c2['verdict']}`. "
                  f"{c2['note']}")

    c3 = controls["C3_soft_404"]
    lines.append(f"- **C3 (soft-404-as-200)** — `{c3['url']}` -> status {c3['status']}, "
                  f"final URL `{c3['final_url']}`, title {c3['title']!r}, verdict "
                  f"`{c3['verdict']}` (expected `SOFT-GONE`). "
                  f"{'PASS' if c3['fired_correctly'] else 'FAIL'}.")

    c4 = controls["C4_token_check"]
    lines.append(f"- **C4 (Layer-2b token check)** — `{c4['url']}`: real token -> "
                  f"`{c4['real_token_result']}`; altered token -> `{c4['altered_token_result']}`. "
                  f"{'PASS' if c4['fired_correctly'] else 'FAIL'}.")

    c5 = controls["C5_per_host_soft_404_sweep"]
    lines.append(f"- **C5 (per-host soft-404 sweep)** — {c5['n_hosts_swept']} hosts swept; "
                  f"soft-404 hosts found: {c5['soft_404_hosts'] or '(none)'}.")
    lines.append("")

    sr = controls["stop_rule"]
    lines.append("## Stop rule")
    lines.append("")
    lines.append(f"C1 fired correctly: **{sr['c1_fired_correctly']}**. "
                  f"C3 fired correctly: **{sr['c3_fired_correctly']}**. "
                  f"Stop rule: **{'PASS — census may proceed' if sr['pass'] else 'FAIL — no census null is reportable'}**.")
    lines.append("")

    if c5["rows"]:
        lines.append("## C5 detail")
        lines.append("")
        lines.append("| host | probe status | verdict | soft-404 host? |")
        lines.append("|---|---|---|---|")
        for row in c5["rows"]:
            lines.append(f"| {row['host']} | {row['status']} | {row['verdict']} | "
                          f"{'yes' if row['soft_404_host'] else '' } |")
        lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Census
# ---------------------------------------------------------------------------

def load_evidence_urls(inventory: dict) -> list[dict]:
    """One row per unique normalised evidence URL (tiers site+repo), with the set of works and
    paths that cite it, and the U-classes it was seen as."""
    by_url: dict[str, dict] = {}
    for ident in inventory["identifiers"]:
        if ident["role"] != "evidence" or ident["tier"] not in ("site", "repo"):
            continue
        u = ident["normalized_url"]
        row = by_url.setdefault(u, {
            "normalized_url": u, "works": set(), "paths": set(), "classes": set(), "tiers": set(),
        })
        row["works"].add(ident["work"])
        row["paths"].add(ident["path"])
        row["classes"].add(ident["class"])
        row["tiers"].add(ident["tier"])
    rows = []
    for u, row in by_url.items():
        rows.append({
            "normalized_url": u,
            "works": sorted(row["works"]),
            "paths": sorted(row["paths"]),
            "classes": sorted(row["classes"]),
            "tiers": sorted(row["tiers"]),
        })
    rows.sort(key=lambda r: r["normalized_url"])
    return rows


def run_census(evidence_rows: list[dict], soft_404_hosts: set[str]) -> list[dict]:
    records = []
    for row in evidence_rows:
        u = row["normalized_url"]
        host = urlparse(u).netloc

        if is_not_a_locator(u):
            records.append({
                **{k: v for k, v in row.items()},
                "self": is_self(u),
                "not_a_locator": True,
                "verdict": "NOT-A-LOCATOR",
                "primary_observation": None,
                "second_vantage": None,
                "soft_gone_host_flag": host in soft_404_hosts,
            })
            continue

        obs = do_request(u, "GET")
        verdict = classify_verdict(obs, soft_404_hosts, host)

        second_vantage = None
        if verdict in ("NETFAIL", "SERVER-ERROR"):
            second_obs = do_request(u, "HEAD")
            second_verdict = classify_verdict(second_obs, soft_404_hosts, host)
            second_vantage = {
                "method": "HEAD",
                "status": second_obs["status"],
                "verdict": second_verdict,
                "error": second_obs["error_message"],
                "agrees_with_primary": second_verdict == verdict,
            }

        record = {
            **{k: v for k, v in row.items()},
            "self": is_self(u),
            "not_a_locator": False,
            "final_url": obs["final_url"],
            "status": obs["status"],
            "byte_count": obs["byte_count"],
            "content_type": obs["content_type"],
            "title": obs["title"],
            "elapsed_s": obs["elapsed_s"],
            "n_redirects": obs["n_redirects"],
            "error": obs["error_message"],
            "verdict": verdict,
            "second_vantage": second_vantage,
            "_body_text": obs.get("_body_text", ""),
        }
        records.append(record)
    return records


# ---------------------------------------------------------------------------
# Layer 2b — token check against the census results
# ---------------------------------------------------------------------------

_TEXTLIKE_CONTENT_TYPES = ("html", "text", "json", "xml")


def is_textlike(content_type: str | None) -> bool:
    if not content_type:
        return False
    ct = content_type.lower()
    return any(t in ct for t in _TEXTLIKE_CONTENT_TYPES)


def run_layer2b(inventory: dict, census_by_url: dict[str, dict]) -> list[dict]:
    results = []
    for binding in inventory["token_bindings"]:
        url = binding["url"]
        token = binding["token"]
        rec = census_by_url.get(url)
        entry = {
            "file": binding["file"],
            "json_path": binding["json_path"],
            "url": url,
            "token": token,
        }
        if rec is None:
            entry["result"] = "NOT-AUTOMATICALLY-CHECKABLE"
            entry["reason"] = "url not in census (unexpected)"
        elif rec.get("not_a_locator"):
            entry["result"] = "NOT-AUTOMATICALLY-CHECKABLE"
            entry["reason"] = "NOT-A-LOCATOR"
        elif not is_textlike(rec.get("content_type")):
            entry["result"] = "NOT-AUTOMATICALLY-CHECKABLE"
            entry["reason"] = f"content-type not text-like: {rec.get('content_type')}"
        else:
            body = rec.get("_body_text") or ""
            unescaped = html_module.unescape(body)
            collapsed = re.sub(r"\s+", " ", unescaped)
            token_collapsed = re.sub(r"\s+", " ", token).strip()
            held = (token in body) or (token_collapsed.lower() in collapsed.lower())
            entry["result"] = "HELD" if held else "NOT-HELD"
            entry["reason"] = None
        results.append(entry)
    results.sort(key=lambda r: (r["file"], r["json_path"], r["url"], r["token"]))
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def sha256_of_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()

    if not INVENTORY_JSON.exists():
        print(f"REFUSAL: {INVENTORY_JSON} does not exist — Layer 0 must be built and locked "
              f"before Layer 1 can run.", file=sys.stderr)
        sys.exit(1)

    inventory = json.loads(INVENTORY_JSON.read_text(encoding="utf-8"))
    inventory_sha256 = sha256_of_file(INVENTORY_JSON)

    evidence_rows = load_evidence_urls(inventory)
    census_urls = [r["normalized_url"] for r in evidence_rows]

    # 1) Controls, first, unconditionally.
    print(f"Running controls ({len(census_urls)} census hosts to sweep for C5)...")
    controls = run_controls(census_urls)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CONTROLS_JSON.write_text(json.dumps(controls, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_controls_md(controls, CONTROLS_MD)
    print(f"Wrote {CONTROLS_JSON}")
    print(f"Wrote {CONTROLS_MD}")

    stop_rule = controls["stop_rule"]
    if not stop_rule["pass"]:
        refusal = {
            "generated_utc": utc_now_iso(),
            "pinned_inventory_sha256": inventory_sha256,
            "stop_rule": stop_rule,
            "refusal": (
                "C1 and C3 did not both fire correctly. Per the pre-registered stop rule "
                "(PREREGISTRATION.md §5), no null from this probe is reportable. The census was "
                "NOT run. No per-URL results exist for this run."
            ),
        }
        PROBE_JSON.write_text(json.dumps(refusal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        PROBE_MD.write_text(
            "# Probe — REFUSED\n\n"
            "This is a dated record. It expires on production and is not an assertion about "
            "this repository.\n\n"
            f"Generated {refusal['generated_utc']}.\n\n"
            "**The pre-registered stop rule failed** (PREREGISTRATION.md §5): C1 and C3 did not "
            "both fire correctly. No census null is reportable. The census was not run.\n\n"
            f"- C1 fired correctly: {stop_rule['c1_fired_correctly']}\n"
            f"- C3 fired correctly: {stop_rule['c3_fired_correctly']}\n\n"
            "See results/controls.json and results/CONTROLS.md for the full control record.\n",
            encoding="utf-8",
        )
        print("STOP RULE FAILED — refusal written to results/probe.json and results/PROBE.md.",
              file=sys.stderr)
        sys.exit(1)

    print("Stop rule passed (C1 and C3 both fired correctly). Proceeding to census.")

    # 2) Census.
    soft_404_hosts = set(controls["C5_per_host_soft_404_sweep"]["soft_404_hosts"])
    print(f"Running census over {len(census_urls)} unique evidence URLs...")
    census_records = run_census(evidence_rows, soft_404_hosts)

    # 3) Layer 2b.
    census_by_url = {r["normalized_url"]: r for r in census_records}
    layer2b_results = run_layer2b(inventory, census_by_url)
    layer2b_by_url: dict[str, list[str]] = {}
    for r in layer2b_results:
        layer2b_by_url.setdefault(r["url"], []).append(r["result"])

    # Build the final, serialisable per-URL record (drop the internal-only body text).
    final_records = []
    for r in census_records:
        rec = {k: v for k, v in r.items() if k != "_body_text"}
        results_here = layer2b_by_url.get(r["normalized_url"])
        if results_here:
            if "HELD" in results_here and "NOT-HELD" not in results_here:
                rec["layer2b"] = "HELD"
            elif "NOT-HELD" in results_here:
                rec["layer2b"] = "NOT-HELD"
            else:
                rec["layer2b"] = "NOT-AUTOMATICALLY-CHECKABLE"
        else:
            rec["layer2b"] = "NOT-AUTOMATICALLY-CHECKABLE"
        final_records.append(rec)
    final_records.sort(key=lambda r: r["normalized_url"])

    probe = {
        "generated_utc": utc_now_iso(),
        "pinned_inventory_sha256": inventory_sha256,
        "pinned_commit": inventory["pinned_commit"],
        "controls": controls,
        "records": final_records,
        "layer2b_bindings": layer2b_results,
    }
    PROBE_JSON.write_text(json.dumps(probe, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {PROBE_JSON}")

    write_probe_md(probe, inventory, PROBE_MD)
    print(f"Wrote {PROBE_MD}")


def write_probe_md(probe: dict, inventory: dict, path: Path) -> None:
    records = probe["records"]
    works = inventory["works"]

    lines = []
    lines.append("# Probe — the state of the archive's outbound identifiers")
    lines.append("")
    lines.append(
        "**This is a dated record, not an assertion about this repository.** It expires on "
        "production; a later state of the web makes it stale, and it may not be cited as a "
        "standing property of any work without a re-run."
    )
    lines.append("")
    lines.append(f"Generated **{probe['generated_utc']}**. "
                  f"Pinned inventory: `{probe['pinned_inventory_sha256']}` "
                  f"(commit `{probe['pinned_commit']}`).")
    lines.append("")

    # Per-work verdict counts.
    by_work_verdict: dict[tuple, int] = {}
    for r in records:
        for w in r["works"]:
            key = (w, r["verdict"])
            by_work_verdict[key] = by_work_verdict.get(key, 0) + 1

    all_verdicts = sorted({r["verdict"] for r in records})
    lines.append("## Per-work verdict counts")
    lines.append("")
    header = "| work | " + " | ".join(all_verdicts) + " |"
    sep = "|---|" + "---|" * len(all_verdicts)
    lines.append(header)
    lines.append(sep)
    for w in works:
        cells = [str(by_work_verdict.get((w, v), 0)) for v in all_verdicts]
        lines.append(f"| {w} | " + " | ".join(cells) + " |")
    lines.append("")

    lines.append("## Per work: everything that is not OK")
    lines.append("")
    for w in works:
        not_ok = [r for r in records if w in r["works"] and r["verdict"] != "OK"]
        lines.append(f"### {w}")
        if not not_ok:
            lines.append("")
            lines.append("(nothing — every probed evidence identifier for this work came back OK)")
            lines.append("")
            continue
        lines.append("")
        for r in not_ok:
            self_tag = " `[self]`" if r["self"] else ""
            lines.append(f"- `{r['verdict']}`{self_tag} — {r['normalized_url']} "
                         f"(status {r.get('status')}, {r.get('paths')})")
        lines.append("")

    self_rows = [r for r in records if r["self"]]
    lines.append("## Self-referential URLs (this practice's own repository / site)")
    lines.append("")
    if self_rows:
        lines.append("| url | verdict | status | works |")
        lines.append("|---|---|---|---|")
        for r in self_rows:
            lines.append(f"| {r['normalized_url']} | {r['verdict']} | {r.get('status')} | "
                          f"{', '.join(r['works'])} |")
    else:
        lines.append("(none)")
    lines.append("")

    nal_rows = [r for r in records if r["verdict"] == "NOT-A-LOCATOR"]
    lines.append("## NOT-A-LOCATOR (assigned before any fetch — never fetchable by construction)")
    lines.append("")
    if nal_rows:
        lines.append("| url | works | paths |")
        lines.append("|---|---|---|")
        for r in nal_rows:
            lines.append(f"| {r['normalized_url']} | {', '.join(r['works'])} | "
                          f"{', '.join(r['paths'])} |")
    else:
        lines.append("(none)")
    lines.append("")

    # Layer 2 summary.
    n_total = len(records)
    n_l2b_checkable = sum(1 for r in records if r["layer2b"] in ("HELD", "NOT-HELD"))
    n_l2b_not_checkable = n_total - n_l2b_checkable
    lines.append("## Layer 2 — custody")
    lines.append("")
    lines.append(f"Of {n_total} evidence identifiers in the census, **{n_l2b_checkable}** carry "
                 f"a structural token binding (Layer 2b) and **{n_l2b_not_checkable}** are "
                 f"`NOT-AUTOMATICALLY-CHECKABLE`.")
    if n_l2b_not_checkable > n_total * 0.5:
        lines.append("")
        lines.append(f"**The custody layer is thin**: {n_l2b_not_checkable} of {n_total} "
                     f"evidence identifiers have no mechanical way to verify that the page "
                     f"still holds the claim the work rests on it.")
    lines.append("")
    lines.append("| url | layer2b result |")
    lines.append("|---|---|")
    for r in records:
        if r["layer2b"] in ("HELD", "NOT-HELD"):
            lines.append(f"| {r['normalized_url']} | {r['layer2b']} |")
    lines.append("")

    # Second-vantage disagreements.
    disagreements = [r for r in records if r.get("second_vantage") and
                      not r["second_vantage"]["agrees_with_primary"]]
    lines.append("## Second-vantage disagreements (NETFAIL / SERVER-ERROR re-checked)")
    lines.append("")
    n_second = sum(1 for r in records if r.get("second_vantage"))
    lines.append(f"{n_second} identifiers triggered a second-vantage re-check "
                 f"(primary verdict NETFAIL or SERVER-ERROR).")
    if disagreements:
        lines.append("")
        lines.append("| url | primary verdict | second-vantage verdict |")
        lines.append("|---|---|---|")
        for r in disagreements:
            lines.append(f"| {r['normalized_url']} | {r['verdict']} | "
                         f"{r['second_vantage']['verdict']} |")
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
