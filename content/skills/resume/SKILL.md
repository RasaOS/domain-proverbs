---
name: resume
description: Pick up in-flight work from the most recent handoff so a cold session resumes mid-stride instead of re-deriving context. Reads the stable handoff pointer (`.claude/HANDOFF.md`) or, failing that, discovers the newest dated handoff doc; then calibrates it against current git state and leads with the one next action. Read-only — it briefs, it never mutates. Triggered when returning to unfinished work — e.g. "/resume", "where was I", "pick up where I left off", "load the handoff", "catch me up on the in-flight work".
---

# /resume — Pick up the in-flight work from the last handoff

Read the latest handoff, reconcile it against what git shows has
happened since, and hand back the one next action — so a session
resumes the unfinished thread without reconstructing it. Read-side
counterpart to `/handoff`; read-only, it briefs and changes nothing.
The judgment is the reconciliation: a handoff was true when written;
resume says whether it still is.

## Behavior contract

- **Read-only.** Reads the handoff pointer, the handoff doc, and git
  state; optionally `.claude/rasa.lock.json` for one identity line.
  Writes nothing, commits nothing, checks out nothing. If it surfaces
  work, it names it and stops — the move is the user's.
- **Find the handoff by convention, not a hardcoded path.** Read the
  stable pointer at `.claude/HANDOFF.md` first (`.claude/` is the
  contract-guaranteed dir; the pointer links the dated doc it
  summarizes). If it's absent or its link is stale, discover the newest
  handoff doc by scanning root-relative locations. Never an absolute or
  home-anchored path (per `contract-rules.md`).
- **Calibrate against reality — don't parrot the doc.** The handoff was
  accurate when written; git may have moved. For each in-flight /
  blocked / next item, check whether commits since the handoff already
  addressed it, whether the branch or working tree diverged — and flag
  the mismatch instead of replaying stale state as current.
- **Relay the handoff's own shape.** Summarize whatever sections the doc
  contains; the doc defines them, resume mirrors them. If the handoff is
  thin, say so — don't invent state it doesn't support.
- **Lead with the resume point, distinct from onboard.** The single
  next action is the load-bearing output (conclusion first). `/onboard`
  orients to the installed domain; `/resume` picks up the unfinished
  work a handoff captured — don't substitute a project tour for a resume.

## Process

1. **Read the pointer.** `.claude/HANDOFF.md` if present — the fast
   orient — then follow its link to the dated doc for depth.
2. **Else discover** (no pointer, or its link doesn't resolve): scan
   root-relative locations — a top-level `HANDOFF*.md`, or a `handoff/`
   dir if one exists — and pick the newest by any date in the filename,
   else by mtime (a plain `HANDOFF.md` resolves by mtime). Note the
   fallback; no hardcoded paths.
3. **Nothing found → stop honestly.** Render a short "nothing to resume"
   note pointing at `/handoff` (to create one) and `/onboard` (for cold
   orientation). Don't fabricate a thread from nothing.
4. **Read the selected doc in full;** note its date — that anchors the
   git-delta window.
5. **Gather git ground truth** — current branch vs. the one the handoff
   named, working-tree status, `git log` since that date — and
   cross-reference each in-flight / blocked / next item against it.
6. **Render the briefing**, then stop:
   - **Resume point** — the one next action, drift-adjusted. Leads.
   - **Where you left off** — terse, from the doc.
   - **In flight / blocked** — relayed, git-calibrated.
   - **State check** — handoff branch/tree vs. now, commits since, or
     "no drift"; say if the handoff is more than trivially stale.
   - **Source** — which doc, its date and path; commits by short-SHA.

## What NOT to do

- Don't write, commit, or check out anything — resume briefs; name the
  follow-up and leave it to the user.
- Don't parrot a stale handoff as current; the git-delta calibration is
  required, not optional.
- Don't echo a secret if the handoff wrongly contains one — flag it.

## When NOT to use

- **Orienting to the installed domain** (what this project is, which
  Element governs it) → `/onboard`.
- **Capturing where work stands** (the write side) → `/handoff`.
- **Reconciling against an upstream Element update** → `/sync`.
- **No handoff on disk yet** — nothing to resume; run `/handoff` to
  create one, or `/onboard` for cold orientation.

## Done when

The session can name the one next action, where the work was left, what
was in flight or blocked, and whether the handoff still matches git
reality — from a read-only pass, with nothing written.
