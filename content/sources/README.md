# `content/sources/` — the source registry

Every source the corpus cites lives here as one file. Nothing else
does.

**The authority for this folder is
[`../framework/provenance.md`](../framework/provenance.md).** This
README is operational — what the folder holds and how to add to it. The
rules, the reasoning, and the field definitions are in that chapter,
and it wins on any disagreement.

---

## What's in here

| File | What it is |
|---|---|
| `README.md` | This file. |
| `_TEMPLATE.md` | The per-source record template. Copy it; don't edit it in place. |
| `src-NNNN.md` | One source record. Everything else in this folder. |

The underscore on `_TEMPLATE.md` keeps it sorted above the records and
makes it obvious it isn't one. Same convention as
`content/subjects/`.

This Element ships the registry **empty** — template and README only.
Sources are corpus content, and the domain is subject-agnostic; see
`PHILOSOPHY.md`.

## How the registry works

- One source, one file, one id: `src-NNNN`.
- The id is **assigned once, never changed, never recycled** — not even
  when a source is discredited, withdrawn, or found to be a duplicate.
  Dossiers cite ids; reusing one silently rewrites every citation that
  points at it.
- The next id is the highest existing one plus one. Gaps are fine.
- Dossiers cite inline as `` `[src-0012]` ``, or
  `` `[src-0007, src-0019]` `` for several.

## Adding a source

1. **Find the next id.** Highest `src-NNNN.md` in this folder, plus
   one. Do not fill gaps.
2. **Copy the template** to `src-NNNN.md`. Set `id:` to match the
   filename — they must never disagree.
3. **Fill the frontmatter.** Everything except `tags:` is required.
   `author:` and `date:` take `unknown` when they genuinely are;
   `reliability:` takes `unknown` when you haven't assessed it yet.
   Don't reach for `medium` to avoid admitting `unknown`.
4. **Capture excerpts before anything else** if the source is a web
   page. Quoted text, enough to reconstruct every claim you intend to
   draw from it. The test: *if this page vanished tonight, could I
   still defend tomorrow every claim I took from it?* This is cheap now
   and impossible to retrofit.
5. **Write `## Assessment`** — the one or two lines justifying the
   reliability rating. An unjustified rating is a number somebody made
   up.
6. **Route it.** List every subject it touches in `subjects:` and in
   `## Subjects touched`. Then add the id to each of those subjects'
   `sources:` frontmatter and `## Sources` section, with a one-line
   note on what it was good for. One source usually touches several
   subjects — that routing is the whole of passive mode.
7. **Log it in the subjects, not here.** A source record has no Log.
   The claims it moved are recorded in the Log of each subject it
   moved them in.

## Redistribution

First-party and `self-authored` material may be committed here
alongside its record. Third-party copyrighted work is registered **by
reference and excerpt only** — never a wholesale copy in the corpus.
Full text you need to keep lives outside the corpus, with `locator:`
pointing at it. Reasoning in `provenance.md`.

## What doesn't go in this folder

- **Claims.** Claims live in subjects, with a citation pointing back
  here. A source record says what the source is and what it says; it
  does not say what the corpus believes.
- **Subject narrative.** `## Subjects touched` is a routing list with
  one-line notes, not a place to write up findings.
- **A Log.** Sources are static artifacts. The record can be corrected
  — a reliability downgrade, a better excerpt — but there is no
  append-only history here. Longitudinal history belongs to subjects.
