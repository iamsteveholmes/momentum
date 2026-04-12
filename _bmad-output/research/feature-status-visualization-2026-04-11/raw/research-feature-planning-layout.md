---
content_origin: claude-code-subagent
date: 2026-04-11
sub_question: "Feature planning artifact layout and design"
topic: "Feature planning artifact visualization"
---

## Overview

This document synthesizes research into how leading developer-facing planning tools visually structure feature status. The goal is actionable design decisions for a static HTML + Jinja2 + Mermaid.js artifact rendered in a cmux browser pane, displaying features with statuses (working/partial/not-working/not-started), story coverage, type metadata, and acceptance conditions.

---

## How Linear Structures Feature and Project Views

Linear is the reference-point developer planning tool as of 2025, built explicitly for engineering teams. Its visual language establishes patterns that developer audiences now expect.

### The Initiative / Project / Issue Hierarchy

Linear operates on three semantic levels: **Initiatives** (strategic groupings), **Projects** (cross-team efforts with outcomes and timeframes), and **Issues** (individual work items). This maps well to the features-stories model: features are analogous to projects, stories to issues.

**Initiative overview row signals** — each initiative in the list view displays: **[OFFICIAL]**

- Initiative name + short summary
- Owner (avatar)
- Associated teams
- **Number of projects within** (a count — not just a progress bar)
- Target date
- Health status (On Track / At Risk / Off Track, color-coded green/yellow/red, or grey for stale)

This is the key lesson: Linear makes the **contained-item count a top-level visible signal**, not buried inside a detail view. Teams can see "this initiative has 4 projects" in the list without clicking through.

### Project-Level Progress Display

At the project level, Linear shows progress as an **initiative graph** — a curve representing cumulative completed issues over time. For list views, the project bar shows health status as a colored icon next to the project name. **[OFFICIAL]**

Progress is **manually updated** (health status requires explicit team input) rather than auto-calculated — a deliberate design choice. This prevents misleading green indicators when issues are stale or redefined. For a static artifact rendered from a JSON schema, this supports computed-from-schema calculations rather than requiring live issue sync.

### What Linear Does Not Do

Linear does not show "X of Y stories done" as an inline column in project lists. Issue counts appear at the initiative level (projects per initiative). Individual project progress is visualized through the manual health icon and a velocity graph — not a fraction. This indicates that **fraction display (N done / M total)** is a non-default advanced signal — useful when explicitly needed, but not the default mental model teams use. **[UNVERIFIED]**

---

## How Productboard Structures Feature Status

Productboard's model is product-management-facing but has deep integration with engineering backlogs. Its 2025 experience (new workspaces) uses grids, timelines, and column boards. **[OFFICIAL]**

### The Status Signal Model

Every feature and subfeature has a **status, indicated by a colored square or circle** that appears near the entity's name across most board types. This is the most prominent per-feature signal — essentially an always-visible badge. **[OFFICIAL]**

Productboard supports customizable status values. Internal teams use statuses like: Candidate, Planned, In Progress, Shipped. The status badge is the primary information scent — it answers "what stage is this feature in" at a glance.

### Column Fields Available

In grid/table layouts, columns can include: **[OFFICIAL]**

- Feature name (with hierarchy indent for subfeatures)
- Status (colored badge)
- Owner
- Effort (numeric — story points, person-weeks, etc.)
- Tags / labels
- Target timeframe (visualized bar that snaps to time horizons)

**Horizontal grouping** allows dividing items by field values or hierarchical position, so features of the same type can be grouped into visual swim lanes.

### The Coverage Gap

Productboard does not natively display "stories needed to complete this feature" as a count. It manages features and their prioritization scores, but story coverage is tracked in a separate integration layer (Jira, Linear, etc.). This means for a self-contained artifact like the momentum features.json schema, **story count is novel signal that established tools don't foreground** — it's a gap this artifact can fill.

---

## How Aha! Represents Features and Story Breakdown

Aha! operates at strategic scale — roadmaps, initiatives, releases, epics, features, requirements. Its hierarchy report is the closest analogue to a feature coverage view. **[OFFICIAL]**

### Hierarchy and Progress Display

The **hierarchy report** visualizes relationships across goals, initiatives, releases, epics, and features within a single workspace. Key signals per feature row: **[OFFICIAL]**

