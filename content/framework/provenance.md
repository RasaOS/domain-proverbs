# Provenance — the corpus-wide source registry

One of the four things this domain adds on top of `rasa.module.research`.
Read `topic-overlay.md` first; it establishes the division of labour this
chapter operates inside. Read the module's `research-rules.md` too — the
per-topic reference shelf and the confidence marker on a finding are the
substrate's, and nothing here replaces either.

Scope of this chapter: `research/sources/`, the registry of source
records shared by every topic in the corpus, and the bridge between it
and each topic's local `sources.md`.

---

## Why a global registry exists at all

The substrate gives every topic a `sources.md` with local ids — `[S1]`,
`[S2]` — and that is the right shape for a self-contained investigation.
It stops being sufficient the moment the corpus has more than one topic,
for one specific reason:

**The same source routinely bears on several topics, and a topic-local
id cannot express that a claim in topic A and a claim in topic B rest on
the same evidence.**

That is the entire justification. Not tidiness, not deduplication, not a
richer metadata model — the inability to answer one question:

> Two findings, in two topics, both look well supported. Are they
> actually independent, or are they the same document read twice?

Under local ids alone the answer is unrecoverable without reading both
shelves and recognising a title by eye. `topic-alpha [S1]` and
`topic-beta [S3]` are opaque strings that happen to name the same PDF,
and the corpus has no way to know it. The failure is silent and it
compounds: corroboration gets claimed between two topics resting on one
source, confidence rises on both, and nothing in the record shows why
that was wrong.

A corpus-wide id makes the join expressible. Everything else in this
chapter is downstream of that.

## The `src-NNNN` id

One source is one file: `research/sources/src-NNNN.md`.

The id is a zero-padded counter — `src-0001`, `src-0042`, `src-1337` —
**assigned once, never changed, never recycled.** The next id is the
highest existing id plus one. Gaps are fine and expected. Past
`src-9999` the field widens to five digits rather than renumbering
anything.

Recycling is the rule that matters. When a source is discredited,
withdrawn, or turns out to be a duplicate, its record stays and its id
stays retired. Handing `src-0042` to a different artifact silently
rewrites the meaning of every reference that already points at it, in
every topic, with no diff to catch it. Retired ids are cheap;
retroactively corrupted references are not.

### Why numbers and not slugs

Topics get kebab-case slugs; sources get numbers, and the asymmetry is
deliberate. A topic has a name before you have any material about it. A
source usually does not: two pieces by the same author in the same year,
three revisions of one document, a screenshot with no title. Slugging
forces a naming decision at ingest time and produces collisions the
moment the corpus gets real — `report-2019`, `report-2019-b`,
`report-2019-final`. A counter never collides, costs nothing to assign,
and pushes the human-readable identity into `title:`, where it can be
corrected freely without breaking a single reference.

## The bridge — local shelf, global join key

**Both exist. Neither replaces the other.**

A topic's `sources.md` keeps its local `[S1]` shelf exactly as the
substrate defines it, and each entry gains one field pointing at the
global record:

```markdown
## S1 — <title>
- **Type:** paper | url | file | person | dataset | book
- **Global:** src-0012
- **Locator:** <URL, citation, or @path to a committed copy>
- **Accessed:** 2026-07-18
- **Relevance:** <why it's on the shelf>
- **Cited by:** F2, F5
```

That one line is the whole mechanism. Read across two topics it looks
like this:

| Topic | Local id | Global id |
|---|---|---|
| `topic-alpha` | `[S1]` | `src-0012` |
| `topic-alpha` | `[S2]` | `src-0044` |
| `topic-beta` | `[S1]` | `src-0031` |
| `topic-beta` | `[S3]` | `src-0012` |

Two facts fall straight out of the table, and neither is recoverable
without it:

- `topic-alpha [S1]` and `topic-beta [S3]` are **the same evidence**.
  Findings citing them do not corroborate each other.
- `topic-alpha [S1]` and `topic-beta [S1]` are **different sources**
  despite the identical label. Local ids collide across topics by
  design; they are local.

### Findings still cite `[S1]`, never `src-0012`

The obvious move is to have findings cite the global id directly and
delete the local shelf. It is wrong, for two reasons.

**It breaks the design constraint.** `topic-overlay.md` requires that
the overlay never make the substrate unreadable without it. A topic
whose `findings.md` cites `src-0012` is broken the day the deployment
drops this domain — every citation points at a registry that no longer
exists. A topic whose findings cite `[S1]` stays a valid
`module.research` topic forever; drop the domain and it simply loses
the cross-topic join, which is precisely the thing the domain added.

