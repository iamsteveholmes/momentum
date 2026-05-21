# Eval: Retro Phase 5 Never Invokes momentum:distill

## Purpose

Verify that `momentum:retro` Phase 5 never invokes `momentum:distill` and does not reference
`{{distill_candidates}}` or related template variables, regardless of what priority action items
are present in the retro findings.

## Scenario

A developer runs a full retro session. Phase 4 produces a retro-transcript-audit.md with
the following "Priority Action Items" — deliberately crafted to match what previously would
have been classified as Tier 1 (single-sentence rule addition, one file, signal_type set):

1. "Add a note to model-routing.md clarifying that model: frontmatter pins family, not tier"
   - signal_type: Instruction
   - recommended_change: "One sentence appended to model-routing.md"

Phase 5 is invoked.

## Expected Behaviors

### B1: No Distill-Related Variables or Logic

Phase 5 does not:
- Compute `distill_candidates`
- Reference `distilled_dispositions`
- Check `if distill_candidates is not empty`
- Classify items as "Tier 1" or "Tier 2" for distill routing purposes
- Output a distill count in any summary

### B2: Item Routes to Stub Proposal

The item about model-routing.md is presented as a story stub proposal — even though it
matches all former Tier 1 heuristics (single file, single sentence, signal_type set).
The developer is asked to approve or decline the stub.

### B3: Phase 5 Completes Without Distill

Phase 5 concludes with an output that includes only "Stubbed" and "Skipped" counts.
The word "distill" does not appear in Phase 5 output at all.

### B4: Phase 5.5 Note Cleaned

Phase 5.5 (handoff to intake-queue) does not reference "findings already routed to distill".
Any item rejected by the developer in Phase 5 appears in `{{handoff_items}}` for possible
handoff to the intake queue.

### B5: Phase 5.5 Language Clean

In Phase 5.5, the output for empty handoff items says "all Priority Action Items were
stubbed" — not "stubbed or distilled".

---

## Pass Criteria

- [ ] `distill_candidates` variable is never populated or referenced
- [ ] `distilled_dispositions` variable is never populated or referenced
- [ ] No `momentum:distill` invocation in Phase 5 output or action sequence
- [ ] Item routes to stub proposal regardless of signal_type value
- [ ] Phase 5 summary output contains no "Distilled" count
- [ ] Phase 5.5 does not reference "routed to distill"
- [ ] Phase 5.5 empty-handoff message says "stubbed" not "stubbed or distilled"

## Failure Criteria

- Phase 5 outputs any "Distilled: N" summary count
- Phase 5 invokes momentum:distill for any reason
- Phase 5 classifies any item as Tier 1 for distill routing
- Phase 5.5 references "findings already routed to distill"
- Phase 5.5 says "stubbed or distilled"
