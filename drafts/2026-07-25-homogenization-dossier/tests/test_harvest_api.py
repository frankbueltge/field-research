import json
import os
import shutil
import tempfile
import unittest

import _pathfix  # noqa: F401
import harvest_api
from harvest_api import (
    half_year_query_range,
    build_query_path,
    count_entries_and_total,
    fetch_page,
    harvest_stratum_unit,
    run_harvest,
    _SingleConnection,
    ATOM_NS,
    OPENSEARCH_NS,
    MAX_RESULTS,
)


def _atom_body(n_entries, total_results):
    entries = "".join(f"<entry><id>http://arxiv.org/abs/{i:04d}.0000{i}</id></entry>" for i in range(n_entries))
    xml = (
        f'<feed xmlns="{ATOM_NS}" xmlns:opensearch="{OPENSEARCH_NS}">'
        f"<opensearch:totalResults>{total_results}</opensearch:totalResults>"
        f"{entries}"
        f"</feed>"
    )
    return xml.encode("utf-8")


class TestHalfYearQueryRange(unittest.TestCase):
    def test_h1(self):
        self.assertEqual(half_year_query_range("2015H1"), ("201501010000", "201506302359"))

    def test_h2(self):
        self.assertEqual(half_year_query_range("2015H2"), ("201507010000", "201512312359"))

    def test_invalid_half_raises(self):
        with self.assertRaises(ValueError):
            half_year_query_range("2015H3")


class TestBuildQueryPath(unittest.TestCase):
    def test_exact_format(self):
        path = build_query_path("cs.CL", "201501010000", "201506302359", 2000, 2000)
        expected = (
            "/api/query?search_query=cat:cs.CL+AND+submittedDate:"
            "[201501010000+TO+201506302359]&start=2000&max_results=2000"
            "&sortBy=submittedDate&sortOrder=ascending"
        )
        self.assertEqual(path, expected)


class TestCountEntriesAndTotal(unittest.TestCase):
    def test_counts_entries_and_reads_total(self):
        body = _atom_body(3, 137)
        n, total = count_entries_and_total(body)
        self.assertEqual(n, 3)
        self.assertEqual(total, 137)

    def test_zero_entries(self):
        body = _atom_body(0, 0)
        n, total = count_entries_and_total(body)
        self.assertEqual(n, 0)
        self.assertEqual(total, 0)


