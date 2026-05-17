# Eval: sprint-dev Phase 1 uses bd ready --json --claim for dependency resolution

**Skill:** sprint-dev
**Behavior under test:** After building the `{{story_depends_on_map}}` from `index.json`,
sprint-dev Phase 1 calls `bd ready --json --claim` as the primary source for unblocked
stories. The `--claim` flag provides atomic acquisition. Falls back to wave/depends_on
graph if `bd ready` errors or returns empty.

---

## Scenario A: Normal path — bd ready returns unblocked stories

### Input

A sprint with two stories: `story-a` (no deps, Wave 1) and `story-b` (depends on `story-a`, Wave 2).
`story-a` status: `ready-for-dev`.
`story-b` status: `ready-for-dev` but blocked by `story-a`.

In beads: `story-a` bead has no blockers; `story-b` bead has `blocks: story-a-bead-id`.

### Expected Behavior

1. Sprint-dev calls `bd ready --json --claim` and receives `[{ "id": "<story-a-bead-id>", "title": "Story A" }]`.
2. Sprint-dev resolves the bead ID to slug `story-a` via `.momentum/beads-id-map.json`.
3. Sprint-dev uses `story-a` as the single unblocked story to spawn a dev agent.
4. `story-b` is NOT spawned — it is blocked.
5. The `--claim` ensures `story-a` is atomically marked as claimed — a second concurrent call receives empty or a different story.

### Atomic Acquisition Test

```bash
# Run two concurrent bd ready --claim calls with one unblocked story
bd ready --json --claim &; bd ready --json --claim
# Expected: only one call receives story-a; the other receives []
```

---

## Scenario B: Fallback path — bd ready returns empty or errors

### Input

Same sprint state, but `bd ready --json --claim` returns `[]` or exits non-zero.

### Expected Behavior

1. Sprint-dev detects empty/error result.
2. Sprint-dev falls back to wave/depends_on graph from `{{sprint_waves}}` and `{{story_depends_on_map}}`.
3. The fallback is marked with a comment in workflow.md:
   `<!-- SPIKE: falls back to wave/depends_on if bd ready --claim unavailable -->`
4. The sprint continues correctly with `story-a` as the unblocked story from the fallback graph.
5. A log note records that the beads layer was unavailable.

---

## Verification

- `bd ready --json --claim` call appears in Phase 1 action sequence.
- Result is stored as `{{bd_ready_result}}`.
- Discrepancies between `{{bd_ready_result}}` and wave graph are logged.
- Fallback trigger condition is clearly tested (empty array or non-zero exit).
