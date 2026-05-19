# Eval: e2e-validator Reports BLOCKED When harness.json Is Absent

## Purpose

Verify that when `momentum/verification-harness.json` is absent from the project, the e2e-validator
agent reports BLOCKED and halts instead of proceeding with assumed stack defaults or
Gherkin-based validation.

## Expected Behavior

When `momentum/verification-harness.json` does not exist in the project root, the agent must:
1. Attempt to read the file
2. Detect its absence
3. Report `Verdict: BLOCKED` with a clear explanation that harness.json is required
4. Not proceed with any story contract execution

The agent must NOT fall back to Gherkin specs or any hardcoded defaults when the
harness file is absent.

## Inputs

### Setup condition

No `momentum/verification-harness.json` file exists in the project.

### Test story (placed at `.momentum/stories/test-story.md`)

```markdown
---
change_type: skill-instruction
---

## Acceptance Criteria

- AC1: When I invoke /momentum:impetus, the output includes a sprint summary
```

### Spawn prompt

```
Sprint: test-sprint-2026-01-01
Stories: [test-story.md]
AVFL findings: []
```

## Verification Steps

1. Observe that the agent attempts to read `momentum/verification-harness.json`
2. Observe that the agent detects the file is absent
3. Observe that the agent's validation report contains `Verdict: BLOCKED`
4. Observe that the report explains harness.json is missing
5. Confirm no story contracts were executed (no PASS/FAIL entries for any AC)

## Expected Pass Criteria

- Agent attempts to read `momentum/verification-harness.json`
- Agent reports `Verdict: BLOCKED` when the file is absent
- Report clearly states that `momentum/verification-harness.json` is required and was not found
- No story ACs are executed or marked PASS/FAIL/ERROR (only BLOCKED)

## Expected Fail Criteria

- Agent proceeds with validation despite missing harness.json
- Agent falls back to Gherkin `.feature` file lookup instead of halting
- Agent hardcodes finch/PostgreSQL/FastAPI startup commands and proceeds
- Agent reports a verdict other than BLOCKED (e.g., PASS or ERROR) without explaining the missing harness
