---
lastEdited: '2026-05-25'


description: Registry of architectural and strategic decision records that capture the reasoning behind significant choices. Each decision links back to source research and forward to affected stories/architecture decisions.
---


# Decision Registry

Decisions captured here are **session-level strategic choices** — the bridge between research findings and backlog work. They answer: "research said X, we evaluated it, and decided Y because Z."

Architecture decisions 1-41 remain inline in `architecture.md`. This registry captures decisions that span multiple architecture concerns, emerge from research evaluations, or represent strategic direction changes that don't fit neatly into a single architecture decision slot.

## Decisions

| ID | Title | Date | Source Research | Status |
|----|-------|------|-----------------|--------|
| DEC-001 | [Three-Tier Agent Guidelines Architecture](dec-001-three-tier-agent-guidelines-2026-04-09.md) | 2026-04-09 | agent-guidelines-architecture-2026-04-09 | decided |
| DEC-002 | [Feature Visualization and Developer Orientation](dec-002-feature-visualization-and-orientation-2026-04-11.md) | 2026-04-11 | project-knowledge-visualization-ai-2026-04-11 | decided |
| DEC-003 | [Feature Status Artifact Design — HTML Report, Layout, Signals, and Rendering](dec-003-feature-status-artifact-design-2026-04-11.md) | 2026-04-11 | feature-status-visualization-2026-04-11 | decided |
| DEC-004 | [Feature Schema Value-First Redesign — value_analysis and system_context Required Fields](dec-004-feature-value-first-2026-04-11.md) | 2026-04-11 | AES-002 | decided |
| DEC-005 | [Momentum Cycle Redesign — Feature-First Practice, North Star Floors, Running-App Verification, and Failure as Diagnostic](dec-005-cycle-redesign-feature-first-practice-2026-04-14.md) | 2026-04-14 | adapting-agile-for-gen-ai-development-2026-04-13 | decided |
| DEC-006 | [Artifact Redesign for Dual-Audience Legibility — Story Template, Feature Dashboard, and Story-Level Dependency Graph](dec-006-artifact-redesign-dual-audience-2026-04-14.md) | 2026-04-14 | DEC-005 (developer-proposed follow-on) | decided |
| DEC-007 | [Triage Capture Artifact — Unified Intake-Queue JSONL Event Log](dec-007-triage-capture-artifact-2026-04-14.md) | 2026-04-14 | (developer-conversation) | decided |
| DEC-008 | [Composable Specialist Agents Architecture — Three-Tier Layout, KB Soft Stop, No-Fallback, SM Literacy](dec-008-composable-agents-architecture-2026-04-22.md) | 2026-04-22 | (developer-conversation) | decided |
| DEC-009 | [Practice Knowledge Base Vault — Orchestration Model, Isolation, Merge Strategy, Research Path](dec-009-kb-vault-orchestration-and-ingest-model-2026-04-22.md) | 2026-04-22 | (developer-conversation) | decided |
| DEC-010 | [Fixture-Based Regression Testing as Practice Primitive — Schema, Lifecycle, Skills, and Pruning](dec-010-fixture-based-regression-testing-2026-04-22.md) | 2026-04-22 | retro-microeval-loop-analysis-2026-04-21 | decided |
| DEC-011 | [Project Canvas Implementation Foundations — Canvas Rename, Vite Build, State Source Paths](dec-011-project-canvas-implementation-foundations-2026-04-24.md) | 2026-04-24 | (developer-conversation) | decided |
| DEC-012 | [Retire Per-Sprint State File](dec-012-retire-per-sprint-state-file-2026-04-30.md) | 2026-04-30 | (developer-conversation) | decided |
| DEC-013 | [Universal Agent Model — No Bucket Distinction, Ask Not Fallback, Sprint Planning as Type Discovery](dec-013-universal-agent-model-ask-not-fallback-2026-05-02.md) | 2026-05-02 | (developer-conversation) | decided |
| DEC-014 | [Composed Agent File Staleness — Discovery-Check Model, No Auto-Invalidation](dec-014-composed-file-staleness-discovery-check-2026-05-02.md) | 2026-05-02 | (developer-conversation) | decided |
| DEC-015 | [KB Cold-Context Delivery — Workflow Steps, Prescriptive Constitution Triggers, Skills Audit](dec-015-kb-cold-context-workflow-steps-constitution-audit-2026-05-02.md) | 2026-05-02 | (developer-conversation) | decided |
| DEC-016 | [Agent Taxonomy — Two-Tier Shipped/Customs Model](dec-016-agent-taxonomy-two-tier-shipped-customs-2026-05-03.md) | 2026-05-03 | (developer-conversation) | decided |
| DEC-017 | [Momentum Practice Cycle — Formal Step Sequence Definition](dec-017-momentum-cycle-step-sequence-definition-2026-05-03.md) | 2026-05-03 | (developer-conversation) | decided |
| DEC-018 | [Obsidian Wiki Skills Replace Planned KB Stories — wiki-query as Cold KB Interface](dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md) | 2026-05-03 | (developer-conversation) | decided |
| DEC-019 | [Momentum Canvas Runtime Stack — Hono+HTMX+Bun Supersedes DEC-011 Vite Approach](dec-019-hono-htmx-bun-canvas-runtime-stack-2026-05-03.md) | 2026-05-03 | (developer-conversation) | decided |
| DEC-020 | [Universal Agent Role Taxonomy — BMAD-Aligned Base Bodies](dec-020-universal-agent-role-taxonomy-2026-05-16.md) | 2026-05-16 | (developer-conversation) | decided |
| DEC-021 | [Document Ownership Map — Role-to-Document Pattern Registry](dec-021-document-ownership-map-2026-05-16.md) | 2026-05-16 | (developer-conversation) | decided |
| DEC-022 | [`momentum/` Pipeline Artifact Directory Structure](dec-022-momentum-pipeline-directory-structure-2026-05-16.md) | 2026-05-16 | (developer-conversation) | decided |
| DEC-023 | [Agent Routing Table — Machine-Readable Registry with 1..N Fan-Out](dec-023-agent-routing-table-2026-05-16.md) | 2026-05-16 | (developer-conversation) | decided |
| DEC-024 | [Read-Only Skill Constraint — Context:Fork Replaces Separate Role Bodies](dec-024-read-only-skill-constraint-context-fork-2026-05-16.md) | 2026-05-16 | (developer-conversation) | decided |
| DEC-025 | [Fixer Role Resolution — Document Owner + Fix Constraint, No dev-fixer Base Body](dec-025-fixer-role-resolution-document-owner-2026-05-16.md) | 2026-05-16 | (developer-conversation) | decided |
| DEC-026 | [Build Pipeline Redesign — build-agents, agent-builder, constitution-builder Rework](dec-026-build-pipeline-redesign-2026-05-16.md) | 2026-05-16 | (developer-conversation) | decided |
| DEC-027 | [Skill/Agent Development — Skill-Creator Pipeline + Change-Type Routing in Sprint-Dev](dec-027-skill-agent-development-skill-creator-pipeline-2026-05-16.md) | 2026-05-16 | (developer-conversation) | decided |
| DEC-028 | [Beads as Tracker/Dependency/Memory Substrate — Adoption Under Momentum via Dual-Write Spike](dec-028-beads-tracker-memory-substrate-adoption-2026-05-16.md) | 2026-05-16 | beads-vs-momentum-tracker-evaluation-2026-05-16 | decided |
| DEC-029 | [Method-Routed Acceptance Validation — Harness Profile, Per-Sprint E2E Coverage, and the Unified Validate-Fix Loop](dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md) | 2026-05-17 | (developer-conversation) | decided |
| DEC-030 | [Dependency-Driven Execution Model — DAG Dispatch, Closeable Value-Groupings, Frozen-Scope Sprints, and the Dual-Format Integrity Split](dec-030-dag-dispatch-frozen-sprints-dual-format-2026-05-17.md) | 2026-05-17 | (developer-conversation) | decided |
| DEC-031 | [Legibility-Before-Automation — Canvas Gate Surface, Pipeline Restructure, and Dispatcher Sequencing](dec-031-legibility-before-automation-canvas-gate-surface-2026-05-20.md) | 2026-05-20 | (developer-conversation) | decided |
| DEC-032 | [Gas City as Momentum's Dispatcher — Adoption Decision](dec-032-gas-city-dispatcher-adoption-2026-05-22.md) | 2026-05-22 | gas-town-dispatcher-2026-05-20 research corpus | decided |
| DEC-033 | [Practice-Ledger Event-Log Redesign](dec-033-practice-ledger-event-log-redesign-2026-05-25.md) | 2026-05-25 | AES-003 | decided |
