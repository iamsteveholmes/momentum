# .momentum/signals/ — Pending Work Signal Ledger

This directory holds pending work flags written by Momentum skills during retro, triage, and AVFL workflows. Impetus reads these at session open to surface outstanding items alongside sprint/story state.

## Schema

### Filename Pattern

```
{signal_type}-{slug-or-timestamp}.json
```

Examples:
- `triage-uncleared-2026-04-26.json`
- `avfl-finding-pending-upstream-fix-canvas-vite-scaffold.json`

### Required Fields

| Field | Type | Description |
|---|---|---|
| `signal_type` | string | One of the recognized signal type values (see below) |
| `origin` | string | The Momentum skill that wrote the signal (e.g., `momentum:retro`) |
| `created` | string (ISO 8601) | Timestamp when the signal was written |
| `payload` | object | Signal-type-specific data (shape varies by signal_type) |

### Optional Fields

| Field | Type | Description |
|---|---|---|
| `cleared` | string (ISO 8601) | Timestamp when the signal was resolved; presence means the signal is cleared |

## Recognized signal_type Values

| Value | Written by | Meaning |
|---|---|---|
| `triage-uncleared` | `momentum:triage` | Triage run produced items that have not been actioned |
| `avfl-finding-pending-upstream-fix` | `momentum:avfl` | AVFL found a finding that requires an upstream fix before it can be resolved |

This list is forward-compatible — new `signal_type` values can be added without schema change.

## Example Signal Files

**triage-uncleared-2026-04-26.json**
```json
{
  "signal_type": "triage-uncleared",
  "origin": "momentum:retro",
  "created": "2026-04-26T10:00:00Z",
  "payload": {
    "items": ["item-1", "item-2"]
  }
}
```

**avfl-finding-pending-upstream-fix-canvas-vite-scaffold.json**
```json
{
  "signal_type": "avfl-finding-pending-upstream-fix",
  "origin": "momentum:avfl",
  "created": "2026-04-26T12:00:00Z",
  "payload": {
    "finding_id": "finding-001",
    "story_slug": "canvas-vite-scaffold"
  }
}
```

## Read Authority

Impetus reads this directory at session open. All `.json` files are read; their `signal_type`, `origin`, and `payload` are surfaced in the situational report if present. An empty directory is a valid state — no warning or error is produced.

## Write Authority

Initial set of authorized signal writers:
- `momentum:retro` — writes `triage-uncleared` signals
- `momentum:triage` — writes `triage-uncleared` signals
- `momentum:avfl` — writes `avfl-finding-pending-upstream-fix` signals

These writers are defined in follow-up stories. This story defines the read contract only.

## State Location

This directory is part of the `.momentum/` state layout established by DEC-011 Decision D3 (State Source Paths Under `.momentum/`). See `_bmad-output/planning-artifacts/decisions/dec-011-project-canvas-implementation-foundations-2026-04-24.md` for the decision record.
