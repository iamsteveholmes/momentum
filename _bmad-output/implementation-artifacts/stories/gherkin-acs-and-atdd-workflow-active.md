---
title: "Gherkin ACs and ATDD Workflow Active"
story_key: gherkin-acs-and-atdd-workflow-active
status: ready-for-dev
epic_slug: story-cycles
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/dev/workflow.md
  - skills/momentum/skills/create-story/workflow.md
  - skills/momentum/references/gherkin-template.md
  - skills/momentum/references/protected-paths.json
  - skills/momentum/agents/e2e-validator.md
change_type: skill-instruction
derives_from:
  - path: _bmad-output/planning-artifacts/prd.md
    relationship: derives_from
    section: "FR39: Plain English ACs in story files"
  - path: _bmad-output/planning-artifacts/prd.md
    relationship: derives_from
    section: "FR40: ATDD workflow generates failing acceptance tests from Gherkin"
  - path: _bmad-output/planning-artifacts/prd.md
    relationship: derives_from
    section: "FR58: Gherkin Separation — story files vs sprint specs"
  - path: _bmad-output/planning-artifacts/prd.md
    relationship: derives_from
    section: "FR65: Developer-confirmation checklist from Gherkin scenarios"
  - path: _bmad-output/planning-artifacts/architecture.md
    relationship: derives_from
    section: "Decision 30: Gherkin Specification Separation"
---

# Gherkin ACs and ATDD Workflow Active

## Story

As a developer using Momentum,
I want the ATDD workflow to be fully active so that Gherkin specs generated during
sprint planning drive black-box verification during sprint execution,
so that I have confidence that implemented behavior matches specified behavior
without relying solely on manual developer confirmation.

## Description

Momentum already generates Gherkin specs during sprint planning (Step 4 of
sprint-planning workflow) and uses them for a manual developer-confirmation
checklist during sprint-dev Phase 6. The E2E Validator agent exists and runs
during Team Review (Phase 5). Protected paths already include `*.feature` in
`protected-paths.json`.

What is missing is the **active ATDD workflow** that ties these pieces into a
coherent acceptance-test-driven development cycle:

1. **Outsider Test enforcement is inconsistent.** Retro findings from
   sprint-2026-04-06-2 show the AC-by-AC translation anti-pattern keeps
   resurfacing in generated Gherkin specs. The outsider-test guardrail exists
   in the sprint-planning workflow but needs reinforcement through explicit
   validation criteria that can be checked by review agents.

2. **No pre-implementation verification.** Gherkin specs are generated before
   code exists (correct), but there is no step that confirms specs are
   well-formed and testable before dev agents start work. A malformed spec
   discovered during Phase 5 wastes an entire dev cycle.

3. **The E2E Validator has no feedback loop into spec quality.** When the E2E
   Validator finds untestable scenarios, that signal is not routed back to
   improve the spec generation step. The outsider-test guardrail needs to be
   enforced at generation time, not discovered at verification time.

4. **Dev agents can still read `.feature` files.** While `*.feature` is in
   `protected-paths.json` for write protection, there is no explicit read
   barrier in the dev workflow instructions. The black-box separation
   (Decision 30) requires dev agents to never access `sprints/{slug}/specs/`.

This story activates the full ATDD workflow by hardening spec generation quality,
enforcing the black-box boundary, and creating the feedback loop between
verification findings and spec generation improvement.

**Design principle:** Gherkin must stay behavioral and general. Specificity kills
Gherkin value and couples tests to implementation. Every change in this story
reinforces behavioral framing over structural testing.

## Acceptance Criteria (Plain English)

### AC1: Outsider Test Guardrail Enforced in All Spec-Generation Paths

- The sprint-planning workflow (Step 4) includes an explicit self-check after
  each generated `.feature` file: for every Given/When/Then clause, verify it
  passes the Outsider Test (could someone who has never seen source code verify
  this by only invoking skills, running commands, and reading outputs?)
- Any scenario that references internal mechanisms (which skill was called, which
  file was read, which agent was spawned, what an agent did NOT do internally)
  is flagged and rewritten before the spec is saved
- The quick-fix workflow's spec generation path (if it generates Gherkin) applies
  the same guardrail

### AC2: Dev Agent Black-Box Boundary Explicit

- The momentum:dev workflow explicitly instructs dev agents to never read files
  under `sprints/{sprint-slug}/specs/` or any `.feature` file
- This instruction appears in a `<critical>` directive in the dev workflow, not
  just as a side-effect of protected-paths.json write protection
- The Momentum Implementation Guide injection (create-story Step 4) includes a
  reminder that Gherkin specs exist but are off-limits to the dev agent

### AC3: Spec Quality Pre-Check Before Dev Spawn

- After Gherkin spec generation (sprint-planning Step 4), a lightweight
  validation pass runs on each generated `.feature` file before proceeding to
  team composition
