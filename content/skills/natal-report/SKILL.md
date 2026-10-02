---
name: natal-report
description: Produce a full natal-chart-and-numerology reading for a person, published as an Artifact in the established house format. Use when asked for a natal chart, birth chart, astrology reading, numerology report, or "the full report" for someone's birth details.
user-invocable: true
---

# Natal Chart & Numerology reading

Produces one deliverable: an Artifact titled **`<Full Name> — Natal Chart & Numerology`**,
written *to* the subject, usually commissioned as a gift by someone who knows them.

## Behavior contract

- **Writes files and publishes.** Computes the chart locally, writes a report HTML
  (and a PDF on request) in the working directory, and publishes one Artifact. Publishing
  is outward-facing — confirm with the user before the first publish for a person.
- **Meaning about the person, never the method** (the rule below). The arithmetic is exact
  and almost entirely invisible.
- **Never guess missing inputs.** No birth time/city means no Ascendant, Midheaven or houses —
  say so; do not invent them. Never infer pronouns from a name.
- **Symbolic, not predictive.** The footer states this; the body never claims prediction.
- **Never auto-commit.** Reports are deliverables, not element content.

## Process

1. Collect inputs (below); confirm the timezone/DST for the birth date and place.
2. Run `scripts/chart.py` to compute the chart and all timing.
3. Write the 16 sections (Structure, below), meaning-first, in the house design.
4. Run the Verification checklist; fix before publishing.
5. Publish the Artifact (and export the PDF if asked).

## The rule that governs everything

**Write about the person, not about the method.**

This is the correction that matters most. An earlier version of this report was rejected for
"too much explanations and numbering breakdowns" and not enough about "what everything means for
that person." The arithmetic must be *exact* and almost entirely *invisible*.

A reader who knows nothing about astrology and never learns any should be able to read the whole
report and feel accurately seen. Every paragraph must pass one test: **does this tell them
something about their life?**

### Never appears in the report

- Arithmetic of any kind — no `74 → 11`, no `3 + 4 + 8 = 15`, no letter sums, no digit tallies,
  no "reduces to", no "mod 22".
- Explanations of technique — what a stellium is, how a Life Path is derived, what an orb is,
  how pinnacles or personal years are computed.
- Method disputes on the page: "two schools differ", "by the component method", which system
  produced which number. Resolve these *silently* (see Verification) and state one answer.
- A placement or figure named without the sentence going on to say what it means for them.
- Degrees as decoration. At most one or two exact figures survive in an entire report, and only
  where the precision itself is the point.

### Always appears

- Lived texture: what it feels like from the inside, what other people notice, what they keep
  doing that doesn't work, what they're good at without trying.
- Concrete situations over abstractions. *"You will notice the guest nobody is talking to, and
  you will go over, and you will not experience it as a decision"* beats *"Libra rising indicates
  social awareness."*
- The shadow named as plainly as the gift. A reading that only flatters is worthless. Honest,
  never cruel — this is a gift.
- Ratio: at most one clause of astrology to three of meaning.
- Second person. Warm, literate, grown-up. American spelling. No emoji, no exclamation marks.
- **Never gender the subject** unless they stated pronouns. "You" throughout.
- Interpret symbolism; never predict events.

Banned phrases: *cosmic blueprint · the universe is telling you · divine timing · your soul chose ·
old soul · on a deep level · "journey" as a noun for a life · "energy" as a mass noun · vibration.*
Never open a section by restating its own title.

## Inputs

Required: **full birth name** (as on the birth certificate — middle names count) and **birth date**.
Strongly wanted: **birth time** and **birth city** — without them there is no Ascendant, no
Midheaven, and no houses, so say plainly that the reading will be roughly half a reading.
Ask for pronouns, or use "you" throughout and never guess from the name.

## Toolchain

```bash
pip3 install pyswisseph
```

Real Swiss Ephemeris, arcsecond-accurate, no data files needed for the planets. Use
`scripts/chart.py` in this skill — edit the birth block at the top and run it. It emits positions,
whole-sign houses, aspects with orbs, element/modality balance, sect, moon phase, Part of Fortune,
and all the timing (returns, progressions, personal years, pinnacles, challenges).

Chiron needs one extra file:

