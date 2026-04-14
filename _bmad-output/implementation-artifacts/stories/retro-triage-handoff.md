---
title: Retro → Triage Handoff — Retro Findings Feed Planning via Unified Intake Queue
story_key: retro-triage-handoff
status: backlog
epic_slug: impetus-epic-orchestrator
depends_on: []
touches: []
---

# Retro → Triage Handoff — Retro Findings Feed Planning via Unified Intake Queue

<!-- INTAKE STUB: This story was captured via the triage dog-food process on 2026-04-14,
     rewriting the prior pre-DEC-005 stub. It is a conversational stub, NOT a dev-ready
     story. All sections below marked DRAFT require full rewrite by create-story before
     any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer closing a sprint,
I want the retro's un-actioned findings to flow automatically into the next sprint's planning — as structured entries in the unified `intake-queue.jsonl` — framed with feature-state transitions and failure-diagnosis per DEC-005,
so that retro-identified gaps, user-stated complaints, feature-state regressions, and diagnosed failures are surfaced as story candidates during planning without manual re-injection.

## Description

The sprint-04-10 planning session started without consuming the sprint-04-08 retro findings. The developer had to manually inject the three largest known gaps — Material 3 inconsistency, API stub status, iOS coverage — before planning could proceed. The retro and sprint-planning skills today share no automated state: planning's backlog-synthesis reads `stories/index.json` and accepts developer prompts, but does not read prior retro findings, cross-platform coverage gaps, or user-stated complaints.

This story closes that loop — but reframed per **DEC-005** and channeled through the artifact defined by **DEC-007**:

### DEC-005 reframing

The prior (pre-DEC-005) framing treated the handoff as a narrow "priority action items → planning candidates" pipeline with three explicit buckets: unaddressed prior-retro findings, cross-platform coverage gaps, user-stated complaints. DEC-005 reshapes this:

- **D8 — Retro as feature-state hygienist.** Retro is responsible for transitioning features through Done / Shelved / Abandoned / Rejected terminal states (D6). Handoff items now carry feature-state transition context — "feature X was asserted Done but retro observed Y behavior regressing it to Partial."
- **D7 — Failure as legitimate diagnostic category.** Retro categorizes failures (what was attempted, what didn't work, what was learned) alongside successes. Handoff items carry failure-diagnosed framing so planning can decide whether to retry, shelve, or rethink.
- **D1 / D5 — Feature-first, story-type-tagged.** Handoff items that imply new stories carry `feature_slug` and suggested `story_type`.
- **D10 — No gap-check at handoff.** The handoff does not itself perform value-floor analysis; it carries context so downstream consumers (triage, sprint-planning) can evaluate.

### DEC-007 alignment

Retro writes handoff items as events to the unified `_bmad-output/implementation-artifacts/intake-queue.jsonl` with `source: "retro"` and `kind: "handoff"`. This replaces the previously-proposed `retro-summary.json` and the separate `triage-inbox.md` contract — both are retired. A single artifact, one schema, one reader path. Sprint-planning Step 1 (backlog synthesis) gains a read path on the same artifact. Triage also reads the queue on session start, re-surfacing open handoff items alongside new observations.

**Pain context:** HF-01 (2026-04-11T05:31) and HF-03 (2026-04-11T05:36) captured the user manually injecting retro-surfaced gaps into the sprint-04-10 planning conversation because the automated path did not exist. The sprint-04-06 (D3) retro surfaced M3 inconsistency as a major user-visible problem; sprint-04-08 retro ran 2026-04-10; sprint-04-10 planning ran the same day; findings did not carry across. This story closes that gap at the artifact and workflow level — not at the per-sprint level.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Retro Phase 5 (or successor phase) writes handoff items as JSONL events to `_bmad-output/implementation-artifacts/intake-queue.jsonl` with `source: "retro"` and `kind: "handoff"`.
- Each handoff event includes (schema to be finalized per DEC-007 in Story A):
  - title, description
  - retro sprint slug (provenance)
  - feature-state transition context (per DEC-005 D8) when applicable — e.g., `{"feature_slug": "...", "prior_state": "...", "observed_state": "...", "evidence": "..."}`
  - failure-diagnosis framing (per DEC-005 D7) when applicable — e.g., `{"attempted": "...", "didn't_work": "...", "learned": "..."}`
  - suggested `feature_slug` (per D1) and suggested `story_type` (per D5) when the handoff implies new work
  - open / consumed flag (so triage/planning can skip items already actioned)
- Sprint-planning Step 1 (backlog synthesis) reads the queue filtered to `source: "retro"`, `kind: "handoff"`, `status: open` — and surfaces items as candidates before the developer begins selecting stories.
- Triage at session start reads open handoff items alongside SHAPING/DEFER entries and lets the developer classify them (promote to ARTIFACT → intake, DISTILL, DECISION, continue watching, reject).
- When a handoff item is consumed (promoted to a story, distilled, decided, or explicitly rejected), its entry is updated (e.g., status flipped to consumed, with outcome reference).
- The legacy `triage-inbox.md` contract in architecture.md is retired and cross-referenced to DEC-007 and this story.
- No manual injection of retro findings into sprint-planning is required for the golden path.

> Note: The ACs above are rough captures from conversation. They are starting points only. Create-story will replace them with validated, testable acceptance criteria.

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
- Decisions: DEC-005 (D6, D7, D8, D10 — retro's feature-state hygienist role, failure-as-diagnostic, terminal states, gap-check placement), DEC-007 (unified intake-queue.jsonl)
- Depends on Story A (`triage-skill`): the `intake-queue.jsonl` schema, CLI write path, and triage read path are defined by Story A; this story extends them with the `source: "retro"`, `kind: "handoff"` producer side.
- Superseded artifact: `triage-inbox.md` contract in `architecture.md` lines ~1671–1698 — retired per DEC-007.

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
