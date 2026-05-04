---
title: Momentum Cycle — Feature L2 Drill-Down (Reading Mode)
story_key: momentum-cycle-feature-l2-drill-down-reading-mode
status: ready-for-dev
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: [momentum-cycle-features-lens]
touches:
  - skills/momentum/skills/canvas/server.tsx
---

# Momentum Cycle — Feature L2 Drill-Down (Reading Mode)

## Story

As a developer,
I want to navigate to a feature's L2 detail view rendered as a typographic reading document,
so that I can read feature details, value narrative, and story list without opening raw markdown files.

## Description

Implement the Feature Level-2 detail view in the Momentum Cycle Hono+Bun server. This is Phase 4 of the DEC-019 implementation plan.

When a developer clicks a feature row in the Features lens, the page replaces its main content area with the L2 reading view. The polarity flips from the warm dark dashboard (`--paperDark: #16140f`) to warm light reading mode (`--readingPaper: #faf6ec`). The transition is a 140ms CSS cross-fade achieved by swapping a CSS class on the `.pane-inner` container — no JS animation framework needed.

The L2 surface renders six sections in a 65ch-constrained reading column:

1. **Feature heading** — Source Serif 4, large-scale heading
2. **Meta strip** — status badge + story fraction (e.g., "3 / 7 stories done") + a small "reading mode" label in JetBrains Mono
3. **Value narrative** — the feature's `value_narrative` field rendered as prose in Source Serif 4
4. **Acceptance condition** — the feature's `acceptance_condition` field rendered in a boxed container with a left border (accent color)
5. **System context** — the feature's `system_context` field rendered as a callout block
6. **Stories list** — Inter font; each row shows a status icon + story title + status label; clicking a row navigates to the L3 story detail view

Dependencies render as a plain list below the stories section — feature slugs only, no graph view, no mode pill (per design decision in DEC-019 and iq-20260424205304).

**Navigation contract:**
- URL: `hx-push-url="/features/{slug}"` — the URL updates so the browser history is correct
- Breadcrumb OOB swap: `hx-swap-oob="true"` on the breadcrumb element; updates to "Dashboard / Feature" where "Feature" is styled in `--accent` blue and "Dashboard" is gray + clickable back to `/`
- Back affordance: breadcrumb "Dashboard" segment acts as the back link; no separate back button

**Data sources (read-only):**
- Feature data: `_bmad-output/planning-artifacts/features.json` (keyed by feature slug)
- Story data: `.momentum/stories/index.json` (stories filtered to `feature_slug === slug`)

**Design token values (from DEC-019 / Momentum Cycle - Final.html):**
- `--readingPaper: #faf6ec` — reading mode background
- `--paperDark: #16140f` — dashboard background (no longer active when L2 is shown)
- `--accent: #5863a8` — heading tint, status icons, left border on acceptance condition box
- `--inkOnLight: #1a1814` — body text in reading mode
- `--inkMuted: #6b6660` — meta strip text
- Font stack: Source Serif 4 (headings + body), Inter (story list rows), JetBrains Mono (meta strip)
- Reading measure: 65ch, body 18px, line-height 1.70

**Pain context:** Developers must open raw markdown feature files to read feature details. The L2 view renders them as a typographic document, replacing direct file reads during sprint planning and grooming.

**Source:** triage — conversation (10-pass claude.ai/design prototype approved; DEC-019 Phase 4)

## Acceptance Criteria

