# Eval: QA Normalization — All-VERIFIED Report Produces Empty Array

## Given

The Conductor's stage-2 pipeline has received a qa-reviewer report for story `add-user-profile-screen` where every AC passed:

```
## QA Review Report

### Test Results

| AC# | Description | Status | Evidence | Stakes Class |
|---|---|---|---|---|
| AC-1 | Profile screen displays user name | VERIFIED | Name renders correctly in snapshot | routine |
| AC-2 | Profile screen displays avatar | VERIFIED | Avatar component present with correct src | routine |
| AC-3 | Edit button navigates to edit screen | VERIFIED | Navigation observed via route change | routine |

### Findings

(none)

### Summary
All 3 ACs verified. No findings.
```

## The Conductor Should

Normalize the qa-reviewer report to an empty findings array (zero canonical records). The merge step proceeds with REVIEWER B findings alone. No error is raised, no fabricated placeholder records are created, and the empty result does not block the pipeline. The `{{qa_findings}}` binding resolves to `[]`.
