#!/usr/bin/env python3
"""Minimal PDF text extractor: FlateDecode streams, Tj/TJ operators.

Written for this session because the environment's pypdf could not load
(`cryptography` broken) and because keeping extraction inside our own code
means no model sits between a source and a quoted passage.

Handles the common case only: uncompressed or Flate-compressed content
streams with literal-string text operators. Does not handle encryption,
CID fonts with custom encodings, or Type3. Where it fails it says so
rather than returning plausible text.
"""
import re, sys, zlib

def streams(raw: bytes):
    for m in re.finditer(rb"stream\r?\n", raw):
        start = m.end()
        end = raw.find(b"endstream", start)
        if end == -1:
            continue
        blob = raw[start:end]
        try:
            yield zlib.decompress(blob)
        except zlib.error:
            try:
                yield zlib.decompressobj().decompress(blob)
            except zlib.error:
                yield blob  # possibly uncompressed

ESC = {b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b",
       b"f": b"\f", b"(": b"(", b")": b")", b"\\": b"\\"}

def literals(content: bytes):
    """Yield (text, is_TJ_gap) tokens from a content stream."""
    out, i, n = [], 0, len(content)
    while i < n:
        c = content[i:i + 1]
        if c == b"(":
            buf, depth, i = [], 1, i + 1
            while i < n and depth:
                ch = content[i:i + 1]
                if ch == b"\\":
                    nxt = content[i + 1:i + 2]
                    if nxt in ESC:
                        buf.append(ESC[nxt]); i += 2; continue
                    if nxt.isdigit():
                        oct_ = content[i + 1:i + 4]
                        m = re.match(rb"[0-7]{1,3}", oct_)
                        if m:
                            buf.append(bytes([int(m.group(), 8) & 0xFF]))
                            i += 1 + len(m.group()); continue
                    i += 2; continue
                if ch == b"(":
                    depth += 1
                elif ch == b")":
                    depth -= 1
                    if not depth:
                        i += 1; break
                buf.append(ch); i += 1
            out.append(b"".join(buf))
        elif c == b"T" and content[i:i + 2] in (b"TJ", b"Tj"):
            out.append(b"\x00SP"); i += 2
        elif c in b"-0123456789" and out and out[-1] not in (b"\x00SP", b"\x00NL"):
            # Inside a TJ array the numbers are kerning offsets in thousandths
            # of an em. A large negative offset is how a PDF writes a word
            # space, so words are only separated if we read them.
            m = re.match(rb"-?\d+(\.\d+)?", content[i:i + 12])
            if m:
                try:
                    if float(m.group()) <= -100:
                        out.append(b"\x00SP")
                except ValueError:
                    pass
                i += len(m.group()); continue
            i += 1
        elif content[i:i + 2] in (b"Td", b"TD", b"T*"):
            out.append(b"\x00NL"); i += 2
        else:
            i += 1
    return out

def extract(raw: bytes) -> str:
    parts = []
    for s in streams(raw):
        # A content stream has text operators inside BT/ET blocks. Image and
        # font streams can contain the bytes "Tj" by chance, so require the
        # block markers and a mostly-printable body before treating it as text.
        if b"BT" not in s or b"ET" not in s:
            continue
        if b"Tj" not in s and b"TJ" not in s:
            continue
        sample = s[:4000]
        printable = sum(1 for b in sample if 9 <= b <= 13 or 32 <= b <= 126)
        if not sample or printable / len(sample) < 0.55:
            continue
        for tok in literals(s):
            if tok == b"\x00SP":
                parts.append(" ")
            elif tok == b"\x00NL":
                parts.append("\n")
            else:
                parts.append(tok.decode("latin-1"))
    text = "".join(parts)
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text

if __name__ == "__main__":
    raw = open(sys.argv[1], "rb").read()
    txt = extract(raw)
    if len(txt.strip()) < 200:
        sys.stderr.write("EXTRACTION FAILED (under 200 chars) for %s\n" % sys.argv[1])
        sys.exit(3)
    sys.stdout.write(txt)
