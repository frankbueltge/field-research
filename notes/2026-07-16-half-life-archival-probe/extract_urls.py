#!/usr/bin/env python3
"""Citation-URL extraction from FA's 827-page report PDF — session 41 (2026-07-16).

Input (NOT committed — 218 MB; pin below):
  FA_A-Spatial-Analysis-of-the-Israeli-militarys-conduct-in-Gaza-since-October-2023.pdf
  from https://content.forensic-architecture.org/wp-content/uploads/2024/10/
  sha256 af85fb6511be823e922442731751b0f311c354b6dc846ad0d841c91d73475d6f

Two passes over the extracted text layer (pypdf):
  A. OSCOLA angle-bracket citations `<https://...>` — all strata; wrap hyphens
     (" -" at line breaks) and wrap whitespace removed inside the brackets.
  B. Bare URLs for the two hinge strata only (X/Twitter tweet URLs and Telegram
     t.me URLs), which also occur outside angle brackets in footnotes and in the
     per-incident appendix tables (ID · date · coordinates · source URL · rating);
     these patterns are self-terminating (/status/<digits>; /<channel>/<post-id>)
     and therefore reconstructable across line wraps. Bare URLs of other strata
     (news/org citations without angle brackets) are NOT captured — stated as a
     known undercount in the README.

Output: urls.json — [{url, source: "angle-bracket"|"bare/table", stratum}], deduped
(twitter.com→x.com and www-stripping normalization for the dedup key only).
"""
import re, json, sys
from urllib.parse import urlparse
from pypdf import PdfReader

def stratum(u):
    d = urlparse(u).netloc.lower().removeprefix("www.")
    if d in ("x.com", "twitter.com", "t.co", "mobile.twitter.com"): return "x-twitter"
    if d in ("t.me", "telegram.me"): return "telegram"
    if d in ("facebook.com", "m.facebook.com", "instagram.com", "tiktok.com",
             "youtube.com", "youtu.be"): return "social-other"
    if "archive.org" in d or d in ("archive.ph", "archive.today", "perma.cc"): return "pre-archived"
    if d.endswith("forensic-architecture.org"): return "fa-self"
    return "news-org-other"

def norm(u):
    return u.replace("https://twitter.com/", "https://x.com/").replace("https://www.", "https://")

pdf = sys.argv[1] if len(sys.argv) > 1 else "fa-report.pdf"
text = "\n".join((p.extract_text() or "") for p in PdfReader(pdf).pages)

out, seen = [], set()

# Pass A — angle-bracket citations
for m in re.finditer(r'<\s*(https?://[^<>]{2,800}?)\s*>', text, flags=re.S):
    u = re.sub(r'\s+-\s*', '', m.group(1))
    u = re.sub(r'\s+', '', u)
    if norm(u) not in seen:
        seen.add(norm(u))
        out.append({"url": u, "source": "angle-bracket", "stratum": stratum(u)})

# Pass B — bare/table URLs, hinge strata only
for m in re.finditer(
        r'https?:\s*//\s*(?:www\.)?(?:x\.com|twitter\.com|mobile\.twitter\.com)\s*/\s*@?'
        r'([A-Za-z0-9_][A-Za-z0-9_\s]{0,20}?)\s*/\s*status(?:es)?\s*/\s*(\d[\d\s]{6,24}\d)', text):
    handle = re.sub(r'\s+', '', m.group(1))
    tid = re.sub(r'\s+', '', m.group(2))
    if 1 <= len(handle) <= 15 and 8 <= len(tid) <= 20:
        u = f"https://x.com/{handle}/status/{tid}"
        if norm(u) not in seen:
            seen.add(norm(u))
            out.append({"url": u, "source": "bare/table", "stratum": "x-twitter"})

for m in re.finditer(r'https?:\s*//\s*(?:www\.)?t\.me\s*/', text):
    tail = text[m.end():m.end() + 80]
    tail = re.sub(r'\s*-\s*\n\s*', '', tail)
    tail = re.sub(r'\s+', '', tail)
    mm = re.match(r'([A-Za-z0-9_+]{3,32})(/\d{1,10})?', tail)
    if mm:
        u = "https://t.me/" + mm.group(1) + (mm.group(2) or "")
        if norm(u) not in seen:
            seen.add(norm(u))
            out.append({"url": u, "source": "bare/table", "stratum": "telegram"})

json.dump(out, open("urls.json", "w"), indent=0)
print(len(out), "unique URLs")
