# Eval: Quick Fix — Independent Invocability

## Behavior Under Test

The `momentum:quick-fix` skill loads and begins Phase 1 (Define) when invoked
directly without Impetus orchestration or an active sprint.

## Preconditions

- No active sprint exists in `sprints/index.json`
- Impetus is not running (no active session menu)
- The developer invokes `/momentum:quick-fix` directly

## Expected Behaviors

### 1. Skill loads without sprint dependency

Given no active sprint exists in `sprints/index.json`
When the developer invokes `/momentum:quick-fix`
Then the skill loads and begins execution without error
And the skill does not check for or require an active sprint

### 2. Phase 1 begins with description prompt

Given the quick-fix skill has loaded
When the skill begins Phase 1 (Define)
Then the developer is asked to describe the fix
And the developer is asked for an epic_slug (with "ad-hoc" as default)

### 3. No Impetus session menu required

Given Impetus is not running
When the developer invokes `/momentum:quick-fix`
Then the skill proceeds directly to Phase 1
And does not attempt to read Impetus session state or mode
