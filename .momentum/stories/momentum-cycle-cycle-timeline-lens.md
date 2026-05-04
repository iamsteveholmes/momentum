---
title: Momentum Cycle — Cycle Timeline Lens
story_key: momentum-cycle-cycle-timeline-lens
status: ready-for-dev
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: [momentum-cycle-dashboard-shell-hono-bun-server]
touches:
  - skills/momentum/skills/canvas/server.tsx
change_type: script-code
---

# Momentum Cycle — Cycle Timeline Lens

## Story

As a developer,
I want a horizontal timeline showing the current cycle's phase progression with clear node states,
so that I can instantly see which phases ran, what's next required, and where I am in the cycle without digging through files.

## Description

Implement the Cycle Timeline section of the Momentum Cycle dashboard. Shows a horizontal 7-node timeline representing the current cycle's phase progression.

Phases in canonical order (DEC-017): triage → feature-grooming → epic-grooming → refine → sprint-planning → sprint-dev → retro. The `intake` sub-step lives inside triage and is not a separate timeline node.

Node states:
- **done** — filled indigo dot (`--accent #5863a8`), dark label
- **next-required** — indigo ring + 3px glow box-shadow, accent-colored label; advances only as required phases complete
- **not-run** — gray dot, faint label (optional phases skipped in this cycle)
- **pending** — gray dot, faint label (not yet reached)

Required phases: sprint-planning, sprint-dev, retro. Optional phases: triage, feature-grooming, epic-grooming, refine. Optional phases never show the `next-required` outline state.

Status line below the timeline: `cycle started · next required: {phase} · last sprint: {slug}`.

Phase state is derived by reading `.momentum/sprints/index.json` — the completed sprint entries record which practice steps (triage, sprint-planning, sprint-dev, retro, etc.) were run during the cycle.

The Hono server exposes a `/lenses/cycle` route that reads sprint state and returns the rendered HTML partial. The Cycle lens section in the dashboard shell uses `hx-get="/lenses/cycle"` `hx-trigger="every 5s"` for live refresh.

Design reference: `/tmp/momentum-design/feature-status/project/Momentum Cycle - Final.html` (cycle-nodes CSS section, `.cycle-node` states). Design was prototyped in a 10-pass claude.ai/design session and approved.

**Pain context:** Developers have no at-a-glance view of where they are in the current cycle. The timeline makes "what did we run, what's next required" instantly visible.

## Acceptance Criteria (Plain English)

### AC1: Cycle Timeline Renders Seven Ordered Nodes

- The Cycle lens renders a horizontal timeline with exactly 7 nodes
- Nodes appear left-to-right in canonical DEC-017 order: triage, feature-grooming, epic-grooming, refine, sprint-planning, sprint-dev, retro
- Each node shows its phase label below the dot
- The timeline renders correctly on initial page load with no HTMX polling required for the first render

### AC2: Node States Display Correctly

- **done**: filled indigo dot (`--accent #5863a8` background), label at full opacity, dark color
- **next-required**: indigo ring border (not filled), `box-shadow: 0 0 0 3px var(--accent)` glow effect, label in accent color — this state is mutually exclusive with `done`
- **not-run**: gray dot, label at reduced opacity (e.g., 0.45), indicating an optional phase that was skipped this cycle
- **pending**: gray dot, label at reduced opacity, indicating a phase not yet reached

### AC3: next-required Advances Only Through Required Phases

- The `next-required` indicator applies only to required phases: sprint-planning, sprint-dev, retro
- Optional phases (triage, feature-grooming, epic-grooming, refine) never show the `next-required` ring — they show `done` or `not-run` only
- The `next-required` indicator advances to the next required phase after the prior required phase completes: once sprint-planning is done, sprint-dev gets the ring; once sprint-dev is done, retro gets the ring
- If all required phases are complete, no node shows `next-required`

### AC4: Phase State Derived from Sprint Index

