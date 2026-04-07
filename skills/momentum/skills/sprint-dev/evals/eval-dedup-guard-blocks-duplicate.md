# Eval: Deduplication Guard — Blocks Duplicate Spawn for Same (Story, Role)

## Setup

Sprint record has two stories: `story-alpha` (wave 1) and `story-beta` (wave 1).
Both are `ready-for-dev`. Sprint-dev Phase 1 initializes `{{spawn_registry}} = {}`.

Phase 2 runs and spawns agents for both stories:
- `story-alpha::dev-skills` → registered in spawn_registry
- `story-beta::dev-skills` → registered in spawn_registry

Phase 3 detects `story-alpha` completion and re-enters Phase 2 to check for
newly unblocked stories. The unblocked query mistakenly includes `story-beta`
again (simulating stale state or status lag).

## Expected Behavior — Duplicate Spawn Suppressed

When Phase 2 processes `story-beta` on re-entry:
1. The orchestrator computes key `story-beta::dev-skills`
2. The orchestrator finds that key in `{{spawn_registry}}`
3. The orchestrator does NOT spawn a second agent for `story-beta`
4. The orchestrator emits a log via `momentum-tools log` with:
   - `--event decision`
   - `--detail` containing "Dedup" and "story-beta::dev-skills"
5. Execution continues — the duplicate suppression does not stall the sprint

## Failure Condition

If a second agent is spawned for `story-beta::dev-skills` after it was already
registered in `{{spawn_registry}}`, the deduplication guard is not functioning.

## Verification

The workflow.md step n="2" must contain:
- A check against `{{spawn_registry}}` before the spawn action
- A log emission for suppressed duplicates
- Logic that continues (does not halt) when a duplicate is detected
