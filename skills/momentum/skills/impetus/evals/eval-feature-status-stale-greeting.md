---
id: eval-feature-status-stale-greeting
target: impetus happy-path greeting (SKILL.md and workflow.md Step 7)
---

# Eval: Stale Feature Status in Greeting

## Scenario

Given:
- `preflight.route == "greeting"` and `preflight.has_open_threads == false`
- `preflight.greeting.feature_status` is `{ "state": "stale", "summary": "3 features: 1 working · 2 partial" }`
- `greeting.narrative` is `Sprint "sprint-xyz" is underway — steady ground.`
- `greeting.planning_context` is null
- `greeting.menu` and `greeting.closer` are present

## Expected Behavior

The greeting output contains the feature status line:
`· 3 features: 1 working · 2 partial  ! may be out of date — run feature-status to refresh`

The staleness indicator `! may be out of date — run feature-status to refresh` is appended to the summary line.
The line appears after the narrative (since planning_context is null, that line is omitted).
The menu and closer are unchanged.
