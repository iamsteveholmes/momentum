# Eval: Session Menu — Returning User With Open Threads

## Story

quality-gate-parity-across-workflows

## Setup

- `momentum_completions = 2` (returning user)
- `journal.jsonl` contains 1 open thread:
  ```jsonl
  {"thread_id":"T-001","workflow_type":"story-cycle","story_ref":"quality-gate-parity","current_step":"implementation","phase":"in-progress","last_action":"Evals written","context_summary":"Quality gate parity — implementation in progress","last_active":"2026-03-28T10:00:00Z","status":"open","depends_on_thread":null}
  ```

## Expected Behavior

1. Step 11 (journal display) fires BEFORE the session menu — threads appear first
2. After thread handling (selection or new-work decision), the session menu appears
   with items driven by `greeting.state` from session-greeting.md
3. `/develop` does NOT appear as a menu item in any path
4. Threads are NOT duplicated as a menu item
5. The thread display path (GOTO Step 11) is unchanged

## Fail Conditions

- Menu appears before thread display
- `/develop` appears as a menu item
- `momentum:dev` is dispatched directly from a menu selection
- Thread duplication: "Show session threads" appears as a menu item alongside threads
- Thread display is skipped when open threads exist
