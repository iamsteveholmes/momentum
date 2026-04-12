---
title: "Feature planning artifact visualization — Research Report"
date: 2026-04-11
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: false
derives_from:
  - path: raw/research-feature-planning-layout.md
    relationship: synthesized_from
  - path: raw/research-useful-vs-overwhelming.md
    relationship: synthesized_from
  - path: raw/research-cli-generated-visual-artifacts.md
    relationship: synthesized_from
---

# Feature planning artifact visualization — Research Report

This report synthesizes findings across three research threads into actionable design decisions for a feature-status planning artifact generated from `features.json`, rendered as single-file HTML (Jinja2 + Mermaid.js) and opened in a cmux browser pane. The target reader is a solo developer orienting at session start — not a product manager running portfolio reviews.

The short version: build a single-view table grouped by feature type, lead with a colored status badge and a story-coverage fraction, put acceptance conditions and dependency diagrams behind `<details>` disclosure, and inline every asset so `file://` works without a server. Mermaid goes inline but collapsed. Keep the active surface to five features or fewer before the eye starts gliding.

---

## Q1. Layout and Visual Structure — What Works for Developer-Facing Feature Views

Four tools dominate the precedent: Linear, Productboard, Aha!, and Jira Advanced Roadmaps. Each solves a different slice of the problem, and the aggregate picture is clear.

**Table/list is the correct primary layout.** Across Linear, Productboard, GitHub Projects, and Jira, the dense list view is the workhorse for developer audiences [OFFICIAL]. Kanban wins when the question is "what's moving through stages"; tables win when the question is "which features have gaps?" The features artifact is a coverage-analysis question, not a flow question, so the table pattern is correct.

**The status badge is the loudest signal.** Every tool surveyed places a colored badge or dot immediately adjacent to the feature name. IBM's Carbon Design System is precise about the requirement: minimum three visual elements — geometric shape, color, and icon — to satisfy WCAG [OFFICIAL]. Red = error, orange = serious warning, yellow = warning, green = success, grey = not started. Never repeat the same shape in different colors within one experience.

**Story coverage is a differentiator.** No surveyed tool shows "stories needed to complete this feature" as an inline column. Linear surfaces project counts per initiative but not issue counts per project [OFFICIAL]. Aha! shows progress as a percent bar at feature level [OFFICIAL]. Jira shows a tri-color proportional bar but no fraction label, and Atlassian Community threads show strong unmet demand for an inline fraction [PRAC]. Rendering `N/M stories complete` as a visible column is a genuine gap this artifact can fill.

**Feature type belongs in group headers, not columns.** Productboard and Aha! both support grouping by categorical fields [OFFICIAL]. For a schema with three types (flow / connection / quality), grouping by type reduces repetition, creates visual rhythm, and allows per-group status summaries ("flow: 3 of 8 working"). Per-row type icons multiply visual noise.

**Progressive disclosure for acceptance conditions.** Every surveyed tool puts verbose detail behind a click. HTML `<details>`/`<summary>` is the native analogue — zero JavaScript, full-fidelity browser behavior, and works under `file://`.

---

## Q2. Useful vs. Overwhelming — Lessons From Teams That Built and Abandoned Planning Views

The through-line across practitioner accounts is uniform: teams over-build, then strip down. The surviving views answer *"what should we do next?"* — not *"what is happening?"*

**Dashboard blindness is empirically common.** A 2026 cloud engineering case study found 28 of 47 dashboards (60%) had zero views in 90 days; 11 more were opened exactly once by their creator [PRAC]. Only 19 survived. Deleting the dead dashboards reduced mean time to diagnosis by 35% inside a quarter. "Every unused dashboard is a tax on response time."

**Three failure modes cause abandonment.** Practitioners converge on three causes [PRAC]:

