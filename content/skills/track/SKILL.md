---
name: track
description: Open a NEW subject in the research corpus — triggered by "/track", "start tracking X", "open a subject for X", "add X to the corpus", "we should be following X", "put X on the board". Collects title, type, initial cadence, and why the subject is being opened; assigns a stable kebab-case id after checking it isn't already taken; writes a fresh dossier at content/subjects/<id>.md with all seven sections present and honestly empty, confidence low, and the reason-for-opening as the first Open question and the first Log line. Suggests links to existing related subjects and adds the symmetric back-link. Writes durable files (one new dossier plus back-link edits to linked subjects); never auto-commits.
---

# /track — Open a new subject

Create one Subject file from the subject template and put it into the
corpus. The entire job is a correct, honest skeleton: a stable id,
complete frontmatter, all seven sections, and a first Log line.
Content is not this skill's job — `/investigate` and `/ingest` fill a
subject, `/sweep` maintains it.

A new subject opens empty. That is the correct opening state, not a
gap to be papered over. See `framework/subject-model.md`.

## Behavior contract

- **Writes durable files.** Creates `content/subjects/<id>.md`, and
  edits each subject named in `links:` to add the symmetric back-link.
  Nothing else is touched. **Never auto-commit** — edits land in the
  working tree for review.
- **The id is assigned once and is permanent.** It is checked against
  the whole corpus before use, including closed and superseded
  subjects, and it is never recycled. A closed subject holds its id
  forever.
- **Never fabricates a Standing section.** At open time there is no
  evidence, so `## Standing` is empty and `confidence: low`. Writing
  a plausible opening paragraph from background knowledge is the
  failure this skill exists to refuse — once it is in Standing it is
  indistinguishable from researched material.
- **The reason for opening is recorded twice**: as the first entry
  under `## Open questions`, and as the first `## Log` line. Those are
  the only two places a brand-new subject legitimately has content.
- **One subject per invocation.** Bulk-opening produces a corpus of
  skeletons nobody wrote a reason for.
- **Confirms the frontmatter before writing.** Title, type, id,
  status, cadence and links are read back to the user; the file is
  written after agreement.

## Process

1. **Collect four things.** Title (human-facing, may change later);
   `type:` (topic | person | event | org | place | work | thread);
   initial `cadence:` (7d | 30d | 90d | 365d | none); and why the
   subject is being opened, in the user's own words. Ask for whatever
   is missing rather than inferring it. If the "why" cannot be stated,
   stop — a subject nobody can say why they opened will not survive a
   sweep.
2. **Derive the id.** Kebab-case slug from the title, trimmed to
   something durable — drop honorifics, articles, and anything likely
   to change (job titles, "2026", "new", "proposed").
3. **Check the id isn't taken.** Scan `content/subjects/` for a
   matching filename, a matching `id:` in frontmatter, and any
   `superseded_by:` pointing at it. A hit means pick a different
   slug — never reuse, never suffix an existing id with a number to
   force it through. If the collision is because the subject already
   exists, say so and stop; the user probably wants `/dossier` or
   `/investigate`, not a second file.
4. **Choose status.** `speculative` when the subject is opened on a
   hunch that may not survive first contact. `active` when it is
   opened with a concrete question to work. If it is neither — real,
   worth keeping, nobody working it — `dormant` is honest. Say which
   was chosen and why.
5. **Suggest links.** Scan existing subjects for plausible neighbours
   by title, tags, and existing links. Propose them; the user
   confirms. Do not link speculatively to pad the graph.
6. **Write the dossier** from `content/subjects/subject.md.template`.
   All seven sections present in order, empty except as stated below.
   `opened:` and `last_swept:` both set to today.
7. **Add the symmetric back-link.** For each confirmed entry in
   `links:`, add this subject's id to that subject's `links:` and
   append a Log line there recording the link. A one-directional link
   rots — the other subject has no idea it is connected.
8. **Report** the id, the path, the status chosen, and the single open
   question. State plainly that the subject is empty.

## The opening state

What a freshly tracked subject looks like on disk:

```markdown
## Standing
_Empty — opened <date>, no research pass yet._

## Open questions
- <the reason for opening, stated as an answerable question>

## Established
## Contested
## Timeline
## Sources

## Log
- <date> — opened. <why, in one line.> Standing empty; confidence low.
```

`## Established`, `## Contested`, `## Timeline` and `## Sources` are
present and empty. They are not omitted — `/sweep` reports a dossier
with missing sections as broken.

## What NOT to do

- **Don't write a Standing section.** Not a summary, not "initial
  understanding", not a paragraph of what you already happen to know.
  There has been no pass. Standing is empty.
- **Don't populate `## Established` or `## Sources`.** No pass has
  registered a source, so there is nothing to cite, and an unsourced
  claim in Established is a rule violation from the first minute of
  the subject's life.
- **Don't set `confidence:` above `low`.** There is no evidence to be
  confident about.
- **Don't recycle or edit an id.** Not to fix a typo, not because the
  title changed, not because the old subject was closed. If a subject
  genuinely becomes a different subject, close the old one with
  `superseded_by:` and open a new one.
- **Don't invent tags or links to make the subject look connected.**
  An empty `tags:` list is fine.
- **Don't open a duplicate.** Check first.
- **Don't auto-commit.**

## Done when

`content/subjects/<id>.md` exists with a unique, never-before-used id;
frontmatter is complete and valid per `framework/subject-model.md`;
all seven sections are present; `## Standing` is empty and
`confidence: low`; the reason for opening appears as the first Open
question and the first Log line; every linked subject carries the
symmetric back-link and a Log line recording it; and everything is
uncommitted in the working tree.
