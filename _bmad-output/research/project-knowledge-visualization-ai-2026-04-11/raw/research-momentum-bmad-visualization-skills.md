---
content_origin: claude-code-subagent
date: 2026-04-11
sub_question: "What existing Momentum skills or BMAD agents address project state visualization, knowledge mapping, or sprint/story coverage gaps?"
topic: "Project knowledge visualization and cognitive load reduction in AI-assisted development"
---

# Existing Momentum Skills and BMAD Agents for Project State Visualization

## Summary

This document surveys the Momentum plugin (local codebase at `/Users/steve/projects/momentum/skills/momentum/`) and the upstream BMAD ecosystem for existing capabilities that address project state visualization, knowledge mapping, and sprint/story coverage gap detection. The goal is to establish a clear baseline before designing new visualization features.

---

## Momentum: What Exists Today

### 1. Impetus — Session Orientation and Sprint Awareness

**Skill:** `momentum:impetus`
**File:** `/Users/steve/projects/momentum/skills/momentum/skills/impetus/SKILL.md`

Impetus is the primary entry point for all Momentum sessions and provides the most direct project state visualization currently available. Its session orientation function constructs a mental model of "where am I in this project" at session start. [OFFICIAL]

**Visualization capabilities:**

- **Progress Indicator (3-line format):** Impetus renders a compact, always-3-line progress indicator showing completed phases (✓), current phase (→), and upcoming phases (◦) with narrative descriptions. This is defined in `/skills/momentum/references/progress-indicator.md` and can be triggered on-demand when a developer asks "where am I?" or "show me my progress." The indicator collapses arbitrarily long workflows into exactly 2–3 lines, never growing with workflow length. [OFFICIAL]

- **Sprint awareness in greeting:** On session start, the preflight script (`momentum-tools.py session startup-preflight`) returns a pre-rendered `planning_context` field included in the greeting — this surfaces the active sprint name, stories in progress, and recent activity without requiring the developer to query separately. [OFFICIAL]

- **Open-thread orientation:** When the journal (`~/.claude/momentum/journal.jsonl`) contains open workflow threads, Impetus reads and presents them ordered by most-recently-active, with phase label, elapsed time, and last action. This is the closest Momentum currently comes to a "what was I working on?" map. The eval `eval-session-orientation-with-threads.md` specifies that within two exchanges, the developer should have: active story/task, current phase, last completed action, and suggested next action — without asking. [OFFICIAL]

- **On-demand position query:** Any query like "where am I?" during an active workflow triggers the progress indicator display, which reconstructs from journal state (`completed_steps`, `current_step` fields). [OFFICIAL]

**What it does NOT do:**
- Does not show cross-story coverage or gap analysis
- Does not visualize feature-to-story mapping or FR traceability
- Does not show the dependency graph between stories visually
- The progress indicator is workflow-scoped (shows phases of the current planning workflow), not sprint-scoped (does not show how many of N sprint stories are done)

---

### 2. Sprint Planning — Backlog Coverage and Dependency Graph

**Skill:** `momentum:sprint-planning`
**File:** `/Users/steve/projects/momentum/skills/momentum/skills/sprint-planning/workflow.md`

Sprint planning produces the most comprehensive "sprint topology" view in the current system. [OFFICIAL]

**Visualization capabilities:**

- **Backlog display:** Step 1 produces a grouped, sorted backlog view organized by `epic_slug`, with priority badges [C/H/M/L], status, dependency readiness, and `story_file` presence flags. This gives a snapshot of the complete open backlog at planning time.

- **Staleness detection:** Step 1 cross-references story `touches` paths against recent git history (`git log --since="30 days ago"`) to identify potentially stale stories — those that may already have been addressed by recent commits. Stale candidates are surfaced separately under "Potentially stale (may already be implemented)."

- **Dependency graph and execution waves:** Step 5 computes a dependency graph from `depends_on` fields and partitions stories into execution waves (Wave 1 = no dependencies on other selected stories; Wave 2 = depends on Wave 1; etc.). This wave assignment is stored in `sprints/index.json` and surfaced in the final sprint plan display.

