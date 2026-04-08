---
title: Quality Gate Parity Across Workflows — Ensure sprint-dev, quick-fix, and dev Apply Equivalent Gates
story_key: quality-gate-parity-across-workflows
status: ready-for-dev
epic_slug: quality-enforcement
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/quick-fix/workflow.md
  - skills/momentum/skills/dev/workflow.md
change_type: skill-instruction
---

# Quality Gate Parity Across Workflows — Ensure sprint-dev, quick-fix, and dev Apply Equivalent Gates

## User Story

As a developer using Momentum, I want all three execution paths (sprint-dev,
quick-fix, dev) to apply equivalent quality gates so that code quality does not
depend on which workflow I happened to use.

## Description

Retro finding from sprint-2026-04-06-2: sprint-dev, quick-fix, and direct dev
workflows each have different quality gate implementations. Some paths skip AVFL,
code review, or team review entirely. The momentum:dev workflow in particular
has no post-merge validation at all — it delegates to bmad-dev-story, proposes
a merge, and exits. A developer using momentum:dev directly gets significantly
less quality assurance than one running the same story through sprint-dev.

This story standardizes what quality gates fire across all three execution paths,
ensuring every path applies: (1) pre-implementation AVFL checkpoint on the plan,
(2) post-merge AVFL scan on the integrated code, (3) code review, and
(4) team validation (E2E/QA based on change_type). The gates may differ in
profile or scope (sprint-dev validates the full sprint changeset; quick-fix and
dev validate a single story), but every path must include all four gate types.

A new FR should be added to the PRD: "All execution paths (sprint, quick-fix,
dev) must apply equivalent quality gates: pre-implementation AVFL checkpoint,
post-merge AVFL scan, code review, and team validation."

## Acceptance Criteria (Plain English)

1. momentum:dev runs a post-merge AVFL scan (profile: checkpoint, stage: final)
   after the story branch merges to the target branch, before emitting the
   completion signal.
2. momentum:dev runs a code review via momentum:code-reviewer scoped to the
   story's touches array after merge, presenting findings to the developer.
3. momentum:dev runs change_type-based team validation after AVFL and code
   review: E2E Validator for skill-instruction, QA for script-code, both when
   both types are present.
4. momentum:dev reads the story's change_type field from the story file
   frontmatter to determine which validators to spawn.
5. All three workflows (sprint-dev, quick-fix, dev) apply these four gate types:
   pre-implementation AVFL checkpoint, post-merge AVFL scan, code review, and
   team validation — though profiles and scope may differ by workflow.
6. The PRD is updated with a new FR stating the quality gate parity requirement.
7. Gate failures in momentum:dev are presented to the developer with fix/defer/
   accept options, matching the UX pattern used by quick-fix Phase 4.
8. Worktree cleanup is deferred until all quality gates pass. The worktree must
   remain available for fix iterations during AVFL, code review, and team
   validation. Only after all gates pass (or the developer explicitly accepts
   remaining findings) is the worktree deleted.

## Dev Notes

### Current State — Quality Gate Comparison

| Gate                         | sprint-dev                                | quick-fix                              | dev                           |
|------------------------------|-------------------------------------------|----------------------------------------|-------------------------------|
| Pre-impl AVFL checkpoint     | Handled by sprint-planning (separate skill) | Phase 2 step 2f: checkpoint profile    | NONE                          |
| Post-merge AVFL scan         | Phase 4: checkpoint profile on full sprint diff | Phase 4 step 4a: scan profile on single story | NONE                  |
| Code review                  | Phase 4b: per-story momentum:code-reviewer | NONE (validators cover some of this)   | NONE                          |
| Team validation (E2E/QA)     | Phase 5: QA + E2E + Architect Guard, parallel | Phase 4 steps 4b-4d: TeamCreate with Dev + E2E/QA collaborative fix loop | NONE |
| Developer review gate        | Phase 6: Gherkin verification checklist   | Phase 1 + Phase 2: BLOCKING gates with cmux surfaces | NONE              |

### Key Gaps in momentum:dev

The momentum:dev workflow (workflow.md) currently:
1. Resolves a story from stories/index.json or an explicit path
2. Creates a worktree and enters it
3. Delegates ALL implementation to bmad-dev-story
4. Proposes merge and cleans up worktree
5. Emits a structured completion signal

It has zero post-merge quality gates. After bmad-dev-story completes and the
story merges, the workflow is done. No AVFL scan, no code review, no team
validation.

### What This Story Changes in momentum:dev

**Worktree lifecycle change:** Currently the worktree is cleaned up at Step 4
(after merge). This must move to after all quality gates pass — the worktree
stays alive for fix iterations during AVFL, code review, and team validation.
Cleanup becomes the final step before the completion signal.

Add three new steps between the current Step 7 (merge) and the completion signal:

**Step 8: Post-merge AVFL scan**
- Invoke momentum:avfl with profile: checkpoint, stage: final
- Scope: files in the story's touches array
- Source material: story acceptance criteria
- If critical findings: present to developer with fix/defer/accept options
- If developer chooses fix: spawn a targeted fix agent on the target branch (no worktree)

**Step 9: Code review**
- Invoke momentum:code-reviewer scoped to the story's touches
- Present findings to developer
- Findings merge into the same fix queue as AVFL findings

