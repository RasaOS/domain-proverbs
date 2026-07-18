# CLAUDE.md — `rasa.domain.proverbs`

Per-repo working contract for Claude sessions opened inside this folder.
Extends the user-level Claude contract and the `rasa.tenant.rasaos`
tenant contract; does not override them.

> **Who you are (canon SA-025).** `rasa.domain.proverbs` — the RasaOS
> domain for long-running, subject-agnostic research. Substrate:
> **RasaOS**; role: **domain**. The machine-readable identity is
> `rasa.json#rasa.identity`; on install `bin/init` renders it into
> `.claude/rasa-identity.md` alongside the project-owned
> `.claude/rasa-deployment.md`. `/whoami` composes the answer.

## What you are when you're in this folder

You are working on **the Element** — the research *method* and its
machinery. You are almost certainly **not** doing research right now.

This distinction is the one that matters most here, because the two jobs
look similar and have opposite rules:

| | Authoring the Element (here) | Running a deployment |
|---|---|---|
| You edit | `content/framework/`, `content/skills/`, rules | `.claude/proverbs/subjects/` |
| You add | method, chapters, gates | subjects, sources, timeline entries |
| Subject content | **never** | always |
| Gate | `check-manifest` + `check-shape` | `research-rules.md` |

If you find yourself writing about an actual topic, person, or event in
this repo, stop — that content belongs in a deployment's corpus, not in
the Element. The one exception is a brief illustrative example inside a
framework chapter, and it should be obviously a placeholder.

## Read first

1. `content/PHILOSOPHY.md` — the five tenets. Everything else is
   downstream.
2. `content/framework/subject-model.md` — **the spine**. The Subject
   node, the seven sections, the mutable/immutable split. No change to
   this domain makes sense without it.
3. `content/README.md` — what ships and why.
4. `rasa.json` — the formal declaration + `element.files[]` registration.

## Source of truth

- **The workspace canon** — authoritative for everything architectural.
  Spec §6 defines the `domain` kind; `ELEMENT_CONTRACT.md` is the
  contract this Element conforms to (§4 required files, §7 install
  policies, §8 forbidden vocabulary, §9 validation gates).
- **`content/framework/`** — authoritative for the research method. If a
  skill and a chapter disagree, the chapter wins and the skill is a bug.
- **`content/PHILOSOPHY.md`** — authoritative for the stance. If a
  chapter contradicts a tenet, that's a real conflict; resolve it
  explicitly rather than letting both stand.

## The invariants

Do not break these without an explicit decision recorded in the
CHANGELOG. They are load-bearing, and each has a failure mode that only
shows up months later:

1. **One node type.** Kind is `type:`, not a folder. Typed folders force
   classification when you know least and punish reclassification.
2. **Standing is rewritten; the Log is append-only.** The entire scaling
   claim rests on this. Nothing may blur it.
3. **No claim without provenance.** Three places for an assertion —
   Established (sourced), Standing (marked synthesis), Open questions
   (suspicion). There is no fourth.
4. **Contested stays open.** Conflicting sources are held, not resolved
   by convenience.
5. **Nothing is deleted.** Subjects close with a reason; ids are never
   recycled.
6. **No-change is recorded.** A sweep that finds nothing still advances
   `last_swept` and writes a Log line.
7. **Subject-agnostic.** No field vocabulary, no assumed source type, no
   opinion about what is worth researching.

## Adding to this domain

Follow `content/rules/authoring-rules.md` — template → fill → validate →
register → record. Concretely:

- **A new skill:** start from `content/templates/SKILL.md.template`. The
  four sections `## Behavior contract`, `## Process`, `## What NOT to
  do`, `## Done when` are enforced by `bin/check-shape`; frontmatter
  `name:` must match the folder name. Then add it to the enumerating
  note on the `content/skills/` entry in `rasa.json`, or check-shape
  warns.
- **A new framework chapter:** it's covered by the `content/framework/`
  directory entry — no manifest edit needed — but add it to the table in
  `content/README.md` and the README layout block.
- **A new rule:** filename must be `<topic>-rules.md` with a real H1.
- **Anything else under `content/` or `seed/`:** must be covered by an
  `element.files[]` / `seed.files[]` entry, exact or by ancestor
  directory, or `check-manifest` reports UNREGISTERED.

## Gates

```
git add -A            # check-manifest inventories git-tracked files ONLY
bin/check-manifest    # INVENTORY — exit 0 required
bin/check-shape       # STRUCTURE — exit 0 required
```

**Run `git add -A` first.** On an unstaged tree `check-manifest` reports
"0 tracked files" and passes *vacuously*, proving nothing. Both gates
must exit 0 before any tag.

## Don'ts

- **Don't hardcode filesystem paths.** No absolute or home-anchored
  paths anywhere in this Element. References must survive a `git clone`
  to any location. (Codified in `content/rules/contract-rules.md`.)
- **Don't add subject-matter content.** See the table above.
- **Don't bump `contract_version`.** It stays `1.3.0` — the last LOCKED
  and published contract. This Element is authored to canon v1.4.0 rules
  but declares 1.3.0, like the whole fleet. The migration to 1.4.0 is a
  coordinated `bin/lock-sequence` at the v1.4.0 lock, **never** a
  per-element bump.
- **Don't `bin/init` this Element into itself.** `content/` is the
  source; `.claude/` is for sessions. They don't duplicate.
- **Don't add typed link edges.** `links:` is flat and untyped on
  purpose — see `content/framework/cross-linking.md` for the argument.
  A typed edge is an unsourced claim smuggled into frontmatter.
- **Don't add a priority field.** Cadence carries urgency. Two urgency
  fields drift apart immediately.
- **Don't ship on a red gate**, and don't push without an explicit go
  from the user.

## How a version bump works

- **Patch** — typo, doc clarification, skill bug fix. No method change.
- **Minor** — additive: a new skill, a new framework chapter, a new
  optional frontmatter field, a new rule.
- **Major** — a breaking change to the Subject model or the seven
  sections. This invalidates existing corpora and needs a migration
  note; avoid without explicit direction.

Each bump: edit `VERSION`, update `rasa.json#version`, write a
`CHANGELOG.md` entry, run both gates, commit + tag + push. Then register
in the workspace: `elements/REGISTRY.md`, `elements/CHANGELOG.md`
(track #2), and a line in `canon/AUDIT.md`.

## What success looks like

- A deployment can install this and start tracking subjects the same
  day, without deciding anything structural first.
- A corpus tracked under this method for five years is still readable at
  a glance, and any claim in it can be traced to a source and a date.
- The Element still ships zero subject content at v1.0.
