# Eval: intake dual-writes discovered work via discovered-from edge

**Skill:** intake
**Behavior under test:** When intake captures a new story and beads is active, it calls
`bd create "<title>" --deps discovered-from:<origin-bead-id>` using the `discovered-from`
edge type (not a generic `blocks` edge). The origin bead ID is resolved from
`.momentum/beads-id-map.json` using the source story slug. The existing `intake-queue.jsonl`
append is NOT removed — this is additive dual-write.

---

## Scenario

### Input

A developer is working on story `sprint-planning-improvement` (bead ID `bd-a3f8abc`).
During development, they discover a follow-up story: "Add validation to sprint activation."

Intake is invoked with the discovered story context.

`.momentum/beads-id-map.json` contains:
```json
{ "sprint-planning-improvement": "bd-a3f8abc" }
```

### Expected Behavior

1. Intake writes the stub file `.momentum/stories/add-validation-sprint-activation.md`.
2. Intake appends to `intake-queue.jsonl` (unchanged from pre-spike behavior).
3. Intake resolves the origin bead ID: `bd-a3f8abc` (from `beads-id-map.json` for `sprint-planning-improvement`).
4. Intake calls: `bd create "Add validation to sprint activation" --deps discovered-from:bd-a3f8abc`
5. The new bead's ID is written back to `beads-id-map.json`: `{ "sprint-planning-improvement": "bd-a3f8abc", "add-validation-sprint-activation": "<new-bead-id>" }`.

### Edge Type Validation

```bash
NEW_BEAD_ID=$(cat .momentum/beads-id-map.json | python3 -c "import sys,json; m=json.load(sys.stdin); print(m['add-validation-sprint-activation'])")
bd show $NEW_BEAD_ID
# Expected: deps field shows "discovered-from: bd-a3f8abc" — NOT "blocks: ..."
```

The `discovered-from` edge type is semantically distinct from `blocks`. This eval fails if
the dep type is `blocks` instead of `discovered-from`.

---

## Scenario B: No origin bead ID available

### Input

Intake captures a story where the origin story slug is unknown or not in `beads-id-map.json`.

### Expected Behavior

1. Intake uses a sentinel `bd-discovery-root` bead as the origin.
2. `bd create "<title>" --deps discovered-from:bd-discovery-root`
3. The `bd-discovery-root` bead must exist in the beads DB (created during spike initialization).

---

## Verification

- `bd show <new-bead-id>` shows dep type `discovered-from`, not `blocks`.
- `intake-queue.jsonl` still has the new entry (additive, not replaced).
- `beads-id-map.json` has the new slug → bead ID mapping.
- Sprint-dev AC 11 validates this: `bd show <bead-id>` inspects deps field type and confirms semantic distinction.
