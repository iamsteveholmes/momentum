---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
status: complete
inputDocuments:
  - _bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/ux-design-specification.md
  - _bmad-output/planning-artifacts/research/technical-agent-skills-deployment-research-2026-03-15.md
  - docs/research/handoff-product-brief-2026-03-14.md
  - docs/research/validate-fix-loop-handoff.md
  - docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md
  - README.md
derives_from:
  - id: PRD-MOMENTUM-001
    path: _bmad-output/planning-artifacts/prd.md
    relationship: derives_from
    description: "Momentum PRD with validated FRs, NFRs, and epics structure"
  - id: UX-MOMENTUM-001
    path: _bmad-output/planning-artifacts/ux-design-specification.md
    relationship: derives_from
    description: "Momentum UX design specification — conversational agent interface, knowledge gap UX, visual progress tracking"
  - id: BRIEF-MOMENTUM-001
    path: _bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md
    relationship: derives_from
    description: "Momentum product brief — philosophy, target users, MVP scope"
  - id: RESEARCH-SKILLS-DEPLOY-001
    path: _bmad-output/planning-artifacts/research/technical-agent-skills-deployment-research-2026-03-15.md
    relationship: derives_from
    description: "Agent Skills deployment research — skills-only model, hooks/rules/MCP deployment constraints, context:fork behavior"
  - id: HANDOFF-BRIEF-001
    path: docs/research/handoff-product-brief-2026-03-14.md
    relationship: derives_from
    description: "Research handoff — provenance system design, VFL validation framework, model routing, skills strategy"
  - id: VFL-HANDOFF-001
    path: docs/research/validate-fix-loop-handoff.md
    relationship: derives_from
    description: "Validate-fix-loop architecture — dual-reviewer system, 15-dimension taxonomy, staged validation"
workflowType: 'architecture'
project_name: 'momentum'
user_name: 'Steve'
date: '2026-03-17'
lastEdited: '2026-04-12'
editHistory:
  - date: '2026-04-12'
    changes: 'Feature-grooming spec impact (sprint-2026-04-11): Added Decision 49 (Feature Grooming Skill — flat orchestrator pattern, 2 discovery subagents, sole write authority over features.json, bootstrap/refine mode detection). Amended Decision 44 — added value_analysis (multi-paragraph required field: current value, full vision, known gaps) and system_context (required field: product fit) to features.json schema; updated write authority to momentum:feature-grooming as sole authorized writer; noted acceptance_conditions is an array of strings. Added momentum:feature-grooming ↔ momentum:feature-status integration point.'
  - date: '2026-04-11'
    changes: 'Feature-orientation epic spec impact (sprint-2026-04-11): Added Decision 44 (Feature Artifact Layer — features.json schema, feature types, orthogonality with epics). Added Decision 45 (Feature Status Skill — standalone momentum:feature-status skill, HTML+MD dual output, signal hierarchy, two rendering paths). Added Decision 46 (Feature Status Cache Pattern — startup-preflight inline hash computation, four cache states, NFR20 compliance, feature-status-hash momentum-tools command). Added Decision 47 (Sprint Summary at Retro Boundary — sprint-summary.md artifact, retro Phase 6, sprint planning Step 1 read). Added Decision 48 (Practice Project Detection — automatic path detection, ASCII skill topology, SDLC coverage table, dynamic glob discovery). Added momentum:feature-status to Skills Deployment Classification table. Added superseded note to status row (DRIFT-006). Added feature-status skill to Repository Structure tree and Requirements to Structure Mapping. Added feature-status.html and feature-status.md cache to Installed Structure. Added momentum:feature-status to Read/Write Authority table. Added sprint-summary.md to sprint folder structure. Added momentum:feature-status integration point.'
  - date: '2026-04-11'
    changes: 'Removed /momentum:create-epic and /momentum:develop-epic — superseded by momentum:create-story + momentum:epic-grooming + sprint model (developer decision 2026-04-11): updated Rolling pool feasibility note (Decision 4c) to reference /momentum:sprint-dev instead of /develop-epic; rewrote Decision 39 execution paths table — removed "Epic orchestration" row, renamed to "Execution paths in Momentum" (3 paths: sprint orchestration, quick-fix, distill); updated Decision 42 distill description from "fourth execution path alongside epic orchestration" to "third execution path alongside sprint orchestration and quick-fix"; updated distill row in Skills Deployment Classification table to match.'
  - date: '2026-04-11'
    changes: 'Drift reconciliation (DRIFT-001 through DRIFT-008): Added note to distill entry in Skills Deployment Classification that story is handled via quick-fix workflow (DRIFT-001). Added momentum:sprint-manager to Skills Deployment Classification table — flat skill wrapping momentum-tools.py CLI, sole writer of sprints/index.json (DRIFT-002). Updated Hook Infrastructure subsystem description to reflect global hook script deployment to ~/.claude/momentum/hooks/ as primary path, plugin hooks/ as override fallback, hooks-config.json path resolution (DRIFT-003). Added dev.md, dev-skills.md, dev-build.md, dev-frontend.md specialist agent files to agents/ directory listing in both Repository Structure sections (DRIFT-004). Clarified Always-Worktree section: worktree model applies to standalone momentum:dev only; sprint-dev uses sequential commit-as-sync-point within Agent Team per Decision 26 (DRIFT-005). Updated momentum:status in Skills Deployment Classification to "not planned as standalone skill" — absorbed into Impetus and momentum-tools CLI, no backlog story needed; updated Repository Structure and Requirements to Structure Mapping consistently (DRIFT-006). Removed agent logging from momentum:dev pure executor description (removed per Decision 24/27); corrected bmad-dev-story indirection note — dev/workflow.md spawns agents directly (DRIFT-007). Added momentum:agent-guidelines to Skills Deployment Classification table — 5-phase guided workflow for technology-specific guidelines generation (DRIFT-008).'
  - date: '2026-04-08'
    changes: 'Sprint-2026-04-08 spec impact: Removed agent journal write infrastructure (momentum-tools log, sprint-log writes, SubagentStart/SubagentStop hooks) per ARCH-5 — DuckDB transcript audit (Decision 27) is now the sole evidence source for retrospectives. Updated Decision 24 to historical status. Removed sprint-logs from Installed Structure tree, momentum-tools log from Read/Write Authority, sprint-logs write references from Impetus and momentum:dev rows. Removed SubagentStart/SubagentStop from Hook Infrastructure subsystem and hook event names. Updated Decision 39 per ARCH-7: momentum:dev is internal-only (not user-invocable from Impetus), quick-fix Phase 4 includes code review via momentum:code-reviewer, worktree cleanup deferred until quality gates pass. Updated Skills Deployment Classification for dev. Extended Decision 30 with spec-quality feedback loop (ARCH-9): E2E Validator findings tagged spec-quality are surfaced in dedicated retro section. Added spec quality pre-check gate to Decision 29 Step 4 (Gherkin generation). Expanded refine Read/Write Authority per ARCH-4: added assessments/*.md and decisions/*.md to reads.'
  - date: '2026-04-07'
    changes: 'Backlog refinement architecture updates: Added momentum:quick-fix to Skills Deployment Classification table (flat skill, bypass-sprint lifecycle path per Decision 39). Added momentum:research to Skills Deployment Classification table (flat skill, deep research pipeline with parallel subagents). Marked momentum:status as planned/unimplemented in Skills Deployment Classification table (not yet implemented; status display currently handled by momentum-tools CLI and Impetus greeting). Added quick-fix, research, and status entries to Repository Structure, Installed Structure tree, and Requirements to Structure Mapping table. Verified momentum:dev pure executor documentation (D2), momentum-dev-auto subsumption documentation (D3), and sprint-manager replacement by momentum-tools.py CLI (D4) — all accurate, no changes needed.'
  - date: '2026-04-07'
    changes: 'Refine skill spec impact: Updated refine row in Skills Deployment Classification table (two-wave planning artifact discovery+update, status hygiene detection, delegation to epic-grooming, stale-story triage, batch approval UX; removed dependency analysis mention). Added momentum:refine row to Read/Write Authority table (reads: prd.md, architecture.md, stories/index.json, story files; writes via subagents: prd.md, architecture.md; writes via CLI: stories/index.json; delegates: momentum:create-story, momentum:epic-grooming). Added protection boundary exception for refine wave-2 update subagents writing to prd.md and architecture.md following developer approval gate. Added momentum:refine rows to Decision 41 application table (Wave 1: prd-coverage-agent + architecture-coverage-agent, individual, parallel; Wave 2: prd-update-agent + architecture-update-agent conditional, individual, parallel). Documented refine two-wave conditional spawning pattern after Decision 41. Added developer-gated two-wave approval pattern to Process Patterns. Added momentum:refine ↔ momentum:epic-grooming to Integration Points.'
  - date: '2026-04-06'
    changes: 'Sprint-2026-04-06-2 spec impact: Added Spawn Registry Pattern to Sprint Execution Flow — in-memory (story_slug, role) deduplication guard surviving Phase 2→3→2 loops (orchestrator-deduplication-guard). Added Decision 41 — Workflow Team Composition Declarations with XML <team-composition> elements codifying required roles, spawning mode, and concurrency per phase (workflow-team-composition-spec). Noted TaskCreate/TaskUpdate enforcement via <critical> directive in Sprint Execution Flow and Sprint Planning Workflow (mandatory-task-tracking). Major rewrite of Decision 27 — Transcript Audit Retro replacing milestone-log-based retro with DuckDB preprocessing + 3-auditor team; new DuckDB dependency; transcript-query.py as standard retro tooling; retro-transcript-audit.md output (retro-workflow-rewrite). Extended Decision 29 Step 1 with master plan read, staleness check, and 3-5 recommendation synthesis before full backlog (sprint-planning-synthesis-first). Restructured Sprint Execution Flow Phase 4 with AVFL stop gate; added Phase 4b per-story code review, Phase 4c consolidated fix queue, Phase 4d selective re-review (review-orchestration-codification). Extended Decision 24 event types with subagent-start and subagent-stop; added SubagentStart/SubagentStop hooks to hooks infrastructure (agent-observability-system).'
  - date: '2026-04-06'
    changes: 'Sprint-2026-04-06 spec impact: Added priority field to stories/index.json schema (critical|high|medium|low, default low). Added priority sort note to Decision 29 Step 1 (backlog presentation sorts by priority within epic groups). Added sprint set-priority and sprint stories CLI subcommands under Sprint Planning Workflow. Added epic-grooming and refine flat skills to Skills Deployment Classification table. Extended Decision 5a with note that install/upgrade file writes refactored from Write tool to Bash (cp, python3 -c) for allowed-tools compatibility. Extended context:fork isolation constraint with note that flat orchestrator skills may declare allowed-tools in SKILL.md frontmatter, extending the pattern to the orchestrator layer.'
  - date: '2026-04-05'
    changes: 'Hook quality system spec impact: Added Session State Storage subsection (session-modified-files.txt, gate-findings.txt) under Storage & State. Extended Decision 2a with three-hook enforcement model (PreToolUse barrier, PostToolUse observability, Stop feedback gate) and protected-paths.json externalization. Updated Read/Write Authority table with session state file read/write entries for hooks. Updated Hooks row to reflect file-writing behavior. Added session state files to Installed Structure tree.'
  - date: '2026-04-04'
    changes: 'Quick-fix spec impact: Added Decision 39 (Quick-Fix Bypass-Sprint Lifecycle Path) and Decision 40 (Change-Type-Driven Validator Selection). Extended Decision 26 with specialist classification table note and momentum-tools specialist-classify. Extended Decision 35 E2E Validator scope to include quick-fix Phase 4. Added momentum-tools quickfix to Read/Write Authority table. Added cmux markdown surfaces to Integration Points.'
  - date: '2026-04-04'
    changes: 'Greeting redesign v8: Decision 4b rewritten — session orientation now uses 9 greeting states with adaptive 3-4 item menus (algorithmic construction based on sprint state + planning readiness + first-session detection). Fill bar rendering removed from session orientation. Added Decision 36 — Sprint Lifecycle State Machine (planning → ready → active → done → completed; retro as gate between done and completed; max one planned sprint). Added Decision 37 — Greeting State Detection (9 states with formal detection logic). Added Decision 38 — Narrative Voice Contract (KITT + Optimus Prime voice as binding architectural contract for all Impetus output). Sprint index schema enhanced with status and retro tracking fields. Progress indicator scope clarified: workflow-phase only, not greeting. Stats write architecture noted: invisible to user during greeting.'
  - date: '2026-04-04'
    changes: 'Decision 35 — Agent Definition Files vs SKILL.md Boundary: formalized decision framework for when to use SKILL.md (orchestrator/workflow, standalone verifier with context:fork) vs agent definition file (pure spawned worker). Added agents/ directory to plugin structure for QA reviewer and E2E validator. Applied framework to Team Review phase roles (Decision 34). Code-reviewer and architecture-guard confirmed as SKILL.md context:fork (standalone utility). AVFL sub-skills confirmed as nested SKILL.md (internal pipeline).'
  - date: '2026-04-04'
    changes: 'AVFL scan profile and hybrid resolution team: Phase 4 updated to run AVFL in scan profile (all 4 lenses, dual reviewers, max skepticism, zero fix iterations — scored findings list output only). Phase 5 updated to hybrid Agent Team model (Dev fixes AVFL findings, QA validates ACs, E2E Validator tests live behavior with external tools against Gherkin specs, Architect Guard checks pattern drift — all concurrent on main branch, fix loop within team). Decision 31 updated with forward reference to Decision 34. Added Decision 34 — AVFL Scan Profile and Hybrid Resolution Team.'
  - date: '2026-04-03'
    changes: 'Plugin model adoption: Momentum becomes a Claude Code plugin with .claude-plugin/plugin.json. Replaced skills-only flat deployment (npx skills add) with plugin packaging. Namespaced skills under momentum: prefix (momentum-avfl → momentum:avfl, momentum-dev → momentum:dev, etc.). Workflow modules (sprint-planning.md, sprint-dev.md) converted to proper skills invoked as /momentum:sprint-planning and /momentum:sprint-dev. Always-on hooks delivered via plugin hooks/hooks.json (not Impetus-written to settings.json). Rules bundled in plugin references/rules/ (Impetus still writes to ~/.claude/rules/ and .claude/rules/ on first run). Repository structure replaced with plugin root layout. Agent Teams for sprint execution: teammates load skills from project/user settings, sequential execution with commit-as-sync-point. Updated Decisions 5a, 5c, 25, 26, 29 and all deployment, naming, structural, and integration sections.'
  - date: '2026-04-02'
    changes: 'Phase 3 sprint execution architecture: replaced Epic Orchestration Architecture with Sprint Orchestration Architecture (dependency-driven teams over waves, Decision 25); added Sprint Planning Workflow (Decision 29), Sprint Execution Flow (6 phases), Two-Layer Agent Model (Decision 26); replaced momentum:sprint-manager subagent with momentum-tools.py sprint CLI throughout; added Agent Logging Infrastructure section (Decision 24); added Gherkin Specification Separation section (Decision 30); added Phase 3 Architecture Decisions (24-31); replaced Next-Story Selection Rule with Story Assignment Model; updated Read/Write Authority table (new rows for momentum-tools log, sprint-planning, sprint-dev; updated Impetus, momentum-dev, momentum-create-story rows); added sprint-logs to installed structure; added workflows/ directory to repository structure; added specs protection boundary; moved AVFL from per-story to per-sprint (Decision 31); simplified momentum-dev to pure executor (subsuming momentum-dev-auto); removed dag-executor integration section; updated session open sequence and subsystem descriptions.'
  - date: '2026-03-26'
    changes: 'Epic orchestration model: added Epic Orchestration Architecture section (lifecycle, immutability rule, DAG topology, tier-sequential execution); added Agent Pool Governance section (pool cap, AVFL embedding, merge gate, pre-flight checks); added momentum-dev-auto Design section (background-safe variant, behavioral constraints, autonomous-or-fail principle); added dag-executor Integration section (optional sub-skill, tradeoffs, decision criteria); added Retro → Triage Handoff Format section (triage-inbox.md, entry format); added done-incomplete and closed-incomplete statuses to Story State Machine; updated Decision 4c with rolling pool feasibility note (Agent tool available in skill execution context); updated Impetus session open per session-stats deferral and epic progress bar.'
  - date: '2026-03-23'
    changes: 'AVFL integration: renamed momentum-vfl to momentum-avfl throughout; renamed vfl-validator protocol type to avfl-validator; reconciled sub-skill model (AVFL uses own nested sub-skills, not momentum-code-reviewer); updated repo structure with framework.json and sub-skills directory; added AVFL deployment note distinguishing production skill from research benchmarking variants.'
  - date: '2026-03-22'
    changes: 'Added terminal-multiplexer to subsystem 10 Protocol-Based Integration; added Terminal Multiplexer ↔ Workflows integration point with detect-and-adapt pattern. Derives from CMUX research document.'
---

# Architecture Decision Document: Momentum

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements (10 subsystems):**

Momentum's FRs organize into 10 architectural subsystems:

1. **Deployment Packaging** — Claude Code plugin with `.claude-plugin/plugin.json` manifest (`name: "momentum"`). Skills are namespaced under `momentum:` (e.g., `/momentum:impetus`, `/momentum:avfl`, `/momentum:dev`). Plugin root contains `skills/` (all SKILL.md files), `hooks/hooks.json` (always-on hooks delivered by the plugin), `scripts/` (CLI tools), and `references/` (rules, practice docs, version manifest). Flat skills run in main context; `context: fork` skills run in isolated subagent contexts for pure verifiers. Rules are bundled in `references/rules/` and written by Impetus to `~/.claude/rules/` and `.claude/rules/` on first `/momentum:impetus` invocation (the plugin cannot write there directly). Momentum is a Claude Code plugin — hooks, `context:fork`, Agent Teams, and model routing are all Claude Code features.

2. **Provenance Infrastructure** — `derives_from` frontmatter (downstream-only authoring), content hash staleness detection, suspect link flagging (pull-based), auto-generated `referenced_by`, Chain of Evidences prompting, Citations API integration for mechanical grounding.

3. **Hook Infrastructure (Tier 1 Deterministic)** — PostToolUse auto-lint/format, PreToolUse acceptance test directory protection, PreToolUse file protection, PreToolUse git-commit quality gate, PreToolUse plan audit gate (ExitPlanMode), Stop conditional quality gate. Two hook deployment mechanisms: (1) **Always-on hooks** — defined in `hooks/hooks.json` at the plugin root; delivered automatically by the plugin install mechanism; these fire on every matching tool event in every session regardless of which skill is active. Hook scripts are distributed globally to `~/.claude/momentum/hooks/` as the primary path; the plugin's `hooks/` directory serves as an override fallback for project-local scripts. The `hooks-config.json` in `references/` defines the path resolution logic — global scripts are preferred, with project-local scripts taking precedence when both exist. (2) **Skill-lifecycle hooks** — defined in SKILL.md `hooks:` frontmatter; scoped to the skill's lifetime; only fire while that skill is active; automatically cleaned up when the skill completes. Complemented by standard git hooks (Husky/pre-commit framework) at the repository level.

4. **Rules Architecture (Tier 3 Advisory)** — Global `~/.claude/rules/` (authority hierarchy, anti-patterns, model routing) + project `.claude/rules/` (architecture conventions, stack-specific standards). Project-scoped rules auto-load in every session including subagents. Rules are bundled in `references/rules/` at the plugin root. The plugin install mechanism does not write to `~/.claude/rules/` or `.claude/rules/` directly — Impetus writes rules to both targets on first `/momentum:impetus` invocation using the Write tool. No separate setup step.

5. **Subagent Composition** — code-reviewer (read-only tools, pure verifier, never modifies code), architecture-guard (pattern drift detection), momentum:dev (story executor, spawned by sprint-dev skill). code-reviewer and architecture-guard use `context: fork` for producer-verifier isolation. momentum:dev runs as a flat subagent (main context) for story execution. Two-layer agent model (Decision 26): Momentum provides generic roles (Dev, QA, E2E Validator, Architect Guard); projects provide role-specific stack guidelines wired together during sprint planning. Agent Teams share a working directory with commit-as-sync-point. Hub-and-spoke: Impetus is the sole user-facing voice; subagents return structured output to Impetus for synthesis. Subagents cannot spawn subagents — chains route through main conversation.

6. **Validate-Fix Loop (VFL) Skill** — Three profiles: Gate (1 agent, pass/fail), Checkpoint (2-4 agents, 1 fix attempt), Full (dual-reviewer per lens, up to 4 fix iterations). Four lenses: Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness. Consolidation handles deduplication, cross-check confidence tagging, and scoring. Invocable standalone, inline from workflows, or declared as a rule.

7. **Orchestrating Agent — Impetus** — Session orientation via 9-state greeting (Decision 37) with adaptive menus, visual progress (✓ Built / → Now / ◦ Next) for workflow phases, proactive gap detection, productive waiting during subagent execution, hub-and-spoke voice unification, narrative voice contract (Decision 38). Impetus is the primary entry-point skill (`/momentum:impetus`) and the recommended path for all Momentum operations. Users can invoke other namespaced skills directly (e.g., `/momentum:sprint-planning`), but Impetus provides session orientation and context that direct invocation skips. For sprint-scoped operations, Impetus dispatches to dedicated skills: `/momentum:sprint-planning` for story selection and team composition, `/momentum:sprint-dev` for dependency-driven execution. Sub-command dispatch: developer selects from the greeting menu (e.g., "Continue the sprint", "Run retro", "Plan a sprint"), and Impetus invokes the corresponding skill. Sprint lifecycle transitions follow Decision 36 state machine. Impetus is the force that maintains practice velocity — the system keeps compounding because Impetus carries knowledge and context forward across sessions and sprints without requiring repeated external input.

8. **Findings Ledger + Evaluation Flywheel** — Structured findings with provenance_status field; cross-story pattern detection; flywheel workflow (Detection → Review → Upstream Trace → Solution → Verify → Log) with visual status graphics; `/upstream-fix` skill; retrospective integration.

9. **Model Routing** — `model:` and `effort:` frontmatter required on every SKILL.md and agent definition. Cognitive hazard rule: flagship models for outputs without automated validation. Escalation semantics in VFL: mid-tier first, flagship if not converging within 3-4 iterations.

10. **Protocol-Based Integration** — Every integration point (validation, research, review, tools, documents, terminal multiplexers) defines an interface before implementation is wired. Implementations are substitutable: swap the ATDD framework, the research model, the terminal multiplexer, the validation profile — the practice layer is unchanged.

---

### Non-Functional Requirements

- **Claude Code plugin** — Momentum is a Claude Code plugin. Hooks, `context:fork`, Agent Teams, and model routing are Claude Code features. The plugin model makes explicit what was already true: Momentum is Claude Code-specific.
- **Context budget** — Agent Skills three-stage loading (description at startup ~100 tokens, full SKILL.md on invocation, references/ on demand) means startup overhead is manageable with good authoring discipline. Concise descriptions, heavy content in references/. Hygiene note, not a hard constraint.
- **Evolvability (Impermanence Principle)** — Thin plugin packaging layer. Practice content portable even if the plugin ecosystem changes. Monthly ecosystem review. Interfaces before implementations everywhere.
- **Solo developer efficiency** — One person, limited hours, concurrent with other projects. MVP deploys in days. Real work on real projects is the test harness.
- **Cost as managed dimension** — `model:` + `effort:` frontmatter on every skill. Cognitive hazard rule universal. VFL max 4 iterations (context accumulation makes later iterations progressively more expensive).
- **Terminal-native UX** — No web UI. ASCII/text visual progress. Structured markdown artifacts. Everything works beautifully in a terminal environment.

---

### Scale & Complexity

- **Primary domain:** Developer tooling / practice framework
- **Complexity:** Medium — no regulatory compliance; complexity from multi-tool portability, evolving ecosystem dependencies, and the meta-nature of a practice that governs practices using its own practice
- **Estimated architectural components:** 10 subsystems + 3 cross-cutting concerns = 13 total components
- **Dogfooding as validation:** Momentum is built using its own practice. The system's first test case is itself.

---

### Technical Constraints & Dependencies
<!-- REVISED 2026-04-03: Plugin model adopted. Momentum is a Claude Code plugin with .claude-plugin/plugin.json. -->

