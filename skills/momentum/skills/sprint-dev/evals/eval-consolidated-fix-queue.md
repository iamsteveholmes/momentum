# Eval: Consolidated Fix Queue

**Behavior:** Phase 4c merges AVFL findings and per-story code review findings into a single prioritized queue, presents it to the developer for fix/defer decisions, and only spawns fix agents for confirmed items.

## Input

AVFL findings (from Phase 4):
- [CRITICAL] auth: broken import path in `src/auth/session.ts`
- [HIGH] api: missing error handler in `src/api/users.ts`
- [MEDIUM] api: naming inconsistency in `src/api/posts.ts`

Code review findings (from Phase 4b):
- `story-auth-refactor`: [HIGH] missing input sanitization in `src/auth/login.ts`
- `story-api-pagination`: [MEDIUM] n+1 query risk in `src/api/users.ts`
- `story-ui-loading-states`: [LOW] unused prop `className` in `src/components/Loader.tsx`

## Expected Behavior

1. **Unified queue presented**: All 6 findings (3 AVFL + 3 code review) are merged into a single list, sorted by severity: critical first, then high, then medium, then low.
2. **Source tagged**: Each item is tagged with its origin (AVFL or code-reviewer + story key) so re-review routing works correctly in Phase 4d.
3. **Developer fix/defer decision**: The workflow presents the queue and asks the developer to confirm which items to fix and which to defer. No automatic assumption — each item waits for explicit decision.
4. **Fix agents spawned only for confirmed items**: If developer defers [MEDIUM] api and [LOW] ui findings, fix agents are spawned ONLY for the 4 confirmed items, not all 6.
5. **Deferred items offered as follow-up stories**: Deferred findings are offered to the developer as follow-up backlog stories before proceeding.

## Anti-Patterns (Must Not Occur)

- Spawning fix agents for all 6 findings without developer confirmation
- Presenting AVFL and code review findings in separate lists without merging
- Losing source tags — needed for selective re-review in Phase 4d
- Spawning fix agents before the developer has confirmed/deferred each item
- Proceeding to Phase 4d with zero confirmed items without flagging to developer

## Verification

The eval passes if:
- A single merged queue of 6 items is presented (not two separate lists)
- Items are sorted by severity
- Developer is asked fix/defer for each item
- Fix agents spawned exactly for confirmed items (not deferred ones)
- Deferred items are offered as follow-up stories
