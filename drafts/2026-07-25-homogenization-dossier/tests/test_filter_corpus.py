import gzip
import json
import os
import shutil
import tempfile
import unittest

import _pathfix  # noqa: F401
from filter_corpus import half_year_unit, primary_category, in_date_range, filter_corpus

OAI_NS = "http://www.openarchives.org/OAI/2.0/"
ARXIV_NS = "http://arxiv.org/OAI/arXiv/"


def _long_abstract(n=60):
    return " ".join(f"lexeme{i}" for i in range(n))


def _short_abstract(n=10):
    return " ".join(f"lexeme{i}" for i in range(n))


def _record(identifier, created, categories, abstract, deleted=False, datestamp=None):
    if datestamp is None:
        datestamp = created  # default: metadata untouched since creation
    if deleted:
        return f"""
        <record>
          <header status="deleted">
            <identifier>oai:arXiv.org:{identifier}</identifier>
            <datestamp>{datestamp}</datestamp>
          </header>
        </record>"""
    return f"""
    <record>
      <header>
        <identifier>oai:arXiv.org:{identifier}</identifier>
        <datestamp>{datestamp}</datestamp>
      </header>
      <metadata>
        <arXiv xmlns="{ARXIV_NS}">
          <id>{identifier}</id>
          <created>{created}</created>
          <categories>{categories}</categories>
          <abstract>{abstract}</abstract>
        </arXiv>
      </metadata>
    </record>"""


