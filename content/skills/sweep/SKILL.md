---
name: sweep
description: Run a longitudinal pass over research topics that are due for revisit — re-read State of play, check open questions against material that has arrived since, re-check live sources, and record what changed AND what didn't. Triggers on "/sweep", "what's due for review", "revisit stale topics", "corpus health check", "what changed since last time", "sweep the [tag] topics". Writes durable files: advances `last_swept` and appends a `log.md` line in every topic it opens, including no-change passes. Reports structural health findings rather than silently fixing them. Never auto-commits.
---

# /sweep — Longitudinal pass over due topics

Revisit topics whose cadence has elapsed, diff each against its last
known state, and record the result — including the result "no change",
which is the one this skill exists to make sure gets written down. Also
reports structural health findings across the corpus.

Operates on `rasa.module.research` topic folders at
`<research-root>/<topic-slug>/`, plus this domain's `contested.md` and
its corpus-wide `sources/` registry. Read `framework/longitudinal.md`
before changing anything here; this skill is its enforcement surface.

## Behavior contract

- **Always advance `last_swept` and always append a `log.md` line —
  including on no change.** A no-change pass produces exactly as much
  durable record as a pass that rewrote everything. Without it,
  `last_swept` degrades into "date of last *change*" and the corpus can
  no longer distinguish "checked recently, still true" from "abandoned
  two years ago". `## State of play` cannot carry that difference; only
  the frontmatter and the log can.
- **Move `updated:` only when content actually moved.** `last_swept`
  moves every pass; `updated:` moves when the topic changed. Collapsing
  them destroys the distinction above.
- **Never advance `last_swept` for a topic that was not opened, and
  never backdate it.** Topics outside the batch stay due and are
  reported as deferred.
- **Always run against an explicit selection.** All due (default), a
  tag, one slug, or a slug list. Never silently over the whole corpus —
  an unreviewed sweep is worse than no sweep, because it leaves a
  durable false claim that those topics were checked.
- **Only `status: active` is in the due queue.** `open`, `dormant`,
  `concluded`, and `archived` have no clock and are reached only by
  explicit naming.
- **Bound the batch.** Past roughly 15–25 topics, take the most overdue
  and defer the rest. Do not widen the batch to clear the queue; report
  the queue instead.
- **Report health findings; never silently auto-fix them.** Defects are
  surfaced with topic slug and specific defect, banded by severity.
  Mechanical fixes may be offered as a batch for approval — never
  applied unasked, because a structural break is usually a symptom and
  silent repair destroys the evidence that the corpus drifted.
- **Delegate the graph checks to `/xref`.** Dangling `[[slug]]` links,
  back-references, and `related:`-versus-`[[ ]]` disagreement are the
  substrate's job. Run it, fold its output into the report, do not
  re-walk the graph here.
- **Propose decay demotions; don't apply them unilaterally.** Present
  candidates with their evidence and let the user confirm.
- **Do no new research.** A question that became answerable but needs an
  outside pull is flagged for `/investigate` and left open. Twenty
  investigations is not a sweep.
- **Never rewrite or reorder `log.md`.** Append only, under a dated
  heading.
- **Never resolve a `contested.md` entry by picking the more convenient
  source.** If it resolves, it resolves on evidence, migrates to
  `findings.md`, and the resolution goes in `log.md`.
- **Never delete a topic, a log entry, or a source.** Decay is
  expressed as `status` and `cadence`.
- **Never auto-commit.** Edits land in the working tree for review with
  `git diff`.

## Process

1. **Resolve the selection.** Default is all due: `status: active`
   topics where `last_swept + cadence < today`, computed on read from
   frontmatter — never from a stored flag. Accept a tag, a single slug,
   or a slug list instead. Order by overdue depth, most overdue first.
   State the selection and its size before touching anything.
2. **Apply the batch bound.** If the selection exceeds a workable
   batch, take the most overdue and record the remainder as deferred.
   Say so up front — do not quietly truncate.
3. **Run the corpus-wide frontmatter checks.** `cadence:` and
   `last_swept:` presence and validity, `last_swept` in the future,
   `last_swept` older than the newest `log.md` entry, `active` with
   `cadence: none`, `active` with an empty `open-questions.md`, orphan
   `src-NNNN` records. These read cheaply across every topic; run them
   regardless of selection. Collect findings, fix nothing.
4. **Run `/xref`** and hold its dangling-link, back-reference, and
   `related:` asymmetry output for the report.
5. **For each selected topic, run the six-step pass**
   (`framework/longitudinal.md`):
   1. Re-read `## State of play` cold — as a reader, not the author.
   2. Check `open-questions.md` for questions now answerable from
      material that entered the corpus since `last_swept` — other
      topics, newly registered sources, timeline entries. Highest
      yield, zero cost.
   3. Re-check live sources for change. Static sources (a filed PDF, a
      published paper) are not re-fetched.
   4. Diff against last known state: what in `findings.md` still holds,
      what is contradicted, what in `contested.md` resolved or
      hardened, what is new on the timeline.
   5. Record. Rewrite `## State of play` only if the picture moved;
      adjust a finding's `**Confidence:**` only if the evidence moved
      it; move `updated:` only if content moved.
   6. Append the `log.md` line and advance `last_swept`. Both happen
      either way.
