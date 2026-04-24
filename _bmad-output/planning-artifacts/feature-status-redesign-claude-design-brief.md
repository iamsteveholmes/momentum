---
title: Feature Dashboard Redesign — Claude Design Handoff Brief
owner: Steve
prepared_by: Sally (bmad-agent-ux-designer)
date: 2026-04-19
target_tool: Claude Design (claude.com/design)
derives_from:
  - dec-006-artifact-redesign-dual-audience-2026-04-14.md
  - dec-005-cycle-redesign-feature-first-practice-2026-04-14.md
related_stories:
  - dashboard-ux-wireframes
  - feature-dependency-graph-ux-wireframes
revisions:
  - date: 2026-04-22
    note: >-
      Pass 1 returned from Claude Design; developer locked Variant B (cards).
      Scope expanded from feature dashboard to project canvas — see §14 for
      the three-view model (Features / Sprints / Flywheel). Skill rename
      flagged as open question. Original §1–§13 remain authoritative for the
      Features view; §14 is additive.
---

# Feature Dashboard Redesign — Claude Design Handoff Brief

## How to use this document

Start a new project in Claude Design. Paste the **Opening Prompt** (bottom
of this file) as the first chat message. Upload the files listed under
**Attachments** alongside it. Then iterate conversationally using the
**Design Questions** as anchors.

Claude Design inherits your organization's design system automatically;
this brief adds project-specific direction on top of that.

> **Revision note (2026-04-22).** Pass 1 returned with Variant B (card
> grid) locked as the Level-1 shape for the Features view. Shortly
> afterward the scope broadened from a feature dashboard to a full
> project canvas — three coordinated views (Features / Sprints /
> Flywheel). See **§14 Scope Expansion — Project Canvas** at the end of
> this document. Sections 1–13 remain authoritative for the Features
> view; §14 is additive and governs the canvas-level work.

---

## 1. Goal

Transform the current feature status page from a flat, static "status
report" into a hierarchical, navigable **feature-planning thinking space**
— the primary surface a solo developer uses at the start of each session
to see what the product is, what it does, what's missing, and where to go
next.

The developer's framing (direct quote):

> Features, end-to-end workflows, and abilities are about 75% of the work.
> Most other things are bugs and dependencies. This document should close
> the user's knowledge gap about what it requires to build something.

The redesign is read-only, generated from JSON data by a skill. The UX
must feel like a document you want to read, not a dashboard you have to
scan.

---

## 2. Audience

**Primary user — the developer.**
- Solo developer working with AI collaborators across multiple projects.
- Senior, tool-fluent, reads docs at speed, hates fake progress signals
  (no velocity charts, no percentages, no gamification).
- Uses the dashboard daily, in a terminal-multiplexer browser pane
  (cmux) — not a public-facing surface.
- Values narrative over data density. A paragraph that explains *why*
  this feature exists is more useful than a KPI.

**Secondary user — the AI collaborator.**
- Reads the same artifacts the developer does, to stay contextually
  aligned. Human-readable narrative serves both.

**Context of use.**
- Opens as a local `file://` in a browser pane. No server, no auth.
- Inspected in 30–60 second bursts between other work.
- Often re-opened mid-task to check "what's the next feature I should
  care about?"

---

## 3. Current state — what exists today

The live artifact is a single flat HTML page:

- Header with generation timestamp.
- A row of stat cards (Total / Working / Partial / Not Started / With Gaps).
- A collapsed Mermaid dependency graph (being retired per DEC-006 D3).
- Three stacked tables grouped by feature type (flow / connection / quality).
- Each row: feature name, status badge, story fraction, gap flag,
  expandable details.

It works. It's legible. But it's a **report**, not a **thinking space** —
no drill-down, no narrative room for the feature's value story, no way to
read a story's human context without opening the source file.

Please review `feature-status.html` (attached) to calibrate on the
starting point before designing the new shape.

---

## 4. Vision — the three-level hierarchy (from DEC-006)

The dashboard becomes an HTML *directory* of linked pages with
back-navigation:

```
Level 1 — Index
  └── Level 2 — Feature drill-down
        └── Level 3 — Story drill-down
```

**Level 1 — Index.** All features at a glance, state, story coverage,
gap flags. Entry point to everything.

