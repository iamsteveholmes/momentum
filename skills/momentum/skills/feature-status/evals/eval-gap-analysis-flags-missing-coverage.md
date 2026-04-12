# Eval: Gap Analysis Flags Missing Coverage

## Scenario

Given a `features.json` where a feature's `acceptance_condition` is broader than
what its assigned stories actually deliver, the skill must identify and flag the gap
explicitly.

## Input

### features.json (excerpt)
```json
{
  "features": [
    {
      "id": "feat-sprint-planning",
      "name": "Sprint Planning with Gap Analysis",
      "type": "flow",
      "status": "partial",
      "acceptance_condition": "A developer can run momentum:sprint-planning and receive a prioritized backlog with coverage gap analysis identifying which features lack sufficient story coverage.",
      "stories": ["create-skill-wrapper"]
    }
  ]
}
```

### stories/index.json (excerpt)
```json
{
  "stories": {
    "create-skill-wrapper": {
      "title": "Create SKILL.md wrapper for sprint-planning",
      "status": "done",
      "summary": "Creates the SKILL.md file and workflow.md delegation scaffold"
    }
  }
}
```

## Expected Behavior

1. The skill reasons that `acceptance_condition` requires "gap analysis identifying
   which features lack sufficient story coverage" — a substantive capability.
2. The assigned story (`create-skill-wrapper`) only delivers scaffolding (SKILL.md),
   not the gap analysis capability.
3. The skill produces an explicit gap flag for `feat-sprint-planning`:
   - Gap flag is set to `true`
   - Gap description names what is missing: something like "Gap: acceptance_condition
     requires coverage gap analysis capability; assigned story only covers skill
     scaffolding — gap analysis logic is not addressed."
4. In the HTML output, `feat-sprint-planning` sorts to the top of the `flow` type
   group (GAP features first).
5. The row has a visible `GAP` indicator in the always-visible section.
6. The full gap description is behind a `<details>` expand.

## Pass Criteria

- [ ] Gap flag is set for the feature (not just a partial status)
- [ ] Gap description names the specific missing capability
- [ ] Feature sorts to top of its type group in HTML
- [ ] GAP indicator is in the always-visible row section (not hidden in details)
- [ ] Full gap description text is inside `<details>` expand
- [ ] A feature with complete coverage does NOT receive a gap flag

## Failure Criteria

- Skill counts stories and marks "sufficient" because ≥1 story is assigned
- Skill flags gap but provides no description
- GAP features do not sort to the top of their type group
- GAP indicator is hidden inside the details expand
