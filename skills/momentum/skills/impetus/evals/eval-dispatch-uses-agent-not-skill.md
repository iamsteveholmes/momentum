# Eval: Menu Dispatch — Uses Agent Tool, Not Skill Tool

## Scenario

Given a developer invokes `/momentum` and reaches the session menu (greeting route or post-install orientation), when they select any menu item that dispatches a subworkflow (e.g., "Run sprint" → sprint-dev, "Plan sprint" → sprint-planning, "Refine backlog" → create-story), Impetus should dispatch using the Agent tool.

## Expected Behavior

1. Developer selects a menu item (by number or fuzzy-continue)
2. Impetus dispatches the corresponding workflow via Agent tool call
3. The Agent invocation targets the correct skill (e.g., `momentum:sprint-dev`)
4. No Skill tool call is made by Impetus — Skill is for human invocation, not orchestrator dispatch

## NOT Expected

- Impetus calling the Skill tool to invoke `momentum:sprint-dev` or any other skill
- Impetus doing the work of the dispatched skill directly (no orchestrator purity violation)
- Write or Edit tool calls during dispatch

## Why Agent, Not Skill

The `Skill` tool is the human-facing invocation mechanism (e.g., `/momentum:sprint-dev`). Impetus
dispatches subagents programmatically via the `Agent` tool. Using `Skill` from within Impetus would
be an orchestrator purity violation — it bypasses the agent boundary and subverts separation of concerns.
