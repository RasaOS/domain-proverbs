# Natal Report — Specification

The formal specification of the deliverable the `natal-report` skill
produces. `SKILL.md` carries the judgment and the process; this file
carries the contract. **Where the two disagree, this file wins** — the
same rule the domain applies between a framework chapter and a skill.
Versioned with the Element; changing anything here is at least a minor
bump (§12).

---

## 1. The deliverable

One self-contained HTML document, published as one Artifact titled
exactly

```
<Full Birth Name> — Natal Chart & Numerology
```

optionally exported to one Letter-size PDF of the same name. It is
written **to** the subject, in the second person, usually commissioned
as a gift by someone who knows them. The governing rule, from which
every other rule descends:

> **Write about the person, not about the method.** The arithmetic is
> exact and almost entirely invisible. A reader who knows nothing about
> astrology and never learns any must be able to read the whole report
> and feel accurately seen.

The deliverable is **symbolic, not predictive**; the footer says so and
the body never claims otherwise.

## 2. Input — `birth.json`

One JSON object. `templates/birth.example.json` is a filled example;
`chart.py --example` prints a skeleton.

| Field | Required | Type | Meaning |
|---|---|---|---|
| `name` | **yes** | string | Full name **as on the birth certificate** — middle names count. Diacritics are folded, hyphens and apostrophes dropped, for the letter arithmetic. |
| `date` | **yes** | `YYYY-MM-DD` | Birth date, local calendar. |
| `time` | no | `HH:MM` or `null` | 24-hour **local clock** time. `null` means unknown — **never guess one.** |
| `utc_offset` | with `time` | number | Hours east of UTC, DST included, **for that date, place and year.** The single most common source of a wrong Ascendant. |
| `tz_label` | no | string | Display label, e.g. `CST`. Falls back to `UTC−6`. |
| `place` | no | string | Display name of the birthplace. |
| `lat`, `lon` | with `time` | number | Decimal degrees, +N / +E. |
| `pronouns` | no | string or `null` | Only if the subject stated them. `null` → "you" throughout; the gate warns on any gendered pronoun. |
| `prepared` | no | `YYYY-MM-DD` | The date the reading is made. Default: today. Drives age, the current chapter, the current year. |
| `for` | no | string | Footer dedication name. Default: `name`. |
| `from` | no | string | Footer sign-off ("with affection, from *a friend*"). Omitted if absent. |

Keys beginning with `_` are ignored (comments).

**Without `time`** the engine computes for noon UT: no angles, no
houses, no sect, no Part of Fortune, no angle aspects, and a Moon that
may be several degrees off. The report then omits §5 row 6, replaces
the Rising card with a plain statement, and says in the Big Three that
roughly half of what a chart can say is missing.

## 3. Computed source — `chart.json`

`scripts/chart.py birth.json` writes `chart.json`, schema
`natal-report/chart.v1`. It is the **only** source the later steps read;
nothing in the report is computed anywhere else.