def _wrap(records_xml):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <OAI-PMH xmlns="{OAI_NS}">
      <ListRecords>
        {records_xml}
      </ListRecords>
    </OAI-PMH>"""


class TestHalfYearUnit(unittest.TestCase):
    def test_h1(self):
        self.assertEqual(half_year_unit("2015-01-01"), "2015H1")
        self.assertEqual(half_year_unit("2015-06-30"), "2015H1")

    def test_h2(self):
        self.assertEqual(half_year_unit("2015-07-01"), "2015H2")
        self.assertEqual(half_year_unit("2015-12-31"), "2015H2")


class TestPrimaryCategory(unittest.TestCase):
    def test_first_token_is_primary(self):
        self.assertEqual(primary_category("cs.CL cs.LG stat.ML"), "cs.CL")

    def test_single_category(self):
        self.assertEqual(primary_category("math.NT"), "math.NT")

    def test_empty(self):
        self.assertIsNone(primary_category(""))
        self.assertIsNone(primary_category(None))


class TestDateRange(unittest.TestCase):
    def test_in_range(self):
        self.assertTrue(in_date_range("2015-01-01"))
        self.assertTrue(in_date_range("2026-06-30"))
        self.assertTrue(in_date_range("2020-03-15"))

    def test_out_of_range(self):
        self.assertFalse(in_date_range("2014-12-31"))
        self.assertFalse(in_date_range("2026-07-01"))


class TestFilterCorpusPipeline(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.raw_dir = os.path.join(self.tmpdir, "raw")
        self.outdir = os.path.join(self.tmpdir, "out")
        os.makedirs(os.path.join(self.raw_dir, "cs"))
        os.makedirs(os.path.join(self.raw_dir, "math"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_chunk(self, set_name, filename, xml_text):
        path = os.path.join(self.raw_dir, set_name, filename)
        with gzip.open(path, "wb") as f:
            f.write(xml_text.encode("utf-8"))

    def test_full_pipeline_rules(self):
        cs_records = "".join([
            _record("1501.00001", "2015-01-02", "cs.CL cs.LG", _long_abstract()),
            _record("1501.00002", "2015-01-03", "cs.CL", _short_abstract()),  # excluded_short
            _record("1501.00003", "2015-02-01", "cs.LG cs.CL", _long_abstract()),  # not primary target
            _record("1501.00004", "2014-12-31", "cs.CV", _long_abstract()),  # out of range
            _record("1501.00005", "2015-01-04", "cs.CV", _long_abstract(), deleted=True),  # deleted
            _record("1501.00006", "2015-07-05", "cs.CV", _long_abstract()),  # H2 unit
        ])
        self._write_chunk("cs", "00001.xml.gz", _wrap(cs_records))

        math_records = "".join([
            _record("1501.00007", "2015-03-01", "math.NT", _long_abstract()),
            # cross-listed duplicate of a cs record already kept under cs -- should
            # NOT be double-counted (dedup by id).
            _record("1501.00001", "2015-01-02", "cs.CL cs.LG", _long_abstract()),
        ])
        self._write_chunk("math", "00001.xml.gz", _wrap(math_records))

        counts = filter_corpus(self.raw_dir, self.outdir)

        self.assertEqual(counts["cs.CL"]["2015H1"]["kept"], 1)
        self.assertEqual(counts["cs.CL"]["2015H1"]["excluded_short"], 1)
        # cs.CV's only in-range, non-deleted record (1501.00006) is dated 2015-07-05
        # (H2); the H1 cs.CV candidate (1501.00004) was out of date range.
        self.assertNotIn("2015H1", counts["cs.CV"])
        self.assertEqual(counts["cs.CV"]["2015H2"]["kept"], 1)
        self.assertEqual(counts["math.NT"]["2015H1"]["kept"], 1)

        # dedup: 1501.00001 must appear exactly once across outputs
        cl_path = os.path.join(self.outdir, "cs.CL.jsonl")
        with open(cl_path) as f:
            cl_rows = [json.loads(line) for line in f]
        ids = [r["id"] for r in cl_rows]
        self.assertEqual(ids.count("1501.00001"), 1)

        # JSONL rows carry the OAI datestamp alongside the four original fields.
        row = cl_rows[0]
        self.assertEqual(set(row.keys()), {"id", "created", "datestamp", "unit", "abstract"})
        self.assertEqual(row["datestamp"], "2015-01-02")  # default: untouched since creation

        # manifest + counts files exist
        self.assertTrue(os.path.exists(os.path.join(self.outdir, "manifest.json")))
        self.assertTrue(os.path.exists(os.path.join(self.outdir, "counts.json")))
        with open(os.path.join(self.outdir, "manifest.json")) as f:
            manifest = json.load(f)
        self.assertIn("input_sha256", manifest)
        self.assertIn("output_sha256", manifest)

        with open(os.path.join(self.outdir, "counts.json")) as f:
            counts_json = json.load(f)
        self.assertIn("cells", counts_json)
        self.assertIn("contamination_ceiling", counts_json)
        # No contaminated records in this fixture (all datestamp == created).
        self.assertEqual(counts_json["contamination_ceiling"]["cs.CL"]["pre2023_datestamp_post2023_count"], 0)
        self.assertEqual(counts_json["contamination_ceiling"]["cs.CL"]["pre2023_kept_count"], 1)
        self.assertEqual(counts_json["contamination_ceiling"]["cs.CL"]["share"], 0.0)

    def test_contamination_ceiling_counts_post_launch_datestamp_touches(self):
        cs_records = "".join([
            # pre-2023 created, datestamp untouched -> not contaminated
            _record("2001.00001", "2020-01-02", "cs.CL", _long_abstract()),
            # pre-2023 created, datestamp touched post-launch -> contaminated
            _record("2001.00002", "2020-03-01", "cs.CL", _long_abstract(), datestamp="2023-05-01"),
            # pre-2023 created, datestamp touched post-launch -> contaminated
            _record("2001.00003", "2021-06-01", "cs.CL", _long_abstract(), datestamp="2024-01-15"),
            # post-2023 created -> irrelevant to the pre-2023 contamination ceiling
            _record("2001.00004", "2023-02-01", "cs.CL", _long_abstract(), datestamp="2023-02-01"),
        ])
        self._write_chunk("cs", "00001.xml.gz", _wrap(cs_records))
        self._write_chunk("math", "00001.xml.gz", _wrap(""))

        filter_corpus(self.raw_dir, self.outdir)
        with open(os.path.join(self.outdir, "counts.json")) as f:
            counts_json = json.load(f)

        cl_contamination = counts_json["contamination_ceiling"]["cs.CL"]
        self.assertEqual(cl_contamination["pre2023_kept_count"], 3)
        self.assertEqual(cl_contamination["pre2023_datestamp_post2023_count"], 2)
        self.assertAlmostEqual(cl_contamination["share"], 2 / 3)

    def test_refuses_nothing_special_but_output_is_deterministic(self):
        cs_records = _record("1501.00010", "2015-01-02", "math.NT", _long_abstract())
        self._write_chunk("cs", "00001.xml.gz", _wrap(cs_records))
        self._write_chunk("math", "00001.xml.gz", _wrap(""))

        filter_corpus(self.raw_dir, self.outdir)
        out1 = os.path.join(self.outdir, "math.NT.jsonl")
        with open(out1) as f:
            content1 = f.read()

        outdir2 = os.path.join(self.tmpdir, "out2")
        filter_corpus(self.raw_dir, outdir2)
        with open(os.path.join(outdir2, "math.NT.jsonl")) as f:
            content2 = f.read()

        self.assertEqual(content1, content2)


if __name__ == "__main__":
    unittest.main()
