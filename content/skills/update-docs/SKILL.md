---
name: update-docs
description: Pause and reconcile documentation against reality. Discovers the docs that actually exist in this project, checks each claim against the real state of the code/content, flags what's drifted, and proposes surgical edits — report first, apply only on approval. Domain-agnostic: it reconciles whatever docs the project has, not a fixed list. Triggered when the user wants a doc-sync pass — e.g. "/update-docs", "let's check our docs", "are our docs still accurate", "make sure everything's documented properly".
---

# /update-docs — Documentation reconciliation

Stop building for a beat. Walk the docs against reality. Find the
drift. Propose edits. Don't rewrite from scratch — surgical updates
only.

Honest reporting (see `output-rules.md`): if a doc is fine, say it's
fine. If it's stale, say what's stale and why. Don't manufacture work.

> **Domain-agnostic here; subject-aware once installed.** In
> `rasa.domain.core` this skill reconciles only the universal surfaces
> below and references no subject. A fork should extend the in-scope
> inventory with its own domain's doc surfaces (a legal domain's
> `FIRM.md`, a code domain's `DEPLOY.md`/`.env.example`, etc.) when it
> adopts the skill.

## Behavior contract

- **Discover, don't assume.** Inventory the docs that actually exist in
  the repo before reconciling. Never reconcile against a hardcoded list
  a project may not have — skip what isn't there, and note doc surfaces
  you'd expect but didn't find.
- **Read before editing.** Read every doc in scope AND the code/content
  it describes. A doc is only "drifted" once you've verified the actual
  state contradicts it.
- **Propose, don't apply by default.** First pass produces a report of
  proposed changes. The user approves which to apply. Edits happen only
  after explicit approval.
- **Surgical edits.** Change only what's drifted. Don't rewrite a
  paragraph because one sentence is wrong. Don't reformat. Don't
  "improve" prose that's accurate.
- **No new docs unless asked.** This skill reconciles existing docs; it
  doesn't invent new ones. If a gap genuinely needs a new doc, propose
  it in the report and let the user decide.
- **Don't touch user-voice docs** (vision, marketing copy, personal
  notes) without asking — flag them in ⚪ Notes instead.
- **Honest about confidence.** "This is wrong, the code says X" vs "I
  think this is stale but couldn't fully verify" — distinguish them.
- **Never commit.** Edits land in the working tree for the user's
  normal git review.

## Doc surfaces in scope

Walk whatever of these **exists**; skip the rest. This is the universal
baseline — a fork extends it with its own subject docs.

**Repo-level:**
- `README.md` — the front door: does what it claims match what's here?
- `CLAUDE.md` — the working contract: do its stated conventions, layout,
  and source-of-truth pointers still hold?
