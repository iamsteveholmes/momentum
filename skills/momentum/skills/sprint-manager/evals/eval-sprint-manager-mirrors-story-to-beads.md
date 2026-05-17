# Eval: sprint-manager mirrors story to beads shadow layer

**Skill:** sprint-manager
**Behavior under test:** When sprint-manager creates or status-transitions a story, it also
dual-writes to the beads layer — creating a bead with the correct status mapping and storing
the bead ID in `.momentum/beads-id-map.json`.

---

## Scenario

### Input

Sprint-manager receives `sprint_plan` action to add story `test-story-slug` to a sprint.

The story has:
- title: "Test Story"
- slug: `test-story-slug`

`.momentum/stories/index.json` has an entry for `test-story-slug` with status `backlog`.

`.beads/` is initialized and `bd list --json` works.

### Expected Behavior

1. Sprint-manager writes the story to `.momentum/sprints/index.json` as the primary JSON write (index.json is authoritative).
2. Sprint-manager calls `bd create "Test Story" --type task --spec-id .momentum/stories/test-story-slug.md`.
3. The resulting bead ID is stored in `.momentum/beads-id-map.json` as `{ "test-story-slug": "<bead-id>" }`.
4. The bead ID can be verified via `bd show <bead-id>` returning a bead with spec_id equal to `.momentum/stories/test-story-slug.md`.
5. If `bd create` fails, sprint-manager logs the failure and does NOT abort the primary JSON write.

### Failure Modes to Test

- `bd create` returns a non-zero exit: sprint-manager completes the `index.json` write and logs beads failure.
- `beads-id-map.json` is missing: sprint-manager creates it with the new entry.

---

## Verification Steps

```bash
# After sprint-manager sprint_plan add for test-story-slug:
cat .momentum/beads-id-map.json | python3 -c "import sys,json; m=json.load(sys.stdin); print(m.get('test-story-slug', 'MISSING'))"
# Expected: a hash ID like "bd-a3f8..."

bd show $(cat .momentum/beads-id-map.json | python3 -c "import sys,json; m=json.load(sys.stdin); print(m['test-story-slug'])")
# Expected: shows bead with spec_id = ".momentum/stories/test-story-slug.md"
```
