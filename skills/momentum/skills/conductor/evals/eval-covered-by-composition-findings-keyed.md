# Eval: covered-by-composition path — bmad-code-review-only findings also receive finding_id

## Scenario

Given a story whose `{{coverage_disposition}}` is `"covered-by-composition"` — meaning only
REVIEWER B (bmad-code-review) runs and `{{stage2_findings}}` is bound directly from
`{{cr_findings}}` (no qa-reviewer merge):

```
cr_findings = [
  { story_slug: "story-c", source: "bmad-code-review", verdict: null, severity: "major",
    stakes_class: "routine", type: "spec-compliance", location: "src/core.ts:200",
    summary: "Missing null check", detail: "...", evidence: "...", ac_id: null,
    legitimate: true, suggested_fix: "Add null guard before access." },
  { story_slug: "story-c", source: "bmad-code-review", verdict: null, severity: "minor",
    stakes_class: "security-auth-isolation", type: "security", location: "src/auth.ts:50",
    summary: "Token not invalidated on logout", detail: "...", evidence: "...", ac_id: null,
    legitimate: true, suggested_fix: "Invalidate session token in logout handler." }
]

stage2_findings = cr_findings  // covered-by-composition path: direct bind, no merge
```

Neither finding carries a `finding_id` — bmad-code-review output does not include this field.

## Expected behavior

The step 2.S3 assignment instruction runs over `{{stage2_findings}}` regardless of which path
populated it (dedicated-run or covered-by-composition). The two bmad-code-review-only findings
receive unique `finding_id` values before Phase B is invoked:
- finding[0]: `finding_id = "bmad-code-review-0"`
- finding[1]: `finding_id = "bmad-code-review-1"`

The Phase B fixer invocation input lists both findings with `finding_id` present.

## Pass condition

The assignment step in step 2.S3 is placed after BOTH the dedicated-run `{{stage2_findings}}`
bind (line ~759) AND the covered-by-composition `{{stage2_findings}}` bind (line ~779), so it
fires unconditionally for any non-empty `{{stage2_findings}}`, no matter which reviewer path
produced it. Reading the workflow top-to-bottom: the assignment instruction appears after the
last `{{stage2_findings}}` bind and before Phase B — meaning it covers both paths without
branching.

## Fail condition

The assignment step is placed only inside the dedicated-run branch, leaving the
covered-by-composition path unguarded. Or the assignment step references only `{{qa_findings}}`
without also covering `{{cr_findings}}`-only scenarios.

## Why this matters

The covered-by-composition path sets `{{stage2_findings}} = {{cr_findings}}` directly (workflow.md
line ~779) without a merge step. If the finding_id assignment were placed before that bind (or only
in the qa-reviewer branch), bmad-code-review-only findings would reach Phase B without a
`finding_id`, silently violating the directed-fix invocation contract on this path.