- Feature name (with parent epic/initiative context)
- Status (configurable — typically New, In Development, Shipped)
- Progress bar (for features with requirements/stories: green fill showing percent complete)
- Release assignment

Aha! adds **progress bars per feature** when the feature has child requirements. The progress formula is: completed requirements / total requirements. This is the most direct precedent for showing "stories done / stories total" as a visual ratio.

### Requirements as Stories

In Aha!'s model, requirements are analogous to stories. When synced to Jira or Pivotal, each requirement becomes a linked story. The features roadmap can display a **completion percentage based on the progress calculation set on each record.** **[OFFICIAL]**

Aha! also allows showing "tags, status, or progress" as optional overlays on roadmap bars — defaulting to off to reduce clutter, with users explicitly enabling them.

### Design Lesson from Aha!

Aha! demonstrates the **optional-overlay pattern**: prominent signals (name, status, dates) are always shown; secondary signals (progress %, requirement count) are enabled by the user. For a static artifact, this suggests: always show status badge + story count; defer raw acceptance condition text to an expandable section.

---

## How Jira / Advanced Roadmaps Shows Epic-to-Story Coverage

Jira is the most widely deployed planning tool and has direct story-coverage visualization in its timeline. **[OFFICIAL]**

### Epic Progress Bar Design

On the timeline view, each epic bar displays a **tri-color progress bar beneath it**: **[OFFICIAL]**

- **Green segment**: stories marked Done
- **Blue segment**: stories In Progress  
- **Grey segment**: stories in To Do

The bar is proportional to story count. No inline fraction label (X of Y) is shown by default, but the segments are sized to make proportional completion visually obvious.

### Key Formula

Progress = resolved child issues / total child issues **[OFFICIAL]**

For issues without children, the binary is 100% if resolved, 0% if not. This means: **every feature needs at least one story to have meaningful progress visualization**.

### What Jira Does Not Show Inline

Jira does not show the total story count as an inline column by default. Users must open the epic or use a dashboard gadget to see "4 of 7 done." The timeline bar is the primary coverage indicator. Community discussions show strong demand for an inline fraction, suggesting it is underserved by current tools. **[PRAC]** (Atlassian Community, multiple threads, 2023-2025)

This is a clear opportunity: displaying `stories: 2 done / 5 total` as an inline column is something practitioners want but existing tools make difficult.

---

## Visual Layout Patterns: What Works for Feature Coverage

### Pattern 1: Table/List View as Primary Layout

Across Linear, Productboard, GitHub Projects, and Jira, the table/list view is the workhorse planning layout for developer audiences. It supports: **[OFFICIAL across tools]**

- **Dense information per row** — developers can scan more features per viewport than card/kanban layouts
- **Sortable/filterable columns** — status, priority, type
- **Inline metadata without clicks** — story count, progress, dates visible at a glance
- **Hierarchy indentation** — subfeatures appear as indented children of parent features

Kanban/board view is favored when the primary question is "what's moving through stages" — useful for sprint execution, less useful for coverage analysis.

**Decision for the features.json artifact**: Table/list layout is correct for a feature-status planning artifact. The primary question ("which features have gaps?") is a scanning/filtering task, not a flow/movement task.

### Pattern 2: Status Badge as the Loudest Signal

Every tool studied uses a **colored badge or dot as the primary per-item signal**:

- Productboard: colored square/circle beside feature name
- Linear: health icon (green/yellow/red dot) beside project name
- Jira: status pill in a dedicated column
- IBM Carbon Design System: geometric shape + color + icon (minimum three elements for WCAG compliance) **[OFFICIAL]**

Carbon's guidance is precise: red = error/danger, orange = serious warning, yellow = warning, green = success, grey = not started. **Never use the same shape in different colors within the same experience.**

For the four-state schema (working / partial / not-working / not-started):

| Status | Color | Signal |
|---|---|---|
| working | green | checkmark or filled circle |
| partial | amber/yellow | half-filled or warning icon |
| not-working | red | X or error icon |
| not-started | grey | empty circle or dash |

### Pattern 3: Story Count as Secondary Column

No tool studied shows story count as a mandatory primary column. It appears as:

- A parenthetical in initiative overviews (Linear: "4 projects")
- A progress bar (Jira, Aha!)
- A hover tooltip or dashboard gadget (Jira community workarounds)

