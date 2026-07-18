# Changelog — `rasa.domain.proverbs`

All notable changes to this Element. Format follows the RasaOS
per-Element convention; this file is the authoritative history and is
rolled up into the workspace's aggregated elements changelog (track #2).

---

## v0.1.0 — 2026-07-18 — INITIAL

First release. Forked from `rasa.domain.core` v1.3.0. Ships the research
**method complete** and the **corpus empty**.

### The domain

A subject-agnostic research instrument for the long run — tracks and
manages an open-ended, growing set of subjects (topics, people, events,
organizations, places, works, open threads) without the corpus
degrading as it grows. Hybrid shape (canon SHAPE pattern 3): structural
corpus folders plus a toolkit layer.

### Design decisions locked at v0.1.0

- **One generic Subject node type.** Kind is a `type:` field, not a
  folder. Chosen over typed folders (`people/`, `events/`, `orgs/`)
  because typed folders force a classification decision at creation
  time — when you know the least — and punish reclassification with file
  moves that break every link pointing at the subject.
- **The mutable/immutable split.** `## Standing` (the current picture)
  is rewritten wholesale each pass; `## Log` (how the picture moved) is
  append-only and never rewritten, reordered, or pruned. This is the
  load-bearing decision: the synthesis layer stays bounded while only
  the record layer grows, which is what lets the corpus scale.
- **Seven dossier sections**, fixed and ordered: Standing, Open
  questions, Established, Contested, Timeline, Sources, Log.
- **Provenance enforced, not encouraged.** Claims in Established carry a
  source id and a calibrated confidence marker. There are exactly three
  places an assertion can live; there is no fourth.
- **Contested is first-class.** Conflicting sources are held open, never
  resolved by picking the more convenient one.
- **Nothing is deleted.** Subjects close with a recorded reason; ids are
  never recycled.
- **No-change is a recorded result.** A sweep advances `last_swept` and
  writes a Log line even when nothing changed — otherwise "checked,
  still true" is indistinguishable from "nobody has looked at this in
  two years."
- **Untyped, symmetric links.** Typed edges (`caused_by`, `employed_by`)
  rejected: edge vocabularies rot, force premature commitment, and a
  typed edge is an unsourced claim smuggled into frontmatter.
- **Timeline as a separate axis.** A timeline entry is a dated fact
  relating N subjects (no single subject owns it), distinct from a
  `type: event` Subject, which is a research target with its own open
  questions. Both coexist and reference each other.
- **No priority field.** Cadence carries all the urgency there is; two
  urgency fields drift apart immediately.
- **Staleness computed, never stored.** A subject is due when
  `last_swept + cadence < today`. A stored flag drifts the moment a
  sweep runs and someone forgets to clear it.

### Content shipped

- `content/PHILOSOPHY.md` — five tenets, the three-mode table, what
  "agnostic" commits the Element to, and the falsifiable scaling claim
  stated so it can fail.
- `content/framework/` ×6 — `subject-model.md` (the spine),
  `provenance.md`, `investigation.md`, `ingestion.md`,
  `longitudinal.md`, `cross-linking.md`.
- `content/vocabulary.md` — method terms plus the refused-terms table.
- `content/skills/` ×5 new — `track`, `investigate` (active),
  `ingest` (passive), `sweep` (longitudinal), `dossier` (read-only).
  The inherited `domain-core` Element-mechanics skills are **kept**
  (`sync`, `promote`, `whoami`, `codify`, `new-skill`, `onboard`,
  `handoff`, `resume`, `update-docs`) — `handoff` + `resume` earn their
  place here more than in most domains, because a research corpus spans
  many sessions.
- `content/rules/research-rules.md` — the domain gates, alongside the
  inherited universal rules.
- `content/subjects/`, `content/timeline/`, `content/sources/` — each
  ships `_TEMPLATE.md` + `README.md` and **no content**.

### Manifest

- `shape_pattern` → `hybrid`; 10 capabilities declared under the
  `proverbs.*` namespace.
- `permissions` extended with **`network:fetch`** — `/investigate` does
  live web research, and §9 does not catch under-declaration.
- `rasa.identity` replaced wholesale (the fork inherits `domain-core`'s
  template identity verbatim, which would misdeclare the Element at
  install per SA-025).
- `contract_version` left at **1.3.0** — the last LOCKED and published
  contract. Authored to current canon v1.4.0 rules (post-SA-023, seven
  kinds) but declaring 1.3.0 per the fleet-wide convention; the
  migration is a coordinated `bin/lock-sequence` at the v1.4.0 lock,
  never a per-element bump.
- Template fork-time files removed **and deregistered**:
  `content/SHAPE.md` deleted and its `element.files[]` entry dropped;
  `content/README.md` replaced with the fork's own.

### Gates

`bin/check-manifest` and `bin/check-shape` both exit 0 on a staged tree.

### Not in this release

- No agents (`content/agents/` ships the scaffold + README only). A
  parallel source-triage agent for wide investigation fan-out is a
  plausible v0.2 addition.
- No `requires.elements[]`. The domain stands alone at v0.1.0;
  `rasa.module.calculations` is a plausible future dependency if
  quantitative subjects need a lab-notebook seam.
- No automated corpus tooling (`bin/` carries only the inherited
  `init` / `check-manifest` / `check-shape`). A `bin/due` that computes
  the sweep queue without invoking a model is an obvious v0.2 candidate.
- The name `proverbs` is a codename; no subject commitment is implied.
