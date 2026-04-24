---
title: Project Canvas Redesign — Session Handoff
owner: Steve
prepared_by: Sally (bmad-agent-ux-designer)
date: 2026-04-23
session_start: 2026-04-19
purpose: >-
  Self-contained handoff so a new session (Sally returning, a different
  agent, or Steve solo) can pick up the project-canvas redesign work
  without rebuilding context.
status: in-flight — awaiting Claude Design Pass 2 output
---

# Project Canvas Redesign — Session Handoff

## TL;DR

Steve is redesigning the Momentum `feature-status` HTML artifact from a
flat status report into a **three-lens project canvas** (Features /
Sprints / Flywheel) that reads like a thinking space. Design work is
happening in Claude Design. Pass 1 landed (Variant B card grid locked
for the Features lens). Pass 2 was scoped to extend into the full
canvas; Claude Design returned 15 clarifying questions, Steve and Sally
answered them, and the next response from Claude Design is pending.

## Context

**What this is.** Momentum's `feature-status` skill currently generates
a flat single-page HTML report showing features, their states, story
counts, and gaps. It works but reads as a *report*, not a *thinking
space*. The developer's framing: *features and end-to-end workflows
are about 75% of the work; this document should close the user's
knowledge gap about what it takes to build something*.

**Why now.** DEC-006 (2026-04-14) already captured the core redesign
intent: hierarchical HTML directory (index → feature → story), dual-
audience story template, story-level dependency graph. Two backlog
stubs have been waiting for UX wireframes:

- `dashboard-ux-wireframes.md`
- `feature-dependency-graph-ux-wireframes.md`

This session started (2026-04-19) to produce those wireframes by
handing off to Claude Design. The scope then expanded.

## Scope expansion — what changed mid-session

After reviewing Pass 1's output, Steve identified that the artifact
should broaden from a feature dashboard into a **project canvas** with
three coordinated lenses sharing one design system:

1. **Features** — what the product IS. Designed in Pass 1.
2. **Sprints** — what the practice is DOING right now. New.
3. **Flywheel** — how the practice is COMPOUNDING. New.

Inspiration reference: **Cursor 3.1's Canvas view** — one rich surface,
lenses switch rather than deep nav tree. Conceptual reference only; we
generate static artifacts, not a live app.

## Current status

**Where we are:** waiting on Claude Design Pass 2 output. 15
clarifying questions were answered (see "Decisions" section below).

**What's locked from Pass 1** (inherited as primitives for all new
work — NOT open for redesign):

- Color palette: warm paper `#fbfaf7`, soft ink `#1e1d1a`, muted
  indigo accent `#5863a8`, warm terracotta gap flag `#a85a2a`.
  Terminal states at 55–75% opacity.
- Typography stack: Inter (UI), Source Serif 4 (narrative, 17px/1.65,
  68ch reading column), JetBrains Mono (meta fields).
- Badge system: active vs terminal, dot-first, monospace lowercase
  label, matched low-chroma hues.
- Variant B card grid: locked as Features-lens Level-1 layout.
  Level-2 drill-down (feature detail page) is in flight on a separate
  Claude Design pass.

**Tech decision — deliberately held open.** Static HTML with vanilla
JS worked for Pass 1. React via CDN or a small Vite step may be
justified for Flywheel interactivity. Decide AFTER seeing the
information design, not before.

## Decisions made in this session

### Canvas-level

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Scope expands from dashboard to canvas, three lenses | Features alone don't show sprint execution or practice compounding. Single surface with coordinated lenses beats three separate artifacts. |
| 2 | Pass 1 Variant B (cards) locked for Features | Half-width cmux pane is primary viewport (~700px). Card grid collapses cleanly to 1-col; table did not. |
| 3 | Target viewport is 700px (half-width cmux) | Steve's actual working width. Full-width is bonus, not target. |
| 4 | Tech stays static HTML for now; may adopt React-via-CDN later | Design information first, pick tech after. |
| 5 | Skill rename flagged but not decided — route to `momentum:decision` | `feature-status` becomes misleading if artifact broadens. Candidates: `momentum:canvas`, `momentum:project-canvas`. Decision via skill, not wireframe iteration. |

### Pass 2 direction (answered to Claude Design)

- **Format:** design-canvas first for divergent exploration; hi-fi
  prototype second, gated on reaction.
- **Nav model candidates:** tabs / sidebar / long-scroll. Slight lean
  toward long-scroll (Cursor Canvas parallel, narrow viewport favors
  vertical scroll), but all three explored honestly.
- **Flywheel directions:** Timeline + Provenance Graph. Explicitly NOT
  a metrics dashboard — fights the "no velocity/percentages" rule.
- **Quality-gate visual:** new primitive, inherited family (reuse
  palette, typography, terminal-opacity pattern; distinct shape so
  gates are glance-distinguishable from state badges).
- **Dark mode:** deferred. Lands after Flywheel direction settled.
- **Sample data:** use real story slugs from content-sample.md. Invent
  plausible retro findings in Momentum voice.

### Hard constraints (repeatedly reinforced — do not drift)

- No emoji anywhere in UI
- No percentages, no velocity, no burndown
- No "great job" / cheerleader copy
- Developer-to-developer tone
- Half-width primary (700px), full-width secondary
- Terminal states de-emphasized, not deleted

## Artifacts — where things live

### Authored this session (committed to repo)

