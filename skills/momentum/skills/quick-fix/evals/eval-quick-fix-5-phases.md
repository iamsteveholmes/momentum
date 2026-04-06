# Eval: Quick Fix — 5-Phase Reachability

## Behavior Under Test

All 5 phases (Define, Specify, Implement, Validate, Ship) are reachable in the
quick-fix workflow and execute in order.

## Preconditions

- The `momentum:quick-fix` skill is invoked
- The developer provides a fix description and approves each gate

## Expected Behaviors

### 1. Phase 1 (Define) is reachable and produces a story

Given the developer has described a fix
When Phase 1 completes
Then a story file exists in the stories directory
And the story is registered in `stories/index.json`
And the developer has approved the story via a rendered review surface

### 2. Phase 2 (Specify) is reachable and produces a Gherkin spec

Given Phase 1 is complete and the story is approved
When Phase 2 completes
Then a `.feature` file exists for the story
And spec impact analysis has been performed
And specialist classification has been determined
And a quickfix entry is registered in `sprints/index.json`
And the developer has approved the Gherkin spec via a rendered review surface

### 3. Phase 3 (Implement) is reachable and produces code changes

Given Phase 2 is complete and the Gherkin spec is approved
When Phase 3 completes
Then a worktree was created and the specialist dev agent ran
And changes are merged back to the working branch
And the worktree is cleaned up

### 4. Phase 4 (Validate) is reachable and runs validation

Given Phase 3 is complete and code is merged
When Phase 4 completes
Then a post-merge AVFL scan has run
And a validation team was created with the dev agent and appropriate validators
And validators reported findings or confirmed clean

### 5. Phase 5 (Ship) is reachable and completes the quickfix

Given Phase 4 is complete and validation has passed
When Phase 5 completes
Then the quickfix entry in `sprints/index.json` has a completed date
And a push summary is shown to the developer
And the developer is asked whether to push
