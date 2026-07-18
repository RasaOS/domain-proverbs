# Cross-linking and the timeline axis

How subjects relate to each other, and how dated facts are kept out of
them. Read `subject-model.md` first — this chapter assumes the Subject
and only describes what sits between subjects.

---

## `links:` is flat, symmetric, and untyped

```yaml
links: [other-subject, third-subject]
```

That is the entire relation model. A list of subject ids. No predicate,
no direction, no weight, no nesting.

A link asserts exactly one thing: **these two subjects bear on each
other; if you are reading one, the other is probably relevant.** It does
not say how they relate. The prose says how.

### Why not typed edges

`caused_by`, `employed_by`, `parent_of`, `member_of` are the obvious
alternative and they are a trap. Three reasons, in ascending order of
importance.

**Typed vocabularies rot.** You add `employed_by`. Then a subject is a
contractor, so you add `contracted_by`. Then a board member, so
`advised`. Then `formerly_employed_by`, because the first predicate had
no tense. Within a year there are eleven predicates, three of which are
near-synonyms, and the corpus is stratified by authoring date — half the
edges were written before predicate seven existed. Nothing queries
reliably. Retrofitting means revisiting every edge in the corpus, which
nobody does, so the vocabulary stays broken and quietly stops being
used.

**They force commitment at the moment of least knowledge.** The edge is
typed when the link is created — the same failure the one-node-type
decision avoids for `type:`. You know that A and B are connected long
before you know *how*; a typed edge makes you guess, and the guess
becomes load-bearing structure that later evidence has to argue against
rather than simply extend.

**A typed edge is an unsourced claim.** This is the decisive one.
`employed_by: acme` asserts a fact about the world. It carries no
source, no date, no confidence, and no qualification. Tenet 2 says a
claim without provenance is not a claim, and that there is no fourth
place for an unsourced assertion to hide. A typed-edge vocabulary is
precisely that fourth place — a claims layer in frontmatter that the
provenance discipline does not reach.

The Established bullet carries strictly more truth than any edge label
can:

```markdown
- Worked at Acme 1987–1991, as contractor for the first two years.
  `[src-0012]` (medium)
```

That is sourced, dated, confidence-marked, and qualified. The edge label
`employed_by` is a lossy compression of it with the provenance thrown
away. Keep the sentence; keep the link untyped.

**What is lost:** you cannot machine-query "all employers of X". That
capability is genuinely given up. It is worth giving up, because the
query would have returned an answer assembled from unsourced labels of
uneven vintage — confident, fast, and untrustworthy. Reading X's
Established section answers the same question with provenance attached.

## Symmetry is a convention, checked — not generated

**If A links B, B links A.** Both files carry the id. `/sweep` reports
any asymmetric pair as a finding.

The obvious alternative is to write one side and have tooling generate
the other. Rejected, for three reasons.

**A generated back-link means writing to a file you did not open.**
Adding a link to A would silently mutate B — B's git history fills with
edits no one made deliberately, and the property that one file is one
subject, changed on purpose, breaks. In a corpus meant to be auditable
six months later, invisible writes are the thing to avoid.

**The convention has to survive a text editor.** These are plain
markdown files with no daemon behind them; the whole portability claim
in PHILOSOPHY depends on that. A rule that only holds while tooling runs
is not a property of the corpus, it is a property of the tooling, and it
breaks the first time someone edits by hand. A rule that is checked
holds regardless of how the edit arrived.

**Asymmetry is signal.** A one-sided link usually means one of three
things: the link was added carelessly and does not survive inspection
from the other side; the reciprocal subject does not exist yet; or the
relation was real but only appeared while working on one of them.
Auto-generation would erase that signal by resolving it silently, always
in favour of keeping the link. The check surfaces it and a human decides
which direction was right — add the reciprocal, or drop the original.

## Link, merge, or split

Three different answers to "these two things are related." Getting this
wrong is the main way a subjects tree degrades, in both directions:
merging too eagerly produces sprawling subjects nobody can read,
splitting too eagerly produces a fog of stubs.