- Phase state is computed by reading `.momentum/sprints/index.json`
- A phase is **done** if evidence of its execution exists in the sprints index for the current cycle (e.g., a completed sprint with `retro_run_at` field set means retro is done; sprint entries with `status: done` means sprint-dev ran; the `planned` field on a sprint entry means sprint-planning ran)
- A phase is **not-run** if it is optional and no evidence of its execution exists in the current cycle
- A phase is **pending** if it is required but has not yet run in the current cycle
- The cycle boundary is the most recent completed retro — phases run after the last retro and up to the present constitute the current cycle

### AC5: Status Line Below Timeline

- A status line renders below the timeline nodes
- Content: `cycle started · next required: {phase} · last sprint: {slug}`
- `{phase}` is the label of the current next-required node (e.g., "sprint-planning"); if all required phases complete, shows "none — cycle complete"
- `{slug}` is the slug of the most recently completed sprint (from `sprints/index.json` completed array); if no sprints exist, shows "none"
- Status line uses JetBrains Mono font, subdued color (e.g., `--inkSubtle`)

### AC6: Live Polling via HTMX

- The Cycle lens section in the dashboard shell polls via `hx-get="/lenses/cycle"` `hx-trigger="every 5s"`
- The Hono server exposes a `/lenses/cycle` GET route that reads sprint state and returns the rendered HTML partial
- Polling is at 5-second interval (vs. Features lens 2-second — cycle state changes less frequently)
- The partial returned by `/lenses/cycle` contains the full cycle timeline markup; HTMX swaps the target element

### AC7: Design Token Compliance

- All visual rendering uses approved design tokens from Momentum Cycle - Final.html
- Dark mode tokens: `--paperDark #16140f` background, `--inkOnDark #f0eee9` text, `--accent #5863a8`, `--gap #a85a2a`
- Node connector lines between dots use a subdued color (e.g., `--inkSubtle` or equivalent at low opacity)
- Fonts: JetBrains Mono for the status line meta text; Inter for node labels

### AC8: Graceful Handling of Missing/Empty Sprint Data

- If `.momentum/sprints/index.json` does not exist or has no completed entries, the timeline renders all 7 nodes in `pending`/`not-run` state with no error
- The status line shows `cycle started · next required: sprint-planning · last sprint: none` when no sprints exist
- No uncaught exceptions or broken HTML when sprint data is absent

## Tasks / Subtasks

- [ ] Task 1 — Add `/lenses/cycle` route to `server.tsx`
  - [ ] Implement `computeCycleState()` function: reads `.momentum/sprints/index.json`, identifies current cycle boundary (last completed retro), classifies each of the 7 phases as done/next-required/not-run/pending
  - [ ] Implement `CycleTimeline` JSX component: renders 7 nodes with correct state-driven CSS classes, connector lines, node labels
  - [ ] Implement `CycleStatusLine` JSX component: renders `cycle started · next required: {phase} · last sprint: {slug}` below the timeline
  - [ ] Register `GET /lenses/cycle` Hono route that calls `computeCycleState()` and returns `<CycleTimeline>` + `<CycleStatusLine>` as HTML partial

- [ ] Task 2 — Wire HTMX polling in the dashboard shell Cycle section
  - [ ] Locate the Cycle lens placeholder div in the dashboard shell (from `momentum-cycle-dashboard-shell-hono-bun-server` story)
  - [ ] Add `hx-get="/lenses/cycle"` and `hx-trigger="every 5s"` attributes to the Cycle lens container
  - [ ] Verify the initial render populates the Cycle lens on page load (either via `hx-trigger="load, every 5s"` or by server-rendering the initial state inline)

- [ ] Task 3 — Implement node state CSS
  - [ ] Add `.cycle-node` base styles (dot size, label typography, connector line)
  - [ ] Add `.cycle-node--done` styles: filled indigo dot, full-opacity label
  - [ ] Add `.cycle-node--next-required` styles: indigo ring, 3px glow box-shadow, accent label color
  - [ ] Add `.cycle-node--not-run` and `.cycle-node--pending` styles: gray dot, reduced-opacity label
  - [ ] Verify design tokens match `/tmp/momentum-design/feature-status/project/Momentum Cycle - Final.html` cycle-nodes section

