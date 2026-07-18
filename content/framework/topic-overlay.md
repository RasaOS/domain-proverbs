# The topic overlay

The load-bearing chapter. `rasa.domain.proverbs` does **not** define its own
research structure — it requires `rasa.module.research` and layers on top of
the topic folders that module already provides. Read this before any other
chapter, and read the module's `.claude/research-rules.md` before this one.

---

## The division of labour

`rasa.module.research` owns the **substrate**. This domain owns the
**discipline layer**. Neither reimplements the other.

```
research/<topic-slug>/          ← module.research owns this shape
├── README.md                       State of play · Scope · Related · frontmatter
├── log.md                          dated research log, dead ends included
├── findings.md                     claims + evidence + confidence
├── open-questions.md               the live question list
├── sources.md                      the topic's local reference shelf ([S1])
└── contested.md                ← proverbs ADDS

research/INDEX.md               ← module.research owns
research/sources/               ← proverbs ADDS (corpus-wide registry)
research/timeline/              ← proverbs ADDS (the dated axis)
```

**The rule: if `module.research` already names a thing, use its name.** There
is no `Subject`, no `Standing`, no `Established` in this domain. A topic is a
topic; its current picture is `## State of play`; its durable claims are
findings. Two vocabularies for one structure is precisely the drift the
substrate exists to prevent, and it would be self-inflicted here.

## What the substrate already gives us

Worth stating plainly, because it is more than it first appears and this
domain must not duplicate any of it:

| Concern | Where it already lives |
|---|---|
| One folder per sustained investigation | `research/<topic-slug>/` |
| Current picture, distilled | `README.md` → `## State of play` |
| Chronological record, dead ends kept | `log.md` |
| Durable claims + evidence + confidence | `findings.md` (`F1`, `**Confidence:**`) |
| "A claim without evidence is an open question" | module's `research-rules.md` |
| Live question list, three resolution paths | `open-questions.md` |
| Per-topic reference shelf, local `[S1]` ids | `sources.md` |
| Lifecycle `open→active⇄dormant→concluded→archived` | frontmatter `status:` |
| Topic graph, back-references, tag matching | `[[slug]]` / `@path` / `tags:` + `/xref` |
| The registry/map of all topics | `research/INDEX.md` |
| Where topics live, tag taxonomy, promotion target | `.claude/research-canon.md` (the seam) |

The mutable/immutable split this domain cares about is **already present** in
the substrate: `## State of play` is rewritten, `log.md` is appended. This
domain does not introduce that split — it *enforces* it and builds on it.

## What this domain adds

Four things, and only these four. Each exists because the substrate has no
equivalent, not because a different flavour was preferred.

### 1. `contested.md` — disagreement held open

The substrate resolves conflict with `Superseded-by:` on a finding: one claim
replaces another. That is the right primitive for *corrected* claims and the
wrong one for *unresolved* ones, because it forces a winner at the moment you
have least warrant to pick one.

`contested.md` holds claims where sources genuinely disagree, with both sides
and their provenance, indefinitely, as a first-class artifact. A contest that
resolves migrates to `findings.md` with the resolution recorded in `log.md`.
Silently resolving a contest by adopting the more convenient source is the
single most damaging thing that can be done to a long-running corpus, because
the error becomes invisible and load-bearing.

### 2. Cadence — the revisit clock

The substrate has a lifecycle but **nothing dated**: `status: active` tells
you a topic is live, never when it was last actually looked at. Two added
frontmatter fields close that gap on the topic `README.md`:

```yaml
cadence: 30d        # 7d | 30d | 90d | 365d | none
last_swept: 2026-07-18
```

A topic is **due** when `last_swept + cadence < today`. Computed on read,
never stored — a stored flag drifts the moment a sweep runs and someone
forgets to clear it. Only `status: active` accrues cadence pressure;
`dormant`, `concluded`, and `archived` have no clock.

Cadence is **not** priority. The substrate has no importance ranking and this
domain does not add one; cadence carries all the urgency there is.

### 3. `research/sources/` — the corpus-wide registry

The substrate's `sources.md` is per-topic with local `[S1]` ids. That is
correct for a self-contained investigation and insufficient for a corpus,
because the same source routinely bears on several topics and a local id
cannot express that a claim in topic A and a claim in topic B rest on the
*same* evidence.

This domain adds a corpus-wide registry with stable `src-NNNN` ids,
reliability ratings, and captured excerpts. **Both coexist:** a topic's
`sources.md` keeps its local shelf and gains a column pointing at the global
id. → `provenance.md`

### 4. `research/timeline/` — the dated axis

The substrate has no dated structure other than `log.md`, which records what
*the researcher* did, not what *happened*. A timeline entry is a dated fact
that relates N topics and is owned by none of them. → `timeline-axis.md`

## Frontmatter contract

The topic `README.md` frontmatter is the module's, plus this domain's two
fields. Everything else is untouched:

```yaml
---
id: {{RT_ID}}              # module.research
slug: some-topic           # module.research
status: active             # module.research
created: 2026-07-18        # module.research
updated: 2026-07-18        # module.research
tags: []                   # module.research
related: []                # module.research
cadence: 30d               # ← proverbs
last_swept: 2026-07-18     # ← proverbs
---
```

Additive only. A topic carrying these fields is still a perfectly valid
`module.research` topic; a deployment that later drops this domain keeps
every topic intact and simply stops sweeping. **The overlay must never make
the substrate unreadable without it.** That is the design constraint on
everything in this chapter.

## What is deliberately NOT added

- **No new node type.** Topics are the only unit. An earlier draft of this
  domain defined its own `Subject` node in `subjects/<id>.md`; it was
  removed at v0.2.0 because it duplicated `research/<topic-slug>/` under a
  different name.
- **No second linking system.** The substrate's three layers (`@path`,
  `[[slug]]`, `tags:`/`related:`) are sufficient and `/xref` already
  reconciles them. This domain adds no link syntax.
- **No competing index.** `research/INDEX.md` is the registry. `/dossier`
  reads it; it does not maintain a rival.
- **No `/track` skill.** Opening a topic is `/research new`, which already
  exists. This domain's skills operate on topics that already exist.
- **No priority field.** See above.

## Where the two rule files sit

The module installs `.claude/research-rules.md` (substrate discipline). This
domain installs `.claude/proverbs-rules.md` (the overlay's gates). Distinct
filenames on purpose — at v0.1.0 this domain also shipped a
`research-rules.md` and would have overwritten the module's on install. On
any disagreement, **the module's file wins for substrate concerns** and this
one wins for the four additions above.
