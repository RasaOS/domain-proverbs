# Contested — {{TOPIC_TITLE}}

Claims where the sources genuinely **disagree**. Both sides recorded
with their own provenance and confidence, held open indefinitely. This
file is added by `rasa.domain.proverbs` on top of the
`rasa.module.research` topic folder; it sits alongside
[`findings.md`](findings.md), [`log.md`](log.md), and
[`open-questions.md`](open-questions.md).

Disagreement is data. A contest that stands for two years is a healthy
artifact. Silently resolving one by adopting the more convenient source
is the single most damaging thing that can be done to a long-running
corpus, because the error becomes invisible and load-bearing.

## Contested vs `Superseded-by:` — the line

The substrate resolves conflict on a finding with `Superseded-by:`.
That is the right primitive for a **corrected** claim and the wrong one
for an **unresolved** one:

| | `findings.md` + `Superseded-by:` | `contested.md` |
|---|---|---|
| Situation | The claim was wrong; a better one replaces it. | The evidence does not pick a side. |
| Live claims | One. The old is retired, kept for the trail. | Two or more, all live. |
| What you know | Which one is right. | That they conflict. |

**The test:** if you know which position is correct, this is a finding
with a `Superseded-by:` on the loser. If you are choosing because one
source is newer, better written, or more convenient — it belongs here.
`Superseded-by:` forces a winner at the moment you have least warrant
to pick one; this file is what stops that.

A claim that is merely *thin* is not contested either — a single weak
source with nothing against it is a low-confidence finding, or an entry
in `open-questions.md`. Contested requires an actual opposing source.

## Resolving a contest

A contest resolves **on evidence, explicitly**, and never as a side
effect of an edit:

1. Fill `**Resolution:**` with which position stands and on what
   evidence.
2. Migrate the surviving position to [`findings.md`](findings.md) as a
   normal finding, with its citations and confidence.
3. **Record it in [`log.md`](log.md)** under a dated heading — which
   contest, which position won, on what evidence. A resolution with no
   log line is a health-check finding, not a resolution.
4. Leave the entry here with its `**Resolution:**` filled. Nothing is
   deleted; the contest and its history are the record of why the
   finding is believed.

---

<!-- Template for each contest:

## C1 — TODO one line stating what is in dispute

**Position A — TODO the claim, one line**
- **Evidence:** TODO what supports it — cite [S#] from sources.md, or
  `[src-NNNN]` from the corpus-wide registry
- **Confidence:** high | medium | low
- **Held by:** TODO which sources assert this, and what standing they
  have to know

**Position B — TODO the competing claim, one line**
- **Evidence:** TODO — cite [S#] / `[src-NNNN]`
- **Confidence:** high | medium | low
- **Held by:** TODO

(Add Position C… where more than two positions are live. Every
position carries its own evidence; a position with no source is not a
position — it is an open question, and it moves to
open-questions.md.)

## Why unresolved

TODO what specifically is missing: the sources are independent and
irreconcilable / one side's provenance cannot be checked / both rest
on the same upstream material / the question as posed may not have a
single answer. State what evidence WOULD settle it — that sentence is
what makes this tractable on a later sweep.

**Resolution:** (unresolved)

-->

_No contested claims recorded yet._