**It redefines a substrate convention for no gain.** The module already
specifies the citation form. Changing it buys nothing a `**Global:**`
field on the shelf doesn't already buy, and costs a second vocabulary
for one structure — the drift `topic-overlay.md` exists to prevent.

The rule, stated once: **local ids are what claims cite; the global id
is what the corpus joins on.** A reader working inside one topic never
needs the registry. A reader asking a corpus-wide question never needs
the local ids.

## The source record

Frontmatter on `research/sources/src-NNNN.md`. Every field except
`tags:` is required; `author:` and `date:` take `unknown` when they
genuinely are.

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
topics: [some-topic]      # topic slugs this source touches
tags: [tag-a]             # free-form, flat, optional
---
```

`date:` and `retrieved:` are distinct and both matter. `date:` places
the source in time relative to what it describes; `retrieved:` places
your reading of it in time relative to a page that may since have
changed. A source dated 2019 and retrieved 2026 is a different
evidential object from one retrieved in 2019.

`added:` answers "when did this enter the corpus" — a question about the
research, not about the source.

`topics:` is the registry-side half of the join. Without it, answering
"what did this document feed?" means grepping every topic's shelf. Keep
it in agreement with the `**Global:**` fields on those topics'
`sources.md` by convention; `/sweep` reconciles the two directions and
reports disagreements rather than silently repairing them.

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
| `self-authored` | Material you wrote: your own notes, your own earlier analysis, a prior output of this corpus. |

`self-authored` earns its place because the alternative is worse.
Without it, your own synthesis either goes uncited or gets laundered
into looking external. Registering it makes the circularity visible: a
run of findings all resting on `self-authored` records is a corpus
talking to itself, and that should be obvious at a glance rather than
discovered later.

### Kind is not reliability

A `primary` source can be a self-serving statement by an interested
party. A `tertiary` source can be a carefully maintained reference that
is right nearly all the time. Distance from the event and
trustworthiness are two axes; collapsing them produces exactly the wrong
ranking on the cases that matter. Both fields are recorded; neither is
derived from the other.

## Reliability — and why it is not confidence

`reliability:` is a property of **the source**, set once when the record
is created and revised only with a reason.

| Value | Meaning |
|---|---|
| `high` | Track record, accountability, or direct access. You would defend a claim on this source alone. |
| `medium` | Generally sound, with a known limitation: an interest in the outcome, no editorial process, second-hand access, or no track record yet. |
| `low` | Weak provenance, known errors, anonymous, heavily interested, or reconstructed after the fact. Usable, but never alone. |
| `unknown` | Not yet assessed. Honest, and normal for freshly ingested material. Do not default to `medium` to avoid saying `unknown`. |

The rating carries no weight without its reason. Every record states the
basis in `## Assessment`, in one or two lines. A bare rating is a number
somebody made up, and six months later nobody — including you — can tell
whether it was a judgement or a reflex.

**This is the domain's actual contribution to the evidence model,** so
it gets stated flatly. The substrate already carries a per-finding
`**Confidence:**` marker in `findings.md`. This domain does not touch
it, extend it, or shadow it. It adds a second, orthogonal property that
attaches to a different object:

| | Attaches to | Set by | Answers |
|---|---|---|---|
| **Confidence** | one finding in one topic | the substrate (`findings.md`) | How well does the evidence support *this specific claim*? |
| **Reliability** | one source record | this domain (`research/sources/`) | Do we trust this source, in general? |

The value sets differ on purpose and do not map onto each other. The
substrate's fourth value is `tentative` — a statement about a claim's
standing. Reliability's fourth is `unknown` — a statement about an
assessment you have not done yet. Reading either as a translation of the
other is a mistake.

### The cases where they diverge

Both directions, concretely, because this is where the distinction earns
its keep:

- **High reliability, low confidence.** A source with a long track
  record and direct access mentions the thing once, in passing, in a
  subordinate clause, with no elaboration and no attribution. The source
  stays `high` — nothing about it changed. The support for *that
  particular claim* is a single unelaborated aside, so the finding is
  `**Confidence:** low`. Nothing is wrong here; the source is simply not
  addressing the claim squarely.

