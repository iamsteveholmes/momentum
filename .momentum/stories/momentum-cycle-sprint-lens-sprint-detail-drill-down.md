---
title: Momentum Cycle — Sprint Lens + Sprint Detail Drill-Down
story_key: momentum-cycle-sprint-lens-sprint-detail-drill-down
status: review
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
change_type: frontend-feature
depends_on:
  - momentum-cycle-dashboard-shell-hono-bun-server
touches:
  - skills/momentum/skills/canvas/server.tsx
---

# Momentum Cycle — Sprint Lens + Sprint Detail Drill-Down

## Story

As a developer,
I want to see an active sprint summary card on the Momentum Cycle dashboard and drill into sprint story status with outcome-band grouping,
so that I can gauge sprint health at a glance without reading raw sprint files.

## Description

Implement the Sprint section of the Momentum Cycle dashboard (L1 lens card) and the sprint detail view (L2 drill-down) using the Hono+HTMX+Bun stack established by the dashboard shell story.

**Dashboard sprint section (dark mode):** A sprint card rendered inside the existing Sprint lens placeholder. Displays sprint slug, start date, and a closure strip indicating retro/triage completion state (sourced from `retro_run_at` in `.momentum/sprints/index.json`). Polling via `hx-get="/lenses/sprint"` `hx-trigger="every 2s"` against the Hono server.

**Sprint detail view (dark mode):** Reached by clicking the sprint card. Hono route `/sprints/{slug}` returns an HTML partial. Displays three outcome bands:
- **Blocked** — red left border, stories with status `blocked` or `closed-incomplete`
- **In Progress** — amber left border, stories with status `in-progress` or `review` or `verify`
- **Validated** — green left border, stories with status `done`

Stories for the active sprint are sourced from `.momentum/stories/index.json` filtered to slugs in the active sprint's `stories[]` array. Backlog and `ready-for-dev` stories are omitted from the detail view (they have not yet started). Each story row shows title + status badge. Clicking a story row navigates to Story L3 via `hx-push-url="/stories/{slug}?from=sprint"`.

**No-active-sprint state:** If `active` is `null` in the sprint index, the Sprint lens renders an empty-state card: "No active sprint — run /momentum:sprint-planning to start one." No drill-down is available from the empty state.

**Navigation:** HTMX partial swap from dashboard shell. Clicking the sprint card fires `hx-get="/sprints/{slug}"` `hx-target="#main-content"` `hx-push-url="/sprints/{slug}"`. Breadcrumb OOB swap (`hx-swap-oob="true"` on the breadcrumb element) adds a "Sprint" segment (blue accent `--accent #5863a8`) and grays out the "Dashboard" segment. Clicking "Dashboard" in the breadcrumb fires `hx-get="/"` returning the dashboard shell and resetting the breadcrumb. No polarity flip — sprint detail stays dark (same as dashboard).

**Design tokens (inherited from dashboard shell):** `--paperDark: #16140f` background, `--inkOnDark: #f0eee9` text, `--accent: #5863a8`, `--gap: #a85a2a`. Fonts: Inter for UI, JetBrains Mono for meta/slug values.

## Acceptance Criteria

1. The Sprint lens section on the dashboard renders a sprint card when an active sprint exists in `.momentum/sprints/index.json`. The card shows the sprint slug and `started` date in JetBrains Mono.

2. The sprint card includes a closure strip indicating retro completion state: "Retro done" (green) if `retro_run_at` is non-null on the active sprint entry; "Retro pending" (amber) otherwise.

3. When no active sprint exists (`active` is null), the Sprint lens renders an empty-state message: "No active sprint — run /momentum:sprint-planning to start one."

4. The Hono server exposes a `GET /lenses/sprint` route that reads `.momentum/sprints/index.json` and returns the sprint card HTML partial.

5. The Sprint lens container has `hx-get="/lenses/sprint"` `hx-trigger="every 2s"` so the card live-polls from the server.

