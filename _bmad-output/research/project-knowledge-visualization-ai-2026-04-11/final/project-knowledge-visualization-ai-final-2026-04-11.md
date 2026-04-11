---
title: "Project Knowledge Visualization and Cognitive Load Reduction — Research Report"
date: 2026-04-11
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: true
derives_from:
  - path: raw/research-momentum-bmad-visualization-skills.md
    relationship: synthesized_from
  - path: raw/research-project-mgmt-visualization-patterns.md
    relationship: synthesized_from
  - path: raw/research-ai-dev-tools-sprint-awareness.md
    relationship: synthesized_from
  - path: raw/research-story-feature-traceability-patterns.md
    relationship: synthesized_from
  - path: raw/research-distance-to-working-software.md
    relationship: synthesized_from
  - path: raw/research-context-fragmentation-ai-workflows.md
    relationship: synthesized_from
  - path: validation/avfl-report.md
    relationship: validated_by
  - path: raw/practitioner-notes.md
    relationship: informed_by
---

# Project Knowledge Visualization and Cognitive Load Reduction in AI-Assisted Development

## Executive Summary

This report synthesizes research across six sub-questions to answer a single design problem: how should Momentum help developers orient to project state, feature completeness, and workflow topology without requiring them to hold that information in their heads?

The central finding is a structural gap. No explicit Feature artifact exists between PRD-level descriptions and story-level implementation. Stories get completed. Features do not emerge. The developer cannot see which user-facing capabilities actually work because no artifact tracks that question. This is true across the Momentum practice, the BMAD ecosystem, and every mainstream AI-assisted development tool surveyed.

The report proposes a concrete Feature artifact model, differentiates visualization frameworks for product projects (Nornspun) versus practice projects (Momentum), and identifies where new Momentum skills should be built to close the gap.

---

## 1. Existing Momentum and BMAD Capabilities

### What Momentum Provides Today

Momentum has substantial depth in coverage analysis, but it is scattered across skills that run on-demand and produce text output. No persistent, always-available project state view exists.

**Impetus** provides session orientation. It reads journal threads, renders a 3-line progress indicator (completed/current/upcoming phases), and surfaces the active sprint context in its greeting. For a developer returning to a session, Impetus answers "what was I working on?" within two exchanges. The progress indicator is the only visual state element that persists across sessions via journal reconstruction. [OFFICIAL]

**Sprint-planning** produces the richest sprint topology view at planning time: backlog grouped by epic with priority badges, git-based staleness detection for stories that may already be implemented, dependency graphs partitioned into execution waves, and spec impact analysis identifying PRD/architecture gaps. None of this is queryable after planning completes. [OFFICIAL]

**Refine** performs the most thorough coverage gap analysis: bidirectional PRD and architecture drift detection, status/DoD mismatch flagging, assessment and decision staleness review, and re-prioritization heuristics based on retro recurrence. It runs only when explicitly invoked. [OFFICIAL]

**Epic-grooming** audits the epic taxonomy for orphaned slugs and FR coverage per epic. **Assessment** spawns parallel discovery agents to audit codebase reality against declared state, producing evidence tables with Component/Status/Evidence. **Retro** performs transcript-level sprint execution analysis with story verification tables. [OFFICIAL]

**Configuration gap detection** is the only always-on mechanism. It scans `installed.json` and protocol mappings at session start, classifying gaps as blocking or non-blocking. It covers tooling gaps, not story or feature gaps. [OFFICIAL]

### What BMAD Provides

BMAD's `bmad-sprint-status` reads `sprint-status.yaml` and displays story counts by state, the current epic, and the next recommended story. Developers check sprint status in under 10 seconds. This on-demand story dashboard is the one capability Momentum lacks a direct equivalent for. [OFFICIAL]

`bmad-check-implementation-readiness` validates PRD, UX, Architecture, and Epics/Stories for coherence as a blocking pre-development gate. `bmad-document-project` and `bmad-generate-project-context` address brownfield onboarding with automated codebase surveys. `bmad-create-epics-and-stories` creates an implicit FR-to-story mapping during planning, though no dedicated reverse-query exists. [OFFICIAL]

### The Gap Map

| Need | Momentum | BMAD |
|---|---|---|
| Session orientation | Yes (Impetus) | Partial |
| Workflow position indicator | Yes (3-line progress) | Static doc |
| On-demand sprint story counts | No | Yes (sprint-status) |
| PRD/architecture drift detection | Yes (refine, on-demand) | Yes (readiness gate) |
| Dependency graph / execution waves | Yes (sprint-planning, at plan time only) | Partial |
| Epic taxonomy coverage | Yes (epic-grooming) | No |
| Git-based staleness detection | Yes (sprint-planning) | No |
| Brownfield knowledge mapping | Partial (assessment) | Yes (document-project) |
| Always-on sprint dashboard | No | No (on-demand only) |
| Feature coverage heat map | No | No |
| Workflow topology diagram | No | Static reference doc |

