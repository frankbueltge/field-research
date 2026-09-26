import json, os, sys
from playwright.sync_api import sync_playwright
ART = sys.argv[1]
url = "file://" + os.path.join(ART, "index.html")
out = {"note": "Rendered in a real browser from the filesystem, scripting on and off. "
               "The page carries no JavaScript, so the two must be identical.", "widths": []}
with sync_playwright() as p:
    for js in (True, False):
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for w in (390, 768, 1280):
            ctx = b.new_context(viewport={"width": w, "height": 900}, java_script_enabled=js)
            pg = ctx.new_page()
            errs, reqs = [], []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("request", lambda r: reqs.append(r.url) if not r.url.startswith("file:") else None)
            pg.goto(url, wait_until="load")
            m = pg.evaluate("({sw: document.documentElement.scrollWidth,"
                            " iw: window.innerWidth,"
                            " tables: document.querySelectorAll('table').length,"
                            " rows: document.querySelectorAll('tbody tr').length,"
                            " controls: document.querySelectorAll("
                            "'input,select,button,textarea,details,[onclick]').length,"
                            " text: document.body.innerText.length})")
            out["widths"].append({"width": w, "javascript": js, "scroll_width": m["sw"],
                                  "inner_width": m["iw"],
                                  "horizontal_overflow": m["sw"] > m["iw"],
                                  "tables": m["tables"], "table_rows": m["rows"],
                                  "interactive_controls": m["controls"],
                                  "text_chars": m["text"],
                                  "console_errors": len(errs), "network_requests": len(reqs)})
            ctx.close()
        b.close()
json.dump(out, open(os.path.join(ART, "data", "render-check.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
for r in out["widths"]:
    print(f"  js={str(r['javascript']):5} w={r['width']:>5}  overflow={r['horizontal_overflow']}"
          f"  rows={r['table_rows']}  controls={r['interactive_controls']}"
          f"  errors={r['console_errors']}  requests={r['network_requests']}"
          f"  text={r['text_chars']}")
