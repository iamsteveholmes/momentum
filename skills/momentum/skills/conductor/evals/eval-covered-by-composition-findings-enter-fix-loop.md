# Eval: covered-by-composition story's code-review findings enter the fix loop

## Scenario

Given a story S with `coverage_disposition: "covered-by-composition"`, and REVIEWER B returns a non-empty findings list (e.g., two findings: one major, one minor):

## Expected Behavior

The Conductor should:

1. Bind `{{stage2_findings}}` to REVIEWER B's findings (not `[]`).
2. Invoke step 2.S3 with those findings.
3. Step 2.S3's empty-findings check (`{{stage2_findings}} is empty`) evaluates to false — the fix loop runs.
4. The directed fixer receives the code-review findings and applies fixes per the normal Phase B-C-D cycle with retry-bound-3.
5. The story does NOT short-circuit to merge on an artificially empty findings list.

## Anti-Behaviors (must NOT occur)

- `{{stage2_findings}}` is NOT `[]` when REVIEWER B returned findings.
- The empty-findings fast path does NOT fire when there are actual findings.
- No special handling differentiates covered-by-composition findings from dedicated-run findings in stage-3 — they use the same fix-loop machinery.
