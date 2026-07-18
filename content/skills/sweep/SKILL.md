---
name: sweep
description: Run a longitudinal pass over subjects that are due for revisit — re-read Standing, check open questions against material that has arrived since, re-check live sources, record what changed AND what didn't. Triggered by "/sweep", "what's due for review", "revisit stale subjects", "corpus health check", "what changed since last time", "sweep the [tag] subjects". Writes durable files: advances `last_swept` and appends a Log line in every subject it opens, including no-change passes. Reports structural health findings rather than silently fixing them. Never auto-commits.
---

# /sweep — Longitudinal pass over due subjects

Revisit subjects whose cadence has elapsed, diff them against their
last known state, and record the result — including the result "no
change", which is the one this skill exists to make sure gets written
down. Also reports structural health findings across the corpus.

Read `framework/longitudinal.md` before changing anything here; this
skill is its enforcement surface.

## Behavior contract

- **Always advance `last_swept` and always write a Log line — including
  on no change.** A no-change pass produces exactly as much durable
  record as a pass that rewrote everything. This is not optional and it
  is not a nicety: without it, `last_swept` silently degrades into
  "date of last change" and the corpus can no longer distinguish
  "checked recently, still true" from "abandoned two years ago".
- **Never advance `last_swept` for a subject that was not opened, and
  never backdate it.** Subjects that fall outside the batch stay due
  and are reported as deferred.
- **Always run against an explicit selection.** All due (default), a
  tag, one subject, or an id list. Never silently over the whole
  corpus — an unreviewed sweep is worse than no sweep, because it
  leaves a durable false claim that those subjects were checked.
- **Bound the batch.** Past roughly 15–25 subjects, take the most
  overdue and defer the rest. Do not widen the batch to clear the
  queue; report the queue instead.
- **Report health findings; do not silently auto-fix them.** Dangling
  links, missing frontmatter, unsourced Established claims and the rest
  are surfaced with subject id and defect. Mechanical fixes may be
  offered as a batch for approval — never applied unasked, because a
  structural break is usually a symptom and silent repair destroys the
  evidence that the corpus drifted.
- **Propose decay demotions; don't apply them unilaterally.** Present
  the candidates with their evidence and let the user confirm.
- **Do no new research.** A question that became answerable but needs
  an outside pull is flagged for `/investigate` and left open. Twenty
  investigations is not a sweep.
- **Never rewrite or reorder the Log.** Append only, per the subject
  model.
- **Never delete a subject, a Log entry, or a source.** Decay is
  expressed as `status` and `cadence`.
- **Never auto-commit.** Edits land in the working tree for review with
  `git diff`.

## Process

1. **Resolve the selection.** Default is all due: active subjects where
   `last_swept + cadence < today`. Accept a tag, a single id, or an id
   list instead. Compute overdue depth and order most-overdue first.
   State the selection and its size before touching anything.
2. **Apply the batch bound.** If the selection exceeds a workable
   batch, take the most overdue and record the remainder as deferred.
   Say so up front — do not quietly truncate.
3. **Run the corpus-wide cheap checks.** Frontmatter completeness and
   the link graph read cheaply across every subject; run those
   regardless of selection. Collect findings, fix nothing.
4. **For each selected subject, run the five-step pass**
   (`framework/longitudinal.md`):
   1. Re-read `## Standing` cold — as a reader, not the author.
   2. Check `## Open questions` for ones now answerable from material
      that entered the corpus since `last_swept` — other subjects, new
      sources, timeline entries. Highest yield, zero cost.
   3. Re-check live sources for change. Static sources (a filed PDF, a
      published paper) are not re-fetched.
   4. Diff against last known state: what in Established still holds,
      what is contradicted, what Contested resolved, what is new in
      Timeline.
   5. Record. Rewrite Standing only if the picture moved; adjust
      `confidence` only if the evidence moved it; append the Log line;
      advance `last_swept`. The last two happen either way.
