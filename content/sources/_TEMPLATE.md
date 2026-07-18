---
id: src-NNNN              # must match the filename; assigned once, never recycled
title:                    # human-facing; may be corrected freely
author:                   # person, org, or `unknown`
date:                     # YYYY-MM-DD the SOURCE was created/published, or `unknown`
kind:                     # primary | secondary | tertiary | personal-communication | dataset | self-authored
locator:                  # URL, DOI, ISBN, file path, or a description if none exists
retrieved:                # YYYY-MM-DD you fetched/read it — mandatory for any URL
added:                    # YYYY-MM-DD it entered the registry
reliability:              # high | medium | low | unknown
access:                   # public | paywalled | offline | private | restricted
subjects: []              # subject ids this source touches
tags: []                  # free-form, flat, optional
---

# <title>

## Summary

What this source is and what it covers, in two or three sentences.
Written so a future pass can decide whether to re-open it without
re-reading it.

Describe the source, not the corpus's view of the subject. Claims go in
subjects, with a citation pointing back here.

## Key excerpts

Quoted text, verbatim, enough to reconstruct every claim cited from
this source.

> The exact words, quoted.

URLs die — domains lapse, pages get rewritten in place, archives go
behind logins. The `retrieved:` date plus the excerpts below are what
survives that. A paraphrase does not survive it, because a paraphrase
is already your reading of a page nobody can check any more.

The test, applied before this record is considered finished: *if this
page vanished tonight, could I still defend tomorrow every claim I drew
from it?* If not, go back and quote more.

Third-party copyrighted work is excerpted only — the minimum needed to
support the cited claims, never a wholesale copy. First-party and
`self-authored` material may be committed alongside this record in
full.

## Subjects touched

Routing list. One line per subject, saying what this source was good
for there. Keep in sync with `subjects:` above and with each subject's
`sources:` list and `## Sources` section.

- `some-subject` — what this gave that subject.

## Assessment

Why the `reliability:` rating is what it is, in one or two lines.
Standing, track record, access, interest in the outcome, editorial
process — whatever actually drove the call. A rating with no stated
basis is a number somebody made up.

Note anything that limits the source: gaps, bias, second-hand access,
dependence on another source. If this source is **not independent** of
another registry entry, say so here and name the id — corroboration
between two sources that share an origin is not corroboration, and this
is the only place that will be recorded.

Reliability is a property of this source, not of any claim drawn from
it. A source rated `high` can still support a claim at `(low)` when it
only mentions the thing in passing. See
[`../framework/provenance.md`](../framework/provenance.md).
