# The timeline axis

The fourth and last thing this domain adds. Read `topic-overlay.md`
first — this chapter assumes the division of labour it sets out, and
describes only the dated axis that sits beside the topic folders.

---

## Why the substrate needs this

`rasa.module.research` has exactly one dated structure: `log.md`. It
is not enough, and the reason is not that it is thin. **`log.md`
records what the researcher did; it does not record what happened.**

Those are different objects with different time axes. "2026-07-18 —
read the annual report, found the merger date" is a fact about the
investigation, dated by when you looked. "1987-03-02 — the merger was
announced" is a fact about the world, dated by when it occurred. The
first belongs to one topic and is append-only narrative. The second
belongs to no topic in particular and is settled as of writing.

Collapse them and both degrade. Filing world-facts in `log.md` makes
the log's dates mean two incompatible things, so a date range over it
answers neither question. Filing research activity on the timeline
turns the timeline into a second log with worse ergonomics. The axis
exists because the substrate has no home for the second kind of date,
not because `log.md` is deficient at the first.

## An entry is not a topic

A **timeline entry** is a dated fact that relates N topics and is
owned by none of them. It is closed as of writing: no state of play to
rewrite, no open questions, no cadence, no sweep. It does not
accumulate. It is corrected if a source turns out to be wrong, and the
correction is noted in the `log.md` of the topics it touches.

A **topic** is a research target. It has a driving question, open
questions, a cadence clock, and a `## State of play` that is rewritten
as evidence moves. It accumulates for as long as it is tracked.

The test is one question: **does this have open questions?** If yes,
it is a topic. If it is "this happened, on this date, per this
source", it is a timeline entry.

They coexist and reference each other; they are not alternatives.

### Worked example

A long-running topic `research/acme-holdings/` tracks an organization:
`status: active`, `cadence: 90d`, a state of play that is rewritten
each sweep, contested claims about ownership, a live question list.

`research/timeline/1987-03-02-acme-borden-merger-announced.md` is a
timeline entry: the merger was announced on that date, per source
`src-0114`. That fact will never grow. The entry names three topics —
`[[acme-holdings]]`, `[[borden-industrial]]`,
`[[regional-consolidation-1980s]]` — because the announcement bears on
all three and is a fact about none of them exclusively.

Neither is redundant. The topic answers "where does Acme stand and
what don't we know"; the entry answers "what happened, when, and on
whose authority". The topic's `## State of play` may say the merger
was the turning point; the entry is where the date itself lives, once,
so correcting it is a single edit rather than a hunt through three
topics for three drifting copies.

**That is the whole justification for a separate axis:** an event
relates N topics and none of them owns it. Storing the fact inside one
topic is an arbitrary choice the other N−1 have to work around;
storing it in all of them is duplication, and duplicated facts drift —
one copy gets corrected, the others do not, and the corpus quietly
contradicts itself.

## Files and naming

Entries live at `research/timeline/`, one file per entry, named by
date then slug:

```
research/timeline/
├── 1916-00-00-somme-planning-begins.md      year-only
├── 1916-07-00-summer-offensive-opens.md     month-only
├── 1916-07-01-first-day-casualties.md       day
└── 1987-03-02-acme-borden-merger-announced.md
```

**Every component is zero-padded to fixed width: `YYYY-MM-DD-slug`.**
Unknown components are filled with `00`, not omitted. This is a
mechanical requirement, not a stylistic one — the sorted directory
listing *is* the chronological index, and it is only chronological if
every filename has the same shape.

Unpadded names sort wrong, and they do it **silently**. `1916-7-1-x`
sorts *after* `1916-11-x`, because lexical comparison reaches `7` vs
`1` before it knows either is a month. The listing is still sorted;
it is simply not sorted by time, and nothing errors. A year-only entry
written `1916-somme-planning.md` is worse: it has no distinguishable
shape, and any slug beginning with digits (`1916-2nd-wave.md`) parses
as a date component to the eye and to a range filter alike. Padding
costs two characters and removes the entire failure class.

`00` sorts before any real month or day, so a year-only entry sits at
the head of its year and a month-only entry at the head of its month.
That ordering is deliberate: the less precisely dated fact comes
first, where a reader scanning the period will see it before the
precisely dated ones it may contextualize.

The filename minus `.md` is the entry's `id`.

## `date_precision:`

Four values. The field is required, because "1916-00-00" alone cannot
distinguish a fact known to the year from a fact guessed at.

