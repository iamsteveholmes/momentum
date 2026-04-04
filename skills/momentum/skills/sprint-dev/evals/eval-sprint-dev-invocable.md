# Eval: Sprint Dev Skill — Independent Invocability

## Setup
Invoke `/momentum:sprint-dev` directly (not through Impetus).

## Expected Behavior
1. The skill loads without error
2. The skill begins Phase 1 (Initialization) — reading sprints/index.json for the active sprint
3. The skill does not require Impetus context or session state to start
4. If no active sprint exists, the skill halts with a clear message
