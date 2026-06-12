# Eval: dedicated-run story dispatches both reviewers unchanged

## Scenario

Given a sprint plan where story S has `coverage_disposition: "dedicated-run"` (or defaulted to it), and the stage-1 dev agent has committed changes:

## Expected Behavior

The Conductor should:

1. Compute `{{story_diff}}` using the canonical Scenario A diff range.
2. Dispatch BOTH reviewers CONCURRENTLY (individual-agent fan-out, NOT TeamCreate):
   - REVIEWER A (`qa-reviewer`) with story_slug, worktree_path, verification_contract, story_diff
   - REVIEWER B (`momentum:code-reviewer`) with story_slug, story_diff, worktree_path, review_depth
3. Wait for BOTH to return.
4. Bind `{{qa_findings}}` and `{{cr_findings}}` from their respective outputs.
5. Merge into `{{stage2_findings}}`: deduplicated union, severity-sorted, with the existing dedup rule (same location+issue keeps higher-severity record, annotated source).
6. Advance to stage-3 with the merged findings.

## Anti-Behaviors (must NOT occur)

- Neither reviewer is skipped.
- The merge/dedup logic is not altered from its pre-fix form.
- No new finding source strings are introduced.
