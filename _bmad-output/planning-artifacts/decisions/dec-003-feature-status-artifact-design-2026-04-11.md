---
id: DEC-003
title: Feature Status Artifact Design — HTML Report, Layout, Signals, and Rendering
date: '2026-04-11'
status: decided
source_research:
  - path: _bmad-output/research/feature-status-visualization-2026-04-11/final/feature-status-visualization-final-2026-04-11.md
    type: prior-research
    date: '2026-04-11'
prior_decisions_reviewed:
  - DEC-002 D2 — feature-status-skill output format left undefined; this decision resolves it
  - DEC-002 D3 — impetus-feature-status-cache summary line format; this decision specifies it
stories_affected:
  - feature-status-skill
---

# DEC-003: Feature Status Artifact Design — HTML Report, Layout, Signals, and Rendering

## Summary

DEC-002 D2 adopted `momentum:feature-status` as a standalone skill but left the output format undefined — it said "compact terminal output" without specifying layout, signals, or rendering. Research spike `feature-status-visualization-2026-04-11` (light profile, 3 agents) answered the open questions. The central finding: compact text output is the wrong format for a planning artifact. Teams over-build dashboards and abandon them when updates are manual and the artifact shows too much at once. The solution: a generated-from-schema static HTML file opened in a cmux browser pane, with a deliberate signal hierarchy (status badge + story fraction + GAP flag always visible; full detail behind expand). All 7 design decisions adopted.

---

## Decisions

### D1: Output Format — Static HTML File Opened in cmux Browser — ADOPT

**Research recommended:** A self-contained HTML file written to `.claude/momentum/feature-status.html` and opened in a cmux browser pane. No terminal text dump. Alongside it, `.claude/momentum/feature-status.md` with YAML frontmatter (`input_hash`, `summary`, `generated_at`) serves as the Impetus cache and index.

**Decision:** Adopt. `momentum:feature-status` produces two outputs: (1) `.claude/momentum/feature-status.html` — the full planning artifact, opened in a cmux browser pane; (2) `.claude/momentum/feature-status.md` — frontmatter-only cache for Impetus staleness detection. Terminal output is a single confirmation line: `Feature status written → .claude/momentum/feature-status.html`.

**Rationale:** Terminal text can't render visual layout, color-coded badges, progress bars, or expandable detail. The developer said "a picture is worth a thousand words" — a compact text dump does not answer "what does this feature need?" A generated-from-schema HTML file requires no manual updates and stays current whenever the skill runs.

---

### D2: Layout Structure — ADOPT

**Research recommended:** Single-page HTML: page header (project name, generated date) → summary stats bar (counts by status, gap count) → Mermaid dependency graph (collapsed by default) → feature tables grouped by type (flow / connection / quality) → footer. Each table row: feature name (bold) → status badge (color-coded) → story fraction N/M with mini progress bar → GAP indicator.

**Decision:** Adopt as recommended. The table/list layout (not kanban) is the correct choice for a coverage-scanning planning artifact. Every major tool (Linear, Productboard, Aha!, Jira) uses table/list for planning-phase work where the primary question is "which features have gaps." Kanban is for flow/movement, not coverage scanning.

**Rationale:** Planning artifacts need to answer "which features have gaps" at a scan, not require reading narrative text. The table row pattern (name → status → N/M → GAP) answers that question in one visual sweep per feature.

---

### D3: Prominent vs. On-Demand Signals — ADOPT

**Research recommended:** Always visible: status badge, story fraction N/M, GAP flag. Behind `<details>` expand: full acceptance_condition text, individual story list with statuses, gap description. Never shown: velocity, RICE scores, dates, raw percentages, owner/assignment.

**Decision:** Adopt. The `<details>`/`<summary>` pattern (pytest-html model) puts the full acceptance condition, story list, and gap description one click away without cluttering the scan view. The "never shown" list is firm — practitioners consistently report that velocity, RICE, and raw percentages are noise that causes dashboard abandonment.

**Rationale:** The Q2 research finding: teams that audit their dashboards delete 60% of signals. The signals that survive are those that answer a specific recurring decision. Status + fraction + GAP answer "do I need to act on this feature?" Everything else is secondary.

---

### D4: Story Importance Representation — ADOPT

**Research recommended:** Row ordering within each type group — not a separate priority column. Features with GAP flags sort to top within each group.

**Decision:** Adopt. No explicit priority column. GAP features sort to top of each type group. Within the non-GAP rows, sort by status (not-working → partial → working).

**Rationale:** Adding a priority column requires either manual maintenance or a priority field in features.json that doesn't exist. Sorting by gap+status achieves the same planning outcome (highest-priority work surfaces first) without the maintenance cost.

---

### D5: Mermaid Diagram Type — ADOPT

**Research recommended:** `flowchart TD` with `classDef` status coloring. Shows feature-to-story dependency trees. Collapsed by default.

**Decision:** Adopt. `flowchart TD` with `classDef` blocks for status colors (green/amber/red/grey). The diagram section is collapsed by default inside a `<details>` block — summary stats are the first thing seen, not a graph. The graph is there when the developer needs to reason about dependencies.

**Rationale:** Mermaid `flowchart TD` is the right type for directed feature-to-story relationships. CDN ESM import works on `file://` with no server needed. Collapsed by default because the table view answers most planning questions; the graph is for deeper dependency reasoning.

---

### D6: CSS/HTML Implementation Pattern — ADOPT

**Research recommended:** Single self-contained file (no sibling assets). `data-status` attribute-driven CSS (Istanbul/pytest-html pattern). Full inline CSS. Jinja2 `BaseLoader` template with autoescape. CDN ESM import for Mermaid.js (works on `file://`). Dark-mode support via `color-mix`.

**Decision:** Adopt. Reference implementation: pytest-html for single-file self-contained pattern; Istanbul/nyc for `data-status` CSS color conventions (green ≥ threshold, amber partial, grey not-started, red not-working). Jinja2 `Environment(loader=BaseLoader(), autoescape=True)` for template rendering from a Python dict built from features.json + stories/index.json.

**Rationale:** The `file://` constraint (no server) requires all assets inline. pytest-html is the gold standard for this pattern — single Jinja2 template, all CSS inlined, no sibling files. The `data-status` attribute pattern lets CSS do all the color work without JavaScript, keeping the file simple and maintainable.

---

### D7: Terminal Summary Line Format (Impetus Cache) — ADOPT

**Research recommended:** One-line summary for `.claude/momentum/feature-status.md` frontmatter:
`{N} features: {working} working · {partial} partial · {not-started} not-started · {gaps} gaps`

**Decision:** Adopt. This is the `summary` field written to `.claude/momentum/feature-status.md` frontmatter after each skill run. Impetus renders it verbatim in the greeting line.

**Rationale:** The summary must fit in one greeting line without wrapping at 80 chars. Counts + gap flag is the minimum information that lets a developer decide whether to open the full HTML artifact.

---

## Implementation Notes

The `feature-status-skill` story (DEC-002 D2) must be rewritten against these decisions. Key changes:
- Output is HTML + .md (not terminal text)
- Workflow adds: Step 7 (write feature-status.md frontmatter), Step 8 (write feature-status.html via Jinja2), Step 9 (open in cmux browser)
- The `touches` list expands to include `.claude/momentum/feature-status.html` and momentum-tools.py (for the Jinja2 HTML generation command)
- The "compact output" AC (AC7) is replaced with the HTML artifact ACs

The `impetus-feature-status-cache` story is unaffected — it reads `.claude/momentum/feature-status.md` frontmatter, which this decision confirms as the cache mechanism.
