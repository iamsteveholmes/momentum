# Eval: sprint-dev derives dependency ordering from waves and stories/index.json

**Eval ID:** eval-sprint-dev-derives-ordering-from-waves  
**Sprint-dev workflow version:** post DEC-012 (fix-per-sprint-json-contract-drift)

## Scenario

Given a workspace where:
- `sprints/index.json` contains an `active` block with:
  ```json
  {
    "slug": "sprint-2026-04-27",
    "status": "active",
    "locked": true,
    "waves": [
      { "wave": 1, "stories": ["story-a"] },
      { "wave": 2, "stories": ["story-b", "story-c", "story-d"] }
    ],
    "stories": ["story-a", "story-b", "story-c", "story-d"]
  }
  ```
- `stories/index.json` contains entries for all four stories with `depends_on: []` for each (no explicit cross-story dependencies beyond what the wave grouping implies)
- All four stories have status `ready-for-dev`

## Expected Behavior

The sprint-dev workflow's dependency-graph construction step should:

1. Bind `{{sprint_waves}}` from `active.waves` — this is the **primary** ordering source.
2. Bind `{{story_depends_on_map}}` from `stories/index.json` `depends_on` arrays — this is the **secondary** cross-wave detail source.
3. Compute the dependency graph as follows:
   - **story-a** (wave 1): unblocked at start — no predecessors.
   - **story-b**, **story-c**, **story-d** (wave 2): blocked until story-a (the sole wave-1 story) reaches `done` status.
4. Identify **story-a** as the only initially-unblocked story for Phase 2 dev spawning.
5. Identify **story-b**, **story-c**, **story-d** as blocked (pending wave-1 completion).
6. **Never** reference a `dependencies` field on the sprint record (no such field exists on the `active` block by design).
7. **Never** reference a per-sprint `sprints/{slug}.json` file for ordering information.

## Pass Criteria

The eval passes if the described agent behavior:
- Identifies story-a as the only unblocked story in the initial state
- Identifies story-b, story-c, story-d as blocked on story-a (wave-1) completion
- Derives ordering from `active.waves` (primary) and `stories/index.json` `depends_on` (secondary)
- Does not reference a `dependencies` field on the sprint record
- Does not reference any per-sprint file for ordering

## Fail Criteria

The eval fails if the described agent behavior:
- Treats all four stories as unblocked (ignores wave ordering)
- References a `dependencies` object on the sprint record
- Attempts to read ordering from a per-sprint file
- Incorrectly blocks story-a or treats wave-1 stories as dependent on wave-2 stories

## Notes

Tests the wave-based ordering derivation fix. The old workflow referenced `{{sprint_dependencies}}` from a `dependencies` field on the per-sprint record — a field that has never existed. The new workflow derives ordering from `active.waves` (each wave N story is blocked until all wave N-1 stories are `done`) supplemented by per-story `depends_on` arrays from `stories/index.json`.
