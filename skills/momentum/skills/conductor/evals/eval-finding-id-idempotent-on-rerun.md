# Eval: finding_id assignment is idempotent — pre-existing ids are never overwritten

## Scenario

Given a `{{stage2_findings}}` array containing two findings where ONE already carries a
`finding_id` (e.g., rehydrated from the build ledger on resume or re-presented from a prior
fix-loop iteration) and ONE lacks a `finding_id`:

```
stage2_findings = [
  { story_slug: "story-b", source: "qa-reviewer", verdict: "MISSING", severity: "major",
    stakes_class: "routine", type: "spec-compliance", location: "src/widget.ts:99",
    summary: "AC-3 not implemented", detail: "...", evidence: "...", ac_id: "AC-3",
    legitimate: true, suggested_fix: null,
    finding_id: "qa-reviewer-0" },   // <-- pre-existing id from prior session
  { story_slug: "story-b", source: "bmad-code-review", verdict: null, severity: "minor",
    stakes_class: "routine", type: "spec-compliance", location: "src/widget.ts:120",
    summary: "Dead code path", detail: "...", evidence: "...", ac_id: null,
    legitimate: true, suggested_fix: "Remove dead branch." }
    // no finding_id — needs fresh assignment
]
```

## Expected behavior

When step 2.S3's assignment instruction runs over this `{{stage2_findings}}` array:

1. The finding that already carries `finding_id: "qa-reviewer-0"` is **left unchanged**. Its
   `finding_id` remains `"qa-reviewer-0"` — the assignment step does not overwrite it, reset
   it, or generate a new id for it.
2. The finding that lacks a `finding_id` receives a fresh, unique id (e.g., `"bmad-code-review-1"`).
3. The `{{fix_attempts}}` retry counter, ledger dedup guard `(story_slug, event, finding_id)`,
   and every downstream `F.finding_id` reference in the disposition CASE blocks can rely on the
   pre-existing id being stable across resume and loop iterations.

## Pass condition

The workflow instruction text explicitly conditions the assignment on "each finding that lacks
a `finding_id`" (or equivalent phrasing: "if `finding_id` is absent or empty"). The instruction
does NOT assign a new id unconditionally to every finding in the array.

## Fail condition

The assignment step overwrites pre-existing ids (unconditional assignment). Or the pre-existing
`finding_id` is not preserved when the assignment instruction runs a second time over the same array.

## Why this matters

The build ledger dedup guard uses `(story_slug, event, finding_id)` tuples to prevent duplicate
ledger rows on resume. If the assignment were non-idempotent (resetting ids on each loop pass),
a finding presented twice would get two different ids, and the dedup guard would fire too late or
not at all — allowing duplicate disposition rows for the same underlying finding.
