# Eval: Triage Writes SHAPING/DEFER/REJECT Items via CLI to practice-ledger.jsonl

## Purpose

Verify that `momentum:triage` writes SHAPING, DEFER, and REJECT items to
`practice-ledger.jsonl` via the `momentum-tools practice-ledger append` CLI command —
never by direct Write or Edit of the JSONL file.

## Scenario

A developer invokes `/momentum:triage` and the following items are approved after
batch-approval:

- "There's a vague idea about AI-assisted code review workflow" → SHAPING (approved)
- "Revisit the multi-workspace cmux integration after the current sprint" → DEFER (approved)
- "The old triage-inbox.md design" → REJECT (approved)

## Setup

Seed the ledger with no pre-existing entries for these entity IDs:
```bash
# Ensure practice-ledger.jsonl exists but has no conflicting entries
python3 skills/momentum/scripts/momentum-tools.py practice-ledger summary
```

## Expected Behaviors

### B1: SHAPING → event_type: created with triage_class: shaping

For the SHAPING item, triage runs:
```
python3 skills/momentum/scripts/momentum-tools.py practice-ledger append \
  --event-type created \
  --entity-id "triage-<short-id>" \
  --source "triage" \
  --actor "triage" \
  --payload '{"triage_class":"shaping","title":"...","description":"..."}'
```

The event appended to `practice-ledger.jsonl` has `event_type: "created"` and
`payload.triage_class: "shaping"`. The entity remains open (non-terminal event_type).

Verify: `practice-ledger open` returns the entity.

### B2: DEFER → event_type: created with triage_class: defer

For the DEFER item, triage runs the same CLI with `--event-type created` and
`--payload '{"triage_class":"defer","title":"...","description":"..."}'`.
The event has `event_type: "created"` and `payload.triage_class: "defer"`.

Verify: `practice-ledger open` returns the entity.

### B3: REJECT → event_type: rejected

For the REJECT item, triage runs the CLI with `--event-type rejected` and
`--payload '{"reason":"...","title":"...","description":"..."}'`.
The event has `event_type: "rejected"`.

Verify: `practice-ledger open` does NOT return this entity (rejected is terminal).

### B4: CLI — Not Direct Write

Triage does NOT use the Write or Edit tool to append to `practice-ledger.jsonl` directly.
The CLI is the sole write path for ledger events.

### B5: Event Schema

Each written event contains at minimum:
- `event_id`: short unique identifier
- `entity_id`: identifier for the logical entity being tracked
- `event_type`: one of the DEC-033 D3 seven-value enum (`created`, `updated`, `consumed`,
  `rejected`, `closed_stale`, `reopened`, `custom`)
- `ts`: ISO-8601 UTC timestamp
- `source`: "triage"
- `payload`: JSON object; for SHAPING/DEFER includes `triage_class`; for REJECT includes `reason`

### B6: Summary Reports Ledger Counts

The final summary output includes the count of items written per class:
- "N shaping (event_type: created, triage_class: shaping)"
- "N deferred (event_type: created, triage_class: defer)"
- "N rejected (event_type: rejected)"

## Pass Criteria

B1–B6 must all be satisfied. Direct file writes to `practice-ledger.jsonl` is an automatic failure.
Any use of the legacy CLI subcommand (pre-DEC-033) or the `kind:` schema field is an automatic failure.
