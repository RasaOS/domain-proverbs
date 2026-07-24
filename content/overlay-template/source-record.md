<!-- Copy to research/sources/src-NNNN.md — one record per source.
     The id is the next unused counter, assigned once and never recycled.
     Fill every TODO. See framework/provenance.md for the field contract. -->

---
id: src-NNNN                 # TODO next unused id; never changed, never recycled
title: TODO source title     # human-facing; may be corrected freely
author: TODO                 # person, org, or `unknown`
date: TODO                   # YYYY-MM-DD the SOURCE was created/originated/published, or `unknown`
surfaced: TODO               # OPTIONAL YYYY-MM-DD it was discovered / excavated / declassified / re-surfaced, when that differs from `date:`; omit or `unknown` otherwise
kind: TODO                   # primary | secondary | tertiary | personal-communication | dataset | self-authored
locator: TODO                # URL, DOI, ISBN, @path to a committed copy, or a description
retrieved: TODO              # YYYY-MM-DD you fetched/read it — mandatory for any URL
added: TODO                  # YYYY-MM-DD it entered the registry
reliability: unknown         # high | medium | low | unknown
access: TODO                 # public | paywalled | offline | private | restricted
topics: []                   # topic slugs this source touches — keep in step with ## Topics touched
tags: []                     # free-form, flat, optional
---

# TODO source title

## Summary

TODO two to four lines: what this source is, what it covers, and why it
is in the corpus. Enough that a reader can decide whether to open it
without opening it. Not an assessment — that goes in `## Assessment` —
and not a claim; claims live in a topic's `findings.md`.

## Key excerpts

Quoted text, verbatim, sufficient to reconstruct every claim drawn from
this source if the source itself becomes unreachable. URLs die: domains
lapse, pages are rewritten in place, archives go behind logins. The
`retrieved:` date plus these excerpts are what survive that. Apply the
vanished-page test before considering this record finished — *if this
page vanished tonight, could I still defend tomorrow every claim I drew
from it?* If no, keep excerpting.

Third-party copyrighted material is excerpted, never bulk-copied: quote
the passages the claims rest on and nothing more. First-party and
`self-authored` material may be committed alongside this record and
pointed at from `locator:`.

> TODO verbatim quote.

TODO locate it — page, section, timestamp, or line — and note in one
line which claim it supports.

> TODO second excerpt; delete this block if one is enough.

TODO locator + what it supports.

## Topics touched

The topic slugs this source bears on, as `[[wikilinks]]` (the
substrate's Layer 2 topic graph — the same edges `/xref` resolves and
back-references). This list is the registry-side half of the join;
each of these topics carries the matching `**Global:** src-NNNN` field
on its local `sources.md` entry. Keep the two in step and keep
`topics:` in the frontmatter in agreement; `/sweep` reports
disagreements rather than repairing them.

- [[TODO-topic-slug]] — TODO local id on that topic's shelf (e.g. `[S1]`)
  and one line on what it feeds there.

## Assessment

TODO one or two lines stating the **basis for the `reliability:`
rating** — track record, accountability, direct access, editorial
process, known errors, an interest in the outcome. A bare rating with no
stated basis is a number somebody made up; six months on, nobody can
tell a judgement from a reflex.

TODO **independence disclosure**, when it applies: does this source draw
on another record already in the registry? Reprints of one wire story,
a paper and the press release written from it, a document and your own
earlier summary of it — each of those is one source, not two, and a
finding must not claim corroboration across them. Name the `src-NNNN`
ids this source is *not* independent of. If it is genuinely
independent, say so and say why.

TODO record any later revision to `reliability:` here, dated, with the
reason. The rating is set once and changed only with a stated cause; the
old rating and its basis stay visible above the new one.