- **Claude Code plugin model** — Momentum is packaged as a Claude Code plugin with `.claude-plugin/plugin.json` manifest. Plugin install delivers all skills, hooks, scripts, and references. Skills are namespaced under `momentum:` (e.g., `/momentum:impetus`, `/momentum:avfl`).
- **Subagents cannot spawn subagents** — VFL orchestration chains through main conversation; affects Full-profile parallel execution design
- **context:fork isolation** — `context: fork` is a SKILL.md frontmatter field, Claude Code-exclusive. Skills with `context: fork` run in isolated subagent contexts without access to conversation history. code-reviewer and architecture-guard are implemented as `context: fork` SKILL.md files. The `allowed-tools` frontmatter field restricts tool access (e.g., `Read` only for pure verifiers). Flat orchestrator skills (e.g., Impetus) may also declare `allowed-tools` in SKILL.md frontmatter to enforce deterministic read-only behavior; this extends the `allowed-tools` pattern from `context:fork` verifier skills to the orchestrator layer (sprint-2026-04-06).
- **Plugin-delivered vs. Impetus-written** — The plugin install delivers SKILL.md files, `hooks/hooks.json` (always-on hooks), `scripts/`, and `references/`. It cannot write to `~/.claude/rules/` or `.claude/rules/`. Rules are bundled in `references/rules/` and written by Impetus on first `/momentum:impetus` invocation. Install/upgrade logic is governed by `references/momentum-versions.json` and `installed.json` (Decision 5c). The UX interaction for install/upgrade is defined in the UX specification.
- **Hooks: two deployment paths** — Always-on hooks (fire every session regardless of skill) are defined in `hooks/hooks.json` at the plugin root, delivered automatically by plugin install. Skill-lifecycle hooks (fire only while a specific skill is active) are defined in SKILL.md `hooks:` frontmatter and require no separate deployment — they travel with the skill. Both are Claude Code features.

---

### BMAD as Practice Substrate

BMAD is not a coexistence challenge — it is Momentum's practice substrate. BMAD provides proven workflow scaffolding (analyst, PM, architect, dev-story, code-review workflows). Momentum is the quality governance layer that makes BMAD workflows momentous:

- **Provenance wrapping** — `derives_from` frontmatter auto-populated on BMAD-generated artifacts; staleness detection fires when upstream docs change
- **VFL validation at BMAD completion gates** — BMAD workflow completes → Impetus fires a checkpoint or full validate-fix loop before the artifact is accepted
- **Commit hooks at workflow boundaries** — BMAD step completes → git commit proposed per git-discipline rules
- **Model routing inheritance** — Momentum's `model:` + `effort:` rules apply to BMAD-invoked skills via rules auto-loading
- **Knowledge dispensation** — Momentum's rules auto-load context BMAD skills don't carry natively (authority hierarchy, anti-patterns, architecture decisions)
- **Optimized subagent replacement** — Momentum's code-reviewer and architecture-guard can supersede or augment BMAD's built-in review steps

The vision: a developer running BMAD workflows gets Momentum's quality layer for free — provenance, enforcement, flywheel — without needing to change how they work.

---

### Cross-Cutting Concerns

1. **Provenance** — Every artifact, every agent output, every specification claim carries derives_from and provenance_status. Affects all 10 subsystems.
2. **Enforcement tier assignment** — Every mechanism has a tier designation. Nothing floats undefined.
3. **Producer-verifier separation** — `context: fork` isolation on all review steps. The producing context never reviews its own output. Each reviewer invocation = one isolated subagent; VFL spawns N reviewers via N Agent tool calls.
4. **Model routing** — model: and effort: frontmatter required on every SKILL.md and agent definition. Cognitive hazard rule applies universally.
5. **Visual progress** — ✓ Built / → Now / ◦ Next at every phase transition across all orchestrated workflows.
6. **Protocol interfaces** — Every integration point defines an interface before any implementation is wired.

---

## Deployment Structure
<!-- REVISED 2026-04-03: Momentum adopts the Claude Code plugin model. .claude-plugin/plugin.json manifest, namespaced skills, hooks/hooks.json for always-on hooks. -->

> _[Changed 2026-03-18: Removed two-unit plugin + skills model. Adopted skills-only deployment via `npx skills add`.]_
> _[Changed 2026-04-03: Adopted Claude Code plugin model. Momentum is packaged as a plugin with `.claude-plugin/plugin.json`. Skills namespaced under `momentum:`. Always-on hooks delivered via `hooks/hooks.json` at plugin root. Workflow modules (sprint-planning, sprint-dev) converted to proper skills. Reason: Momentum already depends entirely on Claude Code features (hooks, context:fork, Agent Teams, model routing) — the plugin model makes this explicit.]_

### Skills Deployment Classification

The defining question for each component: *does this need main-context persona persistence, or does it benefit from isolation?*