- Any `docs/` directory.
- Any project manifest/config that documents how things run (discover
  it; don't assume a language) — does it match what the docs say?

**Element / install surfaces (if this is a rasa Element or a project
installed from one):**
- `.claude/rasa.lock.json` — does the recorded Element identity, pin,
  and `overrides[]` match what's actually installed and edited? Flag
  unmanaged drift (an Element file edited but not recorded as an
  override — see `contract-rules.md`).
- `rasa.json` — for an Element repo, does the manifest describe what's
  actually on disk? (Coverage/dangling is `bin/check-manifest`'s job —
  defer the mechanical check to it and just confirm it passes.)
- Rule files (`*rules*.md`, `content/rules/` or `.claude/`) — do the
  documented rules still match how work is actually done?
- Skill files (`*/SKILL.md`) — does each skill's frontmatter
  `description` (its trigger surface) still match what the skill body
  actually does?
- `CHANGELOG.md` / `VERSION` — does the top entry reflect the latest
  shipped state, and do `VERSION` and `rasa.json#version` agree?

## Process

### Step 1 — Inventory
List every in-scope doc that exists. Output a one-line "found N docs"
header so the user sees the surface area, and note any expected-but-
missing surfaces.

### Step 2 — Reconcile
For each doc, compare its claims to reality. Read the code/content it
describes; don't infer. For each finding record:
- **Doc + section** (file path + heading or line range)
- **Claim in doc** (quoted when wording matters)
- **Reality** (what the code/state actually shows, with `path:line`)
- **Severity** (rubric below)
- **Proposed edit** (the specific change, ready to apply)

### Step 3 — Report
Render findings using the structure below. Stop and wait for approval
before editing anything.

### Step 4 — Apply (only after approval)
Apply only what the user approves. `Edit` for surgical changes; `Write`
only for a full rewrite the user explicitly requested. Don't commit.

## Severity rubric

- **🔴 Wrong** — the doc says something the code contradicts. A reader
  will be misled or break their setup. Fix with priority.
- **🟡 Stale** — missing recent additions or describing a previous
  state. Not actively misleading, but incomplete.
- **🟢 Drift-watch** — small inconsistencies (a renamed file, a
  reordered section). Worth fixing in the same pass.
- **⚪ Note** — not a doc bug, but worth surfacing (e.g. "this section
  has grown to 200 lines, consider splitting"). User decides.

## Output structure

```markdown
# 📚 Documentation reconciliation

> **Headline.** <one-sentence read on overall doc health.>

**Docs reviewed.** <count> — <comma list of paths>
**Areas cross-checked.** <short list of code/content areas>
**Expected but missing.** <surfaces you'd expect and didn't find, or "none">

---

## 🔴 Wrong — fix these

### 1. `path/to/doc.md` — <section>

**Doc says:**
> <quoted claim>

**Reality:**
<what the code/state actually shows, with `path:line`>

**Proposed edit:**
```diff
- <old line>
+ <new line>
```

---

## 🟡 Stale — should update
*(same shape)*

---

## 🟢 Drift-watch — small fixes
- `path/to/doc.md:line` — <one-line description + proposed change>

---

## ⚪ Notes — surfacing for your call
- <observation, no edit proposed>

---

## ✅ Verified accurate
Docs (or sections) you read and confirmed still correct — so the user
knows the silence isn't laziness.
- `README.md` — install / run section
- …

---

## Bottom line
<2–4 sentences. Recommended action — "apply all 🔴 + 🟡", "🔴 only,
defer the rest", or "docs are in good shape". Be direct.>

**Next step.** <tell me which to apply — "all red", "everything", or
"skip" — and I'll edit accordingly.>
```

## Style rules

- **Cite `path:line` for every reality claim.** Receipts, not vibes.
- **Quote the doc, don't paraphrase, when wording matters.** If you say
  it's wrong, the reader needs to see what "it" is.
- **Diff blocks for proposed edits.** `- old` / `+ new` scans fastest.
- **Don't grade.** No "B+ on docs" — use the headline + bottom line.
- **No "you might want to consider".** Propose the edit concretely, or
  say you're not proposing one.

## What NOT to do

- **Don't apply edits in the report pass.** Report first; edit on
  approval.
- **Don't reformat for taste.** Match local style (wrap width, trailing
  spaces, heading style).
- **Don't add doc sections the user didn't ask for.**
- **Don't edit user-voice docs** without asking — flag in ⚪ Notes.
- **Don't commit.**

## When NOT to use this skill

- **Writing one new doc** → just write it; skip the report-then-apply
  flow for a single file.
- **Reconciling the manifest against disk** → that's `bin/check-manifest`
  (coverage/dangling); this skill only confirms it passes.
- **Orienting a fresh session** → use `onboard` (read-only briefing).
- **Capturing a rule that emerged mid-session** → use `codify`.
- **Pulling upstream Element changes** → use `sync`.

## Done when

The user leaves with one or more of:
- A clear report of what's drifted, ready to triage.
- Approved edits applied surgically across the affected docs.
- Confidence that the docs reflect reality again.

"Everything's accurate, nothing to do" is a valid outcome. Don't
manufacture work to justify the run.