```bash
curl -sL -o ephe/seas_18.se1 https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
```

Get the timezone right — it is the single most common source of a wrong Ascendant. Check whether
DST was in effect on that date *in that jurisdiction* in that year, then convert to UT.

Conventions: **tropical zodiac, whole-sign houses.** Compute quadrant cusps too; where the two
systems disagree about a body's house, that is worth knowing (and occasionally worth one honest
sentence, if the divergence itself is meaningful).

## Structure

Sections, in order. Marked ★ are the ones that carry the meaning — give them the most room.

1. **The Portrait** ★ — the long-form centerpiece, 1100–1300 words, drop cap, one italic closing
   line. Must stand alone for a reader who never learns any astrology.
2. **The Big Three** — Sun, Rising, Moon as three cards.
3. **The House of Home** ★ (or whichever house/sign dominates) — the chart's centre of gravity.
   Name the section after *the meaning*, not the technique. Never "The Stellium".
4. **Your Sun in Depth** — sign, decan, best/shadow, and the house it lives in.
5. **How You Meet the World** — the angles, as relational meaning.
6. **The Six Numbers** — Life Path, Expression, Soul Urge, Personality, Birthday, Maturity, as
   plates. Epithet + meaning. No derivations. Follow with what the name *failed* to supply.
7. **The Eleven / master numbers** ★ — only if present; meaning and cost, no method.
8. **What You Are Here to Learn** ★ — the lunar nodes. Usually the most *useful* section in the
   report. South Node = the over-practiced default groove; North Node = the unpracticed direction
   that actually grows them. Get these the right way round.
9. **How You Work** — vocation, money, worth: MC, Saturn, 2nd/6th/8th/10th houses.
10. **What Wounds You, and How It Heals** ★ — Chiron, the hard Moon aspects, the honest one.
11. **Numerology Across Traditions** — Pythagorean, Chaldean, Vedic, Kabbalistic, Chinese Lo Shu.
    Keep it short and meaning-first.
12. **Where it all rhymes** — synthesis: where independent systems describe the same person.
13. **Life Arc** — the nine-year rhythm as lived chapters: been / are / going / purpose.
14. **The Road Ahead** — the four life eras and the genuine thresholds.
15. **Love & Matches** — need vs. pull, best and higher-friction, their own contribution to the
    difficulty, and what repair actually looks like.
16. **Kindred Spirits** — real people sharing the date, Life Path, Sun sign, Birthday number,
    computed from published birth dates. Verify the dates.

Cut or fold anything that is mostly a table. A compact positions table may live near the end for
the curious; an aspect grid, a letter-by-letter name breakdown, and an element-balance chart are
usually machinery and should go.

## Design

House style, consistent across the set — match it rather than inventing:

- Light: warm parchment `#f3ead6` ground, `#ece0c6` panels, `#241c10` ink, brass `#9a6a12` accent,
  slate-blue `#3c5a7c` secondary. Dark: `#0b1322` ground, `#111b2e` panels, `#ece7d7` ink,
  brass `#d9b364`, `#8ba7cc`. Define all tokens on bare `:root`, redefine under
  `@media (prefers-color-scheme:dark){:root:not([data-theme="light"])}` **and** `:root[data-theme="dark"]`.
- Type: `"Iowan Old Style", Palatino, Georgia, serif` for display; system sans for body; mono for
  labels and eyebrows.
- `.wrap` max-width 940px. Section heads are `h2` + hairline rule + a mono eyebrow on the right.
- Canvas chart wheel in the hero — see `scripts/wheel.js`.

### Chart-wheel gotcha (this will bite)

A stellium collides. Naive angular relaxation lets glyphs **cross each other**, after which
array-adjacent items are no longer circle-adjacent and the gap test silently passes on a false
~347° gap — producing overlapping glyphs that look fine to the code. Use the order-preserving
spread in `scripts/wheel.js`: cut the circle at the largest gap, clamp forward then backward, then
re-centre each rigid block on its members' true mean, and draw leader lines from the true degree
out to the displaced glyph. Verify the wheel by rendering it and *looking at it*, in both themes.

## Verification — rigorous, and invisible

Check hard; publish clean. Run an adversarial pass over the drafted prose for:

