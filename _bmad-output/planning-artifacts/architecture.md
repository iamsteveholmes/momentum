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
lastEdited: '2026-06-11'
editHistory:
  - date: '2026-06-11'
    changes: 'Sprint-2026-06-10 spec impact (conductor seam-fix): Added .momentum/sprints/{sprint-slug}/build-ledger.jsonl — append-only conduct build ledger, sole writer Conductor — to the .momentum/ State Layout tree, the per-sprint folder structure tree, the per-sprint subdirectory prose (with a build-ledger.jsonl description block: rows appended at event time — story launches, stage transitions, finding dispositions, escalations, quarantines, coverage deferrals/discharges, contract-integrity stops, end-gate fixer events; corrections are append-only override rows, never edits; row vocabulary aligns with finding-schema.md v1.1 and build-results-ledger-schema.md v1.0 joined on story slug), and the Read/Write Authority table (sole writer: Conductor; read at step 2.0 resume rehydration and Phase 5 end-gate assembly). Extended Decision 59 with five paragraphs: branch-base rule (story/{slug} forked from current tip of sprint/{sprint-slug} — never main, never inferred default — then .worktrees/story-{slug}, before stage-1 dev spawn; idempotent remove-and-recreate for stale branches/worktrees; keeps merge-base review diff exactly story-scoped), stage-2 qa-reviewer finding normalization (Conductor-side deterministic adapter: verdict→severity BLOCKED→critical / MISSING→major / PARTIAL→minor, severity never derived from stakes; type from stakes_class; fixed legitimate:true / source:qa-reviewer / suggested_fix:null; story_slug from pipeline context; mirrors code-reviewer REVIEWER B adapter), coverage-deferral build-time semantics (covered-by defers only the dedicated QA verification run; adversarial code review always runs on every per-story diff, never deferred/demoted/skipped; stage-2 findings never unconditionally bound empty), build ledger (durable per-sprint record), and ledger-sourced end-gate/resume (step 2.0 rehydrates Conductor-scoped accumulators from the ledger; Phase 5 assembles the end-gate report from ledger rows; in-context accumulators are write-through convenience, ledger authoritative; interrupted-then-resumed build produces the same end-gate report as an uninterrupted run). Added conduct-path branch-base note to Parallel Story Execution Model worktree conventions. Added build-time semantics sentence to the story_assignments frozen-contract block (coverage_disposition). Updated Decision 59 Traceability line.'
  - date: '2026-05-18'
    changes: 'Sprint-2026-05-17 spec impact (DEC-029 Phase 1): Added momentum/verification-harness.json to plugin root layout table (defaults block + project block; sole writers: agent-builder, agent-guidelines). Added momentum/verification-harness.json row to Read/Write Authority table (readers: e2e-validator, sprint-planning; writers: agent-builder, agent-guidelines; plugin ships defaults with all surfaces "skip"). Updated Rules Architecture subsystem (4) to note verification-standard.md as a new plugin-shipped rule written by Impetus to ~/.claude/rules/ on first run, replacing retired docs/process/acceptance-testing-standard.md. Updated E2E Validator role description in Skills Deployment Classification and Decision 35 Application table: now method-polymorphic and harness-driven, dispatches by contract file extension (.eval.yaml, .trigger.md, .smoke.sh, .review.md, .feature), reads momentum/verification-harness.json at startup. Added verification_method as story file YAML frontmatter field (written by momentum:create-story at story creation time; derived from verification-standard.md routing table). Added coverage-plan.md to per-sprint folder structure tree (DEC-029; post-activation immutable). Updated .momentum/ State Layout tree and Installed Structure tree to reflect all 5 contract types in specs/ directory plus coverage-plan.md. Updated Protection Boundaries: specs/ now covers all 5 contract types (not Gherkin-only); added coverage-plan.md as post-activation immutable path. Updated sprint-planning Read/Write Authority row to include verification-harness.json as read, multi-extension contracts and coverage-plan.md as writes. Extended Decision 30 to cover all 5 contract types (not Gherkin-only). Added Decision 58 (DEC-029 D3: verification-harness.json Validation Harness Profile).'
  - date: '2026-05-16'
    changes: 'Sprint-2026-05-16 spec impact (DEC-023, DEC-026, DEC-028): Added momentum/agents.json to plugin root layout table (defaults block + project block, agent-builder sole writer). Added .momentum/beads-id-map.json (git-tracked slug→bead hash map) and .beads/ (gitignored Dolt DB) to Installed Structure tree. Added three rows to Read/Write Authority table: momentum/agents.json (sole writer: agent-builder), momentum-tools agent-resolve (pure resolver, no writes), agents/ux.md + analyst.md + researcher.md (structured output only). Added ux.md, analyst.md, researcher.md to agents/ directory listing in Repository Structure (preview + full) and Decision 35 plugin structure. Added base body conventions note to Decision 35: CREED block (3-5 I-verb-because anchors), constitution.md as project context source, mandatory output templates with AGENT_OUTPUT_START/END sentinel markers, prohibitions with consequence clauses. Added routing-table-driven specialist resolution note to Sprint Execution Flow Phase 2 (momentum-tools agent-resolve --role dev --touches). Added routing-table-driven reviewer resolution note to Sprint Execution Flow Phase 5 (momentum-tools agent-resolve --role qa-reviewer/e2e-validator). Added Decision 55 (DEC-023: Agent Routing Table — agents.json schema, defaults 9 roles + project block, glob-match resolution algorithm, 1..N fan-out, write_permissions enforcement). Added Decision 56 (DEC-026 D3/D5: Agent Builder Three-Skill Pipeline — constitution-builder Tier 1 once, agent-builder Tier 2 per role×domain, build-agents orchestrates, constitution.md as context source, agent-builder writes .claude/guidelines/agents/{role}-{domain}.md + routing entry). Added Decision 57 (DEC-028: Beads Dual-Write Spike — index.json authoritative, sprint-manager mirrors to beads best-effort, bd ready --json --claim as Phase 1 dependency source, bd prime --no-git-ops via SessionStart hook, .beads/ gitignored, .momentum/beads-id-map.json git-tracked, four gate criteria).'
  - date: '2026-05-03'
    changes: 'Canvas skill spec impact (sprint-2026-05-03): Added momentum:canvas to Skills Deployment Classification table (flat skill, invoker with SKILL.md + workflow.md + server.tsx; supersedes momentum:feature-status per DEC-019). Added canvas/ directory to Repository Structure tree (both preview and full). Deprecated momentum:feature-status in Skills Deployment Classification table, Read/Write Authority table, and all Integration Points mentioning feature-status (deprecated — use momentum:canvas per DEC-019). Added canvas server read authority row to Read/Write Authority table (reads: features.json, stories/index.json, sprints/index.json, stories/{slug}.md; no writes). Extended Decision 44 features.json schema: added note to stories field (also story_slugs alias), added depends_on field (feature-to-feature dependency list, optional). Added Decision 53 (DEC-017: Canonical Momentum Cycle Step Sequence — triage → intake → feature-grooming → epic-grooming → refine → sprint-planning → sprint-dev → retro; 7-node canvas timeline; required/optional phase classification; cycle boundary rule). Added Decision 54 (DEC-019: Hono+HTMX+Bun Canvas Runtime Stack — single-file server.tsx, port 3456, bun --hot; HTMX navigation protocol for lens/L2/L3 routes; dark/light polarity model with 140ms CSS cross-fade; supersedes DEC-011 D2 Vite approach).'
  - date: '2026-04-30'
    changes: 'Wave 1 retry — per-story `.md` relocation (Task 2.3b, AC #8 follow-up). Migrated 268 per-story spec files from `_bmad-output/implementation-artifacts/stories/{slug}.md` to `.momentum/stories/{slug}.md` (byte-equivalent, file count preserved). Legacy `_bmad-output/implementation-artifacts/stories/` directory deleted to enforce single-source-of-truth (AC #11, Task 2.8). Supersedes the prior 2026-04-30 AC9 entry below where individual story `.md` files were left at the legacy location.'
  - date: '2026-04-30'
    changes: 'Wave 1 state relocation AC9 fixes: `_bmad-output/implementation-artifacts/sprints/index.json` + `stories/index.json` moved to `.momentum/`. All skill workflows and `momentum-tools.py` updated. Individual story `.md` files were relocated in a follow-up entry above (superseded 2026-04-30). Updated Decision 45 inputs list + hash computation (stories/index.json path). Added momentum:triage row to Read/Write Authority table (`.momentum/signals/` write target). Added `.momentum/signals/` write note to VFL/AVFL row. AC: impetus-momentum-state-migration (DEC-011 D3, DEC-012).'
  - date: '2026-04-30'
    changes: 'Retired `.momentum/sprints/{slug}.json` per-sprint state file per DEC-012 (story fix-per-sprint-json-contract-drift) — sprint state consolidated to holistic `.momentum/sprints/index.json` (`active`, `planning`, `completed[]`, `quickfixes[]` sections) as the sole canonical source. Updated three sections: Read/Write Authority table (`momentum-tools sprint` row no longer lists per-sprint file as a write target), Protection Boundaries list (per-sprint file entry removed — no longer a protected path because it is no longer written), Sprint Tracking Schema (`.momentum/sprints/` folder description rewritten to describe one canonical state file plus per-sprint subdirectories for specs/sprint-summary/retro/audit-extracts; per-sprint folder structure tree preserved unchanged). DEC-012 clarifies DEC-011 D3 at the state-model level (D3 specified canvas-read scope only).'
  - date: '2026-04-28'
    changes: 'Sprint-2026-04-27 spec impact: State relocation to .momentum/ closes DEC-011 Gate G1 (impetus-momentum-state-migration). Added .momentum/ State Layout top-level section (single-source-of-truth invariant, hidden-prefix rationale, per-sprint subtree, signals/ ledger pattern with read-only contract). Updated all path references in Read/Write Authority table, Session-open sequence, Sprint Tracking Schema, and Installed Structure tree from `_bmad-output/implementation-artifacts/{sprints,stories,intake-queue.jsonl}` to `.momentum/` paths; planning carve-out: features.json stays under _bmad-output/planning-artifacts/. Added per-story approval contract — `approvals: []` on sprint records with story_file_sha (SHA-256), activation gate against current-matching SHAs (sprint-planning-adds-per-story-approval-gate). Added sprint-dev pre-execution verification gate (Phase 1 verify-approvals subcommand). Extended CMUX Markdown Surfaces integration to sprint-planning per-story approval viewer. Added Impetus session-start preflight component — plugin-cache-vs-source version-skew detector with status taxonomy (match/skew-cache-behind/skew-cache-ahead/no-cache/no-source/indeterminate) and `momentum-tools session plugin-cache-check` CLI; one explicit exception to never-narrate-the-reads rule (plugin-cache-staleness-detection). Added Orchestrator Behavioral Guards pattern with retro Phase 4 singleton-count guard as canonical example (retro-team-singleton-guard). Codified Decision 34 defense-in-depth: agent-definition Critical Constraints must be self-sufficient — QA Reviewer + E2E Validator parity contract for Phase 5 reviewer spawns (harden-sprint-dev-phase5-spawn-prompts). Added Decision 41 retro Phase 4 row (documenter as singleton coordinator distinct from auditor fan-out). Refined Decision 34 BLOCKED-vs-MISSING semantics — BLOCKED for missing infrastructure, MISSING reserved for execution-succeeded-without-AC-evidence; both reviewers follow .claude/rules/e2e-validation.md Environment Startup. Extended Decision 27 Wave 1 with dynamic transcript-query.py path resolution, worktree session discovery, UTC end-of-day inclusivity, --story-slugs filter, and explicit hard-fail on zero session matches. Promoted peek-first / 500-line-chunk convention to documented architectural convention under Cross-Cutting Concerns. Added one-line note that retire-sprint-log-final-cleanup story closes the ARCH-5 sprint-log historical cleanup.'
  - date: '2026-04-26'
    changes: 'Refine drift reconciliation (arch-1 through arch-5): Added Decision 51 (DEC-005 Cycle Redesign — formal section summarizing sub-decisions D1/D2/D5/D6/D7/D8/D10 referenced from triage-skill and retro-triage-handoff stories). Added Decision 52 (DEC-007 Unified Triage/Retro Capture Artifact — formal section summarizing intake-queue.jsonl producer/consumer model, CLI-only writes, retired triage-inbox.md). Added momentum:agent-guidelines to Repository Structure tree (both preview and full structure) and Requirements to Structure Mapping (FR61a). Added momentum_version field to Decision 1c findings-ledger schema and findings JSON example, with cross-reference to Decision 43; extended Decision 42 (Distill) ledger write authority paragraph with explicit momentum_version mention. Added intake-queue.jsonl to Installed Structure tree (under _bmad-output/implementation-artifacts/) and Requirements to Structure Mapping. Added per-sprint folder structure tree (under Sprint Tracking Schema) showing sprints/{sprint-slug}/sprint-summary.md alongside specs/, retro-transcript-audit.md, and audit-extracts/.'
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

4. **Rules Architecture (Tier 3 Advisory)** — Global `~/.claude/rules/` (authority hierarchy, anti-patterns, model routing) + project `.claude/rules/` (architecture conventions, stack-specific standards). Project-scoped rules auto-load in every session including subagents. Rules are bundled in `references/rules/` at the plugin root. The plugin install mechanism does not write to `~/.claude/rules/` or `.claude/rules/` directly — Impetus writes rules to both targets on first `/momentum:impetus` invocation using the Write tool. No separate setup step. **`skills/momentum/references/rules/verification-standard.md` is a plugin-shipped rule (added sprint-2026-05-17, `enforced-verification-rule` story): Impetus writes it to `~/.claude/rules/` on first run. It establishes the enforcement-tier taxonomy, change-type → verification-method routing table, and the mandatory `verification_method` frontmatter field for story files. It replaces `docs/process/acceptance-testing-standard.md`, which is now retired.** **`skills/momentum/references/rules/decision-grade-presentation.md` is a plugin-shipped enforced rule (added sprint-2026-06-02, conduct-core; DEC-036 D5): Impetus writes it to `~/.claude/rules/` on first run, alongside `verification-standard.md`. It establishes the practice-wide decision-grade presentation standard — `effort` drives work depth while measurable caps (≤N bullets / word budgets, executive-summary-first, output schemas) govern output verbosity — bounded by a self-sufficiency floor: every decision must carry its `what / why / evidence` inline so the human never has to reference other material to make a call ("tight on the irrelevant, complete on the decision-relevant"). It applies to the conduct end-gate template and the live conversational skills.**

5. **Subagent Composition** — code-reviewer (read-only tools, pure verifier, never modifies code), architecture-guard (pattern drift detection), momentum:dev (story executor, spawned by sprint-dev skill). code-reviewer and architecture-guard use `context: fork` for producer-verifier isolation. momentum:dev runs as a flat subagent (main context) for story execution. Three-layer agent model (Decisions 26, 55, 56): (1) Base roles — generic agent definitions (Dev, QA, E2E Validator, Architect Guard) shipped with the plugin; (2) Routing table resolution — `momentum/agents.json` maps story `change_type` / `touches` paths to specialist agent files via glob-match (Decision 55 / DEC-023); (3) Project-composed specialist files — base body + constitution + **manifesto (the diagnostic-table tier)**, assembled by the agent-builder pipeline (Decision 56 / DEC-026). This three-layer **composition** model reconciles with DEC-008's three-**tier** agent model: the composed specialist (layer 3) is itself **base body + constitution + manifesto**, and the **manifesto tier** is named canonically per DEC-026 D4 / DEC-038 — it is the agent's stable, per-role×domain **diagnostic table** (observable developer symptom → exact `wiki-query` KB lookup), *not* a per-sprint or per-story context overlay. See Decision 56 for the full manifesto definition. The old two-layer description ("Momentum provides generic roles; projects provide role-specific stack guidelines wired together during sprint planning") is superseded by this three-layer model where the routing table is the resolution mechanism between generic roles and project-specific specialists. Agent Teams share a working directory with commit-as-sync-point. Hub-and-spoke: Impetus is the sole user-facing voice; subagents return structured output to Impetus for synthesis. Subagents cannot spawn subagents — chains route through main conversation.

6. **Validate-Fix Loop (VFL) Skill** — Three profiles: Gate (1 agent, pass/fail), Checkpoint (2-4 agents, 1 fix attempt), Full (dual-reviewer per lens, up to 4 fix iterations). Four lenses: Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness. Consolidation handles deduplication, cross-check confidence tagging, and scoring. Invocable standalone, inline from workflows, or declared as a rule.