1. A Hono route `GET /features/:slug` exists in `server.tsx` and returns a full HTML response (not a partial fragment — this is a top-level navigation target)
2. Navigating to `/features/{slug}` updates the browser URL via `hx-push-url="/features/{slug}"` — the address bar reflects the current feature
3. The breadcrumb OOB swap fires on navigation, updating the breadcrumb to "Dashboard / {Feature Name}" — "Dashboard" is gray and clickable back to `/`, the feature name is styled in `--accent` blue
4. The main content area background transitions from dark (`--paperDark: #16140f`) to reading mode (`--readingPaper: #faf6ec`) via a 140ms CSS cross-fade when navigating to L2; transitioning back to dashboard reverses the transition
5. The feature heading renders in Source Serif 4 at an appropriate large scale
6. The meta strip shows the status badge, story fraction ("N / M stories done"), and a small "reading mode" label in JetBrains Mono
7. The value narrative section renders as Source Serif 4 prose in a 65ch column at 18px / 1.70 line-height; if `value_narrative` is absent or empty, the section is omitted (not an empty box)
8. The acceptance condition renders in a boxed container with a left border in `--accent` color; if absent, the section is omitted
9. The system context renders as a callout block; if absent, the section is omitted
10. The stories list renders in Inter; each row shows a status icon, story title, and status label; story rows are ordered by status (in-progress → ready-for-dev → backlog → done)
11. Clicking a story row navigates to the L3 story detail view via `hx-get="/stories/{slug}"` with `hx-push-url="/stories/{slug}"`
12. Dependencies render as a plain list of feature slugs below the stories section — no graph view, no mode pill
13. If the feature slug does not exist in `features.json`, the server returns a graceful 404 view with a "Feature not found" message and a breadcrumb back link to Dashboard
14. If `features.json` is missing or unparseable, the route returns a graceful error view — the server does not crash

## Dev Notes

### Architecture Context

This story implements Phase 4 of the DEC-019 implementation plan. The canonical architecture decisions are:

- **DEC-019** (`_bmad-output/planning-artifacts/decisions/dec-019-hono-htmx-bun-canvas-runtime-stack-2026-05-03.md`) — Hono+HTMX+Bun replaces DEC-011 D2 Vite approach. This is the binding architecture for all canvas work.
- **DEC-011** (`_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md`) — D1 (rename to `momentum:canvas`) and D3 (state source paths under `.momentum/`) remain in force.

**Dependency:** This story requires `momentum-cycle-features-lens` (Phase 2) to be complete. The Features lens provides the navigation entry point — story rows click to navigate here. The Hono server infrastructure is established in `momentum-cycle-dashboard-shell-hono-bun-server` (Phase 1).

### What Exists Today (Pre-Implementation State)

The Hono server (`skills/momentum/skills/canvas/server.tsx`) exists from Phase 1 and 2 stories. It exposes:
- `GET /` — dashboard shell with dark paper theme
- `GET /lenses/features` — HTMX partial for the Features lens (live-polled every 2s)

Phase 4 adds `GET /features/:slug` as a new top-level route alongside these.

The `features.json` file lives at `_bmad-output/planning-artifacts/features.json`. Its schema (from `feature-artifact-schema` story) includes per-feature fields: `slug`, `title`, `status`, `has_gap`, `acceptance_condition`, `value_narrative`, `system_context`, `story_slugs`, `depends_on`.

The `.momentum/stories/index.json` file provides story metadata. Each entry has `status`, `title`, `epic_slug`, `feature_slug`, and related fields. Filter by `feature_slug === slug` to get the feature's stories.

### What to Create / Change

**Single file: `skills/momentum/skills/canvas/server.tsx`**

Add one Hono route handler:

```typescript
app.get('/features/:slug', async (c) => {
  const slug = c.req.param('slug')
  // 1. Read features.json — graceful error if missing
  // 2. Find feature by slug — graceful 404 if not found
  // 3. Read stories/index.json — graceful error if missing
  // 4. Filter stories where feature_slug === slug
  // 5. Sort stories: in-progress → ready-for-dev → backlog → done
  // 6. Return full HTML page with reading-mode polarity
})
```

The response is a **full page** (not a fragment) — it replaces the entire `innerHTML` via `hx-target="body" hx-swap="innerHTML"` on the click trigger in the Features lens story rows. The page must include the `<html>`, `<head>` (with HTMX CDN, font imports, CSS design tokens), and `<body>` tags — or a consistent shell structure matching the existing dashboard shell.

**CSS polarity flip — implementation approach:**

The dark→light transition is a CSS class swap on `.pane-inner`:
- Dashboard: `.pane-inner` has no modifier class — `background: var(--paperDark)`
- L2/L3 reading mode: `.pane-inner` gets `.reading-mode` class — `background: var(--readingPaper); transition: background 140ms ease`

The class swap happens automatically because L2 returns a full page with `.pane-inner.reading-mode` already set in the HTML. HTMX replaces the body, which swaps the class, triggering the CSS transition.

