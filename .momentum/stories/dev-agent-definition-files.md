---
title: Dev Agent Definition Files — Lightweight Agent for Sprint-Dev Spawning
story_key: dev-agent-definition-files
status: ready-for-dev
epic_slug: agent-team-model
depends_on: []
touches:
  - skills/momentum/agents/dev.md
  - skills/momentum/skills/sprint-dev/workflow.md
change_type: config-structure + skill-instruction
---

# Dev Agent Definition Files — Lightweight Agent for Sprint-Dev Spawning

## Goal

Create a lightweight `agents/dev.md` agent definition file that sprint-dev spawns
directly via the Agent tool, replacing the current pattern where sprint-dev spawns
the full `momentum:dev` skill for each story. The dev agent receives a story file
path, implements it by delegating to bmad-dev-story, commits when done, and returns
structured completion output. All worktree management, story selection, and merge
gating stay in sprint-dev — the agent never handles those concerns.

## Acceptance Criteria (Plain English)

1. `skills/momentum/agents/dev.md` exists with proper agent definition frontmatter
   (name, description, model, effort, tools) following the pattern established by
   qa-reviewer.md and e2e-validator.md
2. The agent receives: story file path, sprint context (sprint slug), role
   assignment, and optional project guidelines path
3. The agent implements the story per its spec by delegating to bmad-dev-story,
   commits when done, and returns structured completion output (status, files
   changed, story key, test results)
4. Sprint-dev Phase 2 spawns `agents/dev.md` via the Agent tool (not the
   momentum:dev skill) for each unblocked story
5. The `momentum:dev` skill continues to work for direct `/momentum:dev`
   invocation — no regression, no modifications to the skill
6. The dev agent uses the same tool set as qa-reviewer and e2e-validator where
   appropriate (Read, Glob, Grep, Bash, Edit, Write) plus Agent (to delegate to
   bmad-dev-story)
7. The agent definition follows the structural pattern established by
   qa-reviewer.md and e2e-validator.md: frontmatter, role description, critical
   constraints, input section, process steps, output format

## Dev Notes

### Current state

Sprint-dev Phase 2 (step n="2") spawns `momentum:dev` as a skill for each
unblocked story. But `momentum:dev` is a 7-step workflow (209 lines) that handles:

- Story selection from stories/index.json (redundant — sprint-dev already selected)
- Crash recovery and worktree creation (redundant — sprint-dev manages worktrees)
- Lock file management (redundant — sprint-dev tracks in-progress state)
- Merge proposal and user confirmation (redundant — sprint-dev Phase 3 handles merges)
- Status transitions (redundant — sprint-dev transitions via momentum-tools)

The only non-redundant part of momentum:dev is step 6: invoke bmad-dev-story
inside the worktree and capture completion output. That is the kernel the new
agent definition wraps.

### Target state

Sprint-dev Phase 2 spawns `agents/dev.md` directly via the Agent tool. The agent:

1. Receives story file path, sprint slug, role, and optional guidelines path
2. Reads the story file to understand what to implement
3. Delegates to bmad-dev-story skill for the actual implementation
4. Captures bmad-dev-story completion output (files modified, test results)
5. Commits implementation work
6. Returns structured completion output to sprint-dev

This eliminates ~180 lines of redundant orchestration per story spawn.

### Agent body content

The `agents/dev.md` body should contain:

- **Role description**: You are a dev agent in Momentum's sprint execution. You
  implement a single story and return results.
- **Critical constraints**: No worktree management. No story selection. No merge
  operations. No status transitions. Those are sprint-dev's responsibility.
- **Input format**: Story file path, sprint slug, role, guidelines path (optional)
- **Implementation instructions**: Read the story file, delegate to bmad-dev-story
  for implementation, capture completion output
- **Output format**: Structured JSON completion signal matching the subagent output
  contract (Decision 3b) — status, files_modified, tests_run, test_result, story_key
- **Constraints**: Read-write agent (unlike qa-reviewer and e2e-validator which are
  read-only). Commits autonomously per git-discipline rules.

### Model and effort

- model: sonnet
- effort: medium

Matches qa-reviewer and e2e-validator. The dev agent delegates heavy lifting to
bmad-dev-story — it does not need opus-level reasoning for its own orchestration
logic.

### Sprint-dev workflow update

