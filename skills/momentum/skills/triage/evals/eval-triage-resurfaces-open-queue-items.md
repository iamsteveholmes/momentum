# Eval: Triage Re-surfaces Open Ledger Entities from practice-ledger.jsonl

## Purpose

Verify that `momentum:triage` reads `practice-ledger.jsonl` at startup and re-presents
open entities (non-terminal last event) alongside new observations for re-classification.
"Open" is a derived state: an entity is open if its most recent event has a non-terminal
`event_type` (i.e., not `consumed`, `rejected`, or `closed_stale`).

## Scenario

`practice-ledger.jsonl` contains two existing events (one entity each):
```jsonl
{"event_id":"ev-001","entity_id":"ent-abc1","event_type":"created","ts":"2026-04-10T10:00:00Z","source":"triage","actor":"triage","payload":{"title":"AI code review workflow idea","description":"...","triage_class":"shaping"}}
{"event_id":"ev-002","entity_id":"ent-def2","event_type":"created","ts":"2026-04-12T14:30:00Z","source":"triage","actor":"triage","payload":{"title":"Multi-workspace cmux integration","description":"...","triage_class":"defer"}}
```

A third event for a consumed entity also exists (should NOT be surfaced):
```jsonl
{"event_id":"ev-003","entity_id":"ent-ghi3","event_type":"consumed","ts":"2026-04-13T09:00:00Z","source":"triage","actor":"triage","payload":{"reason":"promoted to story"}}
```

The developer also provides one new observation: "Add a retro summary email feature."

## Expected Behaviors

### B1: Open Entities Displayed Before New Items

Before asking for new observations (or presenting the classification), triage calls
`practice-ledger open` and displays the two non-terminal entities with `[QUEUED]` prefix
or equivalent visual distinction.

### B2: Open Items Included in Classification Pass

The two queued entities and the new observation are all included in the classification step.
The developer can re-classify any queued entity (e.g., promote from SHAPING to ARTIFACT,
change DEFER to REJECT).

### B3: No Re-surfacing of Consumed/Rejected Entities

The entity `ent-ghi3` (last event: `consumed`) is NOT surfaced as open, even though
earlier events exist for it. The derived-state rule applies: only the most recent
event determines open/closed status.

### B4: Resolve Prompt at End

After batch-approval decisions are made, triage asks whether any open entities with
no new classification action should be marked as consumed. The developer can provide
entity IDs to consume.

### B5: Consume via CLI

Entities the developer marks as consumed are processed via:
```
python3 skills/momentum/scripts/momentum-tools.py practice-ledger append \
  --event-type consumed \
  --entity-id "ent-abc1" \
  --source "triage" \
  --actor "triage" \
  --payload '{"reason":"manually resolved"}'
```

Not by direct Edit of the JSONL file.

Verify: `practice-ledger open` no longer returns `ent-abc1` after the consumed event
is appended.

### B6: Missing File is Not an Error

If `practice-ledger.jsonl` does not exist (first triage session), the skill proceeds
normally with an empty open entities list — no error is raised.

## Pass Criteria

B1–B6 must all be satisfied. Surfacing consumed or rejected entities as open is a failing eval.
Any use of the legacy CLI subcommand (pre-DEC-033) or the mutable-row `kind:`/`status:` fields
is an automatic failure.
