# Eval: Bootstrap Synthesizes Epic List

Given a project with PRD, architecture, and stories but no `_bmad-output/planning-artifacts/epics.json` file (or an epics.json with fewer than 3 entries), the skill should:

1. Announce "bootstrap" mode before producing any analysis output or spawning subagents
2. Spawn exactly 2 subagents in a single message (Agent A reading PRD + stories/index.json; Agent B reading architecture.md + existing epics context) and wait for both before proceeding
3. Synthesize a candidate epic list from the merged subagent findings with multi-paragraph `value_analysis`, `system_context`, typed classification, and verifiable `acceptance_condition` strings on every candidate
4. Not write or modify `epics.json` until the developer reaches the approval gate and explicitly confirms with "Y"
5. Include coverage of both the orphan-resolution/taxonomy work (from the categorical grooming path) and the value-analysis/classification work (from the value-first path) in the bootstrap output
