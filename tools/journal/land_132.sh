#!/bin/sh
# Landing for session 132, written while the probe was still running so that the close is one
# command and not a sequence improvised at the edge of a session.
#
# The session opened at 03:35:54Z; the run it exists to deliver was projected to close near 05:35Z,
# which is beyond the longest session span this record documents (1 h 53 m 30 s). This file is what
# a session does about that: it makes the last step short.
#
# It runs ONLY the close pipeline, the record generator and the guards. It builds nothing to send:
# `CONDITIONS-128.md`'s stop, unchanged by `CONDITIONS-131.md` item 1, forbids that.
set -e
cd "$(dirname "$0")/../.."
ARC=drafts/2026-08-11-the-arm-that-was-missing

test -f "$ARC/ledger/run-2026-08-22T0341Z.json" || {
    echo "NO COMPLETED RUN FILE — day 11 is a hole. A partial is never a run." >&2
    echo "Do not run this script. Land the hole honestly instead." >&2
    exit 1
}

( cd "$ARC" && sh run_day11_close.sh )
( cd "$ARC" && python3 day11_record.py )
( cd "$ARC" && python3 e34_sweep.py )

python3 tools/chronicle_check.py | tail -2
python3 tools/journal/check_anchors.py | tail -2
python3 tools/requests_room_check.py | tail -1
echo "--- minutes word count ---"
python3 tools/journal/count_132.py journal/2026-08-22.md