- [ ] Task 4 — Write tests for `computeCycleState()`
  - [ ] Test: empty sprints index → all nodes pending/not-run, next-required = sprint-planning
  - [ ] Test: one completed sprint with retro → sprint-planning, sprint-dev, retro all done; next-required = sprint-planning (new cycle)
  - [ ] Test: sprint-planning done but sprint-dev not started → sprint-planning done, sprint-dev next-required
  - [ ] Test: optional phases (triage, refine) never receive next-required state

- [ ] Task 5 — Manual visual verification
  - [ ] Start server with `bun --hot server.tsx`, open `http://localhost:3456` in cmux browser pane
  - [ ] Verify Cycle lens renders with correct node states reflecting actual `.momentum/sprints/index.json`
  - [ ] Verify status line text is correct
  - [ ] Verify HTMX polling updates the lens (write a test change to confirm swap)

## Dev Notes

### Architecture Compliance

This story adds to `skills/momentum/skills/canvas/server.tsx` — the single-file Hono+Bun server established by `momentum-cycle-dashboard-shell-hono-bun-server`. DEC-019 mandates:
- All canvas logic lives in `server.tsx` (single-file architecture)
- Data reads are read-only; no writes to `.momentum/` from the server
- Routing is Hono; live data is HTMX polling; JSX for rendering

Do not create additional files for the cycle lens. All JSX components, route handlers, and utility functions belong in `server.tsx`.

**DEC-017 Cycle Step Sequence (authoritative):**
```
triage → intake → feature-grooming → epic-grooming → refine → sprint-planning → sprint-dev → retro
```
`intake` is a sub-step of triage — not a separate node. The timeline shows 7 nodes (intake collapsed into triage).

Required phases: sprint-planning, sprint-dev, retro.
Optional phases: triage, feature-grooming, epic-grooming, refine.

### Testing Requirements

This story is classified `script-code` (TypeScript in `server.tsx`). Use TDD:

1. **Red:** Write tests for `computeCycleState()` before implementing it. Tests should cover: empty sprints, first sprint started, sprint-planning done / sprint-dev pending, all required phases done (cycle complete), optional phases never returning `next-required` state.
2. **Green:** Implement `computeCycleState()` to pass all tests.
3. **Refactor:** Clean up before marking done.

Tests can be Bun-native (`.test.ts` files using `bun test`) or plain Node. The `computeCycleState()` function is pure (takes sprint index data, returns phase state map) — no HTTP or file I/O needed for unit tests.

The JSX rendering (components, CSS) is verified by Task 5 manual visual check against the design reference, not unit tests.

### Implementation Guide

#### `computeCycleState(sprintsIndex)` — Pure Function

Input: the parsed contents of `.momentum/sprints/index.json`.

Output: an object with:
```ts
{
  phases: Array<{
    slug: string,          // e.g. "sprint-planning"
    label: string,         // display label, e.g. "sprint-planning"
    state: "done" | "next-required" | "not-run" | "pending",
    required: boolean
  }>,
  nextRequired: string | null,   // slug of next-required phase, null if cycle complete
  lastSprintSlug: string | null  // most recent completed sprint slug
}
```

Cycle boundary logic:
- Find the most recent sprint in `completed[]` that has `retro_run_at` set — this is the last completed cycle's retro
- All activity after that retro (and up to now) constitutes the **current cycle**
- Specifically, look at: `active` sprint (if any), and the `planning` sprint (if any), to determine which phases have run in the current cycle

Phase detection heuristics (based on `sprints/index.json` schema):
- **sprint-planning ran** if a sprint in the current cycle has `status: "planning"` or later, and the `planned` field is set
- **sprint-dev ran** if a sprint in the current cycle has `status: "done"` or `status: "active"` with `started` set
- **retro ran** if a sprint in the current cycle has `retro_run_at` set
- **triage/feature-grooming/epic-grooming/refine ran** — these are practice sessions that don't leave structured traces in `sprints/index.json`. For now, classify them as `not-run` (optional phases default to not-run unless explicit evidence exists). A future story can add trace fields.