The critical observation: both systems produce text/table output. Neither produces interactive or graphical visualizations. All coverage analysis is triggered, not continuous. There is no persistent dashboard in either ecosystem.

---

## 2. Project Management Visualization Patterns

### Cognitive Load Foundations

Cognitive Load Theory (Sweller, 1988; updated 2024) distinguishes intrinsic load (task complexity), extraneous load (interface overhead), and germane load (productive schema-building). The design goal for a developer dashboard is minimizing extraneous load. [OFFICIAL — ScienceDirect]

Research on dashboard density found that **individuals become overwhelmed when dashboards contain nine or more information modules**. This provides a concrete ceiling for multi-widget designs. [OFFICIAL — ScienceDirect]

Dual Coding Theory (Paivio, 1971) establishes that text labels paired with visual structure (color, position, shape) are processed more efficiently than either channel alone. Story status as a colored badge next to a title is more cognitively efficient than a text status field. [OFFICIAL — Wikipedia]

### Applicable Patterns

**Kanban (WIP limits)** has the highest orientation value for the smallest dashboard footprint. A compact 4-column summary (Backlog/In Progress/In Review/Done) with story counts per state gives instant orientation. The blocked-count signal is the highest-value indicator for a developer returning to context. [OFFICIAL — Atlassian]

**Story Map** (Patton, 2014) is the most direct pattern for feature gap visibility. The horizontal backbone represents user activities; stories stack vertically underneath. Gaps are structurally visible as blank columns. For dashboard use, a row-summary or coverage heatmap derived from the story map structure is more tractable than the full map. [OFFICIAL — jpattonassociates.com]

**Dependency Graph (DAG)** answers "what can I start now without waiting?" and "what am I blocking?" Developers already read DAG representations from CI/CD pipelines (GitLab, GitHub Actions), so the visual idiom transfers directly to story dependencies. Must be scoped to sprint or epic to avoid unreadable clutter. [OFFICIAL — GitLab]

**Now/Next/Later Roadmap** eliminates date-based schedule math. Position in three zones is the status. Translates directly to developer prioritization: what am I working on, what needs context preparation, what can I ignore. [PRAC — Aha!, Zenhub]

**Progressive Disclosure** is the meta-pattern. Three disclosure levels maximum (overview, sprint detail, story detail) before navigation overhead exceeds cognitive savings. Presenting minimal information by default, revealing detail on demand, achieves 30-50% faster initial task completion while maintaining 70-90% feature discoverability. [PRAC — Honra.io]

### Design Principles for Momentum

1. **Eight-or-fewer modules.** A developer dashboard must be opinionated about what it does not show.
2. **Visual hierarchy over density.** Layouts with less than 40% information density show substantially faster pattern recognition. [PRAC — Agile Analytics]
3. **Blocked state is the highest-value signal.** Dependency graphs and blocked indicators take priority over progress percentages.
4. **Dual-channel presentation.** Text labels plus visual structure (color, position, shape) for every status indicator.
5. **Stable signal vocabulary.** Changing what a dashboard shows erodes its utility. Developers build pattern recognition for specific signals. Minimal, stable indicator sets.

---

## 3. AI Development Tools and Sprint Awareness

### The Industry Bifurcation

The AI tooling ecosystem splits cleanly into two halves that do not talk to each other:

**Top-down planning intelligence** (Linear, Jira, Notion): Story state, assignment, priority, duplicate detection. No awareness of what code exists.

**Bottom-up code intelligence** (Cursor, Windsurf, Copilot): Deep codebase awareness. No awareness of which stories are in scope.

No mainstream tool occupies the middle: a developer-facing orientation layer that synthesizes sprint state, story coverage, and codebase topology.

### Notable Capabilities

**GitHub Copilot Mission Control** (October 2025) is the closest thing to sprint-level agent visibility: a centralized dashboard tracking all active Copilot agent tasks with real-time status, progress, and navigation. It tracks code agent sessions, not sprint stories. [OFFICIAL — GitHub Blog]

**Linear Product Intelligence** (Technology Preview, August 2025) builds a semantic map of the issue space, detecting duplicates and suggesting routing. It operates at the story level, not the feature or epic level. It cannot answer "what parts of this epic are not yet covered by any story." [OFFICIAL — Linear Changelog]

**Notion 3.0 Agents** (September 2025) can aggregate open issues, propose sprint plans, and flag tasks missing test coverage. This is the most explicit feature coverage gap capability found in any mainstream tool. However, it is prompt-driven, not a continuous monitor, and has no git-level awareness. [OFFICIAL — Notion]

**Jira Atlassian Intelligence** processes each issue in isolation. A practitioner review states directly: "Atlassian Intelligence looks at each issue alone and never connects the dots." Cross-issue reasoning is absent from the product. [PRAC — Cotera]

