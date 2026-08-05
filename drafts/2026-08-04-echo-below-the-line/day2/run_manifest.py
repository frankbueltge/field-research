#!/usr/bin/env python3
"""Record which bytes produced the day-2 numbers.

The pre-registration promises that the two measurement scripts run UNMODIFIED at their
session-89 committed state. Because those scripts anchor their input and output paths on
their own file location, running them over a second day's pool means running a COPY of
them in this directory. This script records the sha256 of every copy beside the sha256 of
the original, so "unmodified" is a checkable statement rather than an assurance.
"""
import hashlib, json, os, time

PAIRS = [
    ('measure_echo.py', '../scripts/measure_echo.py', 'scripts/measure_echo.py'),
    ('decompose_drop.py', '../scripts/decompose_drop.py', 'scripts/decompose_drop.py'),
]

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

out = {'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'scripts': [], 'inputs': {}}
for name, original, copy in PAIRS:
    a, b = sha(original), sha(copy)
    out['scripts'].append({'script': name, 'sha256_session_89_original': a,
                           'sha256_copy_run_here': b, 'identical': a == b})
for f in sorted(os.listdir('provenance')):
    if f.startswith('gdelt-') and f.endswith('.json'):
        out['inputs'][f] = sha(os.path.join('provenance', f))
out['all_scripts_identical'] = all(s['identical'] for s in out['scripts'])
json.dump(out, open('RUN-MANIFEST.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
