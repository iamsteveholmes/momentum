# Eval: Quick Fix — Code Review in Phase 4 Between AVFL and Team Validation

## Behavior Under Test

Phase 4 of the quick-fix workflow includes an explicit code review step via
`momentum:code-reviewer`, positioned between the post-merge AVFL scan (step 4a)
and team creation (step 4c). Code review findings are merged into the
collaborative fix loop task list.

## Preconditions

- Phase 3 (Implement) is complete and changes are merged to the working branch
- The story's `touches` array is available from the story file frontmatter
- The worktree has been cleaned up after the merge (Phase 3)
- A post-merge AVFL scan has just completed (step 4a)

## Expected Behaviors

### 1. Code review runs after AVFL and before team creation

Given the post-merge AVFL scan (step 4a) has completed
When Phase 4 continues
Then `momentum:code-reviewer` is invoked before the validation team is created
And the code reviewer is scoped to the files in the story's `touches` array
And code review findings are collected before team validation begins

### 2. Code review findings are presented alongside AVFL findings

Given `momentum:code-reviewer` has completed
When the workflow presents findings to the developer
Then both AVFL findings and code review findings are visible before team validation
And findings from each source are attributed (AVFL vs code-reviewer)

### 3. Code review findings flow into the collaborative fix loop

Given both AVFL and code review findings exist
When the validation team (Dev + validators) is created
Then the Dev agent receives both AVFL findings and code review findings as its task list
And the Dev agent can address code review findings during the collaborative fix loop
And validators re-verify after fixes are applied

### 4. Worktree remains available through all gate iterations

Given the validation gates are in progress (AVFL, code review, team validation)
When fix iterations are needed
Then the worktree is still available for fix agents to use
And the worktree is NOT deleted until all gates have passed or the developer
    explicitly accepts remaining findings

## Fail Conditions

- Code review step is absent from Phase 4 (code-reviewer never invoked)
- Code review runs after team validation instead of before it
- Code review findings are not passed to the Dev agent in the fix loop
- The worktree is cleaned up before all quality gates complete
- Code review scoping does not use the story's `touches` array
