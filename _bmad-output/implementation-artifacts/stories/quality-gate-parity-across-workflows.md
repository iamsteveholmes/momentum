---
title: Quality Gate Parity Across Workflows — Align quick-fix Gates with sprint-dev, Remove Direct Dev Invocation
story_key: quality-gate-parity-across-workflows
status: review
epic_slug: quality-enforcement
depends_on: []
touches:
  - skills/momentum/skills/quick-fix/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/impetus/workflow.md
change_type: skill-instruction
---

# Quality Gate Parity Across Workflows — Align quick-fix Gates with sprint-dev, Remove Direct Dev Invocation

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

1. quick-fix adds an explicit code review step via momentum:code-reviewer in
   Phase 4, between the AVFL scan and team validation, presenting findings to
   the developer.
2. sprint-dev and quick-fix both apply these four gate types: pre-implementation
   AVFL checkpoint, post-merge AVFL scan, code review, and team validation.
   sprint-dev already has all four; quick-fix is missing code review (this story
   adds it).
3. momentum:dev is an internal sub-tool only — it is NOT a user-facing endpoint.
   The `/develop` menu item in Impetus is removed. Users who want to develop a
   single story use `/momentum:quick-fix` instead.
4. momentum:dev does NOT run its own quality gates. Gates are the responsibility
   of the calling workflow (sprint-dev or quick-fix). Dev is a pure executor:
   resolve story, create worktree, delegate to bmad-dev-story, propose merge.
5. The Impetus dispatch table and menu are updated to remove `/develop` and any
   menu item that routes to momentum:dev directly.
6. The PRD is updated with a new FR stating the quality gate parity requirement
   and that momentum:dev is not user-invocable.
7. Worktree cleanup in the calling workflow is deferred until all quality gates
   pass. The worktree must remain available for fix iterations during AVFL, code
   review, and team validation. Only after all gates pass (or the developer
   explicitly accepts remaining findings) is the worktree deleted.

## Dev Notes

### Current State — Quality Gate Comparison

| Gate                         | sprint-dev                                | quick-fix                              | dev                           |
|------------------------------|-------------------------------------------|----------------------------------------|-------------------------------|
| Pre-impl AVFL checkpoint     | Handled by sprint-planning (separate skill) | Phase 2 step 2f: checkpoint profile    | NONE                          |
| Post-merge AVFL scan         | Phase 4: checkpoint profile on full sprint diff | Phase 4 step 4a: scan profile on single story | NONE                  |
| Code review                  | Phase 4b: per-story momentum:code-reviewer | NONE (validators cover some of this)   | NONE                          |
| Team validation (E2E/QA)     | Phase 5: QA + E2E + Architect Guard, parallel | Phase 4 steps 4b-4d: TeamCreate with Dev + E2E/QA collaborative fix loop | NONE |
| Developer review gate        | Phase 6: Gherkin verification checklist   | Phase 1 + Phase 2: BLOCKING gates with cmux surfaces | NONE              |

### momentum:dev — Internal Sub-Tool Only

momentum:dev is a pure executor called by sprint-dev and quick-fix. It does NOT
run its own quality gates — gates are the calling workflow's responsibility. This
avoids double-gating (sprint-dev runs gates after dev finishes, so dev running
them too would be redundant).

This story removes the `/develop` menu item from Impetus and any direct user
invocation path. Users who want to develop a single story use
`/momentum:quick-fix` instead, which provides the full gate suite.

### What This Story Changes in Impetus

- Remove the `/develop` menu item from the Impetus dispatch table
- Remove any menu entry that routes to momentum:dev directly
- Update eval files that reference `/develop` dispatching to momentum:dev

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
momentum:dev has no equivalent — and doesn't need one, because dev is always
called through a parent workflow that handles checkpointing upstream.

### Orchestrator Purity

momentum:dev remains a pure executor — it resolves a story, creates a worktree,
delegates to bmad-dev-story, proposes merge, and emits a completion signal. No
quality gates are added to dev itself. Gates are the calling workflow's
responsibility (sprint-dev, quick-fix). This story adds code review to
quick-fix's Phase 4, not to dev.

### Requirements Coverage

- PRD: New FR needed — "All execution paths must apply equivalent quality gates"
- Architecture: Aligns with Decision 31 (AVFL at appropriate scope), Decision 34
  (team review), Decision 35 (code-reviewer as context:fork skill)
- Epic 3 (Automatic Quality Enforcement): Extends enforcement to cover the dev
  execution path that currently has no post-merge gates

## Tasks / Subtasks

