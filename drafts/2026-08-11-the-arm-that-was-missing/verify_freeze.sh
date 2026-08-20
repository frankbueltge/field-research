#!/bin/sh
# Verify a freeze manifest against the directory it describes, and not against whatever files
# happen to share those basenames where the manifest is stored.
#
# Session 128, 2026-08-20. The ninth gauntlet's adversary noticed in passing that running
# `sha256sum -c FROZEN-128.sha256` from the arc root prints EIGHT `OK` lines against files in the
# arc root that are not the frozen ones, because the manifest's paths are bare basenames and eight
# of them collide. A freeze that reports OK for the wrong files, when run from where it is stored,
# is a guard that is true somewhere and false where it lives. The manifest itself is NOT edited —
# it is the artifact two reviewers checked against — so the fix is this wrapper.
#
#   sh verify_freeze.sh letter FROZEN-128.sha256
set -e
DIR=${1:-letter}
MAN=${2:-FROZEN-128.sha256}
HERE=$(cd "$(dirname "$0")" && pwd)
test -f "$HERE/$MAN" || { echo "no manifest at $HERE/$MAN" >&2; exit 2; }
N_LISTED=$(grep -c . "$HERE/$MAN")
N_PRESENT=$(ls -1 "$HERE/$DIR" | wc -l)
cd "$HERE/$DIR"
sha256sum -c "$HERE/$MAN"
echo "membership: $N_PRESENT files present, $N_LISTED listed"
test "$N_PRESENT" -eq "$N_LISTED" || {
  echo "MEMBERSHIP MISMATCH — contents verify but the directory is not the frozen one" >&2; exit 1; }
echo "freeze OK: $N_LISTED of $N_LISTED, membership matches"
