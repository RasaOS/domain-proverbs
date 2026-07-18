# Passive ingestion

How supplied material enters the corpus. The user hands over a source —
a PDF, a link, a transcript, a page of notes — and the domain distils it
and files it against every subject it touches. Read `subject-model.md`
first; this chapter assumes the Subject file shape and says nothing
about it.

---

## The defining asymmetry

**Ingestion is source-first and fans out to many subjects.
Investigation is subject-first and fans out to many sources.**

That inversion is the whole difference between the two modes, and it
dictates everything downstream.

| | Active (`/investigate`) | Passive (`/ingest`) |
|---|---|---|
| Starts from | one subject | one source |
| Fans out to | many sources | many subjects |
| Reads first | the subject's Open questions | the source, whole |
| Typically writes | one dossier | several dossiers |
| Failure mode | thin sourcing | claims filed under the wrong subject |

An investigation pass knows where its output goes before it starts. An
ingestion pass does not — the routing is discovered by reading. A
source about one nominal topic routinely carries load-bearing detail
about three other subjects already in the corpus and introduces two
that aren't. Treating ingestion as "summarise this into its obvious
dossier" throws away most of what the source was worth, and it is the
single most common way this mode is done badly.

The corollary: an ingestion pass that touched exactly one subject is
not wrong, but it deserves a second look. Ask whether the fan-out was
genuinely absent or merely not looked for.

## The pipeline

Seven steps, in order. Steps 1 and 2 complete before any file is
written.

### 1. Register the source

The source gets a record and an id (`src-NNNN`) in the source registry
before anything is extracted from it — see `provenance.md`. Provenance
is assigned at intake, not reconstructed afterwards. A claim extracted
from an unregistered source has nowhere to point, and the id is what
every later step carries.

Register what the source *is*: what it claims to be, who produced it,
when, how it was obtained, and how reliable it looks. Reliability is
recorded once, at the source, rather than re-argued at every claim.

### 2. Read it whole before writing anything

Read the entire source before the first edit. This is not a courtesy
rule; it is load-bearing for routing. Correct routing requires knowing
what the source covers in total, and material that seems peripheral on
page 2 often turns out to be the reason the source matters by page 30.
A pass that writes as it reads files its early claims against the wrong
subject set and then has to be unpicked.

For long sources, note candidates while reading and write nothing until
the read completes.

### 3. Extract candidate claims

Pull out discrete, checkable statements. One statement per candidate —
a compound sentence carrying three facts is three candidates, because
they will route differently and may not share a confidence level.

A candidate is a claim, not a topic. "Discusses the funding round" is a
topic; "the round closed in March 1998" is a claim. Only claims get
filed.

Candidates that are pure interpretation by the source's author are
still candidates — they are recorded as *that author's* position, with
attribution, not as fact.

### 4. Route each claim

Decide which subjects each candidate touches. See **Routing** below.

### 5. Open new subjects where the source earns them

Entities the source introduces that aren't tracked yet may deserve a
dossier of their own. See **The new-subject threshold** below. New
subjects are proposed to the user, not created silently.

### 6. Update each touched dossier

For each subject in the routing set, edit the dossier per the section
rules in `subject-model.md`:

- new sourced claims → `## Established`, with the src ref and a
  confidence marker
- claims that conflict with something already Established → `##
  Contested`, both sides kept with their sources, the conflict left
  standing
- questions the source raises but does not answer → `## Open questions`
- dated facts → `## Timeline`
- the src id and a one-line note on what it was good for → `## Sources`
- `## Standing` rewritten if the picture actually moved

Standing is rewritten, never appended to. If the source didn't change
the picture, leave Standing alone — an ingestion pass that only adds
Established bullets is a normal outcome.

### 7. Append to each touched Log

Every touched subject gets a Log line, and every one of those lines
carries **the same source id**. This is what makes the fan-out
recoverable: six months later, "what did src-0043 change?" is answered
by grepping the id across Logs, and the answer is complete because the
id was written uniformly at ingest time.

```markdown
- 2026-07-18 — /ingest src-0043: two claims to Established; one
  existing claim moved to Contested.
```

## Routing

A claim belongs to a subject when it changes what that subject's
dossier would say — not merely when the subject's name appears in the
sentence. Mentions are not claims about the mentioned thing.

The test, applied per claim per candidate subject:

1. Does the claim assert something about this subject's substance, its
   timeline, or its relations?
2. Would someone reading only this dossier be missing something if the
   claim were absent?
