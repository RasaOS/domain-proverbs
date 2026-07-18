---
name: investigate
description: Run an active research pass on a subject in the corpus — live web search, fetch, source registration, and a dossier update. Triggered when the user wants outside material pulled in on a tracked subject — e.g. "/investigate", "look into <subject>", "research this subject", "dig into X", "what can we find out about X". Reads the subject's Open questions first and works those rather than free-associating; fans out independent search angles; registers every fetched source before citing it. Writes durable files — edits the subject dossier and the source registry in the working tree, never auto-commits.
---

# /investigate — Active research pass on a subject

Pull outside material into a Subject dossier. Question-driven: the
pass reads `## Open questions` and works them, then reconciles what it
found against what is already recorded and rewrites `## Standing`.

The method chapter is `framework/investigation.md`; the file shape is
`framework/subject-model.md`. This skill enforces both. Its hardest
rule is the last one: a pass that finds nothing says so and leaves
Standing untouched.

## Behavior contract

- **Writes to the working tree for review; never auto-commits.** Edits
  land in the subject dossier and the source registry. The user reviews
  with `git diff`.
- **Never assert an unsourced claim.** Anything in `## Established`
  carries a source id and a confidence marker. Synthesis goes to
  `## Standing` as synthesis; suspicion goes to `## Open questions`.
  There is no fourth place.
- **Register before citing.** Every fetched source is written into the
  source registry — id, locator, retrieval date — *before* any dossier
  line references it. Sources that turned out useless are registered
  too, marked as checked-and-empty, so they aren't re-fetched.
- **Question-driven.** Scope comes from `## Open questions`. If the
  subject has none, stop and ask for questions rather than inventing a
  research direction.
- **Contradiction moves a claim to Contested, never overwrites it.** A
  new source disagreeing with an Established claim promotes the
  disagreement; it does not settle it. Resolution is explicit and
  logged.
- **Standing is rewritten; Log is appended.** Never edit, reorder, or
  prune an existing Log line.
- **An empty pass is recorded, not papered over.** No sources found
  means a Log line naming the angles searched and the date, and zero
  changes to Standing. No inference dressed as a finding.
- **One subject per invocation.** Adjacent material is noted, not
  chased into other dossiers.

## Process

1. Read the subject file. If it's missing required frontmatter or has
   no `## Open questions`, stop and report that before searching.
2. Scope: pick two to four open questions to work this pass. State
   them. Rewrite any that are malformed, or demote them with a note.
3. Fan out. Per scoped question, run several independent angles — by
   entity name and known aliases, by event or date without the name,
   by adjacent actor, by primary-document type. Breadth beats depth.
4. Fetch. Register each source in the registry at fetch time.
5. Extract claims, one per bullet, each with source id and confidence.
   Confidence describes the evidence, not the source's tone.
6. Reconcile against `## Established` and `## Contested`: new claim
   adds; agreeing claim merges source ids; contradicting claim moves
   the existing claim to Contested with both sides; a resolved contest
   moves back to Established with the winning evidence named.
7. Rewrite `## Standing` as the current picture, short, no narration
   of the pass. Update `confidence:` in frontmatter if the evidence
   moved. Append to `## Sources` and `## Timeline` as applicable.
8. Append one dated `## Log` line: what was worked, what moved, and
   which stopping rule ended the pass.
9. Report to the user: questions closed, questions opened, sources
   registered, claims moved to Contested. Leave everything uncommitted.

## Stopping rules

End the pass and name the reason in the Log when one holds:

- **Questions closed** — every scoped question answered, narrowed, or
  recorded as unanswerable with the reason.
- **Saturation** — two consecutive search angles return no source not
  already registered for this subject.
- **Budget** — the user's time or call budget is spent. Log that the
  pass was cut short so the next one knows where it stands.

## What NOT to do

- Don't research the topic freely instead of the open questions.
- Don't cite a source that isn't in the registry.
- Don't write a claim into `## Established` without a source id.
- Don't overwrite an Established claim with a contradicting one, or
  resolve a Contested claim by preferring the newer or better-written
  source. Both are tenet-3 violations and both are invisible later.
- Don't treat several outlets carrying one wire story as independent
  corroboration and raise confidence on it.
- Don't synthesize a plausible paragraph when the search came back
  empty. Write the empty result.
- Don't raise `confidence:` to look productive. `low` is a normal
  resting state.
- Don't edit `## Log` history, reorder it, or compact it.
- Don't edit other subjects' dossiers, open new subjects unasked, or
  commit.

## When NOT to use this skill

- The user supplied the material (a PDF, an article, notes) — that's
  `/ingest`, the passive mode.
- The ask is "what's gone stale across the corpus" — that's `/sweep`.
- The subject doesn't exist yet, or has no open questions. Open it and
  write questions first; an investigation pass with nothing to answer
  has no scope and no stopping condition.

## Done when

The subject file is updated in the working tree: `## Standing`
rewritten, `## Established` / `## Contested` reconciled, every new
source registered before it was cited, and one dated `## Log` line
recording what moved and which stopping rule fired — or, on an empty
pass, Standing untouched and a Log line naming the angles searched and
the date. Nothing is committed.