**Level 2 — Feature drill-down.** Full feature summary, value narrative,
acceptance condition, story list with gaps, and a story-level dependency
graph bounded to this feature.

**Level 3 — Story drill-down.** Collapses to the story's **human
section** (narrative, paragraph-style) — not the dense LLM execution
spec. For stubs, renders a graceful "content pending" state.

---

## 5. Information architecture — what lives at each level

### Level 1 — Index page

Each feature is represented by (card or row — design choice):

- Feature name (primary, bold)
- Type group (flow / connection / quality) — used for grouping
- One-line purpose (from `description` field, truncated)
- State badge (see Status Semantics below)
- Story coverage as a fraction (`5/7`) — no percentage, no progress bar
  unless minimalist
- Gap flag when `has_gap == true` (a quiet indicator, not an alarm)

**Sort within each type group:**
1. Features with gaps first
2. Then `not-working` → `partial` → `working` → `not-started`
3. Within each band, alphabetical by name

**Navigation pattern.** Clicking any feature opens its Level 2 page.
Index page is always one click away via breadcrumb.

### Level 2 — Feature drill-down page

- **Page title** — feature name
- **Breadcrumb** — `Dashboard › {type} › {feature name}`
- **Meta strip** — state badge, story fraction, type label

Body sections (in order):

1. **Value narrative** — the `value_analysis` field rendered as prose
   in a readable column. This is the feature's *story*, not its spec.
   It's the single most important element on the page. Give it
   typographic room.
2. **Acceptance condition** — a boxed one-paragraph block. Crisp,
   declarative. Answers "what does done look like?"
3. **System context** — the `system_context` field, rendered as a
   short callout explaining how this feature relates to the rest of the
   product.
4. **Stories list** — assigned stories with status icons. Each story
   links to Level 3.
5. **Gaps** — explicit, prose. Example: "Acceptance condition requires
   X; assigned stories only cover Y. Missing: Z." Shown only when a gap
   exists.
6. **Story-level dependency graph** (DEC-006 D3) — scoped to this
   feature: implementing stories + non-feature stories those depend on
   (bugs, supporting maintenance, infrastructure). Data source is the
   `depends_on` field in `stories/index.json`.

### Level 3 — Story drill-down page

- **Breadcrumb** — `Dashboard › {type} › {feature name} › {story title}`
- **Story title** as page header
- **Meta strip** — status, sprint assignment (if any), date last touched
- **Body** — the story's **human section** (DEC-006 D1). Prose. Narrative.
  Warm. For feature stories, may inherit the Feature Judgment Frame from
  the parent feature.
- **If the story is a stub** (no human section yet) — render "Content
  pending" gracefully. Not an error. A clear, calm placeholder with a
  hint: "Run `momentum:create-story` on this story to enrich."

---

## 6. Key design questions to answer in wireframes

1. **Does a Journey/Workflow layer belong between Index and Feature?**
   The developer's framing emphasizes "end-to-end workflows" as peer
   to features. Some features are atomic abilities; others are stops on
   a user journey (e.g., "Session Prep Loop — open app to play-ready"
   spans multiple features). Explore both: (a) no journey layer, with
   cross-linking between related features; (b) an explicit journey layer
   that groups features participating in the same end-to-end flow. Show
   wireframes of both and name a recommended default.

2. **Dependency graph scale bounds.** DEC-006 D3 repurposes the graph
   to story-scope because the project-scope version was unreadable. At
   what node count does even the story-scope graph become noise? Design
   the fallback: collapse transitive, tab between direct/transitive,
   switch to a list when N > threshold, or a different visualization
   entirely. Make the scale decision explicit in the wireframe.

3. **Index density.** ~20 features today, growing to ~40. Card grid?
   Compact table? Type-banded sections with sticky headers? Solve for
   fast scan + single-click drill. Show at least two density treatments.

4. **Status semantics and visual treatment.** Active states:
   `working`, `partial`, `not-working`, `not-started`. Terminal states
   (per DEC-005 D6): `Done`, `Shelved`, `Abandoned`, `Rejected`. Design
   the visual hierarchy so terminal states feel *settled*
   (de-emphasized, neutral) while active states draw attention. Avoid
   traffic-light melodrama — the developer is not a stoplight.

