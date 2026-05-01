# Eval: sprint-dev reads active block from sprints/index.json only

**Eval ID:** eval-sprint-dev-reads-active-block-only  
**Sprint-dev workflow version:** post DEC-012 (fix-per-sprint-json-contract-drift)

## Scenario

Given a workspace where:
- `sprints/index.json` contains a populated `active` block with `slug: "sprint-2026-04-27"`, `status: "active"`, `locked: true`, `waves: [{wave: 1, stories: ["story-a"]}]`, and a valid `team.story_assignments` object
- No file `sprints/sprint-2026-04-27.json` exists on disk (nor any other per-sprint JSON file in the sprints/ directory)
- The current git branch is `sprint/sprint-2026-04-27`

## Expected Behavior

The sprint-dev workflow's Phase 1 (Initialization) should:

1. Read `sprints/index.json` and bind `{{sprint_record}}` to the `active` block.
2. Verify that `active.slug == "sprint-2026-04-27"` — matching `{{sprint_slug}}` — before proceeding.
3. Verify that `active.locked == true` before proceeding.
4. Extract `{{sprint_stories}}`, `{{team}}`, and `{{sprint_waves}}` from the `active` block.
5. Proceed to read `stories/index.json` for per-story `depends_on` detail.
6. Proceed to dependency-graph construction without halting.
7. **Never** attempt to read, reference, or check for `sprints/sprint-2026-04-27.json` or any file matching `sprints/{slug}.json`.

## Pass Criteria

The eval passes if the described agent behavior:
- Reads only `sprints/index.json` (the active block) for sprint-level state
- Does not reference or attempt to read a per-sprint JSON file
- Does not produce a HALT or error related to a missing per-sprint file
- Successfully binds sprint state from the `active` block and proceeds to dependency-graph construction

## Fail Criteria

The eval fails if the described agent behavior:
- Attempts to read `sprints/sprint-2026-04-27.json` or any `sprints/{slug}.json`
- HALTs with an error about a missing per-sprint file
- Derives sprint state from any source other than `sprints/index.json` `active` block

## Notes

Tests the primary correctness property of the DEC-012 workflow fix: Phase 1 must be exclusively grounded in the holistic `sprints/index.json` `active` block. The per-sprint file has never been written by `momentum-tools.py` and must not be expected.
