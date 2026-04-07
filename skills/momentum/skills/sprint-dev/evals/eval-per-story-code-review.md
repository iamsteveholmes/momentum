# Eval: Per-Story Code Review

**Behavior:** Phase 4b spawns an independent `momentum:code-reviewer` for each merged story, scoped to that story's changeset. Reviews are independent — one reviewer per story, not a single sprint-level review.

## Input

Sprint has 3 merged stories:
- `story-auth-refactor` — touches: `src/auth/login.ts`, `src/auth/session.ts`
- `story-api-pagination` — touches: `src/api/users.ts`, `src/api/posts.ts`, `tests/api.spec.ts`
- `story-ui-loading-states` — touches: `src/components/Loader.tsx`, `src/components/Table.tsx`

AVFL findings have been acknowledged (Phase 4 complete). Phase 4b begins.

## Expected Behavior

1. **Three independent reviews spawned**: One `momentum:code-reviewer` invocation per story — 3 total. Not one review of the whole sprint.
2. **Scope isolation**: Each reviewer receives only the files in that story's `touches` array. The auth reviewer does not see API files; the API reviewer does not see UI files.
3. **Parallel execution**: All 3 reviews are spawned in a single parallel batch (single message, 3 agent invocations), not sequentially.
4. **Structured findings collected**: Each reviewer produces structured findings tagged with the story key they reviewed.
5. **Findings preserved for Phase 4c**: All findings from all 3 reviews are collected and passed to the consolidation phase.

## Anti-Patterns (Must Not Occur)

- Spawning a single code review for the entire sprint
- Spawning reviews sequentially (one at a time, waiting for each to complete before starting the next)
- Scoping a reviewer to files from a different story
- Dropping any story from review (all merged stories must be reviewed)
- Proceeding to Phase 4c before all 3 reviews complete

## Verification

The eval passes if:
- Exactly 3 code reviewer invocations are spawned (one per story)
- Each invocation is scoped to the correct story's files only
- All 3 are spawned in parallel
- Phase 4b does not complete until all 3 produce findings
