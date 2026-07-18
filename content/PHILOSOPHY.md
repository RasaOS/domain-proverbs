# PHILOSOPHY — `rasa.domain.proverbs`

The stance this domain takes. Read before authoring content or invoking
any of its skills; the skills enforce what follows.

---

## What this domain is

A **research instrument for the long run**. It exists to track an
open-ended and growing set of subjects — topics, people, events,
organizations — across years, without the corpus degrading as it grows.

It is **subject-agnostic**. It carries no opinion about what is worth
researching. The method is the content; the subjects are supplied.
This is the same posture `rasa.domain.writer` takes toward stories and
`rasa.domain.code` takes toward codebases.

## The five tenets

### 1. The record is immutable; the picture is not.

Every dossier separates a **rewritten synthesis** (what is believed
now) from an **append-only log** (how the belief moved and when).
Neither can do the other's job. A corpus that only appends becomes
unreadable; a corpus that only rewrites loses the ability to audit its
own history. Both layers, always, in every subject.

This is the load-bearing decision of the whole domain. See
`framework/subject-model.md`.

### 2. A claim without provenance is not a claim.

Anything asserted in `## Established` carries a source reference and a
confidence marker. Synthesis without citation lives in `## Standing`,
clearly marked as synthesis. Suspicion without evidence lives in
`## Open questions`. There is no fourth place for an unsourced
assertion to hide, and the sweep will find it if one is smuggled in.

### 3. Disagreement is data, not noise.

`## Contested` is a first-class section. When sources conflict, both
sides are recorded with their provenance and the conflict is left
standing. Resolving a contested claim by quietly picking the more
convenient source is the single most damaging thing that can be done to
a long-running corpus, because the error becomes invisible and
load-bearing. If a contest resolves, it resolves explicitly, with the
resolution recorded in the Log.

### 4. Dead ends are findings.

A subject that turns out to be nothing gets `status: closed` with the
reason written down — never deleted. The purpose is to stop the same
dead end being re-explored in eighteen months. This is the corpus-level
form of the working principle that failures get documented so they
aren't re-litigated.

### 5. Calibrate, or say you don't know.

Confidence markers are honest or they are worthless. `low` is a normal
resting state for a well-tended subject. "I don't know" is a complete
and acceptable answer for any field, recorded as such. The instrument
must never manufacture a confident picture to appear productive — a
thin Standing section with three open questions is a better artifact
than a fluent paragraph resting on nothing.

## Three modes, one corpus

The domain runs in three modes against the same subject files. They are
not separate systems.

| Mode | Skill | Direction | Question it answers |
|---|---|---|---|
| **Active** | `/investigate` | pulls from outside | *What can I find out about this?* |
| **Passive** | `/ingest` | pushes from supplied material | *What does this source tell me, and about which subjects?* |
| **Longitudinal** | `/sweep` | revisits what's already here | *What changed, what went stale, what needs another look?* |

Active research fills a subject. Passive ingestion routes external
material into the subjects it touches — one source usually updates
several. Longitudinal sweeps are what make the corpus an *ongoing*
instrument rather than a pile of one-time write-ups; without a sweep
discipline, a research corpus silently becomes an archive.

## What "agnostic" commits us to

- **No subject content ships with this Element.** The Element ships the
  method, the templates, and the machinery. `content/subjects/` ships
  empty except for its template and README.
- **No domain vocabulary about any field.** The vocabulary covers the
  research method only — Subject, Standing, Log, sweep, cadence,
  provenance. Nothing about law, physics, sport, or any other vertical.
- **Nothing assumes a source type.** Web pages, PDFs, interviews,
  personal notes, and datasets are all just sources with provenance.
- **The corpus is portable.** A subjects tree written under this method
  is plain markdown with YAML frontmatter and no tool lock-in. If the
  machinery disappears, the research survives.

## The scaling claim, stated so it can fail

This domain makes one falsifiable claim: **a corpus built this way stays
workable as subject count grows, because the synthesis layer is bounded
while only the record layer grows.**

The test: reading the current state of N subjects should cost O(N) short
paragraphs, independent of how long each has been tracked. If Standing
sections are creeping past a few paragraphs, or if answering "what do we
know about X" requires reading X's Log, the method is failing and the
fix is structural — split the subject, or tighten the rewrite
discipline — not more prose.

## On the name

`proverbs` is a codename, not a subject. It carries no commitment to
proverbs as a field of study. The fitting reading, if one is wanted: a
proverb is a durable claim distilled from long accumulated
observation — which is what a well-tended `## Standing` section is.
Nothing in the method depends on this.
