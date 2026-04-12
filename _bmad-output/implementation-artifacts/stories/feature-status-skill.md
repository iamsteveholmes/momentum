---
title: Feature Status Skill — HTML Planning Artifact with Coverage Gap Analysis
story_key: feature-status-skill
status: ready-for-dev
epic_slug: feature-orientation
depends_on:
  - feature-artifact-schema
touches:
  - skills/momentum/skills/feature-status/SKILL.md
  - skills/momentum/skills/feature-status/workflow.md
  - .claude/momentum/feature-status.html
  - .claude/momentum/feature-status.md
change_type: skill-instruction
derives_from:
  - path: _bmad-output/planning-artifacts/decisions/dec-002-feature-visualization-and-orientation-2026-04-11.md
    relationship: derives_from
    section: "D2: Build momentum:feature-status Skill — ADAPT"
  - path: _bmad-output/planning-artifacts/decisions/dec-003-feature-status-artifact-design-2026-04-11.md
    relationship: derives_from
    section: "D1–D7: HTML artifact design, layout, signals, rendering"
---

# Feature Status Skill — HTML Planning Artifact with Coverage Gap Analysis

## Story

As a developer using Momentum,
I want to run `momentum:feature-status` and see a rich HTML planning artifact
in a browser pane showing which features are working, which have gaps, and
exactly what each feature needs to reach working state,
so I can make informed sprint planning decisions about where to focus work.

## Description

Stories and epics complete while no user-facing capabilities complete. The
feature artifact (`features.json`) introduced in `feature-artifact-schema` tracks
user-observable capabilities as persistent units with acceptance conditions,
status, and story links. But a status dump is not enough — the developer needs to
see at a glance which features have coverage gaps, what stories are assigned, and
whether the assigned story set is actually sufficient.

`momentum:feature-status` is a standalone skill (superseding DRIFT-006) that
performs this evaluation on demand. It reads `features.json`, cross-references
`stories/index.json`, runs coverage gap analysis, and writes a self-contained
HTML planning artifact opened in a cmux browser pane.

The output is a rich, visual, generated-from-schema HTML file. No terminal text
dump. No manual updates required — the file is always current when the skill runs.

Two rendering paths exist: product projects (Nornspun: flow/connection/quality
tables with gap analysis) and practice projects (Momentum: skill topology diagram
+ SDLC coverage table). Both produce the same HTML structure, adapted to project type.

The skill also writes `.claude/momentum/feature-status.md` with YAML frontmatter
(`input_hash`, `summary`, `generated_at`) for the Impetus cache (DEC-002 D3).

## Acceptance Criteria (Plain English)

### AC1: Skill Is Independently Invocable

- A skill exists at `skills/momentum/skills/feature-status/SKILL.md` with valid
  frontmatter: `name: feature-status`, `description`, `model`, `effort`
- `momentum:feature-status` is invocable without Impetus running
- SKILL.md body delegates to `./workflow.md`
- SKILL.md description is ≤150 characters

### AC2: Reads features.json and stories/index.json

- The skill reads `_bmad-output/planning-artifacts/features.json`
- The skill cross-references `_bmad-output/implementation-artifacts/stories/index.json`
  to get current story statuses (done, in-progress, backlog, etc.)
- If `features.json` does not exist, the skill surfaces a clear error:
  "features.json not found — run feature-artifact-schema story first"

### AC3: Coverage Gap Analysis Is First-Class

