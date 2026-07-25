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

Deep-paging split (§10 amendment D1a): the live run hit a persistent HTTP 500 at
start=10000 on cs.CL 2024H1 (the API's deep-paging weakness). Per (stratum, unit), page
0 of the unit-level query is fetched first as a PROBE, purely to read that query's own
opensearch:totalResults. If totalResults <= MONTHLY_SPLIT_THRESHOLD (8,000), pagination
continues exactly as D1 originally specified (the probe page's data is kept as the
unit's page 1). If totalResults > 8,000, the probe page's data is DISCARDED UNREAD (per
D1a: "so every stored chunk belongs to exactly one query series") and the unit is
re-fetched as 6 independent, shallowly-paged monthly queries instead (same query shape,
month-long date windows). Per D1a, the per-month totalResults must sum to the unit's own
probed totalResults, and unit assignment always comes from each record's <published>
date -- never from which query window (unit-level or monthly) fetched it -- so the split
has no epistemic content, only a pagination-depth workaround.

Output layout: --outdir/<stratum>/<unit>/<page:05d>.xml.gz for unsplit units;
--outdir/<stratum>/<unit>/<YYYYMM>-<page:05d>.xml.gz for split units. Either way,
--outdir/harvest-log.json records, per stratum x unit: mode ("unit" or "monthly"), the
unit's own totalResults (from the probe page), per-month totalResults when split,
fetched, pages, start/end UTC, and a tally_matches flag (unit mode: fetched ==
totalResults; monthly mode: BOTH sum-of-month-totals == unit totalResults AND fetched ==
sum-of-month-totals).
"""
import argparse
import calendar
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
MONTHLY_SPLIT_THRESHOLD = 8000  # §10 amendment D1a
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


def unit_months(unit):
    """unit e.g. '2015H1' -> ['201501', ..., '201506']; '2015H2' -> ['201507', ..., '201512']."""
    year = unit[:4]
    half = unit[4:]
    if half == "H1":
        months = range(1, 7)
    elif half == "H2":
        months = range(7, 13)
    else:
        raise ValueError(f"unrecognized unit {unit!r}")
    return [f"{year}{m:02d}" for m in months]


def month_query_range(yyyymm):
    """yyyymm e.g. '201502' -> ('201502010000', '201502282359') (last day computed via
    calendar.monthrange, so Feb 28/29 and 30/31-day months are handled correctly)."""
    year = int(yyyymm[:4])
    month = int(yyyymm[4:6])
    last_day = calendar.monthrange(year, month)[1]
    return f"{yyyymm}010000", f"{yyyymm}{last_day:02d}2359"


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

def _page_one_query(conn, stratum, start_ts, end_ts, name_fn, request_counter,
                     sleep_seconds, sleep_fn, max_results, first_page_data=None):
    """Page a single query window (unit-level or one month) to completion, writing
    each page via name_fn(page_number) -> chunk path. If `first_page_data` is given
    (body, entry_count, total_results) it is used as page 1 without re-fetching (the
    D1a probe-reuse case for unsplit units); otherwise page 1 is fetched fresh (used
    for each of the 6 monthly queries after a split's probe page was discarded).
    Returns (total_results, fetched, pages)."""
    page = 0
    fetched = 0
    total_results = None
    start_param = 0

    if first_page_data is not None:
        body, entry_count, total_results = first_page_data
        page = 1
        with gzip.open(name_fn(page), "wb") as f:
            f.write(body)
        fetched = entry_count
        start_param = max_results
        if entry_count < max_results:
            return total_results, fetched, page  # single page already covers everything

    while True:
        if request_counter["n"] > 0:
            sleep_fn(sleep_seconds)
        path = build_query_path(stratum, start_ts, end_ts, start_param, max_results)
        body, entry_count, page_total = fetch_page(conn, path, cumulative_before=fetched, sleep_fn=sleep_fn)
        request_counter["n"] += 1
        page += 1

        with gzip.open(name_fn(page), "wb") as f:
            f.write(body)

        if total_results is None:
            total_results = page_total
        fetched += entry_count
        start_param += max_results

        if entry_count < max_results:
            break

    return (total_results if total_results is not None else 0), fetched, page


def harvest_stratum_unit(conn, stratum, unit, outdir, request_counter,
                          sleep_seconds=SLEEP_SECONDS, sleep_fn=time.sleep,
                          max_results=MAX_RESULTS, split_threshold=MONTHLY_SPLIT_THRESHOLD):
    start_ts, end_ts = half_year_query_range(unit)
    unit_dir = os.path.join(outdir, stratum, unit)
    os.makedirs(unit_dir, exist_ok=True)

    start_utc = _utcnow_iso()

    # Probe: page 0 of the unit-level query, purely to read totalResults.
    if request_counter["n"] > 0:
        sleep_fn(sleep_seconds)
    probe_path = build_query_path(stratum, start_ts, end_ts, 0, max_results)
    probe_body, probe_entry_count, unit_total_results = fetch_page(
        conn, probe_path, cumulative_before=0, sleep_fn=sleep_fn
    )
    request_counter["n"] += 1

    if unit_total_results <= split_threshold:
        # Unit mode: keep the probe page as page 1 (plain <page:05d>.xml.gz naming);
        # continue paging exactly as D1 originally specified.
        def name_fn(page):
            return os.path.join(unit_dir, f"{page:05d}.xml.gz")

        total_results, fetched, pages = _page_one_query(
            conn, stratum, start_ts, end_ts, name_fn, request_counter,
            sleep_seconds, sleep_fn, max_results,
            first_page_data=(probe_body, probe_entry_count, unit_total_results),
        )
        end_utc = _utcnow_iso()
        return {
            "mode": "unit",
            "total_results": total_results,
            "fetched": fetched,
            "pages": pages,
            "start_utc": start_utc,
            "end_utc": end_utc,
            "tally_matches": fetched == total_results,
        }

    # Monthly mode (D1a): the probe page's data is discarded UNREAD -- it belongs to
    # the abandoned unit-level query series, not the monthly one, and D1a requires
    # every stored chunk to belong to exactly one query series.
    del probe_body
    months = unit_months(unit)
    month_results = {}
    total_fetched = 0
    total_pages = 0
    for yyyymm in months:
        m_start, m_end = month_query_range(yyyymm)

        def name_fn(page, _yyyymm=yyyymm):
            return os.path.join(unit_dir, f"{_yyyymm}-{page:05d}.xml.gz")

        m_total, m_fetched, m_pages = _page_one_query(
            conn, stratum, m_start, m_end, name_fn, request_counter,
            sleep_seconds, sleep_fn, max_results, first_page_data=None,
        )
        month_results[yyyymm] = {"total_results": m_total, "fetched": m_fetched, "pages": m_pages}
        total_fetched += m_fetched
        total_pages += m_pages

    end_utc = _utcnow_iso()
    sum_month_totals = sum(mr["total_results"] for mr in month_results.values())
    return {
        "mode": "monthly",
        "total_results": unit_total_results,
        "months": month_results,
        "sum_month_total_results": sum_month_totals,
        "fetched": total_fetched,
        "pages": total_pages,
        "start_utc": start_utc,
        "end_utc": end_utc,
        "tally_matches": (sum_month_totals == unit_total_results) and (total_fetched == sum_month_totals),
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
                 sleep_fn=time.sleep, connection_factory=None, max_results=MAX_RESULTS,
                 split_threshold=MONTHLY_SPLIT_THRESHOLD):
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
                    split_threshold=split_threshold,
                )
    finally:
        conn.close()
    run_end = _utcnow_iso()

    log = {
        "endpoint": f"https://{ENDPOINT_HOST}{ENDPOINT_PATH}",
        "parameters": {
            "max_results": max_results,
            "monthly_split_threshold": split_threshold,
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
        "deviation": (
            "D1 (PREREGISTRATION.md §10): route switched from OAI-PMH to this query API "
            "before any measurement data was consumed. D1a: (stratum, unit) queries whose "
            "own totalResults exceed monthly_split_threshold are split into 6 calendar-month "
            "queries each, paged shallowly; unit assignment always comes from each record's "
            "<published> date, never from which query window fetched it."
        ),
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
