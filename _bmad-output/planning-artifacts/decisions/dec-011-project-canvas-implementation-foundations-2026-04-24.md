---
id: DEC-011
title: Project Canvas Implementation Foundations — Canvas Rename, Vite Build, State Source Paths
date: '2026-04-24'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-04-24'
prior_decisions_reviewed:
  - DEC-002 (Feature Visualization and Developer Orientation)
  - DEC-003 (Feature Status Artifact Design — superseded in scope by canvas redesign)
  - DEC-005 (Momentum Cycle Redesign — Feature-First Practice)
  - DEC-006 (Artifact Redesign for Dual-Audience Legibility — direct precursor; this DEC implements it)
stories_affected:
  - dashboard-ux-wireframes
  - feature-dependency-graph-ux-wireframes
---

# DEC-011: Project Canvas Implementation Foundations — Canvas Rename, Vite Build, State Source Paths

## Summary

After seven Claude Design passes (Pass 1–7) on the project canvas redesign — landing the Features lens, Sprints lens with closure strip, Flywheel lens with triage status, Level-2 feature detail, Level-3 story detail, and the dark/reading-mode polarity behavior — three implementation foundations are settled before story creation begins. The artifact is renamed from `feature-status` to `momentum:canvas` to match its scope as a general-purpose product-management surface. The runtime is a tiny Vite build using `vite-plugin-singlefile` (replacing the React-via-CDN + Babel-standalone prototype approach) so the page the developer opens is fully static — no in-browser transpile cost. State is read silently at startup from `.momentum/sprints/`, `.momentum/stories/`, and `.momentum/signals/` — the new locations established by parallel Impetus state-relocation work — with `.momentum/signals/` serving as the findings ledger that several Pass 5 design elements were waiting on.

---

## Decisions

### D1: Skill Rename — `feature-status` → `momentum:canvas` — ADOPTED

**Developer framing:** The artifact has expanded across seven Claude Design passes from a flat feature dashboard into a three-lens project canvas (Features / Sprints / Flywheel) with Level-2 feature detail and Level-3 story detail. The name `feature-status` no longer reflects what the artifact is.

**Decision:** Rename the skill. Directory moves from `skills/momentum/skills/feature-status/` to `skills/momentum/skills/canvas/`. Slash command becomes `/momentum:canvas`.

**Rationale:**
We want a general name for the tool we use to manage the product.

---

### D2: Implementation Tech — Tiny Vite Build with `vite-plugin-singlefile` — ADOPTED

**Developer framing:** Pass 4–7 prototypes were built in Claude Design using React-via-CDN + Babel standalone. That works for design previews but the developer's browser pays a Babel transpile cost on every page open. A real implementation should ship a static, pre-built artifact that opens via `file://` with no runtime transpile.

**Decision:** Implement as a small Vite project using `vite-plugin-singlefile` to inline JS and CSS into a single `dist/index.html` template. The canvas skill performs data injection at render time: read `.momentum/sprints/`, `.momentum/stories/`, `.momentum/signals/`, build a `__DATA__` object, splice `<script>window.__DATA__ = {...}</script>` into the template, write the resulting HTML to a known location, open in a cmux browser pane.

**Rationale:**
I vastly prefer a static to dynamic page in this case. The build cycle is completely worth it.

---

### D3: State Source Paths Under `.momentum/` — ADOPTED

**Developer framing:** Concurrent Impetus work is consolidating sprint and story state under a unified `.momentum/` directory. The canvas needs to read this state silently at startup. Any earlier design assumption that state lives under `_bmad-output/implementation-artifacts/sprints/` is superseded by this relocation.

**Decision:** The canvas reads (read-only, silent at startup) from:

- `.momentum/sprints/index.json` — sprint lifecycle, drives the closure strip and sprint header
- `.momentum/stories/index.json` — story status, drives the outcome bands and the Level-3 story detail metadata
- `.momentum/signals/` — what retro flagged as outstanding; this IS the findings ledger that Flywheel lens elements (finding cards, triage status, distillation chain) depend on

Canvas implementation depends on the Impetus state-relocation stories landing first.

**Rationale:**
I want to get a better hold of the state of momentum and this is a great start.

---

## Phased Implementation Plan

| Phase | Focus | Timing | Notes |
|-------|-------|--------|-------|
| 0 | Impetus state relocation under `.momentum/` (parallel work) | Already in flight | Prerequisite for canvas data plumbing |
| 1 | Vite scaffold, design tokens, primitives, pane shell + anchor rail | Next sprint | Foundation that all lens stories build on |
| 2 | Features lens with real data plumbing | After Phase 1 | First lens, exercises the data injection pattern |
| 3 | Sprints lens with closure strip + outcome bands | After Phase 2 | Depends on `.momentum/sprints/` lifecycle states being final |
| 4 | Flywheel lens with timeline + triage | After Phase 3 | Depends on `.momentum/signals/` ledger format being final |
| 5 | Level-2 feature detail (replace-view nav) | After Phase 2 (independent of 3/4) | Reading-mode lock applies here |
| 6 | Level-3 story detail (markdown → typographic doc) | After Phase 5 | Reading-mode lock applies here |
| 7 | Reading-mode override + transition + dark-mode toggle persistence | After Phase 6 | Polishes the polarity behavior across all surfaces |

Two pre-existing backlog stubs (`dashboard-ux-wireframes`, `feature-dependency-graph-ux-wireframes`) are pending intake/triage as part of the next batch — they predate the seven-pass design work but their wireframe scope is now satisfied; the triage pass will decide whether to retire them, fold them into the new phase stories, or keep them as discrete deliverables.

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| G1 | Before Phase 1 starts | Is the Impetus state relocation complete enough to wire against? | `.momentum/sprints/index.json`, `.momentum/stories/index.json`, `.momentum/signals/` directory all exist with stable schemas |
| G2 | After Phase 1 | Did the Vite + singlefile bundle hold up? | `dist/index.html` is one file, opens via `file://`, no runtime transpile, no missing-asset errors |
| G3 | After Phase 4 | Does the Flywheel render real findings, not stubs? | At least one real retro finding from `.momentum/signals/` renders end-to-end with triage status, story link, and skill link |
