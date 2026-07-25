import gzip
import json
import os
import shutil
import tempfile
import unittest

import _pathfix  # noqa: F401
from filter_corpus_api import extract_id, parse_entries, filter_corpus_api, iter_raw_files, ATOM_NS, ARXIV_ATOM_NS


def _long_abstract(n=60):
    return " ".join(f"lexeme{i}" for i in range(n))


def _short_abstract(n=10):
    return " ".join(f"lexeme{i}" for i in range(n))


def _entry(raw_id, created, datestamp, primary, abstract, first_category=None):
    first_category = first_category or primary
    return f"""
    <entry>
      <id>http://arxiv.org/abs/{raw_id}</id>
      <published>{created}T00:00:00Z</published>
      <updated>{datestamp}T00:00:00Z</updated>
      <summary>{abstract}</summary>
      <category term="{first_category}" scheme="http://arxiv.org/schemas/atom"/>
      <arxiv:primary_category xmlns:arxiv="{ARXIV_ATOM_NS}" term="{primary}" scheme="http://arxiv.org/schemas/atom"/>
    </entry>"""


def _wrap(entries_xml, total_results=1):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="{ATOM_NS}" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
      <opensearch:totalResults>{total_results}</opensearch:totalResults>
      {entries_xml}
    </feed>"""


class TestExtractId(unittest.TestCase):
    def test_new_style_with_version(self):
        self.assertEqual(extract_id("http://arxiv.org/abs/2501.01234v2"), "2501.01234")

    def test_new_style_https_with_version(self):
        self.assertEqual(extract_id("https://arxiv.org/abs/2501.01234v10"), "2501.01234")

    def test_new_style_no_version(self):
        self.assertEqual(extract_id("http://arxiv.org/abs/2501.01234"), "2501.01234")

    def test_old_style_keeps_slash_form(self):
        self.assertEqual(extract_id("http://arxiv.org/abs/math/0501001v1"), "math/0501001")

    def test_old_style_no_version(self):
        self.assertEqual(extract_id("http://arxiv.org/abs/math/0501001"), "math/0501001")

    def test_unparseable_returns_none(self):
        self.assertIsNone(extract_id("not a url"))
        self.assertIsNone(extract_id(""))
        self.assertIsNone(extract_id(None))


class TestParseEntries(unittest.TestCase):
    def _write(self, tmpdir, name, xml_text):
        path = os.path.join(tmpdir, name)
        with gzip.open(path, "wb") as f:
            f.write(xml_text.encode("utf-8"))
        return path

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_version_suffix_stripped(self):
        xml = _wrap(_entry("2501.01234v2", "2025-01-02", "2025-01-02", "cs.CL", _long_abstract()))
        path = self._write(self.tmpdir, "a.xml.gz", xml)
        entries = list(parse_entries(path))
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["id"], "2501.01234")

    def test_old_style_id_preserved(self):
        xml = _wrap(_entry("math/0501001v1", "2015-01-02", "2015-01-02", "math.NT", _long_abstract()))
        path = self._write(self.tmpdir, "b.xml.gz", xml)
        entries = list(parse_entries(path))
        self.assertEqual(entries[0]["id"], "math/0501001")

    def test_primary_category_wins_over_first_listed_category(self):
        # Cross-listed: the FIRST <category> is cs.LG, but arxiv:primary_category is
        # cs.CL -- the parser must report cs.CL (the explicit primary), not cs.LG.
        xml = _wrap(_entry(
            "2501.05555", "2025-01-02", "2025-01-02", primary="cs.CL",
            abstract=_long_abstract(), first_category="cs.LG",
        ))
        path = self._write(self.tmpdir, "c.xml.gz", xml)
        entries = list(parse_entries(path))
        self.assertEqual(entries[0]["primary_category"], "cs.CL")

    def test_created_and_datestamp_from_published_and_updated(self):
        xml = _wrap(_entry("2501.06666", "2025-02-03", "2025-06-01", "cs.CV", _long_abstract()))
        path = self._write(self.tmpdir, "d.xml.gz", xml)
        entries = list(parse_entries(path))
        self.assertEqual(entries[0]["created"], "2025-02-03")
        self.assertEqual(entries[0]["datestamp"], "2025-06-01")

    def test_multiple_entries_in_one_feed(self):
        xml = _wrap(
            _entry("2501.07777", "2025-01-01", "2025-01-01", "cs.CL", _long_abstract())
            + _entry("2501.08888", "2025-01-02", "2025-01-02", "cs.CV", _long_abstract())
        )
        path = self._write(self.tmpdir, "e.xml.gz", xml)
        entries = list(parse_entries(path))
        self.assertEqual(len(entries), 2)


class TestFilterCorpusApiPipeline(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.raw_dir = os.path.join(self.tmpdir, "raw")
        self.outdir = os.path.join(self.tmpdir, "out")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_chunk(self, stratum, unit, filename, xml_text):
        path = os.path.join(self.raw_dir, stratum, unit, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with gzip.open(path, "wb") as f:
            f.write(xml_text.encode("utf-8"))

    def test_full_pipeline_rules(self):
        entries = "".join([
            _entry("2501.00001", "2025-01-02", "2025-01-02", "cs.CL", _long_abstract()),
            _entry("2501.00002", "2025-01-03", "2025-01-03", "cs.CL", _short_abstract()),  # excluded_short
            # cross-listed: query stratum dir is cs.CV, but primary is actually cs.LG
            # (not one of the three target strata) -- must be dropped entirely.
            _entry("2501.00003", "2025-02-01", "2025-02-01", "cs.LG", _long_abstract(), first_category="cs.CV"),
            _entry("2014.99999", "2014-12-31", "2014-12-31", "cs.CV", _long_abstract()),  # out of range
            _entry("2501.00006", "2025-07-05", "2025-07-05", "cs.CV", _long_abstract()),  # H2 unit
        ])
        self._write_chunk("cs.CL", "2025H1", "00001.xml.gz", _wrap(entries))

        # cross-listed duplicate of 2501.00001, surfacing under a different query
        # stratum's raw file -- must NOT be double-counted.
        dup_entries = _entry("2501.00001", "2025-01-02", "2025-01-02", "cs.CL", _long_abstract())
        self._write_chunk("cs.CV", "2025H1", "00001.xml.gz", _wrap(dup_entries))

        math_entries = _entry("2501.00007", "2025-03-01", "2025-03-01", "math.NT", _long_abstract())
        self._write_chunk("math.NT", "2025H1", "00001.xml.gz", _wrap(math_entries))

        counts = filter_corpus_api(self.raw_dir, self.outdir)

        self.assertEqual(counts["cs.CL"]["2025H1"]["kept"], 1)
        self.assertEqual(counts["cs.CL"]["2025H1"]["excluded_short"], 1)
        self.assertNotIn("2025H1", counts["cs.CV"])  # the only cs.CV-primary candidate was out of range
        self.assertEqual(counts["cs.CV"]["2025H2"]["kept"], 1)
        self.assertEqual(counts["math.NT"]["2025H1"]["kept"], 1)

        cl_path = os.path.join(self.outdir, "cs.CL.jsonl")
        with open(cl_path) as f:
            cl_rows = [json.loads(line) for line in f]
        ids = [r["id"] for r in cl_rows]
        self.assertEqual(ids.count("2501.00001"), 1)  # dedup across raw files
        self.assertEqual(set(cl_rows[0].keys()), {"id", "created", "datestamp", "unit", "abstract"})

        self.assertTrue(os.path.exists(os.path.join(self.outdir, "manifest.json")))
        with open(os.path.join(self.outdir, "manifest.json")) as f:
            manifest = json.load(f)
        self.assertIn("input_sha256", manifest)
        self.assertIn("output_sha256", manifest)
        self.assertIn("D1", manifest["route"])

        with open(os.path.join(self.outdir, "counts.json")) as f:
            counts_json = json.load(f)
        self.assertIn("cells", counts_json)
        self.assertIn("contamination_ceiling", counts_json)

    def test_contamination_ceiling_uses_updated_date(self):
        entries = "".join([
            _entry("2001.00001", "2020-01-02", "2020-01-02", "cs.CL", _long_abstract()),  # untouched
            _entry("2001.00002", "2020-03-01", "2023-05-01", "cs.CL", _long_abstract()),  # updated post-launch
            _entry("2001.00003", "2021-06-01", "2024-01-15", "cs.CL", _long_abstract()),  # updated post-launch
        ])
        self._write_chunk("cs.CL", "2020H1", "00001.xml.gz", _wrap(entries))

        filter_corpus_api(self.raw_dir, self.outdir)
        with open(os.path.join(self.outdir, "counts.json")) as f:
            counts_json = json.load(f)
        cl = counts_json["contamination_ceiling"]["cs.CL"]
        self.assertEqual(cl["pre2023_kept_count"], 3)
        self.assertEqual(cl["pre2023_datestamp_post2023_count"], 2)
        self.assertAlmostEqual(cl["share"], 2 / 3)

    def test_deterministic_output_across_runs(self):
        entries = _entry("2001.00010", "2020-01-02", "2020-01-02", "math.NT", _long_abstract())
        self._write_chunk("math.NT", "2020H1", "00001.xml.gz", _wrap(entries))

        filter_corpus_api(self.raw_dir, self.outdir)
        with open(os.path.join(self.outdir, "math.NT.jsonl")) as f:
            content1 = f.read()

        outdir2 = os.path.join(self.tmpdir, "out2")
        filter_corpus_api(self.raw_dir, outdir2)
        with open(os.path.join(outdir2, "math.NT.jsonl")) as f:
            content2 = f.read()

        self.assertEqual(content1, content2)

    def test_mixed_naming_across_units_both_discovered_and_parsed(self):
        # §10 amendment D1a: a split unit's chunks are named <YYYYMM>-<page:05d>.xml.gz
        # while an unsplit unit in the SAME raw_dir keeps the plain <page:05d>.xml.gz
        # naming. Both must be discovered and parsed identically.
        plain_entries = _entry("2501.00001", "2025-01-02", "2025-01-02", "cs.CL", _long_abstract())
        self._write_chunk("cs.CL", "2025H1", "00001.xml.gz", _wrap(plain_entries))

        # cs.CL 2024H1 was split into monthly chunks (D1a); simulate two of its months.
        jan_entries = _entry("2401.00001", "2024-01-15", "2024-01-15", "cs.CL", _long_abstract())
        feb_entries = _entry("2402.00001", "2024-02-20", "2024-02-20", "cs.CL", _long_abstract())
        self._write_chunk("cs.CL", "2024H1", "202401-00001.xml.gz", _wrap(jan_entries))
        self._write_chunk("cs.CL", "2024H1", "202402-00001.xml.gz", _wrap(feb_entries))

        # confirm iter_raw_files finds all three chunks regardless of naming shape
        found = sorted(os.path.basename(path) for _s, _u, path in iter_raw_files(self.raw_dir))
        self.assertEqual(found, ["00001.xml.gz", "202401-00001.xml.gz", "202402-00001.xml.gz"])

        counts = filter_corpus_api(self.raw_dir, self.outdir)
        self.assertEqual(counts["cs.CL"]["2025H1"]["kept"], 1)
        self.assertEqual(counts["cs.CL"]["2024H1"]["kept"], 2)

        with open(os.path.join(self.outdir, "cs.CL.jsonl")) as f:
            rows = [json.loads(line) for line in f]
        ids = {r["id"] for r in rows}
        self.assertEqual(ids, {"2501.00001", "2401.00001", "2402.00001"})
        units = {r["id"]: r["unit"] for r in rows}
        self.assertEqual(units["2401.00001"], "2024H1")
        self.assertEqual(units["2402.00001"], "2024H1")


if __name__ == "__main__":
    unittest.main()
