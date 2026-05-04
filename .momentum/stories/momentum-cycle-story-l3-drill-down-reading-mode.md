---
title: Momentum Cycle — Story L3 Drill-Down (Reading Mode)
story_key: momentum-cycle-story-l3-drill-down-reading-mode
status: ready-for-dev
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: [momentum-cycle-feature-l2-drill-down-reading-mode, momentum-cycle-sprint-lens-sprint-detail-drill-down]
touches:
  - skills/momentum/skills/canvas/server.tsx
---

# Momentum Cycle — Story L3 Drill-Down (Reading Mode)

## Story

As a developer,
I want to read a story's full detail in a polished, typography-focused view inside the practice pane,
so that I can review and approve stories without opening raw markdown files and breaking my flow.

## Description

Implement the Story Level-3 detail view — the deepest drill-down surface in the Momentum Cycle navigation hierarchy. This is the reading surface that replaces raw markdown file opens during story review, sprint planning, and grooming.

**Entry points (two):**
1. Feature L2 stories list → clicking a story row navigates here; breadcrumb shows "Dashboard / Feature / Story"
2. Sprint detail outcome bands → clicking a story row navigates here; breadcrumb shows "Dashboard / Sprint / Story"

**Polarity:** Reading mode (warm light — `--readingPaper: #faf6ec` background). No polarity flip when arriving from Feature L2 (which is already warm light). A polarity flip DOES apply when arriving from Sprint detail (which is dark mode) — use the same 140ms CSS cross-fade on `.pane-inner` used in L2. The `?from=feature` or `?from=sprint` query param on the Hono route controls breadcrumb OOB swap content only — the polarity is always warm light for L3 regardless of entry point.

**Surface renders:**
- Frontmatter strip: slug, type, status, epic, `derives_from` (if present) in JetBrains Mono, styled as meta
- Title: Source Serif 4 heading
- Value narrative (if present in story body — the paragraph before ACs)
- Numbered acceptance criteria: Source Serif 4, numbered list
- Workflow phases section (if story has a `workflow` field in frontmatter or a `## Workflow` section in body)
- Dev notes section: render collapsed summary if long (first paragraph or 3 bullet points visible, rest behind expand)
- File list: renders `touches` array from frontmatter as a list, if non-empty

**Data source:** Individual story files at `.momentum/stories/{slug}.md` — parse frontmatter + markdown body at request time. No separate JSON needed; the story file is the authoritative source.

**Typography spec:** 65ch measure, 18px body, 1.70 line-height, Source Serif 4 throughout except meta/code elements (JetBrains Mono).

**Architecture alignment:** DEC-019 — Hono+HTMX+Bun runtime stack. Single Hono route `/stories/{slug}`, query param `?from=feature|sprint` controls breadcrumb OOB swap. Navigation via `hx-push-url`. Breadcrumb swap via `hx-swap-oob="true"`.

**Pain context:** Developers must open raw markdown story files to approve stories, which breaks flow. Story L3 renders stories as a polished reading surface directly in the practice pane.

## Acceptance Criteria

1. Navigating to `/stories/{slug}` renders the story detail view in warm light reading mode (`--readingPaper: #faf6ec` background, `--inkOnLight` text).
2. When arriving from sprint detail (dark mode surface), the page background transitions from dark to light with a 140ms CSS cross-fade on `.pane-inner`. When arriving from Feature L2 (already warm light), no visible transition occurs.
3. The frontmatter strip renders the story's `slug`, `story_type`, `status`, `epic_slug`, and `derives_from` (if present) in JetBrains Mono at a reduced size (meta style, dimmed).
4. The story title renders in Source Serif 4 at appropriate heading scale (≥24px).
5. Body text uses Source Serif 4, 18px, 1.70 line-height, constrained to 65ch measure.
6. The value narrative paragraph (prose before the acceptance criteria) renders if present in the story body.
7. Acceptance criteria render as a numbered list in Source Serif 4.
8. A workflow phases section renders if the story's frontmatter contains a `workflow` field or the story body contains a `## Workflow` section.
9. The dev notes section renders; if the section contains more than 3 list items OR more than one paragraph (i.e., is multi-paragraph), the full content is collapsed behind an expand affordance (no JavaScript framework required — plain `<details>`/`<summary>` is acceptable). Single-sentence or single-paragraph sections render inline without collapse.
10. The `touches` file list renders as a plain list if the story frontmatter `touches` array is non-empty; the section is omitted entirely if `touches` is empty or absent.
11. With `?from=feature`, the breadcrumb OOB swap updates to show "Dashboard / Feature / Story" — "Story" in accent blue, ancestors in gray, clickable.
12. With `?from=sprint`, the breadcrumb OOB swap updates to show "Dashboard / Sprint / Story" — "Story" in accent blue, ancestors in gray, clickable.
13. Clicking the "Feature" breadcrumb segment navigates back to the Feature L2 view. Clicking "Sprint" navigates back to the sprint detail view. Clicking "Dashboard" navigates to root `/`.
14. The story data is read from `.momentum/stories/{slug}.md` at request time (no cached layer).
15. If a story slug is not found (no matching `.md` file), the route returns a graceful 404 fragment with a plain "Story not found" message rather than a server error.
16. The route and reading experience are functional in both Chrome and Safari (the two browsers used in the cmux viewer pane).

