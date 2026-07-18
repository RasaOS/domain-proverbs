---
name: handoff
description: Write a session handoff/checkpoint capturing where work stands so the next session (or person) resumes without re-deriving context — what was done, what's in flight, what's blocked, what's next, and the exact state (branch, uncommitted changes, open questions). Writes a durable handoff doc; never commits. Triggered when the user is wrapping up or switching context — e.g. "/handoff", "write a handoff", "checkpoint where we are", "hand this off", "save state before I stop".
---

# /handoff — Capture session state for the next session

Distill the current session into a durable handoff so the next session
resumes from state, not from scratch. The judgment is in what to keep:
decisions and their why, in-flight work, blockers — not a transcript
replay.

## Behavior contract

- **Capture state, not narrative.** Decisions made (and why), work in
  flight, what's blocked and on what, and the concrete next step. Skip
  the play-by-play.
- **Record the exact ground truth.** Current branch, uncommitted
  changes, tests last-run status, open questions still unanswered. The
  next session should be able to trust it and act.
- **Be honest about done-ness.** Partial work is described as partial;
  a failing check is recorded as failing. A handoff that overstates
  progress is worse than none.
- **Write durably.** Emit a dated handoff file — default
  `handoff/<date>.md` (or a top-level `HANDOFF.md` if the project has no
  `handoff/` dir); ask only if neither fits. Also refresh a stable
  pointer at `.claude/HANDOFF.md` — a short "where you left off" summary
  ending in a relative link to the dated doc, rewritten in full each
  run. The pointer is what `/resume` reads first to pick this up. Never
  auto-commit.
- **No secrets.** Don't write tokens, keys, or credentials into the
  handoff.

## Process

1. Gather ground truth: `git status`/branch, what changed this session,
   last test/build result if relevant.
2. Reconstruct the arc: goal, decisions + rationale, what got done.
3. List in-flight items and blockers with enough specificity to resume.
4. State the single clear next step.
5. Write the dated handoff doc, then rewrite `.claude/HANDOFF.md` as a
   short pointer linking it. Show both paths. Leave them uncommitted.

## Output shape

```markdown
# Handoff — <date>

**Goal:** <what this session was trying to achieve>

## Done
- <completed, with the why where it isn't obvious>

## In flight
- <started, current state, where it's parked>

## Blocked
- <blocked on what / whom / which decision>

## State
- Branch: <name> · Uncommitted: <summary> · Tests: <status>

## Next
- <the one concrete next action>

## Open questions
- <unresolved decisions the next session must make>
```

## What NOT to do

- Don't replay the transcript; capture state.
- Don't overstate progress or bury a failing check.
- Don't write secrets. Don't auto-commit.

## Done when

A dated handoff doc exists that a cold session could read and resume
from — accurate about what's done, what's not, and what's next — and
`.claude/HANDOFF.md` points at it (the target `/resume` reads first).
