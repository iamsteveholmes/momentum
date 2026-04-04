# Eval: Concurrent Tab Warning

## Scenario

Given `.claude/momentum/journal.jsonl` contains an open thread with `last_active` timestamp 5 minutes ago (simulating activity in another tab):

```jsonl
{"thread_id":"T-004","workflow_type":"story-cycle","story_ref":"4.2","current_step":"implementation","phase":"coding","last_action":"Wrote unit tests for parser module","context_summary":"Story 4.2 implementation — unit tests for parser module written, moving to integration","last_active":"2026-03-23T14:55:00Z","status":"open","depends_on_thread":null}
```

When the developer invokes `/momentum` at 2026-03-23T15:00:00Z in a different tab:

## Expected Behavior

1. Impetus reads the journal and detects this thread's `last_active` is within the last 30 minutes
2. Impetus flags the thread as likely active in another tab:
   - Warning format: "! This thread appears active in another tab (5 minutes ago)."
   - Additional context: "Opening here may cause conflicts. Proceed anyway?"
3. The warning is non-blocking — the developer can choose to proceed
4. If the developer wants to work on the same story, Impetus asks for confirmation before starting a competing thread

## NOT Expected

- Blocking the developer from proceeding (warn, never block)
- Silently allowing a competing thread without any warning
- Warning about threads active more than 30 minutes ago (those are not concurrent)
- Treating the 30-minute threshold as a hard lock mechanism