This simplification is correct for the current sprint: the cycle timeline primarily tracks the required phases (sprint-planning → sprint-dev → retro); optional phases are informational.

#### Cycle lens HTMX wiring

The dashboard shell story established the Cycle lens placeholder:
```html
<div id="cycle-lens" hx-get="/lenses/cycle" hx-trigger="load, every 5s" hx-swap="innerHTML">
  <!-- initial state rendered server-side on first request -->
</div>
```

The `/lenses/cycle` route returns only the inner HTML of the lens (the timeline + status line) — not a full page. HTMX swaps `innerHTML`.

#### Node CSS Classes

Follow the pattern in the design reference's `.cycle-node` section:
```css
.cycle-node { /* base: dot + label column layout */ }
.cycle-node--done .dot { background: var(--accent); }
.cycle-node--next-required .dot { 
  border: 2px solid var(--accent);
  box-shadow: 0 0 0 3px var(--accent);
}
.cycle-node--not-run .dot,
.cycle-node--pending .dot { background: var(--inkSubtle, #888); }
.cycle-node--not-run .label,
.cycle-node--pending .label { opacity: 0.45; }
```

Connector lines between nodes use a thin horizontal rule at low opacity.

### Project Structure Notes

All code for this story goes into `skills/momentum/skills/canvas/server.tsx`. No new files are created.

This story depends on `momentum-cycle-dashboard-shell-hono-bun-server` being complete: the Hono server exists, the shell renders, and the Cycle lens placeholder div is present.

The design reference at `/tmp/momentum-design/feature-status/project/Momentum Cycle - Final.html` contains the approved cycle-nodes CSS and layout. Read it for exact token values, dot sizes, and typography before implementing.

### Data Flow

| Source | Access | Purpose |
|--------|--------|---------|
| `.momentum/sprints/index.json` | Read at `/lenses/cycle` request time | Compute phase states for current cycle |
| `_bmad-output/planning-artifacts/features.json` | Not read by this story | Features lens only |
| Design reference at `/tmp/momentum-design/…/Momentum Cycle - Final.html` | Read once during implementation | CSS design tokens, `.cycle-node` styles |

### References

- DEC-019: `_bmad-output/planning-artifacts/decisions/dec-019-hono-htmx-bun-canvas-runtime-stack-2026-05-03.md` — Hono+HTMX+Bun stack decision (authoritative for all canvas stories)
- DEC-017: `_bmad-output/planning-artifacts/decisions/dec-017-momentum-cycle-step-sequence-definition-2026-05-03.md` — Canonical cycle step sequence and required/optional classification
- DEC-011 D3: State source paths under `.momentum/` — sprints/index.json is the cycle state source
- Design reference: `/tmp/momentum-design/feature-status/project/Momentum Cycle - Final.html` (Pass 10 final, cycle-nodes CSS section)
- Depends on: `momentum-cycle-dashboard-shell-hono-bun-server` (Hono server and Cycle lens placeholder)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → script-code (TDD)
- Task 4 → script-code (TDD — tests themselves)
- Task 5 → script-code (manual visual verification)

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively:

1. **Red:** Write failing tests for `computeCycleState()` before implementing. Tests in a `.test.ts` file alongside `server.tsx` or in a `__tests__/` subdirectory. Confirm they fail.
2. **Green:** Implement `computeCycleState()` to make all tests pass.
3. **Refactor:** Clean up internal structure while keeping tests green.

The JSX components and CSS are not unit-tested — verify visually per Task 5.

**Note on Gherkin specs:** Gherkin `.feature` files may exist in the sprint's `specs/` directory for this story. The dev agent implements against the plain English ACs in this story file only — never against `.feature` files. Gherkin specs are for acceptance testing after implementation, not a dev input (Decision 30 black-box separation).

**DoD additions for script-code tasks:**
- [ ] Tests written for `computeCycleState()` covering all 4 AC4 scenarios
- [ ] All tests passing (`bun test` or equivalent)
- [ ] No regressions in existing server behavior (shell still renders after changes)
- [ ] Visual verification completed per Task 5 checklist

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
