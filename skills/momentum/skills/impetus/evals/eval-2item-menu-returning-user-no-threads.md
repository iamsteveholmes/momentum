# Eval: Session Menu — Returning User, No Threads

## Story

quality-gate-parity-across-workflows

## Setup

- `momentum_completions = 3` (returning user)
- `journal.jsonl` absent or contains zero open threads
- Momentum fully installed, version matches
- Active sprint exists (`active-in-progress` state)

## Expected Behavior

1. Session menu renders with context-appropriate items (e.g., "Continue the sprint",
   "Refine backlog", "Triage") — driven by `greeting.state` from session-greeting.md
2. `/develop` does NOT appear as a menu item — momentum:dev is an internal sub-tool only
3. `/momentum:quick-fix` is the user-facing path for single-story development (via natural language input)
4. Number aliases dispatch to the items shown in the rendered menu for the detected state
5. Stats write (deferred) does not block or delay menu rendering

## Fail Conditions

- `/develop` appears as a menu item in any session state
- `momentum:dev` is dispatched directly from a menu selection
- Number aliases are not recognized
- Menu renders without reading `greeting.state` from session-greeting.md
- Stats write blocks menu rendering
