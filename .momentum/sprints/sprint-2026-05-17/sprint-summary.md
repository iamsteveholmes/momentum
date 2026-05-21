# Sprint Summary — sprint-2026-05-17

**Sprint completed:** 2026-05-19
**Retro date:** 2026-05-20

## Stories Completed vs. Planned

5 / 5 stories reached `done`.

| Story | Status |
|---|---|
| enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard | done |
| momentum-harnessjson-schema-and-plugin-shipped-defaults | done |
| e2e-validator-agent-body-rewrite-de-gherkin-harness-driven | done |
| create-story-method-selection-step | done |
| sprint-planning-frozen-per-story-contract-holistic-coverage | done |

## Key Decisions

- DEC-029: Method-Routed Acceptance Validation — Harness Profile, Per-Sprint E2E Coverage, and the Unified Validate-Fix Loop (2026-05-17)
- DEC-030: Dependency-Driven Execution Model — DAG Dispatch, Closeable Value-Groupings, Frozen-Scope Sprints, and the Dual-Format Integrity Split (2026-05-17)

## Unresolved Issues

23 findings written to intake-queue.jsonl (source: retro, kind: handoff) for triage in the next planning cycle. Top three by severity:

1. agents.json defaults block missing architect, pm, sm roles (critical — runtime errors)
2. agent-builder approval gate absent from workflow.md (critical — DoD item not implemented)
3. e2e-validator hardcoded service assumptions block all signal for practice projects (critical — third consecutive sprint with zero E2E signal)

## Narrative

Sprint-2026-05-17 delivered the foundational enforcement layer for method-routed E2E validation: `verification-harness.json` as the project-scoped validation contract, a rewritten e2e-validator that reads the harness instead of assuming Gherkin, a method-selection step in create-story, and frozen per-story validation contracts in sprint-planning. Together these close the gap where the E2E gate produced permanent BLOCKED verdicts due to hardcoded service assumptions. The sprint also produced DEC-029 and DEC-030, two significant architectural decisions governing validation pipeline design and sprint execution semantics. Retro audit found 23 actionable practice gaps — primarily around execution visibility, gate legibility, and carry-forward implementation debt in the agent base bodies — all queued for the next triage cycle.
