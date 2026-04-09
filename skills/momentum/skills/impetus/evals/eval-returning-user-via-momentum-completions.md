# Eval: Returning User Routed to Session Menu When Skills Not in Component Registry

## Story

impetus-journal-hygiene-script (E2E fix: cmux pane sessions route correctly)

## Setup

- `session_stats.momentum_completions = 3` present in `.claude/momentum/installed.json`
- `installed.json.components` contains only `hooks` — "skills" is NOT registered as a component
- `global-installed.json.components` contains only `rules` — "skills" is NOT registered globally
- Claude launched in a cmux terminal pane (may not have project-level installed.json in scope)

## Expected Behavior

1. Impetus reads `momentum_completions` from any reachable installed.json
2. Because `momentum_completions > 0`, Impetus routes directly to the session menu (step 10)
3. The first-install consent prompt does NOT appear
4. The install/setup flow does NOT execute
5. The developer sees the normal session menu (sprint state, threads, etc.)

## Fail Conditions

- First-install consent prompt appears despite `momentum_completions > 0`
- Install steps execute (writing rules, hooks) when they are already present
- Impetus treats absent "skills" component registration as evidence of first-install
- Routing falls through to first-install because component completeness check fires before `momentum_completions` check
