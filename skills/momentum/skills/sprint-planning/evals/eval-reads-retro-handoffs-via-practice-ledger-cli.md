# Eval: Phase A.6 reads retro handoff items via practice-ledger by-source CLI

## Scenario

Given sprint planning is running Step 1 and has reached Phase A.6 (Retro handoff items),
and `.momentum/practice-ledger.jsonl` exists with an open (non-terminal) entity created by a
prior retro — appended via the A1 CLI:

```
python3 skills/momentum/scripts/momentum-tools.py practice-ledger append \
  --entity-id retro-handoff-1 --event-type created --source retro --actor retro \
  --payload '{"intent":"handoff","title":"Investigate flaky AVFL lens"}'
```

## Expected Behavior

The sprint planning orchestrator should, in Phase A.6:

1. Run `momentum-tools practice-ledger by-source retro` (NOT the legacy
   `intake-queue list --source retro --kind handoff --status open`) to read prior retro events.
2. Filter the returned events to those whose current entity state is non-terminal and whose
   `payload.intent == "handoff"` — these are un-actioned retro findings handed off for sprint planning.
   The command returns the event list under the `events` key, e.g.:

   ```json
   {
     "action": "practice_ledger_by_source",
     "success": true,
     "source": "retro",
     "events": [
       {
         "entity_id": "retro-handoff-1",
         "event_type": "created",
         "source": "retro",
         "payload": { "intent": "handoff", "title": "Investigate flaky AVFL lens" }
       }
     ],
     "count": 1
   }
   ```

3. Store `{{retro_handoff_items}}` = the filtered entity list and include it in the recommendation
   synthesis context alongside the sprint summary.
4. When the developer selects a handoff item during story selection (via `handoff-N` or title match),
   append a `consumed` event for that entity:

   ```
   python3 skills/momentum/scripts/momentum-tools.py practice-ledger append \
     --entity-id retro-handoff-1 --event-type consumed --source sprint-planning \
     --actor sprint-planning --payload '{"outcome_ref":"{{slug}}"}'
   ```

   After which `practice-ledger open` no longer lists that entity (the consumed event moves its
   current state to terminal).

## What This Tests

- Phase A.6 uses the new `practice-ledger by-source retro` reader, not the removed `intake-queue list` surface
- Handoff items are filtered by current-state non-terminal + `payload.intent == "handoff"`
- Consuming a selected handoff appends a `consumed` event (append-only) rather than mutating a row
- When the ledger has no open retro handoffs (empty `events` or all terminal), `{{retro_handoff_items}}`
  is set to `[]` and planning continues without retro handoff context
