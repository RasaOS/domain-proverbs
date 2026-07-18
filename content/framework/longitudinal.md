# The longitudinal mode

The mode that makes this a research instrument rather than an archive.
Active research fills a subject once; longitudinal sweeps are what keep
the corpus honest about *when* each picture was last checked. Read
`subject-model.md` first — everything here reads and writes the Subject
defined there.

---

## Cadence and staleness

Two frontmatter fields carry the whole clock:

```yaml
last_swept: 2026-07-18   # date of the last longitudinal pass
cadence: 30d             # 7d | 30d | 90d | 365d | none
```

A subject is **due** when `last_swept + cadence < today`. That is the
entire definition. There is no `stale:` field and no `due:` field,
because a stored staleness flag drifts the moment a sweep runs and
someone forgets to clear it. Staleness is **computed on read, never
stored**.

**Only `status: active` accrues cadence pressure.** Dormant subjects
are real and kept but not being worked — they have no clock. Closed
subjects have no clock. Speculative subjects are opened on a hunch and
get their first pass from `/investigate`, not from the sweep clock; a
speculative subject worth putting on a clock should be promoted to
active first. This is the pressure valve that keeps the due queue
proportional to actual attention rather than to subject count.

`cadence: none` means an active subject deliberately off the clock —
a live thread whose sources only move on an unpredictable external
event. It never appears in the due queue and is reached only by
explicit selection or by `/ingest` routing new material into it. Used
carelessly, `cadence: none` is how a subject goes quietly unwatched
for two years, so the sweep flags active subjects carrying it.

