# Vocabulary — `rasa.domain.proverbs`

Overlay terms only. The substrate's vocabulary is **inherited, not
redefined** — see the inherited table below and
`.claude/research-rules.md` for its definitions.

Where a term is fully specified in a chapter, that chapter is
authoritative and the entry here is a pointer.

---

## Inherited from `rasa.module.research` — do not redefine

These are the substrate's. This domain uses them exactly as the module
defines them, and ships no synonym for any of them.

| Term | What it is | Never call it |
|---|---|---|
| **topic** | one sustained investigation, a folder at `research/<topic-slug>/` | ~~Subject~~ |
| **State of play** | the topic's distilled current picture (in its `README.md`) | ~~Standing~~ |
| **findings** | durable claims + evidence + confidence (`findings.md`, `F1` form) | ~~Established~~ |
| **open questions** | the live question list (`open-questions.md`) | — |
| **log** | the dated record of what the researcher did (`log.md`) | — |
| **sources** (local) | the topic's own reference shelf, local `[S1]` ids | — |
| **lifecycle** | `open → active ⇄ dormant → concluded → archived` | — |
| **INDEX** | `research/INDEX.md`, the registry of all topics | — |
| **the three layers** | `@path` context pointers · `[[slug]]` topic graph · `tags:`/`related:` matching | — |
| **`/xref`** | the module's skill that reconciles the three layers + back-references | — |
| **the seam** | `.claude/research-canon.md` — where topics live, tag taxonomy, promotion target | — |

The struck-through column is not decoration. Those were this domain's own
v0.1.0 terms for the same structures, removed in v0.2.0.

## Added by this domain

### Contested claims

**contested** — a claim where sources genuinely disagree, held open with
both sides and their evidence. Lives in `contested.md` inside the topic
folder. → `framework/topic-overlay.md`

**contest** — one such disagreement, with an id (`C1`) and a
`**Resolution:**` field that stays `(unresolved)` until it migrates to
`findings.md`.

**superseded vs contested** — `Superseded-by:` (the substrate's) is for
**corrected** claims, where you have warrant to name the wrong side.
`contested.md` is for **unresolved** ones, where you do not.

### The revisit clock

**cadence** — the revisit interval on a topic (`7d` | `30d` | `90d` |
`365d` | `none`). Carries urgency. **Not a priority ranking.**

**`last_swept`** — the date of the last longitudinal pass. Distinct from
the substrate's `updated:`, which moves on any edit.

**due** — computed, never stored: `last_swept + cadence < today`.

**overdue depth** — `today - (last_swept + cadence)`. The ordering key
for the due queue, most overdue first.

**sweep** — the longitudinal pass over a bounded selection. Advances
`last_swept` and writes a `log.md` line **even on no-change**.
→ `framework/longitudinal.md`

**no-change** — a real, recorded sweep result. The distinction between
"checked, still true" and "unlooked-at for two years."

**decay / demotion** — the ladder a repeatedly-unmoving topic descends:
`7d → 30d → 90d → 365d → none`, then `status: dormant`.

### Provenance

**`src-NNNN`** — a stable corpus-wide source id. Assigned once, **never
recycled**. Lives in `research/sources/`. → `framework/provenance.md`

**the join key** — the role `src-NNNN` plays: a topic's local `[S1]`
stays the citation; the global id is what lets two topics be seen to rest
on the same evidence.

**reliability** — a property of a **source**. Distinct from the
substrate's **confidence**, which is a property of a **claim**. A
high-reliability source can support a low-confidence claim; three
independent low-reliability sources can support a high-confidence one.

**capture / the vanished-page test** — retrieved date plus enough excerpt
to reconstruct the claim if the page disappears.

### The timeline axis

**timeline entry** — a dated fact relating N topics and owned by none, at
`research/timeline/`. Records **what happened**, as opposed to `log.md`,
which records **what the researcher did**.
→ `framework/timeline-axis.md`

**`date_precision`** — `day` | `month` | `year` | `circa`. `year` is
truncated (the year is known, the day is not); `circa` is estimated (the
year itself is uncertain).

### Modes

**investigate** — the ACTIVE mode. Topic-first, question-driven; fans out
to many sources. → `framework/investigation.md`

**ingest** — the PASSIVE mode. Source-first; one source fans out to many
topics. Does **not** advance `last_swept`.
→ `framework/ingestion.md`

**dossier** — render a topic's current state. Read-only.

**saturation** — the investigation stopping heuristic: consecutive search
angles returning no newly-registrable sources.

**routing** — deciding which topics a claim from an ingested source
belongs to. A claim touching N topics is recorded in all N.

## Terms this domain refuses

| Refused | Use instead | Why |
|---|---|---|
| *priority*, *importance* | `cadence` | Two urgency fields drift apart immediately. |
| a `due:` or `stale:` field | compute it | A stored flag rots the first time nobody clears it. |
| a second confidence scale | the substrate's `**Confidence:**` | One claim, one confidence. Reliability is a separate axis on the *source*. |
| a second index | `research/INDEX.md` | The substrate owns the registry. |
| a second link syntax | `@path` / `[[slug]]` / `tags:` | The substrate owns linking; `/xref` reconciles it. |
| a topic-opening skill | `/research new` | Duplicating it is the v0.1.0 mistake. |
| *archive* (as an action) | `status:` transition | The substrate's lifecycle already has it. |

## Inherited substrate vocabulary

RasaOS-level terms (Element, `rasa.json`, Connection Contract, install vs
pull, `seed/`) are defined in canon and not redefined here. The forbidden
legacy terms (kit, MANIFEST.json, bootstrap/, foundation.json) are
forbidden in this Element too.
