---
title: "AVFL Phase 4c — Structured Human Review via bmad-checkpoint-preview"
story_key: avfl-checkpoint-preview-integration
status: backlog
epic_slug: story-cycles
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
change_type: skill-instruction
derives_from:
  - path: docs/planning-artifacts/momentum-master-plan.md
    relationship: derives_from
    section: "Attention as a Finite Resource"
---

# AVFL Phase 4c — Structured Human Review via bmad-checkpoint-preview

## Story

As a Momentum developer completing a sprint,
I want a guided human review checkpoint before committing to fix/defer decisions on AVFL findings,
so that I review findings with intent-first context rather than rubber-stamping a raw list under cognitive load.

## Description

Momentum's AVFL produces consolidated findings at Phase 4c. Currently the developer receives a list and makes fix/defer decisions without structure. This creates review debt — the 39-point perception gap means developers cannot self-assess when they're rubber-stamping vs genuinely reviewing.

`bmad-checkpoint-preview` (new in BMad 6.3.0) walks the developer through a change from purpose and context into details. Integrated at Phase 4c it converts the unguided findings list into a structured walkthrough that links each finding back to its spec/story AC and halts if referenced specs are missing.

Identified in the 2026-04-10 BMad 6.3.0 impact analysis session.

## Acceptance Criteria

### AC1: checkpoint-preview invoked at Phase 4c
- After AVFL and code-reviewer findings are merged, before the developer makes fix/defer decisions, `bmad-checkpoint-preview` is invoked
- Input: merged findings set grouped by story and severity
- checkpoint-preview walks through findings in intent-first order (purpose → context → details)

### AC2: Each finding links to its spec/AC
- Each finding in the walkthrough displays the spec path and AC number it references
- If a referenced spec file is missing, the walkthrough halts with a remediation instruction before continuing

### AC3: Structured fix/defer output
- checkpoint-preview exits with a structured fix/defer decision registry (keyed by finding ID)
- This registry is passed to Phase 4d (fix spawning) rather than requiring the developer to track decisions manually

### AC4: Flagship model routing
- checkpoint-preview is invoked with Opus (flagship) since it is a developer decision gate, not advisory
- This is declared in the sprint-dev workflow step, not left to default routing

## Tasks / Subtasks

- [ ] Task 1 — Add checkpoint-preview invocation to sprint-dev Phase 4c (AC: 1, 4)
  - [ ] Locate Phase 4c in sprint-dev/workflow.md
  - [ ] Insert checkpoint-preview step before fix/defer decision prompt
  - [ ] Pass merged findings as structured input; specify Opus routing
- [ ] Task 2 — Wire spec-link and halt behavior (AC: 2)
  - [ ] Confirm checkpoint-preview's missing-spec halt is surfaced to developer
  - [ ] Document remediation instruction (create missing spec file, then resume)
- [ ] Task 3 — Thread fix/defer registry to Phase 4d (AC: 3)
  - [ ] Capture checkpoint-preview output as structured registry
  - [ ] Pass registry to Phase 4d fix-spawning step as input
- [ ] Task 4 — Verify no regression in AVFL clean-pass path (AC: 1)
  - [ ] When AVFL is CLEAN (no findings), checkpoint-preview step is skipped

## Dev Notes

### Implementation scope
Single file: `skills/momentum/skills/sprint-dev/workflow.md`. No new skills — `bmad-checkpoint-preview` is an existing BMad 6.3.0 skill invoked as a delegation target.

### Key decision
checkpoint-preview is marked as high-effort/flagship in this invocation because it is a human decision gate. Phase 4c is where fix/defer decisions are made — these decisions drive rework cost. This is not advisory.

### References
- [Source: _bmad-output/planning-artifacts/README.md] — "Attention as a Finite Resource" principle
- [Source: session 2026-04-10] — bmad-checkpoint-preview fit analysis

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
