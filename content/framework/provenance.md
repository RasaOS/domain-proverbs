# Provenance

The source discipline. Tenet 2 says a claim without provenance is not
a claim; this chapter defines what provenance means mechanically — what
a source record is, how it is identified, how it is cited, and how a
claim's confidence relates to its source's reliability.

Read `subject-model.md` first. Sources exist to be cited from
Subjects; they are not interesting on their own.

---

## The source registry

One source is one file: `content/sources/src-NNNN.md`.

The id is a zero-padded counter — `src-0001`, `src-0042`,
`src-1337` — **assigned once, never changed, never recycled**. The next
id is the highest existing id plus one. Gaps are fine and expected. Past
`src-9999` the field widens to five digits rather than renumbering
anything.

Recycling is the rule that matters. When a source is discredited,
withdrawn, or turns out to be a duplicate, its record stays and its id
stays retired. Handing `src-0042` to a different artifact silently
rewrites the meaning of every citation that already points at it, in
every dossier, with no diff to catch it. Retired ids are cheap;
retroactively corrupted citations are not.

### Why numbers and not slugs

Subjects get kebab-case slugs. Sources get numbers, and the asymmetry
is deliberate. A subject has a name before you have any material about
it. A source usually does not: two pieces by the same author in the
same year, three revisions of one document, a screenshot with no title.
Slugging forces a naming decision at ingest time and produces
collisions the moment the corpus gets real — `report-2019`,
`report-2019-b`, `report-2019-final`. A counter never collides, costs
nothing to assign, and pushes the human-readable identity into
`title:`, where it can be corrected freely without breaking a single
reference.

## The source record

Frontmatter. Every field except `tags:` is required; `author:` and
`date:` take `unknown` when they genuinely are.

```yaml
---
id: src-0001              # stable; assigned once, never recycled
title: Some Document      # human-facing; may be corrected freely
author: Some Author       # person, org, or `unknown`
date: 2019-04-11          # date the SOURCE was created/published
kind: secondary           # see taxonomy below
locator: https://…        # URL, DOI, ISBN, file path, or description
retrieved: 2026-07-18     # date YOU fetched/read it — mandatory for URLs
added: 2026-07-18         # date it entered the registry
reliability: medium       # high | medium | low | unknown
access: public            # public | paywalled | offline | private | restricted
subjects: [some-subject]  # subject ids this source touches
tags: [tag-a]             # free-form, flat, optional
---
```

`date:` and `retrieved:` are distinct and both matter. `date:` places
the source in time relative to the events it describes; `retrieved:`
places your reading of it in time relative to a page that may since
have changed. A source dated 2019 and retrieved 2026 is a different
evidential object from one retrieved in 2019.

`added:` mirrors a subject's `opened:`. It answers "when did this enter
the corpus", which is a question about the research, not about the
source.

`subjects:` exists because passive ingestion is a real mode. One source
routinely updates several subjects, and the routing needs to be
recoverable from the source side — otherwise answering "what did this
document feed" means grepping the whole corpus. Keep it symmetric with
the subject's `sources:` list by convention, the same way `links:` is
symmetric between subjects.

`access:` records what a future reader has to do to see this. It is not
a quality judgement — a private interview and a public web page can be
equally reliable — but it is what tells you whether a claim is
independently checkable by anyone but you.

## `kind:` taxonomy

Six values. `kind` measures **distance from the thing described**, not
quality.

| `kind` | What it is |
|---|---|
| `primary` | The thing itself, or a direct contemporaneous record of it: the original document, the filing, the raw recording, notes by a participant at the time. |
| `secondary` | Analysis or reporting built on primary material: an article, a paper, a biography, a review. |
| `tertiary` | A summary of secondary material: encyclopedia entry, textbook, aggregator, digest. Good for orientation, never load-bearing. |
| `personal-communication` | Interview, email, message, conversation. Real evidence, not independently verifiable by a third party. Always set `access:` accordingly. |
| `dataset` | Structured or machine-readable data. Cite the snapshot or version in `locator:`; a live dataset with no version is not a citable source. |
| `self-authored` | Material you wrote: your own notes, your own earlier analysis, a prior dossier. |

