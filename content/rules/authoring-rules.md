# Authoring Rules

How anything gets authored in a domain Element — a skill, a rule, an
agent. **Read this before adding or reshaping anything under
`content/`.** The shape is templated first, then followed;
`bin/check-shape` is the teeth. Subject-neutral: these rules govern
*how* content is authored, never what a domain knows.

## The lifecycle

Every authored artifact follows the same five steps, in order:

1. **Start from the template.** Copy the skeleton from
   `content/templates/` (`SKILL.md.template`, `rule.md.template`,
   `agent.md.template`). Don't freehand the shape — the template IS the
   contract, and freehand drift is exactly what the validator exists to
   catch.
2. **Fill every TODO.** An unfilled trigger surface fails validation —
   a skill/agent `description` or a rule H1 still starting with TODO.
   Body TODOs are the author's to clear: the gate checks shape, not
   completeness. A scaffolded skeleton (e.g. from `new-skill`) may sit
   in `content/` while being filled — but it blocks the tag until every
   TODO is resolved and both gates pass.
3. **Validate.** `bin/check-shape` must pass (structure) and
   `bin/check-manifest` must pass (inventory). Both are release gates —
   a violation blocks the tag, not just the review.
4. **Register.** Add the artifact to the Element's human-readable
   inventories — in `rasa.domain.core` that's the `content/skills/`
   note in `rasa.json` and the tree in `content/README.md`; a fork uses
   its own inventory docs. `check-shape` warns on skills missing from
   the manifest note.
5. **Record.** Write the CHANGELOG entry and bump the version per the
   taxonomy (patch / minor / major). An unrecorded change is invisible
   to forks and consumers — it effectively didn't happen.

## Why enforced, not just documented

- **Predictability is the product.** A consumer picking up any domain
  can trust that every skill has a behavior contract, a process, and a
  done-definition — because the shape is validated, not hoped for.
- **Drift is caught mechanically, not by review.** Prose conventions
  decay one small deviation at a time; a validator fails loudly on the
  first one.
- **The process travels.** Forks inherit the templates, the validator,
  and this rule together — so every domain authored downstream follows
  the same structured process without re-deriving it.

## Boundaries

- **Structure is enforced; substance is judged.** `check-shape`
  validates shape (frontmatter, sections, naming) — it does not grade
  prose quality. Substance review stays human.
- **Extra sections are welcome.** The required sections are a floor,
  not a ceiling (`Output shape`, `When NOT to use`, severity rubrics —
  add what the artifact needs).
- **Forks validate what they ship.** A structural-shape domain with no
  `skills/` passes clean; the validator checks only what exists.
