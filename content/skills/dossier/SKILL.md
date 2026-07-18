---
name: dossier
description: Render the current state of a tracked subject, or a brief across several — triggered by "/dossier", "what do we know about X", "show me the subject", "brief me on X", "where does X stand", "brief me on everything tagged Y". READ-ONLY — it reads content/subjects/*.md and writes nothing, ever. Answers from Standing plus Open questions plus Contested; it never answers a current-state question by dumping the Log. Always shows confidence, always flags claims sitting in Contested rather than presenting a false-settled picture, and always reports staleness (last_swept against cadence) so the reader knows how much to trust what they are being told. Can render a multi-subject brief over a tag or a link neighbourhood.
---

# /dossier — Read the current state of a subject

Answer "what do we know about X" from the synthesis layer of X's
dossier. The whole point of the Subject model is that this question
is answerable in a few short paragraphs no matter how long the
subject has been tracked; this skill is where that claim gets tested.

If answering required reading the Log, the method is failing — say so
rather than working around it.

## Behavior contract

- **READ-ONLY. This skill writes nothing.** No file under
  `content/subjects/` is created, edited, or touched. Not to fix a
  typo, not to advance `last_swept`, not to tidy a section it thinks
  is malformed. Problems found while reading are reported to the
  user, and fixing them is `/sweep`'s job.
- **Answers from Standing, Open questions, and Contested.** Those
  three sections are the current picture. `## Established` is drawn on
  for specific sourced claims when the question calls for them.
- **Never answers a current-state question by dumping the Log.** The
  Log is history, not state. It is read only when the user asks a
  historical question — "how did this change", "when did we first
  think X", "what did the last pass do" — and then it is read as
  history and labelled as such.
- **Always reports confidence.** The frontmatter `confidence:` value
  is shown with the brief, not buried. `low` is reported plainly and
  without apology.
- **Always surfaces staleness.** `last_swept` measured against
  `cadence` determines whether the brief is current or overdue, and
  by how much. A reader who is not told the picture is nine months
  past its cadence has been misled by omission.
- **Never presents a contested claim as settled.** If it is in
  `## Contested`, it is rendered as contested, with both sides and
  their sources. Picking the more convenient side to give a cleaner
  answer is the single most damaging thing this skill could do.
- **Reports gaps as gaps.** An empty Standing is reported as empty,
  not filled in from background knowledge. A subject that has never
  had a pass is described as one.

## Process

1. **Resolve the selection.** One subject id or title; or a tag; or a
   link neighbourhood ("X and everything it links to"); or a filter
   over frontmatter (all `status: active`, all overdue). Ambiguous
   title matches are listed for the user to pick from — never guessed.
2. **Read frontmatter first.** `status`, `confidence`, `cadence`,
   `last_swept`, `opened`, `type`, `links`, `tags`. Compute staleness:
   days since `last_swept` against `cadence`; `cadence: none` and
   `status: dormant`/`closed` are never stale.
3. **Read `## Standing`.** This is the answer to "what do we know".
   Render it as-is or condensed to the user's altitude — never
   embellished, never extended with material that is not in the file.
4. **Read `## Open questions`.** What is not known is part of the
   current state, not an appendix to it.
5. **Read `## Contested`.** Anything here is rendered as an open
   disagreement with both sides and both source ids.
6. **Pull from `## Established` only as needed** — when the user asked
   something specific enough that a sourced claim answers it. Cite the
   source id with the claim; never restate an Established claim
   without its ref.
7. **Assemble the brief** per the output shape below.
8. **Report structural problems, don't fix them.** Missing required
   frontmatter, absent sections, an unsourced claim sitting in
   Established, a one-directional link — name them and point at
   `/sweep`.

## Output shape

Single subject:

```
<Title>  ·  <type> · <status> · confidence: <c>
Swept <date> (<n>d ago, cadence <cadence>) — <current | overdue by Nd>

STANDING
<the current picture>

OPEN QUESTIONS
- <...>

CONTESTED
- <claim> — side A [src-…] vs side B [src-…]

LINKS  <ids>
```

Order is deliberate: status and staleness before content, so the
reader knows how much weight the picture carries before reading it.
Contested is never below the fold.

## Multi-subject briefs

For a tag, a link neighbourhood, or a status filter: render one short
block per subject — title, status, confidence, staleness, and the
Standing section condensed to a line or two — then, across the whole
selection, list the contested claims and the open questions.

The cost of the brief is one short block per subject, and it does not
grow with how long any subject has been tracked. If a multi-subject
brief is unreadable, the individual Standing sections have crept and
the fix is structural — split subjects, tighten the rewrite
discipline — not a shorter rendering here. Say so when it happens.

## What NOT to do

- **Don't write.** Anything. This skill has no write path.
- **Don't reconstruct current state from the Log.** If Standing is
  thin, report that Standing is thin. Reading five years of Log to
  synthesise a picture is exactly the failure mode the two-layer
  model exists to prevent, and doing it here hides the fact that a
  subject needs a sweep.
- **Don't resolve a contest in the rendering.** Not by picking a side,
  not by picking the newer source, not by mentioning only one side
  because the brief is meant to be short.
- **Don't fill an empty section from general knowledge.** Empty is the
  reported answer.
- **Don't omit confidence or staleness** because they make the brief
  look weak. That information is the brief's calibration.
- **Don't quietly widen the selection.** If the requested tag matches
  nothing, say it matches nothing.

## Done when

The user has the current picture for the requested subject or
selection, drawn from Standing, Open questions and Contested;
confidence and staleness are stated alongside it; every contested
claim is shown as contested with both sides; every Established claim
quoted carries its source id; any structural problems found are
reported with a pointer to `/sweep`; and no file on disk changed.