## Tasks / Subtasks

- [ ] **Task 1 — Hono route `/stories/{slug}`** (`script-code`)
  - Add a GET handler for `/stories/{slug}` in `skills/momentum/skills/canvas/server.tsx`
  - Accept optional `?from=feature|sprint` query param; default to `from=feature` if absent
  - Read `.momentum/stories/{slug}.md`; return 404 fragment if file not found
  - Parse frontmatter (slug, story_type, status, epic_slug, derives_from, workflow, touches) using a minimal YAML frontmatter parser (no heavy deps — manual regex split on `---` delimiters is fine)
  - Return full HTML response with warm light reading mode applied to `.pane-inner`

- [ ] **Task 2 — Story markdown parser** (`script-code`)
  - Extract the value narrative from the `## Description` section — specifically the prose paragraph(s) describing user pain and context. If absent from Description, fall back to prose content that appears before `## Acceptance Criteria` in the body. Do NOT extract the `## Story` user-story statement ("As a developer, I want...") as the value narrative.
  - Extract acceptance criteria from `## Acceptance Criteria` section as an ordered list
  - Extract workflow phases from `## Workflow` section (if present) or `workflow` frontmatter field
  - Extract dev notes section (`## Dev Notes`) — truncate for collapse affordance if >3 items/paragraphs
  - Extraction must handle the standard Momentum story format used by all `.momentum/stories/*.md` files

- [ ] **Task 3 — Reading mode HTML template** (`script-code`)
  - Compose the story detail HTML fragment using the design tokens: `--readingPaper: #faf6ec` (the warm reading surface — distinct from `--paper: #fbfaf7` which is the lighter base used in the shell), `--inkOnLight`, `--accent: #5863a8`
  - Frontmatter strip: JetBrains Mono, dimmed, flex row layout
  - Title: Source Serif 4, heading scale
  - Body regions: 65ch max-width column, 18px, 1.70 line-height, Source Serif 4
  - Dev notes uses `<details>`/`<summary>` for collapse when length exceeds threshold
  - Touches list: plain `<ul>` with file path entries; omit section if empty
  - Apply `.reading-mode` class to `.pane-inner` in the response (triggers the 140ms CSS transition already defined for L2)

- [ ] **Task 4 — Breadcrumb OOB swap** (`script-code`)
  - When `?from=feature`: emit `<div id="breadcrumb" hx-swap-oob="true">` containing "Dashboard / Feature / Story"
  - When `?from=sprint`: emit `<div id="breadcrumb" hx-swap-oob="true">` containing "Dashboard / Sprint / Story"
  - Rightmost segment ("Story") styled accent blue, preceding segments gray + clickable links
  - "Dashboard" links to `/`; "Feature" links back to `/features/{feature_slug}` (derived from story frontmatter `feature_slug`); "Sprint" links back to `/sprints/{active_sprint_slug}` — read active sprint slug from `.momentum/sprints/index.json` at request time and use the same slug pattern as the sprint detail route

- [ ] **Task 5 — Story row navigation wiring in L2 and Sprint Detail** (`script-code`)
  - In the Feature L2 stories list (route `/features/{slug}`), ensure each story row link is wired: `hx-get="/stories/{story_slug}?from=feature"` `hx-push-url="/stories/{story_slug}"` `hx-target=".pane-inner"` `hx-swap="innerHTML"`
  - In the Sprint detail view (route `/sprints/{slug}`), ensure each story row link in outcome bands is wired: `hx-get="/stories/{story_slug}?from=sprint"` `hx-push-url="/stories/{story_slug}"` `hx-target=".pane-inner"` `hx-swap="innerHTML"`
  - Confirm `hx-push-url` updates browser address bar correctly so back/forward works

- [ ] **Task 6 — Graceful 404 handling** (`script-code`)
  - If `.momentum/stories/{slug}.md` does not exist, return a simple HTML fragment with "Story not found: {slug}" message styled in the reading mode container; HTTP 200 is acceptable for HTMX fragment responses (no redirect needed)

## Dev Notes

### Architecture Compliance

This story implements DEC-019 (Hono+HTMX+Bun runtime stack). All routing goes through `skills/momentum/skills/canvas/server.tsx` — the single-file Hono server.

Key constraints from the decision:
- One Hono server file. No separate build step, no bundler. Bun runs TypeScript directly.
- HTMX handles all navigation. No client-side router.
- Polarity flip (dark ↔ light) is a CSS class swap on `.pane-inner` with 140ms transition — defined when L2 was built. L3 reuses the same class. Do not add a second transition definition.
- Breadcrumb updates use `hx-swap-oob="true"` — the breadcrumb element must have `id="breadcrumb"` in the shell HTML.
- `hx-push-url` is set on the trigger element, not in the response. Browser history is maintained by HTMX automatically.

