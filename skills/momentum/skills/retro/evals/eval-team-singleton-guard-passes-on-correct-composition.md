# Eval: Team singleton guard passes silently on correct team composition

## Scenario

Given a retro for `sprint-2026-04-20` where Phase 4 has used Shape A topology: TeamCreate
with cardinality=1 produced the documenter into team `retro-sprint-2026-04-20`, then 3
individual Agent spawns joined the same team (auditor-human, auditor-execution, auditor-review).
The team config file at `~/.claude/teams/retro-sprint-2026-04-20/config.json` exists and contains:

```json
{
  "members": [
    { "name": "documenter", "agentId": "b1", "agentType": "documenter" },
    { "name": "auditor-human", "agentId": "b2", "agentType": "auditor-human" },
    { "name": "auditor-execution", "agentId": "b3", "agentType": "auditor-execution" },
    { "name": "auditor-review", "agentId": "b4", "agentType": "auditor-review" }
  ]
}
```

(Exactly 4 members: 1 documenter + 1 auditor-human + 1 auditor-execution + 1 auditor-review —
the intended composition.)

The singleton guard step runs immediately after the spawn block and before the wait loop.

## Expected Behavior

The retro orchestrator should:

1. Read `~/.claude/teams/retro-sprint-2026-04-20/config.json`.
2. Parse the `members` array and tally per-role counts:
   - documenter: 1
   - auditor-human: 1
   - auditor-execution: 1
   - auditor-review: 1
   - Total: 4
3. Confirm the composition matches the required assertion: 4 total members, exactly 1 of each role.
4. Emit at most a single confirmation line (e.g., "Team composition verified: 1 documenter + 3 auditors") — no multi-line block, no developer prompt.
5. Advance to the existing `Wait for the team to complete` action with no behavioral change.
6. NOT halt, NOT emit a diagnostic block, NOT prompt the developer.
7. The existing wait loop, the findings-document presence check, and the auditor-team-failure halt
   path all remain in effect and are reached normally.

## What This Tests

- A correctly composed 4-member team produces no friction (silent pass or single line)
- Phase 4 continues to the wait loop unchanged
- The guard does not interfere with the existing wait loop and findings checks
- The four system prompts (auditor-human, auditor-execution, auditor-review, documenter) are
  executed as normal — the guard does not prevent agent work
- The findings document is written normally by the documenter
