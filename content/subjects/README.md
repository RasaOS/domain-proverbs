# `content/subjects/` — the corpus

One file per tracked Subject: `<id>.md`. This is where the research
actually lives. Everything else in this Element is machinery for
reading and writing these files.

**This folder ships empty.** `rasa.domain.proverbs` is subject-agnostic —
it carries the method, not anyone's research. A deployment fills it.

## The authority

`framework/subject-model.md` is the specification for these files —
frontmatter fields, the seven body sections, the mutable/immutable
split, and the reasoning behind each. It wins over anything written
here. This README is orientation only.

## Naming

`<id>.md`, where the id is a stable kebab-case slug assigned once and
**never changed or recycled**. Links point at ids, so an id change
breaks the graph silently. Titles are free to change; ids are not.

If a subject genuinely becomes a different subject, close the old one
with `superseded_by:` and open a new one. Do not rename.

## The seven sections

Every dossier carries all seven, in order, even when empty:

| Section | Mutability | Purpose |
|---|---|---|
| `## Standing` | rewritten each pass | the current picture |
| `## Open questions` | rewritten | what drives the next pass |
| `## Established` | edited as evidence moves | sourced claims that hold |
| `## Contested` | edited | sourced claims that conflict |
| `## Timeline` | appended | pointers into `../timeline/` |
| `## Sources` | appended | source ids drawn on |
| `## Log` | **append-only** | how the picture moved, and when |

The Standing/Log split is the load-bearing design decision of this
domain. Standing tells you what is believed; the Log tells you how the
belief got there. Neither substitutes for the other, and the Log is
never rewritten.

## Working with this folder

| Task | Skill |
|---|---|
| Open a new subject | `/track` |
| Research an existing one | `/investigate` |
| File supplied material into it | `/ingest` |
| Revisit what's due or stale | `/sweep` |
| Read the current state | `/dossier` |

Start from `_TEMPLATE.md` if creating a dossier by hand — but `/track`
is the supported path, because it also checks id collisions and writes
the symmetric back-links.

## What does not belong here

- **Source records** — those go in `../sources/`, referenced by id.
- **Dated events** — those go in `../timeline/`, referenced by id. A
  subject's `## Timeline` section holds pointers, not the events.
- **Working notes with no subject** — a note that doesn't belong to a
  subject is a signal that a subject is missing, not that the model
  needs a scratch folder.
- **Bulk-copied third-party material.** Register by reference and short
  excerpt; see `framework/provenance.md`.