- **Low reliability, high confidence.** Three sources rated `low` —
  weak provenance, no editorial process, each individually not worth
  leaning on — independently document the same thing in detail. None
  drew from the others. Nothing contradicts them. Each record stays
  `low`; their ratings do not improve by being agreed with. The finding
  can honestly sit at `**Confidence:** high`, and `## Assessment` on
  each record states why the three are independent.

The operating rule: **reliability sets a soft ceiling on a single
source, not a floor, and corroboration is what lifts the ceiling.** One
`low` source cannot carry a `high` finding no matter how detailed it is.
One `high` source does not automatically lift every claim drawn from it
— only the ones it actually addresses squarely.

### What does not count as corroboration

The load-bearing word above is *independent*. Three outlets reprinting
one wire story are one source wearing three hats. A paper and the press
release written from it are one source. A document and your own earlier
summary of it are one source — which is why `self-authored` is in the
taxonomy.

Before raising a finding's confidence on corroboration, state in
`## Assessment` why the sources are actually independent. If you can't
state it, they aren't, and the global registry is what lets you check:
two topics citing the same `src-NNNN` never corroborate each other.

## Link rot

URLs die. Domains lapse, pages get rewritten in place, archives go
behind logins. Anything that depends on a live URL is a claim with a
timer on it.

Two rules follow.

1. **`retrieved:` is mandatory for any source with a URL.** An undated
   URL is not a citation — a page edited since you read it can no longer
   confirm or deny what you took from it.

2. **A record must capture enough excerpt to reconstruct every claim
   drawn from it.** Not a summary, not a paraphrase — quoted text, in
   `## Key excerpts`, sufficient that the claim still stands if the page
   is gone.

**The vanished-page test**, applied at ingest time, before the record is
considered finished:

> If this page vanished tonight, could I still defend tomorrow every
> claim I drew from it?

If no, the record is incomplete and the ingest isn't done. This is the
cheapest possible discipline at ingest and an impossible one to
retrofit, which is why it is a rule rather than a suggestion — by the
time you discover the page is gone, the excerpt can no longer be taken.

An archive URL in `locator:` alongside the original is good practice and
does not replace the excerpt. Archives fail too.

The registry is where this lives rather than the per-topic shelf for the
same reason as everything else here: one capture serves every topic that
cites the source. Excerpting the same page separately in three topics is
three chances to capture too little.

## Redistribution: what may live in the corpus

Two categories, one line between them.

**First-party and `self-authored` material IS redistributable.** If you
wrote it, or it was given to you to hold, the artifact itself can be
committed next to its record. This matches the substrate's own rule for
per-topic sources.

**Third-party copyrighted sources are registered by reference and short
excerpt only.** The record holds the citation, the locator, and the
quoted passages needed to support the claims drawn from it — never a
wholesale copy of the work. If you need the full document, keep it
outside the corpus and point `locator:` at where it lives.

The reason isn't only legal caution. A corpus stuffed with full copies
of other people's work cannot be published, shared, or moved without
untangling every file first, and a research corpus that can't move is
one bad laptop away from gone. Excerpt-and-reference keeps it portable
by construction.

---

## What this deliberately does not add

- **No second confidence scale.** `findings.md` owns confidence, with
  the substrate's four values. This chapter defines reliability, which
  attaches to a different object. If you find yourself wanting a
  confidence field on a source record, you want `## Assessment` prose.
- **No rival to `findings.md`.** A source record summarises and excerpts
  a source. It does not state what the corpus believes. The claim lives
  in the topic that made it; the record only supplies what the claim
  rests on.
- **No change to the substrate's citation form.** Findings cite `[S1]`.
  See the bridge section.
- **No confidence derived from reliability.** The formula is tempting
  and the passing-mention case breaks it. Confidence is assessed per
  claim, by hand, against what the source actually says about *that*
  claim.
- **No numeric reliability score.** Four buckets are all the resolution
  the underlying judgement has. A 0–100 score implies a precision nobody
  can defend and invites arithmetic — averaging two sources into a
  number, which is not how evidence works.
- **No per-source decay.** A source does not become less reliable
  because it is old; an old source is frequently the best primary record
  in existence. Staleness is a property of a topic's cadence, not of a
  source's rating.
- **No deletion.** A discredited source gets its `reliability:` lowered,
  the reason recorded in `## Assessment`, and the affected findings
  revisited with dated entries in each topic's `log.md`. The record and
  the references to it stay. Deleting it erases the trail explaining why
  a claim was ever believed, which is the exact history a longitudinal
  corpus exists to keep.
