# Eval: Sprint Planning Skill — Independent Invocability

## Setup
Invoke `/momentum:sprint-planning` directly (not through Impetus).

## Expected Behavior
1. The skill loads without error
2. The skill begins by reading `_bmad-output/implementation-artifacts/stories/index.json` to present the backlog
3. The skill does not require Impetus context or session state to start
4. The skill identifies stories grouped by epic, excluding terminal states (done, dropped)