| Value | Meaning |
|---|---|
| `day` | The exact date is known. `YYYY-MM-DD` in full. |
| `month` | Known to the month. Day is `00`. |
| `year` | Known to the year. Month and day are `00`. |
| `circa` | The date is estimated. `date:` holds the best guess. |

**`year` and `circa` are not the same claim, and conflating them is
the error this field exists to prevent.**

`year` is **truncation**. The year is known with exactly the same
warrant a `day` entry has for its day — you simply do not have the
finer grain. "The merger closed sometime in 1987" is a `year` entry.
The stated year is load-bearing: it may be used to order the entry
against other entries, to bound a "before/after" argument, and to
scope a period query, all with full confidence.

`circa` is **estimation**. You are not certain of the year either.
"The partnership formed around 1985, per an undated internal memo" is
`circa`. The stated year is a placeholder for sorting, not an
assertion. It may **not** be used to bound before/after reasoning
without saying that the bound is soft, and an entry adjacent to it in
the listing is not thereby known to be adjacent in time.

Widen precision freely when a better source arrives (`circa` → `year`
→ `month` → `day`); the filename changes with it, which is a rename
and a `log.md` line in the affected topics. Narrowing precision
because a source was discredited is the same operation in reverse and
is equally normal.

## How entries reference topics

With `[[slug]]` wikilinks — the substrate's Layer 2, unchanged.
**This domain adds no link syntax.** An entry's `topics:` frontmatter
list carries `[[slug]]` entries and the body prose uses the same form,
exactly as a topic's `related:` and prose do. Nothing here is new
notation; it is the existing topic graph with dated nodes hanging off
it.

Source citations use the corpus-wide `src-NNNN` ids from
`provenance.md`, again unchanged.

## Delegation — what this chapter does not define

Linking, back-references, and tag matching belong to the substrate:
three layers (`@path`, `[[slug]]`, `tags:`/`related:`), all reconciled
by `/xref` (`research-rules.md`, Capability 2). This chapter defines
the dated axis and nothing else. If you find yourself specifying how
a back-reference is computed, you are rewriting the substrate.

The one consequence worth stating: because entries carry `[[slug]]`,
`/xref` sees them for free. An entry that names a nonexistent topic is
a dangling link — a "create this topic next" signal, handled the way
`/xref` already handles danglers.

## Traversal

Both queries are greps over plain frontmatter and filenames. No index
is built and none is maintained.

**"What happened in period P?"** A filename range filter over
`research/timeline/`. Because names are date-prefixed and zero-padded,
the sorted listing is already chronological — the listing is the
index, which is the entire reason for the naming rule. Narrow by
`topics:` to scope the period to one topic or a set.

**"What is this topic's history?"** Every entry whose `topics:`
contains `[[slug]]`, read in filename order.

**A topic's history is a query over the timeline, not a copy stored in
the topic.** A topic README may carry a short pointer list as a
convenience view; it is a cache, it may lag, and when it disagrees
with the entries the entries win. Prefer not to store it at all —
running the query is cheap and always correct, and a cached list is a
second copy of exactly the facts the axis exists to keep single.

**Co-occurrence** is the axis's contribution to relatedness: entries
whose `topics:` names both A and B connect them through a *sourced,
dated* fact rather than an assertion of relatedness. A co-occurrence
with no corresponding `[[link]]`/`related:` edge is worth surfacing —
the edge is probably missing. Authoring that edge is `/link`'s job,
not this chapter's.

## No `date_end:`

There is deliberately no end-date field. A span is either two entries
or a topic.

Two entries when both ends are datable facts: "1914-07-28 — war
declared" and "1918-11-11 — armistice signed" are separately sourced,
separately correctable, and each lands in the sorted listing at the
point a reader scanning that period needs it. One entry with a
`date_end:` collapses two facts of possibly different precision and
different provenance into one record with one confidence value.

A topic when the span is the research target — when "how long did this
last, and when did it really start" has open questions. That is a
driving question, and driving questions get topic folders.

Mechanically, `date_end:` also introduces a second sort key that the
filename does not carry, so a range filter over the directory listing
silently misses every entry whose span overlaps the period but whose
start does not. The listing would stop being the index. That property
is worth more than the field.

## The entry contract

Frontmatter and body sections are fixed by
`../overlay-template/timeline-entry.md`. Entries get no row in
`research/INDEX.md` — the index is the topic registry, and the sorted
directory is the timeline's own index. Two registries for one axis is
the drift this overlay exists to avoid.
