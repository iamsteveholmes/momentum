---
title: Momentum Cycle — Features Lens
story_key: momentum-cycle-features-lens
status: ready-for-dev
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on:
  - momentum-cycle-dashboard-shell-hono-bun-server
touches:
  - skills/momentum/skills/canvas/server.tsx
  - skills/momentum/skills/canvas/server.test.ts
---

# Momentum Cycle — Features Lens

## Story

As a developer,
I want a live Features lens in the Momentum Cycle dashboard that shows feature status, gap flags, and story coverage,
so that I always see current feature state without re-running the feature-status skill manually.

## Description

Implement the `/lenses/features` Hono route and its rendered HTML fragment for the Momentum Cycle dashboard. The route reads `_bmad-output/planning-artifacts/features.json` and `.momentum/stories/index.json` on every request, runs gap analysis (same logic as `feature-status` skill Step 5), and returns a server-rendered HTML partial that the dashboard shell polls via HTMX every 2 seconds.

Each row in the features table displays: feature name, status badge (working=indigo `--accent #5863a8`, partial=amber, not-working=red, not-started=gray), gap indicator (terracotta `--gap #a85a2a` row background when `has_gap=true`), and a story fraction (N done / M total) with a mini progress bar. Rows sort: gap features first, then by status severity (not-working → partial → working → not-started), then alphabetically within each group.

Each Wave 2 story wires its own HTMX polling to the lens placeholder div. This story adds `hx-get="/lenses/features" hx-trigger="every 2s" hx-swap="innerHTML"` to the `id="lens-features"` placeholder and adds the server route that responds to those polls.

**Pain context:** The current `momentum:feature-status` skill requires a manual re-run and writes a static HTML file. The Features lens polls live — the developer sees current state the moment features.json or stories/index.json changes.

## Acceptance Criteria

1. `GET /lenses/features` returns an HTML fragment containing one row per feature found in `features.json`. If `features.json` is absent or empty, the route returns a single empty-state row: `<tr><td colspan="4">No features found — run momentum:feature-grooming first</td></tr>`.

2. Each row displays the feature name, a status badge with the correct design-token color (working → `--accent #5863a8` indigo; partial → `#d97706` amber; not-working → `#dc2626` red; not-started → `#6b7280` gray), a story fraction showing `<stories_done>/<stories_done + stories_remaining>` with a mini progress bar, and a gap indicator icon (⚠) when `has_gap=true`.

3. Rows with `has_gap=true` receive a `background: var(--gap, #a85a2a)` inline style (or equivalent CSS class) so they visually stand out from non-gap rows.

4. Row sort order within the rendered table is: gap rows first (sorted alphabetically within the gap group), then non-gap rows sorted by status severity (not-working → partial → working → not-started), then alphabetically within each status group.

5. Gap analysis uses a structural heuristic (not the LLM-based plausibility check in `feature-status` workflow.md Step 5 — the server route requires a deterministic, synchronous check): a feature `has_gap=true` when its `stories_done` count is 0 and its status is not `working`. Features with `status: working` are never flagged, regardless of story counts.

6. Story metadata for gap analysis is read from `.momentum/stories/index.json`. Story slugs listed in a feature's `stories` array are looked up in the index. If the index is absent, all stories are treated as status `unknown` and any feature with an `acceptance_condition` and zero done stories is flagged as having a gap.

7. The route completes within 500ms under normal conditions (both JSON files present, <100 features). No caching is required — reads happen on every request.

8. The rendered HTML fragment uses only inline styles and design tokens defined in the dashboard shell's `<style>` block — no new CDN links, no external CSS files, no `<style>` tags in the partial itself.

9. The features lens renders correctly when `features.json` is present but all features have `status: working` and no gaps — table renders with all rows in working (indigo) badge color and no terracotta highlights.

10. The Hono server does not crash when `stories/index.json` is missing — it logs a warning and falls back to treating all story statuses as `unknown`.

## Tasks / Subtasks

