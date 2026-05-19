# Eval: e2e-validator Uses Document Review for research-spike change_type

## Purpose

Verify that the e2e-validator agent correctly routes `research-spike` stories to the
document-review method (a human_review_carveout), reading the artifact and verifying
ACs by inspection rather than attempting to execute commands or run tools.

## Expected Behavior

When a story has `change_type: research-spike`, the agent must:
1. Identify the story as a human_review_carveout
2. Read the research artifact referenced in the story ACs
3. Verify each AC by document inspection
4. Report each AC as VERIFIED, PARTIAL, or MISSING based on document content
5. NOT attempt to run Bash commands, invoke skills, or trigger behavioral tests

Document-review results must NOT affect the overall verdict (PASS/FAIL) — they are
reported separately as human follow-up.

## Inputs

### Test harness.json (placed at `momentum/harness.json`)

```json
{
  "defaults": {
    "env": { "startup": [], "readiness_probes": [] },
    "execution_surfaces": {
      "skill-instruction": "skill-invoke",
      "agent-definition": "skill-invoke",
      "rule": "behavioral-trigger",
      "research-spike": "document-review",
      "specification": "document-review"
    },
    "driver_bindings": {
      "skill-invoke": { "driver": "Skill", "description": "Invoke a skill directly" },
      "document-review": { "driver": null, "description": "Human document review — no automated driver" }
    },
    "human_review_carveouts": ["research-spike", "specification"],
    "trivial_smoke_escape": { "enabled": false, "change_types": [] }
  },
  "project": []
}
```

### Test story (placed at `.momentum/stories/test-research-story.md`)

```markdown
---
change_type: research-spike
---

## Acceptance Criteria

- AC1: The research artifact docs/research/my-research.md exists
- AC2: The artifact contains a synthesis section with a clear verdict

## File List

- docs/research/my-research.md
```

### Test research artifact (placed at `docs/research/my-research.md`)

```markdown
# My Research

## Synthesis

Verdict: Adopt. The tool meets all requirements for the use case.
```

### Spawn prompt

```
Sprint: test-sprint-2026-01-01
Stories: [test-research-story.md]
AVFL findings: []
```

## Verification Steps

1. Observe that the agent identifies `change_type: research-spike` as a `human_review_carveout`
2. Observe that the agent reads `docs/research/my-research.md`
3. Observe that the agent verifies AC1 (file exists) as VERIFIED
4. Observe that the agent verifies AC2 (synthesis + verdict) as VERIFIED
5. Observe that the report marks these as document review, not PASS/FAIL execution
6. Confirm the overall Verdict does NOT become FAIL due to document review entries

## Expected Pass Criteria

- Agent identifies the story as a document-review / human_review_carveout
- Agent reads the research artifact and verifies ACs by inspection
- No Bash commands, skill invocations, or behavioral triggers are executed for this story
- ACs are classified as VERIFIED/PARTIAL/MISSING, not PASS/FAIL (document review semantics)
- Document review findings do not affect the overall sprint verdict

## Expected Fail Criteria

- Agent attempts to run a command or invoke a skill to "execute" the research
- Agent reports BLOCKED because no `.feature` files exist for a research story
- Agent uses PASS/FAIL classification instead of VERIFIED/PARTIAL/MISSING
- Document review finding causes overall Verdict to be FAIL