| Key | Contents |
|---|---|
| `birth`, `has_time`, `jd_ut`, `labels` | Echoed input; display strings (`date_long`, `time_label`, `prepared_long`, `age_at_prepared`, `day_month`). |
| `meta` | `unavailable` (e.g. Chiron without its ephemeris file), `moon_uncertain`, and a note to repeat in the report when there is no time. |
| `bodies` | Sun … Pluto, Chiron, True Node, Lilith: `lon`, `sign`, `deg`, `min`, `fmt`, `decan`, `retrograde`, `house` (whole-sign), `house_quadrant` (Placidus), `glyph`. |
| `angles`, `chart_ruler`, `houses`, `house_disagreements`, `stellium_houses`, `stellium_signs` | Angles and the twelve whole-sign houses with occupants; where whole-sign and quadrant disagree; any house or sign holding three or more bodies. |
| `sect`, `saturn_in_sect`, `mars_in_sect`, `part_of_fortune`, `altitudes`, `moon_phase` | Sect by the Sun's house. **Saturn is diurnal:** in sect by day, harsher by night. Lights' true altitude settles above/below-horizon arguments. |
| `aspects`, `tightest_aspect` | Sorted by orb. Orbs: 8° for a light, 6° otherwise, 3° quincunx, 6° to an angle. `kind` ∈ `cnj`/`hard`/`soft`/`null`. |
| `balance` | Weighted element and modality counts (Sun/Moon/ASC 3, Mercury/Venus/Mars/MC 2, rest 1). |
| `numerology` | The six numbers, `masters`, `tally`, `karmic_lessons`, `hidden_passion`, `balance_number`, `chaldean`, `kabbalistic` (letter · card · attribution), `vedic` (psychic · destiny · name, each with its planet), `lo_shu` (grid · missing · strongest), `pinnacles` (with ages and `current`), `challenges`, `personal_years` (with `current`). |
| `timing` | Saturn, Jupiter, nodal and Chiron returns; Uranus opposition; Neptune and Pluto squares (date + age); progressed Sun by decade and now; progressed Moon now. |
| `wheel` | Exactly what `wheel.js` draws — see §6. |

**Conventions, fixed:** tropical zodiac; whole-sign houses (quadrant
reported only for disagreements); Pythagorean letter values on the full
birth name with **Y as a consonant**; Life Path by the
reduce-each-component method, the all-digit method reported alongside
and **never put on the page**; masters 11/22/33 kept in the six numbers
and pinnacles, reduced for challenges and personal years; pinnacle ages
from `36 − Life Path` with a master Life Path reduced first (11→2, 22→4,
33→6); Lo Shu from the digits of day, month and full year, zeros
dropped; Kabbalistic path = Expression total mod 22 under the Golden
Dawn attributions, 0 → Tav.

## 4. The pipeline

```
1  birth.json                       collect inputs; confirm DST for that date, place, year
2  scripts/chart.py birth.json      → chart.json + the writer's working summary on stdout
3  scripts/build.py chart.json      → report.html: machinery filled, prose slots left as {{WRITE: …}}
4  write                            fill every slot in report.html; delete slots marked optional
5  scripts/check-report.py report.html --chart chart.json     the conformance gate (§9)
6  the human pass                   doctrine · arithmetic · leaked method · overclaimed convergence
7  publish                          the Artifact; scripts/build.py --pdf report.html if a PDF is wanted
```

Ownership is strict and never crosses:

| Owner | What | Marker |
|---|---|---|
| **Machine** (`build.py`) | title, name, dateline, glyphs, signs, house labels, the six numerals and master chips, the four chapter numerals and ranges and the Now chip, the positions table, the wheel data and renderer, the footer's data sentence, the prepared/for/from line, the conditional sections | `{{UPPER_CASE}}` tokens, `<!-- @if … -->` blocks |
| **Writer** | every sentence a reader reads | `{{WRITE: guidance}}` slots |

The writer never edits a machine-filled value; the gate (R16) checks
that the numbers on the page are still the ones in `chart.json`. The
machine never writes a sentence of meaning.

## 5. Structure

In this order. `data-sec` is the identity the gate checks; the title
is the default and ★ marks the sections that carry the meaning — give
them the most room. "When" = always unless stated.

