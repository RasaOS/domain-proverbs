# `content/timeline/` — the dated-fact axis

Dated facts that relate subjects. One fact, one file. This directory is
a cross-cutting axis over `content/subjects/`, not a subdirectory of it.

Read `../framework/cross-linking.md` for why the axis exists and how it
differs from a `type: event` subject. This file covers the mechanics.

The Element ships this directory empty except for `_TEMPLATE.md` and
this README. No subject matter ships with the domain.

---

## What belongs here

A timeline entry is **a dated fact that relates subjects.** It is
settled as of writing and does not accumulate. It has no Standing, no
open questions, no cadence, and is not swept for staleness.

What does *not* belong here: anything with open questions. That is a
subject — open it under `content/subjects/`, with `type: event` if that
is what it is, and let it reference the entries. The two coexist; see
`../framework/cross-linking.md`.

An entry that starts growing open questions is telling you it should
have been a subject. Promote it: open the subject, move the questions
there, and leave the entry as the dated fact it always was. Do not grow
the entry.

## File naming

```
<sort-key>-<kebab-slug>.md
```

The sort key is the entry's date, **zero-padded to full `YYYY-MM-DD`
width regardless of precision**:

| Precision known | Sort key | Example filename |
|---|---|---|
| Day | `1916-07-01` | `1916-07-01-somme-offensive-begins.md` |
| Month | `1916-07-00` | `1916-07-00-first-tank-deliveries.md` |
| Year | `1916-00-00` | `1916-00-00-shell-output-doubles.md` |

`00` is not a valid month or day, which is the point: it reads as
unknown at a glance and it sorts. Padding is not cosmetic — it is what
makes `ls` chronological, and a chronological listing is the only index
this axis has. An unpadded `1916-shell-output.md` sorts *after* every
month-precise entry in 1916, which is wrong and would be wrong silently.

The slug is kebab-case, descriptive, and stable. **The `id:` in
frontmatter is the filename stem**, exactly. Renaming a file means
renaming the id, which means fixing inbound references — so name it once
and leave it.

## Dates and uncertainty

Two fields carry the date. They do different jobs.

- **`date:`** — the claim, as truncated ISO 8601. `1916-07-01`,
  `1916-07`, or `1916`. Only the precision actually known is written.
  This differs in form from the padded filename on purpose: the filename
  is a sort key, `date:` is the assertion, and `date: 1916-00-00` would
  be a date no parser should accept.
- **`date_precision:`** — one of `day`, `month`, `year`, `circa`.

`year` and `circa` are not the same and the distinction matters:

- **`year`** — it definitely happened in 1916; the day is unknown. The
  date is *truncated*.
- **`circa`** — it happened around 1916; 1915 or 1917 are live. The date
  is *estimated*.

When precision is `circa`, state the basis for the estimate in `## What
happened` — what bounds it, and how loosely. An unexplained `circa` is
an unsourced claim about a date, which is the same failure as an
unsourced claim about anything else.

**Granularity is per entry.** A year-only entry sitting next to a
day-precise one is normal and needs no apology. Do not manufacture a day
to make the directory look uniform; a fabricated precision is worse than
a visible gap.

**Spans** use the start date as the sort key and state the end in `##
What happened`. There is deliberately no `date_end:` field: it would be
absent on most entries, which makes any query over it quietly
unreliable, and a span that matters enough to query is usually a subject
with its own entries for the start and the end.

## Referencing subjects

```yaml
subjects: [somme-offensive, british-expeditionary-force]
```

Every id must resolve to a file under `content/subjects/`. `/sweep`
reports dangling ids.

Order carries no meaning. There is no "primary" subject — an entry that
touches four subjects belongs equally to all four, which is the reason
the axis is separate in the first place.

**The entry is authoritative.** A subject's `## Timeline` section is a
convenience view of the entries that name it, and when the two disagree,
the entry wins and the section gets fixed. This is a different rule from
`links:` symmetry, where neither side is authoritative because both
sides are the same kind of thing. Here the entry is the single record of
the fact and the section is a cache.

Adding an entry that names a subject is a change to that subject's
picture. Log it there if it moves anything.

## Corrections

Entries are corrected in place, not appended to and not superseded. If a
source turns out to be wrong about a date or a fact, edit the entry,
note the correction in `## Provenance`, and **write a Log line in each
subject the entry names** — the subjects carry the audit trail, because
they are the things whose picture changed.

If the fact turns out not to have happened at all, delete the entry and
record why in the Logs of the subjects that referenced it. This is the
one place the corpus deletes: an entry is a claim about a discrete
event, and a claim that dissolves leaves nothing behind to keep. Closed
*subjects* are still never deleted — the rule differs because a subject
carries a research history and an entry does not.

## Authoring

Copy `_TEMPLATE.md`, fill it, name the file per the convention above.
Do not freehand the frontmatter.
