# RasaOS Domain · Proverbs

`rasa.domain.proverbs` — a **subject-agnostic research instrument for the
long run**. It tracks and manages an open-ended, growing set of
subjects — topics, people, events, organizations, places, works, open
threads — without the corpus degrading as it grows.

- **Kind:** `domain` · **Shape:** hybrid (structural corpus + toolkit)
- **Version:** 0.1.0 · **Contract:** Element Contract v1.3.0
- **Ships zero subject content.** The method, the templates, and the
  machinery — never anyone's research.

---

## The problem it solves

Long-running research corpora fail in one of two ways.

Append-only ones become unreadable: answering "what do we currently
believe about X" requires reading everything ever written about X. These
die at around thirty subjects.

Rewrite-only ones lose their own history: you can see what is believed
but not how the belief moved, when it was last checked, or which source
changed it. These can't audit themselves, which is the one thing a
long-running instrument uniquely offers.

This domain refuses the choice. Every dossier carries **both layers**.

## The load-bearing decision

| Layer | Sections | Mutability | Grows over time? |
|---|---|---|---|
| **Synthesis** | `## Standing`, `## Open questions` | rewritten each pass | **no** — stays short |
| **Evidence** | `## Established`, `## Contested` | edited as evidence moves | slowly |
| **Record** | `## Timeline`, `## Sources`, `## Log` | appended; the Log is **immutable** | yes |

The synthesis layer stays a constant size no matter how long a subject
is tracked. The record layer grows monotonically and is never compacted.
A corpus of 500 subjects tracked for five years is still readable,
because reading means reading Standing — 500 short paragraphs — and the
five years of record is there when you need to audit a claim, not in
your way when you don't.

## One node type

A **Subject** is anything tracked. Kind is a `type:` field, not a
folder — so reclassifying a subject that turns out to be two things at
once is a one-line frontmatter edit, not a file move that breaks every
link pointing at it. Ids are stable, never changed, never recycled.

Full specification: [`content/framework/subject-model.md`](content/framework/subject-model.md).

## Three modes, one corpus

| Mode | Skill | Direction | Answers |
|---|---|---|---|
| **Active** | `/investigate` | pulls from outside | *What can I find out about this?* |
| **Passive** | `/ingest` | pushes from supplied material | *What does this source tell me, and about which subjects?* |
| **Longitudinal** | `/sweep` | revisits what's here | *What changed, what went stale, what needs another look?* |

Plus `/track` to open a subject and `/dossier` to render current state
(read-only).

Investigation is subject-first and fans out to many sources. Ingestion
is source-first and fans out to many subjects — one source usually
updates several dossiers. Sweeps are what make this *ongoing* rather
than an archive: **a sweep advances `last_swept` and writes a Log line
even when nothing changed**, because otherwise you cannot distinguish
"checked, still true" from "nobody has looked at this in two years."

## What is enforced

Not encouraged — enforced, by `content/rules/research-rules.md` and by
the skills themselves:

- No unsourced claim in `## Established`. Synthesis goes in Standing,
  marked as synthesis; suspicion goes in Open questions.
- The Log is append-only. Never rewritten, reordered, or pruned.
- Contested claims are never silently resolved by picking the more
  convenient source.
- Closed subjects are never deleted — a dead end that isn't recorded
  gets re-explored in eighteen months.
- "Nothing found" is recorded, never replaced with plausible-sounding
  synthesis.
- Confidence markers are calibrated honestly. `low` is a normal
  resting state for a well-tended subject.

## Layout

```
content/
├── PHILOSOPHY.md          the stance: five tenets, three modes, the scaling claim
├── vocabulary.md          method terms + the terms this domain refuses
├── framework/             the method, six chapters
│   ├── subject-model.md      THE SPINE — read this first
│   ├── provenance.md         sources, reliability vs confidence, link rot
│   ├── investigation.md      active mode
│   ├── ingestion.md          passive mode
│   ├── longitudinal.md       ongoing mode
│   └── cross-linking.md      the graph + the timeline axis
├── subjects/              THE CORPUS — ships empty (template + README)
├── timeline/              dated entries relating subjects — ships empty
├── sources/               the source registry — ships empty
├── skills/                5 domain skills + inherited Element mechanics
├── rules/                 research-rules + inherited universal rules
├── agents/                none shipped at v0.1.0
└── templates/             authoring skeletons (opt-in, never installed)
```

## Install

```
bin/init /path/to/target
```

Subject content namespaces under `.claude/proverbs/`; skills to
`.claude/skills/`; rules flat to `.claude/`. The three corpus folders
install their README + template so a fresh deployment inherits the shape
and the discipline, then grows its own content.

The corpus it produces is plain markdown with YAML frontmatter and no
tool lock-in. If the machinery disappears, the research survives.

## Gates

```
git add -A
bin/check-manifest    # INVENTORY — everything tracked is registered
bin/check-shape       # STRUCTURE — everything authored follows the template
```

Exit 0 on both is the release gate.

## On the name

`proverbs` is a codename, not a subject. The domain carries no
commitment to proverbs as a field of study. The fitting reading, if one
is wanted: a proverb is a durable claim distilled from long accumulated
observation — which is what a well-tended `## Standing` section is.
