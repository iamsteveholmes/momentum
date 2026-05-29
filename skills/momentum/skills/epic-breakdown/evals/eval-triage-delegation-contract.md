# Eval: Triage Delegation Contract

Given an approved gap list with 3 items (1 ARTIFACT, 1 DECISION, 1 SHAPING) after the developer review gate, the skill should:

1. Invoke `momentum:triage` exactly once with:
   - `raw_items` as plain observation strings in format "{{item.title}} — {{item.description}}" (no suggested_class forwarded)
   - `source_label` set to `"epic-breakdown:{{epic_slug}}"` (using the actual epic slug, not the literal template variable)
2. NOT write to any planning artifacts directly — no writes to epics.json, stories/index.json, prd.md, or any file under _bmad-output/planning-artifacts/
3. Wait for triage to complete and surface triage's summary output as the final report
4. If triage cannot be found (SKILL.md missing), halt with a descriptive error before attempting delegation

The source_label format "epic-breakdown:{epic_slug}" (not "feature-breakdown:{epic_slug}") must be used in all delegations from this skill.