### Six Gaps No Tool Fills

1. **Continuous feature coverage monitoring.** No tool proactively monitors the sprint backlog against PRD or epic specs.
2. **Cross-issue reasoning in PM tools.** Neither Jira nor Linear synthesizes feature-level coverage from individual stories.
3. **Bidirectional code-to-story coverage.** No tool bridges from "code written" to "acceptance criteria exercised."
4. **Sprint topology visualization.** No tool provides a developer-facing view of story dependencies and coverage topology within a sprint.
5. **Definition of Done AI enforcement.** No tool monitors whether DoD criteria are met at the code level in real time.
6. **Workflow topology awareness.** AI coding assistants have no knowledge of the team's workflow structure.

The 2025 DORA State of AI-Assisted Development report confirms the consequence: AI tools increase individual output (21% more tasks completed, 98% more PRs merged) but do not automatically improve organizational delivery metrics. Higher AI adoption correlates with increased deployment instability in teams with weak processes. [OFFICIAL — DORA]

---

## 4. Story-to-Feature Traceability Patterns

### The Layered Approach

No single pattern solves the traceability problem. The field has converged on a stack:

| Layer | Pattern | Gap Revealed |
|---|---|---|
| Strategic | Impact Map | Business goals with no stories; stories with no business rationale |
| Structural | Story Map | Activities with no coverage; isolated stories not connected to a journey |
| Hierarchical | Work Item Hierarchy | Features with few/no stories; stories not assigned to any feature |
| Specification | BDD Feature Files + Serenity Reports | Acceptance criteria not yet implemented |
| Verification | Requirements Traceability Matrix (RTM) | Requirements with no test coverage |
| Lifecycle | Feature Flag Registry | Capabilities in partial delivery with no completion path |

### The Core Insight

Traceability requires explicit modeling of the feature layer. Whether the model is a story map backbone, an Azure DevOps Feature work item, a BDD Feature file, or an impact map branch, the feature must be a **named, persistent artifact** — not an implicit grouping. When features are explicit, gaps become visible as the absence of child stories, test coverage, or behavioral specifications. [OFFICIAL — Inflectra, Microsoft Learn]

### The Work Item Hierarchy Gap

Azure DevOps uses a 4-level hierarchy: Epic > Feature > User Story > Task. Features are explicitly modeled as a level between Epics and Stories. [OFFICIAL — Microsoft Learn]

Jira uses a 3-level hierarchy: Epic > Story > Subtask. There is no native "Feature" level. Teams model features inconsistently — sometimes as Epics, sometimes via custom hierarchy. [PRAC — Atlassian Community]

**Momentum has no Feature level at all.** PRD has feature descriptions. Epics are thematic containers. Stories implement code. Nothing tracks "can a user do X yet?" This is confirmed as the central design problem by practitioner input.

### BDD Living Documentation

BDD with Gherkin syntax addresses traceability through executable specifications. Serenity BDD produces structured reports showing requirement coverage — which features have been tested, which have not. The traceability chain runs: Feature file > Scenario > Step definitions > implementation code. Over 60% of agile teams have adopted BDD practices (2024 World Quality Report), though 42% still struggle to trace scenarios to CI test results. [PRAC — TestQuality]

### AI-Assisted Traceability

Emerging tools (aqua cloud, TestCollab) use AI for automated link suggestion between tests and requirements, gap detection for unmapped requirements, and impact analysis when requirements change. These are strongest at the test-requirement link level. The higher question — "which stories together deliver a coherent feature?" — still requires human modeling because it depends on product intent not derivable from text similarity. [PRAC — aqua cloud]

---

## 5. Visualizing Distance to Working Software

### The Core Tension

A team can check off every story in a sprint and still not have a working, user-visible feature. This is not a theoretical risk. It is the current state of Nornspun: many stories completed, zero features working E2E. Stories "done" individually do not add up to something shippable. This is the "last mile" problem in feature delivery.

### What Existing Frameworks Measure (and What They Miss)

**Definition of Done** applies at the story level. A capability may require five stories, all individually "Done" per DoD, but without integration and E2E testing, the capability is not working. DoD measures task completion, not capability delivery. [OFFICIAL — Scrum Alliance]

**DORA Lead Time** measures elapsed time from commit to production. It measures speed, not coverage. It does not tell you which capabilities are incomplete. [OFFICIAL — DORA]

**Feature flags** decouple code deployment from feature activation. A flag's rollout percentage (0% > 10% > 100%) is an implicit readiness indicator. But flags do not show what is still needed — only whether what exists is on or off. [OFFICIAL — LaunchDarkly]

**CI/CD pipeline position** shows where a deployment is in the pipeline (build > test > staging > production). It does not connect to user-visible capabilities. [PRAC — TestRail]

