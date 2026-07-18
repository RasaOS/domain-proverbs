# `templates/` — the enforced authoring shapes

Each file here is the canonical skeleton for one authorable artifact
in a domain Element. **Copy the template, fill every TODO — don't
freehand the shape.** The shape is templated first, then followed;
`bin/check-shape` is the enforcement: a missing required section, or a
trigger surface still starting with TODO (a skill/agent `description`,
a rule H1), fails validation. Body TODOs are the author's to clear —
the gate checks shape, not completeness.

| Template | Copy to | Enforced by check-shape |
|---|---|---|
| `SKILL.md.template` | `content/skills/<name>/SKILL.md` | frontmatter `name` == folder, substantive `description`, required sections |
| `rule.md.template` | `content/rules/<topic>-rules.md` | `<topic>-rules.md` naming, H1 title |
| `agent.md.template` | `content/agents/<name>.md` | frontmatter `name`/`description`/`tools`, `name` == filename |

The full lifecycle (template → fill → validate → register → record)
is codified in `content/rules/authoring-rules.md`. The `new-skill`
starter skill scaffolds from `SKILL.md.template` automatically.

**Authoring-time, not install-time.** These templates guide authoring
*in the Element/fork*; they're registered `opt-in` and typically stay
that way — consumer projects don't need them. This directory itself is
exempt from `check-shape` (it holds the TODO skeletons).
