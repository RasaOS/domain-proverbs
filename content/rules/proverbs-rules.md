# Proverbs Rules

The gates `rasa.domain.proverbs` enforces, installed at
`.claude/proverbs-rules.md`.

**This file governs the overlay only.** The substrate — what a topic is,
the folder shape, the lifecycle, the index, the three linking layers — is
`rasa.module.research`'s, and its `.claude/research-rules.md` is
authoritative there. Read that file first. **On any disagreement about a
substrate concern, the module's file wins.** These rules win for the four
things this domain adds: contested claims, the revisit clock, the
corpus-wide source registry, and the timeline axis.

The filenames differ on purpose. v0.1.0 of this domain shipped its own
`research-rules.md` and would have overwritten the module's on install.

---

## Group 1 — Contested claims

**P-1. A contested claim is never silently resolved.**
When sources genuinely disagree, both sides go in `contested.md` with
their own evidence, and stay there.
*Why:* resolving by adopting the more convenient source makes the error
invisible and load-bearing. Every later claim built on it inherits the
mistake with no trace back.

**P-2. `Superseded-by:` is for corrected claims; `contested.md` is for
unresolved ones.**
Use the substrate's `Superseded-by:` when you have warrant to name the
wrong side. Use `contested.md` when you do not.
*Why:* `Superseded-by:` forces a winner. Applied to an open question it
manufactures certainty at exactly the moment you have least of it.

**P-3. A contest resolves explicitly or not at all.**
Migration to `findings.md` requires the resolution recorded in `log.md`,
naming what settled it.
*Why:* a contest that quietly disappears is indistinguishable from one
that was never recorded.

**P-4. Both sides of a contest carry evidence.**
A position with no `[S#]` or `src-NNNN` behind it is not a side of a
contest; it is an open question.
*Why:* otherwise `contested.md` becomes a holding pen for hunches and
loses its meaning.

## Group 2 — The revisit clock

**P-5. `last_swept` advances on every sweep, including no-change sweeps.**
A sweep that finds nothing still advances `last_swept` and still writes a
`log.md` line.
*Why:* this is the whole point of the clock. Without it, "checked, still
true" and "nobody has looked at this in two years" are the same state on
disk.

**P-6. Dueness is computed, never stored.**
`last_swept + cadence < today`. No `due:` or `stale:` field.
*Why:* a stored flag goes wrong the first time a sweep runs and nobody
clears it, and a wrong flag is worse than no flag.

**P-7. Cadence is not priority.**
Do not set a short cadence to mark something important.
*Why:* the substrate has no importance ranking and this domain adds none.
A `7d` cadence on something that changes yearly generates noise that
trains you to ignore the due queue.

**P-8. Only `status: active` accrues cadence pressure.**
`open`, `dormant`, `concluded`, and `archived` have no clock.
*Why:* the due queue must stay proportional to actual attention, not to
topic count, or it becomes unreadable and therefore unread.

**P-9. Ingestion does not advance `last_swept`.**
Routing a claim into a topic is not a check of that topic's picture.
*Why:* conflating them lets a topic look freshly verified when all that
happened was an unrelated source mentioned it in passing.

## Group 3 — Provenance

**P-10. A `src-NNNN` id is assigned once and never recycled.**
Retired sources keep their id.
*Why:* it is the join key across topics. Recycling silently re-points
every citation that ever used it.

**P-11. Reliability is a property of the source; confidence is a property
of the claim.**
Never collapse them into one number.
*Why:* a high-reliability source can support a low-confidence claim (it
mentions the thing in passing), and three independent low-reliability
sources can support a high-confidence one. One scale cannot say that.

**P-12. A web source is captured, not just linked.**
Retrieved date plus enough excerpt to reconstruct the claim if the page
vanishes.
*Why:* URLs die. A citation that resolves to a 404 is a claim with no
evidence, discovered years later when it is least recoverable.

**P-13. Third-party copyrighted material is referenced and excerpted,
never bulk-copied.**
First-party and self-authored material is redistributable.

## Group 4 — The timeline axis

**P-14. A timeline entry records what happened; `log.md` records what the
researcher did.**
Never file research activity as a timeline entry.
*Why:* the axis exists precisely because the substrate had nothing that
recorded the world as distinct from the work on it.

**P-15. A timeline entry is owned by no topic.**
It references topics via `[[slug]]`; a topic's history is a query over
the timeline, not a copy stored in the topic.
*Why:* a copied history goes stale silently, and there is then no way to
tell which copy is right.

## Group 5 — Staying additive

**P-16. The overlay must never make the substrate unreadable without it.**
A topic carrying `cadence:`, `last_swept:`, and a `contested.md` is still
a valid `module.research` topic. Drop this domain and every topic
survives; only sweeping stops.
*Why:* this is the design constraint that justifies the composition at
all. A layer that captures its substrate is a fork wearing a dependency.

**P-17. Do not duplicate the substrate.**
No second node type, no second index, no second link syntax, and no skill
that opens a topic — `/research new` does that.
*Why:* v0.1.0 of this domain shipped a parallel structure under different
names. That is the mistake this version exists to correct.

**P-18. "Nothing found" is recorded, never replaced with plausible
synthesis.**
An empty pass writes what was searched and when, and leaves `## State of
play` untouched.
*Why:* an empty result is a real finding about the state of the evidence.
Filling the gap with fluent prose destroys it, and the fabrication is
unfalsifiable later.

---

## Fuller treatment

| Rules | Chapter |
|---|---|
| the division of labour, the frontmatter contract | `framework/topic-overlay.md` |
| P-10 … P-13 | `framework/provenance.md` |
| P-2, P-18 | `framework/investigation.md` |
| P-9 | `framework/ingestion.md` |
| P-5 … P-8 | `framework/longitudinal.md` |
| P-14, P-15 | `framework/timeline-axis.md` |