class _ScriptedConn:
    """Stub matching _SingleConnection's .get(path) interface."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def get(self, path, headers=None):
        self.calls.append(path)
        return self._responses.pop(0)


class TestFetchPageRetry(unittest.TestCase):
    def test_normal_success(self):
        conn = _ScriptedConn([(200, _atom_body(3, 3))])
        body, n, total = fetch_page(conn, "/p", cumulative_before=0, sleep_fn=lambda s: None)
        self.assertEqual(n, 3)
        self.assertEqual(total, 3)

    def test_retries_on_5xx_then_succeeds(self):
        sleeps = []
        conn = _ScriptedConn([(503, b""), (200, _atom_body(2, 2))])
        body, n, total = fetch_page(conn, "/p", cumulative_before=0, sleep_fn=sleeps.append)
        self.assertEqual(n, 2)
        self.assertEqual(len(sleeps), 1)  # one backoff sleep before the successful retry

    def test_persistent_5xx_raises_after_max_retries(self):
        conn = _ScriptedConn([(500, b"")] * 3)
        with self.assertRaises(RuntimeError):
            fetch_page(conn, "/p", cumulative_before=0, max_retries=3, sleep_fn=lambda s: None)

    def test_empty_feed_anomaly_retries_then_succeeds(self):
        # cumulative_before=0, total=10 -> a 0-entry page IS an anomaly (more expected).
        conn = _ScriptedConn([(200, _atom_body(0, 10)), (200, _atom_body(5, 10))])
        body, n, total = fetch_page(conn, "/p", cumulative_before=0, sleep_fn=lambda s: None)
        self.assertEqual(n, 5)
        self.assertEqual(len(conn.calls), 2)

    def test_empty_feed_at_exact_tally_is_not_an_anomaly(self):
        # cumulative_before=10, total=10 -> a 0-entry page is the legitimate end.
        conn = _ScriptedConn([(200, _atom_body(0, 10))])
        body, n, total = fetch_page(conn, "/p", cumulative_before=10, sleep_fn=lambda s: None)
        self.assertEqual(n, 0)
        self.assertEqual(len(conn.calls), 1)  # not retried

    def test_persistent_empty_feed_anomaly_raises(self):
        conn = _ScriptedConn([(200, _atom_body(0, 10))] * 3)
        with self.assertRaises(RuntimeError):
            fetch_page(conn, "/p", cumulative_before=0, max_retries=3, sleep_fn=lambda s: None)

    def test_non_5xx_http_error_raises_immediately_not_retried(self):
        conn = _ScriptedConn([(404, b""), (200, _atom_body(1, 1))])
        with self.assertRaises(RuntimeError):
            fetch_page(conn, "/p", cumulative_before=0, sleep_fn=lambda s: None)
        self.assertEqual(len(conn.calls), 1)  # the second (200) response was never consumed
        self.assertEqual(len(conn._responses), 1)


class TestHarvestStratumUnit(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_pagination_stops_on_partial_page(self):
        # max_results=3, total=7 -> pages of 3, 3, 1 (stop: 1 < 3).
        conn = _ScriptedConn([
            (200, _atom_body(3, 7)),
            (200, _atom_body(3, 7)),
            (200, _atom_body(1, 7)),
        ])
        request_counter = {"n": 0}
        sleeps = []
        result = harvest_stratum_unit(
            conn, "cs.CL", "2015H1", self.tmpdir, request_counter,
            sleep_fn=sleeps.append, max_results=3,
        )
        self.assertEqual(result["pages"], 3)
        self.assertEqual(result["fetched"], 7)
        self.assertEqual(result["total_results"], 7)
        self.assertTrue(result["tally_matches"])
        # sleep happens before every request except the very first of the whole run
        self.assertEqual(len(sleeps), 2)

        unit_dir = os.path.join(self.tmpdir, "cs.CL", "2015H1")
        files = sorted(os.listdir(unit_dir))
        self.assertEqual(files, ["00001.xml.gz", "00002.xml.gz", "00003.xml.gz"])

        import gzip
        with gzip.open(os.path.join(unit_dir, "00001.xml.gz"), "rb") as f:
            content = f.read()
        n, total = count_entries_and_total(content)
        self.assertEqual(n, 3)
        self.assertEqual(total, 7)

    def test_single_page_when_first_page_already_partial(self):
        conn = _ScriptedConn([(200, _atom_body(1, 1))])
        request_counter = {"n": 0}
        result = harvest_stratum_unit(
            conn, "math.NT", "2020H2", self.tmpdir, request_counter,
            sleep_fn=lambda s: None, max_results=2000,
        )
        self.assertEqual(result["pages"], 1)
        self.assertEqual(result["fetched"], 1)
        self.assertEqual(result["total_results"], 1)


class TestOutdirGuard(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_refuses_nonempty_outdir(self):
        with open(os.path.join(self.tmpdir, "stray.txt"), "w") as f:
            f.write("x")
        with self.assertRaises(SystemExit):
            run_harvest(self.tmpdir, sleep_fn=lambda s: None)


class TestSingleConnection(unittest.TestCase):
    class _FakeHTTPConnection:
        def __init__(self, script):
            self._script = list(script)
            self.requests = []
            self.closed = False

        def request(self, method, path, headers=None):
            self.requests.append(path)

        def getresponse(self):
            item = self._script.pop(0)
            if isinstance(item, Exception):
                raise item
            status, body = item
            return TestSingleConnection._FakeResponse(status, body)

        def close(self):
            self.closed = True

    class _FakeResponse:
        def __init__(self, status, body):
            self.status = status
            self._body = body

        def read(self):
            return self._body

    def test_single_connection_object_reused_across_gets(self):
        conn_obj = self._FakeHTTPConnection([(200, b"a"), (200, b"b"), (200, b"c")])
        created = []

        def factory():
            created.append(conn_obj)
            return conn_obj

        sc = _SingleConnection("host.example", connection_factory=factory)
        sc.get("/p1")
        sc.get("/p2")
        sc.get("/p3")
        self.assertEqual(len(created), 1)
        self.assertEqual(conn_obj.requests, ["/p1", "/p2", "/p3"])

    def test_reconnects_once_on_broken_connection(self):
        broken = self._FakeHTTPConnection([ConnectionError("boom")])
        healthy = self._FakeHTTPConnection([(200, b"ok")])
        pool = iter([broken, healthy])
        created = []

        def factory():
            c = next(pool)
            created.append(c)
            return c

        sc = _SingleConnection("host.example", connection_factory=factory)
        status, body = sc.get("/p")
        self.assertEqual(status, 200)
        self.assertEqual(body, b"ok")
        self.assertEqual(len(created), 2)
        self.assertTrue(broken.closed)


class TestRunHarvestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_run_harvest_writes_log_and_chunks(self):
        conn_obj = TestSingleConnection._FakeHTTPConnection([
            (200, _atom_body(1, 1)),  # cs.CL 2015H1
            (200, _atom_body(1, 1)),  # cs.CL 2015H2
        ])

        def factory():
            return conn_obj

        outdir = os.path.join(self.tmpdir, "out")
        log = run_harvest(
            outdir,
            strata=("cs.CL",),
            units=("2015H1", "2015H2"),
            sleep_fn=lambda s: None,
            connection_factory=factory,
            max_results=2000,
        )
        self.assertEqual(log["results"]["cs.CL"]["2015H1"]["fetched"], 1)
        self.assertEqual(log["results"]["cs.CL"]["2015H2"]["fetched"], 1)
        self.assertTrue(os.path.exists(os.path.join(outdir, "harvest-log.json")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "cs.CL", "2015H1", "00001.xml.gz")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "cs.CL", "2015H2", "00001.xml.gz")))

        with open(os.path.join(outdir, "harvest-log.json")) as f:
            on_disk = json.load(f)
        self.assertIn("deviation", on_disk)
        self.assertEqual(on_disk["single_connection"], True)


if __name__ == "__main__":
    unittest.main()
