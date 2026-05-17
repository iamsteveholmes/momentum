# Eval: sprint-manager spec-id linkage holds for all story beads

**Skill:** sprint-manager
**Behavior under test:** Every bead created by sprint-manager for a Momentum story
includes `--spec-id .momentum/stories/{slug}.md`, and `bd show <bead-id>` confirms
`spec_id` equals the correct `.md` path. No story spec prose is stored in the Dolt bead body.

---

## Scenario

### Input

Sprint-manager creates a bead for story slug `example-feature-story`.

### Expected Behavior

1. `bd create "Example Feature Story" --type task --spec-id .momentum/stories/example-feature-story.md` is called.
2. `bd show <bead-id>` returns a bead where:
   - `spec_id` == `.momentum/stories/example-feature-story.md`
   - The bead body/description does NOT contain acceptance criteria prose, dev notes, or task lists (those live only in the `.md` file)
3. The same pattern holds for epic-type beads — `bd create "<epic-title>" --type epic` (epics do not use `--spec-id`).
4. The bead ID is recorded in `.momentum/beads-id-map.json`.

### Failure Modes to Test

- `--spec-id` is omitted from the `bd create` call: eval fails — the bead lacks linkage.
- Story prose appears in the bead body: eval fails — spec content must stay in the `.md` file.

---

## Verification Steps

```bash
BEAD_ID=$(cat .momentum/beads-id-map.json | python3 -c "import sys,json; m=json.load(sys.stdin); print(m['example-feature-story'])")
bd show $BEAD_ID | grep spec_id
# Expected output: spec_id: .momentum/stories/example-feature-story.md

bd show $BEAD_ID | grep -c "acceptance criteria"
# Expected: 0 (no AC prose in the bead)
```
