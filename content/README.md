# `content/` — what `rasa.domain.proverbs` ships

A **hybrid**-pattern domain that is, above all, a **layer**. It requires
`rasa.module.research` and adds four things to that module's topic
folders. Read `PHILOSOPHY.md`, then `framework/topic-overlay.md`.

**The most useful thing to know about this Element is what it does NOT
ship**, because v0.1.0 shipped all of it and was wrong to.

---

## Not shipped — the substrate owns these

| Concern | Owner |
|---|---|
| what a topic is, the folder shape | `rasa.module.research` |
| the current-picture section (`## State of play`) | `rasa.module.research` |
| durable claims + evidence + confidence (`findings.md`) | `rasa.module.research` |
| the live question list (`open-questions.md`) | `rasa.module.research` |
| the dated research log (`log.md`) | `rasa.module.research` |
| the lifecycle `open→active⇄dormant→concluded→archived` | `rasa.module.research` |
| the registry (`research/INDEX.md`) | `rasa.module.research` |
| linking: `@path` · `[[slug]]` · `tags:`/`related:` + `/xref` | `rasa.module.research` |
| opening a topic (`/research new`) | `rasa.module.research` |
| the seam (`.claude/research-canon.md`) | `rasa.module.research` |

## Shipped — the four additions

| Addition | Artifact | Chapter |
|---|---|---|
| Disagreement held open | `contested.md` in each topic folder | `topic-overlay.md` |
| The revisit clock | `cadence:` + `last_swept:` frontmatter | `longitudinal.md` |
| Corpus-wide evidence | `research/sources/` (`src-NNNN`) | `provenance.md` |
| The dated axis | `research/timeline/` | `timeline-axis.md` |

## The knowledge layer

| File | What it is |
|---|---|
| `PHILOSOPHY.md` | the stance: why a layer and not a system, the four tenets, the falsifiable claim |
| `framework/topic-overlay.md` | **the spine** — the division of labour, what the substrate already gives, the additive-frontmatter contract |
| `framework/provenance.md` | the `src-NNNN` registry, the `[S1]`→global join key, reliability vs confidence, link rot |
| `framework/investigation.md` | ACTIVE mode over topic folders; the `Superseded-by:`-vs-contested line; saturation |
| `framework/ingestion.md` | PASSIVE mode; source-first fan-out; why it does not advance `last_swept` |
| `framework/longitudinal.md` | cadence, due arithmetic, no-change recording, health bands, the decay ladder |
| `framework/timeline-axis.md` | what happened vs what the researcher did |
| `vocabulary.md` | overlay terms + the **inherited** table (substrate terms, not redefined) + refused terms |

## The skills

| Skill | Mode | Writes? |
|---|---|---|
| `/investigate` | **active** — topic-first, question-driven | yes |
| `/ingest` | **passive** — source-first, fans out to many topics | yes |
| `/sweep` | **longitudinal** — revisit, diff, health-check | yes |
| `/dossier` | render current state | **read-only** |

All four operate on topics that **already exist**. There is no
topic-opening skill here — that is `/research new`. The inherited
`domain-core` Element-mechanics skills (`sync`, `promote`, `whoami`,
`codify`, `new-skill`, `onboard`, `handoff`, `resume`, `update-docs`) are
kept; `handoff` and `resume` earn their place because research spans
sessions.

## Templates

`overlay-template/` holds the three artifacts this domain adds —
`contested.md`, `source-record.md`, `timeline-entry.md`. It installs to
`.claude/proverbs-overlay-template/`, mirroring how the module installs
its own topic template to `.claude/research-topic-template/`.

Distinct from `templates/`, which holds the **authoring** skeletons
(`SKILL.md.template`, …) validated by `bin/check-shape`. Those are
authoring-time and must never be flipped to auto-install.

## Install shape, and the one collision to know about

Reference content namespaces under `.claude/proverbs/`; overlay templates
under `.claude/proverbs-overlay-template/`; skills to `.claude/skills/`;
rules flat to `.claude/`. `research/sources/` and `research/timeline/`
are scaffolded empty.

**The rules file is `proverbs-rules.md`, not `research-rules.md`.** The
module installs `.claude/research-rules.md`; v0.1.0 of this domain
shipped a file of the same name and would have silently overwritten it.
On any disagreement, the module's file wins for substrate concerns and
this one wins for the four additions.

## The constraint everything answers to

**The overlay must never make the substrate unreadable without it.** A
topic carrying `cadence:`, `last_swept:`, and a `contested.md` is still a
valid `module.research` topic. Drop this domain and every topic survives;
only sweeping stops. A layer that captures its substrate is a fork
wearing a dependency.
