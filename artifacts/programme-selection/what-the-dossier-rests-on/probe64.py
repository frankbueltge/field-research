"""Study 64, step 2: one anonymous request per dataset named in a candidate's Reach line.
Usage: python3 -I probe64.py <scratch-dir>   Writes probes64.out.json beside this script.
Classes: delivers = data bytes (JSON/CSV/zip/xlsx) with no key; gated = 401, or 403 with a stated auth wall, or a form;
refused = 403 with no stated reason;
portal = an HTML page and no data at this address; error = network failure or 4xx/5xx other than 401/403."""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; S = Path(sys.argv[1]); S.mkdir(parents=True, exist_ok=True)
P = json.loads((HERE / 'probes64.json').read_text())['probes']; out = []
for i, p in enumerate(P):
    f = S / f'q{i}.bin'
    a = ['curl', '-sS', '-L', '--max-time', '40', '-A', 'Mozilla/5.0 (X11; Linux x86_64) research-check', '-o', str(f),
         '-w', '%{http_code}\t%{size_download}\t%{content_type}']
    if p.get('method') == 'POST': a += ['-X', 'POST', '-H', 'Content-Type: application/json', '-d', '{"inputs":{}}']
    if p.get('method') == 'RANGE': a += ['-r', '0-4095']
    r = subprocess.run(a + [p['url']], capture_output=True, text=True)
    code, size, ctype = (r.stdout.split('\t') + ['', '', ''])[:3]
    head = f.read_bytes()[:200] if f.exists() else b''
    datalike = head[:2] == b'PK' or head[:1] in (b'{', b'[') or 'csv' in ctype or 'json' in ctype or 'spreadsheet' in ctype or 'zip' in ctype
    authwall = any(w in head.lower() for w in (b'authentication', b'token required', b'permission denied', b'login'))
    if code == '401' or (code == '403' and authwall): cls = 'gated'
    elif code == '403': cls = 'refused'
    elif code in ('200', '206') and datalike and b'error' not in head[:40].lower(): cls = 'delivers'
    elif code in ('200', '206') and 'html' in ctype: cls = 'portal'
    else: cls = 'error'
    if p.get("manual_class") and code == "200": cls = p["manual_class"]
    out.append({**p, 'status': code, 'bytes': int(size or 0), 'type': ctype, 'class': cls,
                'head': head[:100].decode('utf-8', 'replace'), 'curl_error': r.stderr.strip()[:120]})
    print(i, p['cand'], p['name'], code, cls)
(HERE / 'probes64.out.json').write_text(json.dumps(out, indent=1, ensure_ascii=False))
