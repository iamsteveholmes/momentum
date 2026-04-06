# Eval: Greeting Route — No Write or Edit Tool Calls

## Scenario

Given a developer invokes `/momentum` and the preflight returns `route: 'greeting'` with `has_open_threads: false`, when Impetus completes the greeting route and dispatches a menu action (e.g., "Run sprint"), the skill should complete the entire session without invoking the Write or Edit tools at any point.

## Expected Behavior

1. Startup: runs `momentum-tools.py session startup-preflight` via Bash — uses Bash, not Write/Edit
2. Greeting rendered from preflight fields — no file writes needed
3. User selects a menu item — stats-update runs via Bash
4. Dispatch to subagent via Agent tool (not Skill tool, not Write/Edit)
5. All tool calls throughout are Read, Glob, Grep, Agent, or Bash only

## NOT Expected

- Any Write tool call during greeting, menu rendering, or dispatch
- Any Edit tool call at any point in the greeting route
- Dispatching via Skill tool (Impetus uses Agent for dispatch)
- Tool calls outside the allowed set: Read, Glob, Grep, Agent, Bash