- The validation checks:
  - Every scenario has at least one Given, one When, and one Then
  - No scenario name contains AC numbers or phase numbers
  - No Given/When/Then clause references internal agent names, tool names, or
    file paths that would fail the Outsider Test
  - The feature file follows the structure rules in `gherkin-template.md`
    (indentation, no tags, no Scenario Outline, no comments)
- Validation failures are surfaced to the developer with the specific clause
  that failed and why, and the spec is regenerated before planning proceeds

### AC4: E2E Validator Findings Feed Back to Spec Improvement

- When the E2E Validator (sprint-dev Phase 5) produces findings categorized as
  "untestable scenario" or "scenario fails Outsider Test," those findings are
  tagged with `spec-quality` metadata
- During sprint retrospective, `spec-quality` tagged findings are aggregated and
  surfaced as a dedicated section in the retro output
- This creates the feedback loop: retro findings inform future sprint planning's
  spec generation quality

### AC5: Gherkin Specs Remain Behavioral and General

- No generated Gherkin scenario references specific file paths, function names,
  class names, or internal data structures
- Scenarios describe observable system behavior: what the user does, what the
  system produces, what the developer can see
- The gherkin-template.md reference document includes an explicit "Anti-Patterns"
  section listing the AC-by-AC translation pattern, internal-mechanism references,
  and implementation-coupled assertions as things to avoid
- This anti-patterns section is referenced by the sprint-planning workflow's spec
  generation step

### AC6: Protected Paths Cover Spec Read Barrier

- `protected-paths.json` already has `*.feature` with write policy -- verify this
  is correct and sufficient
- The sprint-dev workflow's critical directives already state "Dev agents never
  access sprints/{sprint-slug}/specs/" -- verify this directive is present and
  prominent
- If any gap exists in either protection, close it

## Tasks / Subtasks

- [ ] Task 1 -- Write behavioral eval (EDD: before implementation) (AC: 1-6)
  - [ ] Create `skills/momentum/skills/sprint-planning/evals/eval-gherkin-atdd-workflow.md`
    with scenarios covering: outsider-test enforcement, black-box boundary,
    spec quality pre-check, feedback loop tagging, behavioral generality

- [ ] Task 2 -- Add anti-patterns section to gherkin-template.md (AC: 5)
  - [ ] Add explicit "Anti-Patterns" section to
    `skills/momentum/references/gherkin-template.md` listing:
    - AC-by-AC translation (one scenario per AC, AC numbers in names)
    - Internal mechanism references (agent names, tool names, file reads)
    - Implementation-coupled assertions (specific file paths, function names)
    - Passive voice in When clauses
  - [ ] Each anti-pattern includes a "Bad" and "Good" example pair

- [ ] Task 3 -- Harden spec generation in sprint-planning workflow (AC: 1, 3, 5)
  - [ ] Add a self-check action after each `.feature` file is generated in Step 4:
    iterate every Given/When/Then clause and apply Outsider Test
  - [ ] Add spec quality validation sub-step after all specs are generated:
    structural checks (Given/When/Then present), naming checks (no AC numbers),
    outsider-test checks (no internal references), format checks (per template)
  - [ ] Surface failures with specific clause and rewrite before saving
  - [ ] Reference the new anti-patterns section in gherkin-template.md from
    the spec generation step

- [ ] Task 4 -- Enforce dev agent black-box boundary (AC: 2, 6)
  - [ ] Add `<critical>` directive to `skills/momentum/skills/dev/workflow.md`
    explicitly forbidding reads of `sprints/{sprint-slug}/specs/` and `*.feature`
  - [ ] Verify `protected-paths.json` has `*.feature` entry (it does -- confirm
    and document)
  - [ ] Verify sprint-dev workflow critical directives include the specs access
    prohibition (it does -- confirm and document)
  - [ ] Add a note to the Momentum Implementation Guide injection template
    (create-story workflow) reminding that Gherkin specs are off-limits

- [ ] Task 5 -- Add spec-quality feedback tagging to E2E Validator (AC: 4)
  - [ ] Update `skills/momentum/agents/e2e-validator.md` to tag findings that
    involve untestable or outsider-test-failing scenarios with `spec-quality`
    metadata in the structured output
  - [ ] Document the tag format so the retro workflow can filter on it

- [ ] Task 6 -- Run eval and verify (AC: 1-6)
  - [ ] Run eval via subagent
  - [ ] Manually verify: generate a sample `.feature` file and confirm the
    quality pre-check catches anti-patterns
  - [ ] Manually verify: dev workflow contains the critical directive
  - [ ] Manually verify: e2e-validator output includes spec-quality tag field

## Dev Notes

### What Already Exists