6. **Run the body-level health checks over the selection** — unsourced
   `findings.md` claims, `contested.md` entries with only one side
   sourced, a filled `**Resolution:**` with no `log.md` line, oversized
   `## State of play`.
7. **Collect decay candidates.** Three consecutive no-change sweeps
   with nothing in `log.md` between them but the sweep lines → propose
   stepping `cadence` one rung (`7d → 30d → 90d → 365d → none`). A
   topic already at `none` that still finds nothing → propose
   `status: dormant`. Attach the dates as evidence. Any movement resets
   the count.
8. **Emit the report** (shape below). Apply approved demotions and
   approved mechanical fixes, each with its own `log.md` line. Leave
   everything uncommitted.

## Output shape

A sweep report. Derived and disposable — everything load-bearing in it
is reconstructible from the topic folders, since each swept topic
carries its own `log.md` line.

```markdown
# Sweep — 2026-09-14
Selection: all due (batch bound 20)
Due 27 · swept 20 · changed 4 · unchanged 16 · flagged 6 · deferred 7

## Moved
- some-topic — two findings moved to contested.md after src-0031;
  F3 confidence medium → low.
- other-topic — one open question closed from material registered for
  third-topic; State of play rewritten.
- third-topic — live source src-0018 changed; new timeline entry
  2026-09-02.
- fourth-topic — concluded as a dead end, reason in log.md.

## Health findings
Breaks the clock
- fifth-topic — `last_swept:` missing.
- sixth-topic — `cadence: 45d` is not a ladder value.
- seventh-topic — `last_swept: 2026-09-14` predates newest log entry
  (2026-09-15).

Breaks a discipline rule
- eighth-topic — findings.md F4 "…" carries no [S#].
- ninth-topic — contested.md C2: position B has no source.
- tenth-topic — contested.md C1 Resolution filled, no log.md line.

Discipline drift
- eleventh-topic — State of play at 9 paragraphs; wants splitting.
- twelfth-topic — status active, open-questions.md empty.
- thirteenth-topic — status active, cadence: none. Still deliberate?
- src-0044 — registered, cited by no topic.

From /xref
- fourteenth-topic — `[[fifteenth-topic]]` dangles; no such topic.
- sixteenth-topic ↔ seventeenth-topic — asymmetric `related:`.

## Decay candidates (not applied)
- eighteenth-topic — 3 no-change passes (2026-07-19, 2026-08-16,
  2026-09-14). Propose cadence 30d → 90d.

## Deferred (still due)
7 topics. Most overdue: nineteenth-topic (+41d), twentieth-topic
(+22d), twenty-first-topic (+9d).
```

The corresponding `log.md` entry in an unchanged topic:

```markdown
## 2026-09-14

- /sweep: no change. Rechecked src-0007, src-0031 (both unmoved);
  3 open questions still open; no findings movement; F2 held at
  medium.
```

## What NOT to do

- **Don't skip the log line when nothing changed.** This is the single
  most damaging shortcut available in this skill. It looks like noise
  reduction and it destroys the corpus's ability to tell verified from
  abandoned.
- **Don't write a bare "no change".** Name what was rechecked and what
  held, so a later reader can tell a real pass from a glance.
- **Don't manufacture movement to justify the pass.** Most passes over
  a well-tended corpus find nothing. Inventing a State of play rewrite
  to show productivity is the exact failure the calibration tenet
  names.
- **Don't store dueness.** No `stale:`, no `due:`, no overdue counter
  written to frontmatter. Compute it on read, every time.
- **Don't sweep everything because the selection was vague.** Ask, or
  default to all-due with a batch bound. Never assume "the whole
  corpus".
- **Don't widen the batch to empty the due queue.** A large standing
  queue is a cadence problem; report it as one.
- **Don't demote topics to shrink the queue.** Demotion follows the
  no-change evidence, nothing else.
- **Don't auto-create missing topics to resolve dangling links.** The
  dangle is the finding.
- **Don't collapse a contest.** Both positions stay, with provenance,
  until evidence settles it.
- **Don't start investigating.** Flag the newly-tractable question and
  move to the next topic.
- **Don't touch `open`, `dormant`, `concluded`, or `archived` topics on
  a due sweep** unless they were named in the selection.
- **Don't reimplement `/xref`.** Two implementations of one check
  drift.
- **Don't auto-commit.**

## Done when

Every topic in the selection has been opened, has an appended `log.md`
line describing what changed or explicitly recording that nothing did,
and has `last_swept` set to today. `updated:` moved only where content
moved. Topics outside the batch are untouched and reported as deferred.
Health findings and decay candidates are reported with topic slugs and
evidence, unfixed unless the user approved them. The working tree holds
the edits, uncommitted.
