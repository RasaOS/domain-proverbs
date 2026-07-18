---
name: dossier
description: Render what is currently known about a research topic, or a brief across several — triggered by "/dossier", "what do we know about X", "brief me on X", "show me the topic", "where does X stand", "brief me on everything tagged Y". READ-ONLY — it reads the topic folder and writes nothing, ever. Answers from the README's State of play plus open-questions.md plus contested.md; it never answers a current-state question by dumping log.md. Always reports staleness (last_swept against cadence) before the content, always flags contested claims rather than presenting a false-settled picture, and can include a topic's timeline slice.
---

# /dossier — What do we know about X

Answer "what do we know about X" from a topic's synthesis layer. The
whole point of the overlay is that this question is answerable in a
few short paragraphs no matter how long the topic has been tracked;
this skill is where that claim gets tested.

If answering required reading `log.md`, the method is failing — say
so rather than working around it.

## Behavior contract

- **READ-ONLY. This skill writes nothing, ever.** No file under the
  research root is created, edited, or touched. Not to fix a typo,
  not to advance `last_swept`, not to tidy a malformed section, not
  to add a missing `[[link]]` it noticed. Problems found while
  reading are *reported*; fixing them is `/sweep`'s job. There is no
  write path in this skill and none may be added.
- **Answers from `## State of play`, `open-questions.md`, and
  `contested.md`.** Those three are the current picture.
  `findings.md` is drawn on for specific sourced claims when the
  question calls for one.
- **Never reconstructs current state from `log.md`.** The log records
  what the researcher did, not what is currently believed. Reading it
  to answer a current-state question is the exact failure mode the
  mutable/immutable split exists to prevent, and doing it here hides
  the fact that a topic needs a sweep. The log is read only for an
  explicitly historical question — "how did this change", "when did
  we first think X", "what did the last pass do" — and is labelled as
  history when it is.
- **Always surfaces staleness, up front.** `last_swept` measured
  against `cadence` decides how much the picture is worth, and the
  reader is told before they read it. A reader not told the picture
  is nine months past its cadence has been misled by omission.
- **Never presents a contested claim as settled.** Anything in
  `contested.md` is rendered as an open disagreement, with both sides
  and both source ids. Picking the more convenient side for a cleaner
  brief is the single most damaging thing this skill could do.
- **Reports gaps as gaps.** An empty `## State of play` is reported
  as empty, never filled in from background knowledge. A topic that
  has never had a pass is described as one.
- **Cites locations.** Every claim names the file it came from, so
  the user can jump to it.

## Process

1. **Resolve the selection.** One topic slug or title; or a tag; or
   a `related:` neighbourhood ("X and everything it relates to"); or
   a frontmatter filter (all `status: active`, all overdue). Read
   `research/INDEX.md` for the roster. Ambiguous title matches are
   listed for the user to pick from, never guessed. For anything
   beyond one hop of graph traversal — back-references, tag-match
   discovery, the full map — **defer to `/xref`**; do not
   reimplement it here.
2. **Read the topic `README.md` frontmatter first.** `status`,
   `tags`, `related`, `created`, `updated`, `cadence`, `last_swept`.
   Compute staleness: `last_swept + cadence` against today.
   `cadence: none` and any status other than `active` are never
   stale. Overdue depth is `today - (last_swept + cadence)`.
3. **Read `## State of play`.** This is the answer to "what do we
   know". Render it as-is or condensed to the user's altitude —
   never embellished, never extended with material not in the file.
4. **Read `open-questions.md`.** What is not known is part of the
   current state, not an appendix to it.
5. **Read `contested.md`.** Everything in it is rendered as an open
   disagreement with both sides and their `src-NNNN` ids.
6. **Pull from `findings.md` only as needed** — when the question is
   specific enough that a sourced claim answers it. Cite the source
   with the claim; never restate a finding without its ref.
7. **Add the timeline slice when asked, or when the question is
   historical.** Every entry in `research/timeline/` whose `topics:`
   names this topic, in filename order (see
   `framework/timeline-axis.md`). This is a query run now, not a
   cached list read out of the topic; if the topic carries a pointer
   list that disagrees with the entries, the entries win and the
   disagreement is reported.
8. **Assemble the brief** per the output shape below.
9. **Report structural problems, don't fix them.** Missing
   frontmatter, an absent section, a claim in `findings.md` with no
   evidence, a `related:` entry with no `[[link]]` — name them and
   point at `/sweep` (or `/xref` for graph health).

## Output shape

Single topic:

```
<Title>  ·  <status> · tags: <…>
Swept <date> (<n>d ago, cadence <cadence>) — <current | overdue by Nd>

STATE OF PLAY
<the current picture>

OPEN QUESTIONS
- <…>

CONTESTED
- <claim> — side A [src-…] vs side B [src-…]

TIMELINE  (if requested)
- <date> — <title>  [entry id]

RELATED  [[slug]] …
```

Order is deliberate: status and staleness before content, so the
reader knows how much weight the picture carries before reading it.
Contested is never below the fold.

## Multi-topic briefs

For a tag, a `related:` neighbourhood, or a status filter: one short
block per topic — title, status, staleness, and the state of play
condensed to a line or two — then, across the whole selection, the
contested claims and the open questions.

The cost is one short block per topic and it does not grow with how
long any topic has been tracked. If a multi-topic brief is
unreadable, the individual `## State of play` sections have crept and
the fix is structural — split topics, tighten the rewrite discipline
— not a shorter rendering here. Say so when it happens.

## What NOT to do

- **Don't write.** Anything. Including "harmless" fixes.
- **Don't reconstruct current state from `log.md`.** If the state of
  play is thin, report that it is thin. Reading five years of log to
  synthesise a picture is the precise failure this model exists to
  prevent.
- **Don't resolve a contest in the rendering.** Not by picking a
  side, not by preferring the newer source, not by mentioning only
  one side because the brief is meant to be short.
- **Don't bury staleness** at the end, or omit it because the topic
  is only slightly overdue.
- **Don't fill an empty section from background knowledge.** Empty is
  the reported answer. If the corpus does not say it, the brief does
  not say it.
- **Don't quietly widen the selection.** If the requested tag matches
  nothing, say it matches nothing.
- **Don't reimplement `/xref`.** Back-references, tag-match
  discovery, and the graph map are the substrate's. Read
  `research/INDEX.md` and a topic's own `related:`; for anything
  further, hand off.
- **Don't maintain a rival index.** `research/INDEX.md` is the
  registry; this skill reads it and never writes it.

## Done when

The user has the current picture for the requested topic or
selection, drawn from `## State of play`, `open-questions.md`, and
`contested.md`; staleness is stated ahead of the content; every
contested claim is shown as contested with both sides; every finding
quoted carries its source id; any timeline slice was computed from
`research/timeline/` rather than read from a cache; structural
problems found are reported with a pointer to `/sweep` or `/xref`;
and no file on disk changed.
