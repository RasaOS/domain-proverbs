# Contract Rules

How a project stays honest about the domain Element installed into it.
**Read this file before touching `.claude/rasa.lock.json`, before
editing anything under `.claude/` that came from the Element, or when
reconciling against an upstream update.**

These rules govern the **Element ↔ consumer** relationship — the one
thing every rasa domain shares. They carry no subject knowledge; a
fork adds its own subject rules as separate `*-rules.md` files.

## The three parties

- **The Element** — the installed domain (e.g. `rasa.domain.code`), a
  fork of `rasa.domain.core`. Ships `content/` (skills, rules, agents)
  and `seed/` (one-time project files).
- **The upstream** — `rasa.domain.core` and any layer above it. Forks
  inherit shape changes from upstream; consumer projects never talk to
  it directly.
- **The consumer project** — where the Element is installed. Owns its
  own `CLAUDE.md` and source; borrows the Element's `content/`.

## The lockfile is the source of truth

`.claude/rasa.lock.json` records **which Element is installed, at what
version, pinned to which commit**:

```json
{
  "element": { "name": "…", "kind": "domain", "version": "…", "repo": "…", "branch": "…" },
  "pinned_sha": "…",
  "installed_at": "…",
  "overrides": []
}
```

- **`pinned_sha` is the real pin.** Version is human-legible; the SHA
  is what a sync reconciles against. Never hand-edit the SHA to "skip
  ahead" — run a sync so the diff is actually applied.
- **The lockfile is written by tooling, read by everyone.** `bin/init`
  stamps it at install; the `sync` skill advances it. A session may
  *read* it to learn its identity but should not casually rewrite it.
- **One Element per lockfile.** A project installs one domain. Stacking
  two domains' `content/` into one `.claude/` is out of contract.

## Installed content is borrowed, not owned

Files that mirrored in from the Element's `content/` (skills, rules,
agents under `.claude/`) belong to the Element. The consumer project
**should not hand-edit them** — the next sync will overwrite the edit,
or worse, silently conflict.

When a project genuinely needs to diverge from an Element file:

- **Record it as an override.** Add the file's path to
  `overrides[]` in the lockfile. A sync then treats it as
  intentionally-diverged: surfaced for awareness, never overwritten
  without explicit approval.
- **An unrecorded local edit is a latent bug.** It looks like
  Element content but isn't; it will drift. If you must edit, override
  it or push the change upstream to the Element.

## Project-owned files are off-limits to sync

Some files are seeded once and owned by the project forever — chiefly
`CLAUDE.md` (seeded `skip-if-exists`) and the project's own history/docs.
A sync **never** touches these. They are the project's, not the
Element's, and the lockfile's `overrides[]` doesn't govern them because
they were never Element-managed to begin with.

## Reference by identity, never by hardcoded path

**No hardcoded filesystem paths at the base level of a domain — ever.**
The template, its `CLAUDE.md`/`README.md`/`rasa.json`, and a fork's
top-level files must not bake in absolute or home-anchored paths
(`~/…`, `/Users/…`, `/home/…`, a workspace-specific tree) to point at
other Elements, the canon, or the workspace. Those paths are
machine- and layout-specific: they rot the moment the workspace moves
or someone clones elsewhere, and they're a portability leak in an
artifact that's meant to be forked and installed anywhere.

Refer to things by **stable identity** instead:

- **Another Element** → its Element name (`rasa.domain.code`) or repo
  slug (`RasaOS/domain-code`), not where it happens to sit on disk.
- **The canon / workspace contracts** → by role ("the workspace canon",
  "the tenant's `CLAUDE.md`"), not an absolute path.
- **Files inside this Element** → paths **relative to the Element root**
  (`content/skills/`, `bin/init`, `.claude/rasa.lock.json`). These are
  portable and correct wherever the Element lives — use them freely.

The carve: **relative-to-root is fine; absolute/home/workspace-anchored
is not.** A path that stays valid after `git clone` anywhere is a
reference; one that assumes a particular machine's layout is a bug.

## Changes flow one direction

Element → consumer, via install and sync. A useful change made *in* a
consumer project does not flow back automatically — it's a deliberate
upstream contribution (edit the fork, commit, tag), reviewed before it
propagates to other projects. This keeps the Element's `content/` a
curated source, not a junk drawer of project-local edits.

## Before you tag an Element release

- Run `bin/check-manifest` — `rasa.json` must be a complete, accurate
  inventory of `content/` + `seed/`. An unregistered file silently
  never ships.
- Run `bin/check-shape` — everything under `content/` must conform to
  the templated shape (see `authoring-rules.md`). A skill without a
  behavior contract or a done-definition doesn't ship.
- Bump `VERSION` + `rasa.json#version` together; write a `CHANGELOG.md`
  entry. Patch = fix, Minor = additive (forks adopt optionally), Major
  = breaking (forks must migrate).