```
_bmad-output/planning-artifacts/
├── feature-status-redesign-claude-design-brief.md        # PRIMARY BRIEF
│                                                          # §1–§13: Features view
│                                                          # §14: canvas expansion
├── feature-status-redesign-content-sample.md             # Real content for mockups
└── project-canvas-session-handoff.md                     # THIS FILE
```

### Claude Design Pass 1 output (NOT yet in repo — still in /tmp and ~/Downloads)

```
~/Downloads/Feature Status-handoff.zip        # 14 files, with README
~/Downloads/Feature Status.zip                # same 13 files, no README
/tmp/feature-status-handoff/feature-status/   # extracted snapshot (ephemeral)
```

Key files inside those zips:

- `tokens.jsx` — design tokens (palette, type stack)
- `primitives.jsx` — Badge, GapFlag, StoryFraction, TypeTag, Breadcrumb, SumStat
- `badge-system.jsx` — badge artboard
- `variant-b-cards.jsx` — locked Features Level-1 layout
- `level-two.jsx` — Features Level-2 drill-down (in-flight)
- `data.jsx` — BADGES, FEATURES, SUMMARY structures
- `Pass 1 - Density + Badges.html` — rendered reference
- `Pass 2 - Level 2 Drill-Down.html` — rendered reference

**Action item:** promote these into the repo at
`_bmad-output/planning-artifacts/claude-design-output/pass-1/` before
the download folder gets cleaned. They are the provenance for the
`dashboard-ux-wireframes` story when `create-story` is eventually run.

### Related governing decisions (pre-existing)

```
_bmad-output/planning-artifacts/decisions/
├── dec-005-cycle-redesign-feature-first-practice-2026-04-14.md
└── dec-006-artifact-redesign-dual-audience-2026-04-14.md
```

### Related backlog stubs (pre-existing, waiting to be enriched)

```
_bmad-output/implementation-artifacts/stories/
├── dashboard-ux-wireframes.md
└── feature-dependency-graph-ux-wireframes.md
```

Claude Design's output will flow into these stories via
`momentum:create-story` once the wireframes are final.

## Open questions

| Question | Owner | Notes |
|----------|-------|-------|
| Nav model — tabs vs sidebar vs long-scroll | Claude Design → Sally review | Slight prior lean to long-scroll |
| Flywheel rendering direction — timeline vs provenance graph | Claude Design → Sally review | Wait for divergent wireframes |
| Quality-gate primitive shape | Claude Design → Sally review | New primitive, inherited family |
| Skill rename (`feature-status` → ?) | Needs `momentum:decision` | Route outside wireframe loop |
| Tech choice (static HTML vs React-via-CDN) | Held open | Decide after information design stable |
| Dark mode scope | Deferred to Pass 3 | Reskin on stable structure |
| Journey / Workflow layer (brief §6 Q1) | Deferred past Pass 2 | Originally deferred from Pass 1 |

## What to do next

**If Claude Design returns with Pass 2 wireframes:**
1. Read the output. React on nav model, Flywheel direction, quality-gate primitive.
2. Iterate — push back on anything that drifts from the locked primitives or the hard constraints list.
3. Once direction is selected, ask for one hi-fi prototype of the chosen Flywheel + chosen nav model at 700px. Tweaks wired.

**If starting fresh (no response from Claude Design yet):**
Open the existing Claude Design project:

```
https://claude.ai/design/p/e1197de1-6428-4a89-a70a-fe5ca865db0c
```

Wait for or nudge the pending Pass 2 output.

**If starting a brand-new Claude Design session from scratch:**
Use the cold-start prompt drafted earlier in the conversation
(reproduced in §14 of the brief and in the prior Sally response). Upload
the brief, content sample, and the locked-primitive JSX files from
`~/Downloads/Feature Status-handoff.zip`.

**Parallel loose ends to clean up:**
- [ ] Promote Pass 1 snapshot into `_bmad-output/planning-artifacts/claude-design-output/pass-1/`
- [ ] Queue a `momentum:decision` for the skill-rename question
- [ ] Commit this handoff + brief §14 update + content sample (already written, not yet committed)
- [ ] When wireframes are final, run `momentum:create-story` on both pending backlog stubs

## Glossary — for anyone picking this up cold

- **Features view** — the "what the product is" lens. Card grid at Level 1, narrative drill-down at Level 2.
- **Sprints view** — the "what the practice is doing now" lens. New in Pass 2.
- **Flywheel view** — the "how the practice is compounding" lens. New in Pass 2. Most open design question.
- **Variant A / Variant B** — two Level-1 density treatments Claude Design produced in Pass 1. Variant A was compact table; Variant B was card grid. B won.
- **Locked primitives** — design-system elements from Pass 1 that are NOT open for redesign: palette, typography stack, badge system, terminal-state opacity.
- **Gate primitive** — proposed new visual primitive for AVFL / code-review / E2E pass/fail/pending signals per story per sprint.
- **Cursor Canvas** — Cursor 3.1's design inspiration reference. Conceptual: one surface, switchable lenses. We are not cloning it.

## Sally's signoff note

The brief is the source of truth. This handoff points to it. If
anything in this handoff contradicts the brief, the brief wins. If a
new session needs to rebuild context: read the brief first (especially
§14), then the content sample, then skim this handoff for the most-
recent state.

Voice stays the Momentum voice: direct, paragraph-style, no marketing,
no cheerleader tone. Analogies welcome, percentages not.
