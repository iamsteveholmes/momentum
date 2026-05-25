# Eval: Step 4 approval UX shows dedup sections before classification

## Scenario

Given a triage session where Phase 2 dedup subagents returned findings including:
- 2 items with `match_type: duplicate` (recommended_action: consume)
- 1 item with 2 per-theme findings (split candidate)
- 1 merge candidate group (2 items with matching `consolidation_hint.target_slug_or_theme`)

The orchestrator reaches Step 4 batch approval.

## Expected Behaviors

The approval output shows THREE sections BEFORE the existing five-class classification block:

1. **Dedup actions** — findings grouped by `recommended_action`. Each finding shows: theme, match_type, matched_story_slug, evidence.

2. **Split candidates** — the 1 item with 2 per-theme findings appears here with both themes listed.

3. **Merge candidates** — the 1 consolidation group appears here labeled "flagged for consolidation analysis (Phase 4 scope — no action available yet)." The orchestrator does NOT attempt to execute any merge operation.

After developer approves dedup actions, items marked as duplicates (consume) are removed from the queue. Surviving items proceed to the existing five-class classification.
