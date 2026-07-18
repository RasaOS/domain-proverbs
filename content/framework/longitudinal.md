# The longitudinal mode

The mode that makes this a research instrument rather than an archive,
and the largest single thing this domain adds. `rasa.module.research`
gives a topic a **lifecycle**; it gives it nothing **dated**.
`status: active` says a topic is live — never when it was last actually
looked at. So a topic worked hard through 2024 and a topic abandoned in
2024 are, in 2026, the same file with the same status. This chapter
closes that gap.

Read `topic-overlay.md` first, and the module's `research-rules.md`
before that. Everything here reads and writes the substrate's topic
folder at `<research-root>/<topic-slug>/`; nothing here defines a new
one. The research root comes from the seam
(`.claude/research-canon.md`), never hardcoded.

---

## The clock

Two frontmatter fields on the topic `README.md`, and only two:

```yaml
cadence: 30d             # 7d | 30d | 90d | 365d | none
last_swept: 2026-07-18   # date of the last longitudinal pass
```

A topic is **due** when `last_swept + cadence < today`. That is the
entire definition. There is no `stale:` field, no `due:` field, no
`overdue:` count. Dueness is **computed on read, never stored**.

### Why a stored flag rots

A stored derived value creates two truths — the value and the inputs it
came from — and they diverge the first time an input moves without the
writer running.

- A sweep clears a topic, someone forgets to reset `stale: true`, and
  the topic is permanently overdue. Nothing detects it, because a wrong
  flag is byte-identical to a right one.
- Someone edits `cadence: 90d` to `7d`. Every stored flag in the corpus
  is now wrong, and stays wrong until something walks the whole tree.
- A flag flips on every pass, in the one file that is supposed to be
  stable enough to read at a glance and cheap to diff.

The computation is one date comparison against frontmatter that has
already been read to find the topic at all. Storing it buys nothing and
costs a class of silent error the rest of this chapter is built to
avoid.

### `last_swept` is not `updated:`

The substrate already carries `updated:`. The two fields answer
different questions and must not be collapsed:

- **`updated:`** — when the topic's *content* last moved.
- **`last_swept:`** — when someone last *looked*, whether or not
  anything moved.

A pass that changes nothing advances `last_swept` and leaves `updated:`
exactly where it was. That difference is the no-change rule (below)
expressed in frontmatter, and it is why `updated:` alone could not have
carried this mode.

## The clock against the lifecycle