- [ ] **Task 1 — Add `/lenses/features` route to `server.tsx`** (`script-code`)
  - Register `app.get('/lenses/features', ...)` in the Hono server
  - Read `_bmad-output/planning-artifacts/features.json` (graceful empty-state if absent)
  - Read `.momentum/stories/index.json` (graceful fallback if absent, log warning)
  - Build story lookup map: `story_slug → { status, title }`

- [ ] **Task 2 — Gap analysis function** (`script-code`)
  - Implement `analyzeGap(feature, storyMap)` pure function
  - Returns `{ has_gap: boolean, reason: string }`
  - Logic: zero assigned stories + status != 'working' → gap; acceptance_condition present + no done stories plausibly covering it → gap
  - Unit test: gap detected when zero stories assigned; no gap when status='working' and all stories done

- [ ] **Task 3 — Sort and render rows** (`script-code`)
  - Implement sort: gap rows first (alpha), then by status severity index (not-working=0, partial=1, working=2, not-started=3), then alpha
  - Render each row as a `<tr>` with: gap background style when `has_gap`, name cell, status badge `<span>` with correct color, story fraction `N/M` + `<progress>` element, gap warning icon `⚠` when applicable
  - Unit test: sort order is correct for a mixed input with gaps and varying statuses

- [ ] **Task 4 — Wire status badge colors to design tokens** (`script-code`)
  - Define color map: `{ working: 'var(--accent, #5863a8)', partial: '#d97706', 'not-working': '#dc2626', 'not-started': '#6b7280' }`
  - Apply as inline `background` style on badge `<span>` elements
  - Confirm no new `<style>` tags appear in the partial output

- [ ] **Task 5 — Empty-state and error handling** (`script-code`)
  - Route returns empty-state row when `features.json` is absent or parses to empty object/array
  - Bun catches JSON parse errors and returns an error row: `<tr><td colspan="4">Error reading features.json</td></tr>`
  - stories/index.json absence: console.warn, continue with empty story map

- [ ] **Task 6 — Integration smoke test** (`script-code`)
  - Start server locally with `bun --hot server.tsx`
  - Navigate to `http://localhost:3456` in cmux browser pane
  - Confirm features table renders with correct row count matching features.json entry count
  - Confirm a feature with `has_gap: true` (or manually introduce one) shows terracotta background
  - Confirm polling updates: edit features.json, observe table update within ~2s

## Dev Notes

### Architecture Compliance

This story adds a single Hono route to `server.tsx`. Per DEC-019 (Hono+HTMX+Bun stack), the entire server lives in `skills/momentum/skills/canvas/server.tsx`. This story is Phase 2 of the DEC-019 phased implementation plan (Live lenses — Features).

**Data sources (read-only):**
- `_bmad-output/planning-artifacts/features.json` — written solely by `momentum:feature-grooming`; the canvas never writes to it
- `.momentum/stories/index.json` — written solely by `momentum:sprint-manager` and `momentum:sprint-planning`; the canvas never writes to it

**Dependency:** `momentum-cycle-dashboard-shell-hono-bun-server` must be complete before this story begins. This story wires HTMX polling (`hx-get="/lenses/features" hx-trigger="every 2s" hx-swap="innerHTML"`) to the `id="lens-features"` placeholder div and adds the server-side route.

**DEC-019 Gate 2 criterion:** This story helps satisfy Gate 2 — "Features lens updates within 2s of a features.json write; no flicker on re-render." The dev agent should verify this gate as part of Task 6 smoke testing.

### Testing Requirements

All tasks are `script-code` (TypeScript, Bun runtime). Use TDD:

- **Task 2 (gap analysis):** Unit test in `skills/momentum/skills/canvas/server.test.ts` (create if it does not exist). Test: zero-story feature → gap=true. Test: working-status feature with all stories done → gap=false.
- **Task 3 (sort):** Unit test: provide mixed input array and assert output order matches spec (gap first, then not-working, partial, working, not-started, alpha within groups).
- **Task 5 (error handling):** Test that missing stories/index.json does not throw; empty features.json returns empty-state HTML string.
- **Task 6:** Integration smoke test (manual, cmux environment). Not automated.

