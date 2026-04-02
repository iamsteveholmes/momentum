# Story 1.7: Acceptance Testing Process and Standards

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a team,
I want a documented acceptance testing process with role separation and story-type classification,
so that verification is structurally independent from implementation and every story type has appropriate test coverage.

## Acceptance Criteria

**AC1 — Story type classification table:**
Given the acceptance testing standard document
When a team member reads it
Then it defines a story type classification table that maps each story type to its required verification method
And the classification includes at minimum: skill-instruction stories (EDD with adversarial eval authoring), config-structure stories (execution test), install/deploy stories (end-to-end test), and rule/hook stories (behavioral trigger test)

**AC2 — Role separation:**
Given the acceptance testing standard document
When a team member reads the role separation section
Then the acceptance tester role is defined as structurally separate from the developer role
And the developer does not author, read, or execute acceptance tests or EDD evals for their own work
And enforcement mechanism is specified so the dev agent cannot load verification artifacts during implementation

**AC3 — Team agreements codified:**
Given the acceptance testing standard document
When a team member reads the team agreements section
Then the three Epic 1 retro team agreements are codified as process constraints:
And end-to-end deployment testing is mandatory for any story with an install or deploy path
And acceptance testing role separation is active immediately, not deferred to Epic 4 tooling
And every story file includes an explicit Acceptance Test Plan section

**AC4 — Epic 2 story audit:**
Given all Epic 2 stories currently in ready-for-dev status
When the acceptance test audit is complete
Then each Epic 2 story file contains an Acceptance Test Plan section
And each plan identifies the story type and corresponding verification method from the classification table

## Tasks / Subtasks

- [x] Task 1: Create the acceptance testing standard document (AC: 1, 2, 3)
  - [x] 1.1: Create `docs/process/acceptance-testing-standard.md` with story type classification table mapping each type to its verification method: skill-instruction -> EDD (adversarial eval authoring by independent tester), config-structure -> execution test, install/deploy -> end-to-end test, rule/hook -> behavioral trigger test
  - [x] 1.2: Write role separation section — acceptance tester role is structurally separate from developer; developer does not author, read, or execute acceptance tests or EDD evals for their own work
  - [x] 1.3: Specify enforcement mechanism — the dev agent must not load verification artifacts during implementation; document how file storage/flagging ensures structural separation (e.g., `tests/acceptance/` path protection via PreToolUse hooks per architecture Decision 2a)
  - [x] 1.4: Codify the three Epic 1 retro Team Agreements as process constraints: (1) E2E deployment testing mandatory for install/deploy stories, (2) acceptance testing role separation active immediately (not deferred to Epic 4), (3) every story file includes an Acceptance Test Plan section

- [x] Task 2: Define the Acceptance Test Plan section template (AC: 3)
  - [x] 2.1: Create a standard section template that goes into every story file, containing: story type classification, verification method, test artifacts location, and acceptance tester assignment
  - [x] 2.2: Document where in the story file template the section should appear (after Dev Notes, before Dev Agent Record — or as a subsection of Dev Notes)

- [x] Task 3: Audit and update Epic 2 story files with Acceptance Test Plan sections (AC: 4)
  - [x] 3.1: Read each Epic 2 ready-for-dev story file (2-1, 2-2, 2-3, 2-4) and classify its story type using the classification table from Task 1
  - [x] 3.2: Add an Acceptance Test Plan section to each Epic 2 story file with: the classified story type, the corresponding verification method, and the test artifact location
  - [x] 3.3: Verify each updated story file is well-formed and the new section is correctly placed

## Dev Notes

### Epic Context

This story originates from the Epic 1 retrospective, which identified two related gaps:

1. **No acceptance testing process exists** (Retro Challenge): EDD tests skill behavior but not end-to-end reachability. Config-structure tasks were verified by JSON parsing only. No story type had a concrete E2E acceptance test. This gap let a broken install experience ship (90 skills shown instead of 8).

2. **Developer authors their own verification** (Retro Challenge): The dev agent writes EDD evals, implements the skill, and runs verification — all in the same context. Evals unconsciously mirror implementation assumptions rather than challenging them.

The retro produced three Team Agreements that this story must codify:
1. End-to-end deployment testing is mandatory for any story with an install or deploy path
2. Acceptance testing role separation starts now, not when Epic 4 tooling ships
3. Story files should include an explicit "Acceptance Test Plan" section going forward

**Source:** `_bmad-output/implementation-artifacts/epic-1-retro-2026-03-22.md`

### Architecture Constraints

The architecture document already establishes relevant patterns:

