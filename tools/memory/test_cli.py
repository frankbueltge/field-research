import json
import subprocess
import sys
from pathlib import Path

CLI = Path(__file__).parent / "cli.py"


def _write_journal(repo: Path):
    journal = repo / "journal"
    journal.mkdir(parents=True, exist_ok=True)
    (journal / "one.md").write_text(
        "# Benford Check\nbenford law digit distribution used to flag fraud in filings\n"
    )
    (journal / "two.md").write_text(
        "# Cats\ncats are small animals that purr a lot\n"
    )


def _run(args, cwd):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_index_writes_jsonl_with_at_least_two_records(tmp_path):
    _write_journal(tmp_path)

    result = _run(["index", str(tmp_path)], cwd=tmp_path)
    assert result.returncode == 0, result.stderr

    index_file = tmp_path / "memory" / "index.jsonl"
    assert index_file.exists()

    lines = [line for line in index_file.read_text().splitlines() if line.strip()]
    assert len(lines) >= 2
    for line in lines:
        record = json.loads(line)
        assert set(record.keys()) >= {"path", "heading", "text"}


def test_recall_returns_matching_path_after_index(tmp_path):
    _write_journal(tmp_path)

    index_result = _run(["index", str(tmp_path)], cwd=tmp_path)
    assert index_result.returncode == 0, index_result.stderr

    recall_result = _run(["recall", "digit fraud detection", "-k", "1"], cwd=tmp_path)
    assert recall_result.returncode == 0, recall_result.stderr

    results = json.loads(recall_result.stdout)
    assert len(results) == 1
    assert results[0]["path"] == "journal/one.md"


def test_recall_without_prior_index_auto_rebuilds(tmp_path):
    _write_journal(tmp_path)

    # No prior "index" call — memory/index.jsonl does not exist yet.
    assert not (tmp_path / "memory" / "index.jsonl").exists()

    recall_result = _run(["recall", "digit fraud detection", "-k", "1"], cwd=tmp_path)
    assert recall_result.returncode == 0, recall_result.stderr

    results = json.loads(recall_result.stdout)
    assert len(results) == 1
    assert results[0]["path"] == "journal/one.md"
    # Auto-rebuild must have created the index file as a side effect.
    assert (tmp_path / "memory" / "index.jsonl").exists()


def test_recall_with_no_matching_terms_prints_empty_list(tmp_path):
    _write_journal(tmp_path)

    _run(["index", str(tmp_path)], cwd=tmp_path)
    recall_result = _run(["recall", "zzznonexistentqueryterm", "-k", "5"], cwd=tmp_path)
    assert recall_result.returncode == 0, recall_result.stderr

    results = json.loads(recall_result.stdout)
    assert results == []


def test_recall_rebuilds_when_index_is_stale(tmp_path):
    _write_journal(tmp_path)
    _run(["index", str(tmp_path)], cwd=tmp_path)

    # Add a new journal file after the index was built; make sure its mtime
    # is clearly newer than the index file.
    import os
    import time

    index_file = tmp_path / "memory" / "index.jsonl"
    old_time = index_file.stat().st_mtime - 10
    os.utime(index_file, (old_time, old_time))

    (tmp_path / "journal" / "three.md").write_text(
        "# Whales\nwhales are large aquatic mammals with fraud digit unrelated content\n"
    )
    time.sleep(0.01)
    (tmp_path / "journal" / "three.md").touch()

    recall_result = _run(["recall", "whales aquatic", "-k", "1"], cwd=tmp_path)
    assert recall_result.returncode == 0, recall_result.stderr
    results = json.loads(recall_result.stdout)
    assert len(results) == 1
    assert results[0]["path"] == "journal/three.md"
