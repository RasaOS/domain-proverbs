# Passive ingestion

How supplied material enters the corpus. The user hands over a source —
a PDF, a link, a transcript, a page of notes — and the domain distils it
and files it against every topic it touches. Read `topic-overlay.md`
first, and the module's `.claude/research-rules.md` before that; this
chapter assumes the topic-folder shape and adds nothing to it.

---

## The defining asymmetry

**Ingestion is source-first and fans out to many topics.
Investigation is topic-first and fans out to many sources.**

That inversion is the whole difference between the two modes, and it
dictates everything downstream.

| | Active (`/investigate`) | Passive (`/ingest`) |
|---|---|---|
| Starts from | one topic | one source |
| Fans out to | many sources | many topics |
| Reads first | the topic's `open-questions.md` | the source, whole |
| Typically writes | one topic folder | several topic folders |
| Failure mode | thin sourcing | claims filed under the wrong topic |

An investigation pass knows where its output goes before it starts. An
ingestion pass does not — the routing is discovered by reading. A
source about one nominal subject routinely carries load-bearing detail
about three other topics already tracked and introduces two that
aren't. Treating ingestion as "summarise this into its obvious topic"
throws away most of what the source was worth, and it is the single
most common way this mode is done badly.

The corollary: an ingestion pass that touched exactly one topic is not
wrong, but it deserves a second look. Ask whether the fan-out was
genuinely absent or merely not looked for.

## The pipeline

Eight steps, in order. Steps 1 and 2 complete before any topic file is
written.

### 1. Register the source

The source gets a record and an id (`src-NNNN`) in `research/sources/`
before anything is extracted from it — see `provenance.md`. Provenance
is assigned at intake, not reconstructed afterwards. A claim extracted
from an unregistered source has nowhere to point, and the id is what
every later step carries.

Register what the source *is*: what it claims to be, who produced it,
when, how it was obtained, and how reliable it looks. Reliability is
recorded once, at the source, rather than re-argued at every claim.

The global record comes first because the fan-out has not happened yet.
The local `[S#]` shelf rows come in step 7, once the routing is known —
a source's topic set is an output of the read, not an input to it.

### 2. Read it whole before writing anything

Read the entire source before the first edit. This is not a courtesy
rule; it is load-bearing for routing. Correct routing requires knowing
what the source covers in total, and material that seems peripheral on
page 2 often turns out to be the reason the source matters by page 30.
A pass that writes as it reads files its early claims against the wrong
topic set and then has to be unpicked.

For long sources, note candidates while reading and write nothing until
the read completes.

### 3. Extract candidate claims

Pull out discrete, checkable statements. One statement per candidate —
a compound sentence carrying three facts is three candidates, because
they will route differently and may not share a confidence value.

A candidate is a claim, not a topic. "Discusses the funding round" is a
topic; "the round closed in March 1998" is a claim. Only claims get
filed.

Candidates that are pure interpretation by the source's author are
still candidates — they are recorded as *that author's* position, with
attribution, not as fact.

### 4. Route each claim

Decide which topics each candidate touches. See **Routing** below. Read
the candidate topics' `open-questions.md` while routing: a source that
answers a standing question is the highest-value routing hit there is.

### 5. Propose new topics where the source earns them

Entities the source introduces that aren't tracked yet may deserve a
topic of their own. See **The new-topic threshold** below.

**Opening a topic is the substrate's `/research new`, not this mode's
job.** Ingestion proposes; the user decides; `/research new` scaffolds
the folder, assigns the `RT-NNN` id, and adds the `INDEX.md` row. An
ingestion pass that creates topic folders directly bypasses the
registry and the slug confirmation, and produces exactly the sprawl the
threshold exists to prevent.

### 6. Update each touched topic

For each topic in the routing set, per the substrate's file contract
plus this domain's `contested.md`:

- new sourced claims → `findings.md`, as the next `## F#` with
  `**Confidence:**` and a basis citing the local `[S#]`
- claims that conflict with an existing finding → `contested.md`, both
  sides kept with their sources, the conflict left standing
- questions the source raises but does not answer → `open-questions.md`
- dated facts that relate several topics and are owned by none →
  `research/timeline/` (see `timeline-axis.md`)
- `## State of play` in the README rewritten **only if** the picture
  actually moved; bump `updated:`

