# PHILOSOPHY — `rasa.domain.proverbs`

The stance this domain takes. Read `framework/topic-overlay.md` next; it
turns this into structure.

---

## What this domain is

The **epistemic and longitudinal discipline layer** over
`rasa.module.research`.

It is not a research system. `rasa.module.research` is the research
system: it owns topics, their folder shape, the lifecycle, the index, and
the linking layers. This domain requires it and adds the four things it
has no equivalent for — held-open disagreement, a revisit clock, a
corpus-wide source registry, and a dated timeline axis.

It is **subject-agnostic**. It carries no opinion about what is worth
researching. The discipline is the content; the subjects are supplied.

## Why a layer and not a system

v0.1.0 of this domain was a system. It defined its own file-per-subject
structure, its own current-picture section, its own claims file, its own
log — every one of which already existed in `rasa.module.research` under
a different name. The overlap was found after that version shipped.

The lesson is recorded here rather than quietly fixed, because it is the
governing constraint on everything that follows: **when the substrate
already names a thing, use its name.** A second vocabulary for one
structure is not a richer model, it is drift, and it costs most at the
moment two deployments have to be reconciled.

So: a topic is a topic. Its current picture is `## State of play`. Its
durable claims are findings. This domain introduces no synonyms.

## The four tenets

Each governs one addition, and each exists because the substrate is
silent on it — not because a different flavour was preferred.

### 1. Disagreement is data, not noise.

`contested.md` holds claims where sources genuinely conflict, both sides
with their provenance, indefinitely.

The substrate resolves conflict with `Superseded-by:`— one claim replaces
another. That is right for *corrected* claims and wrong for *unresolved*
ones, because it forces a winner at the moment you have least warrant to
pick one. Silently resolving a contest by adopting the more convenient
source is the most damaging single act available in a long-running
corpus: the error becomes invisible, and everything built on it inherits
the mistake with no trace back.

### 2. A picture without a date is not a status.

`status: active` says a topic is live. It never says when the topic was
last actually looked at. Those are different facts and only one of them
was recorded.

`cadence:` and `last_swept:` close the gap, and the rule that makes them
worth anything is that **a sweep records no-change**. `last_swept`
advances and `log.md` gets a line even when nothing moved — because
otherwise "checked, still true" and "nobody has looked at this in two
years" are the same state on disk. This is the difference between a
research instrument and an archive.

### 3. Evidence is corpus-wide, not topic-local.

The same source routinely bears on several topics. A topic-local `[S1]`
cannot express that a claim in one topic and a claim in another rest on
the *same* evidence, so it cannot answer "what else did this source
support?" or "what falls if this source is discredited?"

A stable `src-NNNN` registry answers both. It coexists with the local
shelf rather than replacing it — the local id stays the citation, the
global id is the join key. And reliability is tracked as a property of
the *source*, distinct from confidence in a *claim*, because one number
cannot say that three independent weak sources agreeing is stronger than
one strong source mentioning something in passing.

### 4. What happened is not what the researcher did.

`log.md` is a record of the investigation. It is not a record of the
world. Conflating them means a corpus can tell you when it learned
something but never when the thing occurred.

A timeline entry is a dated fact relating several topics and owned by
none of them.

## Two standing commitments

**Stay additive.** A topic carrying this domain's fields is still a valid
`module.research` topic. Drop this domain and every topic survives
intact; only sweeping stops. A layer that captures its substrate is a
fork wearing a dependency, and this one must never become that.

**Calibrate, or say you don't know.** Confidence and reliability markers
are honest or worthless. "Nothing found" is a real result and gets
recorded as such — an empty pass writes what was searched and when, and
leaves `## State of play` untouched. A thin picture with three open
questions is a better artifact than a fluent paragraph resting on
nothing, and it is the only one of the two that can later be shown wrong.

## What "agnostic" commits us to

- **No subject content ships.** The Element carries discipline,
  templates, and machinery. The corpus is the deployment's.
- **No field vocabulary.** Overlay terms only, and inherited substrate
  terms are pointed at rather than redefined.
- **Nothing assumes a source type.** Pages, PDFs, interviews, notes, and
  datasets are all sources with provenance.
- **The corpus stays portable.** Plain markdown with YAML frontmatter, on
  top of a substrate that is itself plain markdown. If the machinery
  disappears, the research survives.

## The claim, stated so it can fail

**A corpus under this overlay can answer, for any topic, both "what do we
currently believe" and "when was that last actually checked" — in bounded
time, however long the corpus has been running.**

The test: pick any topic. If answering the first question requires
reading `log.md`, the substrate's rewrite discipline has failed. If the
second question has no answer better than "sometime after `updated:`",
the clock has failed. Either way the fix is structural, not more prose.
