# Eval: Bootstrap Synthesizes Feature List

Given a project with PRD, epics, architecture, and stories but no `_bmad-output/planning-artifacts/features.json` file (or a features.json with fewer than 3 entries), the skill should:

1. Announce "bootstrap" mode before producing any analysis output or spawning subagents
2. Spawn exactly 2 subagents in a single message (Agent A reading PRD + epics.md; Agent B reading architecture.md + stories/index.json) and wait for both before proceeding
3. Synthesize between 8 and 25 candidate features from the merged subagent findings; if the count falls outside this range, emit a `! WARNING: N candidates outside 8–25 range` notice
4. Include a multi-paragraph `value_analysis` on every candidate covering: (a) current value delivered, (b) full vision including new capabilities beyond pain removal, and (c) known gaps
5. Include a `system_context` string on every candidate explaining how the feature fits and enhances the overall product
6. Not write or modify `features.json` until the developer reaches the Step 5 approval gate and explicitly confirms with "Y"