**Step 10: Team validation**
- Read change_type from story frontmatter
- skill-instruction -> spawn E2E Validator (agent: skills/momentum/agents/e2e-validator.md)
- script-code -> spawn QA (agent: skills/momentum/agents/qa-reviewer.md)
- Both present -> spawn both
- Present findings with fix/defer/accept options
- If fix: spawn dev fix agent, re-run only affected validators

### What This Story Changes in quick-fix

Add an explicit code review step in Phase 4 between the AVFL scan and team
validation:

**Phase 4, new step after 4a (AVFL scan), before 4b (team creation):**
- Invoke momentum:code-reviewer scoped to the story's touches
- Present findings alongside AVFL findings
- Merge code review findings into the team's task list so the Dev agent can
  address them in the collaborative fix loop

### What Does NOT Change in sprint-dev

sprint-dev already has all four gate types. No changes needed. It serves as the
reference implementation.

### Pre-implementation AVFL Checkpoint

sprint-dev gets its pre-implementation checkpoint from sprint-planning (a
separate upstream skill). quick-fix includes it inline in Phase 2 step 2f.
momentum:dev currently has no equivalent.

For this story, the pre-implementation checkpoint in dev is NOT added because
dev receives stories that are already `ready-for-dev` — meaning they were
already checkpointed during sprint-planning or create-story. Adding a redundant
checkpoint would slow the workflow without adding value. The parity requirement
covers the three post-implementation gates.

If a story reaches dev without having gone through sprint-planning (e.g., a
manually created story file), the post-merge gates will catch plan-level issues
anyway. This is an acceptable trade-off.

### Orchestrator Purity

momentum:dev is a pure executor — it orchestrates but does not write files
directly. The new steps follow this principle: AVFL, code-reviewer, and
validators are all spawned as subagents or skill invocations. The dev workflow
only routes, presents findings, and waits for developer decisions.

### Requirements Coverage

- PRD: New FR needed — "All execution paths must apply equivalent quality gates"
- Architecture: Aligns with Decision 31 (AVFL at appropriate scope), Decision 34
  (team review), Decision 35 (code-reviewer as context:fork skill)
- Epic 3 (Automatic Quality Enforcement): Extends enforcement to cover the dev
  execution path that currently has no post-merge gates

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before workflow changes)
  - [ ] Create `skills/momentum/skills/dev/evals/eval-dev-post-merge-avfl.md`
    — verifies AVFL runs after merge before completion signal
  - [ ] Create `skills/momentum/skills/dev/evals/eval-dev-code-review.md`
    — verifies code review runs after merge with findings presented
  - [ ] Create `skills/momentum/skills/dev/evals/eval-dev-team-validation.md`
    — verifies team validators run based on change_type

- [ ] Task 2 — Update momentum:dev workflow with post-merge gates (ACs 1-4, 7)
  - [ ] Add Step 8: Post-merge AVFL scan (profile: checkpoint, stage: final)
  - [ ] Add Step 9: Code review via momentum:code-reviewer
  - [ ] Add Step 10: Team validation based on change_type
  - [ ] Add developer fix/defer/accept UX for gate findings
  - [ ] Move completion signal emission to after all gates pass

- [ ] Task 3 — Add code review step to quick-fix workflow (AC 5)
  - [ ] Insert momentum:code-reviewer invocation in Phase 4 between AVFL scan
    and team creation
  - [ ] Merge code review findings into the collaborative fix loop task list

- [ ] Task 4 — Update PRD with quality gate parity FR (AC 6)
  - [ ] Add new FR under the Sprint Execution section: "All execution paths
    (sprint, quick-fix, dev) must apply equivalent quality gates"

- [ ] Task 5 — Run evals and verify gate parity (AC 5)
  - [ ] Run each eval via subagent
  - [ ] Manually verify: invoke momentum:dev on a test story, confirm AVFL,
    code review, and team validation all fire
  - [ ] Verify quick-fix Phase 4 now includes code review

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 -> skill-instruction (EDD)
- Tasks 2, 3 -> skill-instruction (EDD)
- Task 4 -> docs (spec update via subagent)
- Task 5 -> skill-instruction (EDD verification)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before writing a single line of the workflow:**
1. Write 3 behavioral evals in `skills/momentum/skills/dev/evals/`:
   - One per eval above, testing AVFL, code review, and team validation
   - Format: "Given [input/context], the skill should [observable behavior]"

**Then implement:**
2. Update dev/workflow.md with Steps 8-10
3. Update quick-fix/workflow.md with code review step

**Then verify:**
4. Run evals via subagent, confirm behaviors match

**NFR compliance:**
- workflow.md changes must preserve orchestrator purity (no direct file writes)
- New steps must follow existing XML structure patterns
- AVFL/code-reviewer/validator invocations must match parameter patterns from sprint-dev

**DoD items for skill-instruction tasks:**
- [ ] 3 behavioral evals written
- [ ] EDD cycle ran — all eval behaviors confirmed
- [ ] dev/workflow.md updated with 3 new gate steps
- [ ] quick-fix/workflow.md updated with code review step
- [ ] Gate findings UX matches quick-fix Phase 4 pattern

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
