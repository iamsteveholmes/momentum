# Eval: Assigns finding_id before directed fixer invocation

## Scenario

Given a `{{stage2_findings}}` array containing three findings, NONE of which carry a `finding_id`
field (the field is absent from every record — as produced by the qa-reviewer normalization path
and/or the bmad-code-review output path before the Conductor's assignment step):

```
stage2_findings = [
  { story_slug: "story-a", source: "qa-reviewer", verdict: "MISSING", severity: "major",
    stakes_class: "routine", type: "spec-compliance", location: "src/foo.ts:42",
    summary: "AC-1 not implemented", detail: "...", evidence: "...", ac_id: "AC-1",
    legitimate: true, suggested_fix: null },
  { story_slug: "story-a", source: "qa-reviewer", verdict: "PARTIAL", severity: "minor",
    stakes_class: "routine", type: "spec-compliance", location: "src/bar.ts:10",
    summary: "AC-2 partially complete", detail: "...", evidence: "...", ac_id: "AC-2",
    legitimate: true, suggested_fix: "Add the missing branch." },
  { story_slug: "story-a", source: "bmad-code-review", verdict: null, severity: "minor",
    stakes_class: "routine", type: "spec-compliance", location: "src/baz.ts:5",
    summary: "Unused import", detail: "...", evidence: "...", ac_id: null,
    legitimate: true, suggested_fix: "Remove the import." }
]
```

## Expected behavior

When step 2.S3 processes `{{stage2_findings}}` in the entry block, BEFORE invoking the directed
fixer (Phase B), it must:

1. **Assign a `finding_id` to every finding** that lacks one (all three in this scenario).
2. **Produce unique ids within the array**: no two findings may share the same `finding_id`.
   For example, using the scheme `<source>-<zero-based-index>`:
   - finding[0]: `finding_id = "qa-reviewer-0"`
   - finding[1]: `finding_id = "qa-reviewer-1"`
   - finding[2]: `finding_id = "bmad-code-review-2"`
3. **The directed fixer invocation at Phase B** receives a findings batch where EVERY finding
   carries a non-empty `finding_id`. The fixer is never called with a finding missing the key.

## Pass condition

The workflow instruction text in step 2.S3 includes an explicit, deterministic assignment step
positioned AFTER the `{{stage2_findings}}` bind and BEFORE the Phase B fixer invocation.
Reading the entry block top-to-bottom confirms: bind `{{stage2_findings}}` → bind `{{fix_attempts}}`
→ assign `finding_id` to each finding lacking one → Phase B fixer invocation.

## Fail condition

The fixer invocation at Phase B is reached with any finding in `{{stage2_findings}}` that lacks
a `finding_id`. Or the assignment step appears AFTER Phase B in the reading order.
