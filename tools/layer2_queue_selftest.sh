#!/bin/bash
# Self-test for tools/layer2_queue.py. Run from anywhere: bash tools/layer2_queue_selftest.sh
#
# The driver executes a script the queue names, with a live detector credential in the
# environment, and commits what that script declares. Every guard on that path is asserted
# here rather than described in a comment — this practice does not claim what it has not
# checked, and the guards are the whole reason the credential can stay where it is.
#
# No network call happens: the runner under test is a probe that only writes its own
# output file. The probe and the queue are restored at the end.
set -u
cd "$(dirname "$0")/.." || exit 1

Q=layer2-queue.json
GHO="$(mktemp)"
PROBE_DIR=drafts/2026-07-23-grandfather-clause/a1
PROBE=$PROBE_DIR/tools/_selftest_runner.py
OUTFILE=$PROBE_DIR/layer2.json
QUEUE_BACKUP="$(mktemp)"
[ -f $Q ] && cp $Q "$QUEUE_BACKUP"
pass=0; fail=0
log=/tmp/layer2-selftest.log

entry="{\"runner\":\"$PROBE\",\"outputs\":[\"$OUTFILE\"],\"requested\":\"2026-08-02\",\"note\":\"selftest probe\"}"

run () { : > "$GHO"; GITHUB_OUTPUT="$GHO" python3 tools/layer2_queue.py > $log 2>&1; ec=$?; }

check () { # name, expected exit, expected substring
  if [ "$ec" = "$2" ] && grep -qF -- "$3" $log; then
    echo "  ok    $1"; pass=$((pass + 1))
  else
    echo "  FAIL  $1 — exit $ec (expected $2), looking for: $3"
    sed 's/^/        /' $log; fail=$((fail + 1))
  fi
}

assert () { # name, condition-already-evaluated
  if [ "$2" = "0" ]; then echo "  ok    $1"; pass=$((pass + 1))
  else echo "  FAIL  $1"; fail=$((fail + 1)); fi
}

queue_len () { python3 -c "import json;print(len(json.load(open('$Q'))))"; }

echo "layer2_queue self-test"

# ── nothing to do ─────────────────────────────────────────────────────────────
echo '[]' > $Q
run; check "an empty queue is a no-op" 0 "queue is empty"

# ── a malformed queue is named, never guessed at ──────────────────────────────
echo 'not json' > $Q
run; check "invalid JSON is reported" 1 "not valid JSON"
echo '{"runner":"x"}' > $Q
run; check "an object instead of a list is refused" 1 "must contain a list"

# ── the path guards: a session writes this file, so it is not trusted blindly ──
echo "[{\"runner\":\"/etc/passwd\",\"outputs\":[\"$OUTFILE\"]}]" > $Q
run; check "an absolute path is refused" 1 "relative path"
echo "[{\"runner\":\"works/../../evil.py\",\"outputs\":[\"$OUTFILE\"]}]" > $Q
run; check "path traversal is refused" 1 "relative path"
echo "[{\"runner\":\"tools/layer2_queue.py\",\"outputs\":[\"$OUTFILE\"]}]" > $Q
run; check "a runner outside drafts/ or works/ is refused" 1 "is outside"
echo "[{\"runner\":\"works/nope.py\",\"outputs\":[\"$OUTFILE\"]}]" > $Q
run; check "a runner that is not committed is named" 1 "does not exist"
echo '[{"runner":"works/2026-07-11-split-seal/tools/run_layer2.py","outputs":[]}]' > $Q
run; check "an entry declaring no output is refused" 1 "non-empty list"

# ── refusing to run blind ─────────────────────────────────────────────────────
printf 'from pathlib import Path\nPath("%s").write_text("{}\\n")\n' "$OUTFILE" > $PROBE
echo "[$entry]" > $Q
unset DETECTOR_IMAGE_API_USER DETECTOR_IMAGE_API_SECRET
run; check "without credentials it refuses rather than producing nothing" 1 "refusing to run"

# ── the happy path, and the budget rule ───────────────────────────────────────
export DETECTOR_IMAGE_API_USER=selftest DETECTOR_IMAGE_API_SECRET=selftest
rm -f "$OUTFILE"
echo "[$entry,$entry]" > $Q
run; check "a valid job runs, and only ONE per invocation" 0 "1 job(s) still waiting"
grep -qF "paths=$OUTFILE $Q" "$GHO"; assert "the paths to commit are reported to the workflow" $?
[ "$(queue_len)" = "1" ]; assert "a finished entry is removed, so nothing is scored twice" $?

# ── failure stays visible ─────────────────────────────────────────────────────
printf 'import sys\nsys.exit(3)\n' > $PROBE
echo "[$entry]" > $Q
run; check "a failing runner turns the job red" 1 "entry kept in the queue"
[ "$(queue_len)" = "1" ]; assert "and its entry stays queued — the job is still owed" $?

# ── a runner that succeeds without producing its output ───────────────────────
printf 'pass\n' > $PROBE
echo "[$entry]" > $Q
rm -f "$OUTFILE"   # an earlier case wrote it; leaving it would hide this defect
run; check "a runner that declares an output and writes none fails" 1 "declared output missing"

rm -f $PROBE "$OUTFILE"
if [ -s "$QUEUE_BACKUP" ]; then cp "$QUEUE_BACKUP" $Q; else echo '[]' > $Q; fi
rm -f "$QUEUE_BACKUP" "$GHO"

echo
echo "$pass passed, $fail failed"
[ "$fail" = 0 ]
