---
name: ingest
description: Take supplied material — a PDF, a link, a transcript, a page of notes, a batch of files — register it as a source, distil it into claims, and file those claims against every subject in the corpus they touch. Passive mode: source-first, fanning out to many dossiers. Reads the source whole before writing, carries the source id into every claim and every Log line, proposes new subjects rather than creating them silently, and writes durable files to content/subjects/ and the source registry (never commits). Triggered by "/ingest", "file this source", "add this PDF to the corpus", "process these notes", "ingest this link", "here's a transcript — file it".
---

# /ingest — File supplied material into every subject it touches

Passive mode. The user supplies the material; this skill decides what it
says and where it belongs. One source typically updates several
dossiers — the fan-out is the point, not a side effect. See
`framework/ingestion.md` for the model this enforces.

The two ways this goes wrong are summarising a source into its one
obvious dossier and letting a distillation drift into an assertion the
source never made. Both are guarded against below.

## Behavior contract

- **Read the source fully before writing anything.** No file is touched
  until the read completes. Routing requires knowing what the whole
  source covers; writing as you read files early claims against the
  wrong subject set.
- **Register the source first.** The source gets a record and a
  `src-NNNN` id before extraction. Provenance is assigned at intake,
  never reconstructed after.
- **Every claim carries the source id.** Nothing lands in `##
  Established` or `## Contested` without a src ref and a confidence
  marker. Nothing lands in a `## Log` without the src id. Same id in
  every subject the source touched.
- **Fan out; file in all N.** A claim touching N subjects is recorded
  in all N with the same src ref. There is no "main" subject and
  `links:` is not a substitute for filing.
- **Propose new subjects; never sprawl.** Entities that meet the
  threshold in `framework/ingestion.md` are proposed to the user as a
  short list with reasons. Created only on approval, at
  `status: speculative`, with a long or absent cadence.
- **Source's terms first, interpretation marked second.** Hedges,
  attribution, and scope are preserved verbatim in meaning. Synthesis
  goes in `## Standing` and says it is synthesis; unchecked inference
  goes in `## Open questions` as a question.
- **Excerpt, don't mirror.** Third-party material is registered by
  reference plus short attributed excerpt where the wording is
  load-bearing. Never bulk-copy a source into the corpus.
- **One source, one record, one Log line each.** Batches are ingested
  in sequence and never merged into a single registry record or a
  single Log entry.
- **Conflicts are left standing.** A claim contradicting an existing
  Established claim moves the pair to `## Contested` with both sources.
  Never resolve a conflict by preferring the newer or longer source.
- **Writes durable files; never auto-commits.** Edits to
  `content/subjects/*.md` and the source registry land in the working
  tree for review via `git diff`.

## Process

1. **Take the material.** Identify what was supplied and how many
   distinct sources it is. If any item is unreadable or inaccessible,
   say so and ingest the rest rather than guessing at its contents.
2. **Register each source.** Assign `src-NNNN`; record what it is, its
   origin, its date, how it was obtained, and an honest reliability
   note. Do this per source, including within a batch.
3. **Read it whole.** Note candidate claims while reading; write
   nothing yet. For long sources, hold the candidate list in the
   session, not on disk.
4. **Extract candidates.** One checkable statement per candidate.
   Compound sentences split. Topics discarded — only claims are filed.
   Preserve hedges and attribution as written.
5. **Route.** For each candidate, list the subjects it touches, using
   the three-part test in `framework/ingestion.md`. Read the candidate
   subjects' `## Open questions` — a source that answers a standing
   question is the highest-value routing hit.
6. **Propose new subjects.** Present the entities that met the
   threshold, with the trigger that fired for each (recurrence,
   attached open question, future lookup, overloading). Wait for the
   user. Create approved ones at `status: speculative`.
7. **Show the routing plan before editing.** A short table: claim →
   subjects → target section. This is the cheapest point to catch a
   misroute; get it wrong here and the corpus carries it for years.
8. **Update each touched dossier.** Sourced claims to `##
   Established`; conflicts to `## Contested` with both sides; unanswered
   questions to `## Open questions`; dated facts to `## Timeline`; the
   src id plus a one-line "good for" note to `## Sources`. Update
   `sources:` and, for new relations, `links:` on both sides.
9. **Rewrite Standing only where the picture moved.** If the source
   added facts without changing the current view, leave Standing alone
   and say so.
10. **Append one Log line per touched subject**, each carrying the same
    src id and naming what changed.
11. **Report.** Source ids registered, subjects touched, claims filed
    per subject, contests opened, subjects proposed and their
    disposition, and anything deliberately not filed. Leave everything
    uncommitted.

## What NOT to do

- **Don't write before the read finishes.** Not even the "obvious"
  first claim.
- **Don't file into one dossier and rely on `links:`.** Each dossier is
  read on its own; a fact that isn't in it isn't known there.
- **Don't invent a "main" subject** to avoid duplication. Duplication
  across dossiers is the intended cost of the fan-out.
- **Don't drop hedges.** "Some evidence suggests X" never becomes "X".
  Same for collapsing attribution — a source quoting someone else is
  not the source claiming it.
- **Don't aggregate three weak indications into one confident claim.**
  Confidence does not accumulate through paraphrase.
- **Don't set confidence by plausibility.** The marker describes what
  this source supports, not how likely the claim feels. A forceful
  claim from a weak source is `low`.
- **Don't open a dossier for every named entity.** If no threshold
  trigger fires, name it in prose with a src ref and move on.
- **Don't create subjects without asking**, and don't put a new
  speculative subject on a short cadence.
- **Don't resolve a contest during ingestion.** Record both sides and
  leave it.
- **Don't bulk-copy copyrighted text** into a dossier or any file under
  `content/`, in one pass or accumulated across several.
- **Don't merge a batch** into one registry record or one Log entry.
- **Don't rewrite or reorder any `## Log`.** It is append-only.
- **Don't auto-commit.**

## Done when

Every supplied source has a registry record with its own id. Every
claim extracted from them sits in the right section of every subject it
touches, with that src ref and a confidence marker. Every touched
subject has one new append-only Log line carrying the same src id. New
subjects, if any, were proposed, approved, and created at
`status: speculative`. No third-party text was bulk-copied. Everything
is in the working tree, uncommitted, and the user has a report naming
the subjects touched and anything deliberately left unfiled.
