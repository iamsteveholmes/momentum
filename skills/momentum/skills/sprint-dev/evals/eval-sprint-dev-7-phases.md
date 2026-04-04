# Eval: Sprint Dev Skill — 7-Phase Coverage

## Setup
Walk through the sprint-dev workflow end-to-end.

## Expected Behavior — All 7 Phases Reachable
1. Phase 0: Task tracking setup — create phase-level and story-level tasks
2. Phase 1: Initialization — read sprint record, validate locked, build dependency graph
3. Phase 2: Dev Wave — spawn dev agents for unblocked stories
4. Phase 3: Progress Tracking — monitor completion, propose merges, unblock next wave
5. Phase 4: Post-Merge AVFL — single AVFL scan on full integrated codebase
6. Phase 5: Team Review — QA + E2E Validator + Architect Guard in parallel
7. Phase 6: Verification — developer-confirmation checklist from Gherkin specs
8. Phase 7: Sprint Completion — archive sprint, merge to main, summary

## Verification
Each phase must be reachable in sequence. The workflow file must contain all 7 phases (0-7).
Note: Phase 0 is task tracking setup, so there are 8 steps total covering 7 execution phases.
