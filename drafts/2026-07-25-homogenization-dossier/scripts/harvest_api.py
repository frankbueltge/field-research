"""
scripts/harvest_api.py — the archive's query-API harvester, per PREREGISTRATION.md §10
deviation D1 (OAI-PMH's sustained throughput made the locked §2 route infeasible within
a session; the query API replaces it, same archive, same metadata corpus, same courtesy
pacing, every epistemic parameter unchanged). Stdlib only (http.client, gzip, json,
time, hashlib, xml.etree).

Endpoint: https://export.arxiv.org/api/query. One query per (stratum, half-year unit):
  search_query=cat:<stratum>+AND+submittedDate:[<YYYYMMDD0000>+TO+<YYYYMMDD2359>]
  &start=<n>&max_results=2000&sortBy=submittedDate&sortOrder=ascending
paged via `start` in steps of 2,000 until a page returns fewer than 2,000 entries.
`cat:` matches any-listing (like the OAI-PMH `set=` did); primary-category filtering
stays client-side, in filter_corpus_api.py, per §2.

Pacing (D1): 3-second sleep between EVERY request (not just between pages of the same
unit — globally, across the whole run), over a SINGLE persistent connection, retrying
with backoff (up to 5 tries) on HTTP 5xx OR an "empty-feed anomaly" — a page that comes
back with zero entries while the running fetched-count is still short of that query's
own opensearch:totalResults (a transient hiccup, not a legitimate end-of-results page;
a page with fewer than max_results entries, INCLUDING zero when the tally already
matches totalResults, is the normal, non-anomalous end of pagination).

Discard-and-restart (§2): if --outdir is non-empty, this script refuses to run at all.

Output layout: --outdir/<stratum>/<unit>/<page:05d>.xml.gz (raw Atom response bytes,
gzip-compressed, one file per page) plus --outdir/harvest-log.json recording, per
stratum x unit: totalResults, fetched, pages, start/end UTC — the D1-mandated
cross-check between the harvest's own tally and the feed's declared total.
"""
import argparse
import gzip
import http.client
import json
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ENDPOINT_HOST = "export.arxiv.org"
ENDPOINT_PATH = "/api/query"
MAX_RESULTS = 2000
SLEEP_SECONDS = 3
MAX_RETRIES = 5
RETRY_BASE_SECONDS = 3
STRATA = ("cs.CL", "cs.CV", "math.NT")

ATOM_NS = "http://www.w3.org/2005/Atom"
OPENSEARCH_NS = "http://a9.com/-/spec/opensearch/1.1/"


# ---------------------------------------------------------------------------
# Units (duplicated, deliberately, from envelope.py's generator: harvest scripts
# stay decoupled from the analysis pipeline, same way harvest.py/filter_corpus.py
# already do not import envelope.py).
# ---------------------------------------------------------------------------

def half_year_units(start_year=2015, start_half=1, end_year=2026, end_half=1):
    units = []
    y, h = start_year, start_half
    while (y, h) <= (end_year, end_half):
        units.append(f"{y}H{h}")
        h, y = (2, y) if h == 1 else (1, y + 1)
    return units


UNITS = half_year_units()  # 23 units, 2015H1..2026H1


def half_year_query_range(unit):
    """unit e.g. '2015H1' -> ('201501010000', '201506302359')."""
    year = unit[:4]
    half = unit[4:]
    if half == "H1":
        return f"{year}01010000", f"{year}06302359"
    elif half == "H2":
        return f"{year}07010000", f"{year}12312359"
    raise ValueError(f"unrecognized unit {unit!r}")


def build_query_path(stratum, start_ts, end_ts, start_param, max_results=MAX_RESULTS):
    query = (
        f"search_query=cat:{stratum}+AND+submittedDate:[{start_ts}+TO+{end_ts}]"
        f"&start={start_param}&max_results={max_results}"
        f"&sortBy=submittedDate&sortOrder=ascending"
    )
    return f"{ENDPOINT_PATH}?{query}"


def _utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Single persistent connection (D1: "single connection")
# ---------------------------------------------------------------------------

class _SingleConnection:
    """Wraps ONE http.client connection, reused across every request this script
    makes. Reconnects (once) only if the persistent connection breaks; never opens a
    second concurrent connection. `connection_factory` is injectable for testing."""

    def __init__(self, host, timeout=30, connection_factory=None):
        self.host = host
        self.timeout = timeout
        self._connection_factory = connection_factory or (
            lambda: http.client.HTTPSConnection(host, timeout=timeout)
        )
        self._conn = None

    def get(self, path, headers=None):
        headers = headers or {"User-Agent": "field-research-arxiv-api-harvester/1.0"}
        last_exc = None
        for attempt in (1, 2):  # one reconnect attempt on a broken persistent connection
            if self._conn is None:
                self._conn = self._connection_factory()
            try:
                self._conn.request("GET", path, headers=headers)
                resp = self._conn.getresponse()
                body = resp.read()
                return resp.status, body
            except (http.client.HTTPException, ConnectionError, OSError) as exc:
                last_exc = exc
                try:
                    self._conn.close()
                except Exception:
                    pass
                self._conn = None
                if attempt == 2:
                    raise
        raise RuntimeError("unreachable") from last_exc

    def close(self):
        if self._conn is not None:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None


# ---------------------------------------------------------------------------
# Atom parsing (lightweight, pagination-control only -- full field extraction is
# filter_corpus_api.py's job, from the saved raw gz chunks)
# ---------------------------------------------------------------------------