6. Clicking the sprint card navigates to the sprint detail view. The URL updates to `/sprints/{slug}` via `hx-push-url`. The main content area swaps to the sprint detail partial.

7. The sprint detail view displays three outcome bands: Blocked (red left border), In Progress (amber left border), Validated (green left border).

8. Stories displayed in the detail view are loaded from `.momentum/stories/index.json`, filtered to slugs in the active sprint's `stories[]` array, and excluding stories with status `backlog` or `ready-for-dev`.

9. Story status-to-band mapping: `blocked` and `closed-incomplete` → Blocked band; `in-progress`, `review`, and `verify` → In Progress band; `done` → Validated band.

10. Each story row in the detail view shows the story title and a status badge. The badge uses color tokens matching the band (red/amber/green respectively).

11. Clicking a story row sets `hx-push-url="/stories/{slug}?from=sprint"` and navigates to the Story L3 view.

12. The breadcrumb OOB swap on drill-down adds a "Sprint" segment in `--accent` blue and grays out the "Dashboard" segment. Clicking "Dashboard" in the breadcrumb returns to the dashboard root.

13. The sprint detail view uses dark mode throughout (`--paperDark` background, `--inkOnDark` text). No polarity flip from the dashboard.

14. An outcome band with no stories renders a faint empty label (e.g., "No blocked stories") rather than disappearing entirely, so the three-band structure is always visible.

## Tasks / Subtasks

- [x] Task 1 — Add `/lenses/sprint` route to `server.tsx` (AC: 4, 5)
  - [x] Read `.momentum/sprints/index.json` from the project root; handle file-not-found gracefully
  - [x] Return the sprint card HTML partial: sprint slug, start date, closure strip (retro_run_at present/absent)
  - [x] Return empty-state partial when `active` is null (AC: 3)

- [x] Task 2 — Wire the Sprint lens section in the dashboard shell (AC: 1, 2, 3, 5)
  - [x] Add `hx-get="/lenses/sprint"` `hx-trigger="every 2s"` to the Sprint lens container in the existing shell
  - [x] Ensure the initial server-side render on `GET /` already includes the sprint card (no flash-of-empty on first load)

- [x] Task 3 — Add `/sprints/{slug}` route to `server.tsx` (AC: 6, 7, 8, 9, 10, 13, 14)
  - [x] Read `.momentum/stories/index.json` and filter to the active sprint's `stories[]` array
  - [x] Exclude `backlog` and `ready-for-dev` statuses from the display set
  - [x] Sort stories into three bands by status mapping (blocked/in-progress-family/done)
  - [x] Render each band with left-border color and story rows (title + status badge)
  - [x] Render empty-band placeholder when a band has no stories

- [x] Task 4 — Wire sprint card click navigation (AC: 6, 12)
  - [x] Add `hx-get="/sprints/{slug}"` `hx-target="#main-content"` `hx-push-url="/sprints/{slug}"` to the sprint card element
  - [x] Add `hx-swap-oob="true"` breadcrumb update in the `/sprints/{slug}` response fragment (Sprint=blue, Dashboard=gray+clickable)

- [x] Task 5 — Wire story row click to Story L3 (AC: 11)
  - [x] Add `hx-get="/stories/{slug}?from=sprint"` `hx-target="#main-content"` `hx-push-url="/stories/{slug}?from=sprint"` to each story row in the sprint detail

- [x] Task 6 — Wire breadcrumb "Dashboard" back-navigation (AC: 12)
  - [x] "Dashboard" segment in the breadcrumb fires `hx-get="/"` `hx-target="#main-content"` `hx-push-url="/"`
  - [x] Dashboard response includes a breadcrumb OOB swap that resets to "Dashboard" (blue, no ancestors)

