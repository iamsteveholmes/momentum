# Eval: Product vs. Practice Rendering Paths

## Scenario

The skill must detect project type and render the correct HTML layout:
- **Product project:** flow/connection/quality grouped tables with per-group gap summaries
- **Practice project:** skill topology Mermaid diagram + SDLC phase coverage table

Both paths must produce valid, self-contained HTML.

---

## Input A: Product Project

### features.json
```json
{
  "project_type": "product",
  "features": [
    {
      "id": "feat-search",
      "name": "Content Search",
      "type": "flow",
      "status": "not-started",
      "acceptance_condition": "A user can search content by keyword with results ranked by relevance.",
      "stories": []
    },
    {
      "id": "feat-api-connect",
      "name": "External API Integration",
      "type": "connection",
      "status": "working",
      "acceptance_condition": "The app connects to the external API and surfaces live data.",
      "stories": ["api-client", "api-error-handling"]
    },
    {
      "id": "feat-perf",
      "name": "Sub-2s Page Load",
      "type": "quality",
      "status": "partial",
      "acceptance_condition": "All key pages load in under 2 seconds on a standard 4G connection.",
      "stories": ["lazy-load-images"]
    }
  ]
}
```

### Expected Behavior (Product)

1. HTML contains three `<section class="feature-group">` elements: `data-type="flow"`,
   `data-type="connection"`, `data-type="quality"`
2. Each group has a header and per-group gap summary ("N features, M with gaps")
3. Status badges: green (working), amber (partial), grey (not-started), red (not-working)
4. Mermaid diagram shows feature-to-story relationships (not skill topology)

### Pass Criteria (Product)
- [ ] Three type groups rendered: flow, connection, quality
- [ ] Per-group gap summary present ("N features, M with gaps")
- [ ] Status badge colors follow convention (green/amber/grey/red)
- [ ] Mermaid `flowchart TD` shows features linked to stories

---

## Input B: Practice Project

### features.json
```json
{
  "project_type": "practice",
  "features": [
    {
      "id": "feat-sprint-planning",
      "name": "Sprint Planning",
      "sdlc_phase": "planning",
      "covering_skills": ["sprint-planning"],
      "status": "working",
      "acceptance_condition": "Developer can run momentum:sprint-planning and get a prioritized sprint.",
      "stories": []
    },
    {
      "id": "feat-dev-execution",
      "name": "Story Dev Execution",
      "sdlc_phase": "development",
      "covering_skills": ["dev", "quick-fix"],
      "status": "partial",
      "acceptance_condition": "Developer can execute any story via momentum:dev or momentum:quick-fix.",
      "stories": []
    },
    {
      "id": "feat-retro",
      "name": "Sprint Retrospective",
      "sdlc_phase": "retrospective",
      "covering_skills": [],
      "status": "not-started",
      "acceptance_condition": "Developer can run momentum:retro to get actionable sprint insights.",
      "stories": ["retro-skill"]
    }
  ]
}
```

### Expected Behavior (Practice)

1. HTML Mermaid diagram shows **skill hand-off topology** (skills as nodes, hand-off
   edges between them) rather than feature-to-story relationships
2. Feature table shows **SDLC phase coverage**: rows are SDLC phases, columns show
   which skills cover each phase
3. SDLC phases with no covering skill are flagged as gaps in the table
4. `feat-retro` (covering_skills: []) generates a gap flag with description

### Pass Criteria (Practice)
- [ ] Mermaid diagram shows skill nodes and hand-off edges (not feature→story)
- [ ] SDLC coverage table rendered (not flow/connection/quality groups)
- [ ] Phases with no covering skill flagged as GAP
- [ ] `feat-retro` has GAP flag (no covering skills)

---

## Shared Pass Criteria (Both Paths)

- [ ] Both produce valid HTML5 with `<!DOCTYPE html>`
- [ ] Both are self-contained (no external CSS; Mermaid via CDN ESM only)
- [ ] Both work via `file://` protocol
- [ ] Both include summary stats bar
- [ ] Both include a collapsed dependency/topology graph in `<details>`
- [ ] Both write `.claude/momentum/feature-status.md` cache file

## Failure Criteria

- Product path renders SDLC table instead of flow/connection/quality groups
- Practice path renders feature-type groups instead of skill topology + SDLC table
- Either path has broken HTML or missing required sections
- Project type inference fails silently (should ask developer if ambiguous)
