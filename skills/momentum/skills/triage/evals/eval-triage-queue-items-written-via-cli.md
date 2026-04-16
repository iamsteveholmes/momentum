# Eval: Triage Writes SHAPING/DEFER/REJECT Items via CLI to intake-queue.jsonl

## Purpose

Verify that `momentum:triage` writes SHAPING, DEFER, and REJECT items to
`intake-queue.jsonl` via the `momentum-tools intake-queue append` CLI command —
never by direct Write or Edit of the JSONL file.

## Scenario

A developer invokes `/momentum:triage` and the following items are approved after
batch-approval:

- "There's a vague idea about AI-assisted code review workflow" → SHAPING (approved)
- "Revisit the multi-workspace cmux integration after the current sprint" → DEFER (approved)
- "The old triage-inbox.md design" → REJECT (approved)

## Expected Behaviors

### B1: SHAPING → kind: shape

For the SHAPING item, triage runs:
```
python3 skills/momentum/scripts/momentum-tools.py intake-queue append \
  --kind shape \
  --title "..." \
  --description "..." \
  --source "triage"
```

The event written to `intake-queue.jsonl` has `kind: "shape"` and `status: "open"`.

### B2: DEFER → kind: watch

For the DEFER item, triage runs the same CLI with `--kind watch`.
The event written has `kind: "watch"` and `status: "open"`.

### B3: REJECT → kind: rejected

For the REJECT item, triage runs the CLI with `--kind rejected`.
The event written has `kind: "rejected"`.

### B4: CLI — Not Direct Write

Triage does NOT use the Write or Edit tool to append to `intake-queue.jsonl` directly.
The CLI is the sole write path for queue events.

### B5: Event Schema

Each written event contains at minimum:
- `id`: short unique identifier
- `kind`: one of {shape, watch, rejected, handoff}
- `title`: non-empty string
- `description`: non-empty string
- `source`: one of {triage, retro, assessment}
- `status`: "open" on initial write
- `timestamp`: ISO-8601 UTC timestamp

### B6: Summary Reports Queue Counts

The final summary output includes the count of items written to each queue kind:
- "N shaping (kind: shape)"
- "N deferred (kind: watch)"
- "N rejected (kind: rejected)"

## Pass Criteria

B1–B6 must all be satisfied. Direct file writes to intake-queue.jsonl is an automatic failure.