**Breadcrumb OOB swap — implementation approach:**

Every Hono response (dashboard + L2 + future L3) must include an OOB breadcrumb element:
```html
<nav id="breadcrumb" hx-swap-oob="true">
  <a href="/" hx-get="/" hx-push-url="/" hx-target="body">Dashboard</a>
  <span> / </span>
  <span class="current">{Feature Name}</span>
</nav>
```

The breadcrumb element with `id="breadcrumb"` must already exist in the dashboard shell (from Phase 1). The L2 response includes the same element with `hx-swap-oob="true"` so HTMX updates it out-of-band without replacing the whole page breadcrumb logic.

**Story status sort order:**

```typescript
const STATUS_ORDER = ['in-progress', 'ready-for-dev', 'backlog', 'done']
stories.sort((a, b) => STATUS_ORDER.indexOf(a.status) - STATUS_ORDER.indexOf(b.status))
```

**Status icon mapping (for story rows):**

| Status | Icon (text/Unicode) | Color |
|---|---|---|
| done | ✓ | green (`#3d8b3d`) |
| in-progress | ⟳ | amber (`#c48a1a`) |
| ready-for-dev | → | accent (`--accent: #5863a8`) |
| backlog | · | muted (`--inkMuted`) |

Use consistent Unicode characters or SVG inline icons matching the established pattern from the Features lens rows (Phase 2).

**Story row click navigation:**

```html
<div class="story-row"
     hx-get="/stories/{slug}"
     hx-push-url="/stories/{slug}"
     hx-target="body"
     hx-swap="innerHTML">
  <span class="status-icon">{icon}</span>
  <span class="story-title">{title}</span>
  <span class="status-label">{status}</span>
</div>
```

### Testing Requirements

This story is a Hono route and server-rendered HTML — no unit test framework is configured for the canvas server. Verify by functional inspection:

1. Start the server (`bun --hot server.tsx`) and navigate to `/features/{slug}` for a known slug from `features.json`
2. Confirm URL updates in browser address bar
3. Confirm breadcrumb shows correct "Dashboard / {Feature Name}" text
4. Confirm background transitions to warm light (`#faf6ec`)
5. Confirm all six sections render correctly for a feature with all fields populated
6. Confirm sections are omitted (not empty) for features with absent optional fields
7. Navigate back to Dashboard via breadcrumb — confirm dark polarity restores
8. Click a story row — confirm navigation to `/stories/{slug}` occurs
9. Test with a non-existent slug — confirm 404 view, not server crash
10. Test with missing `features.json` — confirm error view, not server crash

### Project Structure Notes

All changes are confined to a single file:

```
skills/momentum/skills/canvas/
  server.tsx          ← add GET /features/:slug route here
```

No new files, no new directories. This story is purely additive — it extends the server file established in Phase 1 (`momentum-cycle-dashboard-shell-hono-bun-server`) and Phase 2 (`momentum-cycle-features-lens`).

The Hono server entry point location is `skills/momentum/skills/canvas/server.tsx` per DEC-019 D1. The skill invoker that starts the server (`cmux respawn-pane bun --hot server.tsx`) was established in Phase 1 and requires no changes for this story.

### Gherkin Specs Note

Gherkin `.feature` files for this sprint live in `sprints/{sprint-slug}/specs/`. **Dev agent must NOT read or implement against these files.** The black-box separation (Decision 30) means the dev agent implements against the plain English ACs in this story file only. The Gherkin specs are for the E2E Validator role, not the implementer.

### References

- DEC-019: `_bmad-output/planning-artifacts/decisions/dec-019-hono-htmx-bun-canvas-runtime-stack-2026-05-03.md`
- DEC-011: `_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md`
- Features lens story (Phase 2 predecessor): `.momentum/stories/momentum-cycle-features-lens.md`
- Dashboard shell story (Phase 1 predecessor): `.momentum/stories/momentum-cycle-dashboard-shell-hono-bun-server.md`
- Story L3 story (Phase 5 successor): `.momentum/stories/momentum-cycle-story-l3-drill-down-reading-mode.md`
- Design source: `/tmp/momentum-design/feature-status/project/Momentum Cycle - Final.html` (10-pass claude.ai/design prototype)

