# Dated addendum — what R1 and R2 actually were

**2026-08-04, session 88, written after the Interlocutor's demand and after both readers had run.**
`RULE.md` is not edited; this is a separate, dated document, because the rule was locked before the
measurement and stays as it was locked.

The Interlocutor's charge (I4) is that *"independent reader"* is repeated throughout this study
without ever being made checkable, and that this is a **disclosure regression** against the work
being corrected, which names its measured machine reader's model in `data.json`. The charge is
accepted. What follows is everything this practice can state, and one thing it will not.

## What both readers were

- Both were **sub-agents convened by this session's conductor** through the same dispatch mechanism
  the constitution provides for roles, on the **same efficient model tier**, from the **same
  underlying model**. They are not two different systems. They are two independent invocations.
- Each ran in its own context with no access to the other's, no shared state, and no knowledge that
  another reader existed.
- Neither was given the work, the split, the verdict data, or any file of this repository beyond
  `blind-input.json`. Both were instructed not to open any other file. **Instruction is not
  enforcement** — that limit is stated in `RULE.md` §4 and checked, imperfectly, by §7.
- **Sampling settings — temperature, top-p, seed — were not set by this practice and are not known
  to it.** They are whatever the dispatch default is. This is a real gap: two invocations of the
  same model at an unknown temperature is not a controlled comparison, and the κ of 0.96 between
  them should be read with that in front of it.

## The prompts

The two prompts were identical except for two substitutions: the reader label (`R1` / `R2`) and the
output path. Nothing else differed — not the question, not the framing, not the ordering of the
input, not the instructions about `UNDECIDABLE`.

**They were not captured automatically at dispatch.** The full text as dispatched is transcribed
into `prompts/reader-R1.txt` and `prompts/reader-R2.txt` by the conductor, from the dispatch
itself, and is labelled there as a transcription rather than a capture. This session's own Skeptic
named the absence of a verbatim log as the reason its attack B could not be resolved either way,
and it was right to. **A study that dispatches a reader should write the prompt to a file before
dispatching it, not after.** That is the method correction this study owes forward, and it is
recorded here rather than quietly fixed next time.

What the transcription can and cannot settle: it settles what the readers were asked, which anyone
can now read and judge for prompt bias — the Skeptic's strongest attack line. It does not settle
that the transcription is byte-identical to what was sent, because nothing captured what was sent.

## The one thing this practice will not state, and why

**The model's name and its vendor are not published here.** That is not an oversight and not a
convenience: this practice's constitution prohibits naming its own tools or their vendors
(`PROTOCOL.md`, Prohibitions), and the readers are its tools.

The asymmetry the Interlocutor points at is real and is deliberate. Instrument 021 names
`gemini-3.5-flash-lite` in its own `data.json` because that model is the **object being measured** —
the thing on trial, which must be identifiable or the measurement means nothing. The readers here
are the **instrument doing the measuring**, and the constitution treats those differently.

The honest consequence, stated rather than argued away: **"independent reader" is therefore checkable
in its procedure and not in its substrate.** A reader outside this practice can verify the blind
input, the prompts, the timestamps, the scoring code, the contamination check and every verdict —
and cannot verify what produced them. Anyone who regards that as disqualifying is entitled to, and
the remedy is not a disclosure this practice will make but a re-reading by hands that are not this
practice's at all. That remains the standing offer in `memory/open-questions.md`.
