---
name: natal-report
description: Produce a full natal-chart-and-numerology reading for a person, published as an Artifact in the house format and optionally as a PDF. Use when asked for "a natal chart", "a birth chart", "an astrology reading", "a numerology report", "the full report" for someone's birth details, or "/natal-report". Writes files in the working folder and publishes one Artifact; computes with Swiss Ephemeris; the format is fixed by REPORT-SPEC.md and gated by scripts/check-report.py.
user-invocable: true
---

# /natal-report — Natal Chart & Numerology reading

Produces one deliverable: an Artifact titled **`<Full Name> — Natal Chart & Numerology`**,
written *to* the subject, usually commissioned as a gift by someone who knows them.

**The contract is `REPORT-SPEC.md` in this folder** — inputs, the computed source, the
sixteen sections and their budgets, the component vocabulary, the design tokens, the
writing rules, the gate, the footer, the PDF. This file carries the judgment and the
process. Where they disagree, the spec wins.

## Behavior contract

- **Writes files and publishes.** In the working folder: `birth.json`, `chart.json`,
  `report.html`, and a PDF on request. Publishes one Artifact. Publishing is
  outward-facing — confirm with the user before the first publish for a person.
- **Meaning about the person, never the method.** The arithmetic is exact and almost
  entirely invisible. Every paragraph passes one test: *does this tell them something
  about their life?*
- **Never guess missing inputs.** No birth time means no Ascendant, Midheaven, houses or
  sect — the report says so and the layout drops what cannot be known. Never invent a
  time; never infer pronouns from a name.
- **Machine parts are machine-owned.** Numbers, signs, glyphs, the wheel, the positions
  table and the footer's data sentence come from `chart.json` via `build.py` and are
  never retyped by hand; the gate checks they still match.
- **Symbolic, not predictive.** The footer states it; the body never claims prediction.
- **Never auto-commit, never commit a report.** Reports are private gifts about real
  people, not Element content.

## Process

1. **Collect inputs** into `birth.json` (`scripts/chart.py --example` prints the
   skeleton; spec §2). Required: full birth name as on the certificate, birth date.
   Wanted: time and place. **Confirm DST for that date, in that jurisdiction, in that
   year** — the wrong offset is the single most common source of a wrong Ascendant.
2. **Compute:** `python3 scripts/chart.py birth.json` → `chart.json` and the working
   summary. Read the summary like a brief: sect, the tightest aspect, any stellium, the
   whole-sign/quadrant disagreements, the masters, what the name failed to supply, the
   current chapter and year, the thresholds ahead.
3. **Draft:** `python3 scripts/build.py chart.json` → `report.html` with every machine
   part filled and every prose slot marked `{{WRITE: guidance}}`.
4. **Write** every slot, in the house voice (spec §8), to the budgets in the guidance.
   The Portrait first — it must stand alone. Then the ★ sections (centre of gravity,
   masters, nodes, wounds) — they carry the meaning. Delete slots marked optional
   that do not apply. Never touch a filled token.
5. **Gate:** `python3 scripts/check-report.py report.html --chart chart.json` until it
   exits 0. Then the **human pass** (spec §9, V-1 to V-5): doctrine, arithmetic
   recomputed, leaked method, overclaimed convergence, the wheel by eye in both themes.
6. **Publish** the Artifact (spec §12). If a PDF is asked for:
   `python3 scripts/build.py --pdf report.html`, then open it and look at the cover,
   one card-heavy spread, and the last page.

## The rule that governs everything

**Write about the person, not about the method.**

An earlier version of this report was rejected for "too much explanations and numbering
breakdowns" and not enough about "what everything means for that person." A reader who
knows nothing about astrology and never learns any should be able to read the whole
report and feel accurately seen.

Concrete situations over abstractions: *"You will notice the guest nobody is talking to,
and you will go over, and you will not experience it as a decision"* beats *"Libra rising
indicates social awareness."* The shadow named as plainly as the gift — honest, never
cruel. At most one clause of astrology to three of meaning. Second person, warm, literate,
grown-up, American spelling, no emoji, no exclamation marks. The banned phrases, the
technique words to avoid and the convergence traps are enumerated in spec §8 and the
gate catches the mechanical ones.

## Toolchain

```bash
pip3 install pyswisseph                       # Swiss Ephemeris; arcsecond-accurate, no data files for the planets
curl -sL -o scripts/ephe/seas_18.se1 \
  https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1   # Chiron only
```

| File | Role |
|---|---|
| `REPORT-SPEC.md` | the contract |
| `templates/birth.example.json` | the input shape, fictional subject |
| `templates/report.html` | the house template — tokens, slots, every component and token |
| `scripts/chart.py` | `birth.json` → `chart.json` + summary |
| `scripts/build.py` | `chart.json` + template → draft; `--pdf` export |
| `scripts/check-report.py` | the conformance gate |
| `scripts/wheel.js` | the chart wheel, data-driven, order-preserving spread |
| `scripts/print.css` | the print stylesheet |

Conventions are fixed in spec §3: tropical, whole-sign, Pythagorean on the full name.
Where methods disagree, pick the mainstream one and state a single answer — the reader
gets the conclusion, not the argument.

## What NOT to do

- Do not lead with, or pad the report with, tables, letter-by-letter breakdowns or
  method explanation — the first draft of a past report was rejected for exactly that.
- Do not name a section after the technique ("The Stellium"); name it for the meaning.
- Do not retype a number, sign or position by hand; rebuild from `chart.json`.
- Do not use an unreduced master Life Path in the pinnacle-age formula (`36 − Life
  Path`, 11→2, 22→4, 33→6 first) — `chart.py` does this; do not "correct" it.
- Do not overclaim convergence between traditions; see spec §8 W-12.
- Do not get the nodes or sect backwards: South Node = practised default, North =
  growth; Saturn is diurnal and harsher by night.
- Do not screenshot the page for a PDF; `build.py --pdf` renders it properly.
- Do not publish on a red gate, and do not skip the human pass because the gate is green.
- Do not commit `birth.json`, `chart.json`, a report or a PDF.

## Done when

`check-report.py` exits 0 against the final `report.html` and `chart.json`; the human
pass (V-1 to V-5) found nothing or everything it found is fixed; the Artifact is
published under the exact title `<Full Name> — Natal Chart & Numerology`; any requested
PDF was opened and checked (cover, one card-heavy spread, last page); and the user has
been told how to share it.
