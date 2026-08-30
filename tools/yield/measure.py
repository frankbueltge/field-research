#!/usr/bin/env python3
"""Yield of an automated research loop — the measurement.

Reads this repository's own git history and journal headings and writes the dataset
behind artifacts/cycle-001/2026-08-30-yield-of-a-loop/.

Definitions are fixed in that directory's METHOD.md, written before this ran.
Run from the repository root on a full (non-shallow) clone:

    python3 tools/yield/measure.py
"""

import csv
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

OUT = "artifacts/cycle-001/2026-08-30-yield-of-a-loop/data"

# --- area classification (METHOD.md §"Definitions") -------------------------

REGISTER_TOP = {
    "WORKBOARD.md", "FIELD.md", "REQUESTS.md", "REQUESTS-ARCHIVE.md", "DAILY-LINE.md",
    "PROTOCOL.md", "README.md", "BULLETIN.md", "SEASON.md", "SITE-API.md", "LICENSE.md",
    "chronicle.json", "layer2-queue.json",
}


PROSE = {".md"}
DATA = {".json", ".csv", ".ndjson", ".txt", ".tsv", ".jsonl"}
CODE = {".py", ".js", ".mjs", ".astro", ".sh", ".html", ".css", ".yml", ".yaml"}


def kind(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in PROSE:
        return "prose"
    if ext in DATA:
        return "data"
    if ext in CODE:
        return "code"
    return "other"


def area(path):
    if path.startswith(("works/", "presentations/", "closing-report/", "artifacts/")):
        return "output"
    if path.startswith("drafts/"):
        return "drafts"
    if path.startswith(("journal/", "memory/", "notes/", "archive/")):
        return "register"
    if path.startswith(("tools/", ".github/")):
        return "tooling"
    if path.startswith("field-feedback/"):
        return "feedback"
    if "/" not in path and path in REGISTER_TOP:
        return "register"
    return "other"


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True,
                          check=True).stdout


# --- 1. session index from the journal's own headings ----------------------

# The practice's own index uses two schemes. On its first day the journal numbers nine
# invocations 01..09 and calls only the ninth "collective session 01"; from 2026-07-02 the
# canonical number is the collective one. So: a heading that states a collective session
# number always wins, and a bare "# Session NN — DATE" heading counts as collective session
# NN everywhere except in the first day's file, where it is a day-local invocation.
# This ambiguity is a fact about the record and is reported, not smoothed away.
FIRST_DAY_FILE = "2026-07-01.md"

P_COLLECTIVE = re.compile(r"collective session\s+(?P<num>\d+)", re.I)
P_DATE = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})")
P_BARE = re.compile(r"^#+\s+Session\s+(?P<num>\d+)\s+[—-]\s+(?P<date>\d{4}-\d{2}-\d{2})")


def session_index():
    seen, rows, dupes, local = {}, [], [], []
    for name in sorted(os.listdir("journal")):
        if not name.endswith(".md"):
            continue
        with open(os.path.join("journal", name), encoding="utf-8") as fh:
            for line in fh:
                if not line.startswith("# "):
                    continue
                head = line.strip()
                mc, md = P_COLLECTIVE.search(head), P_DATE.search(head)
                mb = P_BARE.match(head)
                if mc and md:
                    num, date = int(mc.group("num")), md.group("date")
                elif mb:
                    if name == FIRST_DAY_FILE:          # day-local invocation, not canonical
                        local.append({"invocation": int(mb.group("num")),
                                      "date": mb.group("date"), "heading": head})
                        continue
                    num, date = int(mb.group("num")), mb.group("date")
                else:
                    continue
                if num in seen:
                    dupes.append((num, date, head))
                    continue
                seen[num] = date
                rows.append({"session": num, "date": date, "journal_file": name,
                             "heading": head})
    rows.sort(key=lambda r: r["session"])
    return rows, dupes, local


# --- 2. per-commit line counts --------------------------------------------