State of play is rewritten, never appended to. If the source added
facts without changing the current view, leave it alone — an ingestion
pass that only adds findings is a normal outcome.

Where a claim asserts a relation between two tracked topics, add the
`[[slug]]` in prose and mirror it into `related:` on the topic you are
editing. Do not hand-maintain the reverse edge — `/xref` computes
back-references and reconciles `related:` against the inline links.

### 7. Add the local `[S#]` row to each touched `sources.md`

Every topic that received a claim from this source gets a row on its
own shelf: the next `[S#]` in that topic, a one-line note on what the
source was good for *here*, and a pointer to the global `src-NNNN`.

The same source is `[S4]` in one topic and `[S11]` in another. That is
correct and not a defect — the local id keeps each topic readable
standalone, and the global id is what reconciles them. A claim citing
an `[S#]` whose row is missing from that topic's shelf is a broken
citation even though the global record exists.

### 8. Append to each touched `log.md`

Every touched topic gets an entry under today's dated heading, and
every one of those entries carries **the same `src-NNNN`**. This is
what makes the fan-out recoverable: six months later, "what did
src-0043 change?" is answered by grepping the id across logs, and the
answer is complete because the id was written uniformly at ingest time.

```markdown
## 2026-07-18

- /ingest src-0043 (local [S4]): two claims to findings.md; F2 moved
  to contested.md.
```

`last_swept` is **not** advanced by ingestion. Routing a claim into a
topic is not the same as re-examining that topic's picture, and a pass
that fans out to six topics has glanced at six, not swept six.
Advancing the clock there would make the corpus assert an attention it
did not receive — the one thing the longitudinal record must never lie
about. The sweep advances it; `/investigate` advances it; ingestion
does not.

## Routing

A claim belongs to a topic when it changes what that topic's folder
would say — not merely when the topic's subject appears in the
sentence. Mentions are not claims about the mentioned thing.

The test, applied per claim per candidate topic:

1. Does the claim assert something about this topic's substance, its
   chronology, or its relations?
2. Would someone reading only this topic be missing something if the
   claim were absent?
3. Does it answer, sharpen, or open a line in this topic's
   `open-questions.md`?

Any yes routes the claim there.

**The N-topic rule: a claim that touches N topics is recorded in all N,
with the same `src-NNNN` — not only in the "main" one.**

There is no main topic. The instinct to file a claim once, under
whichever topic feels most central, and rely on `related:` / `[[slug]]`
to carry it to the others, is the failure that hollows out a fan-out
corpus. It fails because each topic folder is read on its own — the
point of the State-of-play/findings discipline is that answering "what
do we know about X" means reading X, not X plus its neighbours plus a
judgement call about which neighbour someone filed a fact under. The
link layers are for association, not for storage. Duplication across
topics is the intended cost; the global src id is what keeps the copies
reconcilable.

Word the claim for each topic it lands in. The same fact reads
differently from two topics' vantage points, and rewording is not drift
as long as the src id and the confidence value are identical. If two
wordings would need *different* confidence, they are two claims, not
one.

## The new-topic threshold

Sources name far more entities than a corpus should track. Most
mentions belong in prose in `## State of play` or in a finding, named
but not tracked. Opening a topic is a commitment to maintain it, and a
corpus full of one-line stubs is worse than one that names things in
prose, because the stubs consume sweep attention and return nothing.
The substrate says the same thing from the other direction: err toward
fewer, larger topics; a swarm of thin ones defeats the index.

An entity earns a topic when **any** of these holds:

- **Recurrence.** It has appeared in two or more registered sources.
  Recurrence across independent sources is the strongest available
  signal that it will keep coming up.
- **Attached open questions.** The source raises a question about it
  that no current topic is the right home for. A question with nowhere
  to live is the clearest case for a new topic.
- **Future lookup.** It is something that will plausibly be searched
  for later on its own terms — a name someone would type. If a future
  reader would go looking for it directly, it needs a folder to find.
- **Overloading.** An existing topic is accumulating a distinct
  sub-picture that is starting to crowd its State of play. Splitting is
  the fix, per the scaling claim in `PHILOSOPHY.md`.

None of those holding means: name it in prose, cite the source, move
on. It costs nothing to open the topic later when it recurs — that is
what the recurrence trigger is for.

