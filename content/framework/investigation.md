# Investigation — the active mode

How a research pass runs against a Subject. This is the **active**
mode of the three: it pulls material from outside the corpus and lands
it in a dossier. Read `subject-model.md` first — everything here is
read and write operations on the seven sections defined there.

---

## Question-driven, not topic-driven

A pass reads `## Open questions` **first**, before anything else in the
file, and works those questions. It does not free-associate about the
subject and see what turns up.

The distinction is not stylistic. Topic-driven research on a subject
already tracked for a year re-finds what is already in `## Established`
and produces a pass that costs an hour and adds nothing. Question-driven
research is bounded: the questions define what would count as progress,
so the pass can be scoped, can be judged, and can *end*.

The consequence: **a subject with no open questions is not ready for an
investigation pass.** Either write questions first, or the subject is
mislabeled `active` and belongs at `dormant`. A pass that opens with
"there's nothing specific to chase here, let me look around" is the
failure mode, not the warm-up.

Open questions are also the pass's output, not only its input. Most
passes close some questions and open others; a pass that answers three
questions and raises five has done well, not badly.

## The pass

Seven steps, in order. Each one has a defined input and a defined
write target.

### 1. Scope from open questions

Read the dossier. Take `## Open questions` and pick the ones this pass
will work — usually two to four. State them explicitly at the start of
the pass. Questions not picked are left alone, not silently dropped.

If a question turns out to be malformed (unanswerable as written,
or answerable only by opinion), rewrite it into an answerable form or
demote it with a note. Recording that a question was malformed is a
result.

### 2. Fan out searches

Turn each scoped question into several independent search angles. See
**search breadth discipline** below. This is the step where a pass is
won or lost.

### 3. Fetch and register sources

Fetch what the searches return. **Every source that will be cited gets
registered in the source registry before it is cited** — id, locator,
retrieval date, and whatever the registry schema requires (see
`provenance.md`). Nothing cites an unregistered source, and the
registration happens at fetch time, not at write-up time, because
write-up time is when the URL turns out to have been lost.

A source that was fetched and turned out to be useless still gets
registered, with a note that it was checked and was empty. That is what
stops it being re-fetched next pass.

### 4. Extract claims with provenance

Pull discrete claims out of each source. One claim per bullet, each
carrying its source id and a confidence marker. A claim that cannot be
tied to a specific source is not a claim — it is synthesis, and it goes
to `## Standing`, or a suspicion, and it goes to `## Open questions`.
Tenet 2 has no exceptions and the sweep enforces it.

Confidence at this step describes the *source's* support for the claim,
not how plausible it sounds. A single source of unknown reliability
saying something is `low`, however confident the source's own prose is.

### 5. Reconcile against Established and Contested

The new claims meet the existing ones. Rules below.

### 6. Rewrite Standing

`## Standing` is **rewritten**, not appended to. Produce the current
picture as it stands after this pass, in prose, short. Do not narrate
the pass — "we now also know that..." is Log material. Standing reads
as if written fresh today by someone who never saw the earlier version.

Update `confidence:` in frontmatter if the state of the evidence moved.
It is normal for it to stay at `low`.

### 7. Append to Log

One line, dated, describing what the pass did and what moved. Append
only — never edit an earlier line, never reorder, never prune.

```markdown
- 2026-07-18 — /investigate: worked Q1, Q3. Four sources registered;
  one Established claim demoted to Contested (src-0044 vs src-0012).
```

The Log line is what makes the pass auditable six months later. A pass
that changed the dossier but wrote no Log line has corrupted the record
even if every claim it added is correct.

## Reconciliation rules

The new claims meet the existing ones. Four cases:

**New claim, no existing counterpart.** Add to `## Established` with
its source ref and confidence.

**New claim agrees with an Established claim.** Add the new source id
to the existing bullet. Raise confidence if independent corroboration
warrants it — independent, meaning not two outlets reprinting one wire
story. Two sources with a common upstream are one source.

**New claim contradicts an Established claim.** The Established claim
is **not overwritten and not deleted.** Move it to `## Contested`,
carrying both sides and both sources, and leave the conflict standing.
Record the move in the Log.

