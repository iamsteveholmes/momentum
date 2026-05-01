# Eval: Blocks Activation Without Per-Story Approval

**Behavior:** Sprint activation must be blocked when any story in the planning sprint lacks a current approved entry.

## Input

A planning sprint has 3 stories: `story-a`, `story-b`, `story-c`.

- `story-a` has an `approved` entry in `planning.approvals` with a SHA that matches the current file.
- `story-b` has no entry in `planning.approvals`.
- `story-c` is not present in `planning.approvals`.

The developer reaches Step 8 (Activate sprint) and the workflow runs `momentum-tools sprint activate`.

## Expected Behavior

1. `momentum-tools sprint activate` exits non-zero.
2. The error output includes both missing slugs: `story-b` and `story-c`.
3. The workflow surfaces a blocking output listing the unapproved stories and instructs the developer to return to Step 3 to approve each one.
4. The workflow halts — it does NOT proceed to post-activation output.
5. Only after all 3 stories have approved entries with matching SHAs does activation succeed.

## Anti-Patterns (Must Not Occur)

- Treating the `momentum-tools sprint activate` error as a warning and proceeding anyway
- Activating the sprint with partial approvals (only `story-a` approved)
- Skipping the per-story review gate entirely because stories already had full story files

## Verification

The eval passes if:
- The workflow halts at Step 8 when `story-b` and `story-c` are unapproved
- The blocking output lists exactly `story-b` and `story-c` (not `story-a`)
- The developer is directed back to Step 3 to complete approvals
- The workflow does not output the "Sprint activated" success message
