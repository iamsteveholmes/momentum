# Eval: Phase 4 No Duplicate tool_use_id

## Scenario

Given Phase 4 of the retro workflow spawns its auditor team (1 documenter + 3 auditors),
the session transcript is inspected for the tool_use_id values associated with each spawned agent.

## Expected Behavior

Every spawned agent must have a distinct tool_use_id in the session transcript. No two agents
share a tool_use_id. Shared tool_use_id values would indicate that multiple agents were produced
from a single API call (single-call replication — the root cause of the historical defect).

## Verification

After Phase 4 completes, query the session JSONL for Phase 4 agent spawn tool calls:

```bash
# DuckDB query pattern (adjust session path):
# SELECT tool_use_id, COUNT(*) as cnt
# FROM session_events
# WHERE type = 'agent_spawn' AND phase = 4
# GROUP BY tool_use_id
# HAVING cnt > 1;
# Expected: zero rows (no shared tool_use_id)

# Or with jq against session transcript:
# jq '[.[] | select(.type=="tool_use" and .name=="Agent")] | group_by(.id) | map(select(length > 1))' session.jsonl
# Expected: empty array
```

## Pass Condition

Zero tool_use_id values appear more than once across the 4 Phase 4 agent spawns. Each of the
4 agents (documenter, auditor-human, auditor-execution, auditor-review) has a unique tool_use_id.

## Fail Condition

Any tool_use_id appears more than once — indicating that one API call produced multiple agent
instances (the replication defect observed in sprint-2026-04-08 and sprint-2026-04-10 retros,
where 8–10 documenters shared a tool_use_id).

## Rationale

AC1 and AC5 of `fix-retro-documenter-replication-defect`: "Distinct tool_use_id per spawned
agent in the session transcript (no two agents share a tool_use_id, ruling out single-call
replication)."