A topic opened this way opens at the substrate's **`status: open`** —
"registered, scoped, but not yet actively worked." That is precisely
the honest state for a topic that exists on one source's say-so, and it
is why this domain adds no status value of its own. It moves to
`active` when a second source or an investigation pass justifies it,
and to `archived` with a recorded reason when it turns out to be
nothing. Failed topics are archived, never deleted — a dead end that
isn't recorded gets re-explored.

Cadence for a newly proposed topic should be long (`90d`) or `none`. Do
not put a hunch on a 7-day clock.

## Fidelity

**Distil on the source's own terms first. Interpretation is a separate,
marked layer.**

The first pass records what the source says, in the source's own frame,
with its own hedges intact. A source that says "appears to have" is
recorded as "appears to have" — flattening a hedge into an assertion is
a fabrication, and it is invisible once the source is closed.

Then, separately and marked as such, record what it means. Synthesis
lives in `## State of play`, where the prose says plainly that it is
synthesis. Inference that goes beyond the source and hasn't been
checked lives in `open-questions.md` as a question. There is no third
place.

The rule stated so it can be checked: **never let a summary silently
become an assertion the source didn't make.** Test any finding by
asking whether the source's author would recognise it as something they
wrote. If they'd say "that's not quite what I said," it is either
misworded or it is synthesis in the wrong file.

Specific ways this goes wrong:

- **Hedge removal.** "Some evidence suggests X" → "X". The most common
  and the hardest to catch later.
- **Attribution collapse.** The source quoting someone else's claim
  becomes the source claiming it. Record who said it.
- **Aggregation.** Three weak indications summarised as one confident
  statement. Confidence does not accumulate through paraphrase.
- **Scope creep.** A claim about one instance restated as a general
  rule.

Confidence reflects what the *source* supports, not how plausible the
claim feels. A single unreliable source asserting something forcefully
is a `low`-confidence finding.

## Excerpt discipline

Third-party sources are usually copyrighted. The corpus registers them
**by reference and short excerpt** — it does not become a mirror of
them.

- Register the pointer: identifier, locator, and where the material can
  be obtained. That is what the `research/sources/` record is for.
- Quote sparingly, and only where the exact wording is load-bearing —
  a contested claim turning on a specific phrase, a definition, a hedge
  that matters. Keep quotes short, in quotation marks, attributed by
  src id and locator (page, timestamp, section).
- Everything else is distilled into the corpus's own words as sourced
  findings. That is the normal case, and it is also better research
  practice than transcription.
- **Never bulk-copy** a source's text into a topic folder or a file
  under `content/`. No pasted chapters, no full transcripts, no
  reconstruct-by-excerpt across several ingestion passes.
- First-party material — the user's own notes, their own recordings,
  documents they hold the rights to — may be committed in full,
  alongside the source record or in the topic folder. The distinction
  is rights, not format.

If a source cannot be excerpted at all, register it and distil it; the
claims survive without the text.

## Batch ingestion

Several sources supplied at once are ingested as several sources, run
through the pipeline in sequence. The batch is a convenience for the
user, not a unit in the corpus.

**Each source gets its own `research/sources/` record, its own `[S#]`
row in every topic it touches, and its own log entry in every one of
those topics.** Never merge a batch into one record ("the March
documents") or one log entry ("ingested six sources").

Three reasons, all of which bite later:

1. **Corroboration needs distinct ids.** Two sources agreeing is the
   corpus's main confidence signal, and two `[S#]` refs on one finding
   is what encodes it. A merged record makes two independent
   confirmations look like one, and the recurrence trigger for
   proposing new topics stops working.
2. **Reliability is per-source.** If one source in the batch is later
   discredited, its claims must be identifiable and revisitable
   individually. Under a merged id every claim from the batch is
   contaminated and none can be cleanly separated.
3. **The log is an audit trail.** "What did this source change?" must
   be answerable per source. Merged entries destroy exactly the
   granularity the append-only layer exists to preserve.

Order matters within a batch when sources conflict. Ingest, let the
conflict land in `contested.md`, and leave it standing — do not resolve
a conflict inside a batch by preferring the source read last, or the
longer one. Resolution is a separate, explicit act recorded in
`log.md`, and it requires the warrant `investigation.md` describes.

A batch may legitimately produce one summary *to the user* at the end.
It never produces one record on disk.