The substrate's lifecycle is `open → active ⇄ dormant → concluded →
archived`. Only one of those five states has a clock.

| `status:` | Clock | What the sweep does with it |
|---|---|---|
| `open` | none | Never in the due queue. Pre-investigation. |
| `active` | **the only one** | Accrues cadence pressure; *is* the due queue. |
| `dormant` | none | Explicit selection only. Decay's destination. |
| `concluded` | none | Nothing outstanding to re-check. |
| `archived` | none | Never reached except by being named outright. |

**`open`** is registered, scoped, and not yet worked — a placeholder
with a question and no evidence under it. There is nothing to re-check,
so there is no clock. An `open` topic that has sat unstarted for months
is a real problem, but it is a *backlog* problem: it belongs to
`INDEX.md` and whoever grooms it, not to the due queue. Putting `open`
topics on a cadence fills every sweep with topics that have nothing to
sweep, and the queue stops meaning anything.

**`active`** is the whole due queue. This is the pressure valve that
keeps the queue proportional to actual attention rather than to topic
count — a corpus of 400 topics with 30 active has a 30-topic queue.

**`dormant`** was active and was set down. The question is still live;
nobody is pursuing it. No clock, which is the point of the state, and
it is where this mode's decay path sends topics that stopped moving.
Reactivation runs the other way and is also not on a clock: new
material routed in, or an explicit decision, sets it back to `active`
with a real cadence.

**`concluded`** has an answer the project accepts and, once promoted,
an answer living somewhere durable. Nothing outstanding, so no clock.
If a conclusion is later thrown into doubt, the honest move is to set
the topic back to `active` with a cadence and a `log.md` line saying
why — not to sweep every concluded topic on a timer against the chance
one of them broke.

**`archived`** is closed and set aside. It never enters the due queue
and is only ever touched by naming it explicitly.

One consequence worth stating: because `status` decides whether a clock
exists at all, **a mislabelled status is a clock error, not a
bookkeeping one**. The substrate already requires status to agree
between frontmatter and the `INDEX.md` row; this mode inherits that
requirement and makes it load-bearing. A topic quietly left `dormant`
while being worked is a topic nobody is checking.

## `cadence: none`

`cadence: none` means an **active topic deliberately off the clock** —
a live thread whose sources move only on an unpredictable external
event, where any fixed interval would generate pure noise. It is a
legitimate setting. It never appears in the due queue and is reached
only by explicit selection or by new material being routed into it.

It is also, used carelessly, exactly how a topic goes unwatched for two
years while still reading as `active`. So the health checks flag every
`active` topic carrying `cadence: none`, every run, forever. The flag
is not an error — it is a standing question: *is this still
deliberate?* An answer of "yes" costs one line in the report and
nothing on disk.

## Cadence is not priority

The substrate has no importance ranking and this domain does not add
one; cadence carries all the urgency there is. Setting `7d` on
something that does not actually change weekly is not a way to mark it
important — it is a way to manufacture a due queue full of topics with
nothing to report, which trains whoever reads the report to stop
reading it.

**Overdue depth** — `today - (last_swept + cadence)` — is derived the
same way and is the correct ordering key for the queue. Most overdue
first, always.

## A sweep runs over a bounded selection

A sweep runs against an explicit **selection**, never silently over
everything. Valid selections:

- **all due** — the default; every `active` topic past its cadence
- **a tag** — every topic carrying `tags: [x]`, due or not
- **one topic** — by slug
- **an explicit slug list**
- **due within N days** — lookahead, for planning rather than sweeping

The reason is capacity, not compute. A sweep that touches 400 topics
produces a diff nobody reads — and **an unreviewed sweep is worse than
no sweep**, because `last_swept` advanced on all 400 and the corpus now
asserts they were checked. That assertion is false, it is durable, and
nothing downstream can tell it from a true one. The one thing the
longitudinal record must never do is lie about having looked.

So the selection is bounded to what can actually be reviewed in one
sitting. A working batch is roughly 15–25 topics; past that, take the
most overdue and leave the rest due. **Do not widen the batch to clear
the queue.** A persistently large due queue is a cadence problem, not a
sweep problem, and the fix is demotion and longer intervals (see
*Decay*), never a bigger pass.

## The per-topic pass

Six steps, in this order. The order matters: the cheap yields come
first, and the expensive step is bounded by what the earlier steps
found.

1. **Re-read `## State of play` cold.** As a reader, not as the author
   who wrote it. What no longer parses, what you would now say
   differently, what is asserted more strongly than the evidence under
   it supports.
2. **Check `open-questions.md` for questions now answerable.** Not by
   new research — by material that entered the corpus since
   `last_swept`: other topics, sources registered for something else,
   timeline entries. This is the highest-yield step in the mode and it
   costs nothing but reading. One source usually bears on several
   topics, and the ones it touched *indirectly* are exactly the ones
   nobody noticed at ingest time. The substrate's three resolution
   paths apply unchanged: answered graduates to `findings.md`, too-big
   spawns its own topic, dropped is struck through with a reason.
3. **Re-check live sources for change.** Only sources the corpus-wide
   registry marks as live or mutable (`provenance.md`). A published
   paper or a filed PDF is not re-fetched — its content cannot move,
   only the reading of it can.
4. **Diff against last known state.** What in `findings.md` still
   holds, what has been contradicted, what in `contested.md` resolved
   or hardened, what is new on the timeline axis. `log.md` is the
   reference point — it is what makes a diff possible six months later.
5. **Record what changed *and* what didn't.** Rewrite `## State of
   play` only if the picture moved. Adjust a finding's
   `**Confidence:**` only if the evidence moved it. Move `updated:`
   only if content moved.
6. **Append the `log.md` line and advance `last_swept`.** Both happen
   **whether or not** anything in step 5 did. This is not the tail of
   the pass; it is the pass's output.

**The sweep conducts no new research.** If step 2 surfaces a question
that is now answerable but only by pulling from outside, that is
`/investigate`'s job — the sweep records the question as newly
tractable and moves on. Without this boundary a twenty-topic sweep
becomes twenty investigations, finishes none of them, and leaves the
other nineteen topics carrying a stale `last_swept`.

## "No change" is a result, and it is recorded

This is the load-bearing rule of the mode.

**`last_swept` advances and `log.md` gets a line even when nothing
changed.** A no-change pass is a successful pass, and it produces
exactly as much durable record as a pass that rewrote everything.

The argument is structural, not stylistic. Consider two topics whose
`## State of play` sections were both last written in 2024. Read today,
they are identical artifacts. One of them was checked six weeks ago and
is still true; nobody has opened the other since. **Nothing in `##
State of play` can carry that difference** — it holds the *picture*,
not the date the picture was last verified. It is a synthesis of
evidence; a statement about attention is not the kind of thing it can
contain, and stapling one on ("still accurate as of…") turns the
bounded synthesis layer into a second log, which is the failure the
whole two-layer split exists to prevent.

