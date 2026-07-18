# Investigation — the active mode

How a research pass runs against a topic. This is the **active** mode
of the three: it pulls material from outside the corpus and lands it in
a topic folder. Read `topic-overlay.md` first, and the module's
`.claude/research-rules.md` before that — everything here is read and
write operations on files those two already define. This chapter adds
no structure of its own.

---

## Question-driven, not topic-driven

A pass reads `open-questions.md` **first** — before the README, before
`findings.md`, before anything else in the folder — and works those
questions. It does not free-associate about the topic and see what
turns up.

The distinction is not stylistic. Topic-driven research against a topic
already tracked for a year re-finds what is already in `findings.md`
and produces a pass that costs an hour and adds nothing.
Question-driven research is bounded: the questions define what would
count as progress, so the pass can be scoped, can be judged, and can
*end*.

The consequence: **a topic with no open questions is not ready for an
investigation pass.** Either write questions first, or the topic is
mislabeled `status: active` and belongs at `dormant`. A pass that opens
with "there's nothing specific to chase here, let me look around" is
the failure mode, not the warm-up.

Open questions are also the pass's output, not only its input. Most
passes close some and open others; a pass that answers three questions
and raises five has done well, not badly. The substrate gives a
question three exits — answered (it graduates to a finding), too big
(it spawns its own topic via `/research new`), or dropped with a
one-line reason. Use them; do not silently delete a line.

## The pass

Eight steps, in order. Each has a defined input and a defined write
target.

### 1. Scope from `open-questions.md`

Read the topic folder. Take the live question list and pick the ones
this pass will work — usually two to four. State them explicitly at the
start of the pass. Questions not picked are left alone, not silently
dropped.

If a question turns out to be malformed — unanswerable as written, or
answerable only by opinion — rewrite it into an answerable form or
strike it with a reason. Recording that a question was malformed is a
result.

### 2. Fan out searches

Turn each scoped question into several independent search angles. See
**search breadth discipline** below. This is the step where a pass is
won or lost.

### 3. Register sources — global registry first, then the local shelf

Every source that will be cited is registered **twice, in this order**,
before it is cited:

1. **`research/sources/src-NNNN.md`** — the corpus-wide registry this
   domain adds. Id, locator, retrieval date, reliability, and whatever
   else the record requires (`provenance.md`).
2. **the topic's `sources.md`** — the substrate's local shelf. Next
   `[S#]` in this topic, with its row pointing at the global
   `src-NNNN`.

Findings cite the **local `[S#]`**, per the substrate. The global id is
what makes "topic A's claim and topic B's claim rest on the same
evidence" recoverable; the local id is what keeps the topic readable on
its own. Both, always — a source on one shelf and not the other is a
half-registered source.

Registration happens at fetch time, not at write-up time, because
write-up time is when the URL turns out to have been lost. A source
that was fetched and turned out to be useless still gets a global
record, marked checked-and-empty. That is what stops it being
re-fetched next pass.

### 4. Extract claims with provenance

Pull discrete claims out of each source. One claim per candidate, each
carrying its `[S#]` and a confidence value. A claim that cannot be tied
to a specific source is not a finding — the substrate's rule is that a
claim without evidence is an open question. It goes to the README's
`## State of play` as marked synthesis, or to `open-questions.md` as a
suspicion. Tenet 2 has no exceptions.

Confidence describes the *source's* support for the claim, not how
plausible it sounds. A single source of unknown reliability saying
something is `low`, however confident the source's own prose is.

### 5. Reconcile against `findings.md` and `contested.md`

The new claims meet the existing ones. Rules below.

### 6. Rewrite `## State of play`

The topic README's `## State of play` is **rewritten**, not appended
to. Produce the current picture as it stands after this pass, in prose,
short. Do not narrate the pass — "we now also know that…" is `log.md`
material. It reads as if written fresh today by someone who never saw
the earlier version.

Bump `updated:` in frontmatter. Flip `status: open` → `active` if this
is the topic's first real pass.

### 7. Append to `log.md`

One entry, under today's dated heading, describing what the pass did
and what moved. Append only — never edit an earlier entry, never
reorder, never prune.

```markdown
## 2026-07-18

- /investigate: worked Q1, Q3. Four sources registered (src-0044…0047,
  local [S6]–[S9]); F2 moved to contested.md against src-0044.
  Saturated at four angles.
```

Dated facts that belong to no single topic go to `research/timeline/`
rather than into a finding — see `timeline-axis.md`. The log entry is
what makes the pass auditable six months later. A pass that changed the
topic but wrote no log entry has corrupted the record even if every
claim it added is correct.

### 8. Advance `last_swept`

Set `last_swept:` to today in the topic README's frontmatter. An
investigation pass **is** a look at the topic, so it resets the cadence
clock the same way a sweep does. This holds on an empty pass too — a
topic that was searched and yielded nothing is in a completely
different state from one nobody has opened in a year, and `last_swept`
is the only field that carries the difference.

Never backdate it, and never advance it for a topic the pass did not
actually open.

## Reconciliation rules

The new claims meet the existing ones. Four cases.

**New claim, no existing counterpart.** Append to `findings.md` as the
next `## F#` with its `**Confidence:**`, its basis citing `[S#]`, and
its implications.

**New claim agrees with an existing finding.** Add the new `[S#]` to
that finding's basis line. Raise `**Confidence:**` if independent
corroboration warrants it — independent, meaning not two outlets
reprinting one wire story. Two sources with a common upstream are one
source.

**New claim contradicts an existing finding.** The finding is **not
overwritten, not deleted, and not marked `Superseded-by:`.** It moves
to `contested.md`, carrying both sides and both `[S#]` refs, and the
conflict is left standing. Record the move in `log.md`.

