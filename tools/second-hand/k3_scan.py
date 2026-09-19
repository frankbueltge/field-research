#!/usr/bin/env python3
"""K3, limbs (a) and (b): an independent implementation must be pure standard
library and must make no network call and no model call. Session 164.

A source scan, not a sandbox. It reads the module text and reports every import
and every name that would reach a network or a model. What it cannot do is prove
absence, and the page says so where its result appears.
"""
import ast
import json
import os
import sys

STDLIB = set(getattr(sys, "stdlib_module_names", ()))
# Repaired 2026-09-19, after the first run failed all four modules on a SUBSTRING
# scan. It matched "curl" inside "curly quotes" — the specification's own wording —
# and "http" inside the MPL-2.0 and EPL-2.0 operative phrases, which are the texts
# under identification. Both false positives came from the phenomenon, not the
# apparatus, which is the one thing a kill condition must never do. The failing run
# is kept at data/k3-run1-defective.json.
#
# The repair reads the syntax tree instead of the characters: a module reaches the
# network or a model only by importing something, or by reaching for one of the
# dynamic escapes below.
FORBIDDEN_MODULES = {"urllib", "urllib2", "http", "httplib", "socket", "ssl", "requests",
                     "httpx", "aiohttp", "ftplib", "telnetlib", "smtplib", "xmlrpc",
                     "asyncio", "subprocess", "multiprocessing", "ctypes", "openai",
                     "anthropic", "google", "transformers", "torch", "litellm", "ollama",
                     "boto3", "pycurl"}
# Run 2 of this check failed all four modules again, on `re.compile`: the call name
# was matched without looking at what it was called ON. Every text-matching rule in
# this corpus compiles a regular expression, so that too was the phenomenon. Run 2 is
# kept at data/k3-run2-defective.json. Twice in one night, in the apparatus written to
# guard against exactly this.
BARE_CALLS = {"__import__", "eval", "exec", "compile", "open"}      # builtins only
ESCAPE_ATTRS = {"system", "popen", "urlopen", "check_output", "spawnl", "spawnv",
                "execv", "execvp", "connect", "socket"}


def scan(path):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imports.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])
    nonstd = sorted(m for m in imports if m not in STDLIB)
    bad_imports = sorted(imports & FORBIDDEN_MODULES)
    def root_of(node):
        while isinstance(node, ast.Attribute):
            node = node.value
        return node.id if isinstance(node, ast.Name) else None

    called = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if isinstance(f, ast.Name) and f.id in BARE_CALLS:
            called.add(f.id)
        elif isinstance(f, ast.Attribute):
            if root_of(f) in FORBIDDEN_MODULES or f.attr in ESCAPE_ATTRS:
                called.add(f"{root_of(f)}.{f.attr}")
    hits = sorted(bad_imports) + sorted("call:" + c for c in called)
    has_score = any(isinstance(n, ast.FunctionDef) and n.name == "score"
                    for n in tree.body)
    return {
        "path": os.path.basename(path),
        "bytes": len(src.encode()),
        "sha256": __import__("hashlib").sha256(src.encode()).hexdigest(),
        "imports": sorted(imports),
        "non_stdlib_imports": nonstd,
        "forbidden_name_hits": hits,
        "module_level_score_def": has_score,
        "pass": not nonstd and not hits and has_score,
    }


if __name__ == "__main__":
    d = sys.argv[1]
    out = [scan(os.path.join(d, f)) for f in sorted(os.listdir(d)) if f.endswith(".py")]
    res = {"note": "K3 limbs (a) and (b): a syntax-tree scan. It cannot prove absence; it "
                   "reports every import and every dynamic escape it finds. Run 1 of this "
                   "check was a substring scan and failed all four modules on the word "
                   "'curly' and on the http URLs inside the MPL-2.0 and EPL-2.0 licence "
                   "texts; run 2 failed them again on re.compile. Both are kept beside "
                   "the artifact, at data/k3-run1-defective.json and "
                   "data/k3-run2-defective.json.",
           "n_scanned": len(out), "all_pass": all(o["pass"] for o in out), "modules": out}
    if len(sys.argv) > 2:
        json.dump(res, open(sys.argv[2], "w"), indent=1)
    print(json.dumps(res, indent=1))