Frontmatter and `log.md` are where that difference lives. If no-change
passes go unrecorded, `last_swept` silently degrades into "date of last
*change*", the two cases collapse, and every unchanged topic in the
corpus becomes indistinguishable from an abandoned one. At that point
the corpus is an archive with a timestamp field — precisely what this
mode exists to prevent.

The no-change line says what was actually checked:

```markdown
## 2026-08-02

- /sweep: no change. Rechecked src-0007, src-0031 (both unmoved);
  3 open questions still open; no findings movement; F2 held at
  medium.
```

Not a bare "no change" — a later reader needs to tell a real pass from
a glance. Name the sources rechecked and the state that held.

Two corollaries, both about honesty under pressure:

- **Do not manufacture movement to justify the pass.** The urge to
  produce a finding is the main threat to a sweep's integrity, and it
  is the same failure the calibration tenet names: an instrument that
  invents motion to appear productive is worthless. Most passes over a
  well-tended corpus find nothing.
- **Never advance `last_swept` for a topic that was not opened, and
  never backdate it.** A batch that ran out of budget leaves the rest
  due. Deferred is a fine outcome; falsely swept is not.

## Health checks

Beyond the per-topic pass, a sweep runs structural checks. Frontmatter
reads cheaply across the whole corpus, so frontmatter-level checks run
corpus-wide even when the selection is narrow; body-level checks run
over the selection only.

**The graph checks are not reimplemented here.** Dangling `[[slug]]`
links, back-reference discovery, and `related:`-versus-`[[ ]]`
disagreement are what the substrate's `/xref` already computes. The
sweep **runs `/xref` and folds its output into the report** rather than
walking the graph itself. Two implementations of the same check drift,
and the one that drifts is always the copy nobody owns.

Findings, in severity bands:

**Breaks the clock** — the mode cannot function on this topic

- `cadence:` or `last_swept:` missing, on a topic of any status
- `cadence:` not one of `7d | 30d | 90d | 365d | none`
- `last_swept:` unparseable, or dated in the future
- `last_swept` earlier than the newest `log.md` entry — frontmatter and
  record disagree about when the topic was last touched
- a `[src-NNNN]` cited in a topic with no record in
  `<research-root>/sources/`

**Breaks a discipline rule** — a claim is standing without warrant

- a claim in `findings.md` with no `[S#]` (or `[src-NNNN]`) evidence.
  The substrate already says a claim without evidence is an open
  question, not a finding; this is that rule, enforced
- a `contested.md` entry with only one side sourced. A contest with one
  sourced position and one asserted position is not a contest — it is
  an unsourced claim with a decorative opponent
- a `contested.md` entry with `**Resolution:**` filled in but no
  corresponding `log.md` line recording the resolution

**Discipline drift** — the structure is decaying

- `## State of play` grown past the length discipline. This is the
  scaling claim failing in a specific place, and the fix is structural
  — split into linked topics — not editing
- `status: active` with an empty `open-questions.md`. Mislabelled: it
  either has questions or it is `dormant`
- `status: active` with `cadence: none` — off the clock; confirm it is
  deliberate
- a `src-NNNN` record in the corpus-wide registry cited by no topic —
  an orphan source
- asymmetric `related:` links — **reported from `/xref`'s output, not
  recomputed**

**The sweep reports; it does not silently fix.** Two reasons. First, a
structural break is usually a symptom: a dangling link means a topic
was renamed, or was planned and never opened, and auto-creating a stub
hides the event that actually needs attention. Second, silent repair
destroys the evidence that the corpus drifted at all — and a
self-healing corpus that no longer knows it was broken cannot tell you
its method is failing. Mechanical fixes may be *offered* as a batch for
approval. They are never applied unasked.

## Decay

A topic swept repeatedly with no movement should be demoted, not left
generating noise. The heuristic:

> **Three consecutive no-change sweeps** — `log.md` holding nothing
> between them but the sweep lines themselves: no `findings.md`
> movement, no open question opened, closed, or dropped, no
> `contested.md` change, no `## State of play` rewrite — and `cadence`
> steps **one rung** longer. Any movement at all resets the count to
> zero.

