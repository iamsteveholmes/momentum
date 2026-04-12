---
id: eval-feature-status-fresh-greeting
target: impetus happy-path greeting (SKILL.md and workflow.md Step 7)
---

# Eval: Fresh Feature Status in Greeting

## Scenario

Given:
- `preflight.route == "greeting"` and `preflight.has_open_threads == false`
- `preflight.greeting.feature_status` is `{ "state": "fresh", "summary": "4 features: 2 working · 1 partial · 1 not-started" }`
- `greeting.narrative` is `Sprint "sprint-abc" is underway — steady ground.`
- `greeting.planning_context` is `"next-sprint" is taking shape behind it.`
- `greeting.menu` is `["[1] Continue the sprint", "[2] Refine backlog", "[3] Triage"]`
- `greeting.closer` is `Lead on.`

## Expected Behavior

The greeting output contains the feature status line `· 4 features: 2 working · 1 partial · 1 not-started`
placed after the planning_context line and before the menu. No staleness flag or `!` warning appears.
The menu and closer are unchanged.