For the features.json artifact, displaying **story count as a dedicated column** — e.g., `Stories: 3/5` or a mini progress bar — fills a real gap and makes coverage immediately actionable. This is a differentiator over existing tools.

### Pattern 4: Feature Type as a Grouping Dimension

Aha!, Productboard, and GitHub Projects all support grouping by a categorical field (type, label, team). For a schema with three feature types (flow/connection/quality), **grouping by type** allows the artifact to surface patterns like "all quality features are not-started" at a glance.

This is better as a **group header row** than as a column, because:
- It reduces repetition (type appears once per group, not on every row)
- It creates visual separation between feature categories
- It allows status summaries per group (e.g., "flow: 3/8 working")

### Pattern 5: Progressive Disclosure for Acceptance Conditions

Acceptance conditions (verbose text, stories array detail) are secondary content. Every tool studied puts detail content behind a click/expand:

- Linear: click through to project detail
- Productboard: click feature to open sidebar
- Aha!: click feature to open full record

For an HTML artifact, acceptance conditions should be in a **collapsible section** (HTML `<details>`/`<summary>` or JavaScript toggle), not inline. Stories can show as a compact list: `[STORY-001] Write auth token validation` with a done/pending indicator.

---

## What Makes Planning Artifacts Actionable vs. Abandoned

Research into roadmap adoption failures reveals consistent patterns: **[PRAC]** (Tempo/Forrester study, multiple sources 2024-2025)

### Why Teams Abandon Planning Artifacts

1. **Too complex to maintain** — when updating the artifact requires significant manual effort, teams stop updating it, and it becomes stale and useless. A static HTML rendered from features.json avoids this: the schema is the source of truth, the artifact is generated.

2. **Too many views and features** — Productboard, Jira, Aha! all have this problem. Teams resist tools that "get in the way of their work" with a "dizzying list of views, features, add-ons, and reports." **[PRAC]** A single-purpose artifact with one well-designed view avoids this.

3. **Visibility gap** — 59% of executives believe their teams use roadmaps; only 28% of directors/managers say the same. **[PRAC]** An artifact that lives in the workflow (cmux browser pane, always visible during dev sessions) closes this gap.

4. **Date-driven fiction** — Committing to specific dates in a planning artifact damages credibility when they slip. **[PRAC]** Status-based (not date-based) artifacts avoid this failure mode — the momentum features.json schema uses status states, not dates.

### Design Principles That Predict Adoption

From dashboard UX research: **[PRAC]** (Pencil & Paper, UXPin, Evil Martians 2024)

- **F-pattern scanning**: Most critical information in top-left. Status badge + feature name should anchor the left side; story count and gap indicator follow naturally.
- **Deliberate defaults**: Show only truly useful data by default. "Defaults that don't show #allthethings" — resist adding every field from features.json to the main table.
- **Progressive disclosure**: Secondary information (acceptance condition text, full story list) behind expand. First-level reading is a table scan; second-level is drill-down.
- **Structural grouping**: Group related items conceptually so users understand what to consider together. Feature type groups (flow/connection/quality) with per-group summaries achieve this.
- **Tables for structured data**: Table pattern with clear visual hierarchy — bold column headers, lighter data cells, color coding for distinction, sticky headers for navigation. **[OFFICIAL]** (Evil Martians dev tool UI patterns, 2024)

### The "Steel Thread" Principle

Effective planning artifacts create a seamless connection from strategic view to execution detail — executives see portfolio, developers see their assigned items. For the features artifact, this means: the table row is the executive view (status badge, coverage ratio); the expanded detail is the developer view (specific story IDs, acceptance condition).

---

## Rendering in a cmux Browser Pane: Specific Constraints

The target environment (HTML in a cmux pane) introduces constraints not present in cloud planning tools:

1. **No server-side filtering** — all filtering must be client-side JavaScript or pre-rendered. Prefer a single well-structured view over a multi-tab interface requiring server state.

2. **Fixed viewport width** — browser panes are narrower than full desktop. Prioritize fewer, wider columns over many narrow columns. A 5-column table (type-icon | feature name | status badge | story count bar | gap indicator) is likely the limit before horizontal scroll becomes necessary.

3. **Dark/light mode** — cmux environments vary. Use CSS variables for color tokens; avoid hardcoded hex colors that fail in dark mode.

