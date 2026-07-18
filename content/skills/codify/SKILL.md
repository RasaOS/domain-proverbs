---
name: codify
description: Capture a rule that emerged in the current conversation ("from now on do X", "we just decided Y") into a durable place — the project's CLAUDE.md (project-specific) or a domain rule file (Element-level). Confirms the exact wording, asks scope, drafts the edit, shows the diff, applies on approval, always with a one-line "why". The fix for tribal knowledge that evaporates into transcript history. Triggered when the user wants to write down a rule mid-session — e.g. "/codify", "from now on do X", "make this a rule", "we just decided this — write it down".
---

# /codify — Capture a session rule into durable storage

Take a rule that emerged from the conversation and put it where it
survives session boundaries: the project's `CLAUDE.md` (default) or a
domain rule file under `rules/` (when it's general enough to apply
across projects).

A vague rule is worse than no rule. Confirm exact wording with the user
before writing anything.

## Behavior contract

- **Confirm wording first, write second.** Never paraphrase
  unilaterally — the user agrees on the exact text before any file is
  touched.
- **Default scope is project.** Most rules belong in the project's
  `CLAUDE.md`. Promotion to an Element-level rule file needs explicit
  say-so, because it will propagate to every project on the next sync.
- **One rule per invocation.** Don't bulk-codify; each rule is a
  distinct decision, surfaced on its own.
- **Always attach the why.** Write a one-line rationale pointing at the
  situation that prompted the rule. Rules without context rot — the
  next reader can't tell a constraint from an accident.
- **Place it in the right section.** Read the target file first; find
  the section the rule belongs in. If none fits, ask before creating
  one.
- **Never auto-commit.** The edit lands in the working tree; the user
  reviews with `git diff`.

## Process

1. Restate the rule in one or two sentences. Get explicit agreement on
   the wording.
2. Ask scope: **project** (`CLAUDE.md`) or **Element** (a `rules/`
   file). Note the propagation consequence for Element scope.
3. Read the target. Pick the section; propose one if needed.
4. Draft the edit — the rule plus its one-line "why". Show the diff.
5. Apply on approval. Leave it uncommitted.
6. For an Element-level rule, remind to run `bin/check-manifest` if a
   new rule *file* was created (not just an edit).

## What NOT to do

- Don't write a rule the user hasn't agreed to word-for-word.
- Don't promote to Element scope without explicit consent.
- Don't drop the rationale.
- Don't auto-commit.

## Done when

The rule is written in the agreed wording, in the right file and
section, with a one-line why, left in the working tree for review.