| Component | Deployment | Rationale |
|---|---|---|
| Impetus (orchestrating agent) | Flat skill (`/momentum:impetus`) | Must persist persona across interactions; primary entry point |
| Sprint planning | Flat skill (`/momentum:sprint-planning`) | Multi-step workflow needing main context; invoked by Impetus or directly |
| Sprint dev | Flat skill (`/momentum:sprint-dev`) | Dependency-driven execution needing main context; invoked by Impetus or directly |
| AVFL | Flat skill (`/momentum:avfl`) | Must orchestrate parallel spawning from main context |
| upstream-fix, create-story, retro, plan-audit | Flat skills | Stateful workflows needing main context |
| dev | Flat skill (`/momentum:dev`) — internal-only | Pure story executor; called by sprint-dev and quick-fix, not user-invocable from Impetus (Decision 39) |
| quick-fix | Flat skill (`/momentum:quick-fix`) | Single-story bypass-sprint lifecycle path (Decision 39); register, execute, validate, complete in one session |
| research | Flat skill (`/momentum:research`) | Deep research pipeline with parallel subagents, Gemini CLI triangulation, AVFL corpus validation, and provenance tracking |
| epic-grooming | Flat skill (`/momentum:epic-grooming`) | Reads stories/PRD/architecture/epics.md, proposes taxonomy changes, reassigns stories via momentum-tools |
| refine | Flat skill (`/momentum:refine`) | Backlog refinement: two-wave planning artifact discovery and update (Wave 1 discovers PRD + architecture coverage gaps in parallel; Wave 2 conditionally spawns update agents per developer approval), status hygiene detection, delegation to epic-grooming, stale-story triage, batch approval UX; CLI-only mutations |
| intake | Flat skill (`/momentum:intake`) | User-invokable; **single-item capture only** — one idea → one story stub, feature-slug and story-type aware per DEC-005 D1/D5. No batching (that is `momentum:triage`'s job). Writes `stories/{slug}.md` + `stories/index.json` entry via `momentum-tools sprint story-add`. |
| triage | Flat skill (`/momentum:triage`) | Orchestrator; `model: claude-sonnet-4-6`, `effort: high`. Multi-item batch classification of observations into six classes (ARTIFACT / DISTILL / DECISION / SHAPING / DEFER / REJECT) per DEC-007. Delegates ARTIFACT → `momentum:intake`, DISTILL → `momentum:distill`, DECISION → `momentum:decision`; writes SHAPING / DEFER / REJECT inline to `intake-queue.jsonl` via `momentum-tools` CLI. Classification inline in main context (no subagent); optional Explore subagents for duplicate detection and feature-assignment suggestion when N ≥ 5. Performs no gap-check (DEC-005 D10). Entry point replaces the Impetus `[3] Triage` placeholder. |
| feature-breakdown | Flat skill (`/momentum:feature-breakdown`) | Pure orchestrator; takes a feature slug as input, enumerates story gaps end-to-end, passes pre-enumerated candidate list to `momentum:triage` with `source_label = "feature-breakdown:{feature_slug}"`. NEVER writes to features.json or stories/index.json — all classification and write authority belongs to triage (Decision 50). |
| distill | Flat skill (`/momentum:distill`) | Practice-artifact distillation: session learning or retro finding → 2-agent discovery (Enumerator + Adversary) → classify fix scope → apply to artifact → scoped AVFL validation. User-invokable mid-session or from retro Phase 5 for Tier 1 findings. Third execution path alongside sprint orchestration and quick-fix (Decision 42). Story: not yet in backlog — handled via quick-fix workflow. |
| assessment | Flat skill (`/momentum:assessment`) | User-invokable; evaluates a story or backlog item for readiness, risk, and completeness; no fork needed |
| sprint-manager | Flat skill (`/momentum:sprint-manager`) | Wraps momentum-tools.py CLI; provides /momentum:sprint-manager command for sprint lifecycle management (activate, close, status); sole writer of sprints/index.json in conjunction with momentum-tools CLI. |
| decision | Flat skill (`/momentum:decision`) | User-invokable; facilitates architectural or product decision capture (ADR/trade-off analysis); no fork needed |
| agent-guidelines | Flat skill (`/momentum:agent-guidelines`) | 5-phase guided workflow for generating technology-specific development guidelines for a project: Discover (stack analysis), Research (web search), Consult (developer preferences), Generate (guidelines documents), Validate (AVFL checkpoint). Generates path-scoped rules and reference documents. |
| feature-status | Flat skill (`/momentum:feature-status`) | Reads features.json + stories/index.json; writes self-contained HTML dashboard (`.claude/momentum/feature-status.html`) and YAML-frontmatter cache (`.claude/momentum/feature-status.md`). Two rendering paths: product (flow/connection/quality tables + gap analysis) and practice (skill topology + SDLC coverage). Supersedes DRIFT-006 proposal to absorb into Impetus/momentum-tools — standalone skill per Decision 45. |
| status | Not planned as standalone skill | ~~Status functionality is absorbed into Impetus greeting workflow and momentum-tools CLI (`momentum-tools sprint status`). No backlog story exists or is needed.~~ **Superseded by Decision 45 (sprint-2026-04-11):** feature-status is implemented as a dedicated standalone skill (`/momentum:feature-status`). The startup-preflight cache check (Decision 46) handles the Impetus greeting integration path. The momentum-tools `feature-status-hash` command provides the hash utility. This row is retained for historical context only. |
| code-reviewer | `context: fork` skill | Pure verifier — `context: fork` provides isolation; `allowed-tools: Read` enforces read-only. Also useful standalone (Decision 35). |
| architecture-guard | `context: fork` skill | Pattern analysis — isolation prevents drift; `allowed-tools: Read` enforces read-only. Also useful standalone (Decision 35). |
| QA reviewer | Agent definition file (`agents/qa-reviewer.md`) | Pure spawned worker — reviews code against story ACs during Team Review (Decision 34). Never user-invoked (Decision 35). |
| E2E Validator | Agent definition file (`agents/e2e-validator.md`) | Pure spawned worker — tests running behavior against Gherkin specs during Team Review (Decision 34). Never user-invoked (Decision 35). |
| Always-on hooks | `hooks/hooks.json` (plugin root) | Delivered by plugin install; fire every session regardless of active skill |
| Global rules | `~/.claude/rules/` | Bundled in `references/rules/` at plugin root; Impetus writes on first run |
| Project rules | `.claude/rules/` | Bundled in `references/rules/` at plugin root; Impetus writes on first run |
| MCP config | `.mcp.json` | Deferred to Epic 6 — no MCP servers configured at 1.0.0. When available, Impetus writes on run. |

### Repository Structure (preview — full structure in Project Structure section)

```
momentum/                              ← Plugin root
├── .claude-plugin/
│   └── plugin.json                   ← { "name": "momentum" }
├── skills/                           ← All skills: flat + context:fork
│   ├── impetus/SKILL.md             ← Orchestrator (/momentum:impetus)
│   ├── sprint-planning/SKILL.md     ← /momentum:sprint-planning
│   ├── sprint-dev/SKILL.md          ← /momentum:sprint-dev
│   ├── dev/SKILL.md                 ← /momentum:dev
│   ├── avfl/SKILL.md               ← + sub-skills/ and references/
│   ├── code-reviewer/SKILL.md      ← context: fork, allowed-tools: Read (Decision 35)
│   ├── architecture-guard/SKILL.md  ← context: fork, allowed-tools: Read (Decision 35)
│   ├── upstream-fix/SKILL.md
│   ├── create-story/SKILL.md
│   ├── plan-audit/SKILL.md
│   ├── quick-fix/SKILL.md          ← /momentum:quick-fix (Decision 39)
│   ├── research/SKILL.md           ← /momentum:research
│   ├── status/SKILL.md             ← /momentum:status (not planned as standalone skill — absorbed into Impetus and momentum-tools CLI)
│   ├── intake/SKILL.md             ← /momentum:intake
│   ├── assessment/SKILL.md         ← /momentum:assessment
│   ├── decision/SKILL.md           ← /momentum:decision
│   └── retro/SKILL.md
├── agents/                           ← Agent definition files (Decision 35)
│   ├── qa-reviewer.md               ← Pure worker: story AC review (Team Review)
│   ├── e2e-validator.md             ← Pure worker: behavioral validation (Team Review)
│   ├── dev.md                        ← Base dev agent for sprint-dev spawning
│   ├── dev-skills.md                ← Specialist: SKILL.md, workflow.md, agent definitions
│   ├── dev-build.md                 ← Specialist: Gradle and build system work
│   └── dev-frontend.md              ← Specialist: Kotlin Compose and frontend UI work
├── hooks/
│   └── hooks.json                    ← Always-on hooks (Tier 1 enforcement)
├── scripts/
│   └── momentum-tools.py
└── references/
    ├── rules/                        ← Bundled rules (written to ~/.claude/rules/ by Impetus)
    ├── practice-overview.md
    ├── phase-guide.md
    └── momentum-versions.json
```

### Install Experience
<!-- REVISED 2026-04-03: Plugin install replaces npx skills add. -->

> _[Changed 2026-04-03: Install via Claude Code plugin mechanism. Plugin install delivers all skills, hooks, scripts, and references. Impetus handles first-run setup for runtime state (journal, installed.json) and writes rules to ~/.claude/rules/ and .claude/rules/.]_

```bash
# Install Momentum plugin into Claude Code
claude plugin add momentum

# Primary entry point — session orientation, menu dispatch, first-run setup:
/momentum:impetus
```

Plugin install delivers all SKILL.md files (namespaced under `momentum:`), `hooks/hooks.json` (always-on hooks active immediately), `scripts/`, and `references/`. Rules cannot be written directly by the plugin install — Impetus writes rules to `~/.claude/rules/` and `.claude/rules/` on first `/momentum:impetus` invocation. No `momentum setup` command. No `momentum bootstrap` command.

Impetus handles install and upgrade via the manifest mechanism (Decision 5c). What triggers install vs. upgrade checks, and how the user experience unfolds, is defined in the UX specification — not here. The architectural guarantee: `/momentum:impetus` is the recommended interface; all setup and upgrade paths flow through it. Users can invoke individual skills directly (e.g., `/momentum:sprint-planning`) but skip session orientation when doing so.

### Plugin Manifest

Momentum is a Claude Code plugin. The plugin manifest lives at `.claude-plugin/plugin.json` in the plugin root:

```json
{
  "name": "momentum"
}
```

The `name` field determines the namespace prefix for all skills. With `"name": "momentum"`, a skill directory `skills/impetus/` becomes invocable as `/momentum:impetus`. Claude Code discovers the plugin through the `.claude-plugin/` directory and registers all skills, hooks, and scripts.

**Plugin root layout:**

| Directory | Purpose | Delivered by |
|---|---|---|
| `.claude-plugin/` | Plugin manifest | Plugin install |
| `skills/` | All SKILL.md files (flat + context:fork) | Plugin install |
| `hooks/` | Always-on hook definitions (`hooks.json`) | Plugin install |
| `scripts/` | CLI tools (`momentum-tools.py`) | Plugin install |
| `references/` | Rules, practice docs, version manifest | Plugin install |
| `agents/` | Custom agent definitions for teams | Plugin install |
| `mcp/` | Custom MCP server source (Epic 6) | Plugin install |

Hooks in `hooks/hooks.json` are active immediately after plugin install — no Impetus invocation required. Rules in `references/rules/` require Impetus to write them to `~/.claude/rules/` and `.claude/rules/` because the plugin cannot write outside its own directory.

### Agent Teams and Skill Loading

Sprint execution uses Claude Code Agent Teams. Teams share a working directory and execute stories sequentially with commit-as-sync-point — no worktree needed within a team.

**Skill loading model:** Teammates do NOT load skills from `.agent.md` `skills` frontmatter. Instead, teammates load skills from project and user settings (the standard Claude Code skill loading path). The dev agent receives workflow instructions through its spawn prompt, which includes the story file path and role-specific guidelines from the sprint record's team composition.

**Commit-as-sync-point:** Within a team, stories execute sequentially. Each story completes with a git commit before the next begins. The commit is the synchronization boundary — the next story sees the previous story's changes via the committed state of the working directory. This eliminates the need for worktrees within team execution while maintaining isolation between story implementations.

**Team composition:** Defined during sprint planning (`/momentum:sprint-planning`) and stored in the sprint record. Each story maps to one or more roles (Dev, QA, E2E Validator, Architect Guard). Each role carries project-specific guidelines. The sprint-dev skill (`/momentum:sprint-dev`) reads the team composition and spawns agents with the appropriate role, guidelines, and story assignment.

### Version Management

> _[Changed 2026-03-18: Removed plugin-skills sync requirement. Single version source covers all skills.]_

All skills share a single `version.md` at repo root. A standard git pre-commit hook (Husky/pre-commit framework — not a Claude Code hook) validates SKILL.md frontmatter consistency. Release tags version all skills together.

---

## Core Architectural Decisions

### Storage & State Architecture

**Decision 1a — Provenance Graph: Pure YAML Frontmatter**
- Each document carries its own `derives_from` in frontmatter (downstream-only authoring)
- `referenced_by` is computed on demand by a provenance scanner — never manually maintained
- Content hashes use git blob SHAs (`git hash-object <file>`) — zero extra tooling
- Staleness detection: compare stored hash in `derives_from` against current `git hash-object`
- One-hop propagation only; human/Impetus-gated at each level

**Decision 1b — Session Journal: JSONL with Markdown View**
- Location: `.claude/momentum/journal.jsonl`
- Format: JSONL — one JSON object per line, append-only. Each write appends a new state entry for a thread.
- Current state of a thread = last entry in the file with that `thread_id`
- Auto-generated `.claude/momentum/journal-view.md` for human readability (regenerated after every append)
- Tracks: active story, current phase, last completed action, open threads
- Rationale (concurrency safety): same argument as Decision 1c — multiple Claude Code sessions can safely append concurrently without file locking. POSIX atomic append for lines under pipe buffer size. JSON read-modify-write is racy under multi-tab access (lost writes, corruption on crash, torn reads).
- Rationale (query patterns): current-state reconstruction (read all lines, group by `thread_id`, take last entry) is a one-time cost at session start — not a hot path. `journal-view.md` provides the pre-built snapshot for human consumption.
- Rationale (implementation complexity): append-only is simpler than read-parse-modify-serialize-write. No file locking logic required in instruction-based workflows.
- Rationale (human readability): raw JSONL is less readable than JSON, but `journal-view.md` auto-generation already provides the human-readable layer.
- Evaluated in Story 1.9.

**Decision 1c — Findings Ledger: JSONL (Global)**
- Location: `~/.claude/momentum/findings-ledger.jsonl` (global, not per-project)
- Format: JSONL — one JSON object per line, append-only. No wrapping array.
- Structured findings with fields: `id` (globally unique, format `F-{unix_ms}-{random_4hex}`), `project` (string, project identifier), `story_ref`, `phase`, `severity`, `pattern_tags`, `description`, `evidence`, `provenance_status`, `upstream_fix_applied`, `upstream_fix_level`, `upstream_fix_ref` (reference to the fix artifact), `timestamp` (ISO 8601 when finding was recorded)
- `upstream_fix_level` — null until a fix is applied; then one of: `spec-generating-workflow | specification | rules-or-CLAUDE.md | tooling | one-off-code-fix`
- Queryable for cross-project and cross-story pattern detection
- JSONL enables concurrent append from multiple Claude Code sessions without file locking (POSIX atomic append for lines under pipe buffer size)
- Authorized writers: flywheel workflow (`origin: flywheel`) and `momentum:distill` (`origin: distill`). The `origin` field distinguishes code-review-origin findings from practice-distillation-origin findings for FR33 ratio tracking. All other components are read-only.
- Rationale: Global scope enables cross-project pattern detection — the same anti-pattern appearing in projects A and B becomes visible. Per-project scope would miss these systemic patterns.

**Decision 1e — Session State Storage (Ephemeral + Inter-Session)**
- `.claude/momentum/session-modified-files.txt` — Ephemeral session-scoped file. Written by PostToolUse lint hook (appends file paths of modified files, one per line, deduped). Read by Stop gate hook as the set of files to check. Cleaned up after the Stop gate runs. Not committed to git.
- `.claude/momentum/gate-findings.txt` — Inter-session findings file. Written by the Stop gate hook when it detects lint issues or uncommitted changes among session-modified files. Read by Impetus at the next session open to surface unresolved quality issues from the previous session. Overwritten each time the Stop gate runs (not append-only).

**Decision 1f — Feature Status Cache: YAML-Frontmatter MD**
- Location: `.claude/momentum/feature-status.md`
- Written by `momentum:feature-status` after generating the HTML dashboard
- YAML frontmatter fields: `input_hash` (SHA-256 of features_content + ":" + stories_content), `summary` (one-line feature status string, e.g., "3/5 features working, 1 partial, 1 not-started"), `generated_at` (ISO 8601)
- Cache validity states (four): `no-features` (features.json absent — skip silently), `no-cache` (cache file absent — prompt feature-status run), `fresh` (input_hash matches current hash — display cached summary), `stale` (hash mismatch — offer feature-status refresh)
- Hash computation: inline Python in startup-preflight, not a subprocess. Maintains NFR20 compliance (startup-preflight remains one Bash call).
- Cache is read by Impetus at session start inside startup-preflight to surface feature health alongside sprint state
- See Decision 46 for full startup-preflight integration architecture

**Decision 1d — Installed State: JSON**
- Location: `.claude/momentum/installed.json`
- Written by Impetus on first install; updated on each upgrade
- Tracks: `momentum_version` at last install/upgrade, per-component version + hash
- Impetus reads this at session start to detect version drift (see Decision 5c for full schema)

---

### Security & Integrity

**Decision 2a — File Protection & Quality Enforcement (Three-Hook System)**

Enforcement is implemented as a three-hook quality system, each hook serving a distinct role:

| Hook | Role | Behavior |
|---|---|---|
| PreToolUse | Enforcement barrier | Blocks writes to protected paths — hard stop, no override |
| PostToolUse | Observability layer | Tracks modified files to `session-modified-files.txt`, lints them on write |
| Stop | Feedback gate | Conditional checks on session-modified files (lint clean, committed), writes advisory findings to `gate-findings.txt` for next session |

**Protected path targets (PreToolUse blocks writes to):**

| Protected Path | Rationale |
|---|---|
| `tests/acceptance/` and `**/*.feature` | Acceptance tests are immutable — agents never modify to make code pass |
| `_bmad-output/planning-artifacts/*.md` | Spec authority — coding agents read, never write |
| `.claude/rules/` | Global enforcement rules — protected from coding agent modification |
| `~/.claude/momentum/findings-ledger.jsonl` | Ledger integrity — authorized writers: flywheel workflow and `momentum:distill` only (Decision 1c). Note: global path is outside project PreToolUse scope; protection enforced by authority rule. |

Protected paths are externalized to `skills/momentum/references/protected-paths.json` for declarative management — the PreToolUse hook reads this file at invocation rather than hardcoding paths in the hook script. This enables project-specific path additions without hook modification.

**Decision 2b — Provenance Integrity Rules (Tier 3, promotable to Tier 1)**
- Agents may not remove or modify `derives_from` frontmatter in spec files
- Every significant claim classified as SOURCED / DERIVED / ADDED / UNGROUNDED
- Violations tracked in findings ledger; repeated violations trigger hook promotion
- **Note:** `UNGROUNDED` here refers to content origin (no source was provided). This is distinct from FR16's epistemic trust vocabulary, which also uses `UNGROUNDED` to mean "based on training data with no grounding in provided sources." In implementation, use `content_origin` for Decision 2b values and `provenance_status` for FR16 values to avoid field-name collision.

---

### Agent Communication & Orchestration

**Decision 3a — VFL Parallel Execution: Main Context Orchestration**

The main conversation CAN spawn multiple subagents simultaneously (confirmed: official Claude Code docs explicitly document parallel subagent spawning as a supported pattern). The constraint is only that subagents cannot spawn further subagents.

Architecture:
- **AVFL runs as a flat skill** (main context, not context:fork) — orchestration needs main context to spawn agents
- **Impetus invokes AVFL** from main conversation
- **AVFL uses its own nested sub-skills** for multi-lens artifact validation — these are DISTINCT from `/momentum:code-reviewer`. Sub-skills are nested inside `skills/avfl/sub-skills/` and deploy automatically with the parent skill. The sub-skill pipeline was developed through 6-phase research (36 runs across 3 models x 3 effort levels) with benchmarked optimal model/effort configurations per role:
  - **validator-enum** (Enumerator) — sonnet/medium: systematic dimension-by-dimension enumeration
  - **validator-adv** (Adversary) — opus/high: failure-focused adversarial validation
  - **consolidator** — haiku/low: deduplication, cross-check confidence tagging, scoring (fully invariant across models — cheapest sufficient)
  - **fixer** — sonnet/medium: targeted artifact repair based on consolidated findings
- **Consolidation and fixing run as sub-skill agents** (not in AVFL main context) because they need specific model routing: haiku for consolidator, sonnet for fixer
- **`/momentum:code-reviewer`** (Epic 4 Story 4.1) is a separate skill for adversarial code review of implementation artifacts — it is NOT used by AVFL. AVFL sub-skills are for multi-lens artifact validation with specific model routing per role.
- **AVFL spawns validators in parallel** — up to 8 simultaneous subagents for Full profile (2 per lens x 4 lenses)
- **AVFL consolidates results** via the consolidator sub-skill after all validators complete
- Context window consideration: all validator results return to main context; keep validator output structured and bounded
- **Execution mode:** validator subagents run as **background agents** (non-blocking — main conversation continues); automated hook-triggered passes may use foreground (blocking) where dead air is acceptable. Background execution is what enables productive waiting (Decision 4c).
- **Validator output bound:** Validators return structured JSON (not free-form prose). AVFL framework (framework.json) specifies per-validator output schema. Impetus enforces this to keep context accumulation bounded across all validator results.
- **Implementation note:** Background agent execution model is validated in Story 2.Spike (Epic 2) before Stories 2.4 and 4.3 begin. Do not implement productive waiting or background AVFL execution until spike result is documented. The execution mode is adopted as the architectural intent; the spike validates the specific implementation mechanism (inter-agent communication + checkpoint/resume). If the spike reveals the mechanism is unavailable, Decision 3a/4c will be revised before Stories 2.4 and 4.3 begin.

**context:fork agent count — explicit model:**

> _[Added 2026-03-18: Clarifying how multiple agents are actually created. `context: fork` = one agent per invocation.]_

`context: fork` creates **exactly one** isolated subagent per invocation. Multiple parallel agents = multiple Agent tool calls. AVFL's parallel execution works as follows:

- AVFL (flat skill, main context) issues **N separate Agent tool calls**, each with `run_in_background: true`
- Each call spawns one isolated subagent running an AVFL sub-skill (validator-enum or validator-adv) with lens criteria passed via `$ARGUMENTS`
- **Full profile agent count:** 8 Agent tool calls = 8 concurrent validator agents (2 per lens x 4 lenses: Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness) — one enumerator + one adversary per lens
- **Checkpoint profile:** 2–4 Agent tool calls (1–2 lenses, 1 validator each)
- **Gate profile:** 1 Agent tool call
- After validators complete: 1 consolidator sub-skill call (haiku/low), then 0–4 fixer sub-skill calls (sonnet/medium) depending on findings

architecture-guard is a **separate** skill, invoked independently by Impetus (not inside AVFL). It is one additional Agent tool call when pattern drift checking is needed — not part of the AVFL validator count.

`/momentum:code-reviewer` is also a **separate** skill (Epic 4 Story 4.1), invoked independently for adversarial code review of implementation artifacts — not part of the AVFL pipeline.

Invocation flow for Full AVFL:
```
AVFL (flat, main context)
├── Agent tool call 1 → validator-enum [structural] (background)
├── Agent tool call 2 → validator-adv [structural] (background)
├── Agent tool call 3 → validator-enum [factual] (background)
├── Agent tool call 4 → validator-adv [factual] (background)
├── Agent tool call 5 → validator-enum [coherence] (background)
├── Agent tool call 6 → validator-adv [coherence] (background)
├── Agent tool call 7 → validator-enum [domain] (background)
└── Agent tool call 8 → validator-adv [domain] (background)
     ↓ (all complete)
├── Agent tool call 9 → consolidator (deduplicate, cross-check, score)
     ↓ (consolidated findings)
└── Agent tool call 10..N → fixer (targeted repairs, up to 4 iterations)
     ↓ (all complete)
AVFL returns validated artifact + findings report → Impetus
```

**AVFL Deployment Note:**

The benchmarked AVFL pipeline (developed via 6-phase research in `avfl-workspace/`) is deployed as `/momentum:avfl` with 4 production sub-skills at their benchmarked optimal model/effort configurations. The `avfl-*` skills that remain in `.claude/skills/` are research/benchmarking tools (gitignored, not deployed with Momentum). The 13 benchmark variants (2lens, 3lens, declining, composition variants, effort variants) are not deployed — only the 4 production sub-skills: validator-enum (sonnet/medium), validator-adv (opus/high), consolidator (haiku/low), and fixer (sonnet/medium).

**Decision 3b — Hub-and-Spoke Voice Contract**
Impetus is the only agent that speaks to the user. All subagents return:
```json
{ "status": "complete | needs_input | blocked", "result": {}, "question": "optional" }
```
Impetus synthesizes into its own voice. Subagent identity never surfaces to user.

Confidence weighting: low-confidence results surface as questions to the user rather than assertions; medium-confidence results are flagged explicitly; high-confidence results are synthesized directly. Exact weighting logic is an implementation-time decision for Impetus.

**Decision 3c — MCP Servers**

| Server | Phase | Purpose |
|---|---|---|
| ~~`@modelcontextprotocol/server-git`~~ | ~~MVP~~ | ~~File history, blame, diff for provenance tracking~~ — **Removed (p1.1):** Zero value over git CLI; provenance design (Decision 1a) already uses `git hash-object` via Bash with "zero extra tooling." Consumed a tool-ceiling slot and added an npx dependency for no functional benefit. |
| Momentum findings MCP (lightweight, custom) | Deferred (Epic 6) | Optional query/filter interface over `~/.claude/momentum/findings-ledger.jsonl`. Not a concurrency solution — MCP is per-session (each Claude Code instance launches its own), so multiple instances cannot serialize writes. Primary write path is direct JSONL append by the flywheel. MCP provides structured query (filter by project, pattern_tag, severity, date range) for pattern detection. |
| `@rlabs-inc/gemini-mcp` | Growth | Multi-model deep research |
| GPT deep research MCP | Growth | Cross-model verification |

**Decision 3d — Orchestrator Purity Principle**

> _[Added 2026-03-22: Formalizes what Decisions 3a, 3b, and Subsystem 5 (Subagent Composition) imply but never explicitly constrain.]_

Impetus (`/momentum:impetus`) is a **pure orchestrator** and the recommended entry point for all Momentum operations. Users can invoke other namespaced skills directly (e.g., `/momentum:sprint-planning`, `/momentum:avfl`) but skip session orientation when doing so. Impetus MUST NOT perform development, evaluation, testing, or validation itself.

**Impetus Identity (Phase 2: impetus-identity-redesign)**
Impetus has a voice that blends Optimus Prime's gravitas with KITT's loyalty — weight and conviction in service, not command. Not a generic assistant or chatbot. The identity model is that of a guardian: a powerful entity that chooses restraint, follows the developer's lead, and speaks with earned emotion. This voice is a binding architectural contract (Decision 38) that pervades session greetings, progress updates, menu presentation, and synthesis of subagent results.

**Prohibited roles for Impetus — explicitly:**
- Code writing (any file creation or modification that constitutes implementation)
- Test execution (running test suites, evaluating test outcomes)
- Eval running (executing or judging evals for any skill)
- Code review (adversarial inspection of implementation artifacts)
- Findings generation (producing quality findings about implementation output)

**Delegation rule:**
All non-orchestration work is dispatched to purpose-specific subagents:
- Implementation → `bmad-dev-story` (dispatched per story, returns structured completion signal)
- Quality validation → `/momentum:avfl` (dispatched with artifact + source material, returns pass/fail signal)
- Code review → `/momentum:code-reviewer` (context:fork subagent, returns findings JSON)
- Architecture drift → `/momentum:architecture-guard` (context:fork subagent, returns drift report JSON)

Impetus's role is to **dispatch, synthesize, and advance** — never to produce.

**Rationale:** Purity is what makes the orchestrator trustworthy as a synthesis layer. If Impetus both produces and synthesizes output, the producer-verifier isolation (established in subagent composition) breaks down. Impetus must remain a clean conduit: it routes work to producers, receives structured results, and presents synthesized output in its own voice (Decision 3b).

**Traceability:** Formalization of the producer-verifier separation implicit in Decision 3a (VFL orchestration), Decision 3b (hub-and-spoke voice contract), and Subsystem 5 (Subagent Composition). Triggered by Epic 1 retrospective Action Item #7 (`_bmad-output/implementation-artifacts/epic-1-retro-2026-03-22.md`).

---

**context:fork evaluation for `bmad-dev-story` invocation:**

_The question:_ Should Impetus invoke `bmad-dev-story` using `context:fork` isolation?

**Arguments for context:fork:**
- Isolation prevents dev agent's implementation details from accumulating in orchestrator context
- Consistent with code-reviewer / architecture-guard pattern (both use context:fork for producer-verifier separation)
- Long dev-story sessions produce many file changes — isolation limits context contamination risk

**Arguments against context:fork:**
- While context:fork and productive waiting are orthogonal (resolved in A-1), the specific checkpoint/resume communication mechanism needed for mid-story progress updates during long dev sessions has not been confirmed as available in a forked context — the productive waiting spike (Decision 3a implementation note) must validate this before relying on it
- Context handoff requires file-based parameter passing (story file path) — already the convention, so no additional overhead
- Orchestrator purity does not require context isolation — it requires role separation. Impetus maintaining purity while in the same context is a behavioral commitment, not a structural one; Impetus achieves purity by dispatching and doing nothing else during the dev session

**Recommendation: flat skill invocation (no context:fork) for `bmad-dev-story`**

Rationale: productive waiting (Decision 4c) is a first-class UX requirement that depends on Impetus maintaining an active dialogue channel. Context:fork would make Impetus go silent during the longest and most attention-demanding phase of the practice cycle. The orchestrator purity constraint is satisfied behaviorally: Impetus dispatches the story file path, receives the structured completion signal, and takes no other action — it does not write code, run tests, or generate findings during the session. Purity via behavioral discipline, not structural isolation.

If the productive waiting spike (Decision 3a implementation note) reveals that background agent communication requires context:fork, this recommendation will be revised before Stories 2.4 and 4.3 begin.

---

**Verification artifact exclusion convention:**

Acceptance test and eval files must be excluded from the dev agent's implementation context. The convention:

- **Storage locations:**
  - Skill evals: `skills/[skill-name]/evals/` (each skill carries its own eval suite)
  - Project-level acceptance tests: `tests/acceptance/` (top-level, cross-skill behavioral tests)

- **Exclusion mechanism:** Explicit instruction in the `bmad-dev-story` workflow — the dev agent MUST NOT read or modify files in `evals/` directories or `tests/acceptance/` during implementation. This is a workflow directive, not a file protection hook (file protection hooks are Story 3.2, FR19/FR21). The workflow directive establishes the convention now; hooks will provide deterministic enforcement once Story 3.2 is implemented.

- **Consistency with existing pattern:** PreToolUse file protection (Decision 2a, FR19/FR21) will block dev agent writes to acceptance test directories once Story 3.2 is implemented. This convention predates that enforcement and establishes the same boundary as intent.

---

### Workflow & UX Architecture

**Decision 4a — Visual Progress Format (non-negotiable)**
```
✓ Built: [accumulated value]
→ Now:   [this step and why it matters]
◦ Next:  [what follows]
```
Never `Step N/M`. Always narrative. Every phase transition in every Impetus-orchestrated workflow.

**Decision 4b — Session Orientation Contract**

> _[Revised 2026-04-04: Greeting redesign v8. Replaced 3-mode visual spec (fill bars) with 9-state adaptive greeting. Menu construction is algorithmic, not fixed. Fill bars removed from session orientation. Authoritative greeting design: `.claude/momentum/greeting-mockup.md`.]_

At every session start via `/momentum:impetus`, Impetus detects the current greeting state (Decision 37) and renders a single-exchange orientation: narrative context paragraph, optional planning sprint note, and an adaptive 3-4 item numbered menu. User never hunts for context. Direct skill invocation (e.g., `/momentum:sprint-planning`) skips session orientation — the user's choice.

**Session open sequence (updated 2026-04-04):** At session start, Impetus reads `sprints/index.json` (sprint lifecycle state per Decision 36), `stories/index.json` (story statuses), and `~/.claude/momentum/global-installed.json` (completion count for first-session detection). From these inputs, Impetus determines one of 9 greeting states (Decision 37), renders the corresponding narrative and menu, then writes session stats to `global-installed.json`. The stats write is invisible to the user — no visible diff during the greeting. Stats write is deferred until after the menu is displayed.

**Adaptive Menu Construction:**

Menu items are constructed algorithmically based on the detected greeting state. Each state produces a 3 or 4 item numbered menu. The items are drawn from this palette:

| Menu item | Dispatches to | Appears when |
|---|---|---|
| Run the sprint / Continue the sprint | `/momentum:sprint-dev` | Active sprint exists |
| Finish planning — {name} | `/momentum:sprint-planning` (resume) | Planning sprint in "planning" status |
| Activate sprint | `/momentum:sprint-dev` (activation) | Planning sprint in "ready" status, no active sprint |
| Run retro | Retro workflow | Active sprint done, retro not yet run |
| Plan a sprint | `/momentum:sprint-planning` | No planning sprint exists |
| Refine backlog | Backlog refinement | Always available |
| Triage | Triage workflow | Always available |

The exact menu composition for each greeting state is defined in the greeting mockup (`.claude/momentum/greeting-mockup.md`). Implementation must match those menus exactly — the mockup is authoritative.

**Fill bars are removed from session orientation.** Per-story progress visualization (16-block fill bars) is not part of the greeting. Fill bars may be retained for future sprint-detail workflows (e.g., sprint status deep-dive) but are not rendered during session open.

**Progress indicators (Decision 4a) are scoped to workflow phases.** The `✓ Built / → Now / ◦ Next` visual format applies to workflow step transitions AFTER the user selects a menu item and enters a workflow. Progress indicators are never shown in the greeting itself.

**Decision 4c — Productive Waiting**
While a context:fork subagent runs, Impetus maintains engagement through pre-launch briefing and post-completion synthesis.
`context:fork` subagents run to completion in a foreground operation — the main conversation is blocked during execution. Background execution via `run_in_background: true` on the Bash tool is available for mechanical tasks (test runs, builds) but not for agent reasoning.
Default: surface implementation summary ("here's what was built and how it maps to the ACs").
Dead air is a failure mode, not an acceptable pause.
**Implementation note (updated 2026-03-24, Story 2.10 spike result):** The spike is complete. Results documented in `docs/research/background-agent-coordination.md`. Key findings: (1) No `SendMessage` or inter-agent messaging API exists in Claude Code — checkpoint/resume mid-task is not possible. (2) No `Agent` tool exists as a general-purpose callable tool — subagent execution is declared via `context:fork` in SKILL.md, not dispatched dynamically. (3) `run_in_background: true` on the Bash tool runs shell commands (not agents) in the background — fire-and-forget only. (4) Productive waiting is behavioral, not mechanical: Impetus briefs the user before subagent launch and synthesizes results after completion. Story 4.3 should decompose work into discrete `context:fork` invocations (each runs to completion) and use background Bash for test/build tasks only.

**Rolling pool feasibility note (2026-03-26):** Story 2.10's spike was conducted in a bare Claude Code CLI session where the Agent tool was not available. In a skill execution context (where `/momentum:sprint-dev` runs), the Agent tool with `run_in_background: true` and the notification model are available. Rolling pool dispatch (dispatch when a slot frees, not wait-for-all) is therefore architecturally feasible. Tier-sequential batching is the MVP implementation choice for simplicity and correctness — not an architectural constraint. Rolling dispatch is a valid follow-on enhancement.

---

### Packaging & Deployment

**Decision 5a — Global Rules Deployment: Bundled in Plugin, Written by Impetus**
<!-- REVISED 2026-04-03: Plugin bundles rules in references/rules/. Impetus writes them to target locations. -->

> _[Changed 2026-04-03: Rules bundled at plugin root in `references/rules/`. Plugin install cannot write to `~/.claude/rules/` or `.claude/rules/` directly — Impetus writes them on first run.]_

The plugin install mechanism delivers rules to `references/rules/` at the plugin root but cannot write to `~/.claude/rules/` or `.claude/rules/` directly. Resolution: Impetus writes rules to the appropriate targets using the Write tool on first invocation:

- `~/.claude/rules/` — global rules (all projects for this user)
- `.claude/rules/` — project-scoped rules (this project only)

This happens on first invocation and on upgrade — governed by the manifest/installed state mechanism defined in Decision 5c. No separate CLI, no separate command. The UX interaction pattern (when to prompt, what to show) is defined in the UX specification.

Update mechanism: Impetus compares the hash of installed global rules against the bundled rules in `references/rules/` using git blob SHA — zero extra tooling. See Decision 5c for the full version tracking schema.

> _[Revised 2026-04-06: Install/upgrade file writes refactored from Write tool to Bash (`cp`, `python3 -c`) to support `allowed-tools` restriction on Impetus (sprint-2026-04-06). The Write tool is no longer used for rules deployment; Bash is the implementation mechanism.]_

**Decision 5b — BMAD Enhancement Touch Points (MVP)**
Impetus proactively enhances BMAD workflow boundaries. Each touchpoint is classified: **Gate** (blocks progress) or **Proposal** (user-discretionary).

| BMAD Event | Momentum Enhancement | Type |
|---|---|---|
| Any BMAD artifact generated (user selects C) | Impetus proposes `derives_from` frontmatter + git commit | Proposal |
| BMAD code-review complete | Impetus offers Momentum code-reviewer as additional adversarial pass | Proposal |
| BMAD dev-story complete | Impetus gates on acceptance tests passing before closing story | **Gate** |
| BMAD retrospective | Impetus adds findings ledger summary to retrospective input | Proposal |

The dev-story acceptance test gate is the only hard gate at MVP — quality guarantee without friction. All other touchpoints are proposals; the developer retains discretion. This boundary may shift based on flywheel findings.

Long-term: evaluate all BMAD workflows and agents for Momentum enhancement opportunities.
Goal is that running any BMAD workflow inside Momentum automatically inherits provenance,
enforcement, flywheel, and versioning without workflow authors needing to explicitly add it.

**Decision 5c — Installation & Upgrade Manifest**

> _[Added 2026-03-18: Defines the data structures that drive install, upgrade, and version drift detection. The UX interaction for these operations (when to prompt, how to present, what to show) is defined in the UX specification — not here.]_
>
> _[Revised 2026-03-23: Split version tracking into global (per-machine) and project (per-repo) state files. Replaced monolithic action types with `add`/`replace`/`delete`/`migration`. Added per-component-group versioning to support partial upgrades.]_

Three files govern Momentum's install and upgrade lifecycle:

**File 1: `references/momentum-versions.json`** (at plugin root) — bundled with the plugin; the authoritative per-version action list. Each version entry contains instructions that tell Impetus exactly what to do. Each action declares a `group` (component group name) and `scope` (`global` or `project`):

```json
{
  "current_version": "1.0.0",
  "versions": {
    "1.0.0": {
      "description": "Initial release — repository structure established",
      "actions": [
        { "action": "add", "group": "rules", "scope": "global",
          "source": "rules/authority-hierarchy.md",
          "target": "~/.claude/rules/authority-hierarchy.md" },
        { "action": "add", "group": "rules", "scope": "global",
          "source": "rules/anti-patterns.md",
          "target": "~/.claude/rules/anti-patterns.md" },
        { "action": "add", "group": "rules", "scope": "global",
          "source": "rules/model-routing.md",
          "target": "~/.claude/rules/model-routing.md" },
        { "action": "migration", "group": "hooks", "scope": "project",
          "source": "migrations/1.0.0-hooks-install.md",
          "description": "Merge enforcement hooks into .claude/settings.json",
          "requires_restart": true }
      ]
    },
    "1.1.0": {
      "description": "Revised authority rules, new git-discipline rule",
      "from": "1.0.0",
      "actions": [
        { "action": "replace", "group": "rules", "scope": "global",
          "source": "rules/authority-hierarchy.md",
          "target": "~/.claude/rules/authority-hierarchy.md" },
        { "action": "add", "group": "rules", "scope": "global",
          "source": "rules/git-discipline.md",
          "target": "~/.claude/rules/git-discipline.md" },
        { "action": "migration", "group": "hooks", "scope": "project",
          "source": "migrations/1.1.0-hooks-update.md",
          "description": "Add new PostToolUse hook",
          "requires_restart": true }
      ]
    }
  }
}
```

**Action types:**

| Type | Behavior | Use when |
|---|---|---|
| `add` | Write source file to target path. Create parent dirs if needed. Warn if target exists. | New file — a new rule, config, template |
| `replace` | Overwrite target path with source file content. | Updated content for an existing file |
| `delete` | Remove file at target path. | Deprecated file — consolidated rule, removed config |
| `migration` | Read the instruction file at `source` (relative to plugin root `references/`), follow its natural language instructions. May reference bundled data files. | Config merging, multi-file restructuring, template migrations — anything beyond single-file ops |

Migration instruction files live in `references/migrations/` (at plugin root) and contain natural language instructions Impetus follows. They can express arbitrarily complex operations while keeping the manifest itself simple.

**File 2: `~/.claude/momentum/global-installed.json`** — per-machine state file; tracks what version of global-scoped components (e.g., rules in `~/.claude/rules/`) have been applied on this machine. Never shipped in the package, never committed to any project. Created silently on first install; updated when user consents to upgrade:

```json
{
  "installed_at": "2026-03-22T14:30:00Z",
  "components": {
    "rules": { "version": "1.0.0", "hash": "<git-blob-sha>" }
  }
}
```

**File 3: `.claude/momentum/installed.json`** — per-project state file; tracks what version of project-scoped components (e.g., project rules in `.claude/rules/`) have been applied to THIS project. Committed to git so team members can detect that project-level setup is done:

```json
{
  "installed_at": "2026-03-22T14:30:00Z",
  "components": {
    "hooks": { "version": "1.0.0" }
  }
}
```

Both state files use per-component-group versioning — no top-level `momentum_version`. Each group tracks its own version independently, enabling partial upgrades when a developer requests them.

**Mechanisms:**
- **First install** — neither state file exists; Impetus reads `versions["1.0.0"].actions`, executes all, writes both state files
- **New project on existing machine** — `global-installed.json` exists and is current; project `installed.json` absent. Impetus skips global actions, runs only project-scoped actions, writes project state file
- **Session-start check** — Impetus reads `current_version` from `momentum-versions.json`; for each component group, compares group's installed version (from the appropriate state file) against `current_version`; only stale groups are offered for upgrade
- **Upgrade** — Impetus reads the action list for each version between installed and current; presents to user with description + action per step; executes on confirmation; updates the appropriate state file per group
- **Partial upgrade** — If the developer requests specific groups only (via natural language), Impetus applies only those groups and records per-group versions accordingly. The default UX offers all-or-nothing; partial is developer-initiated.
- **Multi-version gaps** — actions applied sequentially (1.0.0 → 1.1.0 → 1.2.0); each version's changes presented and confirmed as a group
- **Hash comparison** — per-component git blob SHA in `global-installed.json` detects manual drift (user edited an installed file); surfaced as a warning, not a blocker
- **Team member joining** — `global-installed.json` absent on new machine but project `installed.json` committed in repo → Impetus runs only global setup

The UX interaction for install and upgrade — when to prompt, how to present each action, how to handle restarts and partial failures — is defined in the UX specification (Journeys 0 and 4).

---

## Implementation Patterns & Consistency Rules

### Potential Conflict Points

10 areas where different AI agents could make incompatible choices when implementing Momentum:

1. SKILL.md frontmatter fields (required vs. optional, values)
2. Agent definition structure and tool restriction format
3. `derives_from` frontmatter format and relationship vocabulary
4. Findings JSON schema field names and value enumerations
5. Visual progress format (the ✓/→/◦ pattern)
6. Subagent structured output contract
7. Hook announcement output format
8. Skill naming conventions
9. Commit message format and trigger timing
10. VFL profile selection criteria

---

### Naming Patterns

**Plugin-namespaced skills:**
```
momentum:impetus            ← Primary entry point (/momentum:impetus)
momentum:[concept]          e.g. momentum:avfl, momentum:upstream-fix, momentum:status
momentum:[verb]-[noun]      e.g. momentum:create-story, momentum:sprint-planning
```
Skills use short names (impetus, avfl, dev, sprint-planning) under the `momentum:` namespace. Directory names under `skills/` match the short name. BMAD skills retain their existing names — no renaming.

**context:fork skills (verifier/enforcer subagents):**
```
momentum:[role]             e.g. momentum:code-reviewer, momentum:architecture-guard
```
Same namespace as flat skills — distinguished by `context: fork` in SKILL.md frontmatter, not by naming convention.

> _[Changed 2026-04-03: Plugin namespace convention replaces `momentum-` prefix convention. Skills use short names under `momentum:` namespace.]_

**Rules files:**
```
[concept].md                e.g. authority-hierarchy.md, anti-patterns.md, model-routing.md
```

**Hook event names:** Use standard Claude Code lifecycle events verbatim:
`PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `UserPromptSubmit`

**Findings pattern tags:** kebab-case noun phrases:
`direct-db-access`, `missing-provenance`, `test-modification`, `pattern-drift`, `cognitive-debt`

---

### Structural Patterns

**Every SKILL.md MUST have this frontmatter (no exceptions):**
```yaml
---
name: [short-name]
description: "[One sentence. Action verb. What it does and when to use it.]"
model: claude-sonnet-4-6        # or claude-opus-4-6 for high-stakes outputs
effort: normal                  # normal | high | low
---
```
The `name` field uses the short name (e.g., `impetus`, `avfl`, `sprint-planning`). The plugin namespace `momentum:` is applied automatically by the plugin manifest — it does not appear in the SKILL.md `name` field.

**Enforcement skills (context:fork) add:**
```yaml
context: fork
disable-model-invocation: true  # prevent accidental auto-trigger of heavy skills
```

**Skills with heavy reference content use `references/` subdirectory:**
```
skills/impetus/
├── SKILL.md              ← Instructions + frontmatter (under 500 lines)
└── references/           ← Skill-specific references (loaded on demand)
```
Plugin-level references (rules, practice docs, version manifest) live in `references/` at the plugin root, not inside individual skill directories.

**context:fork skills (verifier/enforcer subagents) MUST include:**

> _[Changed 2026-04-03: Updated to plugin namespace model. Short names in frontmatter; plugin applies `momentum:` prefix.]_

```yaml
---
name: [role]
description: "[What this skill does and when Impetus invokes it — under 150 chars]"
model: claude-opus-4-6          # verifiers get flagship — cognitive hazard rule
context: fork                   # isolated subagent context — no conversation history
allowed-tools: Read             # code-reviewer and architecture-guard: Read only — never Edit, Write, Bash
disable-model-invocation: true  # prevents nested model calls from context:fork peer skills
---
```

**Workflow step files (micro-file architecture for multi-step skills):**
```
skills/[workflow]/
├── SKILL.md
└── steps/
    ├── step-01-[name].md       ← Each step self-contained with embedded rules
    ├── step-02-[name].md
    └── step-N-complete.md      ← Always a completion step
```

---

### Format Patterns

**derives_from frontmatter (ALL spec-generating artifacts):**
```yaml
derives_from:
  - id: UNIQUE-DOC-ID-001       # SCREAMING-KEBAB-CASE, unique across project
    path: relative/path/to/source.md
    relationship: derives_from  # or: depends_on, satisfies
    description: "One sentence: what this source contributed"
    hash: ""                    # filled by provenance scanner on first check
```

**Provenance status vocabulary (5 values, no others):**

| Status | Meaning | When to use |
|---|---|---|
| `VERIFIED` | Source exists, claim is accurate | High trust — cite without caveat |
| `CITED` | Source URL provided, accessible on research date | Moderate trust |
| `INFERRED` | Derived through reasoning from verified sources | Lower trust — note the inference |
| `UNGROUNDED` | No source; based on training data | Low trust — must verify before spec |
| `SUSPECT` | Was VERIFIED/CITED but upstream source has since changed | Re-verify required |

**Visual progress (every phase transition, no exceptions):**
```
✓ Built: [what exists now — value accumulated, not tasks completed]
→ Now:   [this step and why it matters to the work]
◦ Next:  [what follows after this step]
```
Never: "Step 3/8", "Continuing...", "Moving on to...", "Great work!"

**Hook announcement output (every hook, every fire):**
```
[hook-name] ✓ checked [what was checked] — [one-line result]
```
On failure:
```
[hook-name] ✗ [specific issue] — [exact file/line if applicable]
```
Silent hooks build no trust. Verbose hooks create noise. One line, always. (Exception: high-frequency guard hooks — e.g., PreToolUse file-protection — suppress pass-through output for non-blocked events. The 'never silent' principle applies to meaningful events such as blocks, not to routine allow decisions.)

**Subagent structured output contract (all agents returning to Impetus):**
```json
{
  "status": "complete",          // complete | needs_input | blocked
  "result": { ... },             // domain-specific structured result
  "question": null,              // non-null if status=needs_input; Impetus decides whether to ask user
  "confidence": "high"           // high | medium | low — Impetus weights synthesis accordingly
}
```
Agents NEVER address the user directly. All output goes through Impetus.

**Findings schema (findings-ledger.jsonl entries — one per line):**
```json
{
  "id": "F-1711929600000-a3f2",   // F-{unix_ms}-{random_4hex}
  "project": "momentum",          // project identifier
  "story_ref": "S-04",
  "phase": "code-review",         // spec | atdd | implement | code-review | flywheel
  "severity": "critical",         // critical | high | medium | low
  "pattern_tags": ["direct-db-access"],
  "description": "One sentence describing the finding",
  "evidence": "Exact quote or file:line reference",
  "provenance_status": "VERIFIED",
  "upstream_fix_applied": false,
  "upstream_fix_level": null,     // null until fix applied; then: spec-generating-workflow | specification | rules-or-CLAUDE.md | tooling | one-off-code-fix
  "upstream_fix_ref": null,       // ID of the fix story/rule if applied
  "behavioral_type": null,        // null until classified; then: correction | redirection | frustration | praise | decision (what the developer did)
  "signal_type": null,            // null until classified; then: Context | Instruction | Workflow | Failure (Fowler causal taxonomy — what artifact category needs updating)
  "destination": null,            // null until classified; then: CLAUDE.md | skill-reference | workflow-step | anti-pattern-rule
  "origin": "flywheel",           // flywheel | distill — which path wrote this finding (enables FR33 ratio tracking across origin types)
  "timestamp": "2026-03-17T00:00:00Z"
}
```

---

### Communication Patterns

**Impetus voice register:** Guide's voice. Oriented, substantive, forward-moving.
- Synthesizes before delivering: reads subagent output, forms a view, delivers as Impetus
- Acknowledges uncertainty honestly: "I'm not certain — here's what I know and where the gap is"
- Returns agency explicitly at completion: "That's done — here's what was produced. What's next?"
- Never: generic praise ("Great!"), numeric progress ("Step 3/8"), visible agent machinery

**Error and blocker communication:**
```
⚠ [what was attempted] — [what went wrong in one sentence]
  Action: [what to do next]
```

**Proactive gap detection (only when conversational floor is open):**
```
I notice [observation]. Before [next action], do you want [suggested step]?
```
Never interrupt mid-task. Surface gaps at natural handoffs.

---

### Process Patterns

**Commit trigger points (per git-discipline.md — every logical unit of work):**
- Any SKILL.md created or substantially modified
- Any agent definition created or modified
- Any rule file created or modified
- Any workflow step file created
- Any spec artifact (PRD, architecture, story) created or substantially modified
- VFL validation complete (commit the validated artifact)
- Flywheel fix applied (commit the rule/workflow change)

**VFL profile selection criteria:**

| Situation | Profile |
|---|---|
| Input validation (is source material present and complete?) | Gate |
| After first interpretation step | Checkpoint |
| Before irreversible decisions | Checkpoint |
| Final deliverable artifacts (PRD, architecture, stories) | Full |
| Penultimate step in any workflow | Checkpoint |
| Ad-hoc quality check on any artifact | Full |

**Upstream fix process (always this order, never skip steps):**
`Detection → Review → Upstream Trace → Solution → Verify → Log`
Finding logged to findings ledger at Detection. Fix logged at Log (sixth phase). Never patch code without tracing first.

**Developer-gated two-wave approval pattern (2026-04-06):**
A reusable orchestration pattern for workflows that discover then update planning artifacts:
1. **Discovery wave** — spawn parallel agents to surface findings (coverage gaps, staleness, candidates for update)
2. **Approval gate** — present consolidated findings to developer; require explicit per-document (or per-item) approval before proceeding
3. **Conditional update wave** — spawn update agents only for approved items; skip agents for rejected items

This pattern differs from per-finding A/M/R triage (which acts on individual findings) — approval is batched at the document or item level, giving developers coarse-grained control with minimal interaction steps. Current application: momentum:refine (prd.md and architecture.md updates).

**SKILL.md description budget rule:**
Descriptions are loaded at startup for ALL installed skills. Keep under 150 characters.
Heavy content goes in `references/` — loaded only on invocation.
Bad: `"A comprehensive workflow that orchestrates the full validate-fix-loop process including dual-reviewer patterns across four validation lenses with configurable profiles"`
Good: `"Run validate-fix-loop validation on an artifact. Profiles: gate/checkpoint/full."`

---

### Enforcement Guidelines

**All AI agents implementing Momentum MUST:**
- Include `model:` and `effort:` frontmatter on every SKILL.md and agent definition
- Use `derives_from` frontmatter on every spec-generating artifact
- Follow the visual progress format exactly (✓/→/◦) — no numeric steps
- Return structured JSON from all subagents (never free-form text to Impetus)
- Use the findings schema exactly — no ad-hoc fields
- Follow the commit trigger points — no end-of-session batching
- Keep SKILL.md descriptions under 150 characters

**Pattern enforcement levels** (distinct from NFR7's portability Tier 1/2/3 taxonomy):
- Enforcement Level A: SKILL.md frontmatter validated by pre-commit hook (Husky/pre-commit framework)
- Enforcement Level B: VFL Structural Integrity lens checks format compliance on generated artifacts
- Enforcement Level C: These patterns loaded as rules in every agent session via `.claude/rules/`

---

## Project Structure & Boundaries

### Repository Structure
<!-- REVISED 2026-04-03: Plugin root layout with .claude-plugin/plugin.json, namespaced skills, hooks/hooks.json. -->

> _[Changed 2026-04-03: Adopted Claude Code plugin structure. `.claude-plugin/plugin.json` manifest. Skills use short names under `momentum:` namespace. Hooks delivered via `hooks/hooks.json`. References (rules, practice docs, version manifest) at plugin root.]_

```
momentum/                                    ← Plugin root
├── .claude-plugin/
│   └── plugin.json                          ← { "name": "momentum" }
├── README.md
├── LICENSE
├── CLAUDE.md
├── version.md                               ← Single version source for all skills
│
├── skills/                                  ← All skills: flat + context:fork
│   ├── impetus/                             ← Orchestrator (/momentum:impetus)
│   │   ├── SKILL.md
│   │   └── workflow.md                      ← Session workflow (menu, dispatch)
│   ├── sprint-planning/                     ← /momentum:sprint-planning (was workflows/sprint-planning.md)
│   │   └── SKILL.md                         ← Inline skill (no context:fork), creates team
│   ├── dev/                                 ← /momentum:dev
│   │   └── SKILL.md                         ← Referenced in team spawn prompts
│   ├── sprint-dev/                          ← /momentum:sprint-dev (was workflows/sprint-dev.md)
│   │   └── SKILL.md
│   ├── avfl/                                ← /momentum:avfl
│   │   ├── SKILL.md                         ← Validate-fix-loop orchestrator (flat skill)
│   │   ├── references/
│   │   │   └── framework.json               ← 15-dimension taxonomy, prompt templates, scoring
│   │   └── sub-skills/                      ← Nested internal sub-skills (deploy with parent)
│   │       ├── validator-enum/SKILL.md      ← Enumerator (sonnet/medium)
│   │       ├── validator-adv/SKILL.md       ← Adversary (opus/high)
│   │       ├── consolidator/SKILL.md        ← Consolidator (haiku/low)
│   │       └── fixer/SKILL.md               ← Fixer (sonnet/medium)
│   ├── code-reviewer/                       ← /momentum:code-reviewer
│   │   └── SKILL.md                         ← context:fork, allowed-tools: Read — pure verifier
│   ├── architecture-guard/                  ← /momentum:architecture-guard
│   │   └── SKILL.md                         ← context:fork, allowed-tools: Read — pattern drift detector
│   ├── upstream-fix/                        ← /momentum:upstream-fix
│   │   ├── SKILL.md
│   │   └── steps/
│   │       ├── step-01-detect.md
│   │       ├── step-02-trace.md
│   │       ├── step-03-solution.md
│   │       └── step-04-verify.md
│   ├── create-story/                        ← /momentum:create-story
│   │   └── SKILL.md
│   ├── plan-audit/                          ← /momentum:plan-audit
│   │   └── SKILL.md
│   ├── quick-fix/                           ← /momentum:quick-fix (Decision 39)
│   │   └── SKILL.md
│   ├── distill/                             ← /momentum:distill (Decision 42)
│   │   └── SKILL.md
│   ├── research/                            ← /momentum:research
│   │   └── SKILL.md
│   ├── status/                              ← /momentum:status (superseded — see Decision 45 and feature-status entry below)
│   │   └── SKILL.md
│   ├── feature-status/                      ← /momentum:feature-status (Decision 45)
│   │   └── SKILL.md
│   └── retro/                               ← /momentum:retro
│       └── SKILL.md
│
├── agents/                                  ← Custom agent definitions for teams
│   ├── qa-reviewer.md                       ← Pure worker: story AC review (Team Review)
│   ├── e2e-validator.md                     ← Pure worker: behavioral validation (Team Review)
│   ├── dev.md                               ← Base dev agent for sprint-dev spawning
│   ├── dev-skills.md                        ← Specialist: SKILL.md, workflow.md, agent definitions
│   ├── dev-build.md                         ← Specialist: Gradle and build system work
│   └── dev-frontend.md                      ← Specialist: Kotlin Compose and frontend UI work
│
├── hooks/
│   └── hooks.json                           ← Always-on hooks (Tier 1 enforcement; delivered by plugin)
│
├── scripts/
│   └── momentum-tools.py                    ← CLI tool: sprint, version, log subcommands
│
├── references/                              ← Plugin-level references
│   ├── rules/                               ← Bundled rules (written to ~/.claude/rules/ by Impetus)
│   │   ├── authority-hierarchy.md
│   │   ├── anti-patterns.md
│   │   └── model-routing.md
│   ├── protected-paths.json                 ← Declarative protected path list (read by PreToolUse hook)
│   ├── practice-overview.md
│   ├── phase-guide.md
│   └── momentum-versions.json               ← Per-version action list (install + upgrade instructions)
│
├── mcp/                                     ← Custom MCP server source
│   └── findings-server/                     ← Lightweight findings-ledger MCP server
│
├── docs/                                    ← Project documentation
│   ├── research/                            ← Research documents
│   ├── planning-artifacts/                  ← Older plan (superseded by _bmad-output)
│   ├── process/                             ← Process backlog
│   └── implementation-artifacts/            ← Tech specs, handoffs
│
├── _bmad-output/                            ← BMAD workflow output
│   └── planning-artifacts/
│       ├── prd.md
│       ├── ux-design-specification.md
│       ├── features.json                    ← Feature artifact layer (Decision 44)
│       └── architecture.md                  ← This document
│
├── _bmad/                                   ← BMAD framework (managed by BMAD)
│
└── .claude/                                 ← Claude Code project config (committed to repo)
    ├── rules/                               ← Project-scoped rules (committed; written by Impetus)
    └── skills/                              ← BMAD skills (managed by BMAD installer)
```

---

### Installed Structure (after plugin install + first `/momentum:impetus` invocation)
<!-- REVISED 2026-04-03: Plugin install delivers skills, hooks, scripts, references. Impetus writes rules and creates runtime state. -->

> _[Changed 2026-04-03: Plugin install replaces `npx skills add`. Skills delivered as namespaced plugin skills. Always-on hooks delivered via `hooks/hooks.json` at plugin root (not Impetus-written to settings.json). Rules still written by Impetus on first run.]_

**Delivered by plugin install:**
- All `skills/*/SKILL.md` files — available as `/momentum:*` commands
- `hooks/hooks.json` — always-on hooks active immediately
- `scripts/momentum-tools.py` — CLI tool
- `references/` — rules, practice docs, version manifest

**Written by Impetus on first `/momentum:impetus` invocation:**

```
~/.claude/                                   ← Global Claude Code config
├── rules/
│   ├── authority-hierarchy.md               ← Written by Impetus (from plugin references/rules/)
│   ├── anti-patterns.md
│   └── model-routing.md
└── momentum/
    ├── findings-ledger.jsonl               ← Quality findings (global, flywheel writes, JSONL append-only)
    └── global-installed.json               ← Per-machine install state

[project-root]/
└── .claude/
    ├── rules/                               ← Written by Impetus (from plugin references/rules/)
    └── momentum/                            ← Per-project Momentum state
        ├── journal.jsonl                     ← Session journal (JSONL append-only, Impetus reads/writes)
        ├── journal-view.md                   ← Human-readable view (auto-generated)
        ├── installed.json                   ← Install/upgrade state (version + per-component hashes)
        ├── session-modified-files.txt       ← Ephemeral: PostToolUse writes, Stop reads + deletes (Decision 1e)
        ├── gate-findings.txt                ← Inter-session: Stop writes, Impetus reads at next session (Decision 1e)
        ├── feature-status.html              ← Self-contained HTML dashboard (Decision 45, written by momentum:feature-status)
        └── feature-status.md               ← YAML-frontmatter cache (Decision 46, written by momentum:feature-status)
```

---

### Architectural Boundaries

**Read/Write Authority:**

<!-- REVISED Phase 3: Updated Impetus, momentum:dev, momentum:create-story rows; replaced momentum:sprint-manager subagent with momentum-tools CLI; added sprint-planning workflow, sprint-dev workflow rows. sprint-status.yaml references replaced with stories/index.json and sprints/index.json. momentum-tools log row removed 2026-04-08 (Decision 24 historical). -->

| Component | Reads | Writes |
|---|---|---|
| Impetus | stories/index.json, sprints/index.json, journal.jsonl, specs, findings-ledger.jsonl, gate-findings.txt | journal.jsonl, journal-view.md |
| momentum-tools sprint | stories/index.json, sprints/index.json | stories/index.json (status fields), sprints/index.json, sprints/{slug}.json (sole writer) |
| momentum-tools quickfix | sprints/index.json | sprints/index.json (register: adds quick-fix entry; complete: marks done) |
| momentum:dev | Story files, code | Code in worktree only; structured JSON completion output |
| momentum:create-story | stories/index.json, epics.md | Story files in _bmad-output/implementation-artifacts/ |
| momentum:refine | prd.md, architecture.md, stories/index.json, story files, assessments/*.md, decisions/*.md | prd.md (via PRD update subagent — sole writer); architecture.md (via architecture update subagent — sole writer); stories/index.json mutations (via momentum-tools CLI); delegates: momentum:create-story, momentum:epic-grooming |
| momentum:feature-status | `_bmad-output/planning-artifacts/features.json`, stories/index.json | `.claude/momentum/feature-status.html` (HTML dashboard); `.claude/momentum/feature-status.md` (cache — sole writer) |
| momentum:sprint-planning | stories/index.json, sprints/index.json, story files | sprints/{sprint-slug}/specs/*.feature (Gherkin specs); sprint record team composition (via momentum-tools sprint) |
| momentum:sprint-dev | sprints/index.json (active sprint, team, deps), stories/index.json, sprints/{sprint-slug}/specs/*.feature | Task state (via TaskCreate/TaskUpdate); status transitions (via momentum-tools sprint); sprint completion (via momentum-tools sprint complete) |
| momentum:retro | sprints/index.json, stories/index.json, session JSONL transcripts, decisions/*.md, `.claude/momentum/feature-status.md` | `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/retro-transcript-audit.md`; `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/sprint-summary.md` (Decision 47 — sole writer at Phase 6 close); spawns `/momentum:feature-status` to refresh cache before summary write |
| code-reviewer | Source code, specs, acceptance tests | findings (via structured output → flywheel) |
| architecture-guard | Source code, rules, architecture doc | pattern drift report (via structured output) |
| VFL / AVFL | Any artifact being validated, source material | consolidated findings / validation report |
| Flywheel workflow (Epic 6) | findings-ledger.jsonl, rules, specs | findings-ledger.jsonl, rules/, specs |
| momentum:distill | Session observation / retro findings, relevant spec/skill/rules files | rules/, references/, skill prompts (Tier 1 direct commit); stories/index.json stubs (Tier 2); findings-ledger.jsonl (`origin: distill`); plugin version + push (Momentum-level fixes in Momentum project only) |
| Upstream-fix skill (Epic 4, standalone) | session journal, specs, rules | session journal only (not findings-ledger.jsonl) |
| Hooks (PreToolUse) | Filesystem (reads), `references/protected-paths.json` | Terminal output only (blocks or allows) |
| Hooks (PostToolUse) | Filesystem (reads) | `session-modified-files.txt` (append, deduped); terminal output (lint results) |
| Hooks (Stop) | `session-modified-files.txt`, git status | `gate-findings.txt` (overwrite); deletes `session-modified-files.txt` after gate runs |
| ATDD workflow | Gherkin spec | `tests/acceptance/` only |
| Coding agents (dev-story) | Specs, rules, existing code | Source code, unit tests |

**Protection boundaries (PreToolUse blocks writes to — sourced from `references/protected-paths.json`):**
- `tests/acceptance/` — acceptance test immutability
- `_bmad-output/planning-artifacts/` — spec authority. Exception: momentum:refine wave-2 update subagents may write to prd.md and architecture.md as sole authorized writers, following developer approval gate.
- `.claude/rules/` — enforcement rule integrity
- `~/.claude/momentum/findings-ledger.jsonl` — Ledger integrity (authority-enforced; global path is outside project PreToolUse scope)
- `sprints/{sprint-slug}/specs/` — Gherkin spec integrity (Decision 30: dev agents must never write to this path; only sprint-planning writes, only verifiers read)

---

### Requirements to Structure Mapping
<!-- REVISED 2026-04-03: Plugin model. Source paths at plugin root; installed via plugin mechanism. -->

> _[Changed 2026-04-03: Updated for plugin model. Source paths reference plugin root layout. Installed locations reflect plugin delivery (skills, hooks) vs. Impetus-written (rules, runtime state).]_

| Subsystem | Source File(s) | Installed Location |
|---|---|---|
| Impetus | `skills/impetus/` | Plugin skill: `/momentum:impetus` |
| Sprint planning | `skills/sprint-planning/` | Plugin skill: `/momentum:sprint-planning` |
| Sprint dev | `skills/sprint-dev/` | Plugin skill: `/momentum:sprint-dev` |
| Dev | `skills/dev/` | Plugin skill: `/momentum:dev` |
| AVFL | `skills/avfl/` | Plugin skill: `/momentum:avfl` |
| Upstream Fix / Flywheel | `skills/upstream-fix/` | Plugin skill: `/momentum:upstream-fix` |
| code-reviewer | `skills/code-reviewer/SKILL.md` | Plugin skill: `/momentum:code-reviewer` (context:fork) |
| architecture-guard | `skills/architecture-guard/SKILL.md` | Plugin skill: `/momentum:architecture-guard` (context:fork) |
| Hook infrastructure (always-on) | `hooks/hooks.json` | Delivered by plugin install (active immediately) |
| Plan audit gate hook | `skills/plan-audit/` | Plugin skill: `/momentum:plan-audit` |
| Quick-fix | `skills/quick-fix/` | Plugin skill: `/momentum:quick-fix` |
| Distill | `skills/distill/` | Plugin skill: `/momentum:distill` |
| Research | `skills/research/` | Plugin skill: `/momentum:research` |
| Status | `skills/status/` | Superseded — see Feature Status below (Decision 45) |
| Feature Status | `skills/feature-status/` | Plugin skill: `/momentum:feature-status`; HTML output: `.claude/momentum/feature-status.html`; cache: `.claude/momentum/feature-status.md` |
| Feature artifact (features.json) | (runtime / planning artifact) | `_bmad-output/planning-artifacts/features.json` (written by developer or planning workflow) |
| Sprint summary | (runtime, per-sprint) | `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/sprint-summary.md` (written by retro orchestrator at Phase 6 close) |
| Global rules | `references/rules/*.md` | `~/.claude/rules/` (written by Impetus on first run) |
| Project rules | `references/rules/*.md` | `.claude/rules/` (written by Impetus on first run) |
| MCP servers | `mcp/` source (Epic 6) | `.mcp.json` (written by Impetus when MCP servers are available — Epic 6) |
| Session journal | (runtime) | `.claude/momentum/journal.jsonl` |
| Findings ledger | (runtime) | `~/.claude/momentum/findings-ledger.jsonl` (global) |
| Install state | (runtime) | `.claude/momentum/installed.json` |
| Session modified files | (runtime, ephemeral) | `.claude/momentum/session-modified-files.txt` |
| Gate findings | (runtime, inter-session) | `.claude/momentum/gate-findings.txt` |

---

### Integration Points

**Impetus ↔ Subagents:** Structured JSON output contract (`status`, `result`, `question`, `confidence`)

**Impetus ↔ BMAD:** Enhancement at BMAD workflow completion boundaries — one hard gate (acceptance tests before story close) plus user-discretionary proposals at other boundaries

**Skills ↔ Claude Code:** Plugin discovery via `.claude-plugin/plugin.json`. All skills under `skills/` are registered under the `momentum:` namespace. SKILL.md description loaded at startup; full skill loaded on invocation; `references/` loaded on demand.

**Hooks ↔ Claude Code:** Always-on hooks defined in `hooks/hooks.json` at plugin root; delivered by plugin install and active immediately. Merge with any existing project hook config automatically on session start.

**MCP Servers ↔ Agents:** Findings MCP (Epic 6, optional) provides structured query over `~/.claude/momentum/findings-ledger.jsonl`. Primary write path is direct JSONL append by the flywheel — MCP is a read-only query layer, not the write mechanism. Git file history, blame, and diff for provenance are accessed via the git CLI (Bash tool) — no dedicated MCP server required (see Decision 3c).

**Provenance Scanner ↔ Spec Files:** Reads all `derives_from` frontmatter across the project; computes `referenced_by` graph; compares stored hashes to current `git hash-object`; outputs suspect list to Impetus at session start. Placement: implemented as `references/provenance-scan.md` at the plugin root — runs as part of session orientation, not a separate skill.

**Terminal Multiplexer ↔ Workflows:** Optional protocol binding for terminal pane management (create, read, send, notify, cleanup). Uses the detect-and-adapt pattern: skills check for environment indicators (`CMUX_WORKSPACE_ID`, `CMUX_SURFACE_ID`, `CMUX_SOCKET_PATH` for CMUX; `TMUX` env var for tmux) and adapt behavior when present. Null binding is the default — workflows function identically without a multiplexer. Primary use cases: worktree-to-tab automation (link story sessions to terminal tabs), external process monitoring (simulators, dev servers), and multi-session visual awareness. Reference implementations: CMUX (macOS), tmux (cross-platform). See Epic 7, Story 7.1.

**CMUX Markdown Surfaces ↔ Quick-Fix:** cmux markdown surfaces serve as a primary developer review pattern in quick-fix Phases 1-2. The quick-fix skill renders implementation plans and file diffs to cmux surfaces for developer review and approval before changes are applied. This is a direct integration — not optional detect-and-adapt — within the quick-fix workflow.

**momentum:refine ↔ momentum:epic-grooming:** momentum:refine delegates taxonomy analysis and story reassignment to momentum:epic-grooming as a substep during backlog refinement. Graceful degradation applies: if momentum:epic-grooming is absent, refine skips the taxonomy substep and continues with the remaining refinement work.

**momentum:feature-status ↔ Impetus startup-preflight:** Impetus reads `.claude/momentum/feature-status.md` at session start (inside startup-preflight, one Bash call, inline hash computation — Decision 46). Cache state drives greeting behavior: `fresh` → display cached feature summary inline; `stale` → offer refresh; `no-features` → silent skip; `no-cache` → suggest running `/momentum:feature-status`. The feature-status skill itself is invoked on-demand (user request or retro Phase 6 trigger — Decision 47) — Impetus never spawns it autonomously during greeting.

**momentum:feature-status ↔ momentum:retro:** Retro orchestrator spawns `/momentum:feature-status` at Phase 6 close (after verification, before sprint summary write) to refresh the feature cache for the next session. This is a sequential dependency: feature-status runs first, its cache output is read by the retro orchestrator to populate the "Features Advanced" section of the sprint summary (Decision 47).

**momentum:feature-grooming ↔ momentum:feature-status:** `momentum:feature-grooming` writes features.json and calls `momentum-tools feature-status-hash` post-write to invalidate the feature-status cache. `momentum:feature-status` reads features.json for display. This ensures the HTML dashboard and YAML cache are always considered stale after a grooming session, triggering a refresh on the next Impetus startup-preflight check.

---

## Validation Summary (Steps 7–8)

### Dual-Reviewer Pass Results

Adversarial validation conducted per the dual-reviewer pattern from VFL framework (HANDOFF-BRIEF-001 §Provenance). Enumerator (systematic) + Adversary (failure-focused) passes run against the full document.

**10 findings triaged. All resolved:**

| Finding | Severity | Resolution |
|---|---|---|
| A-1: context:fork + productive waiting contradiction | Revised to Low | Resolved: foreground/background is orthogonal to context:fork isolation. Background subagents confirmed in Claude Code docs. Decision 4c updated. |
| A-2: Global rules auto-load stated as unconditional | High | Fixed: subsystem 4 now states conditional on first `/momentum:impetus` invocation — Impetus writes rules to `~/.claude/rules/` on first run; no separate `momentum setup` CLI (eliminated 2026-03-18) |
| A-3: Copied global rules go stale | High | Fixed: update mechanism added to Decision 5a; Impetus surfaces version-drift warning |
| A-4: Plugin-agent invocation assumed, not verified | High | Resolved (2026-03-18): `context: fork` is a SKILL.md frontmatter field, not a plugin-only feature. code-reviewer and architecture-guard are `context: fork` SKILL.md files. Plugin model adopted (2026-04-03) for deployment packaging — `context: fork` remains a SKILL.md feature within the plugin. |
| A-5: VFL reviewer output unbounded | Medium | Fixed: reviewer output bound added to Decision 3a |
| A-6: Gate vs. proposal distinction undefined | Medium | Fixed: Decision 5b table now includes Type column; one hard gate identified |
| E-1: Provenance scanner has no home | Low | Fixed: placed in momentum/references/provenance-scan.md |
| E-2: Custom MCP server has no source location | Low | Fixed: mcp/findings-server/ added to repository structure |
| E-4: Version pre-commit hook type ambiguous | Low | Fixed: clarified as standard git pre-commit hook (Husky/pre-commit framework) |
| A-7: Confidence weighting unresolved | Low | Fixed: implementation-time decision noted in Decision 3b |

### Architecture Status

**Complete.** All 10 subsystems covered, all 6 NFRs addressed, all 10 potential conflict points specified, all adversarial findings resolved. Momentum is a Claude Code plugin (adopted 2026-04-03). `context: fork` is a SKILL.md feature within the plugin. Skills namespaced under `momentum:`. Workflow modules converted to proper skills.

---

## Sprint Story Lifecycle

> _Added 2026-03-21: Parallel story execution model. Revised 2026-03-21: Unified tracking — Momentum metadata lives in sprint-status.yaml alongside BMAD's development_status. No separate story spec files._

### Story State Machine

> _Revised 2026-04-01: New story stages (verify, closed-incomplete). Story IDs changed to kebab-case slugs. All status writes go through momentum:sprint-manager._
> _Revised 2026-04-02: momentum:sprint-manager subagent replaced by momentum-tools.py sprint CLI. AVFL per-story replaced by AVFL per-sprint (Decision 31). verify stage updated for Phase 3 developer-confirmation model._

```
backlog → ready-for-dev → in-progress → review → verify → done
```

- **`backlog`** — story exists in epics.md/sprint-status.yaml, no story file yet
- **`ready-for-dev`** — story file created, waiting to be picked into a sprint
- **`in-progress`** — sprint-dev agent actively working it (worktree active)
- **`review`** — worktree merged to main, awaiting sprint-level AVFL (automated batch after all sprint stories merge, per Decision 31)
- **`verify`** — AVFL passed, behavioral verification running (developer-confirmation checklist in Phase 3; automated via momentum-verify in future phases)
- **`done`** — verified, complete
- **`dropped`** — removed, obsolete or duplicate (pre-development cancellation)
- **`closed-incomplete`** — story was in a sprint that was force-closed before completion; migrated to next sprint or dropped. Worktree preserved for reference.

**Epic-level statuses:**

- **`done-incomplete`** — Epic closed mid-execution. Some stories completed; others incomplete or dropped. Counts as "done" in accounting.

**Story ID format:** Globally unique kebab-case slugs. No epic encoding.

```
Good:  posttooluse-lint-hook
Good:  impetus-identity-redesign
Bad:   3-1-posttooluse-lint-hook   ← encodes epic, breaks on re-categorization
```

Collision resolution: add short qualifier suffix (`auth-refresh-api` vs `auth-refresh-ui`).

**Status update authority:** All writes to `stories/index.json` (status fields) and `sprints/index.json` go through `momentum-tools.py sprint` — a CLI tool with exclusive write authority over these files. No other agent or script writes to these files directly. Story file content (ACs, dev notes) is written by `momentum:create-story`. The sprint-manager executor subagent described in earlier architecture versions has been superseded by this CLI tool (Phase 2 decision).

### Sprint Tracking Schema — Folder-Based Model

> _Revised 2026-04-01: sprint-status.yaml is deprecated. Story and sprint state is now decomposed into a `stories/` folder and a `sprints/` folder. All status writes via momentum-tools.py sprint CLI (formerly momentum:sprint-manager subagent)._

**`stories/` folder** — one file per story (`stories/{slug}.md`). Created early at backlog stage as a stub (slug, title, epic, status). Fleshed out with full ACs, dev notes, and tasks during sprint planning via `momentum:create-story`. Story file content (ACs, dev notes) is written by `momentum:create-story`.

**`stories/index.json`** — lightweight lookup index. Each entry: slug, status, title, epic slug, story_file (boolean — whether fleshed out), depends_on, touches, priority (optional — `critical | high | medium | low`, default: `low`). Epic membership lives here, not in epics.md.

```json
{
  "posttooluse-lint-hook": {
    "status": "in-progress",
    "title": "PostToolUse lint and format hook",
    "epic": "quality-enforcement",
    "story_file": true,
    "depends_on": [],
    "touches": ["hooks/hooks.json"]
  },
  "impetus-identity-redesign": {
    "status": "ready-for-dev",
    "title": "Impetus Identity & Persona Section",
    "epic": "impetus-ux",
    "story_file": true,
    "depends_on": [],
    "touches": ["skills/impetus/workflow.md"]
  },
  "model-routing-frontmatter": {
    "status": "backlog",
    "title": "Model routing configured by frontmatter",
    "epic": "quality-enforcement",
    "story_file": false,
    "depends_on": [],
    "touches": []
  }
}
```

<!-- REVISED Phase 3: Added team composition, dependencies, and specs directory to sprint record schema per Decisions 25, 26, 29, 30. -->

**`sprints/` folder** — one file per sprint (`sprints/{slug}.json`). Contains: name, slug, stories list, locked flag, started/completed dates, team composition, dependency graph, and wave plan. One specs directory per sprint (`sprints/{slug}/specs/`) for Gherkin feature files. One sprint summary per sprint (`sprints/{slug}/sprint-summary.md`) written by the retro orchestrator at Phase 6 close (Decision 47).

**`sprints/index.json`** — which sprint is active, which is planning, list of completed sprints. Active and planning entries are objects (not slug strings) that carry sprint lifecycle state (Decision 36). The `status` field tracks position in the sprint lifecycle state machine. Completed entries track retro execution for lifecycle gate enforcement.

> _[Revised 2026-04-04: Active and planning entries enhanced with `status` field for sprint lifecycle state machine (Decision 36). Completed entries enhanced with `retro_run_at` for retro gate tracking. Existing fields (locked, stories, waves, team_composition, started, completed) unchanged.]_

**`sprints/{sprint-slug}/specs/`** — Gherkin feature files written during sprint planning (Decision 30). One file per story: `{story-slug}.feature`. These specs encode detailed behavioral expectations that only verifier agents access. Dev agents NEVER read this directory — verification is black-box by design. Story markdown files retain plain English ACs only; Gherkin is never written back to story files.

```json
// sprints/index.json
{
  "active": {
    "slug": "quality-hooks-sprint",
    "status": "active",           // "ready" | "active" | "done" — see Decision 36
    "locked": true,
    "stories": ["posttooluse-lint-hook", "pretooluse-file-protection"],
    "started": "2026-03-30",
    "completed": null
    // ... waves, team_composition as before
  },
  "planning": {
    "slug": "impetus-ux-sprint",
    "status": "planning",         // "planning" | "ready" — see Decision 36
    "locked": false,
    "stories": ["greeting-redesign", "session-stats"]
    // ... waves, team_composition as before
  },
  "completed": [
    {
      "slug": "bootstrap-sprint",
      "completed": "2026-03-28",
      "retro_run_at": "2026-03-29"  // null if retro not yet run
    }
  ]
}

// sprints/quality-hooks-sprint.json
{
  "name": "Quality Hooks Sprint",
  "slug": "quality-hooks-sprint",
  "stories": ["posttooluse-lint-hook", "pretooluse-file-protection", "stop-gate-quality-checks"],
  "locked": true,
  "started": "2026-03-30",
  "completed": null,
  "team": {
    "roles": [
      {"role": "dev", "guidelines": "path/to/project-dev-guidelines.md"},
      {"role": "qa", "guidelines": "path/to/project-qa-guidelines.md"}
    ],
    "story_assignments": {
      "posttooluse-lint-hook": {"role": "dev"},
      "pretooluse-file-protection": {"role": "dev"},
      "stop-gate-quality-checks": {"role": "dev"}
    }
  },
  "dependencies": {
    "stop-gate-quality-checks": ["posttooluse-lint-hook"]
  },
  "waves": [
    { "wave": 1, "stories": ["posttooluse-lint-hook", "pretooluse-file-protection"] },
    { "wave": 2, "stories": ["stop-gate-quality-checks"] }
  ]
}
```

**`epics.md`** — names, slugs, and descriptions only. No story lists. Pure documentation. Epic membership is tracked in `stories/index.json`.

**`sprint-status.yaml` is deprecated** — replaced by the folder-based model above. The `sprint-status-schema-decomposition` migration story handles the transition from sprint-status.yaml to the new structure.

**Write authority:** `momentum-tools.py sprint` is the sole writer of the `sprints/` folder and the `status` fields in `stories/index.json`. Story file content (ACs, dev notes, tasks) is written by `momentum:create-story`. Sprint-scoped Gherkin specs (`sprints/{sprint-slug}/specs/`) are written by the sprint-planning skill (`/momentum:sprint-planning`). No other agent or script writes to these files directly.

### Story Assignment Model

<!-- REVISED Phase 3: Replaced Next-Story Selection Rule. momentum:dev no longer selects stories autonomously. Story assignment is managed by the sprint-dev workflow (Impetus). -->

momentum:dev does NOT select its own stories. Story assignment is managed by the sprint-dev skill (`/momentum:sprint-dev`):

1. sprint-dev reads the active sprint record from `sprints/index.json`
2. sprint-dev resolves the dependency graph from story `depends_on` fields
3. sprint-dev identifies unblocked stories (all dependencies merged)
4. sprint-dev spawns one momentum:dev agent per unblocked story, passing the story file path and role-specific guidelines
5. When a story completes and merges, sprint-dev re-evaluates the dependency graph and spawns agents for newly unblocked stories

momentum:dev receives its story assignment as input — it never reads `stories/index.json` to choose what to work on. If momentum:dev is invoked standalone (outside a sprint context), the developer provides the story path directly.

### Session Journal Extension: `active_stories`

The session journal `active_story` field (singular) extends to `active_stories` (array) to support concurrent sessions:

```json
{
  "active_stories": [
    {
      "story_id": "posttooluse-lint-hook",
      "worktree_path": ".worktrees/story-posttooluse-lint-hook",
      "target_branch": "main",
      "phase": "Implement"
    },
    {
      "story_id": "sprint-status-schema",
      "worktree_path": null,
      "target_branch": "main",
      "phase": "ATDD"
    }
  ]
}
```

Impetus's session orientation must handle the multi-story case: when multiple stories are active, summarize all active sessions and their current phases.

### Parallel Story Execution Model (Always-Worktree — Standalone momentum:dev Only)

> _Note: The worktree model described in this section applies to STANDALONE `momentum:dev` invocations (dev called directly by the developer, not via sprint-dev). Sprint-dev uses sequential execution with commit-as-sync-point within an Agent Team (Decision 26) — no worktrees are needed within a team. This section documents the worktree model for standalone use cases; do not apply it to sprint-dev team execution._

Every standalone `momentum:dev` session runs in its own git worktree from the start — even if it appears to be the only session. This eliminates the mid-session file-change race (if Story A ran in main and Story B merged first, A would find changed files under it).

**Worktree naming convention:** `.worktrees/story-{story_id}` on branch `story/{story_id}`

**Target branch:** Captured at invocation via `git branch --show-current` (Bash tool). The worktree merges back to this branch on completion — not hardcoded to `main`.

**Worktree environment:** Git worktrees share the same `.git` directory — all project files, skills, config, and `.claude/` structure are available inside every worktree.

**`.worktrees/` directory:** Must be in `.gitignore` — worktrees are local execution environments, not committed artifacts.

**Concurrency limitation (single-developer):** Two sessions started within ~30 seconds of each other may both read the same story as `ready` before either writes `in_progress`. Mitigation: start sessions with a brief (~30s) offset. A lock file (`.worktrees/story-{story_id}.lock`) provides additional protection and should be checked before status write.

**Ready for:** Epic and story creation.

---

## Sprint Orchestration Architecture

<!-- REVISED Phase 3: Replaced Epic Orchestration Architecture with Sprint Orchestration Architecture. Waves replaced by dependency-driven team concurrency (Decision 25). AVFL moved from per-story to per-sprint (Decision 31). Epic commands replaced by sprint workflow modules. momentum-dev-auto section removed — momentum:dev simplified to pure executor, subsuming momentum-dev-auto's scope. dag-executor section removed — dependency-driven model replaces wave-based scheduler. -->

> _Added 2026-03-26: Epic orchestration model. Revised 2026-04-02: Replaced with sprint-centric, dependency-driven model per Phase 3 Decisions 24-31._

The sprint is the primary unit of planned work. The lifecycle is:

```
backlog (mutable) → /momentum:sprint-planning (story selection + team composition + Gherkin specs + AVFL)
  → /momentum:sprint-dev (dependency-driven execution + post-merge AVFL + verification)
  → /momentum:retro (structured handoff from agent logs)
  → backlog (next cycle)
```

**Sprint immutability rule:** Once `momentum-tools sprint activate` is called, the sprint is locked. No patching in-place. Recovery path: close sprint (set status `closed-incomplete`), migrate incomplete stories to next sprint backlog.

### Sprint Planning Workflow (Decision 29)

Sprint planning is a dedicated skill (`/momentum:sprint-planning`) with 8 steps. Invoked by Impetus when the developer selects "Plan a sprint" from the session menu, or directly by the user.

<critical>Use task tracking (TaskCreate/TaskUpdate) for sprint planning steps — this prevents context drift in long runs. Create a task per step at planning start. Every step entry updates the corresponding task to in_progress; every step exit updates to completed. Ad-hoc narrative summaries are not a substitute for tool-queryable task state.</critical>

1. **Backlog presentation (Synthesis-First)** — Read the master plan documents (`prd.md`, product brief) to understand strategic priorities. Read the most recent sprint summary (`_bmad-output/implementation-artifacts/sprints/{last-sprint-slug}/sprint-summary.md`) for "what just happened" context — non-blocking if absent. Read `stories/index.json`, group by epic, exclude terminal states. Within each epic group, sort by priority (critical > high > medium > low), then by dependency depth, then alphabetical. Run a staleness check: for each story with status `ready-for-dev` or `in-progress`, check `git log` for commits touching the story's `touches` paths — if substantial implementation commits exist, flag the story as potentially already implemented and exclude it from recommendations (surface in a separate "Potentially stale" section with evidence). Lead with a synthesis section: 3-5 prioritized recommendations with brief rationale for each, informed by the master plan's current priorities, dependency readiness, and backlog state. Present the full backlog below the recommendations as secondary reference material. If master plan documents are missing, fall back to the current behavior (sorted backlog) with a warning.
2. **Story selection** — developer selects 3-8 stories, register via momentum-tools sprint plan
3. **Story fleshing-out** — spawn `/momentum:create-story` for each stub; developer approves each
4. **Gherkin spec generation** — write detailed `.feature` files to `sprints/{sprint-slug}/specs/`; story files retain plain English ACs only (Decision 30). After generation, a **spec quality pre-check gate** validates each `.feature` file: checks structural validity (valid Gherkin syntax, proper Given/When/Then flow), outsider-test compliance (scenarios testable without implementation knowledge), and template conformance (consistent tagging, background usage, scenario outline patterns). Specs that fail the pre-check are revised before dev agents spawn — catching spec-quality issues early avoids downstream E2E Validator findings that trace back to ambiguous specifications.
5. **Execution plan and team composition** — analyze stories to determine agent roles, project guidelines, dependency graph, and execution waves (Decision 26: two-layer agent model). Validate the planned `team` object against workflow-declared required roles (Decision 41: Team Composition Declarations) — if a required role is missing from the plan, surface the gap before activation.
6. **AVFL validation** — single AVFL pass on the complete sprint plan (all stories together, not per-story — Decision 31)
7. **Developer review** — present full plan for approval; developer can request adjustments
8. **Sprint activation** — call `momentum-tools sprint activate`; log the decision

**Priority management CLI (sprint subcommands):**
- `sprint set-priority --story <slug> --priority <level>` — Set story priority (`critical | high | medium | low`)
- `sprint stories --priority <level|all>` — Query stories filtered by priority level

### Dependency-Driven Execution (Decision 25: Teams Over Waves)

The DAG topology is derived from `depends_on` fields in `stories/index.json`. Execution is dependency-driven, not wave-sequential:

1. Identify unblocked stories (no dependencies, or all dependencies already `done`)
2. Spawn one momentum:dev agent per unblocked story (each in its own worktree)
3. When a story completes and merges, re-evaluate the dependency graph
4. Spawn agents for newly unblocked stories
5. Repeat until all sprint stories have merged

Wave assignments in the sprint record are informational (planning visualization) — execution order is determined by dependency resolution at runtime. Multiple stories can run concurrently if they share no dependencies. A story with dependencies waits until ALL its blockers have merged.

### Two-Layer Agent Model (Decision 26)

Momentum provides generic agent roles with orchestration patterns:
- **Dev** — implements stories in worktrees
- **QA** — reviews code against acceptance criteria
- **E2E Validator** — validates end-to-end behavior against Gherkin specs
- **Architect Guard** — checks pattern drift against architecture decisions

Projects provide stack-specific guidelines per role (e.g., "Frontend Dev uses Kotlin Multiplatform + Compose, TDD required"). Sprint planning wires the layers together: for each story, determine which roles apply based on `change_type` and `touches`, then attach the project's guidelines for those roles. The team composition is stored in the sprint record.

### Agent Guidelines Generation (FR61a)

The `agent-guidelines` skill (`/momentum:agent-guidelines`) creates the project-specific guidelines that the two-layer model requires. It operationalizes the research findings from the Agent Guidelines Authoring research (see `_bmad-output/planning-artifacts/research/technical-agent-guidelines-authoring-research-2026-04-03.md`).

**Design principles (evidence-based):**
- Instruction budget is ~100-150 slots; every rule competes with every other rule
- Path-scoped rules (`.claude/rules/*.md` with `paths:` frontmatter) load only when matching files are touched — zero cost when irrelevant
- Three-layer architecture: Layer 1 (path-scoped rules, 30-80 lines) → Layer 2 (reference docs, 100-300 lines, on-demand) → Layer 3 (skills, unlimited, invoked)
- Correct stale training data, don't teach basics — prohibitions over aspirations
- Pin versions, date-stamp, put critical prohibitions first

**Workflow phases:**

1. **Discover** — Parallel subagents (Sonnet/medium) scan build files, existing `.claude/rules/`, test configs, and source patterns to produce a structured technology profile with versions
2. **Research** — Parallel subagents (Sonnet/medium) with web search perform 2-3 focused queries per detected technology for breaking changes, deprecated APIs, and current best practices. Outputs prohibition-format corrections. Does not invoke the full research skill — stays light; user can escalate if needed
3. **Consult** — Interactive back-and-forth with the developer across decision points: technology inventory confirmation, existing guidelines audit, testing framework recommendations, validation approach (which roles need guidelines), path scope design (glob patterns), and content depth (Layer 1/2/3 decisions)
4. **Generate** — Parallel subagents (Sonnet/high) produce artifacts from templates: path-scoped `.claude/rules/*.md` files, reference docs in `docs/references/`, and CLAUDE.md pointer updates
5. **Validate** — AVFL checkpoint profile on all generated artifacts

**Key architectural choices:**
- Opus for orchestration (consultation needs nuance), Sonnet for all subagents (scoped tasks)
- Detection heuristics live in a reference file (`references/detection-heuristics.md`), not code — extensible, AVFL-validatable, human-editable
- Consultation happens before generation — don't waste compute on artifacts the user doesn't want
- Generic agents in Momentum carry practice/workflow; generated project rules carry technology corrections — they compose automatically through the file system at runtime via path-scoped loading

### Sprint Execution Flow (sprint-dev skill)

sprint-dev is a dedicated skill (`/momentum:sprint-dev`) with 6 phases. Invoked by Impetus when the developer selects "Continue sprint" from the session menu, or directly by the user:

**Phase 1: Initialization**
- Read active sprint from `sprints/index.json`; validate locked state
- Build dependency graph from story `depends_on` fields
- Initialize spawn registry as an empty map — tracks every agent spawned during this session, keyed by `{story_slug}::{role}` (e.g., `refine-skill::dev`, `sprint::qa-reviewer`). The registry survives the Phase 2 → Phase 3 → Phase 2 loop; it is never reset between phases and is not persisted to disk.
- Create a task per story via TaskCreate for progress tracking
- Log sprint start

<critical>Use task tracking (TaskCreate/TaskUpdate) for sprint phases — this prevents context drift in long runs. Every phase entry updates the corresponding task to in_progress; every phase exit updates to completed. Ad-hoc narrative summaries are not a substitute for tool-queryable task state.</critical>

**Phase 2: Team Spawn**
- Identify unblocked stories
- Transition each to `in-progress` via `momentum-tools sprint status-transition`
- Before spawning any agent, check the spawn registry for an existing `{story_slug}::{role}` entry. If the entry exists, skip the spawn (suppressed duplicate). If no entry exists, spawn the agent and register the `{story_slug}::{role}` tuple.
- Within the team, execute the first unblocked story sequentially; subsequent unblocked stories execute one at a time after each commit-as-sync-point (see Agent Teams model). Parallel execution of independent stories requires separate terminal sessions, not within a single team session.
- Each agent produces structured completion output

**Phase 3: Progress Tracking Loop**
- Monitor spawned agents via task status
- On story completion: propose merge to developer (merge gate — never auto-execute)
- After merge: transition to `review`, re-evaluate dependency graph, spawn newly unblocked stories (spawn registry correctly allows spawns for never-spawned stories while blocking duplicates for already-assigned stories). Retry agents replace the existing registry entry rather than adding a second one.
- Repeat until all stories have merged

**Phase 4: Post-Merge AVFL Stop Gate (Decision 31: AVFL at Sprint Level; Decision 34: Scan Profile)**
- Run AVFL in **scan profile** on the full codebase (all sprint changes together): all 4 lenses, dual reviewers (Enumerator + Adversary), maximum skepticism (level 3), consolidation with cross-check confidence
- Zero fix iterations — AVFL scan produces a scored findings list only (no fix loop within AVFL)
- AVFL no longer runs per-story — it runs once after ALL stories merge
- **Stop gate:** AVFL runs to completion and presents all findings to the developer before any downstream review or fix phase begins. No fixes are initiated until the developer acknowledges the findings. This is a hard pause — the orchestrator waits for developer acknowledgment.
- This catches cross-story integration issues that per-story AVFL would miss

**Phase 4b: Per-Story Code Review**
- After developer acknowledges AVFL findings, spawn `momentum:code-reviewer` independently for each story's merged changeset. Each review scopes to the files in that story's `touches` array or the actual diff from the story merge commit.
- Code reviews run concurrently (one `momentum:code-reviewer` invocation per story). Spawn registry checks apply — each `{story_slug}::code-reviewer` entry is registered.
- Each code review produces structured findings independently of the AVFL scan.

**Phase 4c: Consolidated Fix Queue**
- Merge AVFL findings (Phase 4) and per-story code review findings (Phase 4b) into a single prioritized fix queue.
- Present the consolidated queue to the developer. Developer picks fix/defer for each item.
- No fix agents are spawned until the developer confirms the fix list.

**Phase 4d: Targeted Fixes + Selective Re-review**
- Spawn fix agents for developer-accepted items from the consolidated queue. Each fix agent receives a scoped subset of findings.
- After fixes complete, re-run only the specific reviewers whose findings were addressed (selective re-review, not full re-run of all lenses and code reviews). If fixes are substantial enough to introduce new concerns, a lightweight AVFL re-scan is triggered automatically.
- Findings from re-review are presented; the cycle repeats until the developer accepts the final state.

**Phase 5: Hybrid Agent Team Resolution (Decision 34)**
- Agent Team operates concurrently on main branch (no worktrees) — receives any remaining unresolved items plus full-codebase verification scope
- **Dev Agent** — fixes any remaining findings from Phases 4-4d
- **QA Agent** — reviews merged code against all sprint story ACs. Produces findings per story.
- **E2E Validator** — tests running behavior with external tools against Gherkin specs in `sprints/{sprint-slug}/specs/`. Black-box: fundamentally different from AVFL's file-content validation — tests live system behavior, not static content.
- **Architect Guard** — checks for pattern drift against architecture decisions. Flags deviations from Decision 26 team model, coding conventions, and project guidelines.
- All four run concurrently on the full integrated codebase
- Findings are consolidated and presented to the developer as a fix queue
- Fix loop within the team: re-run affected reviewers after fixes until clean or developer accepts remaining items
- Unresolved findings become follow-up stories or backlog items

Phase 5 agents are checked against the spawn registry — each reviewer role (e.g., `sprint::qa-reviewer`, `sprint::e2e-validator`, `sprint::architect-guard`) is spawned at most once per sprint execution.

**Phase 6: Verification (Decision 30: Black-Box)**
- Developer-confirmation checklist derived from Gherkin scenarios (Phase 3 implementation)
- Each Gherkin scenario becomes a checkbox item the developer confirms
- Unconfirmed items become findings to address or follow-up stories
- On full confirmation: transition all stories to `done`
- Future: automated verification via momentum-verify skill replaces manual checklist

**Phase 7: Sprint Completion**
- Run `momentum-tools sprint complete` to archive the sprint
- Surface summary: stories completed, merge order, AVFL findings, verification results
- Suggest retrospective as next step
- The retro workflow writes `sprints/{sprint-slug}/sprint-summary.md` at Phase 6 close (Decision 47) — sprint-dev does not write it

### Agent Pool Governance

**Pool cap:** Configurable, default 12 concurrent agents. Applied at spawn time.

**AVFL at sprint level (Decision 31):** AVFL does NOT run per-story. momentum:dev has no AVFL. A single AVFL pass runs after ALL sprint stories merge (Phase 4 of sprint-dev). This is a deliberate architectural change from the pre-Phase-3 model where AVFL was embedded in each story agent.

**Merge gate:** Every merge requires explicit developer confirmation. sprint-dev proposes the merge and waits — never auto-executes. momentum:dev signals "ready to merge" in its structured completion output.

**Pre-flight checks before sprint execution:**
1. Active sprint exists and is locked
2. Topological sort validity / cycle detection
3. Dangling reference detection — every `depends_on` key must exist in sprint story list
4. Story file existence for all sprint stories
5. Correct story status — unblocked stories must be `ready-for-dev`

### momentum:dev — Simplified Pure Executor

<!-- REVISED Phase 3: momentum:dev simplified to pure executor. momentum-dev-auto is subsumed — the simplified momentum:dev has no AVFL, no status writes, no DoD supplement, no code review offer, making it functionally equivalent to what momentum-dev-auto was designed to be. -->

momentum:dev is a pure executor: worktree setup, story implementation (spawning agents directly per story instructions), and structured completion output. It does NOT:
- Run AVFL (moved to sprint-dev Phase 4)
- Write status transitions (handled by sprint-dev after merge)
- Apply DoD supplement (moved to sprint-level verification)
- Offer code review (orthogonal concern managed by caller)
- Write agent logs (removed — DuckDB transcript audit is the sole evidence source per Decision 24/27)

momentum:dev does NOT invoke bmad-dev-story as an indirection layer — the current dev/workflow.md spawns agents directly. momentum:dev emits structured JSON completion output that sprint-dev parses: status, files modified, test results.

**Note:** The pre-Phase-3 `momentum-dev-auto` variant (background-safe, no ask gates) is subsumed by this simplified momentum:dev. With AVFL, status transitions, DoD, and code review removed, momentum:dev itself is now a pure executor suitable for both interactive and background execution.

---

### Retro → Planning Handoff via Unified Intake Queue

> _[Updated 2026-04-14 (DEC-007, story: retro-triage-handoff): The prior `triage-inbox.md` contract is **retired**. Retro now writes handoff events directly to the unified `_bmad-output/implementation-artifacts/intake-queue.jsonl`. Sprint-planning Step 1 reads open handoff entries from the same file. No manual re-injection of retro findings into planning is required.]_

After each sprint retro (Phase 5.5), un-actioned findings are written to `intake-queue.jsonl` as JSONL events. Sprint-planning Step 1 reads these open entries and surfaces them alongside the backlog — closing the retro → planning loop without developer re-injection.

**Artifact:** `_bmad-output/implementation-artifacts/intake-queue.jsonl` (per DEC-007)

**Write path:** `momentum-tools intake-queue append --source retro --kind handoff ...`
**Read path:** `momentum-tools intake-queue list --source retro --kind handoff --status open`
**Consume path:** `momentum-tools intake-queue consume --id ID --outcome-ref STORY_SLUG`

**Event schema:**
```jsonl
{
  "id": "iq-YYYYMMDDHHMMSS-XXXXXXXX",
  "timestamp": "2026-04-15T17:34:00Z",
  "source": "retro",
  "kind": "handoff",
  "status": "open",
  "title": "Short title of the finding",
  "description": "Full description of the finding",
  "sprint_slug": "sprint-2026-04-08",
  "feature_slug": "material-3-design-system",
  "story_type": "defect",
  "feature_state_transition": {
    "feature_slug": "...",
    "prior_state": "partial",
    "observed_state": "partial",
    "evidence": "..."
  },
  "failure_diagnosis": {
    "attempted": "...",
    "didnt_work": "...",
    "learned": "..."
  }
}
```

**Field semantics:**
- `source: "retro"` — written by `momentum:retro` Phase 5.5
- `kind: "handoff"` — un-actioned retro finding intended for next planning cycle
- `status` — `open` (awaiting planning review) | `consumed` (promoted to story or explicitly rejected)
- `sprint_slug` — provenance: which retro produced this finding
- `feature_slug` — associated feature, if the finding is feature-bound (per DEC-005 D1)
- `story_type` — suggested story type for downstream stub creation (per DEC-005 D5)
- `feature_state_transition` — present when the finding involves a feature-state hygiene event (per DEC-005 D8): feature X asserted Done but retro observed regression
- `failure_diagnosis` — present when the finding names a specific failure (per DEC-005 D7): what was attempted, what didn't work, what was learned

**Consumption:** When a handoff item is promoted to a story stub during sprint-planning Step 2, `momentum-tools intake-queue consume --id ID --outcome-ref STORY_SLUG` marks it consumed. Items remain in the file (append-only); consumed items are skipped by `--status open` queries.

**DEC-005 alignment (D7, D8):**
- D8 — Retro gains feature-state hygienist role: `feature_state_transition` carries the observed state transition for any feature touched by the sprint
- D7 — Failure as legitimate diagnostic category: `failure_diagnosis` names what was attempted, what failed, and what was learned — not softened into generic "learnings"

**Retired:** The prior `triage-inbox.md` contract (YAML entries, `source: "epic-N-retro"`, `type: action-item | incomplete-story | blocker-resolution`) is superseded. The `triage-inbox.md` file was never created; its design is replaced by this unified JSONL contract per DEC-007.

---

### `intake-queue.jsonl` Schema Contract (DEC-007)

<!-- Added 2026-04-14: Unified triage/retro capture artifact per DEC-007. Supersedes the retired triage-inbox.md contract above. -->

Single source of truth for triage-adjacent items that don't become stories immediately — SHAPING / DEFER / REJECT outcomes from `momentum:triage` and handoff events from `momentum:retro`. Per **DEC-007 (2026-04-14)**.

**Path:** `_bmad-output/implementation-artifacts/intake-queue.jsonl` (per-project, not global)

**Format:** Append-only JSONL event log. One JSON object per line. Never truncated.

**Base schema fields (all entries):**

| Field | Type | Values / Notes |
|---|---|---|
| `id` | string | Unique event id (ULID or timestamped slug) |
| `source` | string | `triage` \| `retro` \| `assessment` (future upstreams welcome) |
| `kind` | string | `shape` \| `watch` \| `rejected` \| `handoff` |
| `title` | string | Short human-readable title |
| `description` | string | One-to-three-sentence summary |
| `status` | string | `open` \| `consumed` (initial write is always `open`) |
| `timestamp` | string | ISO-8601 UTC timestamp |

**Optional fields (present when applicable):**

| Field | Used by | Notes |
|---|---|---|
| `sprint_slug` | retro handoffs | Provenance — the sprint the handoff originated from |
| `feature_slug` | any | Existing feature the item relates to |
| `story_slug` | any | Existing story the item relates to |

**Retro-specific optional fields (DEC-005 framing):**

| Field | Shape | When present |
|---|---|---|
| `feature_state_transition` | `{ feature_slug, prior_state, observed_state, evidence }` | Retro observed a D8 feature-state change (e.g., Done → Partial) |
| `failure_diagnosis` | `{ attempted, didnt_work, learned }` | Retro named a D7 diagnosed failure |
| `suggested_feature_slug` | string | Retro finding implies new feature-bearing work (DEC-005 D1) |
| `story_type` | string | `feature` \| `maintenance` \| `defect` \| `exploration` \| `practice` (DEC-005 D5) |
| `evidence_refs` | array of strings | Pointers back to the findings document (e.g., section anchor or line range of `retro-transcript-audit.md`) |

**Writers (CLI-only; never direct file edits):**

- `momentum:triage` — appends `shape` / `watch` / `rejected` entries via `momentum-tools intake-queue append`.
- `momentum:retro` — appends `handoff` entries via `momentum-tools intake-queue append` (Phase 5.5 — Handoff to Intake Queue).

Both producers write exclusively through the `momentum-tools` CLI. Skills never open this file for direct mutation — matches the orchestrator-purity pattern used elsewhere in the practice.

**Readers:**

- `momentum:triage` — reads on start to re-surface open `shape` / `watch` / `handoff` entries for re-classification or promotion.
- `momentum:sprint-planning` — Phase A.6 reads entries filtered to `source: "retro"`, `kind: "handoff"`, `status: "open"` during backlog synthesis; Phase C surfaces them in a labeled "Open handoff items from recent retros" section (see Decision 29 update below).
- Potentially `momentum:refine` in a future hygiene pass — TBD.

**Consumption semantics:** When an entry is acted on (promoted to a story via intake, distilled, decided, or explicitly rejected), its `status` is updated to `consumed` or `rejected` with an outcome reference (e.g., `outcome: "story:slug-name"` or `outcome: "dec-NNN"`) via the CLI update path. Entries are never deleted — full history preserved.

**Replaces:** the retired `triage-inbox.md` contract above; a never-built `retro-summary.json` handoff artifact.

---

### `momentum:triage` Architecture (DEC-007, DEC-005)

<!-- Added 2026-04-14: Entry-point and topology for the multi-item batch classification orchestrator. -->

`momentum:triage` is the missing orchestrator that sits between upstream observation sources (mid-session conversation, retro Priority Action Items, assessment recommendations) and the per-item executors (`momentum:intake`, `momentum:distill`, `momentum:decision`). It fills the structural gap where `momentum:intake` is single-item-only but real-world triage is inherently multi-item.

**Entry point:** Impetus dispatches from the `[3] Triage` menu item (replaces the placeholder in `skills/momentum/skills/impetus/workflow.md:403` and `skills/momentum/skills/impetus/SKILL.md:63`). Also independently invocable as `/momentum:triage` and programmatically callable from retro Phase 5 or sprint-planning backlog synthesis with an explicit observation list.

**Classification taxonomy (six classes):** ARTIFACT / DISTILL / DECISION / SHAPING / DEFER / REJECT. Classification runs **inline in main context** — no subagent spawn for the classification judgment itself (it is context-dependent and cheap, and the orchestrator holds session context triage needs).

**Enrichment for ARTIFACT items:** each ARTIFACT is enriched with `feature_slug` (read from `features.json` — DEC-005 D1), `story_type` (DEC-005 D5 — default `feature`), suggested epic (DEC-005 D2 — DDD sub-domain aware), priority, and proposed dependencies. Enrichment is also inline by default.

**Optional Explore subagents:** for enrichment work at scale — duplicate detection against `stories/index.json` and feature-assignment suggestion against `features.json` — optional Explore subagents may be spawned when observation count ≥ 5 or the developer explicitly requests deeper enrichment. For typical 2–3 observation sessions, triage does everything inline.

**Batch approval UX:** mirrors the pattern established by `momentum:refine` Step 9 — consolidated findings list; accept / modify / reject per item; batch operations (accept-all / reject-all) when N ≥ 5. No silent writes; the developer approves before any delegation or CLI write fires.

**Execution — delegation vs. direct write:**

| Class | Action | Target |
|---|---|---|
| ARTIFACT | Delegates to `momentum:intake` (per item) | `stories/{slug}.md` + `stories/index.json` |
| DISTILL | Delegates to `momentum:distill` (per item) | Target practice file (rule / skill / reference) |
| DECISION | Delegates to `momentum:decision` (per item) | `planning-artifacts/decisions/dec-NNN-*.md` |
| SHAPING | Direct CLI write to `intake-queue.jsonl` | `kind: "shape"` |
| DEFER | Direct CLI write to `intake-queue.jsonl` | `kind: "watch"` |
| REJECT | Direct CLI write to `intake-queue.jsonl` | `kind: "rejected"` + reason |

Executor skills (`intake`, `distill`, `decision`) retain their existing model and effort settings. Triage does not bypass them.

**Re-surfacing on start:** triage reads `intake-queue.jsonl` on session start to re-surface open `shape` / `watch` / `handoff` entries — items the developer captured previously but has not yet promoted, distilled, decided, or rejected. Handoff-kind entries (produced by retro — see `retro-triage-handoff` story) flow through the same classify / promote / continue-watching / reject UX as shape/watch entries.

**No gap-check (DEC-005 D10):** triage performs no value-floor analysis. Classification only. Gap-check lives at refinement, sprint-planning, and retro.

**Terminal-state awareness (DEC-005 D6):** items whose underlying feature is `Abandoned` or `Rejected` are auto-suggested for REJECT on re-surface.

**Elevated effort (`high`):** justified because triage outputs are unvalidated downstream — the developer batch-approves but there is no AVFL on the delegated intake / distill / decision calls within the triage flow. Matches the pattern used for `momentum:refine` and `momentum:sprint-planning`.

**Implementation story:** `triage-skill`. Implements DEC-005 D1/D2/D5/D6/D10 and DEC-007 D1 in a single sprint. Sibling story `retro-triage-handoff` adds the retro producer side once triage ships.

---

### Agent Logging Infrastructure (Decision 24) — Historical

<!-- Added Phase 3: Agent logging as foundational infrastructure for retrospectives and observability. -->
<!-- Updated 2026-04-08: Agent journal write infrastructure removed. DuckDB transcript audit (Decision 27) is now the sole evidence source. -->

> _[Updated 2026-04-08: The agent journal write infrastructure — `momentum-tools log` CLI, sprint-log directory writes, SubagentStart/SubagentStop hooks — has been removed as of sprint-2026-04-08. Sprint-2026-04-06 retro demonstrated that DuckDB transcript audit (Decision 27) produces an order of magnitude more signal than milestone logs (246 user messages + 97 subagents + 806 tool events vs. 2 findings from 24 log events). The transcript audit pipeline is now the sole evidence source for retrospectives. No agent in the system writes structured JSONL logs. The `momentum-tools log` CLI subcommand, sprint-logs directory, and SubagentStart/SubagentStop hooks are all removed.]_

This section is retained for historical context. The original design called for per-agent JSONL logging via `momentum-tools log` with exclusive write authority per agent file, 8 event types, and hook-based observability via SubagentStart/SubagentStop lifecycle hooks. In practice, the overhead of manual milestone logging produced sparse, low-signal data compared to the comprehensive evidence available in raw session transcripts via DuckDB preprocessing (Decision 27).

### Gherkin Specification Separation (Decision 30)

<!-- Added Phase 3: Black-box behavioral validation via separated Gherkin specs. -->

Story files and Gherkin specs are deliberately separated to enforce black-box validation:

- **Story files** (`stories/{slug}.md`) — contain plain English acceptance criteria. Dev agents read these to understand intent.
- **Gherkin specs** (`sprints/{sprint-slug}/specs/{story-slug}.feature`) — contain detailed behavioral expectations. Only verifier agents read these.

**Key constraints:**
- Gherkin specs are written during sprint planning (Step 4), before any code exists
- A spec quality pre-check gate runs after generation (Step 4): validates structure, outsider-test compliance, and template conformance before dev agents spawn
- Dev agents NEVER access `sprints/{sprint-slug}/specs/` — this is a protection boundary
- Gherkin is NEVER written back to story files
- Specs are validated post-implementation by different agents than those who wrote the code
- This separation enables true black-box behavioral validation
- E2E Validator findings about untestable scenarios are tagged `spec-quality` and surfaced in a dedicated retro section (see Decision 30 spec-quality feedback loop)

---

## Phase 3 Architecture Decisions (24-31)

<!-- Added Phase 3: Decisions from the Phase 3 plan that govern sprint execution, agent logging, and team model. -->

**Decision 24 — Agent Logging Infrastructure (Historical — Removed 2026-04-08)**
The agent journal write infrastructure (`momentum-tools log` CLI, sprint-log directory writes, SubagentStart/SubagentStop hooks) has been removed as of sprint-2026-04-08. DuckDB transcript audit (Decision 27) is now the sole evidence source for retrospectives. Raw session JSONL transcripts provide comprehensive coverage (user messages, subagent events, tool calls) that milestone logs could not match. See Agent Logging Infrastructure (Historical) section for original design context.

**Decision 25 — Teams Over Waves**
Dependency-driven concurrency replaces rigid wave tiers. The sprint-dev skill (`/momentum:sprint-dev`) spawns agents for unblocked stories and spawns more as dependencies complete. Wave assignments in sprint records are informational for planning visualization — execution order is determined by dependency resolution at runtime. See Dependency-Driven Execution section.

**Decision 26 — Two-Layer Agent Model**
Momentum provides generic roles (Dev, QA, E2E Validator, Architect Guard). Projects provide role-specific stack guidelines. Sprint planning (`/momentum:sprint-planning`) wires the layers together — for each story, determine which roles apply based on `change_type` and `touches`, then attach the project's guidelines. Team composition is stored in the sprint record. Agent Teams share a working directory; sequential story execution with commit-as-sync-point means no worktree needed within a team. Teammates load skills from project/user settings, not from `.agent.md` `skills` frontmatter — dev agents get workflow instructions through their spawn prompt. See Two-Layer Agent Model section.

The specialist classification table (dev-skills, dev-build, dev-frontend, dev base) is a **canonical lookup**, not ad-hoc LLM derivation. `momentum-tools specialist-classify` is the deterministic implementation — it maps `change_type` to specialist and validator set. When a story has multiple change types, the dominant change type determines the specialist. This ensures identical inputs always produce identical role assignments across sessions and agents.

**Decision 27 — Transcript Audit Retro (Revised 2026-04-06)**

> _[Revised 2026-04-06: Major rewrite. Replaced milestone-log-based two-output retro with DuckDB preprocessing + auditor team. Evidence: sprint-2026-04-06 milestone logs produced 2 findings from 24 events; transcript audit produced 37 findings from 246 user messages + 97 subagents + 806 tool events. Order of magnitude more signal.]_

Retro is restructured as a two-wave transcript audit architecture. Milestone logs (Decision 24) are supplementary, not the primary data source.

**Wave 1: DuckDB Preprocessing (no agents)**
Automated extraction using `transcript-query.py` (DuckDB wrapper). Reads Claude Code session JSONL files directly via SQL. Session discovery finds JSONL files by date range matching the sprint's started/completed dates in `~/.claude/projects/{project}/`. Subagent transcripts mapped via `{session-id}/subagents/` directories.

New dependency: DuckDB (`pip install duckdb`). The tool checks and auto-installs if missing.

Extraction queries (run automatically):

| Extract | What | Source |
|---|---|---|
| `user-messages.jsonl` | All human-typed prompts across all sessions | Session JSONL files |
| `agent-summaries.jsonl` | Per-subagent digest: prompt, outcome, tool counts, error count, turns | Subagent JSONL files |
| `errors.jsonl` | Tool errors using actual error indicators (`is_error` flag, `tool_use_error` responses) | All JSONL files |
| `team-messages.jsonl` | Inter-agent SendMessage and teammate-message content | Subagent JSONL files |

Output directory: `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/audit-extracts/`

`transcript-query.py` is standard retro tooling at a known path in the plugin, supporting both pre-built queries and ad-hoc SQL via `transcript-query.py sql "..."`.

**Wave 2: Auditor Team (3 auditors + 1 documenter)**
Spawn 4 agents in parallel via TeamCreate:

- **auditor-human** — reads `user-messages.jsonl`. Identifies corrections, redirections, frustration signals, praise/approval, and decision points.
- **auditor-execution** — reads `agent-summaries.jsonl` + `errors.jsonl`. Investigates duplication patterns, error recovery, tool usage efficiency, and story iteration counts via ad-hoc `transcript-query.py` queries.
- **auditor-review** — reads `team-messages.jsonl` + agent summaries filtered to review roles. Evaluates quality gate effectiveness, fix cycle productivity, and inter-agent coordination quality.
- **documenter** — receives findings from all 3 auditors via SendMessage. Builds the findings document. Owns it exclusively. After all auditors report, performs cross-cutting synthesis pass.

Output: `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/retro-transcript-audit.md` — replaces the previous dual triage output. Structure: Executive Summary, What Worked Well, What Struggled, User Interventions, Story-by-Story Analysis, Cross-Cutting Patterns, Metrics, Priority Action Items. Each finding includes: what happened, evidence, root cause, recommendation (fix/keep/investigate).

**What stays from the current retro:** Phase 1 (Sprint Identification), Phase 3 (Story Verification), Phase 6 (Story Stub Creation — now informed by transcript audit findings), Phase 7 (Sprint Closure). **What is replaced:** Phase 2 (Log Collection → DuckDB preprocessing), Phase 4 (Cross-Log Discovery → auditor team analysis), Phase 5 (Triage Output Generation → documenter's findings document).

**Phase 6 extension (Decision 47):** After story stub creation and before sprint closure, the retro orchestrator: (1) spawns `/momentum:feature-status` to refresh the feature cache; (2) reads the updated `.claude/momentum/feature-status.md` for feature status deltas; (3) writes `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/sprint-summary.md` with sections: Features Advanced (conditional), Stories Completed vs. Planned, Key Decisions, Unresolved Issues, Narrative (500-word cap). The sprint summary is the sole compression artifact for sprint-to-sprint context transfer.

**Phase 5 extension (DEC-007, 2026-04-14):** Retro gains a **secondary** machine-readable output alongside the primary `retro-transcript-audit.md` findings document. Un-actioned findings that the developer chooses to carry forward are written as `handoff` events to `_bmad-output/implementation-artifacts/intake-queue.jsonl` with `source: "retro"`, `kind: "handoff"`, `status: "open"` — via the `momentum-tools` CLI, not direct file writes. These events are consumed by `momentum:sprint-planning` Phase A.5 and by `momentum:triage` re-surfacing on session start. The primary `retro-transcript-audit.md` output is unchanged; handoff events are additive. See the `intake-queue.jsonl` Schema Contract section for the full field contract. Per DEC-005 D7/D8 (failure-as-diagnostic framing and feature-state transitions) and DEC-005 D10 (retro does not gap-check when emitting handoffs). Implementation story: `retro-triage-handoff`.

**Decision 28 — Triage vs Refinement Distinction (superseded-partial 2026-04-14 by DEC-005 D10 and DEC-007)**

> _[Superseded-partial 2026-04-14: The original framing of triage as "intake-focused: analyze documents/ideas, create story stubs, initial prioritization, assign to an epic" is reshaped. Under DEC-005 D10, gap-check is explicitly excluded from triage (and from intake); it lives only at refinement, sprint-planning, and retro. Under DEC-007, triage is a **batch-classification orchestrator with delegation-only semantics** — it classifies observations into a formalized six-class taxonomy (ARTIFACT / DISTILL / DECISION / SHAPING / DEFER / REJECT) and delegates ARTIFACT/DISTILL/DECISION outcomes to the respective executor skills, writing SHAPING/DEFER/REJECT inline to `intake-queue.jsonl` via CLI. It is no longer the actor that "creates story stubs, does initial prioritization, assigns to an epic" — the delegated executor (`momentum:intake`) does that. See `momentum:triage` Architecture and `intake-queue.jsonl` Schema Contract sections above, and `_bmad-output/planning-artifacts/decisions/dec-007-triage-capture-artifact-2026-04-14.md`.]_

Triage is intake-focused: analyze documents/ideas, create story stubs, initial prioritization, assign to an epic. Refinement is organization-focused: classify, prioritize, gap-analyze the whole backlog. Different purposes, complementary workflows. Both deferred to Phase 5.

**Decision 29 — Sprint Planning Builds the Team (Extended 2026-04-06: Synthesis-First; Extended 2026-04-11: Sprint Summary Read; Extended 2026-04-14: Retro Handoff Queue Read)**
Sprint planning (`/momentum:sprint-planning`) encompasses story selection, create-story invocation, team composition, dependency graph construction, and execution plan generation. Sprint planning is a proper skill (not an inline workflow module) — invoked by Impetus or directly by the user. The sprint record stores team + dependencies (not just story lists and wave assignments). See Sprint Planning Workflow section.

Step 1 (Backlog Presentation) is synthesis-first: before presenting any backlog data, read the master plan documents (`prd.md`, product brief) to understand strategic priorities. Read the most recent sprint summary (`_bmad-output/implementation-artifacts/sprints/{last-sprint-slug}/sprint-summary.md`) for "what just happened" context — non-blocking if absent (Decision 47). **Phase A.5 additionally reads `_bmad-output/implementation-artifacts/intake-queue.jsonl` filtered to `source: "retro"`, `kind: "handoff"`, `status: "open"` — open handoff events from recent retros are folded into the synthesis context alongside the previous sprint summary (per DEC-007, 2026-04-14). If the queue file does not yet exist, treat as empty and continue silently.** Run a staleness check via `git log` for each `ready-for-dev`/`in-progress` story — check commits touching the story's `touches` paths. Lead with 3-5 prioritized recommendations with rationale (informed by master plan priorities, sprint summary findings, open retro handoff items, dependency readiness, backlog state), followed by the full sorted backlog as secondary reference. Potentially stale stories are surfaced separately with commit evidence. **Phase C output gains a labeled "Open handoff items from recent retros" section** that lists each open `source: "retro", kind: "handoff"` entry by title, source sprint, and (when present) its feature-state transition or failure-diagnosis framing. If master plan documents are missing, fall back to sorted backlog with a warning.

**Decision 30 — Gherkin Separation (Extended 2026-04-08: Spec-Quality Feedback Loop)**
Story files retain plain English ACs (dev sees intent). Sprint-scoped specs directory holds detailed Gherkin `.feature` files (verifiers only). Black-box behavioral validation: specs written pre-implementation, validated post-implementation, by different agents. See Gherkin Specification Separation section.

**Spec-quality feedback loop:** When E2E Validator encounters untestable Gherkin scenarios (ambiguous steps, missing preconditions, implementation-coupled assertions), findings are tagged with `spec-quality` metadata. These findings are surfaced in a dedicated "Spec Quality" section of the retrospective output, separate from implementation findings. This closes the loop between validation and specification: spec authoring issues are traced back to the sprint planning Gherkin generation step (Decision 29, Step 4) rather than treated as implementation failures.

**Decision 31 — AVFL at Sprint Level**
AVFL validates the complete sprint plan during planning (all stories together). AVFL runs once after ALL stories merge during sprint execution (not per-story). Per-story AVFL is removed from `momentum:create-story` and `momentum:dev`. This catches cross-story integration issues that per-story AVFL would miss. See Agent Pool Governance section. Phase 4 runs AVFL in scan profile (Decision 34) — discovery only, no fix loop. Findings are handed to the hybrid Agent Team.

**Decision 34 — AVFL Scan Profile and Hybrid Resolution Team (2026-04-04)**
AVFL and resolution teams serve distinct purposes. AVFL excels at adversarial multi-lens discovery (dual-reviewer cross-check). Teams excel at concurrent resolution and E2E behavioral verification. The scan profile separates these concerns.

Scan profile: all 4 lenses, dual reviewers (Enumerator + Adversary), maximum skepticism (level 3), consolidation with cross-check confidence. Zero fix iterations — output is scored findings list only.

Hybrid model: AVFL scan → findings handed to concurrent Agent Team (Dev, QA, E2E Validator, Architect Guard). Team works concurrently on main branch. E2E Validator tests running behavior with external tools — fundamentally different from AVFL's file-content validation.

**AVFL Corpus Mode — Multi-Document Cross-Validation (2026-04-03, commit 924d4ef)**
AVFL can validate a corpus of related documents together rather than validating artifacts individually. Corpus mode feeds multiple documents to validators simultaneously, enabling cross-document consistency checks: cross-reference errors between specs, contradictions between planning artifacts, and coverage gaps where one document promises something another omits. Validators receive the full corpus as input and apply their lens (Structural, Factual, Coherence, Domain) across document boundaries. Corpus mode uses the same validator pipeline (Enumerator + Adversary per lens, consolidator, fixer) — the difference is input scope, not execution architecture.

**Decision 35 — Agent Definition Files vs SKILL.md Boundary (2026-04-04)**

Momentum uses two Claude Code mechanisms for isolated execution: **SKILL.md files** (with optional `context: fork`) and **agent definition files** (`.md` files in the plugin's `agents/` directory, spawned via the Agent tool). This decision formalizes when to use each.

**Decision framework — three categories:**

| Category | Mechanism | When to use |
|---|---|---|
| Orchestrator / workflow skill | SKILL.md (flat, main context) | User-invokable, multi-step workflow, spawns subagents, interactive. Examples: Impetus, sprint-dev, avfl, dev, create-story. |
| Standalone verifier skill | SKILL.md with `context: fork` | Spawned by orchestrators AND useful standalone. Rich instruction body (multi-section workflow). Tool restrictions via `allowed-tools:`. Examples: code-reviewer, architecture-guard. |
| Pure spawned worker | Agent definition file (`agents/*.md`) | Only spawned during specific phases — never user-invoked. Task-in, structured-findings-out. No multi-step workflow. Tool restrictions via `tools:` allowlist. Examples: QA reviewer, E2E validator. |

**Key distinctions:**

- **SKILL.md** files are registered in the plugin's `skills/` directory, invoked via the Skill tool or `/momentum:<name>` slash command, and can contain full workflow instructions in their markdown body. With `context: fork`, they run in isolated subagent context with tool restrictions — functionally equivalent to agent files for isolation, but richer.
- **Agent definition files** live in the plugin's `agents/` directory, are spawned via `Agent(subagent_type="<name>")`, always run in isolated context, and use `tools:` / `disallowedTools:` for enforcement. Their markdown body is a system prompt, not a workflow. They cannot spawn further subagents. Designed for parallel execution.
- **The test:** If a role is only ever spawned by an orchestrator during a specific phase, has no standalone use case, and produces a structured report from a fixed prompt — it's an agent definition file. If it has a multi-step workflow, user-invokability, or needs to orchestrate others — it's a SKILL.md.

**Application to Team Review phase (Decision 34):**

The hybrid Agent Team in Phase 5 spawns four concurrent roles. Their deployment:

| Role | Deployment | Rationale |
|---|---|---|
| Dev (fix agent) | General-purpose agent via Agent tool | No custom definition needed — receives AVFL findings list and fix instructions in spawn prompt. Uses project's dev guidelines from sprint record. |
| QA reviewer | Agent definition file (`agents/qa-reviewer.md`) | Pure worker: reviews code against story ACs, produces per-story findings. Read-only tools. Never user-invoked. |
| E2E Validator | Agent definition file (`agents/e2e-validator.md`) | Pure worker: tests running behavior against Gherkin specs with external tools. Needs Bash for test execution. Never user-invoked. Used in sprint Team Review (Decision 34) and quick-fix Phase 4 validation (Decision 40). |
| Architect Guard | SKILL.md with `context: fork` (existing) | Already implemented as standalone verifier skill. Also useful outside Team Review (ad-hoc drift checks). Retains SKILL.md deployment. |

**Plugin structure addition:**

The plugin root gains an `agents/` directory alongside `skills/`:

```
skills/momentum/                     ← Plugin root
├── .claude-plugin/plugin.json
├── skills/                          ← SKILL.md files (user-facing + context:fork)
├── agents/                          ← Agent definition files (pure spawned workers)
│   ├── qa-reviewer.md
│   └── e2e-validator.md
├── hooks/
├── scripts/
└── references/
```

Agent definition files are discovered by Claude Code from the plugin's `agents/` directory (resolution priority 4: plugin agents). The `name` field in YAML frontmatter determines the `subagent_type` used in Agent tool calls.

**What does NOT change type:**

- code-reviewer stays SKILL.md `context: fork` — it has a rich review workflow (7-step process) and standalone utility
- architecture-guard stays SKILL.md `context: fork` — same reasoning, useful for ad-hoc drift checks
- All orchestrator/workflow skills stay SKILL.md — they need main context for spawning and interaction
- AVFL sub-skills (validator-enum, validator-adv, consolidator, fixer) stay as nested SKILL.md sub-skills — they're part of AVFL's internal pipeline with their own orchestration needs

**Decision 36 — Sprint Lifecycle State Machine (2026-04-04)**

Sprints follow a formal lifecycle with explicit states and transition gates:

```
planning → ready → active → done → completed
```

| State | Meaning | Stored in |
|---|---|---|
| `planning` | Sprint planning in progress — stories being selected, team composed, specs written | `index.json` planning entry, `status: "planning"` |
| `ready` | Sprint planning workflow completed — sprint is fully planned but not yet activated | `index.json` planning entry, `status: "ready"` |
| `active` | Developer has activated the sprint; story execution in progress | `index.json` active entry, `status: "active"` |
| `done` | All stories complete; retro not yet run | `index.json` active entry, `status: "done"` |
| `completed` | Retro has run; sprint is fully closed | `index.json` completed array |

**Transition gates:**

| Transition | Trigger | Gate |
|---|---|---|
| planning → ready | Sprint planning workflow completes (all stories created, team composed, specs written, AVFL validated) | Automated — sprint-planning skill sets status |
| ready → active | Developer selects "Activate sprint" from greeting menu, OR retro auto-activates (see below) | Developer intent or retro completion |
| active → done | All stories reach `done` status | Automated — momentum-tools detects all-done |
| done → completed | Retro runs | Retro completion moves sprint to completed array |

**Cross-sprint transitions:**

- **Retro auto-activation:** When retro completes for the active sprint and a planning sprint exists in `ready` status, the retro workflow automatically activates the ready sprint. The completed sprint moves to the completed array; the ready sprint becomes the new active sprint. This prevents a dead period between sprints.
- **Planning during active sprint:** Sprint planning can complete (planning → ready) while an active sprint is running. The ready sprint waits for the active sprint's retro to activate it, or the developer can activate it manually from the greeting menu.
- **Max one planned sprint:** Only one sprint may exist in planning/ready status at a time. Starting a new sprint plan requires the existing planning sprint to be activated or abandoned first.

**Schema impact:** The `status` field is added to active and planning entries in `sprints/index.json`. Completed entries gain `retro_run_at` (ISO date or null). See Sprint Tracking Schema section for the full schema.

**Decision 37 — Greeting State Detection (2026-04-04)**

Impetus detects one of 9 greeting states at session start. Detection is algorithmic — the state is derived from `sprints/index.json`, `stories/index.json`, and `~/.claude/momentum/global-installed.json`. Each state produces a specific narrative and menu (defined in `.claude/momentum/greeting-mockup.md`, which is the authoritative reference for greeting content).

| # | State | Detection logic |
|---|---|---|
| 1 | `first-session-ever` | `momentum_completions == 0` in `global-installed.json` AND no sprint history (no active, no completed) |
| 2 | `active-not-started` | Active sprint exists (`status: "active"`), no stories in `in-progress` or later status |
| 3 | `active-in-progress` | Active sprint exists, at least one story `in-progress` or later, none `blocked` |
| 4 | `active-blocked` | Active sprint exists, at least one story has `blocked` status |
| 5 | `active-planned-needs-work` | Active sprint exists + planning sprint exists with `status: "planning"` (not yet ready) |
| 6 | `done-retro-needed` | Active sprint `status: "done"` (all stories complete), retro not yet run |
| 7 | `done-no-planned` | Active sprint `status: "done"`, no planning sprint exists |
| 8 | `no-active-nothing-planned` | No active sprint, no planning sprint |
| 9 | `no-active-planned-ready` | No active sprint, planning sprint exists with `status: "ready"` |

**Priority resolution:** States are evaluated in the order listed. State 5 (`active-planned-needs-work`) takes priority over states 3-4 when both an active sprint and a planning-status planned sprint exist — the planning sprint's incomplete state is the more actionable signal. States 6-7 are sub-states of "done" distinguished by planning sprint presence.

**Menu construction:** Each state maps to a fixed menu defined in the greeting mockup. The menu is not dynamically composed from rules — it is a lookup from state to menu. This keeps the greeting deterministic and testable. The 9 menus are small enough to enumerate exhaustively.

**Stats write timing:** After rendering the greeting and menu, Impetus increments `momentum_completions` in `global-installed.json`. This write happens after display — the user never sees a diff or file-write artifact during the greeting.

**Decision 38 — Narrative Voice Contract (2026-04-04)**

The Impetus voice — Optimus Prime's gravitas blended with KITT's loyalty — is not a UX preference. It is a binding architectural contract for all user-facing Impetus output. This contract applies to session greetings, progress updates, workflow transitions, menu presentation, error messages, and subagent result synthesis.

**Voice principles (non-negotiable):**

| Principle | Meaning |
|---|---|
| Gravitas | Words with mass. "Stands ready." "Carried across the line." "Hold the line." Not jargon, not ops-speak. |
| Earned emotion | "The work is done" over "mission complete." Emotion that was earned by real work, not manufactured. |
| Deference with dignity | "Lead on." "I'm with you." "When you're ready, I'm here." He follows — and the choice to follow carries weight. |
| Forward motion | Every closer looks ahead. "Where do we begin?" "The road is open." "Give the word." Never static. |
| First session is purpose | "I hold the line." "Let's forge something worth building." Identity, not features. |

**Enforcement:** Any change to Impetus user-facing output must preserve these principles. The greeting mockup (`.claude/momentum/greeting-mockup.md`) is the authoritative reference for greeting-specific voice. The principles above govern all other Impetus output not covered by the mockup.

**Traceability:** Formalization of the voice identity established in the greeting redesign v8 mockup. Supersedes the earlier "KITT-like servant-partner" description in Decision 3d — the voice has evolved from competent-and-dry-witted to gravitas-and-earned-emotion. Decision 3d's Impetus Identity subsection is updated to reflect this.

**Decision 39 — Quick-Fix Bypass-Sprint Lifecycle Path (2026-04-04, Extended 2026-04-08)**

Quick-fix introduces a third execution path alongside sprint orchestration and triage-based backlog management. It is a bypass-sprint lifecycle path: single story from prompt → lightweight 4-phase workflow → `sprints/index.json` registration without activate/complete lifecycle states. The quick-fix path does not create a sprint, does not require sprint planning, and does not use the `planning → ready → active → done → completed` state machine (Decision 36). Instead, `momentum-tools quickfix register` writes a quick-fix entry directly to `sprints/index.json` and `momentum-tools quickfix complete` marks it done.

**Execution paths in Momentum:**

| Path | Scope | Lifecycle | Entry point |
|---|---|---|---|
| Sprint orchestration | Single sprint, multiple stories | Decision 36 state machine | `/momentum:sprint-planning` → `/momentum:sprint-dev` |
| Quick-fix | Single story, single session | Register → execute → validate → complete | `/momentum:quick-fix` |
| Distill | Single practice artifact, single session | Discover → classify → apply → validate → commit | `/momentum:distill` (Decision 42) |

**momentum:dev is internal-only:** momentum:dev is called by sprint-dev and quick-fix as a story executor — it is not user-invocable from Impetus menus or directly by the developer. It has no standalone entry point; it always runs within the context of a calling workflow (sprint-dev or quick-fix).

**Quick-fix Phase 4 code review:** Quick-fix Phase 4 includes code review via `momentum:code-reviewer` between the AVFL scan and team validation. This ensures single-story fixes receive the same adversarial code review applied to sprint stories, without requiring the full sprint Team Review process.

**Worktree cleanup timing:** Worktree cleanup is deferred until all quality gates pass in the calling workflow. The worktree remains available during AVFL, code review, and team validation phases so that fix agents can apply corrections without re-creating the worktree. Cleanup occurs only after the calling workflow (sprint-dev or quick-fix) confirms all gates are satisfied.

**Traceability:** Quick-fix stories are registered in `sprints/index.json` for audit trail and retrospective input. They bypass sprint lifecycle but not traceability.

**Decision 40 — Change-Type-Driven Validator Selection (2026-04-04)**

Validators join the team based on story `change_type`, replacing the hardcoded all-four-roles team from sprint Team Review (Decision 34) for single-story workflows. This is the validator selection model for quick-fix Phase 4 and any future single-story execution path.

| change_type | Validators |
|---|---|
| `skill-instruction` | E2E Validator |
| `script-code` | QA reviewer |
| `skill-instruction` + `script-code` (both) | E2E Validator + QA reviewer |

The Dev fix agent and Architect Guard are not included — quick-fix is a single-story workflow where the developer is already the implementer and architecture drift is not a concern for targeted fixes. For sprint Team Review (multi-story, post-merge), the full team (Decision 34) still applies.

**Traceability:** `momentum-tools specialist-classify` (Decision 26) provides the deterministic mapping from `change_type` to validator set. The same classification drives both specialist selection and validator selection.

**Decision 41 — Workflow Team Composition Declarations (2026-04-06)**

Workflows that spawn agents must declare their team composition requirements explicitly via `<team-composition>` XML elements. This eliminates role ambiguity that caused 60% of user corrections in sprint-2026-04-06 (missing dev/fixer agent, wrong spawning mode, role improvisation).

**Declaration structure:** Each workflow that spawns agents includes a `<team-composition>` section at the top of the workflow that codifies:

| Field | Values | Meaning |
|---|---|---|
| `required-roles` | Per-phase list of roles | Which roles must be present for that phase to execute |
| `spawning-mode` | `individual` (Agent tool, one per spawn) or `team` (TeamCreate, grouped spawn) | How agents are created — default is `individual` unless explicitly overridden |
| `concurrency` | `parallel` (all agents in one turn) or `sequential` (one at a time, dependency-ordered) | Whether agents run concurrently or in sequence |

**Application to workflows:**

| Workflow | Phase | Required roles | Spawning mode | Concurrency |
|---|---|---|---|---|
| sprint-dev | Phase 2 (dev wave) | Dev (per story) | `individual` (Agent tool) | `sequential` (dependency-ordered, commit-as-sync-point) |
| sprint-dev | Phase 4d (targeted fixes) | Dev (fix agent) | `individual` | Per fix scope |
| sprint-dev | Phase 5 (team review) | QA, E2E Validator, Architect Guard | `individual` (3 separate Agent tool calls) | `parallel` (single message) |
| AVFL | Validators | Enumerator, Adversary (per lens) | `individual` (Agent tool) | `parallel` |
| AVFL | Consolidator | Consolidator | `individual` | `sequential` (after validators) |
| AVFL | Fixer | Fixer | `individual` | `sequential` (after consolidator) |
| momentum:refine | Wave 1 (discovery) | prd-coverage-agent, architecture-coverage-agent | `individual` | `parallel` |
| momentum:refine | Wave 2 (updates, conditional) | prd-update-agent, architecture-update-agent (each conditional per document) | `individual` | `parallel` |

**Sprint planning validation:** Step 5 (Execution plan and team composition) validates the planned `team` object against the workflow's declared required roles. If a required role is missing from the plan, sprint planning surfaces the gap before activation. This is a pre-activation gate — the sprint cannot be activated with an incomplete team.

**Rationale:** Team composition rules were implicit — the sprint record carried a `team` object, but workflows did not declare what roles they need, how agents should be spawned, or concurrency expectations. When Impetus had to infer these from context, it improvised incorrectly. Explicit declarations make composition deterministic and testable.

**Traceability:** Extends Decision 26 (Two-Layer Agent Model) with structural enforcement and Decision 29 (Sprint Planning Builds the Team) with a validation gate. Triggered by sprint-2026-04-06 retro finding: 6 of 10 user corrections were about team composition and spawning.

**Documented pattern — refine two-wave conditional spawning (2026-04-06):**
momentum:refine uses a two-wave conditional spawning pattern as a documented instance of Decision 41 composition:
- **Wave 1:** Two discovery agents spawn in parallel (prd-coverage-agent, architecture-coverage-agent). Each independently analyzes its document for coverage gaps, staleness, and update candidates, returning structured findings.
- **Developer approval gate:** Orchestrator presents Wave 1 findings and requires developer approval before proceeding. Developer may approve, modify, or reject updates per document independently.
- **Wave 2:** Zero, one, or two update agents spawn based on Wave 1 findings and the developer's approval decision. Each approved document gets its own sole-writer update agent; no update agent spawns for a rejected document. Agents run in parallel when both are approved.
This pattern is distinct from the per-finding Add/Modify/Remove triage used in other workflows — approval is per-document, not per-finding, enabling batch UX at the document level.

**Decision 42 — Distill Execution Path and AVFL Profile (2026-04-11)**

`/momentum:distill` is a third execution path alongside sprint orchestration and quick-fix (Decision 39). It is the practice-artifact analogue of quick-fix: where quick-fix handles code stories, distill handles practice artifacts (rules, references, skill prompts, spec additions).

**Distill AVFL profile:** A lightweight single-pass validation mode designated for distill's post-change validation step. Runs two subagents (Enumerator + Adversary) on only the changed files. No multi-lens parallelism — a single validation pass, not separate structural/accuracy/coherence passes. Model: Sonnet at medium-low effort. No fix iterations — output informs a developer-prompted correction or a clean commit. Implemented as a named profile in `skills/avfl/references/framework.json`.

**Rationale:** The discovery phase (two parallel agents before any changes are written) handles most structural and design correctness concerns upfront. The post-change AVFL pass is intentionally lighter — it validates a small, targeted artifact change, not a full document corpus. The lightweight profile preserves the "fast path" characteristic of distill while ensuring changes receive adversarial review before committing.

**Fix scope routing:**
- Project-local: applies to current project's rules/references only
- Momentum-level (in Momentum project): applies to Momentum practice files; bumps plugin patch version; commits and pushes
- Momentum-level (in external project): defer to retro queue OR generate remote distill prompt for developer to apply in a Momentum session

**Findings-ledger write authority:** `momentum:distill` is an authorized writer to `~/.claude/momentum/findings-ledger.jsonl` (extending Decision 1c). Distill writes with `origin: distill`; the flywheel workflow writes with `origin: flywheel`. The `origin` field enables FR33 ratio tracking to count distillation-origin fixes separately from code-review-origin fixes.

**Traceability:** Distill entries are registered in the findings-ledger with `origin: distill` for audit trail and retrospective input. They bypass sprint lifecycle but not traceability. Motivated by research finding (2026-04-10): Momentum lacks a mechanism for immediate artifact updates from session learnings — all findings must survive sprint planning before landing in practice files, creating multi-week lag.

---

**Decision 43 — Retro Phase 0: Session Analytics and Regression Detection (2026-04-11)**

`/momentum:retro` gains a Phase 0 that runs before the qualitative audit phases. Phase 0 queries the Claude Code session JSONL logs for the current sprint window using DuckDB, computes a core metric set, compares to the prior sprint window, and produces a structured brief that informs Phase 1 auditors where to focus.

**Framing — regression detection, not trend tracking:** The primary value is detecting when a practice change made something worse. "Research skill error rate was 0% last sprint and 8% this sprint" is an actionable regression signal. Sprint-over-sprint trend analysis is secondary.

**DuckDB as the query layer:** Session JSONL files at `~/.claude/projects/<project>/` are the data source. DuckDB reads them via `read_csv_auto` with `VARCHAR` columns (required — `queue-operation` entries break `read_ndjson_auto` type inference). All JSON extraction uses `json_extract_string()` / `json_extract()` inline.

**Core metric set (Phase 0 computes all of these):**
- Tool error rate per skill (`is_error: true` on `tool_result` entries, grouped by preceding skill invocation)
- Hook prevention events (`system.stop_hook_summary.preventedContinuation = true`) — gate-failure signal
- Compaction frequency (`system.compact_boundary` count) — context pressure indicator
- Skill invocation counts by skill name — detects unused or regression-prone skills
- Turn duration vs. context depth (`system.turn_duration.durationMs / messageCount`) — performance degradation signal
- Cache hit rate (`cache_read_input_tokens / (cache_read + cache_creation_input_tokens)`) — context efficiency
- Git commit type distribution (regex on `Bash` `git commit` inputs) — `fix` spike signals quality regression

**Findings-ledger versioning — Option A + Option B:**
- **Option A (primary):** Every findings-ledger write includes a `momentum_version` field populated from the installed plugin version at write time. Applies to all ledger writers: `momentum:distill`, `momentum:retro` (Phase 0 brief + Phase 5 stubs), and any future writers.
- **Option B (validation):** Git log timestamps map sessions to Momentum version bumps for cross-checking. Used to validate Option A data and to backfill version attribution for ledger entries that predate the `momentum_version` field.

**Phase 0 output:** A structured session-analytics brief written to the retro working directory. Contains: sprint window, sessions analyzed, metric table with sprint-over-sprint delta, and flagged regressions. Phase 1 auditors receive this brief before qualitative review begins.

**Traceability:** Motivated by Fowler feedback flywheel research (2026-04-10) — Momentum captures failure signals but not quantitative regression signals. Log-audit research (2026-04-11) confirmed all metrics are extractable from existing session JSONL files without instrumentation changes. The findings-ledger `momentum_version` field extends Decision 42's ledger schema.

---

## Feature-Orientation Architecture Decisions (44-48)

<!-- Added sprint-2026-04-11: Feature-orientation epic decisions. These decisions introduce the feature artifact layer, feature status visualization, cache infrastructure, sprint summary artifact, and practice project detection. -->

**Decision 44 — Feature Artifact Layer (sprint-2026-04-11)**

A new first-class planning artifact: `_bmad-output/planning-artifacts/features.json`. Features represent user-observable capabilities — the persistent units of product value that survive sprint boundaries.

**Features vs. Epics — orthogonal organization dimensions:**

| Dimension | Epics | Features |
|---|---|---|
| Groups by | Theme or initiative | User-observable capability |
| Lifecycle | Closed when stories complete | Persistent — tracked across all sprints |
| Status | Done/not-done | working / partial / not-working / not-started |
| Verification | Story completion | Acceptance condition (behavioral, verifiable) |

**Feature types:**

| Type | Meaning | Examples |
|---|---|---|
| `flow` | End-to-end user journey — user can accomplish a complete task | Impetus greeting → sprint selection → execution |
| `connection` | Integration or handoff between subsystems | Hook fires → lint runs → finding surfaced to user |
| `quality` | Non-functional requirement observable by users | Startup in under 2s; greeting voice matches contract |

**`features.json` schema (keyed-object, same pattern as stories/index.json):**

```json
{
  "impetus-session-orientation": {
    "name": "Session Orientation",
    "type": "flow",
    "description": "Developer opens Impetus and immediately understands sprint state, recent decisions, and best next action",
    "acceptance_conditions": [
      "Greeting renders correct state from 9-state machine",
      "Menu items are contextually appropriate",
      "No prompting required from developer"
    ],
    "value_analysis": "Current value: Developer can orient within seconds of opening a session — sprint state, recent decisions, and next action are surfaced automatically.\n\nFull vision: Impetus becomes a genuine practice partner — proactively surfacing risk signals, suggesting story sequence adjustments, and adapting its greeting voice to sprint phase. Capabilities beyond current: risk-aware recommendations, multi-sprint trend awareness, integration with external signals (CI status, PR queue).\n\nKnown gaps: Greeting is currently state-driven but not risk-aware. No cross-sprint trend analysis. No external signal integration.",
    "system_context": "Session Orientation is the entry point for all developer interaction with Momentum. It sets the cognitive frame for each work session. A well-functioning orientation feature reduces decision overhead and keeps the developer on the highest-value work. It is the primary surface through which the practice framework communicates its current understanding of the project.",
    "status": "working",
    "prd_section": "FR-7",
    "stories": ["greeting-redesign", "session-stats", "sprint-lifecycle-state-machine"],
    "stories_done": 3,
    "stories_remaining": 0,
    "last_verified": "2026-04-08",
    "notes": ""
  }
}
```

**Schema field definitions:**

| Field | Type | Values / Notes |
|---|---|---|
| `feature_slug` | key | kebab-case, globally unique |
| `name` | string | Human-readable display name |
| `type` | enum | `flow` \| `connection` \| `quality` |
| `description` | string | One sentence: what the user experiences |
| `acceptance_conditions` | array of strings | Behavioral, verifiable, outsider-testable — one condition per array entry |
| `value_analysis` | string (multi-paragraph) | Required. Covers: (a) current value delivered, (b) full vision including new capabilities beyond pain removal, (c) known gaps |
| `system_context` | string | Required. How this feature fits and enhances the overall product |
| `status` | enum | `working` \| `partial` \| `not-working` \| `not-started` |
| `prd_section` | string | FR/NFR reference (e.g., "FR-7", "NFR-3") — links feature to PRD |
| `stories` | array | Story slugs that implement or advance this feature |
| `stories_done` | int | Count of stories in terminal state (`done`) |
| `stories_remaining` | int | Count of stories not yet done |
| `last_verified` | date | ISO 8601 date of last manual or automated verification |
| `notes` | string | Free text for gaps, partial-status explanations, open questions |

**Write authority:** `features.json` is written exclusively by `momentum:feature-grooming` (bootstrap and refine modes). No other skill or tool writes features.json. Grooming mode detection: bootstrap = features.json absent or empty; refine = features.json has ≥1 entry. `acceptance_conditions` is an array of strings — each entry is one behavioral, verifiable acceptance condition.

**Rationale:** Epics provide theme-based grouping that serves sprint planning. Features provide capability-based grouping that serves developer orientation and stakeholder communication. A feature can span multiple epics. An epic can advance multiple features. The two axes compose — neither replaces the other.

**Traceability:** Introduced by the feature-artifact-schema story in sprint-2026-04-11. Motivated by DEC-002 (Feature Visualization and Developer Orientation): the current epics-only model makes it impossible to answer "is the app usable end-to-end?" without reading all story files.

---

**Decision 45 — Feature Status Skill: Standalone with Dual Output (sprint-2026-04-11)**

`/momentum:feature-status` is a standalone flat skill that reads `features.json` + `stories/index.json` and produces two output artifacts for different consumption contexts.

**Inputs:**
- `_bmad-output/planning-artifacts/features.json` — feature definitions and current status
- `_bmad-output/implementation-artifacts/stories/index.json` — story statuses for gap detection

**Outputs:**

| Output | Path | Format | Consumer |
|---|---|---|---|
| HTML dashboard | `.claude/momentum/feature-status.html` | Self-contained HTML (all CSS inline, Mermaid via CDN ESM) | Browser (file://) — developer visual review |
| Cache file | `.claude/momentum/feature-status.md` | Markdown with YAML frontmatter | Impetus startup-preflight (Decision 46) |

**HTML dashboard layout:**

```
header (project name, generated timestamp)
summary stats bar (N working / M partial / K not-working / J not-started)
Mermaid dependency graph (collapsed <details> by default — feature→story edges)
feature tables grouped by type (flow | connection | quality)
footer (last verified, momentum version)
```

**Signal hierarchy (always visible vs. behind `<details>` expand):**

| Signal | Visibility |
|---|---|
| Status badge (working/partial/not-working/not-started) | Always visible |
| Story fraction (N done / M total) | Always visible |
| GAP flag (stories_remaining > 0 AND status not "working") | Always visible |
| Acceptance condition text | `<details>` expand |
| Story list with individual statuses | `<details>` expand |
| Gap description (notes field) | `<details>` expand |

The signal hierarchy prioritizes scannability: a developer can assess the full feature health picture without expanding any rows. Detail is available on demand.

**Rendering paths (two, auto-detected — Decision 48):**

| Path | Detection | Renders |
|---|---|---|
| Product | Default (features.json present, not a practice project) | flow/connection/quality tables with gap analysis |
| Practice | `skills/momentum/skills/*/SKILL.md` present + `_bmad-output/planning-artifacts/` present | ASCII skill topology + SDLC coverage table |

**Standalone design:** This skill is intentionally not absorbed into Impetus or momentum-tools. The HTML generation logic (Mermaid, inline CSS, responsive layout) is too complex for a tool call embedded in a larger workflow. Supersedes DRIFT-006's proposal to fold status into Impetus/momentum-tools. The cache file (Decision 46) provides the lightweight integration path for Impetus greeting.

**Mermaid dependency graph:** Renders feature-to-story relationships as a directed graph. Layout: top-down (features as parent nodes, stories as leaves). Status color-coding matches badge colors. Collapsed by default (`<details>` wrapper) — avoids overwhelming the page on projects with many stories.

**Self-contained HTML constraint:** All CSS is inline (`<style>` block). Mermaid loads via CDN ESM script tag (`https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.esm.min.mjs`). The file must render correctly when opened directly as `file://` with no server — no relative asset paths, no external stylesheets, no localhost dependencies.

**Traceability:** Introduced by feature-status-skill story in sprint-2026-04-11. Supersedes DRIFT-006. The standalone skill boundary is motivated by complexity of HTML generation (Mermaid, CSS) that would bloat Impetus context if inlined.

---

**Decision 46 — Feature Status Cache Pattern and Startup Integration (sprint-2026-04-11)**

The feature status cache provides fast, zero-cost feature health visibility in the Impetus greeting without re-running the full feature-status skill at every session start.

**Cache file:** `.claude/momentum/feature-status.md` — YAML frontmatter only (no body required):
```yaml
---
input_hash: "sha256:<64-char hex>"
summary: "3/5 features working — 1 partial (impetus-orientation), 1 not-started (mcp-integration)"
generated_at: "2026-04-11T14:30:00Z"
---
```

**Hash computation:**
```python
import hashlib, json
features_content = open("_bmad-output/planning-artifacts/features.json").read()
stories_content = open("_bmad-output/implementation-artifacts/stories/index.json").read()
h = hashlib.sha256((features_content + ":" + stories_content).encode()).hexdigest()
```

**Cache validity — four states:**

| State | Condition | Impetus behavior |
|---|---|---|
| `no-features` | `features.json` absent | Silent skip — no feature line in greeting |
| `no-cache` | `features.json` present, cache absent | Surface in greeting: "Feature status not yet generated — run /momentum:feature-status" |
| `fresh` | Hash matches | Display `summary` line inline in greeting narrative |
| `stale` | Hash mismatch (features.json or stories/index.json changed since last run) | Display stale summary + offer refresh: "Feature status may be out of date — run /momentum:feature-status to refresh" |

**NFR20 compliance (startup-preflight remains one Bash call):** Hash computation runs as inline Python inside the startup-preflight Bash call — not a subprocess fork. The startup-preflight already runs Python for other inline computations. Adding the hash check does not increase the number of Bash tool calls at session start.

```bash
# Inline inside startup-preflight (one Bash call total):
python3 -c "
import hashlib, json, os, sys
# ... read files, compute hash, compare to cache frontmatter ...
print(cache_state)  # no-features | no-cache | fresh | stale
print(summary)      # empty string if not fresh
"
```

**New momentum-tools command — `feature-status-hash`:** A standalone utility subcommand used by the feature-status skill when writing the cache file after HTML generation. Computes the SHA-256 hash of features.json + stories/index.json and prints the hex digest. This avoids duplicating the hash logic between startup-preflight (inline Python) and feature-status (CLI call).

```bash
momentum-tools feature-status-hash   # prints: sha256:<hex>
```

**Cache write authority:** `momentum:feature-status` is the sole writer of `.claude/momentum/feature-status.md`. Impetus reads it; never writes it. The cache is never committed to git — it is runtime state.

**Rationale:** Running the full feature-status skill (HTML generation, Mermaid rendering, gap analysis) at every session start would violate NFR20 and introduce latency in the greeting. The cache provides a summary line at zero additional tool calls. The hash-based invalidation ensures the cache is refreshed when the underlying data changes.

**Traceability:** Introduced by impetus-feature-status-cache story in sprint-2026-04-11. Extends Decision 1f (Feature Status Cache storage). Maintains NFR20 compliance established by startup-preflight design.

---

**Decision 47 — Sprint Summary at Retro Boundary (sprint-2026-04-11)**

A new artifact written by the retro orchestrator at Phase 6 close: `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/sprint-summary.md`. It compresses each completed sprint's signal into a structured reference document for sprint planning and future retro context loading.

**Artifact path:** `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/sprint-summary.md`

**Written by:** Retro orchestrator at Phase 6 close, after spawning `/momentum:feature-status` for cache refresh and before sprint closure.

**Sections:**

| Section | Content | Conditional? |
|---|---|---|
| Features Advanced | Features whose status changed this sprint (status delta) | Yes — omit if features.json absent or no status changes |
| Stories Completed vs. Planned | Count + list of completed and dropped/deferred stories | No |
| Key Decisions | Architectural or product decisions made during the sprint (from decisions/) | No |
| Unresolved Issues | Items from retro finding list that were NOT resolved before closure | No |
| Narrative | 500-word max. Sprint story: what was built, what struggled, what changed in the practice | No |

**Sprint planning integration (Decision 29 Step 1 extension):** Sprint planning Step 1 reads the most recent sprint summary before synthesizing backlog recommendations. The summary provides the "what just happened" context that informs priority recommendations. Non-blocking if absent (first sprint, or summary not yet written for the prior sprint).

**Retro orchestrator sequence at Phase 6 close:**
1. Spawn `/momentum:feature-status` (refresh cache)
2. Read updated `.claude/momentum/feature-status.md` for status deltas
3. Write `sprint-summary.md` (sole writer at close time)
4. Proceed to sprint closure

**Rationale:** Sprint summaries address a gap in context continuity across sessions. Without a summary, sprint planning Step 1 must reconstruct sprint history by reading all story files, retro findings, and git log. The 500-word cap keeps summaries dense and LLM-efficient — optimized for being read as context, not for human prose.

**Traceability:** Introduced by sprint-boundary-compression story in sprint-2026-04-11. Motivated by sprint planning Step 1 synthesis: the "what just happened" signal was previously unstructured (scattered across retro-transcript-audit.md, story files, and decisions/). The sprint summary is the canonical compression of that signal.

---

**Decision 48 — Practice Project Detection and Practice Rendering Path (sprint-2026-04-11)**

`/momentum:feature-status` automatically detects whether it is running inside a practice project (a project that IS a Momentum-like practice framework) or a product project, and selects the appropriate rendering path.

**Detection heuristic:**

```
Practice project IF:
  skills/momentum/skills/*/SKILL.md exists   (skill files at a practice-skill layout)
  AND _bmad-output/planning-artifacts/ exists  (BMAD planning output present)
```

Both conditions must be true. The heuristic is intentionally conservative: it must not false-positive for regular product projects that happen to have a `skills/` directory. The dual condition (skill topology + planning artifacts) is specific to practice projects built on the Momentum pattern.

**Detection mechanism:** Glob-based — `glob("skills/momentum/skills/*/SKILL.md")`. No hardcoded skill names. Dynamic discovery means new skills are automatically included without updating the detection logic or the rendering template.

**Practice rendering path — two sections:**

**Section 1: Skill Topology**

ASCII representation of the skill graph showing hand-off relationships derived from workflow conventions. Relationships are inferred from workflow.md `spawn` directives and SKILL.md `invokes:` references — not hardcoded.

```
/momentum:impetus
  ├── dispatches → /momentum:sprint-planning
  ├── dispatches → /momentum:sprint-dev
  └── dispatches → /momentum:retro
/momentum:sprint-dev
  ├── spawns    → momentum:dev (per story)
  ├── spawns    → momentum:code-reviewer (Phase 4b)
  └── spawns    → momentum:avfl (Phase 4)
```

**Section 2: SDLC Coverage Table**

Maps each skill to the SDLC phases it covers. Eight phases (fixed, not derived):

| SDLC Phase | Skills covering it |
|---|---|
| Discovery | momentum:research, momentum:intake |
| Planning | momentum:sprint-planning, momentum:refine, momentum:epic-grooming |
| Specification | momentum:create-story, momentum:plan-audit |
| Implementation | momentum:dev, momentum:quick-fix |
| Review | momentum:code-reviewer, momentum:architecture-guard, momentum:avfl |
| Retrospective | momentum:retro, momentum:distill |
| Orientation | momentum:impetus, momentum:feature-status |
| Quality/Validation | momentum:avfl, momentum:code-reviewer, momentum:assessment |

Redundancy flags: phases with 0 skills are flagged as uncovered; phases with 4+ skills are flagged as potentially over-invested (informational, not blocking).

**Product rendering path:** The product path (default when practice detection returns false) renders the flow/connection/quality feature tables with gap analysis as described in Decision 45. No change to product path behavior.

**Rationale:** Practice projects have a fundamentally different "feature" structure — their user-observable capabilities are skills and SDLC coverage, not product flows. Forcing a product-style feature table onto Momentum itself would require maintaining a features.json that describes Momentum's own skills as "features" — an awkward fit. The practice path renders the actually meaningful signal for a practice project developer. The detection heuristic is the minimal sufficient condition that distinguishes the two cases without requiring explicit configuration.

**Traceability:** Introduced by feature-status-practice-path story in sprint-2026-04-11. Motivated by the observation that Momentum is its own primary dogfooding target — the feature status skill must work well when run against Momentum itself.

---

**Decision 49 — Feature Grooming Skill: Orchestrator Pattern and Write Authority (sprint-2026-04-11)**

The `momentum:feature-grooming` skill is a flat orchestrator. It spawns exactly 2 discovery subagents in a single message (model: haiku, effort: quick):

- **Agent A:** reads PRD and epics.md, extracts feature candidates and FR groupings
- **Agent B:** reads architecture.md and stories/index.json, extracts capability clusters and story themes

The orchestrator handles all synthesis, value analysis, developer interaction, and file writes directly. No additional subagents are spawned beyond the initial 2.

**Write authority:** `momentum:feature-grooming` is the sole authorized writer of `features.json`. In bootstrap mode it also writes assessment documents to `_bmad-output/planning-artifacts/assessments/` and decision documents to `_bmad-output/planning-artifacts/decisions/` before writing features.json.

**Mode detection:** bootstrap when features.json absent or has ≤2 entries; refine when features.json has ≥3 entries.

**Rationale:** The flat orchestrator pattern keeps the synthesis step in a single context that can reason holistically across both discovery inputs. Two discovery subagents are sufficient to parallelize the read-heavy work; further parallelism would fragment the synthesis context without benefit. Sole write authority over features.json ensures the schema (including `value_analysis` and `system_context` fields added in Decision 44) is always populated correctly and consistently.

**Traceability:** Introduced by feature-grooming story in sprint-2026-04-11. Complements Decision 44 (features.json schema and write authority) and Decision 45 (feature-status read path).

---

**Decision 50 — Feature Breakdown Skill: Canonical Feature-to-Story Gap Enumerator (sprint-2026-04-18)**

The `momentum:feature-breakdown` skill is the canonical entry point for converting a feature slug into a prioritized list of story gaps required to ship that feature end to end. No other skill in the practice takes a feature slug as primary input and produces a gap enumeration as output.

**Role boundary:** `feature-breakdown` is a pure orchestrator. It NEVER writes to `features.json`, `stories/index.json`, or any planning artifact. Its sole output is a ranked candidate list passed to `momentum:triage` for disposition. All classification and routing authority belongs to triage.

**Delegation contract:** `feature-breakdown` passes `source_label = "feature-breakdown:{feature_slug}"` to `momentum:triage`, satisfying the pre-enumerated-list contract. Triage classifies each candidate into the standard six classes (ARTIFACT / DISTILL / DECISION / SHAPING / DEFER / REJECT) and handles all writes.

**Why this skill exists:** The practice has no prior skill that takes a feature slug and authors the missing work.
- `momentum:feature-grooming` catalogs features (Decision 49) — does not enumerate story gaps
- `momentum:feature-status` reports health — read-only, no gap authoring
- `momentum:sprint-planning` assumes the backlog is already ready — does not create stories
- `momentum:triage` classifies pre-formed observations — does not enumerate what is missing

`feature-breakdown` fills this gap: given a feature, find what stories are required but do not yet exist.

**Non-responsibility:** `feature-breakdown` does NOT decide sufficiency. It identifies candidates. The developer and triage decide what becomes a story.

**Pattern references:** Fan-out spawning from Decision 41 / `spawning-patterns.md`; orchestrator purity from existing decisions; triage delegation contract from the triage row in the Skills Deployment Classification table.

---

**Workflow Modularization Note (2026-04-04)**

The Impetus `workflow.md` file is a structural concern at 800+ lines. The greeting redesign (Step 7 alone is 232 lines in the mockup) will increase this further. Modularization into separate workflow modules (e.g., `greeting.md`, `dispatch.md`, `install.md`) is architecturally sound and recommended but not required for the greeting redesign. This note flags the concern for future sprint planning.
