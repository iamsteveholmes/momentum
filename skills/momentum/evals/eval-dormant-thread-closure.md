# Eval: Dormant Thread Closure

## Scenario

Given `.claude/momentum/journal.jsonl` contains one open thread with `last_active` more than 3 days ago:

```jsonl
{"thread_id":"T-003","workflow_type":"architecture-research","story_ref":"3.1","current_step":"gathering-inputs","phase":"research","last_action":"Surveyed three API options","context_summary":"Architecture research for Story 3.1 — surveyed API options, no decision yet","last_active":"2026-03-19T10:00:00Z","status":"open","depends_on_thread":null}
```

When the developer invokes `/momentum` and startup routing reaches session orientation:

## Expected Behavior

1. Impetus reads the journal and detects this thread has been inactive for >3 days
2. After displaying the Session Journal (if applicable), Impetus surfaces the dormant thread separately:
   - Shows brief context from `context_summary`
   - States it has been dormant (e.g., "4 days inactive")
   - Offers one-action closure (e.g., "Close this thread? [Y/N]")
3. Developer confirms with a single response (e.g., "Y" or "yes")
4. Impetus appends a new entry to `journal.jsonl` with `status: "closed"` for that thread_id
5. Closure is complete — no further questions about this thread

## NOT Expected

- Requiring more than one confirmation to close a dormant thread
- Failing to detect dormancy (thread silently remains open)
- Modifying existing journal lines (must append, never overwrite)
- Surfacing dormant thread without context
