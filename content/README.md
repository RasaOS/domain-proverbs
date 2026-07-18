# `content/` — what `rasa.domain.proverbs` ships

A **hybrid**-pattern domain (canon SHAPE pattern 3): structural
subdirectories that hold the corpus, plus a toolkit layer of skills and
rules that operate on it.

Read `PHILOSOPHY.md` first, then `framework/subject-model.md`. Those two
carry the design; everything else implements it.

---

## The structural half — where research lives

| Folder | Holds | Ships |
|---|---|---|
| `subjects/` | one file per tracked Subject | **empty** + template + README |
| `timeline/` | dated entries relating Subjects | **empty** + template + README |
| `sources/` | the source registry, one record per source | **empty** + template + README |

All three ship empty of content on purpose. This Element is
subject-agnostic: it carries the method, never anyone's research. A
deployment fills them.

## The toolkit half — machinery

| Folder | Holds |
|---|---|
| `skills/` | the five domain skills + the inherited Element-mechanics skills |
| `rules/` | `research-rules.md` (the domain gates) + the inherited universal rules |
| `agents/` | subagent definitions (none shipped yet) |
| `templates/` | authoring skeletons — **authoring-time only, never installed** |

### The five domain skills

| Skill | Mode | Writes? |
|---|---|---|
| `/track` | open a new Subject | yes |
| `/investigate` | **active** — pull from outside | yes |
| `/ingest` | **passive** — file supplied material | yes |
| `/sweep` | **longitudinal** — revisit, diff, health-check | yes |
| `/dossier` | render current state | **read-only** |

The inherited skills from `rasa.domain.core` (`sync`, `promote`,
`whoami`, `codify`, `new-skill`, `onboard`, `handoff`, `resume`,
`update-docs`) are kept — a long-running research corpus spans many
sessions, so `/handoff` and `/resume` earn their place here more than in
most domains.

## The knowledge layer

| File | What it is |
|---|---|
| `PHILOSOPHY.md` | the stance: five tenets, three modes, the falsifiable scaling claim |
| `framework/subject-model.md` | **the spine** — the Subject node, the seven sections, the mutable/immutable split |
| `framework/provenance.md` | source registry, reliability vs confidence, citation form, link rot |
| `framework/investigation.md` | the active mode: question-driven passes, reconciliation, saturation |
| `framework/ingestion.md` | the passive mode: source-first routing, the new-subject threshold |
| `framework/longitudinal.md` | the ongoing mode: cadence, due arithmetic, no-change recording, health checks |
| `framework/cross-linking.md` | the graph: untyped symmetric links, the timeline axis, hub splitting |
| `vocabulary.md` | method terms, and the terms this domain refuses |

## Install shape

Subject content namespaces under `.claude/proverbs/` in a consumer, per
the domain convention. Skills install to `.claude/skills/`, rules flat
to `.claude/`. `templates/` stays `opt-in` — authoring-time only, and
must never be flipped to auto-install.

The three corpus folders install their README + template so a fresh
deployment gets the shape and the discipline, then grows its own
content.

## The one thing to not get wrong

**Standing is rewritten. The Log is append-only.** Every other rule in
this domain is downstream of that split. A corpus that appends to
Standing becomes unreadable at around thirty subjects; a corpus that
rewrites the Log loses the ability to audit its own history, which is
the only thing a long-running research instrument uniquely offers.