- [x] Task 7 — Manual verification pass
  - [x] Open `http://localhost:3456` with an active sprint in the index — confirm card renders with slug, date, closure strip
  - [x] Confirm live-polling: edit `started` in the sprint index and see the card update within 2s
  - [x] Click sprint card — confirm URL changes, three bands appear, story rows visible
  - [x] Click a story row — confirm navigation to Story L3 with `?from=sprint` param
  - [x] Click "Dashboard" breadcrumb — confirm return to dashboard root, breadcrumb resets

## Dev Notes

### Architecture Compliance

This story implements Phase 3 of the DEC-019 phased plan (sprint lens + sprint detail). All architectural constraints come from DEC-019 D1 and DEC-011 D3:

- **Server file location:** All server logic lives in `skills/momentum/skills/canvas/server.tsx`. No new files — extend the existing server from the dashboard shell story.
- **Data sources are read-only:** Sprint data from `.momentum/sprints/index.json`; story data from `.momentum/stories/index.json`. The canvas never writes these files.
- **HTMX routing model:** Navigation is `hx-get` with `hx-push-url` for URL sync and `hx-swap-oob="true"` for breadcrumb updates. Server returns HTML fragments, not full-page reloads.
- **No polarity flip on sprint detail:** Sprint detail stays dark (same as dashboard). Only Feature L2 and Story L3 flip to warm-light reading mode — those are separate stories.

**Sprint index schema relevant fields (`.momentum/sprints/index.json`):**
```json
{
  "active": {
    "slug": "sprint-2026-05-03",
    "status": "active",
    "locked": true,
    "stories": ["story-a", "story-b"],
    "started": "2026-05-03",
    "completed": null,
    "retro_run_at": null
  }
}
```

**Stories index schema relevant fields (`.momentum/stories/index.json`):**
```json
{
  "story-a": {
    "status": "in-progress",
    "title": "Story A Title",
    ...
  }
}
```

**Status-to-band mapping:**
| Story Status | Band |
|---|---|
| `blocked`, `closed-incomplete` | Blocked (red) |
| `in-progress`, `review`, `verify` | In Progress (amber) |
| `done` | Validated (green) |
| `backlog`, `ready-for-dev` | Omit from detail view |

### Testing Requirements

No automated tests for this story — the canvas is a UI rendering layer with no business logic that warrants test scaffolding. Manual verification (Task 7) covers the behavioral surface:

- Live-poll update visible within 2s of data change
- Three bands always present (including empty-band placeholder)
- Navigation/breadcrumb round-trip works correctly

### Implementation Guide

**Change type: frontend-feature** — this is a Hono server-side JSX extension. No evals, no EDD preamble required.

**Extending `server.tsx`:**

The dashboard shell story establishes `server.tsx` with three empty lens placeholder divs and the Hono app instance. This story adds:

1. Two new route handlers: `app.get('/lenses/sprint', ...)` and `app.get('/sprints/:slug', ...)`
2. Two helper functions: `readSprintsIndex()` and `filterSprintStories(sprintStories, storiesIndex)`
3. JSX components: `SprintCard`, `SprintDetailBand`, `SprintStoryRow`

**Breadcrumb OOB pattern (established by DEC-019):**

Every navigation response must include a breadcrumb fragment with `id="breadcrumb"` and `hx-swap-oob="true"`. The sprint detail breadcrumb:

```tsx
<nav id="breadcrumb" hx-swap-oob="true">
  <a hx-get="/" hx-target="#main-content" hx-push-url="/" style="color: var(--inkOnDark); opacity: 0.6">Dashboard</a>
  <span style="opacity: 0.4"> / </span>
  <span style="color: var(--accent)">Sprint</span>
</nav>
```

The dashboard response resets the breadcrumb to just "Dashboard" in blue with no ancestors.

**Empty-state handling:** Bun's `Bun.file()` returns a file object that can be checked with `.exists()` before reading. Wrap sprint/stories index reads in try/catch — if the file doesn't exist, return the empty-state partial rather than a 500.

**Design token consistency:** All color values come from CSS custom properties defined in the dashboard shell. Do not hardcode hex values in route handlers — use `var(--accent)`, `var(--paperDark)`, etc. in inline styles or a `<style>` block in the partial.