This is tenet 3 and it is the rule most likely to be violated by a pass
that wants to look productive. Picking the newer, better-written, or
more convenient source and quietly editing the old claim away is the
single most damaging operation available in this domain, because the
error becomes invisible and load-bearing: every later pass inherits the
resolved claim with no trace that it was ever in doubt. A contested
claim that sits contested for two years is a healthy artifact. A
silently resolved one is a landmine.

**New claim resolves an existing Contested claim.** Allowed, but
explicitly: move it back to `## Established`, state which side won and
on what evidence, and record the resolution in the Log. "Resolved
because a third source arrived and it agrees with side A" is a
resolution. "Resolved because side B seemed weak" is not.

## Search breadth discipline

**Multiple independent angles beat one deep thread.** A single search
line followed for an hour explores one corner of the available material
and returns a coherent, confident, and possibly badly skewed picture.
Four shallow angles from different directions surface the disagreement
that tells you where the real question is.

Concrete angle types to run against a scoped question:

- **By entity name** — the subject's own name, plus known aliases,
  former names, and misspellings. Renamed entities are frequently
  invisible under their current name.
- **By event or date** — what happened, when, without the subject's
  name in the query. Catches material where the subject is mentioned
  but is not the headline.
- **By adjacent actor** — the people, organizations, or subjects
  linked to this one. Adjacent parties leave records about each other,
  and their accounts of the same events are where contests come from.
- **By primary-document type** — filings, transcripts, registries,
  datasets, official records. The document class that would *have* to
  exist if a claim is true, searched for directly.

Run angles in parallel where the tooling allows and treat their results
as independent evidence. Two angles converging on the same source is
one source, not two.

## Stopping rules

A pass ends when one of these is true. Name which one in the Log.

**Questions closed.** Every scoped open question is answered, demoted
to a narrower question, or recorded as unanswerable with the reason.

**Saturation.** The searches stop returning new material. The explicit
heuristic: **two consecutive search angles return no source that is not
already registered for this subject.** Not "the results look familiar" —
two angles, consecutively, zero new registrations. At that point the
accessible surface for these questions is exhausted and further
searching is spending time to re-find what is already in the file.

**Budget.** The pass hits whatever time or call budget the user set.
This ends the pass but does not close the questions; the Log says the
pass was cut short so the next one knows where it stands.

Saturation is a finding in its own right. "Saturated at four angles
with no new sources" written in the Log tells the next pass, and the
next sweep, that this question needs a different kind of source rather
than more of the same searching.

## The anti-fabrication gate

**If the search yields nothing, the pass writes that down and changes
nothing else.**

The Log line records what was actually attempted:

```markdown
- 2026-07-18 — /investigate: nothing found. Searched entity name +
  two aliases, filings 2019–2024, adjacent org registry. No new
  sources. Standing untouched.
```

`## Standing` is left exactly as it was. No claims are added. No
confidence is raised. No open question is quietly deleted to make the
subject look tidier.

An empty pass is a real result and one of the more valuable ones,
because it is evidence about the availability of material — and because
it is checkable. The named angles let the next pass avoid repeating
them, and let a reader judge whether the pass looked in sensible
places.

The failure this gate exists to prevent: a pass that finds nothing and
produces a fluent paragraph anyway, assembled from background knowledge
and inference, that reads exactly like a paragraph built from sources.
Once that paragraph is in Standing it is indistinguishable from
researched material, it will be cited by the next pass, and there is no
way to find it later. Per tenet 5, a thin Standing section with five
open questions is a better artifact than a confident paragraph resting
on nothing.

The gate is unconditional. It applies when the pass has found nothing,
when it has found a little and wants to round up, and when the user
asked for a summary and would clearly prefer a substantive one.

## What a pass does not do

- **Does not touch other subjects' dossiers.** Material about an
  adjacent subject that surfaces during a pass is noted in this
  subject's Log and routed by `/ingest`, which is the mode built for
  fan-out. A pass that starts editing three neighbouring dossiers has
  become an unbounded pass.
- **Does not open new subjects on its own.** It can propose one; the
  user decides.
- **Does not commit.** Edits land in the working tree for review.
- **Does not rewrite the Log.** Ever, under any circumstance.
