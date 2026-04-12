---
content_origin: claude-code-subagent
date: 2026-04-11
sub_question: "CLI-generated rich visual artifacts — rendering patterns"
topic: "Feature planning artifact visualization"
---

# CLI-Generated Rich Visual Artifacts — Rendering Patterns

Research for: Python script generating a feature planning artifact as a static HTML file opened via `cmux browser open file:///path`. Stack: Jinja2, Mermaid.js (CDN), plain HTML/CSS, no server.

---

## 1. Istanbul/nyc HTML Coverage Reports — How They Work

Istanbul (and its CLI wrapper nyc) is the canonical example of "JSON data → rich visual HTML" in the JS toolchain. The pattern is instructive.

### Data Flow

1. Test runner instruments code and produces a `coverage.json` (or `.nyc_output/out.json`) — a flat map of `{ filePath: CoverageData }` objects.
2. The `CoverageData` per file contains: `s` (statement counts), `b` (branch counts), `f` (function counts), each keyed by numeric ID.
3. Report generation is invoked separately: `npx nyc report --reporter=html`. Istanbul's report subsystem calls `createCoverageMap()` to merge raw data, then `createContext({ dir, coverageMap })` to prepare rendering, then the HTML reporter walks the map and emits files.

### HTML Report Structure

- `coverage/index.html` — directory-level summary table (file rows with % bars, color-coded green/yellow/red by threshold)
- `coverage/<file>.html` — per-file line-annotated source with inline hit counts
- All CSS/JS is either inlined or written as sibling files in `coverage/`; the report is self-contained for offline browsing

### Key Takeaway for Our Context

Istanbul proves the pattern is mature: **emit JSON from your generator, pass it into a Jinja/template context, render HTML once.** No server needed. The color-coded threshold approach (green ≥ 80%, yellow ≥ 50%, red < 50%) directly translates to story-completion status badges.