The story depends on:
- `momentum-cycle-feature-l2-drill-down-reading-mode` — provides the L2 stories list where story row links must be wired (Task 5)
- `momentum-cycle-sprint-lens-sprint-detail-drill-down` — provides the sprint detail outcome bands where story row links must be wired (Task 5)

Both dependencies must be merged before this story can be fully validated, as Task 5 modifies both routes.

### Testing Requirements

Change type is `script-code` (Hono route handler, markdown parser, HTML template). Use TDD via bmad-dev-story:

1. **Red:** Write tests for the markdown parser (Task 2) first — test frontmatter extraction, AC list extraction, dev notes truncation logic, and `touches` rendering.
2. **Green:** Implement the parser to make tests pass.
3. **Refactor:** Clean up; keep tests green.

The Hono route handler (Task 1) and HTML template (Task 3) are integration-level and can be verified by manual inspection in the cmux browser pane — load `http://localhost:3456/stories/momentum-cycle-story-l3-drill-down-reading-mode?from=feature` and verify visually against ACs 1–16.

### Implementation Guide

#### Reading the Story `.md` File

Story files are at `.momentum/stories/{slug}.md`. Use `Bun.file()` and `.text()` to read:

```typescript
const file = Bun.file(`.momentum/stories/${slug}.md`)
if (!await file.exists()) { /* return 404 fragment */ }
const raw = await file.text()
```

Frontmatter split: split on `---\n` — first block after initial `---` is YAML frontmatter, remainder is markdown body.

Parse frontmatter fields manually (no heavy YAML library needed for the small set of fields used):
- `touches:` may be a YAML list (multiline `- item` entries) or inline `[item1, item2]`
- `derives_from:` may be absent — handle gracefully

#### Polarity Transition

The `.reading-mode` CSS class on `.pane-inner` triggers the 140ms warm-light background. This class was defined in the L2 story implementation. L3 emits the same class. The CSS transition fires automatically when the class is added — no JavaScript needed beyond what HTMX already does.

For the sprint entry point: the sprint detail view is dark mode. When the user clicks a story row, HTMX swaps `.pane-inner` innerHTML with the L3 fragment (which carries `.reading-mode`). The existing CSS transition handles the visual fade. This is zero additional code.

#### Dev Notes Collapse

Use native `<details>`/`<summary>`:

```html
<details class="dev-notes">
  <summary>Dev Notes (click to expand)</summary>
  <div class="dev-notes-body">... full content ...</div>
</details>
```

Collapse threshold: if the dev notes body contains >3 block-level items (paragraphs, list items, subsections) OR is longer than 400 characters, wrap in `<details>`. Otherwise render inline.

#### Breadcrumb Back Links

The "Feature" breadcrumb segment links back to `/features/{feature_slug}`. Derive `feature_slug` from the story frontmatter's `feature_slug` field. The "Sprint" segment links to `/sprints/{active_sprint_slug}` — derive the active sprint slug from `.momentum/sprints/index.json` at request time (read `.active` field if present, else read `.planning.stories[0]` sprint context). Use the same URL pattern as the sprint detail route (`/sprints/{slug}`).

### Project Structure Notes

All changes in this story go into `skills/momentum/skills/canvas/server.tsx` (the single Hono server file for the canvas). Story markdown parsing utilities may be extracted into a small helper in the same file or a sibling `server-utils.ts` if the main file exceeds 400 lines.

No new directories or config files are created by this story.

### References

- **DEC-019** — Hono+HTMX+Bun runtime stack: `_bmad-output/planning-artifacts/decisions/dec-019-hono-htmx-bun-canvas-runtime-stack-2026-05-03.md`
- **DEC-011** — Canvas rename + state paths (D1 and D3 still in force): `_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md`
- **Dependency story L2**: `.momentum/stories/momentum-cycle-feature-l2-drill-down-reading-mode.md` — defines reading mode polarity, CSS transition, breadcrumb pattern
- **Dependency story Sprint Detail**: `.momentum/stories/momentum-cycle-sprint-lens-sprint-detail-drill-down.md` — defines sprint detail outcome bands and story row structure
- **Design prototype reference**: 10-pass Claude Design session (claude.ai); Pass 10 locked breadcrumb nav model; Pass 6 defined L3 typography spec

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5, 6 → script-code (TDD)

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively — the implementation guidance below matches its standard approach:

1. **Red:** Write failing tests for the task's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** The Hono server lives at `skills/momentum/skills/canvas/server.tsx`. Follow the pattern already established by prior canvas stories (dashboard shell, L2, sprint detail) for route structure and HTML fragment composition.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies — listed here for reference):**
- Tests written and passing for markdown parser (Task 2)
- Manual integration verification in cmux browser pane for Hono route and HTML template
- No regressions in existing canvas routes (dashboard, features lens, sprint detail, L2)
- Code quality checks pass if configured

**Gherkin specs note:** Gherkin `.feature` specs exist for this sprint in `sprints/{sprint-slug}/specs/`. Per Decision 30 (black-box separation), the dev agent implements against the plain English ACs in this story file only. Never read or reference `.feature` files during implementation.

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
