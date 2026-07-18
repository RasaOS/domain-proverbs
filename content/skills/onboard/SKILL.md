---
name: onboard
description: Orient a fresh session to the domain installed in this project. Reads .claude/rasa.lock.json to identify the Element and pin, loads the domain's rule files and available skills, reads the project CLAUDE.md, and produces a short briefing — what this project is, which domain governs it, what capabilities are available, and anything that looks off (missing lockfile, unmanaged drift, stale pin). Read-only. Triggered at the start of work in an unfamiliar project — e.g. "/onboard", "get oriented", "what domain is this", "catch me up on this project".
---

# /onboard — Orient a session to the installed domain

Produce a fast, accurate briefing so a session starts grounded instead
of guessing. Read-only: it reports, it never changes anything.

## Behavior contract

- **Lockfile first.** Read `.claude/rasa.lock.json` to learn the
  Element (name, kind, version), the `pinned_sha`, and any
  `overrides[]`. If it's missing, say so plainly — this project may not
  be a rasa install, and everything downstream is uncertain.
- **Load the governing context.** Read the project `CLAUDE.md`, the
  domain's `rules/` files, and enumerate the available skills. Report
  what exists; don't run any of them.
- **Report, don't act.** No edits, no sync, no commits. If onboarding
  surfaces work to do, name it and stop.
- **Flag what's off.** Missing lockfile, an override with no obvious
  reason, an Element file edited but not recorded in `overrides[]`
  (unmanaged drift, per `contract-rules.md`) — surface these, don't
  paper over them.
- **Calibrated, not exhaustive.** A briefing, not a file dump. Lead
  with what a session needs to act correctly.

## Process

1. Read `.claude/rasa.lock.json`; capture identity + pin + overrides.
2. Read the project `CLAUDE.md`.
3. List the domain's rule files and skills; one-line each.
4. Sanity-check: lockfile present? overrides explained? any unmanaged
   drift? pin resolvable?
5. Emit the briefing:
   - **Project** — one line on what it is.
   - **Domain** — Element name, version, pin.
   - **Capabilities** — skills + rules available.
   - **Watch-outs** — anything off, or "nothing flagged".

## What NOT to do

- Don't edit, sync, or commit.
- Don't dump whole files — summarize.
- Don't invent a project description the `CLAUDE.md` doesn't support;
  if it's thin, say the project is under-documented.
- Don't use this to pick up unfinished work mid-stride — that's the last
  handoff's job → `/resume`. Onboard orients to the project; resume
  resumes the work.

## Done when

The session can name what the project is, which domain governs it at
what pin, what capabilities are on hand, and what (if anything) looks
wrong — from a read-only pass.
