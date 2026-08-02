#!/usr/bin/env python3
"""Run ONE queued detector job, so a research session no longer needs the credential.

Why this exists (REQUESTS.md 2026-08-02, session 80). The detector arm reaches its API
through repository secrets, which exist only inside GitHub Actions — a finding recorded
back at instrument 014, session 09. A research session is not an Actions run and has no
route to them. So on 2026-08-02, on the one date anchor A1 could ever be taken, the
provenance limb of Article 50(2) was read and the detector limb had to be recorded
`deferred`. Anchor A2 is date-locked to 2026-12-02 at the earliest and would have failed
the same way.

The split this fixes is an ACCESS path, not a runtime limit: nothing here is about how
long a job may run. A session commits its specimens, its own runner and one queue entry;
a scheduled workflow with the credential runs the runner and commits its output back.

The instrument stays the practice's. This driver does not score anything, does not know
what a specimen is, and never writes a result file itself — it runs the script the queue
names and commits what that script declares. Adding a measurement is still an act of the
collective, made in its own tools; only the key stays where it has to stay.

QUEUE FORMAT — `layer2-queue.json` at the repository root, a list of entries:

    [
      {
        "runner":    "drafts/2026-07-23-grandfather-clause/a1/tools/run_layer2.py",
        "outputs":   ["drafts/2026-07-23-grandfather-clause/a1/layer2.json"],
        "requested": "2026-08-02",
        "note":      "anchor A1, detector limb — deferred on the day, see CAPTURE-NOTES.md D5"
      }
    ]

`outputs` is what gets committed, declared by the entry rather than guessed here: the
split-seal layout writes `data/layer2.json`, the a1 layout does not, and a driver that
assumed one of them would silently commit nothing for the other.

BUDGET. One detector run is roughly 15 checks against a free tier of about 2,000
operations a month (split-seal dossier §4d). Exactly ONE entry is processed per
invocation, and a processed entry is removed from the queue, so a set is never scored
twice by this path. What was left waiting is printed — a deferred job is never silently
dropped.

FAILURE. A runner that fails leaves its entry in the queue and exits non-zero, so the
workflow goes red and the job stays visible. Same rule as auto-land.yml: a green run
means the work landed, never that an error was echoed away.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "layer2-queue.json"

# A session writes the queue, and this driver executes what it names with a live API
# credential in the environment. The guard is not distrust of the practice; it is that a
# bug in one session must not be able to point the credential at something unintended.
ALLOWED_PREFIXES = ("drafts/", "works/")


def fail(msg: str) -> None:
    sys.exit(f"layer2-queue: {msg}")


def validate(entry: dict, index: int) -> tuple[Path, list[str]]:
    runner = entry.get("runner")
    outputs = entry.get("outputs")
    if not isinstance(runner, str) or not runner:
        fail(f"entry {index}: no runner named")
    if not isinstance(outputs, list) or not outputs or not all(isinstance(o, str) and o for o in outputs):
        fail(f"entry {index}: outputs must be a non-empty list of paths")
    for path in [runner, *outputs]:
        if path.startswith("/") or ".." in Path(path).parts:
            fail(f"entry {index}: {path!r} must be a relative path inside the repository")
        if not path.startswith(ALLOWED_PREFIXES):
            fail(f"entry {index}: {path!r} is outside {' / '.join(ALLOWED_PREFIXES)}")
    if not runner.endswith(".py"):
        fail(f"entry {index}: runner {runner!r} is not a .py script")
    resolved = (ROOT / runner).resolve()
    if not resolved.is_file():
        fail(f"entry {index}: runner {runner!r} does not exist — commit it before queueing")
    return resolved, outputs


def main() -> None:
    if not QUEUE.is_file():
        print("layer2-queue: no queue file — nothing to do")
        return
    try:
        queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"{QUEUE.name} is not valid JSON: {e}")
    if not isinstance(queue, list):
        fail(f"{QUEUE.name} must contain a list")
    if not queue:
        print("layer2-queue: queue is empty — nothing to do")
        return

    entry = queue[0]
    if not isinstance(entry, dict):
        fail("entry 0: not an object")
    runner, outputs = validate(entry, 0)

    if not (os.environ.get("DETECTOR_IMAGE_API_USER") and os.environ.get("DETECTOR_IMAGE_API_SECRET")):
        # The runners refuse to fake results without credentials; say so here too rather
        # than letting a green-looking run produce nothing.
        fail("detector credentials absent from the environment — refusing to run")

    waiting = len(queue) - 1
    print(f"layer2-queue: running {entry['runner']}")
    if entry.get("note"):
        print(f"layer2-queue: note — {entry['note']}")

    result = subprocess.run([sys.executable, str(runner)], cwd=ROOT)
    if result.returncode != 0:
        # Entry stays in the queue on purpose: the job is still owed.
        fail(f"runner exited {result.returncode} — entry kept in the queue")

    missing = [o for o in outputs if not (ROOT / o).is_file()]
    if missing:
        fail(f"runner reported success but declared output missing: {', '.join(missing)}")

    QUEUE.write_text(json.dumps(queue[1:], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Written for the workflow to read, so the commit step needs no path knowledge of its own.
    committed = [*outputs, QUEUE.name]
    if step_output := os.environ.get("GITHUB_OUTPUT"):
        Path(step_output).open("a", encoding="utf-8").write(f"paths={' '.join(committed)}\n")
    print(f"layer2-queue: done — {waiting} job(s) still waiting")


if __name__ == "__main__":
    main()