`self-authored` earns its place in the taxonomy because the alternative
is worse. Without it, your own synthesis either goes uncited — which
Tenet 2 forbids — or gets laundered into looking external. Registering
it makes the circularity visible: a chain of Established claims all
resting on `self-authored` sources is a corpus talking to itself, and
that should be obvious at a glance rather than discovered later.

### Kind is not reliability

A `primary` source can be a self-serving statement by an interested
party. A `tertiary` source can be a carefully maintained reference that
is right nearly all the time. Distance from the event and
trustworthiness are two axes, and collapsing them into one produces
exactly the wrong ranking on the cases that matter. Both fields are
recorded; neither is derived from the other.

## Reliability

`reliability:` is a property of **the source**, set once when the
record is created and revised only with a reason.

| Value | Meaning |
|---|---|
| `high` | Track record, accountability, or direct access. You would defend a claim on this source alone. |
| `medium` | Generally sound, with a known limitation: an interest in the outcome, no editorial process, second-hand access, or no track record yet. |
| `low` | Weak provenance, known errors, anonymous, heavily interested, or reconstructed after the fact. Usable, but never alone. |
| `unknown` | Not yet assessed. Honest, and normal for freshly ingested material. Do not default to `medium` to avoid saying `unknown`. |

The rating carries no weight without its reason. Every record states
the basis in `## Assessment`, in one or two lines. A bare rating is a
number somebody made up, and six months later nobody — including you —
can tell whether it was a judgement or a reflex.

### Reliability is not confidence

This is the distinction most likely to be collapsed in practice, so it
gets stated flatly.

| | Attaches to | Answers |
|---|---|---|
| **Reliability** | the source record | Do we trust this source, in general? |
| **Confidence** | one claim in one dossier | How well does the evidence support *this specific statement*? |

They are independent, and the interesting cases are the ones where they
diverge:

- **High reliability, low confidence.** A source you trust completely
  mentions the thing once, in passing, without elaboration or
  attribution. The source is excellent. The support for that particular
  claim is a single unelaborated aside. The claim is `(low)`.
- **Low reliability, medium confidence.** A source you distrust
  documents something in exhaustive first-hand detail that would be
  laborious to fabricate, and nothing contradicts it. The source stays
  `low`. The claim can honestly sit above what the rating alone
  suggests.

The operating rule: **reliability sets a soft ceiling, not a floor.** A
`low` source cannot carry a `high` claim by itself no matter how
detailed it is. A `high` source does not automatically lift every claim
drawn from it — only the ones it actually addresses squarely.

### Corroboration, and what doesn't count as it

Two independent `medium` sources agreeing can support a claim at a
confidence neither reaches alone. The load-bearing word is
*independent*. Three outlets reprinting one wire story are one source
wearing three hats; a paper and the press release it was written from
are one source. Before raising confidence on corroboration, state in
`## Assessment` why the sources are actually independent. If you can't,
they aren't.

## Citation form

Inline, in backticks, in `## Established` and `## Contested`:

```markdown
- The thing happened in 1987. `[src-0012]` (high)
- The two parties met at least twice. `[src-0007, src-0019]` (medium)
```

Multiple ids go in one bracket, comma-separated, ascending. Nothing
else goes inside the brackets — no page numbers, no titles, no URLs. If
a claim rests on a specific passage, that passage belongs in the source
record's `## Key excerpts`, where one copy serves every citation.

Every id cited anywhere in a dossier must exist in the registry and
must appear in that dossier's `## Sources` section with its one-line
note. `/sweep` checks both directions: citations with no record, and
records listed in `## Sources` that nothing cites.

### Why an id and not a link

