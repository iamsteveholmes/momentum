# Story 2.10: Background Agent Coordination Mechanism Validated and Documented

Status: ready-for-dev

## Story

As a developer building Momentum,
I want the background agent coordination mechanism investigated and documented as a research artifact,
so that Architecture Decision 4c's gate is satisfied and Epic 4 Story 4.3 can proceed with a validated technical foundation.

## Acceptance Criteria

**AC1 — Research document exists with actionable findings:**
Given the need for background agent communication in Story 4.3,
When this story completes,
Then a research document exists at `docs/research/background-agent-coordination.md` documenting: (1) what inter-agent communication mechanisms exist (SendMessage, TaskOutput, structured return values, or other) and whether any support checkpoint/resume, (2) reliability/latency/context constraints if yes, (3) alternative pattern if no

**AC2 — Architecture Decision 4c updated:**
Given Architecture Decision 4c's implementation note ("do not implement productive waiting or background VFL execution until spike result is documented"),
When spike results are documented,
Then Decision 4c is updated with actual mechanism or revised approach

**AC3 — Story 2.4 dev notes cross-referenced:**
Given Story 2.4 dev notes acknowledge the gate was not satisfied,
When this story completes,
Then the dev notes reference the research document

## Tasks / Subtasks

- [ ] Task 1: Execute the spike — test SendMessage API for checkpoint/resume (AC: 1)
  - [ ] 1.1: Investigate what inter-agent communication mechanisms Claude Code supports: TaskOutput, SendMessage (if it exists), structured return values, or other
  - [ ] 1.2: Test whether a background agent launched with `run_in_background: true` can receive mid-task communication (checkpoint/resume)
  - [ ] 1.3: Test whether background agents simply run to completion and return structured output, or whether mid-task communication is possible
  - [ ] 1.4: Document reliability, latency, and context constraints for whichever mechanism(s) exist
  - [ ] 1.5: If no mid-task communication mechanism exists, propose an alternative to the checkpoint/resume pattern for Stories 2.4 and 4.3

- [ ] Task 2: Document results as research artifact (AC: 1)
  - [ ] 2.1: Create `docs/research/background-agent-coordination.md` using this required structure:
    ```
    ## Mechanism Investigated
    ## Test Methodology
    ## Results
    ## Constraints and Failure Modes
    ## Recommendation for Story 4.3
    ```
  - [ ] 2.2: Each section must contain concrete findings — not vague summaries. Include specific API calls tested, exact behavior observed, error messages if any, latency measurements if relevant.
  - [ ] 2.3: The Recommendation section must be actionable — enough detail that a developer could implement background agent coordination for Story 4.3 without additional research

- [ ] Task 3: Update Architecture Decision 4c (AC: 2)
  - [ ] 3.1: Read current Decision 4c text in `_bmad-output/planning-artifacts/architecture.md` (line 432)
  - [ ] 3.2: Update the implementation note with spike outcome — replace "Do not implement productive waiting or background VFL execution until spike result is documented" with actual findings and revised guidance
  - [ ] 3.3: If mechanism is unavailable, revise Decision 4c approach and flag impact on Story 4.3

- [ ] Task 4: Cross-reference from Story 2.4 dev notes (AC: 3)
  - [ ] 4.1: Read Story 2.4 dev notes section "Critical Dependency: Story 2.Spike" (line 117 of `_bmad-output/implementation-artifacts/2-4-completion-signals-and-productive-waiting.md`)
  - [ ] 4.2: Add a cross-reference note indicating the spike has been completed and pointing to `docs/research/background-agent-coordination.md`

## Dev Notes

### Root Cause

The spike defined as Story 2.Spike in the epics was never executed. Architecture Decision 4c includes an explicit gate: "Do not implement productive waiting or background VFL execution until spike result is documented." Story 2.4 proceeded anyway — safely, because its ACs (completion signals, productive waiting instructions, subagent synthesis rules) are behavioral skill instructions that don't depend on the checkpoint/resume mechanism. Story 2.4's dev notes explicitly acknowledge this: "The spike has not been completed and no research document exists in `docs/research/`."

However, the gate remains unsatisfied. Epic 4 Story 4.3 (full story cycle with background agents) genuinely depends on knowing whether mid-task communication is possible. Epic 1 Retro #6 flagged this as an action item. The Epic 2 refinement proposal converts it from a spike to a standard story (Story 2.10) so results are captured as committed artifacts.

### Architecture Compliance

| Requirement | Source | How This Story Complies |
|---|---|---|
| Background agent coordination gate | Decision 4c (architecture.md, line 432) | This story satisfies the gate by documenting the spike result |
| Spike result before Story 4.3 | Decision 4c implementation note | Research document blocks Epic 4 Story 4.3 |
| Spike documented in `docs/research/` | Story 2.Spike AC (epics.md, line 726) | Task 2 creates `docs/research/background-agent-coordination.md` |

