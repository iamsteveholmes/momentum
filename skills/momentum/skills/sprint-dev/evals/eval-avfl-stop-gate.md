# Eval: AVFL Stop Gate

**Behavior:** AVFL must run to completion and present all findings before any fix agents are spawned. No fix actions occur during Phase 4 — all fixes are deferred to Phase 4c/4d.

## Input

Sprint execution has reached Phase 4. AVFL has completed and returned a findings report containing:
- 2 critical findings (unused variable references, broken import path)
- 1 high finding (missing error handler in async function)
- 1 medium finding (style inconsistency in parameter naming)

The workflow is processing the AVFL output.

## Expected Behavior

1. **Stop gate fires**: The workflow presents ALL AVFL findings to the developer in a consolidated read-only report before any action is proposed.
2. **No fix spawns in Phase 4**: The workflow does NOT spawn fix agents in this step. It does NOT ask "address before Team Review?" in Phase 4.
3. **Developer acknowledgement required**: The workflow asks the developer to acknowledge receipt of findings before proceeding to Phase 4b.
4. **Findings stored for consolidation**: All findings (critical, high, medium) are preserved with severity and source tags for Phase 4c consolidation.
5. **Transition to Phase 4b**: After acknowledgement, the workflow proceeds to per-story code review — NOT directly to fix spawning.

## Anti-Patterns (Must Not Occur)

- Spawning fix agents inside Phase 4 immediately after AVFL runs
- Presenting findings and asking "fix now or proceed?" without a deliberate stop gate
- Dropping medium/low findings before Phase 4c consolidation
- Proceeding to Phase 4b without developer acknowledgement of AVFL findings

## Verification

The eval passes if:
- Phase 4 ends with a findings report presented and developer acknowledgement received
- No fix agents were spawned in Phase 4
- All 4 findings (2 critical, 1 high, 1 medium) carry through to Phase 4c
