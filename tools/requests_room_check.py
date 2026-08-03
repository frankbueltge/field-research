#!/usr/bin/env python3
"""requests_room_check.py — refuse to land a REQUESTS.md the receiving site cannot render.

WHY THIS EXISTS (2026-08-03, session 85)
----------------------------------------
`REQUESTS.md` is not ours alone. The ecology's site copies it into its own tree and
renders a public room from it at `/field/requests`: the standing rule, EVERY open item,
five recently answered ones. That room's word count is asserted by a test that runs
inside the build gating all three practices' publishing. On 2026-08-02 and again on
2026-08-03 the gate went red on exactly that assertion — `~1521 words, budget 1500` —
and no practice deployed on either day. Instrument 021 shipped on 2026-08-03 and was
never served.

The input the gate choked on was ours, and nothing on our side could see it: we write a
markdown file, and a word budget in another repository decides whether anyone publishes.
This script closes that blindness. It computes the same number, offline, before landing.

WHAT IT MEASURES, AND WHY THAT MATTERS MORE THAN THE TOTAL
---------------------------------------------------------
The room's per-item budget SHRINKS as the open queue grows, by the receiving repo's own
design ("a long queue must make the page denser, never make a collective unable to
publish"). So the number that actually moves the total is the COUNT of open sections —
and a section counts as open purely because its first `**Status:**` line contains the
bare word "open". A section answered in the journal, or answered in a second status line
further down, or superseded by a later section, still prints as *"waiting on a human"*
until that first line is closed. Four of the thirteen open items on 2026-08-03 were of
exactly that kind. So the table below is not decoration: it is the queue this practice is
publicly claiming a human still owes it.

THE RULE IS NOT OURS AND IS PINNED, NOT INVENTED
------------------------------------------------
Every rule below is transcribed from the receiving repository's published source:

    repo   : github.com/frankbueltge/frankbueltge.de   (public)
    commit : 6615ee69e552c1dbdeb5a2c26450a459a0b18625   (read 2026-08-03)
    files  : src/lib/zentrale/requestsMd.ts
             sha256 76540e793620e3fe1743e1be142b3373191efcc20d7c5bed0081fa09817c477c
             src/lib/zentrale/requestsRoom.test.ts
             sha256 b1056bf21e8323825cce463d47d0f127fa86d10d305ba9fac95a1ca22b8b5171
             src/config/field-wording.ts
             sha256 efb38e5be333579044a88d45ba4ee1b5dfad330ddf3196495434d6ae0f050c5d

WHAT THIS SCRIPT CANNOT DO — stated, not buried
-----------------------------------------------
1. It is a pinned replica and CANNOT DETECT ITS OWN STALENESS. If the receiving repo
   changes the budget, the chrome constant, the composition, or the room copy, this
   script keeps computing the old number and keeps saying green. Same limit as
   `tools/chronicle_check.py`, and named here for the same reason.
2. `CHROME_WORDS = 220` is the receiving repo's own measured constant for header, footer
   and rail, not something either side can derive from this file.
3. It measures the FIELD room only. The other practices' rooms are theirs.
4. Passing this check is not a licence to grow the queue to the line. Headroom is
   reported so a session can see how close it is standing.

USAGE
-----
    python3 tools/requests_room_check.py            # exit 1 if the room would not render
    python3 tools/requests_room_check.py --quiet    # exit code only
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ── pinned constants (receiving repo) ────────────────────────────────────────────────
BUDGET = 1500  # requestsRoom.test.ts line 24
CHROME_WORDS = 220  # requestsRoom.test.ts line 39 — header/footer/rail, measured on the built page
# requestsRoom.test.ts line 96, `expect(words).toBeLessThan(document / 5)` — "the room must be a
# real reduction, not a cosmetic one". Transcribed like everything else here; it is the second
# pass condition and it is checked in main(). Named separately because a session 85 reader took it
# for a rule this practice had invented, and a guard whose whole claim is "none of this is ours"
# cannot afford an unlisted constant. Their division is float; ours is integer, which is at most
# one word stricter and never laxer.
ONE_FIFTH_RULE = True
EXCERPT_BUDGET = 270  # requestsMd.ts openExcerptWords
STATUS_WORDS_OPEN = 10  # requestsMd.ts STATUS_WORDS
STATUS_WORDS_CLOSED = 5

# field-wording.ts → FIELD_NARRATIVE.requestsRoom — the receiving repo's copy, verbatim.
ROOM = {
    "intro": "What this collective needs from its human team member, and what came back. Every open item stands first — all of them, never a selection.",
    "standingHeading": "The standing rule of this channel",
    "openHeading": "Open — waiting on a human",
    "openNone": "Nothing is open. Every request in this channel has an answer on the record.",
    "openNote": "Oldest ask first. An unanswered request is never a blocker — past its deadline the collective decides for itself, and records it.",
    "answeredHeading": "Recently answered",
    "answeredNote": "The five most recent closed exchanges, each in full in the archive.",
    "seedsHeading": "The other direction — seeds",
    "seedsNote": "Offers left here for the collective, from the team and from the public. Offers, not orders.",
    "archiveLink": "The whole channel, unedited →",
    "fullTextLabel": "read it in full",
}


# ── transcribed helpers ──────────────────────────────────────────────────────────────
def count_words(text: str) -> int:
    return len([w for w in re.split(r"\s+", text) if w])


def trim_words(text: str, max_words: int) -> str:
    words = [w for w in re.split(r"\s+", text) if w]
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words]) + " …"


def open_excerpt_words(open_count: int) -> int:
    per = EXCERPT_BUDGET // max(1, open_count)
    return max(12, min(40, per))


def strip_md(s: str) -> str:
    return re.sub(r"`", "", re.sub(r"\*\*?", "", re.sub(r"^#+\s*", "", s))).strip()


def plain_line(line: str) -> str:
    s = re.sub(r"^(?:\s*>)+\s*", "", line)
    s = re.sub(r"^\s*[-*+]\s+", "", s)
    s = re.sub(r"^\s*\d+\.\s+", "", s)
    s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return strip_md(s)


def locate_sections(md: str):
    out = []
    for m in re.finditer(r"^## (.*)$", md, re.M):
        out.append({"heading": m.group(1).strip(), "start": m.start(), "body_start": m.end()})
    for i, s in enumerate(out):
        s["end"] = out[i + 1]["start"] if i + 1 < len(out) else len(md)
    return out


def preamble(md: str) -> str:
    secs = locate_sections(md)
    head = md[: secs[0]["start"]] if secs else md
    head = re.sub(r"^\s*#\s+[^\n]*\n?", "", head)
    return head.strip()


def heading_date(heading: str):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", heading)
    return m.group(1) if m else None


HEADING_TITLE_RE = re.compile(
    r"^(?:Team note|Team responses|Response|Status)?\s*(?:\([^)]*\))?\s*(?:—|–|-)?\s*"
    r"\d{4}-\d{2}-\d{2}(?:\s*\([^)]*\))?\s*(?:—|–|:)\s*(.+)$"
)


def heading_title(heading: str) -> str:
    t = heading.strip()
    m = HEADING_TITLE_RE.match(t)
    return (m.group(1) if m else t).strip()


def is_open_status(status) -> bool:
    return isinstance(status, str) and re.search(r"\bopen\b", status, re.I) is not None


def is_seeds_section(heading: str) -> bool:
    return re.match(r"^Seeds\b", heading.strip(), re.I) is not None


HR_OR_TABLE_RE = re.compile(r"^(\||[ ]{0,3}([-*_])\s*(\2\s*){2,}$)")


def excerpt(body: str, max_words: int) -> str:
    parts, in_fence, words = [], False, 0
    for raw in body.split("\n"):
        bare = re.sub(r"^(?:\s*>)+\s*", "", raw)
        if re.match(r"^(```|~~~)", bare):
            in_fence = not in_fence
            continue
        if in_fence or not bare.strip():
            continue
        if re.match(r"^#{1,6}\s", bare) or re.match(r"^\*\*Status:\*\*", bare):
            continue
        if HR_OR_TABLE_RE.match(bare):
            continue
        text = plain_line(raw)
        if not text:
            continue
        parts.append(text)
        words += count_words(text)
        if words >= max_words:
            break
    return trim_words(" ".join(parts), max_words)


STATUS_VALUE_RE = re.compile(r"^(?:\s*>?\s*)\*\*Status:\*\*\s*(.*)$", re.M)


def request_cards(md: str, excerpt_words: int = 40):
    cards = []
    for s in locate_sections(md):
        raw = md[s["body_start"] : s["end"]]
        body = re.sub(r"\s+$", "", re.sub(r"^\n", "", raw))
        m = STATUS_VALUE_RE.search(raw)
        status = m.group(1).strip() if m else None
        heading = s["heading"]
        cards.append(
            {
                "heading": heading,
                "title": heading_title(heading),
                "date": heading_date(heading),
                "status": status,
                "open": is_open_status(status) and not is_seeds_section(heading),
                "seeds": is_seeds_section(heading),
                "excerpt": excerpt(body, excerpt_words),
                "words": count_words(body),
            }
        )
    return cards


def room_words(md: str):
    cards = request_cards(md)
    opens = [c for c in cards if c["open"]]
    answered = [c for c in cards if not c["open"] and not c["seeds"]][-5:]
    seeds = [c for c in cards if c["seeds"]]
    lead = open_excerpt_words(len(opens))

    words = count_words(preamble(md))
    words += count_words(
        " ".join(
            [
                ROOM["intro"],
                ROOM["standingHeading"],
                ROOM["openHeading"],
                ROOM["answeredHeading"],
                ROOM["answeredNote"],
                ROOM["archiveLink"],
            ]
        )
    )
    words += count_words(ROOM["openNone"] if not opens else ROOM["openNote"])
    if seeds:
        words += count_words(f"{ROOM['seedsHeading']} {ROOM['seedsNote']}")

    open_rows = []
    for c in opens:
        w = (
            count_words(c["title"])
            + (1 if c["date"] else 0)
            + count_words(trim_words(c["status"] or "", STATUS_WORDS_OPEN))
            + 2
            + count_words(trim_words(c["excerpt"], lead))
            + count_words(ROOM["fullTextLabel"])
            + 1
        )
        words += w
        open_rows.append((w, c["heading"]))

    ans_rows = []
    for c in answered:
        w = (
            count_words(c["title"])
            + (1 if c["date"] else 0)
            + count_words(trim_words(c["status"] or "", STATUS_WORDS_CLOSED))
            + 2
            + count_words(c["excerpt"])
        )
        words += w
        ans_rows.append((w, c["heading"]))

    for c in seeds:
        words += count_words(c["heading"]) + 3

    return {
        "composed": words,
        "total": words + CHROME_WORDS,
        "open": len(opens),
        "cards": len(cards),
        "seeds": len(seeds),
        "lead": lead,
        "document": count_words(md),
        "open_rows": open_rows,
        "ans_rows": ans_rows,
    }


def main() -> int:
    quiet = "--quiet" in sys.argv
    md_path = Path(__file__).resolve().parent.parent / "REQUESTS.md"
    md = md_path.read_text(encoding="utf-8")
    r = room_words(md)
    ok = r["total"] < BUDGET and r["total"] < r["document"] // 5

    if not quiet:
        print(f"/field/requests would render ~{r['total']} words "
              f"({r['composed']} composed + {CHROME_WORDS} chrome); budget {BUDGET}.")
        print(f"headroom {BUDGET - r['total'] - 1} words · "
              f"{r['open']} open of {r['cards']} sections · "
              f"{r['lead']} words of lead per open item · document {r['document']} words")
        print()
        print("OPEN — this is what the room publicly says a human still owes this practice:")
        for w, h in r["open_rows"]:
            print(f"  {w:3d}w  {h}")
        print("RECENTLY ANSWERED (the five the room shows, in document order):")
        for w, h in r["ans_rows"]:
            print(f"  {w:3d}w  {h}")
        print()
        print("GREEN" if ok else "RED — the receiving build gate would fail, and no practice deploys.")
        if not ok:
            print("Do not raise the budget: it is not ours. Check whether an item listed above is")
            print("actually still open — a stale first **Status:** line is the cheapest way to be wrong.")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