**Sprint-planning Gherkin generation (modify, don't rewrite):**
Step 4 of `skills/momentum/skills/sprint-planning/workflow.md` already generates
`.feature` files with extensive instructions about the Outsider Test, behavioral
scenarios, and what not to include. This story adds a validation gate after
generation, not a rewrite of the generation instructions.

**Gherkin template (extend):**
`skills/momentum/references/gherkin-template.md` defines format, voice, tense,
naming, structure rules, and "What NOT to Include." This story adds an
"Anti-Patterns" section with concrete bad/good examples to reinforce behavioral
quality.

**E2E Validator agent (extend):**
`skills/momentum/agents/e2e-validator.md` already tests running behavior against
Gherkin specs. This story adds structured tagging of findings that indicate spec
quality issues (untestable scenarios, outsider-test failures) so retro can
aggregate them.

**Protected paths (verify, minimal change):**
`skills/momentum/references/protected-paths.json` already contains `*.feature`
with policy `acceptance-test-dir`. This provides write protection. The read
barrier is enforced by workflow directives, not file protection hooks (which
only block writes).

**Dev workflow (add directive):**
`skills/momentum/skills/dev/workflow.md` delegates to bmad-dev-story. It needs
an explicit `<critical>` directive forbidding `.feature` file reads to enforce
Decision 30's black-box separation.

**Sprint-dev verification (no changes needed):**
Phase 5 (Team Review) and Phase 6 (Verification Checklist) in
`skills/momentum/skills/sprint-dev/workflow.md` already use Gherkin specs
correctly. No changes to these phases.

### Key Architecture References

- **Decision 30: Gherkin Specification Separation** -- Story files contain plain
  English ACs only. Gherkin specs are sprint-scoped. Dev agents never access
  specs. Verifiers validate against specs. (architecture.md)
- **FR39:** Plain English ACs in story files, never Gherkin
- **FR40:** ATDD workflow generates failing acceptance tests from Gherkin
- **FR58:** Gherkin separation enforcement (story files vs sprint specs)
- **FR65:** Developer-confirmation checklist from Gherkin scenarios (Phase 6)

### Important Constraints

- **Behavioral, not structural.** Every Gherkin scenario must describe observable
  behavior. No file path assertions, no code structure assertions, no internal
  mechanism assertions. This is the single most important quality criterion.
- **No new skills.** This story modifies existing workflows and references. It
  does not create a new skill or agent.
- **Spec generation is already good.** The sprint-planning workflow's Step 4
  already has detailed instructions. This story adds validation and enforcement,
  not a rewrite of the generation logic.
- **Read barrier is convention, not enforcement.** PreToolUse hooks only block
  writes. The read barrier for `.feature` files is enforced by workflow
  directives (`<critical>` tags) telling agents not to read specs. This is
  consistent with Decision 30's design.

### What NOT to Change

- The sprint-planning Step 4 generation instructions (already comprehensive)
- The sprint-dev Phase 5 Team Review structure (already correct)
- The sprint-dev Phase 6 Verification Checklist (already correct)
- The `momentum-tools.py` CLI (no new commands needed)
- Story file format (stories never contain Gherkin -- this is already enforced)

### Recurring Retro Finding

Sprint-2026-04-06-2 retro identified the AC-by-AC translation anti-pattern as
recurring. Despite explicit instructions to write behavioral scenarios (not
AC-by-AC translations), generated specs kept producing one scenario per AC with
AC numbers in scenario names. The root cause is that generation instructions
tell agents *what to do* but don't validate the output. This story adds the
validation gate that catches the anti-pattern before specs are saved.

### Project Structure Notes

- Sprint-planning workflow: `skills/momentum/skills/sprint-planning/workflow.md`
- Sprint-dev workflow: `skills/momentum/skills/sprint-dev/workflow.md`
- Dev workflow: `skills/momentum/skills/dev/workflow.md`
- Create-story workflow: `skills/momentum/skills/create-story/workflow.md`
- Gherkin template: `skills/momentum/references/gherkin-template.md`
- Protected paths: `skills/momentum/references/protected-paths.json`
- E2E Validator agent: `skills/momentum/agents/e2e-validator.md`

### Momentum Implementation Guide

**Change type classification:** All tasks are `skill-instruction` (modifying
workflow markdown and agent definitions).

**Implementation approach:** EDD (Eval-Driven Development). Write the behavioral
eval first (Task 1), then implement changes, then verify against the eval.

**EDD steps:**
1. Create eval at `skills/momentum/skills/sprint-planning/evals/eval-gherkin-atdd-workflow.md`
2. Implement Tasks 2-5 (template anti-patterns, workflow hardening, boundary
   enforcement, feedback tagging)
3. Run eval to verify all behavioral expectations are met

**DoD additions for skill-instruction:**
- All modified workflow files parse correctly as XML-in-markdown
- No orphaned step references (renumbered steps all cross-reference correctly)
- `<critical>` directives are present for all safety constraints
- Template changes include concrete examples (not abstract guidance)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