**Cadence is not priority.** The subject model deliberately has no
importance ranking (`subject-model.md`, "What this model deliberately
does not have"); cadence carries all the urgency there is. Setting
`7d` on something that does not actually change weekly is not a way to
mark it important — it is a way to generate noise.

**Overdue depth** — `today - (last_swept + cadence)` — is derived the
same way and is the correct ordering key for the due queue. Most
overdue first, always.

## A sweep is over a selection

A sweep runs against an explicit **selection**, never silently over
everything. Valid selections:

- **all due** — the default; every active subject past its cadence
- **a tag** — every subject carrying `tags: [x]`, due or not
- **one subject** — by id
- **an explicit id list**
- **due within N days** — lookahead, for planning rather than sweeping

The reason is capacity, not compute. A sweep that touches 400 dossiers
produces a diff nobody reads, and an unreviewed sweep is **worse than
no sweep**: `last_swept` advanced, so the corpus now asserts those 400
subjects were checked. That assertion is false and it is durable. The
one thing the longitudinal record must never do is lie about having
looked.

So the selection is bounded to what can actually be reviewed in one
sitting. A working batch is roughly 15–25 subjects; past that, sweep
the most overdue first and leave the rest due. **Do not widen the
batch to clear the queue.** A persistently large due queue is a
cadence problem, not a sweep problem — the fix is demotion and longer
intervals (see *Decay signals*), never a bigger pass.

## The per-subject pass

Five steps, in this order. The order matters: the cheap yields come
first, and the expensive step is bounded by what the earlier steps
found.

1. **Re-read Standing cold.** As a reader, not as the author who wrote
   it. What no longer parses, what you would now say differently, what
   is asserted more strongly than the evidence under it supports.
2. **Check open questions for ones now answerable.** Not by new
   research — by material that has entered the corpus since
   `last_swept`: other subjects, sources ingested for something else,
   timeline entries. This is the highest-yield step in the whole mode
   and it costs nothing but reading. One source usually updates
   several subjects, and the ones it updated indirectly are exactly
   the ones nobody noticed at ingest time.
3. **Re-check live sources for change.** Only sources the registry
   marks as live/mutable (`provenance.md`). A published paper or a
   filed PDF does not get re-fetched — its content cannot move, only
   the reading of it can.
4. **Diff against last known state.** What in Established still holds,
   what has been contradicted, what Contested has resolved or
   hardened, what is new in Timeline. The Log is the reference point:
   it is what makes a diff possible six months later.
5. **Record.** Rewrite Standing if the picture moved. Adjust
   `confidence` if the evidence moved it. Append the Log line.
   Advance `last_swept`. The last two happen **whether or not**
   anything else did.

**The sweep does not conduct new research.** If step 2 surfaces a
question that is now answerable but only by pulling from outside, that
is `/investigate`'s job — the sweep records the question as newly
tractable and moves on. Without this boundary a twenty-subject sweep
becomes twenty investigations and finishes none of them, and the other
nineteen subjects silently keep their stale `last_swept`.

## "No change" is a result, and it is recorded

This is the load-bearing rule of the longitudinal mode.

**`last_swept` advances and the Log gets a line even when nothing
changed.** A no-change pass is a successful pass, and it produces
exactly as much durable record as a pass that rewrote everything.

The reason is the entire value proposition of a longitudinal corpus.
Two subjects whose Standing sections were both last *written* in 2024
read identically today. Only the record separates them:

- one was checked six weeks ago and is still true
- nobody has looked at the other in two years

Standing cannot carry that difference — it is a synthesis of evidence,
not a statement about attention. Frontmatter and the Log carry it. If
no-change passes go unrecorded, `last_swept` becomes "date of last
*change*", the two cases collapse, and every unchanged subject in the
corpus becomes indistinguishable from an abandoned one. At that point
the corpus is an archive with a timestamp field, which is what this
mode exists to prevent.

The no-change line says what was actually checked:

```markdown
- 2026-08-02 — /sweep: no change. Rechecked src-0007, src-0031;
  3 open questions still open; confidence held at medium.
```

Not a bare "no change" — a later reader needs to tell a real pass from
a glance. Name the sources rechecked and the state that held.

Two corollaries, both about honesty under pressure:

- **Do not manufacture movement to justify the pass.** The urge to
  produce a finding is the main threat to a sweep's integrity, and it
  is the same failure tenet 5 names: an instrument that invents motion
  to appear productive is worthless. Most passes over a well-tended
  corpus should find nothing.
- **Never advance `last_swept` for a subject that was not opened, and
  never backdate it.** A batch that ran out of budget leaves the rest
  due. Deferred is a fine outcome; falsely swept is not.

## Health checks

Beyond the per-subject pass, a sweep runs structural checks. The
frontmatter and link graph can be read across the whole corpus
cheaply, so those checks run corpus-wide even when the sweep selection
is narrow; body-level checks run over the selection only.

Findings, in rough severity order:

**Breaks the model**
- required frontmatter missing or malformed (every field except
  `tags` and `superseded_by` is required)
- `links:` entries pointing at ids with no file — dangling
- `sources:` or inline `[src-...]` refs not present in the registry
- `superseded_by:` pointing at a missing subject, or at itself
- Log entries out of chronological order, or dated in the future
- `last_swept` earlier than the newest Log entry — frontmatter and
  record disagree about when this subject was last touched

**Breaks a tenet**
- a claim in `## Established` with no source ref (tenet 2 — there is no
  fourth place for an unsourced assertion to hide)
- a `closed` subject with no reason recorded in the Log (tenet 4 — a
  dead end that isn't written down gets re-explored)
- asymmetric `links:` — A links B, B does not link A. The list is
  symmetric by convention, so asymmetry means one side of an edit
  never happened

**Discipline drift**
- `## Standing` grown past the length discipline — a few paragraphs is
  the ceiling. This is the scaling claim failing in a specific place,
  and the fix is structural (split into linked subjects), not editing
- `status: active` with zero open questions — mislabeled; it either
  has questions or it is dormant
- `status: active` with `cadence: none` — off the clock; confirm it is
  deliberate
- orphan sources — registered in the source registry, cited by no
  subject

**The sweep reports; it does not silently fix.** Two reasons. First, a
structural break is usually a symptom: a dangling link means a subject
was renamed, or was planned and never opened, and auto-creating a stub
hides the event that actually needs attention. Second, silent repair
destroys the evidence that the corpus drifted at all — and a
self-healing corpus that no longer knows it was broken cannot tell you
its method is failing. Mechanical fixes may be *offered* as a batch
for approval. They are never applied unasked.

## Decay signals

A subject swept repeatedly with no movement should be demoted, not
left generating noise. The heuristic:

> **Three consecutive sweeps with no change** — no Standing rewrite,
> no open question opened or closed, no Established or Contested
> movement, nothing in the Log but the sweep lines themselves — and
> the subject is demoted to `status: dormant` with `cadence` stepped
> one interval longer.

The ladder: `7d → 30d → 90d → 365d → none`. Demote one step at a time;
a subject that goes quiet is not necessarily dead, and a single jump
from `7d` to `none` throws away the information the three passes
produced.

The demotion is a Log line like anything else, and it carries its
evidence:

```markdown
- 2026-09-14 — /sweep: demoted to dormant, cadence 30d → 90d. Three
  no-change passes (2026-07-19, 2026-08-16, 2026-09-14).
```

Other decay signals, each with a different response:

- **`confidence` never moves off `low` after several passes.** Not a
  demotion case. Either the sources do not exist or the question is
  malformed — reframe the open questions, or close the subject as a
  dead end with the reason recorded (tenet 4).
- **Open questions unchanged across many passes.** They are not
  actually answerable as stated. Rewrite them into questions that
  could be answered, or drop them and say why in the Log.
- **A year of Log entries that are all sweep lines.** That is an
  archive entry wearing an active label. Dormant is the honest one.

Reactivation runs the other way and is not on a clock: `/ingest`
routing new material into a dormant subject is the wake-up path. Set
it back to `active` with a real cadence when there is something to
work.

Two things demotion is not. It is **not deletion** — nothing is ever
deleted, per tenet 4. And it is **not a way to clear a large due
queue**: demoting subjects because the batch is uncomfortable is
queue-fitting, and it silently converts a capacity problem into a
false claim about what is being watched.

## The sweep report

A sweep emits one report. Contents:

- **Header** — date, the selection expression that was run, batch
  bound if one applied.
- **Counts** — due, swept, changed, unchanged, flagged, deferred (due
  but outside the batch).
- **Moved** — the subjects that changed, one line each, saying what
  moved. This is the part a reader actually reads; keep it to the
  change, not the subject's summary.
- **Health findings** — grouped by the severity bands above, each with
  the subject id and the specific defect. Not a count; the defects.
- **Decay candidates** — with the evidence (the dates of the
  no-change passes), proposed but not applied.
- **Deferred queue** — how many remain due and the most overdue few,
  so the next pass has a starting point.

The report is **derived and disposable**. Everything load-bearing in
it is reconstructible from the subject files, because each swept
subject carries its own Log line — which is the point of the
append-only layer. Keeping a separate report ledger would create a
second copy of facts that already live in the subjects, and the two
would diverge. A fork that wants report history can write them
somewhere; nothing in the method depends on it.

## Composing with a schedule

The mode is defined by the due computation, not by any scheduler.
Anything that can invoke a command on an interval is sufficient: cron,
a CI job, a scheduled agent, or a person who remembers on Sundays. The
rules for wiring one up:

- **Cadence lives in the subject, never in the scheduler.** The
  scheduler asks "what is due"; it does not carry per-subject
  intervals. Two sources of truth for the same fact will diverge, and
  the copy outside the corpus is the one that rots unseen.
- **A missed run is not a lost run.** Nothing is scheduled *per
  subject*, so a skipped invocation just leaves subjects due and
  slightly more overdue. The queue carries. There is no catch-up
  state to reconcile and no scheduler-side bookkeeping at all.
- **Running twice in a day is harmless.** The second run computes a
  due set that no longer contains what the first run swept, because
  `last_swept` is now today.
- **A scheduled invocation carries a selection and a batch bound like
  any other.** Never let a scheduler run an unbounded sweep — that is
  precisely the 400-dossier diff, arriving on a timer.
- **Unread scheduled reports mean the cadences are wrong.** If output
  piles up unlooked-at, the corpus is claiming more attention than it
  gets. Fix it with demotions and longer intervals, not by scheduling
  less often — the interval is not where the problem is.

A weekly invocation is a reasonable default for a corpus with mixed
cadences: it is finer-grained than every interval except `7d`, so
nothing overshoots its cadence by much.

## What this mode deliberately does not do

- **No new research.** That is `/investigate`. The sweep reads what is
  already here and re-checks what it already knows about.
- **No deletion or compaction.** Not of subjects, not of Log entries,
  not of sources. Decay is expressed as `status` and `cadence`.
- **No silent structural repair.** Findings are reported. See above.
- **No auto-commit.** The sweep writes to the working tree; the diff
  is the user's to review.
- **No priority inference.** The sweep does not decide what matters.
  It reports what is due, what moved, and what is broken.