7. **Orchestrating Agent — Impetus** — Session orientation via 9-state greeting (Decision 37) with adaptive menus, visual progress (✓ Built / → Now / ◦ Next) for workflow phases, proactive gap detection, productive waiting during subagent execution, hub-and-spoke voice unification, narrative voice contract (Decision 38). Impetus is the primary entry-point skill (`/momentum:impetus`) and the recommended path for all Momentum operations. Users can invoke other namespaced skills directly (e.g., `/momentum:sprint-planning`), but Impetus provides session orientation and context that direct invocation skips. For sprint-scoped operations, Impetus dispatches to dedicated skills: `/momentum:sprint-planning` for story selection and team composition, `/momentum:sprint-dev` for dependency-driven execution. **Per DEC-037, "run the sprint build" may also route to `/momentum:conduct` — the standalone conduct execution engine, which coexists with `/momentum:sprint-dev` (both builders live during the transition; sprint-dev's wave loop is retired later at adoption).** When invoked directly as the top-level session, `/momentum:conduct` legitimately owns commits, merges, and the approve-time `git push` (orchestrator-purity forbids only *spawned* subagents from mutating git — see Decision 59). Sub-command dispatch: developer selects from the greeting menu (e.g., "Continue the sprint", "Run retro", "Plan a sprint"), and Impetus invokes the corresponding skill. Sprint lifecycle transitions follow Decision 36 state machine. Impetus is the force that maintains practice velocity — the system keeps compounding because Impetus carries knowledge and context forward across sessions and sprints without requiring repeated external input.

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
7. **Peek-first read convention (added 2026-04-28)** — High-volume artifacts (`agent-summaries.jsonl`, `errors.jsonl`, `prd.md`, `architecture.md`, `stories/index.json`, retro extracts) are NEVER read with a full Read in one call. The convention: `wc -l` first to peek the size, then read in 500-line chunks via the `offset`/`limit` pattern. Skills that consume these artifacts (Impetus, sprint-planning, sprint-dev, retro auditors) MUST follow this convention to keep context budgets predictable. This is an architectural convention, not a hint — workflows that violate it accumulate avoidable token cost and risk truncation.

---

## `.momentum/` State Layout

<!-- Added 2026-04-28: Single-source-of-truth state layout. Closes DEC-011 Gate G1. Origin: impetus-momentum-state-migration story. -->

> _[Added 2026-04-28: Sprint-2026-04-27 introduces `.momentum/` as the single, hidden top-level location for Momentum's operational runtime state. Replaces the prior split where sprints/stories/intake-queue lived under `_bmad-output/implementation-artifacts/`. Closes DEC-011 Gate G1.]_

Momentum's operational runtime state lives under a single hidden top-level directory: `.momentum/` at the project root. This directory holds everything the practice itself produces and consumes during normal operation — sprint records, story index, signals, the intake queue, and per-sprint working subtrees. Planning artifacts that describe what to build (PRD, architecture, epics, decisions, assessments) remain under `_bmad-output/planning-artifacts/` — that carve-out is intentional. Note: `features.json` was the prior planning artifact for feature taxonomy; it is superseded by `epics.json` per DEC-034 (2026-05-25).

### Layout

```
.momentum/                                       ← Operational runtime state (single source of truth)
├── sprints/
│   ├── index.json                               ← Active / planning / completed sprint registry (Decision 36)
│   └── {sprint-slug}/                           ← Per-sprint subtree
│       ├── sprint-summary.md                    ← Decision 47 — written by retro at Phase 6 close
│       ├── retro-transcript-audit.md            ← Decision 27 — written by retro documenter
│       ├── specs/                               ← Contract files (sprint-planning writes; verifier-only reads)
│       │   ├── {story-slug}.feature             ← Gherkin (Decision 30)
│       │   ├── {story-slug}.eval.yaml           ← LLM eval
│       │   ├── {story-slug}.trigger.md          ← Trigger-based
│       │   ├── {story-slug}.smoke.sh            ← Smoke test
│       │   └── {story-slug}.review.md          ← Manual review
│       ├── coverage-plan.md                     ← Per-sprint verification coverage plan (DEC-029; post-activation immutable)
│       ├── build-ledger.jsonl                   ← Append-only conduct build ledger (Decision 59 — sole writer: Conductor)
│       └── audit-extracts/                      ← Decision 27 — DuckDB preprocessing output
│           ├── user-messages.jsonl
│           ├── agent-summaries.jsonl
│           ├── errors.jsonl
│           └── team-messages.jsonl
├── stories/
│   ├── index.json                               ← Lightweight story index (slug → status, epic, depends_on, touches, priority)
│   └── {slug}.md                                ← Story files (written by momentum:create-story)
├── signals/                                     ← RETIRED — absorbed into practice-ledger (DEC-033 D6; see note below)
├── practice-ledger.jsonl                        ← Append-only event log (DEC-033 / Decision 52 superseded — true append-only, CLI-only writes via momentum-tools practice-ledger)
└── practice-ledger-pre-2026-05.jsonl            ← Hard-cut archive of the prior intake-queue.jsonl (88 entries; legacy schema; read-only; DEC-033 D8)
```

### Single-source-of-truth invariant

`.momentum/` is the **only** location for these artifacts. There is no fallback to a legacy path, no symlink to `_bmad-output/implementation-artifacts/`, no dual-write. Skills resolve paths to `.momentum/` directly. Migration of pre-existing state is handled once by the `impetus-momentum-state-migration` story; after migration, `_bmad-output/implementation-artifacts/{sprints,stories,intake-queue.jsonl}` is gone.

**entity_id semantics (DEC-033):** The practice-ledger uses two identifiers per event row. `event_id` identifies the immutable event row (unique, never reused). `entity_id` identifies the logical thing the event is about — it repeats across rows for the same logical entity. "Open" is a derived state: fold all events by `entity_id`, take the last by `ts`; if that last event is non-terminal (`consumed`, `rejected`, `closed_stale` are terminal; all others are non-terminal), the entity is open. State is never stored — derivation is the source of truth.

### Hidden-prefix rationale

The leading `.` distinguishes operational state (Momentum's working memory) from source content (planning artifacts, code, docs). Hidden directories are conventional for "tooling state" in Unix-shaped projects (`.git/`, `.cache/`, `.claude/`). Developers do not need to browse `.momentum/` during normal work — Momentum skills read and write it on their behalf. Surfacing it as a hidden directory keeps the visible project tree focused on intentional content.

### Planning artifact carve-out

`_bmad-output/planning-artifacts/epics.json` (and the rest of `_bmad-output/planning-artifacts/`) intentionally stays where it is. Planning artifacts are spec/source — they describe the product, are committed to the repo as primary content, and are produced by planning workflows (PRD, architecture, epic grooming). They are not Momentum's operational state.

### `.momentum/signals/` — RETIRED (DEC-033 D6)

> _[Retired 2026-05-28 by story a1-practice-ledger-schema-cli-redesign-true-append-only (DEC-033 D6): The `signals/` subsection and its directory are absorbed into the unified practice-ledger. The two signal use cases — `triage-uncleared` and `avfl-finding-pending-upstream-fix` — are now entries in `.momentum/practice-ledger.jsonl` with `source: triage` / `source: avfl` and appropriate `payload`. Every open entry in the ledger IS the attention surface; no separate attention-filter mechanism is needed. ARCH-8 is resolved by this retirement — since no producers were ever shipped, there is no migration burden. Impetus session-start drops the `signals/*.json` read and replaces it with `momentum-tools practice-ledger summary`. See DEC-033 D6 for full rationale and the DEC-033 D9 Impetus surfacing model update.]_

The schema documentation is preserved below for historical traceability only. **This subsection is no longer active. Do not implement new writers for `.momentum/signals/`.**

**Retired signal types (use practice-ledger entries instead):**
- `triage-uncleared` → practice-ledger entry with `source: "triage"` and `event_type: "created"` / `payload: {kind: "triage-uncleared", ...}`
- `avfl-finding-pending-upstream-fix` → practice-ledger entry with `source: "avfl"` and appropriate `payload`

### Cross-references

- **DEC-011 Gate G1** — closure of the state-relocation gate; this section operationalizes the gate's exit criteria
- **Decision 27** — retro audit-extracts subtree under `.momentum/sprints/{slug}/audit-extracts/`
- **Decision 30** — Gherkin specs subtree under `.momentum/sprints/{slug}/specs/`
- **Decision 36** — sprint lifecycle state machine; `.momentum/sprints/index.json` is its store
- **Decision 47** — sprint-summary.md path; written under `.momentum/sprints/{slug}/`
- **Decision 52 (DEC-007) — SUPERSEDED by DEC-033** — see rewritten Decision 52 section below; `.momentum/practice-ledger.jsonl` is the current unified event log

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
| epic-grooming | Flat skill (`/momentum:epic-grooming`) | Unified grooming skill (DEC-034 D6): sole writer of `epics.json`; bootstrap/refine mode detection; value analysis + system_context + acceptance_condition on every epic; taxonomy orphan resolution and story reassignment via momentum-tools; absorbs former momentum:feature-grooming (retired B4) and former categorical epic-grooming scope. |
| refine | Flat skill (`/momentum:refine`) | Backlog refinement: two-wave planning artifact discovery and update (Wave 1 discovers PRD + architecture coverage gaps in parallel; Wave 2 conditionally spawns update agents per developer approval), status hygiene detection, delegation to epic-grooming, stale-story triage, batch approval UX; CLI-only mutations |
| intake | Flat skill (`/momentum:intake`) | User-invokable; **single-item capture only** — one idea → one story stub, feature-slug and story-type aware per DEC-005 D1/D5. No batching (that is `momentum:triage`'s job). Writes `stories/{slug}.md` + `stories/index.json` entry via `momentum-tools sprint story-add`. |
| triage | Flat skill (`/momentum:triage`) | Orchestrator; `model: claude-sonnet-4-6`, `effort: high`. Multi-item batch classification of observations into five active classes (ARTIFACT / DECISION / SHAPING / DEFER / REJECT) per DEC-005. The DISTILL class is removed post-removal of the distill skill (ARCH-1/ARCH-5). Delegates ARTIFACT → `momentum:intake`, DECISION → `momentum:decision`; writes SHAPING / DEFER / REJECT inline to `practice-ledger.jsonl` as `created` events via `momentum-tools practice-ledger append` CLI (DEC-033 supersedes DEC-007 intake-queue writes). Deterministic prefilter via `momentum-tools triage prefilter` (TF-IDF + Jaccard + epic boost, status-filtered, top-K=10 shortlist); inline batch clustering; parallel per-cluster dedup fan-out subagents returning per-theme JSON findings; inline consolidation-candidate grouping; five-class classification for unique survivors. Performs no gap-check (DEC-005 D10). Entry point replaces the Impetus `[3] Triage` placeholder. |
| epic-breakdown | Flat skill (`/momentum:epic-breakdown`) — **renamed from feature-breakdown (B4, DEC-034 D6)** | Pure orchestrator; takes an `epic_slug` as input, enumerates story gaps end-to-end, passes pre-enumerated candidate list to `momentum:triage` with `source_label = "epic-breakdown:{epic_slug}"`. NEVER writes to epics.json or stories/index.json. Reads `epics.json` (not features.json). |
| distill | Flat skill (`/momentum:distill`) — **(removed — `remove-momentum-distill` story ready-for-dev)** | Practice-artifact distillation: session learning or retro finding → 2-agent discovery (Enumerator + Adversary) → classify fix scope → apply to artifact → scoped AVFL validation. Previously listed as third execution path alongside sprint orchestration and quick-fix (Decision 42). **ARCH-1: This skill is being removed. The `remove-momentum-distill` story is ready-for-dev. Decision 42 references to distill as an active execution path are deprecated; see Decision 42 note below.** |
| assessment | Flat skill (`/momentum:assessment`) | User-invokable; evaluates a story or backlog item for readiness, risk, and completeness; no fork needed |
| sprint-manager | Flat skill (`/momentum:sprint-manager`) | Wraps momentum-tools.py CLI; provides /momentum:sprint-manager command for sprint lifecycle management (activate, close, status); sole writer of sprints/index.json in conjunction with momentum-tools CLI. |
| decision | Flat skill (`/momentum:decision`) | User-invokable; facilitates architectural or product decision capture (ADR/trade-off analysis); no fork needed |
| agent-guidelines | Flat skill (`/momentum:agent-guidelines`) | 5-phase guided workflow for generating technology-specific development guidelines for a project: Discover (stack analysis), Research (web search), Consult (developer preferences), Generate (guidelines documents), Validate (AVFL checkpoint). Generates path-scoped rules and reference documents. |
| feature-status | Flat skill (`/momentum:feature-status`) — **(deprecated — use momentum:canvas)** | Reads ~~features.json~~ `epics.json` **(DEC-034)** + stories/index.json; writes self-contained HTML dashboard and YAML-frontmatter cache. **Deprecated by DEC-019 (2026-05-03) — canvas supersedes this skill as the unified planning dashboard.** |
| canvas | Flat skill (`/momentum:canvas`) — invoker (SKILL.md + workflow.md + server.tsx) | Bun-based live dashboard server (port 3456). Reads `epics.json` **(DEC-034 — replaces features.json)**, stories/index.json, sprints/index.json to render a Hono+HTMX multi-lens planning canvas. Three view layers: L1 timeline/cycle overview (dark), L2 epic detail (warm light), L3 story detail (warm light). No writes. Canvas update to render epics instead of features: story B3 (sprint-2026-05-26). |
| status | Not planned as standalone skill | ~~Status functionality is absorbed into Impetus greeting workflow and momentum-tools CLI (`momentum-tools sprint status`). No backlog story exists or is needed.~~ **Superseded by Decision 45 (sprint-2026-04-11):** feature-status is implemented as a dedicated standalone skill (`/momentum:feature-status`). The startup-preflight cache check (Decision 46) handles the Impetus greeting integration path. The momentum-tools `feature-status-hash` command provides the hash utility. This row is retained for historical context only. |
| code-reviewer | `context: fork` skill | Pure verifier — `context: fork` provides isolation; `allowed-tools: Read` enforces read-only. Also useful standalone (Decision 35). |
| architecture-guard | `context: fork` skill | Pattern analysis — isolation prevents drift; `allowed-tools: Read` enforces read-only. Also useful standalone (Decision 35). |
| QA reviewer | Agent definition file (`agents/qa-reviewer.md`) | Pure spawned worker — reviews code against story ACs during Team Review (Decision 34). Never user-invoked (Decision 35). |
| E2E Validator | Agent definition file (`agents/e2e-validator.md`) | Pure spawned worker — method-polymorphic and harness-driven (sprint-2026-05-17, `e2e-validator-agent-body-rewrite` story). Reads `momentum/verification-harness.json` at startup; dispatches by contract file extension: `.eval.yaml` (LLM eval), `.trigger.md` (trigger-based), `.smoke.sh` (smoke test), `.review.md` (manual review prompt), `.feature` (Gherkin). Never user-invoked (Decision 35). Used in sprint Team Review (Decision 34) and quick-fix Phase 4 validation (Decision 40). |
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
│   ├── canvas/                     ← /momentum:canvas (DEC-019; supersedes feature-status — ARCH-6)
│   │   ├── SKILL.md
│   │   ├── workflow.md
│   │   └── server.tsx               ← Bun+Hono+HTMX server (port 3456, bun --hot)
│   ├── intake/SKILL.md             ← /momentum:intake
│   ├── assessment/SKILL.md         ← /momentum:assessment
│   ├── decision/SKILL.md           ← /momentum:decision
│   ├── agent-guidelines/SKILL.md   ← /momentum:agent-guidelines (5-phase guided workflow, FR61a)
│   └── retro/SKILL.md
├── agents/                           ← Agent definition files (Decision 35)
│   ├── qa-reviewer.md               ← Pure worker: story AC review (Team Review)
│   ├── e2e-validator.md             ← Pure worker: behavioral validation (Team Review)
│   ├── dev.md                        ← Base dev agent for sprint-dev spawning
│   ├── dev-skills.md                ← Specialist: SKILL.md, workflow.md, agent definitions
│   ├── dev-build.md                 ← Specialist: Gradle and build system work
│   ├── dev-frontend.md              ← Specialist: Kotlin Compose and frontend UI work
│   ├── ux.md                         ← Specialist: UX design and UI specification work
│   ├── analyst.md                    ← Specialist: business analysis and requirements work
│   └── researcher.md                 ← Specialist: technical research and discovery work
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

| Directory / File | Purpose | Delivered by |
|---|---|---|
| `.claude-plugin/` | Plugin manifest | Plugin install |
| `skills/` | All SKILL.md files (flat + context:fork) | Plugin install |
| `hooks/` | Always-on hook definitions (`hooks.json`) | Plugin install |
| `scripts/` | CLI tools (`momentum-tools.py`) | Plugin install |
| `references/` | Rules, practice docs, version manifest | Plugin install |
| `agents/` | Custom agent definitions for teams | Plugin install |
| `momentum/agents.json` | Agent routing table — `defaults` block (9 roles defined; not all shipped — see ARCH-3 note in Decision 55) + `project` block (per-role×domain entries, written by agent-builder) | Plugin ships defaults; agent-builder writes project entries |
| `momentum/verification-harness.json` | Validation harness profile — `defaults` block (plugin-shipped) + `project` block (per-project overrides written by agent-builder/agent-guidelines) | Plugin ships defaults block; agent-builder/agent-guidelines write project block |
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
- Structured findings with fields: `id` (globally unique, format `F-{unix_ms}-{random_4hex}`), `project` (string, project identifier), `story_ref`, `phase`, `severity`, `pattern_tags`, `description`, `evidence`, `provenance_status`, `upstream_fix_applied`, `upstream_fix_level`, `upstream_fix_ref` (reference to the fix artifact), `momentum_version` (installed plugin version at write time, populated by all writers per Decision 43), `timestamp` (ISO 8601 when finding was recorded)
- `upstream_fix_level` — null until a fix is applied; then one of: `spec-generating-workflow | specification | rules-or-CLAUDE.md | tooling | one-off-code-fix`
- `momentum_version` — populated by every ledger writer (`momentum:retro`, flywheel) at write time per Decision 43 (Findings-Ledger Versioning, Option A). Enables regression detection by mapping findings to the practice version that produced them. Entries written before the field's introduction are backfilled via Decision 43 Option B (git log timestamps). Note: `momentum:distill` was previously listed as an authorized writer; it is removed with the distill skill (see Decision 42 — removed).
- Queryable for cross-project and cross-story pattern detection
- JSONL enables concurrent append from multiple Claude Code sessions without file locking (POSIX atomic append for lines under pipe buffer size)
- Authorized writers: flywheel workflow (`origin: flywheel`) only. `momentum:distill` is removed as an authorized writer (ARCH-7: distill skill removed — see Decision 42). The `origin` field distinguishes code-review-origin findings for FR33 ratio tracking. All other components are read-only.
- Rationale: Global scope enables cross-project pattern detection — the same anti-pattern appearing in projects A and B becomes visible. Per-project scope would miss these systemic patterns.

> **DEC-033 D10 — Forward pointer (AMENDED 2026-05-28):** When Epic 6 flywheel work eventually activates the Findings Ledger, the implementation MUST inherit the event-log shape established by DEC-033 (Decision 52 superseded): `event_id` (immutable per row, unique) + `entity_id` (repeats for the same logical entity), append-only writes with no whole-file rewrites, and closure as appended events not field mutations. The current schema above (with `id` as a single unique identifier) should be updated at activation time to adopt the `event_id` / `entity_id` distinction. This forward pointer exists because the latent defect class — JSONL whole-file-rewrite on consume — was the root cause of the intake-queue.jsonl production defects resolved by DEC-033. Do not reproduce the defect when activating this ledger. See `_bmad-output/planning-artifacts/decisions/dec-033-practice-ledger-event-log-redesign-2026-05-25.md` for the full event-log design rationale.

**Decision 1e — Session State Storage (Ephemeral + Inter-Session)**
- `.claude/momentum/session-modified-files.txt` — Ephemeral session-scoped file. Written by PostToolUse lint hook (appends file paths of modified files, one per line, deduped). Read by Stop gate hook as the set of files to check. Cleaned up after the Stop gate runs. Not committed to git.
- `.claude/momentum/gate-findings.txt` — Inter-session findings file. Written by the Stop gate hook when it detects lint issues or uncommitted changes among session-modified files. Read by Impetus at the next session open to surface unresolved quality issues from the previous session. Overwritten each time the Stop gate runs (not append-only).

**Decision 1f — Feature Status Cache: YAML-Frontmatter MD** _(deprecated — ARCH-6: canvas supersedes feature-status; cache files removed from installed structure)_
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
| `~/.claude/momentum/findings-ledger.jsonl` | Ledger integrity — authorized writer: flywheel workflow only (Decision 1c; `momentum:distill` removed as authorized writer — ARCH-7). Note: global path is outside project PreToolUse scope; protection enforced by authority rule. |

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
- Implementation → `momentum:dev` (dispatched per story by sprint-dev; `momentum:dev` resolves the specialist agent via agents.json routing-table, then delegates to the specialist agent file — path: sprint-dev → `momentum:dev` → agents.json routing-table resolution → specialist agent files; returns structured completion signal)
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

**Session open sequence (updated 2026-04-28; amended 2026-05-28 per DEC-033):** At session start, Impetus reads `.momentum/sprints/index.json` (sprint lifecycle state per Decision 36), `.momentum/stories/index.json` (story statuses), runs `momentum-tools practice-ledger summary` (honest ledger counts — DEC-033 D9; replaces the prior `signals/*.json` iteration which is retired per DEC-033 D6), and reads `~/.claude/momentum/global-installed.json` (completion count for first-session detection). It also runs `momentum-tools session plugin-cache-check` to detect plugin-cache-vs-source version skew (see Impetus session-start preflight component below). From these inputs, Impetus determines one of 9 greeting states (Decision 37), renders the corresponding narrative and menu, then writes session stats to `global-installed.json`. The stats write is invisible to the user — no visible diff during the greeting. Stats write is deferred until after the menu is displayed.

**Situational State — Practice ledger summary (updated 2026-05-28 per DEC-033 D9):** The prior "Pending signals present" state (which read `.momentum/signals/*.json`) is **retired** alongside the signals/ directory (DEC-033 D6). Impetus instead reads `momentum-tools practice-ledger summary` and surfaces honest counts: "N open entries (X this week, Y older than 30 days, Z near auto-close)". Recurring `closed_stale` patterns for the same entity shape are surfaced as meta-signals (e.g., "'X' has been closed_stale 4 times in 60 days"). Developer drills in via `momentum-tools practice-ledger open` when curious. No inline enumeration of entries — counts only (DEC-033 D9 anti-pattern guard against the prior "last 5" defect). An empty ledger or zero open entries produces no ledger-related output in the situational band and is not an error.

**Adaptive Menu Construction:**

Menu items are constructed algorithmically based on the detected greeting state. Each state produces a 3 or 4 item numbered menu. The items are drawn from this palette:

| Menu item | Dispatches to | Appears when |
|---|---|---|
| Run the sprint / Continue the sprint | `/momentum:sprint-dev` **or** `/momentum:conduct` (DEC-037 — coexisting builders; conduct runs as the top-level session and owns git) | Active sprint exists |
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
  "origin": "flywheel",           // flywheel — sole authorized writer (distill removed — ARCH-7); origin field retained for schema compatibility
  "momentum_version": "1.4.2",    // installed plugin version at write time — populated by all ledger writers per Decision 43 (regression detection)
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

**Orchestrator Behavioral Guards — post-spawn singleton-count guard (added 2026-04-28):**

A defensive pattern for orchestrators that spawn fixed-cardinality teams: after the spawn call returns, the orchestrator MUST assert that the spawned team's actual composition matches the declared composition before any downstream coordination begins. If the assertion fails, the orchestrator HALTs and surfaces the mismatch — it does not attempt to recover by spawning additional agents or proceeding with a partial team.

**Canonical example — retro Phase 4 invariant guard:** Retro Phase 4 spawns 4 agents using Shape A (preferred topology): 1 documenter as a singleton coordinator (individual Agent spawn) and 3 auditors fanned out as individual Agent spawns (`auditor-human`, `auditor-execution`, `auditor-review`). After spawning, the retro orchestrator asserts:

- Exactly one agent has role `documenter`
- Exactly three agents have role `auditor`
- The three auditor `subagent_type` values are distinct (`auditor-human` ≠ `auditor-execution` ≠ `auditor-review`)

Any mismatch (e.g., two documenters because the orchestrator's spawn prompt was misinterpreted, or only two auditors because one role was dropped) triggers a HALT. The orchestrator emits a structured error and stops — it does not "fix" the team by spawning a missing agent.

**Why a post-spawn guard:** The spawn layer is treated as a black-box primitive — the orchestrator declares intent, but the actual team composition is observable only after the call. Defensive composition checking catches integration drift between the orchestrator's declared `<team-composition>` (Decision 41) and the spawn-mechanics layer's behavior. The guard is the orchestrator's last line of defense against silent miscomposition.

**Shape A vs Shape B:** Shape A (preferred) spawns the documenter as a singleton individual Agent and fans out the 3 auditors as individual Agent calls, eliminating the TeamCreate multiplexing path entirely. Shape B (fallback only) keeps all 4 roles in TeamCreate when a documenter handle must be carried in TeamCreate config — each role declared exactly once with no implicit cardinality. Use Shape A unless the documenter handle cannot be passed via any other mechanism.

**Origin:** `retro-team-singleton-guard` story (sprint-2026-04-27). The pattern is reusable beyond retro — any orchestrator spawning a fixed-cardinality team should apply the same post-spawn invariant check.

**Impetus session-start preflight component — plugin-cache-vs-source version-skew detector (added 2026-04-28):**

Impetus session start runs a lightweight version-skew check against the installed Momentum plugin cache vs. the working source tree. The check is implemented as `momentum-tools session plugin-cache-check` and surfaces one of six status values:

| Status | Meaning |
|---|---|
| `match` | Plugin cache version equals source version. Normal startup. |
| `skew-cache-behind` | Cache is older than source. Source has unreleased work; cached plugin behavior may diverge from in-tree skill files. |
| `skew-cache-ahead` | Cache is newer than source. Cached plugin contains shipped work not present in this checkout. |
| `no-cache` | Plugin cache absent. Plugin not yet installed on this machine, or cache cleared. |
| `no-source` | Source tree absent or unrecognized. Running outside a Momentum source checkout (normal for downstream projects). |
| `indeterminate` | Version metadata unreadable on either side. Surface as a soft warning, do not block. |

**Narration exception:** Per the established convention, Impetus does not narrate its session-start reads ("Reading sprints/index.json…" is noise). The plugin-cache check is the **one explicit exception** to that rule — when the status is anything other than `match` or `no-source`, Impetus narrates the skew status in a single sentence so the developer is aware that practice behavior may not match in-tree skill files. This narration rule is enforced as part of the greeting state composition; future preflight checks must justify their narration explicitly rather than inheriting this exemption.

**Origin:** `plugin-cache-staleness-detection` story (sprint-2026-04-27). Closes a category of "why is the practice behaving like a previous version?" diagnostic friction.

**Defense-in-depth across spawn-prompt and agent-definition layers (added 2026-04-28):**

Decision 34 (AVFL Hybrid Resolution Team) establishes that Phase 5 reviewer agents — QA Reviewer and E2E Validator — are agent definition files (`agents/qa-reviewer.md`, `agents/e2e-validator.md`). These definitions carry their own Critical Constraints sections and must be **self-sufficient**: a reviewer spawned from these definitions must classify ACs correctly even if the orchestrator's spawn prompt is silent on a given concern. The orchestrator's spawn prompt and the agent definition are two independent enforcement layers — neither may rely on the other to be the only source of a critical rule.

**Parity contract:** Every Critical Constraint that appears in the QA Reviewer definition must appear in the E2E Validator definition (and vice versa) when the constraint applies to both roles. Examples: AC classification rules, BLOCKED-vs-MISSING semantics, the mandate to follow `.claude/rules/e2e-validation.md` Environment Startup before classifying any AC. Drift between the two definitions creates inconsistent classifications between reviewers in the same sprint — which is a defect at the Decision 34 contract level.

**Origin:** `harden-sprint-dev-phase5-spawn-prompts` story (sprint-2026-04-27). Codified into Decision 34's "What does NOT change type" guidance — see Decision 34 update below.

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
│   ├── distill/                             ← /momentum:distill (removed — ARCH-1; `remove-momentum-distill` story ready-for-dev)
│   │   └── SKILL.md
│   ├── research/                            ← /momentum:research
│   │   └── SKILL.md
│   ├── canvas/                              ← /momentum:canvas (DEC-019; supersedes feature-status — ARCH-6)
│   │   ├── SKILL.md
│   │   ├── workflow.md
│   │   └── server.tsx                       ← Bun+Hono+HTMX server (port 3456, bun --hot)
│   ├── agent-guidelines/                    ← /momentum:agent-guidelines (FR61a, 5-phase guided workflow)
│   │   └── SKILL.md
│   ├── conductor/                           ← /momentum:conduct (Decision 59 — in-session conduct execution engine; DEC-035/036/037)
│   │   └── SKILL.md
│   ├── constitution-builder/                ← /momentum:constitution-builder (Decision 56 / DEC-026 D3 — Tier 1: hot constitution + ## Quick Routing)
│   │   └── SKILL.md
│   ├── agent-builder/                       ← /momentum:agent-builder (Decision 56 / DEC-026 D5 — Tier 2: composes base body + constitution + manifesto → composed agent + agents.json entry)
│   │   └── SKILL.md
│   ├── refine/                              ← /momentum:refine (backlog hygiene — planning-artifact drift detection, status mismatches, stale-story triage)
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
│   ├── dev-frontend.md                      ← Specialist: Kotlin Compose and frontend UI work
│   ├── ux.md                                ← Specialist: UX design and UI specification work
│   ├── analyst.md                           ← Specialist: business analysis and requirements work
│   └── researcher.md                        ← Specialist: technical research and discovery work
│
├── hooks/
│   └── hooks.json                           ← Always-on hooks (Tier 1 enforcement; delivered by plugin)
│
├── scripts/
│   └── momentum-tools.py                    ← CLI tool: sprint, triage, practice-ledger, quickfix, version subcommands (intake-queue deprecated → practice-ledger per DEC-033)
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
│       ├── epics.json                       ← Unified epic layer (DEC-034, replaces features.json — Decision 44 HISTORICAL)
│       ├── archive/
│       │   └── features-pre-2026-05.json    ← Frozen archive of features.json pre-DEC-034 migration
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
├── .claude/
│   ├── rules/                               ← Written by Impetus (from plugin references/rules/)
│   └── momentum/                            ← Per-project Momentum state
│       ├── journal.jsonl                     ← Session journal (JSONL append-only, Impetus reads/writes)
│       ├── journal-view.md                   ← Human-readable view (auto-generated)
│       ├── installed.json                   ← Install/upgrade state (version + per-component hashes)
│       ├── session-modified-files.txt       ← Ephemeral: PostToolUse writes, Stop reads + deletes (Decision 1e)
│       └── gate-findings.txt                ← Inter-session: Stop writes, Impetus reads at next session (Decision 1e)
└── .momentum/                                  ← Operational runtime state (added 2026-04-28; see `.momentum/` State Layout section)
    ├── sprints/
    │   ├── index.json                          ← Sprint registry (Decision 36)
    │   └── {sprint-slug}/                      ← Per-sprint runtime artifacts (see Sprint Tracking Schema)
    │       ├── specs/                          ← Contract files (Decision 30 + DEC-029, written by sprint-planning)
    │       │   ├── *.feature                   ← Gherkin contracts
    │       │   ├── *.eval.yaml                 ← LLM eval contracts
    │       │   ├── *.trigger.md                ← Trigger contracts
    │       │   ├── *.smoke.sh                  ← Smoke test contracts
    │       │   └── *.review.md                 ← Manual review contracts
    │       ├── coverage-plan.md                ← Per-sprint verification coverage plan (DEC-029; post-activation immutable)
    │       ├── retro-transcript-audit.md       ← Retro findings document (Decision 27, written by retro)
    │       ├── sprint-summary.md               ← Sprint summary (Decision 47, written by retro at Phase 6 close)
    │       └── audit-extracts/                 ← DuckDB preprocessing output (Decision 27)
    ├── stories/
    │   ├── index.json                          ← Story status index
    │   └── {slug}.md                           ← Story files (written by momentum:create-story)
    ├── signals/                                ← RETIRED (DEC-033 D6) — preserved on disk; no new writes; former use cases flow through practice-ledger
    ├── practice-ledger.jsonl                   ← Append-only event log (DEC-033 / Decision 52 superseded — true append-only, CLI-only writes via momentum-tools practice-ledger)
    ├── practice-ledger-pre-2026-05.jsonl       ← Hard-cut archive of prior intake-queue.jsonl (DEC-033 D8; 88 legacy entries; read-only)
    └── beads-id-map.json                       ← Git-tracked slug → bead hash ID map (DEC-028 — maintained by sprint-manager dual-write; maps story_slug to Beads bead ID)

[project-root]/
└── .beads/                                     ← Gitignored Dolt DB (DEC-028 — Beads tracker local store; never committed)
```

> _Planning artifacts (PRD, architecture, epics.json, decisions, assessments) intentionally remain under `_bmad-output/planning-artifacts/` — they are spec/source, not operational state. Note: `features.json` superseded by `epics.json` per DEC-034 (2026-05-25). See `.momentum/` State Layout section for the carve-out rationale._

---

### Architectural Boundaries

**Read/Write Authority:**

<!-- REVISED Phase 3: Updated Impetus, momentum:dev, momentum:create-story rows; replaced momentum:sprint-manager subagent with momentum-tools CLI; added sprint-planning workflow, sprint-dev workflow rows. sprint-status.yaml references replaced with stories/index.json and sprints/index.json. momentum-tools log row removed 2026-04-08 (Decision 24 historical). -->
<!-- REVISED 2026-04-28: All sprints/, stories/, intake-queue.jsonl path references migrated to .momentum/ per State Layout section (DEC-011 Gate G1). Impetus reads .momentum/signals/ at session start. -->

| Component | Reads | Writes |
|---|---|---|
| Impetus | `.momentum/stories/index.json`, `.momentum/sprints/index.json`, journal.jsonl, specs, findings-ledger.jsonl, gate-findings.txt; `.momentum/practice-ledger*.jsonl` (via `momentum-tools practice-ledger summary` at session start — DEC-033 D9; replaces prior `signals/*.json` read per DEC-033 D6 retirement) | journal.jsonl, journal-view.md |
| momentum-tools sprint | `.momentum/stories/index.json`, `.momentum/sprints/index.json` | `.momentum/stories/index.json` (status fields), `.momentum/sprints/index.json` (sole writer; per-sprint `.momentum/sprints/{slug}.json` retired per DEC-012) |
| momentum-tools quickfix | `.momentum/sprints/index.json` | `.momentum/sprints/index.json` (register: adds quick-fix entry; complete: marks done) |
| momentum-tools triage | `.momentum/stories/index.json` (read-only scoring: `triage prefilter` subcommand — TF-IDF + Jaccard + epic boost, status-filtered, top-K=10 shortlist) | _(none — pure scorer, no writes)_ |
| momentum:dev | Story files, code | Code in worktree only; structured JSON completion output |
| momentum:create-story | `.momentum/stories/index.json`, epics.md | Story files in `.momentum/stories/` |
| momentum:refine | prd.md, architecture.md, `.momentum/stories/index.json`, story files, assessments/*.md, decisions/*.md | prd.md (via PRD update subagent — sole writer); architecture.md (via architecture update subagent — sole writer); `.momentum/stories/index.json` mutations (via momentum-tools CLI); delegates: momentum:create-story, momentum:epic-grooming |
| momentum:feature-status **(deprecated — use momentum:canvas)** | ~~`_bmad-output/planning-artifacts/features.json`~~ `_bmad-output/planning-artifacts/epics.json` **(DEC-034)**, `.momentum/stories/index.json` | `.claude/momentum/feature-status.html` (HTML dashboard); `.claude/momentum/feature-status.md` (cache — sole writer) |
| canvas server (Bun process, port 3456) | `_bmad-output/planning-artifacts/epics.json` **(DEC-034 — replaces features.json)**, `.momentum/stories/index.json`, `.momentum/sprints/index.json`, `.momentum/stories/{slug}.md` | _(none — read-only server)_ |
| `_bmad-output/planning-artifacts/epics.json` **(DEC-034)** | _(read by: canvas server, momentum:epic-grooming, momentum:epic-breakdown, momentum:create-story)_ | **Sole writer (skills): `momentum:epic-grooming`** (DEC-034 D6, B4). No other skill or tool writes epics.json. _Transitional exception: the one-time B1 migration script (`skills/momentum/scripts/migrate_features_to_epics.py`) produced the initial epics.json from the legacy features.json. It is an idempotent, run-once bootstrap — not an ongoing writer — and does not participate in the steady-state write path. The sole-writer principle for skills is unaffected._ |
| momentum:sprint-planning | `.momentum/stories/index.json`, `.momentum/sprints/index.json`, story files, `momentum/verification-harness.json` (for per-story contract-type selection) | `.momentum/sprints/{sprint-slug}/specs/` (multi-extension contract files: `.feature`, `.eval.yaml`, `.trigger.md`, `.smoke.sh`, `.review.md` per story `verification_method`); `.momentum/sprints/{sprint-slug}/coverage-plan.md` (written at activation, then immutable); sprint record team composition + `approvals[]` entries (via momentum-tools sprint) |
| momentum:sprint-dev | `.momentum/sprints/index.json` (active sprint, team, deps, approvals), `.momentum/stories/index.json`, `.momentum/sprints/{sprint-slug}/specs/*.feature` | Task state (via TaskCreate/TaskUpdate); status transitions (via momentum-tools sprint); sprint completion (via momentum-tools sprint complete). Phase 1 verifies `active.approvals` SHAs against current story-file SHAs before any in-progress transition (`momentum-tools sprint verify-approvals`). |
| momentum:retro | `.momentum/sprints/index.json`, `.momentum/stories/index.json`, session JSONL transcripts, decisions/*.md | `.momentum/sprints/{sprint-slug}/retro-transcript-audit.md`; `.momentum/sprints/{sprint-slug}/sprint-summary.md` (Decision 47 — sole writer at Phase 6 close); `.momentum/practice-ledger.jsonl` (handoff `created` events via `momentum-tools practice-ledger append`; replaces prior `signals/*.json` writes — DEC-033 D6). Note: feature-status cache read and `/momentum:feature-status` spawn removed — **ARCH-6: feature-status deprecated, canvas supersedes** |
| momentum:triage | `.momentum/stories/index.json`, `.momentum/practice-ledger*.jsonl` (reads `open` + `summary` for session-start re-surfacing — DEC-033 D9) | `.momentum/practice-ledger.jsonl` (SHAPING/DEFER/REJECT entries as `created` events via `momentum-tools practice-ledger append`; triage-uncleared attention signal also flows here as a `created` event with `source: triage`; replaces prior `momentum-tools intake-queue` + `signals/` writes — DEC-033 D6) |
| code-reviewer | Source code, specs, acceptance tests | findings (via structured output → flywheel) |
| architecture-guard | Source code, rules, architecture doc | pattern drift report (via structured output) |
| VFL / AVFL | Any artifact being validated, source material | consolidated findings / validation report; `.momentum/practice-ledger.jsonl` (avfl-finding-pending-upstream-fix entries as `created` events with `source: avfl` via `momentum-tools practice-ledger append`; replaces prior `signals/*.json` writes — DEC-033 D6) |
| Flywheel workflow (Epic 6) | findings-ledger.jsonl, rules, specs | findings-ledger.jsonl, rules/, specs |
| momentum:distill | **(removed — ARCH-1/ARCH-7)** Session observation / retro findings, relevant spec/skill/rules files | ~~rules/, references/, skill prompts (Tier 1 direct commit); stories/index.json stubs (Tier 2); findings-ledger.jsonl (`origin: distill`); plugin version + push (Momentum-level fixes in Momentum project only)~~ — all write authority removed; flywheel is the sole findings-ledger writer |
| Upstream-fix skill (Epic 4, standalone) | session journal, specs, rules | session journal only (not findings-ledger.jsonl) |
| Hooks (PreToolUse) | Filesystem (reads), `references/protected-paths.json` | Terminal output only (blocks or allows) |
| Hooks (PostToolUse) | Filesystem (reads) | `session-modified-files.txt` (append, deduped); terminal output (lint results) |
| Hooks (Stop) | `session-modified-files.txt`, git status | `gate-findings.txt` (overwrite); deletes `session-modified-files.txt` after gate runs |
| ATDD workflow | Gherkin spec | `tests/acceptance/` only |
| Coding agents (dev-story) | Specs, rules, existing code | Source code, unit tests |
| `momentum/agents.json` | Read by all skills at spawn time (routing resolution) | Sole writers: agent-builder (writes `project` array entries per role×domain); plugin ships `defaults` block — agent-builder never overwrites defaults |
| `momentum/verification-harness.json` | Read by e2e-validator at startup (harness profile) and sprint-planning (contract-type selection per story) | Sole writers: agent-builder (writes `project` block overrides); agent-guidelines (writes `project` block overrides); plugin ships `defaults` block (all surfaces default to `"skip"`) — neither skill overwrites the `defaults` block |
| `momentum-tools agent-resolve` | `momentum/agents.json` (reads `defaults` + `project` blocks, glob-matches paths against `project` entries, falls back to `defaults.dev`) | _(none — pure resolver, no writes)_ |
| `.momentum/sprints/{sprint-slug}/build-ledger.jsonl` | Read by the Conductor at partial-run resume (step 2.0 accumulator rehydration) and at end-gate assembly (Phase 5) — Decision 59 | **Sole writer: the Conductor** (`/momentum:conduct` top-level session). Append-only rows at event time; corrections are append-only override rows, never edits |
| `agents/ux.md`, `agents/analyst.md`, `agents/researcher.md` | Spawned by skills during specialized phases; read story files, research inputs, planning artifacts | Structured findings output only; no direct file writes |

**Protection boundaries (PreToolUse blocks writes to — sourced from `references/protected-paths.json`):**
- `tests/acceptance/` — acceptance test immutability
- `_bmad-output/planning-artifacts/` — spec authority. Exception: momentum:refine wave-2 update subagents may write to prd.md and architecture.md as sole authorized writers, following developer approval gate.
- `.claude/rules/` — enforcement rule integrity
- `~/.claude/momentum/findings-ledger.jsonl` — Ledger integrity (authority-enforced; global path is outside project PreToolUse scope)
- `.momentum/sprints/{sprint-slug}/specs/` — Contract file integrity (Decision 30 + DEC-029: dev agents must never write to this path; only sprint-planning writes, only verifiers read; covers all five contract types: `.feature`, `.eval.yaml`, `.trigger.md`, `.smoke.sh`, `.review.md`)
- `.momentum/sprints/{sprint-slug}/coverage-plan.md` — Post-activation immutable (DEC-029, `sprint-planning-frozen-per-story-contract` story: coverage-plan.md is written by sprint-planning at activation time and must not be modified after sprint activation)
- `.momentum/stories/index.json`, `.momentum/sprints/index.json` — sole writer is `momentum-tools.py sprint`. Direct edits by any other agent are blocked. (Per-sprint `.momentum/sprints/{slug}.json` retired per DEC-012 — no longer a protected path because it is no longer written.)
- `.momentum/practice-ledger.jsonl` — append-only via `momentum-tools practice-ledger`. Direct edits blocked (replaces prior `.momentum/intake-queue.jsonl` protection per DEC-033).
- `.momentum/signals/` — RETIRED (DEC-033 D6). Directory preserved on disk for git history; no new writes. Former signal use cases flow through practice-ledger.

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
| Distill | `skills/distill/` | ~~Plugin skill: `/momentum:distill`~~ — **removed (ARCH-1)** |
| Research | `skills/research/` | Plugin skill: `/momentum:research` |
| Status | `skills/status/` | Superseded — see Feature Status below (Decision 45) |
| Feature Status | `skills/feature-status/` | ~~Plugin skill: `/momentum:feature-status`; HTML output: `.claude/momentum/feature-status.html`; cache: `.claude/momentum/feature-status.md`~~ — **deprecated (ARCH-6); canvas supersedes feature-status per DEC-019** |
| Canvas | `skills/canvas/` | Plugin skill: `/momentum:canvas`; Bun+Hono+HTMX server at port 3456; SKILL.md + workflow.md + server.tsx (DEC-019, supersedes feature-status — ARCH-6) |
| Agent Guidelines | `skills/agent-guidelines/` | Plugin skill: `/momentum:agent-guidelines` (FR61a — 5-phase guided workflow generating path-scoped rules and reference docs) |
| Epic artifact (epics.json) **(DEC-034 — replaces features.json)** | (planning artifact) | `_bmad-output/planning-artifacts/epics.json` (written by migration script B1; future sole writer: momentum:epic-grooming after B4) |
| Sprint summary | (runtime, per-sprint) | `.momentum/sprints/{sprint-slug}/sprint-summary.md` (written by retro orchestrator at Phase 6 close) |
| Practice ledger | (runtime, per-project) | `.momentum/practice-ledger.jsonl` (DEC-033 / Decision 52 superseded — true append-only event log; written by momentum:triage, momentum:retro, momentum:avfl, and automation routine via `momentum-tools practice-ledger` CLI); `.momentum/practice-ledger-pre-2026-05.jsonl` (frozen archive; 88 legacy entries; read-only) |
| Sprint registry | (runtime, per-project) | `.momentum/sprints/index.json` (sole writer: `momentum-tools sprint`) |
| Story registry | (runtime, per-project) | `.momentum/stories/index.json` (sole writer: `momentum-tools sprint`) |
| Signal ledger | (runtime, per-project) | **RETIRED (DEC-033 D6)** — `.momentum/signals/` absorbed into practice-ledger; signal use cases flow as practice-ledger entries with appropriate `source` + `payload` |
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

**CMUX Markdown Surfaces ↔ Quick-Fix and Sprint-Planning:** cmux markdown surfaces serve as a primary developer review pattern in quick-fix Phases 1-2 and in sprint-planning's per-story approval flow (added 2026-04-28). The quick-fix skill renders implementation plans and file diffs to cmux surfaces for developer review and approval before changes are applied. The sprint-planning skill renders per-story approval views to a cmux markdown surface during Step 3 (Flesh out stories) — each fleshed-out story file is opened in its own surface so the developer can scan content before recording an approval entry (Per-story approval contract). This is a direct integration — not optional detect-and-adapt — within both workflows.

**momentum:refine ↔ momentum:epic-grooming:** momentum:refine delegates taxonomy analysis and story reassignment to momentum:epic-grooming as a substep during backlog refinement. Graceful degradation applies: if momentum:epic-grooming is absent, refine skips the taxonomy substep and continues with the remaining refinement work.

**momentum:feature-status ↔ Impetus startup-preflight (deprecated — use momentum:canvas):** Impetus reads `.claude/momentum/feature-status.md` at session start (inside startup-preflight, one Bash call, inline hash computation — Decision 46). Cache state drives greeting behavior: `fresh` → display cached feature summary inline; `stale` → offer refresh; `no-features` → silent skip; `no-cache` → suggest running `/momentum:feature-status`. The feature-status skill itself is invoked on-demand (user request or retro Phase 6 trigger — Decision 47) — Impetus never spawns it autonomously during greeting. **Deprecated by DEC-019 — momentum:canvas supersedes feature-status as the unified planning dashboard.**

**momentum:feature-status ↔ momentum:retro (deprecated — use momentum:canvas):** Retro orchestrator spawns `/momentum:feature-status` at Phase 6 close (after verification, before sprint summary write) to refresh the feature cache for the next session. This is a sequential dependency: feature-status runs first, its cache output is read by the retro orchestrator to populate the "Features Advanced" section of the sprint summary (Decision 47). **Deprecated by DEC-019.**

**momentum:epic-grooming ↔ momentum:canvas:** `momentum:epic-grooming` is the sole writer of `epics.json` (DEC-034 D6, B4). After a grooming session, the canvas server (Bun, port 3456) reads the updated `epics.json` live — no cache invalidation step needed. _Historical note: The prior `momentum:feature-grooming ↔ momentum:feature-status` integration (features.json + cache invalidation via feature-status-hash) is retired. Both `momentum:feature-grooming` and `momentum:feature-status` are superseded by DEC-034 and DEC-019 respectively._

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
> _Revised 2026-04-28: Folder root migrated to `.momentum/` per `.momentum/` State Layout section (DEC-011 Gate G1). All paths below resolve under `.momentum/`._

**`.momentum/stories/` folder** — one file per story (`.momentum/stories/{slug}.md`). Created early at backlog stage as a stub (slug, title, epic, status). Fleshed out with full ACs, dev notes, and tasks during sprint planning via `momentum:create-story`. Story file content (ACs, dev notes) is written by `momentum:create-story`. Story file YAML frontmatter fields include: `title`, `story_key`, `status`, `epic_slug`, `feature_slug`, `story_type`, `change_type` (array), `depends_on` (array), `touches` (array), and `verification_method` (string — added sprint-2026-05-17, `create-story-method-selection-step` story; written by `momentum:create-story` at story creation time; derived from the change-type routing table in `verification-standard.md`). **Driver-binding enum (reconciled sprint-2026-06-02, conduct-core; supersedes the legacy `eval|trigger|smoke|review|gherkin|skip` vocabulary):** `skill-invoke | behavioral-trigger | bash | smoke | document-review | curl`. The `verification_method` value is the **driver-binding key** — it equals the `harness_profile` selected for the story and the dispatch key the verifier resolves against `momentum/verification-harness.json` (method == harness_profile == driver-binding key). Each method maps to a contract file extension via the `contract_extensions` table: `skill-invoke`/`behavioral-trigger` → `.trigger.md`, `bash`/`smoke` → `.smoke.sh`, `document-review` → `.review.md`, `curl` → `.smoke.sh`, with `.eval.yaml` (LLM eval) and `.feature` (Gherkin) retained as contract extensions.

**`.momentum/stories/index.json`** — lightweight lookup index. Each entry: slug, status, title, epic slug, story_file (boolean — whether fleshed out), depends_on, touches, priority (optional — `critical | high | medium | low`, default: `low`). Epic membership lives here, not in epics.md.

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

**`.momentum/sprints/` folder** — one canonical state file (`.momentum/sprints/index.json`) holds all sprint state in sectioned blocks (`active`, `planning`, `completed[]`, `quickfixes[]`); see the schema description below. Per DEC-012, no per-sprint JSON file is written — the per-slug `.momentum/sprints/{slug}.json` pattern is retired in favor of the holistic index. Per-sprint **subdirectories** (`.momentum/sprints/{slug}/`) remain — one per sprint — and hold sprint-scoped artifacts: `specs/` (Gherkin feature files), `sprint-summary.md` (Decision 47, written by the retro orchestrator at Phase 6 close), `retro-transcript-audit.md` (Decision 27), `audit-extracts/` (DuckDB preprocessing output), and `build-ledger.jsonl` (Decision 59 — append-only conduct build ledger, sole writer: the Conductor). The subdirectory structure is shown below.

**Per-sprint folder structure (under `.momentum/sprints/{sprint-slug}/`):**

```
.momentum/sprints/{sprint-slug}/
├── specs/                                ← Contract files (sprint-planning writes; verifier-only reads)
│   ├── {story-slug}.feature             ← Gherkin contract (Decision 30)
│   ├── {story-slug}.eval.yaml           ← LLM eval contract
│   ├── {story-slug}.trigger.md          ← Trigger-based contract
│   ├── {story-slug}.smoke.sh            ← Smoke test contract
│   └── {story-slug}.review.md          ← Manual review contract
├── coverage-plan.md                     ← Per-sprint verification coverage plan (DEC-029, written by sprint-planning; post-activation immutable)
├── build-ledger.jsonl                   ← Append-only conduct build ledger (Decision 59, sprint-2026-06-10 — sole writer: Conductor)
├── retro-transcript-audit.md             ← Retro findings document (Decision 27, written by retro documenter)
├── sprint-summary.md                     ← Sprint summary (Decision 47 — sole writer: retro orchestrator at Phase 6 close)
└── audit-extracts/                       ← DuckDB preprocessing output (Decision 27)
    ├── user-messages.jsonl
    ├── agent-summaries.jsonl
    ├── errors.jsonl
    └── team-messages.jsonl
```

The per-sprint folder is the primary durable record of a sprint's execution. `sprint-summary.md` is the canonical compression artifact read by the next sprint-planning Step 1 (Decision 29).

**`build-ledger.jsonl` (added sprint-2026-06-10, conductor seam-fix):** the append-only JSONL build ledger at `.momentum/sprints/{sprint-slug}/build-ledger.jsonl` is the durable record of a conduct build's execution. The **Conductor is the sole writer**; rows are appended at event time — story launches, stage transitions, finding dispositions, escalations, quarantines, coverage deferrals/discharges, contract-integrity stops, and end-gate fixer events. Corrections are **append-only override rows, never edits** to existing rows. The row vocabulary aligns with `finding-schema.md` v1.1 and `build-results-ledger-schema.md` v1.0 (the companion schemas, joined on story slug). See Decision 59 for the ledger-sourced end-gate and partial-run resume semantics.

**`.momentum/sprints/index.json`** — which sprint is active, which is planning, list of completed sprints. Active and planning entries are objects (not slug strings) that carry sprint lifecycle state (Decision 36). The `status` field tracks position in the sprint lifecycle state machine. Active and planning entries also carry an `approvals: []` array (Per-story approval contract — added 2026-04-28). Completed entries track retro execution for lifecycle gate enforcement.

**Per-story approval contract (added 2026-04-28):**

Sprint records carry an `approvals: []` array on `planning`, `active`, and `completed` entries. Each entry records that the developer has approved a specific story file at a specific content state:

```json
"approvals": [
  {
    "story_slug": "impetus-momentum-state-migration",
    "approved_at": "2026-04-27T17:42:11Z",
    "decision": "approve",
    "story_file_sha": "9b2c4f0e6a8d1e5b7c3a..."
  }
]
```

| Field | Type | Notes |
|---|---|---|
| `story_slug` | string | Slug from `.momentum/stories/index.json` |
| `approved_at` | string | ISO-8601 UTC timestamp of the developer decision |
| `decision` | string | `approve` (currently the only recognized value; reserved for future `reject` / `defer` extensions) |
| `story_file_sha` | string | SHA-256 of the story file content at approval time. Hex-encoded. Used as a tamper-evident pin. |

**Activation gate:** sprint-planning Step 8 (sprint activation) requires that every selected story has an `approvals[]` entry where `story_file_sha` matches the SHA-256 of the story file's current content on disk. If a story file changes after approval, its SHA no longer matches and activation is blocked until the developer re-approves the modified file.

**Pre-execution gate:** sprint-dev Phase 1 re-verifies the approval SHAs against the current story files on disk before any in-progress transition. This catches edits made between activation and execution start. Implementation: `momentum-tools sprint verify-approvals --sprint <slug>` returns non-zero on any SHA mismatch; sprint-dev halts and surfaces the mismatch to the developer.

**Origin:** `sprint-planning-adds-per-story-approval-gate` story (sprint-2026-04-27).

> _[Revised 2026-04-04: Active and planning entries enhanced with `status` field for sprint lifecycle state machine (Decision 36). Completed entries enhanced with `retro_run_at` for retro gate tracking. Existing fields (locked, stories, waves, team, started, completed) unchanged.]_

**`.momentum/sprints/{sprint-slug}/specs/`** — Gherkin feature files written during sprint planning (Decision 30). One file per story: `{story-slug}.feature`. These specs encode detailed behavioral expectations that only verifier agents access. Dev agents NEVER read this directory — verification is black-box by design. Story markdown files retain plain English ACs only; Gherkin is never written back to story files.

```json
// .momentum/sprints/index.json
{
  "active": {
    "slug": "quality-hooks-sprint",
    "status": "active",           // "ready" | "active" | "done" — see Decision 36
    "locked": true,
    "stories": ["posttooluse-lint-hook", "pretooluse-file-protection"],
    "started": "2026-03-30",
    "completed": null,
    "approvals": []               // see Per-story approval contract
    // ... waves, team (contains story_assignments) as before
  },
  "planning": {
    "slug": "impetus-ux-sprint",
    "status": "planning",         // "planning" | "ready" — see Decision 36
    "locked": false,
    "stories": ["greeting-redesign", "session-stats"],
    "approvals": []               // see Per-story approval contract
    // ... waves, team (contains story_assignments) as before
  },
  "completed": [
    {
      "slug": "bootstrap-sprint",
      "completed": "2026-03-28",
      "retro_run_at": "2026-03-29",  // null if retro not yet run
      "approvals": []                // historical approval record preserved
    }
  ]
}

// .momentum/sprints/quality-hooks-sprint.json
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
      "posttooluse-lint-hook": {
        "role": "dev",
        "verification_method": "bash",          // driver-binding key (== harness_profile)
        "can_merge_independently": true,
        "contract": {
          "path": ".momentum/sprints/quality-hooks-sprint/specs/posttooluse-lint-hook.smoke.sh",
          "harness_profile": "bash",            // equals verification_method
          "coverage_disposition": "direct",     // direct | covered-by | waived
          "covered_by_scenario": null,          // set when coverage_disposition == covered-by
          "frozen_sha256": "<sha256-of-contract-file>"  // computed at activation; freezes the contract
        }
      },
      "pretooluse-file-protection": {"role": "dev", "verification_method": "bash", "can_merge_independently": true, "contract": { /* ... as above ... */ }},
      "stop-gate-quality-checks": {"role": "dev", "verification_method": "bash", "can_merge_independently": false, "contract": { /* ... as above ... */ }}
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

**`story_assignments` frozen-contract block (sprint-2026-06-02, conduct-core):** Each story assignment carries, alongside `role`, the fields the conduct/sprint pipeline binds against: `verification_method` (the driver-binding key), `can_merge_independently` (whether the story may merge on its own or must land with its cohort), and a `contract` object — `{ path, harness_profile, coverage_disposition, covered_by_scenario, frozen_sha256 }`. `harness_profile` equals `verification_method` (the driver-binding key). `frozen_sha256` is computed at sprint **activation** over the contract file's content and freezes the contract: any post-activation edit changes the SHA and is caught at the verify-approvals / build-time integrity gate. `coverage_disposition` records whether the story is verified `direct`, `covered-by` another story's scenario (then `covered_by_scenario` names it), or `waived`. **Build-time semantics (sprint-2026-06-10, conductor seam-fix — Decision 59):** covered-by-composition defers **only** the dedicated QA verification run to the named integration scenario; adversarial code review still runs at build time on every story's per-story diff and is never deferred, demoted, or skipped by the disposition. Stage-2 findings are never unconditionally bound empty by coverage routing. **Emitters:** `momentum:sprint-planning` authors the contract block at planning time; `momentum:sprint-manager` (sole writer of `sprints/index.json`) persists it and computes `frozen_sha256` at activation.

**`epics.md`** — names, slugs, and descriptions only. No story lists. Pure documentation. Epic membership is tracked in `.momentum/stories/index.json`.

**`sprint-status.yaml` is deprecated** — replaced by the folder-based model above. The `sprint-status-schema-decomposition` migration story handles the transition from sprint-status.yaml to the new structure.

**Write authority:** `momentum-tools.py sprint` is the sole writer of the `.momentum/sprints/` folder and the `status` fields in `.momentum/stories/index.json`. Story file content (ACs, dev notes, tasks) is written by `momentum:create-story`. Sprint-scoped Gherkin specs (`.momentum/sprints/{sprint-slug}/specs/`) are written by the sprint-planning skill (`/momentum:sprint-planning`). No other agent or script writes to these files directly.

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

**Conduct path — branch-base rule (Decision 59, sprint-2026-06-10):** the conduct execution engine reuses the `.worktrees/story-{slug}` / `story/{slug}` naming convention, but the **Conductor** (not the dev agent) performs every worktree operation, and the branch base is fixed — not captured at invocation. At story launch the Conductor creates `story/{slug}` from the **current tip of `sprint/{sprint-slug}`** (never `main`, never an inferred default), then adds `.worktrees/story-{slug}`, before the stage-1 dev spawn. Stale branches or worktrees left by a prior interrupted run are handled idempotently: remove and recreate. Rationale: forking from the sprint tip keeps the merge-base review diff exactly story-scoped.

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

1. **Backlog presentation (Synthesis-First)** — Read the master plan documents (`prd.md`, product brief) to understand strategic priorities. Read the most recent sprint summary (`.momentum/sprints/{last-sprint-slug}/sprint-summary.md`) for "what just happened" context — non-blocking if absent. Read `.momentum/stories/index.json`, group by epic, exclude terminal states. Within each epic group, sort by priority (critical > high > medium > low), then by dependency depth, then alphabetical. Run a staleness check: for each story with status `ready-for-dev` or `in-progress`, check `git log` for commits touching the story's `touches` paths — if substantial implementation commits exist, flag the story as potentially already implemented and exclude it from recommendations (surface in a separate "Potentially stale" section with evidence). Lead with a synthesis section: 3-5 prioritized recommendations with brief rationale for each, informed by the master plan's current priorities, dependency readiness, and backlog state. Present the full backlog below the recommendations as secondary reference material. If master plan documents are missing, fall back to the current behavior (sorted backlog) with a warning.
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

sprint-dev is a dedicated skill (`/momentum:sprint-dev`) with 6 phases. Invoked by Impetus when the developer selects "Continue sprint" from the session menu, or directly by the user. **Coexistence note (DEC-037):** `/momentum:conduct` (the conduct execution engine — Decision 59) is a standalone builder that coexists with this sprint-dev flow. The two run in parallel during the transition; sprint-dev's wave loop is retired only at the later adoption step. The phases below describe the sprint-dev path; conduct's per-story build→review→fix pipeline is described in Decision 59.

**Phase 1: Initialization**
- Read active sprint from `.momentum/sprints/index.json`; validate locked state
- **Verify per-story approvals against current story files (added 2026-04-28).** Run `momentum-tools sprint verify-approvals --sprint <slug>` to compare every entry in `active.approvals` against the SHA-256 of the corresponding story file's current content on disk. If any approval SHA does not match the current file, halt before any in-progress transition and surface the mismatch to the developer (story slug, expected SHA, actual SHA). This catches story-file edits made between activation and execution start. Re-execution requires the developer to re-approve via sprint-planning.
- Build dependency graph from story `depends_on` fields
- Initialize spawn registry as an empty map — tracks every agent spawned during this session, keyed by `{story_slug}::{role}` (e.g., `refine-skill::dev`, `sprint::qa-reviewer`). The registry survives the Phase 2 → Phase 3 → Phase 2 loop; it is never reset between phases and is not persisted to disk.
- Create a task per story via TaskCreate for progress tracking
- Log sprint start

<critical>Use task tracking (TaskCreate/TaskUpdate) for sprint phases — this prevents context drift in long runs. Every phase entry updates the corresponding task to in_progress; every phase exit updates to completed. Ad-hoc narrative summaries are not a substitute for tool-queryable task state.</critical>

**Phase 2: Team Spawn**
- Identify unblocked stories
- Transition each to `in-progress` via `momentum-tools sprint status-transition`
- **Specialist agent resolution (sprint-2026-05-16):** For each unblocked story, resolve the specialist agent via `momentum-tools agent-resolve --role dev --touches {story.touches}`. Resolution is routing-table-driven (Decision 55 / DEC-023): glob-match the story's `touches` paths against `momentum/agents.json` `project` entries, fall back to `defaults.dev` if no match. Multi-domain stories (multiple result groups) spawn one agent per result group. Never hardcode agent paths in skill prompts — always use `momentum-tools agent-resolve`.
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
- **Reviewer agent resolution (sprint-2026-05-16):** qa-reviewer and e2e-validator agent paths are resolved via `momentum-tools agent-resolve --role qa-reviewer` and `momentum-tools agent-resolve --role e2e-validator` respectively, using the `defaults` block of `momentum/agents.json` (Decision 55). Project-specific overrides in the `project` block take precedence when present. Never hardcode agent paths — always use `momentum-tools agent-resolve`.
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

### Retro → Planning Handoff via Practice Ledger

> _[Updated 2026-04-14 (DEC-007, story: retro-triage-handoff): The prior `triage-inbox.md` contract was retired. Retro writes handoff events to the unified event log. No manual re-injection of retro findings into planning is required.]_
>
> _[Updated 2026-05-28 (DEC-033, story: a1-practice-ledger-schema-cli-redesign-true-append-only): Renamed from "Retro → Planning Handoff via Unified Intake Queue". The artifact is now `.momentum/practice-ledger.jsonl` with the DEC-033 schema. CLI paths updated to `momentum-tools practice-ledger`. The prior `intake-queue.jsonl` contract (DEC-007) is superseded in full.]_

After each sprint retro (Phase 5.5), un-actioned findings are appended to `practice-ledger.jsonl` as `created` events. Sprint-planning Step 1 reads open entries with `source: "retro"` and surfaces them alongside the backlog — closing the retro → planning loop without developer re-injection.

**Artifact:** `.momentum/practice-ledger.jsonl` (per DEC-033; supersedes prior `intake-queue.jsonl` / DEC-007)

**Write path:** `momentum-tools practice-ledger append --entity-id <ENTITY_ID> --event-type created --source retro --actor <ACTOR> --payload '<JSON>'`
**Read path:** `momentum-tools practice-ledger open` or `momentum-tools practice-ledger by-source retro`
**Consume path:** `momentum-tools practice-ledger consume --entity-id <ENTITY_ID> --actor <ACTOR> --outcome-ref STORY_SLUG`

**Event schema (DEC-033 D2):**
```jsonl
{
  "event_id": "pl-20260415T173400000000-a1b2c3d4",
  "entity_id": "retro-finding-sprint-2026-04-08-1",
  "ts": "2026-04-15T17:34:00Z",
  "event_type": "created",
  "source": "retro",
  "actor": "momentum:retro",
  "payload": {
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
}
```

**Field semantics:**
- `event_id` — immutable unique row identifier
- `entity_id` — logical finding; repeats across event rows for the same finding's lifecycle
- `event_type: "created"` — initial event written by `momentum:retro` Phase 5.5
- `source: "retro"` — producer identity
- `payload.sprint_slug` — provenance: which retro produced this finding
- `payload.story_type` — suggested story type for downstream stub creation (DEC-005 D5)
- `payload.feature_state_transition` — present when the finding involves a feature-state hygiene event (DEC-005 D8)
- `payload.failure_diagnosis` — present when the finding names a specific failure (DEC-005 D7)

**Consumption:** When a handoff item is promoted to a story stub during sprint-planning Step 2, `momentum-tools practice-ledger consume --entity-id <ENTITY_ID>` appends a `consumed` event. The original row is never modified — state is derived.

**DEC-005 alignment (D7, D8):** Retro-specific enrichment fields are carried in the `payload` object, unchanged from the DEC-007 contract.

**Retired:** The prior `triage-inbox.md` contract is superseded. The `intake-queue.jsonl` DEC-007 schema contract is superseded by DEC-033.

---

### `practice-ledger.jsonl` Schema Contract (DEC-033)

<!-- Added 2026-05-28: Supersedes the prior `intake-queue.jsonl` Schema Contract (DEC-007). True append-only event log per DEC-033 D1–D3. -->

Single source of truth for non-story practice outcomes — SHAPING / DEFER / REJECT outcomes from `momentum:triage`, handoff events from `momentum:retro`, and attention signals from `momentum:avfl`. Per **DEC-033 (2026-05-25)**.

**Path:** `.momentum/practice-ledger.jsonl` (active log); `.momentum/practice-ledger-pre-2026-05.jsonl` (archive — read-only)

**Format:** True append-only JSONL event log. One JSON object per line. Never truncated, never rewritten. O_APPEND semantics enforced at the writer level.

**Schema fields (every row):**

| Field | Type | Values / Notes |
|---|---|---|
| `event_id` | string | Immutable unique row identifier (format: `pl-{timestamp}-{hex8}`; never reused) |
| `entity_id` | string | Identifies the logical entity this event is about; repeats across rows for the same entity |
| `ts` | string | ISO-8601 UTC timestamp ending in `Z` |
| `event_type` | string | One of seven values — see enum below |
| `source` | string | Originating skill/workflow (e.g., `triage`, `retro`, `avfl`, `momentum-tools-close-stale`) |
| `actor` | string | Human or agent identity that produced this event |
| `payload` | object | Event-type-specific structured data (may be `{}`) |
| `custom_event_type` | string | Present only when `event_type == "custom"` — names the actual event type |

**Event type enum:**

| Value | Terminal? | Semantics |
|---|---|---|
| `created` | No | Entity born; sets the TTL clock |
| `updated` | No | Non-status field changed |
| `consumed` | **Yes** | Actively resolved with outcome reference |
| `rejected` | **Yes** | Explicitly won't-do |
| `closed_stale` | **Yes** | Auto-emitted when TTL elapses without resolution |
| `reopened` | No | Previously closed entity brought back (reuses same `entity_id`) |
| `custom` | No | Escape hatch; `custom_event_type` carries the actual name |

**Derived current state:** Fold all events for an `entity_id` by `ts` ascending; the last event's `event_type` is the current state. Terminal = consumed, rejected, or closed_stale. Non-terminal = all others. State is NEVER stored — derivation is the source of truth.

**Writers (CLI-only; never direct file edits):**

- `momentum:triage` — appends `created` events for SHAPING/DEFER/REJECT outcomes via `momentum-tools practice-ledger append`.
- `momentum:retro` — appends `created` events for handoff items via `momentum-tools practice-ledger append` (Phase 5.5).
- `momentum:avfl` — appends `created` events for pending-upstream-fix findings via `momentum-tools practice-ledger append`.
- Daily routine (CronCreate) — appends `closed_stale` events via `momentum-tools practice-ledger close-stale --age-days 15`.

**Readers:**

- `momentum:triage` — reads `open` + `summary` on start to re-surface open entries (DEC-033 D9).
- `momentum:sprint-planning` — Phase A.6 reads open entries filtered to `source: "retro"` during backlog synthesis.
- Impetus session-start — reads `summary` for honest counts in situational report.

**TTL closure discipline:** 15-day default. Entities without terminal events after TTL automatically receive a `closed_stale` event from the daily routine. The `close-stale` command is idempotent.

**Replaces:** `.momentum/intake-queue.jsonl` (DEC-007, now archived as `practice-ledger-pre-2026-05.jsonl`); the retired `triage-inbox.md` contract; the retired `.momentum/signals/` directory (DEC-033 D6).

---

### `momentum:triage` Architecture (DEC-007, DEC-005)

<!-- Added 2026-04-14: Entry-point and topology for the multi-item batch classification orchestrator. -->

`momentum:triage` is the missing orchestrator that sits between upstream observation sources (mid-session conversation, retro Priority Action Items, assessment recommendations) and the per-item executors (`momentum:intake`, `momentum:distill`, `momentum:decision`). It fills the structural gap where `momentum:intake` is single-item-only but real-world triage is inherently multi-item.

**Entry point:** Impetus dispatches from the `[3] Triage` menu item (replaces the placeholder in `skills/momentum/skills/impetus/workflow.md:403` and `skills/momentum/skills/impetus/SKILL.md:63`). Also independently invocable as `/momentum:triage` and programmatically callable from retro Phase 5 or sprint-planning backlog synthesis with an explicit observation list.

**Classification taxonomy:** Originally six classes (ARTIFACT / DISTILL / DECISION / SHAPING / DEFER / REJECT). **ARCH-5: The DISTILL class is removed with the removal of the distill skill (`remove-momentum-distill` story ready-for-dev). Post-removal: five active classes (ARTIFACT / DECISION / SHAPING / DEFER / REJECT).** Classification runs **inline in main context** — no subagent spawn for the classification judgment itself (it is context-dependent and cheap, and the orchestrator holds session context triage needs).

**Enrichment for ARTIFACT items:** each ARTIFACT is enriched with `feature_slug` (read from `features.json` — DEC-005 D1), `story_type` (DEC-005 D5 — default `feature`), suggested epic (DEC-005 D2 — DDD sub-domain aware), priority, and proposed dependencies. Enrichment is also inline by default.

**Mandatory dedup gate (four phases):** before classification, triage runs a deterministic duplicate-detection pipeline. **Phase 0 — Prefilter:** `momentum-tools triage prefilter` scores each incoming observation against all open/ready stories in `.momentum/stories/index.json` using TF-IDF + Jaccard similarity + epic-name boost (status-filtered: skips done/cancelled/deferred), returning a top-K=10 shortlist per observation. **Phase 1 — Clustering:** inline batch clustering groups the shortlisted candidates into per-theme clusters. **Phase 2 — Dedup fan-out:** one Explore subagent per cluster is spawned in parallel; each returns per-theme JSON findings (candidate pairs, similarity signals, consolidation recommendation). Fan-out pattern is identical to retro Phase 4. **Phase 3 — Consolidation grouping:** inline pass groups confirmed duplicate pairs into consolidation candidates for the developer's batch-approval review before any delegation fires. This gate is mandatory — not optional — regardless of observation count.

**Batch approval UX:** mirrors the pattern established by `momentum:refine` Step 9 — consolidated findings list; accept / modify / reject per item; batch operations (accept-all / reject-all) when N ≥ 5. No silent writes; the developer approves before any delegation or CLI write fires.

**Execution — delegation vs. direct write:**

| Class | Action | Target |
|---|---|---|
| ARTIFACT | Delegates to `momentum:intake` (per item) | `stories/{slug}.md` + `stories/index.json` |
| DISTILL | ~~Delegates to `momentum:distill` (per item)~~ — **removed** (ARCH-5: distill skill removed; this class is no longer active) | ~~Target practice file (rule / skill / reference)~~ |
| DECISION | Delegates to `momentum:decision` (per item) | `planning-artifacts/decisions/dec-NNN-*.md` |
| SHAPING | Appends `created` event to `practice-ledger.jsonl` via `momentum-tools practice-ledger append` (DEC-033 supersedes DEC-007) | `source: "triage"`, payload carries title/description |
| DEFER | Appends `created` event to `practice-ledger.jsonl` via `momentum-tools practice-ledger append` | `source: "triage"`, payload carries title/description |
| REJECT | Appends `created` event to `practice-ledger.jsonl` via `momentum-tools practice-ledger append` | `source: "triage"`, `event_type: "rejected"` + reason in payload |

Executor skills (`intake`, `decision`) retain their existing model and effort settings. Triage does not bypass them.

**Re-surfacing on start:** triage reads `momentum-tools practice-ledger open` on session start to re-surface open entries — items the developer captured previously but has not yet promoted, decided, or rejected. Retro handoff entries (source: `retro`) flow through the same classify / promote / continue-watching / reject UX as triage-originated entries. **No enumeration** — counts and entity_ids only (DEC-033 D9). Developer drills in via `practice-ledger history --entity <id>` for detail.

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

> _[Cleanup note 2026-04-28: The historical-status text above remains the only sprint-log mention in the architecture. The `retire-sprint-log-final-cleanup` story (sprint-2026-04-27) closes the residual cleanup — removing any leftover sprint-log scaffolding (filesystem stubs, CLI subcommands, references in skill prompts) that survived the 2026-04-08 architectural removal.]_

### Gherkin Specification Separation (Decision 30)

<!-- Added Phase 3: Black-box behavioral validation via separated Gherkin specs. -->

Story files and Gherkin specs are deliberately separated to enforce black-box validation:

- **Story files** (`.momentum/stories/{slug}.md`) — contain plain English acceptance criteria. Dev agents read these to understand intent.
- **Gherkin specs** (`.momentum/sprints/{sprint-slug}/specs/{story-slug}.feature`) — contain detailed behavioral expectations. Only verifier agents read these.

**Key constraints:**
- Gherkin specs are written during sprint planning (Step 4), before any code exists
- A spec quality pre-check gate runs after generation (Step 4): validates structure, outsider-test compliance, and template conformance before dev agents spawn
- Dev agents NEVER access `.momentum/sprints/{sprint-slug}/specs/` — this is a protection boundary
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

**Path resolution and session discovery (added 2026-04-28):** `transcript-query.py` is resolved dynamically at retro start — the highest-semver glob match wins (e.g., `~/.claude/plugins/momentum-*/scripts/transcript-query.py`), with an in-repo fallback to the source-tree copy when no installed plugin is found. This avoids hard-coding install paths and makes the tool work in both downstream-project and dogfood contexts. Worktree session discovery uses `git worktree list --porcelain` so JSONL files produced inside per-story worktrees during sprint execution are captured alongside the main checkout's sessions.

**Date filter semantics:** `--before` is **UTC end-of-day inclusive** — a sprint that completes on 2026-04-27 includes sessions up to `2026-04-27T23:59:59Z`. This avoids losing the last day of activity to timezone boundaries. `--story-slugs` is a same-day filter for sprints whose stories finished on the same calendar date as a previous sprint — passing the explicit story-slug list disambiguates which sessions belong to which sprint.

**Hard-fail on zero session matches:** When session discovery returns zero matching JSONL files, retro **halts**. There is no "continue with empty extracts" branch — empty extracts produce vacuously clean retros that mask the underlying problem (wrong sprint window, unreadable plugin path, worktree not yet committed). The hard-fail surfaces the misconfiguration immediately so the developer can correct it before auditors run.

New dependency: DuckDB (`pip install duckdb`). The tool checks and auto-installs if missing.

Extraction queries (run automatically):

| Extract | What | Source |
|---|---|---|
| `user-messages.jsonl` | All human-typed prompts across all sessions | Session JSONL files |
| `agent-summaries.jsonl` | Per-subagent digest: prompt, outcome, tool counts, error count, turns | Subagent JSONL files |
| `errors.jsonl` | Tool errors using actual error indicators (`is_error` flag, `tool_use_error` responses) | All JSONL files |
| `team-messages.jsonl` | Inter-agent SendMessage and teammate-message content | Subagent JSONL files |

Output directory: `.momentum/sprints/{sprint-slug}/audit-extracts/`

`transcript-query.py` is standard retro tooling resolved dynamically (highest-semver plugin-cache glob, in-repo fallback), supporting both pre-built queries and ad-hoc SQL via `transcript-query.py sql "..."`. The peek-first convention (run `wc -l` before reading any file, read in 500-line chunks for files over 200 lines, never full-Read known-large files) applies to all auditor and spec-impact-discovery agents reading extract files or planning artifacts.

**Wave 2: Auditor Team (3 auditors + 1 documenter)**
Shape A topology (Decision 41; fix-retro-documenter-replication-defect): spawn the documenter alone first via TeamCreate(cardinality=1) into team `retro-{sprint-slug}`, then fan out 3 individual Agent spawns that join the same team:

- **documenter** — spawned first via TeamCreate(cardinality=1). Receives findings from all 3 auditors via SendMessage. Builds the findings document. Owns it exclusively. After all auditors report, performs cross-cutting synthesis pass.
- **auditor-human** — individual Agent spawn joining team `retro-{sprint-slug}`. Reads `user-messages.jsonl`. Identifies corrections, redirections, frustration signals, praise/approval, and decision points.
- **auditor-execution** — individual Agent spawn joining team `retro-{sprint-slug}`. Reads `agent-summaries.jsonl` + `errors.jsonl`. Investigates duplication patterns, error recovery, tool usage efficiency, and story iteration counts via ad-hoc `transcript-query.py` queries.
- **auditor-review** — individual Agent spawn joining team `retro-{sprint-slug}`. Reads `team-messages.jsonl` + agent summaries filtered to review roles. Evaluates quality gate effectiveness, fix cycle productivity, and inter-agent coordination quality.

Output: `.momentum/sprints/{sprint-slug}/retro-transcript-audit.md` — replaces the previous dual triage output. Structure: Executive Summary, What Worked Well, What Struggled, User Interventions, Story-by-Story Analysis, Cross-Cutting Patterns, Metrics, Priority Action Items. Each finding includes: what happened, evidence, root cause, recommendation (fix/keep/investigate).

**What stays from the current retro:** Phase 1 (Sprint Identification), Phase 3 (Story Verification), Phase 6 (Story Stub Creation — now informed by transcript audit findings), Phase 7 (Sprint Closure). **What is replaced:** Phase 2 (Log Collection → DuckDB preprocessing), Phase 4 (Cross-Log Discovery → auditor team analysis), Phase 5 (Triage Output Generation → documenter's findings document).

**Phase 6 extension (Decision 47):** After story stub creation and before sprint closure, the retro orchestrator: (1) spawns `/momentum:feature-status` to refresh the feature cache; (2) reads the updated `.claude/momentum/feature-status.md` for feature status deltas; (3) writes `.momentum/sprints/{sprint-slug}/sprint-summary.md` with sections: Features Advanced (conditional), Stories Completed vs. Planned, Key Decisions, Unresolved Issues, Narrative (500-word cap). The sprint summary is the sole compression artifact for sprint-to-sprint context transfer.

**Phase 5 extension (DEC-007, 2026-04-14):** Retro gains a **secondary** machine-readable output alongside the primary `retro-transcript-audit.md` findings document. Un-actioned findings that the developer chooses to carry forward are written as `handoff` events to `.momentum/intake-queue.jsonl` with `source: "retro"`, `kind: "handoff"`, `status: "open"` — via the `momentum-tools` CLI, not direct file writes. These events are consumed by `momentum:sprint-planning` Phase A.5 and by `momentum:triage` re-surfacing on session start. The primary `retro-transcript-audit.md` output is unchanged; handoff events are additive. See the `intake-queue.jsonl` Schema Contract section for the full field contract. Per DEC-005 D7/D8 (failure-as-diagnostic framing and feature-state transitions) and DEC-005 D10 (retro does not gap-check when emitting handoffs). Implementation story: `retro-triage-handoff`.

**Decision 28 — Triage vs Refinement Distinction (superseded-partial 2026-04-14 by DEC-005 D10 and DEC-007)**

> _[Superseded-partial 2026-04-14: The original framing of triage as "intake-focused: analyze documents/ideas, create story stubs, initial prioritization, assign to an epic" is reshaped. Under DEC-005 D10, gap-check is explicitly excluded from triage (and from intake); it lives only at refinement, sprint-planning, and retro. Under DEC-007, triage is a **batch-classification orchestrator with delegation-only semantics** — it classifies observations into a formalized six-class taxonomy (ARTIFACT / DISTILL / DECISION / SHAPING / DEFER / REJECT) and delegates ARTIFACT/DISTILL/DECISION outcomes to the respective executor skills, writing SHAPING/DEFER/REJECT inline to `intake-queue.jsonl` via CLI. It is no longer the actor that "creates story stubs, does initial prioritization, assigns to an epic" — the delegated executor (`momentum:intake`) does that. See `momentum:triage` Architecture and `intake-queue.jsonl` Schema Contract sections above, and `_bmad-output/planning-artifacts/decisions/dec-007-triage-capture-artifact-2026-04-14.md`.]_

Triage is intake-focused: analyze documents/ideas, create story stubs, initial prioritization, assign to an epic. Refinement is organization-focused: classify, prioritize, gap-analyze the whole backlog. Different purposes, complementary workflows. Both deferred to Phase 5.

**Decision 29 — Sprint Planning Builds the Team (Extended 2026-04-06: Synthesis-First; Extended 2026-04-11: Sprint Summary Read; Extended 2026-04-14: Retro Handoff Queue Read)**
Sprint planning (`/momentum:sprint-planning`) encompasses story selection, create-story invocation, team composition, dependency graph construction, and execution plan generation. Sprint planning is a proper skill (not an inline workflow module) — invoked by Impetus or directly by the user. The sprint record stores team + dependencies (not just story lists and wave assignments). See Sprint Planning Workflow section.

Step 1 (Backlog Presentation) is synthesis-first: before presenting any backlog data, read the master plan documents (`prd.md`, product brief) to understand strategic priorities. Read the most recent sprint summary (`.momentum/sprints/{last-sprint-slug}/sprint-summary.md`) for "what just happened" context — non-blocking if absent (Decision 47). **Phase A.5 additionally reads `.momentum/intake-queue.jsonl` filtered to `source: "retro"`, `kind: "handoff"`, `status: "open"` — open handoff events from recent retros are folded into the synthesis context alongside the previous sprint summary (per DEC-007, 2026-04-14). If the queue file does not yet exist, treat as empty and continue silently.** Run a staleness check via `git log` for each `ready-for-dev`/`in-progress` story — check commits touching the story's `touches` paths. Lead with 3-5 prioritized recommendations with rationale (informed by master plan priorities, sprint summary findings, open retro handoff items, dependency readiness, backlog state), followed by the full sorted backlog as secondary reference. Potentially stale stories are surfaced separately with commit evidence. **Phase C output gains a labeled "Open handoff items from recent retros" section** that lists each open `source: "retro", kind: "handoff"` entry by title, source sprint, and (when present) its feature-state transition or failure-diagnosis framing. If master plan documents are missing, fall back to sorted backlog with a warning.

**Decision 30 — Gherkin Separation (Extended 2026-04-08: Spec-Quality Feedback Loop; Extended sprint-2026-05-17: All Contract Types)**
Story files retain plain English ACs (dev sees intent). Sprint-scoped specs directory holds contract files (verifiers only). As of sprint-2026-05-17 (`sprint-planning-frozen-per-story-contract` story), the specs directory covers all five contract types driven by each story's `verification_method` field — not Gherkin-only: `.feature` (Gherkin), `.eval.yaml` (LLM eval), `.trigger.md` (trigger-based), `.smoke.sh` (smoke test), `.review.md` (manual review). Black-box behavioral validation: contracts written pre-implementation, validated post-implementation, by different agents. See Gherkin Specification Separation section. **Enum reconciliation (sprint-2026-06-02, conduct-core):** the `verification_method` values use the driver-binding vocabulary `skill-invoke | behavioral-trigger | bash | smoke | document-review | curl` (superseding the legacy `eval|trigger|smoke|review|gherkin|skip` keys); the contract extensions above are unchanged. The method is the driver-binding key — method == harness_profile == driver-binding key.

**Spec-quality feedback loop:** When E2E Validator encounters untestable Gherkin scenarios (ambiguous steps, missing preconditions, implementation-coupled assertions), findings are tagged with `spec-quality` metadata. These findings are surfaced in a dedicated "Spec Quality" section of the retrospective output, separate from implementation findings. This closes the loop between validation and specification: spec authoring issues are traced back to the sprint planning Gherkin generation step (Decision 29, Step 4) rather than treated as implementation failures.

**Decision 31 — AVFL at Sprint Level**
AVFL validates the complete sprint plan during planning (all stories together). AVFL runs once after ALL stories merge during sprint execution (not per-story). Per-story AVFL is removed from `momentum:create-story` and `momentum:dev`. This catches cross-story integration issues that per-story AVFL would miss. See Agent Pool Governance section. Phase 4 runs AVFL in scan profile (Decision 34) — discovery only, no fix loop. Findings are handed to the hybrid Agent Team.

**Conduct path — AVFL-on-merge (DEC-035 / Decision 59):** the conduct execution engine does **not** use this legacy post-all-merge stop-gate. Instead it runs AVFL as a dynamic Workflow **on each merge**, scoped to the **merge-base diff** for that story, returning a typed verdict `CLEAN | NON_CONVERGENT`. A `CLEAN` result lets the merge proceed; `NON_CONVERGENT` routes back into the conduct fix loop. This is distinct from the sprint-dev Phase 4 stop-gate (which runs once over the whole codebase after all stories merge and halts for developer acknowledgment). The two paths coexist while sprint-dev and conduct coexist (DEC-037).

**Decision 34 — AVFL Scan Profile and Hybrid Resolution Team (2026-04-04, Extended 2026-04-28)**
AVFL and resolution teams serve distinct purposes. AVFL excels at adversarial multi-lens discovery (dual-reviewer cross-check). Teams excel at concurrent resolution and E2E behavioral verification. The scan profile separates these concerns.

Scan profile: all 4 lenses, dual reviewers (Enumerator + Adversary), maximum skepticism (level 3), consolidation with cross-check confidence. Zero fix iterations — output is scored findings list only.

Hybrid model: AVFL scan → findings handed to concurrent Agent Team (Dev, QA, E2E Validator, Architect Guard). Team works concurrently on main branch. E2E Validator tests running behavior with external tools — fundamentally different from AVFL's file-content validation.

**BLOCKED-vs-MISSING semantics for AC classification (added 2026-04-28):**

QA Reviewer and E2E Validator classify each acceptance criterion against observed sprint output. Two outcomes that look superficially similar must remain semantically distinct:

| Classification | Meaning | When to use |
|---|---|---|
| `BLOCKED` | Execution was prevented by missing infrastructure (e.g., test runner not installed, environment dependency absent, required service not running). The reviewer could not even attempt to gather AC evidence. | Infrastructure gap — surface as a blocker, not as an AC failure |
| `MISSING` | Execution succeeded, but no AC evidence was found (e.g., the test ran but the behavior the AC describes was not observed; the feature appears unimplemented). | Genuine AC failure — feature did not deliver what the story promised |

`BLOCKED` items are not "the AC failed" — they are "the practice failed to produce evidence." Treating BLOCKED as MISSING produces false-failure findings that mischaracterize execution gaps as product gaps. Both reviewers MUST follow `.claude/rules/e2e-validation.md` Environment Startup before classifying any AC — environment readiness is a precondition for the BLOCKED-vs-MISSING distinction to be meaningful.

**Defense-in-depth contract:** The QA Reviewer (`agents/qa-reviewer.md`) and E2E Validator (`agents/e2e-validator.md`) definitions both carry Critical Constraints sections that encode these rules. The constraints are kept in **parity** between the two definitions — see Defense-in-depth across spawn-prompt and agent-definition layers in the Process Patterns section. Drift between the two definitions creates inconsistent classifications and is a defect at the Decision 34 contract level.

**Origin:** `harden-sprint-dev-phase5-spawn-prompts` story (sprint-2026-04-27).

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
| E2E Validator | Agent definition file (`agents/e2e-validator.md`) | Pure worker: method-polymorphic and harness-driven (sprint-2026-05-17). Reads `momentum/verification-harness.json` at startup; dispatches by contract file extension (`.eval.yaml`, `.trigger.md`, `.smoke.sh`, `.review.md`, `.feature`). Needs Bash for test execution. Never user-invoked. Used in sprint Team Review (Decision 34) and quick-fix Phase 4 validation (Decision 40). |
| Architect Guard | SKILL.md with `context: fork` (existing) | Already implemented as standalone verifier skill. Also useful outside Team Review (ad-hoc drift checks). Retains SKILL.md deployment. |

**Plugin structure addition:**

The plugin root gains an `agents/` directory alongside `skills/`:

```
skills/momentum/                     ← Plugin root
├── .claude-plugin/plugin.json
├── skills/                          ← SKILL.md files (user-facing + context:fork)
├── agents/                          ← Agent definition files (pure spawned workers)
│   ├── qa-reviewer.md               ← Team Review: story AC review
│   ├── e2e-validator.md             ← Team Review: behavioral validation (Gherkin)
│   ├── dev.md                       ← Base dev agent for sprint-dev spawning
│   ├── dev-skills.md                ← Specialist: SKILL.md, workflow.md, agent definitions
│   ├── dev-build.md                 ← Specialist: Gradle and build system work
│   ├── dev-frontend.md              ← Specialist: Kotlin Compose and frontend UI work
│   ├── ux.md                        ← Specialist: UX design and UI specification work
│   ├── analyst.md                   ← Specialist: business analysis and requirements work
│   └── researcher.md                ← Specialist: technical research and discovery work
├── hooks/
├── scripts/
└── references/
```

Agent definition files are discovered by Claude Code from the plugin's `agents/` directory (resolution priority 4: plugin agents). The `name` field in YAML frontmatter determines the `subagent_type` used in Agent tool calls.

**Base body conventions for agent definition files (added sprint-2026-05-16):**

Every shipped agent definition follows a standard body structure:
- **CREED block** — 3–5 statements in the form "I [verb] because [reason]" that anchor the agent's identity and decision-making orientation (e.g., "I validate because correctness is cheaper to catch early than to fix late").
- **Constitution source** — agents reference `constitution.md` as the project context source (not `project-context.md`). `constitution.md` is produced by constitution-builder (Tier 1, once per project).
- **Mandatory output templates with sentinel markers** — every agent definition includes a concrete output template using `AGENT_OUTPUT_START` / `AGENT_OUTPUT_END` sentinel markers. Orchestrators detect structured output by scanning for these sentinels; freeform prose between them is not parsed.
- **Prohibitions with consequence clauses** — each Critical Constraints section pairs every prohibition with an explicit consequence: "Do not X — doing so causes Y and violates the [contract name] contract." Bare prohibitions without consequence clauses are disallowed in shipped definitions.

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
| ~~Distill~~ | ~~Single practice artifact, single session~~ | ~~Discover → classify → apply → validate → commit~~ | ~~`/momentum:distill` (Decision 42)~~ — **removed (ARCH-1)** |

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
| momentum:retro | Phase 4 (auditor team) | documenter (singleton coordinator, cardinality 1) — distinct from auditor fan-out group: auditor-human, auditor-execution, auditor-review (cardinality 3, distinct subagent_types) | `individual` (singleton spawn for documenter; fan-out for auditors via 3 individual Agent spawns — Shape A preferred; Shape B via TeamCreate as fallback only if documenter handle must be in TeamCreate config) | `parallel` |

**Sprint planning validation:** Step 5 (Execution plan and team composition) validates the planned `team` object against the workflow's declared required roles. If a required role is missing from the plan, sprint planning surfaces the gap before activation. This is a pre-activation gate — the sprint cannot be activated with an incomplete team.

**Rationale:** Team composition rules were implicit — the sprint record carried a `team` object, but workflows did not declare what roles they need, how agents should be spawned, or concurrency expectations. When Impetus had to infer these from context, it improvised incorrectly. Explicit declarations make composition deterministic and testable.

**Traceability:** Extends Decision 26 (Two-Layer Agent Model) with structural enforcement and Decision 29 (Sprint Planning Builds the Team) with a validation gate. Triggered by sprint-2026-04-06 retro finding: 6 of 10 user corrections were about team composition and spawning.

**Documented pattern — refine two-wave conditional spawning (2026-04-06):**
momentum:refine uses a two-wave conditional spawning pattern as a documented instance of Decision 41 composition:
- **Wave 1:** Two discovery agents spawn in parallel (prd-coverage-agent, architecture-coverage-agent). Each independently analyzes its document for coverage gaps, staleness, and update candidates, returning structured findings.
- **Developer approval gate:** Orchestrator presents Wave 1 findings and requires developer approval before proceeding. Developer may approve, modify, or reject updates per document independently.
- **Wave 2:** Zero, one, or two update agents spawn based on Wave 1 findings and the developer's approval decision. Each approved document gets its own sole-writer update agent; no update agent spawns for a rejected document. Agents run in parallel when both are approved.
This pattern is distinct from the per-finding Add/Modify/Remove triage used in other workflows — approval is per-document, not per-finding, enabling batch UX at the document level.

**Decision 42 — Distill Execution Path and AVFL Profile (2026-04-11) — REMOVED**

> _[ARCH-1: `momentum:distill` is being removed. The `remove-momentum-distill` story is ready-for-dev. All references to distill as an active system component — including findings-ledger write authority, triage DISTILL class, and the "third execution path" framing — are deprecated. After the story ships, distill will no longer exist as an execution path. The content below is preserved for historical context only.]_

~~`/momentum:distill` is a third execution path alongside sprint orchestration and quick-fix (Decision 39).~~ It was the practice-artifact analogue of quick-fix: where quick-fix handles code stories, distill handled practice artifacts (rules, references, skill prompts, spec additions). **This execution path is removed.**

**Distill AVFL profile:** A lightweight single-pass validation mode designated for distill's post-change validation step. Runs two subagents (Enumerator + Adversary) on only the changed files. No multi-lens parallelism — a single validation pass, not separate structural/accuracy/coherence passes. Model: Sonnet at medium-low effort. No fix iterations — output informs a developer-prompted correction or a clean commit. Implemented as a named profile in `skills/avfl/references/framework.json`.

**Rationale:** The discovery phase (two parallel agents before any changes are written) handles most structural and design correctness concerns upfront. The post-change AVFL pass is intentionally lighter — it validates a small, targeted artifact change, not a full document corpus. The lightweight profile preserves the "fast path" characteristic of distill while ensuring changes receive adversarial review before committing.

**Fix scope routing:**
- Project-local: applies to current project's rules/references only
- Momentum-level (in Momentum project): applies to Momentum practice files; bumps plugin patch version; commits and pushes
- Momentum-level (in external project): defer to retro queue OR generate remote distill prompt for developer to apply in a Momentum session

**Findings-ledger write authority:** ~~`momentum:distill` is an authorized writer to `~/.claude/momentum/findings-ledger.jsonl` (extending Decision 1c).~~ **ARCH-7: With the removal of the distill skill, `momentum:distill` is no longer an authorized findings-ledger writer. The sole authorized writer shrinks to the flywheel workflow only (`origin: flywheel`).** Decision 1c is updated accordingly — the `origin: distill` write path is removed.

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
- **Option A (primary):** Every findings-ledger write includes a `momentum_version` field populated from the installed plugin version at write time. Applies to all ledger writers: `momentum:retro` (Phase 0 brief + Phase 5 stubs), and any future writers. Note: `momentum:distill` was previously listed here; it is removed as an authorized writer — see ARCH-7 / Decision 42.
- **Option B (validation):** Git log timestamps map sessions to Momentum version bumps for cross-checking. Used to validate Option A data and to backfill version attribution for ledger entries that predate the `momentum_version` field.

**Phase 0 output:** A structured session-analytics brief written to the retro working directory. Contains: sprint window, sessions analyzed, metric table with sprint-over-sprint delta, and flagged regressions. Phase 1 auditors receive this brief before qualitative review begins.

**Traceability:** Motivated by Fowler feedback flywheel research (2026-04-10) — Momentum captures failure signals but not quantitative regression signals. Log-audit research (2026-04-11) confirmed all metrics are extractable from existing session JSONL files without instrumentation changes. The findings-ledger `momentum_version` field extends Decision 42's ledger schema.

---

## Feature-Orientation Architecture Decisions (44-48)

<!-- Added sprint-2026-04-11: Feature-orientation epic decisions. These decisions introduce the feature artifact layer, feature status visualization, cache infrastructure, sprint summary artifact, and practice project detection. -->

**Decision 44 — Feature Artifact Layer (sprint-2026-04-11)** — **HISTORICAL — superseded by DEC-034 (Epic-Layer Consolidation, 2026-05-25)**

> _[HISTORICAL: The dual features.json + categorical-epics architecture described in Decisions 44–49 is superseded by DEC-034, which unifies both layers into a single `epics.json` at `_bmad-output/planning-artifacts/epics.json`. Migration executed in story B1 (sprint-2026-05-26). See DEC-034 and `_bmad-output/planning-artifacts/epics.json` for the current schema. Decisions 44–49 are preserved here as historical record only.]_

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
| `stories` | array | Story slugs that implement or advance this feature (also referenced as `story_slugs` in some contexts — both refer to the same array of kebab-case slug strings) |
| `stories_done` | int | Count of stories in terminal state (`done`) |
| `stories_remaining` | int | Count of stories not yet done |
| `last_verified` | date | ISO 8601 date of last manual or automated verification |
| `notes` | string | Free text for gaps, partial-status explanations, open questions |
| `depends_on` | array | Optional. Feature-to-feature dependency list — array of feature slugs that must reach `working` status before this feature can be considered complete. Absent or empty means no feature-level dependencies. |

**Write authority:** `features.json` is written exclusively by `momentum:feature-grooming` (bootstrap and refine modes). No other skill or tool writes features.json. Grooming mode detection: bootstrap = features.json absent or empty; refine = features.json has ≥1 entry. `acceptance_conditions` is an array of strings — each entry is one behavioral, verifiable acceptance condition.

**Rationale:** Epics provide theme-based grouping that serves sprint planning. Features provide capability-based grouping that serves developer orientation and stakeholder communication. A feature can span multiple epics. An epic can advance multiple features. The two axes compose — neither replaces the other.

**Traceability:** Introduced by the feature-artifact-schema story in sprint-2026-04-11. Motivated by DEC-002 (Feature Visualization and Developer Orientation): the current epics-only model makes it impossible to answer "is the app usable end-to-end?" without reading all story files.

---

**Decision 45 — Feature Status Skill: Standalone with Dual Output (sprint-2026-04-11)** — **HISTORICAL — superseded by DEC-034 (2026-05-25)**

`/momentum:feature-status` is a standalone flat skill that reads `features.json` + `stories/index.json` and produces two output artifacts for different consumption contexts.

**Inputs:**
- `_bmad-output/planning-artifacts/features.json` — feature definitions and current status
- `.momentum/stories/index.json` — story statuses for gap detection

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

**Decision 46 — Feature Status Cache Pattern and Startup Integration (sprint-2026-04-11)** — **HISTORICAL — superseded by DEC-034 (2026-05-25)**

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
stories_content = open(".momentum/stories/index.json").read()
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

**Decision 47 — Sprint Summary at Retro Boundary (sprint-2026-04-11)** — **HISTORICAL in part — features.json reference superseded by DEC-034 (2026-05-25); sprint-summary.md artifact remains in force**

A new artifact written by the retro orchestrator at Phase 6 close: `.momentum/sprints/{sprint-slug}/sprint-summary.md`. It compresses each completed sprint's signal into a structured reference document for sprint planning and future retro context loading.

**Artifact path:** `.momentum/sprints/{sprint-slug}/sprint-summary.md`

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

**Decision 48 — Practice Project Detection and Practice Rendering Path (sprint-2026-04-11)** — **HISTORICAL — features.json reference superseded by DEC-034 (2026-05-25); detection heuristic may survive in different form for canvas**

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

**Decision 49 — Feature Grooming Skill: Orchestrator Pattern and Write Authority (sprint-2026-04-11)** — **HISTORICAL — superseded by DEC-034 (2026-05-25); momentum:feature-grooming retired and absorbed into momentum:epic-grooming (B4, sprint-2026-05-26). Successor: `momentum:epic-grooming` is now the sole authorized writer of `epics.json` with the same orchestrator pattern and mode detection described here, retargeted at `epics.json`.**

The `momentum:feature-grooming` skill is a flat orchestrator. It spawns exactly 2 discovery subagents in a single message (model: haiku, effort: quick):

- **Agent A:** reads PRD and epics.md, extracts feature candidates and FR groupings
- **Agent B:** reads architecture.md and stories/index.json, extracts capability clusters and story themes

The orchestrator handles all synthesis, value analysis, developer interaction, and file writes directly. No additional subagents are spawned beyond the initial 2.

**Write authority:** `momentum:feature-grooming` is the sole authorized writer of `features.json`. In bootstrap mode it also writes assessment documents to `_bmad-output/planning-artifacts/assessments/` and decision documents to `_bmad-output/planning-artifacts/decisions/` before writing features.json.

**Mode detection:** bootstrap when features.json absent or has ≤2 entries; refine when features.json has ≥3 entries.

**Rationale:** The flat orchestrator pattern keeps the synthesis step in a single context that can reason holistically across both discovery inputs. Two discovery subagents are sufficient to parallelize the read-heavy work; further parallelism would fragment the synthesis context without benefit. Sole write authority over features.json ensures the schema (including `value_analysis` and `system_context` fields added in Decision 44) is always populated correctly and consistently.

**Traceability:** Introduced by feature-grooming story in sprint-2026-04-11. Complements Decision 44 (features.json schema and write authority) and Decision 45 (feature-status read path).

---

**Decision 50 — Epic Breakdown Skill: Canonical Epic-to-Story Gap Enumerator (sprint-2026-04-18, updated B4 sprint-2026-05-26)** — _Renamed from feature-breakdown to epic-breakdown per DEC-034 D6 (B4). Now takes `epic_slug` as input and reads `epics.json` instead of `features.json`. `source_label` updated to `"epic-breakdown:{epic_slug}"`._

The `momentum:epic-breakdown` skill is the canonical entry point for converting an epic slug into a prioritized list of story gaps required to ship that epic end to end. No other skill in the practice takes an epic slug as primary input and produces a gap enumeration as output.

**Role boundary:** `epic-breakdown` is a pure orchestrator. It NEVER writes to `epics.json`, `stories/index.json`, or any planning artifact. Its sole output is a ranked candidate list passed to `momentum:triage` for disposition. All classification and routing authority belongs to triage.

**Delegation contract:** `epic-breakdown` passes `source_label = "epic-breakdown:{epic_slug}"` to `momentum:triage`, satisfying the pre-enumerated-list contract. Triage classifies each candidate into the standard classes (ARTIFACT / DECISION / SHAPING / DEFER / REJECT) and handles all writes.

**Why this skill exists:** The practice has no other skill that takes an epic slug and authors the missing work.
- `momentum:epic-grooming` catalogs epics (successor to Decision 49) — does not enumerate story gaps
- `momentum:canvas` reports health — read-only, no gap authoring
- `momentum:sprint-planning` assumes the backlog is already ready — does not create stories
- `momentum:triage` classifies pre-formed observations — does not enumerate what is missing

`epic-breakdown` fills this gap: given an epic, find what stories are required but do not yet exist.

**Non-responsibility:** `epic-breakdown` does NOT decide sufficiency. It identifies candidates. The developer and triage decide what becomes a story.

**Pattern references:** Fan-out spawning from Decision 41 / `spawning-patterns.md`; orchestrator purity from existing decisions; triage delegation contract from the triage row in the Skills Deployment Classification table.

---

**Decision 51 — Cycle Redesign: Feature-First Practice (DEC-005, 2026-04-14)**

Formalizes the cycle redesign captured in `_bmad-output/planning-artifacts/decisions/dec-005-cycle-redesign-feature-first-practice-2026-04-14.md`. DEC-005 reframes the practice around features (the units of user-observable value) and codifies a set of capture, classification, and hygiene rules that ripple through intake, triage, retro, refinement, and sprint planning.

**Adopted sub-decisions (D1–D10):**

| Sub-decision | Summary |
|---|---|
| D1 — Feature-bound capture | Every captured observation must be feature-aware. `intake` and `triage` enrich items with `feature_slug` (read from `features.json`); items that imply new feature-bearing work carry `suggested_feature_slug`. |
| D2 — DDD sub-domain awareness for epics | Epic suggestions during triage are sub-domain-aware: epic recommendations consider DDD bounded-context boundaries, not just thematic grouping. |
| D5 — Story type taxonomy | Every story carries an explicit `story_type`: `feature` \| `maintenance` \| `defect` \| `exploration` \| `practice`. Default is `feature`. Type drives downstream validator selection and reporting. |
| D6 — Terminal-state awareness | Items whose underlying feature is `Abandoned` or `Rejected` are auto-suggested for REJECT on triage re-surface. Prevents zombie capture against dead features. |
| D7 — Failure as legitimate diagnostic category | Retro names specific failures via `failure_diagnosis` (`{ attempted, didnt_work, learned }`) — not softened into generic "learnings." Failure diagnosis is a first-class retro output. |
| D8 — Retro feature-state hygienist role | Retro observes and records `feature_state_transition` events (`{ feature_slug, prior_state, observed_state, evidence }`) — e.g., feature X asserted Done but retro observed regression. |
| D10 — Gap-check boundary | Gap-check (value-floor analysis, missing-work enumeration) is explicitly excluded from `triage` and `intake`. It lives only at refinement, sprint-planning, and retro. Triage classifies; it does not enumerate gaps. |

(Sub-decisions D3, D4, D9 are reserved/deferred per the source decision document — no architectural impact in this revision.)

**Where DEC-005 surfaces in the architecture:**
- Skills Deployment Classification — `intake` (single-item, feature-slug and story-type aware per D1/D5) and `triage` (no gap-check per D10) rows reference the sub-decisions directly
- `intake-queue.jsonl` Schema Contract — `feature_slug`, `suggested_feature_slug`, `story_type`, `feature_state_transition`, and `failure_diagnosis` optional fields encode D1, D5, D7, D8
- `momentum:triage` Architecture — enrichment uses D1/D5/D2; terminal-state awareness uses D6; the no-gap-check rule enforces D10
- Retro → Planning Handoff via Unified Intake Queue — D7 (`failure_diagnosis`) and D8 (`feature_state_transition`) define the structured framing for handoff events

**Motivating stories:**
- `triage-skill` — implements D1/D2/D5/D6/D10 in the new triage orchestrator
- `retro-triage-handoff` — implements D7/D8 in the retro producer side

**Source decision document:** `_bmad-output/planning-artifacts/decisions/dec-005-cycle-redesign-feature-first-practice-2026-04-14.md`

---

**Decision 52 — Practice-Ledger Event-Log Redesign (DEC-033, 2026-05-25) — SUPERSEDES DEC-007**

> _[Rewritten 2026-05-28 by story a1-practice-ledger-schema-cli-redesign-true-append-only. DEC-007 / the prior intake-queue.jsonl contract is superseded in full by DEC-033. The original DEC-007 text is preserved in the decision document at `_bmad-output/planning-artifacts/decisions/dec-007-triage-capture-artifact-2026-04-14.md` for historical traceability.]_

Formalizes the practice-ledger redesign recorded in `_bmad-output/planning-artifacts/decisions/dec-033-practice-ledger-event-log-redesign-2026-05-25.md`. DEC-033 resolves four production defects in the prior `intake-queue.jsonl` design (architecture-vs-code drift; lost-update concurrency unsafety; backlog rot; "last 5" surfacing defect) and pre-empts a latent fifth in Decision 1c. The `.momentum/signals/` directory is simultaneously retired (DEC-033 D6) — its two signal use cases flow through the unified ledger.

**What was decided (DEC-033 D1–D8 + D10):**

- **Filename:** `.momentum/intake-queue.jsonl` → `.momentum/practice-ledger.jsonl`. The prior file is frozen as `.momentum/practice-ledger-pre-2026-05.jsonl` (hard-cut migration, DEC-033 D8). No schema transformation of the 88 archived entries — they are readable for archeology.
- **True append-only (DEC-033 D1):** Every write uses POSIX `open(path, 'a')` with O_APPEND semantics. "Consume" appends a new `consumed` event referencing the original `entity_id` — the whole-file-rewrite consume path is eliminated. The file is never truncated or rewritten.
- **Schema — first-class event_id / entity_id distinction (DEC-033 D2):** Every row carries: `event_id` (unique per row, immutable), `entity_id` (repeats for the same logical entity), `ts` (ISO-8601 UTC ending in Z), `event_type` (fixed enum, see D3), `source` (originating skill/workflow), `actor` (human or agent identity), `payload` (JSON object). `custom_event_type` present only when `event_type == "custom"`. `status` is not a stored field — current state is derived by folding events.
- **Seven event types (DEC-033 D3):** `created`, `updated`, `consumed`, `rejected`, `closed_stale`, `reopened`, `custom`. Terminal types: `consumed`, `rejected`, `closed_stale`. Non-terminal: `created`, `updated`, `reopened`, `custom`.
- **Closure discipline + 15-day TTL (DEC-033 D4, D5):** `momentum-tools practice-ledger close-stale --age-days 15` appends `closed_stale` events for every non-terminal entity whose `created` event is older than the TTL. A daily Claude Code Routine runs this command. The command is idempotent. Impetus session-start invokes close-stale as a safety net if the last routine run is older than 24h.
- **Signals/ retired (DEC-033 D6):** `.momentum/signals/` directory is retired. The two signal use cases (`triage-uncleared`, `avfl-finding-pending-upstream-fix`) are entries in practice-ledger with appropriate `source` + `payload`. Every open entry IS the attention surface.
- **Fixed-read reader CLI (DEC-033 D7):** `momentum-tools practice-ledger` subcommands — `summary`, `open`, `history --entity <id>`, `since <iso-ts>`, `by-source <source>`. As implemented in story a1, state is derived today via a **pure-Python fold** (`_load_ledger_events`: glob `.momentum/practice-ledger*.jsonl` → per-line JSON parse → fold by `entity_id`); never stored. No `duckdb` import is present. D7 originally called this a "DuckDB-backed reader," but the value DuckDB actually adds — an arbitrary-SQL-query interface over the ledger — was not built and is DEFERRED to follow-up story `practice-ledger-duckdb-sql-query-command` (high priority). The five fixed subcommands above are complete and tested without it. `summary` distinguishes new-schema entries from legacy archive entries (`archive_entries` count).
- **CLI-only writes:** All writers go through `momentum-tools practice-ledger`. Skills never open the file for direct mutation.

**Producer/consumer matrix:**

| Direction | Component | Operation |
|---|---|---|
| Writer | `momentum:triage` | `created` events for SHAPING/DEFER/REJECT outcomes via `momentum-tools practice-ledger append` |
| Writer | `momentum:retro` Phase 5.5 | `created` events for handoff items via `momentum-tools practice-ledger append` |
| Writer | `momentum:avfl` | `created` events for pending-upstream-fix findings (source: `avfl`) |
| Writer | Routine (daily) | `closed_stale` events via `momentum-tools practice-ledger close-stale` |
| Reader | `momentum:triage` | `summary` + `open` to re-surface open entries on session start |
| Reader | `momentum:sprint-planning` Phase A.5/A.6 | `open` filtered to `source: retro` entries for backlog synthesis |
| Reader | Impetus session-start | `summary` for honest counts in situational report |

**Glob-ready reader path:** `.momentum/practice-ledger*.jsonl` — covers both active file and pre-2026-05 archive. Legacy archive entries that lack `event_id` are reported as `archive_entries` (not crashes) by the reader.

**Source decision document:** `_bmad-output/planning-artifacts/decisions/dec-033-practice-ledger-event-log-redesign-2026-05-25.md`

**Prior DEC-007 decision document (historical):** `_bmad-output/planning-artifacts/decisions/dec-007-triage-capture-artifact-2026-04-14.md`

---

**Workflow Modularization Note (2026-04-04)**

The Impetus `workflow.md` file is a structural concern at 800+ lines. The greeting redesign (Step 7 alone is 232 lines in the mockup) will increase this further. Modularization into separate workflow modules (e.g., `greeting.md`, `dispatch.md`, `install.md`) is architecturally sound and recommended but not required for the greeting redesign. This note flags the concern for future sprint planning.

---

**Decision 53 — Canonical Momentum Cycle Step Sequence (DEC-017, 2026-05-03)**

Formalizes the canonical step sequence for a Momentum practice cycle, establishing which phases are required and which are optional. DEC-017 also defines the cycle boundary rule used by the canvas dashboard timeline.

**Canonical step sequence:**

```
triage → intake → epic-grooming → refine → sprint-planning → sprint-dev → retro
```

_Note: The prior sequence included separate `feature-grooming` and `epic-grooming` nodes. Per DEC-034 D6 (B4, sprint-2026-05-26), these are collapsed into a single `epic-grooming` node. The canvas timeline renders **6 nodes** (not 7) after B3 updates the L1 view._

The canvas timeline collapses `intake` into the `triage` node for visual compactness.

**Phase classification:**

| Phase | Classification |
|---|---|
| `sprint-planning` | Required |
| `sprint-dev` | Required |
| `retro` | Required |
| `triage` | Optional |
| `epic-grooming` | Optional |
| `refine` | Optional |

**Cycle boundary rule:** The most recent sprint entry in `.momentum/sprints/index.json` whose `retro_run_at` field is set (non-null) marks the end of the previous cycle. All practice activity after that sprint's `retro_run_at` timestamp constitutes the current cycle. Sprints without `retro_run_at` belong to the current cycle.

**Canvas timeline application:** The canvas L1 timeline view renders one column per cycle. Each column shows which phases ran (filled node) and which did not run (hollow node) during that cycle. The current cycle column is always the rightmost, showing in-progress phases in a distinct state.

**Traceability:** Introduced by canvas-skill story (sprint-2026-05-03). Motivated by the need for a deterministic cycle boundary that the canvas timeline can compute without developer input.

---

**Decision 54 — Hono+HTMX+Bun Canvas Runtime Stack (DEC-019, 2026-05-03)**

Formalizes the runtime stack for the canvas dashboard. DEC-019 supersedes DEC-011 D2 (which proposed a Vite-based approach) in favor of a single-file Bun server with no compile step.

**Stack:**

| Component | Choice | Notes |
|---|---|---|
| HTTP framework | Hono | Minimal, TypeScript-native, edge-compatible |
| Frontend interaction | HTMX | Live fragment polling — no client-side JS framework |
| Runtime | Bun | `bun --hot server.tsx`; no compile step; TypeScript runs directly |
| Entry point | `skills/momentum/skills/canvas/server.tsx` | Single file; all routes and HTML fragments co-located |
| Port | 3456 | Fixed; not configurable in MVP |

**Supersedes:** DEC-011 D2 (Vite approach). Canvas serves HTML directly from the Bun process — no static asset pipeline, no build artifact, no hot-module-replacement complexity.

**HTMX navigation protocol:**

| Route type | HTMX response | Effect |
|---|---|---|
| Lens routes (L1 timeline, etc.) | Fragment HTML | `hx-swap="innerHTML"` on the container — replaces pane content |
| L2 feature detail | Full-page HTML | `hx-swap="innerHTML"` on `<body>` — replaces entire body |
| L3 story detail | Full-page HTML | `hx-swap="innerHTML"` on `<body>` — replaces entire body |
| Breadcrumb updates | `hx-swap-oob="true"` fragment | Out-of-band breadcrumb refresh alongside the primary response |

URL sync: all navigations use `hx-push-url` to keep the browser address bar in sync with the current view. Direct URL loads (browser refresh, link sharing) hit a full-page route and return a complete HTML document.

**Polarity model — dark/light view layers:**

| Layer | View | Background | CSS token |
|---|---|---|---|
| L1 | Timeline / cycle overview | Dark | `--paperDark: #16140f` |
| L2 | Feature detail | Warm light | `--readingPaper: #faf6ec` |
| L3 | Story detail | Warm light | `--readingPaper: #faf6ec` |

**Polarity transition:** The `.reading-mode` CSS class is added to `.pane-inner` when navigating from L1 (dark) to L2/L3 (warm light). The cross-fade is a 140ms CSS transition on the `background-color` and `color` properties. Navigating back to L1 removes `.reading-mode`, reversing the transition.

**Rationale:** Bun's `bun --hot` mode provides instant server reloads during development without a separate watcher process. HTMX's fragment-swap model keeps the server as the authoritative renderer with no client-side state synchronization. Single-file server keeps the canvas skill self-contained and reviewable without build tooling.

**Traceability:** Introduced by canvas-skill story (sprint-2026-05-03). Supersedes DEC-011 D2. Motivated by DEC-019 adoption decision (2026-04-26) to replace the static HTML approach of momentum:feature-status with a live, navigable dashboard.

**Naming convention note:** The implementation used a `momentum-cycle-*` story naming convention rather than the original `canvas-*` naming from early backlog stubs. All `momentum-cycle-*` stories are done. The old `canvas-*` backlog stubs were superseded by the `momentum-cycle-*` stories and will be dropped.

---

### Sprint 2026-05-16 Decisions

**Decision 55 — Agent Routing Table (DEC-023, sprint-2026-05-16)**

Formalizes the agent routing table schema and resolution algorithm for `momentum/agents.json`. Supersedes ad-hoc specialist selection in sprint-dev Phase 2.

**Schema:**

`momentum/agents.json` has two top-level blocks:

- **`defaults`** — 9 roles defined in the schema (dev, qa-reviewer, e2e-validator, architect-guard, ux, analyst, researcher, constitution-builder, agent-builder). **ARCH-3: Not all 9 are currently shipped. Roles actually shipped as base bodies: dev, qa-reviewer, e2e-validator, e2e-validator (method-polymorphic rewrite), ux, analyst, researcher. Roles still backlog (base body not yet shipped): architect-guard (pending `base-body-collapse-rollback` and `architecture-decision-26-update` stories), constitution-builder, agent-builder.** Each role entry specifies `agent_path` (relative to plugin `agents/`) and `write_permissions` (array of glob patterns the agent is authorized to write). Defaults are immutable at runtime — agent-builder never overwrites them.
- **`project`** — per-role×domain entries written by agent-builder. Each entry adds a domain-specific override (e.g., `dev/android`, `qa-reviewer/canvas`). Resolution prefers `project` entries over `defaults`.

**Resolution algorithm (`momentum-tools agent-resolve`):**

1. Accept `--role <role>` and `--touches <path,...>` (story `touches` array).
2. Glob-match each path in `touches` against `project` entries. Group matches by `slug` (role+domain).
3. If matches exist: return one agent path per result group (1..N fan-out). Multiple domains in one story → one agent spawned per matched group.
4. If no matches: fall back to `defaults.<role>`. For untyped stories, fall back to `defaults.dev`.
5. `write_permissions` from the matched entry are enforced by the orchestrator at spawn time — passed as `disallowedTools` overrides.

**Invariants:**
- Every skill spawning a typed role must use `momentum-tools agent-resolve` — no hardcoded agent paths in skill prompts.
- 1..N fan-out: multi-domain stories spawn one agent per result group (not one aggregate agent).
- `defaults` block is plugin-shipped and read-only at runtime.

**Resolver hardening (sprint-2026-06-02, conduct-core):** `momentum-tools agent-resolve` now (a) performs **dead-role cleanup** — role entries whose `agent_path` no longer points to a shipped base body are pruned/ignored rather than resolved to a missing file, and (b) applies **`Path.exists()` validation** on every resolved `agent_path` before returning it, hard-failing on a non-existent agent file instead of silently emitting an unspawnable path. This closes the failure mode where a stale routing entry resolved to a deleted agent definition.

**Traceability:** Introduced by agent-routing-table story (sprint-2026-05-16). Implements DEC-023. Consumed by sprint-dev Phase 2 and Phase 5 reviewer spawns, and by the conduct execution engine (Decision 59).

---

**Decision 56 — Agent Builder Three-Skill Pipeline (DEC-026 D3/D5, sprint-2026-05-16)**

Formalizes the two-tier build pipeline for project-specific agent definitions.

**Pipeline:**

| Tier | Skill | When | Output |
|---|---|---|---|
| Tier 1 | constitution-builder | Once per project | `constitution.md` — project identity, values, constraints, and domain glossary |
| Tier 2 | agent-builder × N | Once per role×domain | `.claude/guidelines/agents/{role}-{domain}.md` + routing entry in `momentum/agents.json` `project` block |

**Orchestration:** `build-agents` skill orchestrates both tiers. It runs constitution-builder first (blocking), then fans out agent-builder calls for each requested role×domain combination (parallel after Tier 1 completes).

**agent-builder inputs:**
- `base_body_path` — path to the plugin-shipped base agent body for this role (from `agents/{role}.md`)
- `constitution_excerpt` — relevant sections from `constitution.md` for this role's domain
- `manifesto` — the agent's **diagnostic table** (DEC-026 D4 / DEC-038): the stable, per-role×domain table mapping *observable developer symptoms → exact `wiki-query` KB lookups*, plus the stack facts that scope it. This is the manifesto in the canonical sense — see the DEC-026 D4 definition block below.
- `creed_anchors` — project-specific values, vocabulary, and behavioral anchors for the CREED block. **Distinct from the manifesto/diagnostic table.** The earlier single `manifesto_inputs` field ("project-specific values, vocabulary, and behavioral anchors for the CREED block") **conflated** the CREED behavioral anchors with the diagnostic table; per DEC-038 these are now separate inputs — `manifesto` is the diagnostic table, `creed_anchors` feeds the CREED block.

**agent-builder output:**
- `{role}-{domain}.md` at `.claude/guidelines/agents/` — the full agent definition merging base body + constitution excerpt + domain manifesto (diagnostic table) + CREED anchors
- A routing entry written to `momentum/agents.json` `project` block: `{ "role": "{role}", "domain": "{domain}", "touches": [...glob patterns...], "agent_path": ".claude/guidelines/agents/{role}-{domain}.md", "write_permissions": [...] }`

**Constraint:** agent-builder is the sole authorized writer to `momentum/agents.json` `project` block. constitution-builder writes only `constitution.md`. No other skill writes to either target.

**Manifesto — canonical definition (DEC-026 D4 / DEC-038, 2026-06-16):** the original Decision 56 covered DEC-026 D3 (constitution-builder) and D5 (agent-builder pipeline) but **omitted D4 — the manifesto definition**. DEC-038 ratifies one canonical definition, grounded in the recovered nornspun `cmp-dev` prototype:

> **The manifesto *is* the agent's diagnostic table** — a **stable**, per-role×domain table mapping *observable developer symptoms → the exact `wiki-query` KB lookup* for each, plus the **stack facts** that scope it. It is the agent's standing "how everything is implemented here" guidance.

Key clarifications:
- **Stable, not per-story.** The manifesto is the *same* across every sprint and every story. The earlier "sprint/story context overlay" reading (PRD FR136/FR138; see the annotation below) is **rejected** — the manifesto does not change per story.
- **Completeness criterion.** If an agent hits a situation the manifesto does not guide, the manifesto is **incomplete**. This is an acceptance criterion on the `agent-manifesto-format-specification` story.
- **Canonical term:** "diagnostic table."
- **Reference exemplar:** `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` (verbatim nornspun `cmp-dev.md`; ~35 worked symptom→`wiki-query` entries across 9 technology areas). The exemplar is a **format exemplar only** — never a Momentum agent (see project-scoped agents below).

**Routing ownership — per-agent, not shared constitution (DEC-038):** Decisions 55 and 56 did not state *where* per-agent routing is owned. It is now explicit: **agent-specific routing is owned at the manifesto / agent-builder layer (per-agent, per role×domain)** — it is the manifesto's diagnostic table — **not** the shared, project-wide constitution. The routing table (`momentum/agents.json`, Decision 55) still resolves *which agent* handles a story; *within* an agent, the symptom→`wiki-query` routing is the manifesto. This resolves an open design conflict: constitution-builder currently writes a project-**shared** `## Quick Routing` block, but a single shared Compose/Kotest routing table is **meaningless for a `pm` or `architect`** whose domain has different symptoms and KB pages. **Resolution:** symptom→`wiki-query` routing belongs in the **per-agent manifesto (diagnostic table)**, not the shared constitution; constitution-builder's `## Quick Routing` ownership must be reconciled to either (a) emit only genuinely project-universal routing and defer role-specific routing to the manifesto, or (b) be parameterized per write-mode/role. This reconciliation is tracked by stories `constitution-builder-write-mode-parameterization` and `constitutionmd-generation-acceptance-criteria` (DEC-038 Phase 1) — flagged here as the open design item it is until those stories land.

**wiki-query as the cold-KB interface, extended to multiple per-project KBs (DEC-018 / DEC-038):** the manifesto's diagnostic table is only useful against a real knowledge base. `wiki-query` is the **cold-KB interface** — the lookup mechanism a composed agent runs against an Obsidian KB to retrieve "how everything is implemented" knowledge on demand (cold context, fetched per-symptom, not preloaded). DEC-018 introduced `wiki-query` as that interface; **DEC-038 extends it to support multiple, per-project KBs.** A given symptom→`wiki-query` entry resolves against the KB of the agent's project.

**Project-scoped agents + multi-KB architecture (DEC-038 D2):** knowledge bases and agents are **project-scoped**:
- **Agents are project-scoped** — **nornspun agents ≠ Momentum agents.** `cmp-dev.md` and `nornspun-agentic-kb` are nornspun artifacts; `cmp-dev.md` is a format exemplar only, never a Momentum agent.
- **Momentum needs its own KB.** Each project keeps its own KB; **multiple KBs coexist.**
- **Consequence — KB-buildout is a distinct workstream.** "Build the agents" now also includes **standing up each project's KB** (a separate, sequenced workstream) plus a **multi-KB support requirement** on the `build-agents` pipeline and the `wiki-query` interface (DEC-018 extended). A manifesto's diagnostic table has value only against a real KB whose pages match its queries — Momentum's agents diagnose Momentum problems against Momentum knowledge, a separate KB from nornspun's.
- **Backlog stories:** `momentum-knowledge-base-buildout` (stand up the Momentum KB) and `manifesto-builder-skill-generate-then-curate` (the generate-then-curate manifesto authoring skill — auto-drafts diagnostic-table entries from the KB, then human-curates the expensive symptom-phrasing quality; see DEC-038 Gate G2).

**PRD FR136/FR138 annotation (DEC-038):** PRD FR136 ("Gen-2 Agent Composition Model") and FR138 ("`momentum:agent-builder` Pipeline") describe the manifesto as the **"project- or sprint-scoped context overlay (current story, sprint guidelines, project-specific rules)."** Per DEC-038 D1 this overlay reading is **superseded / rejected** — the manifesto is the agent's **stable diagnostic table** (symptom → `wiki-query`), the *same* across every sprint and story, **not** a per-sprint/per-story overlay. The three layers FR136 names remain correct (base body + constitution + manifesto); only the *manifesto's definition* is corrected. (Mirrors how other superseded descriptions are annotated in this document, e.g. the Subsystem 5 two-layer-model supersession note.)

**Traceability:** Introduced by agent-builder story (sprint-2026-05-16). Implements DEC-026 D3 (constitution-builder), D4 (manifesto = diagnostic table), and D5 (agent-builder pipeline). build-agents orchestrates both. **Manifesto definition, routing ownership, multi-KB / project-scoped agents, and the FR136/FR138 annotation added per DEC-038 (2026-06-16).**

---

**Decision 57 — Beads Dual-Write Adoption (DEC-028, sprint-2026-05-16)**

Formalizes the Beads tracker integration. The `beads-dual-write-spike` story is complete and the Beads infrastructure is **adopted**. `index.json` remains the authoritative source of truth; Beads is a best-effort secondary.

**Architecture:**

- **Authoritative source:** `.momentum/stories/index.json` and `.momentum/sprints/index.json` — unchanged.
- **Secondary write:** sprint-manager mirrors story status transitions to Beads as best-effort. If the Beads write fails, the primary index.json write succeeds and the error is logged but not surfaced as a blocking error.
- **Dependency source for sprint-dev Phase 1:** `bd ready --json --claim` is the **intended** primary dependency-ready source. **ARCH-4: The `dag-dispatcher-loop` story that wires this end-to-end is still backlog. Current state: the dual-write infrastructure is adopted, but `bd ready` as the live dependency source for sprint-dev Phase 1 is not yet wired end-to-end.** Falls back to `depends_on` fields in `stories/index.json` — this remains the actual primary source until the dag-dispatcher-loop story ships.
- **Session prime:** `bd prime --no-git-ops` runs via SessionStart hook to keep the local Beads DB in sync without triggering git operations.

**Storage:**
- `.beads/` — gitignored Dolt DB; the Beads local store. Never committed.
- `.momentum/beads-id-map.json` — git-tracked map of `story_slug → bead_hash_id`. Written by sprint-manager at each dual-write. Enables offline reconstruction of the slug↔ID mapping without querying Beads.

**Adoption status:** The `.beads/` directory, `.momentum/beads-id-map.json`, and `bd prime --no-git-ops` via SessionStart hook are **adopted infrastructure** — not experimental or provisional. The `beads-verification-with-sprint-data` story is a verification and hardening item; it is not a gate for adoption. **ARCH-4: `bd ready --json --claim` as the primary dependency source for sprint-dev Phase 1 is not yet wired end-to-end — the `dag-dispatcher-loop` story (which completes this wiring) is still backlog. The dual-write infrastructure is adopted; the sprint-dev dependency integration is in-progress/pending.**

**Gate criteria for full promotion (four gates):**

The four gates below govern the future decision to replace `index.json` dependency tracking with Beads as the primary source — a separate promotion step beyond the current adopted dual-write:

| Gate | Criteria |
|---|---|
| G1 — Round-trip fidelity | `bd ready --json --claim` returns the same story set as `depends_on` resolution from index.json for 3 consecutive sprints |
| G2 — Failure resilience | Beads write failures leave index.json in correct state and produce a recoverable error in beads-id-map.json without data loss |
| G3 — Session prime latency | `bd prime --no-git-ops` completes within 5 seconds on a warm local DB (P95 across 10 sessions) |
| G4 — Sprint-dev correctness | sprint-dev Phase 1 using `bd ready` produces no incorrect wave ordering vs. the index.json fallback path across 2 sprints |

Full promotion (Beads as primary dependency source) is deferred until all four gates pass.

**Traceability:** Introduced by beads-dual-write-spike story (sprint-2026-05-16). Implements DEC-028. Adopted sprint-2026-05-16.

---

**Decision 58 — verification-harness.json Validation Harness Profile (DEC-029 D3, sprint-2026-05-17)**

`momentum/verification-harness.json` is the plugin-shipped validation harness profile. It sits at the plugin root as a sibling to `momentum/agents.json` and uses the same two-block schema pattern:

```json
{
  "defaults": { ... },   // Plugin-shipped safe defaults — never overwritten by project tooling
  "project": [...]       // Per-project overrides — written by agent-builder or agent-guidelines
}
```

**`defaults` block:** Contains an `env` object (`startup`, `readiness_probe` keys), an `execution_surfaces` object keyed by change-type slug (10 surfaces: `"skill-instruction"`, `"agent-definition"`, `"rule-hook"`, `"script-code"`, `"script-cli"`, `"backend"`, `"app-ui"`, `"research-spike"`, `"specification"`, `"config-structure"` — full list in `momentum/verification-harness.json`), and a `contract_extensions` object mapping `verification_method` values to file extensions. All surface values default to `"skip"` — safe for projects with no running environment. Projects override via the `project` block.

**Driver-binding enum reconciliation (sprint-2026-06-02, conduct-core):** the `verification_method` keys in `contract_extensions` use the driver-binding vocabulary `skill-invoke | behavioral-trigger | bash | smoke | document-review | curl` (superseding the legacy `eval|trigger|smoke|review|gherkin|skip` keys). The contract extensions themselves are unchanged and accurate: `.eval.yaml`, `.trigger.md`, `.smoke.sh`, `.review.md`, `.feature`. The `verification_method` value is simultaneously the `harness_profile` and the verifier's dispatch key — method == harness_profile == driver-binding key.

**`project` block:** An array of override objects keyed by project context. Written by `momentum:agent-builder` (during agent customization for a project) and `momentum:agent-guidelines` (during guidelines generation). Neither skill overwrites the `defaults` block.

**Consumers:**
- `e2e-validator` — reads at startup to determine dispatch method per contract file extension
- `momentum:sprint-planning` — reads during Step 4 (contract generation) to determine which contract type to write per story `verification_method`

**Schema parallels `momentum/agents.json`:** defaults block is plugin-shipped and authoritative; project block is the per-project extension surface; neither consumer merges blocks — consumers check `project` entries first, fall back to `defaults`.

**Traceability:** Introduced by `momentum-harnessjson-schema-and-plugin-shipped-defaults` story (sprint-2026-05-17). Implements DEC-029 D3.

---

**Decision 59 — Conduct Execution Engine (DEC-035 / DEC-036 / DEC-037, sprint-2026-06-02)**

Conduct is Momentum's in-session sprint build orchestrator, adopted as the execution engine by DEC-035, calibrated for human-in-the-loop oversight by DEC-036, and given its invocation model by DEC-037. It is built on the in-session **dynamic Workflow** tool (Gas City deferred; beads decoupled — DEC-035 D2).

**Invocation model (DEC-037 D1):** Conduct ships as a **standalone `/momentum:conduct` skill that coexists with `/momentum:sprint-dev`**. A thin command invokes the existing `conductor` skill **as the top-level session**. Because it runs as the top-level session (not a spawned subagent), it legitimately owns commits, merges, and the approve-time `git push` — orchestrator-purity forbids only *spawned* skills from mutating git. `sprint-dev` remains the live builder, unchanged, during the transition; retiring sprint-dev's wave loop is a separate later **adoption** step (`conduct-adoption-retire-sprint-dev`), at which point spec §10/§12's "replace the build phase inside sprint-dev" is finally honored.

**Execution model (DEC-035 D1/D3/D4):** the Conductor runs each story through a **per-story pipeline** — dev → concurrent QA + `bmad-code-review` (via the `code-reviewer` adapter) → fix → self-merge — with a **Conductor-owns-git invariant**: spawned dev/reviewer subagents never touch git; the Conductor performs every worktree, merge, and push operation. On each merge it runs **AVFL-on-merge** as a dynamic Workflow over the merge-base diff, returning a typed `CLEAN | NON_CONVERGENT` verdict (distinct from sprint-dev's post-all-merge stop-gate — see Decision 31). After all stories land it runs **E2E validation**, then presents **exactly one human acceptance gate at the end**. The HITL plan-and-evaluate unit is a **finite-lived epic / complete feature** evaluated against its `acceptance_condition` — the arbitrary 2–8 story-count cap (DEC-030) is **removed**; the unit is whatever the feature requires. The auto-fix loop stays autonomous but is **legible**: the end-gate report renders both what the fixer **changed** and what it **dismissed** (with rationale), organized by user-facing functionality and divergences from plan (DEC-035 D5/D6, DEC-036 D3).

**Branch-base rule (sprint-2026-06-10, conductor seam-fix):** at story launch the Conductor creates `story/{slug}` from the **current tip of `sprint/{sprint-slug}`** — never `main`, never an inferred default branch — then adds the worktree `.worktrees/story-{slug}`, before the stage-1 dev spawn. Stale branches or worktrees from a prior interrupted run are handled idempotently: remove and recreate. Rationale: forking from the sprint tip keeps the merge-base review diff exactly story-scoped — the diff a reviewer sees contains the story's changes and nothing else. (See also the conduct-path note under Parallel Story Execution Model.)

**Stage-2 finding normalization — qa-reviewer adapter (sprint-2026-06-10, conductor seam-fix):** immediately after the QA reviewer returns, the Conductor deterministically maps producer-format qa-reviewer findings to the canonical finding schema (`finding-schema.md` v1.1) **before** merging them with code-review findings: verdict→severity (`BLOCKED`→`critical`, `MISSING`→`major`, `PARTIAL`→`minor`; severity is **never** derived from stakes), `type` from `stakes_class` (`security-auth-isolation`→`security`, else `spec-compliance`), fixed values `legitimate: true` / `source: "qa-reviewer"` / `suggested_fix: null`, and `story_slug` from pipeline context. This mirrors the existing code-reviewer (REVIEWER B) adapter — normalization is Conductor-side, so producer output formats stay clean.

**Coverage-deferral build-time semantics (sprint-2026-06-10, conductor seam-fix):** a `covered-by` coverage disposition (covered-by-composition) defers **only** the dedicated QA verification run to the named integration scenario. Adversarial code review still runs at build time on every story's per-story diff and is never deferred, demoted, or skipped by the disposition; stage-2 findings are never unconditionally bound empty by coverage routing. (See the `story_assignments` frozen-contract block in Sprint Tracking Schema for the disposition fields.)

**Build ledger — durable per-sprint record (sprint-2026-06-10, conductor seam-fix):** the Conductor is the **sole writer** of an append-only JSONL build ledger at `.momentum/sprints/{sprint-slug}/build-ledger.jsonl`. Rows are appended at event time — story launches, stage transitions, finding dispositions, escalations, quarantines, coverage deferrals/discharges, contract-integrity stops, and end-gate fixer events. Corrections are **append-only override rows, never edits**. The row vocabulary aligns with `finding-schema.md` v1.1 and `build-results-ledger-schema.md` v1.0 (companion schemas, joined on story slug).

**Ledger-sourced end-gate and resume (sprint-2026-06-10, conductor seam-fix):** the single end-gate and partial-run resume are **ledger-sourced**. Step 2.0 rehydrates all Conductor-scoped accumulators from the build ledger when one exists; Phase 5 assembles the end-gate report from ledger rows. In-context accumulators remain a write-through convenience — the ledger is authoritative at end-gate assembly. Durability property: an interrupted-then-resumed build produces the **same end-gate report** as an uninterrupted run.

**Stakes-and-timing HITL gate model (DEC-036 D1/D2/D4):** the single end-gate is **stakes-aware**, not a single undifferentiated altitude. HITL is gated only for three **stakes classes** — (1) security / auth-isolation, (2) irreversible / destructive (migration, delete, force-push, prod deploy), (3) high-blast-radius / architecture — with everything else falling through as **routine** (stays autonomous and collapses to a line). Two **timing tiers** route stakes findings: an **end-gate-expanded** default (stakes items become decision cards on the terminal gate) and a **narrow, high-bar mid-flight** tier reserved for irreversible-and-imminent or build-invalidating cases. Stakes-class `legitimate` findings leave the silent auto-fix path and are **raised** as decision cards (per-story + AVFL fixer schema carries a `stakes_class`); routine findings remain always-auto-fixed. An **anti-rubber-stamp forcing function** governs the end-gate: the Approve control loses its default check and, when stakes-class items are present, requires explicit per-card acknowledgment before Approve enables. This amends DEC-035's binding decision #1 (zero intermediate gates) narrowly and intent-preservingly — the anti-firehose intent (no routine asks, no per-finding prompts) is fully preserved; only safety-critical / irreversible / build-invalidating judgments are exempted from the single terminal gate.

**Presentation standard (DEC-036 D5):** the end-gate template and conduct's human-facing output follow the practice-wide **decision-grade presentation** rule (`references/rules/decision-grade-presentation.md`, Rules Architecture subsystem) — measurable caps govern verbosity, `effort` drives depth, and a self-sufficiency floor guarantees each decision carries its `what / why / evidence` inline.

**Carried forward (not decided here):** plan-gate legibility stays a separate, deferred epic (DEC-035 D7 / DEC-036 D6 — the canvas Reviewer surface and sprint-planning pre-sprint render gate already exist as backlog stories); Conductor context-budget handling is a build implementation detail (subagents do heavy work in their own contexts and return structured results; the report renders from a persisted data model). DEC-030 Gate 4 is validated in the first real conduct run (DEC-035 D8).

**Traceability:** Implements DEC-035 (Conduct Execution Engine), DEC-036 (HITL Calibration), DEC-037 (Standalone `/momentum:conduct`, coexisting with sprint-dev). Realized by the `sprint-2026-06-02-conduct-core` core build (`skills/momentum/skills/conductor/`). Branch-base rule, stage-2 qa-reviewer normalization, coverage-deferral build-time semantics, build ledger, and ledger-sourced end-gate/resume added by sprint-2026-06-10 (conductor seam-fix).
