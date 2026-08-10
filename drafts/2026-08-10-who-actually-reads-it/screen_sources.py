#!/usr/bin/env python3
"""Mechanical screen over every fetched candidate source. This produces LEADS ONLY;
every cell that reaches RESULT-1.md is confirmed by reading the file by hand."""
import os, re, json

PATTERNS = {
  "raw_file_host":   r"data\.gdeltproject\.org",
  "doc_api_host":    r"api\.gdeltproject\.org",
  "masterfilelist":  r"masterfilelist",
  "md5_token":       r"\bmd5\b",
  "hashlib":         r"hashlib",
  "digest_compare":  r"(hexdigest|md5sum|checkMD5|digest\(\))",
  "status_404":      r"404",
  "raise_for_status":r"raise_for_status",
  "try_except":      r"except\s+\w*(Error|Exception)",
  "timedelta_grid":  r"(timedelta\(minutes\s*=\s*15|15\s*\*\s*60|'15min'|\"15min\"|freq\s*=\s*['\"]15)",
  "zipfile":         r"(zipfile|ZipFile|unzip)",
}
EXT = (".py", ".R", ".r", ".rs", ".toml", ".cfg", ".txt", ".md", ".Rd")

rows = []
for pkg in sorted(os.listdir("src")):
    hits = {k: [] for k in PATTERNS}
    nfiles = 0
    for root, _, files in os.walk(os.path.join("src", pkg)):
        for f in files:
            if not f.endswith(EXT):
                continue
            p = os.path.join(root, f)
            nfiles += 1
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for k, pat in PATTERNS.items():
                for m in re.finditer(pat, t, re.I):
                    line = t[:m.start()].count("\n") + 1
                    hits[k].append(f"{os.path.relpath(p,'src')}:{line}")
                    break
    rows.append({"package": pkg, "text_files": nfiles,
                 **{k: hits[k] for k in PATTERNS}})
json.dump(rows, open("screen-leads.json", "w"), indent=1)

cols = ["raw_file_host", "masterfilelist", "md5_token", "digest_compare", "status_404", "timedelta_grid"]
print(f'{"package":20}' + "".join(f'{c[:14]:16}' for c in cols))
for r in rows:
    print(f'{r["package"]:20}' + "".join(f'{("Y" if r[c] else "-"):16}' for c in cols))
