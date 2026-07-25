import os
import shutil
import tempfile
import unittest

import _pathfix  # noqa: F401
from harvest import (
    _initial_url,
    _resumption_url,
    _extract_resumption_token,
    _check_outdir_empty,
    ENDPOINT,
    METADATA_PREFIX,
    FROM_DATE,
)

OAI_NS = "http://www.openarchives.org/OAI/2.0/"


class TestUrlBuilding(unittest.TestCase):
    def test_initial_url_has_fixed_parameters(self):
        url = _initial_url("cs")
        self.assertTrue(url.startswith(ENDPOINT + "?"))
        self.assertIn("verb=ListRecords", url)
        self.assertIn(f"metadataPrefix={METADATA_PREFIX}", url)
        self.assertIn("set=cs", url)
        self.assertIn(f"from={FROM_DATE}", url)

    def test_resumption_url_only_carries_verb_and_token(self):
        token = "abc/def+123==xyz"
        url = _resumption_url(token)
        self.assertIn("verb=ListRecords", url)
        self.assertIn("resumptionToken=", url)
        # token content is percent-encoded, not left verbatim in the query string,
        # but must round-trip byte-for-byte.
        import urllib.parse
        parsed = urllib.parse.parse_qs(url.split("?", 1)[1])
        self.assertEqual(parsed["resumptionToken"][0], token)
        self.assertNotIn("metadataPrefix", url)
        self.assertNotIn("set=", url)


class TestExtractResumptionToken(unittest.TestCase):
    def test_token_present(self):
        xml = f"""<OAI-PMH xmlns="{OAI_NS}">
          <ListRecords>
            <record></record>
            <resumptionToken>tok123</resumptionToken>
          </ListRecords>
        </OAI-PMH>""".encode("utf-8")
        token, error = _extract_resumption_token(xml)
        self.assertEqual(token, "tok123")
        self.assertIsNone(error)

    def test_empty_token_means_done(self):
        xml = f"""<OAI-PMH xmlns="{OAI_NS}">
          <ListRecords>
            <record></record>
            <resumptionToken></resumptionToken>
          </ListRecords>
        </OAI-PMH>""".encode("utf-8")
        token, error = _extract_resumption_token(xml)
        self.assertIsNone(token)
        self.assertIsNone(error)

    def test_no_token_element_means_done(self):
        xml = f"""<OAI-PMH xmlns="{OAI_NS}">
          <ListRecords>
            <record></record>
          </ListRecords>
        </OAI-PMH>""".encode("utf-8")
        token, error = _extract_resumption_token(xml)
        self.assertIsNone(token)
        self.assertIsNone(error)

    def test_oai_error_detected(self):
        xml = f"""<OAI-PMH xmlns="{OAI_NS}">
          <error code="badResumptionToken">token expired</error>
        </OAI-PMH>""".encode("utf-8")
        token, error = _extract_resumption_token(xml)
        self.assertIsNone(token)
        self.assertIn("badResumptionToken", error)


class TestOutdirGuard(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_empty_or_missing_dir_is_ok(self):
        missing = os.path.join(self.tmpdir, "does-not-exist")
        _check_outdir_empty(missing)  # must not raise
        empty = os.path.join(self.tmpdir, "empty")
        os.makedirs(empty)
        _check_outdir_empty(empty)  # must not raise

    def test_non_empty_dir_refuses(self):
        nonempty = os.path.join(self.tmpdir, "nonempty")
        os.makedirs(nonempty)
        with open(os.path.join(nonempty, "00001.xml.gz"), "wb") as f:
            f.write(b"x")
        with self.assertRaises(SystemExit):
            _check_outdir_empty(nonempty)


if __name__ == "__main__":
    unittest.main()