### Project Structure Notes

Single file touched: `skills/momentum/skills/canvas/server.tsx` (created by the dashboard shell story, extended here).

**Merge Conflict Note:** This story runs in Wave 2 alongside momentum-cycle-features-lens, momentum-cycle-sprint-lens-sprint-detail-drill-down, and momentum-cycle-cycle-timeline-lens. All three stories modify skills/momentum/skills/canvas/server.tsx. To minimize conflicts: this story's changes are isolated to the `/lenses/sprint` and `/sprints/:slug` route handlers and helper functions. Do not modify the shell HTML (GET / route) — shell HTML changes are owned by Wave 1. When merging, the sequential merge gate in sprint-dev will sequence the merges — coordinate with the merge integrator if conflicts arise.

No new files needed. The sprint data lives at:
- `.momentum/sprints/index.json` — read relative to the Bun process's working directory (the project root where `bun --hot server.tsx` runs)
- `.momentum/stories/index.json` — same root

The `server.tsx` process is started from the project root by the canvas skill invoker (`cmux respawn-pane --command "cd /path/to/project && bun --hot skills/momentum/skills/canvas/server.tsx"`), so relative paths from process CWD resolve correctly.

### References

- DEC-019: `_bmad-output/planning-artifacts/decisions/dec-019-hono-htmx-bun-canvas-runtime-stack-2026-05-03.md` — stack decision, phased plan (this story is Phase 3)
- DEC-011 D3: `_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md` — state source paths under `.momentum/`
- Architecture § Sprint Tracking Schema: `_bmad-output/planning-artifacts/architecture.md` (line ~1493) — sprint index schema and story state machine
- Sibling story (dashboard shell): `.momentum/stories/momentum-cycle-dashboard-shell-hono-bun-server.md`
- Sibling story (features lens): `.momentum/stories/momentum-cycle-features-lens.md`
- Downstream story (story L3): `.momentum/stories/momentum-cycle-story-l3-drill-down-reading-mode.md`

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6[1m]

### Debug Log References

None — clean implementation.

### Completion Notes List

- Added `readSprintsIndex()` and `readStoriesIndex()` async helpers with graceful file-not-found handling via `Bun.file().exists()` + try/catch.
- Added `getStoryBand()` pure function mapping story status to band name (blocked/in-progress/validated), returning null to omit backlog and ready-for-dev stories.
- Added `SprintCard` component rendering sprint slug, started date (JetBrains Mono), and closure strip with green/amber color based on `retro_run_at`.
- Added `SprintLensSection` component with `hx-get="/lenses/sprint"` `hx-trigger="every 2s"` `hx-swap="outerHTML"` for live polling. Sprint card click wired with `hx-target="#main-content"` and `hx-push-url`.
- Added `SprintDetailBand` + `SprintStoryRow` components with left-border colors, status badges, and empty-band placeholder text.
- Added `SprintDetailView` function returning breadcrumb OOB (`hx-swap-oob="true"`) as a sibling to the primary content (HTMX extracts OOB elements before inserting primary into target).
- Added `GET /lenses/sprint` route (AC 4).
- Added `GET /sprints/:slug` route with story filtering, band sorting, and OOB breadcrumb (AC 6–14).
- Updated `GET /` root route to SSR sprint section for no-flash first load; detects `HX-Request` header and returns fragment with breadcrumb OOB reset for HTMX back-navigation (AC 1, 2, 3, 5).
- Updated `DashboardShell` to use hardcoded `id="breadcrumb"` nav and `id="main-content"` div as HTMX swap target.
- All CSS tokens use CSS custom properties (`var(--accent)`, `var(--paperDark)`, etc.) — no hardcoded hex values in the template layer.
- Removed now-superseded `/lens/sprint` placeholder route. `/lens/features` and `/lens/cycle` placeholders retained.

### File List

- skills/momentum/skills/canvas/server.tsx
