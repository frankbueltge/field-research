#!/usr/bin/env python3
"""arXiv HTML (LaTeXML) -> plain text for the 09-23 rule. Session 171, 2026-09-26.

PREREGISTRATION.md §2: the body from the first section to the bibliography, captions
included; the abstract, the bibliography and every appendix after it excluded. Each
paragraph, caption and heading is one line; each table row one `| a | b |` line, so the
rule's amendment A-3 treats a row as one sentence. Inline math is replaced by its LaTeX
alt text with `\\%` read as `%` and braces and simple commands dropped.
No model, no network.
"""
import html
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "figcaption", "li", "div", "caption"}
SKIP_CLASSES = ("ltx_bibliography", "ltx_appendix", "ltx_abstract", "ltx_authors",
                "ltx_title_document", "ltx_page_footer", "ltx_role_footnote_mark")


def tex_to_text(alt):
    t = alt.replace("\\%", "%")
    t = re.sub(r"\\(?:mathbf|mathrm|text|textbf|mathit|operatorname|textit|bm)\s*", "", t)
    t = re.sub(r"\\(?:,|;|!|:| )", " ", t)
    t = re.sub(r"\\(?:pm)", "±", t)
    t = re.sub(r"\\(?:times)", "×", t)
    t = re.sub(r"\\(?:approx|sim)", "≈", t)
    t = re.sub(r"\\(?:leq|le)", "≤", t)
    t = re.sub(r"\\(?:geq|ge)", "≥", t)
    t = re.sub(r"\\[A-Za-z]+", " ", t)
    t = t.replace("{", "").replace("}", "").replace("^", "").replace("$", "")
    return re.sub(r"\s+", " ", t).strip()


class Body(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, skipping, is_row)
        self.lines = []
        self.buf = []
        self.row = None
        self.cell = None
        self.math_depth = 0
        self.started = False
        self.skip_depth = 0

    def _flush(self):
        s = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if s and self.started and not self.skip_depth:
            self.lines.append(s)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class") or ""
        skipping = any(c in cls.split() for c in SKIP_CLASSES)
        if tag == "section" and "ltx_section" in cls.split():
            self.started = True
        self.stack.append((tag, skipping))
        if skipping:
            self.skip_depth += 1
            return
        if tag == "math":
            self.math_depth += 1
            if self.row is None or self.cell is not None:
                self._text(" " + tex_to_text(a.get("alttext", "")) + " ")
            return
        if tag == "tr":
            self._flush()
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
        elif tag in BLOCK or tag == "br":
            self._flush()

    def handle_endtag(self, tag):
        while self.stack:
            t, skipping = self.stack.pop()
            if skipping:
                self.skip_depth -= 1
            if t == "math" and not skipping and not self.skip_depth:
                self.math_depth -= 1
            if t == "math" and not skipping and self.skip_depth:
                pass
            if not skipping and not self.skip_depth:
                if t in ("td", "th") and self.row is not None and self.cell is not None:
                    self.row.append(re.sub(r"\s+", " ", "".join(self.cell)).strip())
                    self.cell = None
                elif t == "tr" and self.row is not None:
                    if self.started and any(self.row):
                        self.lines.append("| " + " | ".join(self.row) + " |")
                    self.row = None
                elif t in BLOCK:
                    self._flush()
            if t == tag:
                break

    def _text(self, s):
        if self.skip_depth:
            return
        if self.cell is not None:
            self.cell.append(s)
        elif self.row is None:
            self.buf.append(s)

    def handle_data(self, data):
        if self.math_depth:
            return                                    # alt text already emitted
        self._text(data)


MATH_RE = re.compile(r'<math\b[^>]*?alttext="([^"]*)"[^>]*>.*?</math>', re.S)


def extract(doc):
    doc = MATH_RE.sub(lambda m: " " + html.escape(tex_to_text(html.unescape(m.group(1)))) + " ", doc)
    p = Body()
    p.feed(doc)
    p._flush()
    out, prev = [], None
    for line in p.lines:
        if line != prev:
            out.append(line)
        prev = line
    return "\n".join(out)


if __name__ == "__main__":
    print(extract(open(sys.argv[1], encoding="utf-8").read()))