5. **Stub-tolerant rendering.** Most backlog stories are stubs with no
   human section. Design what a Level-3 page looks like when content is
   missing — calm placeholder, not a broken page, not a scolding.

6. **Staleness signal.** The dashboard is generated from a content
   hash of the input JSON files. When inputs change after render, the
   dashboard should show a subtle "refresh available" affordance —
   without alarming the developer.

7. **Dark-mode parity.** The developer works in dark terminals. Show
   at least a light-mode full design + a dark-mode key-screen variant.

---

## 7. Visual and tonal direction

- **Sober professional.** Developer tool. Linear / Figma FigJam /
  Railway aesthetic. Not Notion gradients. Not SaaS marketing gloss.
- **Typographic-first.** The feature narrative is the product. Body
  text 15–16px, generous line-height, reading-column widths capped at
  ~72ch. Feature value narrative gets its own column of breathable prose.
- **Muted palette.** Neutral grays + one accent + status-coded badges.
  No rainbow. State colors should be distinguishable but calm: greens
  that don't scream, reds that warn without panicking, yellows that
  advise without demanding.
- **No motion unless it teaches.** Micro-transitions for drill-down are
  fine; decorative motion is not.
- **No emoji in UI.** Hard rule. The developer has explicitly asked
  for this — icons and text only.
- **No infantilizing copy.** No "Great job!", no "Oops!", no cheerleader
  voice. Developer-to-developer tone.

---

## 8. Technical constraints

- **Output shape.** Static HTML pages — one `index.html` plus
  per-feature and per-story drill-down pages, all linked relatively.
  Self-contained: inline CSS, no external stylesheet dependencies.
- **Renderability.** Opens as `file://` in a browser pane. No server,
  no build step at view time.
- **Acceptable dependencies.** Mermaid.js via CDN ESM import is fine for
  the dependency graph. Vanilla JS for interactions (collapse/expand,
  etc.) is fine. No frameworks — no React, Vue, Svelte.
- **Generation context.** An LLM-powered skill generates these files
  from JSON sources. Wireframes should not assume a front-end build
  pipeline.
- **Data volume.** ~20 features today, growing to ~40. Each feature has
  2–10 stories. `stories/index.json` is large (>10k tokens); partial
  reads are expected.

---

## 9. Deliverables requested from Claude Design

Please produce:

1. **Wireframes** (low-to-mid fidelity) for:
   - Level 1 index page
   - Level 2 feature drill-down page
   - Level 3 story drill-down page (with populated content + stub state)
2. **At least one wireframe variant** exploring a Journey/Workflow
   layer (Design Question 1).
3. **Dependency-graph wireframe** with explicit scale-bound decision
   (Design Question 2).
4. **Empty states** for stub stories and for first-use (no features
   populated yet).
5. **Navigation model diagram** — breadcrumbs, back-links, intra-
   dashboard links, with hover/active states.
6. **State-badge system** — visual treatment spec for both active and
   terminal states.
7. **One mid-fidelity mockup of a representative feature** end-to-end
   (e.g., "Sprint Planning — Backlog to Ready Sprint" from the attached
   `features.json`), showing the full text content populated from real
   data, so the developer can feel the reading experience.
8. **Dark-mode variant** of at least one key screen.

Iterate conversationally — the developer wants to refine specific
spacing, typography, and interaction details rather than accept a
single-pass design.

---

## 10. Non-goals — do not design these

- No authentication, no multi-user, no roles.
- No editing affordances. This is a **read-only** generated view.
- No metrics beyond story counts — explicitly no velocity,
  percentage-complete, burndown, estimated dates.
- No "design system claim." Momentum has no formal DS. Claude Design
  can propose primitives (badge, card, table, graph container,
  breadcrumb) and we'll formalize them later.
- No marketing surface. This is not shown to stakeholders.

---

## 11. Attachments to upload with this brief

Drop these files into the Claude Design project alongside the opening
prompt:

**Current artifacts (what exists today — the baseline to move from):**
- `.claude/momentum/feature-status.html`
- `.claude/momentum/feature-status-mockup.html`

**Source data (to populate mockups with real content):**
- `_bmad-output/planning-artifacts/features.json`
- `_bmad-output/implementation-artifacts/stories/index.json`

