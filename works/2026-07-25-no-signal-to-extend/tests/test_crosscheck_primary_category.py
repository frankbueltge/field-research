"""Unit tests for the D1 stratum-rule cross-check parser."""

import unittest

import _pathfix  # noqa: F401  (puts scripts/ on sys.path, repo convention)

from crosscheck_primary_category import entries


ENTRY_TEMPLATE = """<entry>
  <id>http://arxiv.org/abs/{ident}v1</id>
  <title>t</title>
  {cats}
  <arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom" term="{primary}" scheme="s"/>
</entry>"""


def feed(*entry_xml):
    return "<feed>" + "".join(entry_xml) + "</feed>"


def one(ident, cat_terms, primary):
    cats = "\n  ".join('<category term="%s" scheme="s"/>' % c for c in cat_terms)
    return ENTRY_TEMPLATE.format(ident=ident, cats=cats, primary=primary)


class EntryParsingTest(unittest.TestCase):
    def test_extracts_id_first_category_and_primary(self):
        parsed = list(entries(feed(one("2101.00001", ["cs.CL", "cs.AI"], "cs.CL"))))
        self.assertEqual(parsed, [("2101.00001v1", "cs.CL", "cs.CL")])

    def test_first_category_is_document_order_not_alphabetical(self):
        parsed = list(entries(feed(one("2101.00002", ["cs.CV", "cs.AI", "cs.CL"], "cs.CV"))))
        self.assertEqual(parsed[0][1], "cs.CV")

    def test_disagreement_is_visible(self):
        parsed = list(entries(feed(one("2101.00003", ["cs.AI", "cs.CL"], "cs.CL"))))
        _, first, primary = parsed[0]
        self.assertNotEqual(first, primary)

    def test_multiple_entries_are_separated(self):
        parsed = list(entries(feed(
            one("2101.00004", ["math.NT"], "math.NT"),
            one("2101.00005", ["cs.CL"], "cs.CL"),
        )))
        self.assertEqual(len(parsed), 2)
        self.assertEqual([p[1] for p in parsed], ["math.NT", "cs.CL"])

    def test_missing_primary_category_yields_none(self):
        xml = "<entry><id>http://arxiv.org/abs/2101.00006v1</id>" \
              '<category term="cs.CL" scheme="s"/></entry>'
        parsed = list(entries(feed(xml)))
        self.assertEqual(parsed[0][2], None)
        self.assertEqual(parsed[0][1], "cs.CL")


if __name__ == "__main__":
    unittest.main()
