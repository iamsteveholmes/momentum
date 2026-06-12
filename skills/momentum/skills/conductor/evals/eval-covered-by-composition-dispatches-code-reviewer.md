# Eval: covered-by-composition story still dispatches code reviewer at build time

## Scenario

Given a sprint plan where story S has `coverage_disposition: "covered-by-composition"` with a valid `covered_by_scenario`, and the stage-1 dev agent has committed changes producing a non-trivial diff on the story branch:

## Expected Behavior

The Conductor should:

1. Compute `{{story_diff}}` using the canonical Scenario A diff range (merge-base of sprint branch and story branch) — the same diff range used for dedicated-run stories.
2. Dispatch REVIEWER B (`momentum:code-reviewer`) on that diff with the same inputs (story_slug, story_diff, worktree_path, review_depth) and report-only constraint as the dedicated-run path.
3. NOT dispatch REVIEWER A (`qa-reviewer`) — the dedicated QA verification run is deferred to the named integration scenario.
4. Bind `{{stage2_findings}}` to REVIEWER B's returned findings — normalized per finding-schema.md, `stakes_class` populated, severity-sorted (critical > major > minor > low). Source field: `bmad-code-review`.
5. NOT bind `{{stage2_findings}}` unconditionally to `[]`.
6. Advance to stage-3 with those findings so the fix loop runs normally on any code-review findings.

## Anti-Behaviors (must NOT occur)

- Stage-2 is NOT skipped entirely.
- `{{stage2_findings}}` is NOT unconditionally bound to `[]`.
- REVIEWER A is NOT dispatched at build time for this story.
- The code-review dispatch is NOT construed as a QA verification run anywhere in the routing.
