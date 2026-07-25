"""
scripts/harvest.py — OAI-PMH bulk-metadata harvester, per PREREGISTRATION.md §2.

`ListRecords`, `metadataPrefix=arXiv`, sets "cs" and "math", `from=2015-01-01`, against
`https://oaipmh.arxiv.org/oai`, at the courtesy rate (~1 request / 3 s), following
`resumptionToken` until the archive stops returning one.

Stdlib only: urllib, gzip, json, time, hashlib. No third-party dependencies.

Determinism / resumability contract (per §2 and the build precondition in
provenance/feasibility-pretest.md): a partial harvest is discarded and restarted, never
topped up. If `--outdir/<set>/` already exists and is non-empty for a requested set,
this script refuses to run for that set. There is no "resume from here" mode — delete
the partial directory yourself if you want to restart.

Every raw HTTP response body is written verbatim, gzip-compressed, one file per
response, under `--outdir/<set>/<zero-padded-sequence>.xml.gz`. A `harvest-log.json` is
written to `--outdir` with start/end UTC timestamps, the endpoint, the fixed request
parameters, and the request count per set.
"""
import argparse
import gzip
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ENDPOINT = "https://oaipmh.arxiv.org/oai"
METADATA_PREFIX = "arXiv"
FROM_DATE = "2015-01-01"
SETS = ("cs", "math")
SLEEP_SECONDS = 3
MAX_RETRIES = 5
RETRY_BASE_SECONDS = 3
USER_AGENT = "field-research-oai-harvester/1.0"

OAI_NS = "http://www.openarchives.org/OAI/2.0/"


def _utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _initial_url(set_name):
    params = {
        "verb": "ListRecords",
        "metadataPrefix": METADATA_PREFIX,
        "set": set_name,
        "from": FROM_DATE,
    }
    return f"{ENDPOINT}?{urllib.parse.urlencode(params)}"


def _resumption_url(token):
    # Per OAI-PMH, a resumptionToken request carries only verb+resumptionToken.
    # The token is passed verbatim (as issued by the archive), URL-encoded.
    params = {"verb": "ListRecords", "resumptionToken": token}
    return f"{ENDPOINT}?{urllib.parse.urlencode(params)}"


def _fetch(url):
    """Fetch `url` with retry-with-backoff on HTTP 5xx, up to MAX_RETRIES tries.
    Returns the raw response bytes. Raises on non-5xx HTTP errors or after exhausting
    retries."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if 500 <= e.code < 600:
                last_error = e
                if attempt < MAX_RETRIES:
                    backoff = RETRY_BASE_SECONDS * (2 ** (attempt - 1))
                    time.sleep(backoff)
                    continue
                raise RuntimeError(
                    f"HTTP {e.code} from {url} after {MAX_RETRIES} attempts"
                ) from e
            raise
    raise RuntimeError(f"unreachable retry exhaustion for {url}") from last_error


def _extract_resumption_token(xml_bytes):
    """Returns (token_or_none, oai_error_or_none)."""
    root = ET.fromstring(xml_bytes)
    error_el = root.find(f"{{{OAI_NS}}}error")
    if error_el is not None:
        code = error_el.get("code", "")
        text = (error_el.text or "").strip()
        return None, f"{code}: {text}"
    list_records = root.find(f"{{{OAI_NS}}}ListRecords")
    if list_records is None:
        return None, None
    token_el = list_records.find(f"{{{OAI_NS}}}resumptionToken")
    if token_el is None:
        return None, None
    token = (token_el.text or "").strip()
    return (token if token else None), None


def _check_outdir_empty(set_dir):
    if os.path.isdir(set_dir) and os.listdir(set_dir):
        raise SystemExit(
            f"refusing to run: {set_dir} already exists and is non-empty. "
            "Partial harvests are discarded and restarted, never topped up. "
            "Remove it manually to re-harvest this set."
        )


def harvest_set(set_name, outdir, sleep_seconds=SLEEP_SECONDS):
    set_dir = os.path.join(outdir, set_name)
    os.makedirs(set_dir, exist_ok=True)

    seq = 0
    url = _initial_url(set_name)
    request_count = 0

    while True:
        body = _fetch(url)
        request_count += 1
        seq += 1
        chunk_path = os.path.join(set_dir, f"{seq:05d}.xml.gz")
        with gzip.open(chunk_path, "wb") as f:
            f.write(body)

        token, oai_error = _extract_resumption_token(body)
        if oai_error is not None:
            raise RuntimeError(f"OAI-PMH error for set={set_name} at request {request_count}: {oai_error}")

        if token is None:
            break

        time.sleep(sleep_seconds)
        url = _resumption_url(token)

    return request_count


def run_harvest(outdir, sets=SETS, sleep_seconds=SLEEP_SECONDS):
    os.makedirs(outdir, exist_ok=True)

    # Pre-flight: refuse up front for ALL requested sets before doing any work.
    for set_name in sets:
        _check_outdir_empty(os.path.join(outdir, set_name))

    start_utc = _utcnow_iso()
    requests_per_set = {}
    for set_name in sets:
        requests_per_set[set_name] = harvest_set(set_name, outdir, sleep_seconds)
    end_utc = _utcnow_iso()

    log = {
        "endpoint": ENDPOINT,
        "parameters": {
            "verb": "ListRecords",
            "metadataPrefix": METADATA_PREFIX,
            "from": FROM_DATE,
            "sets": list(sets),
        },
        "courtesy_sleep_seconds": sleep_seconds,
        "max_retries": MAX_RETRIES,
        "start_utc": start_utc,
        "end_utc": end_utc,
        "requests_per_set": requests_per_set,
    }
    log_path = os.path.join(outdir, "harvest-log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, sort_keys=True)
    return log


def main(argv=None):
    parser = argparse.ArgumentParser(description="OAI-PMH ListRecords harvester (PREREGISTRATION.md §2).")
    parser.add_argument("--outdir", required=True, help="Directory to write raw gzipped chunks + harvest-log.json.")
    parser.add_argument("--sets", nargs="+", default=list(SETS), help="OAI sets to harvest (default: cs math).")
    args = parser.parse_args(argv)

    log = run_harvest(args.outdir, tuple(args.sets))
    print(json.dumps(log, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
