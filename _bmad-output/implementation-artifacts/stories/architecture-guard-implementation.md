---
title: Architecture Guard Implementation — Replace Stub with Real Agent Definition
story_key: architecture-guard-implementation
status: ready-for-dev
epic_slug: agent-team-model
depends_on: []
touches:
  - skills/momentum/agents/architecture-guard.md
  - skills/momentum/skills/architecture-guard/SKILL.md
change_type: config-structure + skill-instruction
---

# Architecture Guard Implementation — Replace Stub with Real Agent Definition

## Goal

Replace the architecture-guard SKILL.md stub (which says "full implementation in
Story 4.X" and has no review logic) with a proper `agents/architecture-guard.md`
agent definition file that reads architecture decisions from
`_bmad-output/planning-artifacts/architecture.md` and checks sprint changes for
pattern drift, naming violations, and decision non-compliance. The agent produces
structured findings in the same format as qa-reviewer.md and e2e-validator.md.

The architecture guard is a one-shot reviewer spawned during Team Review (Phase 5
of sprint-dev). It focuses exclusively on architecture DECISIONS — not code quality
(that is code-reviewer's job) and not acceptance criteria (that is QA reviewer's
job).

## Acceptance Criteria (Plain English)

1. `skills/momentum/agents/architecture-guard.md` exists with proper agent
   definition frontmatter (name, description, model, effort, tools) following the
   pattern established by qa-reviewer.md and e2e-validator.md
2. The agent reads `_bmad-output/planning-artifacts/architecture.md` and extracts
   key decisions — deployment classification, naming conventions, plugin structure,
   read/write authority, separation of concerns, and any numbered decisions
3. The agent checks sprint changes (via git diff against the sprint branch base, or
   via file reads of touched files) against the extracted decisions
4. The agent produces structured findings with fields: decision_violated, file or
   pattern, evidence, and severity (CRITICAL / HIGH / MEDIUM / LOW)
5. The agent follows the same output format as qa-reviewer.md for consistency:
   report header with sprint slug and verdict, findings grouped by severity, and a
   summary section
6. Sprint-dev Phase 5 spawns `agents/architecture-guard.md` via the Agent tool (not
   the existing skill stub)
7. The skill SKILL.md is updated to reference the agent definition — removes the
   "full implementation in Story 4.X" placeholder, updates the description to note
   that Team Review uses the agent definition, and retains `context: fork` for
   standalone ad-hoc invocations that delegate to the same review logic
8. Model: sonnet, effort: medium (read-only analysis, same tier as QA reviewer and
   E2E validator)
9. Tools: Read, Glob, Grep, Bash (same as qa-reviewer — read-only operations plus
   git commands for diff analysis)

## Dev Notes

### Current state

`skills/momentum/skills/architecture-guard/SKILL.md` is a stub:

```yaml
---
name: architecture-guard
description: "Detects pattern drift against architecture decisions..."
model: claude-opus-4-6
context: fork
allowed-tools: Read
effort: high
---

Architecture guard subagent — full implementation in Story 4.X.
```

No review logic. No decision extraction. No findings format. The model is set to
opus with high effort — both wrong for a read-only reviewer. The tool set is
restricted to Read only, which blocks git diff commands needed for change analysis.

### Target state

`skills/momentum/agents/architecture-guard.md` — a proper agent definition file
with:

- Frontmatter: name, description, model (sonnet), effort (medium), tools (Read,
  Glob, Grep, Bash)
- Role description: architecture decision compliance reviewer
- Decision extraction process: read architecture.md, build a decision checklist
- Change analysis process: identify what changed in the sprint, check each change
  against the decision checklist
- Findings output: structured report matching the team review format

The existing SKILL.md is updated to remove the stub placeholder and reference the
agent definition. It retains `context: fork` for standalone ad-hoc use but the
body delegates to the same review logic rather than being empty.

### What the agent checks

The architecture guard focuses on decisions in architecture.md. Key categories:

1. **Deployment classification compliance** — Is each component deployed as the
   correct mechanism (SKILL.md vs agent definition vs hook vs rule)? Does a new
   skill have the right `context:` setting? (Decision 35)
2. **Naming conventions** — Does new code follow the `momentum:` namespace for
   skills? Are agent definition files in `agents/`? Are skills in `skills/`?
3. **Plugin structure** — Do new files land in the correct plugin directory?
   (`skills/`, `agents/`, `hooks/`, `scripts/`, `references/`)
4. **Read/write authority** — Does each agent/skill only write to files it is
   authorized to modify? (Architecture read/write authority table)
5. **Separation of concerns** — Does a new agent try to spawn subagents (violating
   the chain-through-main rule)? Does a dev agent handle merge gating (sprint-dev's
   job)? Does a verifier modify code?
6. **Decision compliance** — Any numbered decision (1a through 35+) that the sprint
   changes interact with. The guard reads the decision text and checks whether the
   implementation honors it.
7. **Orchestrator purity** — Does Impetus stay pure (Decision 3d)? Are all
   subagent spawns hub-and-spoke?
8. **Model routing** — Do new SKILL.md and agent definition files have `model:`
   and `effort:` frontmatter? Is the cognitive hazard rule honored?

### Real examples from prior sprint reviews

The sprint-2026-04-04 architect guard review (performed manually) found real
issues that this agent should catch automatically:

- **Sprint-manager supersession**: A new skill was created that duplicated
  sprint-manager's write authority over `stories/index.json` — violating the
  single-writer principle from the read/write authority table
- **Missing spec'd skills**: Skills referenced in the architecture (sprint-planning,
  sprint-dev) existed as workflow modules but not as proper SKILL.md files — the
  plugin structure decision required them as skills
