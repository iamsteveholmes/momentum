# Eval: Session Menu — Natural Language Dispatch for Non-Listed Actions

## Story

quality-gate-parity-across-workflows

## Setup

- `momentum_completions = 3` (returning user)
- No open threads
- Active sprint exists; session menu has been displayed with state-appropriate items
- Developer types: "I want to fix a single story"

## Expected Behavior

1. Input Interpretation gate fires: Impetus confirms extracted intent before dispatching
2. Example confirmation: "Running quick-fix workflow for a single story — correct?"
3. On developer confirmation (Y), `momentum:quick-fix` dispatches (not `momentum:dev`)
4. The session menu does not need to list every possible action for natural language to work
5. `/develop` dispatch to `momentum:dev` is NOT offered — users use `/momentum:quick-fix` instead

## Fail Conditions

- Natural language input "fix a single story" dispatches `momentum:dev` directly
- Input Interpretation gate is bypassed (dispatch fires without confirmation)
- Error occurs when typing about single-story work after menu is shown
- `/develop` is mentioned in the confirmation or response as a valid user path