### Default to link

Two subjects that bear on each other, each with its own questions and
its own evidence, stay two subjects with a link between them. High link
count is not a problem. A subject with fifteen links and a tight
Standing section is working exactly as intended.

### Merge when the synthesis layer duplicates

The signals, in order of how reliable they are:

- **Their Standing sections keep restating each other.** You rewrite one
  and find yourself rewriting the same sentences in the other. This is
  the strongest signal and it is decisive on its own — Standing is
  supposed to be the non-redundant current picture, and if two of them
  hold the same picture, there is one subject here.
- **Every source that touches one touches the other.** If no source in
  the registry has ever updated exactly one of them, they are not
  independently observable and the split is not carrying its weight.
- **Their Open questions are the same question phrased twice.**
- **You cannot state a rule for what belongs in which.** If routing a
  new fact between them requires a coin flip, the boundary is not real.

Merging: pick the id that survives, fold the other's Established,
Contested, Sources, and Log into it, close the loser with `status:
closed` and `superseded_by:` pointing at the survivor. **The Log lines
of the closed subject move across verbatim, dates intact.** Never
recycle the closed id and never delete the file — inbound links still
resolve to it, and the pointer tells a reader where the material went.

### Split when the synthesis layer needs internal structure

The signals:

- **Standing needs internal section headings.** A dossier whose current
  picture requires sub-headings to be readable is two or more pictures
  in a trench coat. This is the sharpest available test, and it is worth
  applying literally: the moment you type a `###` inside Standing, stop
  and split instead.
- **Standing runs past a few paragraphs** and tightening the prose does
  not fix it. Length that survives an honest rewrite is structural.
- **One `confidence:` value cannot honestly describe it.** If half the
  Standing rests on solid sourcing and half is speculation, the single
  field has to lie about one of them. That is a split, not a hedge.
- **Open questions cluster into groups that never interact.** Two
  investigation passes that would touch disjoint sources and answer
  disjoint questions are two subjects.
- **The parts want different cadences.** One aspect moving weekly and
  another dormant for a year cannot share a cadence clock.

Splitting: create new ids for the parts, link every new part to every
other and to the original, and write a Log line **in each new subject
recording where it came from, and in the original recording what left.**

If the original remains a real subject at a higher altitude — the
general topic, with the specifics moved out — keep it, keep its id, and
let it hold a short Standing that points at the parts. If the original
dissolves completely, close it. Note that `superseded_by:` takes a
single id and a dissolving split has no single successor: point it at
the largest successor and let `links:` carry the rest. Do not invent a
list-valued `superseded_by` to cover this case — it is rare, the Log
line records the split honestly, and a second list-valued relation field
is the typed-edge mistake creeping back in.

## The timeline is a separate axis

`content/timeline/` holds dated entries. Each entry is one file, named
by its date, whose frontmatter lists the subject ids it touches:

```yaml
id: 1916-07-01-somme-offensive-begins
date: 1916-07-01
subjects: [somme-offensive, british-expeditionary-force]
```

Entries reference subjects. Subjects do not own entries. **A subject's
history is a query over the timeline, not a copy of it.** The `##
Timeline` section inside a dossier is a convenience view — a list of
pointers — and when it disagrees with the entries, the entries win. See
`../timeline/README.md` for the file convention.

### Why events are not just subjects

The Subject model does allow `type: event`, so this needs stating
precisely. The two are not alternatives; they are different objects that
often coexist and reference each other.

**A timeline entry is a dated fact that relates subjects.** It is closed
as of writing. It has no Standing to rewrite, no Open questions, no
cadence, no confidence about the *picture* — only about whether the
thing happened as stated, on the date stated. It does not accumulate. It
gets corrected if a source turns out to be wrong, and the correction is
noted in the Logs of the subjects it touches.

**A `type: event` subject is a research target.** It has open questions,
a cadence, a Standing section that gets rewritten as evidence moves, and
a Log recording how the picture changed. It accumulates for as long as
it is tracked.