**Governing decisions (the "why" behind the redesign):**
- `_bmad-output/planning-artifacts/decisions/dec-006-artifact-redesign-dual-audience-2026-04-14.md`
- `_bmad-output/planning-artifacts/decisions/dec-005-cycle-redesign-feature-first-practice-2026-04-14.md`

**Prior research (frames the visualization space):**
- `_bmad-output/research/feature-status-visualization-2026-04-11/final/feature-status-visualization-final-2026-04-11.md`

**Pending backlog stubs (Claude Design's output will flow into these
stories when the developer returns to Momentum):**
- `_bmad-output/implementation-artifacts/stories/dashboard-ux-wireframes.md`
- `_bmad-output/implementation-artifacts/stories/feature-dependency-graph-ux-wireframes.md`

---

## 12. Opening prompt — paste this as the first message

```
I'm redesigning a read-only developer dashboard that's currently a flat
HTML status report. The target is a three-level hierarchical directory
(index → feature drill-down → story drill-down) that reads like a
thinking space, not a report.

Please review the attached brief document first — it contains the goal,
audience, information architecture, design questions, visual direction,
and technical constraints. Then review the attached current artifact
(feature-status.html) to understand what we're moving away from. Finally,
skim features.json and stories/index.json so mockups can be populated
with real content.

Start with two things in parallel:

1. A wireframe for the Level-1 index page using the real feature data
   from features.json. Show a compact-table density treatment and a
   card-grid density treatment side by side.

2. A visual exploration of the state-badge system covering both active
   states (working, partial, not-working, not-started) and terminal
   states (Done, Shelved, Abandoned, Rejected). Muted palette. No emoji.

Once I've reacted to those, we'll move to Level 2 and Level 3, the
dependency graph scale question, and the Journey/Workflow layer
exploration.

Design tone: sober, typographic-first, Linear/Figma-adjacent. No
emoji, no percentages, no velocity, no infantilizing copy. Read the
"Visual and tonal direction" and "Non-goals" sections of the brief
carefully — they are hard constraints, not preferences.
```

---

## 13. After Claude Design produces wireframes — what to do with the output

When you're happy with the designs in Claude Design:

1. **Export the wireframes / mockups** from Claude Design as images or
   a shareable link.
2. **Run `momentum:create-story` on `dashboard-ux-wireframes.md`** — the
   Claude Design output becomes the deliverable attached to that story.
3. **Run `momentum:create-story` on `feature-dependency-graph-ux-wireframes.md`**
   for the graph-specific wireframe output.
4. **Phase 3 of DEC-006 can then begin** — the `feature-status` skill
   rewrite to generate the new hierarchical HTML directory, implementing
   against the approved wireframes.

This brief is the artifact that bridges "design intent" to "design
output" to "implementation story." Keep it with the wireframes as the
provenance record.

---

## 14. Scope Expansion — From Feature Dashboard to Project Canvas

**Added 2026-04-22.** After reviewing Pass 1 output, the developer
identified that features-and-stories, while critical, are only one
lens on project health. The artifact should broaden into a full
project canvas with three coordinated views sharing one design
system. This section governs the expanded work; §1–§13 remain
authoritative for the Features view that Pass 1 already designed.

### 14.1 Inspiration reference

