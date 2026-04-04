# Eval: Session Orientation With Threads

## Scenario

Given `.claude/momentum/journal.jsonl` contains these two open thread entries:

```jsonl
{"thread_id":"T-001","workflow_type":"story-cycle","story_ref":"4.2","current_step":"code-review","phase":"mid-review","last_action":"Code reviewer dispatched","context_summary":"Story 4.2 implementation — reviewer is analyzing the null-check pattern","last_active":"2026-03-23T12:30:00Z","status":"open","depends_on_thread":null}
{"thread_id":"T-002","workflow_type":"ux-design","story_ref":"5.1","current_step":"visual-foundation","phase":"early-design","last_action":"Color palette selected","context_summary":"UX design specification — visual foundation phase, color palette locked","last_active":"2026-03-22T09:00:00Z","status":"open","depends_on_thread":null}
```

When the developer invokes `/momentum` and startup routing reaches session orientation (installed.json exists, version matches):

## Expected Behavior

1. Impetus reads `journal.jsonl` and reconstructs current thread state (last entry per thread_id)
2. Impetus displays a numbered list of open threads ordered by most-recently-active:
   - Thread 1: Story 4.2 (most recent — ~hours ago) with phase "mid-review" and elapsed time
   - Thread 2: UX design 5.1 (yesterday) with phase "early-design" and elapsed time
3. Each thread is selectable by number
4. Display ends with a prompt like "Continue (1/2) or tell me what you need?"
5. Within two exchanges total, Impetus surfaces: active story/task, current phase, last completed action, and suggested next action — without the developer asking "where were we?"

## NOT Expected

- Threads displayed out of order (older thread before newer)
- Missing elapsed time or phase information
- Developer needing to ask what they were working on
- More than two exchanges before orientation is complete
- Journal display appearing when journal has no open threads
