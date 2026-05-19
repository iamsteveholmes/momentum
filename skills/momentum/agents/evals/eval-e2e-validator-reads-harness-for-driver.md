# Eval: e2e-validator Reads harness.json to Determine Driver and Method

## Purpose

Verify that the e2e-validator agent reads `momentum/verification-harness.json` before executing any
validation, and uses the harness-defined driver binding and execution surface rather than
hard-coding any tool, runtime, or stack assumption.

## Expected Behavior

When spawned with a sprint slug, the agent must:
1. Read `momentum/verification-harness.json` before executing any story validation
2. Look up the `change_type` in `defaults.execution_surfaces` to get the surface name
3. Look up the surface name in `defaults.driver_bindings` to get the driver
4. Use that driver to execute the verification

The agent must NOT assume Gherkin files, finch, PostgreSQL, FastAPI, or any specific
stack unless declared in `harness.json`.

## Inputs

### Test harness.json (placed at `momentum/verification-harness.json`)

```json
{
  "defaults": {
    "env": {
      "startup": [],
      "readiness_probes": []
    },
    "execution_surfaces": {
      "skill-instruction": "skill-invoke",
      "agent-definition": "skill-invoke",
      "rule": "behavioral-trigger",
      "hook": "behavioral-trigger",
      "script": "bash",
      "cli": "bash",
      "backend": "bash",
      "app-ui": "smoke",
      "research": "document-review",
      "spike": "document-review"
    },
    "driver_bindings": {
      "skill-invoke": {
        "driver": "Skill",
        "description": "Invoke a skill directly in the agent context"
      },
      "behavioral-trigger": {
        "driver": "cmux",
        "description": "Trigger and observe rule/hook behavior via cmux terminal surface"
      },
      "bash": {
        "driver": "cmux",
        "description": "Execute scripts/CLI via cmux terminal surface"
      },
      "smoke": {
        "driver": "Maestro",
        "description": "UI smoke test via Maestro (mobile/web); falls back to Playwright for web-only targets",
        "fallback": "Playwright"
      },
      "document-review": {
        "driver": null,
        "description": "Human document review — no automated driver"
      }
    },
    "human_review_carveouts": ["research", "spike"],
    "trivial_smoke_escape": {
      "enabled": false,
      "change_types": []
    }
  },
  "project": []
}
```

### Test story (placed at `.momentum/stories/test-skill-story.md`)

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
Stories: [test-skill-story.md]
AVFL findings: []
```

## Verification Steps

1. Observe that the agent's first or second action reads `momentum/verification-harness.json`
2. Observe that the agent identifies `change_type: skill-instruction` → surface `skill-invoke` → driver `Skill`
3. Observe that the agent invokes the skill (or attempts to invoke it) using the Skill tool or cmux, NOT by reading the skill file and inspecting its contents
4. Observe that the report labels the method as `skill-invoke` or equivalent

## Expected Pass Criteria

- Agent reads `momentum/verification-harness.json` before executing any story contract
- Agent correctly maps `skill-instruction` → `skill-invoke` surface → `Skill` driver
- Agent does not open the skill's SKILL.md file and call it PASS based on file content
- Validation report includes `change_type: skill-instruction` and `method: skill-invoke` or similar

## Expected Fail Criteria

- Agent never reads `momentum/verification-harness.json`
- Agent invokes the skill by reading its SKILL.md and asserting strings found in the file
- Agent assumes Gherkin `.feature` files and reports BLOCKED because none exist
- Agent hardcodes finch, PostgreSQL, FastAPI, or any specific backend stack in its execution plan
