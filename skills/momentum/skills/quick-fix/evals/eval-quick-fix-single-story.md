# Eval: Quick Fix — Single-Story Scope

## Behavior Under Test

The quick-fix workflow operates on exactly one story and never introduces
multi-story ceremony: no backlog presentation, no wave planning, no dependency
graphs, no sprint activation/completion lifecycle.

## Preconditions

- The `momentum:quick-fix` skill is invoked
- The developer provides a fix description

## Expected Behaviors

### 1. No backlog is presented

Given the workflow has started
When the developer is asked to describe the fix
Then no list of existing stories is shown for selection
And no backlog filtering, sorting, or grouping occurs

### 2. No wave planning or dependency graphs

Given the story has been created and specified
When the workflow proceeds to implementation
Then no wave numbers are assigned
And no dependency graph is computed
And no stories are grouped for parallel execution

### 3. No sprint activation or completion lifecycle

Given the workflow is running
When the quickfix is registered for traceability
Then the entry appears under `quickfixes` in `sprints/index.json`
And no `planning` or `active` sprint slot is used
And no `momentum-tools sprint activate` or `sprint complete` is invoked

### 4. Exactly one story is processed

Given the workflow has completed all phases
When the developer reviews what was done
Then exactly one story was created, specified, implemented, and validated
And no story selection prompt was shown
And no story count or batch sizing occurred