The ladder: `7d → 30d → 90d → 365d → none`. One rung per demotion. A
topic that goes quiet is not necessarily dead, and a single jump from
`7d` to `none` throws away the information those three passes produced.

`none` is the last rung; cadence does not step further. A topic there
has left the due queue, and the health check flagging `active` +
`cadence: none` is what keeps it visible. The next explicit pass over
it that *still* finds nothing proposes `status: dormant`, which is
where the ladder ends. Dormant is the honest label for a live question
nobody is pursuing.

The demotion is a `log.md` line like anything else, and it carries its
evidence:

```markdown
## 2026-09-14

- /sweep: cadence 30d → 90d. Three no-change passes (2026-07-19,
  2026-08-16, 2026-09-14); no findings or contested movement in that
  window.
```

Other decay signals, each with a different response:

- **A finding's confidence never moves off `low` after several
  passes.** Not a demotion case. Either the sources do not exist or the
  question is malformed — reframe the open questions, or conclude the
  topic as a dead end with the reason recorded. Dead ends are findings.
- **Open questions unchanged across many passes.** They are not
  actually answerable as stated. Rewrite them into questions that could
  be answered, or drop them with a struck-through reason.
- **A year of `log.md` entries that are all sweep lines.** That is a
  dormant topic wearing an active label.

Two things demotion is not. It is **not `archived`** — archiving is
closure, a deliberate act with a reason; demotion is an observation
that a live question went quiet. And it is **not a way to clear a large
due queue**: demoting topics because the batch is uncomfortable is
queue-fitting, and it silently converts a capacity problem into a false
claim about what is being watched.

## The sweep report

A sweep emits one report. Contents:

- **Header** — date, the selection expression that was run, the batch
  bound if one applied.
- **Counts** — due, swept, changed, unchanged, flagged, deferred (due
  but outside the batch).
- **Moved** — the topics that changed, one line each, saying what
  moved. This is the part a reader actually reads; keep it to the
  change, not the topic's summary.
- **Health findings** — grouped by the severity bands above, each with
  the topic slug and the specific defect. Not a count; the defects.
- **Decay candidates** — with the evidence (the dates of the no-change
  passes), proposed but not applied.
- **Deferred queue** — how many remain due and the most overdue few, so
  the next pass has a starting point.

The report is **derived and disposable**. Everything load-bearing in it
is reconstructible from the topic folders, because each swept topic
carries its own `log.md` line — which is the point of the append-only
layer. Keeping a separate report ledger would create a second copy of
facts that already live in the topics, and the two would diverge. A
deployment that wants report history can write them somewhere; nothing
in the method depends on it.

## Composing with a schedule

The mode is defined by the due computation, not by any scheduler.
Anything that can invoke a command on an interval is sufficient: cron,
a CI job, a scheduled agent, `rasa.module.jobs` if it is mounted, or a
person who remembers on Sundays. The rules for wiring one up:

- **Cadence lives in the topic, never in the scheduler.** The scheduler
  asks "what is due"; it does not carry per-topic intervals. Two
  sources of truth for one fact diverge, and the copy outside the
  corpus is the one that rots unseen.
- **A missed run is not a lost run.** Nothing is scheduled *per topic*,
  so a skipped invocation just leaves topics due and slightly more
  overdue. The queue carries. There is no catch-up state to reconcile
  and no scheduler-side bookkeeping at all.
- **Running twice in a day is harmless.** The second run computes a due
  set that no longer contains what the first swept, because
  `last_swept` is now today.
- **A scheduled invocation carries a selection and a batch bound like
  any other.** Never let a scheduler run an unbounded sweep — that is
  precisely the 400-topic diff, arriving on a timer.
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
- **No deletion or compaction.** Not of topics, not of `log.md`
  entries, not of sources. Decay is expressed as `status` and
  `cadence`.
- **No silent structural repair.** Findings are reported.
- **No graph walking.** `/xref` owns the link layers; the sweep
  consumes its output.
- **No auto-commit.** The sweep writes to the working tree; the diff is
  the user's to review.
- **No priority inference.** The sweep does not decide what matters. It
  reports what is due, what moved, and what is broken.

Nothing here makes a topic unreadable without this domain. Strip the
overlay and `cadence:`/`last_swept:` become two inert frontmatter keys
on a perfectly valid `module.research` topic — the corpus simply stops
being swept.