Cursor 3.1's Canvas view — a single rich surface where lenses
switch rather than deep navigation tree traversal. Not a direct
clone (Cursor's Canvas is a live app; we generate static artifacts),
but the *model* of "one surface, multiple coordinated lenses" is the
target experience.

### 14.2 The three views

Each view is a legitimate lens; merging them into one flat page
flattens meaning. They share palette, typography, badges, and
navigation chrome — they differ in the information they surface.

**View 1 — Features** *(designed, Variant B locked)*
What the product **is**. The feature taxonomy, story coverage,
gaps, value narratives. Already designed — this is what Pass 1 of
Claude Design produced. Treat as stable baseline.

**View 2 — Sprints** *(new — needs design)*
What the practice is **doing right now**. Expected content:
- Active sprint: name, stories in flight, in-wave, merged, blocked
- Recent sprints: a short backward-looking window (last 3–5)
- Merge queue state: what's pending, what's gated, what failed
- Quality-gate signal per sprint (AVFL, code-review, E2E passes/fails)
- Cross-cutting view: which features this sprint is advancing

This view makes the relationship between story-execution and
feature-progress visible — right now, the developer has to piece
that together from Impetus + feature-status + memory.

**View 3 — Flywheel** *(new — needs design)*
How the practice is **compounding**. Expected content:
- Retro findings ledger: accumulating patterns across sprints
- Distilled artifacts: which skills/rules/agents were produced from
  which retros — the full provenance chain from finding → distillation
- Quality-gate trend: failure types over time, which ones are
  decreasing, which recurring
- Feature progress over time: not "velocity" but "which features
  advanced this month, which stalled, which shipped"
- Practice-health signals: the living loop visualized

The Flywheel view is the one that turns a sprint log into a
*practice*. It is also the view with the most open interaction-
design questions — is it a timeline? A dashboard? A living graph?

### 14.3 Navigation model — open for exploration

Three candidates for Claude Design to wireframe:

- **Tabs** — top of canvas: `Features · Sprints · Flywheel`. Familiar,
  simple, each view is a distinct page.
- **Sidebar** — left rail with view switcher. Allows persistent
  peripheral context (e.g., current sprint banner across all views).
- **Single long-scroll canvas** with anchored sections. Zero
  navigation friction; the full picture is always one scroll away.
  Closest to Cursor Canvas's model.

No pre-decided default — ask Claude Design to show all three and
recommend one with rationale.

### 14.4 Tech decision — deliberately open

The existing brief (§8) specifies static HTML, self-contained, no
frameworks. That constraint held cleanly for the Features view. The
Sprints and Flywheel views may justify richer interactions — drill
from a retro finding to the story it generated to the distilled
skill, for example — and the tech decision should be revisited *once
the information design is clear*.

Three options, in increasing complexity:

1. **Vanilla HTML + light JS** (current Pass 1 path). Simple.
   Maintainable by the skill. Flywheel view may feel flat.
2. **React + ReactDOM via CDN + Babel Standalone for JSX.** No
   build step, works from `file://`, handles the JSX Claude Design
   already produces. Middle path. Larger artifact, richer
   interactions.
3. **Small Vite/esbuild step inside the skill.** Closest to Cursor
   Canvas parity. Adds complexity to the skill's generation path.

**Rule for this decision.** Design the information first. Pick the
tech after seeing whether the views *need* interactivity. Do not
let tech preference dictate information design.

### 14.5 Skill-rename question

If the artifact broadens to a project canvas, `momentum:feature-status`
becomes a misleading name. Candidates:

- `momentum:canvas`
- `momentum:project-canvas`
- `momentum:status` (broadens scope of the name)

Not decided. Flagged as an open question; the rename decision should
be made via `momentum:decision` before the skill rewrite lands, not
inside the wireframe iteration loop.

### 14.6 What stays locked from earlier sections

The following Pass-1 decisions carry forward to the canvas and are
**not** open for redesign:

- Variant B (card grid) for the Features view Level-1 layout
- Color palette: warm paper, soft ink, muted indigo accent, warm
  terracotta gap flag
- Typography stack: Inter (UI), Source Serif 4 (narrative),
  JetBrains Mono (meta)
- Badge system: active vs terminal, dot-first, monospace label
- Terminal-state opacity treatment (55–75%)

New views must share these primitives. Consistency across the three
views is the whole point — no view should feel like a different
product.

### 14.7 Updated deliverables for the next Claude Design pass

On top of the already-queued Pass 2 Features-view tweaks (half-
width stress test, gap-flag relocation, meta-strip fixes), Claude
Design should produce:

1. **Canvas-level navigation wireframes** — three candidates (tabs,
   sidebar, long-scroll). Recommend one.
2. **Sprints view — Level 1 wireframe** using real sprint data
   (request sample from developer; sprint index files are at
   `_bmad-output/implementation-artifacts/sprints/*/`).
3. **Flywheel view — Level 1 wireframe** with exploration of how
   the compounding loop renders. This is the most open question;
   produce at least two distinct directions.
4. **Cross-view interactions** — how does clicking a feature from
   Features navigate into Sprints (which sprints advanced it)? How
   does a retro finding in Flywheel link back to the story it
   produced?

The Features view wireframes (Variant B) remain the baseline —
these new views extend the canvas, they do not replace the work
already locked.
