# Story 1.8: Orchestrator Purity Principle

Status: ready-for-dev

## Story

As an architect,
I want a formal architecture decision establishing that Impetus is a pure orchestrator,
so that the development, evaluation, testing, and validation roles remain structurally separated from orchestration.

## Acceptance Criteria

**AC1 — Architecture Decision exists:**
Given the architecture document (`_bmad-output/planning-artifacts/architecture.md`),
When an architect or developer reads the decisions section,
Then a formal Architecture Decision exists stating that Impetus is a pure orchestrator
And the decision explicitly prohibits Impetus from performing development, evaluation, testing, or validation
And the decision specifies that all non-orchestration work must be delegated to purpose-specific subagents

**AC2 — context:fork evaluation documented:**
Given the orchestrator purity decision,
When a developer reviews the `context:fork` evaluation,
Then the decision documents whether `bmad-dev-story` invocation should use `context:fork` isolation
And the rationale for the chosen approach is recorded

**AC3 — Story 2.1 constraint ACs added:**
Given the orchestrator purity decision,
When a developer reviews Story 2.1 acceptance criteria,
Then Story 2.1 contains constraint ACs that enforce the orchestrator purity principle
And the constraints are traceable to the architecture decision

**AC4 — Verification artifact exclusion mechanism:**
Given acceptance test and eval files exist for a story,
When the dev agent is working on implementation,
Then the file storage convention or flagging mechanism ensures the dev agent can explicitly exclude verification artifacts from its context

## Tasks / Subtasks

- [ ] Task 1: Add formal Architecture Decision to architecture.md (AC: 1)
  - [ ] 1.1: Draft Architecture Decision (new Decision number in sequence) titled "Orchestrator Purity Principle"
  - [ ] 1.2: State the decision: Impetus is a pure orchestrator — it MUST NOT perform development, evaluation, testing, or validation
  - [ ] 1.3: Enumerate the prohibited roles explicitly: code writing, test execution, eval running, code review, findings generation
  - [ ] 1.4: State the delegation rule: all non-orchestration work is dispatched to purpose-specific subagents (code-reviewer, dev-story agent, VFL, architecture-guard)
  - [ ] 1.5: Reference the existing hub-and-spoke voice contract (Decision 3b) as the communication pattern that enforces purity — subagents return structured output; Impetus synthesizes

