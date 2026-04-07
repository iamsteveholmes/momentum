# Eval: Sprint Dev Skill — Phase Coverage

## Setup
Walk through the sprint-dev workflow end-to-end.

## Expected Behavior — All Phases Reachable
1. Phase 0: Task tracking setup — create phase-level and story-level tasks
2. Phase 1: Initialization — read sprint record, validate locked, build dependency graph
3. Phase 2: Dev Wave — spawn dev agents for unblocked stories
4. Phase 3: Progress Tracking — monitor completion, propose merges, unblock next wave
5. Phase 4: Post-Merge AVFL — stop gate: findings presented, no fixes spawned
6. Phase 4b (step 4.1): Per-Story Code Review — independent code-reviewer per merged story
7. Phase 4c (step 4.2): Consolidated Fix Queue — merge AVFL + code review findings, developer fix/defer
8. Phase 4d (step 4.3): Targeted Fixes + Selective Re-review — spawn fix agents, re-run affected reviewers
9. Phase 5: Team Review — QA + E2E Validator + Architect Guard in parallel
10. Phase 6: Verification — developer-confirmation checklist from Gherkin specs
11. Phase 7: Sprint Completion — archive sprint, merge to main, summary

## Verification
Each phase must be reachable in sequence. The workflow file must contain all phases (0-7 including sub-phases 4.1, 4.2, 4.3).
Note: Phase 0 is task tracking setup. Phases 4b/4c/4d are sub-phases of the review orchestration pipeline.