- **Astrological doctrine.** Sect trips people constantly: **Saturn is diurnal**, so it is *out of
  sect and harsher* in a night chart. Uranus/Neptune/Pluto have no sect. Nodes: South = practiced
  default, North = growth direction.
- **Arithmetic**, recomputed independently — every letter sum, personal year, pinnacle, and every
  famous person's Life Path and Sun sign.
- **Leaked method** — anything that survived the meaning-first rule.
- **Overclaimed convergence.** These are routinely oversold; state the dependence or drop the claim:
  - Two letter systems (Pythagorean/Chaldean) reducing to the same number is weak — same letters,
    same digit-sum ending. Any two totals differing by a multiple of 9 share a digital root.
  - A surname's own master number is a *component* of the full-name total, not a second arrival.
  - Vedic Destiny and Pythagorean Life Path come from the same date digits: one signature, not two.
  - A Kabbalistic path landing on a sign present in the chart is ~1-in-12 by chance.
  - The genuinely strong convergence is one where the **inputs don't overlap** — e.g. a number from
    the letters of a name matching an aspect measured from an ephemeris.

Where methods disagree, pick the mainstream one and state a single answer. The reader gets the
conclusion; they do not get the argument.

## Footer

One short paragraph, not three. Name the ephemeris, the zodiac and house system, the birth data
used, and the date prepared. Then one sentence: these are symbolic traditions, not predictive
instruments — the arithmetic is exact, what it is taken to mean is tradition and belief. Read as a
portrait, not a forecast. Then who it was made for and by whom.

## Exporting a PDF

People ask for one. Do not screenshot the page — render it properly:

```bash
python3 - <<'EOF'
h=open('report.html').read()
css=open('scripts/print.css').read()
open('report-print.html','w').write(
  '<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8">'
  '<title>NAME — Natal Chart &amp; Numerology</title><style>body{margin:0}</style>'
  + h + css + '</body></html>')
EOF

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --virtual-time-budget=25000 \
  --run-all-compositor-stages-before-draw --print-to-pdf-no-header --no-pdf-header-footer \
  --print-to-pdf="NAME — Natal Chart & Numerology.pdf" "file://$PWD/report-print.html"
```

`scripts/print.css` handles the four things that otherwise go wrong:

1. **`data-theme="light"` on `<html>`** — otherwise a dark-mode host prints white text on cream.
2. **`print-color-adjust: exact`** — without it Chrome drops every panel and background and you get
   plain text on white.
3. **The canvas wheel mattes to white.** A transparent canvas gets a white box behind it in the PDF.
   Fixed in `wheel.js` by painting `--ground` over the canvas before drawing, plus a real inset
   plate on `.chartbox` — which also looks deliberate on screen. Keep both.
4. **Page breaks.** Short card-shaped things (`.plate`, `.card`, `.pin`, `.kin`, `.ky`, `.lsc`) get
   `break-inside: avoid`. Long prose blocks (`.mcard`, `.qcard`, `.callout`, `.bridge`) get
   `break-inside: auto` and the tall two-column grids collapse to one column — otherwise unbreakable
   rows strand half-empty pages. Getting this wrong cost five wasted pages out of thirty-one.

The header is a flex-centred cover page with `break-after: page`. Expect roughly 26 pages at Letter.
Verify by reading the finished PDF, not by assuming — check the cover, one card-heavy spread, and
the last page.

## Publishing

Artifact, favicon `🌙`, title exactly `<Full Name> — Natal Chart & Numerology`. Artifacts are
private; tell the person they can share it from the page's share menu. To revise later, republish
the same file path, or pass the existing artifact URL as `url`.

## What NOT to do

- Do not lead with, or pad the report with, tables, letter-by-letter breakdowns or method
  explanation — the first draft of a past report was rejected for exactly that.
- Do not use an unreduced master Life Path in the pinnacle-age formula (`36 − Life Path`,
  reduce 11→2, 22→4, 33→6 first).
- Do not screenshot the page for a PDF; render it with `scripts/print.css`.
- Do not overclaim convergence between traditions; see the traps in Verification.

## Done when

The Artifact is published under the exact title `<Full Name> — Natal Chart & Numerology`,
every Verification item passed, any requested PDF was opened and checked (cover, one
card-heavy spread, last page), and the user has been told how to share it.
