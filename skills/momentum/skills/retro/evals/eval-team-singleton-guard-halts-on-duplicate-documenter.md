# Eval: Team singleton guard halts Phase 4 when documenter is duplicated

## Scenario

Given a retro for `sprint-2026-04-08` where Phase 4 has called TeamCreate with team name
`retro-sprint-2026-04-08`, and the team config file at
`~/.claude/teams/retro-sprint-2026-04-08/config.json` exists and contains:

```json
{
  "members": [
    { "name": "documenter", "agentId": "a1", "agentType": "documenter" },
    { "name": "documenter", "agentId": "a2", "agentType": "documenter" },
    { "name": "documenter", "agentId": "a3", "agentType": "documenter" },
    { "name": "documenter", "agentId": "a4", "agentType": "documenter" },
    { "name": "documenter", "agentId": "a5", "agentType": "documenter" },
    { "name": "auditor-human", "agentId": "a6", "agentType": "auditor-human" },
    { "name": "auditor-execution", "agentId": "a7", "agentType": "auditor-execution" },
    { "name": "auditor-review", "agentId": "a8", "agentType": "auditor-review" }
  ]
}
```

(8 total members: 5 documenters + 3 auditors — the replication defect pattern observed in
sprint-2026-04-08.)

The singleton guard step runs immediately after the spawn block and before the wait loop.

## Expected Behavior

The retro orchestrator should:

1. Read `~/.claude/teams/retro-sprint-2026-04-08/config.json`.
2. Parse the `members` array and tally per-role counts:
   - documenter: 5
   - auditor-human: 1
   - auditor-execution: 1
   - auditor-review: 1
   - Total: 8
3. Detect that the tally does not match the expected composition (1 + 1 + 1 + 1 = 4 total).
4. Emit a diagnostic block that includes ALL of the following:
   - The sprint slug under retro (`sprint-2026-04-08`)
   - Expected composition: `1 documenter + 1 auditor-human + 1 auditor-execution + 1 auditor-review (4 total)`
   - Actual composition per role (e.g., `5 documenter, 1 auditor-human, 1 auditor-execution, 1 auditor-review (8 total)`)
   - The path to the team config file read (`~/.claude/teams/retro-sprint-2026-04-08/config.json`)
   - A reference to story slugs `retro-team-singleton-guard` and `fix-retro-documenter-replication-defect`
5. HALT Phase 4 — do NOT proceed to the `Wait for the team to complete` action.
6. NOT prompt the developer to "continue anyway" — there is no continue-with-known-bad-team path.
7. NOT write or await the findings document (`retro-transcript-audit.md`).

## What This Tests

- The guard runs before any auditor or documenter work begins
- Duplicate members (same role appearing multiple times) trigger a HALT
- The diagnostic output names the actual per-role counts, not just a total mismatch
- The HALT is unconditional — no "continue anyway" prompt
- The findings document is not written when the guard fires