**Decision 4c full text (architecture.md, lines 432-437):**
> Decision 4c — Productive Waiting
> While a context:fork subagent runs in background, Impetus maintains dialogue on the same topic. Background execution (confirmed: Claude Code subagents explicitly support foreground/background modes) means the main conversation is not blocked — Impetus can continue responding to the user while isolated agents run concurrently. Default: surface implementation summary ("here's what was built and how it maps to the ACs"). Dead air is a failure mode, not an acceptable pause.
> **Implementation note:** Background agent execution model is validated in Story 2.Spike (Epic 2) before Stories 2.4 and 4.3 begin. Do not implement productive waiting or background VFL execution until spike result is documented. The execution mode is adopted as the architectural intent; the spike validates the specific implementation mechanism (inter-agent communication + checkpoint/resume). If the spike reveals the mechanism is unavailable, Decision 3a/4c will be revised before Stories 2.4 and 4.3 begin.

**Story 2.Spike definition (epics.md, lines 710-728):**
> Story 2.Spike: Validate Background Agent Coordination Mechanism
> Type: Technical Spike
> FR Trace: Architecture prerequisite for Stories 2.4, 4.3
> Validate that the SendMessage API reliably supports background agent checkpoint/resume for multi-step story cycles. Stories 2.4 (productive waiting) and 4.3 (full story cycle) depend on background agents that can be resumed mid-task via SendMessage.

### File Structure

**Create:**
- `docs/research/background-agent-coordination.md` — research findings document

**Modify:**
- `_bmad-output/planning-artifacts/architecture.md` — Decision 4c implementation note update (line 437)
- `_bmad-output/implementation-artifacts/2-4-completion-signals-and-productive-waiting.md` — cross-reference in "Critical Dependency" section (line 117)

### Testing

**Story type:** specification
**Verification method:** Direct authoring with cross-reference verification — no tests or evals needed. AVFL validates the produced artifacts against the three ACs.

This is a research/specification story. The deliverables are a research document and two cross-reference updates. There is no code to test and no behavioral skill instructions to eval. The AVFL pass verifies:
1. Research document exists and contains actionable findings (not vague)
2. Decision 4c is updated consistently with findings
3. Story 2.4 dev notes reference the research document

### Previous Story Intelligence

**From Story 2.4 (the story that bypassed this gate):**
- Story 2.4 proceeded without the spike because its ACs are behavioral skill instructions, not runtime mechanisms
- The gate reconciliation rationale is documented in Story 2.4 dev notes (lines 117-129)
- Story 2.4 explicitly flags: "The spike's concern (checkpoint/resume mid-task) is relevant to Story 4.3 (full story cycle), not to the completion signal and synthesis patterns defined here"

**From Epic 1 Retro #6:**
- Action item: "Validate background agent coordination mechanism (SendMessage checkpoint/resume). Sequence after spec fatigue agent to avoid competing modifications to Epic 2 stories."
- Success criteria: "Spike documented in `docs/research/` before Stories 2.4 and 4.3"

### Git Intelligence

This is the first spike-as-story in the project. No prior research documents for background agent coordination exist in `docs/research/`. The architecture.md file was last modified during Epic 2 story development. Story 2.4 dev notes have not been modified since the story was completed (status: review).

### References

- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 4c, lines 432-437] — Productive Waiting decision and gate
- [Source: _bmad-output/planning-artifacts/epics.md#Story 2.Spike, lines 710-728] — Original spike definition
- [Source: _bmad-output/implementation-artifacts/2-4-completion-signals-and-productive-waiting.md#Critical Dependency, lines 117-129] — Gate bypass rationale
- [Source: _bmad-output/implementation-artifacts/epic-1-retro-2026-03-22.md#Retro #6, lines 111-115] — Retro action item
- [Source: _bmad-output/implementation-artifacts/epic-2-refinement-proposal.md#Story 2.10, lines 170-189] — Refinement proposal

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4 → specification (direct authoring)

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

**Do NOT use TDD or EDD for specification/research stories.** There is no code to test and no skill behavior to eval. Use direct authoring:

**Execute the research:**
1. Investigate the Claude Code inter-agent communication mechanisms (TaskOutput, SendMessage, structured returns, etc.)
2. Test `run_in_background: true` agents — can they receive mid-task messages? Can they be resumed?
3. Document what works, what doesn't, constraints, and failure modes

**Author the artifacts:**
4. Create `docs/research/background-agent-coordination.md` with structured findings — mechanism tested, methodology, results, constraints, recommendation for Story 4.3
5. Update Decision 4c in `_bmad-output/planning-artifacts/architecture.md` (line 437) — replace the "do not implement" gate with actual findings
6. Add cross-reference in Story 2.4 dev notes (`_bmad-output/implementation-artifacts/2-4-completion-signals-and-productive-waiting.md`, line 119) pointing to the research document

**AVFL validates:**
7. Research document exists at `docs/research/background-agent-coordination.md` with actionable content (AC1)
8. Decision 4c updated — implementation note reflects spike outcome (AC2)
9. Story 2.4 dev notes contain cross-reference to research document (AC3)

**NFR compliance note:** This story produces a research document in `docs/research/`, not a skill file. SKILL.md line-count NFRs do not apply.

---

### Verification (post-AVFL)

Adversarial subagent verification — manual review (cmux not applicable for research artifact). Subagent reviews the research document adversarially:
1. Checks `docs/research/background-agent-coordination.md` exists with actionable findings (not vague)
2. Verifies Decision 4c in architecture.md is updated and consistent with research
3. Checks Story 2.4 dev notes cross-reference
4. Adversarially challenges: are the findings reproducible? Does the document cover failure modes? Would a developer have enough info to implement Story 4.3?

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
