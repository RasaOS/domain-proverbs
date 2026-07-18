<!-- Copy to content/timeline/<sort-key>-<slug>.md — see README.md for the
     zero-padded sort-key convention. One dated fact per file. If it has
     open questions, it is a subject, not a timeline entry. -->

---
id: TODO-yyyy-mm-dd-slug   # filename stem, exactly; never changes
date: TODO                 # truncated ISO: 1916-07-01 | 1916-07 | 1916
date_precision: TODO       # day | month | year | circa
title: TODO                # one line, human-facing
subjects: [TODO]           # subject ids this fact relates; no primary, no order
sources: [TODO]            # source ids from the registry; at least one
confidence: TODO           # high | medium | low
---

# TODO Title

## What happened

TODO the fact, in two or three sentences. Dated, concrete, and closed —
what is known to have occurred, not what it might mean. If this is a
span, state the end date here; if `date_precision` is `circa`, state
what bounds the estimate and how loosely.

Resist writing more than a short paragraph. An entry that needs length
is either two entries or a subject.

## Why it matters

TODO one or two sentences: which of the listed subjects this bears on,
and how. This is the only interpretive section — keep it to the bearing
on those subjects, and leave the wider synthesis to their Standing
sections, where it can be rewritten as the picture moves.

Delete this section if the fact is self-evidently relevant. An empty
"why it matters" is worse than none.

## Provenance

TODO one line per source: what it supports and how directly.

- `[src-TODO]` — TODO what this source establishes; primary or
  secondary; any known limitation.

TODO if sources disagree on the date or the fact, say so here and pick
the entry's `date:` deliberately, with the reason. Do not average
conflicting dates. If the disagreement is substantive rather than
incidental, it belongs in the `## Contested` section of the subjects
involved, and this line points at it.

TODO record corrections here, dated, when a source is later revised —
and write the matching Log line in each subject this entry names.
