# Eval: Triage Re-surfaces Open Queue Items from intake-queue.jsonl

## Purpose

Verify that `momentum:triage` reads `intake-queue.jsonl` at startup and re-presents
open SHAPING and DEFER items alongside new observations for re-classification.

## Scenario

`intake-queue.jsonl` contains two existing events:
```jsonl
{"id":"abc1","kind":"shape","title":"AI code review workflow idea","description":"...","source":"triage","captured_at":"2026-04-10T10:00:00"}
{"id":"def2","kind":"watch","title":"Multi-workspace cmux integration","description":"...","source":"triage","captured_at":"2026-04-12T14:30:00"}
```

The developer also provides one new observation: "Add a retro summary email feature."

## Expected Behaviors

### B1: Open Items Displayed Before New Items

Before asking for new observations (or presenting the classification), triage displays
the two open queue items with `[QUEUED]` prefix or equivalent visual distinction.
Items without `resolved_at` are treated as open.

### B2: Open Items Included in Classification Pass

The two queued items and the new observation are all included in the classification step.
The developer can re-classify any queued item (e.g., promote from SHAPING to ARTIFACT,
change DEFER to REJECT).

### B3: No Re-opening of Resolved Items

A third event with `resolved_at` set is NOT surfaced as open, even if its kind is "shape"
or "watch".

### B4: Resolve Prompt at End

After batch-approval decisions are made, triage asks whether any open queue items with
no new classification action should be marked as resolved. The developer can provide IDs
to resolve.

### B5: Resolve via CLI

Items the developer marks as resolved are processed via:
```
python3 skills/momentum/scripts/momentum-tools.py intake-queue resolve --id ID
```

Not by direct Edit of the JSONL file.

### B6: Missing File is Not an Error

If `intake-queue.jsonl` does not exist (first triage session), the skill proceeds
normally with an empty open items list — no error is raised.

## Pass Criteria

B1–B6 must all be satisfied. Surfacing resolved items as open is a failing eval.