For each feature in `features.json`, the skill evaluates:
- Which stories are assigned (from the feature's `stories` list)
- What those stories actually deliver (from their titles and summaries)
- Whether the assigned story set is sufficient to deliver the feature's
  `acceptance_condition` in full
- A gap description if coverage is incomplete: "Stories cover X but
  acceptance_condition requires Y — gap: [description]"

Gap analysis is the primary output — not an annotation on a status table.
The skill must reason about sufficiency, not just count stories.

### AC4: HTML Artifact Is Written and Opened

- The skill writes a self-contained HTML file to `.claude/momentum/feature-status.html`
- The file has no external dependencies (all CSS inline, Mermaid.js via CDN ESM import)
- The file works when opened via `file://` (no server required)
- After writing, the skill opens it in a cmux browser pane:
  `cmux browser open file://{claude_project_dir}/.claude/momentum/feature-status.html`
- If cmux is not available, the skill outputs the file path and instructs the
  developer to open it manually

### AC5: HTML Layout Matches DEC-003 D2

The HTML artifact contains in order:
1. Page header: project name + generated date
2. Summary stats bar: total features, count by status (working/partial/not-working/not-started), gap count
3. Mermaid dependency graph: `flowchart TD` showing feature-to-story relationships,
   collapsed inside a `<details>` block by default
4. Feature tables grouped by type (flow / connection / quality for product; skill
   topology + SDLC coverage for practice)
5. Footer

Each table row shows: feature name (bold) → status badge (color-coded) →
story fraction N/M with mini progress bar → GAP indicator if coverage is incomplete.

### AC6: Signal Hierarchy Matches DEC-003 D3

- **Always visible in each row:** status badge, story fraction N/M, GAP flag
- **Behind `<details>` expand:** full acceptance_condition text, individual story
  list with per-story statuses, gap description
- **Never shown:** velocity, RICE scores, dates, raw percentages, owner/assignment
- Features with GAP flags sort to the top within each type group
- Within non-GAP rows, sort order: not-working → partial → working

### AC7: Product Project Rendering Path

When project type is `product` (or inferred as such):
- Feature tables are grouped by type: `flow`, `connection`, `quality`
- Each type group has a header and a per-group gap summary:
  "N features, M with gaps"
- Status badges use color convention: green (working), amber (partial),
  grey (not-started), red (not-working)

### AC8: Practice Project Rendering Path

When project type is `practice` (or inferred as such):
- The Mermaid diagram shows skill hand-off topology instead of feature-to-story
- Feature tables show SDLC phase coverage: which skills cover which phases
- Phases with no covering skill are flagged as gaps in the table

### AC9: Project Type Determination

- Project type is read from `project_type` in `_bmad/bmm/config.yaml` if present
- If not in config, inferred from features.json:
  - Features with `type: flow/connection/quality` → product
  - Features mapping to skills or SDLC phases → practice
  - Ambiguous → skill asks the developer to confirm

### AC10: Cache File Written

After writing the HTML artifact, the skill writes `.claude/momentum/feature-status.md`
with YAML frontmatter:
```
---
input_hash: {sha256 of features_content + ":" + stories_content}
summary: {N} features: {working} working · {partial} partial · {not-started} not-started · {gaps} gaps
generated_at: {ISO 8601 datetime}
---
```
The body of the file is the one-line summary (same as the frontmatter `summary` field).

### AC11: Workflow.md Exists and Drives the Skill

- `skills/momentum/skills/feature-status/workflow.md` exists with full step-by-step logic
- SKILL.md delegates entirely to workflow.md — no logic in SKILL.md body
- Workflow covers all steps: load config → read inputs → determine project type →
  gap analysis → build HTML context → write HTML → write cache .md → open in cmux

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before implementation)
  - [ ] `evals/eval-gap-analysis-flags-missing-coverage.md`
    "Given a features.json with a feature whose acceptance_condition is broader than
    its assigned stories, the skill produces an explicit gap flag naming what is missing
    and places that feature at the top of its type group in the HTML output."
  - [ ] `evals/eval-html-artifact-written-and-opened.md`
    "Given a valid features.json and stories/index.json, the skill writes
    .claude/momentum/feature-status.html (self-contained, works on file://) and
    opens it in a cmux browser pane, and writes .claude/momentum/feature-status.md
    with the correct frontmatter fields."
  - [ ] `evals/eval-product-vs-practice-rendering-paths.md`
    "Given a product project, the skill renders flow/connection/quality grouped tables.
    Given a practice project, the skill renders skill topology diagram + SDLC coverage
    table. Both produce valid HTML artifacts."

- [ ] Task 2 — Create SKILL.md (AC: 1)
  - [ ] `skills/momentum/skills/feature-status/SKILL.md` with frontmatter:
    name: feature-status, description ≤150 chars, model, effort
  - [ ] SKILL.md body: "Follow the instructions in ./workflow.md"

- [ ] Task 3 — Create workflow.md (AC: 2–11)
  - [ ] Step 1: Load config from `_bmad/bmm/config.yaml`, resolve paths
  - [ ] Step 2: Read `features.json`; surface clear error if not found
  - [ ] Step 3: Read `stories/index.json`, extract status and metadata per story
  - [ ] Step 4: Determine project type (config → inference → ask)
  - [ ] Step 5: For each feature, run gap analysis — evaluate whether assigned
    stories cover the full acceptance_condition; produce gap description where insufficient
  - [ ] Step 6: Build HTML context dict — feature groups, stats, Mermaid diagram source,
    gap flags, signal hierarchy (prominent vs. behind `<details>`)
  - [ ] Step 7: Write `.claude/momentum/feature-status.html` — self-contained HTML
    per DEC-003 D2/D3/D5/D6 layout (see Dev Notes for template structure)
  - [ ] Step 8: Write `.claude/momentum/feature-status.md` with frontmatter per AC10
  - [ ] Step 9: Open HTML in cmux browser pane (or output path if cmux unavailable)

- [ ] Task 4 — Run evals and verify (AC: 1–11)
  - [ ] Run each eval via subagent with SKILL.md and workflow.md as context
  - [ ] Confirm gap analysis eval: GAP features sort to top, gap description present
  - [ ] Confirm HTML artifact eval: file written, cmux opened, cache .md written
  - [ ] Confirm rendering eval: correct path per project type
  - [ ] Verify SKILL.md description ≤150 characters (count precisely)
  - [ ] Verify model: and effort: frontmatter present

## Dev Notes

### Architecture Context

This skill supersedes DRIFT-006. Feature-status is a standalone skill, not an
Impetus subcommand (DEC-002 D2).

**Inputs:** `features.json` (from feature-artifact-schema) + `stories/index.json`

**Outputs:**
- `.claude/momentum/feature-status.html` — full HTML planning artifact (DEC-003 D1)
- `.claude/momentum/feature-status.md` — frontmatter-only Impetus cache (DEC-003 D7)

### HTML Template Structure

The workflow.md should instruct the agent to write an HTML file following this pattern (reference: pytest-html self-contained single-file pattern):

```html
<!DOCTYPE html>
<html data-project-type="{product|practice}">
<head>
  <meta charset="utf-8">
  <title>Feature Status — {project_name}</title>
  <style>
    /* All CSS inline — no external files */
    [data-status="working"] .badge { background: #22c55e; }
    [data-status="partial"] .badge { background: #f59e0b; }
    [data-status="not-working"] .badge { background: #ef4444; }
    [data-status="not-started"] .badge { background: #9ca3af; }
    /* ... */
  </style>
</head>
<body>
  <header>...</header>
  <section class="summary-stats">...</section>
  <details class="dependency-graph">
    <summary>Feature dependency graph</summary>
    <div class="mermaid">flowchart TD ...</div>
  </details>
  <section class="feature-group" data-type="flow">
    <table>
      <tr data-status="partial">
        <td class="feature-name">User Onboarding</td>
        <td><span class="badge">partial</span></td>
        <td>2/4 <progress value="2" max="4"></progress></td>
        <td><span class="gap-flag">GAP</span></td>
        <td>
          <details>
            <summary>Details</summary>
            <p class="acceptance-condition">...</p>
            <ul class="stories">...</ul>
            <p class="gap-description">...</p>
          </details>
        </td>
      </tr>
    </table>
  </section>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
  </script>
</body>
</html>
```

The agent writes this directly using the Write tool — no momentum-tools.py
dependency needed. The workflow instructs what content to put in each section.

### Gap Analysis Logic

The gap analysis is a judgment call, not a mechanical count. The skill must
reason about what the acceptance_condition requires and whether the stories in
the `stories` list plausibly deliver it.

Example: if a feature's `acceptance_condition` is "A developer can run
momentum:sprint-planning and get a prioritized backlog with gap analysis" and
the only assigned story is "create SKILL.md wrapper", that story set has a gap.
Flag: "Gap: acceptance_condition requires gap analysis capability; assigned
stories only cover skill scaffolding."

### Mermaid Diagram

Use `flowchart TD` with `classDef` status coloring:

```
flowchart TD
  classDef working fill:#22c55e
  classDef partial fill:#f59e0b
  classDef notWorking fill:#ef4444
  classDef notStarted fill:#9ca3af

  F1["User Onboarding"]:::partial --> S1["onboarding-flow ✓"]
  F1 --> S2["feed-init ○"]
```

Node labels use feature name or story title. Status class applied per
features.json `status` field. The diagram is collapsed by default — wrap in
`<details><summary>Feature dependency graph</summary>...</details>`.

### Input Hash Computation

SHA-256 of `features_file_content + ":" + stories_file_content` (raw UTF-8).
The workflow instructs the agent to compute this via a Bash tool call:
```bash
python3 -c "
import hashlib
f = open('_bmad-output/planning-artifacts/features.json').read()
s = open('_bmad-output/implementation-artifacts/stories/index.json').read()
print(hashlib.sha256((f+':'+s).encode()).hexdigest())
"
```

### Relationship to Other Skills

| Skill | Relationship |
|---|---|
| `momentum:impetus` | Reads `.claude/momentum/feature-status.md` frontmatter for greeting cache (DEC-002 D3 / impetus-feature-status-cache story) |
| `feature-artifact-schema` | Must complete first — provides features.json |
| `feature-status-practice-path` | Extends this skill's practice rendering path |
| `sprint-boundary-compression` | Retro spawns this skill to refresh cache at sprint close |

### References

- [DEC-002 D2] `_bmad-output/planning-artifacts/decisions/dec-002-feature-visualization-and-orientation-2026-04-11.md`
- [DEC-003 D1–D7] `_bmad-output/planning-artifacts/decisions/dec-003-feature-status-artifact-design-2026-04-11.md`
- [Research] `_bmad-output/research/feature-status-visualization-2026-04-11/final/feature-status-visualization-final-2026-04-11.md`

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → skill-instruction (EDD — evals before implementation)
- Tasks 2, 3 → skill-instruction (SKILL.md + workflow.md)
- Task 4 → skill-instruction (EDD verification cycle)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Use EDD:

**Before writing a single line of the skill:**
Write 3 behavioral evals in `skills/momentum/skills/feature-status/evals/` per the
Tasks section above.

**Then implement:**
Write SKILL.md (frontmatter + delegation) then workflow.md (9-step workflow).

**Then verify:**
Run each eval via subagent. Give it the eval scenario + SKILL.md + workflow.md.
Observe whether behavior matches. Max 3 fix cycles; surface to user if still failing.

**NFR compliance:**
- SKILL.md `description` ≤150 characters (NFR1)
- `model:` and `effort:` frontmatter present (FR23)
- SKILL.md body ≤500 lines / 5000 tokens (NFR3)
- Skill name uses `momentum:` namespace prefix (NFR12)

**Additional DoD items:**
- [ ] 3 behavioral evals written in `skills/momentum/skills/feature-status/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented)
- [ ] SKILL.md description ≤150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present
- [ ] SKILL.md body ≤500 lines confirmed
- [ ] AVFL checkpoint documented

**Gherkin specs:** Off-limits to dev agent (Decision 30 black-box separation).

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