**New claim resolves an existing contest.** Allowed, but explicitly:
move it back to `findings.md`, state which side won and on what
evidence, and record the resolution in `log.md`. "Resolved because a
third source arrived and it agrees with side A" is a resolution.
"Resolved because side B seemed weak" is not.

### `Superseded-by:` versus `contested.md` — the line

The substrate's `findings.md` carries a `Superseded-by:` field. This
domain adds `contested.md`. They handle different situations and using
one for the other's job is the mistake this section exists to prevent.

| | `Superseded-by:` | `contested.md` |
|---|---|---|
| The claim is | **corrected** | **disputed** |
| You can name | which side is wrong, and why | only that the sources disagree |
| The corpus has | warrant to pick | no warrant to pick |
| Outcome | one claim replaces another | both stand, indefinitely |

**The test: can you state, on evidence, why the old claim is wrong?**

If yes — a date was misread, a source issued a correction, a better
primary document settles it — that is a correction. Write the new
finding, point the old one's `Superseded-by:` at it, and log the
reason. Nothing is contested; the question is answered.

If the honest answer is "the newer source seems better," or "the
longer one is more thorough," or "this one is easier to work with" —
that is not a correction. It is a disagreement you have no warrant to
settle, and it goes to `contested.md` with both sides.

This is tenet 3, and it is the rule most likely to be violated by a
pass that wants to look productive, precisely because `Superseded-by:`
is sitting right there and makes the resolution look sanctioned.
Reaching for it without warrant is the single most damaging operation
available in this domain: the loser disappears from `findings.md`,
every later pass inherits a settled claim with no trace it was ever in
doubt, and the error becomes invisible and load-bearing. A claim that
sits in `contested.md` for two years is a healthy artifact. A silently
superseded one is a landmine.

## Search breadth discipline

**Multiple independent angles beat one deep thread.** A single search
line followed for an hour explores one corner of the available material
and returns a coherent, confident, and possibly badly skewed picture.
Four shallow angles from different directions surface the disagreement
that tells you where the real question is.

Concrete angle types to run against a scoped question:

- **By entity name** — the topic's own subject matter by name, plus
  known aliases, former names, and misspellings. Renamed things are
  frequently invisible under their current name.
- **By event or date** — what happened, when, without the name in the
  query. Catches material where the subject is mentioned but is not the
  headline.
- **By adjacent actor** — the people, organizations, or topics linked
  to this one (`related:` and `[[slug]]` are the starting list).
  Adjacent parties leave records about each other, and their accounts
  of the same events are where contests come from.
- **By primary-document type** — filings, transcripts, registries,
  datasets, official records. The document class that would *have* to
  exist if a claim is true, searched for directly.

Run angles in parallel where the tooling allows and treat their results
as independent evidence. Two angles converging on the same source is
one source, not two.

## Stopping rules

A pass ends when one of these is true. Name which one in `log.md`.

**Questions closed.** Every scoped question is answered, narrowed to a
sharper question, or recorded as unanswerable with the reason.

**Saturation.** The searches stop returning new material. The explicit
heuristic: **two consecutive search angles return no source that is not
already registered for this topic.** Not "the results look familiar" —
two angles, consecutively, zero new registrations. At that point the
accessible surface for these questions is exhausted and further
searching is spending time to re-find what is already on the shelf.

**Budget.** The pass hits whatever time or call budget the user set.
This ends the pass but does not close the questions; the log says the
pass was cut short so the next one knows where it stands.

Saturation is a finding in its own right. "Saturated at four angles
with no new sources" in `log.md` tells the next pass, and the next
sweep, that this question needs a different kind of source rather than
more of the same searching.

## The anti-fabrication gate

**If the search yields nothing, the pass writes that down and changes
nothing else.**

The log entry records what was actually attempted:

```markdown
## 2026-07-18

- /investigate: nothing found. Searched entity name + two aliases,
  filings 2019–2024, adjacent-org registry. No new sources. State of
  play untouched. last_swept advanced.
```

`## State of play` is left exactly as it was. No findings are added. No
confidence is raised. No open question is quietly deleted to make the
topic look tidier. Only `log.md` and `last_swept` move.

An empty pass is a real result and one of the more valuable ones,
because it is evidence about the availability of material — and because
it is checkable. The named angles let the next pass avoid repeating
them, and let a reader judge whether the pass looked in sensible
places.

The failure this gate exists to prevent: a pass that finds nothing and
produces a fluent paragraph anyway, assembled from background knowledge
and inference, that reads exactly like a paragraph built from sources.
Once that paragraph is in `## State of play` it is indistinguishable
from researched material, it will be cited by the next pass, and there
is no way to find it later. Per tenet 5, a thin State of play with five
open questions is a better artifact than a confident paragraph resting
on nothing.

The gate is unconditional. It applies when the pass has found nothing,
when it has found a little and wants to round up, and when the user
asked for a summary and would clearly prefer a substantive one.

## What a pass does not do

- **Does not touch other topics' folders.** Material about an adjacent
  topic that surfaces during a pass is noted in this topic's `log.md`
  and routed by `/ingest`, which is the mode built for fan-out. A pass
  that starts editing three neighbouring topics has become an unbounded
  pass.
- **Does not open topics.** Opening a topic is the substrate's
  `/research new`. A pass can propose one, and should when a scoped
  question turns out to be too big; the user decides.
- **Does not conclude or promote.** That is `/research conclude`, which
  reads the seam and hard-stops without a `promotion_target`.
- **Does not commit.** Edits land in the working tree for review.
- **Does not rewrite `log.md`.** Ever, under any circumstance.
