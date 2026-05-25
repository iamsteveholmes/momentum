# Eval: Phase 2 dedup fan-out uses parallel single-message spawning

## Scenario

Given a triage batch of 8 incoming items that produce 2 clusters after Phase 1 clustering (cluster A with 4 items, cluster B with 4 items), the orchestrator reaches Phase 2.

## Expected Behaviors

The orchestrator spawns BOTH dedup subagents in a SINGLE message (parallel foreground agents). It does NOT:
- Spawn agent A, wait for it to finish, then spawn agent B sequentially
- Use TeamCreate or SendMessage
- Process clusters one by one in a loop

Each spawned agent receives only its cluster's items plus the union of prefiltered shortlists for those cluster members (not the full backlog). Each agent returns a JSON array of per-theme findings conforming to the schema with fields: `source_item_id`, `theme`, `match_type`, `matched_story_slug`, `evidence`, `recommended_action`, `consolidation_hint`.

The orchestrator collects both JSON arrays before proceeding to Phase 3.