Writing `[the report](https://…)` in a dossier is the obvious move and
it is wrong. It bakes the URL into every place the source is used, so
link rot has to be repaired N times; it carries no retrieved date, so
the reference is undated; and it gives the reader no way to see what
else the corpus knows about that source. `[src-0012]` points at a
record that owns the URL, the date, the reliability rating, and the
excerpts. One place to update, one place to assess.

## Link rot

URLs die. Domains lapse, pages get rewritten in place, archives go
behind logins. Anything that depends on a live URL is a claim with a
timer on it.

Two rules follow.

1. **`retrieved:` is mandatory for any source with a URL.** An undated
   URL is not a citation — a page that has been edited since you read
   it can no longer confirm or deny what you took from it.

2. **A web source must capture enough excerpt to reconstruct every
   claim cited from it.** Not a summary, not a paraphrase — quoted
   text, in `## Key excerpts`, sufficient that the claim still stands
   if the page is gone.

The test to apply at ingest time: *if this page vanished tonight, could
I still defend tomorrow every claim I drew from it?* If no, the record
is incomplete and the ingest isn't finished. This is the cheapest
possible discipline at ingest and an impossible one to retrofit, which
is exactly why it is a rule rather than a suggestion.

An archive URL in `locator:` alongside the original is good practice
and does not replace the excerpt. Archives fail too.

## Redistribution: what may live in the corpus

Two categories, one line between them.

**First-party and `self-authored` material IS redistributable.** If you
wrote it, or it was given to you to hold, the artifact itself can be
committed next to its record.

**Third-party copyrighted sources are registered by reference and
excerpt only.** The record holds the citation, the locator, and the
quoted passages needed to support the cited claims — never a wholesale
copy of the work. If you need the full document, keep it outside the
corpus and point `locator:` at where it lives.

The reason isn't only legal caution. A corpus stuffed with full copies
of other people's work cannot be published, shared, or moved without
untangling every file first — which breaks the portability claim in
`PHILOSOPHY.md`. Excerpt-and-reference keeps the research portable by
construction.

## Confidence markers

Every bullet in `## Established` carries one, after the citation:
`(high)`, `(medium)`, or `(low)`.

| Marker | Evidential meaning |
|---|---|
| `high` | Multiple independent sources, or one source that states it directly, unambiguously, and with standing to know. You would expect it to survive a hostile check. |
| `medium` | Genuinely supported, with one identifiable gap: a single source, an inference over a short step, or sources whose independence you can't fully establish. |
| `low` | Thin: a passing mention, a longer inference, a source you don't trust much, or a thing you believe for reasons that got weaker when you wrote them down. |

`low` is a normal resting state, not a defect. Per Tenet 5, a dossier
full of honest `low` markers is a better instrument than one where
everything is `medium` because `medium` felt safe.

If a claim cannot honestly reach `low`, it is not Established. It goes
to `## Open questions` as a suspicion, or to `## Standing` as flagged
synthesis. There is no fourth place.

Markers are re-read on every sweep and they move in both directions. A
demotion — `high` to `medium`, or Established to Contested — is a Log
entry, never a silent edit. The Log line is the whole point: it is what
lets a future pass see that the picture moved and why, rather than
finding a claim quietly softened by someone with no memory of doing it.

---

## What this model deliberately does not have

- **No numeric reliability score.** Four buckets are all the resolution
  the underlying judgement actually has. A 0–100 score implies a
  precision nobody can defend, and worse, it invites arithmetic —
  averaging two sources into a number, which is not how evidence works.
- **No confidence derived from reliability.** The formula is tempting
  and the passing-mention case breaks it. Confidence is assessed per
  claim, by hand, against what the source actually says about *that*
  claim.
- **No per-source decay.** A source does not become less reliable
  because it is old; an old source is frequently the best primary
  record in existence. Staleness is a property of a subject's cadence,
  not of a source's rating.
- **No deletion.** A discredited source gets its `reliability:`
  lowered, the reason recorded in `## Assessment`, and the affected
  claims revisited with Log entries. The record and its citations stay.
  Deleting it erases the trail explaining why a claim was ever
  believed, which is the exact history a longitudinal corpus exists to
  keep.
