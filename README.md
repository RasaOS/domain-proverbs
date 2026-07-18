# RasaOS Domain · Proverbs

`rasa.domain.proverbs` — the **epistemic and longitudinal discipline
layer** over [`rasa.module.research`](https://github.com/RasaOS/module-research).

- **Kind:** `domain` · **Shape:** hybrid · **Version:** 0.2.0
- **Requires:** `rasa.module.research >=0.1.3`
- **Contract:** Element Contract v1.3.0
- **Ships zero subject content.**

---

## What it is

`rasa.module.research` is the research system — one folder per topic,
with a current picture, a log, findings, open questions, sources, a
lifecycle, an index, and a three-layer link graph.

This domain **does not reimplement any of that**. It requires the module
and adds the four things that module has no equivalent for.

| Addition | Why the substrate needs it |
|---|---|
| **`contested.md`** | The module resolves conflict with `Superseded-by:` — one claim replaces another. Right for *corrected* claims, wrong for *unresolved* ones: it forces a winner when you have least warrant to pick one. |
| **`cadence:` + `last_swept:`** | The module has a lifecycle but **nothing dated**. `status: active` says a topic is live; it never says when it was last actually looked at. |
| **`research/sources/`** | Per-topic `[S1]` ids can't express that claims in two topics rest on the *same* evidence. A corpus-wide `src-NNNN` registry can, and tracks source **reliability** as distinct from claim **confidence**. |
| **`research/timeline/`** | `log.md` records what *the researcher did*, not what *happened*. |

## The rule that makes the clock worth anything

**A sweep records no-change.** `last_swept` advances and `log.md` gets a
line even when nothing moved — because otherwise "checked, still true"
and "nobody has looked at this in two years" are the same state on disk.

That distinction is the difference between a research instrument and an
archive, and it is the single largest thing this domain contributes.

## Layout of a topic under the overlay

```
research/<topic-slug>/          ← module.research owns this shape
├── README.md                       State of play · Scope · frontmatter
│                                   + cadence: + last_swept:   ← proverbs
├── log.md                          what the researcher did
├── findings.md                     claims + evidence + confidence
├── open-questions.md               the live question list
├── sources.md                      local [S1] shelf, + global src ids
└── contested.md                ← proverbs

research/INDEX.md               ← module.research
research/sources/               ← proverbs (src-NNNN registry)
research/timeline/              ← proverbs (dated axis)
```

## Skills

| Skill | Mode | Writes? |
|---|---|---|
| `/investigate` | active — topic-first, question-driven | yes |
| `/ingest` | passive — source-first, fans out to many topics | yes |
| `/sweep` | longitudinal — revisit, diff, health-check | yes |
| `/dossier` | render current state | read-only |

All operate on topics that already exist. **Opening a topic is
`/research new`** — the module's skill. This domain deliberately ships no
equivalent.

## Vocabulary

The substrate's, throughout. A **topic** is a topic; its current picture
is **State of play**; its durable claims are **findings**. This domain
introduces no synonyms — see `content/vocabulary.md`, which points at the
module's definitions rather than restating them.

## Install

```
bin/init /path/to/target
```

Reference content → `.claude/proverbs/`; overlay templates →
`.claude/proverbs-overlay-template/`; skills → `.claude/skills/`; rules
flat → `.claude/`. `research/sources/` and `research/timeline/`
scaffolded empty.

**Install `rasa.module.research` first** — this domain is a layer over
it, and its skills assume the topic structure exists.

> **Collision note:** the rules file is **`proverbs-rules.md`**, not
> `research-rules.md`. The module owns `.claude/research-rules.md`;
> v0.1.0 of this domain shipped a same-named file that would have
> overwritten it on install. Fixed in v0.2.0.

## The design constraint

**The overlay must never make the substrate unreadable without it.** A
topic carrying this domain's fields is still a valid `module.research`
topic. Drop this domain and every topic survives intact; only sweeping
stops. A layer that captures its substrate is a fork wearing a
dependency.

## Gates

```
git add -A
bin/check-manifest    # INVENTORY — everything tracked is registered
bin/check-shape       # STRUCTURE — everything authored follows the template
```

Exit 0 on both is the release gate.

## History worth knowing

**v0.1.0 was a system, not a layer** — it defined its own
file-per-subject structure (`subjects/<id>.md` with `## Standing`,
`## Established`, `## Open questions`, `## Log`), every part of which
already existed in `rasa.module.research` under a different name. The
overlap was found after that version shipped. v0.2.0 deletes the
duplicate structure and keeps only what is genuinely additive. The
CHANGELOG records it in full rather than quietly rewriting history.

## On the name

`proverbs` is a codename, not a subject commitment.
