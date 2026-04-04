# Eval: 2-Item Menu — Returning User With Open Threads

## Story

2a-3: Session-Open Menu Redesign

## Setup

- `momentum_completions = 2` (returning user)
- `journal.jsonl` contains 1 open thread:
  ```jsonl
  {"thread_id":"T-001","workflow_type":"story-cycle","story_ref":"2a-3","current_step":"implementation","phase":"in-progress","last_action":"Evals written","context_summary":"Story 2a-3 — menu redesign in progress","last_active":"2026-03-28T10:00:00Z","status":"open","depends_on_thread":null}
  ```

## Expected Behavior

1. Step 11 (journal display) fires BEFORE the 2-item menu — threads appear first
2. After thread handling (selection or new-work decision), the 2-item menu appears with exactly `/create` and `/develop`
3. Threads are NOT duplicated as a menu item
4. The thread display path (GOTO Step 11) is unchanged

## Fail Conditions

- Menu appears before thread display
- Thread duplication: "Show session threads" appears as a menu item alongside threads
- Thread display is skipped when open threads exist
- Menu contains items beyond `/create` and `/develop`
