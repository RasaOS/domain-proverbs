# `agents/` — subagent conventions

A **subagent** is a scoped Claude agent a session can dispatch for a
self-contained sub-task (a focused review, a broad search, a
structured extraction). Each agent is one `.md` file: frontmatter
declaring its name, tools, and dispatch triggers, plus a body that is
the agent's system prompt.

```
agents/
└── <name>.md           ← frontmatter (name, description, tools) + system prompt
```

## Why the starter set ships none

Subagents are almost always **subject-specific** — a `code-reviewer`,
a `matter-auditor`, a `doc-scanner` all encode domain judgment.
There's no domain-agnostic subagent worth shipping, so
`rasa.domain.core` ships this convention doc and an empty folder. Forks
populate it.

## `<name>.md` shape

**The canonical skeleton lives at `content/templates/agent.md.template`
— copy it; don't freehand.** `bin/check-shape` enforces the shape:
frontmatter `name` (== the filename stem), `description` (the dispatch
conditions), and `tools` (least-privilege). The body is the agent's
system prompt: its role, what it returns (its final message IS the
return value — raw findings, not chat prose), and what it must never
do.

## Authoring principles

- **Least privilege.** Grant only the tools the agent's job requires. A
  read-only reviewer gets no `Write`/`Edit`.
- **One responsibility.** An agent that reviews *and* fixes *and*
  reports is three agents. Narrow scope makes results composable.
- **Return data, not conversation.** The agent's final message is
  consumed by the caller — instruct it to return structured findings.
- **Subject-aware is expected.** Unlike the starter skills/rules, fork
  agents are meant to encode the fork's domain.
