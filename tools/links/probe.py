#!/usr/bin/env python3
"""Probe every URL an abstract declared and record whether it is publicly reachable
today. Writes data/probes.csv.

Two probe methods, per METHOD.md:
  * github.com/<owner>/<repo>  -> `git ls-remote` (the session's egress proxy answers
    403 for github.com over HTTP regardless of whether the target exists, so an HTTP
    probe there would measure the proxy, not the link)
  * everything else            -> HTTP GET following redirects; 200-399 = reachable

Outcomes: reachable / gone / indeterminate. `indeterminate` covers anything the
probe cannot distinguish from a local blockage (HTTP 403, 429, and transport
errors after a retry); those are reported as their own category and never counted
as rot.

Usage: python3 tools/links/probe.py <datadir> [--workers N]
"""
import csv, os, subprocess, sys, threading, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "field-research-link-probe/1.0 (research measurement; contact via frankbueltge.de)"
TIMEOUT = 25
INDETERMINATE_STATUS = {401, 403, 407, 429, 999}


def is_github(url):
    return urllib.parse.urlparse(url).netloc.lower() in ("github.com", "www.github.com")


def github_ref(url):
    """The branch or tag a link points into, if it names one (/tree/<ref>/...)."""
    parts = [s for s in urllib.parse.urlparse(url).path.split("/") if s]
    if len(parts) >= 4 and parts[2] in ("tree", "blob"):
        return parts[3]
    return None


def github_repo(url):
    p = urllib.parse.urlparse(url)
    if p.netloc.lower() not in ("github.com", "www.github.com"):
        return None
    parts = [s for s in p.path.split("/") if s]
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    if owner.lower() in ("orgs", "settings", "features", "about", "topics", "search"):
        return None
    return "https://github.com/%s/%s" % (owner, repo)


def probe_git(url):
    remote = github_repo(url)
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="echo", GCM_INTERACTIVE="never")
    try:
        r = subprocess.run(["git", "ls-remote", "--heads", remote], capture_output=True,
                           text=True, timeout=60, env=env)
    except subprocess.TimeoutExpired:
        return ("indeterminate", "git-timeout", remote)
    if r.returncode == 0:
        ref = github_ref(url)
        if ref:
            refs = {l.split("/")[-1] for l in (r.stdout or "").splitlines()}
            if ref not in refs:
                # the repository answers but the branch the link names is not among its heads;
                # tags are checked separately before this is called a miss
                try:
                    t = subprocess.run(["git", "ls-remote", "--tags", remote], capture_output=True,
                                       text=True, timeout=60, env=env)
                    tags = {l.split("/")[-1].replace("^{}", "") for l in (t.stdout or "").splitlines()}
                except subprocess.TimeoutExpired:
                    tags = set()
                if ref not in tags:
                    return ("gone", "git-ref-missing:" + ref, remote)
        return ("reachable", "git-ok", remote)
    err = (r.stderr or "").strip().splitlines()[-1] if r.stderr.strip() else "git-fail"
    low = err.lower()
    if "could not read username" in low or "not found" in low or "repository not found" in low \
       or "authentication failed" in low or "403" in low:
        return ("gone", "git-not-public", remote)
    return ("indeterminate", err[:120], remote)


def probe_http(url, attempt=0):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html,application/xhtml+xml,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            code = r.getcode()
            final = r.geturl()
        if 200 <= code < 400:
            return ("reachable", str(code), final)
        return ("gone", str(code), final)
    except urllib.error.HTTPError as e:
        if e.code in INDETERMINATE_STATUS:
            if attempt == 0:
                time.sleep(3)
                return probe_http(url, 1)
            return ("indeterminate", "http-%d" % e.code, url)
        return ("gone", "http-%d" % e.code, url)
    except Exception as e:
        if attempt == 0:
            time.sleep(2)
            return probe_http(url, 1)
        return ("indeterminate", type(e).__name__ + ":" + str(e)[:70], url)


def probe(url):
    if is_github(url) and not github_repo(url):
        # a profile or organisation address, not a repository: the git probe does not apply and
        # this session's egress cannot decide it over HTTP (the proxy answers for github.com
        # regardless of the target). Not decidable from here — never counted as rot.
        return (url, "none", "indeterminate", "github-not-a-repository-address", url)
    if github_repo(url):
        outcome, note, final = probe_git(url)
        return (url, "git", outcome, note, final)
    outcome, note, final = probe_http(url)
    return (url, "http", outcome, note, final)


def main():
    datadir = sys.argv[1]
    workers = 8
    if "--workers" in sys.argv:
        workers = int(sys.argv[sys.argv.index("--workers") + 1])
    urls = []
    with open(os.path.join(datadir, "urls.csv")) as fh:
        for row in csv.DictReader(fh):
            if row["url"] not in urls:
                urls.append(row["url"])
    print("%d distinct URLs to probe" % len(urls), flush=True)
    done, lock = [0], threading.Lock()

    def run(u):
        res = probe(u)
        with lock:
            done[0] += 1
            if done[0] % 25 == 0:
                print("  %d/%d" % (done[0], len(urls)), flush=True)
        return res

    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(run, urls))
    with open(os.path.join(datadir, "probes.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["url", "method", "outcome", "note", "final_url", "probed_utc"])
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for url, method, outcome, note, final in results:
            w.writerow([url, method, outcome, note, final, stamp])
    from collections import Counter
    print(Counter(r[2] for r in results))


if __name__ == "__main__":
    main()