- [x] Task 1 — Write behavioral eval (EDD: before workflow changes)
  - [x] Create `skills/momentum/skills/quick-fix/evals/eval-quickfix-code-review.md`
    — verifies code review runs in Phase 4 between AVFL scan and team validation

- [x] Task 2 — Add code review step to quick-fix workflow (AC: 1, 2, 7)
  - [x] Insert momentum:code-reviewer invocation in Phase 4 between AVFL scan
    and team creation
  - [x] Merge code review findings into the collaborative fix loop task list
  - [x] Ensure worktree remains alive through all gate iterations

- [x] Task 3 — Defer worktree cleanup in sprint-dev (AC: 7)
  - [x] Move worktree removal from Phase 3 (per-story merge) to after Phase 4d
    (fix agents complete) — worktrees must survive through AVFL, code review,
    and fix iterations so fix agents can work in the isolated story context
  - [x] Remove story branch deletion from Phase 3; move to after worktree removal
  - [x] Fix agents in Phase 4d should use the story worktree instead of working
    directly on the sprint branch

- [x] Task 4 — Remove /develop from Impetus (AC: 3, 5)
  - [x] Remove the /develop menu item from the Impetus dispatch table in
    `skills/momentum/skills/impetus/workflow.md` (was not present — confirmed)
  - [x] Remove any menu entry that routes to momentum:dev directly
  - [x] Update eval files that reference /develop dispatching to momentum:dev

- [x] Task 5 — Verify PRD already updated (AC: 6)
  - [x] Confirm FR95 (quality gate parity) already exists in prd.md
  - [x] Confirm FR53 already updated to state dev is internal-only
  - [x] No spec writes needed — already applied in spec impact step

- [x] Task 6 — Run eval and verify (AC: 1-7)
  - [x] Run eval via subagent
  - [x] Verify quick-fix Phase 4 now includes code review
  - [x] Verify sprint-dev worktrees survive through Phase 4d
  - [x] Verify /develop no longer appears in Impetus menu

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
- [x] 1 behavioral eval written (quick-fix code review)
- [x] EDD cycle ran — eval behavior confirmed
- [x] quick-fix/workflow.md updated with code review step
- [x] sprint-dev/workflow.md updated — worktree cleanup deferred to after Phase 4d
- [x] /develop menu item removed from impetus/workflow.md (was never present; impetus evals updated to assert absence)
- [x] PRD FR95 and FR53 update confirmed present

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

N/A

### Completion Notes List

- Wrote behavioral eval `eval-quickfix-code-review.md` before workflow changes (EDD order preserved)
- Added code review step 4a.1 to quick-fix Phase 4 between AVFL scan and team validation; `momentum:code-reviewer` scoped to story touches; findings merged into `{{all_findings}}` passed to Dev agent in collaborative fix loop
- Deferred quick-fix worktree cleanup from Phase 3 to Phase 4e (after collaborative fix loop completes)
- Added `{{pending_worktree_cleanup}}` list to sprint-dev Phase 1 initialization; Phase 3 populates it instead of removing worktrees immediately; Phase 4d fix agents prefer story worktrees from this list; cleanup runs at end of Phase 4d
- Updated sprint-dev `<team-composition>` Phase 4d role note to reflect worktree-based operation
- Updated sprint-dev Phase 0 task description to mention worktree cleanup
- Confirmed impetus/workflow.md and session-greeting.md never had `/develop` as a menu item; updated three stale impetus eval files (eval-2item-menu-returning-user-no-threads.md, eval-2item-menu-returning-user-open-threads.md, eval-2item-menu-natural-language-fallback.md) that described the old 2-item menu design — evals now assert that `/develop` does NOT appear and `momentum:dev` is not user-invocable
- Added `user-invocable: false` to `skills/momentum/skills/dev/SKILL.md` and updated its description to reflect pure executor role
- Confirmed FR95 and FR53 already present in prd.md — no spec writes needed

### File List

- skills/momentum/skills/quick-fix/evals/eval-quickfix-code-review.md (created)
- skills/momentum/skills/quick-fix/workflow.md (modified)
- skills/momentum/skills/sprint-dev/workflow.md (modified)
- skills/momentum/skills/impetus/evals/eval-2item-menu-returning-user-no-threads.md (modified)
- skills/momentum/skills/impetus/evals/eval-2item-menu-returning-user-open-threads.md (modified)
- skills/momentum/skills/impetus/evals/eval-2item-menu-natural-language-fallback.md (modified)
- skills/momentum/skills/dev/SKILL.md (modified)