- **Spec impact analysis:** Steps 4.5 spawns two parallel discovery agents to find gaps between story ACs and what is currently documented in PRD and architecture — surfacing NEW and MODIFIED items. This is a form of forward-looking coverage gap detection (what needs to be added to specs to cover this sprint's work).

- **Team composition matrix:** The final plan display (Step 7) shows a table: story → specialist domain → guidelines status — showing which stories have agent coverage and where guidelines are missing.

**What it does NOT do:**
- Produces output only during the planning workflow; does not provide an always-available sprint status view
- The wave/dependency graph is computed but not re-queryable outside sprint-dev execution

---

### 3. Refine — Backlog Hygiene, Coverage Drift, and Assessment/Decision Staleness

**Skill:** `momentum:refine`
**File:** `/Users/steve/projects/momentum/skills/momentum/skills/refine/workflow.md`

Refine is the most thorough coverage-gap analysis skill in the Momentum suite, though it is oriented toward artifact health rather than developer orientation. [OFFICIAL]

**Visualization/gap-detection capabilities:**

- **PRD coverage agent:** Spawns a subagent to read `prd.md` and `stories/index.json` together, identifying requirements that are Missing (not represented in any story), Outdated (described differently than implemented), or No longer accurate (contradicted by completed work). This is a bidirectional traceability check between planning artifacts and implementation backlog.

- **Architecture coverage agent:** Same pattern applied to `architecture.md` — identifies architectural decisions that are Missing (new architecture emerged, not documented), Outdated, or No longer accurate.

- **Status hygiene scan:** Reads story files and checks DoD checklists — if all `[x]` items are checked but status is not `done`, it flags as a mismatch. Surfaces stories that are effectively complete but not marked so.

- **Assessment and decision review:** Step 8 is a structured staleness review of ASR (Assessment Records) and SDR (Strategic Decision Records). It checks: ASR age (>30 days = stale), unacted-on assessments (decisions_produced is empty), unresolved next steps (no backlog story or SDR covering them), SDR stories_affected coverage (flags missing story slugs), and decision gate readiness (gates where all prerequisite stories are done). This cross-artifact coverage mapping is sophisticated but runs only on demand.

- **Re-prioritization analysis:** Four heuristics — recurrence (stories appearing in multiple sprint retros), workaround burden, forgetting risk, and dependency promotion (blockers at lower priority than what they block). The recurrence heuristic glob-scans `sprints/*/retro-*.md` for recurring patterns.

- **Consolidated findings with batch approval UX:** All findings are presented in a grouped list with batch approve/reject operations, making the gap-review process efficient even when many issues exist.

**What it does NOT do:**
- No visual topology — all output is text/table format
- Coverage analysis is ad-hoc (requires running refine); there is no persistent dashboard
- Runs only when explicitly invoked; not a continuous monitoring layer

---

### 4. Epic Grooming — Taxonomy Coverage and Orphan Detection

**Skill:** `momentum:epic-grooming`
**File:** `/Users/steve/projects/momentum/skills/momentum/skills/epic-grooming/workflow.md`

Epic grooming performs a structural coverage audit of the epic taxonomy. [OFFICIAL]

**Visualization/gap-detection capabilities:**

- **Registered vs. orphaned slug map:** Phase 1 reads `stories/index.json` and `epics.md`, then produces two lists: (a) Registered slugs — appear in epics.md with a definition, and (b) Orphaned slugs — appear in stories but have no epics.md definition. This is a coverage gap display in taxonomy terms.

- **Output format:** The Phase 1 output renders as: registered epics with story counts, orphaned slugs with sample story names, and a total summary. This is a direct "what is mapped vs. unmapped" view of the epic space.

- **FR/NFR coverage per epic:** When drafting CREATE proposals, the skill cross-references story FR mentions against the Requirements Inventory in prd.md — showing which functional requirements each epic covers.

**What it does NOT do:**
- No visual graph of epic relationships
- Does not show story-to-epic assignment density or imbalance (though story counts per epic are visible)

---

### 5. Assessment — Point-in-Time Product State Snapshot

**Skill:** `momentum:assessment`
**File:** `/Users/steve/projects/momentum/skills/momentum/skills/assessment/workflow.md`

Assessment is a collaborative product state evaluation skill that produces an ASR (Assessment Record). [OFFICIAL]

**Visualization/gap-detection capabilities:**

- **Parallel discovery agents:** Spawns multiple background subagents to audit actual codebase state (not documentation claims) — using evidence tables with Component | Status (Real/Stub/Missing/Broken) | Evidence (file path, LOC). This provides a codebase-reality map against declared state.

- **Findings organized by theme:** The ASR structure organizes findings into numbered sections with evidence tables, giving a structured gap map of the product state at assessment time.

- **Bridge to decision skill:** Offers to pass findings directly to `momentum:decision` — creating traceability from discovered gap → documented decision → backlog story.

**What it does NOT do:**
- One-shot; does not maintain a live or refreshable view
- No automatic comparison to prior ASRs (no diff between snapshots)

---

### 6. Retro — Sprint-Level Coverage and Execution Pattern Analysis

**Skill:** `momentum:retro`
**File:** `/Users/steve/projects/momentum/skills/momentum/skills/retro/workflow.md`

The retro skill performs a transcript-level audit of sprint execution, which is a form of retrospective knowledge mapping. [OFFICIAL]

**Visualization/gap-detection capabilities:**

- **Story verification table:** Phase 3 checks every sprint story against `stories/index.json` status and produces a verified vs. incomplete breakdown — a simple but direct coverage map of story completion.

- **Findings document (retro-transcript-audit.md):** The documenter agent synthesizes findings across three auditors into sections: What Worked Well, What Struggled, User Interventions, Story-by-Story Analysis, Cross-Cutting Patterns, and a Metrics table. The metrics table shows: user messages analyzed, subagents analyzed, tool errors, struggles, successes, user interventions, and cross-cutting patterns.

- **Priority Action Items:** Maps findings to proposed story stubs, creating a traceability link from execution gap → proposed backlog item.

**What it does NOT do:**
- Not queryable during sprint execution — only available after sprint completion
- No visual timeline or execution flow map

---

### 7. Configuration Gap Detection

**Reference:** `/Users/steve/projects/momentum/skills/momentum/references/configuration-gap-detection.md`

This is an always-on gap detection layer built into Impetus session startup and workflow step entry. [OFFICIAL]

**Gap detection capabilities:**
- Scans `installed.json` for component completeness at session start
- Checks protocol mapping for unbound types referenced by active workflows
- Checks `.mcp.json` for required MCP providers
- Classifies gaps as blocking (halts workflow) or non-blocking (proactive offer)

This is the closest thing to continuous monitoring in the current Momentum suite — it runs automatically at session start, not on demand. However, it covers configuration/tooling gaps, not story coverage or knowledge gaps.

---

## BMAD Ecosystem: What Exists

### 1. bmad-sprint-status — Story Status Dashboard

**Skill:** `bmad-sprint-status` (available in the local skills directory as a BMAD skill)
**Source:** BMAD-METHOD official repository ([GitHub Issue #886](https://github.com/bmad-code-org/BMAD-METHOD/issues/886)) [OFFICIAL]

The `bmad-sprint-status` skill reads `sprint-status.yaml` and displays:
1. Current epic being worked on
2. Story status breakdown (done/in-progress/review/drafted/backlog counts)
3. Next recommended story
4. Actionable menu: start next story or mark story status

The success metric cited in the BMAD spec is that developers check sprint status in under 10 seconds, versus 2–5 minutes of manual YAML parsing. This is BMAD's primary "project state at a glance" tool. [OFFICIAL]

**Key difference from Momentum's approach:** BMAD uses a flat YAML file (`sprint-status.yaml`) as the tracking artifact; Momentum uses structured JSON (`sprints/index.json` + `stories/index.json`) with CLI-enforced state transitions via `momentum-tools.py`.

---

### 2. bmad-check-implementation-readiness — Pre-Dev Coverage Gate

**Skill:** `bmad-check-implementation-readiness`
**Source:** BMAD-METHOD official repository, listed as a blocking pre-development gate [OFFICIAL]

This skill validates PRD, UX (if applicable), Architecture, and Epics/Stories for coherence before implementation begins. Output is a readiness report identifying gaps or granting approval to proceed. The BMAD documentation notes it "benefits from a separate high-quality model to avoid self-confirmation bias."

This is BMAD's answer to the "do I have enough spec coverage to build?" question — a structured pre-flight check, not a continuous visualization.

---

### 3. bmad-document-project and bmad-generate-project-context — Brownfield Knowledge Mapping

**Skills:** `bmad-document-project`, `bmad-generate-project-context`
**Source:** BMAD-METHOD official documentation ([Brownfield Development](https://deepwiki.com/bmad-code-org/BMAD-METHOD/4.9-brownfield-development)) and [GitHub Issue #1408](https://github.com/bmad-code-org/BMAD-METHOD/issues/1408) [OFFICIAL]

These two skills address developer onboarding and project knowledge mapping for established codebases:

- `bmad-document-project`: Runs the Analyst agent to produce documentation of the existing codebase structure, storing results in `docs/codebase/`. This is an AI-driven brownfield survey that surfaces what exists before planning begins.
- `bmad-generate-project-context`: Creates `project-context.md` capturing codebase patterns and conventions for AI agents — reduces "discovery phase" from ~20 minutes to ~5 minutes according to the BMAD documentation.

GitHub Issue #1408 proposes making these workflows interdependent, with `document-project` as an optional first step that feeds into `generate-project-context` — which would provide a combined human-readable and AI-optimized project knowledge map. [OFFICIAL]

---

### 4. bmad-create-epics-and-stories — PRD-to-Story Traceability

**Skill:** `bmad-create-epics-and-stories`
**Source:** BMAD-METHOD official repository [OFFICIAL]

This skill breaks requirements from a PRD into epics and user stories. In doing so it creates an implicit coverage map (each FR → one or more stories), though BMAD does not appear to have a dedicated reverse-query tool to ask "which FRs have no story coverage?" — that analysis would require running `bmad-check-implementation-readiness` or a custom query.

---

### 5. BMAD Workflow Map

**Source:** [BMAD Method official documentation](https://docs.bmad-method.org/reference/workflow-map/) [OFFICIAL]

BMAD provides a Workflow Map reference that gives a visual overview of all BMM phases, workflow artifacts, and context management. This is a static documentation artifact (not a live query), but it serves as the topological reference for where any given project sits within the BMAD lifecycle.

---

### 6. Sprint Agent Teams — Live Execution Tracking

**Source:** [GitHub Issue #1584 — Claude Code Agent Teams Sprint Automation Guide](https://github.com/bmad-code-org/BMAD-METHOD/issues/1584) [OFFICIAL]

In BMAD's Claude Code Agent Teams pattern (validated in production, per the GitHub issue from February 2026), a LEAD agent reads `sprint-status.yaml` to find stories with status "backlog" and explicitly assigns stories to teammate agents to avoid race conditions. This creates a form of live sprint state visibility — each agent reports its story status back to the shared YAML file, which any agent can query. [OFFICIAL]

This is a coordination-oriented visualization pattern, not a developer-facing dashboard, but it represents the state of the art for BMAD's approach to tracking parallel story execution.

---

## Gap Map: What Exists vs. What Is Missing

| Visualization Need | Momentum Coverage | BMAD Coverage |
|---|---|---|
| Session orientation (where was I?) | ✓ Impetus journal threads | Partial — no persistent thread model |
| Workflow position indicator | ✓ 3-line progress bar | Static Workflow Map doc |
| Sprint story status (done/in-progress/backlog counts) | Partial — shown in sprint-planning and refine, not on-demand | ✓ bmad-sprint-status (on-demand) |
| Backlog grouped by epic with priorities | ✓ Sprint-planning Step 1, refine Step 1 | ✓ bmad-sprint-status reads sprint-status.yaml |
| Dependency graph / execution waves | ✓ Sprint-planning Step 5 (computed at planning time) | Partial — wave-based execution in agent teams, not visualized |
| PRD/FR → story traceability | ✓ Refine PRD coverage agent (on demand) | ✓ bmad-check-implementation-readiness (blocking gate) |
| Architecture → story traceability | ✓ Refine architecture coverage agent | ✓ bmad-check-implementation-readiness |
| Epic taxonomy coverage (orphan detection) | ✓ epic-grooming Phase 1 | Not found |
| Stale story detection (git-based) | ✓ Sprint-planning Step 1 git staleness check | Not found |
| Configuration gap detection | ✓ Impetus session start (automatic) | Not found |
| Brownfield knowledge map | ✓ Assessment skill (collaborative, ad hoc) | ✓ bmad-document-project + bmad-generate-project-context |
| Decision/assessment staleness review | ✓ Refine Step 8 (structured, on demand) | Not found |
| Execution transcript analysis | ✓ Retro auditor team (post-sprint) | Not found — BMAD has retrospective skill but no transcript mining |
| Always-on sprint dashboard | Not found | ✓ bmad-sprint-status (on-demand, not always-on) |
| Cross-sprint gap trend analysis | Partial — refine recurrence heuristic reads retro files | Not found |
| Visual feature/FR coverage heat map | Not found | Not found |
| Workflow topology diagram | Not found | Static reference doc (Workflow Map) |

---

## Key Observations

**1. Momentum covers more depth; BMAD has better on-demand sprint status.**
Momentum's coverage detection is more sophisticated — refine's bi-directional PRD/architecture drift check, epic-grooming's orphan detection, and retro's transcript analysis go significantly deeper than anything in BMAD's published skills. However, BMAD's `bmad-sprint-status` provides a quick on-demand story count dashboard that Momentum does not. In Momentum, to get the equivalent of "how many stories are done vs. in-progress in this sprint?", you would need to run `momentum-tools.py` directly or trigger sprint-planning/refine.

**2. Both systems produce text output, not interactive visualizations.**
Neither Momentum nor the BMAD ecosystem produces graphical visualizations (charts, diagrams, dependency graphs). All state visualization is text/table format rendered in the terminal. There is no equivalent to a Jira board or GitHub Projects kanban view in either system.

**3. Coverage analysis is triggered, not continuous.**
In Momentum, coverage gap analysis (PRD drift, architecture drift, assessment staleness) requires explicit workflow invocation (refine, assessment, or epic-grooming). In BMAD, `bmad-check-implementation-readiness` is a blocking gate but only runs at one point in the workflow. Neither system maintains a live coverage health score or persistent gap dashboard.

**4. The progress indicator is the only persistent visual artifact.**
Momentum's 3-line progress indicator (defined in `progress-indicator.md`) is the only visual state element that persists across sessions via journal reconstruction. Everything else requires re-computation on demand.

**5. Stale detection is uniquely git-grounded in Momentum.**
Momentum's sprint-planning staleness check uses actual `git log` output to detect whether story `touches` paths have recent commits — a novel signal not found in BMAD's documented capabilities. This could surface stories that are already implemented without being marked done, which is a form of knowledge-to-reality gap detection.

**6. BMAD's brownfield skills address a gap Momentum doesn't.**
`bmad-document-project` and `bmad-generate-project-context` explicitly tackle the "new developer (or new agent) needs to understand an existing codebase" scenario. Momentum's `assessment` skill covers similar ground but is scope-driven and collaborative rather than automated survey-oriented.

---

## Sources

- ([GitHub — bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)) — Official BMAD repository
- ([BMAD V6 — Add sprint-status slash command — Issue #886](https://github.com/bmad-code-org/BMAD-METHOD/issues/886)) — Sprint-status feature specification
- ([Feature: Claude Code Agent Teams Sprint Automation — Issue #1584](https://github.com/bmad-code-org/BMAD-METHOD/issues/1584)) — Agent team sprint coordination patterns
- ([Make generate-project-context and document-project Interdependent — Issue #1408](https://github.com/bmad-code-org/BMAD-METHOD/issues/1408)) — Brownfield workflow interdependency proposal
- ([BMAD Method — Established Projects](https://docs.bmad-method.org/how-to/established-projects/)) — Brownfield approach documentation
- ([BMAD Workflow Map](https://docs.bmad-method.org/reference/workflow-map/)) — Official workflow topology reference
- ([Brownfield Development — DeepWiki](https://deepwiki.com/bmad-code-org/BMAD-METHOD/4.9-brownfield-development)) — Community wiki on brownfield workflows
- ([Status Tracking and Workflow State — DeepWiki](https://deepwiki.com/aj-geddes/claude-code-bmad-skills/5.5-status-tracking-and-workflow-state)) — Community documentation on BMAD status tracking
- ([BMAD Standard Workflow — DEV Community](https://dev.to/jacktt/bmad-standard-workflow-2kma)) — Practitioner overview of BMAD workflow sequence [PRAC]
- ([Applied BMAD — Benny Cheung](https://bennycheung.github.io/bmad-reclaiming-control-in-ai-dev)) — Practitioner report on brownfield BMAD usage [PRAC]