## Tasks / Subtasks

- [ ] Task 1 — Add `GET /features/:slug` route to `server.tsx`
  - [ ] Read `features.json` from `_bmad-output/planning-artifacts/features.json` (graceful error if missing/unparseable)
  - [ ] Find feature by slug — return 404 view if not found
  - [ ] Read `.momentum/stories/index.json` and filter by `feature_slug === slug`
  - [ ] Sort stories by status order: in-progress → ready-for-dev → backlog → done
  - [ ] Return full HTML page with reading-mode polarity (`.pane-inner.reading-mode`, `--readingPaper: #faf6ec` background)

- [ ] Task 2 — Implement reading-mode polarity CSS
  - [ ] Add `.reading-mode` modifier class to CSS with `background: var(--readingPaper)` and `transition: background 140ms ease`
  - [ ] Ensure `--readingPaper: #faf6ec` CSS custom property is defined in the root stylesheet (or inline in the server response)
  - [ ] Verify dashboard shell uses no modifier class (stays `--paperDark: #16140f`)

- [ ] Task 3 — Implement breadcrumb OOB swap
  - [ ] Add `id="breadcrumb"` to the breadcrumb element in the dashboard shell (if not already present from Phase 1)
  - [ ] L2 route response includes breadcrumb with `hx-swap-oob="true"`, "Dashboard" as clickable link to `/`, feature name in `--accent` color

- [ ] Task 4 — Render the six L2 content sections
  - [ ] Feature heading in Source Serif 4 at large scale
  - [ ] Meta strip: status badge + story fraction + "reading mode" label in JetBrains Mono
  - [ ] Value narrative prose (65ch / 18px / 1.70lh); omit section entirely if field absent
  - [ ] Acceptance condition boxed with `--accent` left border; omit if absent
  - [ ] System context callout block; omit if absent
  - [ ] Dependencies as plain list of slugs; omit section if `depends_on` is empty

- [ ] Task 5 — Render the stories list
  - [ ] Each row: status icon (Unicode/SVG) + story title + status label in Inter
  - [ ] Status icons follow the icon/color mapping in Dev Notes
  - [ ] Each row wires `hx-get="/stories/{slug}"` `hx-push-url="/stories/{slug}"` `hx-target="body"` `hx-swap="innerHTML"`

- [ ] Task 6 — Functional verification
  - [ ] Test all 10 verification steps listed in Testing Requirements above
  - [ ] Verify 404 path (non-existent slug) does not crash server
  - [ ] Verify missing `features.json` path does not crash server
  - [ ] Verify breadcrumb back-navigation to Dashboard restores dark polarity

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–6 → script-code (TypeScript / Hono route handler in `server.tsx`)

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). However, the Momentum Cycle server has no automated test harness configured — this is a Hono+Bun server verified by functional inspection (the test environment IS the running browser). Apply the spirit of TDD:

1. **Red:** Before implementing each task, state the expected behavior as a condition that currently fails (e.g., "GET /features/foo currently returns 404 — not yet implemented")
2. **Green:** Implement the minimum route handler to produce the correct response. Start the server and confirm in browser.
3. **Inspect:** Walk through the 10 functional verification steps in Testing Requirements before marking the task done.

**Note:** All canvas code lives in `skills/momentum/skills/canvas/server.tsx`. There is no separate `scripts/` directory — the server IS the deliverable. Do not create additional files for this story.

**DoD items for script-code tasks:**
- [ ] `GET /features/:slug` route returns correct HTML for a valid slug
- [ ] `GET /features/:slug` returns graceful 404 for unknown slug (no server crash)
- [ ] `GET /features/:slug` returns graceful error view if `features.json` missing (no server crash)
- [ ] All six content sections render correctly
- [ ] Optional sections omitted (not empty boxes) when fields absent
- [ ] Reading-mode polarity flip works: background `#faf6ec`, 140ms transition
- [ ] Breadcrumb OOB swap correct on L2 navigation
- [ ] Story rows navigate to L3 via HTMX
- [ ] Dependencies render as plain list with no graph/mode pill
- [ ] All 10 functional verification steps from Testing Requirements completed and passing

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
