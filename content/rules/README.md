# `rules/` — rule conventions

A **rule file** is durable guidance a Claude session reads to stay
consistent with how this domain works — conventions, gates, and
discipline that outlive any single conversation. Rules are prose the
session *consults*; skills are capabilities the session *runs*.

```
rules/
├── contract-rules.md    ← Element ↔ consumer discipline
├── output-rules.md      ← house communication style
├── authoring-rules.md   ← the enforced authoring lifecycle
└── <topic>-rules.md     ← one file per coherent topic
```

**New rule files start from `content/templates/rule.md.template`** and
must be named `<topic>-rules.md` — `bin/check-shape` enforces the
naming and requires an H1 title.

## How rules load

When this domain is installed into a consumer project, rule files
mirror into `.claude/` (flat, per the `content/rules/ → .claude/`
policy in `rasa.json`). A session reads them as standing context. The
project's own `CLAUDE.md` may point at specific rule files for a given
kind of task ("read `contract-rules.md` before touching the lockfile").

## Authoring principles

- **One topic per file.** `contract-rules.md`, `output-rules.md`,
  `<yours>-rules.md`. A rule file that covers everything gets read for
  nothing.
- **State the rule, then the why.** A rule without its rationale rots —
  the next person can't tell an intentional constraint from an
  accident. One line of "why" per rule.
- **Enforceable beats aspirational.** Where a rule can be backed by a
  guard hook or a script check, say so and wire it. Honest-mistake-proof
  is the realistic bar; adversary-proof is not the goal.
- **Universal here; subject-specific in forks.** Rules in
  `rasa.domain.core` govern the Element contract only. A fork adds its
  own subject rules (testing gates, matter intake, clinical safety) as
  new `*-rules.md` files.

Use the `codify` skill to capture a rule that emerged mid-session into
the right rule file (or the project `CLAUDE.md`) with its rationale
attached.
