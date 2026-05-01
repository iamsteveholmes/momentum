---
title: "momentum:create-story — Optional Advanced Elicitation Step"
story_key: create-story-advanced-elicitation
status: backlog
epic_slug: story-cycles
depends_on: []
touches:
  - skills/momentum/skills/create-story/workflow.md
change_type: skill-instruction
derives_from:
  - path: docs/planning-artifacts/momentum-master-plan.md
    relationship: derives_from
    section: "Evaluation Flywheel"
---

# momentum:create-story — Optional Advanced Elicitation Step

## Story

As a Momentum developer creating a story,
I want an optional structured elicitation pass on my acceptance criteria and tasks after drafting,
so that spec gaps are caught before they become code defects — upstream of AVFL, not downstream.

## Description

Momentum's adversarial review (AVFL) fires after implementation. Specification gaps caught at that stage require a full validate-fix cycle. Finding the same gap during story creation costs one elicitation call.

`bmad-advanced-elicitation` pushes the LLM to challenge its own outputs using structured adversarial questioning — surfaces edge cases, unexamined assumptions, and completeness gaps in acceptance criteria before the story is handed to a dev agent.

This adds an optional Step 5.5 to the `momentum:create-story` workflow: after the initial draft, before the existing AVFL checkpoint. User-gated (opt-in) so the fast path is preserved.

Identified in the 2026-04-10 BMad 6.3.0 impact analysis session.

## Acceptance Criteria

### AC1: Optional elicitation step inserted post-draft
- After bmad-create-story completes and Momentum Implementation Guide is injected (Step 4), before AVFL checkpoint (Step 6), a new step asks: "Apply structured elicitation to acceptance criteria and tasks? (y/n)"
- Default is skip (n) — preserves the fast path
- If user confirms, elicitation is applied to the story's ACs and task list

### AC2: Elicitation targets ACs and tasks
- Elicitation focuses on: unstated assumptions, edge cases not covered by ACs, ambiguous task scope, and missing acceptance criteria for known failure modes
- Results are surfaced as suggested additions/clarifications to the story spec
- Developer reviews and applies changes before proceeding to AVFL checkpoint

### AC3: Enhanced spec feeds AVFL checkpoint unchanged
- The existing AVFL checkpoint (Step 6) is unchanged
- If elicitation was run, AVFL receives the enhanced spec
- If elicitation was skipped, AVFL receives the original spec
- No new AVFL profile or invocation changes needed

### AC4: Elicitation is logged in story Dev Notes
- If elicitation was run, a note is added to Dev Notes: "Advanced elicitation applied — N gaps identified, M accepted"
- If skipped, no note added

## Tasks / Subtasks

- [ ] Task 1 — Add elicitation opt-in step to create-story workflow (AC: 1)
  - [ ] Insert new step between Step 4 (Momentum Guide injection) and Step 6 (AVFL)
  - [ ] Prompt: "Apply structured elicitation? (y/n)" — default n
- [ ] Task 2 — Implement elicitation invocation (AC: 2)
  - [ ] If user confirms: invoke bmad-advanced-elicitation targeting ACs and tasks in {{story_file}}
  - [ ] Present findings to developer as suggested edits
  - [ ] Apply accepted suggestions to story file before continuing
- [ ] Task 3 — Thread result into Dev Notes (AC: 4)
  - [ ] After elicitation completes, append summary note to Dev Notes section of story file
- [ ] Task 4 — Verify AVFL checkpoint receives updated spec (AC: 3)
  - [ ] AVFL Step 6 reads {{story_file}} which now contains elicitation-enhanced content

## Dev Notes

### Implementation scope
Single file: `skills/momentum/skills/create-story/workflow.md`. Adds one conditional step between Steps 4 and 6. No changes to AVFL skill or bmad-create-story.

### Key decision
Opt-in by default. Developers working on simple, low-risk stories shouldn't pay elicitation overhead. Developers working on complex or high-ambiguity stories can opt in. This respects "Attention as a Finite Resource" — don't add friction to the default path.

### References
- [Source: session 2026-04-10] — bmad-advanced-elicitation fit analysis
- [Source: README.md#Evaluation Flywheel] — upstream fix economics

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
