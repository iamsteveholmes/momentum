# Eval: Declined Offer Not Resurfaced

## Scenario

**Given** a `journal.jsonl` with an open thread `T-002` (story 4.2, phase `mid-review`, last active 5 days ago — dormant) whose last entry contains a `declined_offers` array with one entry:
```json
{
  "offer_type": "dormant-closure",
  "description": "Close dormant thread: Story 4.2 implementation",
  "declined_at": "2026-03-22T10:00:00Z",
  "context_hash": "T-002|4.2|mid-review|abc123"
}
```

**And** the current context produces the same `context_hash` (`T-002|4.2|mid-review|abc123` — same thread, same story, same phase, same spec file hash),

**When** Impetus reaches Step 11 and runs dormant thread hygiene checks,

**Then** Impetus should NOT surface a dormant-closure offer for thread T-002. The guard clause should detect the matching `offer_type` + `context_hash` in `declined_offers` and suppress the offer.

## What to Observe

- The dormant thread hygiene check (Step 11) does NOT produce a "Close this thread?" prompt for the declined thread.
- Other hygiene checks (concurrent tab, dependency-satisfied, unwieldy triage) still run normally.
- The thread still appears in the thread listing (it is open, just not offered for closure).
