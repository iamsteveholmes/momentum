# Eval: Refine Skill — Two-Wave Planning Artifact Discovery and Update

## Setup
Invoke `/momentum:refine` on a project that has `_bmad-output/planning-artifacts/prd.md`
and `_bmad-output/planning-artifacts/architecture.md`, with `stories/index.json`
containing at least 5 completed stories whose requirements are reflected in the PRD
but whose completion status has not been updated in the planning documents.

## Expected Behavior

### Wave 1 — Discovery (parallel)
1. The skill spawns exactly two discovery subagents in parallel (not sequentially):
   - A PRD coverage agent that reads prd.md and stories/index.json
   - An architecture coverage agent that reads architecture.md and stories/index.json
2. Each agent identifies requirements or decisions that are missing, outdated, or no
   longer accurate given completed work
3. Each agent returns structured findings:
   `[{id, description, action_needed (add/update/remove), rationale}]`
4. Both agents return before findings are presented to the developer

### Gate — Conditional Wave 2
5. If neither agent finds required updates, wave 2 is skipped entirely and the
   workflow proceeds to step 4 (status hygiene)
6. If only one agent finds gaps, only that document's update agent fires in wave 2 —
   the other document's update agent does NOT run
7. The developer is presented with wave 1 findings and must approve before wave 2
   runs — wave 2 is NOT automatic

### Wave 2 — Update (conditional per document)
8. After developer approval, update subagents are spawned only for documents that
   had findings:
   - PRD update agent: sole writer of prd.md, applies approved changes
   - Architecture update agent: sole writer of architecture.md, applies approved changes
9. Both update agents can run in parallel if both documents need updates
10. The orchestrator (refine workflow) does NOT use Edit or Write on planning
    artifact files — only the spawned update subagents write to those files

## Verification
- Confirm wave 1 agents run in parallel (two Agent tool calls in the same message)
- Confirm the developer sees findings and explicitly approves before wave 2 starts
- Confirm wave 2 fires only for documents that had findings, not both automatically
- Confirm the refine workflow itself never calls Edit or Write on prd.md or
  architecture.md — only delegated subagents do
