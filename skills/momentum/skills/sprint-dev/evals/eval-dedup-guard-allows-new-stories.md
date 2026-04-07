# Eval: Deduplication Guard — Allows Spawning for Newly Unblocked Stories

## Setup

Sprint record has three stories:
- `story-alpha` (wave 1, no deps) — already spawned in Phase 2 first pass
- `story-beta` (wave 1, no deps) — already spawned in Phase 2 first pass
- `story-gamma` (wave 2, depends_on: story-alpha) — not yet spawned

After Phase 2 first pass:
```
spawn_registry = {
  "story-alpha::dev-skills": { spawned: true },
  "story-beta::dev-skills": { spawned: true }
}
```

`story-alpha` completes and merges. Phase 3 detects newly unblocked `story-gamma`
and re-enters Phase 2.

## Expected Behavior — New Story Spawns Normally

When Phase 2 processes `story-gamma` on re-entry:
1. The orchestrator computes key `story-gamma::dev-skills`
2. The key is NOT in `{{spawn_registry}}` (never spawned before)
3. The orchestrator spawns the agent for `story-gamma` normally
4. The orchestrator registers `story-gamma::dev-skills` in `{{spawn_registry}}`
5. The spawn count for this re-entry pass = 1 (only the new story)

## Failure Condition

If the orchestrator refuses to spawn `story-gamma` due to an overly broad
dedup check, or if the registry incorrectly contains `story-gamma::dev-skills`
before it was spawned, the guard is broken.

## Verification

The workflow.md step n="2" dedup check must:
- Only skip spawn when the exact key `{slug}::{specialist}` exists in registry
- Allow spawning for keys that are absent from the registry
- Register the new key after spawning (not before)
- The spawn_registry survives Phase 2 → Phase 3 → Phase 2 loop intact
