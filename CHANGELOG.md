# Changelog — `rasa.domain.proverbs`

All notable changes to this Element. Format follows the RasaOS
per-Element convention; this file is the authoritative history and is
rolled up into the workspace's aggregated elements changelog (track #2).

---

## v0.5.0 — 2026-10-01 — NATAL REPORT FORMALIZED

Additive. v0.4.0 moved the `natal-report` skill in as prose: a sixteen-section
list, a design paragraph, a verification checklist, and three scripts with one
real person's birth data hardcoded in two of them. The actual house format lived
only in a lost HTML file — `print.css` referenced a class vocabulary defined
nowhere in the repo. v0.5.0 turns the report into a contract with teeth,
reconstructing the house format from the one shipped PDF (26 pages, 2026-08-23).

- `content/skills/natal-report/REPORT-SPEC.md` — **the contract.** Inputs
  (`birth.json`), the computed source (`chart.json`, schema `natal-report/chart.v1`),
  the pipeline and its machine/writer ownership line, the sixteen sections with
  `data-sec` ids, eyebrows, components and word budgets, the component class
  vocabulary, the design tokens, writing rules W-1…W-15, conformance rules
  R1…R17 and the human pass V-1…V-5, the footer, the PDF, and change control.
  Where SKILL.md and the spec disagree, the spec wins.
- `templates/report.html` — the house template: full stylesheet (both themes, all
  tokens), every section scaffolded with `{{UPPER_CASE}}` machine tokens,
  `{{WRITE: guidance}}` writer slots carrying the budget, and `<!-- @if has_time -->`
  / `@if masters` conditionals. Verified against the shipped PDF by rendering.
- `templates/birth.example.json` — the input shape, fictional subject.
- `scripts/chart.py` — **rewritten.** Takes `birth.json`, writes `chart.json` and the
  writer's summary. No hardcoded subject. Handles no-birth-time (noon UT, no
  angles/houses/sect, flagged). Adds what the house format already used but the
  engine never computed: Vedic psychic/destiny/name planets, the Lo Shu grid, the
  Kabbalistic path's letter/card/attribution, pinnacle age ranges with the current
  one marked, personal years with the current one marked, stellia, Neptune/Pluto
  squares, progressed Moon, and the `wheel` block. Figures regression-checked
  against the v0.4.0 output: identical.
- `scripts/build.py` — new. Fills the machine-owned tokens from `chart.json`,
  resolves the conditionals, refuses to overwrite a draft without `--force`;
  `--pdf` wraps with `print.css`, forces the light theme, prints with headless
  Chrome, and refuses an unfilled report.
- `scripts/check-report.py` — new. The conformance gate: unfilled slots, title,
  section order and conditionals, Portrait budget, banned phrases, leaked
  arithmetic/method, exclamation marks/emoji, gendering, stray exact figures,
  footer, theme tokens, wheel data, machine numbers untouched, kindred years,
  second person. Exit 0 required before publishing; the human pass still follows.
- `scripts/wheel.js` — data-driven from `window.NATAL_WHEEL`; no-time charts draw
  without axes; mattes to `--ground` itself.
- `scripts/print.css` — class list aligned to the template; table rows break
  individually with the head repeated; dead classes from the lost draft removed.
- Two print defects found and fixed while verifying: sign glyphs printed as colour
  emoji (U+FE0E text-presentation selector now appended); the section-head hairline
  collapsed under flex in print (grid now).
- `SKILL.md` — rewritten to carry judgment and process and defer the contract to
  the spec; process is now the six-step pipeline with the gate in it.
- `rasa.json` — version, skills note. `content/README.md` — skills table.
- `bin/check-manifest` + `bin/check-shape` GREEN. `contract_version` unchanged (1.3.0).
- Still ships zero reports and zero real birth data.

## v0.4.0 — 2026-10-01 — NATAL REPORT SKILL

Additive. Moves the `natal-report` skill in from the user-level
`~/.claude/skills/natal-report/` (where it was unversioned and single-host)
so it is versioned, synced and installed with the element. It is subject
content, unlike the other four skills, and does not operate on research topics.

- `content/skills/natal-report/SKILL.md` — the house format (16 sections, design tokens,
  verification checklist). Added the Behavior contract / Process / What NOT to do /
  Done when sections `bin/check-shape` requires; the body is otherwise unchanged.
