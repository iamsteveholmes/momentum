---
id: eval-feature-status-absent-omitted
target: impetus happy-path greeting (SKILL.md and workflow.md Step 7)
---

# Eval: No-Features and No-Cache States in Greeting

## Scenario A: no-features state

Given:
- `preflight.greeting.feature_status` is `{ "state": "no-features" }`

Expected: The greeting includes the line:
`? No features defined yet — run feature-artifact-schema to plan features.`

## Scenario B: no-cache state

Given:
- `preflight.greeting.feature_status` is `{ "state": "no-cache" }`

Expected: The greeting includes the line:
`? No feature status yet — run feature-status to generate one.`

## Shared expectations (both scenarios)

- The feature status line appears after planning_context (or narrative if planning_context is null) and before the menu blank line.
- The menu items and closer are unaltered.
- The `?` symbol is used (not `·`) since no summary data is available.