| # | `data-sec` | Title | Eyebrow | Components | Budget | When |
|---|---|---|---|---|---|---|
| — | `header` | *name* | Natal Chart & Numerology · A Reading | `.eyebrow` `h1` `.dateline` `.hero` (`.lede` + `.chartbox`) | lede 60–90 w | |
| 1 ★ | `portrait` | The Portrait | Who you are, in full | `.prose.p-body` (drop cap) + `.p-close` | **1100–1300 w**, 6–9 ¶ | |
| 2 | `big-three` | The Big Three | Sun · Rising · Moon | `.three` › 3 × `.card` | 110–160 w each | Rising card replaced by a statement when no time |
| 3 ★ | `gravity` | *named for the meaning* (e.g. The House of Home) | *writer's* | `.prose` | 550–800 w | |
| 4 | `sun` | Your Sun in Depth | The core self, unpacked | `.signband` · `.prose` · `.callout` (the face of the sign + house) · `.pair` › `.ky` / `.ky.shadow` | 350–500 + 120–180 + 2 × 70–110 w | |
| 5 | `world` | How You Meet the World | The door, and who comes through it | `.prose` | 350–550 w | **only with a birth time** |
| 6 | `numbers` | The Six Numbers | What they say about you | `.plates` › 6 × `.plate` · `.callout` (what the name failed to supply) | 80–120 w each + 120–200 | |
| 7 ★ | `masters` | *named for the meaning* (e.g. The Live Wire) | *writer's* | `.prose` · `.mcards` › `.mcard` (+ `.pair`) · `.bridge` (the one convergence to keep) | 150–220 + 180–260 + 150–220 w | **only if a master number is present** |
| 8 ★ | `nodes` | What You Are Here to Learn | The growth axis | `.prose` | 500–750 w | |
| 9 | `work` | How You Work | Vocation · Money · Worth | `.prose` | 450–700 w | |
| 10 ★ | `wounds` | What Wounds You | And what actually helps | `.prose` | 450–700 w | |
| 11 | `traditions` | The Other Traditions | Four more readings of the same person | `.prose` intro · `.traditions` › 4 × `.tradcard` (Chaldean · Vedic · Kabbalistic · Lo Shu) · `.synth` *Where they land together* | 80–120 w each + 150–220 | |
| 12 | `arc` | Life Arc | Been · Are · Going | `.ls` › 4 × `.lsc` (been · are · going · `.purpose`) | 130–200 w each | |
| 13 | `road` | The Road Ahead | The four chapters | `.pins` › 4 × `.pin` · `.callout` (the next threshold) · `.sub-head` + `.tbl` (further out) | 50–80 w each + 150–220 + 3–6 rows | |
| 14 | `love` | Love & Matches | Need · Pull · Repair | `.prose` · `.pullneed` › `.need` / `.pull` · `.mline` · 2 × `.match` · 2 × `.callout` | 300–450 + 2 × 90–130 + 130–200 + 110–170 + 2 × ~150 w | |
| 15 | `kindred` | Kindred Spirits | Good company on the same road | 4 × `.kin-group` (same day · same road · same sign · same gift) › `.kins` › `.kin` · `.mono-line` | 6–20 chips each, **dates verified** | |
| 16 | `chart` | The Chart Itself | For the curious | `.tbl` positions table | machine | |
| — | `footer` | | | three short paragraphs (§10) | | |

The synthesis ("where it all rhymes") lives as the closing `.synth`
panel of §11, not as its own section. Nothing that is mostly a table
survives except the positions appendix: no aspect grid, no
letter-by-letter breakdown, no element-balance chart.

## 6. Components — the class vocabulary

Defined in `templates/report.html`; print behaviour in
`scripts/print.css`. These names are the contract between the three
files — rename in all or none.