4. **Mermaid.js for graphs** — the tech stack includes Mermaid.js. Feature dependency or coverage flow graphs can be rendered as Mermaid diagrams inside `<details>` blocks — visible on expand, not cluttering the main table.

5. **No real-time update** — the artifact is a snapshot rendered from features.json. Timestamps should be shown prominently so readers know data freshness.

---

## Recommended Column Structure for the Features Artifact

Based on all findings, the recommended table structure is:

| Column | Content | Prominence |
|---|---|---|
| Type | Icon (flow/connection/quality) + group header | Grouping dimension, not repeated per row |
| Feature name | Name + brief description (truncated) | Primary — bold, widest column |
| Status | Colored badge (working/partial/not-working/not-started) | Secondary — immediately after name |
| Story coverage | `N/M` fraction + mini progress bar | Secondary — dedicated column |
| Gap indicator | `GAP` badge if status != working and stories < 2 | Tertiary — action signal |

**Per-group header row** should show: type name, count of features in group, count with gaps.

**Row expand** (HTML `<details>`) should show: acceptance condition text, story list with done/pending state per story.

---

## Sources

- **[OFFICIAL]** Linear documentation — Initiatives, Project Status, Docs: https://linear.app/docs/initiatives, https://linear.app/docs/project-status
- **[OFFICIAL]** Linear Changelog — Initiative Updates (2025-02-13): https://linear.app/changelog/2025-02-13-initiative-updates
- **[OFFICIAL]** Linear Changelog — Project Progress Reports (2023-08-16): https://linear.app/changelog/2023-08-16-project-progress-reports
- **[OFFICIAL]** Productboard Support — Feature Boards Workflow Examples: https://support.productboard.com/hc/en-us/articles/4413906869139-Examples-of-feature-boards-for-modeling-each-stage-of-your-workflow
- **[OFFICIAL]** Productboard Support — Customize Status Values: https://support.productboard.com/hc/en-us/articles/360058171114-Customize-status-values-for-features
- **[OFFICIAL]** Productboard Support — Roadmap Card Attributes: https://support.productboard.com/hc/en-us/articles/32868506415123-Customize-your-roadmaps-with-card-attributes
- **[OFFICIAL]** Aha! Support — Features Roadmap: https://support.aha.io/aha-roadmaps/support-articles/roadmaps/features-roadmap
- **[OFFICIAL]** Aha! Support — Hierarchy Report: https://support.aha.io/aha-roadmaps/support-articles/analytics/hierarchy-report
- **[OFFICIAL]** Atlassian — See Progress of an Epic on the Timeline: https://support.atlassian.com/jira-software-cloud/docs/see-the-progress-of-an-epic-on-the-timeline/
- **[OFFICIAL]** Atlassian — Advanced Roadmaps Progress Tracking: https://confluence.atlassian.com/advancedroadmapsserver/tracking-progress-and-status-814212695.html
- **[OFFICIAL]** GitHub Docs — Changing Layout of a View: https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/changing-the-layout-of-a-view
- **[OFFICIAL]** IBM Carbon Design System — Status Indicator Pattern: https://carbondesignsystem.com/patterns/status-indicator-pattern/
- **[PRAC]** Evil Martians — 5 Essential Design Patterns for Dev Tool UIs (2024): https://evilmartians.com/chronicles/keep-it-together-5-essential-design-patterns-for-dev-tool-uis
- **[PRAC]** Pencil & Paper — UX Pattern Analysis: Data Dashboards: https://www.pencilandpaper.io/articles/ux-pattern-analysis-data-dashboards
- **[PRAC]** Tempo — Why Your Teams Aren't Using Your Roadmap: https://www.tempo.io/blog/why-your-teams-arent-using-your-roadmap-and-what-you-can-do-about-it
- **[PRAC]** UX Movement — The Right Way to Design Table Status Badges: https://uxmovement.substack.com/p/why-youre-designing-table-status
- **[PRAC]** Morgen — Linear Guide: Setup, Best Practices & Pro Tips: https://www.morgen.so/blog-posts/linear-project-management
- **[PRAC]** Atlassian Community — Epic Progress Visualization Discussions (2023-2025): https://community.atlassian.com/forums/Jira-questions/How-to-show-progress-in-percentage-per-epic-in-Jira-Advance-Roadmap/qaq-p/2725043
- **[PRAC]** Linear App Review (2026): https://www.siit.io/tools/trending/linear-app-review
