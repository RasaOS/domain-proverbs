# Vocabulary — `rasa.domain.proverbs`

The terms this domain uses, and the ones it refuses. Method terms only —
the domain is subject-agnostic and carries no field vocabulary.

Where a term is fully specified elsewhere, the framework chapter is
authoritative and this entry is a pointer.

---

## Core structures

**Subject** — the single node type. Anything the corpus tracks: a topic,
person, event, organization, place, work, or open thread. Kind is a
`type:` field, not a folder. One Subject is one file under
`content/subjects/`. → `framework/subject-model.md`

**Dossier** — the file that holds a Subject. Used interchangeably with
Subject in prose; strictly, the Subject is the thing tracked and the
dossier is the record of it.

**Id** — a Subject's stable kebab-case slug. Assigned once, **never
changed, never recycled**. Links point at ids.

**Standing** — the dossier section holding the current picture, in
prose. **Rewritten wholesale each pass**, never appended to. What you
would say if asked about the subject today.

**Log** — the dossier section holding the dated record of how the
picture moved. **Append-only: never rewritten, reordered, or pruned.**

**Established** — sourced claims that hold. Every entry carries a source
ref and a confidence marker.

**Contested** — sourced claims that conflict, recorded with both sides
and their provenance. A first-class section, not an appendix.

**Open questions** — what is not known, phrased as answerable questions.
Drives the next investigation pass.

**Source record** — the registry entry for a source, under
`content/sources/`, with a stable `src-NNNN` id. → `framework/provenance.md`

**Timeline entry** — a dated fact that relates one or more Subjects,
under `content/timeline/`. A separate cross-cutting axis, not a
Subject. → `framework/cross-linking.md`

## Properties

**Status** — `active` | `dormant` | `closed` | `speculative`. Only
`active` accrues cadence pressure. Closed subjects are never deleted.

**Cadence** — the revisit interval (`7d` | `30d` | `90d` | `365d` |
`none`). Carries urgency. **Not a priority ranking.**

**Due** — computed, never stored: `last_swept + cadence < today`.

**Overdue depth** — `today - (last_swept + cadence)`. The ordering key
for the due queue.

**Confidence** — `high` | `medium` | `low`, a calibrated statement about
the state of the evidence for a claim (or for Standing). `low` is a
normal resting state, not a defect.

**Reliability** — a property of a *source*, distinct from the confidence
of a *claim*. A high-reliability source can support a low-confidence
claim. → `framework/provenance.md`

## Operations

**Investigate** — the *active* mode. Subject-first, question-driven;
fans out to many sources. → `framework/investigation.md`

**Ingest** — the *passive* mode. Source-first; one source fans out to
many subjects. → `framework/ingestion.md`

**Sweep** — the *longitudinal* mode. Revisits a bounded selection,
advances `last_swept`, records change **and no-change**.
→ `framework/longitudinal.md`

**Track** — open a new Subject in the corpus.

**Dossier (verb)** — render the current state of a Subject. Read-only.

**Saturation** — the investigation stopping heuristic: consecutive
search angles returning no newly-registrable sources.

**Routing** — deciding which Subjects a claim from an ingested source
belongs to. A claim touching N Subjects is recorded in all N.

**Reconciliation** — folding a new claim against existing Established
and Contested entries. A contradiction moves a claim to Contested; it
never overwrites.

**Hub** — a Subject that too many others link to, losing discriminating
power. Split it. → `framework/cross-linking.md`

## Terms this domain refuses

| Refused | Use instead | Why |
|---|---|---|
| *priority*, *importance* | `cadence` | Two urgency fields drift apart immediately. |
| *owner*, *assignee* | (nothing) | Single-researcher corpus by design. |
| typed edges (`caused_by`, `employed_by`) | flat `links:` + sourced prose in Standing | Edge vocabularies rot and force premature commitment; a typed edge is an unsourced claim in frontmatter. |
| *archive* | `status: dormant` / `closed` | Nothing is removed from the corpus; it changes status. |
| *delete a subject* | `status: closed` + reason | Dead ends are findings. |
| *summary* (auto-generated) | Standing (written) | Standing is authored synthesis, not derivation. |
| *note* (subject-less) | a Subject | A note with no subject means a Subject is missing. |

## Inherited substrate vocabulary

The RasaOS-level terms (Element, `rasa.json`, Connection Contract,
install vs pull, seed/) are defined in canon and are **not** redefined
here. The forbidden legacy terms (kit, MANIFEST.json, bootstrap/,
foundation.json) are forbidden in this Element too.