| Class | What it is | In print |
|---|---|---|
| `.page` `.wrap` | ground + 940 px column | full width |
| `.eyebrow` `.brow` `.lab` `.tag` `.sub` | mono uppercase labels (page, section-right, card, tradition, master-card subtitle) | |
| `.sec-head` › `h2` `.rule` `.brow` | section head: serif title, hairline, eyebrow right | `h2` never orphaned |
| `.hero` › `.lede` `.chartbox` › `canvas#wheel` | cover panel: lede left, wheel right on an inset plate | cover page, `break-after: page` |
| `.prose` | body paragraphs; `em` = brass serif italic, `strong` = serif bold | may split |
| `.portrait .p-body` `.p-close` | drop-cap body, centred italic close | |
| `.three` › `.card` (`.glyph` `.lab` `h3` `.epi` `p`) | the Big Three | whole |
| `.signband` (`.glyph` `h3 b` `.motto`) | the Sun's banner | whole |
| `.callout` (`h3` `p`) | brass-rule aside | may split |
| `.pair` › `.ky` / `.ky.shadow` | best / shadow (or cost, hazard) two-up | whole |
| `.plates` › `.plate` (`.num` `.lab` `h3` `p` `.chip`) `.plate.master` | the six numbers | whole |
| `.mcards` › `.mcard` (`.head` › `.bignum` `h3` `.sub`; `p`; `.pair`) | master-number card | may split; stacks |
| `.bridge` (`.bridge-chip` `h3` `p`) | dashed "the one to keep" convergence | may split |
| `.traditions` › `.tradcard` (`h3` + `.tag`, `p`) · `.synth` | the four traditions and their synthesis | whole / may split |
| `.ls` › `.lsc` `.lsc.purpose` | life-arc cards | whole |
| `.pins` › `.pin` `.pin.now` (`.now-chip` `.num` `h3` `.range` `p`) | the four chapters | whole, 4-up |
| `.sub-head` · `.tbl` › `table` (`td.k` for year · age; `td.g` `td.pos` in the positions table) | further-out thresholds; positions | rows whole, head repeats |
| `.pullneed` › `.need` / `.pull` · `.mline` · `.match` | love | whole / may split |
| `.kin-group` › `.kins` › `.kin` `.kin.hi` (`b` `span`) · `.kin-note` · `.mono-line` | kindred | chips whole, group may split |
| `footer` | three mono paragraphs | |

### The wheel

`scripts/wheel.js` reads `window.NATAL_WHEEL`, which `build.py` injects
verbatim from `chart.json#wheel`: `asc`, `mc` (or `null`), `bodies`
(`lon`, `g` glyph, `t` degree label, `w` = 1 for Sun/Moon/Mercury/Venus/
Mars), and `aspects` as `[i, j, kind]` among the drawn bodies — Lilith is
never drawn, the Node is drawn but has no aspect lines; cnj ≤ 6°, hard
≤ 5°, soft ≤ 4°. Ascendant on the left; no time → 0° Aries on the left
and no axes. Colours come from the CSS tokens, so one renderer serves
both themes; it mattes the canvas to `--ground` first so a PDF never
gets a white box behind it.

**The gotcha that bites:** a crowded house collides. Naive angular
relaxation lets glyphs cross, after which array-adjacent items are no
longer circle-adjacent and the gap test passes on a false ~347° gap.
`spread()` is order-preserving on purpose — cut the circle at its
largest gap, clamp forward then backward, re-centre each rigid block on
its members' true mean — and leader lines run from the true degree to
the displaced glyph. Verify by rendering and *looking*, in both themes.

## 7. Design tokens

All defined on bare `:root`, redefined under
`@media (prefers-color-scheme:dark){:root:not([data-theme="light"])}`
**and** `:root[data-theme="dark"]` — both, so the host's preference and
an explicit attribute each work, and the PDF can force light.

| Token | Light | Dark | Role |
|---|---|---|---|
| `--ground` | `#f3ead6` | `#0b1322` | page |
| `--panel` / `--panel-deep` | `#ece0c6` / `#e3d3b2` | `#111b2e` / `#172339` | cards / emphasis |
| `--ink` / `--ink-soft` / `--ink-faint` | `#241c10` / `#4a3f2e` / `#8a7b63` | `#ece7d7` / `#c9c2ae` / `#8d8873` | text tiers |
| `--brass` / `--brass-bright` | `#9a6a12` / `#b8831a` | `#d9b364` / `#e8c87c` | accent |
| `--star` | `#3c5a7c` | `#8ba7cc` | secondary (shadow, need, sign glyphs) |
| `--line` | `#d8c9a6` | `#263650` | hairlines |
| `--wheel-ring` / `--wheel-tick` / `--wheel-web` | `#b89a5e` / `#c9b283` / `#d9c7a1` | `#8a7a52` / `#5c5a4a` / `#2c3a52` | wheel |

