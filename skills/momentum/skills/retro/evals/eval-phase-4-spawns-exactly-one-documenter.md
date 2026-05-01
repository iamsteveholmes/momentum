# Eval: Phase 4 Spawns Exactly One Documenter

## Scenario

Given a retro run that has reached Phase 4 with prepared audit-extracts available at
`.momentum/sprints/sprint-2026-04-10/audit-extracts/`, the orchestrator (the retro skill itself)
executes the Phase 4 spawn step.

## Expected Behavior

The skill should spawn exactly 4 agents total in Phase 4:
- 1 documenter (singleton coordinator)
- 1 auditor-human
- 1 auditor-execution
- 1 auditor-review

No agent role should appear more than once. The documenter is never multiplexed.

## Verification

After Phase 4 completes:
1. Count agents spawned during Phase 4 — must be exactly 4.
2. Count documenter agents specifically — must be exactly 1.
3. Count each auditor type — must be exactly 1 of each (auditor-human, auditor-execution, auditor-review).
4. Each spawned agent has a distinct tool_use_id (no replication from a single API call).

## Pass Condition

Agent counts: total=4, documenter=1, auditor-human=1, auditor-execution=1, auditor-review=1.

## Fail Condition

Any count other than the above — especially documenter > 1 (historical failure: 8–10 documenters
per run against sprint-2026-04-08 and sprint-2026-04-10 audit-extracts).

## Rationale

AC1 and AC4 of `fix-retro-documenter-replication-defect` and AC4 of `retro-workflow-rewrite`:
"Retro spawns an auditor team with 3 specialized roles (human, execution, review) plus 1
documenter, all communicating via SendMessage."
