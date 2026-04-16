# Eval: Triage Re-surfaces Open Queue Items from intake-queue.jsonl

## Purpose

Verify that `momentum:triage` reads `intake-queue.jsonl` at startup and re-presents
open SHAPING and DEFER items alongside new observations for re-classification.

## Scenario

`intake-queue.jsonl` contains two existing events:
```jsonl
{"id":"iq-20260410100000-abc1","kind":"shape","title":"AI code review workflow idea","description":"...","source":"triage","status":"open","timestamp":"2026-04-10T10:00:00Z"}
{"id":"iq-20260412143000-def2","kind":"watch","title":"Multi-workspace cmux integration","description":"...","source":"triage","status":"open","timestamp":"2026-04-12T14:30:00Z"}
```

The developer also provides one new observation: "Add a retro summary email feature."

## Expected Behaviors

### B1: Open Items Displayed Before New Items

Before asking for new observations (or presenting the classification), triage displays
the two open queue items with `[QUEUED]` prefix or equivalent visual distinction.
Items with `status: "open"` are treated as open.

### B2: Open Items Included in Classification Pass

The two queued items and the new observation are all included in the classification step.
The developer can re-classify any queued item (e.g., promote from SHAPING to ARTIFACT,
change DEFER to REJECT).

### B3: No Re-opening of Resolved Items

A third event with `status: "consumed"` is NOT surfaced as open, even if its kind is "shape"
or "watch".

### B4: Resolve Prompt at End

After batch-approval decisions are made, triage asks whether any open queue items with
no new classification action should be marked as consumed. The developer can provide IDs
to consume.

### B5: Consume via CLI

Items the developer marks as consumed are processed via:
```
python3 skills/momentum/scripts/momentum-tools.py intake-queue consume --id ID
```

Not by direct Edit of the JSONL file.

### B6: Missing File is Not an Error

If `intake-queue.jsonl` does not exist (first triage session), the skill proceeds
normally with an empty open items list — no error is raised.

## Pass Criteria

B1–B6 must all be satisfied. Surfacing consumed items as open is a failing eval.