1. *Equal visual weight across all metrics* — forces viewers to interpret everything, which produces disengagement.
2. *Metric substitution (Goodhart's Law)* — teams optimize the displayed number instead of the underlying system. Velocity and RICE scores are the common offenders.
3. *Decay without ownership* — stale status displayed as current is worse than no status. Teams learn to distrust stale boards, then stop looking at them.

**Percentage complete is a signal that looks rigorous but misleads.** Basecamp's Ryan Singer documented why the hill chart replaced it: as teams discover work during implementation, task counts grow, so "a raw percentage count would show progress going backward" [OFFICIAL]. The hill chart instead asks one decision-relevant question: is this feature still in the figuring-out phase, or is it in execution?

**The working ceiling is 3–6 active signals.** Above this, viewers experience decision fatigue [PRAC]. The same ceiling applies per-row: too many columns produces priority blindness.

**Motion beats snapshot.** The hill chart's second-order view — comparing sequential snapshots — reveals which scopes are advancing and which are stuck without anyone explicitly reporting blockage [OFFICIAL]. A non-moving dot is the signal. A static artifact with no temporal signal loses this dimension entirely; the mitigation is a prominent "generated at" timestamp plus clear state transitions in the status vocabulary (working / partial / not-working / not-started already encodes "partial" as a mid-motion state).

**Friction of update determines adoption.** Intercom actively fought tool sprawl ("When managing a product includes all of Google Docs, Trello, Github, Basecamp, Asana, Slack, Dropbox, and Confluence, then something is very wrong") [PRAC]. The features artifact has a structural advantage here: `features.json` is the source of truth, and the HTML is regenerated. Update friction collapses to the cost of editing JSON.

**What to leave out, based on practitioner consensus:**

- Velocity / story points — invites gaming [PRAC]
- RICE or other precision-pretending priority scores — "a scale of 10 is so hard to use. What is the actual difference between 6, 7, 8?" [PRAC]
- Date commitments — damages credibility when they slip [PRAC]
- Raw percentage complete — shown to mislead [OFFICIAL]
- Burndown, cumulative flow — require interpretation to extract meaning [PRAC]

---

## Q3. Generated-From-Code, Rendered-As-Rich-Visual — Patterns That Work

Two reference implementations matter: Istanbul (JS coverage) and pytest-html (Python test results). Allure is a cautionary tale.

**Istanbul / nyc** proves the JSON-to-HTML pattern is mature [OFFICIAL]. The generator consumes `coverage.json` (a flat map of per-file data), merges via `createCoverageMap()`, prepares context via `createContext()`, then walks the map to emit `index.html` plus per-file pages. CSS and JS are inlined or written as siblings; the report is self-contained for offline browsing. Status color thresholds (green ≥80%, yellow ≥50%, red <50%) translate directly to the four-state feature schema.

**pytest-html** is the exact model to copy [PRAC]. It collects test outcomes during the run, then at session end renders a **single self-contained `.html` file** — CSS inlined, JS inlined, no sibling files. The template is Jinja2. The `.html` can be emailed, committed, or opened from any path. This is what `cmux browser open file:///path/artifact.html` needs.

**Allure is what not to do.** It generates a directory with `index.html` plus bundled assets and requires a local web server because ES module imports hit CORS under `file://`. Multi-file output breaks the browser-pane use case.

**Mermaid.js works under `file://` if loaded via ESM CDN.** Import `mermaid@11/dist/mermaid.esm.min.mjs` from jsdelivr, call `mermaid.initialize({ startOnLoad: true })`, and embed diagram text inside `<pre class="mermaid">` [OFFICIAL]. Jinja generates the diagram string at render time; Mermaid renders it client-side on load. No backend required.

**CSS data attributes beat class soup for status-driven styling.** `<div class="card" data-status="{{ feature.status }}">` with CSS selectors like `.card[data-status="partial"]` keeps the template clean and the styling co-located [PRAC]. This approach is Jinja-friendly and readable.

---

## Design Recommendations

This is the operational payoff. Each decision below is concrete and implementable.

### 1. Layout Structure — Sections, Order, HTML Elements

The artifact is a single HTML page with this vertical order:

1. **Header band** — title ("Feature Status — <project>"), `generated_at` timestamp (prominent, timezone-explicit), sprint name if relevant. `<header>` element.
2. **At-a-glance summary strip** — four chips: total features, % working, count with gaps, count not-started. `<section class="summary">`. This is the executive answer to "where do we stand?"
3. **Feature dependency diagram** — a collapsed `<details>` block containing a Mermaid flowchart. Closed by default; the table is the primary view, the diagram is drill-down.
4. **Feature table, grouped by type** — the main surface. One `<section>` per type (flow, connection, quality) with a group header row showing type name, feature count, and a mini "X of Y working" summary. `<table>` inside each section.
5. **Footer** — source path (`features.json`), schema version, "regenerate" command hint.

The table shell is a standard `<table class="features">` with a sticky `<thead>`. Each feature row is a `<tr>`; the expanded detail is a second `<tr>` containing one `<td colspan="5">` that holds a `<details>` element. No JavaScript required for expand/collapse.

### 2. Which Signals Go Prominent vs. Behind Expand/Collapse

**Prominent (always visible in the row):**

- Status badge (colored pill: green / amber / red / grey)
- Feature name (bold)
- Short description — truncated with CSS `text-overflow: ellipsis`, full text on hover via `title` attribute
- Story coverage — dual representation: fraction `N/M` as text and a mini proportional bar (tri-color: done / in-progress / not-started) beneath the number
- Gap indicator — a small `GAP` badge when `status != working` AND `len(stories) < 2`, or when `status == not-working`. This is the action signal.

**Behind `<details>` expand:**

- Full acceptance condition text
- Full story list with per-story status and story ID
- Per-story file-path hints or link references, if schema carries them
- Any dependency / blocker notes
- Raw JSON payload for debugging (inside a nested `<details>`, further demoted)

**Behind the separate top-level diagram `<details>`:**

- Mermaid dependency flowchart

The structure matches Linear's "executive sees portfolio, developer sees assigned items" steel-thread principle: the row is the executive view, the expand is the developer view.

### 3. Representing Story Importance Alongside Status

The features schema does not currently encode story-level priority, so the visible signal derives from structure and status. Two concrete patterns:

- **Story ordering within the expand** — render stories in the order they appear in `features.json` and treat that as authored priority. Do not sort alphabetically; preserve authorial intent.
- **Gap computation** — a feature with few stories and a non-working status is higher-signal than one with many stories in mixed state. The `GAP` badge surfaces this without adding a priority field to the schema. Formula: `status in {partial, not-working} AND stories_done / stories_total < 0.5`, OR `status == not-started AND stories_total == 0`.

Resist adding a `priority` column. Practitioner research is unambiguous: precision-pretending priority scores invite gaming and create false confidence [PRAC]. The coverage fraction combined with status already encodes "what needs attention" more honestly.

If importance must be expressed later, add a single-bit `critical: true` flag on stories and render a small icon (`!`) next to the story title within the expand — never in the row-level view.

### 4. What to Leave Out Entirely

Based on practitioner evidence:

- **Velocity / story points / sprint burndown** — invites gaming; out of scope for a coverage artifact [PRAC]
- **RICE, ICE, or any weighted priority score** — false precision [PRAC]
- **Date commitments or Gantt-style timelines** — damages credibility on slip [PRAC]
- **Raw percent-complete as a primary number** — misleads when scope is discovered [OFFICIAL]
- **Multiple filter tabs or view toggles** — single well-designed view beats a multi-view interface with no server state
- **Owner / avatar column** — irrelevant for a solo-dev practice; only reintroduce if the tool expands to teams
- **Tag / label columns** — adds width pressure with low decision value at this scale
- **Cumulative flow diagrams, velocity charts** — require interpretation, don't drive action [PRAC]
- **Live sync status, "last updated N minutes ago"** — the `generated_at` timestamp in the header is sufficient

The test is Ayush Jha's: can a viewer identify the single most important action to take? If a signal doesn't contribute to that, it's overhead [PRAC].

### 5. Mermaid.js Diagram Type and Purpose

Use **`flowchart TD`** (top-down) for the dependency diagram, rendered inside the top-level collapsed `<details>` block. Justification:

- Dagre (default layout) handles moderate complexity well; switch to `elk` layout for graphs with >15 nodes [OFFICIAL]
- Supports 30 shape types — use rounded boxes for features, plain rectangles for stories
- `classDef` enables status coloring inside the diagram definition itself: `classDef working fill:#22c55e,stroke:#15803d; class F1 working`
- Edge labels can mark dependency type: `F1 -->|blocks| F2`

Do not use mindmap, kanban, or block diagram variants as the primary. Mindmap loses directionality; kanban duplicates the table; block loses edge semantics.

A second, smaller Mermaid diagram can optionally appear inside each feature's row expand to show that feature's local dependency subgraph. This is optional — only include it when the feature has more than three stories or crosses more than one other feature.

Generate the Mermaid text in Python before rendering so Jinja's responsibility is just string substitution into `<pre class="mermaid">{{ diagram }}</pre>`.

### 6. CSS / HTML Pattern — Borrow From Istanbul and pytest-html

The pattern is:

- **All CSS in a single `<style>` block in `<head>`.** No sibling stylesheets. This guarantees `file://` works.
- **Mermaid via ESM CDN only.** No other external assets. No web fonts (use the system font stack).
- **Data-attribute driven status styling,** not class modifiers.

Minimal CSS skeleton:

```css
:root {
  --bg: #fff; --fg: #111827; --muted: #6b7280;
  --border: #e5e7eb; --row-hover: #f9fafb;
  --status-working: #22c55e;
  --status-partial: #f59e0b;
  --status-not-working: #ef4444;
  --status-not-started: #6b7280;
}
@media (prefers-color-scheme: dark) {
  :root { --bg: #0b0f14; --fg: #e5e7eb; --border: #1f2937; --row-hover: #111827; }
}
body { font: 14px/1.5 -apple-system, system-ui, sans-serif; color: var(--fg); background: var(--bg); margin: 0; }
.features { width: 100%; border-collapse: collapse; }
.features thead { position: sticky; top: 0; background: var(--bg); }
.features th, .features td { padding: .5rem .75rem; text-align: left; border-bottom: 1px solid var(--border); }
.features tr:hover { background: var(--row-hover); }
.badge { display: inline-flex; align-items: center; gap: .25em; padding: .15em .55em; border-radius: 9999px; font-size: .72rem; font-weight: 600; text-transform: uppercase; }
.badge[data-status="working"]     { background: color-mix(in srgb, var(--status-working) 18%, transparent); color: var(--status-working); }
.badge[data-status="partial"]     { background: color-mix(in srgb, var(--status-partial) 18%, transparent); color: var(--status-partial); }
.badge[data-status="not-working"] { background: color-mix(in srgb, var(--status-not-working) 18%, transparent); color: var(--status-not-working); }
.badge[data-status="not-started"] { background: color-mix(in srgb, var(--status-not-started) 20%, transparent); color: var(--status-not-started); }
.coverage-bar { display: inline-block; width: 80px; height: 6px; border-radius: 3px; background: var(--border); overflow: hidden; vertical-align: middle; }
.coverage-bar > span { display: block; height: 100%; background: var(--status-working); }
.gap { margin-left: .5em; font-size: .7rem; font-weight: 700; color: var(--status-not-working); border: 1px solid currentColor; padding: 0 .4em; border-radius: 3px; }
details > summary { cursor: pointer; color: var(--muted); font-size: .85rem; }
```

Carbon's three-element rule is satisfied by pairing the badge color with an icon character inside the span (e.g. `OK` / `~` / `X` / `-` or unicode symbols) and the pill shape.

### 7. Jinja2 Templating Approach

Follow pytest-html's single-file generator pattern. The generator is one Python file; the template is a Python string constant using Jinja2's `BaseLoader`. No sibling `.j2` files.

```python
from jinja2 import Environment, BaseLoader
from pathlib import Path
from datetime import datetime, timezone
import json

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Feature Status — {{ project }}</title>
<style>{{ css }}</style>
</head>
<body>
<header>
  <h1>Feature Status — {{ project }}</h1>
  <p class="meta">Generated {{ generated_at }}</p>
</header>

<section class="summary">
  <span class="chip">{{ totals.total }} features</span>
  <span class="chip">{{ totals.working }} working</span>
  <span class="chip">{{ totals.gaps }} with gaps</span>
  <span class="chip">{{ totals.not_started }} not started</span>
</section>

<details>
  <summary>Dependency diagram</summary>
  <pre class="mermaid">{{ mermaid_diagram }}</pre>
</details>

{% for group in groups %}
<section class="group">
  <h2>{{ group.type | capitalize }} <small>({{ group.working }}/{{ group.total }} working)</small></h2>
  <table class="features">
    <thead><tr>
      <th>Feature</th><th>Status</th><th>Stories</th><th>Signal</th><th></th>
    </tr></thead>
    <tbody>
    {% for f in group.features %}
      <tr>
        <td><strong>{{ f.name }}</strong><div class="desc">{{ f.description | default("") }}</div></td>
        <td><span class="badge" data-status="{{ f.status }}">{{ f.status }}</span></td>
        <td>
          {{ f.stories_done }}/{{ f.stories_total }}
          <span class="coverage-bar"><span style="width: {{ f.coverage_pct }}%"></span></span>
        </td>
        <td>{% if f.gap %}<span class="gap">GAP</span>{% endif %}</td>
        <td><details><summary>detail</summary>
          <p><strong>Acceptance:</strong> {{ f.acceptance_condition }}</p>
          <ul>
          {% for s in f.stories %}
            <li><span class="badge" data-status="{{ s.status }}">{{ s.status }}</span> <code>{{ s.id }}</code> {{ s.title }}</li>
          {% endfor %}
          </ul>
        </details></td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</section>
{% endfor %}

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'neutral' });
</script>
</body>
</html>"""

def render(features_path: Path, out_path: Path) -> None:
    data = json.loads(features_path.read_text())
    context = build_context(data)  # compute groups, totals, gap flags, mermaid string
    env = Environment(loader=BaseLoader(), autoescape=True)
    html = env.from_string(TEMPLATE).render(**context)
    out_path.write_text(html)
```

Useful Jinja filters to lean on:

- `selectattr("status", "eq", "working") | list | length` — inline aggregation for per-group counts
- `default("")` — guard against missing schema fields
- `round(1)` — percentages without spurious precision
- `autoescape=True` on the Environment — acceptance condition text is user content and must not inject HTML

Compute gap flags, coverage percentages, and the Mermaid diagram string in Python before render. Templates should be presentation-only — keep logic out of Jinja.

---

## Putting It All Together — The Adoption Test

The artifact will be used if, within three seconds of opening it, the reader can answer: *"Which feature needs my attention next?"* This is the Basecamp / Ayush Jha test for dashboard survival [OFFICIAL][PRAC].

The design above answers that because: the colored status badges draw the eye, the `GAP` indicator filters the row-level view to the action candidates, and the coverage fraction makes "how far off are we?" obvious without opening anything. Everything else is drill-down, earned by a deliberate click.

The artifact will be abandoned if: the reader has to scan more than five features to find the next action (add an "attention" section at the top if the project scales past that), the data goes stale without visible indication (keep `generated_at` prominent and regenerate on every `features.json` edit), or the layout adds columns for signals the reader never consults (resist scope creep; every new column has to earn its place by answering a recurring question).

---

## Sources

**Primary tool documentation [OFFICIAL]:**
- Linear — Initiatives, Project Status
- Productboard — Feature Boards, Status Values, Roadmap Card Attributes
- Aha! — Features Roadmap, Hierarchy Report
- Atlassian / Jira — Epic progress on the timeline, Advanced Roadmaps tracking
- IBM Carbon Design System — Status Indicator Pattern
- GitHub Projects — View layouts
- Basecamp / Ryan Singer — Hill Chart, Shape Up Chapter 13
- Istanbul.js — Coverage object report format
- Mermaid.js — Flowchart syntax, intro
- Atlassian Developer Experience Report 2024

**Practitioner sources [PRAC]:**
- The Cloud Playbook — "We Deleted 60% of Our Dashboards" (2026)
- Ayush Jha — "Why Most Dashboards Fail" (Medium, 2026)
- Abdul Osman — "The Metrics Mirage" (DEV Community)
- Sigma Computing — "Drowning in Dashboards"
- Intercom — "What we learned from scaling a product team"
- Markus Müller — "The Playbook to fix your Product Roadmap"
- Evil Martians — "5 Essential Design Patterns for Dev Tool UIs"
- Pencil & Paper — "UX Pattern Analysis: Data Dashboards"
- Tempo — "Why Your Teams Aren't Using Your Roadmap"
- Lenny Rachitsky — "How Linear builds product"
- pytest-html — repository and template patterns
- Real Python — Jinja2 primer
- Smashing Magazine — Modern CSS Layouts No Framework (2024)