- `content/skills/natal-report/scripts/` — `chart.py` (Swiss Ephemeris, needs
  `pip3 install pyswisseph`), `wheel.js`, `print.css`. Includes the 2026-08-23
  pinnacle-age fix (`36 − Life Path`, master Life Path reduced first).
- `rasa.json` — capability `proverbs.natal-report`; skills note updated.
- `content/README.md` — skills table.
- No example reports shipped: they are private gifts about real people.

## v0.3.0 — 2026-07-20 — SOURCE DISCOVERY DATE

Additive, subject-neutral. One optional frontmatter field on the source
record — `surfaced:` — closing a real gap in provenance: a source's
**creation** and its **discovery / re-surfacing** are often separated by a
long, meaningful span, and the record had a home only for the first
(`date:`) and for our own access (`retrieved:` / `added:`). A clay tablet
created c. 2000 BCE, excavated in 1902, and read by us in 2026 is three
distinct facts; `surfaced:` records the middle one. Optional — omitted when
creation and availability coincide (a same-week web page). It splits along
the domain's existing seam: `date:` and `surfaced:` are facts about the
world (historical); `retrieved:` / `added:` are facts about the research.

- `content/overlay-template/source-record.md` — the `surfaced:` field, marked optional.
- `content/framework/provenance.md` — new "The three dates of a source" section;
  the required-fields sentence updated (`surfaced:` joins `tags:` as optional).
- `bin/check-manifest` + `bin/check-shape` GREEN. `contract_version` unchanged (1.3.0).
- No new file, no manifest slot; existing overlay-template is directory-mirrored.

## v0.2.0 — 2026-07-18 — THE OVERLAY REFACTOR

**Breaking in effect, though the version is a minor bump (pre-1.0).**
v0.1.0's entire data model is deleted and replaced by a dependency.

### Why

v0.1.0 defined its own research structure — `subjects/<id>.md` with
`## Standing`, `## Established`, `## Open questions`, `## Contested`,
`## Timeline`, `## Sources`, `## Log`. **Every part of that except
`## Contested` already existed in `rasa.module.research` under a
different name**, and the module was already shipped, public, and at
v0.1.3.

The overlap was found **after the v0.1.0 ship**, while registering the
Element — `elements/REGISTRY.md` was on disk the whole time and was not
checked for prior art before scaffolding. Recording the miss here
because a corrected model with a quietly rewritten history teaches
nothing.

The mapping that made the duplication obvious:

| v0.1.0 (deleted) | `rasa.module.research` (already existed) |
|---|---|
| `subjects/<id>.md` | `research/<topic-slug>/` |
| `## Standing` | `README.md` → `## State of play` |
| `## Established` | `findings.md` (with `**Confidence:**` — already) |
| `## Open questions` | `open-questions.md` |
| `## Log` | `log.md` |
| `## Sources` | `sources.md` (local `[S1]`) |
| `status:` lifecycle | `open→active⇄dormant→concluded→archived` |
| "no claim without evidence" | already in the module's `research-rules.md` |

### What changed

- **`requires.elements[]` now declares `rasa.module.research >=0.1.3`.**
  This domain is a layer; it no longer defines a research structure.
