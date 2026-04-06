# Eval: Refine Skill — CLI-Only Mutations (No Direct JSON Edits)

## Setup
Invoke `/momentum:refine`. Approve at least one finding of each applicable type:
a priority change, an epic reassignment, and a story drop.

## Expected Behavior
1. For each approved priority change: the skill runs
   `momentum-tools sprint set-priority --story SLUG --priority LEVEL` via Bash
2. For each approved epic reassignment: the skill runs
   `momentum-tools sprint epic-membership --story SLUG --epic SLUG` via Bash
3. For each approved story drop: the skill runs
   `momentum-tools sprint status-transition --story SLUG --target dropped` via Bash
4. For each approved new story (from coverage gap): the skill invokes
   `momentum:create-story` — it does NOT write a story file directly
5. The skill NEVER uses the Edit or Write tool on `stories/index.json` or any
   `_bmad-output/planning-artifacts/*.md` file
6. Dependency updates are flagged as requiring manual resolution — no CLI command
   is run for them and no direct edit is made
7. Each applied change is logged via `momentum-tools log` with event type `decision`
8. A summary is presented at the end: counts of changes applied by type, stories
   created, findings rejected, and before/after priority distribution

## Verification
Check the Bash invocations — all mutations must go through momentum-tools CLI or
subagent spawns. No direct JSON edits. The Write/Edit tool must not be called on
stories/index.json or planning artifact files at any point during the workflow.
