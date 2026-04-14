---
title: Triage Skill — Multi-Item Batch Classification and Routing
story_key: triage-skill
status: backlog
epic_slug: impetus-epic-orchestrator
depends_on: []
touches: []
---

# Triage Skill — Multi-Item Batch Classification and Routing

<!-- INTAKE STUB: This story was captured via the triage dog-food process on 2026-04-14,
     replacing the prior 4-line placeholder stub. It is a conversational stub, NOT a
     dev-ready story. All sections below marked DRAFT require full rewrite by
     create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer using Momentum,
I want a `momentum:triage` skill that processes multiple observations at once and routes each to the correct downstream (story stub, practice distillation, decision document, or durable-watch queue),
so that I can clear a session's backlog of half-formed ideas in one pass — without either losing them or prematurely committing each to a full story.

## Description

The `[3] Triage` menu item in Impetus has always been a placeholder. Two prior stubs existed — `triage-skill` (4 lines, no content) and `retro-triage-handoff` (pre-DEC-005 framing) — and both were invalidated by DEC-005 (2026-04-14), which reshaped the feature/epic/story model.

**The gap this story fills:** `momentum:intake` is single-item by design (one idea → one stub, no batching), but real-world triage is inherently multi-item. A retro produces N findings. A conversation surfaces M observations. An assessment yields K recommendations. None of this fits intake's one-at-a-time contract, so today those items either get force-fit into intake (creating premature story stubs) or are lost.

`momentum:triage` is the missing **orchestrator** that sits between upstream sources (conversation, retro output, assessment) and the per-item executors (`momentum:intake`, `momentum:distill`, `momentum:decision`). It:

1. **Enumerates** observations as a list.
2. **Classifies** each into one of six classes (ARTIFACT / DISTILL / DECISION / SHAPING / DEFER / REJECT). See the plan file for the class table and capture targets.
3. **Enriches** ARTIFACT items with `feature_slug` (DEC-005 D1), `story_type` (D5), suggested epic (D2 — DDD boundary-aware), priority, and proposed dependencies.
4. **Batch-approves** with the developer using the same UX pattern as `momentum:refine` Step 9.
5. **Executes** approved actions by delegating — spawns intake per ARTIFACT, distill per DISTILL, decision per DECISION. Writes `intake-queue.jsonl` (per DEC-007) inline via CLI for SHAPING/DEFER/REJECT.
6. **Reports** a summary of what was stubbed, distilled, flagged, deferred, rejected.

**Scope — prerequisite (fold-in per approved plan):** Before triage can delegate correctly, `momentum:intake` must be extended to capture `feature_slug` (DEC-005 D1) and `story_type` (D5). The stub-template and `momentum-tools sprint story-add` CLI need corresponding updates. This is part of Story A scope, not a separate story.

**DEC-005 alignment:**
- **D10** — triage performs NO value-floor gap-check. Classification only.
- **D1** — feature_slug mandatory on ARTIFACT items
- **D2** — epic boundary awareness (DDD sub-domains)
- **D5** — story_type (feature/maintenance/defect/exploration/practice)
- **D6** — terminal-state awareness for routing

**DEC-007 alignment:**
- SHAPING / DEFER / REJECT outcomes, plus retro→triage handoff items, land in a single unified `_bmad-output/implementation-artifacts/intake-queue.jsonl` event log. Schema uses `source` and `kind` discriminators.

**Agent topology:** Triage is an orchestrator skill (`claude-sonnet-4-6`, effort `high`, matches refine/sprint-planning). Impetus is the entry-point orchestrator that dispatches to triage. Classification is done inline in the main context — no subagent spawning for the judgment step. Optional Explore subagents (quick thoroughness) may be spawned for enrichment (duplicate detection, feature assignment suggestion) when scale warrants. Executor skills (`intake`/`distill`/`decision`) retain their existing model and effort settings.

**Impetus integration:** This story replaces the Impetus `[3] Triage` menu placeholder with a real dispatch. The greeting-state menus in PRD lines ~624–648 already reference "Triage" across 8 session states; their wording does not need to change, but the dispatch handler does.

**Pain context:** Today, observations captured mid-session either (a) go through intake one at a time (high friction for multi-item triage), (b) are verbally discussed and lost, or (c) are force-fit into the developer's working memory. The retro skill already generates multi-finding Priority Action Items that need downstream classification — currently that's also manual. Triage centralizes the pattern.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from the plan. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from the approved plan:

- Running `/momentum:triage` in a session prompts the developer for observations (or auto-extracts from recent conversation/retro output).
- Each observation is classified into exactly one of six classes: ARTIFACT, DISTILL, DECISION, SHAPING, DEFER, REJECT.
- For ARTIFACT items, triage captures `feature_slug` (suggested from `features.json`), `story_type` (default `feature`, heuristic-suggested), epic, priority, and proposed dependencies.
- Classification + enrichment is presented in a batch-approval UX (pattern from `momentum:refine` Step 9). Developer can accept, override, or re-classify per item before execution.
- On approval, triage delegates:
  - ARTIFACT → invokes `momentum:intake` per item (with enriched context passed in)
  - DISTILL → invokes `momentum:distill` per item
  - DECISION → invokes `momentum:decision` per item
  - SHAPING / DEFER / REJECT → writes an event to `_bmad-output/implementation-artifacts/intake-queue.jsonl` via a new `momentum-tools` CLI command (schema per DEC-007)
- At session start, triage reads `intake-queue.jsonl` and re-surfaces open SHAPING/DEFER items alongside new observations — enabling re-classification (promote / continue watching / reject / mark resolved).
- Triage writes NO story files or index entries directly for ARTIFACT/DISTILL/DECISION classes — those are delegated. Only `intake-queue.jsonl` is written directly.
- The Impetus `[3] Triage` menu placeholder is replaced with a real dispatch to `momentum:triage`.
- `momentum:intake` is extended to accept and persist `feature_slug` and `story_type`:
  - `intake/references/stub-template.md` gains both fields in frontmatter
  - `momentum-tools sprint story-add` gains `--feature-slug` and `--story-type` flags
  - `stories/index.json` entries written by intake carry both fields
- `skills/momentum/references/model-routing-guide.md` gains a `momentum:triage` row (model: `claude-sonnet-4-6`, effort: `high`).

> Note: The ACs above are rough captures. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. This section MUST be populated by
     create-story, which will break down the work based on architecture analysis and
     implementation guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. Run create-story to enrich with architecture analysis,
     implementation guide, technical requirements, and Momentum-specific guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

<!-- DRAFT: Architecture compliance has not been assessed for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

<!-- DRAFT: Testing requirements have not been defined for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

<!-- DRAFT: No implementation guide has been generated. Create-story will inject
     Momentum-specific guidance based on change-type classification. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

<!-- DRAFT: File paths, skill directories, and structural alignment have not been
     analyzed. Create-story will populate this based on the relevant epic and
     existing codebase structure. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

<!-- DRAFT: No references have been identified. Create-story will add source citations
     from architecture docs, PRD, and relevant code. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

Seed references (create-story will validate and expand):
- Plan: `/Users/steve/.claude/plans/curious-crunching-crystal.md`
- Decisions: DEC-005, DEC-007
- Existing patterns to reuse: `momentum:refine` Step 9 batch-approval UX; `momentum:retro` Phase 5 classification + routing; `momentum:intake` stub template and CLI path

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
