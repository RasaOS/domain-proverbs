# CLAUDE.md — `rasa.domain.proverbs`

Per-repo working contract for Claude sessions opened inside this folder.
Extends the user-level Claude contract and the `rasa.tenant.rasaos`
tenant contract; does not override them.

> **Who you are (canon SA-025).** `rasa.domain.proverbs` — the RasaOS
> discipline layer over `rasa.module.research`. Substrate: **RasaOS**;
> role: **domain**. The machine-readable identity is
> `rasa.json#rasa.identity`; on install `bin/init` renders it into
> `.claude/rasa-identity.md` alongside the project-owned
> `.claude/rasa-deployment.md`. `/whoami` composes the answer.

## What you are when you're in this folder

You are working on **a layer, not a system**. This is the fact that most
often gets lost, and losing it is how v0.1.0 went wrong.

`rasa.module.research` owns the research substrate. This domain requires
it and adds exactly four things. **Before adding anything here, check
whether the module already has it** — clone
`RasaOS/module-research` and read its `content/research-rules.md` and
`content/topic-template/`. If the module has it, this domain does not.

You are also almost certainly **not doing research** right now:

| | Authoring the Element (here) | Running a deployment |
|---|---|---|
| You edit | `content/framework/`, `content/skills/`, rules | `research/<topic-slug>/` |
| You add | discipline, chapters, gates | topics, sources, timeline entries |
| Subject content | **never** | always |
| Gate | `check-manifest` + `check-shape` | `proverbs-rules.md` |

## Read first

1. `content/PHILOSOPHY.md` — why a layer, the four tenets.
2. `content/framework/topic-overlay.md` — **the spine**. The division of
   labour and the additive-frontmatter contract.
3. The module's `research-rules.md` — the substrate you sit on.
4. `rasa.json` — the declaration + `element.files[]` registration.

## Source of truth

- **The workspace canon** — authoritative for everything architectural.
- **`rasa.module.research`** — authoritative for every substrate concern:
  what a topic is, the folder shape, the lifecycle, the index, linking.
  If this domain and the module disagree there, **the module wins and
  this domain has a bug.**
- **`content/framework/`** — authoritative for the four additions. If a
  skill and a chapter disagree, the chapter wins.
- **`content/PHILOSOPHY.md`** — authoritative for the stance.

## The invariants

Do not break these without an explicit decision recorded in the
CHANGELOG:

1. **Stay additive.** A topic carrying `cadence:`, `last_swept:`, and a
   `contested.md` is still a valid `module.research` topic. Drop this
   domain and every topic survives.
2. **Use the substrate's names.** topic (not Subject), State of play (not
   Standing), findings (not Established). No synonyms, ever.
3. **No duplication.** No second node type, index, link syntax, or
   topic-opening skill.
4. **Contested stays open.** `Superseded-by:` is for corrected claims;
   `contested.md` is for unresolved ones.
5. **No-change is recorded.** A sweep advances `last_swept` and writes a
   `log.md` line even when nothing moved.
6. **Reliability ≠ confidence.** Source property vs claim property; never
   collapsed.
7. **Subject-agnostic.** No field vocabulary, no assumed source type.

## The collision to never re-introduce

The module installs `.claude/research-rules.md`. This domain installs
`.claude/proverbs-rules.md`. **Never rename this domain's rules file to
`research-rules.md`** — v0.1.0 did, and it would have silently
overwritten the module's on install. Same discipline applies to any
future file: check the module's `element.files[]` targets before
choosing an install path.

## Adding to this domain

Follow `content/rules/authoring-rules.md` — template → fill → validate →
register → record. Concretely:

- **A new skill:** start from `content/templates/SKILL.md.template`. The
  four sections `## Behavior contract`, `## Process`, `## What NOT to
  do`, `## Done when` are enforced by `bin/check-shape`; frontmatter
  `name:` must match the folder. Then update the enumerating note on the
  `content/skills/` entry in `rasa.json` or check-shape warns.
- **A new framework chapter:** covered by the `content/framework/`
  directory entry — no manifest edit — but update the tables in
  `content/README.md` and the root `README.md`.
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
"0 tracked files" and passes *vacuously*.

## Don'ts

- **Don't hardcode filesystem paths.** References must survive a
  `git clone` to any location.
- **Don't add subject-matter content.** See the table above.
- **Don't add anything the module already has.** Check first.
- **Don't bump `contract_version`.** It stays `1.3.0` — the last LOCKED
  and published contract. Authored to canon v1.4.0 rules, declaring
  1.3.0, like the whole fleet. Migration is a coordinated
  `bin/lock-sequence`, **never** a per-element bump.
- **Don't `bin/init` this Element into itself.**
- **Don't add a priority field.** Cadence carries urgency.
- **Don't seed research-root files.** `research/INDEX.md` and
  `.claude/research-canon.md` are the module's to seed; duplicating them
  races the module's install.
- **Don't ship on a red gate**, and don't push without an explicit go.

## How a version bump works

- **Patch** — typo, doc clarification, skill bug fix.
- **Minor** — additive: a new skill, chapter, optional frontmatter field.
- **Major** — a breaking change to the overlay contract, or a change to
  the `requires` floor that forces deployments to upgrade the module.

Each bump: edit `VERSION`, update `rasa.json#version`, write a
`CHANGELOG.md` entry, run both gates, commit + tag + push. Then register
in the workspace: `elements/REGISTRY.md`, `elements/CHANGELOG.md`
(track #2), and a line in `canon/AUDIT.md`.

**Watch the `requires` floor.** If the module ships a change this domain
depends on, raise `requires.elements[].version` in the same bump — a
silent floor is how a layer breaks in the field.

## What success looks like

- A deployment with `module.research` installed can add this and start
  sweeping the same day, with no restructuring of existing topics.
- Any topic can answer both "what do we currently believe" and "when was
  that last actually checked," in bounded time.
- Dropping this domain leaves every topic intact.
- The Element still ships zero subject content at v1.0.