Phase 2 (step n="2") currently says:
```
3. Spawn a momentum:dev agent with:
   - Story key: {slug}
   - Story file: ...
   - Sprint context: {{sprint_slug}}
   - Role: ...
   - Guidelines: ...
```

Change to spawn `agents/dev.md` via Agent tool with the same parameters. The
completion output contract stays identical — sprint-dev Phase 3 does not need
changes beyond the spawn mechanism.

### What NOT to change

- **momentum:dev skill** (`skills/momentum/skills/dev/SKILL.md` and `workflow.md`)
  — stays intact for direct `/momentum:dev` invocation
- **bmad-dev-story skill** — the dev agent delegates to it, does not replace it
- **Sprint-dev Phases 3–7** — completion handling, AVFL, team review, verification,
  and sprint completion are unaffected

### Requirements Coverage

- Architecture Decision 26: Two-Layer Agent Model (agents are lightweight
  definitions, skills are heavy workflows)
- Architecture Decision 25: Teams Over Waves (dev agents are team members spawned
  by sprint-dev)
- Master Plan: agents/ directory holds agent definition files

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before agent creation)
  - [ ] Create `skills/momentum/agents/evals/eval-dev-agent-receives-story.md`
    — verifies the agent accepts story file path and sprint context as input
  - [ ] Create `skills/momentum/agents/evals/eval-dev-agent-delegates-to-bmad.md`
    — verifies the agent delegates implementation to bmad-dev-story
  - [ ] Create `skills/momentum/agents/evals/eval-dev-agent-completion-output.md`
    — verifies the agent returns structured completion output matching Decision 3b

- [ ] Task 2 — Create `agents/dev.md` agent definition (AC: 1, 2, 3, 6, 7)
  - [ ] Write frontmatter: name, description, model (sonnet), effort (medium),
    tools (Read, Glob, Grep, Bash, Edit, Write, Agent)
  - [ ] Write role description and critical constraints
  - [ ] Write input format section
  - [ ] Write implementation process (delegate to bmad-dev-story)
  - [ ] Write output format (structured JSON completion signal)

- [ ] Task 3 — Update sprint-dev Phase 2 spawn mechanism (AC: 4)
  - [ ] Replace `momentum:dev` skill invocation with Agent tool spawning
    `agents/dev.md`
  - [ ] Pass story file path, sprint slug, role, and guidelines as agent input
  - [ ] Verify completion output format compatibility with Phase 3 handling

- [ ] Task 4 — Run evals and verify non-regression (AC: 5)
  - [ ] Run each eval via subagent
  - [ ] Confirm `/momentum:dev` still works for direct invocation (read SKILL.md,
    verify no modifications)

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → config-structure (EDD — evals for agent definition)
- Task 2 → config-structure (agent definition file follows qa-reviewer pattern)
- Task 3 → skill-instruction (modifying sprint-dev workflow)
- Task 4 → config-structure (eval execution)

---

### config-structure Tasks: Eval-Driven Development (EDD)

**Before writing the agent definition:**
1. Write 3 behavioral evals in `skills/momentum/agents/evals/`:
   - One per eval above, testing input acceptance, delegation, and output format
   - Format: "Given [input/context], the agent should [observable behavior]"

**Then implement:**
2. Write `agents/dev.md` following the qa-reviewer.md and e2e-validator.md pattern

**Then verify:**
3. Run evals via subagent, confirm behaviors match

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before modifying sprint-dev workflow:**
1. Document current spawn behavior (Phase 2 step 2, action 3)

**Then implement:**
2. Replace momentum:dev skill spawn with Agent tool spawn of agents/dev.md
3. Ensure input parameters match the agent's expected input format

**Then verify:**
4. Confirm sprint-dev Phase 3 completion handling is compatible with new agent
   output format (it should be — the output contract is identical)

**NFR compliance:**
- Agent definition file should be concise — under 150 lines (qa-reviewer is 103,
  e2e-validator is 105)
- Frontmatter `description` must be <= 150 characters
- `model:` and `effort:` frontmatter must be present

**DoD items:**
- [ ] 3 behavioral evals written
- [ ] EDD cycle ran — all eval behaviors confirmed
- [ ] Agent definition frontmatter complete (name, description, model, effort, tools)
- [ ] Agent definition body under 150 lines
- [ ] Sprint-dev Phase 2 updated to spawn agents/dev.md
- [ ] momentum:dev skill unmodified (non-regression)
- [ ] Structured completion output matches Decision 3b contract

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