Type: `--serif` "Iowan Old Style", Palatino, Georgia for display, the
Portrait body and card titles; `--sans` system for body; `--mono` for
labels, eyebrows, datelines, the footer. Favicon 🌙. No other colours,
no other faces.

## 8. Writing rules

✓ = checked mechanically by `check-report.py` (§9). The rest are
checked by the human pass and are no less binding.

- **W-1 ✓ Nothing of the method on the page.** No arithmetic, no
  arrows, no "reduces to", no mod 22, no letter or digit sums, no method
  named, no dispute between methods. Resolve silently; state one answer.
- **W-2 Every placement earns its sentence.** A placement or figure
  named without the sentence going on to what it means for them is a
  defect. Ratio: at most one clause of astrology to three of meaning.
  Technique words (stellium, decan, orb, node, pinnacle, …) are warned
  on ✓ — occasionally one honest sentence earns one.
- **W-3 ✓ At most one or two exact figures survive the whole report**,
  and only where the precision itself is the point.
- **W-4 Lived texture over abstraction.** What it feels like from
  inside, what others notice, what they keep doing that doesn't work,
  what they're good at without trying. Concrete situations.
- **W-5 The shadow as plainly as the gift.** Honest, never cruel. A
  reading that only flatters is worthless; this is a gift.
- **W-6 ✓ Second person**, warm, literate, grown-up. American spelling
  ✓. No emoji ✓, no exclamation marks ✓.
- **W-7 ✓ Never gender the subject** unless they stated pronouns.
- **W-8 ✓ Banned:** cosmic blueprint · the universe is telling you ·
  divine timing · your soul chose · old soul · on a deep level ·
  "journey" as a noun for a life · "energy" as a mass noun · vibration ·
  manifest · soulmate · written in the stars.
- **W-9 ✓ Never open a section by restating its own title.**
- **W-10 Name the meaning, not the technique**, in any title the writer
  supplies (§5 rows 3, 7). Never "The Stellium".
- **W-11 Interpret symbolism; never predict events.** Thresholds are
  "a doorway", "a season", "worth marking" — never "X will happen".
- **W-12 Convergence is claimed only where the inputs don't overlap.**
  Two letter systems agreeing is weak (same letters; totals differing by
  a multiple of 9 share a digital root). A surname's own master number
  is a component of the full-name total, not a second arrival. Vedic
  destiny and the Life Path come from the same date digits: one
  signature. A Kabbalistic path landing on a sign in the chart is
  one-in-twelve. The strong kind: a number from the letters of a name
  matching a contact measured from the sky.
- **W-13 Nodes the right way round.** South = the over-practised
  default groove; North = the unpractised direction that grows them.
- **W-14 Sect the right way round.** Saturn is diurnal: harsher in a
  night chart. Uranus, Neptune, Pluto have no sect.
- **W-15 ✓ Kindred dates verified.** Every chip carries a year; every
  year and Life Path and Sun sign is recomputed from a published birth
  date before it goes on the page.

## 9. Conformance

`scripts/check-report.py report.html --chart chart.json` — exit 0
required before publishing. `--strict` also fails on warnings.

| Rule | Checks | Severity |
|---|---|---|
| R1 | no `{{WRITE: …}}` slot or machine token left | error |
| R2 | `<title>` = `<h1> — Natal Chart & Numerology`; h1 = `birth.name` | error |
| R3 | every required `data-sec` present, in §5 order, no duplicates; `world` iff a time, `masters` iff a master | error |
| R4 | Portrait 1100–1300 words (hard fail outside 1000–1450); close lines present; lede 40–110 | error / warn |
| R5 | W-8 banned phrases | error |
| R6 | W-1 leaks (error) · W-2 technique words (warn) | error / warn |
| R7 | exclamation marks, emoji | error |
| R8 | gendered pronouns outside Kindred, when no pronouns stated | warn |
| R9 | exact figures in prose: >2 warn, >4 error | warn / error |
| R10 | footer names the Swiss Ephemeris, says symbolic, "portrait, not a forecast", Prepared | error |
| R11 | tokens and both dark-theme selectors present; the serif named | error |
| R12 | `canvas#wheel` + `NATAL_WHEEL` present and equal to `chart.json#wheel` | error |
| R13 | W-9 section openers | warn |
| R14 | British spellings | warn |
| R15 | kindred chips carry a year; ≥ 12 chips; no empty notes | error / warn |
| R16 | the six numbers, the four chapter numbers, the single Now chip and the positions rows match `chart.json` | error |
| R17 | ≥ 80 second-person references | warn |