def count_entries_and_total(body):
    root = ET.fromstring(body)
    total_el = root.find(f"{{{OPENSEARCH_NS}}}totalResults")
    total_results = int(total_el.text) if total_el is not None and total_el.text else 0
    entries = root.findall(f"{{{ATOM_NS}}}entry")
    return len(entries), total_results


# ---------------------------------------------------------------------------
# Page fetch with retry (HTTP 5xx OR empty-feed anomaly)
# ---------------------------------------------------------------------------

def fetch_page(conn, path, cumulative_before, max_retries=MAX_RETRIES, retry_base=RETRY_BASE_SECONDS,
               sleep_fn=time.sleep):
    """Fetch one page, retrying (backoff) on HTTP 5xx or an empty-feed anomaly.
    Returns (body, entry_count, total_results). Raises RuntimeError after exhausting
    retries, or immediately on a non-5xx HTTP error (not retried)."""
    last_err = None
    for attempt in range(1, max_retries + 1):
        status, body = conn.get(path)
        if status == 200:
            entry_count, total_results = count_entries_and_total(body)
            anomaly = entry_count == 0 and total_results > 0 and cumulative_before < total_results
            if not anomaly:
                return body, entry_count, total_results
            last_err = RuntimeError(
                f"empty-feed anomaly: fetched {cumulative_before}/{total_results} so far, "
                f"page returned 0 entries"
            )
        elif 500 <= status < 600:
            last_err = RuntimeError(f"HTTP {status}")
        else:
            raise RuntimeError(f"HTTP {status} for {path} (not retried)")
        if attempt < max_retries:
            sleep_fn(retry_base * (2 ** (attempt - 1)))
            continue
        raise RuntimeError(f"giving up after {max_retries} attempts on {path}: {last_err}")
    raise RuntimeError("unreachable") from last_err


# ---------------------------------------------------------------------------
# Per (stratum, unit) pagination
# ---------------------------------------------------------------------------

def harvest_stratum_unit(conn, stratum, unit, outdir, request_counter,
                          sleep_seconds=SLEEP_SECONDS, sleep_fn=time.sleep,
                          max_results=MAX_RESULTS):
    start_ts, end_ts = half_year_query_range(unit)
    unit_dir = os.path.join(outdir, stratum, unit)
    os.makedirs(unit_dir, exist_ok=True)

    start_utc = _utcnow_iso()
    page = 0
    fetched = 0
    total_results = None
    start_param = 0

    while True:
        if request_counter["n"] > 0:
            sleep_fn(sleep_seconds)
        path = build_query_path(stratum, start_ts, end_ts, start_param, max_results)
        body, entry_count, page_total = fetch_page(conn, path, cumulative_before=fetched, sleep_fn=sleep_fn)
        request_counter["n"] += 1
        page += 1

        chunk_path = os.path.join(unit_dir, f"{page:05d}.xml.gz")
        with gzip.open(chunk_path, "wb") as f:
            f.write(body)

        if total_results is None:
            total_results = page_total
        fetched += entry_count
        start_param += max_results

        if entry_count < max_results:
            break

    end_utc = _utcnow_iso()
    return {
        "total_results": total_results if total_results is not None else 0,
        "fetched": fetched,
        "pages": page,
        "start_utc": start_utc,
        "end_utc": end_utc,
        "tally_matches": fetched == (total_results if total_results is not None else 0),
    }


# ---------------------------------------------------------------------------
# Whole-run orchestration
# ---------------------------------------------------------------------------

def _check_outdir_empty(outdir):
    if os.path.isdir(outdir) and os.listdir(outdir):
        raise SystemExit(
            f"refusing to run: {outdir} already exists and is non-empty. "
            "Partial harvests are discarded and restarted, never topped up. "
            "Remove it manually to re-harvest."
        )


def run_harvest(outdir, strata=STRATA, units=UNITS, sleep_seconds=SLEEP_SECONDS,
                 sleep_fn=time.sleep, connection_factory=None, max_results=MAX_RESULTS):
    _check_outdir_empty(outdir)
    os.makedirs(outdir, exist_ok=True)

    conn = _SingleConnection(ENDPOINT_HOST, connection_factory=connection_factory)
    request_counter = {"n": 0}
    run_start = _utcnow_iso()
    results = {}
    try:
        for stratum in strata:
            results[stratum] = {}
            for unit in units:
                results[stratum][unit] = harvest_stratum_unit(
                    conn, stratum, unit, outdir, request_counter,
                    sleep_seconds=sleep_seconds, sleep_fn=sleep_fn, max_results=max_results,
                )
    finally:
        conn.close()
    run_end = _utcnow_iso()

    log = {
        "endpoint": f"https://{ENDPOINT_HOST}{ENDPOINT_PATH}",
        "parameters": {
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "ascending",
            "strata": list(strata),
            "units": list(units),
        },
        "courtesy_sleep_seconds": sleep_seconds,
        "max_retries": MAX_RETRIES,
        "single_connection": True,
        "start_utc": run_start,
        "end_utc": run_end,
        "results": results,
        "deviation": "D1 (PREREGISTRATION.md §10): route switched from OAI-PMH to this query API before any measurement data was consumed.",
    }
    log_path = os.path.join(outdir, "harvest-log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, sort_keys=True)
    return log


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Archive query-API harvester (PREREGISTRATION.md §10 deviation D1)."
    )
    parser.add_argument("--outdir", required=True, help="Directory to write raw gzipped Atom chunks + harvest-log.json.")
    args = parser.parse_args(argv)

    log = run_harvest(args.outdir)
    print(json.dumps(log, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
