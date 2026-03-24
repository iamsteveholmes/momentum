# Eval: Declined Offer Resurfaced on Context Change

## Scenario

**Given** a `journal.jsonl` with an open thread `T-002` (story 4.2, last active 5 days ago — dormant) whose last entry contains a `declined_offers` array with one entry:
```json
{
  "offer_type": "dormant-closure",
  "description": "Close dormant thread: Story 4.2 implementation",
  "declined_at": "2026-03-22T10:00:00Z",
  "context_hash": "T-002|4.2|mid-review|abc123"
}
```

**And** the current context produces a DIFFERENT `context_hash` (`T-002|4.2|late-review|def456` — phase has advanced and spec file hash differs),

**When** Impetus reaches Step 11 and runs dormant thread hygiene checks,

**Then** Impetus SHOULD surface the dormant-closure offer for thread T-002 because the context has materially changed since the declination.

## What to Observe

- The dormant thread hygiene check produces a "Close this thread?" prompt for T-002.
- The re-offer is permitted because the `context_hash` no longer matches the declined entry.
