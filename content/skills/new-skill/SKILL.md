---
name: new-skill
description: Scaffold a new skill that already follows this domain's canonical conventions — frontmatter triggers, behavior contract, process, what-NOT-to-do, and a "done when" definition. Asks targeted questions about scope, what the skill produces (report / written files / applied edits), the consent model, and how much is deterministic script vs AI judgment, then writes a SKILL.md skeleton with TODO markers. Triggered when the user wants to author a skill — e.g. "/new-skill", "scaffold a skill", "create a new skill called X", "I want a skill that does Y".
---

# /new-skill — Scaffold a new skill

Generate a `SKILL.md` skeleton that already follows every convention in
`skills/README.md`. The user fills in the substance; the skill enforces
the shape.

Blunt and calibrated: if the user's idea is better served by extending
an existing skill, say so — don't default to "yes, let's make one".

## Behavior contract

- **Ask before scaffolding.** Get these before writing anything:
  1. **Name** — kebab-case, single word preferred (`onboard`, `handoff`).
  2. **One-sentence purpose** — what problem it solves.
  3. **Triggers** — 3–5 concrete phrases the user would actually say.
  4. **Scope** — Element-level (lives in `content/skills/`, propagates
     to every project via sync) or project-local (lives in the
     project's `.claude/skills/`, stays in that repo).
  5. **Mutation model** — does it (a) only render a report, (b) write
     durable files, or (c) edit source? Each gets a different consent
     boilerplate.
  6. **Script split** — is any of it deterministic plumbing that should
     live in a script (none / partial / full)? Separate "what files to
     touch" from "what judgment the AI brings".
- **Refuse to invent answers.** If the user can't state the triggers or
  the mutation model, that's a sign the skill isn't ready — surface
  that instead of guessing.
- **Universal skills stay subject-neutral.** If the target is
  `content/skills/` in `rasa.domain.core` itself, the skill may
  reference only the Element contract. A fork's skills may be
  subject-aware.
- **Write a skeleton, not a finished skill.** Emit `SKILL.md` with the
  canonical sections and `TODO:` markers where judgment is needed.
  Never fabricate a behavior contract the user didn't describe.

## Process

1. Ask the six questions. Stop until answered.
2. Decide folder: `content/skills/<name>/` (Element) or
   `.claude/skills/<name>/` (project-local).
3. Copy `content/templates/SKILL.md.template` to the chosen path and
   fill it — frontmatter (name + a description built from the purpose
   and triggers), each body section seeded from the user's answers,
   with an explicit `TODO:` wherever judgment is still missing. Don't
   freehand the shape; the template is the contract
   (`rules/authoring-rules.md`).
4. If the split is partial/full, stub the script file next to it and
   note the plumbing/judgment boundary in the contract.
5. Show the path and the skeleton. Do not commit.
6. Remind: for an Element-level skill, run `bin/check-shape` (structure)
   and `bin/check-manifest` (inventory) — both must pass before the
   skill ships.

## What NOT to do

- Don't scaffold when extending an existing skill is the better move.
- Don't fill in the behavior contract with plausible-sounding rules the
  user never stated.
- Don't auto-commit.

## Done when

`SKILL.md` exists at the chosen path, follows the canonical shape, and
every judgment the user hasn't made is an explicit `TODO:` — not a
guess.
