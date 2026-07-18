# Research Rules

The enforced gates of this domain. **Read this file before writing to
anything under `content/subjects/`** — every skill that touches a
dossier (`/track`, `/investigate`, `/ingest`, `/sweep`) is bound by
it, and so is a session editing a subject by hand.

These are the rules that make a corpus survive years of accumulation.
Each one exists because breaking it produces damage that is invisible
at the time and unrecoverable later — that is the common thread, and
it is why these are gates rather than preferences. The fuller
treatment of each is in `framework/subject-model.md` (the two-layer
model, the seven sections) and `framework/investigation.md` (the
pass, reconciliation, the anti-fabrication gate).

## The record layer

1. **The Log is append-only.** Never rewritten, never reordered,
   never pruned. Not to fix a typo, not to reword a clumsy entry, not
   to compact a long history.
   *Why:* the Log is the only layer that makes a six-month diff
   possible, and an edited Log is indistinguishable from an honest
   one. Once it can be edited it cannot be trusted, and every audit
   built on it becomes worthless.

2. **`## Standing` is rewritten wholesale on every pass, never
   appended to.** It reads as if written fresh today by someone who
   never saw the previous version. "We now also know that…" is Log
   material.
   *Why:* the scaling claim of this domain is that the synthesis
   layer stays bounded while only the record layer grows. A Standing
   section that accretes is a second log, and the corpus starts
   dying at around thirty subjects.

3. **`last_swept` advances on every sweep, including a sweep that
   changed nothing.** A no-change sweep also writes a Log line saying
   so.
   *Why:* staleness is computed from `last_swept`. A subject that was
   checked and found unchanged is in a completely different state
   from one nobody has looked at, and if the field doesn't move the
   two are indistinguishable — the checked subject stays flagged
   overdue forever and the signal degrades to noise.

4. **Required frontmatter is complete or the subject is broken.**
   Every field in the schema except `tags:` and `superseded_by:` is
   required, on every subject, from the moment it is opened.
   *Why:* the machinery reads frontmatter, not prose. A missing
   `cadence:` or `last_swept:` silently removes a subject from every
   staleness calculation, and it disappears from the corpus's
   attention without ever being closed.

## Claims and provenance

5. **No unsourced claim in `## Established`.** Every bullet carries a
   source reference and a confidence marker. Synthesis without a
   citation goes to `## Standing` marked as synthesis; a suspicion
   without evidence goes to `## Open questions`.
   *Why:* there is no fourth place for an unsourced assertion to
   hide, and that is deliberate. An unsourced claim in Established is
   cited by the next pass, inherited by the one after, and becomes
   load-bearing with no way to trace where it came from.

6. **Nothing cites an unregistered source.** A source is registered —
   id, locator, retrieval date — at fetch time, before it is cited,
   including sources that turned out to be useless.
   *Why:* write-up time is when the URL turns out to have been lost.
   Registering a dead end is what stops it being re-fetched next
   pass.

7. **A contested claim is never silently resolved.** When sources
   conflict, both sides stay in `## Contested` with their provenance
   and the conflict is left standing. If it resolves, it resolves
   explicitly: which side won, on what evidence, recorded in the Log.
   *Why:* picking the newer, better-written, or more convenient
   source and editing the other away is the most damaging single
   operation available in this domain. The error becomes invisible
   and load-bearing. A claim contested for two years is a healthy
   artifact; a silently resolved one is a landmine.

8. **"Nothing found" is recorded as nothing found.** An empty pass
   writes a Log line naming the angles it actually searched, leaves
   `## Standing` untouched, adds no claims, raises no confidence, and
   deletes no open question.
   *Why:* a pass that finds nothing and produces a fluent paragraph
   anyway — assembled from background knowledge and inference — reads
   exactly like a paragraph built from sources, and there is no way
   to find it again later. The gate is unconditional: it holds when
   the pass found a little and wants to round up, and when the user
   would clearly prefer a substantive answer.

9. **Confidence markers are calibrated honestly, and `low` is an
   acceptable resting state.** Confidence describes the state of the
   evidence, not how strongly the picture is held or how plausible it
   sounds. A single source of unknown reliability is `low` however
   confident its own prose is.
   *Why:* confidence markers are honest or they are worthless — a
   corpus where everything says `medium` carries no information. A
   thin Standing section with three open questions is a better
   artifact than a fluent paragraph resting on nothing. Confidence
   that never moves off `low` after several passes is itself a
   finding.

10. **Corroboration must be independent.** Two outlets reprinting one
    wire story are one source, not two, and do not raise confidence.
    *Why:* counting derivative sources manufactures the appearance of
    convergence, which is precisely the signal confidence is supposed
    to measure.

## Identity and lifecycle

11. **Subject ids are immutable and never recycled.** An id is
    assigned once and outlives the subject — a closed subject holds
    its id forever. If a subject genuinely becomes a different
    subject, close the old one with `superseded_by:` and open a new
    one.
    *Why:* links point at ids. Changing one breaks every reference
    silently; reusing one silently re-points old references at
    unrelated material, which is worse because it still resolves.

12. **A closed subject is never deleted, and the reason is recorded
    in the Log.** This includes speculative subjects that failed on
    first contact — especially those.
    *Why:* the purpose of a closed subject is to stop the same dead
    end being re-explored in eighteen months. A deleted subject
    guarantees it will be. Dead ends are findings.

13. **Links are symmetric.** Adding `b` to `a`'s `links:` means
    adding `a` to `b`'s, in the same operation.
    *Why:* a one-directional link rots — the other subject has no
    idea it is connected, so the neighbourhood is only visible from
    one side and a sweep on `b` never sees `a`.

## Sources and handling

14. **Third-party copyrighted material is referenced, never
    bulk-copied.** Register the locator and quote only what a claim
    actually needs — a short excerpt, attributed. The dossier records
    what a source says and where to find it; it is not a mirror of
    the source.
    *Why:* a research corpus that reproduces its sources is a
    redistribution problem wearing a research corpus's clothes, and
    it destroys the portability the format is built for. First-party
    material the corpus owns is a separate case and may be held in
    full.

15. **Edits land in the working tree; nothing auto-commits.** Every
    skill in this domain leaves its changes uncommitted for review.
    *Why:* the corpus is the durable artifact. A wrong write that was
    reviewed is a correction; a wrong write that was committed
    automatically is archaeology.