- **Deleted:** `content/subjects/`, `content/timeline/`,
  `content/sources/` (the parallel structure),
  `content/framework/subject-model.md`,
  `content/framework/cross-linking.md` (the module owns linking — three
  layers plus `/xref` — and this domain adds no link syntax), and the
  **`/track` skill** (opening a topic is the module's `/research new`).
- **Vocabulary realigned to the substrate's, wholesale.** There is no
  `Subject`, no `Standing`, no `Established` anywhere in this Element.
  `content/vocabulary.md` now carries an explicit INHERITED table that
  points at the module's definitions instead of restating them.
- **COLLISION FIXED:** `content/rules/research-rules.md` →
  `content/rules/proverbs-rules.md`. v0.1.0 installed
  `.claude/research-rules.md` — **the same path the module installs its
  own rules to** — and would have silently overwritten it. This was a
  real defect in the shipped v0.1.0, not a stylistic rename.

### What this domain now adds — and only this

1. **`contested.md`** — a per-topic file for claims where sources
   genuinely disagree, both sides held with their provenance,
   indefinitely. The module's `Superseded-by:` is the right primitive for
   *corrected* claims and the wrong one for *unresolved* ones, because it
   forces a winner when you have least warrant to pick one. That line is
   drawn sharply in `framework/investigation.md`.
2. **`cadence:` + `last_swept:`** on the topic frontmatter — the revisit
   clock. The module has a lifecycle but nothing dated. Due is computed
   on read (`last_swept + cadence < today`), never stored. **A sweep
   advances `last_swept` and writes a `log.md` line even on no-change** —
   otherwise "checked, still true" and "nobody has looked at this in two
   years" are the same state on disk.
3. **`research/sources/`** — a corpus-wide `src-NNNN` registry with
   reliability ratings and captured excerpts. Coexists with each topic's
   local `[S1]` shelf, which gains the global id as a **join key** —
   because the same source bears on several topics and a local id cannot
   express that two claims rest on the same evidence. **Reliability is a
   property of the source, distinct from the module's per-finding
   confidence**; both directions of divergence are worked in
   `framework/provenance.md`.
4. **`research/timeline/`** — the dated axis. A timeline entry is a fact
   relating N topics and owned by none; `log.md` records what the
   *researcher* did, not what *happened*.

### The governing constraint

**The overlay must never make the substrate unreadable without it.** A
topic carrying this domain's fields is still a valid `module.research`
topic; drop this domain and every topic survives intact, only sweeping
stops. Codified as rule P-16 in `proverbs-rules.md`.

### Content

- `content/framework/` — `topic-overlay.md` (**new spine**),
  `provenance.md`, `investigation.md`, `ingestion.md`, `longitudinal.md`
  (all rewritten onto topic folders), `timeline-axis.md` (new, replaces
  `cross-linking.md`).
- `content/overlay-template/` — **new**: `contested.md`,
  `source-record.md`, `timeline-entry.md`. Installs to
  `.claude/proverbs-overlay-template/`, mirroring the module's own
  `.claude/research-topic-template/` convention.
- `content/skills/` — `investigate`, `ingest`, `sweep`, `dossier` all
  rewritten to operate on `research/<topic-slug>/`. All four act on
  topics that already exist.
- `content/rules/proverbs-rules.md` — 18 numbered gates (P-1…P-18) in
  five groups, each with its rationale.
- `PHILOSOPHY.md`, `vocabulary.md`, `content/README.md`, root
  `README.md`, `CLAUDE.md` all rewritten for the layer framing.
- `scaffold.directories` now creates `research/sources` +
  `research/timeline`. **No research-root files are seeded** —
  `research/INDEX.md` and `.claude/research-canon.md` are the module's to
  seed, and duplicating them would race its install.

### Gates

`bin/check-manifest` and `bin/check-shape` both exit 0 on a staged tree.

### Migration from v0.1.0

No deployments existed at v0.1.0 (shipped and superseded the same day),
so no migration path is provided. Anyone who did install it: the
`subjects/<id>.md` files map onto topic folders by the table above, and
`.claude/research-rules.md` should be restored from
`rasa.module.research`.

### Still open

- **`rasa.module.research` has no `requires` back-edge** and needs none —
  the dependency is one-way by design. But the module is free to evolve
  its topic template; if it does, `topic-overlay.md`'s frontmatter
  contract and the `requires` floor both need review. Watch it.
- The overlay has **never been exercised against a real corpus**. The
  falsifiable claim in `PHILOSOPHY.md` is the honest test.

---

## v0.1.0 — 2026-07-18 — INITIAL (superseded same day by v0.2.0)

First release. Forked from `rasa.domain.core` v1.3.0. Hybrid shape.
Shipped a self-contained research method: one generic Subject node type
(`subjects/<id>.md`), a seven-section dossier built on a rewritten
`## Standing` / append-only `## Log` split, enforced provenance with
confidence markers, first-class `## Contested`, cadence-driven
longitudinal sweeps with no-change recording, a timeline axis, and five
skills (`track`, `investigate`, `ingest`, `sweep`, `dossier`).

Both gates green; commit `caf987b`, tag `v0.1.0`, pushed PUBLIC.

**Superseded by v0.2.0 the same day.** The structural half duplicated
`rasa.module.research`, and its `content/rules/research-rules.md`
collided with that module's install path. The design thinking survived —
the four genuinely additive ideas (contested, cadence, corpus-wide
provenance, timeline) are what v0.2.0 keeps. The parallel structure did
not.
