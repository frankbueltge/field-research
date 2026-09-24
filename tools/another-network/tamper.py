#!/usr/bin/env python3
"""Deliberately corrupt each committed data file, one fault at a time, and confirm check.py
fails with the specific check named for that fault — then restore the original bytes.

    python3 tools/another-network/tamper.py
"""
import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/2026-09-24-another-network"
DATA = ART / "data"
CHECK = ROOT / "tools/another-network/check.py"

FILES = ["local.json", "delegate.json", "estimates.json", "population-snapshot.json",
         "render-check.json"]
PAGE = ART / "index.html"


def run_check():
    r = subprocess.run([sys.executable, str(CHECK)], capture_output=True, text=True)
    return r.returncode, r.stdout


def restore(backups):
    for f, content in backups.items():
        path = PAGE if f == "index.html" else (DATA / f)
        path.write_bytes(content)


def main():
    backups = {f: (DATA / f).read_bytes() for f in FILES}
    backups["index.html"] = PAGE.read_bytes()
    rc, out = run_check()
    if rc != 0:
        print("BASELINE ALREADY FAILING — abort tamper run"); print(out); sys.exit(1)
    print("baseline: all checks pass\n")

    results = []

    def trial(name, expect_check, mutate):
        restore(backups)
        mutate()
        rc, out = run_check()
        caught = rc != 0 and expect_check in out
        results.append((name, caught))
        print(f"[{'caught' if caught else 'MISSED'}] {name}")
        if not caught:
            print(out)

    def mut_pop_snapshot_hash():
        d = json.loads((DATA / "population-snapshot.json").read_text())
        d["sha256"] = "0" * 64
        (DATA / "population-snapshot.json").write_text(json.dumps(d))

    def mut_local_refuses_flip():
        d = json.loads((DATA / "local.json").read_text())
        for u in d["units"]:
            if u["unit_id"] == "H:www-fema-gov":
                u["local_refuses"] = not u["local_refuses"]
                break
        (DATA / "local.json").write_text(json.dumps(d))

    def mut_delegate_result_flip():
        d = json.loads((DATA / "delegate.json").read_text())
        for u in d["units"]:
            if u["unit_id"] == "H:www-iea-org":
                u["delegate_refuses"] = not u["delegate_refuses"]
                break
        (DATA / "delegate.json").write_text(json.dumps(d))

    def mut_readd_excluded_unit():
        d = json.loads((DATA / "local.json").read_text())
        d["units"].append({"unit_id": "H:en-wikipedia-org", "stratum": "H",
                            "url": "https://en.wikipedia.org/w/api.php",
                            "recorded_status": 403, "local": None})
        (DATA / "local.json").write_text(json.dumps(d))

    def mut_duplicate_unit():
        d = json.loads((DATA / "local.json").read_text())
        d["units"].append(dict(d["units"][0]))
        (DATA / "local.json").write_text(json.dumps(d))

    def mut_hand_read_verdict_flip():
        d = json.loads((DATA / "estimates.json").read_text())
        for h in d["hand_reads"]:
            if h["unit_id"] == "H:datacenters-microsoft-com":
                h["verdict"] = "true"
                break
        (DATA / "estimates.json").write_text(json.dumps(d))

    def mut_hand_read_drop_case():
        d = json.loads((DATA / "estimates.json").read_text())
        d["hand_reads"] = [h for h in d["hand_reads"] if h["unit_id"] != "C:bijan-davvaz-groups"]
        (DATA / "estimates.json").write_text(json.dumps(d))

    def mut_quadrant_count():
        d = json.loads((DATA / "estimates.json").read_text())
        d["quadrant_read"]["both_refuse"] += 1
        (DATA / "estimates.json").write_text(json.dumps(d))

    def mut_still_refuse_count():
        d = json.loads((DATA / "estimates.json").read_text())
        d["p1_p2_read"]["still_refuse"] -= 1
        (DATA / "estimates.json").write_text(json.dumps(d))

    def mut_of_those_reads_count():
        d = json.loads((DATA / "estimates.json").read_text())
        d["p1_p2_read"]["of_those_delegate_reads"] += 3
        (DATA / "estimates.json").write_text(json.dumps(d))

    def mut_sign_test_p():
        d = json.loads((DATA / "estimates.json").read_text())
        d["sign_test_on_discordant_pairs_read"]["two_sided_exact_p"] = 0.001
        (DATA / "estimates.json").write_text(json.dumps(d))

    def mut_controls_count():
        d = json.loads((DATA / "estimates.json").read_text())
        d["controls"]["local_reads"] += 1
        (DATA / "estimates.json").write_text(json.dumps(d))

    def mut_k1_fired_lie():
        d = json.loads((DATA / "estimates.json").read_text())
        d["kill_conditions"]["K1_instrument_floor"]["fired"] = True
        (DATA / "estimates.json").write_text(json.dumps(d))

    def mut_asym_list_short():
        d = json.loads((DATA / "estimates.json").read_text())
        d["asymmetric_cases"]["delegate_reads_local_refuses"].pop()
        (DATA / "estimates.json").write_text(json.dumps(d))

    def mut_remove_delegate_for_one():
        d = json.loads((DATA / "delegate.json").read_text())
        d["units"] = [u for u in d["units"] if u["unit_id"] != "H:www-fema-gov"]
        (DATA / "delegate.json").write_text(json.dumps(d))

    def mut_render_check_lie():
        d = json.loads((DATA / "render-check.json").read_text())
        d["final_results"]["390"]["overflow"] = True
        (DATA / "render-check.json").write_text(json.dumps(d))

    def mut_page_stale():
        PAGE.write_text(PAGE.read_text() + "\n<!-- stale -->\n")

    trial("population digest corrupted", "population snapshot sha256", mut_pop_snapshot_hash)
    trial("a local_refuses flag flipped without re-deriving", "independent re-derivation from local.status",
          mut_local_refuses_flip)
    trial("a delegate_refuses flag flipped without re-deriving", "independent re-derivation from result/content_len",
          mut_delegate_result_flip)
    trial("a robots-excluded unit re-added to local.json", "none of the 4 pre-registered robots-excluded",
          mut_readd_excluded_unit)
    trial("a duplicate unit appended to local.json", "no duplicate unit_id in local.json", mut_duplicate_unit)
    trial("a hand-read verdict silently flipped", "local_refuses_read is False for every false-positive",
          mut_hand_read_verdict_flip)
    trial("a hand-read case silently dropped", "hand_reads covers exactly the screen's own",
          mut_hand_read_drop_case)
    trial("a quadrant count off by one", "quadrant_read matches an independent recount", mut_quadrant_count)
    trial("still_refuse count off by one", "p1_p2_read.still_refuse matches", mut_still_refuse_count)
    trial("of_those_delegate_reads inflated", "p1_p2_read.of_those_delegate_reads matches", mut_of_those_reads_count)
    trial("sign-test p-value replaced with a smaller one", "sign-test p-value on discordant pairs matches",
          mut_sign_test_p)
    trial("controls.local_reads inflated", "controls.local_reads matches", mut_controls_count)
    trial("K1 marked fired when its own floor is met", "K1's floor of 4 is actually met", mut_k1_fired_lie)
    trial("asymmetric_cases list shortened by one", "asymmetric_cases.delegate_reads_local_refuses length",
          mut_asym_list_short)
    trial("a unit's delegate result deleted entirely", "delegate.json has a result for exactly the 64",
          mut_remove_delegate_for_one)
    trial("render-check.json's 390px overflow lied to false", "render-check reports no horizontal overflow",
          mut_render_check_lie)
    trial("index.html edited without rerunning make_page.py", "index.html is byte-for-byte what make_page.py",
          mut_page_stale)

    restore(backups)
    rc, _ = run_check()
    print(f"\nrestored — checks {'pass' if rc == 0 else 'FAIL'} again")

    n_caught = sum(1 for _, c in results if c)
    print(f"\n{n_caught}/{len(results)} corruptions caught by a named check")
    if n_caught != len(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
