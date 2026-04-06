---
eval: applies-changes-with-logging
behavior: Approved changes update epics.md and reassign stories via momentum-tools, with structured logging
---

# Eval: Applies Approved Changes With Full Logging

## Scenario

Given developer approval of two taxonomy changes:
1. Merge `agent-team-model` (5 stories) into `impetus-epic-orchestrator`
2. Create new registered epic `harden-epic-2-foundation` with a complete epic template filled out

The skill should:

1. Update `epics.md` with the new epic definition for `harden-epic-2-foundation` using the epic template format (slug, category, strategic intent, boundaries, FRs covered, NFRs covered, current state).
2. Call `momentum-tools sprint epic-membership --story <slug> --epic impetus-epic-orchestrator` for each of the 5 stories in `agent-team-model` (5 separate calls, one per story).
3. Call `momentum-tools log --agent epic-grooming --event decision --detail "..."` for each change, capturing old slug, new slug, and rationale in the detail.
4. After all changes are applied, present a final summary: N epics created/updated, M stories reassigned, orphan count before vs. after.

## Expected behavior

The skill makes deterministic, traceable mutations:
- `epics.md` contains the new epic template section for each created/updated epic
- Every story reassignment goes through `momentum-tools sprint epic-membership` (not direct file edits)
- Every decision is logged with structured detail including old_slug, new_slug, and rationale
- The final summary confirms the taxonomy is now clean (or lists any remaining orphans if some proposals were rejected)

The skill does NOT:
- Edit `stories/index.json` directly (epic-membership tool handles this)
- Skip logging for any approved change
- Apply rejected changes
