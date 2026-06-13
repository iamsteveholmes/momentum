# Eval: dedicated-run story dispatches both reviewers unchanged

## Scenario

Given a sprint plan where story S has `coverage_disposition: "dedicated-run"` (or defaulted to it), and the Conductor has committed the stage-1 dev agent's output, producing a non-trivial diff on the story branch:

## Expected Behavior

The Conductor should:

1. Compute `{{story_diff}}` using the canonical Scenario A diff range.
2. Dispatch BOTH reviewers CONCURRENTLY (individual-agent fan-out, NOT TeamCreate):
   - REVIEWER A (`qa-reviewer`) with story_slug, worktree_path, verification_contract, story_diff
   - REVIEWER B (`momentum:code-reviewer`) with story_slug, story_diff, worktree_path, review_depth
3. Wait for BOTH to return.
4. Bind `{{qa_findings}}` to the normalized canonical records produced by the stage-2 normalization of REVIEWER A's report (not the raw producer-format QA Review Report); bind `{{cr_findings}}` directly from REVIEWER B's output.
5. Merge into `{{stage2_findings}}`: deduplicated union, severity-sorted, with the existing dedup rule (same location+issue keeps higher-severity record, annotated source).
6. Advance to stage-3 with the merged findings.

## Invariants (must hold)

- Both reviewers are dispatched and both return findings.
- The merge/dedup logic follows the story-spec-defined rule: same location+issue keeps the higher-severity record, annotated with source `qa-reviewer+bmad-code-review`.
- Finding source strings are exactly `qa-reviewer` and `bmad-code-review` (or the combined annotation); no new source strings are introduced.
