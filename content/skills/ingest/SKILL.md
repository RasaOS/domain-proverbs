---
name: ingest
description: Take supplied material — a PDF, a link, a transcript, a page of notes, a batch of files — register it as a source, distil it into claims, and file those claims against every research topic they touch. Passive mode: source-first, fanning out to many topic folders. Triggered by "/ingest", "file this source", "add this PDF to the corpus", "process these notes", "ingest this link", "here's a transcript — file it". Reads the source whole before writing, carries the src id into every claim and every log entry, proposes new topics rather than creating them, and writes durable files to the topic folders and research/sources/ — never auto-commits.
---

# /ingest — File supplied material into every topic it touches

Passive mode. The user supplies the material; this skill decides what it
says and where it belongs. One source typically updates several topic
folders — the fan-out is the point, not a side effect. See
`framework/ingestion.md` for the model this enforces, and
`framework/topic-overlay.md` for the structure it writes into.

The two ways this goes wrong are summarising a source into its one
obvious topic, and letting a distillation drift into an assertion the
source never made. Both are guarded against below.

## Behavior contract

- **Read the source fully before writing anything.** No topic file is
  touched until the read completes. Routing requires knowing what the
  whole source covers; writing as you read files early claims against
  the wrong topic set.
- **Register the source first.** The source gets a `src-NNNN` record in
  `research/sources/` before extraction. Provenance is assigned at
  intake, never reconstructed after.
- **Every claim carries provenance.** Nothing lands in `findings.md` or
  `contested.md` without a local `[S#]` and a `**Confidence:**`.
  Nothing lands in a `log.md` without the global `src-NNNN`. The same
  src id in every topic the source touched.
- **Fan out; file in all N.** A claim touching N topics is recorded in
  all N with the same src id. There is no "main" topic, and
  `related:` / `[[slug]]` are association, not storage.
- **Both shelves, per topic.** Every topic that received a claim also
  gets the source's next `[S#]` row on its own `sources.md`, pointing
  at the global `src-NNNN`. The same source carries different local ids
  in different topics; that is correct.
- **Propose new topics; never sprawl.** Entities meeting the threshold
  in `framework/ingestion.md` are proposed to the user as a short list
  with the trigger that fired. **This skill does not create topic
  folders** — opening a topic is the substrate's `/research new`, which
  confirms the slug, assigns the `RT-NNN` id, and registers the
  `INDEX.md` row. Hand off; don't scaffold.
- **Source's terms first, interpretation marked second.** Hedges,
  attribution, and scope are preserved in meaning. Synthesis goes in
  `## State of play` and says it is synthesis; unchecked inference goes
  in `open-questions.md` as a question.
- **Excerpt, don't mirror.** Third-party material is registered by
  reference plus short attributed excerpt where the wording is
  load-bearing. Never bulk-copy a source into the corpus.
- **One source, one record, one log entry each.** Batches are ingested
  in sequence and never merged into a single registry record or a
  single log entry.
- **Conflicts are left standing.** A claim contradicting an existing
  finding moves the pair to `contested.md` with both sources. Never
  resolve a conflict by preferring the newer or longer source, and
  never reach for `Superseded-by:` during ingestion — that field is for
  corrections you can justify on evidence, which is `/investigate`'s
  business, not a routing decision.
- **`last_swept` is not advanced.** Routing a claim in is not a check
  of the topic's picture. Bump `updated:` where the README changed;
  leave the cadence clock alone.
- **Writes durable files; never auto-commits.** Edits to the topic
  folders and `research/sources/` land in the working tree for review
  via `git diff`.

## Process

1. **Take the material.** Identify what was supplied and how many
   distinct sources it is. If any item is unreadable or inaccessible,
   say so and ingest the rest rather than guessing at its contents.
2. **Register each source.** Assign `src-NNNN` in `research/sources/`;
   record what it is, its origin, its date, how it was obtained, and an
   honest reliability note. Per source, including within a batch.
3. **Read it whole.** Note candidate claims while reading; write
   nothing yet. For long sources, hold the candidate list in the
   session, not on disk.