Bun has a native test runner (`bun test`). Use it — no Jest, no Vitest needed.

### Implementation Guide

**Hono JSX pattern (matching the shell's approach):**
```tsx
app.get('/lenses/features', async (c) => {
  const features = await readFeaturesJson()  // returns [] on error/absent
  const stories = await readStoriesIndex()   // returns {} on error/absent
  const rows = buildSortedRows(features, stories)
  return c.html(<FeaturesTable rows={rows} />)
})
```

**Reading JSON files in Bun (no fs module needed):**
```ts
const file = Bun.file('_bmad-output/planning-artifacts/features.json')
if (await file.exists()) {
  const data = await file.json()
  // data is the parsed features object
}
```

**Story fraction:** `features.json` has `stories_done` and `stories_remaining` fields — use these directly. Do not recompute from stories/index.json.

**Gap analysis heuristic:** The acceptance-condition check is a judgment call (per feature-status workflow.md Step 5). Implement it as: if `stories_done === 0 && status !== 'working'` → gap=true. The LLM-style plausibility check from feature-status is intentionally simplified here — the Hono server runs synchronously on every request and cannot afford an LLM call. Use the structural heuristic only.

**Progress bar:** Use a native HTML `<progress value={done} max={total} />` element styled to fit within the dark theme via the shell's existing CSS. Do not introduce a JS charting library.

**Row background for gap:** Apply `style="background: var(--gap, #a85a2a);"` directly on the `<tr>` element when `has_gap=true`.

### Project Structure Notes

- Server lives at: `skills/momentum/skills/canvas/server.tsx` (created by the shell story)
- Tests live at: `skills/momentum/skills/canvas/server.test.ts` (create new)
- No new directories needed — this story only adds a route to the existing server file and a test file alongside it

**File scope:**
- Modify: `skills/momentum/skills/canvas/server.tsx`
- Create: `skills/momentum/skills/canvas/server.test.ts`

**Merge Conflict Note:** This story runs in Wave 2 alongside momentum-cycle-features-lens, momentum-cycle-sprint-lens-sprint-detail-drill-down, and momentum-cycle-cycle-timeline-lens. All three stories modify skills/momentum/skills/canvas/server.tsx. To minimize conflicts: this story's changes are isolated to the `/lenses/features` route handler and helper functions. Do not modify the shell HTML (GET / route) — shell HTML changes are owned by Wave 1. When merging, the sequential merge gate in sprint-dev will sequence the merges — coordinate with the merge integrator if conflicts arise.

### References

- DEC-019: `_bmad-output/planning-artifacts/decisions/dec-019-hono-htmx-bun-canvas-runtime-stack-2026-05-03.md` — runtime stack decision and phased implementation plan
- feature-status gap analysis logic: `skills/momentum/skills/feature-status/workflow.md` Step 5
- momentum-canvas feature entry: `_bmad-output/planning-artifacts/features.json` (key: `momentum-canvas`)
- Design reference: `/tmp/momentum-design/feature-status/project/Momentum Cycle - Final.html` (Pass 10 final)
- Architecture: `_bmad-output/planning-artifacts/architecture.md` Decision 44 (features.json schema), Decision 45 (feature-status read path)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5 → `script-code` (TDD via Bun test runner)
- Task 6 → manual integration verification (no change type — not automated)

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively — the implementation guidance below matches its standard approach:

1. **Red:** Write failing tests for the task's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** Scripts in Momentum live under `skills/momentum/skills/[name]/`. Follow the pattern in existing Momentum skills for language choice and structure. This story adds TypeScript to a Bun+Hono server — use native Bun APIs (`Bun.file`, `bun test`) rather than Node.js equivalents.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies):**
- Tests written and passing (`bun test` in the canvas skill directory)
- No regressions in existing test suite
- Code quality checks pass if configured

---

**Gherkin separation reminder:** Gherkin specs for this sprint live in `sprints/{sprint-slug}/specs/`. The dev agent implements against the plain English ACs above only — `.feature` files are off-limits to the dev agent (Decision 30 black-box separation). Do not read or reference `.feature` files during implementation.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