- **Agent definition file boundary**: QA reviewer and E2E validator were initially
  proposed as SKILL.md files but should have been agent definition files per
  Decision 35 — the guard should flag when a pure spawned worker is implemented as
  a SKILL.md instead of an agent definition

These are the kinds of findings the architecture guard should produce.

### The agent should focus on architecture DECISIONS, not code quality

The architecture guard does NOT check:
- Code style, formatting, or lint issues (that is code-reviewer and hooks)
- Whether acceptance criteria are met (that is QA reviewer)
- Whether behavior matches Gherkin specs (that is E2E validator)
- Whether tests pass (that is QA reviewer and E2E validator)

The architecture guard DOES check:
- Whether structural decisions are honored
- Whether naming conventions are followed
- Whether separation of concerns is maintained
- Whether new components are deployed via the correct mechanism
- Whether read/write authority boundaries are respected

### Decision 35 reclassification

Decision 35 currently classifies architecture-guard as a `context: fork` SKILL.md
that "stays SKILL.md — useful for ad-hoc drift checks." This story reclassifies
the primary implementation as an agent definition file for Team Review spawning
(consistent with QA reviewer and E2E validator), while the SKILL.md retains
`context: fork` for standalone ad-hoc invocations. Decision 35's architecture.md
entry should be updated to reflect this dual deployment — but architecture.md
itself is NOT modified by this story (the architecture decision update is a
separate concern).

### What NOT to change

- **`_bmad-output/planning-artifacts/architecture.md`** — the architecture
  document is the source of truth the guard reads, not something the guard modifies.
  Any Decision 35 reclassification is a separate documentation task.
- **qa-reviewer.md and e2e-validator.md** — these are reference patterns, not
  modification targets
- **Sprint-dev Phases 1-4, 6-7** — only Phase 5 spawn mechanism changes
- **code-reviewer SKILL.md** — different role, different concerns

### Requirements Coverage

- Architecture Decision 34: Hybrid Resolution Team (architect guard is one of the
  three Team Review roles)
- Architecture Decision 35: Agent Definition Files vs SKILL.md Boundary (this
  story adds architecture-guard to the agents/ directory)
- Architecture Decision 26: Two-Layer Agent Model (agent definitions are
  lightweight spawned workers)
- Sprint-dev Phase 5: Team Review spawns QA + E2E Validator + Architect Guard

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before agent creation)
  - [ ] Create `skills/momentum/agents/evals/eval-arch-guard-reads-decisions.md`
    — verifies the agent reads architecture.md and extracts numbered decisions
  - [ ] Create `skills/momentum/agents/evals/eval-arch-guard-checks-changes.md`
    — verifies the agent analyzes sprint changes against extracted decisions
  - [ ] Create `skills/momentum/agents/evals/eval-arch-guard-findings-format.md`
    — verifies the agent produces structured findings with decision_violated,
    file/pattern, evidence, and severity fields