**The human pass** happens after the gate and is not optional — the
gate checks shape, not truth:

- **V-1 Doctrine.** Sect (W-14), nodes (W-13), the house and sign of
  every body named, retrogrades, phase.
- **V-2 Arithmetic, recomputed independently** — every letter sum,
  personal year, pinnacle, and every kindred person's Life Path and Sun
  sign.
- **V-3 Leaked method** — read every paragraph for anything that
  survived W-1 and W-2 in a form the regexes don't know.
- **V-4 Overclaimed convergence** — every "both systems agree" against
  W-12; state the dependence or drop the claim.
- **V-5 The wheel, by eye**, in both themes, and the PDF: the cover,
  one card-heavy spread, the last page.

## 10. The footer

Three short paragraphs, mono, in this order:

1. *Data.* "Computed with the Swiss Ephemeris for *date, time tz,
   place* — tropical zodiac, whole-sign houses. The numerology is
   Pythagorean, from the full birth name, with four other traditions
   read alongside it. Every figure was independently rechecked; where
   methods disagreed, the mainstream reading was used." (Machine
   supplies the first two sentences; the no-time variant says noon UT
   and no houses.)
2. *Stance.* "Astrology and numerology are symbolic traditions, not
   predictive instruments. The arithmetic is exact; what it is taken to
   mean is a matter of a long human tradition and of belief. Nothing
   here forecasts an event. Read it as a portrait, not a forecast — and
   keep the parts that are useful."
3. *Dedication.* "Prepared *date* · for *name* · with affection, from
   *from*."

## 11. PDF export

`scripts/build.py --pdf report.html` refuses an unfilled report, writes
`report-print.html` (the report with `data-theme="light"` forced on
`<html>` and `scripts/print.css` appended), and prints it with headless
Chrome (`CHROME=` overrides the binary) to
`<Name> — Natal Chart & Numerology.pdf`. Letter, ~26 pages. Never a
screenshot.

`print.css` handles the four things that otherwise go wrong: the forced
light theme (a dark host otherwise prints white on cream);
`print-color-adjust: exact` (Chrome otherwise drops every panel); the
canvas matte (a transparent canvas gets a white box); and page breaks —
card-shaped things (`.card .plate .pin .lsc .ky .signband .hero .kin
.tradcard .need .pull`) stay whole, long prose blocks (`.mcard
.callout .bridge .synth .match .kin-group`) may split, table rows stay
whole with the head repeated, the header is a centred cover page. Sign
glyphs carry U+FE0E (text presentation) or Chrome prints colour emoji.

## 12. Publishing and change control

Artifact, favicon 🌙, title exactly as §1; Artifacts are private, and
the person is told they can share from the page's share menu. Revising
later republishes the same path or passes the existing URL. Confirm
with the user before the first publish for a person. Reports are
deliverables, never Element content: no example report is ever
committed — they are private gifts about real people.

Changing this specification:

| Change | Bump |
|---|---|
| a guidance slot's wording, a budget, a tolerance in the gate, a token value | patch |
| a new optional slot, component, gate rule, `chart.json` key, or `birth.json` field | minor |
| a section added/removed/reordered, a class renamed, a `chart.json` key renamed or removed (schema → `chart.v2`), a convention in §3 changed | major |

Any change lands in all of `templates/report.html`, `scripts/print.css`,
`scripts/check-report.py` and this file together, and in `CHANGELOG.md`.