- **File protection (Decision 2a):** `tests/acceptance/` and `**/*.feature` are immutable — agents never modify to make code pass. This is the existing structural enforcement mechanism. [Source: architecture.md#Decision 2a]
- **ATDD workflow data flow:** The ATDD workflow writes only to `tests/acceptance/`. Coding agents (dev-story) read specs, rules, and existing code but do NOT read `tests/acceptance/`. [Source: architecture.md#Data Access Matrix]
- **Acceptance test gate (Decision 5b):** "BMAD dev-story complete → Impetus gates on acceptance tests passing before closing story" is the only hard gate at MVP. [Source: architecture.md#Decision 5b]
- **Protection boundaries:** PreToolUse blocks writes to `tests/acceptance/`, `_bmad-output/planning-artifacts/`, `.claude/rules/`, and findings ledger. [Source: architecture.md#Protection boundaries]

The acceptance testing standard document must be consistent with these architectural decisions — it describes the process; the architecture enforces the boundaries.

### Story Type Classification (from Retro Action Items #2 and #3)

The retro defined these verification categories:

| Story Type | Verification Method | Example |
|---|---|---|
| skill-instruction | EDD with adversarial eval authoring (by independent tester) | Story 1.3, 1.4, 2.1 |
| config-structure | Execution test (run the config, verify behavior) | Story 1.1 (JSON parsing + path verification) |
| install/deploy | End-to-end test (run actual install from outside repo) | Story 1.2, 1.6 |
| rule/hook | Behavioral trigger test (trigger the rule/hook, observe result) | Story 3.1–3.4 |

This table must appear in the standard document and be used to classify Epic 2 stories.

### Epic 2 Stories Requiring Audit (Task 3)

Four Epic 2 stories are currently `ready-for-dev` and need Acceptance Test Plan sections:

| Story | File | Likely Type |
|---|---|---|
| 2-1 | `2-1-impetus-skill-created-with-correct-persona-and-input-handling.md` | skill-instruction |
| 2-2 | `2-2-session-orientation-and-thread-management.md` | skill-instruction |
| 2-3 | `2-3-visual-progress-tracks-workflow-position.md` | skill-instruction |
| 2-4 | `2-4-completion-signals-and-productive-waiting.md` | skill-instruction |

All four are Impetus skill stories, so all likely classify as `skill-instruction` with EDD verification. Confirm by reading each file during implementation.

Story 2-5 is still `backlog` and does not need audit yet.

### Role Separation Enforcement

The enforcement mechanism should leverage the existing architecture:

1. **PreToolUse hook** already blocks writes to `tests/acceptance/` and `**/*.feature` — the dev agent cannot modify acceptance tests
2. **Read protection** is the missing piece: the dev agent should not *read* acceptance tests or EDD evals during implementation. This requires either:
   - A convention-based approach (document that dev agent must not load `tests/acceptance/` or `evals/` files)
   - A structural approach (file organization that makes accidental loading unlikely)
   - A hook-based approach (if supported — PreToolUse can potentially block reads)

The standard should specify the chosen approach. The architecture already protects writes; the standard needs to address reads.

### Previous Story Intelligence

**From Story 1.6 (Fix npx skills add):** Story 1.6 explicitly depends on Story 1.7: "Depends on Story 1.7 (needs acceptance test standard defined for Acceptance Test Plan section)." After this story is complete, Story 1.6 should be updated with an Acceptance Test Plan section using the standard defined here.

**From Epic 1 Retro — Key Insight #1:** "Inspection is not acceptance testing. 'JSON parses' and 'fields present' verify structure, not behavior. Stories with deployable or externally-observable outcomes need execution tests."

**From Epic 1 Retro — Key Insight #2:** "Role separation must be structural, not conventional. The person/agent who builds should not author, see, or execute their own verification criteria."

### Output File Location

The primary output is `docs/process/acceptance-testing-standard.md` (new file). This is a process document, not a planning artifact, so it lives under `docs/process/`.

### What NOT to Do

- Do NOT implement the ATDD tooling (that's Story 4.2 — this story defines the *process*, not the *tooling*)
- Do NOT modify the architecture document (that's Story 1.8 — Orchestrator Purity)
- Do NOT create actual acceptance tests for any story (the standard defines *how* tests should be created; actual test creation happens during story development)
- Do NOT modify the bmad-create-story template (the Acceptance Test Plan section template is defined in the standard; template changes would be a separate task)

### Project Structure Notes

- `docs/process/` — existing process documentation directory (contains `process-backlog.md`)
- `docs/process/acceptance-testing-standard.md` — new file to create
- `_bmad-output/implementation-artifacts/2-*.md` — Epic 2 story files to audit and update
- `tests/acceptance/` — the protected directory for acceptance test artifacts (not created in this story, but referenced in the standard)

### References

- [Source: epics.md#Story 1.7 — Acceptance Testing Process and Standards]
- [Source: epics.md#Epic 1b — Foundation Fixes]
- [Source: epic-1-retro-2026-03-22.md#Action Item #2 — Define acceptance testing process with role separation]
- [Source: epic-1-retro-2026-03-22.md#Action Item #3 — Define lightweight acceptance testing standard by story type]
- [Source: epic-1-retro-2026-03-22.md#Team Agreements 1, 2, 3]
- [Source: epic-1-retro-2026-03-22.md#Key Insights #1, #2]
- [Source: architecture.md#Decision 2a — File Protection Targets]
- [Source: architecture.md#Decision 5b — BMAD Enhancement Touch Points]
- [Source: architecture.md#Data Access Matrix]

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → unclassified (process documentation — no Momentum-specific guidance; standard bmad-dev-story DoD applies)
- Task 2 → unclassified (template definition — no Momentum-specific guidance; standard bmad-dev-story DoD applies)
- Task 3 → unclassified (story file audit/update — no Momentum-specific guidance; standard bmad-dev-story DoD applies)

All tasks in this story produce process documentation and story file updates. No skill-instruction, script-code, rule-hook, or config-structure change types are present. Standard bmad-dev-story DoD applies to all tasks.

---

## Acceptance Test Plan

**Story type:** process-doc
**Verification method:** Document review — confirm document satisfies all ACs by inspection and cross-reference
**Test artifacts location:** N/A (document review, no test artifacts)
**Acceptance tester:** unassigned

### Test Scenarios

1. **AC1 verification:** Read Section 2 of `docs/process/acceptance-testing-standard.md`. Confirm it contains a story type classification table mapping at minimum: skill-instruction → EDD, config-structure → execution test, install/deploy → end-to-end test, rule/hook → behavioral trigger test. Fail if any of the four required mappings is absent or incorrect.

2. **AC2 verification:** Read Section 3. Confirm acceptance tester role is defined as structurally separate from developer. Confirm the three developer prohibitions (author, read, execute). Confirm enforcement mechanism is specified (write protection + read protection + session isolation). Fail if role separation is advisory rather than structural.

3. **AC3 verification:** Read Section 4. Confirm three Team Agreements are codified as process constraints: (1) E2E mandatory for install/deploy, (2) role separation active immediately, (3) every story includes ATP section. Fail if any agreement is missing or described as a guideline rather than a constraint.

4. **AC4 verification:** Open each Epic 2 story file (2-1 through 2-4). Confirm each contains an Acceptance Test Plan section. Confirm each identifies story type and verification method from the classification table. Fail if any file is missing the section or has incorrect classification.

### Acceptance Gate

This story passes acceptance when:
- AC1: Classification table present with all four required type-to-method mappings
- AC2: Role separation defined as structural with three developer prohibitions and enforcement mechanism
- AC3: All three Team Agreements codified as binding constraints
- AC4: All four Epic 2 story files contain Acceptance Test Plan sections with correct type and method

---

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6[1m]

### Debug Log References

### Completion Notes List

- Created `docs/process/acceptance-testing-standard.md` — full acceptance testing standard covering: 5-type story classification table (skill-instruction, config-structure, install/deploy, rule/hook, process-doc) with verification methods; role separation section with enforcement mechanism (write protection via PreToolUse hook + read protection by convention + session isolation); three Epic 1 retro Team Agreements codified as binding process constraints; Acceptance Test Plan section template with placement rules and authoring responsibility table.
- All four Epic 2 story files (2-1 through 2-4) confirmed as `skill-instruction` type — all are Impetus skill-extension stories. Each file updated with an Acceptance Test Plan section containing: story type, verification method (EDD with adversarial eval authoring), test artifact location (`skills/momentum/evals/`), story-specific adversarial test scenarios, and acceptance gate conditions per AC.
- Acceptance Test Plan placement: after Momentum Implementation Guide, before Dev Agent Record — consistent across all four files.
- No TDD cycle required: this is a process-doc story producing only markdown documents and story file updates. No executable code, no tests to write or run.
- AVFL checkpoint (3-lens: structural, accuracy, coherence) — CHECKPOINT_WARNING. Score ~90/100 after fix pass. Two HIGH findings fixed: (1) "Example-Driven Development" corrected to "Eval-Driven Development" (F-01), (2) write protection relabeled from "existing" to "planned — Epic 3, Story 3.2" (F-02). One MEDIUM fixed: Story 1.7 ATP section added (SI-003). Six LOW findings remain documented (inline citation, reference list, contamination tension — not blocking). Profile: checkpoint, stage: final. Timestamp: 2026-03-22.

### File List

- `docs/process/acceptance-testing-standard.md` (created)
- `_bmad-output/implementation-artifacts/2-1-impetus-skill-created-with-correct-persona-and-input-handling.md` (modified — Acceptance Test Plan section added)
- `_bmad-output/implementation-artifacts/2-2-session-orientation-and-thread-management.md` (modified — Acceptance Test Plan section added)
- `_bmad-output/implementation-artifacts/2-3-visual-progress-tracks-workflow-position.md` (modified — Acceptance Test Plan section added)
- `_bmad-output/implementation-artifacts/2-4-completion-signals-and-productive-waiting.md` (modified — Acceptance Test Plan section added)

## Change Log

- docs(process): create acceptance-testing-standard.md — story type classification, role separation, enforcement mechanism, Team Agreements 1–3 (Date: 2026-03-22)
- docs(stories): add Acceptance Test Plan sections to Epic 2 stories 2-1 through 2-4 (Date: 2026-03-22)