- [ ] Task 2 — Create `agents/architecture-guard.md` agent definition (AC: 1, 2, 3, 4, 5, 8, 9)
  - [ ] Write frontmatter: name (architecture-guard), description, model (sonnet),
    effort (medium), tools (Read, Glob, Grep, Bash)
  - [ ] Write role description and critical constraints (read-only, architecture
    decisions only, not code quality)
  - [ ] Write input format section (sprint slug, sprint branch, architecture.md
    path, list of touched files)
  - [ ] Write decision extraction process (read architecture.md, build checklist
    of key decisions with their implications)
  - [ ] Write change analysis process (git diff or file reads, check each change
    against decision checklist)
  - [ ] Write output format (structured findings report matching qa-reviewer
    format: header, findings by severity, verdict, summary)

- [ ] Task 3 — Update SKILL.md stub (AC: 7)
  - [ ] Remove "full implementation in Story 4.X" placeholder text
  - [ ] Update description to reflect dual deployment (agent definition for Team
    Review, SKILL.md for standalone ad-hoc use)
  - [ ] Fix model from claude-opus-4-6 to sonnet
  - [ ] Fix effort from high to medium
  - [ ] Update allowed-tools from Read to Read, Glob, Grep, Bash
  - [ ] Add body content that delegates to the same review logic as the agent
    definition (read architecture.md, extract decisions, check changes, report
    findings)

- [ ] Task 4 — Update sprint-dev Phase 5 spawn (AC: 6)
  - [ ] Update the Architect Guard spawn in Phase 5 to reference
    `agents/architecture-guard.md` via the Agent tool
  - [ ] Ensure the spawn passes: sprint slug, sprint branch name, path to
    architecture.md, and list of files touched by sprint stories
  - [ ] Verify the findings output format is compatible with Phase 5's
    consolidation logic

- [ ] Task 5 — Run evals and verify (AC: all)
  - [ ] Run each eval via subagent
  - [ ] Confirm standalone `/momentum:architecture-guard` still works via the
    updated SKILL.md
  - [ ] Confirm sprint-dev Phase 5 integration is compatible

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 -> config-structure (EDD — evals for agent definition)
- Task 2 -> config-structure (agent definition file follows qa-reviewer pattern)
- Task 3 -> skill-instruction (modifying existing SKILL.md)
- Task 4 -> skill-instruction (modifying sprint-dev workflow Phase 5)
- Task 5 -> config-structure (eval execution)

---

### config-structure Tasks: Eval-Driven Development (EDD)

**Before writing the agent definition:**
1. Write 3 behavioral evals in `skills/momentum/agents/evals/`:
   - One per eval above: decision extraction, change analysis, findings format
   - Format: "Given [input/context], the agent should [observable behavior]"

**Then implement:**
2. Write `agents/architecture-guard.md` following the qa-reviewer.md and
   e2e-validator.md pattern

**Then verify:**
3. Run evals via subagent, confirm behaviors match

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before modifying the SKILL.md:**
1. Document current stub state (model, effort, tools, body text)

**Then implement:**
2. Update SKILL.md frontmatter (model, effort, tools) and body (real review
   instructions replacing the stub)

**Before modifying sprint-dev workflow:**
3. Document current Phase 5 Architect Guard spawn mechanism

**Then implement:**
4. Replace the spawn to use Agent tool with `agents/architecture-guard.md`
5. Ensure spawn parameters match the agent's expected input format

**Then verify:**
6. Confirm Phase 5 consolidation logic handles the agent's output format

**NFR compliance:**
- Agent definition file should be concise — under 150 lines (qa-reviewer is 104,
  e2e-validator is 106)
- Frontmatter `description` must be <= 150 characters
- `model:` and `effort:` frontmatter must be present

**DoD items:**
- [ ] 3 behavioral evals written
- [ ] EDD cycle ran — all eval behaviors confirmed
- [ ] Agent definition frontmatter complete (name, description, model, effort, tools)
- [ ] Agent definition body under 150 lines
- [ ] Agent reads architecture.md and extracts decisions
- [ ] Agent produces structured findings with decision_violated, file/pattern,
  evidence, severity
- [ ] SKILL.md stub replaced with real content
- [ ] SKILL.md frontmatter corrected (sonnet, medium, expanded tools)
- [ ] Sprint-dev Phase 5 updated to spawn agents/architecture-guard.md
- [ ] Standalone /momentum:architecture-guard still works (non-regression)
- [ ] Output format consistent with qa-reviewer.md findings structure

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
