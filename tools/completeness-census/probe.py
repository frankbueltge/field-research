#!/usr/bin/env python3
"""Access probe: one real GET per candidate URL, recorded verbatim.

Records HTTP status, final URL after redirects, content type, byte count and
a sha256 of the body. Bodies are saved for extraction. No judgement here:
whether a body is the full text or a paywall page is decided by hand, from
the body, and recorded in the coding record.
"""
import hashlib, json, os, subprocess, sys, time

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
OUT = sys.argv[2] if len(sys.argv) > 2 else "bodies"
os.makedirs(OUT, exist_ok=True)

cands = json.load(open(sys.argv[1]))["candidates"]
rows = []
for c in cands:
    for n, url in enumerate(c["urls"]):
        path = os.path.join(OUT, "%s-%d.body" % (c["id"], n))
        fmt = "%{http_code}\t%{url_effective}\t%{content_type}\t%{size_download}"
        p = subprocess.run(
            ["curl", "-sSL", "--max-time", "70", "-A", UA, "-o", path, "-w", fmt, url],
            capture_output=True, text=True)
        if p.returncode != 0 or "\t" not in p.stdout:
            rows.append({"id": c["id"], "url": url, "status": None,
                         "error": (p.stderr or "curl exit %d" % p.returncode).strip()[:300],
                         "final_url": None, "content_type": None, "bytes": 0, "sha256": None})
            print("%-24s %-6s %s" % (c["id"], "ERR", (p.stderr or "").strip()[:70]))
            continue
        code, final, ctype, size = p.stdout.split("\t")
        body = open(path, "rb").read()
        rows.append({"id": c["id"], "url": url, "status": int(code), "final_url": final,
                     "content_type": ctype, "bytes": int(size),
                     "sha256": hashlib.sha256(body).hexdigest(), "body_file": path})
        print("%-24s %-6s %-9s %s" % (c["id"], code, size, final[:78]))
        time.sleep(1)

json.dump({"probed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "probes": rows},
          open(os.path.join(OUT, "..", "probes.json"), "w"), indent=1)