**Story Map + Release Cuts** is the highest-signal approach. The walking skeleton — the first horizontal release slice, a thin E2E implementation of the most critical path — directly addresses the "stories done but feature not working" problem. But story maps require manual curation and do not auto-update from execution state. [OFFICIAL — Agile Alliance, Patton]

**Value Stream Mapping** makes the full delivery path visible: every step from ideation through deployment, where time is lost, where queues accumulate. The WIP at each stage is the literal distance remaining. [OFFICIAL — DORA]

### The Missing Metric

No mainstream tool or framework models "how many more steps until this end-to-end capability works." The closest approximation is a **capability dependency graph**: Feature X requires stories A, B, C, D. A and B are done. C is in progress. D has not started. The feature is 50% done but 0% usable because C is the integration story that connects A+B to the user. This framing exists in theory (vertical slicing, walking skeleton) but is not operationalized in any tracked metric.

For a solo AI-assisted developer, this gap is amplified. There is no standup to surface "I finished the API but the UI isn't wired up yet." The developer must carry dependency state in working memory or lose track of it. The 2025 DORA AI report confirms: AI tools widen the last-mile gap by accelerating story-level completion without improving end-to-end delivery. [OFFICIAL — DORA]

---

## 6. Managing Context Fragmentation in AI Workflows

### The Scale of the Problem

Model performance drops 39% on average in multi-turn conversations similar to real agent workflows. [UNVERIFIED — this statistic is attributed to Microsoft and Salesforce research but was encountered only via a practitioner blog (LogRocket). The primary source was not directly verified.]

Independent research estimated that nearly 65% of enterprise AI failures in 2025 were attributed to context drift or memory loss during multi-step reasoning — not raw context exhaustion. [PRAC — Zylos Research]

Four named failure modes: context poisoning (false beliefs reinforced), context distraction (performance degrades with irrelevant context), context confusion (irrelevant info influences unrelated responses), and context clash (contradictory information in history). [PRAC — LogRocket]

### Context Engineering as Discipline

Andrej Karpathy coined "context engineering" in mid-2025 as the successor to prompt engineering: "the delicate art and science of filling the context window with just the right information for the next step." [OFFICIAL — Karpathy via pureai.com]

Anthropic formalized three primary techniques for long-horizon tasks: compaction (summarize history, restart with compressed context), structured note-taking (external memory files that persist outside the context window), and sub-agent architectures (specialized agents handle focused tasks, return condensed summaries). [OFFICIAL — Anthropic Engineering]

Factory.ai's empirical study found that **structure forces preservation**. Anchored iterative summarization — extending rather than regenerating summaries — outperformed both Anthropic's full-regeneration approach and OpenAI's opaque compression. The key sections: session intent, file modifications, decisions taken, next steps. [PRAC — Factory.ai]

### File-Based Context Patterns

The AI coding ecosystem has converged on three patterns:

**Single root context file** (CLAUDE.md, .copilot-instructions.md): Read at session start. Under 300 lines is best. Auto-generated files are consistently worse than manually refined ones. Orients the AI to conventions but not to what has changed recently. [OFFICIAL — Anthropic; PRAC — HumanLayer]