5. **Run the body-level health checks over the selection** — unsourced
   Established claims, oversized Standing, active-with-no-open-questions,
   closed-with-no-reason, Log ordering, `last_swept` older than the
   newest Log entry.
6. **Collect decay candidates.** Three consecutive no-change passes with
   no Log movement beyond the sweep lines → propose demotion to
   `dormant` with cadence stepped one interval longer
   (`7d → 30d → 90d → 365d → none`). Attach the dates as evidence.
7. **Emit the report** (shape below). Apply approved demotions and
   approved mechanical fixes, each as its own Log line. Leave
   everything uncommitted.

## Output shape

A sweep report. Derived and disposable — everything load-bearing in it
is reconstructible from the subject files, since each swept subject
carries its own Log line.

```markdown
# Sweep — 2026-09-14
Selection: all due (batch bound 20)
Due 27 · swept 20 · changed 4 · unchanged 16 · flagged 6 · deferred 7

## Moved
- some-subject — two Established claims demoted to Contested after
  src-0031; confidence medium → low.
- other-subject — one open question closed from material ingested for
  third-subject; Standing rewritten.
- third-subject — live source changed; new Timeline entry 2026-09-02.
- fourth-subject — closed as a dead end, reason recorded.

## Health findings
Breaks the model
- fifth-subject — `links: [sixth-subject]` dangles; no such file.
- seventh-subject — `last_swept: 2026-09-14` predates newest Log
  entry (2026-09-15).

Breaks a tenet
- eighth-subject — Established claim "…" carries no source ref.
- ninth-subject — status closed, no reason in the Log.
- tenth-subject ↔ eleventh-subject — asymmetric links.

Discipline drift
- twelfth-subject — Standing at 9 paragraphs; wants splitting.
- src-0044 — registered, cited by no subject.

## Decay candidates (not applied)
- thirteenth-subject — 3 no-change passes (2026-07-19, 2026-08-16,
  2026-09-14). Propose dormant, cadence 30d → 90d.

## Deferred (still due)
7 subjects. Most overdue: fourteenth-subject (+41d),
fifteenth-subject (+22d), sixteenth-subject (+9d).
```

The corresponding Log line in an unchanged subject:

```markdown
- 2026-09-14 — /sweep: no change. Rechecked src-0007, src-0031;
  3 open questions still open; confidence held at medium.
```

## What NOT to do

- **Don't skip the Log line when nothing changed.** This is the single
  most damaging shortcut available in this skill. It looks like noise
  reduction and it destroys the corpus's ability to tell verified from
  abandoned.
- **Don't write a bare "no change".** Name what was rechecked and what
  held, so a later reader can tell a real pass from a glance.
- **Don't manufacture movement to justify the pass.** Most passes over
  a well-tended corpus find nothing. Inventing a Standing rewrite to
  show productivity is the exact failure the domain's fifth tenet
  names.
- **Don't sweep everything because the selection was vague.** Ask, or
  default to all-due with a batch bound. Never assume "the whole
  corpus".
- **Don't widen the batch to empty the due queue.** A large standing
  queue is a cadence problem; report it as one.
- **Don't demote subjects to shrink the queue.** Demotion follows the
  no-change evidence, nothing else.
- **Don't auto-create missing subjects to resolve dangling links.** The
  dangle is the finding.
- **Don't resolve a Contested claim by picking the more convenient
  source.** If it resolves, it resolves on evidence and the resolution
  goes in the Log.
- **Don't start investigating.** Flag the newly-tractable question and
  move to the next subject.
- **Don't touch dormant, closed, or speculative subjects on a due
  sweep** unless they were named in the selection.
- **Don't auto-commit.**

## Done when

Every subject in the selection has been opened, has an appended Log
line describing what changed or explicitly recording that nothing did,
and has `last_swept` set to today. Subjects outside the batch are
untouched and reported as deferred. Health findings and decay
candidates are reported with subject ids and evidence, unfixed unless
the user approved them. The working tree holds the edits, uncommitted.