Source: [Istanbul coverage object report docs](https://istanbul.js.org/docs/advanced/coverage-object-report/), [coverage.json format](https://github.com/gotwarlost/istanbul/blob/master/coverage.json.md)

---

## 2. Mermaid.js Diagram Types for Feature-to-Story Dependency/Coverage

Mermaid.js renders text-defined diagrams via CDN JS — no build step. For feature planning artifacts, two diagram types are most relevant:

### Flowchart (Recommended)

```
flowchart TD
    F1[Feature: Auth] --> S1[Story: Login]
    F1 --> S2[Story: Register]
    S1 --> S3[Story: 2FA]
```

- Default layout engine: **Dagre** (good for moderate complexity)
- Alternative: `elk` layout (v9.4+), better for larger dependency graphs
- Supports **30 shape types** — use rounded boxes for features, rectangles for stories, diamonds for milestones
- Edge IDs can be assigned for styling: `F1 -->|blocks| S3`
- Node class styling: `classDef done fill:#22c55e; class S1 done` — enables status coloring directly in the diagram definition

### Other Useful Types

- **Mindmap** — feature tree with no explicit directionality, better for "what exists" orientation
- **Kanban** — built-in lane support for "Not Started / In Progress / Done" story status
- **Block diagram** — rectangular composition for epic → feature → story hierarchy without arrow clutter

### CDN Usage Pattern

```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'neutral' });
</script>

<pre class="mermaid">
flowchart TD
  ...
</pre>
```

Jinja generates the diagram definition text inline; Mermaid renders it client-side on load. The `file://` protocol works — Mermaid only needs the CDN JS, no backend.

Source: [Mermaid flowchart syntax](https://mermaid.js.org/syntax/flowchart.html), [Mermaid intro](https://mermaid.js.org/intro/)

---

## 3. CSS Patterns for Status Cards/Tables — Single-File, No Framework

Modern CSS (2023+) makes zero-dependency single-file HTML viable for artifact UIs.

### Grid-Based Status Card Layout

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  background: #fff;
}

.card[data-status="done"]    { border-left: 4px solid #22c55e; }
.card[data-status="in-progress"] { border-left: 4px solid #f59e0b; }
.card[data-status="not-started"] { border-left: 4px solid #6b7280; }
.card[data-status="blocked"] { border-left: 4px solid #ef4444; }
```

The `data-status` attribute approach keeps status styling out of class soup and is Jinja-friendly: `<div class="card" data-status="{{ story.status }}">`.

### Status Badge Pattern

```css
.badge {
  display: inline-block;
  padding: .2em .6em;
  border-radius: 9999px;
  font-size: .75rem;
  font-weight: 600;
  text-transform: uppercase;
}
.badge-done     { background: #dcfce7; color: #15803d; }
.badge-blocked  { background: #fee2e2; color: #b91c1c; }
.badge-pending  { background: #f3f4f6; color: #374151; }
```

### Summary Table

Standard `<table>` with sticky header (no JS required):

```css
.summary-table { width: 100%; border-collapse: collapse; }
.summary-table thead { position: sticky; top: 0; background: #f9fafb; }
.summary-table th, .summary-table td {
  padding: .5rem .75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}
.summary-table tr:hover { background: #f9fafb; }
```

### Key Principle

Use `@media print` and `@media (prefers-color-scheme: dark)` blocks even for browser-only artifacts — they cost nothing and make the output robust. Inline all CSS in a `<style>` block in `<head>` so the file is fully self-contained (no sibling `.css` files needed for `file://` access).

Source: [Smashing Magazine — Modern CSS Layouts No Framework](https://www.smashingmagazine.com/2024/05/modern-css-layouts-no-framework-needed/), [W3Schools CSS Cards](https://www.w3schools.com/howto/howto_css_cards.asp)

---

## 4. Python Jinja2 → HTML from JSON — Standard Patterns

Jinja2 is the established choice for this workflow. The canonical pattern:

```python
from jinja2 import Environment, FileSystemLoader
import json

data = json.loads(Path("features.json").read_text())

env = Environment(loader=FileSystemLoader("templates/"))
template = env.get_template("report.html.j2")

html = template.render(
    features=data["features"],
    sprint=data["sprint"],
    generated_at=datetime.utcnow().isoformat(),
)

Path("output/feature-status.html").write_text(html)
```

### For Single-File Generation (Our Case)

Use `Environment(loader=BaseLoader())` with an inline template string, or embed the template as a Python string constant — keeps the generator as a single `.py` file with no sibling template files:

```python
from jinja2 import Environment, BaseLoader

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <style>{{ css }}</style>
</head>
<body>
  {% for feature in features %}
    <div class="card" data-status="{{ feature.status }}">
      <h2>{{ feature.name }}</h2>
      {% for story in feature.stories %}
        <span class="badge badge-{{ story.status }}">{{ story.title }}</span>
      {% endfor %}
    </div>
  {% endfor %}
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
  </script>
  <pre class="mermaid">{{ mermaid_diagram }}</pre>
</body>
</html>"""

env = Environment(loader=BaseLoader())
template = env.from_string(TEMPLATE)
html = template.render(features=..., css=CSS_BLOCK, mermaid_diagram=diagram_text)
```

### Jinja2 Filters Useful for Reports

- `{{ value | default("N/A") }}` — safe missing data
- `{{ stories | selectattr("status", "eq", "done") | list | length }}` — inline aggregation
- `{{ pct | round(1) }}%` — computed completion percentage
- `{% set done = stories | selectattr("status","eq","done") | list %}` — assign computed lists

Source: [Real Python Jinja2 Primer](https://realpython.com/primer-on-jinja-templating/), [python-json-via-jinja2-render (GitHub)](https://github.com/nvtkaszpir/python-json-via-jinja2-render), [Practical Business Python — PDF Reports](https://pbpython.com/pdf-reports.html)

---

## 5. Open-Source "JSON Data → HTML Report" Reference Implementations

### pytest-html

- **Repo**: https://github.com/pytest-dev/pytest-html
- **Pattern**: Plugin collects test outcomes into an in-memory list during test run. At session end, renders a **single self-contained `.html` file** — CSS inlined, JS inlined, all assets base64 or embedded. No sibling files.
- **Template approach**: Jinja2 templates (`.j2` files in the package). The render call passes the collected result list as template context.
- **Key design choice**: Everything inlined so the `.html` can be emailed, committed, or opened from any path. This is the exact model we want.

### Allure Report

- **Pattern**: Two-phase. Phase 1 (adapter): test runner writes structured JSON per test to a results dir. Phase 2 (CLI tool, Java): `allure generate` reads all JSON files, renders a full multi-page app with bundled JS/CSS.
- **Single-file**: No — Allure generates a directory with index.html + assets. Requires a web server or `allure open` to serve it (breaks `file://` due to CORS on ES module imports).
- **Lesson for our context**: Allure's two-phase split is overkill and its multi-file output breaks `file://`. **Avoid this pattern.** pytest-html's single-file approach is the right model.

### coverage.py HTML Reporter (Python)

- **Pattern**: Python's own coverage tool (not Istanbul) follows the same architecture: `coverage run` produces `.coverage` sqlite, `coverage html` renders to `htmlcov/` directory.
- The directory approach requires all files to be co-located, but `htmlcov/index.html` works on `file://` because assets are sibling files, not CDN.
- **Takeaway**: CDN-loaded assets (Mermaid, no local font files) + fully inlined CSS eliminates the sibling-file problem for `file://`.

---

## Synthesis — Recommended Architecture for Our Python Generator

```
generator.py
  └── reads: features.json (or constructs data dict in-memory)
  └── builds: mermaid_diagram string (flowchart TD syntax)
  └── renders: Jinja2 template string → single HTML file
      ├── <style> block — all CSS inlined (cards, badges, table, layout)
      ├── <script type="module"> — Mermaid CDN import
      ├── <pre class="mermaid"> — diagram definition (Jinja-generated)
      └── card/table HTML — Jinja for-loops over features/stories
```

**Status color scheme** (Istanbul-proven): green (#22c55e) = done, amber (#f59e0b) = in-progress, gray (#6b7280) = not-started, red (#ef4444) = blocked.

**Mermaid diagram type**: `flowchart TD` with `classDef` for status coloring — most expressive for feature→story dependency trees. Use `elk` layout directive for graphs with >15 nodes.

**Single-file guarantee**: All CSS inline in `<style>`, Mermaid via ESM CDN import (works on `file://`), no local asset references.
