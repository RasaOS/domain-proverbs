---
name: investigate
description: Run an active research pass on an existing research topic — live web search, fetch, source registration, and a topic-folder update. Triggered when the user wants outside material pulled in on a topic already being tracked — e.g. "/investigate", "look into <topic>", "research this topic", "dig into X", "run a pass on the <slug> topic", "what can we find out about X". Reads the topic's open-questions.md first and works those rather than free-associating; fans out independent search angles; registers every fetched source in the global registry and the topic's local shelf before citing it. Writes durable files — edits the topic folder and research/sources/ in the working tree, never auto-commits.
---

# /investigate — Active research pass on a topic

Pull outside material into an existing topic folder. Question-driven:
the pass reads `open-questions.md` and works those questions, reconciles
what it found against `findings.md` and `contested.md`, and rewrites the
README's `## State of play`.

The method chapter is `framework/investigation.md`; the structure it
operates on is the substrate's (`.claude/research-rules.md`) plus this
domain's overlay (`framework/topic-overlay.md`). This skill enforces
all three. Its hardest rules are the last two: a contradiction does not
get resolved to look productive, and a pass that finds nothing says so
and leaves State of play untouched.

## Behavior contract

- **Operates on an EXISTING topic.** This skill does not open topics.
  Opening one is the substrate's `/research new`. If the named topic
  has no folder, stop and say so — propose the slug and hand off.
- **Writes to the working tree for review; never auto-commits.** Edits
  land in the topic folder and `research/sources/`. The user reviews
  with `git diff`.
- **Question-driven.** Scope comes from `open-questions.md`. If the
  topic has none, stop and ask for questions rather than inventing a
  research direction.
- **Never assert an unsourced claim.** Anything in `findings.md`
  carries a `[S#]` and a `**Confidence:**`. Synthesis goes to
  `## State of play` marked as synthesis; suspicion goes to
  `open-questions.md`. There is no fourth place.
- **Register twice, before citing.** Every fetched source gets a
  `src-NNNN` record in `research/sources/` *and* the next `[S#]` row in
  the topic's `sources.md` pointing at that global id — both before any
  finding references it. Sources that turned out useless are registered
  too, marked checked-and-empty, so they aren't re-fetched.
- **Contradiction moves a finding to `contested.md`; it never
  supersedes it.** `Superseded-by:` is for corrected claims — where you
  can state on evidence why the old one is wrong. Unresolved
  disagreement goes to `contested.md` with both sides. Resolution is
  explicit and logged.
- **State of play is rewritten; `log.md` is appended.** Never edit,
  reorder, or prune an existing log entry.
- **`last_swept` advances every pass**, including an empty one. Never
  backdated.
- **An empty pass is recorded, not papered over.** No sources found
  means a log entry naming the angles searched, `last_swept` advanced,
  and zero changes to State of play. No inference dressed as a finding.
- **One topic per invocation.** Adjacent material is noted, not chased
  into other topic folders.

## Process

1. Read the topic folder — `open-questions.md` first, then `README.md`,
   `findings.md`, `contested.md`, `sources.md`. If the folder is
   missing, or has no open questions, stop and report that before
   searching.
2. Scope: pick two to four open questions to work this pass. State
   them. Rewrite any that are malformed, or strike them with a reason.
3. Fan out. Per scoped question, run several independent angles — by
   entity name and known aliases, by event or date without the name, by
   adjacent actor (`related:` / `[[slug]]` are the starting list), by
   primary-document type. Breadth beats depth.
4. Fetch. Register each source at fetch time: `src-NNNN` in
   `research/sources/`, then the `[S#]` row in the topic's `sources.md`
   pointing at it.
5. Extract claims, one per candidate, each with its `[S#]` and a
   confidence value. Confidence describes the evidence, not the
   source's tone.
6. Reconcile: a new claim with no counterpart appends as the next `F#`;
   an agreeing claim adds its `[S#]` to the existing finding's basis; a
   contradicting claim moves the existing finding to `contested.md`
   with both sides; a resolved contest moves back to `findings.md` with
   the winning evidence named.
7. Rewrite `## State of play` as the current picture, short, with no
   narration of the pass. Bump `updated:`; flip `status: open` →
   `active` if this is the first real pass. Route dated facts that
   belong to no single topic to `research/timeline/`.
8. Append one dated entry to `log.md`: what was worked, what moved,
   which sources registered (global and local ids), and which stopping
   rule ended the pass.
9. Advance `last_swept:` to today.
10. Report to the user: questions closed, questions opened, sources
    registered, findings added, contests opened. Leave everything
    uncommitted.

## Stopping rules

End the pass and name the reason in `log.md` when one holds:

- **Questions closed** — every scoped question answered, narrowed, or
  recorded as unanswerable with the reason.
- **Saturation** — two consecutive search angles return no source not
  already registered for this topic.
- **Budget** — the user's time or call budget is spent. Log that the
  pass was cut short so the next one knows where it stands.

## What NOT to do

- Don't open a topic. No folder means hand off to `/research new`.
- Don't research the topic freely instead of the open questions.
- Don't cite a source that isn't in `research/sources/`, and don't
  leave it off the topic's local `sources.md` shelf. Both, always.
- Don't write a claim into `findings.md` without a `[S#]`.
- Don't set `Superseded-by:` on a finding a new source merely disagrees
  with. Supersede only when you can state on evidence why the old claim
  is wrong; otherwise it goes to `contested.md`.
- Don't resolve a contest by preferring the newer, longer, or
  better-written source. Both are tenet-3 violations and both are
  invisible later.
- Don't treat several outlets carrying one wire story as independent
  corroboration and raise confidence on it.
- Don't synthesize a plausible paragraph when the search came back
  empty. Write the empty result.
- Don't raise confidence to look productive. `low` is a normal resting
  state.
- Don't edit `log.md` history, reorder it, or compact it.
- Don't backdate `last_swept`, and don't advance it for a topic this
  pass didn't open.
- Don't edit other topics' folders, conclude or promote the topic
  (that's `/research conclude`), or commit.

## When NOT to use this skill

- The user supplied the material (a PDF, an article, notes) — that's
  `/ingest`, the passive mode.
- The ask is "what's gone stale across the corpus" — that's `/sweep`.
- The topic doesn't exist yet — that's `/research new`.
- The topic exists but has no open questions. Write questions first; a
  pass with nothing to answer has no scope and no stopping condition.

## Done when

The topic folder is updated in the working tree: `## State of play`
rewritten, `findings.md` and `contested.md` reconciled, every new source
registered in `research/sources/` and on the topic's `sources.md` shelf
before it was cited, one dated `log.md` entry recording what moved and
which stopping rule fired, and `last_swept` advanced — or, on an empty
pass, State of play untouched, `last_swept` advanced, and a log entry
naming the angles searched. Nothing is committed.