- [ ] Task 2: Evaluate and document context:fork for bmad-dev-story invocation (AC: 2)
  - [ ] 2.1: Analyze whether `bmad-dev-story` invocation from Impetus should use `context:fork` isolation
  - [ ] 2.2: Document the tradeoffs: fork provides isolation (dev agent can't pollute orchestrator context) but loses shared state; flat skill in main context allows Impetus to observe progress but risks context contamination
  - [ ] 2.3: Record the recommendation and rationale within the Architecture Decision from Task 1
  - [ ] 2.4: If recommending fork, document how Impetus communicates story context to the forked dev agent (file-based handoff vs. parameter passing)

- [ ] Task 3: Add orchestrator purity constraint ACs to Story 2.1 (AC: 3)
  - [ ] 3.1: Read the current Story 2.1 file (`_bmad-output/implementation-artifacts/2-1-impetus-skill-created-with-correct-persona-and-input-handling.md`)
  - [ ] 3.2: Add a new AC (AC5 or next available number) that enforces orchestrator purity: Impetus must not contain any development, evaluation, testing, or validation logic
  - [ ] 3.3: Add traceability reference back to the Architecture Decision created in Task 1
  - [ ] 3.4: Ensure the constraint AC is testable — it should be verifiable by inspecting `skills/momentum/workflow.md` for absence of prohibited behaviors

- [ ] Task 4: Define verification artifact exclusion convention (AC: 4)
  - [ ] 4.1: Define the file storage convention for acceptance tests and evals (e.g., `evals/` directories within skill packages, `tests/acceptance/` at project level)
  - [ ] 4.2: Document how the dev agent should exclude these paths — either via `.claude/rules/` exclusion rule, `allowed-tools` path restriction, or explicit instruction in the dev-story workflow
  - [ ] 4.3: Add the convention to the Architecture Decision from Task 1
  - [ ] 4.4: Ensure the convention is consistent with the existing PreToolUse file protection pattern (FR19, FR21) that blocks modifications to acceptance test directories

## Dev Notes

### Architecture Context

The orchestrator purity principle formalizes what is already implied by several existing architecture decisions but never explicitly stated as a standalone constraint:

- **Decision 3b (Hub-and-Spoke Voice Contract)** — Impetus is the sole user-facing voice; subagents return structured output. This implies delegation but doesn't prohibit Impetus from also doing work.
- **Decision 3a (VFL Parallel Execution)** — VFL runs in main context, spawns reviewer subagents. The pattern is orchestrate-then-delegate.
- **Subagent Composition (Architecture Principle 5)** — code-reviewer and architecture-guard use `context:fork` for producer-verifier isolation. But the architecture doesn't yet say Impetus itself must never be a producer.
- **Decision 4c (Productive Waiting)** — While a `context:fork` subagent runs in background, Impetus maintains dialogue. This is an orchestration behavior, not a production behavior.

The new decision should be positioned as a formalization of these existing patterns into an explicit constraint, not a new direction.

### context:fork Considerations

Key factors for the `bmad-dev-story` invocation evaluation:
- `context:fork` creates exactly one isolated subagent per invocation (Architecture doc explicitly states this)
- `context:fork` is Claude Code-exclusive (confirmed in deployment constraints section)
- Dev-story sessions are long-running and produce many file changes — isolation prevents the orchestrator context from growing with implementation details
- Counter-argument: flat skill invocation lets Impetus observe and report progress in real-time (productive waiting pattern)
- Existing precedent: code-reviewer and architecture-guard already use `context:fork` for producer-verifier isolation

### Files to Modify

1. `_bmad-output/planning-artifacts/architecture.md` — Add new Architecture Decision
2. `_bmad-output/implementation-artifacts/2-1-impetus-skill-created-with-correct-persona-and-input-handling.md` — Add constraint AC
3. `_bmad-output/planning-artifacts/epics.md` — No changes needed (Epic 1b already defines this story)

### What NOT to Do

- Do NOT implement the orchestrator purity enforcement in code — this story is about the architecture decision and spec updates, not implementation
- Do NOT modify any skill workflow files — that is Epic 2's job
- Do NOT create the PreToolUse file protection hook — that is Story 3.2 (FR19, FR21)
- Do NOT modify the VFL skill — the purity principle constrains Impetus, not the VFL orchestration pattern

### Previous Story Intelligence

No Stories 1.6 or 1.7 have been implemented yet (they are part of Epic 1b alongside this story). However, the Epic 1 retrospective (`_bmad-output/implementation-artifacts/epic-1-retro-2026-03-22.md`) is the source material:
- Action Item #7 explicitly calls for this Architecture Decision
- The retro notes that orchestrator purity was not architecturally enforced during Epic 1
- The retro recommends this be in place before Story 2.1 development begins

### Testing Standards

This is a **docs** story — it produces specification and architecture artifacts, not executable code. Verification is by inspection:
- Architecture Decision is present and complete
- context:fork evaluation rationale is documented
- Story 2.1 has been updated with constraint ACs
- Verification artifact exclusion convention is defined and consistent with existing patterns

### Project Structure Notes

- Architecture decisions follow an established numbered sequence in `architecture.md` (Decision 1a, 1b, 1c, 2a, 3a, 3b, 3c, 4a, 4b, 4c, 5a, 5b, 5c, etc.)
- The new decision should use the next available number in the appropriate category (likely 3d or a new category)
- Story 2.1 file is at `_bmad-output/implementation-artifacts/2-1-impetus-skill-created-with-correct-persona-and-input-handling.md`

### References

- [Source: _bmad-output/planning-artifacts/architecture.md — Decision 3a (VFL Parallel Execution)]
- [Source: _bmad-output/planning-artifacts/architecture.md — Decision 3b (Hub-and-Spoke Voice Contract)]
- [Source: _bmad-output/planning-artifacts/architecture.md — Decision 4c (Productive Waiting)]
- [Source: _bmad-output/planning-artifacts/architecture.md — Principle 5 (Subagent Composition)]
- [Source: _bmad-output/planning-artifacts/architecture.md — Deployment Constraints (context:fork is Claude Code-exclusive)]
- [Source: _bmad-output/implementation-artifacts/epic-1-retro-2026-03-22.md — Action Item #7]
- [Source: _bmad-output/planning-artifacts/epics.md — Epic 1b, Story 1.8]

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → unclassified (no Momentum-specific guidance — standard bmad-dev-story DoD applies)
- Task 2 → unclassified (no Momentum-specific guidance — standard bmad-dev-story DoD applies)
- Task 3 → unclassified (no Momentum-specific guidance — standard bmad-dev-story DoD applies)
- Task 4 → unclassified (no Momentum-specific guidance — standard bmad-dev-story DoD applies)

All tasks in this story produce specification and architecture artifacts (markdown documents). No skill instructions, scripts, rules/hooks, or config/structure changes are involved. Standard bmad-dev-story Definition of Done applies without additional Momentum-specific DoD items.

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
