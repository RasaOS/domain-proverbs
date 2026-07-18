# `skills/` — skill conventions

A **skill** is a named, invokable capability a Claude session runs on
request (e.g. `/onboard`, `/sync`). Each skill is one folder holding a
`SKILL.md`; scripts and templates live alongside it when the skill has
deterministic plumbing.

```
skills/
└── <name>/
    ├── SKILL.md        ← required: frontmatter + behavior contract
    ├── <name>.sh|.py   ← optional: the deterministic mechanics
    └── templates/      ← optional: files the skill emits
```

## `SKILL.md` shape

**The canonical skeleton lives at `content/templates/SKILL.md.template`
— copy it; don't freehand.** `bin/check-shape` enforces the shape:
frontmatter `name` (== the folder) + a substantive `description`, and
the required sections `## Behavior contract`, `## Process`,
`## What NOT to do`, `## Done when`. Extra sections (`Output shape`,
`When NOT to use`, …) are welcome — the required set is a floor. The
full lifecycle (template → fill → validate → register → record) is in
`../rules/authoring-rules.md`.

What each required section is *for*:

- **description (frontmatter)** — the trigger surface; the router
  matches on it.
- **Behavior contract** — the hard rules: what it always/never does,
  and its consent model (report-only / writes files / edits source).
- **Process** — the numbered steps, in reading order.
- **What NOT to do** — the concrete wrong turns it must refuse.
- **Done when** — the observable definition of finished.

## Authoring principles

- **The description is the trigger surface.** The router matches on it.
  Front-load concrete phrases the user would actually say. Vague
  descriptions misfire.
- **Separate plumbing from judgment.** If part of the skill is
  deterministic (which files to touch, how to stamp a lockfile), put
  that in a script and let `SKILL.md` own the judgment. Three tiers:
  **none** (pure AI), **partial** (script plumbs, AI synthesizes),
  **full** (script end-to-end, AI just routes).
- **Domain-agnostic here; subject-aware in forks.** Starter skills in
  `rasa.domain.core` reference only the Element contract. A fork's own
  skills may reference the fork's subject freely.
- **Consent is explicit.** A skill that mutates files says so and
  never auto-commits — edits land in the working tree for the user to
  review.

Use the `new-skill` skill to scaffold a new one that already follows
these conventions.
