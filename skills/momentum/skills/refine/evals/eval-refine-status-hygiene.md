# Eval: Refine Skill — Status Hygiene Detection

## Setup
Invoke `/momentum:refine` on a project where `stories/index.json` contains at least
two stories that meet ALL of the following criteria:
- Status is NOT `done` (e.g., `ready-for-dev` or `in-progress`)
- `story_file: true`
- The story file contains a Dev Agent Record section where every DoD item is checked
  (`[x]`) and no unchecked items (`[ ]`) remain in the File List / DoD section

Also include at least one story where the DoD is NOT fully checked (has `[ ]` items)
to confirm the skill does not flag false positives.

## Expected Behavior
1. The workflow reads each non-terminal story in stories/index.json
2. For stories with `story_file: true`, the workflow reads the actual story file
3. The workflow detects stories where the file shows completion (all DoD items
   checked) but index.json status is not `done`
4. These stories are flagged as status mismatches in the consolidated findings
5. Stories with incomplete DoD (unchecked items) are NOT flagged — no false positives
6. The developer is presented with status mismatch findings and can approve
   transitioning each flagged story to `done`
7. Approved status transitions are applied via:
   `momentum-tools sprint status-transition --story SLUG --target done`
8. The workflow does NOT use Edit or Write on stories/index.json — only
   momentum-tools CLI commands mutate it

## Verification
- Confirm the workflow correctly identifies stories with completed DoD but non-done
  status
- Confirm stories with incomplete DoD are not flagged
- Confirm approved transitions use `momentum-tools sprint status-transition` via Bash
- Confirm no direct Edit/Write calls on stories/index.json
