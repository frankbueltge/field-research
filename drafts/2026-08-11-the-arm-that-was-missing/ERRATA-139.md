# Errata 139 — 2026-08-30

Dated corrections to this arc's record, continuing `ERRATA-138.md` (E59–E62). Nothing here is a
silent patch: the affected sentences stay where they are, and this file is the correction.

---

## E63 — the line numbers published for the one split are 0-based, and `DELIMITATION-139.md` does not say so

**Found by:** the conductor, against its own output, **while both reviewers were in flight** and
before either reported. The commit carrying this file is the evidence of the ordering, and it is an
unsigned commit on this practice's own clock — which `ERRATA-138.md` E61 already established proves
less than it looks like it proves.

**What was published.** `DELIMITATION-139.md`, §"The one split":

> Both readings sit on **the same seven source lines — 16, 18, 20, 22, 24, 26, 28.**

**What is true.** Those are **0-based indices** into `INTERLOCUTOR-133.md` split on `\n`, which is
what `split_check_139.py` computes and writes to `split-check-139.json`. In the 1-based numbering
every text editor and every `sed -n` uses, the seven lines are **17, 19, 21, 23, 25, 27, 29**.
Checkable in one command:

```
sed -n '17p;19p;21p;23p;25p;27p;29p' INTERLOCUTOR-133.md
```

**Why it is recorded rather than fixed in place.** The sentence is not wrong about the measurement —
both readings do sit on the same seven lines, which is the whole of what the sentence is for, and
neither the verdict nor any count moves. It is wrong about the convention a reader would use to
check it, which means a reader following the document would look at the wrong seven lines and find
prose that does not match. **A number a reader cannot reproduce is not a published number**, and
this arc has said so about its own figures often enough to hold itself to it.

**The class it belongs to.** An index convention left unstated because the session that wrote it
knew which one it meant. `split_check_139.py`'s docstring does not state it either, and that is the
deeper defect: the script is the artifact a later session will re-run.

**Binding on the next session:** any line number this arc publishes states its base, or gives the
command that reproduces it.
