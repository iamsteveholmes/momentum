# Eval: QA Normalization — All-VERIFIED Report Produces Empty Array

## Given

The Conductor's stage-2 pipeline has received a qa-reviewer report for story `add-user-profile-screen` where every AC passed:

```
## QA Review Report

**Story:** add-user-profile-screen
**Worktree:** .worktrees/story-add-user-profile-screen
**Verdict:** PASS

### Test Results
- Total: 3 | Passed: 3 | Failed: 0 | Skipped: 0
- Command: ./gradlew :shared:testDebugUnitTest --tests "*.ProfileScreenTest"

### AC Verification

| AC# | Description | Status | Evidence (file:line) | Stakes Class |
|-----|-------------|--------|----------------------|--------------|
| AC-1 | Profile screen displays user name | VERIFIED | ProfileScreenTest.kt:14 | routine |
| AC-2 | Profile screen displays avatar | VERIFIED | ProfileScreenTest.kt:28 | routine |
| AC-3 | Edit button navigates to edit screen | VERIFIED | ProfileScreenTest.kt:41 | routine |

### Findings

(none)

### Summary
All 3 ACs verified. No findings. No non-routine stakes classes.
```

## The Conductor Should

Normalize the qa-reviewer report to an empty findings array (zero canonical records). The merge step proceeds with REVIEWER B findings alone. No error is raised, no fabricated placeholder records are created, and the empty result does not block the pipeline. The `{{qa_findings}}` binding resolves to `[]`.