The test is one question: **does this have open questions?** If it does,
it is a subject. If it is "this happened on this date, per this source",
it is a timeline entry.

Worked example. `somme-offensive` is a subject with `type: event`: an
ongoing research target with contested casualty figures, open questions
about planning, sources that disagree, and a Standing section rewritten
each pass. `1916-07-01-somme-offensive-begins.md` is a timeline entry:
the offensive began on that date, per source, and that fact is settled
and will not grow. The entry lists `somme-offensive` among its subjects;
the subject's `## Timeline` section points back at the entry. Both
exist. Neither is redundant.

### Why the axis is separate at all

Because **an event relates N subjects and none of them owns it.** The
opening of an offensive touches the offensive, the commanders, the
formations, and the places. Storing that fact inside one of those
subjects is an arbitrary choice that every other subject then has to
work around. Storing it in all of them is duplication, and duplicated
facts drift — one copy gets corrected, the others do not, and six months
later the corpus quietly contradicts itself.

A separate axis gives the fact exactly one home, which is also what
makes correcting it a single edit.

The same argument does *not* apply to `links:`, which is why links are
duplicated on both sides. A link is not a fact about the world; it is a
navigation aid local to each subject, and there is no third thing for it
to live in. A dated fact has somewhere to go. A "these are related"
assertion does not.

## Traversal

Both structures are plain frontmatter, so both queries are greps. No
index is built or maintained.

**"What connects A and B?"** In three passes, cheapest first:

1. **Direct link.** Is B in A's `links:`? Done.
2. **Path over links.** Breadth-first from A over `links:`, stopping at
   B. Report the path, and treat length as a warning: a five-hop path is
   usually not a connection, it is the graph being connected to itself.
   Read the Standing sections along the path before claiming anything —
   the link says only that a relation exists, and the prose is where the
   answer actually lives.
3. **Timeline co-occurrence.** Find entries whose `subjects:` list
   contains both A and B. This catches relations the link graph does not
   have, and it is the better answer when it exists, because a shared
   dated fact is a sourced connection rather than an assertion of
   relatedness.

A co-occurrence with no corresponding link is a finding: either the link
is missing, or the two merely shared a date. `/sweep` proposes the link;
a human decides.

**"What happened in period P?"** A filename range filter over
`content/timeline/`. Because entries are date-prefixed and zero-padded,
the directory listing is already in chronological order — the sorted
listing *is* the index, which is the whole reason for the naming
convention. Filter by `subjects:` to scope the period to one subject or
a set of them.

**"What is the history of A?"** Every entry whose `subjects:` contains
`a`, in filename order. Do not read A's `## Timeline` section for this;
that section is a cached view and may lag.

## Graph hygiene at scale

The failure mode of an untyped graph is the **hub**: a subject that
accumulates links from everything until traversing through it means
nothing. Once a hub exists, every path in the corpus runs through it,
which is the same as having no paths at all.

**The test is not link count, it is neighbour coherence.** Ask: *do this
subject's neighbours have anything to do with each other?* A subject
with thirty links whose neighbours are all mutually relevant is a
legitimately central subject. A subject with twelve links whose
neighbours are mutually unrelated is a category wearing a subject's
clothes, and every path through it is a false connection.

Link count is still worth watching as a cheap trigger: **past roughly
fifteen links, apply the coherence test.** Below that, do not bother.

Two fixes:

- **Split it by axis** if the neighbours cluster. The clusters are the
  real subjects; the hub becomes a short parent that links them.
- **Demote it to a tag** if they do not cluster. This is what `tags:` is
  for. The line between the two structures is exact: **if the relation
  is "these are all the same kind of thing", that is a tag; if it is
  "these two bear on each other", that is a link.** A hub is almost
  always a category that was mistakenly given a file. Converting it
  means tagging the members, closing the hub, and recording the reason
  in its Log so the same hub is not opened again in a year.