3. Does it answer, sharpen, or open a question in this subject's `##
   Open questions`?

Any yes routes the claim there.

**The N-subject rule: a claim that touches N subjects is recorded in
all N, with the same src ref — not only in the "main" one.**

There is no main subject. The instinct to file a claim once, under
whichever subject feels most central, and rely on `links:` to carry it
to the others, is the failure that hollows out a fan-out corpus. It
fails because each dossier is read on its own — the point of the
Standing/Established discipline is that answering "what do we know
about X" means reading X, not X plus its neighbours plus a judgement
call about which neighbour someone filed a fact under. Duplication
across dossiers is the intended cost; the src ref is what keeps the
copies reconcilable.

Word the claim for each dossier it lands in. The same fact reads
differently from two subjects' vantage points, and rewording is not
drift as long as the src ref and the confidence marker are identical.
If two wordings would need *different* confidence, they are two claims,
not one.

Relations between two tracked subjects go in both dossiers and get
`links:` updated on both sides. `links:` is symmetric by convention and
ingestion is where the asymmetry usually creeps in.

## The new-subject threshold

Sources name far more entities than a corpus should track. Most
mentions belong in prose in `## Standing` or in a claim in `##
Established`, named but not tracked. Opening a dossier is a commitment
to maintain it, and a corpus full of one-line stubs is worse than one
that names things in prose, because the stubs consume sweep attention
and return nothing.

An entity earns a dossier when **any** of these holds:

- **Recurrence.** It has appeared in two or more registered sources.
  Recurrence across independent sources is the strongest available
  signal that it will keep coming up.
- **Attached open questions.** The source raises a question about it
  that no current subject is the right home for. A question with
  nowhere to live is the clearest case for a new node.
- **Future lookup.** It is something that will plausibly be searched
  for later on its own terms — a name someone would type. If a future
  reader would go looking for it directly, it needs a file to find.
- **Overloading.** An existing dossier is accumulating a distinct
  sub-picture that is starting to crowd its Standing. Splitting is the
  fix, per the scaling claim in `PHILOSOPHY.md`.

None of those holding means: name it in prose, cite the source, move
on. It costs nothing to open the subject later when it recurs — that is
what the recurrence trigger is for.

New subjects opened this way default to **`status: speculative`**. The
source introduced them; nothing has yet confirmed they are worth
tracking. Speculative is the honest state for a node that exists on one
source's say-so. It is promoted to `active` when a second source or an
investigation pass justifies it, and closed with a recorded reason when
it turns out to be nothing. Speculative subjects that fail are closed,
never deleted — a dead end that isn't recorded gets re-explored.

Cadence for a new speculative subject should be long (`90d`) or `none`.
Do not put a hunch on a 7-day clock.

## Fidelity

**Distil on the source's own terms first. Interpretation is a separate,
marked layer.**

The first pass records what the source says, in the source's own frame,
with its own hedges intact. A source that says "appears to have" is
recorded as "appears to have" — flattening a hedge into an assertion is
a fabrication, and it is invisible once the source is closed.

Then, separately and marked as such, record what it means. Synthesis
lives in `## Standing`, where the model says plainly that it is
synthesis. Inference that goes beyond the source and hasn't been
checked lives in `## Open questions` as a question. There is no third
place.

The rule stated so it can be checked: **never let a summary silently
become an assertion the source didn't make.** Test any bullet in `##
Established` by asking whether the source's author would recognise it
as something they wrote. If they'd say "that's not quite what I said,"
it is either misworded or it is synthesis in the wrong section.

Specific ways this goes wrong:

- **Hedge removal.** "Some evidence suggests X" → "X". The most common
  and the hardest to catch later.
- **Attribution collapse.** The source quoting someone else's claim
  becomes the source claiming it. Record who said it.
- **Aggregation.** Three weak indications summarised as one confident
  statement. Confidence does not accumulate through paraphrase.
- **Scope creep.** A claim about one instance restated as a general
  rule.

Confidence markers reflect what the *source* supports, not how
plausible the claim feels. A single unreliable source asserting
something forcefully is a `low`-confidence claim.

## Excerpt discipline

Third-party sources are usually copyrighted. The corpus registers them
**by reference and short excerpt** — it does not become a mirror of
them.

- Register the pointer: identifier, locator, and where the material can
  be obtained. That is what the source record is for.
- Quote sparingly, and only where the exact wording is load-bearing —
  a contested claim turning on a specific phrase, a definition, a
  hedge that matters. Keep quotes short, in quotation marks, attributed
  by src id and locator (page, timestamp, section).
- Everything else is distilled into the corpus's own words as sourced
  claims. That is the normal case, and it is also better research
  practice than transcription.
- **Never bulk-copy** a source's text into a dossier or a file under
  `content/`. No pasted chapters, no full transcripts, no
  reconstruct-by-excerpt across several ingestion passes.
- First-party material — the user's own notes, their own recordings,
  documents they hold the rights to — may be committed in full. The
  distinction is rights, not format.

If a source cannot be excerpted at all, register it and distil it; the
claims survive without the text.

## Batch ingestion

Several sources supplied at once are ingested as several sources, run
through the pipeline in sequence. The batch is a convenience for the
user, not a unit in the corpus.

**Each source gets its own registry record and its own Log line, in
every subject it touches.** Never merge a batch into one record ("the
March documents") or one Log entry ("ingested six sources").

Three reasons, all of which bite later:

1. **Corroboration needs distinct ids.** Two sources agreeing is the
   corpus's main confidence signal, and `[src-0044, src-0051]` on one
   claim is what encodes it. A merged record makes two independent
   confirmations look like one, and the recurrence trigger for opening
   new subjects stops working.
2. **Reliability is per-source.** If one source in the batch is later
   discredited, its claims must be identifiable and revisitable
   individually. Under a merged id every claim from the batch is
   contaminated and none can be cleanly separated.
3. **The Log is an audit trail.** "What did this source change?" must
   be answerable per source. Merged lines destroy exactly the
   granularity the append-only Log exists to preserve.

Order matters within a batch when sources conflict. Ingest, let the
conflict land in `## Contested`, and leave it standing — do not resolve
a conflict inside a batch by preferring the source read last, or the
longer one. Resolution is a separate, explicit act recorded in the Log.

A batch may legitimately produce one summary *to the user* at the end.
It never produces one record on disk.