def commits():
    raw = git("log", "--no-merges", "--date=short",
              "--pretty=format:\x01%H\x02%ad\x02%an\x02%s", "--numstat")
    out = []
    cur = None
    for line in raw.split("\n"):
        if line.startswith("\x01"):
            if cur:
                out.append(cur)
            h, d, a, s = line[1:].split("\x02", 3)
            cur = {"sha": h, "date": d, "author": a, "subject": s, "files": []}
        elif line.strip() and cur is not None:
            parts = line.split("\t")
            if len(parts) != 3:
                continue
            add, dele, path = parts
            add = 0 if add == "-" else int(add)          # "-" marks a binary file
            dele = 0 if dele == "-" else int(dele)
            cur["files"].append((add, dele, path))
    if cur:
        out.append(cur)
    return out


# --- 3. first appearance of every file ------------------------------------

def first_appearance():
    raw = git("log", "--no-merges", "--reverse", "--diff-filter=A", "--date=short",
              "--pretty=format:\x01%ad\x02%an", "--name-only")
    first, date, author = {}, None, None
    for line in raw.split("\n"):
        if line.startswith("\x01"):
            date, author = line[1:].split("\x02", 1)
        elif line.strip():
            first.setdefault(line.strip(), (date, author))
    return first


def main():
    if not os.path.isdir(".git"):
        sys.exit("run from the repository root")
    if os.path.exists(".git/shallow"):
        sys.exit("shallow clone: run `git fetch --unshallow` first")
    os.makedirs(OUT, exist_ok=True)

    sessions, dupes, local = session_index()
    per_day_sessions = defaultdict(int)
    for r in sessions:
        per_day_sessions[r["date"]] += 1

    first = first_appearance()

    # --- shipping events -------------------------------------------------
    # A work's slug carries the date the practice itself gave it. Git's first-appearance
    # date on main is NOT reliably the shipping date: on 2026-07-11 a recovery of lost
    # history re-added many earlier works in one commit. Both dates are published; the
    # timeline uses the slug date, which is the practice's own claim, and the divergence
    # is reported rather than smoothed.
    ship = {}
    for path, (date, author) in first.items():
        if path.startswith("works/") and path.count("/") >= 2:
            slug = path.split("/")[1]
            if slug not in ship or date < ship[slug][0]:
                ship[slug] = (date, author, path)
    standing = set(os.listdir("works")) if os.path.isdir("works") else set()
    withdrawn = sorted(set(ship) - standing)

    works = []
    for slug, (gdate, author, path) in ship.items():
        m = re.match(r"(\d{4}-\d{2}-\d{2})", slug)
        works.append({"slug": slug, "slug_date": m.group(1) if m else "",
                      "git_first_seen": gdate, "git_first_file": path,
                      "still_in_works": slug in standing})
    works.sort(key=lambda w: (w["slug_date"], w["slug"]))
    ship_by_day = defaultdict(int)
    for w in works:
        ship_by_day[w["slug_date"]] += 1

    # --- per-day activity -------------------------------------------------
    created = defaultdict(lambda: defaultdict(int))
    for path, (date, author) in first.items():
        created[date][area(path)] += 1

    cs = commits()
    lines = defaultdict(lambda: defaultdict(int))
    lines_kind = defaultdict(lambda: defaultdict(int))
    commits_by_day = defaultdict(int)
    author_commits, author_lines = defaultdict(int), defaultdict(int)
    for c in cs:
        commits_by_day[c["date"]] += 1
        author_commits[c["author"]] += 1
        for add, dele, path in c["files"]:
            lines[c["date"]][area(path)] += add
            lines_kind[c["date"]][f"{area(path)}:{kind(path)}"] += add
            author_lines[c["author"]] += add

    days = sorted(set(list(commits_by_day) + list(per_day_sessions)
                      + list(created) + list(ship_by_day)))
    AREAS = ["output", "drafts", "register", "tooling", "feedback", "other"]

    with open(f"{OUT}/daily.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "sessions", "commits", "works_shipped_slugdate",
                    "works_first_seen_in_git"]
                   + [f"files_new_{a}" for a in AREAS]
                   + [f"lines_added_{a}" for a in AREAS]
                   + ["lines_added_drafts_prose", "lines_added_drafts_data",
                      "lines_added_output_prose", "lines_added_output_data",
                      "lines_added_register_prose"])
        for d in days:
            w.writerow([d, per_day_sessions.get(d, 0), commits_by_day.get(d, 0),
                        ship_by_day.get(d, 0),
                        sum(1 for s, (dt, _, _) in ship.items() if dt == d)]
                       + [created[d].get(a, 0) for a in AREAS]
                       + [lines[d].get(a, 0) for a in AREAS]
                       + [lines_kind[d].get(k, 0) for k in
                          ("drafts:prose", "drafts:data", "output:prose", "output:data",
                           "register:prose")])

    with open(f"{OUT}/sessions.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["session", "date", "journal_file", "heading"])
        w.writeheader()
        w.writerows(sessions)

    with open(f"{OUT}/works.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["slug", "slug_date", "git_first_seen",
                                           "git_first_file", "still_in_works"])
        w.writeheader()
        w.writerows(works)

    def span(sel):
        sel_set = set(sel)
        s = sum(per_day_sessions.get(d, 0) for d in sel)
        shipped = sum(ship_by_day.get(d, 0) for d in sel)
        out = {
            "from": sel[0], "to": sel[-1], "days": len(sel), "sessions": s,
            "works_shipped": shipped,
            "yield_works_per_session": round(shipped / s, 4) if s else None,
            "files_new": {a: sum(created[d].get(a, 0) for d in sel) for a in AREAS},
            "lines_added": {a: sum(lines[d].get(a, 0) for d in sel) for a in AREAS},
            "lines_added_prose": {
                a: sum(lines_kind[d].get(f"{a}:prose", 0) for d in sel) for a in AREAS},
            "lines_added_data": {
                a: sum(lines_kind[d].get(f"{a}:data", 0) for d in sel) for a in AREAS},
        }
        out["commits"] = sum(commits_by_day.get(d, 0) for d in sel)
        return out

    last_ship = max(w["slug_date"] for w in works)
    after = [d for d in days if d > last_ship]

    # the single draft directory that carried the terminal arc
    ARM = "drafts/2026-08-11-the-arm-that-was-missing/"
    arm_files = [p for p in first if p.startswith(ARM)]
    arm_prose = sum(add for c in cs for add, _, p in c["files"]
                    if p.startswith(ARM) and kind(p) == "prose")
    arm_data = sum(add for c in cs for add, _, p in c["files"]
                   if p.startswith(ARM) and kind(p) == "data")

    total_sessions = len(sessions)
    mid_date = sessions[total_sessions // 2]["date"]
    summary = {
        "generated_from": "git log --no-merges over the full history of main; "
                          "journal/*.md headings; works/ directory listing",
        "window": {"first_day": days[0], "last_day": days[-1], "days": len(days)},
        "sessions_indexed": total_sessions,
        "session_numbers_min_max": [sessions[0]["session"], sessions[-1]["session"]],
        "session_numbers_missing": sorted(
            set(range(sessions[0]["session"], sessions[-1]["session"] + 1))
            - {r["session"] for r in sessions}),
        "day_local_invocations_first_day": len(local),
        "duplicate_session_headings": len(dupes),
        "commits_counted": len(cs),
        # main's history does not reach back to the first session: the earliest sessions'
        # work entered it in bulk. Everything derived from commits is bounded by this day.
        "history_begins": min(c["date"] for c in cs),
        "commits_by_author": dict(sorted(author_commits.items(), key=lambda kv: -kv[1])),
        "lines_added_by_author": dict(sorted(author_lines.items(), key=lambda kv: -kv[1])),
        "shipping_events": len(works),
        "works_standing_now": len([w for w in works if w["still_in_works"]]),
        "works_withdrawn": withdrawn,
        "works_git_date_differs_from_slug_date": sum(
            1 for w in works if w["git_first_seen"] != w["slug_date"]),
        "files_created_total": len(first),
        "whole_run": span(days),
        "last_shipping_day": last_ship,
        "after_last_shipping_day": span(after) if after else None,
        "arm_draft": {"path": ARM, "files_ever_created": len(arm_files),
                      "files_present_now": (len(os.listdir(ARM)) if os.path.isdir(ARM) else 0),
                      "lines_added_prose": arm_prose, "lines_added_data": arm_data},
        "split_day": mid_date,
        "first_half": span([d for d in days if d < mid_date]),
        "second_half": span([d for d in days if d >= mid_date]),
    }

    with open(f"{OUT}/summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if dupes:
        print(f"\n{len(dupes)} duplicate session headings (first kept):", file=sys.stderr)
        for num, date, head in dupes:
            print(f"  {num} {date} {head}", file=sys.stderr)


if __name__ == "__main__":
    main()