**Scoped rule files** (.cursor/rules/*.mdc): Individual rule files for better organization. Same function as CLAUDE.md — anchor conventions, not dynamic state. [PRAC — Cursor docs]

**Memory Bank** (multi-file layered system): Separates stable files (projectbrief.md, techContext.md, systemPatterns.md) from dynamic files (activeContext.md, progress.md). Most project context is stable. Current-state context must be kept fresh. Reduces initial token usage by approximately 70% versus loading all context at once. [PRAC — Lullabot, Tweag]

### What Momentum Already Does

Momentum implements several context fragmentation countermeasures:

- **Journal-based session continuity**: Append-only JSONL with `context_summary` fields designed for re-orientation without re-reading source files. Thread state recovered on each session start via Impetus.
- **Just-in-time spec surfacing**: One sentence from the relevant spec section at the moment it matters, with `[Source: path#Section]` citation. The RAG "just-in-time loading" pattern applied to spec documents.
- **Sub-agent architecture**: Hub-and-spoke model isolates each story's implementation context within a dedicated subagent, preventing story-level detail from polluting the coordinator context.
- **Sprint logs as provenance**: Per-sprint JSONL audit trails for queryable history of workflow decisions.
- **Declined offer tracking**: `context_hash` fingerprints enable material-change detection, preventing stale suppression decisions.

### Remaining Gaps

1. **No aggregate story coverage view.** The journal tracks individual threads but provides no summary of what features have been built across full sprint/epic history.
2. **No feature gap detection from history.** Sprint logs are queryable but not synthesized into a "what has been built" document.
3. **No visual workflow topology.** Sub-agent relationships, story dependencies, and sprint boundaries exist in data but are not visualized.
4. **Context compression is reactive, not proactive.** No sprint-boundary compression summarizes the previous sprint before the next begins.
5. **Decision provenance requires explicit lookup.** Architecture decisions are stored but require knowing which decision number to ask about.

### The Orientation Stack

A coherent orientation stack for AI-augmented workflows requires four layers:

| Layer | Time Horizon | Mechanism | In Momentum? |
|---|---|---|---|
| Session | Current conversation | Journal threads + JIT spec surfacing | Yes |
| Sprint | Active sprint scope | Sprint logs + story dependency graph | Partial (logs exist, no synthesis) |
| Feature | Accumulated capabilities | "What has been built" artifact | No |
| Architecture | Project lifetime | ADRs + decision graph | Partial (architecture.md, no graph) |

The feature and architecture layers — particularly in navigable form — are the primary design opportunity.

---

## Cross-Cutting Themes

### Theme 1: The Feature Layer is the Missing Structural Element

Every sub-question converges on the same finding. The traceability research identifies it as the absent layer between epics and stories. The distance-to-working-software research identifies it as the missing capability dependency graph. The AI tools survey identifies it as the gap no tool fills. The Momentum/BMAD inventory confirms neither ecosystem models it. The context fragmentation research identifies the feature accumulation view as the missing orientation stack layer.

A feature is not an epic. Epics are thematic containers ("Agent UX"). Features are user-observable capabilities ("User can initialize a campaign"). Both are important. Neither replaces the other. The feature must be a named, persistent artifact with an acceptance condition.

### Theme 2: Stories Done Does Not Equal Features Working

The 2025 DORA AI report documents this at industry scale: AI increases story throughput without improving end-to-end delivery. Nornspun exemplifies it: many stories completed, zero E2E features working. The visualization challenge is making this gap visible rather than hiding it behind story completion percentages.

The walking skeleton pattern (Patton) directly addresses this by defining the thinnest E2E slice as the first delivery target. But the pattern needs a tracking artifact — which loops back to Theme 1.

### Theme 3: Two Project Types Need Different Visualization Frameworks

Product projects (Nornspun) and practice projects (Momentum) have fundamentally different orientation needs.

**Product project visualization tracks:**
- Flow features: "User can complete X from start to finish"
- Connection features: "API/client connects and responds"
- Quality features: visual consistency, screenshots actual vs. target wireframe across platforms

**Practice project visualization tracks:**
- Skill topology: how all skills connect through Impetus
- SDLC coverage: which workflow steps are covered vs. missing
- Skill interactions and redundancy
- Process gaps at the SDLC level

These cannot share a single visualization framework. The Feature artifact model must accommodate both types through its type taxonomy, but the rendering and evaluation logic differ.

### Theme 4: Continuous Visibility vs. On-Demand Analysis

Every existing coverage analysis tool — Momentum's refine, BMAD's sprint-status, Linear's Product Intelligence, Notion's agents — runs on demand. None provides continuous monitoring. The dashboard density research (eight-module ceiling, three-disclosure-level maximum) suggests that continuous visibility should be a compact, stable overview that triggers on-demand deep analysis rather than replacing it.

### Theme 5: Context Engineering is the Agent-Side of the Same Problem

Developer orientation and agent orientation are the same problem from different angles. A developer returning after a week and a fresh AI session face identical challenges: no persistent memory of what has been built, why decisions were made, or what is in progress. The Memory Bank's separation of stable context (architecture, conventions) from dynamic context (current state, recent changes) applies to both human and agent consumers. Designing the Feature artifact as an always-current, machine-readable document serves both audiences.

---

## Recommendations

### Recommendation 1: Introduce the Feature Artifact

**What:** A new artifact type — `features.json` or per-feature files in a `features/` directory — that explicitly models user-facing capabilities as persistent, trackable units with acceptance conditions and linked stories.

**Minimal schema:**

```json
{
  "feature_slug": "campaign-init",
  "name": "Campaign Initialization",
  "type": "flow",
  "description": "User can initialize a new campaign from scratch and reach the prep screen.",
  "acceptance_condition": "E2E: User starts app, creates campaign, reaches prep screen with valid state.",
  "status": "not-working",
  "prd_section": "FR-12",
  "stories": ["campaign-init-api", "campaign-init-ui", "campaign-init-e2e-test"],
  "stories_done": ["campaign-init-api"],
  "stories_remaining": ["campaign-init-ui", "campaign-init-e2e-test"],
  "last_verified": null,
  "notes": "API story done but UI not wired up. Zero E2E coverage."
}
```

**Field definitions:**

| Field | Purpose |
|---|---|
| `feature_slug` | Unique identifier. Used for cross-referencing from stories and PRD. |
| `name` | Human-readable feature name. |
| `type` | One of: `flow` (E2E user journey), `connection` (infrastructure prerequisite), `quality` (observable state/UX). Type determines how status is evaluated, not whether something qualifies as a feature. |
| `description` | One sentence describing what the user can accomplish. |
| `acceptance_condition` | The working/not-working test. For flows: E2E journey description. For connections: connectivity assertion. For quality: comparison criteria (screenshot vs. wireframe). |
| `status` | One of: `working`, `partial`, `not-working`, `not-started`. `partial` means some constituent stories are done but the acceptance condition is not met. |
| `prd_section` | Link back to the PRD requirement(s) this feature satisfies. Enables forward traceability. |
| `stories` | All stories that contribute to this feature. A story may appear in multiple features. |
| `stories_done` / `stories_remaining` | Derived from cross-referencing `stories` against `stories/index.json` status. Could be computed rather than stored. |
| `last_verified` | ISO date when the acceptance condition was last manually or automatically verified. Null means never verified. |
| `notes` | Free text for current state context. |

**Relationship to existing artifacts:**

```
PRD (prd.md)
  └─ Feature (features.json) ← NEW
       ├─ Story A (stories/index.json)
       ├─ Story B
       └─ Story C
Epic (epics.md)  ← parallel, not hierarchical
  ├─ Story A
  ├─ Story D
  └─ Story E
```

Features and epics are orthogonal. An epic groups stories by theme. A feature groups stories by user-observable capability. A story can belong to one epic and one or more features. The feature answers "can a user do X yet?" The epic answers "have we addressed the Y theme?"

**Design principle:** A feature is a finite, user-observable unit with a finite set of duties and a clear working/not-working acceptance condition. Granularity does not determine what counts as a feature. "Campaign init" is a feature whether it takes 1 story or 15. E2E flows are features. The type taxonomy (flow/connection/quality) informs how you evaluate status, not whether something qualifies.

### Recommendation 2: Build a `momentum:feature-status` Skill

**What:** An on-demand skill that reads `features.json`, cross-references story statuses from `stories/index.json`, and produces a compact feature status view.

**Output format (product project):**

```
FEATURES — Nornspun (2026-04-11)

FLOW FEATURES
  [NOT WORKING] Campaign Init — 1/3 stories done, E2E not verified
  [NOT WORKING] Game Prep — 0/4 stories done
  [PARTIAL]     Character Select — 3/5 stories done, UI connected but flow breaks at step 4

CONNECTION FEATURES
  [WORKING]     API Auth — verified 2026-04-08
  [NOT WORKING] Chat WebSocket — client connects, no response handling

QUALITY FEATURES
  [NOT STARTED] Visual Consistency (iOS) — no stories assigned
  [NOT STARTED] Visual Consistency (Android) — no stories assigned

Summary: 0/3 flows working | 1/2 connections working | 0/2 quality features started
```

**Output format (practice project):**

```
SKILLS — Momentum (2026-04-11)

SDLC COVERAGE
  [COVERED]   Planning    — sprint-planning, refine, epic-grooming
  [COVERED]   Execution   — sprint-dev, dev, quick-fix
  [COVERED]   Validation  — avfl, code-reviewer
  [COVERED]   Review      — retro, assessment
  [PARTIAL]   Intake      — intake exists, triage not built
  [MISSING]   Release     — no release/deploy skill

SKILL TOPOLOGY (via Impetus)
  impetus → sprint-planning → sprint-dev → dev → avfl → retro
                                         → quick-fix → avfl
  impetus → refine
  impetus → assessment → decision
  impetus → epic-grooming

REDUNDANCY FLAGS
  (none detected)

Summary: 4/6 SDLC phases covered | 1 partial | 1 missing
```

**Why this matters:** This skill fills the gap that no AI development tool currently fills — a developer-facing view that synthesizes sprint state and codebase topology into a unified capability status. It answers the question "what actually works?" rather than "how many stories are done?"

### Recommendation 3: Embed Feature Context in Impetus Greeting

**What:** Extend Impetus session startup to include a one-line feature status summary in the greeting, alongside the existing sprint context.

**Example:**

```
Active sprint: 2026-04-08 (4/7 stories done)
Feature status: 0/3 flows working | 1/2 connections working
Open threads: 2 (campaign-init-ui in dev, chat-websocket blocked)
```

This makes the "stories done does not equal features working" gap visible at every session start without requiring an explicit skill invocation. The feature status line is derived from `features.json` and adds one line to the existing greeting format.

**Design constraint:** This must not increase Impetus startup latency. The feature status line should be pre-computed by the preflight script, not calculated at greeting time.

### Recommendation 4: Add Sprint-Boundary Context Compression

**What:** At sprint close (triggered by retro completion), automatically produce a structured sprint summary artifact that serves as the stable context layer for subsequent sprints.

**Contents:**
- Features advanced (which features moved closer to working, which did not)
- Stories completed vs. planned
- Key decisions made (with SDR references)
- Unresolved issues carried forward
- One-paragraph narrative summary

**Purpose:** This fills the gap between Momentum's session-level journal (too granular for multi-sprint orientation) and the project-level architecture.md (too stable to reflect recent progress). It is the Memory Bank `progress.md` pattern applied at sprint cadence. Agents starting new sprints load the most recent sprint summary rather than parsing raw sprint logs.

### Recommendation 5: Differentiate Product and Practice Visualization Paths

Do not attempt a single visualization framework for both project types. Build two rendering paths within `feature-status`:

**Product projects** get the feature type taxonomy (flow/connection/quality), acceptance condition tracking, and story-to-feature coverage mapping. Quality features should support screenshot comparison data (actual state vs. target wireframe) as a future extension.

**Practice projects** get the skill topology view (how skills connect through Impetus), SDLC coverage mapping (which workflow phases are covered/partial/missing), and redundancy detection. The "feature" concept translates to "SDLC phase coverage" — the acceptance condition is "this phase of the development lifecycle is handled by one or more skills."

The detection of which rendering path to use can be driven by project metadata (a `project_type` field in the Momentum configuration) or inferred from the presence of `features.json` (product) vs. skill directory structure (practice).

### Recommendation 6: Build Incrementally

The priority order based on immediate developer pain:

1. **Feature artifact schema** (Recommendation 1) — foundation for everything else. Define the schema, create `features.json` for Nornspun as the first instance. This is a design task, not a code task.
2. **Feature-status skill** (Recommendation 2) — the first consumer of the artifact. Start with the product project rendering path since that is where the "stories done but nothing works" pain is acute.
3. **Impetus greeting integration** (Recommendation 3) — makes the feature status passively visible without explicit invocation.
4. **Sprint-boundary compression** (Recommendation 4) — addresses multi-sprint context fragmentation. Can be built independently of the feature work.
5. **Practice project rendering** (Recommendation 5) — extend feature-status with the skill topology view for Momentum itself.

Each step produces immediate value. No step depends on all previous steps being complete.

---

## Known Limitations

### Weak Evidence Areas

- The "39% performance drop in multi-turn conversations" statistic attributed to Microsoft and Salesforce research was encountered only via LogRocket, a practitioner blog. The primary source was not directly verified. Treat as directional, not authoritative. [UNVERIFIED]
- The "65% of enterprise AI failures from context drift" statistic is from Zylos Research, a source whose methodology is not independently verifiable. [PRAC]
- Dashboard density research (nine-module ceiling) comes from a construction industry study. Direct applicability to developer dashboards is inferred, not measured. [OFFICIAL source, but cross-domain transfer is unverified]
- Practitioner claims about progressive disclosure achieving "30-50% faster initial task completion" are from Honra.io without cited primary research. [PRAC]

### AVFL-Flagged Items

The AVFL validation (checkpoint profile, score 86/100 post-fix) flagged and resolved seven issues across the corpus. One finding carried forward:

- **C-001 (LOW):** The AI tools research file and the context fragmentation file both discuss Momentum's positioning but do not cross-reference each other's analysis. This creates minor redundancy risk in synthesis but no factual inconsistency. This synthesis addresses the gap by integrating both analyses.

The highest-severity findings were:
- ACCURACY-001: A statistic falsely attributed to a "Stack Overflow developer survey" was actually from a DEV Community blog post. Fixed to "Practitioner research found."
- ACCURACY-002: Specific AI model version names (GPT-5.2, Claude Opus 4.5, Gemini 3) listed as Notion 3.2's multi-model options were unverifiable and likely hallucinated. Fixed to generic provider attribution.

### Open Questions

1. **Feature artifact governance.** Who updates `features.json`? If it requires manual curation, it will drift. If it is agent-updated, what triggers the update? The `momentum:feature-status` skill could update computed fields (stories_done, stories_remaining) automatically, but `status` and `last_verified` require human judgment or E2E test results.

2. **Feature artifact scope.** Should features be defined per-project or per-epic? Per-project is simpler but may not scale. Per-epic creates the risk of features crossing epic boundaries (which they will, by definition — features and epics are orthogonal).

3. **Quality feature verification.** The quality feature type (visual consistency, screenshots actual vs. target) requires a verification mechanism that does not exist today. Screenshot comparison tooling (Percy, Chromatic, Playwright visual regression) could provide this, but integrating it into the feature status pipeline is a separate design problem.

4. **Skill topology generation.** The practice project rendering path requires extracting skill-to-skill relationships from workflow files. This is parseable from existing `workflow.md` files but has not been automated. Whether this should be a computed view or a maintained artifact is an open design question.

5. **Continuous vs. on-demand.** The research supports on-demand analysis with a compact always-visible summary (the Impetus greeting line). Whether to build a continuous monitoring layer beyond this is a cost-benefit question that depends on how frequently feature status changes in practice.

---

## Sources

### Official / Primary

- Anthropic Engineering: Effective Context Engineering for AI Agents — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic: Using CLAUDE.md Files — https://claude.com/blog/using-claude-md-files
- Atlassian: Cumulative Flow Diagram — https://support.atlassian.com/jira-software-cloud/docs/what-is-the-cumulative-flow-diagram/
- Atlassian: Definition of Ready — https://www.atlassian.com/agile/project-management/definition-of-ready
- Atlassian: WIP Limits — https://www.atlassian.com/agile/kanban/wip-limits
- BMAD-METHOD GitHub Repository — https://github.com/bmad-code-org/BMAD-METHOD
- Datadog: Continuous Delivery Visibility — https://docs.datadoghq.com/continuous_delivery/
- DORA.dev: Four Keys Metrics Guide — https://dora.dev/guides/dora-metrics-four-keys/
- DORA: State of AI-Assisted Software Development 2025 — https://dora.dev/dora-report-2025/
- DORA: Value Stream Mapping — https://dora.dev/guides/value-stream-management/
- GitHub Blog: Copilot Mission Control — https://github.blog/changelog/2025-10-28-a-mission-control-to-assign-steer-and-track-copilot-coding-agent-tasks/
- GitHub Blog: Copilot Coding Agent — https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/
- GitLab: Directed Acyclic Graph CI — https://about.gitlab.com/blog/directed-acyclic-graph/
- GitLab Docs: DORA Metrics — https://docs.gitlab.com/user/analytics/dora_metrics/
- Google ADK: Context Compaction — https://google.github.io/adk-docs/context/compaction/
- ImpactMapping.org — https://www.impactmapping.org/
- Inflectra: Requirements Traceability — https://www.inflectra.com/Ideas/Topic/Requirements-Traceability.aspx
- Karpathy on Context Engineering — https://pureai.com/articles/2025/09/23/karpathy-puts-context-at-the-core-of-ai-coding.aspx
- LaunchDarkly: Architecture Deep Dive — https://launchdarkly.com/docs/tutorials/ld-arch-deep-dive
- Linear: Product Intelligence — https://linear.app/changelog/2025-08-14-product-intelligence-technology-preview
- Microsoft Learn: Azure DevOps Features and Epics — https://learn.microsoft.com/en-us/azure/devops/boards/backlogs/define-features-epics
- Microsoft Research: GraphRAG — https://www.microsoft.com/en-us/research/project/graphrag/
- Nielsen Norman Group: User Story Mapping — https://www.nngroup.com/articles/user-story-mapping/
- Notion 3.0: Agents — https://www.notion.com/releases/2025-09-18
- OpenFeature — https://openfeature.dev/
- Patton: User Story Mapping — https://jpattonassociates.com/story-mapping/
- SAFe: PI Planning — https://framework.scaledagile.com/pi-planning
- ScienceDirect: Effect of information load on cognitive load of dashboards — https://www.sciencedirect.com/article/abs/pii/S0926580523002893
- ScienceDirect: Cognitive Load Theory 2024 — https://www.sciencedirect.com/article/pii/S1041608024000165
- Scrum Alliance: DoR vs DoD — https://resources.scrumalliance.org/Article/definition-vs-ready
- Serenity BDD: Living Documentation — https://serenity-bdd.github.io/docs/reporting/living_documentation

### Practitioner / Community

- Agile Analytics: Reducing Developer Cognitive Load — https://www.agileanalytics.cloud/blog/reducing-cognitive-load-the-missing-key-to-faster-development-cycles
- CardBoard: User Story Mapping Guide — https://cardboardit.com/user-story-mapping-guide/
- Cotera: Jira AI Features — https://cotera.co/articles/jira-ai-tools-guide
- Factory.ai: Evaluating Context Compression — https://factory.ai/news/evaluating-compression
- Honra.io: Progressive Disclosure for AI Agents — https://www.honra.io/articles/progressive-disclosure-for-ai-agents
- HumanLayer: Writing a Good CLAUDE.md — https://www.humanlayer.dev/blog/writing-a-good-claude-md
- LinearB: AI-Powered Iteration Summaries — https://linearb.io/blog/ai-powered-iteration-summaries
- LogRocket: The LLM Context Problem in 2026 — https://blog.logrocket.com/llm-context-problem/
- Lullabot: Cursor Rules and Memory Banks — https://www.lullabot.com/articles/supercharge-your-ai-coding-cursor-rules-and-memory-banks
- Tweag: Memory Bank System — https://tweag.github.io/agentic-coding-handbook/WORKFLOW_MEMORY_BANK/
- Zenhub: AI Sprint Planning Tools 2025 — https://www.zenhub.com/blog-posts/the-7-best-ai-assisted-sprint-planning-tools-for-agile-teams-in-2025
- Zylos Research: AI Agent Context Compression Strategies — https://zylos.ai/research/2026-02-28-ai-agent-context-compression-strategies