4. **Extract candidates.** One checkable statement per candidate.
   Compound sentences split. Topics discarded — only claims are filed.
   Preserve hedges and attribution as written.
5. **Route.** For each candidate, list the topics it touches, using the
   three-part test in `framework/ingestion.md`. Read the candidate
   topics' `open-questions.md` — a source that answers a standing
   question is the highest-value routing hit.
6. **Propose new topics.** Present the entities that met the threshold,
   with the trigger that fired for each (recurrence, attached open
   question, future lookup, overloading). Wait for the user, then hand
   approved ones to `/research new` — proposed slug, driving question,
   `status: open`, long or absent cadence.
7. **Show the routing plan before editing.** A short table: claim →
   topics → target file. This is the cheapest point to catch a
   misroute; get it wrong here and the corpus carries it for years.
8. **Update each touched topic.** Sourced claims to `findings.md` as
   the next `F#`; conflicts to `contested.md` with both sides;
   unanswered questions to `open-questions.md`; multi-topic dated facts
   to `research/timeline/`. Add `[[slug]]` + `related:` on the topic
   being edited for new relations; let `/xref` compute the reverse.
9. **Rewrite `## State of play` only where the picture moved.** If the
   source added facts without changing the current view, leave it and
   say so. Bump `updated:` where the README changed.
10. **Add the `[S#]` row** to each touched topic's `sources.md`, with a
    one-line "good for" note and the pointer to the global `src-NNNN`.
11. **Append one log entry per touched topic**, each carrying the same
    src id and naming what changed.
12. **Report.** Src ids registered, topics touched, claims filed per
    topic, contests opened, topics proposed and their disposition, and
    anything deliberately not filed. Leave everything uncommitted.

## What NOT to do

- **Don't write before the read finishes.** Not even the "obvious"
  first claim.
- **Don't create topic folders.** Propose, then hand to
  `/research new`. Scaffolding directly bypasses slug confirmation and
  the `INDEX.md` registration, and produces the sprawl the threshold
  exists to prevent.
- **Don't open a topic for every named entity.** If no threshold
  trigger fires, name it in prose with a src ref and move on. Err
  toward fewer, larger topics.
- **Don't put a newly proposed topic on a short cadence**, and don't
  open it at `active` — `open` is the honest status for a topic
  existing on one source's say-so.
- **Don't file into one topic and rely on the link layers.** Each topic
  folder is read on its own; a fact that isn't in it isn't known there.
- **Don't invent a "main" topic** to avoid duplication. Duplication
  across topics is the intended cost of the fan-out.
- **Don't cite an `[S#]` you didn't add to that topic's `sources.md`,**
  and don't add a local row without a global `src-NNNN` behind it.
- **Don't drop hedges.** "Some evidence suggests X" never becomes "X".
  Same for collapsing attribution — a source quoting someone else is
  not the source claiming it.
- **Don't aggregate three weak indications into one confident claim.**
  Confidence does not accumulate through paraphrase.
- **Don't set confidence by plausibility.** It describes what this
  source supports, not how likely the claim feels. A forceful claim
  from a weak source is `low`.
- **Don't resolve a contest during ingestion,** and don't set
  `Superseded-by:` on a finding this source merely disagrees with.
  Record both sides and leave it.
- **Don't bulk-copy copyrighted text** into a topic folder or any file
  under `content/`, in one pass or accumulated across several.
- **Don't merge a batch** into one registry record or one log entry.
- **Don't rewrite or reorder any `log.md`.** It is append-only.
- **Don't advance `last_swept`, and don't auto-commit.**

## Done when

Every supplied source has its own `research/sources/` record with its
own id. Every claim extracted from them sits in the right file of every
topic it touches, with a local `[S#]` and a confidence value. Every
touched topic has the source's row on its `sources.md` shelf pointing
at the global id, and one new append-only `log.md` entry carrying that
same src id. New topics, if any, were proposed with their triggers and
opened through `/research new` at `status: open` — never scaffolded
here. No third-party text was bulk-copied, no cadence clock was
advanced. Everything is in the working tree, uncommitted, and the user
has a report naming the topics touched and anything deliberately left
unfiled.
