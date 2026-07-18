# The Subject model

The single load-bearing structure in this domain. Everything else —
skills, timeline, sources, sweeps — is machinery that reads or writes a
Subject. Read this chapter before any other.

---

## One node type

A **Subject** is anything the corpus tracks: a topic, a person, an
event, an organization, a place, a work, an open thread. There is
**one node type**, not six. Kind is a `type:` field, not a folder.

This is a deliberate choice, and the reason is scale. A typed-folder
model (`people/`, `events/`, `orgs/`) forces a classification decision
at creation time, when you know the least, and punishes you when a
subject turns out to be two things at once — a person who is also an
event, a topic that resolves into an organization. Reclassifying means
moving files and breaking links. With one node type, reclassifying is
editing one line of frontmatter and nothing else moves.

The cost is that `type:` is unenforced by the filesystem. That's
accepted. The corpus is meant to grow to (n) unknown subjects across
unknown categories; structure that has to be decided up front is
structure that will be wrong.

## The file

One Subject is one file: `content/subjects/<id>.md`.

The `id` is a stable kebab-case slug, assigned once, **never changed**.
Titles change, scopes change, spellings get corrected — the id does
not, because links point at it. If a subject genuinely becomes a
different subject, close the old one and open a new one with a
`superseded_by:` pointer. Never recycle an id.

## Frontmatter

```yaml
---
id: some-subject              # stable slug; never changes
title: Some Subject           # human-facing; may change freely
type: topic                   # topic | person | event | org | place | work | thread
status: active                # active | dormant | closed | speculative
opened: 2026-07-18            # date the subject entered the corpus
last_swept: 2026-07-18        # date of the last longitudinal pass
cadence: 30d                  # revisit interval: 7d | 30d | 90d | 365d | none
confidence: low               # high | medium | low — in the STANDING section
tags: [tag-a, tag-b]          # free-form, flat
links: [other-subject]        # ids of related subjects; symmetric by convention
sources: [src-0001]           # ids from the source registry
superseded_by:                # id, only when status: closed by replacement
---
```

Every field except `superseded_by` and `tags` is required. A subject
with missing required frontmatter is a broken subject; `/sweep` reports
it.

### On `status`

- **active** — under investigation; the cadence clock applies.
- **dormant** — real, kept, but not being worked. No cadence pressure.
  Dormant is not failure; most subjects in a large corpus should be
  dormant most of the time.
- **closed** — resolved, or abandoned with a reason recorded in the Log.
  Closed subjects are never deleted.
- **speculative** — opened on a hunch; may not survive first contact.
  Speculative subjects that fail get closed with the reason, not
  deleted — a dead end that isn't recorded gets re-explored later.

### On `confidence`

Confidence describes the **Standing** section only, and it is a claim
about the state of the evidence, not about how strongly the picture is
held. `low` on a well-tended subject is a normal and honest state. A
subject whose confidence has never moved off `low` after several passes
is telling you something — either the sources aren't there, or the
question is malformed.

## The body

Seven sections, in this order. `/dossier` renders them; `/sweep` checks
them.

```markdown
## Standing
## Open questions
## Established
## Contested
## Timeline
## Sources
## Log
```

### `## Standing`

The current picture, in prose. What you would say if asked about this
subject today. **This section is rewritten, not appended to.** It is
always a synthesis of the present state of the evidence, never a
history of how the view evolved — the Log carries that.

Keep it short. If Standing runs past a few paragraphs the subject
probably wants splitting into linked subjects.

### `## Open questions`

What is not known, stated as questions that could actually be answered.
This section drives the next investigation pass — `/investigate` reads
it first. A subject with no open questions and `status: active` is
mislabeled; either it has questions or it's dormant.

### `## Established`

Claims that hold, each with a source reference and a confidence marker.
One claim per bullet. A claim without a source ref does not belong
here — it belongs in Standing as synthesis, or in Open questions as a
suspicion.

```markdown
- The thing happened in 1987. `[src-0012]` (high)
- The two parties met at least twice. `[src-0007, src-0019]` (medium)
```

### `## Contested`

Claims where sources disagree, with **both sides and their sources**.
Contested is a first-class section, not an appendix — the point of a
long-running research corpus is that disagreement is data. Never
silently resolve a contested claim by picking a side; if it resolves,
move it to Established and record the resolution in the Log.

### `## Timeline`

Dated entries relevant to this subject, oldest first. These are
pointers into `content/timeline/`, not the events themselves — see
`cross-linking.md`. A subject with `type: event` still has a timeline;
an event has antecedents.

### `## Sources`

The source ids this dossier draws on, each with a one-line note on what
it was good for. Full source records live in the source registry —
see `provenance.md`.

### `## Log`

**Append-only. Never rewritten, never reordered, never pruned.**

```markdown
- 2026-07-18 — opened. Initial pass from three sources; Standing is thin.
- 2026-08-02 — /sweep: two Established claims demoted to Contested after src-0031.
```

This is the spine of the whole longitudinal design. Standing tells you
what is believed; the Log tells you how the belief moved and when. The
Log is what makes a diff possible six months later, and it is the one
part of the dossier that must survive every rewrite.

---

## Why the split matters

The mutable/immutable split is the reason this corpus can grow without
degrading:

| Layer | Mutability | Grows with time? |
|---|---|---|
| Standing, Open questions | rewritten each pass | **no** — stays short |
| Established, Contested | edited as evidence moves | slowly |
| Timeline, Sources | appended | yes |
| Log | append-only, immutable | yes |

The synthesis layer stays a constant size no matter how long a subject
is tracked. The record layer grows monotonically and is never
compacted. A corpus of 500 subjects tracked for five years is still
readable, because reading means reading Standing — 500 short
paragraphs — and the five years of accumulated record is there when you
need to audit a claim, not in your way when you don't.

The failure mode this avoids: dossiers that become undifferentiated
append-only logs, where the current picture has to be reconstructed by
reading everything. That corpus dies at around thirty subjects.

## What this model deliberately does not have

- **No priority or importance ranking.** Cadence carries urgency; a
  separate priority field would drift out of sync with it immediately.
- **No assignee / owner.** Single-researcher corpus by design. If this
  ever needs multi-author attribution, it goes in the Log line, not
  frontmatter.
- **No typed relations.** `links:` is a flat symmetric list, not
  `parent_of` / `employed_by` / `caused`. Typed edges are seductive and
  they rot — the relation type is better stated in prose in Standing,
  where it can be qualified and sourced. See `cross-linking.md`.
- **No auto-generated summaries.** Standing is written, not derived.
